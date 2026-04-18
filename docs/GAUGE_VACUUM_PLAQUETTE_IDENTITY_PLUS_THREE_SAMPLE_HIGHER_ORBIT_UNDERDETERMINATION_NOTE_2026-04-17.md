# Gauge-Vacuum Plaquette Identity-Plus-Three-Sample Higher-Orbit Underdetermination

**Date:** 2026-04-17  
**Status:** exact PF-only higher-orbit underdetermination theorem on the
plaquette beta-side lane; even if the full first sample packet
`{Z_hat_6(e), Z_hat_6(W_A), Z_hat_6(W_B), Z_hat_6(W_C)}`
were fixed, the higher-orbit beta-side coefficients would still not be
determined by those four scalars alone  
**Script:** `scripts/frontier_gauge_vacuum_plaquette_identity_plus_three_sample_higher_orbit_underdetermination_2026_04_17.py`

## Question

Suppose future work somehow evaluates the whole first sample packet

- `Z_hat_6(e)`,
- `Z_hat_6(W_A)`,
- `Z_hat_6(W_B)`,
- `Z_hat_6(W_C)`.

Would those four exact scalars determine the full beta-side environment vector
`v_6`?

## Answer

No.

Those four scalars are still only four linear functionals of the full
conjugation-symmetric beta-side coefficient sequence.

Already on any five-dimensional higher-orbit subspace of the coefficient bank,
the map

`higher-orbit coefficients -> (Z_hat_6(e), Z_hat_6(W_A), Z_hat_6(W_B), Z_hat_6(W_C))`

has nontrivial kernel by dimension alone.

Because the identity row has strictly positive weights, any nonzero kernel
vector must contain both positive and negative entries.

So one can start from a strictly positive higher-orbit baseline coefficient
vector and perturb by `± epsilon` times that kernel vector. For small enough
`epsilon`, both perturbed coefficient stacks remain nonnegative and distinct,
yet they give exactly the same identity value and the same three named sample
values.

Therefore even the full first sample packet still does **not** determine the
higher-orbit beta-side coefficients, and hence does **not** determine the full
beta-side vector `v_6`.

## Setup

From
[GAUGE_VACUUM_PLAQUETTE_FIRST_THREE_SAMPLE_ENVIRONMENT_EVALUATOR_ROUTE_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_FIRST_THREE_SAMPLE_ENVIRONMENT_EVALUATOR_ROUTE_NOTE_2026-04-17.md):

- the named environment values are linear functionals of the beta-side vector
  `v_6`,
- and the three-sample route is

  `mathbf_Z_6 = E_3(v_6)`.

From
[GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_CHARACTER_TRUNCATION_ENVELOPE_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_CHARACTER_TRUNCATION_ENVELOPE_NOTE_2026-04-17.md):

- the normalized class function is a conjugation-symmetric nonnegative
  character expansion.

So both the identity value and every named marked-holonomy sample are linear
functionals of the beta-side coefficient bank.

## Theorem 1: four sample scalars do not determine a five-dimensional higher-orbit slice

Choose any five independent higher conjugation-symmetric orbit basis vectors.
For definiteness, take the orbit representatives

`(0,2), (0,3), (0,4), (0,5), (0,6)`.

Let `u in R^5` denote their coefficient vector, and let

`L(u) = (Z_hat_6(e), Z_hat_6(W_A), Z_hat_6(W_B), Z_hat_6(W_C))`

be the four-scalar summary map restricted to this five-orbit slice.

Then `L` is a linear map

`R^5 -> R^4`.

Therefore `ker(L)` is nontrivial.

So there exists a nonzero higher-orbit direction that leaves all four summary
scalars unchanged.

## Theorem 2: the kernel necessarily contains sign-changing directions

For every chosen higher orbit, the identity component of `L` is the strictly
positive orbit weight

`m_(p,q) d_(p,q)^2`,

with multiplicity `m_(p,q) = 2` for `p < q` and `m_(p,q) = 1` for `p = q`.

If a nonzero kernel vector had all coefficients nonnegative or all
nonpositive, its identity component could not vanish because it would be a
nontrivial sum of strictly positive weights.

Therefore every nonzero kernel vector must have both positive and negative
entries.

## Corollary 1: explicit positive witness pair with the same first sample packet

Let `k` be any nonzero kernel vector on the chosen five-orbit slice, and let

`b = (1,1,1,1,1)`

be the strictly positive baseline vector.

Because `k` has finite entries, there exists `epsilon > 0` small enough that

`b_+ = b + epsilon k`,

`b_- = b - epsilon k`

both remain entrywise nonnegative.

Since `k in ker(L)`,

`L(b_+) = L(b_-)`.

But `b_+ != b_-`.

So there are already two distinct nonnegative higher-orbit coefficient stacks
with the same identity value and the same three named sample values.

## What this closes

- exact proof that the four-scalar first sample packet does **not** determine
  the higher-orbit beta-side coefficients
- exact proof that the first sample packet does **not** determine the full
  beta-side vector `v_6`
- exact clarification that even complete first-sample closure would still not
  finish the full beta-side environment solve

## What this does not close

- the true explicit higher-orbit coefficient stack
- the true explicit beta-side vector `v_6`
- the true explicit values `Z_6^env(W_A)`, `Z_6^env(W_B)`, `Z_6^env(W_C)`
- the full plaquette PF closure
- the global sole-axiom PF selector theorem

## Why this matters

This theorem tightens the work order again.

The first sample program is still useful: it closes the first retained seam and
tests candidate beta-side solves.

But it is now mathematically clear that:

- even exact closure of `e, W_A, W_B, W_C` would still not determine the full
  higher-orbit beta-side data,
- so the real load-bearing object is the actual beta-side environment operator
  or vector, not any finite sample packet by itself.
