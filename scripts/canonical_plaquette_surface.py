#!/usr/bin/env python3
"""
Canonical plaquette-derived quantities on the retained SU(3) beta=6 surface.

Authority:
  docs/PLAQUETTE_SELF_CONSISTENCY_NOTE.md

These values are same-surface evaluated constants of the retained theory.
They are not experimental imports and not free parameters.
"""

from __future__ import annotations

import math

CANONICAL_PLAQUETTE = 0.5934
CANONICAL_ALPHA_BARE = 1.0 / (4.0 * math.pi)
CANONICAL_U0 = CANONICAL_PLAQUETTE ** 0.25
CANONICAL_ALPHA_LM = CANONICAL_ALPHA_BARE / CANONICAL_U0
CANONICAL_ALPHA_S_V = CANONICAL_ALPHA_BARE / (CANONICAL_U0 ** 2)

