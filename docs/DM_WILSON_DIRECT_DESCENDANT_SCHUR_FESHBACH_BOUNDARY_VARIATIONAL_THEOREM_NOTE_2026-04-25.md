# DM Wilson Direct-Descendant Schur-Feshbach Boundary Variational Theorem

**Date:** 2026-04-25
**Status:** exact positive boundary theorem for the open DM direct-descendant
microscopic object `L_e = Schur_{E_e}(D_-)`; this proves the boundary-resolvent,
Feshbach-elimination, and positive Dirichlet variational character of `L_e`
once the charged microscopic block is supplied, but does not evaluate `D_-`,
does not select the final DM source point, and does not claim Wilson-native
parent closure
**Script:** none; proof-only note

## Question

The current DM Wilson direct-descendant stack has reduced the live flagship
frontier to a right-sensitive microscopic value law on

`L_e = Schur_{E_e}(D_-)`,

equivalently on the descended Hermitian law

`dW_e^H(X) = Re Tr(L_e^(-1) X)`.

Can `L_e` be characterized by an exact boundary principle, rather than only by
the block determinant identity already on `main`?

## Answer

Yes.

For a charged support split `E_- = E_e (+) E_r` and a block operator

`D_- = [[A, B], [C, F]]`,

with `F` and `L_e = A - B F^(-1) C` invertible, the Schur block satisfies the
exact boundary Green identity

`L_e^(-1) = I_e^* D_-^(-1) I_e`.

Thus the descended source law is not merely a formal determinant response. It
is exactly the compressed boundary resolvent of the charged microscopic
operator:

`dW_e^H(X)
 = Re Tr(I_e^* D_-^(-1) I_e X)`.

Moreover, if the charged microscopic block is Hermitian positive definite,
then `L_e` is the unique Dirichlet effective boundary operator:

`u^* L_e u
 = min_(v in E_r) [u; v]^* D_- [u; v]`,

where `u in E_e` and `v in E_r`, with the canonical eliminated interior field

`v_*(u) = -F^(-1) B^* u`.

This gives a positive, reviewable target for the open microscopic value law.
Any future Wilson-native derivation of `D_-` must reproduce the same boundary
resolvent, the same Feshbach-eliminated equation, and, in the positive
Hermitian case, the same Dirichlet minimum and monotonicity certificates.

The theorem moves the program forward without closing the DM lane: it proves
what `L_e` is as a boundary object once `D_-` is supplied, while leaving the
actual microscopic evaluation and right-sensitive selector law open.

## Setup

Work in the finite-dimensional charged block used by the current
direct-descendant local Schur reduction.

Let

`E_- = E_e (+) E_r`

be the charged support split, where `dim E_e = 3`. Let

`I_e : E_e -> E_-`

be the canonical support inclusion.

Write the charged microscopic operator in block form:

`D_- = [[A, B], [C, F]]`,

where

- `A : E_e -> E_e`,
- `B : E_r -> E_e`,
- `C : E_e -> E_r`,
- `F : E_r -> E_r`.

Assume first that `F` is invertible and define the Schur block

`L_e = A - B F^(-1) C`.

When inverse formulas are used, assume also that `L_e` is invertible. This is
equivalent to invertibility of `D_-` under the already-assumed invertibility of
`F`.

For the positive variational part, impose the additional hypothesis:

- `D_- = D_-^* > 0`.

Then `F = F^* > 0`, `C = B^*`, and the Schur block is Hermitian positive
definite.

This positivity hypothesis is intentionally explicit. The boundary-resolvent
and Feshbach-elimination identities are algebraic and do not require positivity;
the Dirichlet minimum principle does.

## Theorem 1: exact boundary resolvent compression

Assume `F` and `L_e` are invertible. Then

`D_-` is invertible and the `E_e`-to-`E_e` compression of `D_-^(-1)` is exactly

`I_e^* D_-^(-1) I_e = L_e^(-1)`.

Equivalently, the charged Schur block is the inverse of the boundary Green
operator:

`L_e = (I_e^* D_-^(-1) I_e)^(-1)`.

### Proof

Use the exact block factorization

`D_-
 = [[1, B F^(-1)], [0, 1]]
   [[L_e, 0], [0, F]]
   [[1, 0], [F^(-1) C, 1]]`.

Multiplying the three factors gives

`[[L_e + B F^(-1) F F^(-1) C, B F^(-1) F],
  [F F^(-1) C, F]]
 = [[A, B], [C, F]]`,

because `L_e + B F^(-1) C = A`.

All three factors are invertible, so `D_-` is invertible. Inverting the
factorization gives the standard block inverse

`D_-^(-1)
 = [[L_e^(-1), -L_e^(-1) B F^(-1)],
    [-F^(-1) C L_e^(-1),
     F^(-1) + F^(-1) C L_e^(-1) B F^(-1)]]`.

The upper-left block is exactly `L_e^(-1)`. Since `I_e^* D_-^(-1) I_e` is the
upper-left block in the split `E_e (+) E_r`, the displayed identity follows.

This proves the theorem. `QED`

## Corollary 1: exact Green-function form of the descended Hermitian law

For every Hermitian source `X in Herm(E_e)`,

`dW_e^H(X)
 = Re Tr(L_e^(-1) X)
 = Re Tr(I_e^* D_-^(-1) I_e X)`.

Thus the descended `3 x 3` Hermitian law is exactly the real part of the
boundary Green function of the charged microscopic block.

This is a stronger interpretation than the determinant identity alone: the
open microscopic law can be attacked either as a Schur complement value law or
as a boundary resolvent compression law. They are exactly equivalent.

## Theorem 2: exact Feshbach boundary equation

Assume `F` is invertible. For every boundary vector `u in E_e`, define the
eliminated interior vector

`v_*(u) = -F^(-1) C u`.

Then

`D_- [u; v_*(u)] = [L_e u; 0]`.

Consequently, solving the full charged microscopic equation with no residual
interior component is exactly equivalent to solving the boundary equation

`L_e u = boundary source`.

### Proof

Compute directly:

`D_- [u; v_*(u)]
 = [[A, B], [C, F]] [u; -F^(-1) C u]
 = [A u - B F^(-1) C u; C u - F F^(-1) C u]
 = [L_e u; 0]`.

This proves the theorem. `QED`

## Corollary 2: ambient completion uncertainty enters only through the eliminated boundary response

Any two charged microscopic completions with the same eliminated boundary map

`u -> L_e u`

produce the same full descended source law on `E_e`, even if their interior
spaces or interior coordinates differ.

Thus the live DM direct-descendant target is not an arbitrary ambient
completion. It is the boundary response of the charged microscopic equation.

## Theorem 3: positive Dirichlet variational principle for `L_e`

Assume now that

`D_- = D_-^* > 0`.

Then `F > 0`, `L_e > 0`, and for every `u in E_e`,

`u^* L_e u
 = min_(v in E_r) [u; v]^* D_- [u; v]`.

The unique minimizer is

`v_*(u) = -F^(-1) B^* u`.

### Proof

Since `D_- > 0`, every principal compression is positive definite, so
`F > 0`.

For fixed `u`, write the quadratic form as

`Q_u(v)
 = [u; v]^* D_- [u; v]
 = u^* A u + u^* B v + v^* B^* u + v^* F v`.

Complete the square:

`Q_u(v)
 = u^* (A - B F^(-1) B^*) u
   + (v + F^(-1) B^* u)^* F (v + F^(-1) B^* u)`.

Because `F > 0`, the second term is nonnegative and vanishes uniquely at

`v = -F^(-1) B^* u`.

Since `C = B^*` in the Hermitian case,

`A - B F^(-1) B^* = L_e`.

Therefore

`min_v Q_u(v) = u^* L_e u`,

with unique minimizer `v_*(u)`. Since the minimum is strictly positive for
`u != 0`, the Schur block satisfies `L_e > 0`.

This proves the theorem. `QED`

## Corollary 3: trial-interior upper certificates

Under the positive Hermitian hypothesis, any linear trial interior map

`R : E_e -> E_r`

defines a boundary quadratic form

`K_R(u) = [u; R u]^* D_- [u; R u]`.

Then

`u^* L_e u <= K_R(u)`

for all `u in E_e`, with equality for all `u` if and only if

`R = -F^(-1) B^*`.

Equivalently, every trial interior elimination gives a rigorous upper
certificate for the true Dirichlet boundary form, and the certificate is sharp
exactly at the Feshbach-eliminated interior field.

### Proof

Apply Theorem 3 with `v = R u`. The minimum over all `v` is no larger than the
value at the trial `v = R u`, giving `u^* L_e u <= K_R(u)`.

The equality condition for every `u` is exactly the unique minimizer condition
from Theorem 3:

`R u = -F^(-1) B^* u`

for every `u`, hence `R = -F^(-1) B^*`.

This proves the corollary. `QED`

## Theorem 4: monotonicity of the positive boundary law

Let `D_1` and `D_2` be two Hermitian positive charged microscopic blocks on the
same split `E_e (+) E_r`, with invertible interior blocks and Schur complements
`L_1` and `L_2`. If

`D_1 <= D_2`

in Loewner order, then

`L_1 <= L_2`.

### Proof

For every `u in E_e`, Theorem 3 gives

`u^* L_1 u = min_v [u; v]^* D_1 [u; v]`,

`u^* L_2 u = min_v [u; v]^* D_2 [u; v]`.

Since `D_1 <= D_2`, for every `v`,

`[u; v]^* D_1 [u; v] <= [u; v]^* D_2 [u; v]`.

Let `v_2` be the unique minimizer for the second quadratic form. Then

`min_v [u; v]^* D_1 [u; v]
 <= [u; v_2]^* D_1 [u; v_2]
 <= [u; v_2]^* D_2 [u; v_2]
 = min_v [u; v]^* D_2 [u; v]`.

Hence `u^* L_1 u <= u^* L_2 u` for every `u`, which is exactly
`L_1 <= L_2`.

This proves the theorem. `QED`

## Corollary 4: reviewable order certificates for microscopic approximants

If future Wilson-native approximants produce positive charged blocks satisfying

`D_low <= D_actual <= D_high`,

then their boundary laws satisfy

`L_low <= L_actual <= L_high`.

This supplies a clean certification route for a future constructive
calculation: order bounds on the microscopic charged block descend to order
bounds on the actual `L_e` law.

## Consequence for the DM direct-descendant frontier

The earlier local Schur source-family note proved the determinant-response
identity

`det(D + t J_Z) / det(D) = det(L_e + t Z) / det(L_e)`.

The present theorem adds a complementary boundary interpretation:

1. `L_e^(-1)` is exactly the boundary Green compression of `D_-^(-1)`.
2. `L_e` is exactly the Feshbach boundary operator obtained by eliminating
   `E_r`.
3. In the positive Hermitian case, `L_e` is exactly the Dirichlet minimum
   boundary form.
4. Positive microscopic bounds descend monotonically to positive boundary
   bounds.

So the open microscopic value law can now be framed in three equivalent ways:

- compute the charged Schur block `L_e`;
- compute the compressed boundary Green function `I_e^* D_-^(-1) I_e`;
- prove the positive Dirichlet boundary form induced by eliminating `E_r`.

This is real positive progress because it turns the missing `L_e` law into a
boundary-value theorem with exact algebraic and variational certificates.

## Reviewer-pressure checks

1. **No final DM selector is claimed.** The note does not select a point on the
   constructive transport fiber and does not close the DM flagship lane.

2. **No microscopic values are invented.** The theorem does not evaluate
   `D_-`, `L_e`, `H_e`, any transport column, or any dark-matter number.

3. **The positive variational assumption is explicit.** The resolvent and
   Feshbach identities require only invertibility of the relevant blocks. The
   Dirichlet minimum principle and monotonicity require `D_- = D_-^* > 0`.

4. **The theorem is local to the charged block.** It does not assert that the
   current Wilson parent stack has already supplied the correct `D_-` or
   support split.

5. **The result is falsifiable by boundary data.** A proposed microscopic
   derivation of `D_-` must pass the inverse-compression identity, the
   eliminated-interior equation, and, when positive Hermitian, the Dirichlet
   minimum and Loewner monotonicity laws.

## What this closes

- exact boundary Green-function characterization of
  `L_e = Schur_{E_e}(D_-)`
- exact Feshbach eliminated-interior equation for the charged support response
- exact positive Dirichlet minimum principle for `L_e` under the Hermitian
  positive microscopic hypothesis
- exact monotonicity of the positive boundary law under microscopic Loewner
  bounds
- an explicit certificate grammar for future Wilson-native approximants to
  `D_-`

## What this does not close

- actual evaluation of `D_-` from `Cl(3)` on `Z^3`
- Wilson-native proof of the intended charged support split
- the right-sensitive microscopic selector law on `L_e`
- the local `3`-real source fiber above the canonical favored transport column
- the final DM flagship lane
