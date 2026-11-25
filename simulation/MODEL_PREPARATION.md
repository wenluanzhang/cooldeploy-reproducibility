# Model preparation guide

This guide describes the accepted CoolDeploy R2 inputs (ECM-D-26-11398,
Main Methods and SI Sections S1`S3, S5 and S7). Use it to inspect the modeling
decisions or implement them independently. The verified prototype-to-final
preparation chain is unavailable here. An independently prepared IDF is
eligible for the [strict runner](README.md) once its SHA-256 matches the
[case manifest](cases.csv).

## Base model, equipment and controls

1. Select the location, configuration, roof and population in the
   [case manifest](cases.csv). The original prototype's design location can
   differ from the case's weather station. The official office IDFs use
   version 22.1 and the residential IDFs use 23.1. The accepted inputs use
   IDF version 26.1 and EnergyPlus 26.1.0, build 6f2e40d102. The version
   updater is an aid for local migration. The study's historical preparation
   and serialization require additional steps. [Pinned downloads](SOURCES.md)
2. Retain prototype geometry, non-roof envelope, internal gains, schedules,
   thermostat controls and HVAC topology. The study removes service-water-
   heating (SWH) equipment and its coupled thermal, hydraulic, air-side and
   control connections. The native Water Systems report shows zero purchased
   energy. Retain lighting, plug and occupant heat gains in the building
   model. The HVAC bill excludes lighting and plug energy.
3. Use the same installed HVAC capacities, airflows, operating inputs and
   performance curves across the four roofs within each family. For 45
   non-residential-heat-pump families, the reference is the historical
   original Case 0 equipment sizing. Inspect the operative fields of
   `AirLoopHVAC`, `AirTerminal:SingleDuct:VAV:Reheat`,
   `Fan:VariableVolume` and the heating and cooling coils as applicable.
   Design sizing calculations can still report recommended sizes.
4. For the nine residential heat-pump families, original Case 0 supplies
   numerical child-coil capacities and flows, including rated fields of
   `Coil:Cooling:DX:SingleSpeed` and `Coil:Heating:DX:SingleSpeed`.
   Initialization of the `AirLoopHVAC:UnitaryHeatPump:AirToAir` parent is
   source-inferred. Historical internal parent sizing remains unverified.
   Some inactive defrost or reheat fields retain `Autosize`. The residential
   heat pump has electric supplemental heat. The Small Office heat pump uses
   `Coil:Heating:Fuel` with `NaturalGas` for supplemental heat.
5. Preserve `ZoneControl:Thermostat` bindings, the heating and cooling
   schedules referenced by `ThermostatSetpoint:DualSetpoint`, and the
   original HVAC and lighting EMS logic where present. Preserve the
   schedules and setpoints across roofs in each family. The added EMS
   acts on roof materials only. Delivered indoor conditions can differ
   across roofs.

## Roof properties and switching

Trace each exterior `BuildingSurface:Detailed` roof face through its
`Construction` to the outside `Material` layer. Include pitched and garage
roof surfaces where present in the physical treated roof area. The following
are prescribed broadband model inputs.

| Roof | Solar reflectance R | Thermal emittance ` |
| --- | ---: | ---: |
| 0, conventional | Prototype value | Prototype value |
| A, static radiative cooling | 0.95 | 0.95 |
| B, adaptive solar and thermal | 0.05 + 0.90f | 0.10 + 0.85f |
| C, adaptive thermal | 0.75 | 0.20 + 0.70f |

Use solar absorptance `1 ` R`. For the previous zone step exterior face
temperature, the broad switching fraction is
`f = clip((T_previous ` 19 `C) / 8 `C, 0, 1)`, with a 23 `C midpoint.

- **B.** An `EnergyManagementSystem:Sensor` reads `Surface Outside Face Temperature`.
  The EMS program runs via `EnergyManagementSystem:ProgramCallingManager` at
  `BeginZoneTimestepBeforeInitHeatBalance`. Material actuators set surface
  property solar and thermal absorptance. The source-backed timing uses the
  preceding zone timestep. The first predecessor is missing from the annual
  output and excluded only from diagnostics that require it.
- **C.** `MaterialProperty:VariableAbsorptance` uses `SurfaceTemperature` with a
  `Table:Lookup` for thermal absorptance. Its `Table:IndependentVariable`
  uses linear interpolation over 19`27 `C and constant extrapolation.
  Solar reflectance stays fixed. C's timing and thermal response are
  inferred with source support. Direct emittance and timing readbacks
  were unavailable.

## Annual settings and reporting

- Use the case's `RunPeriod` and `SimulationControl`, including the annual
  weather-file period. The recorded clock spans January 1`December 31,
  with 8,760 hours and six zone steps per hour in `Timestep`. Offices and
  residences use different holiday/daylight-saving flags. The
  [numerical and service CSV](../data/processed/canonical/numerical_and_service_216.csv)
  records the flags by family and roof.
- In `Building`, the load convergence tolerance is 0.04. The temperature
  tolerance is 0.2 `C for offices and 0.4 `C for residences. The minimum
  warmup is six days. The maximum is 25 days for residences and 25 or 50
  for offices. Use the case-level record. The office `ConvergenceLimits`
  specifies a one-minute minimum system timestep and a 20-iteration HVAC
  cap. Residences use the version defaults. Actual system timesteps were
  outside the verification.
- Preserve `Output:SQLite` with `SimpleAndTabular`, monthly `Output:Meter`
  requests and annual utility and comfort summary reports. The
  [extraction guide](README.md#extraction-and-comparison) gives native HVAC
  meter names, units and checks. Keep occupied heating and cooling unmet
  hours separate and retain native warnings.

## Sensitivities and tested example

The 216 main annuals cover nine locations, six configurations and four
roofs. The 54 narrow-B cases change the switching bounds to 22.99`23.01 `C
and retain the midpoint and optical endpoints. The 108 additional optical
annuals cover the six configurations in Chicago, Denver and Minneapolis.
Per family, they include two C low-temperature emittance changes (0.35 or
0.50, high endpoint 0.90), two C reflectance changes (0.70 or 0.65), and
two A reflectance changes (0.90 or 0.85). The paired A/C tests reuse the
corresponding C reflectance variants. The 36 original A/C context years
belong to the 216 main cases. Winter retention, energy prices and
financial scenarios are downstream calculations.

For the tested case, look up `main/Seattle/MediumOffice/official_native/B`
in the [manifest](cases.csv). Its original model is
`ASHRAE901_OfficeMedium_STD2022_Seattle.idf`, the EPW station is Seattle`Tacoma
727930 and the treated roof face is `Building_Roof`. The exact executed
Case B IDF has its own manifest hash. Use the
[Seattle run and comparison commands](README.md#check-run-extract-and-compare-one-case)
with that file. The [results map](../docs/RESULTS_MAP.md) links the frozen
comparisons, service records and diagnostic traces.
