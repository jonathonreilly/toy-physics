# PMNS Selector Sign-To-Branch Reduction

**Date:** 2026-04-15
**Status:** support - structural or confirmatory support note
branch-conditioned coefficient derivation
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_pmns_selector_sign_to_branch_reduction.py`

## Question

If a future microscopic bridge realizes the unique reduced PMNS selector with a
nonzero amplitude `a_sel`, what exactly happens to the remaining branch
ambiguity and the coefficient-derivation problem?

## Bottom line

The sign of `a_sel` fixes the branch, and only the branch-conditioned
coefficient problem remains.

Using the canonical reduced selector basis

`S_cls = chi_N_nu - chi_N_e`,

the exact reduced realization is

`B_red = a_sel S_cls`.

So:

- `a_sel > 0` selects the neutrino-side non-universal branch `N_nu`
- `a_sel < 0` selects the charged-lepton-side non-universal branch `N_e`
- `a_sel = 0` leaves the branch unresolved

After that sign choice, the remaining coefficient derivation is exactly the
already-known branch-conditioned problem:

- on `N_nu`: `7` real quantities
- on `N_e`: `3 + 7` real quantities

## Atlas and package inputs

This theorem reuses:

- `PMNS selector unique amplitude slot`
- `Full neutrino closure last-mile reduction`
- `Neutrino Dirac two-Higgs observable inverse problem`
- `Charged-lepton two-Higgs observable inverse problem`

## Why this matters

This note closes the handoff from selector science to coefficient science.

Once a microscopic realization with nonzero `a_sel` exists, there is no longer
any residual branch ambiguity to carry into the coefficient stage. The only
remaining work is the coefficient derivation on the selected branch.

## Theorem-level statement

**Theorem (Sign of the unique selector amplitude reduces full closure to the
branch-conditioned coefficient problem).** Assume the exact PMNS selector
unique-amplitude-slot theorem and the exact full-neutrino last-mile reduction
theorem. Then:

1. every reduced microscopic selector realization is `B_red = a_sel S_cls`
2. the sign of `a_sel` selects `N_nu` or `N_e`
3. after that sign selection, the remaining coefficient derivation is exactly
   the branch-conditioned finite-dimensional inverse problem already isolated by
   the current atlas

Therefore a nonzero selector realization converts the remaining neutrino gap
from “selector plus coefficients” to “coefficients on one selected branch.”

## What this closes

This closes the exact logic bridge from bridge-realization to coefficient
derivation.

It is now exact that the next positive step, if it happens, is not another
branch-selection theorem. It is branch-conditioned coefficient closure.

## What this does not close

This note does **not** derive:

- the microscopic bridge itself
- the sign or magnitude of `a_sel`
- the `7` neutrino-side quantities
- the `3 + 7` charged-lepton-side quantities

It is a reduction theorem only.

## Command

```bash
python3 scripts/frontier_pmns_selector_sign_to_branch_reduction.py
```
