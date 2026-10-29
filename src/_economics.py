"""Frozen native-carrier economic algebra, isolated from its original CLI."""

import itertools
import math
from pathlib import Path

CAN = Path("data/processed/canonical")

CITIES = ("Miami", "Phoenix", "Baltimore", "Seattle", "Denver", "Chicago",
          "Minneapolis", "InternationalFalls", "Fairbanks")

WINTER_CITIES = ("Denver", "Chicago", "Minneapolis", "InternationalFalls", "Fairbanks")

CONFIGS = ("MediumOffice/official_native", "SmallOffice/official_native",
           "SingleFamily/gasfurnace", "SingleFamily/hp",
           "SingleFamily/elecres", "SingleFamily/oilfurnace")

TAGS = ("MO", "SO", "SF-G", "SF-HP", "SF-E", "SF-O")

CARRIERS = {"electricity": "Electricity", "natural_gas": "NaturalGas",
            "fuel_oil_no2": "FuelOilNo2"}

USES = ("Heating", "Cooling", "Fans", "Pumps", "HeatRejection", "Humidification", "HeatRecovery")

MONTHS = (11, 12, 1, 2, 3)

FRACTIONS = (1.0, .75, .5, .25)

SETTINGS = (("reference", 20, .05), ("horizon_10", 10, .05), ("horizon_30", 30, .05),
            ("discount_02", 20, .02), ("discount_08", 20, .08))

FILES = {
    "coefficients": "native_carrier_coefficients_108.csv",
    "boundaries": "native_price_break_even_boundaries_108.csv",  # 324 long rows.
    "financial": "native_PV_headroom_108x5.csv",
    "winter": "winter_availability_native_60x4.csv",
}

MASK_WARNING = (
    "Hypothetical cold-season roof-availability accounting sensitivity; not measured snow "
    "fractions or a physical snow/roof/HVAC response. The common masked fraction has zero "
    "A-minus-target difference; service and numerical qualifications are unchanged."
)

def annuity(n, r):
    return n if r == 0 else (1 - (1 + r) ** (-n)) / r

def indexed(rows, fields):
    result = {tuple(r[k] for k in fields): r for r in rows}
    if len(result) != len(rows):
        raise ValueError(f"Duplicate compact source key: {fields}")
    return result

def boundary(ds, carrier):
    d = ds[carrier]
    other = math.fsum(v for k, v in ds.items() if k != carrier)
    if d == 0:
        return other, "", False, False, "UNDEFINED_ZERO_D"
    critical = -other / d
    return (other, critical, True, critical > 0,
            "POSITIVE_PRICE_BOUNDARY" if critical > 0 else "NO_POSITIVE_PRICE_CROSSING")

def build(data):
    pairs = indexed(data["pair_rebilling_108"], ("family", "pair"))
    services = indexed(data["numerical_and_service_216"], ("family", "roof"))
    cases = indexed(data["case_reality_216"], ("family", "roof"))
    prices = indexed(data["family_carrier_price_162"], ("family", "carrier"))
    monthly = indexed(data["monthly_native_rebilling"], ("family", "roof", "month", "carrier"))
    result = {k: [] for k in FILES}
    f_ref = annuity(20, .05)
    for city, config, target in itertools.product(CITIES, CONFIGS, ("B", "C")):
        family = city + "/" + config
        pair = pairs[family, "A-" + target]
        area, accepted = float(pair["roof_area_m2"]), float(pair["saving_USD"])
        accepted_p = float(pair["allowance_USD_m2"])
        sa, st = services[family, "A"], services[family, target]
        identity = dict(family=family, city=city, native_configuration=config,
                        native_branch_tag=TAGS[CONFIGS.index(config)], reference_roof="A", target_roof=target)
        qualifiers = dict(
            numerical_A=sa["numerical"], numerical_target=st["numerical"],
            numerical_error_bound_A=cases[family, "A"]["numerical_error_bound"],
            numerical_error_bound_target=cases[family, target]["numerical_error_bound"],
            occupied_heating_unmet_A_hours=sa["occupied_heating_unmet"],
            occupied_heating_unmet_target_hours=st["occupied_heating_unmet"],
            occupied_cooling_unmet_A_hours=sa["occupied_cooling_unmet"],
            occupied_cooling_unmet_target_hours=st["occupied_cooling_unmet"],
            occupied_heating_unmet_delta=pair["occupied_heating_unmet_delta"],
            occupied_cooling_unmet_delta=pair["occupied_cooling_unmet_delta"],
            service_equivalence="NOT_ESTABLISHED",
            installed_reference_policy=cases[family, "A"]["policy"])
        row = dict(**identity, roof_area_m2=pair["roof_area_m2"], PV_ref=pair["PV"],
                   accepted_delta_C_ref_USD_year=pair["saving_USD"],
                   accepted_allowance_USD_m2=pair["allowance_USD_m2"])
        ds = {}
        for slug, carrier in CARRIERS.items():
            price = prices[family, carrier]
            ea = math.fsum(float(monthly[family, "A", str(m), carrier]["purchased_kWh"]) for m in range(1, 13))
            et = math.fsum(float(monthly[family, target, str(m), carrier]["purchased_kWh"]) for m in range(1, 13))
            de = math.fsum(float(monthly[family, "A", str(m), carrier]["purchased_kWh"])
                           - float(monthly[family, target, str(m), carrier]["purchased_kWh"]) for m in range(1, 13))
            if not price["frozen_price"] and (ea != 0 or et != 0):
                raise ValueError(f"HOLD missing rate for nonzero native carrier: {family}/{target}/{carrier}")
            ds[slug] = float(price["frozen_price"]) * de if price["frozen_price"] else 0.0
            row.update({
                f"E_A_{slug}_kWh_year": ea, f"E_target_{slug}_kWh_year": et,
                f"delta_E_{slug}_kWh_year": de, f"p0_{slug}_USD_kWh": price["frozen_price"],
                f"D_{slug}_USD_year": ds[slug],
                f"carrier_evidence_{slug}": ("BOTH_NATIVE_ANNUALS_ZERO" if ea == 0 and et == 0
                                           else "NATIVE_PURCHASED_CHANNEL_PRESENT"),
                f"price_sector_{slug}": price["sector"],
                f"price_window_start_{slug}": price["window_start"],
                f"price_window_end_{slug}": price["window_end"],
                f"price_geography_{slug}": price["geography"], f"price_proxy_{slug}": price["proxy"]})
        row["delta_C_from_carriers_USD_year"] = math.fsum(ds.values())
        row["allowance_from_carriers_USD_m2"] = f_ref * math.fsum(ds.values()) / area
        for use in USES:
            row[use + "_saving_USD"] = pair[use + "_saving_USD"]
            row[use + "_PV_contribution_USD_m2"] = f_ref * float(pair[use + "_saving_USD"]) / area
        row.update(qualifiers)
        row["pair_source"] = (CAN / "pair_rebilling_108.csv").as_posix()
        row["monthly_source"] = (CAN / "monthly_native_rebilling.csv").as_posix()
        result["coefficients"].append(row)
        for slug, carrier in CARRIERS.items():
            other, critical, defined, positive, state = boundary(ds, slug)
            result["boundaries"].append(dict(
                **identity, carrier=carrier, carrier_slug=slug, D_q_USD_year=ds[slug],
                other_carriers_at_1_USD_year=other, lambda_star=critical,
                boundary_defined=defined, positive_price_crossing=positive, boundary_status=state,
                slope_USD_m2_per_multiplier=f_ref * ds[slug] / area,
                other_carrier_multipliers=1, multiplier_domain="STRICTLY_POSITIVE_UNBOUNDED_ANALYTIC_ONLY",
                roof_area_m2=pair["roof_area_m2"], PV_ref=pair["PV"], **qualifiers))
        for setting, n, r in SETTINGS:
            factor = annuity(n, r)
            p = factor * accepted / area
            result["financial"].append(dict(
                **identity, setting=setting, horizon_years=n, real_discount_rate=r, PV=factor,
                roof_area_m2=pair["roof_area_m2"], delta_C_ref_USD_year=pair["saving_USD"],
                allowance_USD_m2=p, reference_allowance_USD_m2=pair["allowance_USD_m2"],
                change_from_reference_USD_m2=p - accepted_p,
                signed_headroom_before_incremental_service_USD_m2=p, accounting_only=True, **qualifiers))
        if city in WINTER_CITIES:
            differences = {m: math.fsum(
                float(monthly[family, "A", str(m), k]["cost_USD"])
                - float(monthly[family, target, str(m), k]["cost_USD"]) for k in CARRIERS.values())
                for m in range(1, 13)}
            cold = math.fsum(differences[m] for m in MONTHS)
            noncold = math.fsum(v for m, v in differences.items() if m not in MONTHS)
            baseline = f_ref * (noncold + cold) / area
            for a in FRACTIONS:
                masked = noncold + a * cold
                p = f_ref * masked / area
                result["winter"].append(dict(
                    **identity, retained_function_fraction=a, delta_C_ref_USD_year=pair["saving_USD"],
                    full_year_unmasked_monthly_USD_year=math.fsum(differences.values()),
                    cold_season_signed_USD_year=cold, non_cold_season_signed_USD_year=noncold,
                    masked_annual_signed_USD_year=masked, PV=f_ref, roof_area_m2=pair["roof_area_m2"],
                    masked_allowance_USD_m2=p, reference_allowance_USD_m2=pair["allowance_USD_m2"],
                    change_from_a1_USD_m2=p - baseline,
                    change_from_accepted_reference_USD_m2=p - accepted_p,
                    cold_season_months="11;12;1;2;3", hypothetical_mask_accounting_only=True,
                    mask_warning=MASK_WARNING, **qualifiers))
    return result
