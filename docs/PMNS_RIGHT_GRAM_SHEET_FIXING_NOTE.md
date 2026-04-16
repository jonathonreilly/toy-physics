# PMNS Right-Gram Sheet Fixing

**Date:** 2026-04-15  
**Status:** exact admitted-extension theorem on fixing the residual PMNS sheet  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_pmns_right_gram_sheet_fixing.py`

## Question

The retained bank now proves that after selector realization the selected
two-Higgs branch is explicit up to one residual `Z_2` sheet, and that the
current Hermitian branch bank cannot force that sheet.

If one admits a minimal right-sensitive datum, can the residual sheet be fixed
exactly?

## Bottom line

Yes, generically.

On the selected canonical two-Higgs branch, the retained Hermitian data `H`
determine two candidate roots `t_+, t_-` for `x_1^2`.

Now admit one right-sensitive scalar:

`s_12 = |(Y^dag Y)12|`.

Then

`s_12^2 = x_1^2 y_1^2 = x_1^2 (d_1 - x_1^2)`,

so on the two candidate roots the comparison function is

`f(t) = t (d_1 - t)`.

Generically:

- exactly one candidate root satisfies `f(t) = s_12^2`
- so one right-sensitive off-diagonal modulus fixes the residual sheet

The two-root degeneracy survives only on the nongeneric codimension-one locus

`t_+ + t_- = d_1`.

The same statement holds cyclically with `|(Y^dag Y)23|` or `|(Y^dag Y)31|`,
and likewise on the charged-lepton-side branch.

## Atlas and axiom inputs

This theorem reuses:

- `PMNS branch-conditioned quadratic-sheet closure`
- `PMNS branch sheet nonforcing`
- `Neutrino Dirac two-Higgs observable inverse problem`
- `Charged-lepton two-Higgs observable inverse problem`

## Why this is stronger than the sheet-nonforcing note

The sheet-nonforcing note proved the current Hermitian bank cannot fix the
sheet.

This note shows the minimal kind of admitted datum that **can** fix it:

- one right-sensitive off-diagonal modulus of `Y^dag Y`

So the post-selector sheet gap is no longer vague either.

## Theorem-level statement

**Theorem (One right-Gram off-diagonal modulus fixes the residual PMNS sheet
generically).** Assume the exact branch-conditioned quadratic-sheet closure on
a selected canonical two-Higgs branch, so the retained Hermitian data `H`
determine two candidate roots `t_+, t_-` for `x_1^2`. Let

`s_12 = |(Y^dag Y)12|`.

Then:

1. `s_12^2 = t (d_1 - t)` on the true sheet
2. the two candidate roots satisfy `f(t_+) = f(t_-)` iff `t_+ + t_- = d_1`
3. therefore off the codimension-one locus `t_+ + t_- = d_1`, exactly one
   candidate root matches the observed value of `s_12`

So one right-sensitive scalar modulus of `Y^dag Y` fixes the residual
`Z_2` sheet generically.

## What this closes

This closes the second positive extension route.

It is now exact that the residual sheet bit can be fixed by a minimal
right-sensitive datum, not by a full new matrix family.

## What this does not close

This note does **not** derive:

- the selector sign
- the right-sensitive scalar from the retained axiom bank
- a canonical right-handed frame that makes that scalar intrinsic on the
  retained bank
- the selected-branch Hermitian data

So this is again an admitted right-sensitive extension route, not retained
current-bank closure. See
[PMNS_RIGHT_FRAME_ORBIT_OBSTRUCTION_NOTE.md](./PMNS_RIGHT_FRAME_ORBIT_OBSTRUCTION_NOTE.md)
for the exact orbit-level reason that this route remains basis-conditional.

## Command

```bash
python3 scripts/frontier_pmns_right_gram_sheet_fixing.py
```
