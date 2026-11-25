# Input sources and third-party notices

| Material | Source and attribution | Candidate treatment |
| --- | --- | --- |
| Commercial prototypes | U.S. DOE and Pacific Northwest National Laboratory, [Commercial Prototype Building Models](https://www.energycodes.gov/prototype-building-models), ASHRAE 90.1-2022 Small and Medium Office archives in Table 1 | Obtain upstream and match the manifest prototype basename and SHA-256. |
| Residential prototypes | U.S. DOE and PNNL, [Residential Prototype Building Models](https://www.energycodes.gov/prototype-building-models#residential), 2021 IECC detached single-family slab variants, Table 5 | Obtain the zone archive identified by the prototype basename. Select the pinned system variant and check the exact source hash. |
| Typical-year weather | NREL TMY3 data (2008), in EPW format. DOE/PNNL [prototype weather tables](https://www.energycodes.gov/prototype-building-models) list stations in Tables 4, 6 and 8. The [EnergyPlus weather catalog](https://energyplus-weather.s3.amazonaws.com/index.html) is a separate source. | Obtain candidate EPWs by station and compare the exact manifest SHA-256. Same-station revisions and differently packaged weather files can differ. |
| Final modified IDFs | CoolDeploy revisions of the prototype inputs, including fixed HVAC references and roof controls | User supplies authorized exact files. A distributable final-IDF archive or byte-verified conversion is pending. |
| EnergyPlus | U.S. DOE and EnergyPlus contributors. [26.1.0 release](https://github.com/NatLabRockies/EnergyPlus/releases/tag/v26.1.0) and [release license](https://github.com/NatLabRockies/EnergyPlus/blob/v26.1.0/LICENSE.txt) | Install separately. The release license permits redistribution subject to its attribution, notices, disclaimer and name-use conditions. The candidate contains no simulator files. |
| Project scripts and processed data | CoolDeploy authors | The repository's MIT license applies to project code and documentation and CC BY 4.0 applies to project-generated processed data. |

The [DOE web policy](https://www.energy.gov/web-policies) distinguishes government
information from contributed or licensed third-party material. The retained
DOE/PNNL prototype archives identify the source and contributor context. The
review did not establish file-specific clearance for republishing the modified
IDFs or all nine exact EPWs. Third-party inputs remain external to the project
licenses. This candidate includes only case identities, provenance hashes and
project workflow code. It carries neither prototype/weather bytes, dependency
binaries nor accepted native output files. EPW source notes and the input
manifest identify the source data without implying a redistribution license.
