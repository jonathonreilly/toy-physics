# Perron-Frobenius Step-2 Two-Route Current-Bank Closure

**Date:** 2026-04-17  
**Status:** exact science-only closure theorem for the step-2A route analysis on the current bank  
**Atlas front door:** `docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_perron_frobenius_step2_two_route_current_bank_closure_2026_04_17.py`  
**Framework convention:** "axiom" means only the single framework axiom `Cl(3)` on `Z^3`.

## Question

After the PF lane has now reduced step 2A to two honest upstream targets

1. `Wilson -> D_-`,
2. `Wilson -> dW_e^H`,

does the **current exact bank** already realize either route?

## Bottom line

No.

The step-2A route analysis is now closed on the current bank:

- the honest upstream route space is exhausted by exactly the strong target
  `Wilson -> D_-` and the compressed target `Wilson -> dW_e^H`;
- the current exact bank realizes neither one.

So the next science is no longer route sorting. It is positive construction.

## What is already exact

### 1. The admissible theorem form is already fixed

From
[PERRON_FROBENIUS_STEP2_OPERATOR_FORM_BOUNDARY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_OPERATOR_FORM_BOUNDARY_NOTE_2026-04-17.md):

- any future positive step-2A theorem must be operator-level;
- the admissible schematic forms are
  `I_e^* T_Wilson I_e -> D_-`
  or
  `P_e T_Wilson P_e -> dW_e^H`.

### 2. The strong route is already the cleanest upstream target

From
[PERRON_FROBENIUS_STEP2_MICROSCOPIC_CHANNEL_TARGET_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_MICROSCOPIC_CHANNEL_TARGET_NOTE_2026-04-17.md):

- the live unresolved content is exactly a Wilson-to-charged microscopic
  channel;
- `Wilson -> D_-` is the cleanest strong target.

### 3. The compressed route is already fully reduced

From
[PERRON_FROBENIUS_STEP2_DIRECT_DWEH_ROUTE_REDUCTION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_DIRECT_DWEH_ROUTE_REDUCTION_NOTE_2026-04-17.md):

- `Wilson -> dW_e^H` is the fully typed compressed alternative;
- after it lands, only the right-sensitive selector on `dW_e^H` remains.

### 4. The current bank already realizes neither route

From
[PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md):

- the current exact bank does **not** already contain the missing
  Wilson-to-`D_-` / Wilson-to-`dW_e^H` descendant theorem under another name.

## Theorem 1: exact closure of step-2A route analysis on the current bank

Assume the exact step-2 operator-form boundary theorem, the exact step-2
microscopic-channel target theorem, the exact step-2 direct-`dW_e^H` route
reduction theorem, and the exact current-bank nonrealization theorem. Then:

1. the honest upstream step-2A route space is exhausted by exactly two routes:
   the strong route `Wilson -> D_-` and the compressed route
   `Wilson -> dW_e^H`;
2. the current exact bank already realizes neither route.

Therefore the step-2A route-analysis problem is closed on the current bank.

## Corollary 1: the next science is positive construction, not more route taxonomy

The branch should not spend further theorem effort on:

- looking for a third upstream route,
- reopening scalar-only or support-only route classes,
- or rescanning the current bank for a hidden realization.

Those possibilities are now closed.

## Corollary 2: the branch can attack both surviving routes in parallel without ambiguity

The only honest upstream construction targets are now:

1. build `Wilson -> D_-`,
2. build `Wilson -> dW_e^H`.

No other step-2A route needs theorem triage first.

## What this closes

- one exact exhaustion of the honest step-2A route space on the current bank;
- one exact negative statement that the current bank realizes neither route;
- one cleaner handoff from theorem-order analysis to positive construction.

## What this does not close

- a positive Wilson-to-`D_-` theorem;
- a positive Wilson-to-`dW_e^H` theorem;
- a positive global PF selector.

## Why this matters

This is the last route-analysis note the PF lane should need.

It tells review, and us, the exact state of play:

- the step-2A search space is now exhausted,
- the current bank realizes none of it,
- so the remaining work is genuinely constructive.

## Atlas inputs used

- [PERRON_FROBENIUS_STEP2_OPERATOR_FORM_BOUNDARY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_OPERATOR_FORM_BOUNDARY_NOTE_2026-04-17.md)
- [PERRON_FROBENIUS_STEP2_MICROSCOPIC_CHANNEL_TARGET_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_MICROSCOPIC_CHANNEL_TARGET_NOTE_2026-04-17.md)
- [PERRON_FROBENIUS_STEP2_DIRECT_DWEH_ROUTE_REDUCTION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_DIRECT_DWEH_ROUTE_REDUCTION_NOTE_2026-04-17.md)
- [PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md)

## Command

```bash
python3 scripts/frontier_perron_frobenius_step2_two_route_current_bank_closure_2026_04_17.py
```
