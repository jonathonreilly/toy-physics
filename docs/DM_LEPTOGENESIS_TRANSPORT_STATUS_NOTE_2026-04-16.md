# DM Leptogenesis Transport Status

**Date:** 2026-04-16
**Authority runner:** `scripts/frontier_dm_leptogenesis_transport_status.py`
**Framework convention:** "axiom" means only `Cl(3)` on `Z^3`.

## Status

**EXACT TRANSPORT CHAIN CLOSED; DM GATE STILL OPEN**

The refreshed branch adds real exact transport-side results, but it does not
justify a live `full theorem closure` claim for the DM lane.

What is now exact on the current branch:

- exact source package
  - `gamma = 1/2`
  - `E1 = sqrt(8/3)`
  - `E2 = sqrt(8)/3`
- exact projection law
  - physical denominator `K00 = 2`
- exact equilibrium conversion factors
  - `d_N = 0.003901498367656259`
  - `s/n_gamma = 7.039433661546651`
- exact radiation expansion law
  - `H_rad(T) = sqrt(4*pi^3*g_*/45) * T^2 / M_Pl`
- exact normalized radiation transport branch
  - `E_H(z) = 1`
- exact direct transport solve on that branch

## Exact transport result

On the exact theorem-native radiation branch:

- `epsilon_1 / epsilon_DI = 0.9276209209197268`
- `kappa_axiom = 0.004829545290766509`
- `eta / eta_obs = 0.188785929502`

## PMNS-assisted support status

The refreshed PMNS package strengthens the lane materially:

- the admissible `N_e` PMNS-assisted closure problem is exactly reduced to the
  fixed native seed surface
- reduced-surface optimization support recovers a low-action branch with
  `eta / eta_obs = 1`

But that selector package is not yet promoted here as theorem-grade live
authority. The current reduced-surface optimization still uses previously known
branch anchors and local polishing, so it is carried as strong support rather
than a certified live theorem.

## Meaning

The old transport-side exact boundary on `H_rad(T)` is gone. The current live
end state is:

- exact source + transport chain on the one-flavor theorem-native branch
- exact theorem-native prediction undershoots observation by a factor
  `~ 5.297`
- PMNS-assisted reduced-surface repair is scientifically interesting and
  increasingly structured, but not yet promoted as a live closure theorem

So the DM flagship gate remains open.
