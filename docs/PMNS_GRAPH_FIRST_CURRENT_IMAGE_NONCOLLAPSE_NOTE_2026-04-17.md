# PMNS Graph-First Current-Image Noncollapse

**Date:** 2026-04-17  
**Status:** exact sharpening theorem on the PMNS-native graph-first current lane  
**Script:** `scripts/frontier_pmns_graph_first_current_image_noncollapse_2026_04_17.py`

## Question

Can the graph-first nontrivial-current activation-law target be sharpened on the
current PMNS-native sole-axiom bank?

## Answer

Yes.

The sharper exact result is a **no-go**:

1. on the graph-first reduced lane, the current bank already identifies the
   exact native current image as

   `(\chi, w) in C x R`

   with

   `J_chi = chi`

2. every point of that image is realized exactly on the lower-level active
   response chain
3. even after fixing the trivial-character coordinate `w`, the current bank
   still realizes distinct nonzero currents `chi`

So the current PMNS-native bank does not merely fail to select a point on a
`3`-real family. It already realizes the full graph-first current image and
does not collapse it.

Therefore no hidden current-bank law below a genuinely new collapse relation on
`(\chi, w)` can activate or select nonzero `J_chi`.

## Exact sharpening

### 1. The exact graph-first current image is `C x R`

The graph-first reduced family is

`A_fwd(u,v,w) = (u + i v) E12 + w E23 + (u - i v) E31`.

The exact native `C3` character-mode reduction already gives

- `z0 = w`
- `z2 = chi = u + i v`
- `J_chi = chi`

So the exact reduced PMNS-native current image is not an unspecified
`3`-parameter carrier anymore. It is exactly:

- one real trivial-character coordinate `w`
- one complex nontrivial current `chi`

### 2. The current bank realizes the whole image

The reduced-channel nonselection theorem already proves that every
graph-first reduced point is realized exactly on the active response chain.

Since `(u,v,w)` and `(\chi,w)` are equivalent coordinates with `chi = u + i v`,
the current bank therefore realizes every point of `C x R` on this graph-first
lane.

### 3. Even fixed `w` slices do not select `chi`

This is the sharper no-go.

The bank does not merely fail globally on the full `(\chi,w)` image. Even on a
fixed trivial-character slice `w = w0`, distinct nonzero currents `chi != chi'`
are both realized exactly.

So a future theorem that only fixes `w` would still not activate or select the
native current.

## Consequence

This sharpens the next honest theorem target.

Before:

> derive a PMNS-native graph-first nontrivial-current activation law

Now:

> derive a PMNS-native **graph-first current-image collapse law** on the exact
> `(\chi, w)` image, and in particular a **fixed-slice nontrivial-current
> activation law** that selects nonzero `chi` even after the trivial mode `w`
> is held fixed.

That is smaller and more exact than a generic activation law on the whole
reduced family.

## Verification

```bash
python3 scripts/frontier_pmns_graph_first_current_image_noncollapse_2026_04_17.py
```
