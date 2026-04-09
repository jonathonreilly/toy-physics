# Claude Complex-Action Grown Companion Note

**Date:** 2026-04-05  
**Status:** retained narrow grown-geometry companion of the exact-lattice
complex-action carryover

## Artifact chain

- [`scripts/complex_action_grown_companion.py`](/Users/jonreilly/Projects/Physics/scripts/complex_action_grown_companion.py)
- [`logs/2026-04-05-grown-geometry-complex-action-companion.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-grown-geometry-complex-action-companion.txt)

## Question

Can the exact-lattice complex-action carryover survive on the retained grown
row without becoming a geometry-generic or continuum claim?

This companion stays narrow:

- retained grown row only: `drift = 0.2`, `restore = 0.7`
- source-resolved complex action
- exact `gamma = 0` reduction check
- Born proxy on the grown graph
- weak-field `F~M` sanity check
- one `gamma` sweep for the `TOWARD -> AWAY` crossover

It does **not** claim geometry independence, continuum closure, or any
self-gravity derivation.

## Frozen Result

On the retained grown row, the replay is narrow but real:

- exact `gamma = 0` reduction on seed `0`:
  - baseline deflection: `+2.460475e-01`
  - complex-action at `gamma = 0`: `+2.460475e-01`
  - match: exact within machine precision
- Born proxy on seed `0`:
  - `|I3|/P = 1.456e-15`
- weak-field `F~M` on seeds `0,1`:
  - `gamma = 0.00`: `1.000`
  - `gamma = 0.05`: `1.000`
  - `gamma = 0.10`: `1.000`
  - `gamma = 0.20`: `1.000`
  - `gamma = 0.50`: `1.000`
  - `gamma = 1.00`: `1.000`
- gamma sweep on seeds `0,1`:

| `gamma` | toward | avg deflection | avg escape | `F~M` |
| --- | ---: | ---: | ---: | ---: |
| `0.00` | `2/2` | `+2.606923e-01` | `2.0077` | `1.000` |
| `0.05` | `2/2` | `+1.823141e-01` | `1.7063` | `1.000` |
| `0.10` | `2/2` | `+1.042271e-01` | `1.4522` | `1.000` |
| `0.20` | `0/2` | `-4.931754e-02` | `1.0558` | `1.000` |
| `0.50` | `0/2` | `-4.760660e-01` | `0.4156` | `1.000` |
| `1.00` | `0/2` | `-1.074474e+00` | `0.0935` | `1.000` |

## Safe Read

The narrow, review-safe statement is:

- the exact-lattice complex-action carryover does survive a retained grown-row
  replay
- exact `gamma = 0` reduction is preserved
- the Born proxy is machine clean on the grown graph
- weak-field `F~M` stays at `1.000` in the checked grown-row replay
- the `TOWARD -> AWAY` crossover survives on the retained grown row

## What this is not

- It is not a geometry-generic complex-action result.
- It is not a continuum theorem.
- It is not a self-gravity mechanism claim.

The claim surface stays on the retained grown row only.

## Final Verdict

**retained narrow grown-geometry companion**
