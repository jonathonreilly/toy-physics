# Gravity on Structureless Causal DAGs

**Date:** 2026-04-04 (table refreshed 2026-05-02)
**Status:** frozen probe — bounded universality result on the current harness

## Setup

Random 3D points sorted by x-coordinate (causal ordering).
Edges from `i -> j` if `x_j > x_i` and distance below a fixed radius.
No layers, no grid, no structure beyond causality.
Valley-linear action `S = L(1-f)`, `1/L^2` kernel.

## Runner

Bounded harness:

- [`scripts/structureless_dag_gravity_harness.py`](../scripts/structureless_dag_gravity_harness.py)
- Sizes covered by the current harness: `n = 200` and `n = 500`. The harness
  intentionally does **not** include the older unstable `n = 1000` pocket;
  see "Honest scope" below.

## Results (current harness)

Reported across 8 seeds with strengths `s = [0.001, 0.002, 0.005, 0.01]`,
so 32 source/detector rows per size:

| Configuration | TOWARD rows | seed-local F~M (median) | no-field control |
|---|---|---|---|
| `n = 200`, radius `0.35` | `28/32` (87.5%) | `1.00` | `+0.0e+00` |
| `n = 500`, radius `0.35` | `23/32` (71.9%) | `1.00` | `+0.0e+00` |

These numbers come directly from the current frozen log; the previous
table values (`200n r=3 56%`, `500n r=2.5 73%`, `1000n r=2 50%`) used a
different connectivity scan and are no longer representative of this
harness.

## Honest scope

- this is a bounded random-DAG probe, not a graph-universality theorem
- the harness covers two sizes (`n = 200`, `n = 500`) at one fixed radius
- the older `n = 1000` pocket reported in earlier prose was unstable and is
  not retained in the current harness; it should not be cited as a
  retained pocket
- the safe read is that structureless causal DAGs can show `TOWARD` rows,
  and when they do the source-strength response stays close to linear on
  this pocket
- the sign remains seed-sensitive on the smaller-radius / larger-`n`
  configurations and so the claim stays narrow and review-safe

## Safe wording

"On random `x`-ordered causal DAGs with no imposed structure beyond
causality, the valley-linear propagator gives gravitational deflection
that is `TOWARD` in the majority of seeds and follows `F~M ~= 1.0` on
the positive rows. The Newtonian mass scaling reads as a propagator
property, not a graph property, but only on the bounded pocket the
current harness covers."
