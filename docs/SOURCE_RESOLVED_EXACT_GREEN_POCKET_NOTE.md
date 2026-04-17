# Source-Resolved Exact Green Pocket

**Date:** 2026-04-05  
**Status:** bounded moonshot feasibility pocket on a small exact lattice

## Artifact chain

- [`scripts/source_resolved_exact_green_pocket.py`](/Users/jonreilly/Projects/Physics/scripts/source_resolved_exact_green_pocket.py)
- [`logs/2026-04-05-source-resolved-exact-green-pocket.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-source-resolved-exact-green-pocket.txt)

## Question

Can a source-resolved Green-like field on an exact lattice, built from a
fixed source cluster rather than a telegraph recurrence or edge-carried
transport, preserve the weak-field gravity lane on the retained source
strength ladder?

This note is intentionally narrow:

- one exact lattice family, kept small enough for a fast feasibility check
- one source-resolved Green-like kernel
- one comparison against the instantaneous `1/r` field
- one reduction check: zero source must recover free propagation exactly

## Frozen result

The frozen pocket uses:

- exact lattice with `h = 0.5`, `W = 3`, `L = 20`
- fixed cross5 source cluster clipped at the boundary, leaving 4 in-bounds source nodes
- source strengths `s = 0.001, 0.002, 0.004, 0.008`
- kernel `exp(-mu r) / (r + eps)` with `mu = 0.08`, `eps = 0.5`
- calibration gain `2.131774e+00`

Reduction check:

- zero-source dynamic shift: `+0.000000e+00`

Frozen readout:

| `s` | instantaneous deflection | Green-kernel deflection | ratio | max `|f|` |
| --- | ---: | ---: | ---: | ---: |
| `0.0010` | `+1.713544e-03` | `+2.139974e-03` | `1.249` | `2.5e-03` |
| `0.0020` | `+3.440703e-03` | `+4.279368e-03` | `1.244` | `5.0e-03` |
| `0.0040` | `+6.936763e-03` | `+8.557987e-03` | `1.234` | `1.0e-02` |
| `0.0080` | `+1.410179e-02` | `+1.712572e-02` | `1.214` | `2.0e-02` |

Fitted exponents:

- instantaneous `F~M`: `1.01`
- Green-kernel `F~M`: `1.00`

## Safe read

The strongest bounded statement is:

- exact zero-source reduction survives
- the Green-kernel field keeps the weak-field `TOWARD` sign on the retained
  source ladder
- the mass-scaling class stays essentially linear
- the dynamic field remains nontrivial, with mean `|green/inst| = 1.235`

## Honest limitation

This is a feasibility pocket, not yet a full-size exact-lattice theory.

- the exact lattice here is intentionally small
- the architecture is source-resolved and linear, so it is not a self-
  consistent dynamical field equation
- the source pattern is boundary-clipped rather than fully symmetric, so this
  is a bounded pocket control rather than a clean geometric refinement proof
- still, it is a distinct exact-lattice self-generated field candidate that
  survives the hard gates cleanly

## Branch verdict

Treat this as a real bounded positive:

- distinct from the telegraph recurrence
- distinct from edge-carried transport
- exact zero-source reduction survives
- weak-field sign survives
- `F~M` stays at `1.00`
- the branch is viable as a moonshot pocket worth a later size-transfer test
