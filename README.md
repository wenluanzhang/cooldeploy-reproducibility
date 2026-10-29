# CoolDeploy R1 numerical reproducibility

This candidate reproduces the revised study's **numerical analysis from frozen
processed EnergyPlus outputs**: nine U.S. weather anchors, six native building/HVAC
configurations, roofs 0/A/B/C, 216 canonical annuals and 108 A-minus-B/C comparisons.
It also separates the 54 near-sharp B sensitivity years from the controlled optical
study (18 families, six states, 108 extra annuals and 108 optical contrasts).

Python 3.10+ is required. Validation, table/figure-data regeneration and tests use
only the Python standard library. Start from this directory:

```sh
python src/reproduce.py validate
python src/reproduce.py tables --output generated
python -m unittest discover -s tests -v
# Optional numerical plots; Python 3.11+ and the pinned dependency:
python -m pip install -r requirements.txt
python src/reproduce.py figures --output generated
```

`tables` is the single entry point for all derived numerical tables and figure
backing data. It checks frozen file hashes before computing, writes only under the
selected output directory, and never modifies `data/processed/`. `validate` is
read-only. `figures` draws numerical plots from those tables, not pixel-identical
publication artwork. The publication's approved figures are not rebuilt in place.

## Physical evidence and accounting assumptions

The physical inputs hold installed nominal equipment and prescribed controls
fixed within each family across roofs. Non-HP families use the original0 fixed
implementation; residential HP families use original0-derived numeric child
capacities/flows, with parent initialization source-inferred rather than directly
observed. Fixed inputs do not establish equal delivered service. The canonical
216 annuals retain **93 NUMERICAL_REVIEW_REQUIRED** records; unmet heating/cooling
hours and the absence of an annual numerical-error bound remain explicit.

Costs use native purchased Electricity, NaturalGas and FuelOilNo2 in seven disjoint
end uses (Heating, Cooling, Fans, Pumps, HeatRejection, Humidification,
HeatRecovery). SWH is physically removed from these runs; lighting/plug bills are
excluded. No delivered-load-to-purchased-energy efficiency substitution is used.
Positive signed A-minus-target values mean lower target bills. Normalization uses
physical treated roof area. Twenty years, 5% real discount, stationary annual
savings and frozen carrier prices are accounting assumptions, not measured
product lifetime, complete ownership cost or environmental LCA. The winter mask
is hypothetical common-difference accounting, not a physical snow simulation.

## Scope of reproduction

The numerical closure includes 43/54 positive B and 41/54 positive C comparisons,
B cheaper than C in 50/54, signed medians 1.4125274257 and 0.6858116473 USD/m² roof,
and adverse native Cooling contributions in all 108 canonical comparisons.
See [RESULTS_MAP](docs/RESULTS_MAP.md), [DATA_DICTIONARY](docs/DATA_DICTIONARY.md)
and [PROVENANCE](docs/PROVENANCE.md) for keys, units and limits.

This repository does **not** reproduce EnergyPlus from scratch. The executable,
full IDF/EPW environment, third-party prototype/weather content and raw native
outputs are not bundled. Public source identifiers and hashes are supplied;
independent annual runs require obtaining those inputs and rebuilding the model
boundary and equipment/control policy. No physics is rerun by these commands.

Release status: local candidate awaiting author manifest review and publication
approval. Code/documentation use MIT; project-generated processed data use CC BY
4.0, as selected by the author. See LICENSE, LICENSE_CODE and LICENSE_DATA.
The previous public snapshot is superseded in full;
its historical calculations are not dependencies of this workflow.
