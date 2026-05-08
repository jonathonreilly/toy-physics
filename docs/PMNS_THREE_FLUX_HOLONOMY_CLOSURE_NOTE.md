# PMNS Three-Flux Holonomy Closure

**Status:** bounded - bounded or caveated result note
**Date:** 2026-04-16  
**Script:** `scripts/frontier_pmns_three_flux_holonomy_closure.py`

## Question

Can a finite native family of twisted flux holonomies close the reduced
graph-first PMNS oriented-cycle family exactly?

## Answer

Yes.

On the reduced graph-first cycle family

`A_fwd(u,v,w) = u B1 + v B2 + w B3`

the one-angle flux holonomy is the exact linear functional

`h_phi(A_fwd) = 2 u cos(phi) + 2 v sin(phi) + w`.

Therefore a generic three-angle family `phi_1, phi_2, phi_3` gives the exact
linear system

`M(phis) [u,v,w]^T = h`

with rows `[2 cos(phi_i), 2 sin(phi_i), 1]`.

Whenever `det M(phis) != 0`, the reduced coordinates `(u,v,w)` are recovered
exactly.

## Exact content

For the explicit generic choice

- `phi_1 = 0`
- `phi_2 = pi/2`
- `phi_3 = pi/3`

the design matrix is

```text
[[2,   0,       1],
 [0,   2,       1],
 [1, sqrt(3),   1]]
```

and has nonzero determinant.

So:

1. the three-flux holonomy vector is the exact image of `(u,v,w)`
2. the reduced coordinates are reconstructed exactly by solving that system
3. distinct reduced-channel points are separated exactly by the three-flux
   holonomy data

## Consequence

This upgrades the twisted-flux route from a partial value law to a positive
closure route on the reduced PMNS cycle family.

It is now strengthened further by
[PMNS_C3_CHARACTER_HOLONOMY_CLOSURE_NOTE.md](./PMNS_C3_CHARACTER_HOLONOMY_CLOSURE_NOTE.md),
which shows that the exact `C3` character triple already supplies a canonical
native three-mode holonomy family. So the result below can now be read in two
ways:

- as a generic three-flux closure theorem, and
- more strongly, as a native `C3`-character closure theorem on the retained
  graph-first cycle frame.

It does **not** by itself prove full sole-axiom neutrino closure from
`Cl(3)` on `Z^3` alone. What remains blocked after the stronger `C3`-character
upgrade is no longer the readout family itself, but the sole-axiom production
of **nontrivial values** on that native family.

## Verification

```bash
python3 scripts/frontier_pmns_three_flux_holonomy_closure.py
```
