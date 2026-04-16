# PMNS Oriented Cycle Reduced-Channel Nonselection

**Date:** 2026-04-16  
**Status:** exact nonselection theorem  
**Script:** `scripts/frontier_pmns_oriented_cycle_reduced_channel_nonselection.py`

## Question

Once the retained PMNS lane is reduced to the graph-first selected-axis
oriented-cycle channel, does the current exact bank select the remaining cycle
values?

## Answer

No.

The current exact bank now closes:

- the oriented-cycle carrier
- the native observable/value law on that carrier
- the exact graph-first residual symmetry reduction

But it still does **not** select a unique value on the reduced channel.

The exact reduced family is

`A_fwd(u,v,w) = (u + i v) E_12 + w E_23 + (u - i v) E_31`

and every point of that `3`-real family:

- satisfies the residual antiunitary symmetry
  `A_fwd = P_23 A_fwd^dagger P_23`
- is read exactly by the native observable law
- is realized exactly on the lower-level active response chain

So the last remaining value-selection problem closes negatively for the current
exact bank.

## Exact chain

### 1. Reduced graph-first family

The graph-first selected-axis route reduces the oriented cycle channel to the
`3`-real family

`(u,v,w) <-> (c_1,c_2,c_3) = (u + i v, w, u - i v)`.

Equivalently,

- `c_1 = conjugate(c_3)`
- `c_2` real

### 2. Exact native observable law on the reduced family

The native oriented-cycle observable law already gives

`(c_1,c_2,c_3) = diag(A C^dagger)`.

So on the reduced family, the remaining real coordinates are read exactly as

- `u = Re(c_1)`
- `v = Im(c_1)`
- `w = Re(c_2)`

No further projection ambiguity remains.

### 3. Exact realization on the lower-level active response chain

For any reduced-channel point `(u,v,w)`, the active block

`A = xbar I_3 + A_fwd(u,v,w)`

is recovered exactly from a lower-level active response profile via the already
proved active response chain.

So the reduced family is not merely formal. It is exactly realizable on the
current lower-level active transport/response chain.

### 4. Nonselection theorem

There exist distinct reduced-channel points `(u,v,w) != (u',v',w')` such that:

- both satisfy the graph-first residual antiunitary symmetry
- both sit on the retained diagonal-plus-forward-cycle support
- both are read exactly by the native observable law
- both are realized exactly on the lower-level active response chain

Therefore the current exact bank does not select a unique reduced-channel
value.

## Consequence

This is the clean closeout for the last retained oriented-cycle object.

What remains is **not** another hidden theorem inside the current bank.
Any further positive value-selection law would have to come from:

- genuinely new dynamics, or
- a further admitted extension beyond the current exact bank

## Boundary

This is not a positive value-selection theorem.

It is the exact negative closeout theorem for the retained graph-first reduced
cycle channel.

## Command

```bash
python3 scripts/frontier_pmns_oriented_cycle_reduced_channel_nonselection.py
```
