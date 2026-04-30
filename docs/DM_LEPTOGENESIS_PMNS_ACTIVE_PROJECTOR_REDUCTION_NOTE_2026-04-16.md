# DM Leptogenesis PMNS Active-Projector Reduction

**Status:** bounded - bounded or caveated result note
**Date:** 2026-04-16  
**Branch:** `codex/dm-main-refresh`  
**Script:** `scripts/frontier_dm_leptogenesis_pmns_active_projector_reduction.py`  
**Framework convention:** "axiom" means only `Cl(3)` on `Z^3`

## Status

Exact reduction theorem plus transport-facing diagnostic transplant from the
active PMNS lane.

This note sharpens the flavored-transport target on the DM branch. It does
**not** yet derive the full PMNS active source law.

## Question

After importing the active PMNS / neutrino lane, do we still need the full
Hermitian pair `((H_nu,H_e),s)` to drive flavored DM transport?

Or does the one-sided PMNS structure already reduce the transport-facing object
further?

## Bottom line

Yes. The transport-facing PMNS object reduces further.

On the one-sided minimal PMNS classes:

- the passive monomial Hermitian sector is diagonal
- its left diagonalizer is therefore only phases and/or a basis permutation
- so the flavored transport projector packet is already determined by the
  **active Hermitian block alone**, up to passive column ordering

Therefore the DM flavored-transport target is no longer the full pair law.
It is the active PMNS law.

And after importing the new PMNS-side native laws for:

- branch/orientation
- weak-axis seed averages

the remaining DM-relevant PMNS object sharpens again to:

- the active five-real source

not the full pair.

## Exact active-projector localization

Let

- `H_act` be the active Hermitian block on a one-sided PMNS branch
- `H_pass` be the passive monomial Hermitian block

and let

`U_PMNS = U_pass^dag U_act`.

Because `H_pass` is diagonal on the passive monomial lane, `U_pass` is only a
phase matrix and/or a permutation matrix. Hence:

- on the neutrino-active branch `N_nu`:
  `|U_PMNS|^2 = |U_nu|^2`
- on the charged-lepton-active branch `N_e`:
  `|U_PMNS|^2 = |U_e|^2^T`

So the one-sided flavored transport packet is an active-block object.

## Canonical transport consequences

On the canonical `N_nu` active block, the active packet alone gives the
already-known lift

- `eta/eta_obs = 0.767519440713`

On the canonical `N_e` active block, the active packet alone gives the
near-closing lift

- `eta/eta_obs = 0.989512597197`

So the almost-complete repair of the exact one-flavor miss on the DM branch is
already carried by the active charged-lepton Hermitian block. The passive
monomial side is not what is doing the transport work.

## What the PMNS lane already fixes natively

The active PMNS lane now gives exact native laws for:

- the active/passive branch orientation bit
- the active weak-axis seed averages `(xbar,ybar)`

But those are still not enough to fix the transport packet completely.

Two active microscopic samples can share:

- the same branch/orientation status
- the same seed averages `(xbar,ybar)`

while carrying different active five-real source data

`(xi_1, xi_2, eta_1, eta_2, delta)`,

and those different source data induce:

- different active projector packets
- different flavored DM transport outputs

So the remaining DM-relevant PMNS object is exactly the active five-real
source.

## Consequence for the DM lane

This closes a real planning ambiguity.

We do **not** need:

- a new flavored transport ansatz
- a new ad hoc projector family
- the full PMNS pair law just to write flavored transport

We **do** need:

- a PMNS-side law for the active five-real source

or, more weakly,

- a theorem fixing the transport-relevant active column from that source

because once the active block is known, the one-sided transport packet is
automatic.

## What this closes

This closes the reduction question on the DM side.

The flavored transport packet is now reduced from:

- full pair law `((H_nu,H_e),s)`

to:

- active Hermitian block on the selected one-sided branch

and, after importing the new PMNS-side native selector/seed laws, further to:

- the active five-real source.

## What this does not close

This note does **not** derive:

- the active five-real source from `Cl(3)` on `Z^3`
- the final transport-relevant PMNS column as a theorem-grade axiom output

So the remaining PMNS contribution to DM flavored transport is still open.
But it is now much smaller and more explicit than the earlier full-pair target.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_pmns_active_projector_reduction.py
```
