# Grown Wavefield Companion Note

**Date:** 2026-04-05  
**Status:** bounded no-go for a review-safe grown-row wavefield transfer

## Artifact chain

- [`scripts/gate_b_grown_wavefield_companion.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_grown_wavefield_companion.py)
- [`logs/2026-04-05-grown-wavefield-companion.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-grown-wavefield-companion.txt)

## Question

Can the exact-lattice wavefield mechanism survive as a fixed-field companion
on the retained grown row without becoming a geometry-generic claim?

This probe stays deliberately narrow:

- retained Gate B grown row only: `drift = 0.2`, `restore = 0.7`
- fixed field, no self-consistent graph update
- exact zero-source reduction check
- same promoted observable as the exact wavefield lane when possible:
  detector-line phase-ramp slope / span relative to the same-site control

It does **not** claim geometry independence, continuum closure, or any
self-consistent field derivation.

## Frozen Result

The exact zero-source reduction survives on the retained grown row:

- zero-source same-site shift span: `+0.000000e+00 .. +0.000000e+00`
- zero-source wavefield shift span: `+0.000000e+00 .. +0.000000e+00`

But the promoted phase observable is too weak to freeze as a positive grown-row
transfer:

| layer | depth | inst F~M | same F~M | wave F~M | phase lag | ramp slope | ramp R2 | wave/same |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2 | 22.0 | `0.978` | `1.052` | `1.056` | `0.017` | `0.0193` | `0.294` | `12.485` |
| 4 | 20.0 | `0.938` | `1.030` | `0.904` | `-0.221` | `0.0227` | `0.298` | `6.938` |

## Safe Read

The narrow, honest statement is:

- the fixed-field grown-row replay preserves exact zero-source reduction
- the weak-field mass-law proxy stays near unity on the tested rows
- but the detector-line phase-ramp observable is too weak and too low-R2 to
  count as a review-safe grown-row transfer of the exact-lattice wavefield
  mechanism

## What This Is Not

- It is not a geometry-generic wavefield result.
- It is not a continuum theorem.
- It is not a propagated-field flagship result.

## Final Verdict

**bounded no-go**

The grown-row replay is useful as a control, but it does not materially narrow
the exact-to-grown gap on the promoted phase-ramp observable.
