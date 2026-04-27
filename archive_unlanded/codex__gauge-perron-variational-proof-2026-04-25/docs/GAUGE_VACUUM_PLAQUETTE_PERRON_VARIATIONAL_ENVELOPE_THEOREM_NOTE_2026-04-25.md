# Gauge-Vacuum Plaquette Perron Variational Envelope Theorem

**Date:** 2026-04-25
**Status:** exact positive variational theorem for the already-reduced
gauge-vacuum plaquette Perron problem; this proves the uniqueness,
certification, and source-derivative envelope for the `beta = 6` tensor-transfer
Perron datum, but does not evaluate the still-open boundary coefficients
`rho_(p,q)(6)` or repin the canonical plaquette value
**Script:** none; proof-only note

## Question

The live gauge-vacuum stack has reduced the remaining framework-point
plaquette problem to explicit Perron / boundary data for

`T_6 = exp(3 J) D_6^loc C_(Z_6^env) exp(3 J)`,

where

- `J = (chi_(1,0) + chi_(0,1)) / 6` is the exact plaquette source operator,
- `D_6^loc chi_(p,q) = a_(p,q)(6)^4 chi_(p,q)` is the exact normalized local
  mixed-kernel factor,
- `C_(Z_6^env) chi_(p,q) = rho_(p,q)(6) chi_(p,q)` is the still-open normalized
  residual spatial-environment boundary character operator.

Can the remaining Perron datum be put under an exact positive variational
principle, so that any future explicit `rho_(p,q)(6)` or tensor-transfer solve
has a unique target and reviewable upper/lower certificates?

## Answer

Yes.

On every finite accepted Wilson source surface at `beta > 0`, the reduced
source-sector transfer operator is compact, self-adjoint, and
positivity-improving. Therefore its Perron eigenvalue is the unique maximizer of
an exact Rayleigh variational principle, and the corresponding strictly positive
Perron vector is the unique maximizing state.

On every finite positive character-tensor cutoff of the same source-sector
operator, the same Perron eigenvalue is also characterized by the exact
Collatz-Wielandt envelope

`max_(x > 0) min_i (T x)_i / x_i
 = r(T)
 = min_(x > 0) max_i (T x)_i / x_i`.

Finally, if the marked plaquette source is inserted symmetrically,

`T_6(s) = exp(s J / 2) T_6 exp(s J / 2)`,

then the first source derivative of the Perron pressure is exactly the Perron
expectation of the source operator:

`d/ds log lambda_0(T_6(s)) |_(s=0)
 = <psi_6, J psi_6>`.

Thus the open framework-point object is not merely an unconstrained positive
sequence. Once the residual boundary data are supplied, the exact plaquette
state is the unique positive maximizer of a variational problem, and its
plaquette expectation is the unique Hellmann-Feynman derivative of the Perron
pressure.

This theorem moves the program forward without closing the plaquette lane:
it gives a proof-level certification target for the explicit `beta = 6`
tensor-transfer Perron solve, while leaving the actual residual environment
coefficients open.

## Setup

Work on one finite accepted Wilson `3 spatial + 1 derived-time` source surface.
The previous gauge-vacuum notes establish the following exact objects.

1. The local source operator is the bounded self-adjoint class-function
   multiplication operator

   `J = (chi_(1,0) + chi_(0,1)) / 6`,

   with spectrum contained in `[-1/2, 1]`.

2. The framework-point source-sector transfer law has the exact factorized
   form

   `T_6 = exp(3 J) D_6^loc C_(Z_6^env) exp(3 J)`.

3. `D_6^loc` is the exact normalized four-link Wilson mixed-kernel factor,
   diagonal in the `SU(3)` dominant-weight character basis.

4. `C_(Z_6^env)` is normalized convolution by the unmarked spatial-environment
   boundary class function, equivalently

   `C_(Z_6^env) chi_(p,q) = rho_(p,q)(6) chi_(p,q)`.

5. The still-open constructive data are exactly the residual coefficients
   `rho_(p,q)(6)`, or equivalently the Perron data of the resulting positive
   tensor-transfer operator.

The theorem below assumes only the structural properties already established
for this finite Wilson source surface:

- `T_6` is compact and self-adjoint on the source Hilbert space,
- `T_6` is positivity-improving on the positive cone,
- `T_6` is nonzero.

The finite character-tensor cutoff statement additionally assumes a finite
matrix representation with strictly positive entries in the retained positive
basis. That is the natural setting for any explicit finite tensor-transfer
evaluation.

## Theorem 1: exact Rayleigh-Perron variational principle

Let `T` be a compact self-adjoint positivity-improving transfer operator on the
finite Wilson source Hilbert space, with positive cone inherited from
nonnegative class functions. Let `lambda_0 = r(T)` be its Perron eigenvalue and
let `psi_0 > 0` be the normalized Perron vector.

Then

`lambda_0 = sup_(||f|| = 1) <f, T f>`.

Moreover, equality holds if and only if `f` lies in the one-dimensional Perron
eigenspace. With the positivity normalization `<psi_0, 1> > 0`, the maximizing
state is unique and is exactly `psi_0`.

### Proof

By the compact self-adjoint spectral theorem, `T` has a real point spectrum
away from zero and an orthonormal eigenbasis on the closure of its range.

By the compact positivity-improving Perron-Jentzsch theorem, the spectral radius
`r(T)` is a simple positive eigenvalue with a strictly positive eigenvector
`psi_0`, and every other spectral value has modulus strictly smaller than
`r(T)`. Hence `lambda_0 = r(T)` is the largest spectral value of `T`.

For any unit vector `f`, expand `f` in a spectral resolution:

`f = c_0 psi_0 + f_perp`,

where `f_perp` is orthogonal to `psi_0`. Then

`<f, T f>
 = lambda_0 |c_0|^2 + <f_perp, T f_perp>`.

The spectrum of `T` on `psi_0^perp` is bounded above by some
`lambda_1 < lambda_0`, so

`<f, T f>
 <= lambda_0 |c_0|^2 + lambda_1 ||f_perp||^2
 <= lambda_0`.

Equality forces `||f_perp|| = 0`; hence `f` lies in the Perron eigenspace.
The Perron eigenspace is one-dimensional, and positivity fixes the sign.
Therefore the unique positive maximizer is `psi_0`.

This proves the theorem. `QED`

## Corollary 1: exact variational target for the `beta = 6` source-sector state

For the framework-point operator

`T_6 = exp(3 J) D_6^loc C_(Z_6^env) exp(3 J)`,

once the residual spatial-environment boundary operator `C_(Z_6^env)` is
specified, the exact source-sector Perron state is not a free choice. It is the
unique normalized positive maximizer of

`f -> <f, T_6 f>`

over unit source-sector states.

Thus any proposed explicit `rho_(p,q)(6)` sequence must produce one and only
one variationally certified Perron state.

## Theorem 2: exact finite cutoff Collatz-Wielandt certificate

Let `T` be any finite positive character-tensor cutoff of the reduced
source-sector operator, represented in a retained positive basis by a strictly
positive matrix. For every strictly positive vector `x`, define

`m_T(x) = min_i (T x)_i / x_i`,

`M_T(x) = max_i (T x)_i / x_i`.

Then

`max_(x > 0) m_T(x) = r(T) = min_(x > 0) M_T(x)`.

For any trial vector `x > 0`,

`m_T(x) <= r(T) <= M_T(x)`,

with equality on either side if and only if `x` is proportional to the Perron
vector.

### Proof

Because `T` is a strictly positive finite matrix, Perron-Frobenius theory gives
a simple spectral radius `r(T) > 0`, a right Perron vector `p > 0`, and a left
Perron vector `ell > 0`, normalized by `ell^T p = 1`.

Fix `x > 0`. By definition,

`m_T(x) x <= T x <= M_T(x) x`

componentwise.

Iterating the right inequality gives

`T^n x <= M_T(x)^n x`.

Pair with the strictly positive left Perron vector:

`r(T)^n ell^T x = ell^T T^n x <= M_T(x)^n ell^T x`.

Since `ell^T x > 0`, this implies `r(T) <= M_T(x)`.

The left inequality gives

`T^n x >= m_T(x)^n x`,

and pairing again with `ell` gives

`r(T)^n ell^T x >= m_T(x)^n ell^T x`,

so `m_T(x) <= r(T)`.

For the Perron vector `p`,

`(T p)_i / p_i = r(T)`

for every `i`, so `m_T(p) = M_T(p) = r(T)`. Hence

`max_(x > 0) m_T(x) = r(T) = min_(x > 0) M_T(x)`.

It remains to prove the equality condition. Suppose `M_T(x) = r(T)`. Then

`T x - r(T) x <= 0`.

Pairing with `ell > 0` gives

`ell^T (T x - r(T) x) = 0`.

A nonzero nonpositive vector has strictly negative pairing with `ell > 0`;
therefore `T x - r(T) x = 0`. Thus `x` is a right Perron vector. The
Perron eigenspace is one-dimensional, so `x` is proportional to `p`.

The case `m_T(x) = r(T)` is identical, using `T x - r(T) x >= 0`.

This proves the theorem. `QED`

## Corollary 2: reviewable two-sided envelopes for tensor-transfer solves

Every explicit finite `beta = 6` character-tensor evaluation now has a strict
certificate grammar:

1. choose a positive trial boundary vector `x`;
2. compute the component ratios `(T x)_i / x_i`;
3. report the interval

   `[m_T(x), M_T(x)]`.

That interval contains the exact cutoff Perron eigenvalue. It collapses to a
point exactly when the trial vector is the cutoff Perron vector.

This is useful because it separates two issues that were previously easy to
conflate:

- finite tensor-transfer arithmetic can be audited by Collatz-Wielandt
  envelopes;
- passing from cutoff data to the full `beta = 6` environment still requires a
  separate convergence theorem and is not claimed here.

## Theorem 3: exact Perron source-derivative formula

Let `T` be the exact compact self-adjoint positivity-improving source-sector
transfer operator on the finite Wilson source surface. Let `B` be any bounded
real source insertion whose exponential is positivity-preserving near
`s = 0`; in particular, `B` may be any bounded real multiplication operator
`f(J)`. Define a symmetric source insertion

`T(s) = exp(s B / 2) T exp(s B / 2)`.

Let `lambda(s)` be the Perron eigenvalue of `T(s)` and `psi(s)` the normalized
strictly positive Perron vector, chosen continuously near `s = 0`. Then
`lambda(s)` is differentiable at `s = 0`, and

`d/ds log lambda(s) |_(s=0) = <psi_0, B psi_0>`,

where `psi_0 = psi(0)`.

In particular, for `B = J`,

`d/ds log lambda_0(exp(s J / 2) T_6 exp(s J / 2)) |_(s=0)
 = <psi_6, J psi_6>`.

### Proof

Because `B` is bounded and self-adjoint, `exp(s B / 2)` is a bounded
self-adjoint analytic family in `s`. By the source-insertion hypothesis it is
also positivity-preserving for real `s` near zero, so `T(s)` remains in the
same positive simple-eigenvalue branch. Therefore

`T(s) = T + s T_dot + O(s^2)`

in operator norm, with

`T_dot = (B T + T B) / 2`.

The Perron eigenvalue of `T` is simple by positivity improvement. Standard
simple-eigenvalue perturbation theory for compact operators gives
differentiability of `lambda(s)` at zero and the Hellmann-Feynman formula

`lambda_dot(0) = <psi_0, T_dot psi_0>`,

with `||psi_0|| = 1`.

Since `T psi_0 = lambda(0) psi_0` and `T` is self-adjoint,

`<psi_0, T_dot psi_0>
 = (1/2) <psi_0, B T psi_0>
   + (1/2) <psi_0, T B psi_0>
 = (1/2) lambda(0) <psi_0, B psi_0>
   + (1/2) lambda(0) <psi_0, B psi_0>
 = lambda(0) <psi_0, B psi_0>`.

Dividing by `lambda(0)` gives

`d/ds log lambda(s) |_(s=0) = <psi_0, B psi_0>`.

Taking `B = J` gives the marked plaquette source formula.

This proves the theorem. `QED`

## Corollary 3: exact pressure derivative for the framework-point plaquette

For the `beta = 6` reduced source-sector operator, the large-derived-time
marked plaquette expectation is the Perron pressure derivative:

`P_src(6)
 = <psi_6, J psi_6>
 = d/ds log lambda_0(T_6(s)) |_(s=0)`,

with

`T_6(s) = exp(s J / 2) T_6 exp(s J / 2)`.

This is an exact identity on the finite accepted Wilson source surface. It does
not supply the still-open `rho_(p,q)(6)` coefficients, but once those
coefficients are supplied it fixes the plaquette readout uniquely.

## Why this is positive progress

The previous underdetermination result showed that the existing structural
stack does not force unique `beta = 6` Perron / Jacobi data before the residual
environment is specified.

This theorem adds the complementary positive result:

- after the residual environment is specified, the Perron datum is unique;
- its eigenvalue has exact two-sided positive-vector certificates on finite
  tensor cutoffs;
- its plaquette readout is the exact derivative of the Perron pressure under
  symmetric source insertion.

So the next constructive task is sharply reviewable:

> produce the exact residual boundary character data, or a convergent explicit
> tensor-transfer scheme for them, and certify the resulting Perron object by
> Rayleigh / Collatz-Wielandt / source-derivative identities.

## Reviewer-pressure checks

1. **No numeric plaquette closure is claimed.** The theorem does not assert a
   value for `P(6)`, `u_0`, any `rho_(p,q)(6)`, or any Jacobi coefficient.

2. **No hidden selector is introduced.** The variational maximizer is the
   Perron vector of the operator fixed by the residual environment. The theorem
   does not choose the residual environment.

3. **Finite cutoff certificates stay finite cutoff certificates.**
   Collatz-Wielandt intervals are exact for the finite positive cutoff operator
   being evaluated. A full `beta = 6` Wilson result still needs an explicit
   convergence theorem from cutoff transfer data to the full source-sector
   operator.

4. **The strict uniqueness assumption is visible.** Positivity improvement is
   essential. If a future variant only preserves positivity and is reducible,
   the theorem applies on each primitive block, and global uniqueness can fail.
   The accepted finite Wilson `beta > 0` transfer surface is in the
   positivity-improving case.

5. **The source derivative is an identity, not a fit.** It follows from
   symmetric source insertion and the simplicity of the Perron eigenvalue; no
   perturbative expansion, constant lift, or empirical matching enters.

## What this closes

- exact Rayleigh variational characterization of the reduced gauge-vacuum
  plaquette Perron state after the residual environment is supplied
- exact Collatz-Wielandt upper/lower certification envelope for finite positive
  character-tensor transfer solves
- exact Hellmann-Feynman source-derivative identity for the marked plaquette
  readout
- exact review grammar for future explicit `beta = 6` tensor-transfer Perron
  data

## What this does not close

- explicit evaluation of `rho_(p,q)(6)`
- explicit construction of the full `beta = 6` Perron vector
- explicit Jacobi coefficients or Perron moments beyond the variational
  identities above
- a cutoff-to-full-source-sector convergence theorem
- infinite-volume control in `L_s`
- analytic closure or repo-wide repinning of the canonical plaquette value
