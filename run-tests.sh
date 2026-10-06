#!/usr/bin/env sh
set -eu
export PYTHONDONTWRITEBYTECODE=1
python3 -m unittest discover -s tests -v
python3 -c 'import sys; from pathlib import Path; [compile(Path(p).read_bytes(), p, "exec") for p in sys.argv[1:]]' kit.py assets/hooks/*.py assets/runtime/*.py
