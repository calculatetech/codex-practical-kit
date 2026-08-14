#!/usr/bin/env sh
set -eu
python3 -m unittest discover -s tests -v
python3 -m py_compile kit.py assets/hooks/*.py
