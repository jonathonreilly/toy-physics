# Majorana Doublet-Block Matching Obstruction

**Date:** 2026-04-15
**Status:** exact blocker-sharpening theorem on the obvious normalized
local-to-doublet matching class
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_neutrino_majorana_doublet_block_matching_obstruction.py`

## Question

After the branch fixes the staircase placement

`k_A = 7`, `k_B = 8`,

could the obvious normalized `2 x 2` generation-doublet block be matched
directly to the exact local self-dual Majorana block and thereby fix

`eps/B`?

## Bottom line

No.

On the fixed staircase placement, the natural generation-doublet block is

`G(r) = eps I + B sigma_x = B (r I + sigma_x)`,

with

`r = eps/B`.

If the off-diagonal doublet baseline `B sigma_x` is used as the natural
generation-side background, then the exact normalized generation observables
are

- `Q_rel^(dbl) = r^2`
- `W_rel^(dbl) = (1/2) log|1-r^2|`

The exact local self-dual Majorana values are

- `Q_rel = 1`
- `W_rel = (1/2) log 2`

These do not match in any perturbative regime:

- quadratic matching forces `r = 1`
- log-response matching forces `r = sqrt(3)`
- no `0 < r < 1` can satisfy the local log-response target at all

So the obvious normalized `2 x 2` local-to-doublet matching class is not the
missing `eps/B` law.

## Inputs

This note uses:

- [NEUTRINO_MAJORANA_BACKGROUND_NORMALIZATION_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_BACKGROUND_NORMALIZATION_THEOREM_NOTE.md)
- [NEUTRINO_MAJORANA_AXIS_EXCHANGE_FIXED_POINT_NOTE.md](./NEUTRINO_MAJORANA_AXIS_EXCHANGE_FIXED_POINT_NOTE.md)
- [NEUTRINO_MAJORANA_ADJACENT_SINGLET_PLACEMENT_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_ADJACENT_SINGLET_PLACEMENT_THEOREM_NOTE.md)
- [NEUTRINO_MAJORANA_EPS_OVER_B_RESIDUAL_RATIO_OBSTRUCTION_NOTE.md](./NEUTRINO_MAJORANA_EPS_OVER_B_RESIDUAL_RATIO_OBSTRUCTION_NOTE.md)

Those notes already fix:

1. the exact local self-dual response values
2. the staircase placement `k_A = 7`, `k_B = 8`
3. the residual free ratio `r = eps/B`

So the next honest rescue attempt is:

> perhaps `r` is fixed by directly matching the normalized local self-dual
> block to the normalized generation-doublet block

## Exact theorem

### 1. The obvious normalized generation-doublet observables are explicit

With

`G(r) = B (r I + sigma_x)`

and baseline

`G_0 = B sigma_x`,

the natural normalized quadratic comparator is

`Q_rel^(dbl) = (Q_2(G) - Q_2(G_0)) / B^2 = r^2`.

The natural normalized bosonic determinant response is

`W_rel^(dbl) = (1/2) log(|det G| / |det G_0|) = (1/2) log|1-r^2|`.

### 2. Matching to the exact local self-dual point fails

The exact local targets are

- `Q_rel = 1`
- `W_rel = (1/2) log 2`

So:

- `Q_rel^(dbl) = 1` forces `r = 1`
- `W_rel^(dbl) = (1/2) log 2` forces `|1-r^2| = 2`, whose only positive
  solution is `r = sqrt(3)`

These are incompatible with each other and both are order-`1`, not
perturbative.

### 3. Therefore the obvious matching class is exhausted

The obvious normalized `2 x 2` local-to-doublet block matching class does not
produce a viable perturbative `eps/B` law.

So the remaining `eps/B` blocker lies beyond that class.

## The theorem-level statement

**Theorem (Doublet-block matching obstruction on the fixed staircase
placement).**
Assume:

1. the exact local self-dual Majorana response values
2. the fixed staircase placement `k_A = 7`, `k_B = 8`
3. the obvious normalized generation-doublet block
   `G(r) = B(r I + sigma_x)` with baseline `B sigma_x`

Then direct matching of the normalized local and normalized generation
doublet observables cannot produce a perturbative `eps/B` law.

Equivalently: the missing `eps/B` theorem is not the obvious normalized
`2 x 2` block match.

## What this closes

This closes one real remaining loophole:

- maybe `eps/B` is already fixed by the simplest normalized local-to-doublet
  block matching once the staircase placement is fixed

Answer: no.

So the remaining blocker is now narrower:

- not staircase placement
- not the residual-ratio class in the abstract
- but a genuinely new `eps/B` law beyond the obvious normalized `2 x 2`
  local-to-doublet matching class

## What this does not close

This note does **not** prove:

- that `eps/B` can never be derived
- that no future non-obvious local-to-generation bridge can exist
- that full DM closure is impossible in principle

It only proves that the most natural normalized `2 x 2` block-matching class
fails.

## Safe wording

**Can claim**

- the obvious normalized `2 x 2` local-to-doublet matching class does not fix
  `eps/B`
- its matches force incompatible order-`1` values instead of a perturbative
  splitting
- the remaining blocker is a genuinely new `eps/B` law

**Cannot claim**

- that every possible `eps/B` route is dead

## Command

```bash
python3 scripts/frontier_neutrino_majorana_doublet_block_matching_obstruction.py
```
