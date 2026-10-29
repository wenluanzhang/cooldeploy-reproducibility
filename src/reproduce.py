"""Reproduce R1 numerical tables from frozen processed outputs; no simulations."""
from __future__ import annotations
import argparse
from collections import defaultdict
import csv
import hashlib
import itertools
import json
import math
from pathlib import Path
import statistics

from _economics import build, annuity, CITIES, CONFIGS, USES, CARRIERS, FILES

ROOT = Path(__file__).resolve().parents[1]


def require(ok, message):
    if not ok:
        raise ValueError(message)


def read(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def write(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def index(rows, keys):
    result = {tuple(r[k] for k in keys): r for r in rows}
    require(len(result)==len(rows), 'Duplicate key: '+','.join(keys))
    return result


def close(x, y, tol=1e-7):
    require(math.isfinite(float(x)) and math.isfinite(float(y)) and abs(float(x)-float(y))<=tol,
            f'Numeric closure: {x} != {y} (tolerance {tol})')


def load(root=ROOT):
    data={}
    for path in sorted((root/'data/processed').glob('*/*.csv')):
        require(path.stem not in data, 'Ambiguous input basename: '+path.stem)
        data[path.stem]=read(path)
    return data


def quantile(values, q):
    values=sorted(values);position=(len(values)-1)*q
    i=math.floor(position);j=math.ceil(position)
    return values[i]+(values[j]-values[i])*(position-i)


def optical_summary(data):
    result=[]
    for state in ('E_LOW_035','E_LOW_050','C_ONLY_R070','C_ONLY_R065','PAIRED_R070_090','PAIRED_R065_085'):
        group=[r for r in data['matched_optical_comparisons_108'] if r['condition']==state]
        v=[float(r['delta_P_USD_m2']) for r in group]
        result.append(dict(condition=state,n_families=len(group),minimum=min(v),q25=quantile(v,.25),
                           median=statistics.median(v),q75=quantile(v,.75),maximum=max(v),
                           positive_changes=sum(x>0 for x in v),negative_changes=sum(x<0 for x in v),
                           A_relative_sign_flips=sum(r['A_relative_sign_flip']=='True' for r in group)))
    return result


def validate(root=ROOT):
    pins=json.loads((root/'docs/FROZEN_INPUTS.json').read_text(encoding='utf-8'))
    for item in pins:
        path=root/item['public_path']
        require(hashlib.sha256(path.read_bytes()).hexdigest()==item['public_sha256'], 'Frozen hash changed: '+item['public_path'])
        if 'rows' in item:
            require(len(read(path))==item['rows'],'Frozen row count changed: '+item['public_path'])
    data=load(root)
    families={c+'/'+b for c,b in itertools.product(CITIES,CONFIGS)}
    cases=index(data['case_reality_216'],('family','roof'))
    service=index(data['numerical_and_service_216'],('family','roof'))
    pairs=index(data['pair_rebilling_108'],('family','pair'))
    require(set(cases)==set(service)==set(itertools.product(families,'0ABC')),'216 canonical case/service keys')
    require(set(pairs)==set(itertools.product(families,('A-B','A-C'))),'108 canonical pair keys')
    require(all(float(r['annual_hours'])==8760 for r in cases.values()),'Incomplete canonical annual')
    require(sum(r['numerical']=='NUMERICAL_REVIEW_REQUIRED' for r in cases.values())==93,'93 numerical review annuals')
    monthly=index(data['monthly_native_rebilling'],('family','roof','month','carrier'))
    prices=index(data['family_carrier_price_162'],('family','carrier'))
    require(set(monthly)==set(itertools.product(families,'0ABC',map(str,range(1,13)),CARRIERS.values())), '7776 monthly native keys')
    require(set(prices)==set(itertools.product(families,CARRIERS.values())),'162 native price keys')
    bills=defaultdict(float)
    for (f,r,m,k),row in monthly.items():
        p=prices[f,k];rate=float(p['frozen_price'] or 0);e=float(row['purchased_kWh'])
        require(e>=0 and math.isfinite(e),'Invalid purchased carrier')
        require(bool(p['frozen_price']) or e==0,'Missing price on nonzero carrier')
        require(p['sector']==('residential' if '/SingleFamily/' in f else 'commercial'),'Price sector mismatch')
        close(row['price_USD_kWh'] or 0,rate,0);close(row['cost_USD'],rate*e)
        bills[f,r]+=rate*e
    for key,r in cases.items():
        close(bills[key],r['bill_USD'])
        require(float(r['roof_area_m2'])>0,'Invalid physical area')
    static=index(data['static_54'],('family',))
    require(set(static)=={(f,) for f in families},'54 static context keys')
    for f in families:
        saving=bills[f,'0']-bills[f,'A'];close(saving,static[f,]['saving_0_minus_A_USD'])
        close(annuity(20,.05)*saving/float(cases[f,'A']['roof_area_m2']),static[f,]['allowance_0_minus_A_USD_m2'],1e-9)
    for (f,pair),r in pairs.items():
        close(bills[f,'A']-bills[f,pair[-1]],r['saving_USD'])
        close(sum(float(r[u+'_saving_USD']) for u in USES),r['saving_USD'])
        close(annuity(20,.05)*float(r['saving_USD'])/float(r['roof_area_m2']),r['allowance_USD_m2'],1e-9)
        require(float(r['Cooling_saving_USD'])<0,'Cooling contribution must remain adverse')
        for label,roof in [('A','A'),('target',pair[-1])]:
            require(r['numerical_'+label]==service[f,roof]['numerical'],'Pair numerical qualifier')
        for mode in ('heating','cooling'):
            close(float(service[f,pair[-1]]['occupied_'+mode+'_unmet'])-float(service[f,'A']['occupied_'+mode+'_unmet']), r['occupied_'+mode+'_unmet_delta'])
    counts={roof:sum(float(r['saving_USD'])>0 for (f,p),r in pairs.items() if p=='A-'+roof) for roof in 'BC'}
    require(counts=={'B':43,'C':41},'43/54 B and 41/54 C')
    cheaper=sum(float(pairs[f,'A-B']['saving_USD'])>float(pairs[f,'A-C']['saving_USD']) for f in families)
    require(cheaper==50,'B cheaper than C in 50/54')
    medians={j:statistics.median(float(r['allowance_USD_m2']) for (f,p),r in pairs.items() if p=='A-'+j) for j in 'BC'}
    close(medians['B'],1.4125274257,1e-10);close(medians['C'],.6858116473,1e-10)
    derived=build(data)
    keys={'coefficients':('family','target_roof'),'boundaries':('family','target_roof','carrier'),
          'financial':('family','target_roof','setting'),'winter':('family','target_roof','retained_function_fraction')}
    for name,filename in FILES.items():
        frozen=data[Path(filename).stem]
        require(len(derived[name])==len(frozen),'Derived row count: '+name)
        for actual,expected in zip(derived[name],frozen):
            # Frozen order is part of the pinned snapshot. Numeric values are
            # checked across every retained column, including qualifications.
            for field,value in expected.items():
                current=actual[field]
                if str(current)==str(value):continue
                try:float(value);float(current)
                except (ValueError,TypeError):require(False,f'{name}: {field}: qualifier differs')
                close(current,value,1e-9 if 'USD_m2' in field else 1e-7)
    winter=derived['winter']
    for roof,expected in [('B',[29,29,28,23]),('C',[30,29,24,19])]:
        for a,n in zip((1,.75,.5,.25),expected):
            group=[r for r in winter if r['target_roof']==roof and r['retained_function_fraction']==a]
            require(len(group)==30 and sum(r['masked_allowance_USD_m2']>0 for r in group)==n,'Winter counts')
    require(all(r['cold_season_signed_USD_year']>0 for r in winter),'60 adverse winter-mask effects')
    width=data['matched_54_width_comparisons']
    require(set(index(width,('family',)))=={(f,) for f in families},'54 width keys')
    require(sum(r['A_relative_sign_flip']=='True' for r in width)==0,'Width A-relative signs')
    require(sum(r['B_C_ranking_reversal']=='True' for r in width)==1,'One width B/C reversal')
    for r in width:
        f=r['family'];close(r['C_A_USD_year'],bills[f,'A']);close(r['P_Bbroad_USD_m2'],pairs[f,'A-B']['allowance_USD_m2'],1e-9)
        close(float(r['P_Bsharp_USD_m2'])-float(r['P_Bbroad_USD_m2']),r['sharp_minus_broad_USD_m2'],1e-9)
    width_by=index(width,('family',))
    enduses=index(data['sharp_native_enduse_costs'],('family','roof','end_use','carrier'))
    require(set(enduses)==set(itertools.product(families,('0','A','B','C','Bsharp'),USES,CARRIERS.values())),'5670 width native end-use keys')
    for f,roof in itertools.product(families,('0','A','B','C','Bsharp')):
        total=sum(float(enduses[f,roof,u,k]['native_cost_USD_year']) for u,k in itertools.product(USES,CARRIERS.values()))
        close(total,width_by[f,]['C_Bsharp_USD_year'] if roof=='Bsharp' else bills[f,roof])
    traces=data['native_day_traces']
    require(len(index(traces,('family','native_TimeIndex')))==288,'288 trace keys')
    require({r['family'] for r in traces}=={'Seattle/MediumOffice/official_native','Chicago/MediumOffice/official_native'},'Two SI trace families')
    for f in {r['family'] for r in traces}:
        require(sum(r['family']==f for r in traces)==144,'144 native steps per trace')
    for r in data['illustrative_native_cases']:
        f,roof=r['family'],r['roof']
        close(r['annual_purchased_HVAC_USD'],width_by[f,]['C_Bsharp_USD_year'] if roof=='Bsharp' else bills[f,roof])
        for mode in ('heating','cooling'):
            close(r['occupied_'+mode+'_unmet_h'],width_by[f,][roof+'_occupied_'+mode+'_unmet_h'])
    optical=data['matched_optical_comparisons_108'];index(optical,('family','condition'))
    require(len(optical)==108,'108 separate optical comparisons')
    native=defaultdict(float)
    for r in data['native_enduse_costs']:
        native[r['family'],r['variant']]+=float(r['annual_cost_USD'])
    optical_service=index(data['service_numerical'],('family','variant'))
    require(len(optical_service)==144,'144 contextual optical case qualifications')
    optical_months=index(data['native_monthly_carriers'],('family','variant','carrier','month'))
    require(len(optical_months)==5184,'5184 contextual optical monthly keys')
    optical_bills=defaultdict(float)
    for (f,v,k,m),r in optical_months.items():
        close(float(r['purchased_HVAC_kWh'])*float(r['price_USD_kWh'] or 0),r['cost_USD'])
        close(r['price_USD_kWh'] or 0,prices[f,k]['frozen_price'] or 0,0)
        optical_bills[f,v]+=float(r['cost_USD'])
    require(set(optical_bills)==set(native)==set(optical_service),'Optical native/service variant keys')
    for key,value in native.items():close(value,optical_bills[key])
    for r in optical:
        f=r['family'];close(r['baseline_CA_USD_year'],bills[f,'A']);close(r['baseline_CC_USD_year'],bills[f,'C'])
        close(r['CA_prime_USD_year'],native[f,r['A_variant']]);close(r['CC_prime_USD_year'],native[f,r['C_variant']])
        p=annuity(20,.05)*(float(r['CA_prime_USD_year'])-float(r['CC_prime_USD_year']))/float(r['physical_roof_area_m2'])
        close(p,r['P_prime_USD_m2'],1e-9);close(p-float(r['baseline_P_USD_m2']),r['delta_P_USD_m2'],1e-9)
        close(sum(float(r['A_minus_C_prime_'+u+'_USD_year']) for u in USES),r['A_minus_C_prime_USD_year'])
        require(r['numerical_A']==optical_service[f,r['A_variant']]['numerical'],'Optical A numerical qualifier')
        require(r['numerical_C']==optical_service[f,r['C_variant']]['numerical'],'Optical C numerical qualifier')
    summaries=optical_summary(data)
    expected=index(data['descriptive_summary'],('condition',))
    for r in summaries:
        require(r['n_families']==18,'18 optical families per state')
        state_rows=[x for x in optical if x['condition']==r['condition']]
        require({x['family'] for x in state_rows}=={c+'/'+b for c,b in itertools.product(('Denver','Chicago','Minneapolis'),CONFIGS)},'Exact 18 optical families')
        for k,v in r.items():
            if k!='condition':close(v,expected[r['condition'],][k],1e-9)
    for state in ('E_LOW_035','E_LOW_050'):
        require(expected[state,]['negative_changes']=='18','All 18 emittance effects adverse')
    expected_plots=json.loads((root/'data/processed/expected_main_plot_values.json').read_text())
    for r in expected_plots['figure2']['landscape']:
        close(r['value'],pairs[r['family'],'A-'+r['target']]['allowance_USD_m2'],1e-9)
    for label,distribution in expected_plots['figure2']['distributions'].items():
        for f,v in zip(distribution['families'],distribution['values']):
            close(v,static[f,]['allowance_0_minus_A_USD_m2'] if label=='A' else pairs[f,'A-'+label]['allowance_USD_m2'],1e-9)
    coefficients=index(derived['coefficients'],('family','target_roof'))
    for r in expected_plots['figure3']['balance']:
        co=coefficients[r['family'],r['target']]
        close(r['x'],-sum(co[u+'_PV_contribution_USD_m2'] for u in USES if u!='Heating'),1e-9)
        close(r['y'],co['Heating_PV_contribution_USD_m2'],1e-9)
    for r in expected_plots['figure3']['matched']:
        for j in 'BC':close(r[j],pairs[r['family'],'A-'+j]['allowance_USD_m2'],1e-9)
    for r in expected_plots['figure4']['carrier_balance']:
        co=coefficients[r['family'],r['target']];factor=float(co['PV_ref'])/float(co['roof_area_m2'])
        close(r['x'],-co['D_electricity_USD_year']*factor,1e-9)
        close(r['y'],(co['D_natural_gas_USD_year']+co['D_fuel_oil_no2_USD_year'])*factor,1e-9)
    positives=[float(r['allowance_USD_m2']) for r in pairs.values() if float(r['allowance_USD_m2'])>0]
    thresholds=[0]+sorted(set(positives))
    require(thresholds==expected_plots['figure5']['headroom_thresholds'],'Fig 5A thresholds')
    require([sum(v>t for v in positives) for t in thresholds]==expected_plots['figure5']['headroom_counts'],'Fig 5A counts')
    for r in expected_plots['figure5']['availability']:
        group=[w for w in winter if w['city']==r['city'] and w['target_roof']==r['target'] and w['retained_function_fraction']==r['a']]
        require(sum(w['masked_allowance_USD_m2']>0 for w in group)==r['positive'],'Fig 5B per-city counts')
    report=dict(status='PASS',canonical_annuals=216,canonical_pairs=108,numerical_review_annuals=93,
                B_positive=43,C_positive=41,B_cheaper_than_C=cheaper,signed_medians_USD_m2=medians,
                adverse_cooling_components=108,winter_rows=240,width_pairs=54,optical_pairs=108,optical_states=6,
                closure='frozen hashes; monthly carrier/price/bill; seven end uses; area/PV; finance; winter; accepted Main plot values; optical native costs/statistics',
                limits='fixed equipment does not establish equal service; no annual numerical error bound; processed-output reproduction only')
    return data,derived,report


def tables(root=ROOT):
    data,derived,report=validate(root)
    result={Path(FILES[k]).stem:v for k,v in derived.items()}
    pairs=data['pair_rebilling_108'];co=derived['coefficients']
    result['main_figure2_static']=data['static_54']
    result['main_figure2_landscape']=pairs
    result['main_figure3_balance']=[dict(family=r['family'],target=r['target_roof'],
        x=-sum(r[u+'_PV_contribution_USD_m2'] for u in USES if u!='Heating'),y=r['Heating_PV_contribution_USD_m2']) for r in co]
    by=index(pairs,('family','pair'))
    result['main_figure3_matched']=[dict(family=f,B=by[f,'A-B']['allowance_USD_m2'],C=by[f,'A-C']['allowance_USD_m2']) for f in sorted({r['family'] for r in pairs})]
    result['main_figure4_carriers']=[dict(family=r['family'],target=r['target_roof'],
        x=-r['D_electricity_USD_year']*float(r['PV_ref'])/float(r['roof_area_m2']),
        y=(r['D_natural_gas_USD_year']+r['D_fuel_oil_no2_USD_year'])*float(r['PV_ref'])/float(r['roof_area_m2'])) for r in co]
    positive=[float(r['allowance_USD_m2']) for r in pairs if float(r['allowance_USD_m2'])>0]
    result['main_figure5a_thresholds']=[dict(threshold_USD_m2=t,positive_count=sum(v>t for v in positive)) for t in [0]+sorted(set(positive))]
    winter=derived['winter']
    result['main_figure5b_winter_counts']=[dict(city=c,target=j,retained_function_fraction=a,positive_count=sum(r['masked_allowance_USD_m2']>0 for r in winter if r['city']==c and r['target_roof']==j and r['retained_function_fraction']==a),denominator=6) for c,j,a in itertools.product(('Denver','Chicago','Minneapolis','InternationalFalls','Fairbanks'),'BC',(1.,.75,.5,.25))]
    result['main_figure5c_optical_and_SI_tableS5']=optical_summary(data)
    result['SI_tableS1_stations_areas']=[]
    cases=index(data['case_reality_216'],('family','roof'))
    for r in data['weather_prototype_54']:
        station=json.loads(r['EPW_station'])
        result['SI_tableS1_stations_areas'].append(dict(family=r['family'],station=station[0],TMY3_ID=station[4],latitude=station[5],longitude=station[6],physical_roof_area_m2=cases[r['family'],'A']['roof_area_m2']))
    result['SI_tableS2_roof_laws']=[dict(roof='0',reflectance='native',emittance='native'),dict(roof='A',reflectance='0.95',emittance='0.95'),dict(roof='B',reflectance='0.05+0.90*f',emittance='0.10+0.85*f'),dict(roof='C',reflectance='0.75',emittance='0.20+0.70*f')]
    result['SI_tableS3_prices']=data['family_carrier_price_162']
    width=index(data['matched_54_width_comparisons'],('family',))
    result['SI_tableS4_illustrative']=[]
    for city,roof in itertools.product(('Seattle','Chicago','Denver'),('0','A','B','C','Bsharp')):
        r=width[city+'/MediumOffice/official_native',]
        field={'0':'C_0_USD_year','A':'C_A_USD_year','B':'C_Bbroad_USD_year','C':'C_C_USD_year','Bsharp':'C_Bsharp_USD_year'}[roof]
        result['SI_tableS4_illustrative'].append(dict(city=city,roof=roof,bill_USD_year=r[field],occupied_heating_unmet_h=r[roof+'_occupied_heating_unmet_h'],occupied_cooling_unmet_h=r[roof+'_occupied_cooling_unmet_h'],numerical=r[roof+'_numerical']))
    for output,input_name in [('SI_figureS1_native_costs','sharp_native_enduse_costs'),('SI_figureS2_width','matched_54_width_comparisons'),('SI_figuresS3_S4_native_traces','native_day_traces')]:
        result[output]=data[input_name]
    return result,report


def output_directory(path, root=ROOT):
    p=Path(path).resolve()
    protected=[root/'data',root/'src',root/'docs',root/'tests']
    require(p!=root.resolve() and not any(p==x.resolve() or x.resolve() in p.parents for x in protected),'Output must be outside frozen inputs and source/docs/tests')
    return p


def figures(output):
    # Numerical reference views, intentionally independent of approved artwork.
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    for number,name in [(2,'main_figure2_landscape'),(3,'main_figure3_balance'),(4,'main_figure4_carriers'),(5,'main_figure5c_optical_and_SI_tableS5')]:
        records=read(output/(name+'.csv'));fig,ax=plt.subplots(figsize=(7,4))
        if number==2:
            for target in ('A-B','A-C'):
                v=sorted(float(r['allowance_USD_m2']) for r in records if r['pair']==target)
                ax.plot(range(len(v)),v,label=target)
            ax.set(xlabel='Sorted family index',ylabel='Signed 20-year PV USD/m² roof');ax.legend()
        elif number in (3,4):
            for target in 'BC':
                rs=[r for r in records if r['target']==target];ax.scatter([float(r['x']) for r in rs],[float(r['y']) for r in rs],label=target,s=12)
            ax.set(xlabel='Signed cost penalty (PV USD/m² roof)',ylabel='Signed cost benefit (PV USD/m² roof)');ax.legend()
        else:
            ax.barh([r['condition'] for r in records],[float(r['median']) for r in records]);ax.set(xlabel='Median change in A-minus-C PV USD/m² roof')
        ax.axhline(0,color='gray',lw=.5);fig.tight_layout();fig.savefig(output/f'numerical_figure{number}.png',dpi=150);plt.close(fig)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['validate','tables','figures'])
    parser.add_argument('--output',default='generated')
    args=parser.parse_args()
    if args.command=='validate':
        _,_,report=validate()
    else:
        output=output_directory(args.output);outputs,report=tables()
        for name,records in outputs.items():write(output/(name+'.csv'),records)
        (output/'validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
        if args.command=='figures':figures(output)
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
