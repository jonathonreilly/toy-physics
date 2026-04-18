# DM Wilson Direct-Descendant Positive-Branch Compatibility And Insufficiency Theorem

**Date:** 2026-04-18  
**Status:** exact theorem exhausting the "positive branch alone" selector
direction on the live DM flagship route  
**Script:** `scripts/frontier_dm_wilson_direct_descendant_positive_branch_compatibility_and_insufficiency_theorem_2026_04_18.py`

## Question

After rewriting the current imposed branch-choice rule as the projected-source
discriminant

`Delta_src(dW_e^H) = det(H_e)`,

can the live DM selector problem be closed by demanding only:

- the positive projected-source branch `Delta_src > 0`,
- together with the constructive triplet-sign chamber
  `gamma > 0`, `E1 > 0`, `E2 > 0`?

Or does that still leave a nontrivial point-selection problem?

## Bottom line

It still leaves a nontrivial point-selection problem.

The good news is positive:

- the exact constructive `eta / eta_obs = 1` point from the PMNS continuity
  theorem already lies on the positive projected-source branch
  `Delta_src > 0`.

So there is no incompatibility between:

- exact constructive closure,
- the constructive triplet-sign chamber,
- and the positive projected-source branch.

But that is still not enough to close the selector.

The same explicit continuity family also contains nearby and endpoint points
with:

- `Delta_src > 0`,
- `gamma > 0`,
- `E1 > 0`,
- `E2 > 0`,

but with different transport values, including `eta / eta_obs > 1`.

Therefore the condition

- `Delta_src > 0` plus the constructive triplet-sign chamber

is only a **branch-level condition**, not a point-selection law.

So this direction is exhausted:

- the next positive theorem must be finer than branch sign plus triplet signs.

## What is already exact

### 1. Exact constructive closure exists on the fixed native `N_e` seed surface

From
[DM_LEPTOGENESIS_PMNS_CONSTRUCTIVE_CONTINUITY_CLOSURE_THEOREM_NOTE_2026-04-17.md](./DM_LEPTOGENESIS_PMNS_CONSTRUCTIVE_CONTINUITY_CLOSURE_THEOREM_NOTE_2026-04-17.md):

- there exists an exact `lambda_* in (0,1)` on the explicit interpolation
  family with
  `eta_1(lambda_*) = 1`;
- at that same point the projected-source triplet satisfies
  `gamma > 0`, `E1 > 0`, `E2 > 0`.

So the constructive chamber already contains an exact closure point.

### 2. The imposed branch-choice rule already has an exact projected-source scalar representative

From
[DM_WILSON_DIRECT_DESCENDANT_PROJECTED_SOURCE_BRANCH_DISCRIMINANT_THEOREM_NOTE_2026-04-18.md](./DM_WILSON_DIRECT_DESCENDANT_PROJECTED_SOURCE_BRANCH_DISCRIMINANT_THEOREM_NOTE_2026-04-18.md):

- `Delta_src(dW_e^H) = det(H_e)`;
- the current imposed positive-`det` branch-choice rule can therefore be
  written exactly as `Delta_src > 0` on the projected-source pack.

So the live conditional is now an explicit scalar at the `dW_e^H` endpoint.

## Theorem 1: exact constructive closure is compatible with the positive projected-source branch

Let `lambda_*` be the exact continuity-closure point from the constructive
continuity theorem.

Then at `lambda_*`:

- `eta_1(lambda_*) = 1`,
- `gamma(lambda_*) > 0`,
- `E1(lambda_*) > 0`,
- `E2(lambda_*) > 0`,
- `Delta_src(lambda_*) > 0`.

So the exact constructive closure point lies on the positive projected-source
branch.

### Reason

The continuity theorem already gives the first four items. Evaluating the exact
projected-source discriminant at that same point gives a strictly positive
value:

`Delta_src(lambda_*) = 0.006583113927... > 0`.

Therefore positive branch and exact constructive closure are compatible.

## Theorem 2: positive branch plus constructive signs is not a point selector

Along the same explicit continuity family there exists `lambda_+ > lambda_*`
such that:

- `Delta_src(lambda_+) > 0`,
- `gamma(lambda_+) > 0`,
- `E1(lambda_+) > 0`,
- `E2(lambda_+) > 0`,
- but `eta_1(lambda_+) > 1`.

One explicit witness is

- `lambda_+ = lambda_* + 10^{-3}`,

for which the branch remains positive and constructive, while the transport
value has already moved to

- `eta_1(lambda_+) = 1.000445222278... > 1`.

Therefore the conjunction

- `Delta_src > 0`,
- `gamma > 0`,
- `E1 > 0`,
- `E2 > 0`

does not determine the physical point even inside the constructive positive
branch.

### Reason

At `lambda_*`, all four microscopic inequalities are strict. Since the path is
continuous and those quantities are continuous functions of the path
parameter, they stay positive on a small one-sided neighborhood of
`lambda_*`.

But `eta_1(1) > 1` while `eta_1(lambda_*) = 1`, so the path does not stop at
`lambda_*`. A nearby point on the same positive constructive branch already has
a different transport value.

So the branch condition is compatible but insufficient.

## Corollary 1: the "positive branch only" route is exhausted

This is the clean exhaustion statement for the current direct-descendant
subdirection.

It is not enough to search for a right-sensitive law proving only:

- `Delta_src(dW_e^H) > 0`.

Nor is it enough to combine that with the already-known triplet-sign chamber:

- `gamma > 0`,
- `E1 > 0`,
- `E2 > 0`.

Those conditions choose the right kind of branch, but they still do not choose
the point.

## Corollary 2: the next positive theorem must be finer than branch sign plus triplet signs

The remaining unexhausted target is therefore:

- a finer right-sensitive microscopic law on `L_e / dW_e^H`
  inside the positive constructive branch,

not merely:

- a proof that the physical point lies on `Delta_src > 0`.

In practice that means the next theorem must constrain additional full-pack
projected-source data beyond `(gamma, E1, E2)` and the branch discriminant.

## What this closes

- the question whether `Delta_src > 0` is compatible with exact constructive
  closure
- the question whether positive branch plus constructive sign chamber already
  finishes the selector
- the "positive branch only" subdirection

## What this does not close

- a retained selector law for the physical source point
- a finer right-sensitive microscopic `L_e / dW_e^H` law inside the positive
  constructive branch
- the final DM flagship closeout
