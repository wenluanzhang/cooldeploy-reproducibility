"""Offline preparation and extraction guard tests. No simulator is launched."""
import hashlib
import pathlib
import sqlite3
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "simulation"))
import annual
import native


class SimulationTests(unittest.TestCase):
    def test_manifest_population_keys_and_frozen_references(self):
        cases = annual.case_manifest().values()
        refs = {
            "main": ("canonical/case_reality_216.csv", "roof"),
            "sharp": ("width/matched_54_width_comparisons.csv", None),
            "optical": ("optical/service_numerical.csv", "variant"),
        }
        for population, (file, variant) in refs.items():
            records = annual.read(annual.PROCESSED / file)
            if population == "optical":
                records = [r for r in records if r["variant"] not in ("A", "C")]
            expected = {(row["family"], row[variant] if variant else "Bsharp") for row in records}
            items = [r for r in cases if r["population"] == population]
            self.assertEqual({(r["family"], r["variant"]) for r in items}, expected)
            if population == "main":
                by_key = {(r["family"], r["roof"]): r for r in records}
                for row in items:
                    source = by_key[(row["family"], row["variant"])]
                    self.assertEqual(row["input_sha256"], source["executed_idf_sha256"])
                    self.assertEqual(row["weather_sha256"], source["weather_sha256"])

    def test_prepare_fails_on_missing_or_modified_input_and_weather(self):
        with tempfile.TemporaryDirectory() as folder:
            root = pathlib.Path(folder)
            h = hashlib.sha256(b"example").hexdigest()
            case = {"input_sha256": h, "weather_sha256": h, "weather": "weather.epw"}
            with self.assertRaisesRegex(ValueError, "Missing"):
                annual.check_inputs(case, root)
            for item in ("idf", "weather"):
                (root / item).mkdir()
            idf, epw = root / "idf" / (h + ".idf"), root / "weather/weather.epw"
            idf.write_bytes(b"example")
            epw.write_bytes(b"different")
            with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
                annual.check_inputs(case, root)
            epw.write_bytes(b"example")
            self.assertEqual(annual.check_inputs(case, root), (idf, epw))
            idf.write_bytes(b"different")
            with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
                annual.check_inputs(case, root)

    def test_output_guard(self):
        with tempfile.TemporaryDirectory() as folder:
            root = pathlib.Path(folder).resolve()
            with self.assertRaisesRegex(ValueError, "outside"):
                annual.new_output(ROOT / "data/processed/new.json")
            with self.assertRaisesRegex(ValueError, "outside"):
                annual.new_output(root / "new.json", root)
            with self.assertRaisesRegex(ValueError, "already exists"):
                annual.new_output(root)
            self.assertEqual(annual.new_output(root / "fresh.json"), root / "fresh.json")

    def test_bad_unit_rejected(self):
        with sqlite3.connect(":memory:") as db:
            db.execute("CREATE TABLE TabularDataWithStrings (ReportName,TableName,RowName,ColumnName,Units,Value)")
            db.execute("INSERT INTO TabularDataWithStrings VALUES (?,?,?,?,?,?)",
                       (native.ABUPS, "End Uses", "Heating", "Electricity", "GJ", "3.60"))
            self.assertEqual(native.tabular(db, "End Uses", "Heating", "Electricity", "GJ"), 3.6)
            with self.assertRaisesRegex(ValueError, "wrong units"):
                native.tabular(db, "End Uses", "Heating", "Electricity", "J")

    def test_hour_and_cost_units_and_absent_price_guard(self):
        case = annual.case_manifest()["main/Seattle/MediumOffice/official_native/B"]
        meters = {f"{use}:{carrier}": [0.0] * 12 for use in native.END_USES for carrier in native.CARRIERS}
        meters["Heating:Electricity"][0] = 1
        csv_bridge = annual.bridge(case, {"meter_monthly_kWh": meters})
        self.assertEqual(len(csv_bridge["monthly_carriers"]), 36)
        self.assertEqual(len(csv_bridge["annual_end_uses"]), 21)
        monthly = csv_bridge["monthly_carriers"][0]
        self.assertEqual((monthly["carrier"], monthly["purchased_kWh"]), ("Electricity", 1.0))
        self.assertEqual(monthly["cost_USD"], monthly["price_USD_kWh"])
        self.assertEqual(csv_bridge["annual_bill_USD"], monthly["cost_USD"])
        meters["Heating:FuelOilNo2"][0] = 1
        with self.assertRaisesRegex(ValueError, "Missing price for nonzero"):
            annual.bridge(case, {"meter_monthly_kWh": meters})


if __name__ == "__main__":
    unittest.main()
