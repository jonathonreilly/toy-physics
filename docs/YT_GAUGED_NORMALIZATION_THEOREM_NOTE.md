# Gauged Top-Yukawa Normalization Theorem

**Status:** BARE normalization closed; renormalized matching remains open

This note attacks the missing `Z_Y = Z_g` step directly instead of rephrasing the
older conditional `y_t = g_s / sqrt(6)` result.

## What is now proved

The staggered lattice identities are exact and gauge-field independent:

```text
{Eps, D_gauged} = 2m I
Tr(P_+) / dim(taste) = 1/2
```

The first identity is a genuine gauged Ward identity on the bipartite lattice:
the nearest-neighbour hopping term anticommutes with the chiral parity operator
for arbitrary SU(3) links because the parity flip is geometric, not dynamical.

The second identity is the chiral projector factor in the 8-dim taste space.

Together they fix the **bare cutoff normalization**:

```text
N_c * y_0^2 = g_0^2 * Tr(P_+) / dim(taste) = g_0^2 / 2
y_0 = g_0 / sqrt(2 N_c) = g_0 / sqrt(6)
```

That is the cleanest theorem currently available on this surface.

## What remains open

The renormalized matching step is not fixed by the identities above:

```text
Z_Y(mu) = Z_g(mu)
```

Equivalently, the amputated renormalized Yukawa vertex must be matched to the
renormalized gauge-link normalization in a chosen scheme.

The exact obstruction is simple:

- the chiral Ward identity constrains the operator content
- the projector factor constrains the taste-space trace
- neither of those identities fixes independent finite rescalings of a
  site-local Yukawa insertion and a link-local gauge vertex

So the remaining theorem is not chiral algebra. It is a genuine
Slavnov-Taylor / renormalized matching statement for the full gauged staggered
action.

## Cleanest partial closure

The strongest defensible claim is now:

> At the lattice cutoff, with canonical bare normalization, the top Yukawa is
> fixed by the exact projector factor to `y_0 = g_0 / sqrt(6)`. The only
> missing step for the renormalized theorem is the independent matching
> identity `Z_Y = Z_g`.

That is sharper than the earlier conditional note and isolates the remaining
problem precisely.

## Script

- `scripts/frontier_yt_gauged_normalization_theorem.py`

