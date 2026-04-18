# Gauge-Vacuum Plaquette Retained Class-Sampling Inversion

**Date:** 2026-04-17  
**Status:** exact retained-sector constructive theorem on the plaquette PF lane;
on every finite retained marked class sector, the truncated coefficient vector is
exactly recoverable from finitely many generic marked-holonomy samples of the
compressed boundary class function  
**Script:** `scripts/frontier_gauge_vacuum_plaquette_retained_class_sampling_inversion_2026_04_17.py`

## Question

After the compressed boundary functional is known explicitly as

`Z_beta^env(W) = <K_Lambda(W), v_beta^Lambda>`,

is the retained finite-sector problem still an abstract infinite ambiguity, or
does it reduce to one finite constructive inversion problem?

## Answer

It reduces to one finite constructive inversion problem on every retained finite
sector.

Fix a finite retained marked class sector

`H_Lambda = span{chi_lambda : lambda in Lambda}`,

with `|Lambda| = N`.

For marked holonomies `W_1, ..., W_N`, define the evaluation matrix

`E_(i,lambda) = d_lambda chi_lambda(W_i)`.

Then for every retained coefficient vector

`v_beta^Lambda = sum_(lambda in Lambda) c_lambda chi_lambda`,

the sampled boundary values satisfy

`Z_beta^env(W_i) = sum_(lambda in Lambda) E_(i,lambda) c_lambda`.

Whenever the chosen marked holonomies are generic enough that `E` is invertible,
the retained coefficient vector is recovered exactly:

`c = E^(-1) Z`.

So the retained finite-sector PF seam is no longer a vague coefficient cloud.
It is one exact finite inversion problem.

## Setup

From
[GAUGE_VACUUM_PLAQUETTE_COMPRESSED_RIM_EVALUATION_THEOREM_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_COMPRESSED_RIM_EVALUATION_THEOREM_NOTE_2026-04-17.md):

- on the marked class sector,
  `Z_beta^env(W) = <K(W), v_beta>`,
- all `W`-dependence is already explicit in the Peter-Weyl evaluation vector.

From
[GAUGE_VACUUM_PLAQUETTE_COMPRESSED_RIM_FUNCTIONAL_UNIQUENESS_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_COMPRESSED_RIM_FUNCTIONAL_UNIQUENESS_NOTE_2026-04-17.md):

- on every retained finite sector, the left boundary functional is already the
  universal retained Peter-Weyl evaluation functional,
- so there is no further retained left-functional ambiguity.

From
[GAUGE_VACUUM_PLAQUETTE_BETA6_SCALAR_VALUE_INSUFFICIENCY_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_BETA6_SCALAR_VALUE_INSUFFICIENCY_NOTE_2026-04-17.md):

- one scalar same-surface value does **not** determine the retained coefficient
  vector.

So the next honest retained constructive target is finite inversion from enough
independent samples.

## Theorem 1: exact retained finite-sampling law

Let `Lambda` be any finite retained set of marked class labels, and write

`v^Lambda = sum_(lambda in Lambda) c_lambda chi_lambda`.

For any marked holonomy `W`,

`Z^Lambda(W) = <K_Lambda(W), v^Lambda>
             = sum_(lambda in Lambda) d_lambda c_lambda chi_lambda(W)`.

So for a sample set `W_1, ..., W_m`, the sampled values satisfy the exact
linear system

`Z_i = sum_(lambda in Lambda) E_(i,lambda) c_lambda`,

with

`E_(i,lambda) = d_lambda chi_lambda(W_i)`.

## Corollary 1: generic full-rank samples determine the retained coefficient vector

If `m = |Lambda| = N` and the sample matrix `E` is invertible, then the retained
coefficient vector is recovered exactly:

`c = E^(-1) Z`.

So on every retained finite marked class sector, exact coefficient recovery is a
finite holonomy-sampling problem.

## Corollary 2: too few samples remain underdetermined

If `m < N`, then the sample system cannot generically determine all `N`
retained coefficients.

So the scalar-value insufficiency theorem is the first case of a more general
fact: one needs enough independent marked-holonomy samples to recover the
retained coefficient vector.

## Explicit witness

Take the retained four-weight sector

`Lambda = {(0,0), (1,0), (0,1), (1,1)}`.

Choose four generic marked torus holonomies `W_i`.

Then the `4 x 4` evaluation matrix

`E_(i,lambda) = d_lambda chi_lambda(W_i)`

is invertible for the generic witness used in the runner, and one recovers the
retained coefficient vector exactly from the four sampled values.

By contrast, any three-sample submatrix leaves one retained direction
underdetermined.

## What this closes

- exact retained finite-sector reduction of coefficient recovery to linear
  inversion of a marked-holonomy sampling matrix
- exact clarification that the retained constructive target is finite once a
  retained sector is chosen
- exact clarification that one scalar sample is just the rank-1 endpoint of a
  general sampling/inversion structure

## What this does not close

- explicit same-surface values of the needed marked-holonomy samples
- explicit closed-form class-sector matrix elements of `K_6^env`
- explicit closed-form class-sector matrix elements of `B_6(W)`
- explicit full infinite-sector coefficient data
- the global sole-axiom PF selector theorem

## Why this matters

This is the first genuinely constructive retained-sector upgrade after the
scalar-value insufficiency theorem.

The branch can now say something stronger and more useful:

- one scalar sample is not enough,
- but a finite retained truncation is exactly recoverable from a finite generic
  sample set,
- so the next explicit PF work can target chosen marked-holonomy samples rather
  than an undifferentiated infinite coefficient cloud.

## Command

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_retained_class_sampling_inversion_2026_04_17.py
```

Expected summary:

- `THEOREM PASS=6 SUPPORT=3 FAIL=0`
