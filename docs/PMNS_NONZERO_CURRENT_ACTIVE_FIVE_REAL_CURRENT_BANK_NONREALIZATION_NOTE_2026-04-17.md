# PMNS Nonzero Current Active Five-Real Current-Bank Nonrealization

**Date:** 2026-04-17  
**Status:** exact impossibility theorem on the PMNS-native strong production lane  
**Script:** `scripts/PMNS_NONZERO_CURRENT_ACTIVE_FIVE_REAL_CURRENT_BANK_NONREALIZATION_2026_04_17.py`

## Question

Does the **current exact PMNS-native bank** already determine the active
off-seed `5`-real packet and therefore already realize a sole-axiom law for
nonzero

`J_chi`?

## Answer

No.

The sharp exact impossibility is:

1. the current bank already fixes the aligned seed pair and the current native
   transport summaries on the active microscopic block;
2. those data still leave the active off-seed `5`-real packet free;
3. that free packet already moves the native current `J_chi`.

Therefore the current exact PMNS-native bank still does **not** determine the
current-producing packet and still does **not** realize a sole-axiom law for
nonzero `J_chi` on the strong microscopic route.

## Exact impossibility

### 1. The current bank stops at seed data and transport summaries

The strongest current PMNS-native microscopic laws already recover:

- the aligned seed pair `(xbar, ybar)`,
- the projected transfer kernel,
- and the orbit-averaged corner-transport moments / branch-side summaries.

But those are only the seed-facing part of the active block.

### 2. Explicit witness pair

Take the same witness pair as in the reduction theorem:

- `A = T_act((1.15, 0.82, 0.95), (0.41, 0.28, 0.54), 0.63)`
- `B = T_act((1.20, 0.79, 0.93), (0.52, 0.17, 0.54), 0.63)`

Then:

- `A` and `B` have the same projected transfer kernel;
- `A` and `B` have the same orbit-averaged transport moments;
- `A` and `B` have different active off-seed packets;
- and
  - `J_chi(A) = 0.423167427244281 - 0.159069084644413 i`
  - `J_chi(B) = 0.478167427244281 - 0.159069084644413 i`.

So the current bank’s strongest native microscopic summaries do **not** select
the current.

### 3. The retained sole-axiom routes still force zero current

The explicit retained PMNS-native sole-axiom routes already satisfy

`J_chi = 0`

on:

- the free route,
- the canonical sole-axiom `hw=1` source/transfer route,
- the retained scalar route.

So the current bank has both:

- explicit zero-current retained routes,
- and microscopic witness pairs where the surviving unresolved packet moves
  `J_chi`.

That is exactly the shape of a current-bank nonrealization theorem.

## Consequence

This is the strongest sharper exact impossibility now available on the
PMNS-native strong production front.

Before:

> the current bank does not yet supply a nontrivial fixed-slice holonomy-pair
> source law

Now:

> the current bank does not even determine the smallest live PMNS-native
> current-producing packet on the strong microscopic route, namely the active
> off-seed `5`-real packet

So no sole-axiom nonzero-`J_chi` production law is yet present on the current
PMNS-native strong lane.

## Boundary

This theorem does **not** prove:

- a positive law for the active off-seed `5`-real packet;
- a compressed-route `dW_e^H` theorem;
- a Wilson descendant theorem;
- a global PF selector.

It proves only the sharper negative statement:

- the current bank still leaves the exact current-producing packet unresolved,
  and therefore still leaves nonzero `J_chi` unresolved.

## Verification

```bash
python3 scripts/PMNS_NONZERO_CURRENT_ACTIVE_FIVE_REAL_CURRENT_BANK_NONREALIZATION_2026_04_17.py
```
