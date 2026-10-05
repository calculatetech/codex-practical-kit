#Requires -Version 7.0
& python (Join-Path $PSScriptRoot "kit.py") apply-updates @args
exit $LASTEXITCODE
