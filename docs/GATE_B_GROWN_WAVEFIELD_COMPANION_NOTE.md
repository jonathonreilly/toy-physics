# Gate B Grown Wavefield Companion Note

**Date:** 2026-04-05  
**Status:** bounded no-go for detector-line phase-ramp transfer on the proposed_retained
grown row

## Artifact chain

- [`scripts/gate_b_grown_wavefield_companion.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_grown_wavefield_companion.py)
- [`logs/2026-04-05-gate-b-grown-wavefield-companion.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-grown-wavefield-companion.txt)

## Question

Can the retained exact-lattice wavefield mechanism survive as a narrow
fixed-field grown-row companion without turning into a geometry-generic or
self-consistent field claim?

This probe stays narrow:

- retained grown row only: `drift = 0.2`, `restore = 0.7`
- fixed field only, no graph feedback
- exact zero-source reduction check
- same promoted observable as the exact-lattice wavefield lane when possible:
  detector-line phase-ramp slope/span relative to the same-site control
- small source-layer scan on the retained grown row

## Exact Reduction

The reduction guardrail is the same-source-strength zero-coupling check:

- zero-source same-site shift span: `+0.000000e+00 .. +0.000000e+00`
- zero-source wavefield shift span: `+0.000000e+00 .. +0.000000e+00`

So the fixed-field grown companion does respect exact baseline reproduction at
zero source strength.

## Frozen Result

Frozen on the retained grown row with source layers `2` and `4`:

| `layer` | `depth` | `inst F~M` | `same F~M` | `wave F~M` | `phase_lag` | `ramp_slope` | `ramp_R2` | `wave/same` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `2` | `22.0` | `0.978` | `1.052` | `1.056` | `+0.017` | `+0.0193` | `0.294` | `12.485` |
| `4` | `20.0` | `0.938` | `1.030` | `0.904` | `-0.221` | `+0.0227` | `0.298` | `6.938` |

## Safe Read

The bounded read is:

- the zero-source baseline reproduction survives
- the wavefield update does produce a larger detector response than the
  same-site control on this retained grown row
- but the promoted phase observable does **not** survive as a coherent
  detector-line phase-ramp law
- the phase-ramp slopes are small and the `R^2` values are low

So this is **not** a retained grown-row transfer of the exact-lattice
wavefield mechanism.

The narrow retained statement is only:

- fixed-field grown-row wavefield update is distinguishable from the same-site
  control
- exact zero-source reduction is preserved
- the detector-line phase-ramp mechanism itself does not cleanly carry over on
  the retained grown row

## Final Verdict

**bounded no-go for phase-ramp transfer on the retained grown row**
