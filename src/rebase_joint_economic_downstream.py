"""Rebase deployment sensitivities to the canonical reference economics.

This module reads frozen monthly physical outputs and applies only the current
load-to-purchased-energy, price, and present-value conventions. It never
invokes EnergyPlus or modifies physical simulation outputs.
"""

from pathlib import Path

import numpy as np
import pandas as pd

import frozen_physical_inputs as physical_archive


ROOT = Path(__file__).resolve().parents[1]
JOINT = ROOT / "data" / "processed" / "joint_economic_robustness"
SOURCE = JOINT / "central_baseline_base_price.csv"
PRICE_SOURCE = JOINT / "price_levels.csv"
OPTICAL_PHYSICAL_SOURCE = ROOT / "data" / "processed" / "frozen_physical_inputs" / "phase3b_monthly_physical_results.csv"
OUT = ROOT / "data" / "processed" / "joint_economic_downstream"
PERIODS = (10, 20, 30)
RATES = (0.02, 0.05, 0.08)
AVAILABILITY = (1.00, 0.75, 0.50, 0.25)
WINTER_MONTHS = {11, 12, 1, 2, 3}
COLD_CITIES = ("Denver", "Chicago", "Minneapolis")
BUILDINGS = ("SmallOffice", "MediumOffice")
HEATING = {
    "H1_gas_heat": ("natural_gas", 0.80),
    "H2_heat_pump": ("electricity", 2.50),
    "H3_resistance": ("electricity", 1.00),
}
COOLING_COP = 3.50
PV_FACTOR = 12.462210342539992
ZERO_TOLERANCE = 1e-9


def pv_factor(years: int, rate: float) -> float:
    return float((1.0 - (1.0 + rate) ** (-years)) / rate)


def price_index() -> dict[tuple[str, str], float]:
    prices = pd.read_csv(PRICE_SOURCE)
    if len(prices) != 14 or prices.duplicated(["city", "carrier"]).any():
        raise ValueError("Canonical price table must contain fourteen unique city/carrier rows")
    if set(prices["constant_dollar_basis"]) != {"May 2026 USD"}:
        raise ValueError("Canonical prices must use the May 2026 constant-dollar basis")
    return {(row.city, row.carrier): float(row.base_recent_12m_usd_per_kwh_may2026)
            for row in prices.itertuples(index=False)}


def monthly_cost(row: dict, city: str, heating: str,
                 prices: dict[tuple[str, str], float]) -> tuple[float, float]:
    carrier, efficiency = HEATING[heating]
    cooling = float(row["cooling_load_kwh_th"]) / COOLING_COP * prices[(city, "electricity")]
    heating_cost = float(row["heating_load_kwh_th"]) / efficiency * prices[(city, carrier)]
    return cooling, heating_cost


def monthly_difference(reference: list[dict], tested: list[dict], city: str, heating: str,
                       prices: dict[tuple[str, str], float]) -> list[dict]:
    left = {int(row["month"]): row for row in reference}
    right = {int(row["month"]): row for row in tested}
    if set(left) != set(range(1, 13)) or set(right) != set(range(1, 13)):
        raise ValueError(f"Incomplete monthly physical records for {city}/{heating}")
    output = []
    for month in range(1, 13):
        left_cool, left_heat = monthly_cost(left[month], city, heating, prices)
        right_cool, right_heat = monthly_cost(right[month], city, heating, prices)
        output.append({"month": month,
                       "cooling_cost_difference_usd": left_cool - right_cool,
                       "heating_cost_difference_usd": left_heat - right_heat})
    return output


def discounted_value(monthly: list[dict], roof_area: float,
                     availability: float = 1.0) -> tuple[float, float, float, float]:
    cooling = heating = 0.0
    for row in monthly:
        factor = availability if int(row["month"]) in WINTER_MONTHS else 1.0
        cooling += factor * float(row["cooling_cost_difference_usd"])
        heating += factor * float(row["heating_cost_difference_usd"])
    annual = cooling + heating
    return cooling, heating, annual, annual * PV_FACTOR / roof_area


def canonical_physical() -> dict[tuple[str, str, str], list[dict]]:
    grouped: dict[tuple[str, str, str], list[dict]] = {}
    for row in physical_archive.canonical_physical_rows():
        grouped.setdefault((row["city"], row["building"], row["roof_case"]), []).append(row)
    if len(grouped) != 7 * 2 * 4 or any(len(values) != 12 for values in grouped.values()):
        raise ValueError("Canonical monthly roof-case physical matrix is incomplete")
    return grouped


def validate_reference_reconstruction(source: pd.DataFrame, physical: dict, prices: dict) -> None:
    adaptive = source.loc[source["comparison_type"].eq("ADAPTIVE_A_VS")].copy()
    if len(adaptive) != 84:
        raise ValueError(f"Expected 84 reference adaptive decisions, found {len(adaptive)}")
    for row in adaptive.itertuples(index=False):
        reference = physical[(row.city, row.building, "A_STATIC")]
        tested = physical[(row.city, row.building, physical_archive.ADAPTIVE_CASES[row.adaptive_case])]
        value = discounted_value(
            monthly_difference(reference, tested, row.city, row.heating_technology, prices),
            float(row.roof_area_m2),
        )[3]
        if not np.isclose(value, float(row.max_additional_installed_cost_usd_per_m2_roof), atol=1e-10):
            raise ValueError(f"Monthly reconstruction differs for {row.city}/{row.building}/{row.adaptive_case}/{row.heating_technology}")


def service_and_horizon(source: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    adaptive = source.loc[source["comparison_type"].eq("ADAPTIVE_A_VS")].copy()
    positive = adaptive.loc[adaptive["max_additional_installed_cost_usd_per_m2_roof"].gt(ZERO_TOLERANCE)].copy()
    if positive.groupby("adaptive_case").size().to_dict() != {"B": 7, "C": 12}:
        raise ValueError("Reference positive counts are not B=7 and C=12")
    key = ["city", "state", "building", "adaptive_case", "heating_technology"]
    service = positive[key + ["total_annual_operating_cost_difference_usd", "roof_area_m2",
                              "present_value_factor_20y_5pct",
                              "max_additional_installed_cost_usd_per_m2_roof"]].copy()
    service = service.rename(columns={"max_additional_installed_cost_usd_per_m2_roof":
                                      "break_even_additional_service_burden_pv_usd_per_m2_roof"})
    expected = (service["present_value_factor_20y_5pct"]
                * service["total_annual_operating_cost_difference_usd"] / service["roof_area_m2"])
    if not np.allclose(expected, service["break_even_additional_service_burden_pv_usd_per_m2_roof"]):
        raise ValueError("Reference service-burden thresholds do not reproduce the source matrix")
    detail = []
    for row in positive.itertuples(index=False):
        for years in PERIODS:
            for rate in RATES:
                factor = pv_factor(years, rate)
                detail.append({"city": row.city, "state": row.state, "building": row.building,
                               "adaptive_case": row.adaptive_case, "heating_technology": row.heating_technology,
                               "economic_horizon_years": years, "real_discount_rate": rate, "pv_factor": factor,
                               "max_additional_installed_cost_usd_per_m2_roof":
                                   factor * row.total_annual_operating_cost_difference_usd / row.roof_area_m2})
    horizon = pd.DataFrame(detail)
    summary = (horizon.groupby(["adaptive_case", "economic_horizon_years", "real_discount_rate", "pv_factor"])
               ["max_additional_installed_cost_usd_per_m2_roof"]
               .agg(positive_reference_decision_count="size", minimum="min", q1=lambda x: x.quantile(.25),
                    median="median", q3=lambda x: x.quantile(.75), maximum="max").reset_index())
    if len(service) != 19 or len(horizon) != 171 or len(summary) != 18:
        raise ValueError("Service/horizon cardinality audit failed")
    return service, horizon, summary


def availability_sensitivity(physical: dict, prices: dict, source: pd.DataFrame) -> pd.DataFrame:
    states = dict(zip(source["city"], source["state"]))
    comparisons = (("STATIC_0_VS_A", "", "CASE0_NATIVE_DOE_ROOF", "A_STATIC"),
                   ("ADAPTIVE_A_VS", "B", "A_STATIC", physical_archive.ADAPTIVE_CASES["B"]),
                   ("ADAPTIVE_A_VS", "C", "A_STATIC", physical_archive.ADAPTIVE_CASES["C"]))
    rows = []
    for city in COLD_CITIES:
        for building in BUILDINGS:
            roof = float(physical[(city, building, "A_STATIC")][0]["roof_area_m2"])
            for heating in HEATING:
                for comparison, adaptive_case, reference_case, tested_case in comparisons:
                    monthly = monthly_difference(physical[(city, building, reference_case)],
                                                 physical[(city, building, tested_case)], city, heating, prices)
                    for availability in AVAILABILITY:
                        cooling, heat, annual, value = discounted_value(monthly, roof, availability)
                        rows.append({"comparison_type": comparison, "city": city, "state": states[city],
                                     "building": building, "adaptive_case": adaptive_case,
                                     "heating_technology": heating, "radiative_roof_availability": availability,
                                     "cold_season_months": "November--March", "cooling_cop": COOLING_COP,
                                     "heating_conversion_value": HEATING[heating][1],
                                     "cooling_cost_difference_usd": cooling, "heating_cost_difference_usd": heat,
                                     "total_annual_operating_cost_difference_usd": annual, "roof_area_m2": roof,
                                     "present_value_factor": PV_FACTOR,
                                     "max_additional_installed_cost_usd_per_m2_roof": value,
                                     "availability_basis": "factor applied only to monthly incremental roof-case cost differences in November--March"})
    result = pd.DataFrame(rows)
    unique = ["comparison_type", "city", "building", "adaptive_case", "heating_technology", "radiative_roof_availability"]
    if len(result) != 216 or result.duplicated(unique).any():
        raise ValueError("Current availability matrix must contain 216 unique comparison rows")
    full = result.loc[result["radiative_roof_availability"].eq(1.0)]
    canonical = source.loc[source["city"].isin(COLD_CITIES),
                           ["comparison_type", "city", "building", "adaptive_case", "heating_technology",
                            "max_additional_installed_cost_usd_per_m2_roof"]]
    merged = full.merge(canonical, on=["comparison_type", "city", "building", "adaptive_case", "heating_technology"],
                        how="outer", validate="one_to_one", suffixes=("", "_canonical"), indicator=True)
    if not merged["_merge"].eq("both").all() or not np.allclose(
            merged["max_additional_installed_cost_usd_per_m2_roof"],
            merged["max_additional_installed_cost_usd_per_m2_roof_canonical"], atol=1e-10):
        raise ValueError("Full-availability rows do not close to the canonical reference matrix")
    return result


def optical_physical() -> dict[tuple[str, str, str], list[dict]]:
    rows = pd.read_csv(OPTICAL_PHYSICAL_SOURCE)
    if len(rows) != 432 or rows.duplicated(["case_id", "month"]).any():
        raise ValueError("Frozen optical physical matrix must contain 432 unique monthly rows")
    if not rows[["cooling_load_kwh_th", "heating_load_kwh_th"]].ge(0).all().all():
        raise ValueError("Frozen optical physical loads must be nonnegative")
    grouped = {}
    for (city, building, case_id), frame in rows.groupby(["city", "building", "case_id"], sort=False):
        grouped[(city, building, case_id.split("__")[-1].upper())] = frame.to_dict("records")
    if len(grouped) != 36 or any(len(values) != 12 for values in grouped.values()):
        raise ValueError("Frozen optical-state monthly matrix is incomplete")
    return grouped


def optical_sensitivity(physical: dict, optical: dict, prices: dict,
                        source: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    reference_c = source.loc[source["comparison_type"].eq("ADAPTIVE_A_VS") & source["adaptive_case"].eq("C")]
    reference_index = {(row.city, row.building, row.heating_technology): row
                       for row in reference_c.itertuples(index=False)}
    states = (("E_LOW_035", "low_emissivity_function", "C_ELOW_035", "A_STATIC", 0.35, 0.75, 0.95),
              ("E_LOW_050", "low_emissivity_function", "C_ELOW_050", "A_STATIC", 0.50, 0.75, 0.95),
              ("R_DIFF_070", "adaptive_specific_reflectance", "C_R070", "A_STATIC", 0.20, 0.70, 0.95),
              ("R_DIFF_065", "adaptive_specific_reflectance", "C_R065", "A_STATIC", 0.20, 0.65, 0.95),
              ("R_COMMON_070_090", "matched_comparator_common_mode", "C_R070", "A_R090", 0.20, 0.70, 0.90),
              ("R_COMMON_065_085", "matched_comparator_common_mode", "C_R065", "A_R085", 0.20, 0.65, 0.85))
    rows, interaction = [], []
    for state, branch, tested_state, reference_state, epsilon_low, reflectance_c, reflectance_a in states:
        for city in COLD_CITIES:
            for building in BUILDINGS:
                roof = float(physical[(city, building, "A_STATIC")][0]["roof_area_m2"])
                tested = optical[(city, building, tested_state)]
                reference = (physical[(city, building, "A_STATIC")] if reference_state == "A_STATIC"
                             else optical[(city, building, reference_state)])
                for heating in HEATING:
                    monthly = monthly_difference(reference, tested, city, heating, prices)
                    cooling, heat, annual, value = discounted_value(monthly, roof)
                    pristine = float(reference_index[(city, building, heating)].max_additional_installed_cost_usd_per_m2_roof)
                    base = {"controlled_state": state, "sensitivity_branch": branch, "city": city,
                            "building": building, "heating_technology": heating,
                            "epsilon_low_c": epsilon_low, "epsilon_high_c": 0.90,
                            "solar_reflectance_c": reflectance_c, "solar_reflectance_a": reflectance_a,
                            "reference_roof_state": reference_state, "tested_roof_state": tested_state,
                            "cooling_cop": COOLING_COP, "heating_conversion_value": HEATING[heating][1],
                            "roof_area_m2": roof, "present_value_factor": PV_FACTOR}
                    rows.append({**base, "cooling_cost_difference_usd": cooling,
                                 "heating_cost_difference_usd": heat,
                                 "total_annual_operating_cost_difference_usd": annual,
                                 "max_additional_installed_cost_usd_per_m2_roof": value,
                                 "matched_pristine_case_c_value_usd_per_m2_roof": pristine,
                                 "change_from_matched_pristine_case_c_usd_per_m2_roof": value - pristine})
                    for availability in AVAILABILITY:
                        avail_cool, avail_heat, avail_annual, avail_value = discounted_value(monthly, roof, availability)
                        interaction.append({**base, "radiative_roof_availability": availability,
                                            "cooling_cost_difference_usd": avail_cool,
                                            "heating_cost_difference_usd": avail_heat,
                                            "total_annual_operating_cost_difference_usd": avail_annual,
                                            "max_additional_installed_cost_usd_per_m2_roof": avail_value})
    detail = pd.DataFrame(rows)
    interaction_frame = pd.DataFrame(interaction)
    if len(detail) != 108 or detail.duplicated(["controlled_state", "city", "building", "heating_technology"]).any():
        raise ValueError("Current optical sensitivity must contain 108 unique reference rows")
    if len(interaction_frame) != 432 or interaction_frame.duplicated(
            ["controlled_state", "city", "building", "heating_technology", "radiative_roof_availability"]).any():
        raise ValueError("Current optical/availability interaction must contain 432 unique rows")
    summary = (detail.groupby(["controlled_state", "sensitivity_branch", "epsilon_low_c", "epsilon_high_c",
                               "solar_reflectance_c", "solar_reflectance_a", "reference_roof_state", "tested_roof_state"])
               .agg(reference_decision_count=("max_additional_installed_cost_usd_per_m2_roof", "size"),
                    positive_count=("max_additional_installed_cost_usd_per_m2_roof", lambda x: int((x > ZERO_TOLERANCE).sum())),
                    delta_minimum=("change_from_matched_pristine_case_c_usd_per_m2_roof", "min"),
                    delta_q1=("change_from_matched_pristine_case_c_usd_per_m2_roof", lambda x: x.quantile(.25)),
                    delta_median=("change_from_matched_pristine_case_c_usd_per_m2_roof", "median"),
                    delta_q3=("change_from_matched_pristine_case_c_usd_per_m2_roof", lambda x: x.quantile(.75)),
                    delta_maximum=("change_from_matched_pristine_case_c_usd_per_m2_roof", "max")).reset_index())
    if len(summary) != 6 or not summary["reference_decision_count"].eq(18).all():
        raise ValueError("Optical summary must contain six states with eighteen reference decisions each")
    return detail, summary, interaction_frame


def write_outputs(service: pd.DataFrame, horizon: pd.DataFrame, horizon_summary: pd.DataFrame,
                  availability: pd.DataFrame, optical: pd.DataFrame, optical_summary: pd.DataFrame,
                  interaction: pd.DataFrame) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, frame in {"central_service_burden_thresholds.csv": service,
                        "central_horizon_discount_sensitivity.csv": horizon,
                        "central_horizon_discount_summary.csv": horizon_summary,
                        "central_cold_season_availability_sensitivity.csv": availability,
                        "central_optical_function_sensitivity.csv": optical,
                        "central_optical_function_summary.csv": optical_summary,
                        "central_optical_availability_interaction.csv": interaction}.items():
        frame.to_csv(OUT / name, index=False)
    (OUT / "README.md").write_text(
        "# Current-framework deployment-sensitivity derivations\n\n"
        "Canonical economics: `../joint_economic_robustness/central_baseline_base_price.csv` and "
        "`../joint_economic_robustness/price_levels.csv`.\n\n"
        "All calculations are economic-only post-processing of frozen monthly physical outputs; no EnergyPlus "
        "simulation is invoked or modified. Service-burden and economic-horizon results use the 19 positive "
        "reference decisions (Case B: 7; Case C: 12). Cold-season availability uses 36 adaptive reference "
        "decisions (three cities, two buildings, three heating technologies, and two adaptive cases) at each "
        "availability level; the tidy output also reports the 18 corresponding Case 0--A comparisons. Each "
        "controlled optical state uses 18 Case C reference decisions (three cities, two buildings, and three "
        "heating technologies). The optical/availability interaction contains those 18 decisions for each of "
        "six optical states and four availability levels.\n", encoding="utf-8")


def main() -> None:
    source = pd.read_csv(SOURCE).fillna("")
    prices = price_index()
    physical = canonical_physical()
    validate_reference_reconstruction(source, physical, prices)
    service, horizon, horizon_summary = service_and_horizon(source)
    availability = availability_sensitivity(physical, prices, source)
    optical_detail, optical_summary, interaction = optical_sensitivity(
        physical, optical_physical(), prices, source)
    write_outputs(service, horizon, horizon_summary, availability, optical_detail, optical_summary, interaction)
    adaptive_availability = availability.loc[availability["comparison_type"].eq("ADAPTIVE_A_VS")]
    counts = (adaptive_availability.groupby(["city", "radiative_roof_availability"])
              ["max_additional_installed_cost_usd_per_m2_roof"]
              .apply(lambda x: int((x > ZERO_TOLERANCE).sum())).unstack())
    low = interaction.loc[interaction["radiative_roof_availability"].eq(0.25)]
    low_counts = low.groupby("controlled_state")["max_additional_installed_cost_usd_per_m2_roof"].apply(
        lambda x: int((x > ZERO_TOLERANCE).sum()))
    x = service["break_even_additional_service_burden_pv_usd_per_m2_roof"]
    print("Current-framework downstream economics:")
    print(f"service={len(service)} horizon={len(horizon)} availability={len(availability)} optical={len(optical_detail)} interaction={len(interaction)}")
    print(f"Reference service threshold min/median/max: {x.min():.6f}/{x.median():.6f}/{x.max():.6f}")
    print("Adaptive availability positive counts by city (columns are availability):")
    print(counts.to_string())
    print("Optical reference summaries:")
    print(optical_summary[["controlled_state", "positive_count", "delta_minimum", "delta_median", "delta_maximum"]].to_string(index=False))
    print("Positive optical/availability rows at f_avail=0.25:")
    print(low_counts.to_string())


if __name__ == "__main__":
    main()
