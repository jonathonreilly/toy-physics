# PMNS Graph-First Fixed-Slice Two-Holonomy Collapse

**Date:** 2026-04-17  
**Status:** exact positive collapse theorem on the PMNS-native fixed-slice current lane  
**Script:** `scripts/PMNS_GRAPH_FIRST_FIXED_SLICE_TWO_HOLONOMY_COLLAPSE_2026_04_17.py`

## Question

On the exact PMNS-native graph-first current image

`(\chi, w) in C x R`,

the sharper no-go already shows that:

- fixing the slice `w = w0`,
- fixing the constant selector bundle `(tau, q)`,
- and fixing one exact native twisted-flux holonomy

still does **not** select `chi`.

Is there then a genuinely new native fixed-slice collapse law on the current
readout bank?

## Answer

Yes.

Once `w = w0` is fixed, the remaining unknown is only

`chi = u + i v`.

And the native one-angle holonomy law on the reduced graph-first family is

`h_phi = 2 u cos(phi) + 2 v sin(phi) + w0`.

Therefore any two-angle family `(phi_1, phi_2)` with

`sin(phi_2 - phi_1) != 0`

gives the exact fixed-slice linear system

```text
[h_phi1 - w0]   [2 cos(phi_1)  2 sin(phi_1)] [u]
[h_phi2 - w0] = [2 cos(phi_2)  2 sin(phi_2)] [v]
```

whose determinant is

`4 sin(phi_2 - phi_1)`.

So two independent native holonomies collapse the fixed slice exactly and
recover `chi` exactly.

## Exact theorem

### 1. One angle is insufficient

The existing one-angle theorem already proves that one native holonomy leaves a
kernel on the reduced carrier, and the sharper fixed-slice theorem proves that
this failure survives even after holding `w = w0` fixed.

So the open object was not “some holonomy law.” It was one genuinely new
fixed-slice collapse law beyond a single probe.

### 2. Two independent angles are enough on a fixed slice

On the reduced family

`A_fwd(u, v, w) = (u + i v) E12 + w E23 + (u - i v) E31`,

the map

`(u, v) -> (h_phi1 - w0, h_phi2 - w0)`

is exactly linear with matrix

`M(phi_1, phi_2) = [[2 cos(phi_1), 2 sin(phi_1)], [2 cos(phi_2), 2 sin(phi_2)]]`.

If `sin(phi_2 - phi_1) != 0`, then `det M != 0`, so:

- `u` is recovered exactly,
- `v` is recovered exactly,
- hence `chi = u + i v` is recovered exactly.

This is the exact positive fixed-slice collapse law.

### 3. Canonical native witness: the `C3` character pair

The native character phases are

- `0`
- `2 pi / 3`
- `4 pi / 3`

So the first two already give one canonical exact fixed-slice collapse pair.

With

- `h_0 = h_(phi=0)`
- `h_(2pi/3) = h_(phi=2 pi / 3)`

one gets the explicit exact formulas

```text
u = (h_0 - w0) / 2
v = (h_0 + 2 h_(2pi/3) - 3 w0) / (2 sqrt(3))
chi = u + i v
```

So the fixed-slice collapse law already has a fully native `C3` witness; no
external Wilson or plaquette input is involved.

## Exact witness pattern

The previous fixed-slice no-go gives two exact witness points on the same slice
`w0 = 0.28` with the same one-angle holonomy at `phi = 0.41`, but with
distinct nonzero currents.

The new theorem sharpens that exact same situation:

- one-angle data still fail on that witness pair,
- but adding one independent second angle already separates the pair,
- and the resulting two-angle fixed-slice system reconstructs each witness
  current exactly.

So the gap was exactly one new independent native holonomy on the fixed slice.

## Consequence

The PMNS-native fixed-slice frontier is now closed on the **readout/collapse**
side.

Before:

> derive a genuinely new fixed-slice current-image collapse law beyond the
> current selector/holonomy bank

Now:

> the exact collapse law is fixed: `w = w0` plus any two independent native
> holonomies reconstructs `chi` exactly

So the remaining PMNS-native blocker is no longer fixed-slice readout.
It is production:

> derive a sole-axiom law that actually produces nonzero `J_chi = chi`

on the retained `hw=1` response family.

## Boundary

This theorem is **not** a new sole-axiom production law for nonzero `J_chi`.

It only proves:

- exact collapse/readout of `chi` on a fixed slice once `w0` and two
  independent native holonomies are supplied.

It does **not** prove:

- that the current sole-axiom bank already produces nonzero `chi`,
- a Wilson descendant theorem,
- any plaquette-side statement,
- any compatibility-front statement.

## Verification

```bash
python3 scripts/PMNS_GRAPH_FIRST_FIXED_SLICE_TWO_HOLONOMY_COLLAPSE_2026_04_17.py
```
