# Electrostatics Grown Sign-Law Note

**Date:** 2026-04-05  
**Status:** retained narrow grown-geometry sign-law companion

## Artifact chain

- [`scripts/ELECTROSTATICS_GROWN_SIGN_LAW.py`](/Users/jonreilly/Projects/Physics/scripts/ELECTROSTATICS_GROWN_SIGN_LAW.py)
- [`logs/2026-04-05-electrostatics-grown-sign-law.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-electrostatics-grown-sign-law.txt)

## Question

Can the retained scalar sign-law family survive on the retained grown row
without becoming a geometry-generic claim?

This check is intentionally narrow:

- retained grown geometry row only: `drift = 0.2`, `restore = 0.7`
- fixed-field, no graph update
- one source layer, one final-layer detector centroid
- source sign in `{-1, +1}` plus simple multi-source superposition cases
- exact same-point neutral cancellation guardrail
- linearity check via `+1` versus `+2`

## Frozen Result

On the retained grown row, the sign law survives cleanly:

| case | source(s) | delta_z mean | sign | read |
| --- | ---: | ---: | ---: | --- |
| single `+1` | `+1@3.0` | `-1.882286e-04` | `AWAY` | `repel` |
| single `-1` | `-1@3.0` | `+1.882349e-04` | `TOWARD` | `attract` |
| neutral same-point `+1/-1` | `+1@3.0 + -1@3.0` | `+0.000000e+00` | `ZERO` | `null` |
| like pair `+1/+1` | `+1@2.0 + +1@4.0` | `-2.556525e-04` | `AWAY` | `repel` |
| dipole `+1/-1` | `+1@2.0 + -1@4.0` | `+3.137392e-05` | `TOWARD` | `partial-cancel` |
| double `+2` | `+2@3.0` | `-3.764509e-04` | `AWAY` | `linear` |

Reduction / linearity checks:

- neutral same-point pair mean delta: `+0.000000e+00`
- single `+1` vs double `+2` charge exponent: `1.000`
- single `-1` mean delta: `+1.882349e-04`
- dipole mean delta: `+3.137392e-05`

## Safe Read

The narrow, review-safe statement is:

- the same sign-coupled propagator still supports like/unlike sign response on the retained grown row
- neutral same-point `+/-` sources cancel to printed precision
- the response is approximately linear in source charge on this grown geometry
- this narrows the exact-to-grown transfer gap for the scalar sign-law family

## What this is not

- It is not full electromagnetism.
- It is not a Maxwell or radiation derivation.
- It is not a geometry-generic theorem.

## Final Verdict

**retained narrow grown-geometry sign-law companion**
