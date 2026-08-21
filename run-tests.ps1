#Requires -Version 7.0
$ErrorActionPreference = "Stop"
$env:PYTHONUTF8 = "1"
Set-Location $PSScriptRoot
try {
    & python -m unittest discover -s tests -v
} catch {
    Write-Error $_
    exit 1
}
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
$hooks = Get-ChildItem (Join-Path $PSScriptRoot "assets/hooks/*.py") -File | ForEach-Object FullName
$runtime = Get-ChildItem (Join-Path $PSScriptRoot "assets/runtime/*.py") -File | ForEach-Object FullName
$sources = @((Join-Path $PSScriptRoot "kit.py")) + $hooks + $runtime
try {
    & python -m py_compile @sources
} catch {
    Write-Error $_
    exit 1
}
exit $LASTEXITCODE
