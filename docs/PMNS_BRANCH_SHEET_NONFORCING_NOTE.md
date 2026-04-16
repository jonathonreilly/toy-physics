# PMNS Branch Sheet Nonforcing

**Date:** 2026-04-15  
**Status:** exact post-selector boundary theorem on the residual `Z_2` sheet  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_pmns_branch_sheet_nonforcing.py`

## Question

After selector realization, the selected minimal two-Higgs branch is explicit
up to one residual `Z_2` coefficient sheet.

Can the current retained branch-observable bank fix that sheet bit?

## Bottom line

No.

The two coefficient sheets on a selected canonical two-Higgs branch are
distinct as Yukawa coefficients, but they produce the same Hermitian matrix
`H = Y Y^dag`.

Therefore every current observable that factors through `H` is sheet-even.
That includes the retained seven-coordinate observable grammar and all data
reconstructed from it.

So the current Hermitian branch bank does **not** force the residual sheet bit.
Fixing that bit requires a genuinely new non-Hermitian or right-sensitive
observable, not another `H`-based invariant.

## Atlas and axiom inputs

This theorem reuses:

- `PMNS branch-conditioned quadratic-sheet closure`
- `Neutrino Dirac two-Higgs observable inverse problem`
- `Charged-lepton two-Higgs observable inverse problem`

## Why this is stronger than the quadratic-sheet note

The quadratic-sheet note says the post-selector coefficient problem is explicit
up to one residual `Z_2` sheet.

This note goes one step further:

- it proves the current retained branch-observable bank cannot fix that sheet
  bit
- and it identifies the correct class of any future missing object

So the current post-selector endpoint is not just “there is one sheet bit.”
It is “that sheet bit is invisible to the present Hermitian bank.”

## Theorem-level statement

**Theorem (Current Hermitian branch bank cannot force the residual PMNS sheet
bit).** Assume the exact branch-conditioned quadratic-sheet closure theorem on
either selected canonical two-Higgs branch. Then:

1. the two residual coefficient sheets are distinct as canonical Yukawa data
2. they give the same Hermitian matrix `H = Y Y^dag`
3. any retained branch observable that factors through `H` is therefore
   sheet-even

So the current retained Hermitian branch bank cannot force the residual
`Z_2` sheet. Any future sheet-fixing datum must be genuinely non-Hermitian or
otherwise sensitive to information beyond `H`.

## What this closes

This closes the last easy loophole after selector realization.

It is now exact that the residual sheet bit is **not** secretly determined by:

- the current seven-coordinate observable grammar
- spectra extracted from `H`
- PMNS data reconstructed from `H`
- any other current retained branch observable that depends only on `H`

## What this does not close

This note does **not** derive:

- the selector sign
- the branch Hermitian data
- the residual sheet bit itself
- the new non-Hermitian observable that would fix it

## Command

```bash
python3 scripts/frontier_pmns_branch_sheet_nonforcing.py
```
