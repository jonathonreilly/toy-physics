# Majorana Residual-Sharing Split Theorem

**Date:** 2026-04-15
**Status:** exact positive split theorem on the minimal symmetric
residual-sharing lift
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_neutrino_majorana_residual_sharing_split_theorem.py`

## Question

After the branch fixes

- the absolute doublet anchor `k_B = 8`
- the minimal singlet placement `k_A = 7`

is the doublet splitting `eps/B` still a fitted residual ratio?

## Bottom line

Not on the minimal symmetric residual-sharing bridge.

Three already-exact ingredients now meet:

1. the local Majorana selector is self-dual at `rho = 1`, so the retained
   normal/background and pairing weights are equal on the admitted local block
2. the singlet lies exactly one staircase step above the anchored doublet, so
   a UV-carried increment appears on the doublet scale with one factor of
   `alpha_LM = B/A`
3. the exact weak-axis return on `T_1` splits into one singled-out channel and
   one exact residual rank-`2` doublet channel `diag(0,1,1)`, so a minimal
   symmetric redistribution over that doublet contributes a factor `1/2`

Therefore the minimal split law is fixed as

`eps/B = alpha_LM / 2`.

Numerically:

`eps/B = 0.045333918...`

This is no longer a fitted placeholder on that bridge.

## Inputs

This note combines:

- [NEUTRINO_MAJORANA_AXIS_EXCHANGE_FIXED_POINT_NOTE.md](./NEUTRINO_MAJORANA_AXIS_EXCHANGE_FIXED_POINT_NOTE.md)
- [NEUTRINO_MAJORANA_ADJACENT_SINGLET_PLACEMENT_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_ADJACENT_SINGLET_PLACEMENT_THEOREM_NOTE.md)
- [DM_NEUTRINO_CASCADE_GEOMETRY_NOTE_2026-04-14.md](./DM_NEUTRINO_CASCADE_GEOMETRY_NOTE_2026-04-14.md)

Those notes already prove:

1. the local selector is the self-dual point `rho = 1`
2. the fixed adjacent bridge places `A` one staircase step above `B`
3. the exact residual doublet return is `diag(0,1,1)`

So the remaining honest question is only how the fixed local background
increment should populate that exact residual doublet.

## Exact theorem

### 1. The local self-dual point fixes equal weights

At the exact local selector

`rho = 1`,

the retained background/normal and pairing components carry equal weight.

### 2. One staircase step gives one factor of `alpha_LM`

The adjacent-placement theorem already fixes

`k_A = 7`, `k_B = 8`.

So a singlet-carried increment viewed on the doublet scale comes with the
exact suppression

`B / A = alpha_LM`.

### 3. The residual pair is exact and symmetric

The weak-axis geometry already gives the exact return split

- `via O_0 = diag(1,0,0)`
- `via T_2 = diag(0,1,1)`

So the residual doublet channel is exactly rank `2` and degenerate.

On the minimal symmetric lift, a redistributed singlet-carried increment must
therefore be shared equally over the two doublet states, giving a factor

`1/2`.

### 4. The split law follows

Putting those exact ingredients together:

`eps/B = rho * (B/A) * (1/2) = 1 * alpha_LM * (1/2) = alpha_LM / 2`.

## The theorem-level statement

**Theorem (Residual-sharing split theorem on the fixed adjacent bridge).**
Assume:

1. the exact local selector is the self-dual point `rho = 1`
2. the fixed staircase placement is `k_A = 7`, `k_B = 8`
3. the exact residual doublet return is the rank-`2` degenerate channel
   `diag(0,1,1)`
4. the local background increment is lifted minimally and symmetrically onto
   that residual doublet

Then the doublet splitting is fixed as

`eps/B = alpha_LM / 2`.

## What this closes

This closes a real denominator-side fit:

- the benchmark `eps/B = 0.041` no longer needs to be treated as fitted on the
  minimal bridge

So the live leptogenesis blocker is no longer the doublet split law.

## What this does not close

This note still does **not** derive:

- the full CP-asymmetry kernel `epsilon_1` beyond the current reduced estimate
- the exact relative sign/interference of the `N_2` and `N_3` contributions
- full PMNS / solar-splitting closure
- full zero-import DM closure

So the remaining blocker is now sharper:

> the exact leptogenesis CP kernel, not the staircase placement or the split
> law.

## Safe wording

**Can claim**

- on the minimal symmetric residual-sharing bridge, the Majorana doublet
  splitting is fixed as `eps/B = alpha_LM/2`
- this removes the old fitted `eps/B` placeholder on that bridge
- the remaining denominator blocker moves downstream to the CP-asymmetry kernel

**Cannot claim**

- that every conceivable Majorana bridge gives the same split law
- that full neutrino phenomenology is already closed
- that DM is fully zero-import closed already

## Command

```bash
python3 scripts/frontier_neutrino_majorana_residual_sharing_split_theorem.py
```
