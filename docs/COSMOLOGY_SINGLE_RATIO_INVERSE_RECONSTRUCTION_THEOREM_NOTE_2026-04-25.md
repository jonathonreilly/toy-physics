# Cosmology Single-Ratio Inverse Reconstruction Theorem

**Date:** 2026-04-25
**Status:** exact proposed_retained/admitted-surface structural-support theorem on
`main`. On the retained/admitted flat-FRW, `w_Lambda = -1` cosmology surface,
the single open late-time number `H_inf / H_0` is uniquely reconstructible
from several independent FRW observables and supplies exact consistency
certificates for future cosmology work. It does not derive the numerical value
of `H_inf / H_0`, does not promote `Omega_Lambda`, and does not close the
matter-content bridge.
**Primary runner:** `scripts/frontier_cosmology_single_ratio_inverse_reconstruction.py`

## Question

The current cosmology stack already proves the forward structural reduction:
on the retained/admitted flat-FRW surface with `w_Lambda = -1`, late-time
kinematic observables such as `q_0`, `z_*`, `z_mLambda`, `Omega_Lambda`, and
`H_inf` are functions of one open number,

`x := H_inf / H_0`.

Can that statement be strengthened in the positive direction?

More precisely, can the same surface be put under an inverse reconstruction
theorem, so that each observable gives a unique reconstruction of `x` and all
future calculations must satisfy exact cross-consistency identities?

## Answer

Yes.

On the same surface, set

`R := Omega_r,0`,

`L := Omega_Lambda,0 = x^2`,

`M := Omega_m,0 = 1 - L - R`.

Then the flat matter+radiation+Lambda Friedmann law is

`E(a)^2 := H(a)^2 / H_0^2 = R a^(-4) + M a^(-3) + L`.

The forward map from `L` to late-time kinematics is injective, and the inverse
maps are explicit:

```text
from H(a), a != 1:
L = [E(a)^2 - R a^(-4) - (1 - R) a^(-3)] / [1 - a^(-3)]

from q_0:
L = (1 + R - 2 q_0) / 3

from matter-Lambda equality:
L = s_mL^3 (1 - R) / (1 + s_mL^3),       s_mL := 1 + z_mLambda

from acceleration onset:
L = [a_* (1 - R) + 2 R] / [a_* + 2 a_*^4],       a_* := 1 / (1 + z_*)
```

Therefore the current open cosmology object is not several unrelated
late-time parameters. It is one scalar `L = (H_inf/H_0)^2`, overdetermined by
several independent observables. Any retained derivation or observational
comparison that supplies these observables must reconstruct the same `L`.

This moves the program forward without closing the cosmology lane: it proves
the exact inverse certificate grammar for the open ratio, while leaving the
ratio itself open.

## Setup

Assume the retained/admitted late-time cosmology surface used in the existing
FRW kinematic notes:

1. flat FRW;
2. pressureless matter, `w_m = 0`;
3. radiation, `w_r = 1/3`;
4. retained dark-energy EOS, `w_Lambda = -1`;
5. nonnegative present-day density fractions

   `R = Omega_r,0 >= 0`,

   `L = Omega_Lambda,0 >= 0`,

   `M = Omega_m,0 >= 0`,

   with `L + M + R = 1`;
6. the matter-bridge identity

   `L = Omega_Lambda,0 = (H_inf/H_0)^2`.

The previous forward theorem proves that `q_0`, `z_*`, `z_mLambda`, and
`H_inf` are functions of this same `L`. This note proves the inverse direction
and the resulting consistency certificates.

This is an inverse certificate on the existing FRW support surface, not a
promoted numerical cosmology closure.

It does not close the matter-content bridge.

## Theorem 1: one-point expansion-history reconstruction

For any scale factor `a > 0` with `a != 1`, the normalized expansion rate
`E(a) = H(a)/H_0` reconstructs `L` uniquely by

`L = [E(a)^2 - R a^(-4) - (1 - R) a^(-3)] / [1 - a^(-3)]`.

Moreover, if `M >= 0` and `R >= 0`, then

`E(a)^2 >= L`

for all `a > 0`, and

`E(a)^2 -> L`

as `a -> infinity`.

### Proof

The flat matter+radiation+Lambda Friedmann law is

`E(a)^2 = R a^(-4) + M a^(-3) + L`.

Use flatness to write

`M = 1 - L - R`.

Then

`E(a)^2
 = R a^(-4) + (1 - L - R) a^(-3) + L
 = R a^(-4) + (1 - R) a^(-3) + L (1 - a^(-3))`.

If `a != 1`, the coefficient `1 - a^(-3)` is nonzero, so solving for `L`
gives the displayed formula. Hence one non-present expansion-rate measurement
at a known `a` fixes `L` uniquely on this surface.

If `M >= 0` and `R >= 0`, then

`E(a)^2 - L = M a^(-3) + R a^(-4) >= 0`.

As `a -> infinity`, both `a^(-3)` and `a^(-4)` vanish, so `E(a)^2 -> L`.

This proves the theorem. `QED`

## Corollary 1: the asymptotic Hubble limit is the same inverse datum

The asymptotic de Sitter limit satisfies

`(H_inf / H_0)^2 = lim_(a -> infinity) E(a)^2 = L`.

So the retained matter-bridge ratio is equivalently the limiting expansion
floor of the late-time FRW solution.

## Theorem 2: deceleration-parameter inverse

The present-day deceleration parameter reconstructs `L` uniquely by

`L = (1 + R - 2 q_0) / 3`.

### Proof

On the flat matter+radiation+Lambda surface,

`q_0 = (1/2) (1 + R - 3 L)`.

This expression is affine in `L` with nonzero slope `-3/2`. Solving gives

`L = (1 + R - 2 q_0) / 3`.

This proves the theorem. `QED`

## Corollary 2: acceleration today is an exact bound on `L`

The universe is accelerating today exactly when `q_0 < 0`, hence exactly when

`L > (1 + R) / 3`.

This is a structural bound on the same open number. It does not fix the number,
but it turns present acceleration into a one-sided certificate for it.

## Theorem 3: matter-Lambda equality inverse

Let

`s_mL := 1 + z_mLambda = 1 / a_mL`

be the matter-Lambda equality redshift factor. If `R < 1` and `s_mL > 0`,
then equality reconstructs `L` uniquely by

`L = s_mL^3 (1 - R) / (1 + s_mL^3)`.

The map `s_mL -> L` is strictly increasing.

### Proof

Matter-Lambda equality is

`rho_m(a_mL) = rho_Lambda`.

Using the density scalings,

`M a_mL^(-3) = L`.

With `s_mL = a_mL^(-1)`, this is

`M s_mL^3 = L`.

Flatness gives `M = 1 - L - R`, so

`(1 - L - R) s_mL^3 = L`.

Solving,

`s_mL^3 (1 - R) = L (1 + s_mL^3)`,

and therefore

`L = s_mL^3 (1 - R) / (1 + s_mL^3)`.

For `R < 1`, differentiate with respect to `s_mL`:

`dL/ds_mL = 3 s_mL^2 (1 - R) / (1 + s_mL^3)^2 > 0`.

Thus the inverse is unique and strictly increasing.

This proves the theorem. `QED`

## Theorem 4: acceleration-onset inverse

Let `a_* = 1 / (1 + z_*)` be a positive scale factor at which
`q(a_*) = 0`. Then `L` is reconstructed uniquely by

`L = [a_* (1 - R) + 2 R] / [a_* + 2 a_*^4]`.

### Proof

The exact acceleration-onset equation from the forward FRW theorem is

`2 L a_*^4 - M a_* - 2 R = 0`.

Use `M = 1 - L - R`:

`2 L a_*^4 - (1 - L - R) a_* - 2 R = 0`.

Collect the `L` terms:

`L (2 a_*^4 + a_*) = a_* (1 - R) + 2 R`.

Since `a_* > 0`, the denominator `2 a_*^4 + a_*` is positive. Solving gives

`L = [a_* (1 - R) + 2 R] / [a_* + 2 a_*^4]`.

This proves the theorem. `QED`

## Corollary 3: acceleration onset and matter-Lambda equality are not independent parameters

If `R` is fixed, then `z_*` and `z_mLambda` reconstruct the same `L`.
Therefore their equality constraint is

`[a_* (1 - R) + 2 R] / [a_* + 2 a_*^4]
 = s_mL^3 (1 - R) / (1 + s_mL^3)`.

In the radiation-negligible limit `R -> 0`, this reduces to

`a_*^3 = 1 / (2 s_mL^3)`,

or

`1 + z_* = 2^(1/3) (1 + z_mLambda)`.

This recovers the forward theorem's gap relation as an inverse consistency
identity.

## Theorem 5: exact cross-consistency certificate for the single open number

Define the four reconstructed values

```text
L_H(a)   = [E(a)^2 - R a^(-4) - (1 - R) a^(-3)] / [1 - a^(-3)]
L_q      = (1 + R - 2 q_0) / 3
L_mL     = s_mL^3 (1 - R) / (1 + s_mL^3)
L_acc    = [a_* (1 - R) + 2 R] / [a_* + 2 a_*^4].
```

On the retained/admitted flat-FRW `w_Lambda = -1` surface, every defined
quantity must satisfy

`L_H(a) = L_q = L_mL = L_acc = (H_inf/H_0)^2`.

Conversely, if a candidate late-time data packet satisfies these equalities
for a common `L` in the physical interval

`0 <= L <= 1 - R`,

then the packet is exactly compatible with a flat matter+radiation+Lambda FRW
model with that single ratio.

### Proof

The forward surface equations imply all four inverse formulas by Theorems
1-4, so each reconstructed value equals the same `L`.

Conversely, suppose the reconstructed values agree at a common `L` with
`0 <= L <= 1 - R`. Define

`M = 1 - L - R >= 0`.

Then the Friedmann law

`E(a)^2 = R a^(-4) + M a^(-3) + L`

reproduces the supplied one-point expansion datum by the definition of
`L_H(a)`. The deceleration identity

`q_0 = (1/2)(1 + R - 3 L)`

reproduces the supplied `q_0` by the definition of `L_q`. The equality equation

`M s_mL^3 = L`

reproduces the supplied `z_mLambda` by the definition of `L_mL`. The
acceleration-onset equation

`2 L a_*^4 - M a_* - 2 R = 0`

reproduces the supplied `z_*` by the definition of `L_acc`.

Therefore the whole packet is compatible with the flat matter+radiation+Lambda
surface controlled by the single number `L = (H_inf/H_0)^2`.

This proves the theorem. `QED`

## What this adds beyond the forward kinematic reduction

The forward theorem says:

> once `H_inf/H_0` is supplied, late-time kinematic observables follow.

This inverse theorem says:

> each late-time kinematic observable reconstructs `H_inf/H_0`, and all
> reconstructions must agree.

That turns the current open ratio into an overdetermined target. A future
matter-content derivation, a numerical cosmology cascade, or an observational
comparison can be reviewed by checking whether every route gives the same
`L`.

## Reviewer-pressure checks

1. **No numerical cosmology closure is claimed.** The theorem does not predict
   a value for `H_inf/H_0`, `Omega_Lambda`, `Omega_m`, `q_0`, `z_*`, or
   `z_mLambda`.

2. **No hidden observational input is introduced.** The inverse formulas are
   identities on the same retained/admitted FRW surface already used by the
   forward notes.

3. **Radiation is retained exactly.** The formulas keep `R = Omega_r,0`. The
   common `R -> 0` approximations are stated only as limits.

4. **The theorem is falsifiable.** If independent data reconstruct different
   values of `L`, the flat `w_Lambda = -1` matter+radiation+Lambda surface is
   falsified or one of the supplied inputs is not on that surface.

5. **The open matter bridge stays open.** The theorem supplies certificates for
   the single ratio; it does not derive the ratio from DM relic physics,
   baryon density, or the cosmology-scale matching lane.

## What this closes

- exact inverse reconstruction of `H_inf/H_0` from one non-present expansion
  rate value `H(a)`
- exact inverse reconstruction from `q_0`
- exact inverse reconstruction from matter-Lambda equality redshift
- exact inverse reconstruction from acceleration-onset redshift
- exact cross-consistency certificate showing all these reconstructions must
  agree on one scalar `L = (H_inf/H_0)^2`

## What this does not close

- a first-principles value for `H_inf/H_0`
- a retained numerical value of `Omega_Lambda` or `Omega_m`
- the matter-content bridge behind the present-day cosmological pie chart
- a native derivation of `Omega_r,0`, `T_CMB`, recombination, or the sound
  horizon
- any promotion of the bounded numerical cosmology package

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [cosmology_frw_kinematic_reduction_theorem_note_2026-04-24](COSMOLOGY_FRW_KINEMATIC_REDUCTION_THEOREM_NOTE_2026-04-24.md)
- [omega_lambda_matter_bridge_theorem_note_2026-04-22](OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md)
- [dark_energy_eos_retained_corollary_theorem_note](DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md)
- [cosmological_constant_spectral_gap_identity_theorem_note](COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md)
