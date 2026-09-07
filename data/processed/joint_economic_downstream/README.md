# Current-framework deployment-sensitivity derivations

Canonical economics: `../joint_economic_robustness/central_baseline_base_price.csv` and `../joint_economic_robustness/price_levels.csv`.

All calculations are economic-only post-processing of frozen monthly physical outputs; no EnergyPlus simulation is invoked or modified. Service-burden and economic-horizon results use the 19 positive reference decisions (Case B: 7; Case C: 12). Cold-season availability uses 36 adaptive reference decisions (three cities, two buildings, three heating technologies, and two adaptive cases) at each availability level; the tidy output also reports the 18 corresponding Case 0--A comparisons. Each controlled optical state uses 18 Case C reference decisions (three cities, two buildings, and three heating technologies). The optical/availability interaction contains those 18 decisions for each of six optical states and four availability levels.
