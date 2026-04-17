# DM Leptogenesis Flavor-Column Functional Theorem

**Date:** 2026-04-16  
**Branch:** `codex/dm-main-refresh`  
**Script:** `scripts/frontier_dm_leptogenesis_flavor_column_functional_theorem.py`  
**Framework convention:** "axiom" means only `Cl(3)` on `Z^3`

## Status

Exact transport-facing theorem for the flavored column-selection problem on the
refreshed DM branch.

This note does **not** derive the PMNS active five-real source itself. It
closes the weaker but still important question of how transport selects a PMNS
column once an active packet is supplied.

## Question

After reducing the DM flavored-transport target to the active PMNS block, do we
still need to scan transport numerically across columns to decide which PMNS
column matters?

Or is there an exact transport functional that selects the relevant column?

## Bottom line

Yes. There is an exact functional.

For one exact source on the refreshed DM branch, the flavored transport
equations decouple by flavor once the common heavy-state occupancy profile is
solved. The final flavored transport factor for a projector column

`P = (P_e, P_mu, P_tau)`

is exactly

`F_K(P) = Psi_K(P_e) + Psi_K(P_mu) + Psi_K(P_tau)`

where

`Psi_K(q) = q ∫ S_K(z) exp(-q W_K^tail(z)) dz`

and:

- `S_K(z) = -dN_1/dz` is the exact common source profile from the theorem-native
  one-source transport solve
- `W_K^tail(z) = ∫_z^∞ W_K(t) dt` is the exact common washout tail

So the one-source flavored PMNS column problem is not another ODE problem. It
is an exact scalar functional on the column entries.

## Exact reduction

For one source, the flavored transport equations are

`dY_alpha/dz = P_alpha S_K(z) - P_alpha W_K(z) Y_alpha`.

Because the common source profile `S_K` and common washout profile `W_K` are
already fixed by the exact one-source solve, each flavor channel is a scalar
integrating-factor problem.

Therefore:

`Y_alpha(∞) = Psi_K(P_alpha)`

and the full flavored transport factor is the sum over the three entries.

This is exact on the refreshed branch. It is not a fit.

## Exact current-branch channel preference

On the current exact branch, the one-channel kernel `Psi_K(q)` has a unique
interior maximum at a small nonzero leakage weight:

`q_star ≈ 0.035`.

That means the branch does **not** prefer:

- perfectly democratic `q = 1/3`, or
- an almost pure one-flavor `q ≈ 1`.

Instead it prefers a column with:

- one dominant flavor entry,
- plus small but nonzero leakage into the other flavors.

This is exactly the pattern already seen numerically in the canonical PMNS
charged-lepton-active sample.

## Canonical `N_e` active-column selection

On the canonical `N_e` active block, the active packet is

`[[0.915868, 0.074689, 0.009443],
  [0.071267, 0.900307, 0.028427],
  [0.012865, 0.025004, 0.962131]]`

after the one-sided `N_e` transpose rule is applied.

Evaluating the exact transport functional on its three columns:

- selects the middle column exactly
- reproduces the direct transport ordering exactly
- gives the same near-closing value

`eta/eta_obs = 0.989512597197`.

So the near-closing DM flavored-transport read is now pinned to one exact
active PMNS column on the canonical charged-lepton-active sample.

## Consequence

This sharpens the remaining open science again.

What is now closed:

- the PMNS-pair to projector interface
- the one-sided reduction to the active Hermitian block
- the exact flavored-column transport functional
- the canonical `N_e` active-column selection on the sample already used by the
  DM branch

What remains open:

- the PMNS-side value law for the active five-real source
- or an equivalent theorem producing the selected active transport column
  directly from `Cl(3)` on `Z^3`

So the remaining gap is no longer “which flavored column transport wants.” It
is “derive the PMNS active source / column that transport already knows how to
use.”

## What this closes

This closes the flavored-column selection problem on the DM side.

It is now exact that once an active PMNS packet is supplied, the transport
column is chosen by a scalar exact functional, not by another phenomenological
ansatz.

## What this does not close

This note does **not** derive the PMNS active packet itself from the sole
axiom `Cl(3)` on `Z^3`.

It also does **not** derive the active five-real source.

So it is a transport-facing reduction theorem, not a full PMNS value-law
closure theorem.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_flavor_column_functional_theorem.py
```
