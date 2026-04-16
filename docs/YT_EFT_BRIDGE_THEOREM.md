# y_t EFT Bridge Theorem: Backward Ward Boundary Transfer at `v`

**Date:** 2026-04-15  
**Status:** closed subderivation on open lane; bridge-conditioned  
**Primary runner:** `scripts/frontier_yt_eft_bridge.py`

## Authority role

This note is a supporting theorem inside the current bounded zero-import
renormalized `y_t` authority stack.

It does **not** close the full `y_t` lane by itself. Its job is narrower:

- explain why the physical crossover endpoint is `v`
- explain why the backward Ward transfer is the correct low-energy bridge
- explain why the naive direct-EFT Ward alternative fails

Use this note together with:

- [YT_ZERO_IMPORT_AUTHORITY_NOTE.md](./YT_ZERO_IMPORT_AUTHORITY_NOTE.md)
- [YT_BOUNDARY_THEOREM.md](./YT_BOUNDARY_THEOREM.md)

## Safe statement

The current framework-native bridge is:

1. fix `\alpha_s(v) = 0.1033` from the coupling-map / vertex route
2. treat the SM EFT below `v` as the perturbative low-energy transfer surface
3. impose the lattice Ward boundary at the lattice side
4. transfer that boundary to `y_t(v)` by backward RGE continuation

On that bridge, the current bounded zero-import route gives:

- `y_t(v) = 0.973`
- `m_t = 169.4 GeV`

## Why the backward Ward transfer is the correct bridge

The Ward identity `y_t/g_s = 1/sqrt(6)` belongs to the lattice theory.
The low-energy EFT below `v` has different field content and different
effective couplings, so the Ward identity should not be imposed there as if it
were an EFT symmetry relation.

The clean bridge is therefore:

- lattice Ward identity on the lattice side
- EFT running on the EFT side
- transfer through the `v` endpoint selected by the boundary theorem

That keeps domain separation explicit and avoids mixing lattice and EFT
couplings on the same footing.

## Why the naive direct-EFT Ward alternative fails

Applying `y_t/g_s = 1/sqrt(6)` directly to the EFT coupling at `v` is not the
same operation as applying the Ward identity in the lattice theory and then
transferring the result downward.

The reason is the `u_0` dressing mismatch:

| Operator class | Effective link dressing | Consequence |
|---|---|---|
| gauge vertex | `u_0^2` | contributes to `\alpha_s(v)` through the coupling-map route |
| Yukawa vertex | `u_0^0` | does not inherit the same dressing factor |

So the naive direct-EFT Ward step mixes quantities that no longer live on the
same improvement surface. The backward transfer avoids that category error.

## What this theorem proves

1. the low-energy bridge should be anchored at `v`
2. the backward Ward transfer is the correct bounded bridge on the current
   authority stack
3. the direct-EFT Ward alternative is not a viable competing route

## What it does not prove

This theorem does not by itself make the renormalized `y_t` lane unbounded.

The package still keeps the full lane in the bounded portfolio because:

- the low-energy bridge is still treated as bridge-conditioned
- the full route still relies on perturbative EFT infrastructure below `v`
- the package still distinguishes zero-import and import-allowed bounded
  companion readings

## Runner role

`scripts/frontier_yt_eft_bridge.py` is the supporting runner for this note.
It is not the primary quantitative authority. The primary quantitative
authority remains `scripts/frontier_yt_2loop_chain.py`.
