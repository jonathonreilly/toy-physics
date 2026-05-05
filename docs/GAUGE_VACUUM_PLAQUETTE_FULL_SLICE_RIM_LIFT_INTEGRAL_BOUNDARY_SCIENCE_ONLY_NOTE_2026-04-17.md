# Gauge-Vacuum Plaquette Full-Slice Rim-Lift Integral Boundary

**Date:** 2026-04-17
**Status:** exact local rim-integral boundary theorem on the plaquette PF
lane; `B_beta(W)` and its compressed descendant `eta_beta(W)` are fixed at the
level of one exact local Wilson/Haar rim integral, but explicit closed-form
`beta = 6` evaluation is not derived
**Type:** positive_theorem
**Runner:** `scripts/frontier_gauge_vacuum_plaquette_first_three_sample_local_wilson_retained_positive_cone_obstruction_2026_04_17.py`

## Question

After the compressed rim-functional uniqueness theorem isolated the remaining
local issue as the full slice lift `B_beta(W)`, is that lift still only an
unnamed existential object, or is it already fixed at the level of an exact
local Wilson/Haar construction?

## Answer

It is already fixed at the level of an exact local Wilson/Haar construction.

Let `H_slice` be the orthogonal-slice Hilbert space of one unmarked edge slice
adjacent to the marked plaquette. For fixed marked holonomy `W` and slice
boundary data `U`, let `Xi^rim` denote the unmarked Wilson link variables in
the finite rim neighborhood touching that marked plaquette and the edge slice.

Then the full-slice local rim lift is the exact slice-space boundary function

`B_beta(W)(U)
 = integral_(Omega^rim(U)) dmu_H(Xi^rim)
     exp[(beta / 3) A^rim(U, Xi^rim; W)]`,

where `A^rim` is the local Wilson rim action. This is the full-slice
pre-compression local boundary object.

Its canonical marked class-sector descendant is exactly

`eta_beta(W) = P_cls B_beta(W)`.

So the current exact stack fixes both objects at the integral-expression
level:

- `B_beta(W)` as the full-slice local Wilson/Haar rim lift,
- `eta_beta(W)` as its canonical compressed boundary state.

What is still open is not the construction class of those objects. It is their
explicit evaluation, especially at `beta = 6`.

## Setup

From the exact spatial-environment transfer theorem already on `main`:

- `eta_beta(W)` is the exact boundary state induced on one edge slice by the
  local rim coupling of the marked plaquette holonomy to the adjacent
  unmarked slice,
- `Z_beta^env(W)` is a boundary amplitude generated from the orthogonal-slice
  transfer law.

From the exact local/environment factorization theorem:

- after trivial-channel normalization, non-marked mixed-link factors are
  rep-independent scalars on the marked source sector,
- so the remaining nontrivial local marked data sit on the rim adjacent to the
  marked plaquette.

From the current PF-lane kernel/rim compression statement:

- the compressed boundary slot is already canonically written as
  `eta_beta(W) = P_cls B_beta(W)`.

From the current one-slab kernel integral boundary statement:

- the bulk environment kernel `K_beta^env` is a separate one-slab Haar
  integral,
- and the marked boundary input is a separate local rim integral.

So the natural next theorem statement is the pre-compression local rim lift
itself.

## Theorem 1: exact full-slice Wilson/Haar rim-lift law

Let `H_slice` be the orthogonal-slice Hilbert space of one edge slice of the
unmarked environment. Let `U` denote slice boundary data on that edge slice,
let `W` be the marked plaquette holonomy, and let `Xi^rim` be the local
unmarked Wilson link variables in the rim neighborhood adjacent to the marked
plaquette.

After the exact local four-link Wilson factor has been separated from the
non-marked mixed-link scalars, the remaining local marked boundary input is
exactly the Wilson/Haar rim integral

`B_beta(W)(U)
 = integral_(Omega^rim(U)) dmu_H(Xi^rim)
     exp[(beta / 3) A^rim(U, Xi^rim; W)]`.

Therefore the full local rim lift `B_beta(W)` is not merely an existential
boundary functional. It is one concrete local Wilson/Haar integral on the full
slice Hilbert space.

## Corollary 1: exact integral-expression law for `eta_beta(W)`

Let `P_cls` denote the canonical compression to the marked class-function
sector. Then the boundary state used on the compressed transfer lane is exactly

`eta_beta(W) = P_cls B_beta(W)`.

So `eta_beta(W)` is not an additional free local input. It is the compressed
descendant of the exact full-slice rim integral already fixed above.

## Corollary 2: strongest honest framework-point statement

At the framework point `beta = 6`, the strongest honest theorem-grade boundary
statement is therefore:

- `B_6(W)` is fixed as one exact local Wilson/Haar rim integral on the full
  slice Hilbert space,
- `eta_6(W)` is fixed as its canonical compressed descendant,
- but no explicit closed-form evaluation of either object is derived here.

So the remaining gap is explicit evaluation of those exact local integrals,
not identification of a different local boundary object.

## What this closes

- exact full-slice construction class for the local rim lift `B_beta(W)`
- exact identification of `eta_beta(W)` as the compressed descendant of that
  rim lift
- exact clarification that the live PF gap is evaluation of explicit local rim
  integrals, not existence of some other local boundary functional

## What this does not close

- explicit closed-form `B_6(W)`
- explicit closed-form `eta_6(W)`
- explicit closed-form `K_6^env`
- explicit coefficients `rho_(p,q)(6)`
- explicit framework-point plaquette PF data
- analytic closure of canonical `P(6)`

## Why this matters

This is the sharpest honest local theorem surface now available on the PF lane.

The branch no longer has to say only that a full-slice rim lift is missing.
It can now say exactly what that lift is at the construction level:

- one local Wilson/Haar rim integral `B_beta(W)`,
- whose compressed descendant is `eta_beta(W)`.

What remains open is the explicit `beta = 6` evaluation problem.

## Command

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_first_three_sample_local_wilson_retained_positive_cone_obstruction_2026_04_17.py
```

Expected summary:

- `THEOREM PASS=6 SUPPORT=3 FAIL=0`
