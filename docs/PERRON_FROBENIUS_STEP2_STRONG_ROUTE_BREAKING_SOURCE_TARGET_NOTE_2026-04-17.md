# Perron-Frobenius Step-2 Strong-Route Breaking-Source Target

**Date:** 2026-04-17  
**Status:** exact science-only target reduction for the strong `Wilson -> D_-` route on the active charged-lepton branch  
**Atlas front door:** `docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_perron_frobenius_step2_strong_route_breaking_source_target_2026_04_17.py`  
**Framework convention:** "axiom" means only the single framework axiom `Cl(3)` on `Z^3`.

## Question

If the PF lane attacks the strong upstream target

- `Wilson -> D_-`,

what part of `D_-` is the **actual live constructive content** on the active
charged-lepton PMNS branch?

## Bottom line

Not arbitrary full microscopic operator data again.

On the active charged-lepton branch, the live strong-route content is only the
off-seed breaking-source law beyond the already-exact aligned seed patch.

Concretely, the remaining `D_-`-level content is the active off-seed `5`-real
breaking source

`(xi_1, xi_2, eta_1, eta_2, delta)`,

equivalently the off-seed charge-`-1` projected-source law.

So even the strong route is already much narrower than “derive the whole
microscopic operator from scratch.”

## What is already exact

### 1. The strong route is the cleanest upstream target

From
[PERRON_FROBENIUS_STEP2_MICROSCOPIC_CHANNEL_TARGET_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_MICROSCOPIC_CHANNEL_TARGET_NOTE_2026-04-17.md):

- the live unresolved content is a Wilson-to-charged microscopic channel;
- `Wilson -> D_-` is the cleanest strong target.

### 2. The aligned seed patch is already exact but insufficient

From
[DM_LEPTOGENESIS_PMNS_MICROSCOPIC_D_LAST_MILE_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_PMNS_MICROSCOPIC_D_LAST_MILE_NOTE_2026-04-16.md):

- the aligned weak-axis seed patch is already positively closed at the `D`
  level;
- but the active charged-lepton near-closing sample is genuinely off-seed.

So the live strong-route target is not the aligned seed patch again.

### 3. The remaining `D_-`-level object is already reduced

From the same note:

- the remaining `D`-level object is only the active off-seed `5`-real
  breaking source
  `(xi_1, xi_2, eta_1, eta_2, delta)`;
- equivalently it is the off-seed charge-`-1` projected-source law.

So the strong route already has a sharply reduced microscopic target.

### 4. The compressed route agrees on the same live content

From
[PERRON_FROBENIUS_STEP2_DIRECT_DWEH_ROUTE_REDUCTION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_DIRECT_DWEH_ROUTE_REDUCTION_NOTE_2026-04-17.md):

- the compressed route `Wilson -> dW_e^H` already matches the smallest honest
  PMNS-side microscopic last-mile object;
- the only remaining downstream blocker there is the right-sensitive selector.

So the strong and compressed routes are not disagreeing about the live
microscopic content. They differ only in how high upstream they try to realize
it.

## Theorem 1: exact reduction of the strong route to the off-seed breaking-source law

Assume the exact step-2 microscopic-channel target theorem, the exact PMNS
microscopic `D` last-mile reduction theorem, and the exact step-2 direct-
`dW_e^H` route reduction theorem. Then on the active charged-lepton branch:

1. the cleanest strong upstream target is `Wilson -> D_-`;
2. the aligned seed patch is already exact and is not the live missing content;
3. the remaining `D_-`-level content is only the off-seed `5`-real
   breaking-source law, equivalently the off-seed projected-source law.

Therefore the strong `Wilson -> D_-` route is already reduced to a sharply
typed breaking-source target rather than an unconstrained full-operator search.

## Corollary 1: the strong and compressed routes can share the same microscopic work packet

The branch can attack:

- the strong route at `D_-` level,
- and the compressed route at `dW_e^H` level,

while aiming at the same live off-seed breaking-source content.

## Corollary 2: the next positive construction should not target arbitrary `D_-` freedom

The next constructive attempt should not be framed as:

- “find any full `D_-` law.”

It should be framed as:

- derive the off-seed breaking-source law on the active charged-lepton branch,
  ideally from Wilson parent data.

## What this closes

- one exact reduction of the strong route’s live microscopic content;
- one clearer agreement between the strong and compressed step-2A routes;
- one cleaner construction target for the next positive theorem attempt.

## What this does not close

- a positive Wilson-to-`D_-` theorem;
- a positive Wilson-to-`dW_e^H` theorem;
- a positive global PF selector.

## Why this matters

This note keeps the strong route from being overstated.

The branch can now say:

- even the strong route is already reduced to a specific off-seed breaking
  source law on the active charged-lepton branch.

That is a much better construction target than “some full microscopic operator.”

## Atlas inputs used

- [PERRON_FROBENIUS_STEP2_MICROSCOPIC_CHANNEL_TARGET_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_MICROSCOPIC_CHANNEL_TARGET_NOTE_2026-04-17.md)
- [DM_LEPTOGENESIS_PMNS_MICROSCOPIC_D_LAST_MILE_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_PMNS_MICROSCOPIC_D_LAST_MILE_NOTE_2026-04-16.md)
- [PERRON_FROBENIUS_STEP2_DIRECT_DWEH_ROUTE_REDUCTION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_DIRECT_DWEH_ROUTE_REDUCTION_NOTE_2026-04-17.md)

## Command

```bash
python3 scripts/frontier_perron_frobenius_step2_strong_route_breaking_source_target_2026_04_17.py
```
