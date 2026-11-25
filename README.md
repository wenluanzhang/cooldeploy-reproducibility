# CoolDeploy R2 reproducibility

Choose the workflow that matches what you want to reproduce.

## A. Reproduce the numerical analysis

Start from the bundled, frozen processed EnergyPlus outputs. Python 3.10+
and its standard library are sufficient.

~~~sh
python src/reproduce.py validate
python src/reproduce.py tables --output generated
python -m unittest discover -s tests -v
~~~

Validation checks 22 frozen inputs and the numerical calculations. The tables
command writes 19 CSVs with results and figure backing data, plus
validation.json. See the [results map](docs/RESULTS_MAP.md) for the manuscript
and supplementary tables and figures that each file supports.

For optional numerical reference plots, use Python 3.11+ and install the pinned
dependency with python -m pip install -r requirements.txt. Then run
python src/reproduce.py figures --output generated. The plots illustrate the
numerical results. Publication artwork is outside the plotting workflow.

## B. Explore the EnergyPlus workflow

Start with the [model preparation guide](simulation/MODEL_PREPARATION.md) and
[pinned source downloads](simulation/SOURCES.md). The [simulation guide](simulation/README.md)
covers installing EnergyPlus 26.1.0, verifying exact inputs, running one annual,
extracting native outputs and comparing with the frozen public references.

The [case manifest](simulation/cases.csv) identifies 216 main simulations, 54
narrow-B sensitivity simulations and 108 additional optical simulations. The
36 original A/C annuals used as optical context are already part of the main
study. The strict runner requires a final modified IDF that matches the
manifest SHA-256. Obtain the original prototypes and weather from their
providers. Access to exact final modified IDFs requires a separate authorized
route or independently prepared files that pass the hash check. The model guide
documents the accepted configuration and the limits of preparation from the
public inputs.

## Validation and interpretation

The [validation report](docs/REPRODUCIBILITY_REPORT.md) distinguishes frozen-data
reproduction, local offline verification of 378 accepted cases and one prior
Seattle Medium Office Case B rerun. Fixed installed equipment leaves room
for different indoor conditions across roofs. The data retain separate occupied
heating and cooling unmet hours and 93 numerical-review flags in the main
study. An annual numerical-error bound and field validation were outside the
verification.

The analysis uses native purchased space-conditioning energy and physical
treated roof area. The 20-year period, 5% real discount rate, stationary annual
savings and prices, and winter-retention mask are accounting assumptions.
See the [data dictionary](docs/DATA_DICTIONARY.md) and [provenance notes](docs/PROVENANCE.md).

Project code and documentation use the [MIT license](LICENSE_CODE).
Project-generated processed data use [CC BY 4.0](LICENSE_DATA).
