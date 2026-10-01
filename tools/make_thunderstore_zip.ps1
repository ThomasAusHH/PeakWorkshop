<#
.SYNOPSIS
  Packs the Thunderstore upload ZIP for Peak Workshop. Only packages - never uploads.

.DESCRIPTION
  Layout (what Thunderstore / r2modman expect):
    manifest.json, icon.png (256x256), README.md, CHANGELOG.md,
    plugins/PeakWorkshop/PeakWorkshop.dll
  r2modman copies plugins/ into BepInEx/plugins/, so the DLL lands in BepInEx/plugins/PeakWorkshop/.

  Run tools/finalize.py first (it writes thunderstore/README.md and the final manifest.json).

.PARAMETER Dll
  Path to PeakWorkshop.dll. Default: dist\PeakWorkshop.dll (copy the release build there).

.PARAMETER Team
  Thunderstore team name (default PeakCode) - only used for the ZIP file name.

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File tools\make_thunderstore_zip.ps1
#>
param(
    [string]$Dll = (Join-Path $PSScriptRoot "..\dist\PeakWorkshop.dll"),
    [string]$OutDir = "",
    [string]$Team = "PeakCode"
)
$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem
Add-Type -AssemblyName System.Drawing

$root = Split-Path -Parent $PSScriptRoot
$ts = Join-Path $root "thunderstore"
if ($OutDir -eq "") { $OutDir = Join-Path $root "dist" }

$manifestPath = Join-Path $ts "manifest.json"
$manifest = Get-Content $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json

# --- checks (Thunderstore rules) ---
$errors = @()
if ($manifest.name -notmatch '^[a-zA-Z0-9_]+$') { $errors += "manifest name must match ^[a-zA-Z0-9_]+$" }
if ($manifest.version_number -notmatch '^\d+\.\d+\.\d+$') { $errors += "version_number must be x.y.z" }
if ($manifest.description.Length -gt 250) { $errors += "description longer than 250 characters" }
if ($manifest.website_url -match '\{') { $errors += "website_url still has a placeholder - run tools/finalize.py" }
foreach ($d in $manifest.dependencies) { if ($d -notmatch '^[A-Za-z0-9_]+-[A-Za-z0-9_]+-\d+\.\d+\.\d+$') { $errors += "bad dependency: $d" } }
foreach ($f in "icon.png", "README.md", "CHANGELOG.md") { if (-not (Test-Path (Join-Path $ts $f))) { $errors += "missing thunderstore\$f" } }
if (Test-Path (Join-Path $ts "README.md")) {
    $readme = Get-Content (Join-Path $ts "README.md") -Raw -Encoding UTF8
    if ($readme -cmatch '\{[A-Z][A-Z_0-9]*\}') { $errors += "README.md still has placeholders - run tools/finalize.py" }
}
if (-not (Test-Path $Dll)) { $errors += "DLL not found: $Dll" }
$icon = Join-Path $ts "icon.png"
if (Test-Path $icon) {
    $img = [System.Drawing.Image]::FromFile($icon)
    try { if ($img.Width -ne 256 -or $img.Height -ne 256) { $errors += "icon.png must be 256x256 (is $($img.Width)x$($img.Height))" } }
    finally { $img.Dispose() }
}
if ((Test-Path $Dll) -and ([IO.Path]::GetFileName($Dll) -ne "PeakWorkshop.dll")) { $errors += "DLL must be named PeakWorkshop.dll" }
if ($errors.Count -gt 0) { $errors | ForEach-Object { Write-Host "ERROR: $_" -ForegroundColor Red }; exit 1 }

# --- stage + zip ---
$stage = Join-Path ([IO.Path]::GetTempPath()) ("pw_ts_" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Force (Join-Path $stage "plugins\PeakWorkshop") | Out-Null
Copy-Item $manifestPath, $icon, (Join-Path $ts "README.md"), (Join-Path $ts "CHANGELOG.md") $stage
Copy-Item $Dll (Join-Path $stage "plugins\PeakWorkshop\PeakWorkshop.dll")

New-Item -ItemType Directory -Force $OutDir | Out-Null
$zip = Join-Path $OutDir ($Team + "-PeakWorkshop-" + $manifest.version_number + ".zip")
if (Test-Path $zip) { Remove-Item $zip -Force }
# ZIP entries with forward slashes (CreateFromDirectory on .NET Framework writes backslashes)
$archive = [System.IO.Compression.ZipFile]::Open($zip, [System.IO.Compression.ZipArchiveMode]::Create)
try {
    Get-ChildItem $stage -Recurse -File | ForEach-Object {
        $rel = $_.FullName.Substring($stage.Length + 1).Replace('\', '/')
        [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($archive, $_.FullName, $rel, [System.IO.Compression.CompressionLevel]::Optimal) | Out-Null
    }
} finally { $archive.Dispose() }
Remove-Item $stage -Recurse -Force

Write-Host "Packed: $zip"
Write-Host "Upload it yourself at https://thunderstore.io/c/peak/create/ (team $Team). This script never uploads."
