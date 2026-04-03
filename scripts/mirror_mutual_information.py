#!/usr/bin/env python3
"""Compatibility wrapper for the canonical mirror MI harness.

The dedicated retained exact-mirror chokepoint harness lives in
scripts/mirror_mutual_information_chokepoint.py.
"""

from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.mirror_mutual_information_chokepoint import main


if __name__ == "__main__":
    main()
