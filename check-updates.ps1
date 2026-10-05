#Requires -Version 7.0
& python (Join-Path $PSScriptRoot "kit.py") check-updates @args
exit $LASTEXITCODE
