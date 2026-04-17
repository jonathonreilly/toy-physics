# Source-Resolved Exact Green h=0.25 Pocket

**Date:** 2026-04-05  
**Status:** bounded h=0.25 refinement-positive for the source-resolved Green pocket

## Artifact chain

- [`scripts/source_resolved_exact_green_h025_pocket.py`](/Users/jonreilly/Projects/Physics/scripts/source_resolved_exact_green_h025_pocket.py)
- [`logs/2026-04-05-source-resolved-exact-green-h025-pocket.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-source-resolved-exact-green-h025-pocket.txt)
- [`docs/SOURCE_RESOLVED_EXACT_GREEN_POCKET_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SOURCE_RESOLVED_EXACT_GREEN_POCKET_NOTE.md)
- [`docs/SOURCE_RESOLVED_EXACT_GREEN_SCALING_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SOURCE_RESOLVED_EXACT_GREEN_SCALING_NOTE.md)

## Question

Does the source-resolved Green pocket survive one compact refinement-style
exact-lattice family at `h = 0.25` while preserving:

- exact zero-source reduction
- weak-field `TOWARD` sign
- near-linear mass scaling
- nontrivial amplitude

This note is intentionally narrow:

- one compact exact refinement family
- one source-resolved Green-like kernel
- one comparison against the instantaneous `1/r` field
- one reduction check: zero source must recover free propagation exactly

## Frozen result

The frozen pocket uses:

- exact lattice with `h = 0.25`, `W = 3`, `L = 6`
- fixed cross5 source cluster clipped at the boundary, leaving 4 in-bounds source nodes
- source strengths `s = 0.001, 0.002, 0.004, 0.008`
- kernel `exp(-mu r) / (r + eps)` with `mu = 0.08`, `eps = 0.5`
- calibration gain `1.757890e+00`

Reduction check:

- zero-source dynamic shift: `+0.000000e+00`

Frozen readout:

| `s` | instantaneous deflection | Green-kernel deflection | ratio | max `|f|` |
| --- | ---: | ---: | ---: | ---: |
| `0.0010` | `+1.410541e-03` | `+1.872661e-03` | `1.328` | `2.0e-02` |
| `0.0020` | `+2.821591e-03` | `+3.747301e-03` | `1.328` | `2.0e-02` |
| `0.0040` | `+5.645274e-03` | `+7.502598e-03` | `1.329` | `2.0e-02` |
| `0.0080` | `+1.129975e-02` | `+1.503801e-02` | `1.331` | `2.0e-02` |

Fitted exponents:

- instantaneous `F~M`: `1.00`
- Green-kernel `F~M`: `1.00`

## Safe read

The strongest bounded statement is:

- exact zero-source reduction survives
- the Green-kernel field keeps the weak-field `TOWARD` sign on the compact
  `h = 0.25` refinement family
- the mass-scaling class stays essentially linear
- the dynamic field remains nontrivial, with mean `|green/inst| = 1.329`

## Honest limitation

This is a refinement-positive pocket, not yet a full self-consistent field
theory.

- the exact lattice is intentionally compact
- the architecture is source-resolved and linear, so it is not a self-
  consistent dynamical field equation
- the source pattern is boundary-clipped rather than fully symmetric, so this
  is a bounded refinement pocket rather than a clean symmetric-family proof
- still, it is a distinct compact refinement candidate that survives the hard
  gates cleanly

## Branch verdict

Treat this as a real bounded positive:

- exact zero-source reduction survives
- weak-field sign survives
- `F~M` stays at `1.00`
- the pocket survives one refinement-style exact-lattice step
- together with the larger exact-lattice scaling companion, it is the
  strongest current exact-lattice Green evidence in the moonshot lane
