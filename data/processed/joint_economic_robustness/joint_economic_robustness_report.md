# Joint economic robustness audit

Uses refreshed official EIA/BLS price evidence and frozen EnergyPlus-derived loads only.

## Decision definition and scope

- The decision metric is the maximum additional installed cost (USD/m2 roof) supported by 20-year discounted operating-cost savings. Positive means economically supported under that parameter combination.
- Physical cooling/heating loads and roof areas are frozen inputs. Electricity and gas prices, cooling COP, and heating efficiency/COP are scenario assumptions; no EnergyPlus model was run.
- H1 uses the analytic ratio R = COP_cooling * gas_price / (eta_gas * electricity_price), with Rcrit = -delta_Qcool / delta_Qheat where delta_Qheat > 0. H2 and H3 use their corresponding COP_cooling/COP_heating and COP_cooling threshold forms.

## Validation

- Original production reconstruction max discrepancy: 3.6e-14 USD/m2.
- Previous conversion-efficiency audit central reconstruction max discrepancy: 0 USD/m2.
- Rows: central=126 (42 static, 84 adaptive); adaptive joint=4368; static joint=2184.

## Updated price evidence

| City | Carrier | P10 | Base recent 12m | P90 | Window | Base outside P10-P90 |
| --- | --- | --- | --- | --- | --- | --- |
| Miami | electricity | 0.1164 | 0.1200 | 0.1310 | 2025-07-01 to 2026-06-01 | False |
| Phoenix | electricity | 0.1235 | 0.1245 | 0.1300 | 2025-07-01 to 2026-06-01 | False |
| Baltimore | electricity | 0.1256 | 0.1659 | 0.1520 | 2025-07-01 to 2026-06-01 | True |
| Seattle | electricity | 0.1078 | 0.1182 | 0.1156 | 2025-07-01 to 2026-06-01 | True |
| Denver | electricity | 0.1254 | 0.1335 | 0.1340 | 2025-07-01 to 2026-06-01 | False |
| Chicago | electricity | 0.1189 | 0.1393 | 0.1356 | 2025-07-01 to 2026-06-01 | True |
| Minneapolis | electricity | 0.1271 | 0.1268 | 0.1400 | 2025-07-01 to 2026-06-01 | True |
| Miami | natural_gas | 0.0417 | 0.0413 | 0.0532 | 2025-01-01 to 2025-12-01 | True |
| Phoenix | natural_gas | 0.0318 | 0.0321 | 0.0448 | 2025-07-01 to 2026-06-01 | False |
| Baltimore | natural_gas | 0.0469 | 0.0493 | 0.0587 | 2024-05-01 to 2025-04-01 | False |
| Seattle | natural_gas | 0.0385 | 0.0500 | 0.0475 | 2025-03-01 to 2026-02-01 | True |
| Denver | natural_gas | 0.0317 | 0.0329 | 0.0470 | 2025-07-01 to 2026-06-01 | False |
| Chicago | natural_gas | 0.0407 | 0.0451 | 0.0581 | 2025-07-01 to 2026-06-01 | False |
| Minneapolis | natural_gas | 0.0287 | 0.0350 | 0.0458 | 2024-10-01 to 2025-09-01 | False |

## Central base-price baseline

| Comparison | Positive | Nonpositive | Min | Median | Mean | Max |
| --- | --- | --- | --- | --- | --- | --- |
| B | 7 | 35 | -9.5596 | -1.7766 | -2.3075 | 2.8812 |
| C | 12 | 30 | -4.2135 | -0.5766 | -0.7596 | 3.1621 |
| Static 0-A | 38 | 4 | -0.8222 | 2.6468 | 2.5695 | 6.5864 |
- Central B>C combinations: Chicago / SmallOffice / H3_resistance; Minneapolis / SmallOffice / H3_resistance.

## Full joint matrix

| Case | N | Positive | Fraction | Min | Median | Max |
| --- | --- | --- | --- | --- | --- | --- |
| B | 2184 | 169 | 0.077 | -11.8366 | -1.9471 | 4.2952 |
| C | 2184 | 383 | 0.175 | -5.2853 | -0.6968 | 4.1135 |

- C>B in 2151/2184 matched parameter combinations; B>C in 33. Exact B>C keys are retained in the matrix.
- Cooling contribution positive in 0/4368 adaptive rows.

## Decision robustness

- Robustly positive=17; robustly nonpositive=45; jointly sensitive=22.
- Price-only sensitive at central efficiencies=6; efficiency-sensitive at Base prices=16; both-interaction-required=4.
- H1 central positive rows=1/28; H1 full joint positive rows=234/1512.

## Threshold checks

- H1/H2/H3 threshold prediction failures: 0/0/0.
- H1 boundaries crossed within the tested range: Baltimore / MediumOffice / C; Baltimore / SmallOffice / C; Chicago / MediumOffice / B; Chicago / MediumOffice / C; Chicago / SmallOffice / B; Chicago / SmallOffice / C; Denver / SmallOffice / C; Minneapolis / MediumOffice / C; Minneapolis / SmallOffice / B; Minneapolis / SmallOffice / C; Seattle / SmallOffice / C.
- H1 threshold undefined because delta_Qheat <= 0: Miami / SmallOffice / B; Miami / SmallOffice / C.

## Interpretation and limits

- Miami and Phoenix have 0/1248 positive adaptive joint rows; their robust nonpositive classifications therefore remain unchanged across the tested joint grid.
- Jointly sensitive H1 decisions are: Baltimore / MediumOffice / C; Baltimore / SmallOffice / C; Chicago / MediumOffice / B; Chicago / MediumOffice / C; Chicago / SmallOffice / B; Chicago / SmallOffice / C; Denver / SmallOffice / C; Minneapolis / MediumOffice / C; Minneapolis / SmallOffice / B; Minneapolis / SmallOffice / C; Seattle / SmallOffice / C.
- H2/H3 prices scale the all-electric operating-cost difference without changing its sign; the script enforces this price-only invariance. H1 can change sign because the electricity-to-gas price ratio interacts with conversion efficiency.
- Cooling contribution is never positive (0/4368 rows); any positive result is created by the heating-side operating-cost effect overcoming that cooling penalty.
- This is a service-life economic sensitivity analysis, not an environmental LCA. Findings apply only to the stated price history, CPI basis, building archetypes, and scenario ranges.
