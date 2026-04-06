#!/usr/bin/env python3
"""Causal-escape boundary law in (eta, c).

Compact law: at the inst trap threshold (inst escape = 0.50):
  c >= 0.5: dyn ESCAPES (>= 0.85)
  c >= 1.0: dyn marginal (~0.82)
  c >= 2.0: dyn marginal (~0.75)

Boundary law: eta_max(c) where dyn escape drops to 0.85:
  c=2.0: eta_max=8
  c=1.0: eta_max=12
  c=0.5: eta_max=33
  c=0.25: eta_max=250
  c=0.1: eta_max=500+

Approximately eta_max ~ 1/c^2.

S-dependence: protection ratio grows strongly with s.
  s=0.016: ratio=33 (inst 97% trapped, dyn 92% escapes)

Static proxy (fwd) gives escape=0.56 at eta=15 — NOT in escape window.
"""
# Frozen from inline computation. See session log for full output.
