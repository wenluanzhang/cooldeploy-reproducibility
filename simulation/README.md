# Run an accepted EnergyPlus annual

Use this workflow with a byte-identical final modified IDF and weather file.
The [case manifest](cases.csv) identifies 216 main, 54 narrow-B and 108
additional optical annuals. The 36 original optical A/C context annuals
are canonical main cases. The public files provide the original-source
download links and the case-specific hash pins. Acquire the exact final IDF
through an authorized route or independently prepare a file that passes the
hash check. For the accepted physical inputs and modeling decisions, see the
[model preparation guide](MODEL_PREPARATION.md).

## Install and obtain the inputs

Use Python 3.10+ and the [EnergyPlus 26.1.0 release](https://github.com/NatLabRockies/EnergyPlus/releases/tag/v26.1.0),
Windows x86-64 standard ZIP, build 6f2e40d102. The ZIP SHA-256 is
0bb6932d277eed62f996b625f37c533b8c35f9af0c53710d961d8442fc4e70b3.
Keep the executable and runtime files together. The check pins the executable,
IDD, epJSON schema and API DLL individually. Windows x86-64 is the verified
runtime platform. macOS, Linux and Windows arm64 have different binary hashes
and are outside this checked execution path.

~~~powershell
$zip = 'EnergyPlus-26.1.0-6f2e40d102-Windows-x86_64.zip'
$release = 'https://github.com/NatLabRockies/EnergyPlus/releases/download/v26.1.0'
Invoke-WebRequest -Uri "$release/$zip" -OutFile $zip
(Get-FileHash -Algorithm SHA256 $zip).Hash
# Confirm the hash against the value above before expanding the package.
Expand-Archive $zip -DestinationPath 'energyplus-install'
$engine = (Get-ChildItem energyplus-install -Recurse -Filter energyplus.exe | Select-Object -First 1).FullName
~~~

Use the [input sources and notices](SOURCES.md) to identify DOE/PNNL prototypes
and station downloads. The manifest pins station number, EPW basename and hash,
prototype basename and hash, accepted attempt, annual clock hours,
final IDF SHA-256 and input dependencies, native SQL/ERR hashes, area, separate service
readouts and the frozen CSV selector. Prototype-to-final-IDF generation is
unverified in this package. A historical original-0 sizing reference or a
different run attempt cannot satisfy the hash gate.

Create a separate input folder with two subdirectories. Copy each exact final
IDF to idf/<input_sha256>.idf and each matching EPW to weather/<weather> using
the case manifest values. Preserve raw bytes and line endings. The final IDFs
contain the accepted controls and output requests. No separate schedule file,
EMS plugin, macro or model data file was found for these case inputs. A valid
engine installation supplies its own runtime files.

## Check, run, extract and compare one case

From the repository root in PowerShell, set the paths below. The output parent
must exist. Choose new output paths outside the checkout and supplied input
folders. The examples use Seattle Medium Office Case B, the broad adaptive roof.
Checking all cases reads input hashes without launching simulations.

~~~powershell
$case = 'main/Seattle/MediumOffice/official_native/B'
$inputs = 'D:/cooldeploy-inputs'
$out = 'D:/cooldeploy-work'
python simulation/annual.py list --population main
python simulation/annual.py check --case $case --inputs $inputs --engine $engine
python simulation/annual.py run --case $case --inputs $inputs --engine $engine --output "$out/seattle-b" --timeout 240
python simulation/annual.py extract --case $case --raw "$out/seattle-b" --output "$out/seattle-b-native.json"
python simulation/annual.py compare --case $case --extracted "$out/seattle-b-native.json" --output "$out/seattle-b-comparison.json"
~~~

Use list --population sharp and list --population optical for stable case
IDs. For an inventory of every prepared input, use check --all with the input
folder. Each run command invokes one case. The workflow uses the IDF's native
weather-year settings and retains console.log and native output in the new
directory. A run receipt records the pinned identity, subprocess result and
native output hashes. Failure or timeout leaves the partial run directory for
inspection. Select a new path for any separately authorized attempt.

The compare command above uses the extracted JSON and this checkout's
frozen processed data and case manifest. Run it any time you have an
extracted result. It needs neither the simulator installation nor the
archived accepted output. On the retained Seattle Case B rerun, this
public-reference comparison passed 99 checks covering the case ID,
annual hours, roof area, occupied heating and cooling unmet hours,
monthly carrier energy and cost, annual HVAC bill and end-use costs.

For a separate check against the original run, extract --accepted uses the
accepted eplusout.sql, eplusout.err and eplusout.end. The optional
compare --accepted-native argument adds checks against those files for the
hourly clock, roof faces, per-meter monthly values, warning signatures and
available broad-B roof-temperature observations. This earlier archive-assisted
Seattle comparison passed 355 checks. The extra checks require the original
native files.

## Extraction and comparison

The extractor selects the single annual weather period, filters warmup, checks
the 8,760-hour calendar, and reads twelve native monthly summed joule values per
available end-use carrier meter. It divides by 3.6 million to obtain kWh. The
carrier names are Electricity, NaturalGas and FuelOilNo2. The disjoint end uses
are Heating, Cooling, Fans, Pumps, HeatRejection, Humidification and HeatRecovery.
Monthly meter sums must agree with the rounded annual ABUPS End Uses table within
0.005 GJ plus representation slack. An absent meter can supply zeros only when
this check passes. Frozen-price comparison adds a separate check against the
approved energy and cost records. Lighting, equipment, SWH and PV offsets are
outside this HVAC accounting. Purchased energy comes from native meters.

The extract includes a processed bridge with 36 family/roof/month/carrier rows
and 21 annual end-use/carrier rows. Missing rates are allowed only for zero
energy. Main and optical comparisons check monthly carrier energy, monthly
cost, annual bill and annual end-use costs. Narrow-B uses the frozen annual
end-use and bill records for comparison. The 1e-7 USD threshold follows the
existing cost closure. The 1e-7 kWh threshold allows floating-point aggregation
differences at the recorded precision under the same binary. Facility occupied
heating/cooling unmet hours come from separate ABUPS service rows and the roof
area is the sum of exterior heat-transfer roof gross areas. The 1e-8 h and m²
threshold permits representation differences. The comparison JSON includes
each measured value, reference, unit, tolerance and signed difference, even
when the command exits with a mismatch.

The raw ERR file preserves complete warnings. Extracted signatures and totals
are diagnostic evidence. The accepted warning classification is kept separately
as provenance. Broad-B SQL temperature samples support an inferred preceding-
temperature state profile, with the first predecessor missing. These are not
direct solar or thermal actuator readbacks. A complete annual run does not
establish equal indoor service, an annual numerical-error bound, or field
validation.

## Validation coverage

The [validation report](../docs/REPRODUCIBILITY_REPORT.md) records the local
input and archived-output checks and the previously demonstrated Seattle
Medium Office Case B annual. The bundled processed data support downstream
reproduction and the public-reference comparison for reader-supplied
extracted results. The repository does not distribute final modified IDFs
or the native output archive.
