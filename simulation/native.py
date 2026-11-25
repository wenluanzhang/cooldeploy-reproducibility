"""Read EnergyPlus annual weather-period outputs without modifying native files."""
from __future__ import annotations

from collections import Counter
from contextlib import closing
from itertools import product
from math import fsum, isfinite
from pathlib import Path
import hashlib
import re
import sqlite3

CARRIERS = {"Electricity": "Electricity", "NaturalGas": "Natural Gas", "FuelOilNo2": "Fuel Oil No 2"}
END_USES = {
    "Heating": "Heating", "Cooling": "Cooling", "Fans": "Fans", "Pumps": "Pumps",
    "HeatRejection": "Heat Rejection", "Humidification": "Humidification", "HeatRecovery": "Heat Recovery",
}
MONTHS = tuple(range(1, 13))
ABUPS = "AnnualBuildingUtilityPerformanceSummary"
GJ_ROUNDING = 0.005001  # ABUPS prints to 0.01 GJ.


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_file(path, expected):
    require(path.is_file(), f"Missing file: {path}")
    require(sha256(path) == expected, f"SHA-256 mismatch: {path}")


def native_paths(raw):
    return {kind: raw / f"eplusout.{kind}" for kind in ("sql", "err", "end")}


def tabular(db, table, row, column, units):
    results = db.execute("""
        SELECT Value, Units FROM TabularDataWithStrings
        WHERE ReportName=? AND TableName=? AND RowName=? AND ColumnName=?
    """, (ABUPS, table, row, column)).fetchall()
    require(len(results) == 1 and results[0][1] == units,
            f"Missing, duplicate or wrong units in ABUPS: {table}/{row}/{column}, expected {units}")
    value = float(results[0][0])
    require(isfinite(value) and value >= 0, f"Invalid ABUPS value: {table}/{row}/{column}")
    return value


def windows_warnings(err, end):
    finish = re.search(r"EnergyPlus Completed Successfully--\s+(\d+) Warning;\s+(\d+) Severe Errors", end)
    require(finish is not None, "Missing successful EnergyPlus end marker")
    # Retain each full category header and recurring count line in occurrence order.
    messages = [line.strip() for line in err.splitlines()
                if re.search(r"\*\*\s+(?:Warning|Severe|Fatal)\s+\*\*|This error occurred .* total times", line, re.I)]
    iteration_observed = any("maximum iterations" in line.lower() for line in messages)
    return {
        "warning_count": int(finish[1]), "severe_count": int(finish[2]),
        "maximum_iterations_observed": iteration_observed, "warning_signatures": messages,
    }


def controller_evidence(db, period, faces, case):
    # Canonical broad-B reports roof face temperatures. Missing observations stay explicit.
    if case["population"] != "main" or case["roof"] != "B":
        return {}
    evidence = {}
    for face, _ in faces:
        rows = db.execute("""
            SELECT rd.Value FROM ReportData AS rd
            JOIN ReportDataDictionary AS dd USING (ReportDataDictionaryIndex)
            JOIN Time AS t USING (TimeIndex)
            WHERE dd.KeyValue=? AND dd.Name='Surface Outside Face Temperature'
              AND dd.ReportingFrequency='Zone Timestep' AND dd.Units='C'
              AND t.EnvironmentPeriodIndex=? AND t.WarmupFlag=0
            ORDER BY t.TimeIndex
        """, (face, period)).fetchall()
        if not rows:
            continue
        temps = [row[0] for row in rows]
        require(all(isfinite(t) for t in temps), f"Nonfinite roof temperature: {face}")
        # Inferred states use the preceding native timestep. The first state is unknown.
        states = Counter("low" if t <= 19 else "high" if t >= 27 else "transition" for t in temps[:-1])
        packed = ",".join(t.hex() for t in temps).encode("ascii")
        evidence[face] = {"samples": len(temps), "low": states["low"],
                          "transition": states["transition"], "high": states["high"],
                          "temperature_sha256": hashlib.sha256(packed).hexdigest()}
    return evidence


def extract(case, raw):
    paths = native_paths(raw)
    require(all(path.is_file() for path in paths.values()), "Expected eplusout.sql, eplusout.err and eplusout.end")
    warnings = windows_warnings(paths["err"].read_text(encoding="utf-8", errors="replace"),
                               paths["end"].read_text(encoding="utf-8"))
    uri = paths["sql"].resolve().as_uri() + "?mode=ro&immutable=1"
    with closing(sqlite3.connect(uri, uri=True)) as db:
        builds = db.execute("SELECT EnergyPlusVersion FROM Simulations").fetchall()
        require(len(builds) == 1 and builds[0][0].startswith(f"EnergyPlus, Version {case['engine_build']},"),
                "SQL simulator build differs from the manifest")
        periods = db.execute("SELECT EnvironmentPeriodIndex FROM EnvironmentPeriods WHERE EnvironmentType=3").fetchall()
        require(len(periods) == 1, "Expected one native annual weather-file environment")
        period = periods[0][0]
        hours = db.execute("""
            SELECT Month, Day, Hour, Minute, Interval FROM Time
            WHERE EnvironmentPeriodIndex=? AND WarmupFlag=0 AND IntervalType=1
            ORDER BY TimeIndex
        """, (period,)).fetchall()
        require(len(hours) == int(case["annual_hours"]) and all(row[4] == 60 for row in hours)
                and len({tuple(row[:4]) for row in hours}) == len(hours)
                and hours[0][:3] == (1, 1, 1) and hours[-1][:3] == (12, 31, 24),
                "Incomplete or duplicate hourly weather-period clock")
        faces = db.execute("""
            SELECT SurfaceName, GrossArea FROM Surfaces
            WHERE ClassName='Roof' AND ExtBoundCond=0 AND HeatTransferSurf=1
            ORDER BY SurfaceName
        """).fetchall()
        require(faces and all(isfinite(area) and area > 0 for _,area in faces), "Missing or invalid exterior roof faces")
        area = fsum(area for _, area in faces)
        occupied = {mode.lower(): tabular(db, "Comfort and Setpoint Not Met Summary",
                     f"Time Setpoint Not Met During Occupied {mode}", "Facility", "Hours")
                    for mode in ("Heating", "Cooling")}
        meters = {}
        for end_use, carrier in product(END_USES, CARRIERS):
            name = f"{end_use}:{carrier}"
            ids = db.execute("""
                SELECT ReportDataDictionaryIndex, Units, Type FROM ReportDataDictionary
                WHERE IsMeter=1 AND ReportingFrequency='Monthly' AND Name=?
            """, (name,)).fetchall()
            require(not ids or (len(ids) == 1 and ids[0][1:] == ("J", "Sum")),
                    f"Duplicate meter or wrong energy unit/type: {name}")
            rows = db.execute("""
                SELECT t.Month, rd.Value FROM ReportData AS rd JOIN Time AS t USING (TimeIndex)
                WHERE rd.ReportDataDictionaryIndex=? AND t.EnvironmentPeriodIndex=?
                  AND t.IntervalType=3 AND t.WarmupFlag=0 ORDER BY t.Month
            """, (ids[0][0], period)).fetchall() if ids else []
            if ids:
                require(tuple(month for month, _ in rows) == MONTHS
                        and all(isfinite(v) and v >= 0 for _, v in rows),
                        f"Invalid or incomplete 12-month energy meter: {name}")
            values = [v for _, v in rows] if ids else [0.0] * 12
            printed_gj = tabular(db, "End Uses", END_USES[end_use], CARRIERS[carrier], "GJ")
            require(abs(fsum(values) / 1e9 - printed_gj) <= GJ_ROUNDING,
                    f"Native meter fails 0.005 GJ ABUPS rounding check: {name}")
            meters[name] = [value / 3.6e6 for value in values]
        controller = controller_evidence(db, period, faces, case)
    return {
        "case_id": case["case_id"], "annual_hours": len(hours),
        "hourly_clock_sha256": hashlib.sha256(repr(hours).encode("ascii")).hexdigest(),
        "roof_area_m2": area, "roof_faces": dict(faces), "occupied_unmet_h": occupied,
        "meter_monthly_kWh": meters, "warnings": warnings,
        "broad_B_predecessor_state_evidence": controller,
        "accepted_numerical_classification": case["accepted_numerical_classification"],
    }
