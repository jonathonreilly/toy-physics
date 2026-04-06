# Multipole Tidal Response Note

**Date:** 2026-04-06  
**Status:** retained quadrupole-like tidal response on the ordered 3D family

## Artifact chain

- [`scripts/multipole_tidal_response_probe.py`](/Users/jonreilly/Projects/Physics/scripts/multipole_tidal_response_probe.py)
- [`logs/2026-04-06-multipole-tidal-response-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-multipole-tidal-response-probe.txt)

## Question

Can the retained ordered-lattice scalar lane support a shape-sensitive response
that is genuinely beyond the existing monopole/dipole package?

This probe stays deliberately narrow:

- exact same-site opposite-sign cancellation first
- exact neutral `q_test = 0` control second
- one dipole baseline
- one centered quadrupole family with zero net charge and zero dipole moment
- one tidal observable based on detector width, not just centroid steering

It does **not** claim full tensor gravity or a general multipole theory.

## Frozen Result

On the retained run:

- same-site opposite-sign control:
  - `dc = +0.00000000e+00`
  - `dw = +0.00000000e+00`
  - verdict: `PASS`
- neutral `q_test = 0` control:
  - `dc = +0.00000000e+00`
  - `dw = +0.00000000e+00`
  - verdict: `PASS`
- dipole baseline `(+/- at ±1.0)`:
  - `dc = +1.86858406e-04`
  - `dw = +2.94510740e-08`
- centered quadrupole `(+1, -2, +1)` shape with `a = 1.0`:
  - `dc = +5.30479049e-16`
  - `dw = +4.47720985e-05`
- centered quadrupole with `a = 2.0`:
  - `dc = +8.60006081e-16`
  - `dw = +8.81195303e-05`
- width ratio `a = 2.0 / a = 1.0`:
  - `1.969`

## Safe Read

The narrow, review-safe statement is:

- exact same-site opposite charges still cancel to printed precision
- neutral test charge `q_test = 0` is inert
- the centered dipole mostly produces centroid steering
- the centered quadrupole keeps the centroid essentially pinned but opens a
  real width/tidal channel
- the width response grows with quadrupole separation, so the effect is shape
  sensitive rather than just a rewording of the dipole cancellation story

## What This Is Not

- It is not a full multipole expansion theory.
- It is not a claim about tensor gravity or relativistic tidal fields.
- It is not a replacement for the earlier scalar sign-law lane.

## Final Verdict

**retained quadrupole-like tidal response**
