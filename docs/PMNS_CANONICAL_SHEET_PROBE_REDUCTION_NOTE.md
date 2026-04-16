# PMNS Canonical Sheet-Probe Reduction

**Date:** 2026-04-15  
**Status:** exact reduction theorem on the residual selected-branch sheet datum  
**Script:** `scripts/frontier_pmns_canonical_sheet_probe_reduction.py`

## Question

After the quadratic-sheet theorem, full closure was reduced to deriving:

- the effective lepton operators / Hermitian pair
- plus one active non-Hermitian probe direction

Is that probe direction really an additional independent object?

Or is it already determined once the active Hermitian data are known?

## Bottom line

It is already determined once the active Hermitian data are known.

On a selected canonical two-Higgs branch, the active Hermitian matrix `H`
determines the unordered residual sheet pair

`{Y_0(H), Y_1(H)}`.

From that pair one gets an exact canonical centered sheet-odd probe:

- `Delta(H) = Y_1(H) - Y_0(H)`
- `Y_bar(H) = (Y_0(H) + Y_1(H)) / 2`
- `ell_H(Y) = Re Tr(Delta(H)^dag (Y - Y_bar(H)))`

Then

- `ell_H(Y_0(H)) = - ||Delta(H)||_F^2 / 2`
- `ell_H(Y_1(H)) = + ||Delta(H)||_F^2 / 2`

So once `H` is derived, the residual sheet bit does **not** require an
independently derived probe direction. The needed probe is already a canonical
downstream construction from `H`.

## Exact reduction

### 1. `H` determines the unordered sheet pair

The branch-conditioned quadratic-sheet theorem already shows that, generically,
the selected canonical branch has exactly two positive coefficient sheets with
the same Hermitian data.

So the sheet ambiguity is not a free family. It is the unordered pair
`{Y_0(H),Y_1(H)}` determined by `H`.

### 2. The centered difference is a canonical sheet-odd probe

The two sheets are distinct, so

`Delta(H) = Y_1(H) - Y_0(H) != 0`.

Using the centered functional

`ell_H(Y) = Re Tr(Delta(H)^dag (Y - Y_bar(H)))`

with

`Y_bar(H) = (Y_0(H) + Y_1(H))/2`,

one gets exact opposite values on the two sheets. This is the cleanest
possible sheet-reading probe on the active block.

### 3. Changing the sheet order changes only the bit convention

If one swaps the ordered pair `(Y_0,Y_1)`, then `Delta -> -Delta` and
`ell_H -> -ell_H`.

So the only remaining freedom is the naming convention for the `Z_2` bit.
There is no second independent probe object hiding here.

## Theorem-level statement

**Theorem (Canonical sheet-probe reduction).** Assume the exact
branch-conditioned quadratic-sheet closure theorem on a selected canonical
two-Higgs PMNS branch. Then:

1. the active Hermitian matrix `H` determines the unordered residual sheet pair
   `{Y_0(H),Y_1(H)}`
2. that pair determines the canonical centered sheet-odd probe
   `ell_H(Y) = Re Tr(Delta(H)^dag (Y - Y_bar(H)))`
3. the only remaining freedom is the `Z_2` bit convention coming from the
   order of the two sheets

Therefore the residual sheet datum does not require an independently derived
probe direction beyond the active Hermitian data.

## What this closes

This closes the “extra probe-direction” loophole.

The remaining independent full-closing target is no longer:

- effective lepton operators
- plus an extra active probe direction

It is just:

- effective lepton operators / Hermitian data

because the required sheet-reading probe is a canonical downstream
construction from the active `H`.

## What this does not close

This note does **not** derive the effective lepton operators themselves from
`Cl(3)` on `Z^3`.

It only removes the last independent probe-direction object from the closure
target.

## Command

```bash
python3 scripts/frontier_pmns_canonical_sheet_probe_reduction.py
```
