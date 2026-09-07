"""Load the frozen monthly building-energy results used by the public analysis."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUTS = ROOT / "data" / "processed" / "frozen_physical_inputs"
CITIES = {"Miami", "Phoenix", "Baltimore", "Seattle", "Denver", "Chicago", "Minneapolis"}
BUILDINGS = {"SmallOffice", "MediumOffice"}
CASES = {"CASE0_NATIVE_DOE_ROOF", "A_STATIC", "B_TEMP_TRIGGERED", "C_TEMP_TRIGGERED"}
ADAPTIVE_CASES = {"B": "B_TEMP_TRIGGERED", "C": "C_TEMP_TRIGGERED"}
OLD_CITIES = {"Miami", "Baltimore", "Minneapolis"}


def read_csv(name: str) -> list[dict[str, str]]:
    with (INPUTS / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _accepted(rows: list[dict[str, str]], label: str) -> None:
    failed = [row for row in rows if any(int(float(row[field])) != 0 for field in ("exit_code", "severe_count", "fatal_count"))]
    if failed:
        raise ValueError(f"Frozen input contains an unaccepted simulation record in {label}.")


def canonical_physical_rows() -> list[dict[str, str]]:
    """Merge the four roof cases in the frozen seven-city monthly matrix."""
    compact = read_csv("phase1c_compact_monthly_physical_results.csv")
    triggered = read_csv("phase1e_monthly_physical_results.csv")
    expansion = read_csv("phase2b_monthly_physical_results.csv")
    _accepted(compact, "compact inputs")
    _accepted(triggered, "temperature-triggered inputs")
    _accepted(expansion, "expansion inputs")
    rows: list[dict[str, str]] = []
    for row in compact:
        if row["city"] in OLD_CITIES and row["roof_state"] in {"CASE0_NATIVE_DOE_ROOF", "A_STATIC"}:
            rows.append({**row, "roof_case": row["roof_state"]})
    for row in triggered:
        if row["city"] in OLD_CITIES and row["roof_state"] in set(ADAPTIVE_CASES.values()):
            rows.append({**row, "roof_case": row["roof_state"]})
    rows.extend(expansion)
    expected = len(CITIES) * len(BUILDINGS) * len(CASES) * 12
    keys = {(row["city"], row["building"], row["roof_case"], int(row["month"])) for row in rows}
    if len(rows) != expected or len(keys) != expected:
        raise ValueError("Frozen physical matrix is incomplete or contains duplicate rows.")
    if {row["city"] for row in rows} != CITIES or {row["building"] for row in rows} != BUILDINGS or {row["roof_case"] for row in rows} != CASES:
        raise ValueError("Frozen physical matrix does not contain the expected cases.")
    return rows
