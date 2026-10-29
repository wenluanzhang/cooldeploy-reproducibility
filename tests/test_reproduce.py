"""Release smoke, mutation and output-isolation tests; never run EnergyPlus."""
import hashlib
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
import reproduce


class ReproducibilityTests(unittest.TestCase):
    def test_claim_closure_and_no_input_writes(self):
        paths=list((ROOT/'data').rglob('*'))
        before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p.is_file()}
        data,derived,report=reproduce.validate()
        self.assertEqual(report['canonical_annuals'],216)
        self.assertEqual(report['B_positive'],43)
        self.assertEqual(report['C_positive'],41)
        self.assertEqual(report['optical_states'],6)
        self.assertEqual(len(derived['financial']),540)
        self.assertEqual(before,{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p.is_file()})

    def test_cli_tables_portable_cwd(self):
        with tempfile.TemporaryDirectory() as d:
            run=subprocess.run([sys.executable,str(ROOT/'src/reproduce.py'),'tables','--output',d],cwd=d,capture_output=True,text=True)
            self.assertEqual(run.returncode,0,run.stderr)
            self.assertEqual(len(reproduce.read(Path(d)/'main_figure5c_optical_and_SI_tableS5.csv')),6)
            self.assertEqual(len(reproduce.read(Path(d)/'SI_figuresS3_S4_native_traces.csv')),288)

    def test_protect_frozen_output_locations(self):
        for path in [ROOT,ROOT/'data',ROOT/'data/processed/canonical',ROOT/'src',ROOT/'docs']:
            with self.subTest(path=path),self.assertRaises(ValueError):reproduce.output_directory(path)

    def test_duplicate_key_rejected(self):
        with self.assertRaises(ValueError):reproduce.index([{'id':'a'},{'id':'a'}],('id',))

    def test_hash_corruption_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'docs').mkdir();(root/'data').mkdir()
            (root/'data/bad.csv').write_text('changed',encoding='utf-8')
            (root/'docs/FROZEN_INPUTS.json').write_text('[{"public_path":"data/bad.csv","public_sha256":"wrong"}]',encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'Frozen hash changed'):reproduce.validate(root)


if __name__=='__main__':unittest.main()
