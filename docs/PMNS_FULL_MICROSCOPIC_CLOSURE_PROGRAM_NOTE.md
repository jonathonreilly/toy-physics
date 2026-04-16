# PMNS Full Microscopic Closure Program

**Date:** 2026-04-15  
**Status:** exact reduction / closure-stack collapse  
**Script:** `scripts/frontier_pmns_full_microscopic_closure_program.py`

## Question

Is the PMNS triplet pair

- `D_0^trip`
- `D_-^trip`

an extra unresolved object, or is it already the canonical charge-sector Schur
pair of the full microscopic `Cl(3)` on `Z^3` operator?

## Bottom line

It is not an extra object.

On the retained physical lepton surface,

- `D_0^trip = L_nu = Schur_{E_nu}(D_0)`
- `D_-^trip = L_e  = Schur_{E_e}(D_-)`

So once the full microscopic charge-preserving operator `D` is supplied, the
PMNS triplet pair is supplied automatically.

Then the existing triplet-pair closure program reads:

1. the realized one-sided branch
2. the passive monomial offset and coefficients
3. the active canonical two-Higgs coefficients
4. the residual sheet bit

## Exact stack

The exact chain is now:

`D`
`->` charge split `(D_0,D_-,D_+)`
`->` charge-sector Schur pair `(L_nu,L_e)`
`=` PMNS triplet pair `(D_0^trip,D_-^trip)`
`->` branch / coefficient / sheet data

So the former “derive the PMNS triplet pair” target collapses into the already
existing microscopic Schur localization.

## What this changes

Before this theorem, the remaining target was phrased as:

- derive the PMNS triplet pair from `Cl(3)` on `Z^3`

After this theorem, that is no longer a separate science object. The remaining
target is narrower:

- derive the actual full microscopic operator values of `D`
- or equivalently, evaluate the actual charge-sector Schur complements of `D`

## Boundary

This note does **not** claim that the actual full microscopic operator of the
theory has already been numerically evaluated from `Cl(3)` on `Z^3`.

It proves the narrower exact statement:

> the PMNS triplet pair is not an extra unresolved carrier beyond the full
> microscopic charge-preserving operator.

## Command

```bash
python3 scripts/frontier_pmns_full_microscopic_closure_program.py
```
