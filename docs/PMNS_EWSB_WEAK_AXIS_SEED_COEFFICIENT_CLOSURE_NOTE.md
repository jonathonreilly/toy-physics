# PMNS EWSB Weak-Axis Seed Coefficient Closure

**Date:** 2026-04-15  
**Status:** exact bridge-conditioned coefficient-closure theorem on the
compatible weak-axis seed patch  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_pmns_ewsb_weak_axis_seed_coefficient_closure.py`

## Question

The weak-axis seed theorem already proves that the exact `1+2` split

`diag(A,B,B)`

lifts to the Hermitian seed

`H_seed = mu I + nu(C+C^2)`

and that on the canonical active Yukawa chart this seed is realized iff

`A <= 4 B`.

But if the seed is compatible, do we then get full coefficient closure on that
patch, or is there still a generic post-Hermitian reconstruction problem?

## Bottom line

On the compatible weak-axis seed patch, the coefficient problem is explicit and
collapses to one exact exchange sheet.

Let

- `mu = (A + 2 B) / 3`
- `nu = (A - B) / 3`
- `Delta = mu^2 - 4 nu^2 = A(4B-A)/3`

with `A >= B >= 0` and `A <= 4 B`.

Then the canonical active coefficients are exactly

- `x_+^2 = (mu + sqrt(Delta)) / 2`
- `y_+^2 = (mu - sqrt(Delta)) / 2`
- `x_+ y_+ = nu`

and on the standard positive gauge patch `x_+ >= y_+ >= 0` the two exact
canonical sheets are

- `Y_+ = x_+ I + y_+ C`
- `Y_- = y_+ I + x_+ C`

Both satisfy

- `Y_+ Y_+^dag = Y_- Y_-^dag = H_seed`
- `Y_+^dag Y_+ = Y_-^dag Y_- = H_seed`

So on this seed patch:

- coefficient closure is explicit
- the residual sheet is exactly the exchange `x <-> y`
- even the admitted right-Gram route collapses, because `K = Y^dag Y` is the
  same on both sheets

The remaining full-closure object on this patch is therefore not a generic
coefficient fit and not a right-Gram datum. It is one genuinely `Y`-level
sheet-selection law.

## Atlas and axiom inputs

This theorem reuses:

- `PMNS EWSB weak-axis Z3 seed`
- `PMNS branch-conditioned quadratic-sheet closure`
- `PMNS branch sheet nonforcing`
- `PMNS right-Gram sheet fixing`

The new point is that on the weak-axis seed patch the generic quadratic-sheet
closure collapses further than before.

## Exact coefficient formulas on the seed patch

On the compatible seed patch the weak-axis theorem already forces any exact
canonical active realization to the symmetric chart

`Y = x I + y C`

with

- `x^2 + y^2 = mu`
- `x y = nu`.

So `t = x^2` obeys

`t^2 - mu t + nu^2 = 0`,

with exact roots

- `t_+ = (mu + sqrt(Delta)) / 2`
- `t_- = (mu - sqrt(Delta)) / 2`.

Therefore the two canonical sheets are exactly

- `x = sqrt(t_+)`, `y = sqrt(t_-)`
- or the exchanged sheet `x <-> y`.

There is no higher-dimensional residual family.

## The residual sheet is exactly the exchange `x <-> y`

On the generic compatible patch `B < A < 4 B`, one has

- `nu > 0`
- `Delta > 0`
- `x_+ > y_+ > 0`

so the two sheets

- `Y_+ = x_+ I + y_+ C`
- `Y_- = y_+ I + x_+ C`

are distinct canonical Yukawa data.

At the endpoints:

- `A = B` gives the monomial edge
  `Y_+ = sqrt(A) I`, `Y_- = sqrt(A) C`
- `A = 4 B` gives the merged-sheet edge
  `Y_+ = Y_-`

So the residual ambiguity on the seed patch is fully explicit.

## Right-Gram collapse on the seed patch

For real `x,y`,

`Y = x I + y C`

is normal, since it is a polynomial in the unitary cycle `C`. Therefore

`Y Y^dag = Y^dag Y = (x^2 + y^2) I + x y (C+C^2)`.

So on either seed sheet,

`K = Y^dag Y = H_seed`.

This is stronger than the generic branch-sheet nonforcing theorem:

- generically `H` fails to fix the residual sheet but an admitted right-Gram
  datum can fix it
- on the weak-axis seed patch, even `K` collapses to the same matrix on both
  sheets

So the weak-axis seed patch needs a genuinely `Y`-level selector, not merely a
right-Gram one.

## Theorem-level statement

**Theorem (Exact coefficient closure on the compatible weak-axis PMNS seed
patch).** Assume the exact weak-axis `1+2` Hermitian seed theorem, together
with the compatible-patch condition `A <= 4 B`. Then:

1. the canonical active coefficients reconstruct explicitly as
   `Y_+ = x_+ I + y_+ C` and `Y_- = y_+ I + x_+ C`, with
   `x_+^2 = (mu + sqrt(Delta))/2`, `y_+^2 = (mu - sqrt(Delta))/2`
2. on the generic compatible patch `B < A < 4 B`, these are the two distinct
   residual canonical sheets and they differ exactly by `x <-> y`
3. both sheets have the same Hermitian matrix `H_seed`
4. both sheets also have the same right Gram matrix `K = H_seed`

Therefore full coefficient closure on the weak-axis seed patch is exact up to
one explicit exchange sheet, and even right-Gram data do not fix that sheet.

## What this closes

This closes the coefficient problem on the compatible weak-axis seed patch as
far as the current bank honestly allows.

It is now exact that, on this patch, the remaining object is not:

- a generic seven-parameter coefficient fit
- a generic quadratic-sheet reconstruction problem
- a right-Gram sheet-fixing problem

It is one exact exchange-sheet selector.

## What this does not close

This note does **not** derive:

- that the PMNS-producing branch stays on the weak-axis seed patch
- the two aligned deformation directions away from that seed
- the three generic breaking slots away from the aligned surface
- the `Y`-level sheet selector that chooses between `Y_+` and `Y_-`

So this note gives full coefficient closure only on the explicit compatible
seed patch, not global full neutrino closure.

## Command

```bash
python3 scripts/frontier_pmns_ewsb_weak_axis_seed_coefficient_closure.py
```
