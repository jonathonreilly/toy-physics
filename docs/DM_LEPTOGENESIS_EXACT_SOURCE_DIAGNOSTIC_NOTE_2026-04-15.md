# DM Leptogenesis Exact-Source Diagnostic

**Date:** 2026-04-15  
**Status:** exact-source diagnostic on the refreshed `main`-derived DM lane  
**Script:** `scripts/frontier_dm_leptogenesis_exact_source_diagnostic.py`

## Framework sentence

In this note, “axiom” means only the single framework axiom `Cl(3)` on `Z^3`.
Everything else is a derived atlas row.

## Question

After the refreshed branch fixes

- `c_odd = +1`
- `v_even = (sqrt(8/3), sqrt(8)/3)`
- `a_sel = 1/2`
- `tau_E = tau_T = 1/2`

what happens if that exact source package is inserted into the **same
normalized heavy-kernel convention already used by the current reduced
leptogenesis benchmark**?

Does the branch still underproduce because of weak source amplitudes?

## Bottom line

No.

Under that same normalized-kernel convention, the exact source package no
longer underproduces. It overshoots the Davidson-Ibarra ceiling by an `O(2)`
factor.

Using the exact source package gives

- `gamma = 1/2`
- `E1 = sqrt(8/3)`
- `E2 = sqrt(8)/3`

and therefore

- `cp1 = Im[(K_mass)01^2] = -2 gamma E1 / 3 = -0.544331...`
- `cp2 = Im[(K_mass)02^2] =  2 gamma E2 / 3 =  0.314270...`

When those are inserted into the same normalized-kernel convention already used
implicitly by the current reduced benchmark, the resulting source-side
diagnostic is

- `epsilon_signed / epsilon_DI = 2.10`
- `epsilon_abs / epsilon_DI = 2.16`

so both signed and absolute-sum reconstructions overshoot the DI ceiling.

Therefore the remaining benchmark gap is no longer “the exact source package is
too small.” It is the missing **diagonal normalization / thermal projection**
law from the exact heavy-basis tensor `K_mass` to the physical `epsilon_1`.

## Exact source package

The refreshed branch already closes:

- odd coefficient: `c_odd = +1`
- even coefficients: `v_even = (sqrt(8/3), sqrt(8)/3)`
- sharp selector amplitude: `a_sel = 1/2`
- sharp symmetric source amplitude: `tau_+ = tau_E + tau_T = 1`

So the exact triplet source data are

- `gamma = a_sel = 1/2`
- `E1 = sqrt(8/3) tau_+ = sqrt(8/3)`
- `E2 = (sqrt(8)/3) tau_+ = sqrt(8)/3`

and the exact heavy-basis CP tensor becomes

- `cp1 = -2 gamma E1 / 3`
- `cp2 =  2 gamma E2 / 3`.

## Same-convention diagnostic

The current reduced benchmark already treats the heavy-basis CP kernel in a
normalized way, effectively factoring out `y_0^2` from `(Y^dag Y)_{11}` and
retaining only the off-diagonal CP structure in the numerator.

On **that same convention**, the exact-source diagnostic uses

`epsilon_1 ~ (1/8pi) y_0^2 (cp1 f(x_23) + cp2 f(x_3))`

or, for the incoherent comparator,

`epsilon_1^abs ~ (1/8pi) y_0^2 (|cp1||f(x_23)| + |cp2||f(x_3)|)`.

Numerically this gives

- `epsilon_signed = 5.56e-6`
- `epsilon_abs = 5.71e-6`
- `epsilon_DI = 2.65e-6`

so both versions are above the DI ceiling.

## Consequence

This changes the harsh interpretation of the old `0.30` benchmark.

Before the exact-source closure, that benchmark looked like a source-side CP
deficit.

After the exact-source closure, that interpretation is no longer tenable on the
same normalized-kernel convention. The exact source package is already too
large, not too small.

So the remaining theorem target is sharper:

- derive the diagonal normalization `(Y^dag Y)_{11}` on the same exact source
  package
- or derive the exact thermal / projection map from the heavy-basis tensor
  `K_mass` to `epsilon_1`

Without that, the branch has exact source-side CP data but not yet an exact
`epsilon_1` law.

## What this closes

This closes one misleading reading of the old benchmark:

> the denominator still underproduces because the exact source package is too
> weak.

That is no longer the honest read.

## What this does not close

This note does **not** yet promote a new final `eta` value.

It is a diagnostic on the exact source package under the same normalized-kernel
convention already used by the current reduced benchmark. The exact diagonal
normalization / thermal projection law is still missing.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_exact_source_diagnostic.py
```
