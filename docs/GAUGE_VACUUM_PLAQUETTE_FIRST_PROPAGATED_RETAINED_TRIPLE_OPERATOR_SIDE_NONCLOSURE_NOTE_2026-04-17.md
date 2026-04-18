# Gauge-Vacuum Plaquette First Propagated Retained Triple Operator-Side Nonclosure

**Date:** 2026-04-17  
**Status:** exact PF-only operator-side nonclosure theorem at the minimal
propagated plaquette target; even exact evaluation of the propagated retained
three-sample triple still does **not** determine the full beta-side vector or
the unresolved operator-side `beta = 6` data on the present bank  
**Script:** `scripts/frontier_gauge_vacuum_plaquette_first_propagated_retained_triple_operator_side_nonclosure_2026_04_17.py`

## Question

After the propagated-retained-triple target theorem, the current-bank
minimality no-go, and the fixed-retained-pair / fixed-`Tau` noncollapse
theorem, what would actually happen if future work somehow evaluated the exact
minimal propagated target

`(Z_6^env(W_A), Z_6^env(W_B), Z_6^env(W_C))`?

Would that by itself close the unresolved operator-side `beta = 6` object?

## Answer

No.

That finite propagated target is the right next evaluative target, but it is
still **not** the whole operator-side closure datum.

Already on the explicit four-orbit higher slice

`{(0,2), (0,3), (0,4), (0,5)}`,

the propagated-triple map

`higher-orbit coefficients -> (Z_6^env(W_A), Z_6^env(W_B), Z_6^env(W_C))`

has nontrivial kernel by dimension alone:

- domain dimension `4`,
- codomain dimension `3`.

Moreover, the runner exhibits an explicit sign-changing kernel direction on
that slice. Starting from a strictly positive baseline and perturbing by small
positive and negative multiples of that kernel direction yields two distinct
nonnegative higher-orbit coefficient stacks with the **same exact propagated
triple**.

So even exact knowledge of the minimal propagated three-sample target would
still not determine:

- the higher-orbit beta-side coefficient stack,
- the full beta-side vector `v_6`,
- or the operator-side `beta = 6` data that generate that vector.

This is the operator-side clarification that was still missing:

- the propagated retained triple is the right next finite target,
- but it is not itself an operator-side closure theorem.

## Setup

From
[GAUGE_VACUUM_PLAQUETTE_FIRST_PROPAGATED_RETAINED_TRIPLE_TARGET_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_FIRST_PROPAGATED_RETAINED_TRIPLE_TARGET_NOTE_2026-04-17.md):

- the first honest next plaquette evaluator target is the propagated retained
  three-sample triple

  `(Z_6^env(W_A), Z_6^env(W_B), Z_6^env(W_C))`.

From
[GAUGE_VACUUM_PLAQUETTE_FIRST_THREE_SAMPLE_ENVIRONMENT_EVALUATOR_ROUTE_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_FIRST_THREE_SAMPLE_ENVIRONMENT_EVALUATOR_ROUTE_NOTE_2026-04-17.md):

- that triple already factors exactly as

  `mathbf_Z_6 = E_3(v_6)`,

- through one common beta-side vector `v_6` and one fixed left sample operator
  `E_3`.

From
[GAUGE_VACUUM_PLAQUETTE_IDENTITY_PLUS_THREE_SAMPLE_HIGHER_ORBIT_UNDERDETERMINATION_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_IDENTITY_PLUS_THREE_SAMPLE_HIGHER_ORBIT_UNDERDETERMINATION_NOTE_2026-04-17.md)
and
[GAUGE_VACUUM_PLAQUETTE_FINITE_SAMPLE_PACKET_NONCLOSURE_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_FINITE_SAMPLE_PACKET_NONCLOSURE_NOTE_2026-04-17.md):

- finite sample packets do not determine the full higher-orbit beta-side data.

The new point is sharper and more local to the live frontier:

- even the exact minimal propagated three-sample target, taken by itself, still
  does not close the operator-side `beta = 6` object.

## Theorem 1: the propagated retained triple already has higher-orbit kernel freedom on an explicit four-orbit slice

Restrict the higher-orbit beta-side bank to the conjugation-symmetric slice

`{(0,2), (0,3), (0,4), (0,5)}`.

Let `c in R^4` be the coefficient vector on that slice, and let

`T_3(c) = (Z_A(c), Z_B(c), Z_C(c))`

be the propagated retained three-sample map.

Then:

1. `T_3` is linear;
2. `dim(domain) = 4`;
3. `dim(codomain) = 3`.

Therefore `ker(T_3)` is nontrivial.

So the propagated retained triple alone cannot determine the higher-orbit
coefficient vector even on this explicit finite slice.

## Corollary 1: explicit positive witness pair with the same propagated retained triple

On the explicit slice `{(0,2), (0,3), (0,4), (0,5)}`, the runner finds a
sign-changing kernel direction

`k = (-0.4885403546..., 0.7722564727..., -0.3682858226..., 0.1712127884...)`

with

`T_3(k) = 0`.

Take the strictly positive baseline

`b = (1, 1, 1, 1)`

and `epsilon = 4/5`.

Define

`P = b + epsilon k`,

`Q = b - epsilon k`.

Then:

- `P != Q`,
- `P, Q >= 0` entrywise,
- and

  `T_3(P) = T_3(Q)`.

So there are already two explicit distinct nonnegative higher-orbit
coefficient stacks with the same exact propagated retained triple.

## Corollary 2: exact propagated-triple closure would still not be operator-side closure

Because the evaluator route is exactly

`mathbf_Z_6 = E_3(v_6)`,

and because the same propagated triple can arise from distinct admissible
higher-orbit beta-side vectors, exact evaluation of the minimal propagated
three-sample target would still not by itself determine:

- the full beta-side vector `v_6`,
- the higher-orbit environment distribution,
- or the unresolved operator-side `beta = 6` data that generate them.

So the branch can now say the sharper thing:

- the propagated retained triple is the correct finite *target*,
- but it is still not an operator-side *closure* datum.

## Corollary 3: no contradiction with the exact radical reconstruction map

The exact radical reconstruction map recovers the first retained propagated
coefficient triple from the propagated three-sample target.

The present theorem does not contradict that.

It says only that the same propagated triple still leaves nonunique
higher-orbit data beyond that first retained propagated block.

So the target triple can be sufficient for first retained propagated
coefficients while still being insufficient for full operator-side closure.

## What this closes

- one exact operator-side clarification at the exact minimal propagated
  plaquette target;
- one exact theorem that the propagated retained triple already has
  higher-orbit kernel freedom on an explicit four-orbit slice;
- one explicit positive witness pair with the same propagated retained triple;
- one exact clarification that evaluating the target triple would still not by
  itself close the unresolved operator-side `beta = 6` data.

## What this does not close

- explicit values of `Z_6^env(W_A)`, `Z_6^env(W_B)`, `Z_6^env(W_C)`;
- the true explicit beta-side vector `v_6`;
- the true explicit operator data `K_6^env / B_6(W)`;
- the full plaquette PF closure;
- the global sole-axiom PF selector theorem.

## Why this matters

This is the cleanest operator-side clarification yet on the plaquette lane.

The branch no longer has to speak as if the propagated retained triple were
either:

- too small to matter, or
- enough to close the whole operator-side problem.

It can now say the correct thing:

- the propagated retained triple is the right next finite evaluator target,
- but even exact closure of that target would still leave genuine operator-side
  nonuniqueness on the current bank.

So the remaining load-bearing datum is still explicit operator-side
`beta = 6` data, not merely one more finite propagated sample theorem.

## Command

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_first_propagated_retained_triple_operator_side_nonclosure_2026_04_17.py
```
