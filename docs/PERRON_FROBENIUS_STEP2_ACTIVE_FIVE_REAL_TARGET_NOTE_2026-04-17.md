# Perron-Frobenius Step-2 Active Five-Real Target

**Date:** 2026-04-17  
**Status:** exact science-only reduction theorem for the live `D_-`-level charged-lepton branch target on step 2A  
**Atlas front door:** `docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_perron_frobenius_step2_active_five_real_target_2026_04_17.py`  
**Framework convention:** "axiom" means only the single framework axiom `Cl(3)` on `Z^3`.

## Question

After all current PF step-2A reductions, what is the **smallest live
`D_-`-level microscopic target** on the active charged-lepton branch?

## Bottom line

It is the active off-seed `5`-real source

`(xi_1, xi_2, eta_1, eta_2, delta)`,

equivalently the off-seed charged projected-source law.

This is the live target on the **strong** upstream PF route:

- strong route: `Wilson -> D_-`.

The compressed route already reduces further to `dW_e^H`, so this note is not
claiming that the active five-real packet is the smallest object on the whole
compressed lane.

So the branch no longer needs to talk about, on the `D_-` side:

- a full PMNS pair law,
- a full charged Hermitian block as a live unknown,
- or an unconstrained full microscopic operator.

## What is already exact

### 1. The one-sided transport object already reduces to the active block

From
[DM_LEPTOGENESIS_PMNS_ACTIVE_PROJECTOR_REDUCTION_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_PMNS_ACTIVE_PROJECTOR_REDUCTION_NOTE_2026-04-16.md):

- on the charged-lepton-active branch `N_e`,
  `|U_PMNS|^2 = |U_e|^2^T`;
- the flavored transport packet is therefore an active-block object;
- after importing branch/orientation and seed-average laws, the remaining
  PMNS-relevant object is exactly the active five-real source.

### 2. The `D`-level last mile already reduces to the same off-seed five-real law

From
[DM_LEPTOGENESIS_PMNS_MICROSCOPIC_D_LAST_MILE_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_PMNS_MICROSCOPIC_D_LAST_MILE_NOTE_2026-04-16.md):

- the aligned seed patch is already exact but insufficient;
- the remaining `D`-level object is only the active off-seed `5`-real
  breaking source
  `(xi_1, xi_2, eta_1, eta_2, delta)`.

### 3. The PF strong and compressed routes agree on route order but not on the same final target size

From
[PERRON_FROBENIUS_STEP2_STRONG_ROUTE_BREAKING_SOURCE_TARGET_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_STRONG_ROUTE_BREAKING_SOURCE_TARGET_NOTE_2026-04-17.md):

- the strong route `Wilson -> D_-` is already reduced to that same off-seed
  breaking-source law.

From
[PERRON_FROBENIUS_STEP2_DIRECT_DWEH_ROUTE_REDUCTION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_DIRECT_DWEH_ROUTE_REDUCTION_NOTE_2026-04-17.md):

- the compressed route `Wilson -> dW_e^H` is already a fully typed upstream
  route with only the right-sensitive selector downstream.

So the two surviving routes agree on constructive order, but the compressed
route already factors through the smaller charged Hermitian projected-source
law `dW_e^H`.

## Theorem 1: exact reduction of the live step-2A PMNS-side target

Assume the exact PMNS active-projector reduction theorem, the exact PMNS
microscopic `D` last-mile reduction theorem, and the exact PF strong-route
breaking-source target theorem. Then on the active charged-lepton branch:

1. the transport-facing PMNS object is already reduced to the active block;
2. the remaining microscopic content is only the off-seed active `5`-real
   source
   `(xi_1, xi_2, eta_1, eta_2, delta)`;
3. this is therefore the smallest live target on the strong `Wilson -> D_-`
   route.

Therefore the smallest live `D_-`-level target on step 2A is exactly the
active off-seed `5`-real source.

## Corollary 1: strong-route positive construction can now be judged against one exact data packet

Any future positive Wilson-side construction should be evaluated by whether it
forces or reconstructs this exact off-seed `5`-real packet on the active
charged-lepton branch when the route is attacked at `D_-` level.

## Corollary 2: larger `D_-`-side unknowns are no longer honest live targets

The branch should not frame the next step as solving:

- a full pair law,
- a full PMNS matrix law,
- or arbitrary full `D_-` freedom.

Those are all larger than the exact live target now isolated.

## What this closes

- one exact identification of the smallest live `D_-`-level target on step 2A;
- one exact sharpening of the strong-route construction packet;
- one clearer benchmark for the next positive construction attempt.

## What this does not close

- a positive Wilson-to-`D_-` theorem;
- a positive Wilson-to-`dW_e^H` theorem;
- a positive global PF selector.

## Why this matters

This note makes the strong-route construction target as small as the current
exact bank allows.

That is useful under hard review because the branch can now say exactly what
data packet the missing Wilson-side law must hit.

## Atlas inputs used

- [DM_LEPTOGENESIS_PMNS_ACTIVE_PROJECTOR_REDUCTION_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_PMNS_ACTIVE_PROJECTOR_REDUCTION_NOTE_2026-04-16.md)
- [DM_LEPTOGENESIS_PMNS_MICROSCOPIC_D_LAST_MILE_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_PMNS_MICROSCOPIC_D_LAST_MILE_NOTE_2026-04-16.md)
- [PERRON_FROBENIUS_STEP2_STRONG_ROUTE_BREAKING_SOURCE_TARGET_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_STRONG_ROUTE_BREAKING_SOURCE_TARGET_NOTE_2026-04-17.md)
- [PERRON_FROBENIUS_STEP2_DIRECT_DWEH_ROUTE_REDUCTION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_DIRECT_DWEH_ROUTE_REDUCTION_NOTE_2026-04-17.md)

## Command

```bash
python3 scripts/frontier_perron_frobenius_step2_active_five_real_target_2026_04_17.py
```
