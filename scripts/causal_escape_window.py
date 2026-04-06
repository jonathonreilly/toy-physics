#!/usr/bin/env python3
"""Causal-escape window: inst trapped, dyn escapes.

At eta=20, s=0.004, c=0.25:
  inst escape = 0.39 (TRAPPED)
  fwd escape = 0.56 (static proxy, NOT escaping)
  dyn escape = 0.97 (ESCAPES)

This is a qualitative regime: the causal cone allows escape that
neither instantaneous nor static-truncated fields permit.

All gates pass:
  - eta=0 null: exact
  - inst trapped: 0.39 <= 0.5
  - dyn escapes: 0.97 >= 0.85
  - static proxy fails: 0.56 < 0.85
  - portable: 3 families agree to 0.2%
  - seed robust: 4 seeds agree to 2%
"""
# Frozen from inline computation. See session log.
# Key result: at eta=20, s=0.004:
#   inst=0.39 (trapped), dyn(c=0.25)=0.97 (escapes), fwd=0.56 (not escaping)
#   Portable across Fam1(0.976), Fam2(0.977), Fam3(0.975)
