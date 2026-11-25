# CoolDeploy R2 validation report

The release provides numerical reproduction from frozen processed data and
documents the EnergyPlus modeling, execution and extraction workflow. The
validation used Windows 11 x86-64, Python 3.13.8 and EnergyPlus 26.1.0, build
6f2e40d102. The numerical commands and tests use Python's standard library.

| Check | Scope and result |
| --- | --- |
| Frozen public inputs | 22 manifest entries passed the hash and numerical checks. |
| Public numerical regeneration | 19 regenerated CSVs and the validation summary matched the accepted public baseline byte for byte. |
| Automated tests | All 10 passed, including the five original numerical tests and five simulation-workflow tests. |
| Local exact-input checks | All 378 accepted final IDF and EPW pairs matched the case manifest. |
| Local archived-output extraction | All 378 retained native outputs matched the corresponding frozen public references, covering 216 main, 54 narrow-B and 108 additional optical simulations. |
| Prior annual rerun | One accepted annual was rerun, Seattle Medium Office Case B. It completed 8,760 hours with 97 warnings and zero severe errors. All 355 archive-assisted checks passed. |
| Public-reference comparison | The same Seattle rerun's extracted result passed 99 checks against the checkout's public data, without the accepted native archive. |

The Seattle public-reference check covered case identity, annual hours, treated
roof area, occupied heating and cooling unmet hours, purchased carrier energy,
end-use costs and the annual HVAC bill. The 355-check comparison also used
the accepted native archive for the exact hourly clock, individual roof-face
data, monthly end-use meters, warning signatures and roof-temperature sequence
and inferred switching states. Those additional comparisons require the
original native outputs.

## Numerical closure

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

## Run the checks available from this repository

~~~sh
python src/reproduce.py validate
python src/reproduce.py tables --output generated
python -m unittest discover -s tests -v
~~~

The [simulation guide](../simulation/README.md) shows how to compare your own
extracted outputs with the public reference data. The public files support
the downstream commands immediately. Exact final modified IDFs and the native
output archive are outside this distribution. The pinned original prototypes
and EPWs are available from their [providers](../simulation/SOURCES.md).
Download and verification of the original files do not establish an exact
final-model reconstruction.

The Seattle rerun retains its numerical-review classification. The canonical
records retain 93 numerical-review flags and separate occupied heating and
cooling unmet hours. Fixed installed equipment is compatible with different
indoor conditions. The modeled results provide no annual numerical-error
bound or field validation.
