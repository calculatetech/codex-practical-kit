#!/usr/bin/env python3
"""Remove the per-session Git baseline."""

from hook_common import read_payload, remove_baseline

remove_baseline(read_payload())
