# Gauge-Vacuum Plaquette First Propagated Retained Triple Target

**Date:** 2026-04-17  
**Status:** exact science-only target theorem sharpening the next honest
`beta = 6` plaquette evaluator object  
**Script:** `scripts/frontier_gauge_vacuum_plaquette_first_propagated_retained_triple_target_2026_04_17.py`

## Question

After the evaluator-route reduction theorem, what is the strongest honest next
evaluative target on the plaquette `beta = 6` operator lane?

Is it:

- the full infinite class-sector matrix of `S_6^env`,
- the full family `W -> eta_6(W)`,
- or some smaller exact propagated object?

## Bottom line

It is a smaller propagated object.

The first honest next evaluative target is:

- the propagated retained three-sample output

  `(Z_6^env(W_A), Z_6^env(W_B), Z_6^env(W_C))`,

equivalently:

- the first retained propagated coefficient triple of the common beta-side
  vector `v_6` on

  `span{Phi_0, Phi_1, Phi_2}`,

with

`Phi_0 = chi_(0,0)`,

`Phi_1 = chi_(1,0) + chi_(0,1)`,

`Phi_2 = chi_(1,1)`.

So the next honest plaquette evaluator theorem is not “evaluate everything.”
It is:

- evaluate the first propagated retained triple,
- then recover the first retained propagated coefficients by the already-fixed
  exact radical map.

## What is already exact

### 1. The operator-side seam is already reduced to one common beta-side vector

From
[GAUGE_VACUUM_PLAQUETTE_FIRST_THREE_SAMPLE_ENVIRONMENT_EVALUATOR_ROUTE_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_FIRST_THREE_SAMPLE_ENVIRONMENT_EVALUATOR_ROUTE_NOTE_2026-04-17.md):

- the actual evaluator route is already exactly

  `v_6 -> E_3 -> (Z_A, Z_B, Z_C)`,

- with one fixed three-row sample operator `E_3`,
- and on the first symmetric retained witness sector that operator is exactly
  the radical matrix `F`.

So the true target is already a propagated finite object, not the whole
class-sector matrix.

### 2. The three named samples are already the first exact same-surface target set

From
[GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_RECONSTRUCTION_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_RECONSTRUCTION_NOTE_2026-04-17.md):

- the first symmetric retained witness sector is already fixed,
- and the three named holonomies `W_A, W_B, W_C` are already the first exact
  same-surface target set.

### 3. The inversion map is already exact

From
[GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_EXACT_RADICAL_RECONSTRUCTION_MAP_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_EXACT_RADICAL_RECONSTRUCTION_MAP_NOTE_2026-04-17.md):

- the sample operator on the first retained witness sector is the explicit
  radical matrix `F`,
- `det(F) != 0`,
- and the inverse map from `(Z_A, Z_B, Z_C)` to the first retained coefficient
  triple is already exact.

So no additional reconstruction design remains on this first retained sector.

### 4. The current stack still does not determine even this triple

From
[GAUGE_VACUUM_PLAQUETTE_FIRST_THREE_SAMPLE_ENVIRONMENT_EVALUATOR_ROUTE_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_FIRST_THREE_SAMPLE_ENVIRONMENT_EVALUATOR_ROUTE_NOTE_2026-04-17.md):

- the current exact stack still does **not** determine even the normalized
  three-sample triple.

So this propagated retained triple is not already closed; it is the exact next
honest target.

## Theorem 1: exact first evaluative target on the plaquette `beta = 6` operator lane

Assume the exact evaluator-route theorem, the exact first three-sample
reconstruction theorem, and the exact radical reconstruction-map theorem.

Then:

1. the live operator-side `beta = 6` seam already factors through one common
   beta-side vector `v_6`;
2. on the first retained witness sector, the propagated output is exactly the
   three-sample triple `(Z_A, Z_B, Z_C)`;
3. the recovery of the first retained propagated coefficients from that triple
   is already exact and fixed by the radical inverse map.

Therefore the first honest next evaluative target on the plaquette operator
lane is the propagated retained three-sample triple

`(Z_6^env(W_A), Z_6^env(W_B), Z_6^env(W_C))`,

equivalently the first retained propagated coefficient triple of `v_6`.

## Corollary 1: the next theorem target is finite from the start

The next positive plaquette evaluator attempt may be framed as:

- evaluate `Z_6^env(W_A)`,
- evaluate `Z_6^env(W_B)`,
- evaluate `Z_6^env(W_C)`,
- then apply the exact radical inverse map.

It does **not** need to start as:

- evaluation of the full infinite class-sector matrix of `S_6^env`,
- or evaluation of the full family `W -> eta_6(W)` at once.

## Corollary 2: this does not remove the underlying operator gap

This note does **not** claim that the retained triple is already determined.

It only fixes the next honest target shape.

The actual missing operator-side content still lives in the explicit
class-sector evaluation of `S_6^env` and `eta_6(W)`.

## What this closes

- one exact sharpening of the next honest plaquette evaluator target
- one exact reduction from a vague infinite operator ask to a first propagated
  retained triple
- one exact identification of the first retained propagated coefficient triple
  as the equivalent finite target

## What this does not close

- explicit values of `Z_6^env(W_A)`, `Z_6^env(W_B)`, `Z_6^env(W_C)`
- explicit class-sector matrix elements of `S_6^env`
- explicit class-sector matrix elements of `eta_6(W)`
- full plaquette `beta = 6` operator closure
- global PF closure

## Why this matters

This is the first place where the live plaquette operator seam is reduced to a
finite propagated target without pretending the operator evaluation is already
done.

The branch now knows the next positive plaquette target as a concrete finite
object.

## Command

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_first_propagated_retained_triple_target_2026_04_17.py
```
