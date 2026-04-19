# PMNS Oriented Cycle Channel Reduction

**Date:** 2026-04-16  
**Status:** exact reduction theorem  
**Script:** `scripts/frontier_pmns_oriented_cycle_channel_reduction.py`

## Question

Once the local scalar-field route is closed, what is the exact remaining
non-scalar carrier on the retained PMNS active class?

## Answer

The retained canonical active class is exactly:

- diagonal triplet data, plus
- one oriented forward cycle channel.

So after the local scalar boundary removes the diagonal-only route, the
remaining positive carrier is the oriented cycle transport channel

`span{E_12, E_23, E_31}`.

## Exact chain

### 1. Canonical active support

The retained canonical active support is

`I + C`,

so its nonzero entries are exactly:

- diagonal: `(1,1), (2,2), (3,3)`
- forward cycle: `(1,2), (2,3), (3,1)`

No backward-cycle entry survives.

### 2. Unique decomposition

Any canonical active block has the exact decomposition

`A = A_diag + A_fwd`,

where:

- `A_diag` is diagonal
- `A_fwd` lies in `span{E_12, E_23, E_31}`.

There is no backward-cycle contribution on the retained active class.

### 3. Consequence of the local scalar boundary

The local scalar-field theorem shows the retained scalar route can only fill the
diagonal carrier.

Therefore, once the diagonal-only scalar route is excluded, the remaining
positive carrier is not a vague matrix family. It is exactly the oriented
forward cycle channel.

## Consequence

This does not yet derive the values of the cycle channel, but it sharpens the
next target completely:

> the next honest positive target is a value law for the oriented forward cycle
> transport channel, not a scalar deformation law.

## Boundary

This note is a reduction theorem, not a closure theorem.

It does **not** yet derive the forward cycle values. It only isolates the exact
carrier where any future positive retained PMNS law must live.

## Command

```bash
python3 scripts/frontier_pmns_oriented_cycle_channel_reduction.py
```
