# Results map

Main Fig. 1 is a methods/map schematic; station coordinates and areas are in the
canonical weather/case records. Cartographic artwork is outside numerical scope.
Main Fig. 2 uses static and A-relative PV distributions/landscapes. Fig. 3 uses
heating versus all-other-end-use cost balance and matched B/C. Fig. 4 uses native
electricity versus gas/oil components. Fig. 5 uses positive-value threshold counts,
hypothetical winter-mask counts, and six optical-state distributions.
SI Tables S1–S3 have station/area, prescribed roof-law and frozen-price backing;
Table S4 uses illustrative bills/service plus Denver width records, and Table S5
uses the six optical-state summaries. SI Figs S1–S4 use Seattle costs, the 54 width
comparisons and the two native day traces. Textual methods and full paper prose are
not reproduced here. Historical column names containing `allowance` or `headroom`
are retained as schema identifiers; their values mean signed PV HVAC-cost
differences, not guaranteed profitability or a service-life measurement.

| Public frozen input | Rows | Expected key | Figure/table/claim |
|---|---:|---|---|
| `data/processed/canonical/case_reality_216.csv` | 216 | `family,roof` | Main 2; SI S1/S5/S6: 216 annual identities, areas, bills, warnings |
| `data/processed/canonical/pair_rebilling_108.csv` | 108 | `family,pair` | Main 2/3/5A; 108 signed A-minus-B/C comparisons |
| `data/processed/canonical/static_54.csv` | 54 | `family` | Main 2A: static 0-minus-A context |
| `data/processed/canonical/monthly_native_rebilling.csv` | 7776 | `family,roof,month,carrier` | Main 4/5B; SI S3/S7: native carrier rebilling and winter mask |
| `data/processed/canonical/family_carrier_price_162.csv` | 162 | `family,carrier` | Main 4; SI Table S3: frozen sector/carrier prices |
| `data/processed/canonical/weather_prototype_54.csv` | 54 | `family` | Main 1 anchors; SI Table S1: stations/prototype identifiers |
| `data/processed/canonical/numerical_and_service_216.csv` | 216 | `family,roof` | SI S6; separate occupied heating/cooling service and numerical limitations |
| `data/processed/canonical/price_40_means.csv` | 40 | `see header` | SI Table S3; frozen price means and source identifiers |
| `data/processed/economics/native_carrier_coefficients_108.csv` | 108 | `family,target_roof` | Main 3/4: seven end uses and three purchased carriers |
| `data/processed/economics/native_price_break_even_boundaries_108.csv` | 324 | `family,target_roof,carrier` | SI S7: 324 analytic boundary entries |
| `data/processed/economics/native_PV_headroom_108x5.csv` | 540 | `family,target_roof,setting` | SI S7: 540 financial accounting rows |
| `data/processed/economics/winter_availability_native_60x4.csv` | 240 | `family,target_roof,retained_function_fraction` | Main 5B; SI S7: 240 common-mask accounting rows |
| `data/processed/width/matched_54_width_comparisons.csv` | 54 | `family` | SI S5/Fig S2: 54 separate near-sharp B comparisons |
| `data/processed/width/illustrative_native_cases.csv` | 10 | `family,roof` | SI Table S4: Seattle/Chicago 0/A/B/C/Bsharp examples |
| `data/processed/width/native_day_traces.csv` | 288 | `family,native_TimeIndex` | SI Figs S3/S4: 288 native ten-minute trace records |
| `data/processed/width/sharp_native_enduse_costs.csv` | 5670 | `family,roof,end_use,carrier` | SI Fig S1 and Table S4; 5670 native annual costs |
| `data/processed/optical/matched_optical_comparisons_108.csv` | 108 | `family,condition` | Main 5C; SI S8/Table S5: separate 108 optical contrasts |
| `data/processed/optical/descriptive_summary.csv` | 6 | `condition` | Main 5C; SI Table S5: six states, 18 families each |
| `data/processed/optical/native_enduse_costs.csv` | 3024 | `family,variant,end_use,carrier` | SI S8: native optical carrier/end-use closure |
| `data/processed/optical/native_monthly_carriers.csv` | 5184 | `family,variant,carrier,month` | SI S8: native optical rebilling |
| `data/processed/optical/service_numerical.csv` | 144 | `family,variant` | SI S8: optical baseline/new-year qualifications |
