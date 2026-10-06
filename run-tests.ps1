#Requires -Version 7.0
$ErrorActionPreference = "Stop"
$env:PYTHONUTF8 = "1"
$env:PYTHONDONTWRITEBYTECODE = "1"
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
    & python -c "import sys; from pathlib import Path; [compile(Path(p).read_bytes(), p, 'exec') for p in sys.argv[1:]]" @sources
} catch {
    Write-Error $_
    exit 1
}
exit $LASTEXITCODE
