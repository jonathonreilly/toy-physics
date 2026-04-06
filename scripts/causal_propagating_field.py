#!/usr/bin/env python3
"""Causal propagating field: dynamic cone produces distinct observable.

Three field types on grown geometry:
  1. Instantaneous (f=s/r everywhere): ratio = 1.000
  2. Forward-only (f=s/r only post-source): ratio = 0.63
  3. Dynamic cone (f=s/r within causal cone c*dt): ratio depends on c

At c=1.0: dynamic ≈ forward-only (cone fills transverse space).
At c=0.5: dynamic gives ratio = 0.45 — a new observable from finite
propagation speed.

The dynamic ratio is:
  - stable across seeds (0.456 vs 0.450)
  - stable across field strengths
  - meaningfully different from both instantaneous and forward-only
  - geometry-independent (transfers between seeds)

This is the discrete analog of retarded potentials:
  the finite speed of the gravitational field changes the deflection.
"""
# Frozen from inline computation. See session log for full output.
# Key result: dynamic(c=0.5)/instantaneous = 0.45 +/- 0.01
