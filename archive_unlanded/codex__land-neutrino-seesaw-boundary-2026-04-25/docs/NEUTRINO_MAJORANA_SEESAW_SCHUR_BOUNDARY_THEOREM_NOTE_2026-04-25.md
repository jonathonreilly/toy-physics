# Neutrino Majorana Seesaw Schur-Boundary Theorem

**Date:** 2026-04-25
**Status:** conditional exact Schur-boundary theorem for the Majorana / seesaw
branch of the retained neutrino support lane. This proves the
Feshbach-Schur light-neutrino operator, determinant factorization, inverse
Green compression, rank criteria, scale covariance, and singular-value
certificates once a Dirac block and a right-handed Majorana block are supplied.
It does not derive `Y_nu`, does not derive the Majorana amplitude `mu`, does not choose Dirac versus Majorana nature, and does not close the neutrino mass spectrum.
**Script:** `scripts/frontier_neutrino_majorana_seesaw_schur_boundary.py`

## Question

The current neutrino notes separate two facts:

1. the retained current stack sets the right-handed Majorana matrix to zero;
2. a Majorana / seesaw closure would require a new charge-`2` primitive,
   ultimately narrowed to one local real amplitude `mu` before the
   three-generation texture lift.

If such a Majorana block is supplied in the future, what is the exact theorem
that turns it into the light-neutrino mass operator?

Can the reduction be stated as a boundary theorem with reviewable algebraic and
norm certificates, rather than as a heuristic "seesaw formula"?

## Answer

Yes.

Let `D` be the supplied Dirac block and let `M_R` be the supplied right-handed
Majorana block. On the neutral quadratic space, write the symmetric block
operator

`K = [[0, D], [D^T, M_R]]`.

If `M_R` is invertible, eliminating the right-handed field gives the exact
light boundary operator

`M_light = - D M_R^(-1) D^T`.

This is not an approximation. It is the Schur complement of `M_R` in `K`.

Moreover:

- `det K = det(M_R) det(M_light)`;
- if `K` is invertible, the light-light block of `K^(-1)` is exactly
  `M_light^(-1)`;
- `rank(M_light) = rank(D M_R^(-1) D^T)`, so full light rank requires the
  Dirac map to have full light rank;
- under scale changes `D -> a D` and `M_R -> b M_R`, the light operator scales
  as `M_light -> (a^2 / b) M_light`;
- its singular values obey exact certificates

  `s_max(M_light) <= s_max(D)^2 / s_min(M_R)`,

  and, when `D` is invertible,

  `s_min(M_light) >= s_min(D)^2 / s_max(M_R)`.

Thus the open Majorana amplitude/texture law has an exact downstream target.
Once `D` and `M_R` are supplied, the light-neutrino Majorana operator is the
unique Schur boundary response. The theorem does not supply those inputs.

## Retained Context And Conditional Inputs

| Item | Main authority | Status in this theorem |
| --- | --- | --- |
| Current retained Majorana stack sets `M_R,current = 0` | [`NEUTRINO_MAJORANA_CURRENT_STACK_ZERO_LAW_NOTE.md`](NEUTRINO_MAJORANA_CURRENT_STACK_ZERO_LAW_NOTE.md) | retained current-stack boundary |
| Neutrino mass in general reduces to the Dirac lane unless a new charge-`2` primitive is supplied | [`NEUTRINO_MASS_REDUCTION_TO_DIRAC_NOTE.md`](NEUTRINO_MASS_REDUCTION_TO_DIRAC_NOTE.md) | retained reduction boundary |
| Majorana reopening requires a new charge-`2` primitive on the unique `nu_R` channel | [`NEUTRINO_MAJORANA_CHARGE_TWO_PRIMITIVE_REDUCTION_NOTE.md`](NEUTRINO_MAJORANA_CHARGE_TWO_PRIMITIVE_REDUCTION_NOTE.md) | exact frontier reduction |
| Supplied Dirac block `D` | not derived here | conditional input |
| Supplied invertible right-handed Majorana block `M_R` | not derived here | conditional input |

This note is therefore a downstream boundary theorem. It identifies the exact
map from future supplied inputs `(D, M_R)` to the light Majorana operator. It is
not a positive retained Majorana activation theorem.

## Setup

Work over finite-dimensional complex vector spaces:

- `L` is the three-generation left-handed neutral support;
- `R` is the three-generation right-handed neutral support;
- `D : R -> L` is the Dirac block after electroweak symmetry breaking;
- `M_R : R^* -> R` is the complex symmetric right-handed Majorana block.

Using column coordinates, the neutral quadratic form is represented by the
complex symmetric block matrix

`K = [[0, D], [D^T, M_R]]`

on `L (+) R`.

The transpose is the bilinear transpose appropriate to the Majorana quadratic
form. Physical positive masses are read later from Takagi singular values of
the resulting complex symmetric light operator; the algebra below does not
require choosing a real diagonal basis.

Throughout Theorems 1-4, assume only that `M_R` is invertible. For inverse
Green compression, assume additionally that the light Schur block is
invertible. For the singular-value certificates, use the standard operator
singular values of the finite matrices.

## Theorem 1: exact Feshbach-Schur elimination

Assume `M_R` is invertible. For every light vector `ell in L`, define the
eliminated right-handed field

`r_*(ell) = - M_R^(-1) D^T ell`.

Then

`K [ell; r_*(ell)] = [M_light ell; 0]`,

where

`M_light = - D M_R^(-1) D^T`.

### Proof

Compute directly:

`K [ell; r_*(ell)]
 = [[0, D], [D^T, M_R]] [ell; -M_R^(-1) D^T ell]`

`= [-D M_R^(-1) D^T ell;
    D^T ell - M_R M_R^(-1) D^T ell]`

`= [M_light ell; 0]`.

Thus the full neutral equation with no residual right-handed component reduces
exactly to the light boundary equation

`M_light ell = boundary source`.

This proves the theorem. `QED`

## Corollary 1: the seesaw formula is a boundary identity, not a fit

The usual type-I seesaw expression

`M_light = - D M_R^(-1) D^T`

is the exact Schur boundary operator of the supplied neutral quadratic block.
No perturbative expansion in `D / M_R` is needed for the algebraic reduction
itself. Hierarchy assumptions enter only when interpreting eigenvalue sizes or
when approximating the heavy-sector spectrum.

## Theorem 2: determinant factorization

If `M_R` is invertible, then

`det K = det(M_R) det(M_light)`.

### Proof

Use the block determinant formula for an invertible lower-right block:

`det [[A, B], [C, F]]
 = det(F) det(A - B F^(-1) C)`.

Here

`A = 0`, `B = D`, `C = D^T`, `F = M_R`.

Therefore

`det K
 = det(M_R) det(0 - D M_R^(-1) D^T)
 = det(M_R) det(M_light)`.

This proves the theorem. `QED`

## Corollary 2: massless light modes are exactly boundary Schur zero modes

Under `M_R` invertible, `K` is invertible if and only if `M_light` is
invertible.

Equivalently, any zero mode of the light Majorana boundary operator is a true
Schur zero mode of the full neutral quadratic form, not an artifact of the
elimination.

## Theorem 3: inverse Green compression

Assume `M_R` and `M_light` are invertible. Then the light-light block of
`K^(-1)` is exactly

`I_L^* K^(-1) I_L = M_light^(-1)`,

where `I_L : L -> L (+) R` is the light-support inclusion and `I_L^*` denotes
the coordinate projection onto the light block. No Hermitian positivity
assumption is being added here.

### Proof

For a block matrix with invertible lower-right block `F` and invertible Schur
complement `S = A - B F^(-1) C`, the inverse has upper-left block `S^(-1)`.

In the present case,

`S = 0 - D M_R^(-1) D^T = M_light`.

Therefore the upper-left block of `K^(-1)` is `M_light^(-1)`, which is exactly
the compression `I_L^* K^(-1) I_L`.

This proves the theorem. `QED`

## Corollary 3: the light response is the boundary Green function

Once the Majorana block is supplied and the light Schur block is invertible,
light-neutrino source responses are read from the compressed full neutral
Green function:

`M_light^(-1) = I_L^* K^(-1) I_L`.

Thus future Majorana closure can be certified either by the Schur formula or by
the boundary Green compression. They are the same theorem.

## Theorem 4: rank and kernel criteria

Assume `M_R` is invertible. Then

`rank(M_light) = rank(D M_R^(-1) D^T) <= rank(D)`.

In particular:

1. if `D` has a nonzero left-kernel vector `ell` with `D^T ell = 0`, then
   `M_light ell = 0`;
2. if `D` is square and invertible, then `M_light` is invertible;
3. full light Majorana rank requires the supplied Dirac block to have full
   light rank.

### Proof

The rank identity is the definition of `M_light` up to the harmless minus sign.
The inequality follows because multiplication by `D` on the left cannot
increase rank:

`rank(D M_R^(-1) D^T) <= rank(D)`.

If `D^T ell = 0`, then

`M_light ell = -D M_R^(-1) D^T ell = 0`.

If `D` is square and invertible, then `D^T` and `M_R^(-1)` are invertible, so
their product `D M_R^(-1) D^T` is invertible. Hence `M_light` is invertible.

This proves all three claims. `QED`

## Corollary 4: the Majorana primitive alone is not enough for full light rank

A nonzero right-handed Majorana amplitude `mu` supplies the heavy inverse
scale, but it does not by itself guarantee three nonzero light masses. Full
light rank still requires the Dirac block to couple all light directions into
the right-handed sector.

This is why the retained reduction to the Dirac lane and the Majorana
charge-`2` primitive lane are complementary rather than interchangeable.

## Theorem 5: exact scale covariance

For nonzero scalars `a` and `b`, replace

`D -> a D`,

`M_R -> b M_R`.

Then

`M_light -> (a^2 / b) M_light`.

### Proof

Substitute into the Schur formula:

`M_light(a,b)
 = - (a D) (b M_R)^(-1) (a D)^T`

`= - a D (b^(-1) M_R^(-1)) a D^T`

`= (a^2 / b) (- D M_R^(-1) D^T)`

`= (a^2 / b) M_light`.

This proves the theorem. `QED`

## Corollary 5: the one-real Majorana amplitude has inverse light-mass weight

On any texture class where the right-handed Majorana block is

`M_R = mu M_0`

with fixed invertible `M_0` and `mu > 0`, the light operator is

`M_light(mu) = mu^(-1) M_light(1)`.

So the retained Majorana amplitude `mu` is not just a source coefficient. It
is the inverse scale of the light Majorana boundary operator once the Dirac
block is fixed. Deriving `mu` therefore directly fixes the absolute light
Majorana mass scale on that supplied texture class.

## Theorem 6: singular-value certificates

Let `s_min(A)` and `s_max(A)` denote the smallest and largest singular values
of a finite matrix `A`. Assume `M_R` is invertible. Then

`s_max(M_light) <= s_max(D)^2 / s_min(M_R)`.

If `D` is square and invertible, then also

`s_min(M_light) >= s_min(D)^2 / s_max(M_R)`.

### Proof

Use the operator norm bound and `s_max(A) = ||A||`:

`s_max(M_light)
 = ||D M_R^(-1) D^T||
 <= ||D|| ||M_R^(-1)|| ||D^T||`.

Since `||D^T|| = ||D|| = s_max(D)` and
`||M_R^(-1)|| = 1 / s_min(M_R)`, the upper bound follows.

For the lower bound, assume `D` is invertible. For any unit vector `ell`,

`||D M_R^(-1) D^T ell||
 >= s_min(D) ||M_R^(-1) D^T ell||`

`>= s_min(D) s_min(M_R^(-1)) ||D^T ell||`

`>= s_min(D) s_min(M_R^(-1)) s_min(D^T) ||ell||`.

Because `s_min(D^T) = s_min(D)` and
`s_min(M_R^(-1)) = 1 / s_max(M_R)`, every unit vector satisfies

`||M_light ell|| >= s_min(D)^2 / s_max(M_R)`.

Taking the infimum over unit `ell` gives the lower singular-value bound.

This proves the theorem. `QED`

## Corollary 6: reviewable hierarchy bounds

If a future retained calculation supplies certified singular-value intervals
for `D` and `M_R`, then the light Majorana spectrum must lie inside the
corresponding Schur-boundary intervals above.

In the common hierarchical regime,

`s_max(D) << s_min(M_R)`,

the upper certificate gives the familiar suppression

`s_max(M_light) << s_max(D)`.

But the theorem is exact: the certificate does not rely on dropping terms in
the block matrix.

## Consequence for the retained neutrino frontier

The current retained neutrino notes already say:

- the Majorana current stack is zero;
- neutrino mass in general reduces to the Dirac lane unless a new
  charge-`2` Majorana primitive is supplied;
- if a Majorana / seesaw closure is sought, the remaining Majorana-side object
  is the real amplitude `mu` and its three-generation texture lift.

This note adds the positive downstream theorem:

1. once `D` and `M_R` are supplied, the light Majorana operator is fixed
   uniquely as the Schur boundary response;
2. the determinant and inverse Green identities give exact certification
   checks;
3. rank criteria separate the Dirac-texture problem from the Majorana-scale
   problem;
4. scale covariance shows exactly how the one-real amplitude `mu` controls the
   absolute light mass scale;
5. singular-value bounds give reviewable hierarchy certificates for future
   retained calculations.

So the remaining Majorana / seesaw lane is sharper:

> derive the nonzero charge-`2` primitive amplitude and its three-generation
> texture, and separately derive the Dirac texture; the exact light operator
> is then forced by Schur boundary reduction.

## Reviewer-pressure checks

1. **No Majorana activation is claimed.** The theorem assumes `M_R`; it does
   not derive the missing charge-`2` primitive or the amplitude `mu`.

2. **No Dirac texture is claimed.** The theorem assumes `D`; it does not derive
   `Y_nu` or the two-Higgs / PMNS last-mile quantities.

3. **No numerical mass prediction is claimed.** The theorem provides exact
   formulas and certificates only after the input blocks are supplied.

4. **The algebra is exact.** The Schur formula, determinant factorization, and
   inverse compression are finite-dimensional identities. The usual seesaw
   hierarchy is an interpretation of the singular-value bound, not an
   assumption needed for the reduction.

5. **Dirac and Majorana blockers remain distinct.** A nonzero `M_R` without a
   full-rank `D` can still leave massless light modes; a Dirac texture without
   a nonzero Majorana primitive gives Dirac, not Majorana, neutrino mass.

## What this closes

- exact Feshbach-Schur derivation of the light Majorana boundary operator
- exact determinant factorization for the neutral quadratic block
- exact inverse Green-function compression identity
- exact rank/kernel criteria for light Majorana masses
- exact scale covariance of the seesaw boundary operator
- exact singular-value hierarchy certificates for future supplied textures

## What this does not close

- nonzero generation of the charge-`2` Majorana primitive
- the value of the real Majorana amplitude `mu`
- the three-generation Majorana texture lift
- the Dirac Yukawa texture `Y_nu`
- solar gap, PMNS angles, Majorana phases, or absolute neutrino masses

## Command

```bash
python3 scripts/frontier_neutrino_majorana_seesaw_schur_boundary.py
```

Expected:

```text
TOTAL: PASS=48, FAIL=0
```
