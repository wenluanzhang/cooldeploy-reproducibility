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

Engine identifiers in the case file record EnergyPlus 26.1.0 and content hashes;
these are provenance, not an included or independently reproduced simulator.
Weather identifiers are the TMY3 station basenames in `weather_prototype_54.csv`.
Commercial sources are ASHRAE 90.1-2022 DOE/PNNL prototype variants; residences use
DOE/PNNL 2021 IECC detached slab-on-grade variants. Obtain originals from the
[DOE prototype portal](https://www.energycodes.gov/prototype-building-models)
and [EnergyPlus weather portal](https://energyplus.net/weather), then match the
provided hashes/identifiers. These links identify providers; no third-party
redistribution permission or exact regenerated-IDF availability is implied.

The controlled optical baseline/new-variant table has 144 contextual rows (36
accepted original A/C years plus 108 separate new annuals). These are not 144
additional canonical years. The near-sharp study has 54 separate new B years.
Their warning/service qualifications remain attached to their own populations.
The displayed scientific claims remain conditional modeled observations.
