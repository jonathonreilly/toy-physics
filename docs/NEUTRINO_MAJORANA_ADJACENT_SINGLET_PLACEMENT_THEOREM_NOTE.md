# Majorana Adjacent Singlet-Placement Theorem

**Date:** 2026-04-15  
**Status:** exact positive placement theorem on the minimal adjacent
local-to-generation lift  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_neutrino_majorana_adjacent_singlet_placement_theorem.py`

## Question

After the endpoint-exchange midpoint theorem fixes the absolute doublet anchor

`k_B = 8`,

can the branch also fix the singlet placement, rather than leaving the old
`k_A = k_B - 1` relation as a benchmark?

## Bottom line

Yes, on the minimal adjacent lift of the exact weak-axis cascade geometry.

The exact `Gamma_1` return on `T_1` already splits into:

- one singled-out rank-`1` channel through `O_0`
- one residual rank-`2` channel through `T_2`

and the `O_0` path is exactly one Hamming-weight step closer to the UV
endpoint than `T_1`.

So once the doublet anchor is fixed at

`k_B = 8`,

the minimal adjacent lift places the singled-out singlet one staircase level
above that anchor:

`k_A = 7`.

Equivalently: the branch no longer needs to treat the singlet/doublet
placement as a loose benchmark if it accepts the same kind of minimal
non-homogeneous lift already used in the midpoint theorem.

## Inputs

This note combines three already-exact surfaces:

- [DM_NEUTRINO_CASCADE_GEOMETRY_NOTE_2026-04-14.md](./DM_NEUTRINO_CASCADE_GEOMETRY_NOTE_2026-04-14.md)
- [NEUTRINO_MAJORANA_ENDPOINT_EXCHANGE_MIDPOINT_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_ENDPOINT_EXCHANGE_MIDPOINT_THEOREM_NOTE.md)
- [THREE_GENERATION_STRUCTURE_NOTE.md](./THREE_GENERATION_STRUCTURE_NOTE.md)

Those notes already prove:

1. the exact weak-axis return on `T_1` splits into one singled-out channel and
   one residual two-state channel
2. the doublet anchor is fixed at `k_B = 8` on the minimal endpoint-exchange
   bridge
3. the relevant taste sectors are exactly organized by Hamming-weight
   adjacency on `Z^3`

So the remaining honest question is:

> how should that exact `1 + 2` split be embedded on the already-fixed finite
> staircase?

## Exact theorem

### 1. The `1 + 2` split is exact on `T_1`

The weak-axis operator geometry already gives

- `via O_0 = diag(1,0,0)`
- `via T_2 = diag(0,1,1)`

So one state is exactly singled out, while the remaining two form an exact
residual pair.

### 2. The singled-out channel is the unique UV-directed one

On the chosen weak axis:

- `T_1` has Hamming weight `1`
- `O_0` has Hamming weight `0`
- `T_2` has Hamming weight `2`

So the singled-out `O_0` path is the unique one-step move toward the UV
endpoint, while the residual pair is carried by the `T_2` path.

### 3. The midpoint theorem fixes the doublet anchor

The endpoint-exchange midpoint theorem already fixes the absolute staircase
anchor

`k_B = 8`.

This is the anchored scale of the residual doublet sector on the minimal
bridge.

### 4. The minimal adjacent lift fixes the singlet placement

If the staircase lift preserves the exact adjacency information of the
weak-axis split, then the unique UV-directed singled-out channel must sit one
step above the anchored doublet.

Therefore:

`k_A = k_B - 1 = 7`.

## The theorem-level statement

**Theorem (Adjacent singlet-placement theorem on the midpoint-anchored
Majorana cascade).**
Assume:

1. the exact weak-axis `1 + 2` split on `T_1`
2. the exact midpoint anchor `k_B = 8`
3. the minimal adjacent lift that preserves the UV-directed taste adjacency of
   the singled-out `O_0` channel

Then the singlet/doublet placement is fixed as

`k_A = 7`, `k_B = 8`.

## Relationship to the midpoint theorem

This note is downstream of the midpoint theorem.

The midpoint theorem closed:

- the absolute staircase anchor of the selected Majorana scale

This note closes the next placement step:

- which side of that anchor the singled-out singlet sits on

So the branch now has:

- exact doublet anchor: `k_B = 8`
- exact singlet placement on the minimal adjacent lift: `k_A = 7`

## What this closes

This closes one real denominator-side gap:

- the singlet/doublet placement no longer needs to remain a benchmark

So the live blocker is no longer:

- absolute staircase anchor
- singlet/doublet placement

## What this does not close

This note still does **not** derive:

- the doublet splitting `eps/B`
- the full three-generation `A/B/epsilon` amplitudes
- the remaining `m_3` / texture-factor inputs in the leptogenesis chain
- full zero-import `eta`

So the remaining denominator blocker is now narrower:

> the staircase placement is fixed on the minimal bridge, but the amplitude
> law inside the `A/B/epsilon` texture is still not derived.

## Safe wording

**Can claim**

- the exact midpoint theorem plus the exact weak-axis `1 + 2` geometry fix the
  singlet/doublet placement on the minimal adjacent lift
- the resulting placement is `k_A = 7`, `k_B = 8`
- the remaining blocker is now the doublet splitting / texture-amplitude law,
  especially `eps/B`

**Cannot claim**

- the full `A/B/epsilon` texture is already derived
- the full leptogenesis denominator is already closed
- the entire DM lane is fully across the line

## Command

```bash
python3 scripts/frontier_neutrino_majorana_adjacent_singlet_placement_theorem.py
```
