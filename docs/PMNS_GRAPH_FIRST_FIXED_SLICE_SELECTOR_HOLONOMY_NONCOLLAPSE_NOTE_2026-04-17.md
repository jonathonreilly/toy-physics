# PMNS Graph-First Fixed-Slice Selector/Holonomy Noncollapse

**Date:** 2026-04-17  
**Status:** exact sharpening theorem on the PMNS-native fixed-slice current lane  
**Script:** `scripts/frontier_pmns_graph_first_fixed_slice_selector_holonomy_noncollapse_2026_04_17.py`

## Question

Starting from the exact PMNS-native graph-first current image

`(\chi, w) in C x R`,

can the **current exact native bank** already collapse a fixed slice `w = w0`
by reusing its currently admitted graph-first selector/holonomy data?

More concretely, does the current bank already force a unique nonzero current
`chi` once one fixes:

- the trivial-character coordinate `w`,
- the graph-first selector bundle `(tau, q)`,
- one exact native twisted-flux holonomy probe?

## Answer

No.

The strongest honest next theorem surface is a **sharper exact impossibility
result** on the current bank:

1. the exact PMNS-native graph-first current image is already
   `(\chi, w) in C x R` with `J_chi = chi`
2. the graph-first projected-commutant selector bundle `(tau, q)` is constant
   on the reduced graph-first family, hence also constant on every fixed
   `w` slice
3. even after fixing one exact native twisted-flux holonomy value on a fixed
   slice `w = w0`, distinct nonzero currents `chi != chi'` are still both
   realized exactly on the lower-level active response chain

So the current PMNS-native bank does not merely fail to activate the current on
the full `(\chi, w)` image. It still fails after all currently admitted
graph-first selector/holonomy data below the full character readout are held
fixed.

## Exact sharpening

### 1. The exact current image is already `(\chi, w)`

The current-image noncollapse theorem already closes the native graph-first
current image exactly as

`(\chi, w) in C x R`

with

`J_chi = chi`.

So the unresolved object is no longer a vague `3`-real cycle carrier.

### 2. The selector bundle does not collapse a fixed slice

The graph-first projected-commutant boundary theorem already proves that the
exact graph-native selector bundle `(tau, q)` is constant on the reduced
graph-first family.

Therefore fixing `(tau, q)` adds no collapse on a fixed `w` slice at all.

### 3. One exact native holonomy probe still does not collapse a fixed slice

The twisted-flux holonomy boundary theorem proves that one exact native flux
holonomy is a genuine value law on its own fluxed carrier, but has a kernel on
the reduced PMNS graph-first family.

The sharper fixed-slice statement is:

- there exist two distinct reduced graph-first points with the same exact
  trivial mode `w = w0`,
- the same exact selector bundle `(tau, q)`,
- the same exact one-angle twisted-flux holonomy value,
- but distinct nonzero currents `chi != chi'`.

So even the natural current-bank sharpening below the full exact character
readout still does not select `chi`.

### 4. Exact witness pair

At `phi = 0.41`, with fixed slice `w0 = 0.28`, one exact witness pair is:

- `A = A_fwd(0.41, 0.32, 0.28)`
- `B = A_fwd(0.5694437311937691, -0.04684832912664205, 0.28)`

These satisfy:

- both are graph-first reduced points
- both are realized exactly on the lower-level active response chain
- both have the same exact `w = 0.28`
- both have the same exact projected-commutant selector bundle `(tau, q) = (0, 2)`
- both have the same exact one-angle twisted-flux holonomy at `phi = 0.41`
- but
  - `J_chi(A) = 0.41 + 0.32 i`
  - `J_chi(B) = 0.5694437311937691 - 0.04684832912664205 i`

So the fixed slice still does not collapse.

## Consequence

This sharpens the PMNS-native frontier again.

Before:

> derive a graph-first current-image collapse law on `(\chi, w)`, in
> particular a fixed-slice nontrivial-current activation law

Now:

> derive a genuinely new fixed-slice current-image collapse law **beyond**
> the current graph-first selector bundle `(tau, q)` and beyond one-angle
> native twisted-flux holonomy.

That is the strongest honest next theorem surface on the PMNS-native side of
the current bank.

## Verification

```bash
python3 scripts/frontier_pmns_graph_first_fixed_slice_selector_holonomy_noncollapse_2026_04_17.py
```
