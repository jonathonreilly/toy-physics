# Gauge-Vacuum Plaquette First Three-Sample Local Wilson Partial Evaluation

**Date:** 2026-04-17  
**Status:** exact local sample-side partial-evaluation theorem on the plaquette
PF lane; the current atlas already fixes the exact local Wilson response at the
named holonomies `W_A, W_B, W_C`, but it still does **not** evaluate the full
environment amplitudes `Z_6^env(W_A)`, `Z_6^env(W_B)`, `Z_6^env(W_C)`  
**Script:** `scripts/frontier_gauge_vacuum_plaquette_first_three_sample_local_wilson_partial_evaluation_2026_04_17.py`

## Question

On the first retained three-sample seam, does the current repo already support
any honest exact sample-side evaluation tied to the actual Wilson objects on
the PF lane, rather than only another abstract reduction statement?

## Answer

Yes, but only locally.

The current atlas already fixes:

- the exact sample matrix on `W_A, W_B, W_C`,
- the exact local `SU(3)` one-plaquette Wilson block at `beta = 6`,
- the exact local marked half-slice multiplier `exp(3 J)`.

Combining those two exact surfaces gives the strongest current exact partial
evaluation on the first three-sample seam:

- the exact sample-side values of `J(W_A), J(W_B), J(W_C)`,
- the exact sample-side half-slice factors `exp(3 J(W_i))`,
- the exact sample-side local Wilson weights `w_6(W_i) = exp(6 J(W_i))`,
- and the exact normalized local one-plaquette values
  `w_6(W_i) / Z_(1plaq)(6)`.

Numerically,

- `w_6(W_A) / Z_(1plaq)(6) = 0.1351652795620484`,
- `w_6(W_B) / Z_(1plaq)(6) = 0.3170224955005416`,
- `w_6(W_C) / Z_(1plaq)(6) = 0.5812139466746343`.

So the branch now has one honest exact first approximant on the named seam:
the local Wilson sample values are explicit.

What remains open is still the full environment completion:

- explicit `B_6(W_i)`,
- explicit `K_6^env`,
- and therefore explicit `Z_6^env(W_i)`.

## Setup

From
[GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_EXACT_RADICAL_RECONSTRUCTION_MAP_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_EXACT_RADICAL_RECONSTRUCTION_MAP_NOTE_2026-04-17.md):

- the named holonomies are

`W_A = W(-13 pi / 16,  5 pi / 8)`,

`W_B = W( -5 pi / 16, -7 pi / 16)`,

`W_C = W(  7 pi / 16,-11 pi / 16)`,

- and the first exact sample-matrix second-column entries are

`a = -3 s`,

`b = -3 r + 3 u + 3 v`,

`d =  3 r + 3 u - 3 v`,

with

`r = sqrt(2)`,

`s = sqrt(2 - sqrt(2))`,

`u = sqrt(2 - sqrt(2 + sqrt(2)))`,

`v = sqrt(2 - sqrt(2 - sqrt(2)))`.

From
[GAUGE_VACUUM_PLAQUETTE_LOCAL_ENVIRONMENT_FACTORIZATION_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_LOCAL_ENVIRONMENT_FACTORIZATION_THEOREM_NOTE.md):

- the local one-link Wilson class function is exactly

`w_beta(g) = exp[(beta / 3) Re Tr g]`.

From
[GAUGE_VACUUM_PLAQUETTE_BRIDGE_SUPPORT_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_BRIDGE_SUPPORT_NOTE.md):

- the local `SU(3)` one-plaquette partition function at `beta = 6` is already
  exact through the Bessel-determinant / Weyl-angle block.

From
[GAUGE_VACUUM_PLAQUETTE_FULL_SLICE_RIM_LIFT_INTEGRAL_BOUNDARY_SCIENCE_ONLY_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_FULL_SLICE_RIM_LIFT_INTEGRAL_BOUNDARY_SCIENCE_ONLY_NOTE_2026-04-17.md):

- the full local rim lift is still one open Wilson/Haar rim integral
  `B_6(W)`,
- so any current sample-side exact evaluation beyond the local Wilson block
  must still be treated as open.

## Theorem 1: exact sample-side values of the local source operator

Let `J = (chi_(1,0) + chi_(0,1)) / 6 = Re Tr / 3`.

Because the second sample-matrix column is

`<K(W), Phi_1> = 3 (chi_(1,0)(W) + chi_(0,1)(W)) = 18 J(W)`,

the three named holonomies satisfy

`18 J(W_A) = -3 s`,

`18 J(W_B) = -3 r + 3 u + 3 v`,

`18 J(W_C) =  3 r + 3 u - 3 v`.

Equivalently,

`J(W_A) = -s / 6`,

`J(W_B) = (-r + u + v) / 6`,

`J(W_C) = ( r + u - v) / 6`.

## Corollary 1: exact sample-side half-slice multipliers

At `beta = 6`, the exact marked half-slice multiplier is `exp(3 J)`.

Therefore

`exp(3 J(W_A)) = exp(-s / 2)`,

`exp(3 J(W_B)) = exp((-r + u + v) / 2)`,

`exp(3 J(W_C)) = exp(( r + u - v) / 2)`.

Numerically,

- `exp(3 J(W_A)) = 0.6820287733505370`,
- `exp(3 J(W_B)) = 1.0445161604563595`,
- `exp(3 J(W_C)) = 1.4142889135419967`.

## Theorem 2: exact sample-side local Wilson one-plaquette values

At `beta = 6`, the local Wilson one-link class function is

`w_6(W) = exp[(6 / 3) Re Tr W] = exp(6 J(W))`.

Hence on the three named holonomies,

`w_6(W_A) = exp(-s)`,

`w_6(W_B) = exp(-r + u + v)`,

`w_6(W_C) = exp( r + u - v)`.

Numerically,

- `w_6(W_A) = 0.4651632476780381`,
- `w_6(W_B) = 1.0910140094544953`,
- `w_6(W_C) = 2.0002131309678010`.

These values are strictly ordered:

`w_6(W_A) < w_6(W_B) < w_6(W_C)`.

## Corollary 2: exact normalized local one-plaquette sample values

Let `Z_(1plaq)(6)` denote the exact local one-plaquette partition function.
From the exact Bessel-determinant mode sum,

`Z_(1plaq)(6) = 3.4414403549877783`.

Therefore the normalized local one-plaquette sample values are exactly

`w_6(W_A) / Z_(1plaq)(6) = 0.1351652795620484`,

`w_6(W_B) / Z_(1plaq)(6) = 0.3170224955005416`,

`w_6(W_C) / Z_(1plaq)(6) = 0.5812139466746343`.

So the current atlas already gives one explicit first sample-side local Wilson
approximant on the first retained PF seam.

## Corollary 3: this is a partial evaluation only

These exact sample-side local Wilson values do **not** yet identify

`Z_6^env(W_A)`,

`Z_6^env(W_B)`,

`Z_6^env(W_C)`.

They evaluate only the exact local Wilson block already proved on the current
atlas.

The full environment amplitudes still require the explicit pre-compression
objects:

- `K_6^env`,
- `B_6(W)`,
- and the resulting full rim/environment completion.

## What this closes

- exact sample-side values of `J(W_A), J(W_B), J(W_C)` on the named seam
- exact sample-side values of the marked half-slice multiplier `exp(3 J(W_i))`
- exact sample-side values of the local Wilson one-plaquette weight
  `w_6(W_i)`
- exact normalized local one-plaquette sample values on the named seam
- exact clarification that the current atlas already supplies one real
  sample-side partial evaluation before the full environment solve

## What this does not close

- explicit `Z_6^env(W_A)`, `Z_6^env(W_B)`, `Z_6^env(W_C)`
- explicit full-slice rim lift `B_6(W)`
- explicit one-slab orthogonal kernel `K_6^env`
- explicit `rho_(p,q)(6)`
- the full plaquette PF closure
- the global sole-axiom PF selector theorem

## Why this matters

This is the strongest honest current exact result on the named three-sample
evaluation seam short of the full environment solve.

The branch no longer has to say only:

- the three named samples are still open.

It can now say:

- the exact local Wilson response at those three samples is already explicit,
- the sample-side half-slice and local one-plaquette factors are already known,
- and the remaining open step is specifically the nonlocal environment
  completion from `K_6^env / B_6(W)`.

## Command

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_first_three_sample_local_wilson_partial_evaluation_2026_04_17.py
```

Expected summary:

- `THEOREM PASS=6 SUPPORT=4 FAIL=0`
