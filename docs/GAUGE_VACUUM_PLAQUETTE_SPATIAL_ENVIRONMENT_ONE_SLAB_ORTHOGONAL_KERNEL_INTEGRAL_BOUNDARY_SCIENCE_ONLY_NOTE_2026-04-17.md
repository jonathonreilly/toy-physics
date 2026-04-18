# Gauge-Vacuum Plaquette Spatial-Environment One-Slab Orthogonal-Kernel Integral Boundary

**Date:** 2026-04-17  
**Status:** exact integral-expression boundary theorem on the plaquette PF lane; the current Wilson spatial-environment transfer/factorization stack fixes one exact Haar-integral construction for the one-slab orthogonal kernel `K_beta^env` and one separate local rim integral for the boundary state `eta_beta(W)`, but it does **not** yet evaluate those objects in explicit closed form at `beta = 6`  
**Script:** `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_one_slab_orthogonal_kernel_integral_boundary_science_only_2026_04_17.py`

## Question

After the exact spatial-environment transfer theorem identifies one
orthogonal-slice kernel `K_beta^env` and one rim-induced boundary state
`eta_beta(W)`, what is the strongest honest theorem-grade statement now
supportable about the kernel itself?

## Answer

The strongest honest statement is an exact integral-expression boundary.

Choose the marked plaquette in the `(x,y)` plane and slice the unmarked spatial
environment along the orthogonal spatial direction `z`. For two adjacent
unmarked `z`-slices with gauge-invariant boundary data `U_k` and `U_(k+1)`,
let `Xi_k^bulk` denote the unmarked Wilson link variables strictly inside the
single slab between those slices.

Then the one-slab orthogonal kernel is exactly the Wilson/Haar integral

`K_beta^env(U_(k+1), U_k)
 = integral dmu_H(Xi_k^bulk)
     exp[(beta / 3) A_k^bulk(U_(k+1), U_k, Xi_k^bulk)]`,

where `A_k^bulk` is the real Wilson slab action built from the unmarked
plaquettes contained in that slab, with the standard half-weight convention on
plaquettes shared with neighboring slabs.

Separately, the marked-plaquette dependence does **not** belong to
`K_beta^env`. It enters through one local rim integral on the edge slab:

`B_beta(W; U_k)
 = integral dmu_H(Xi_k^rim)
     exp[(beta / 3) A_k^rim(U_k, Xi_k^rim; W)]`,

and after compression to the marked class-function sector this produces the
boundary state `eta_beta(W)`.

So the current exact stack fixes the right pre-compression construction class:

- one exact bulk one-slab Haar integral for `K_beta^env`,
- one exact local rim integral for `eta_beta(W)`.

What it does **not** yet supply is an explicit closed-form `beta = 6`
evaluation of either integral.

## Setup

From the exact spatial-environment transfer theorem already on `main`:

- integrating the Wilson weight between adjacent orthogonal slices defines one
  exact kernel `K_beta^env(U_(k+1), U_k)`,
- that kernel gives one positive self-adjoint transfer object
  `S_beta^env`,
- and the marked holonomy enters through one rim-induced boundary state
  `eta_beta(W)`.

From the exact local/environment factorization theorem:

- after trivial-channel normalization, the non-marked mixed-link factors are
  rep-independent scalars on the marked class-function sector,
- so the only nontrivial local marked input not already absorbed into the exact
  local four-link Wilson factor sits on the rim adjacent to the marked
  plaquette.

From the exact construction-boundary and kernel/rim-compression results already
present on the PF lane:

- the next constructive target is explicit `K_6^env` together with the local
  rim map producing `eta_6`,
- and once those pre-compression objects are explicit, the class-sector
  transfer data and downstream PF data follow canonically.

## Theorem 1: exact one-slab Haar-integral law for `K_beta^env`

Let `Sigma_k` and `Sigma_(k+1)` be adjacent orthogonal slices of the unmarked
spatial environment, and let `Xi_k^bulk` denote the internal unmarked Wilson
link variables in the slab between them.

Then the one-slab orthogonal kernel is exactly

`K_beta^env(U_(k+1), U_k)
 = integral_(Omega_k^bulk) dmu_H(Xi_k^bulk)
     exp[(beta / 3) A_k^bulk(U_(k+1), U_k, Xi_k^bulk)]`.

Because the Wilson weight is real and pointwise nonnegative, this kernel is
real and nonnegative. Because the slab action is invariant under reflection of
the orthogonal direction together with Haar inversion, the kernel is symmetric
in its boundary arguments:

`K_beta^env(U_(k+1), U_k) = K_beta^env(U_k, U_(k+1))`.

So the current exact stack does not merely assert existence of an abstract
positive kernel. It fixes the kernel as one specific Wilson/Haar slab
integral.

## Theorem 2: exact rim-local boundary integral for `eta_beta(W)`

Let `Xi_k^rim` denote the Wilson variables on the edge slab adjacent to the
marked plaquette, and let `W` be the marked plaquette holonomy.

Then the marked-plaquette boundary input is exactly one local rim integral

`B_beta(W; U_k)
 = integral_(Omega_k^rim) dmu_H(Xi_k^rim)
     exp[(beta / 3) A_k^rim(U_k, Xi_k^rim; W)]`.

Compressing this local rim object to the marked class-function sector gives
the exact boundary state `eta_beta(W)`.

After the exact local four-link factor has been isolated, the local/environment
factorization theorem implies that there is no additional non-rim
representation-dependent marked input hiding in the unmarked bulk slab.

Therefore:

- `K_beta^env` is the bulk one-slab integral,
- `eta_beta(W)` is produced by a separate rim-local integral,
- and the marked holonomy does not have to be inserted back into the bulk
  kernel by hand.

## Corollary 1: strongest honest PF boundary statement now supportable

The live plaquette PF target is therefore not an unspecified positive operator
and not a free closed-form coefficient sequence.

It is exactly the evaluation problem for two explicit pre-compression Wilson
integrals:

- the one-slab bulk kernel integral defining `K_6^env`,
- the local rim integral defining `eta_6`.

Once those are evaluated, the already-proved compression statements determine
`S_6^env`, `rho_(p,q)(6)`, and the downstream plaquette PF data canonically.

Until they are evaluated, explicit closed-form `beta = 6` PF data are not
derived and should not be claimed.

## What this closes

- exact identification of `K_beta^env` as one concrete Wilson/Haar one-slab
  integral rather than an abstract existence object
- exact separation between the bulk one-slab kernel and the local rim integral
  producing `eta_beta(W)`
- exact sharpening of the live PF seam to evaluation of explicit
  pre-compression integrals

## What this does not close

- an explicit closed-form formula for `K_6^env`
- an explicit closed-form formula for the rim integral producing `eta_6`
- explicit coefficients `rho_(p,q)(6)`
- explicit framework-point plaquette PF data
- analytic closure of canonical `P(6)`

## Command

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_spatial_environment_one_slab_orthogonal_kernel_integral_boundary_science_only_2026_04_17.py
```

Expected summary:

- `THEOREM PASS=5 SUPPORT=3 FAIL=0`
