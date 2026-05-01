# Universal QG Projective Schur Closure Note

**Date:** 2026-04-15  
**Role:** direct-universal quantum-gravity / refinement-projective theorem
**Status:** support - projective Schur coarse-graining closure

## Verdict

Yes. The exact discrete partition family is now closed under the right
finite-dimensional projective operation:

> Schur-complement marginalization over fine modes.

This is the correct algebraic coarse-graining theorem for the current
UV-finite direct-universal partition family.

So the remaining continuum/QG issue is no longer:

- whether the discrete densities are projectively compatible at all;
- whether integrating out fine modes destroys the GR stationary sector;
- whether repeated coarse-graining is associative.

Those are now exact.

The remaining issue was narrower:

> construct a canonical geometric refinement/coarsening net on the actual
> discrete spacetime atlas `PL S^3 x R`.

## Exact setup

On the positive-background class, the local universal gravity action is

`I_GR(F ; D, J) = 1/2 <F, K_GR(D) F> - <J, F>`

with

`K_GR(D) = H_D ⊗ Lambda_R`.

The UV-finite partition theorem already shows:

`Z_GR(K,J) = ∫ exp(-I_GR(F;D,J)) dF`

is finite and that its mean/stationary sector equals the discrete GR
stationary field.

## Projective coarse-graining theorem

Split the field variables into coarse and fine sectors:

`F = (F_c, F_f)`,

with block operator and source

`K = [[A, B], [B^T, C]]`,
`J = (eta, xi)`.

Because the positive-background route is symmetric positive definite,
`C` is invertible. Integrating out the fine field gives the exact coarse
effective action

`I_eff(F_c) = 1/2 <F_c, K_eff F_c> - <J_eff, F_c> + const`

with

`K_eff = A - B C^-1 B^T`,
`J_eff = eta - B C^-1 xi`.

So the coarse family is not merely approximate. It is exactly the same class of
finite Gaussian partition family again.

## Exact consequences

### 1. Partition closure

The partition factorizes exactly into the fine normalization factor and the
coarse effective partition:

`Z(K,J) = Z(C,xi) Z(K_eff, J_eff)`.

### 2. Stationary projection

The coarse stationary field is exactly the coarse block of the full stationary
field:

`F_c,* = K_eff^-1 J_eff`.

So integrating out fine modes preserves the GR stationary sector exactly.

### 3. Covariance projection

The coarse connected two-point function is exactly the coarse block of the full
covariance:

`K_eff^-1 = (K^-1)_{cc}`.

### 4. Associativity

If the field is split into coarse / medium / fine blocks, then integrating out
fine and then medium gives the same coarse theory as integrating out the
combined medium+fine sector in one step.

So the finite-dimensional projective law is associative.

## What this changes

Before this theorem, the remaining continuum bridge was described as a generic
projective-system theorem problem.

After this theorem, that is too weak. The algebraic projective closure is now
already available.

That geometric refinement-net step has now been discharged by the canonical
barycentric-dyadic refinement theorem. The remaining frontier is therefore one
level higher:

- interpret the resulting exact discrete projective family as an inverse-limit
  / continuum measure theorem;
- and show what continuum-equivalence statement is justified, if any.

## Honest status

This still does **not** prove a full continuum quantum-gravity theorem.

It does prove that the current direct-universal route is now exact at:

- discrete GR closure;
- UV-finite partition-density closure;
- Schur/projective coarse-graining closure.

So the remaining gap is not algebraic compatibility. And it is no longer the
construction of the geometric refinement net itself. It is the stronger
inverse-limit / continuum-interpretation theorem beyond that now-closed
discrete net.
