# Source-Resolved Exact Green Scaling

**Date:** 2026-04-05  
**Status:** bounded exact-lattice size-transfer positive for the source-resolved Green pocket

## Artifact chain

- [`scripts/source_resolved_exact_green_scaling.py`](/Users/jonreilly/Projects/Physics/scripts/source_resolved_exact_green_scaling.py)
- [`logs/2026-04-05-source-resolved-exact-green-scaling.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-source-resolved-exact-green-scaling.txt)
- [`docs/SOURCE_RESOLVED_EXACT_GREEN_POCKET_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SOURCE_RESOLVED_EXACT_GREEN_POCKET_NOTE.md)

## Question

Does the source-resolved Green-like field remain a real weak-field pocket when
the exact lattice family is made larger, or is it only a small feasibility
artifact?

This note is intentionally narrow:

- one exact lattice family, larger than the original pocket
- one source-resolved Green-like kernel
- one comparison against the instantaneous `1/r` field
- one reduction check: zero source must recover free propagation exactly

## Frozen result

The frozen larger-family replay uses:

- exact lattice with `h = 0.5`, `W = 3`, `L = 24`
- fixed source cluster of 4 nodes
- source strengths `s = 0.001, 0.002, 0.004, 0.008`
- kernel `exp(-mu r) / (r + eps)` with `mu = 0.08`, `eps = 0.5`
- calibration gain `2.131774e+00`

Reduction check:

- zero-source dynamic shift: `+0.000000e+00`

Frozen readout:

| `s` | instantaneous deflection | Green-kernel deflection | ratio | max `|f|` |
| --- | ---: | ---: | ---: | ---: |
| `0.0010` | `+1.455880e-03` | `+1.622715e-03` | `1.115` | `2.5e-03` |
| `0.0020` | `+2.923743e-03` | `+3.254526e-03` | `1.113` | `5.0e-03` |
| `0.0040` | `+5.894605e-03` | `+6.545810e-03` | `1.110` | `1.0e-02` |
| `0.0080` | `+1.197021e-02` | `+1.324085e-02` | `1.106` | `2.0e-02` |

Fitted exponents:

- instantaneous `F~M`: `1.01`
- Green-kernel `F~M`: `1.01`

## Safe read

The strongest bounded statement is:

- exact zero-source reduction survives
- the Green-kernel field keeps the weak-field `TOWARD` sign on the larger
  exact lattice family
- the mass-scaling class stays essentially linear
- the dynamic field remains nontrivial, with mean `|green/inst| = 1.111`

## Honest limitation

This is a larger exact-lattice size-transfer positive, but it is still not a
full self-consistent field theory.

- the architecture is source-resolved and linear
- the result is exact-lattice local, not yet generated-geometry transferred
- the next question is whether the same pocket can survive a robustness sweep
  and then a refinement or generated-family replay

## Branch verdict

Treat this as a real bounded positive:

- it scales beyond the smallest feasibility pocket
- it preserves exact zero-source reduction
- it preserves `TOWARD`
- it preserves `F~M = 1.00` to within the retained fit
- it is the best current exact-lattice Green-packet evidence in the moonshot
  lane
