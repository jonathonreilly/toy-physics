# 3D 1/L^2 + h^2 Numpy h=0.125 Audit

**Date:** 2026-04-05  
**Status:** bounded negative on the reduced numpy audit family

## Artifact chain

- [`scripts/lattice_3d_l2_numpy_h0125_audit.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_3d_l2_numpy_h0125_audit.py)
- [`logs/2026-04-05-lattice-3d-l2-numpy-h0125-audit.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-lattice-3d-l2-numpy-h0125-audit.txt)

## Question

Can the retained 3D dense `1/L^2 + h^2` numpy lane complete a smaller fixed-family
continuum audit through `h = 0.125` without losing the basic weak-field physics?

This probe stays deliberately narrow:

- same dense 3D architecture class
- same `1/L^2` kernel and `h^2` measure
- reduced but fixed physical family for tractability
- one h ladder: `1.0, 0.5, 0.25, 0.125`

## Frozen result

The audit completes numerically on the reduced family:

- `h = 1.0`: 45 nodes, 5 layers, 324 edges
- `h = 0.5`: 441 nodes, 9 layers, 19,208 edges
- `h = 0.25`: 2,873 nodes, 17 layers, 456,976 edges
- `h = 0.125`: 20,625 nodes, 33 layers, 12,500,000 edges

The retained observables are:

| h | Born `|I3|/P` | `d_TV` | `k=0` | Gravity `z=3` | `F~M` | Decoherence | MI |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.0 | `nan` | `0.2605` | `0` | `+0.000000 (AWAY)` | too few TOWARD points | `38.3%` | `0.1248` |
| 0.5 | `1.39e-15` | `0.6586` | `0` | `+0.000000 (AWAY)` | too few TOWARD points | `49.9%` | `0.4985` |
| 0.25 | `2.50e-15` | `0.6994` | `0` | `+0.000000 (AWAY)` | too few TOWARD points | `49.9%` | `0.4699` |
| 0.125 | `4.23e-15` | `0.6725` | `0` | `+0.000000 (AWAY)` | too few TOWARD points | `49.0%` | `0.3787` |

## Safe read

The numpy bridge is real:

- the reduced family runs through `h = 0.125`
- Born stays machine-clean for `h = 0.5, 0.25, 0.125`

But the weak-field gravity lane does **not** recover on this audit family:

- the gravity sign at `z = 3` stays `AWAY` at every spacing
- the `F~M` fit never gets any TOWARD rows to fit

So the narrowest safe conclusion is:

- the reduced `3D 1/L^2 + h^2` numpy lane completes numerically through `h = 0.125`
- it preserves Born
- it does **not** preserve the retained weak-field gravity class on this audit family

## Honest limitation

This is a credibility audit, not a full continuum theorem:

- the family is reduced for tractability
- the gravity readout is still a single-axis weak-field probe
- the result should not be overread as full 3D closure

## Branch verdict

Treat this as a bounded negative for the current `h = 0.125` credibility lane:

- the computation now reaches `h = 0.125`
- the linear quantum bookkeeping survives
- but the Newtonian weak-field lane does not reappear on the reduced family
