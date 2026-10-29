# R1 reproducibility closure

Status: numerical checks PASS; local candidate awaiting author manifest/publication
approval. No EnergyPlus run or raw annual extraction is performed by this release.

| Check | Result |
|---|---|
| Canonical domain | 9 anchors × 6 native systems × 4 roofs = 216 annuals |
| A-minus-B/C contrasts | 108 unique matched comparisons |
| Positive B / C comparisons | 43/54 and 41/54 |
| B cheaper than C | 50/54 |
| Signed medians, PV USD/m² roof | B 1.412527425719486; C 0.6858116472875067 |
| Native Cooling cost contributions | All 108 adverse to adaptation |
| Numerical qualifications | 93/216 NUMERICAL_REVIEW_REQUIRED; retained |
| Native rebilling | 7776 monthly carrier keys; 162 family/carrier price keys |
| Price / financial / winter outputs | 324 analytic roots; 540 financial rows; 240 mask rows |
| Winter positive B counts, retained fractions 1/.75/.5/.25 | 29/29/28/23 of 30 |
| Winter positive C counts | 30/29/24/19 of 30 |
| Near-sharp B sensitivity | 54 separate pairs; no A-relative sign flips; one B/C reversal |
| Optical study | 18 exact families × 6 states = 108 distinct contrasts |
| Optical native closure | 144 contextual baseline/new variants; 5184 monthly rows |
| Main figure numerical backing | Accepted Figs. 2–4 and 5A/B values checked; 5C statistics rebuilt |
| SI backing | Station/area, roof laws, prices, 15 bill/service examples, optical statistics and native traces emitted |

Tested with Python 3.13.8. Validation/table generation/tests require only the
standard library. Optional plotting dependency: matplotlib 3.11.2 (Python 3.11+).
The five standard-library unit tests cover numerical closure/input immutability,
CLI operation from a different working directory, frozen-output protection,
duplicate keys and corrupted-input hash rejection.

Commands:

```sh
python src/reproduce.py validate
python src/reproduce.py tables --output generated
python -m unittest discover -s tests -v
```

The optional `figures` command produces numerical reference plots; it is not a
rebuild of the approved publication artwork. Bulk publication figures were not
regenerated during release preparation. The default tables include backing data
for every panel even where a reference plot is a simplified view.

The full annual simulation environment is not distributed. Fixed installed
equipment does not imply equal delivered service. Occupied heating/cooling unmet
hours remain separate. No annual numerical-error bound, measured coating life,
full installed/maintenance cost, national sampling inference, physical snow
response or environmental LCA is established by this numerical closure.
