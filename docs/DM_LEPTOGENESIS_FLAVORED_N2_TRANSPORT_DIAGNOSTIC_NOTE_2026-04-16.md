# DM Leptogenesis Flavored / N2-Aware Transport Diagnostic

**Date:** 2026-04-16  
**Branch:** `codex/dm-main-refresh`  
**Script:** `scripts/frontier_dm_leptogenesis_flavored_n2_transport_diagnostic.py`  
**Framework convention:** "axiom" means only `Cl(3)` on `Z^3`

## Status

Diagnostic extension lane beyond the current exact one-flavor authority path.

The exact authority path on this branch is still:

- exact source package
- exact transfer coefficients
- exact projection law `physical denominator = K00 = 2`
- exact radiation transport law
- exact one-flavor transport result `eta / eta_obs = 0.188785929502`

This note asks what the most plausible **transport-side** repair routes look
like once the old numerator/denominator inconsistency is removed.

## Question

Can the remaining `~5.30x` denominator miss plausibly be repaired by:

1. flavored `N1` transport, or
2. a protected sequential `N2` source?

## Bottom line

Yes, flavor structure is a plausible repair path. The first new transport lane
worth deriving is **flavored projector structure**, not a brand-new `N2`
source.

The main diagnostics are:

- exact one-flavor authority:
  - `eta / eta_obs = 0.188785929502`
- two-flavor equal aligned splitting:
  - `eta / eta_obs = 0.425764574711`
- three-flavor equal aligned splitting:
  - `eta / eta_obs = 0.693223839689`
- on the hierarchical aligned branch
  - `P = (p, p, 1 - 2p)`
  observation is already reached at
  - `p ~= 0.022895`

So the exact miss can be erased by flavored `N1` transport alone if the
physical projectors are sufficiently non-democratic.

By contrast, in an optimistic protected two-source diagnostic with:

- `N1` sourcing/washing one flavor,
- `N2` sourcing a protected orthogonal flavor,
- diagnostic `K2 = K1 * M1 / M2`,

the branch would need

- `epsilon_2 ~= 3.86644 epsilon_1`

to reach observation.

So `N2`-aware transport can help, but it is **more expensive** than flavored
`N1` protection in the current diagnostic models.

## Exact one-flavor baseline

The refreshed exact authority path gives:

- `epsilon_1 / epsilon_DI = 0.927620920920`
- `kappa_1flavor = 0.004829545291`
- `eta / eta_obs = 0.188785929502`

So the post-closure mismatch is not mainly numerator-side anymore.

## Flavored N1 transport diagnostic

For diagonal flavored transport with aligned source fractions

- `epsilon_{1a} = P_a epsilon_1`
- washout `W_a = P_a W`

the exact transport equations can be solved directly on the flavored branch.

This diagnostic already gives large lifts on the exact branch:

- `P = (1/2, 1/2)`:
  - `eta / eta_obs = 0.425764574711`
- `P = (1/3, 1/3, 1/3)`:
  - `eta / eta_obs = 0.693223839689`

and on the one-parameter hierarchical branch

`P = (p, p, 1 - 2p)`

the first crossing of observation occurs at

- `p ~= 0.022895`

That means flavor protection alone can plausibly erase the whole `5.30x` miss,
provided the exact projector theorem does not force democratic projectors.

## Protected N2 sequential diagnostic

The second diagnostic solves a two-source flavored system with:

- `N1` sourcing and washing flavor `a`
- `N2` sourcing and washing flavor `b`
- `b` protected against later `N1` washout

and measures the extra source size needed to reach observation.

Using the diagnostic scaling

- `lambda_2 = M2 / M1 = 1.094973350083`
- `K2 = K1 * M1 / M2 = 43.138930848244`

the results are:

- `epsilon_2 = 0`:
  - `eta / eta_obs = 0.188785929502`
- `epsilon_2 = epsilon_1`:
  - `eta / eta_obs = 0.398594964429`
- observation requires:
  - `epsilon_2 / epsilon_1 ~= 3.86644`

So an `N2` source can help, but it is not the cheapest recovery path in the
current diagnostic models.

## What this changes

This sharpens the post-closure strategy:

- the exact `5.30x` miss is **not** obviously fatal
- the most promising next derivation is a theorem for **non-democratic flavored
  projectors / flavored transport**
- `N2`-aware sequential transport remains relevant, but not as the first or
  cheapest repair route

## What this does not claim

This note does **not** promote a new authority value for `eta`.

The new flavored / `N2` results are diagnostic transport extensions beyond the
current exact one-flavor closure, because the needed flavor projectors and
sequential `epsilon_2` source are not yet theorem-derived on branch.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_flavored_n2_transport_diagnostic.py
```
