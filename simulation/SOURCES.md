# Input sources and third-party notices

| Material | Source and attribution | Candidate treatment |
| --- | --- | --- |
| Commercial prototypes | U.S. DOE and Pacific Northwest National Laboratory, [Commercial Prototype Building Models](https://www.energycodes.gov/prototype-building-models), ASHRAE 90.1-2022 Small and Medium Office archives in Table 1 | Obtain upstream and match the manifest prototype basename and SHA-256. |
| Residential prototypes | U.S. DOE and PNNL, [Residential Prototype Building Models](https://www.energycodes.gov/prototype-building-models#residential), 2021 IECC detached single-family slab variants, Table 5 | Obtain the zone archive identified by the prototype basename. Select the pinned system variant and check the exact source hash. |
| Typical-year weather | NREL TMY3 data (2008), in EPW format. DOE/PNNL [prototype weather tables](https://www.energycodes.gov/prototype-building-models) list stations in Tables 4, 6 and 8. The [EnergyPlus weather catalog](https://energyplus-weather.s3.amazonaws.com/index.html) is a separate source. | Obtain candidate EPWs by station and compare the exact manifest SHA-256. Same-station revisions and differently packaged weather files can differ. |
| Final modified IDFs | CoolDeploy revisions of the prototype inputs, including fixed HVAC references and roof controls | User supplies authorized exact files. A distributable final-IDF archive or byte-verified conversion is pending. |
| EnergyPlus | U.S. DOE and EnergyPlus contributors. [26.1.0 release](https://github.com/NatLabRockies/EnergyPlus/releases/tag/v26.1.0) and [release license](https://github.com/NatLabRockies/EnergyPlus/blob/v26.1.0/LICENSE.txt) | Install separately. The release license permits redistribution subject to its attribution, notices, disclaimer and name-use conditions. The candidate contains no simulator files. |
| Project scripts and processed data | CoolDeploy authors | The repository's MIT license applies to project code and documentation and CC BY 4.0 applies to project-generated processed data. |

DOE's web policy separates government information from contributed or licensed
material. DOE's prototype page describes opening and modifying the residential
IDFs locally. The exact archives provide DOE/PNNL attribution. PNNL's web notice
covers documents served from its website for non-commercial scientific and
educational use. File-specific permission to redistribute the final modified
IDFs remains unresolved.
[DOE web policy](https://www.energy.gov/web-policies)
[DOE prototype page](https://www.energycodes.gov/prototype-building-models)
[PNNL notices](https://www.pnnl.gov/important-notices)
[ASHRAE permissions](https://www.ashrae.org/permissions)

The project licenses cover project code, documentation and generated data.
The candidate includes the case identifiers, provenance hashes and workflow
code. Obtain original prototypes and EPWs from the verified links below.

## Verified weather downloads

Downloads from these links matched the exact EPW SHA-256 in the case
manifest on 2026-11-25. Download the EPW corresponding to the case and
run the input check before use.

| EPW | Provider |
| --- | --- |
| USA_AK_Fairbanks.Intl_.AP_.702610_TMY3.epw | [DOE Building Energy Codes Program](https://www.energycodes.gov/sites/default/files/2021-05/USA_AK_Fairbanks.Intl_.AP_.702610_TMY3.epw) |
| USA_AZ_Phoenix-Sky.Harbor.Intl_.AP_.722780_TMY3.epw | [DOE Building Energy Codes Program](https://www.energycodes.gov/sites/default/files/2022-09/USA_AZ_Phoenix-Sky.Harbor.Intl_.AP_.722780_TMY3.epw) |
| USA_CO_Denver-Aurora-Buckley.AFB_.724695_TMY3.epw | [DOE Building Energy Codes Program](https://www.energycodes.gov/sites/default/files/2021-05/USA_CO_Denver-Aurora-Buckley.AFB_.724695_TMY3.epw) |
| USA_FL_Miami.Intl_.AP_.722020_TMY3.epw | [DOE Building Energy Codes Program](https://www.energycodes.gov/sites/default/files/2021-05/USA_FL_Miami.Intl_.AP_.722020_TMY3.epw) |
| USA_IL_Chicago-OHare.Intl_.AP_.725300_TMY3.epw | [DOE Building Energy Codes Program](https://www.energycodes.gov/sites/default/files/2022-09/USA_IL_Chicago-OHare.Intl_.AP_.725300_TMY3.epw) |
| USA_MD_Baltimore-Washington.Intl_.AP_.724060_TMY3.epw | [DOE Building Energy Codes Program](https://www.energycodes.gov/sites/default/files/2022-09/USA_MD_Baltimore-Washington.Intl_.AP_.724060_TMY3.epw) |
| USA_MN_International.Falls_.Intl_.AP_.727470_TMY3.epw | [DOE Building Energy Codes Program](https://www.energycodes.gov/sites/default/files/2021-05/USA_MN_International.Falls_.Intl_.AP_.727470_TMY3.epw) |
| USA_MN_Minneapolis-St.Paul.Intl.AP.726580_TMY3.epw | [EnergyPlus weather catalog](https://energyplus-weather.s3.amazonaws.com/north_and_central_america_wmo_region_4/USA/MN/USA_MN_Minneapolis-St.Paul.Intl.AP.726580_TMY3/USA_MN_Minneapolis-St.Paul.Intl.AP.726580_TMY3.epw) |
| USA_WA_Seattle-Tacoma.Intl_.AP_.727930_TMY3.epw | [DOE Building Energy Codes Program](https://www.energycodes.gov/sites/default/files/2021-05/USA_WA_Seattle-Tacoma.Intl_.AP_.727930_TMY3.epw) |

## Verified prototype downloads

All 54 pinned original prototype members matched byte for byte in the DOE
archives below on 2026-11-25. Use the prototype basename and SHA-256 in
the case manifest to select an archive member. The final IDF has its own
independent hash and requires the authorized final-input archive.

| DOE archive | Matched members |
| --- | ---: |
| [ASHRAE901_OfficeMedium_STD2022.zip](https://www.energycodes.gov/sites/default/files/2023-10/ASHRAE901_OfficeMedium_STD2022.zip) | 9 |
| [ASHRAE901_OfficeSmall_STD2022.zip](https://www.energycodes.gov/sites/default/files/2023-10/ASHRAE901_OfficeSmall_STD2022.zip) | 9 |
| [resstd_CZ1A_IECC_2021.zip](https://www.energycodes.gov/sites/default/files/2025-01/resstd_CZ1A_IECC_2021.zip) | 4 |
| [resstd_CZ2B_IECC_2021.zip](https://www.energycodes.gov/sites/default/files/2025-01/resstd_CZ2B_IECC_2021.zip) | 4 |
| [resstd_CZ4A_IECC_2021.zip](https://www.energycodes.gov/sites/default/files/2025-01/resstd_CZ4A_IECC_2021.zip) | 4 |
| [resstd_CZ4C_IECC_2021.zip](https://www.energycodes.gov/sites/default/files/2025-01/resstd_CZ4C_IECC_2021.zip) | 4 |
| [resstd_CZ5A_IECC_2021.zip](https://www.energycodes.gov/sites/default/files/2025-01/resstd_CZ5A_IECC_2021.zip) | 4 |
| [resstd_CZ5B_IECC_2021.zip](https://www.energycodes.gov/sites/default/files/2025-01/resstd_CZ5B_IECC_2021.zip) | 4 |
| [resstd_CZ6A_IECC_2021.zip](https://www.energycodes.gov/sites/default/files/2025-01/resstd_CZ6A_IECC_2021.zip) | 4 |
| [resstd_CZ7_IECC_2021.zip](https://www.energycodes.gov/sites/default/files/2025-01/resstd_CZ7_IECC_2021.zip) | 4 |
| [resstd_CZ8_IECC_2021.zip](https://www.energycodes.gov/sites/default/files/2025-01/resstd_CZ8_IECC_2021.zip) | 4 |
