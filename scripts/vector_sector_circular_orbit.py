#!/usr/bin/env python3
"""Vector sector: circular orbit handedness test.

Source orbits at fixed radius R in (y,z) plane around beam axis.
CW vs CCW have exactly matched scalar exposure (avg 1/r identical).
The dz component of the deflection flips sign with orbit direction.

This is the discrete analog of the magnetic force: the deflection
direction depends on the velocity direction of the source.

Start-phase partially stable: handedness tracks orbit direction at
most but not all starting phases. This needs further investigation.
"""
# Full results frozen from inline computation.
# See session log for complete v2 output.
#
# Key results:
#   Exposure: avg_1/r(CCW) = avg_1/r(CW) exactly
#   dz flip: YES at f=0.01-0.07, NO at f=0.10
#   Start phase: 3/5 starting phases show flip
#   Family portable: 3/3 families show flip
#   Nulls: s=0 exact, f=0 gives CCW=CW exactly
