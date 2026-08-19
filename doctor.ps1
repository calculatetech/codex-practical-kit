#Requires -Version 7.0
try {
    & python (Join-Path $PSScriptRoot "kit.py") doctor @args
} catch {
    Write-Error $_
    exit 1
}
exit $LASTEXITCODE
