# Lepton Shared-Higgs Universality Collapse

**Date:** 2026-04-15  
**Status:** exact extension-class theorem on the PMNS branch split under
shared-Higgs universality  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_lepton_shared_higgs_universality_collapse.py`

## Question

If the same effective Higgs-`Z_3` offset set contributes to both lepton Yukawa
sectors, can the current one-sided PMNS branch split

- neutrino-side only
- charged-lepton-side only

survive?

## Bottom line

No.

Under shared-Higgs universality:

- one active offset keeps **both** sectors monomial
- two active distinct offsets move **both** sectors onto the same two-Higgs
  support family and make both left Gram matrices non-diagonal when the active
  coefficients are nonzero

So the current one-sided branch split collapses.

The neutrino-side-only and charged-lepton-side-only minimal PMNS branches are
available only if shared-Higgs universality fails.

## Atlas and axiom inputs

This theorem reuses:

- `Lepton single-Higgs PMNS triviality theorem`
- `Neutrino Dirac two-Higgs escape theorem`
- `Charged-lepton two-Higgs canonical reduction`

## Why this matters

The current exact bank isolated two minimal PMNS-producing branches:

- a neutrino-side minimal branch
- a charged-lepton-side minimal branch

That split is real only if the lepton sectors are allowed to see different
effective Higgs-offset sets.

If a future theorem forces shared-Higgs universality, the split disappears:
both sectors either stay monomial together or leave the monomial lane together.

## Exact support logic

The single-offset support algebra is the same on both lepton Yukawa lanes.

So if the same offset set `S` is active in both sectors:

- `|S| = 1` gives the same permutation support class on both sides
- `|S| = 2` gives the same six-slot two-Higgs support union on both sides

There is no support-level route by which one sector stays monomial while the
other leaves the monomial class if the active offset set is shared.

## Theorem-level statement

**Theorem (Collapse of the one-sided PMNS branch split under shared-Higgs
universality).**
Assume:

1. the exact single-Higgs lepton-sector PMNS triviality theorem
2. the exact minimal two-Higgs neutrino escape theorem
3. the exact charged-lepton two-Higgs canonical reduction theorem
4. shared-Higgs universality in the precise sense that the same effective
   Higgs-offset set contributes to both lepton Yukawa sectors

Then:

1. one active offset keeps both lepton sectors on monomial lanes
2. two active distinct offsets move both lepton sectors onto the same
   two-Higgs support family
3. the neutrino-side-only and charged-lepton-side-only minimal PMNS branches
   are impossible under that universality hypothesis

Therefore the current one-sided minimal branch split requires failure of
shared-Higgs universality.

## What this closes

This closes an important selector-side ambiguity:

- a future shared-Higgs universality theorem would not select one side
- it would instead collapse the current sector-choice branch bit

## What this does not close

This note does **not** prove:

- that shared-Higgs universality is forced
- that shared-Higgs universality fails
- the remaining coefficient problem on the resulting shared support class

It is a conditional exact theorem only.

## Command

```bash
python3 scripts/frontier_lepton_shared_higgs_universality_collapse.py
```
