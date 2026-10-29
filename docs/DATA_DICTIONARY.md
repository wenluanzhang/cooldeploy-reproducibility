# Frozen data dictionary

Empty numeric values mean unavailable or not applicable; they are not measured
zero. Structural zero purchased carriers remain explicit in the native records.
Annual monetary amounts are under the frozen reference prices; normalized PV
amounts use treated roof area, not conditioned floor area. Positive A-minus-target
cost differences favor the target. Native column identifiers are preserved even
where the publication uses more precise wording. Units below follow field names;
JSON-valued native reporting fields preserve their original native structure.

### `data/processed/canonical/case_reality_216.csv`

Key: `family,roof`. Rows: 216.

| Field | Units / interpretation |
|---|---|
| `family` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `roof` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `policy` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `executed_idf_sha256` | SHA-256 content identifier; not a bundled source file |
| `weather_sha256` | SHA-256 content identifier; not a bundled source file |
| `prototype_source_sha256` | SHA-256 content identifier; not a bundled source file |
| `executable_sha256` | SHA-256 content identifier; not a bundled source file |
| `schema_sha256` | SHA-256 content identifier; not a bundled source file |
| `engine_reported_version` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `annual_hours` | Hours; heating and cooling retained separately; differences follow column order |
| `roof_area_m2` | Square metres; physical roof is economic denominator |
| `bill_USD` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `numerical` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `numerical_error_bound` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `parent_observation_tier` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `EPW_station` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `EIO_site` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `calendar_start` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `calendar_end` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `warmup_days` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `occupied_unmet` | Hours; heating and cooling retained separately; differences follow column order |
| `actual_temperatures` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `conditioned_or_occupied_zone_count` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `geometry_signature` | SHA-256 content identifier; not a bundled source file |
| `operating_input_signature` | SHA-256 content identifier; not a bundled source file |
| `roof_count` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `SWH_objects` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `prototype_native_EMS_writers` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `roof_only_EMS_writers` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `EnergyPlus_reported_source_revision` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `city` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `native_configuration` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `native_HVAC` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `occupied_heating_unmet` | Hours; heating and cooling retained separately; differences follow column order |
| `occupied_cooling_unmet` | Hours; heating and cooling retained separately; differences follow column order |

### `data/processed/canonical/pair_rebilling_108.csv`

Key: `family,pair`. Rows: 108.

| Field | Units / interpretation |
|---|---|
| `family` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `pair` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `saving_USD` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `allowance_USD_m2` | Signed present-value USD per square metre of physical roof (unless price slope explicitly stated) |
| `roof_area_m2` | Square metres; physical roof is economic denominator |
| `PV` | Annuity sum of discounted annual payments; 20 years / 5% for reference |
| `Heating_saving_USD` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `Cooling_saving_USD` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `Fans_saving_USD` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `Pumps_saving_USD` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `HeatRejection_saving_USD` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `Humidification_saving_USD` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `HeatRecovery_saving_USD` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `occupied_heating_unmet_delta` | Hours; heating and cooling retained separately; differences follow column order |
| `occupied_cooling_unmet_delta` | Hours; heating and cooling retained separately; differences follow column order |
| `numerical_A` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `numerical_target` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |

### `data/processed/canonical/static_54.csv`

Key: `family`. Rows: 54.

| Field | Units / interpretation |
|---|---|
| `family` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `saving_0_minus_A_USD` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `allowance_0_minus_A_USD_m2` | Signed present-value USD per square metre of physical roof (unless price slope explicitly stated) |

### `data/processed/canonical/monthly_native_rebilling.csv`

Key: `family,roof,month,carrier`. Rows: 7776.

| Field | Units / interpretation |
|---|---|
| `family` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `roof` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `month` | Calendar month 1–12 |
| `carrier` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `purchased_kWh` | kWh purchased carrier; annual or monthly as named |
| `price_USD_kWh` | Frozen USD per kWh purchased carrier; empty rate only where carrier use is zero |
| `cost_USD` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |

### `data/processed/canonical/family_carrier_price_162.csv`

Key: `family,carrier`. Rows: 162.

| Field | Units / interpretation |
|---|---|
| `family` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `carrier` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `sector` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `frozen_price` | Frozen USD per kWh purchased carrier; empty rate only where carrier use is zero |
| `independent_price_table` | Frozen USD per kWh purchased carrier; empty rate only where carrier use is zero |
| `window_start` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `window_end` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `state` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `geography` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `proxy` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |

### `data/processed/canonical/weather_prototype_54.csv`

Key: `family`. Rows: 54.

| Field | Units / interpretation |
|---|---|
| `family` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `actual_EPW` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `sha256` | SHA-256 content identifier; not a bundled source file |
| `EPW_station` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `instantiated_EIO_site` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `prototype_source` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `source_sha256` | SHA-256 content identifier; not a bundled source file |

### `data/processed/canonical/numerical_and_service_216.csv`

Key: `family,roof`. Rows: 216.

| Field | Units / interpretation |
|---|---|
| `family` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `roof` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `configured_timestep` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `SQL_reported_steps_per_hour` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `building_load_tolerance` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `building_temperature_tolerance` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `configured_maximum_warmup_days` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `configured_minimum_warmup_days` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `observed_warmup_days` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `simulation_control` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `runperiod` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `convergence_limits` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `native_time_interval_groups` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `native_calendar_report` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `actual_HVAC_system_timestep_observation` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `nominal_people_zones` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `conditioned_equipment_connection_zones` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `all_zone_floor_areas` | Square metres; physical roof is economic denominator |
| `occupied_heating_unmet` | Hours; heating and cooling retained separately; differences follow column order |
| `occupied_cooling_unmet` | Hours; heating and cooling retained separately; differences follow column order |
| `numerical` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |

### `data/processed/canonical/price_40_means.csv`

Key: `see header`. Rows: 40.

| Field | Units / interpretation |
|---|---|
| `state` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `sector` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `carrier` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `n` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `reconstructed_mean` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `frozen_mean` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `residual` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `source` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `source_sha256` | SHA-256 content identifier; not a bundled source file |
| `window_start` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `window_end` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |

### `data/processed/economics/native_carrier_coefficients_108.csv`

Key: `family,target_roof`. Rows: 108.

| Field | Units / interpretation |
|---|---|
| `family` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `city` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `native_configuration` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `native_branch_tag` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `reference_roof` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `target_roof` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `roof_area_m2` | Square metres; physical roof is economic denominator |
| `PV_ref` | Annuity sum of discounted annual payments; 20 years / 5% for reference |
| `accepted_delta_C_ref_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `accepted_allowance_USD_m2` | Signed present-value USD per square metre of physical roof (unless price slope explicitly stated) |
| `E_A_electricity_kWh_year` | kWh purchased carrier; annual or monthly as named |
| `E_target_electricity_kWh_year` | kWh purchased carrier; annual or monthly as named |
| `delta_E_electricity_kWh_year` | kWh purchased carrier; annual or monthly as named |
| `p0_electricity_USD_kWh` | Frozen USD per kWh purchased carrier; empty rate only where carrier use is zero |
| `D_electricity_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `carrier_evidence_electricity` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `price_sector_electricity` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `price_window_start_electricity` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `price_window_end_electricity` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `price_geography_electricity` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `price_proxy_electricity` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `E_A_natural_gas_kWh_year` | kWh purchased carrier; annual or monthly as named |
| `E_target_natural_gas_kWh_year` | kWh purchased carrier; annual or monthly as named |
| `delta_E_natural_gas_kWh_year` | kWh purchased carrier; annual or monthly as named |
| `p0_natural_gas_USD_kWh` | Frozen USD per kWh purchased carrier; empty rate only where carrier use is zero |
| `D_natural_gas_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `carrier_evidence_natural_gas` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `price_sector_natural_gas` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `price_window_start_natural_gas` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `price_window_end_natural_gas` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `price_geography_natural_gas` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `price_proxy_natural_gas` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `E_A_fuel_oil_no2_kWh_year` | kWh purchased carrier; annual or monthly as named |
| `E_target_fuel_oil_no2_kWh_year` | kWh purchased carrier; annual or monthly as named |
| `delta_E_fuel_oil_no2_kWh_year` | kWh purchased carrier; annual or monthly as named |
| `p0_fuel_oil_no2_USD_kWh` | Frozen USD per kWh purchased carrier; empty rate only where carrier use is zero |
| `D_fuel_oil_no2_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `carrier_evidence_fuel_oil_no2` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `price_sector_fuel_oil_no2` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `price_window_start_fuel_oil_no2` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `price_window_end_fuel_oil_no2` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `price_geography_fuel_oil_no2` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `price_proxy_fuel_oil_no2` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `delta_C_from_carriers_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `allowance_from_carriers_USD_m2` | Signed present-value USD per square metre of physical roof (unless price slope explicitly stated) |
| `Heating_saving_USD` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `Heating_PV_contribution_USD_m2` | Signed present-value USD per square metre of physical roof (unless price slope explicitly stated) |
| `Cooling_saving_USD` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `Cooling_PV_contribution_USD_m2` | Signed present-value USD per square metre of physical roof (unless price slope explicitly stated) |
| `Fans_saving_USD` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `Fans_PV_contribution_USD_m2` | Signed present-value USD per square metre of physical roof (unless price slope explicitly stated) |
| `Pumps_saving_USD` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `Pumps_PV_contribution_USD_m2` | Signed present-value USD per square metre of physical roof (unless price slope explicitly stated) |
| `HeatRejection_saving_USD` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `HeatRejection_PV_contribution_USD_m2` | Signed present-value USD per square metre of physical roof (unless price slope explicitly stated) |
| `Humidification_saving_USD` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `Humidification_PV_contribution_USD_m2` | Signed present-value USD per square metre of physical roof (unless price slope explicitly stated) |
| `HeatRecovery_saving_USD` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `HeatRecovery_PV_contribution_USD_m2` | Signed present-value USD per square metre of physical roof (unless price slope explicitly stated) |
| `numerical_A` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `numerical_target` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `numerical_error_bound_A` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `numerical_error_bound_target` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `occupied_heating_unmet_A_hours` | Hours; heating and cooling retained separately; differences follow column order |
| `occupied_heating_unmet_target_hours` | Hours; heating and cooling retained separately; differences follow column order |
| `occupied_cooling_unmet_A_hours` | Hours; heating and cooling retained separately; differences follow column order |
| `occupied_cooling_unmet_target_hours` | Hours; heating and cooling retained separately; differences follow column order |
| `occupied_heating_unmet_delta` | Hours; heating and cooling retained separately; differences follow column order |
| `occupied_cooling_unmet_delta` | Hours; heating and cooling retained separately; differences follow column order |
| `service_equivalence` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `installed_reference_policy` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `pair_source` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `monthly_source` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |

### `data/processed/economics/native_price_break_even_boundaries_108.csv`

Key: `family,target_roof,carrier`. Rows: 324.

| Field | Units / interpretation |
|---|---|
| `family` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `city` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `native_configuration` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `native_branch_tag` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `reference_roof` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `target_roof` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `carrier` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `carrier_slug` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `D_q_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `other_carriers_at_1_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `lambda_star` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `boundary_defined` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `positive_price_crossing` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `boundary_status` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `slope_USD_m2_per_multiplier` | Signed present-value USD per square metre of physical roof (unless price slope explicitly stated) |
| `other_carrier_multipliers` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `multiplier_domain` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `roof_area_m2` | Square metres; physical roof is economic denominator |
| `PV_ref` | Annuity sum of discounted annual payments; 20 years / 5% for reference |
| `numerical_A` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `numerical_target` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `numerical_error_bound_A` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `numerical_error_bound_target` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `occupied_heating_unmet_A_hours` | Hours; heating and cooling retained separately; differences follow column order |
| `occupied_heating_unmet_target_hours` | Hours; heating and cooling retained separately; differences follow column order |
| `occupied_cooling_unmet_A_hours` | Hours; heating and cooling retained separately; differences follow column order |
| `occupied_cooling_unmet_target_hours` | Hours; heating and cooling retained separately; differences follow column order |
| `occupied_heating_unmet_delta` | Hours; heating and cooling retained separately; differences follow column order |
| `occupied_cooling_unmet_delta` | Hours; heating and cooling retained separately; differences follow column order |
| `service_equivalence` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `installed_reference_policy` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |

### `data/processed/economics/native_PV_headroom_108x5.csv`

Key: `family,target_roof,setting`. Rows: 540.

| Field | Units / interpretation |
|---|---|
| `family` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `city` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `native_configuration` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `native_branch_tag` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `reference_roof` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `target_roof` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `setting` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `horizon_years` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `real_discount_rate` | Dimensionless prescribed fraction / native reported or inferred fraction, as named |
| `PV` | Annuity sum of discounted annual payments; 20 years / 5% for reference |
| `roof_area_m2` | Square metres; physical roof is economic denominator |
| `delta_C_ref_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `allowance_USD_m2` | Signed present-value USD per square metre of physical roof (unless price slope explicitly stated) |
| `reference_allowance_USD_m2` | Signed present-value USD per square metre of physical roof (unless price slope explicitly stated) |
| `change_from_reference_USD_m2` | Signed present-value USD per square metre of physical roof (unless price slope explicitly stated) |
| `signed_headroom_before_incremental_service_USD_m2` | Signed present-value USD per square metre of physical roof (unless price slope explicitly stated) |
| `accounting_only` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `numerical_A` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `numerical_target` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `numerical_error_bound_A` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `numerical_error_bound_target` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `occupied_heating_unmet_A_hours` | Hours; heating and cooling retained separately; differences follow column order |
| `occupied_heating_unmet_target_hours` | Hours; heating and cooling retained separately; differences follow column order |
| `occupied_cooling_unmet_A_hours` | Hours; heating and cooling retained separately; differences follow column order |
| `occupied_cooling_unmet_target_hours` | Hours; heating and cooling retained separately; differences follow column order |
| `occupied_heating_unmet_delta` | Hours; heating and cooling retained separately; differences follow column order |
| `occupied_cooling_unmet_delta` | Hours; heating and cooling retained separately; differences follow column order |
| `service_equivalence` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `installed_reference_policy` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |

### `data/processed/economics/winter_availability_native_60x4.csv`

Key: `family,target_roof,retained_function_fraction`. Rows: 240.

| Field | Units / interpretation |
|---|---|
| `family` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `city` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `native_configuration` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `native_branch_tag` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `reference_roof` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `target_roof` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `retained_function_fraction` | Dimensionless prescribed fraction / native reported or inferred fraction, as named |
| `delta_C_ref_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `full_year_unmasked_monthly_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `cold_season_signed_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `non_cold_season_signed_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `masked_annual_signed_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `PV` | Annuity sum of discounted annual payments; 20 years / 5% for reference |
| `roof_area_m2` | Square metres; physical roof is economic denominator |
| `masked_allowance_USD_m2` | Signed present-value USD per square metre of physical roof (unless price slope explicitly stated) |
| `reference_allowance_USD_m2` | Signed present-value USD per square metre of physical roof (unless price slope explicitly stated) |
| `change_from_a1_USD_m2` | Signed present-value USD per square metre of physical roof (unless price slope explicitly stated) |
| `change_from_accepted_reference_USD_m2` | Signed present-value USD per square metre of physical roof (unless price slope explicitly stated) |
| `cold_season_months` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `hypothetical_mask_accounting_only` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `mask_warning` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `numerical_A` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `numerical_target` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `numerical_error_bound_A` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `numerical_error_bound_target` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `occupied_heating_unmet_A_hours` | Hours; heating and cooling retained separately; differences follow column order |
| `occupied_heating_unmet_target_hours` | Hours; heating and cooling retained separately; differences follow column order |
| `occupied_cooling_unmet_A_hours` | Hours; heating and cooling retained separately; differences follow column order |
| `occupied_cooling_unmet_target_hours` | Hours; heating and cooling retained separately; differences follow column order |
| `occupied_heating_unmet_delta` | Hours; heating and cooling retained separately; differences follow column order |
| `occupied_cooling_unmet_delta` | Hours; heating and cooling retained separately; differences follow column order |
| `service_equivalence` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `installed_reference_policy` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |

### `data/processed/width/matched_54_width_comparisons.csv`

Key: `family`. Rows: 54.

| Field | Units / interpretation |
|---|---|
| `family` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `city` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `building` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `system` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `C_0_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `C_A_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `C_Bbroad_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `C_Bsharp_USD_year` | SHA-256 content identifier; not a bundled source file |
| `C_C_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `P_Bbroad_USD_m2` | Signed present-value USD per square metre of physical roof (unless price slope explicitly stated) |
| `P_Bsharp_USD_m2` | SHA-256 content identifier; not a bundled source file |
| `sharp_minus_broad_USD_m2` | SHA-256 content identifier; not a bundled source file |
| `A_minus_Bbroad_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `A_minus_Bsharp_USD_year` | SHA-256 content identifier; not a bundled source file |
| `A_relative_sign_flip` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `M_broad_USD_m2` | Signed present-value USD per square metre of physical roof (unless price slope explicitly stated) |
| `M_sharp_USD_m2` | SHA-256 content identifier; not a bundled source file |
| `C_minus_Bbroad_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `C_minus_Bsharp_USD_year` | SHA-256 content identifier; not a bundled source file |
| `B_C_ranking_reversal` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `B_C_sign_convention` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `physical_roof_area_m2` | Square metres; physical roof is economic denominator |
| `PV_factor` | Annuity sum of discounted annual payments; 20 years / 5% for reference |
| `fragile_sign_qualification` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `absolute_minimum_economic_margin_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `annual_error_bound_available` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `equal_service_established` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `A_minus_Bbroad_Heating_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `A_minus_Bbroad_Cooling_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `A_minus_Bbroad_Fans_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `A_minus_Bbroad_Pumps_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `A_minus_Bbroad_HeatRejection_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `A_minus_Bbroad_Humidification_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `A_minus_Bbroad_HeatRecovery_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `A_minus_Bsharp_Heating_USD_year` | SHA-256 content identifier; not a bundled source file |
| `A_minus_Bsharp_Cooling_USD_year` | SHA-256 content identifier; not a bundled source file |
| `A_minus_Bsharp_Fans_USD_year` | SHA-256 content identifier; not a bundled source file |
| `A_minus_Bsharp_Pumps_USD_year` | SHA-256 content identifier; not a bundled source file |
| `A_minus_Bsharp_HeatRejection_USD_year` | SHA-256 content identifier; not a bundled source file |
| `A_minus_Bsharp_Humidification_USD_year` | SHA-256 content identifier; not a bundled source file |
| `A_minus_Bsharp_HeatRecovery_USD_year` | SHA-256 content identifier; not a bundled source file |
| `width_change_Heating_saving_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `width_change_Cooling_saving_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `width_change_Fans_saving_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `width_change_Pumps_saving_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `width_change_HeatRejection_saving_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `width_change_Humidification_saving_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `width_change_HeatRecovery_saving_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `0_occupied_heating_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `0_occupied_cooling_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `0_numerical` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `0_minus_A_occupied_heating_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `0_minus_B_occupied_heating_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `0_minus_C_occupied_heating_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `0_minus_A_occupied_cooling_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `0_minus_B_occupied_cooling_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `0_minus_C_occupied_cooling_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `A_occupied_heating_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `A_occupied_cooling_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `A_numerical` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `A_minus_A_occupied_heating_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `A_minus_B_occupied_heating_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `A_minus_C_occupied_heating_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `A_minus_A_occupied_cooling_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `A_minus_B_occupied_cooling_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `A_minus_C_occupied_cooling_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `B_occupied_heating_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `B_occupied_cooling_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `B_numerical` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `B_minus_A_occupied_heating_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `B_minus_B_occupied_heating_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `B_minus_C_occupied_heating_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `B_minus_A_occupied_cooling_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `B_minus_B_occupied_cooling_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `B_minus_C_occupied_cooling_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `C_occupied_heating_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `C_occupied_cooling_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `C_numerical` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `C_minus_A_occupied_heating_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `C_minus_B_occupied_heating_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `C_minus_C_occupied_heating_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `C_minus_A_occupied_cooling_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `C_minus_B_occupied_cooling_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `C_minus_C_occupied_cooling_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `Bsharp_occupied_heating_unmet_h` | SHA-256 content identifier; not a bundled source file |
| `Bsharp_occupied_cooling_unmet_h` | SHA-256 content identifier; not a bundled source file |
| `Bsharp_numerical` | SHA-256 content identifier; not a bundled source file |
| `Bsharp_minus_A_occupied_heating_unmet_h` | SHA-256 content identifier; not a bundled source file |
| `Bsharp_minus_B_occupied_heating_unmet_h` | SHA-256 content identifier; not a bundled source file |
| `Bsharp_minus_C_occupied_heating_unmet_h` | SHA-256 content identifier; not a bundled source file |
| `Bsharp_minus_A_occupied_cooling_unmet_h` | SHA-256 content identifier; not a bundled source file |
| `Bsharp_minus_B_occupied_cooling_unmet_h` | SHA-256 content identifier; not a bundled source file |
| `Bsharp_minus_C_occupied_cooling_unmet_h` | SHA-256 content identifier; not a bundled source file |

### `data/processed/width/illustrative_native_cases.csv`

Key: `family,roof`. Rows: 10.

| Field | Units / interpretation |
|---|---|
| `family` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `roof` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `annual_purchased_HVAC_USD` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `Heating_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `Cooling_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `Fans_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `Pumps_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `HeatRejection_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `Humidification_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `HeatRecovery_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `occupied_heating_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `occupied_cooling_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `numerical` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |

### `data/processed/width/native_day_traces.csv`

Key: `family,native_TimeIndex`. Rows: 288.

| Field | Units / interpretation |
|---|---|
| `family` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `surface` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `Month` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `Day` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `Hour` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `Minute` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `simulation_day` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `native_TimeIndex` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `selection` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `sharp_Ts_C` | SHA-256 content identifier; not a bundled source file |
| `sharp_direct_EMS_input_C` | SHA-256 content identifier; not a bundled source file |
| `sharp_reported_reflectance` | SHA-256 content identifier; not a bundled source file |
| `sharp_reported_emittance_command` | SHA-256 content identifier; not a bundled source file |
| `sharp_state` | SHA-256 content identifier; not a bundled source file |
| `sharp_incident_W_m2` | SHA-256 content identifier; not a bundled source file |
| `sharp_absorbed_W_m2` | SHA-256 content identifier; not a bundled source file |
| `sharp_solar_reflectance_flux_observed` | SHA-256 content identifier; not a bundled source file |
| `broad_Ts_C` | Degrees Celsius; direct/source-inferred tier retained in accompanying fields |
| `broad_source_previous_Ts_C` | Degrees Celsius; direct/source-inferred tier retained in accompanying fields |
| `broad_inferred_reflectance` | Dimensionless prescribed fraction / native reported or inferred fraction, as named |
| `broad_equation_inferred_emittance` | Dimensionless prescribed fraction / native reported or inferred fraction, as named |
| `context_tier` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `sharp_Heating_Electricity_kWh` | SHA-256 content identifier; not a bundled source file |
| `sharp_Heating_NaturalGas_kWh` | SHA-256 content identifier; not a bundled source file |
| `sharp_Cooling_Electricity_kWh` | SHA-256 content identifier; not a bundled source file |
| `sharp_Fans_Electricity_kWh` | SHA-256 content identifier; not a bundled source file |
| `broad_predecessor_known` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |

### `data/processed/width/sharp_native_enduse_costs.csv`

Key: `family,roof,end_use,carrier`. Rows: 5670.

| Field | Units / interpretation |
|---|---|
| `family` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `roof` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `end_use` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `carrier` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `native_cost_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |

### `data/processed/optical/matched_optical_comparisons_108.csv`

Key: `family,condition`. Rows: 108.

| Field | Units / interpretation |
|---|---|
| `family` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `condition` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `A_variant` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `C_variant` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `baseline_CA_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `baseline_CC_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `CA_prime_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `CC_prime_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `delta_CA_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `delta_CC_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `A_minus_C_prime_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `physical_roof_area_m2` | Square metres; physical roof is economic denominator |
| `PV` | Annuity sum of discounted annual payments; 20 years / 5% for reference |
| `baseline_P_USD_m2` | Signed present-value USD per square metre of physical roof (unless price slope explicitly stated) |
| `P_prime_USD_m2` | Signed present-value USD per square metre of physical roof (unless price slope explicitly stated) |
| `delta_P_USD_m2` | Signed present-value USD per square metre of physical roof (unless price slope explicitly stated) |
| `A_relative_sign_flip` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `annual_error_bound_available` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `equal_service_established` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `numerical_A` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `numerical_C` | Degrees Celsius; direct/source-inferred tier retained in accompanying fields |
| `delta_CA_Heating_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `delta_CC_Heating_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `A_minus_C_prime_Heating_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `delta_CA_Cooling_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `delta_CC_Cooling_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `A_minus_C_prime_Cooling_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `delta_CA_Fans_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `delta_CC_Fans_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `A_minus_C_prime_Fans_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `delta_CA_Pumps_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `delta_CC_Pumps_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `A_minus_C_prime_Pumps_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `delta_CA_HeatRejection_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `delta_CC_HeatRejection_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `A_minus_C_prime_HeatRejection_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `delta_CA_Humidification_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `delta_CC_Humidification_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `A_minus_C_prime_Humidification_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `delta_CA_HeatRecovery_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `delta_CC_HeatRecovery_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `A_minus_C_prime_HeatRecovery_USD_year` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `A_occupied_heating_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `delta_A_occupied_heating_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `A_occupied_cooling_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `delta_A_occupied_cooling_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `C_occupied_heating_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `delta_C_occupied_heating_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `C_occupied_cooling_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `delta_C_occupied_cooling_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |

### `data/processed/optical/descriptive_summary.csv`

Key: `condition`. Rows: 6.

| Field | Units / interpretation |
|---|---|
| `condition` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `n_families` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `minimum` | Signed present-value USD per square metre of physical roof (unless price slope explicitly stated) |
| `q25` | Signed present-value USD per square metre of physical roof (unless price slope explicitly stated) |
| `median` | Signed present-value USD per square metre of physical roof (unless price slope explicitly stated) |
| `q75` | Signed present-value USD per square metre of physical roof (unless price slope explicitly stated) |
| `maximum` | Signed present-value USD per square metre of physical roof (unless price slope explicitly stated) |
| `positive_changes` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `negative_changes` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |
| `A_relative_sign_flips` | Original categorical/native reporting value or dimensionless count; see field name and RESULTS_MAP scope |

### `data/processed/optical/native_enduse_costs.csv`

Key: `family,variant,end_use,carrier`. Rows: 3024.

| Field | Units / interpretation |
|---|---|
| `family` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `variant` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `end_use` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `carrier` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `annual_cost_USD` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |
| `annual_kWh` | kWh purchased carrier; annual or monthly as named |

### `data/processed/optical/native_monthly_carriers.csv`

Key: `family,variant,carrier,month`. Rows: 5184.

| Field | Units / interpretation |
|---|---|
| `family` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `variant` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `carrier` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `month` | Calendar month 1–12 |
| `purchased_HVAC_kWh` | kWh purchased carrier; annual or monthly as named |
| `price_USD_kWh` | Frozen USD per kWh purchased carrier; empty rate only where carrier use is zero |
| `cost_USD` | USD/year for annual quantities; USD for a monthly cost; signed difference follows column name |

### `data/processed/optical/service_numerical.csv`

Key: `family,variant`. Rows: 144.

| Field | Units / interpretation |
|---|---|
| `family` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `variant` | Categorical row identifier; family = anchor/building/native HVAC branch |
| `occupied_heating_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `occupied_cooling_unmet_h` | Hours; heating and cooling retained separately; differences follow column order |
| `numerical` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `warmup` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `annual_error_bound_available` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
| `equal_service_established` | Qualification/flag or original native reporting value; no annual error bound or equal-service inference |
