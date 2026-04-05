# Source-Resolved Exact Green Self-Consistent Pocket

**Date:** 2026-04-05  
**Status:** bounded self-consistent refinement-positive on the compact exact lattice

## Artifact chain

- [`scripts/source_resolved_exact_green_self_consistent.py`](/Users/jonreilly/Projects/Physics/scripts/source_resolved_exact_green_self_consistent.py)

## Question

Does the exact-lattice Green pocket survive a minimal self-consistency update,
where the source-cluster weights are reweighted from the propagated wave once,
while preserving the weak-field gravity lane?

This note is intentionally narrow:

- one compact exact lattice family at `h = 0.25`
- one source-resolved Green-like kernel
- one self-consistency update from source-cluster amplitudes
- one comparison against the instantaneous `1/r` field
- one reduction check: zero source must recover free propagation exactly

## Frozen result

The frozen pocket uses:

- exact lattice with `h = 0.25`, `W = 3`, `L = 6`
- fixed cross5 source cluster clipped at the boundary, leaving 4 in-bounds source nodes
- source strengths `s = 0.001, 0.002, 0.004, 0.008`
- kernel `exp(-mu r) / (r + eps)` with `mu = 0.08`, `eps = 0.5`
- calibration gain `1.757890e+00`
- one self-consistency update from the propagated source-cluster amplitudes

Reduction check:

- zero-source dynamic shift: `+0.000000e+00`

Frozen readout:

| `s` | instantaneous deflection | self-consistent deflection | ratio | max `|f|` |
| --- | ---: | ---: | ---: | ---: |
| `0.0010` | `+1.442000e-03` | `+1.874000e-03` | `1.299` | `2.0e-02` |
| `0.0020` | `+2.885000e-03` | `+3.750000e-03` | `1.300` | `2.0e-02` |
| `0.0040` | `+5.775000e-03` | `+7.508000e-03` | `1.300` | `2.0e-02` |
| `0.0080` | `+1.157000e-02` | `+1.505000e-02` | `1.301` | `2.0e-02` |

Fitted exponents:

- instantaneous `F~M`: `1.00`
- self-consistent Green `F~M`: `1.00`

## Safe read

The strongest bounded statement is:

- exact zero-source reduction survives
- the self-consistent Green field keeps the weak-field `TOWARD` sign on the
  compact `h = 0.25` family
- the mass-scaling class stays essentially linear
- the dynamic field remains nontrivial, with mean `|green/inst| = 1.300`

## Honest limitation

This is a refinement-positive pocket, not yet a full self-consistent field
theory.

- the exact lattice is intentionally compact
- the architecture still uses a single self-consistency update, not a fully
  converged dynamical field evolution
- the source pattern is boundary-clipped rather than fully symmetric, so this
  is a bounded refinement update rather than a symmetry-clean family proof
- still, it is the smallest exact-lattice refinement of the Green pocket that
  preserves the hard gates cleanly

## Branch verdict

Treat this as a real bounded positive:

- exact zero-source reduction survives
- weak-field sign survives
- `F~M` stays at `1.00`
- the pocket survives a self-consistency update on the exact refinement family
- this is the best current exact-lattice propagating-field refinement lead
