# Universal QG UV-Finite Partition Density Note

**Date:** 2026-04-15  
**Role:** direct-universal quantum-gravity / UV-finiteness step

## Verdict

Yes, the current mainline stack is now strong enough to go after the reviewer’s
suggested bridge:

> a finite partition structure whose semiclassical/stationary sector reproduces
> the project’s discrete `3+1` GR route.

That bridge is now exact on the project’s own discrete spacetime setting.

The direct-universal gravity route already defines an exact **UV-finite
finite-dimensional partition-density family** on `PL S^3 x R`, and its
mean/stationary sector is exactly the same discrete Einstein/Regge stationary
family already closed in the gravity capstone.

This is the strongest disciplined quantum-gravity-style statement currently
available from the mainline atlas.

## Exact local partition family

On the positive-background class, the direct-universal local action is

`I_GR(F ; D, J) = 1/2 <F, K_GR(D) F> - <J, F>`

with

`K_GR(D) = H_D ⊗ Lambda_R`.

The existing local GR closure theorem already proves:

- `K_GR(D)` is symmetric positive definite on the positive-background class;
- for every source `J`, there is a unique stationary field

  `F_* = K_GR(D)^-1 J`.

Therefore the exact local Euclidean partition exists and is finite:

`Z_GR(D,J) = ∫ exp(-I_GR(F;D,J)) dF`

`         = (2π)^(N/2) det(K_GR(D))^(-1/2)
            exp(1/2 <J, K_GR(D)^-1 J>)`.

Because the route is finite-dimensional on every finite chart, this is a
genuine discrete UV-finiteness statement: there is no ultraviolet divergence to
renormalize away on the project’s own discrete route.

## Why this is the right semiclassical GR bridge

The stationary/mean field of the partition is exactly

`∂ log Z_GR / ∂J = K_GR(D)^-1 J = F_*`.

So the partition family does not merely coexist with the GR action family. Its
mean/stationary sector is the same bridge field already identified in the
direct-universal GR theorem.

Likewise the connected two-point response is exactly

`∂^2 log Z_GR / ∂J^2 = K_GR(D)^-1`,

which is the inverse of the same universal GR operator controlling the local
quadratic theory.

This is precisely the public point:

> the discrete partition structure is finite, and its semiclassical/stationary
> sector reproduces the project’s own discrete `3+1` GR closure.

## Atlas / chart patching

The raw closed-form partition value is chart-dependent in the expected way:
under a chart change `F' = T F`,

`Z'_GR = |det T| Z_GR`.

That is not a defect. It is the exact Jacobian law of a coordinate density.

So the globally meaningful object is the **partition density / measure class**,
not the raw chart scalar. After compensating for the coordinate Jacobian, the
partition family patches exactly across the same finite atlas structure already
used in the discrete-global GR theorem.

## Relation to Lorentzian GR closure

The exact UV-finite partition statement is naturally Euclidean/positive
background because that is where the Gaussian integral is absolutely convergent.

But the current atlas already separately proves:

- exact Lorentzian signature-class stationary closure;
- exact finite-atlas global stationary patching;
- exact global Lorentzian Einstein/Regge stationary action family on
  `PL S^3 x R`.

So the partition theorem and the GR capstone fit together cleanly:

- **partition side:** exact finite partition-density family;
- **gravity side:** exact global Lorentzian stationary action family;
- **bridge:** the partition mean/stationary sector equals the GR stationary
  field.
- **coarse-graining side:** the family is also exactly closed under
  finite-dimensional Schur coarse-graining, so the remaining continuum issue is
  no longer algebraic projective compatibility

## Honest status

This is strong enough to support a disciplined statement of the form:

> the direct-universal route yields an exact UV-finite discrete partition family
> whose semiclassical/stationary sector reproduces the project’s exact discrete
> `3+1` Einstein/Regge gravity law on `PL S^3 x R`.

What this does **not** yet claim:

- a continuum sum-over-geometries theorem;
- a mature nonperturbative quantum-gravity program in the CDT/LQG sense;
- a continuum renormalizability theorem beyond the project’s discrete route.

So this is best read as an exact **discrete semiclassical quantum-gravity
closure step**, not yet the last word on continuum quantum gravity. The
canonical geometric refinement/coarsening theorem on the actual `PL S^3 x R`
atlas family has now also been discharged, so the remaining stronger bridge is
an inverse-limit / continuum-interpretation theorem for that exact discrete
projective family.
