# CoolDeploy reproducibility package

This repository contains the analysis code and processed numerical results for
the CoolDeploy study of the additional economic value of temperature-adaptive
radiative roofs relative to a high-performance static radiative-cooling
baseline.

The repository is a reproducibility package for the numerical analysis. It
does not contain manuscript files, supplementary files, publication artwork,
or literature PDFs.

## Scope

The retained analysis evaluates:

- annual operating-cost differences derived from frozen building-energy
  simulation outputs;
- the maximum justifiable additional installed cost of adaptive roofs relative
  to the static radiative-cooling baseline;
- sensitivity to heating technology and conversion efficiency;
- sensitivity to electricity and natural-gas prices;
- present-value assumptions;
- differential service burden;
- cold-season roof availability; and
- controlled optical-function changes.

The quantitative analysis is restricted to the modeled U.S. cases.

## Current numerical result sets

The current economic analyses are stored in:

- `data/processed/joint_economic_robustness/`
- `data/processed/joint_economic_downstream/`

Files retained elsewhere in `data/processed/`, if any, are included only when
they are direct dependencies of the current analysis.

## Reproducibility

The analysis uses frozen processed building-energy outputs and economic
post-processing. Reproducing the reported economic results does not require
rerunning EnergyPlus unless explicitly documented otherwise.

See the retained analysis scripts and data documentation for the exact inputs,
outputs, and assumptions.

Install Python 3.10 or later with `numpy`, `pandas`, and `pytest`. Run
`pytest -q` to verify the retained results. Run
`python src/rebase_joint_economic_downstream.py` to regenerate the downstream
economic tables from the frozen inputs.

The four files in `data/processed/frozen_physical_inputs/` are project-generated
processed building-energy outputs; no third-party source data are redistributed.
