# DM Neutrino Breaking-Triplet CP Theorem

**Date:** 2026-04-15  
**Status:** exact triplet-coordinate form of the intrinsic DM CP tensor  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_dm_neutrino_breaking_triplet_cp_theorem.py`

## Question

The active Hermitian DM endpoint is now exact on the seven-coordinate grammar.
Can that endpoint be rewritten in the canonical breaking-source coordinates
already isolated on the PMNS lane?

## Bottom line

Yes.

On the exact decomposition

- `H = H_core + B(delta,rho,gamma)`
- `H_core = [[A,b,b],[b,c,d],[b,d,c]]`
- `B = [[0,rho,-rho-i gamma],[rho,delta,0],[-rho+i gamma,0,-delta]]`

the intrinsic positive-section DM CP tensor becomes

- `Im[(K_mass)01^2] = -2 gamma (delta + rho) / 3`
- `Im[(K_mass)02^2] =  2 gamma (A + b - c - d) / 3`.

So the remaining DM object is even sharper than the seven-coordinate formula:

- `gamma` is the mandatory CP-odd source
- `delta + rho` is the breaking-breaking interference channel
- `A + b - c - d` is the core-breaking interference channel

## Inputs

This note combines:

- [DM_NEUTRINO_POSITIVE_POLAR_H_CP_THEOREM_NOTE_2026-04-15.md](./DM_NEUTRINO_POSITIVE_POLAR_H_CP_THEOREM_NOTE_2026-04-15.md)
- [PMNS_BREAKING_SOURCE_CONSTRUCTION_NOTE.md](/Users/jonBridger/Toy%20Physics-neutrino-majorana/docs/PMNS_BREAKING_SOURCE_CONSTRUCTION_NOTE.md:1)

The PMNS note supplies the canonical triplet basis
`(delta,rho,gamma)`. This note computes the DM tensor on that exact basis.

## Exact theorem

Substituting

- `d1 = A`
- `d2 = c + delta`
- `d3 = c - delta`
- `r12 = b + rho`
- `r31 cos(phi) = b - rho`
- `r31 sin(phi) = gamma`

into the intrinsic Hermitian formula gives:

- `Im[(K_mass)01^2] = -2 gamma (delta + rho) / 3`
- `Im[(K_mass)02^2] =  2 gamma (A + b - c - d) / 3`

So the aligned-core no-go is simply the zero-triplet limit
`delta = rho = gamma = 0`.

## What this closes

This closes the coordinate-language ambiguity on the last-mile DM object.

It is now exact that:

- the remaining H-side gap is not an arbitrary seven-variable deformation
- it is a triplet-side law with one CP-odd source and two interference
  channels

## What this does not close

This note does **not** derive the values of

- `gamma`
- `delta + rho`
- `A + b - c - d`

from the axiom bank. It only identifies them as the exact remaining objects.

## Command

```bash
python3 scripts/frontier_dm_neutrino_breaking_triplet_cp_theorem.py
```
