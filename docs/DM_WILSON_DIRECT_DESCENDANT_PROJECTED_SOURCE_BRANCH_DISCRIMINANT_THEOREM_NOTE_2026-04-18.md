# DM Wilson Direct-Descendant Projected-Source Branch Discriminant Theorem

**Date:** 2026-04-18  
**Status:** exact translation theorem for the live conditional branch-choice
rule into projected-source language on `dW_e^H`  
**Script:** `scripts/frontier_dm_wilson_direct_descendant_projected_source_branch_discriminant_theorem_2026_04_18.py`

## Question

After collapsing the live DM flagship frontier to the right-sensitive
microscopic law on
`L_e = Schur_{E_e}(D_-)`,
can the current imposed PMNS branch-choice rule be rewritten exactly at the
projected-source level?

More concretely:

- can the current conditional branch discriminator be expressed as an explicit
  scalar on the full projected Hermitian response pack `dW_e^H`,
- and does that scalar distinguish the live PMNS closure basin from the rival
  basins even though the exact triplet channels `(gamma, E1, E2)` are frozen?

## Bottom line

Yes.

The current imposed branch-choice rule can be transported exactly to the full
projected-source pack.

Write the projected Hermitian response pack on `E_e` as

`(R11, R22, R33, S12, A12, S13, A13, S23, A23)`,

with the standard Hermitian reconstruction

```text
H_e =
[ R11,           (S12 - i A12)/2,  (S13 - i A13)/2 ]
[ (S12 + i A12)/2, R22,           (S23 - i A23)/2 ]
[ (S13 + i A13)/2, (S23 + i A23)/2, R33           ].
```

Then the exact cubic scalar

```text
Delta_src
= R11 R22 R33
  - (R11 S23^2 + R22 S13^2 + R33 S12^2)/4
  - (A12^2 R33 + A13^2 R22 + A23^2 R11)/4
  + (A12 A13 S23 - A12 A23 S13 + A13 A23 S12)/4
  + S12 S13 S23/4
```

is exactly `det(H_e)`.

So on the current PMNS-assisted route, the existing imposed branch-choice rule

- `signature(H_base + J) = signature(H_base)`,
- equivalently on the current basin set `det(H) > 0`,

becomes the explicit projected-source discriminator

- `Delta_src(dW_e^H) > 0`.

This is not yet a retained selector derivation, but it is now an exact
microscopic scalar on `dW_e^H`, not an abstract external branch label.

## Why this matters

This lands the conditional exactly where the science is now focused:

- on `dW_e^H`,
- on `L_e = Schur_{E_e}(D_-)`,
- and on the right-sensitive full projected-source data.

It also closes a fake positive route:

- the projected-source triplet `(gamma, E1, E2)` is **not** enough to recover
  the branch discriminator.

On the live PMNS closure basin set, all three rival basins already carry the
same exact triplet

- `gamma = 1/2`,
- `E1 = sqrt(8/3)`,
- `E2 = sqrt(8)/3`,

while `Delta_src` changes sign.

So the remaining right-sensitive selector cannot factor only through the
triplet channels or their sign chamber.

## What is already exact

### 1. `dW_e^H` reconstructs the full Hermitian block exactly

From
[DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md):

- the projected Hermitian source law `dW_e^H` reconstructs `H_e` exactly.

So any scalar built from `H_e`, including `det(H_e)`, is already an exact
scalar on the full projected-source pack.

### 2. The current branch-choice rule is still the load-bearing conditional

From
[DM_NEUTRINO_SOURCE_SURFACE_PERTURBATIVE_UNIQUENESS_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_PERTURBATIVE_UNIQUENESS_THEOREM_NOTE_2026-04-17.md):

- the current PMNS closure basin selection still depends on the imposed
  baseline-connected branch-choice rule;
- on the live basin set this is recorded as the positive-sign branch
  `det(H) > 0`, equivalently the baseline signature class.

So transporting that rule to projected-source language is the sharpest exact
translation theorem available without pretending the selector is already
derived.

### 3. The projected-source triplet channels are already exact linear readouts

From
[DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_TRIPLET_SIGN_THEOREM_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_TRIPLET_SIGN_THEOREM_NOTE_2026-04-16.md):

- `gamma = A13 / 2`,
- `E1 = (R22 - R33)/2 + (S12 - S13)/4`,
- `E2 = R11 + (S12 + S13)/4 - (R22 + R33)/2 - S23/2`.

Those are exact, but they do not yet supply the full branch discriminator.

## Theorem 1: the imposed branch-choice rule admits an exact projected-source scalar representative

Assume:

1. the exact projected-source reconstruction theorem
   `dW_e^H -> H_e`;
2. the exact projected-source triplet formulas;
3. the current PMNS basin-selection note with the imposed positive-`det`
   branch-choice rule.

Then the exact cubic scalar `Delta_src` above satisfies

- `Delta_src(dW_e^H) = det(H_e)`.

Therefore the current imposed branch-choice rule can be rewritten exactly at
projected-source level as

- `Delta_src(dW_e^H) > 0`

on the baseline-connected live branch.

### Reason

The pack determines `H_e` entrywise, so `det(H_e)` becomes an explicit cubic
polynomial in the nine projected-source coordinates. Expanding the `3 x 3`
Hermitian determinant gives the displayed formula.

Nothing new is assumed beyond the already exact reconstruction.

## Theorem 2: the branch discriminator is strictly finer than the exact triplet channels

On the three in-chamber PMNS closure basins recorded in the perturbative
uniqueness note:

- Basin 1 `(0.657061, 0.933806, 0.715042)` has `Delta_src = +0.959173586493...`;
- Basin 2 `(28.0, 20.7, 5.0)` has `Delta_src = -70377.1856797559...`;
- Basin X `(21.0, 12.68, 2.089)` has `Delta_src = -20061.5977124964...`.

But all three basins still share the same exact projected-source triplet:

- `gamma = 1/2`,
- `E1 = sqrt(8/3)`,
- `E2 = sqrt(8)/3`.

Therefore no selector that factors only through `(gamma, E1, E2)` or their
sign chamber can reproduce the current branch discriminator.

## Corollary 1: the current conditional now lives as a concrete microscopic scalar on `dW_e^H`

The branch is no longer forced to talk only in external language like

- “baseline-connected component of `W[J]`”
- or “signature-preserving admissibility rule”

when it wants the microscopic form of the live conditional.

It can now say the same conditional exactly as:

- the sign of `Delta_src(dW_e^H)`.

## Corollary 2: the next positive theorem target is sharper

The next positive theorem does **not** need to rediscover the triplet channels.
Those are already exact and already frozen.

The next positive theorem should instead aim at one of:

- a right-sensitive microscopic law that forces `Delta_src(dW_e^H) > 0`;
- a finer right-sensitive projected-source law from which
  `Delta_src(dW_e^H) > 0` follows;
- or a direct `L_e` law whose image lands in the positive-`Delta_src` region.

That is the cleanest positive seam now available.

## What this closes

- the translation gap between the current imposed branch-choice rule and the
  projected-source endpoint `dW_e^H`
- the idea that the exact triplet channels might already encode the branch
  discriminator
- the need to keep expressing the live conditional only in upstream `H_base+J`
  language

## What this does not close

- a retained derivation of why `Delta_src(dW_e^H)` must be positive
- a retained selector law for the physical source branch / point
- the final positive DM closeout
