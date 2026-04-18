# Gauge-Vacuum Plaquette First Symmetric Three-Sample Reconstruction

**Date:** 2026-04-17  
**Status:** exact retained-sector constructive theorem on the plaquette PF lane;
the first nontrivial conjugation-symmetric retained coefficient triple is
recoverable from three explicit regular rational-angle marked holonomies  
**Script:** `scripts/frontier_gauge_vacuum_plaquette_first_symmetric_three_sample_reconstruction_2026_04_17.py`

## Question

After the conjugation-symmetric retained-sampling reduction theorem, can the
first nontrivial symmetric retained coefficient triple be tied to one explicit
sample target set rather than only to generic existence?

## Answer

Yes.

On the first symmetric retained witness sector

`v = a_(0,0) chi_(0,0)
   + a_(1,0) (chi_(1,0) + chi_(0,1))
   + a_(1,1) chi_(1,1)`,

the coefficients `(a_(0,0), a_(1,0), a_(1,1))` are recoverable from the three
explicit marked torus holonomies

`W_A = W(-13 pi / 16,  5 pi / 8)`,

`W_B = W( -5 pi / 16, -7 pi / 16)`,

`W_C = W(  7 pi / 16,-11 pi / 16)`,

where

`W(theta1,theta2)
 = diag(exp(i theta1), exp(i theta2), exp(-i(theta1+theta2)))`.

For these three regular sample points, the symmetric orbit-evaluation matrix is
invertible.

So once the three same-surface values

`Z_A = Z_6^env(W_A)`,

`Z_B = Z_6^env(W_B)`,

`Z_C = Z_6^env(W_C)`

are explicitly evaluated, the first symmetric retained coefficient triple
follows immediately by one fixed `3 x 3` linear inversion.

## Setup

From
[GAUGE_VACUUM_PLAQUETTE_CONJUGATION_SYMMETRIC_RETAINED_SAMPLING_REDUCTION_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_CONJUGATION_SYMMETRIC_RETAINED_SAMPLING_REDUCTION_NOTE_2026-04-17.md):

- the physical retained plaquette coefficients already satisfy conjugation
  symmetry,
- so the first four-weight retained witness reduces to the three symmetric orbit
  coefficients above,
- and three generic marked-holonomy samples are generically enough.

The present theorem replaces generic existence by one explicit sample target
set.

## Theorem 1: explicit three-sample reconstruction law on the first symmetric witness sector

Let

`Phi_0 = chi_(0,0)`,

`Phi_1 = chi_(1,0) + chi_(0,1)`,

`Phi_2 = chi_(1,1)`.

For the three explicit marked holonomies `W_A, W_B, W_C` above, define the
sample matrix

`F_(ij) = <K(W_i), Phi_j>`,

with `i in {A,B,C}` and `j in {0,1,2}`.

Then

`[ Z_A ]   [F_(A0) F_(A1) F_(A2)] [a_(0,0)]`
`[ Z_B ] = [F_(B0) F_(B1) F_(B2)] [a_(1,0)]`
`[ Z_C ]   [F_(C0) F_(C1) F_(C2)] [a_(1,1)]`.

For this explicit sample set, `det(F) != 0`.

Therefore

`a = F^(-1) Z`,

so the first symmetric retained coefficient triple is exactly recoverable from
the three sample values.

## Corollary 1: the first explicit retained PF sample target set

The first symmetric retained `beta = 6` PF target is no longer only “evaluate
some generic three samples.”

It can now be stated explicitly:

- evaluate `Z_6^env(W_A)`,
- evaluate `Z_6^env(W_B)`,
- evaluate `Z_6^env(W_C)`,
- then recover `(a_(0,0), a_(1,0), a_(1,1))` by the fixed inverse matrix.

## Corollary 2: one sample already decouples the `chi_(1,1)` orbit

For the explicit sample `W_A`, the `(1,1)` orbit contribution vanishes on the
runner witness:

`F_(A2) = 0`.

So the first row already decouples the `chi_(1,1)` orbit, making the explicit
three-sample reconstruction especially clean.

## Explicit witness

For the exact sample set above, the runner finds:

- `|det(F)| = 10.810321693970609`,
- `cond(F) = 1.9575988062794747`,
- and the inverse matrix is numerically stable.

So this is not only an exact sample target set but a well-conditioned one.

## What this closes

- one explicit regular rational-angle three-sample target set for the first
  symmetric retained coefficient triple
- exact clarification that the first retained PF sample target is no longer only
  generic existence
- exact reduction of the first symmetric retained beta=6 step to evaluation of
  three named same-surface sample values

## What this does not close

- explicit same-surface values `Z_6^env(W_A)`, `Z_6^env(W_B)`, `Z_6^env(W_C)`
- explicit closed-form class-sector matrix elements of `K_6^env`
- explicit closed-form class-sector matrix elements of `B_6(W)`
- explicit coefficients beyond the first symmetric retained witness sector
- the global sole-axiom PF selector theorem

## Why this matters

This is the first place where the live PF seam turns into a short concrete
shopping list.

The branch no longer says only:

- evaluate low-rank matrix elements somehow.

It now says:

- evaluate these three exact marked-holonomy samples,
- and the first symmetric retained coefficients follow automatically.

## Command

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_first_symmetric_three_sample_reconstruction_2026_04_17.py
```

Expected summary:

- `THEOREM PASS=6 SUPPORT=3 FAIL=0`
