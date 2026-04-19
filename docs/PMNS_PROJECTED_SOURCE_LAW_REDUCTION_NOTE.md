# PMNS Projected Source-Law Reduction

**Date:** 2026-04-15  
**Status:** exact reduction theorem for the clean remaining derivation target
from `Cl(3)` on `Z^3`  
**Script:** `scripts/frontier_pmns_projected_source_law_reduction.py`

## Question

After the full lepton-pair reduction, what is the cleanest source-response
target that still has to be derived from `Cl(3)` on `Z^3` for full neutrino
closure?

## Bottom line

The clean remaining target is one projected lepton source law.

On the one-sided minimal PMNS classes, full neutrino closure is equivalent to
deriving:

1. the projected Hermitian linear source responses on the two effective lepton
   `3 x 3` blocks
2. one oriented non-Hermitian scalar probe on the active block

The first item reconstructs `(H_nu, H_e)` exactly.
The second item fixes the residual active two-Higgs sheet bit `s`.

So the clean target from `Cl(3)` on `Z^3` is not a raw family of PMNS
parameters and not even the piecewise bookkeeping objects
`U_full^nu`, `U_full^e`.

It is:

`(dW_nu^H, dW_e^H, ell_act)`.

## Exact reduction

### Hermitian part

For an effective `3 x 3` Hermitian block `H`, the Hermitian linear source
responses

`X -> Re Tr(X H)`

for the nine Hermitian basis directions determine `H` exactly.

So once the projected Hermitian linear source law is derived on the neutrino
and charged-lepton blocks, the full pair `(H_nu, H_e)` is determined exactly.

### Branch

Once `(H_nu, H_e)` is known on the one-sided minimal PMNS classes, the active
branch is readable directly:

- whichever Hermitian block is non-diagonal is the active two-Higgs branch
- the other is the passive monomial branch

So the branch is not a separate target once the pair law is derived.

### Residual sheet

After the active Hermitian block is known, the canonical active Yukawa matrix
is fixed up to one residual `Z_2` sheet.

That sheet can be fixed by one oriented non-Hermitian scalar probe on the
active block. A simple example is

`ell_11(Y) = Re(Y_11)`.

On the generic canonical branch the two sheets have different values of
`Re(Y_11)`, so one such probe fixes the sheet exactly.

## Theorem-level statement

**Theorem (Projected source-law reduction for full neutrino closure).**
Assume the exact observable principle from `Cl(3)` on `Z^3`, the exact full
lepton-pair reduction theorem, and the exact branch-conditioned quadratic-sheet
closure theorem. Then, on the one-sided minimal PMNS classes:

1. the projected Hermitian linear source responses on the two effective lepton
   `3 x 3` blocks reconstruct `(H_nu, H_e)` exactly
2. the active branch is readable directly from that pair
3. one oriented non-Hermitian scalar probe on the active canonical block fixes
   the residual sheet bit `s`

Therefore full neutrino closure reduces to deriving one projected lepton
source law

`(dW_nu^H, dW_e^H, ell_act)`

from `Cl(3)` on `Z^3`.

## What this closes

This closes the target-shape ambiguity again.

The remaining derivation target is now no longer best described as:

- branch selection
- PMNS bridge coordinates
- passive mass triples
- sheet selection

Those are downstream readable objects once the projected source law is known.

## What this does not close

This note does **not** derive the projected lepton source law itself from
`Cl(3)` on `Z^3`.

It identifies the cleanest exact form of the remaining derivation target.

## Command

```bash
python3 scripts/frontier_pmns_projected_source_law_reduction.py
```
