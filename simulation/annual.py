"""Validate inputs, run one accepted annual, and compare native outputs."""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import json
from itertools import product
from math import fsum, isfinite
from pathlib import Path
import re
import shutil
import sqlite3
import subprocess
import sys
import time

from native import CARRIERS, END_USES, MONTHS, extract, native_paths, require, sha256, verify_file

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data/processed"
MANIFEST = ROOT / "simulation/cases.csv"
ENGINE = {
    "energyplus.exe": "1085db7c1b00f8a021c9d06b9d15cb739be0eae597053772101fc1c752b770e7",
    "Energy+.idd": "7d30c281aa21d63555c753a953124da03d88b6b149dc19e3649f2cbe6c944c68",
    "Energy+.schema.epJSON": "60b24d904e6fa553f773b38037a8a09730e6da1538647df552cd77db8d6704a9",
    "energyplusapi.dll": "bbe6f66240d108df9f51a03b9beb968808a2173234253574d27a31605aec2aa2",
}
BUILD = "26.1.0-6f2e40d102"
POPULATIONS = {"main": 216, "sharp": 54, "optical": 108}
ENERGY_TOL = 1e-7  # kWh, fixed before the validation rerun
COST_TOL = 1e-7    # USD, frozen accounting closure
REPORTED_TOL = 1e-8  # m? and h, permits only representation differences


def read(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def case_manifest(path=MANIFEST):
    rows = read(path)
    cases = {row["case_id"]: row for row in rows}
    require(len(cases) == len(rows), "Duplicate case ID")
    require(Counter(row["population"] for row in rows) == POPULATIONS, "Unexpected population sizes")
    for row in rows:
        require(row["case_id"] == "/".join((row["population"], row["family"], row["variant"]))
                and row["family"] == "/".join(row[k] for k in ("location", "configuration", "hvac")),
                f"Invalid case key: {row['case_id']}")
        require(row["engine_build"] == BUILD and row["auxiliary_inputs"] == "none", "Unsupported run dependencies")
        require(re.fullmatch(r"[\w.-]+\.epw", row["weather"]), "Expected a weather basename")
        require(all(re.fullmatch(r"[0-9a-f]{64}", row[name])
                    for name in ("input_sha256", "weather_sha256", "accepted_sql_sha256", "accepted_err_sha256")),
                f"Invalid SHA-256: {row['case_id']}")
    return cases


def check_inputs(case, folder):
    idf = folder / "idf" / (case["input_sha256"] + ".idf")
    epw = folder / "weather" / case["weather"]
    verify_file(idf, case["input_sha256"])
    verify_file(epw, case["weather_sha256"])
    return idf, epw


def check_engine(exe):
    require(exe.name.lower() == "energyplus.exe", "Use the pinned Windows x86-64 EnergyPlus executable")
    for name, digest in ENGINE.items():
        verify_file(exe if name == "energyplus.exe" else exe.parent / name, digest)


def new_output(path, *protected):
    require(not path.is_symlink(), "Output must not be a symbolic link")
    path = path.resolve()
    require(not any(path.is_relative_to(folder.resolve()) for folder in (ROOT, *protected)),
            "Output must be outside the repository and the supplied input directories")
    require(not path.exists() and not path.is_symlink(), f"Output path already exists: {path}")
    require(path.parent.is_dir(), f"Output parent must exist: {path.parent}")
    return path


def save(path, data):
    with path.open("x", encoding="utf-8") as f:
        json.dump(data, f, indent=2, allow_nan=False)
        f.write("\n")


def run(case, inputs, exe, out, timeout):
    idf, weather = check_inputs(case, inputs)
    check_engine(exe)
    require(1 <= timeout <= 3600, "Timeout must be between 1 and 3600 seconds")
    out = new_output(out, inputs, exe.parent)
    version = subprocess.run([str(exe), "--version"], text=True, capture_output=True, check=True, timeout=15)
    require(version.stdout.strip() == f"EnergyPlus, Version {BUILD}", "EnergyPlus reported an unexpected version")
    out.mkdir()
    staged_idf, staged_weather = out / "in.idf", out / weather.name
    shutil.copyfile(idf, staged_idf)
    shutil.copyfile(weather, staged_weather)
    verify_file(staged_idf, case["input_sha256"])
    verify_file(staged_weather, case["weather_sha256"])
    command = [str(exe), "-i", str(exe.parent / "Energy+.idd"), "-w", str(staged_weather), "-d", str(out), str(staged_idf)]
    started = time.monotonic()
    with (out / "console.log").open("xb") as log:
        completed = subprocess.run(command, cwd=out, stdout=log, stderr=subprocess.STDOUT, timeout=timeout)
    elapsed = time.monotonic() - started
    require(completed.returncode == 0, f"EnergyPlus exit {completed.returncode}; see {out / 'console.log'}")
    save(out / "run.json", {"case_id": case["case_id"], "command": command, "exit_code": completed.returncode,
                           "elapsed_seconds": elapsed, "engine": BUILD, "engine_sha256": ENGINE["energyplus.exe"],
                           "input_sha256": case["input_sha256"], "weather_sha256": case["weather_sha256"],
                           "native_sha256": {kind: sha256(path) for kind, path in native_paths(out).items()}})
    return out


def verified_extraction(case, source, accepted):
    files = native_paths(source)
    if accepted:
        verify_file(files["sql"], case["accepted_sql_sha256"])
        verify_file(files["err"], case["accepted_err_sha256"])
    else:
        receipt = json.loads((source / "run.json").read_text(encoding="utf-8"))
        for k in ("case_id", "input_sha256", "weather_sha256"):
            require(receipt[k] == case[k], f"Run receipt mismatch: {k}")
        require(receipt["exit_code"] == 0 and receipt["engine"] == BUILD
                and receipt["engine_sha256"] == ENGINE["energyplus.exe"], "Unverified run receipt")
        for kind, path in files.items():
            verify_file(path, receipt["native_sha256"][kind])
    return extract(case, source)


def bridge(case, result):
    family = case["family"]
    prices = {r["carrier"]: r["frozen_price"] for r in read(PROCESSED / "canonical/family_carrier_price_162.csv")
              if r["family"] == family}
    require(prices.keys() == CARRIERS.keys(), "Missing frozen case carrier price")
    meters = result["meter_monthly_kWh"]
    monthly = []
    for month, carrier in product(MONTHS, CARRIERS):
        kwh = fsum(meters[f"{use}:{carrier}"][month - 1] for use in END_USES)
        require(prices[carrier] or kwh == 0, f"Missing price for nonzero {carrier} use")
        rate = float(prices[carrier]) if prices[carrier] else None
        monthly.append({"family": family, "roof": case["variant"], "month": month, "carrier": carrier,
                        "purchased_kWh": kwh, "price_USD_kWh": rate, "cost_USD": kwh * (rate or 0)})
    annual = []
    for use, carrier in product(END_USES, CARRIERS):
        kwh = fsum(meters[f"{use}:{carrier}"])
        annual.append({"family": family, "roof": case["variant"], "end_use": use, "carrier": carrier,
                       "purchased_kWh": kwh, "native_cost_USD_year": kwh * float(prices[carrier] or 0)})
    return {"monthly_carriers": monthly, "annual_end_uses": annual,
            "annual_bill_USD": fsum(row["cost_USD"] for row in monthly)}


def compare(case, result, accepted_native=None):
    data = bridge(case, result)
    differences = []

    def number(metric, actual, expected, tolerance, unit):
        actual, expected = float(actual), float(expected)
        delta = actual - expected
        differences.append({"metric": metric, "unit": unit, "actual": actual, "reference": expected,
                            "difference": delta, "tolerance": tolerance,
                            "pass": isfinite(delta) and abs(delta) <= tolerance})

    def exact(metric, actual, expected):
        differences.append({"metric": metric, "actual": actual, "reference": expected, "pass": actual == expected})

    family, roof = case["family"], case["variant"]
    pop = case["population"]
    exact("case ID", result["case_id"], case["case_id"])
    number("annual weather-period hours", result["annual_hours"], case["annual_hours"], 0, "h")
    number("exterior roof area", result["roof_area_m2"], case["roof_area_m2"], REPORTED_TOL, "m2")
    for mode, hours in result["occupied_unmet_h"].items():
        number(f"occupied {mode} unmet", hours, case[f"occupied_{mode}_unmet_h"], REPORTED_TOL, "h")

    if pop != "sharp":
        selector = "roof" if pop == "main" else "variant"
        kwh_key = "purchased_kWh" if pop == "main" else "purchased_HVAC_kWh"
        frozen = [r for r in read(PROCESSED / case["reference_csv"])
                  if r["family"] == family and r[selector] == roof]
        monthly = {(int(r["month"]), r["carrier"]):r for r in frozen}
        require(len(frozen) == len(monthly) == 36, "Expected 36 frozen monthly reference rows")
        for row in data["monthly_carriers"]:
            key = (row["month"], row["carrier"])
            ref = monthly[key]
            number(f"month {key[0]} {key[1]} energy", row["purchased_kWh"], ref[kwh_key], ENERGY_TOL, "kWh")
            number(f"month {key[0]} {key[1]} cost", row["cost_USD"], ref["cost_USD"], COST_TOL, "USD")
        number("annual HVAC bill", data["annual_bill_USD"],
               fsum(float(r["cost_USD"]) for r in frozen), COST_TOL, "USD")

    cost_reference = ("optical/native_enduse_costs.csv" if pop == "optical" else "width/sharp_native_enduse_costs.csv")
    field = "annual_cost_USD" if pop == "optical" else "native_cost_USD_year"
    selector = "variant" if pop == "optical" else "roof"
    frozen_uses = [r for r in read(PROCESSED / cost_reference) if r["family"] == family and r[selector] == roof]
    ref_cost = {(r["end_use"], r["carrier"]):r for r in frozen_uses}
    require(len(frozen_uses) == len(ref_cost) == 21, "Expected 21 frozen end-use/carrier reference rows")
    for row in data["annual_end_uses"]:
        key = (row["end_use"], row["carrier"])
        number(f"{key[0]} {key[1]} annual cost", row["native_cost_USD_year"],
               ref_cost[key][field], COST_TOL, "USD")
    if pop == "sharp":
        number("annual HVAC bill", data["annual_bill_USD"],
               fsum(float(r["native_cost_USD_year"]) for r in frozen_uses), COST_TOL, "USD")

    if accepted_native is not None:
        original = verified_extraction(case, accepted_native, accepted=True)
        for field in ("hourly_clock_sha256", "roof_faces", "warnings", "broad_B_predecessor_state_evidence"):
            exact(field, result[field], original[field])
        for meter, months in result["meter_monthly_kWh"].items():
            for month, kwh in enumerate(months, 1):
                number(f"{meter} month {month} native comparison", kwh,
                       original["meter_monthly_kWh"][meter][month-1], ENERGY_TOL, "kWh")
    return {"status": "PASS" if all(d["pass"] for d in differences) else "MISMATCH",
            "case_id": case["case_id"], "reference": case["reference_csv"],
            "accepted_warning_classification": case["accepted_numerical_classification"],
            "accepted_native_checked": accepted_native is not None, "checks": differences}


def cli(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    ls = commands.add_parser("list")
    ls.add_argument("--population", choices=POPULATIONS)
    check = commands.add_parser("check")
    selection = check.add_mutually_exclusive_group(required=True)
    selection.add_argument("--case")
    selection.add_argument("--all", action="store_true")
    check.add_argument("--inputs", type=Path, required=True)
    check.add_argument("--engine", type=Path)
    execute = commands.add_parser("run")
    execute.add_argument("--case", required=True)
    execute.add_argument("--inputs", type=Path, required=True)
    execute.add_argument("--engine", type=Path, required=True)
    execute.add_argument("--output", type=Path, required=True)
    execute.add_argument("--timeout", type=int, default=240)
    extract_cmd = commands.add_parser("extract")
    extract_cmd.add_argument("--case", required=True)
    extract_cmd.add_argument("--raw", type=Path, required=True)
    extract_cmd.add_argument("--accepted", action="store_true")
    extract_cmd.add_argument("--output", type=Path, required=True)
    compare_cmd = commands.add_parser("compare")
    compare_cmd.add_argument("--case", required=True)
    compare_cmd.add_argument("--extracted", type=Path, required=True)
    compare_cmd.add_argument("--accepted-native", type=Path)
    compare_cmd.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    cases = case_manifest()
    if args.command == "list":
        for row in cases.values():
            if args.population is None or row["population"] == args.population:
                print(row["case_id"])
        return 0
    case_id = args.case
    require(case_id in cases or case_id is None, f"Unknown case: {case_id}")
    if args.command == "check":
        checked = cases.values() if args.all else [cases[case_id]]
        for row in checked:
            check_inputs(row, args.inputs)
        if args.engine:
            check_engine(args.engine.resolve())
        print(f"PASS: {len(checked)} case input pairs match SHA-256")
        return 0
    case = cases[case_id]
    if args.command == "run":
        print(run(case, args.inputs.resolve(), args.engine.resolve(), args.output, args.timeout))
    elif args.command == "extract":
        output = new_output(args.output, args.raw)
        result = verified_extraction(case, args.raw, args.accepted)
        result["processed_bridge"] = bridge(case, result)
        save(output, result)
    elif args.command == "compare":
        paths = (args.accepted_native,) if args.accepted_native else ()
        output = new_output(args.output, *paths)
        result = json.loads(args.extracted.read_text(encoding="utf-8"))
        report = compare(case, result, args.accepted_native)
        save(output, report)
        print(f"{report['status']}: {len(report['checks'])} checks; {output}")
        return 0 if report["status"] == "PASS" else 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(cli())
    except (ValueError, OSError, KeyError, sqlite3.Error, subprocess.SubprocessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
