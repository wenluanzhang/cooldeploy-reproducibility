# Provenance and boundaries

Source snapshot: `437871b85d8a93cf6ad8e2c6e3aa767d224023fe`. `FROZEN_INPUTS.json` records SHA-256 for each original
compact source and its portable projection, row counts, keys and supported claim.
Original numerical strings are retained; only private source selectors and
machine paths are omitted and source-model/weather filenames reduced to basenames.
The public source manifest intentionally excludes private audit history.

The downstream native-carrier algebra is isolated in `src/_economics.py` from the
frozen derivation functions. The public CLI independently reconstructs bills from
monthly purchased energy and prices, checks end-use sums and signed normalization,
and compares regenerated carrier/boundary/finance/winter rows with frozen values.
Expected Main plot values retain the accepted numerical backing of Figs. 2–4 and
5A/B; optical statistics are independently reconstructed for Fig. 5C/Table S5.

The case manifest pins the EnergyPlus 26.1.0 build and the final modified IDF
and EPW hashes. Commercial originals are DOE/PNNL ASHRAE 90.1-2022 variants.
Residential originals are DOE/PNNL 2021 IECC detached slab-on-grade variants.
Use the [verified provider links](../simulation/SOURCES.md) to obtain originals
and match the manifest hashes. See the [model preparation guide](../simulation/MODEL_PREPARATION.md)
for the accepted configuration, and the [validation report](REPRODUCIBILITY_REPORT.md)
for the scope of the one locally rerun annual. The exact final IDFs require
an authorized source or independent preparation followed by hash verification.

The controlled optical baseline/new-variant table has 144 contextual rows (36
accepted original A/C years plus 108 separate new annuals). These are not 144
additional canonical years. The near-sharp study has 54 separate new B years.
Their warning/service qualifications remain attached to their own populations.
The displayed scientific claims remain conditional modeled observations.
