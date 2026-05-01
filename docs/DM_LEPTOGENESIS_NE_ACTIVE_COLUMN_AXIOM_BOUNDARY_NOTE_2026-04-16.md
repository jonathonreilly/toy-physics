# DM Leptogenesis `N_e` Active-Column Axiom Boundary

**Status:** bounded - bounded or caveated result note
**Date:** 2026-04-16  
**Branch:** `codex/dm-main-refresh`  
**Script:** `scripts/frontier_dm_leptogenesis_ne_active_column_axiom_boundary.py`  
**Framework convention:** "axiom" means only `Cl(3)` on `Z^3`

## Status

Exact sole-axiom boundary theorem for the remaining PMNS-assisted flavored DM
transport gap on the refreshed branch.

This note answers the strongest remaining hope after the projector-interface,
active-block localization, and exact transport-selector theorems:

maybe the current native PMNS laws still fail to fix the full active
five-real source, but perhaps they at least force the selected transport column
on the charged-lepton-active branch `N_e`.

The answer is no.

## Question

On the PMNS-assisted DM lane, is the selected `N_e` active transport column
already determined by the currently native PMNS data coming from `Cl(3)` on
`Z^3`?

Equivalently: after importing

- one-sided active-block localization,
- the exact flavored transport selector,
- the active seed pair,
- the active branch/support data,

is there still any real ambiguity left in the transport-relevant `N_e` column?

## Bottom line

Yes, there is still real ambiguity.

There exist explicit charged-lepton-active microscopic samples that share the
same currently native PMNS data:

- the same seed pair `(xbar, ybar)`,
- the same fixed phase `delta`,
- the same one-sided active support count,
- the same active branch bit,

but carry different active five-real source data

`(xi_1, xi_2, eta_1, eta_2, delta)`,

and those different sources induce:

- different active projector packets,
- different exact transport functional values,
- and different selected active columns.

In fact the same current-native `N_e` data class can realize selected column
`0`, `1`, or `2`.

So the selected `N_e` transport column is **not** fixed by the currently native
PMNS laws from `Cl(3)` on `Z^3`.

## Exact selector already closed

The negative result is not coming from transport ambiguity.

The DM branch already has the exact one-source flavored selector

`F_K(P) = Σ_alpha Psi_K(P_alpha)`.

So once an active column `P` is supplied, the transport read is algorithmic.

The question here is strictly upstream: does the sole-axiom PMNS lane already
force the relevant active column on `N_e`?

This note proves it does not.

## Explicit counterexample family

The runner exhibits three explicit charged-lepton-active samples on the same
current-native class:

- same `xbar = 0.973333333333...`,
- same `ybar = 0.41`,
- same `delta = 0.2`,
- same support count `= 2`,
- same active branch bit `= 0`,

but different active five-real source data, yielding:

- sample A: selected column `0`,
- sample B: selected column `1`,
- sample C: selected column `2`.

So the transport-selected column is still sensitive to the active five-real
source.

## Consequence

This sharpens the sole-axiom DM/PMNS boundary one more step.

What is already exact:

- one-sided PMNS projectors localize to the active block,
- the flavored transport selector is exact,
- the canonical `N_e` near-closing middle-column sample is known,
- the seed pair and branch/support data are native.

What is still not fixed:

- the active five-real source,
- and therefore the selected `N_e` active column.

So the remaining PMNS-side DM object is not just a vague “PMNS value law.”
It is exactly the active five-real source law, or an equivalent theorem that
produces the selected active column from it.

## Honest endpoint

The honest sole-axiom endpoint on this lane is now:

- transport selector: closed
- active-block localization: closed
- selected `N_e` column: **not** closed from the current PMNS native laws

Therefore the refreshed DM branch does **not** yet gain full flavored transport
repair from the PMNS lane alone. It gains the correct carrier and selector, but
not the final PMNS-side value law.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_ne_active_column_axiom_boundary.py
```
