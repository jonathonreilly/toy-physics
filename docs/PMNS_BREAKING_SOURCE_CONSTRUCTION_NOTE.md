# PMNS Breaking Source Construction

**Date:** 2026-04-15  
**Status:** exact minimal extension theorem for the active breaking triplet
`(delta,rho,gamma)`  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_pmns_new_breaking_source_construction.py`

## Question

The current retained bank already gives the exact global active Hermitian
decomposition

`H = H_core + B(delta,rho,gamma)`,

but it does not derive the breaking triplet values as axiom-side outputs.

If one insists on a genuinely positive source law beyond the retained bank,
what is the smallest exact source/bridge class that can produce nonzero
triplet data?

## Bottom line

The minimal exact extension class is the three-real breaking-source space

`S_break = span_R{T_delta, T_rho, T_gamma}`,

with canonical generators

`T_delta = [[0,0,0],[0,1,0],[0,0,-1]]`,

`T_rho   = [[0,1,-1],[1,0,0],[-1,0,0]]`,

`T_gamma = [[0,0,-i],[0,0,0],[i,0,0]]`.

Equivalently, the breaking source law is exactly

`B(delta,rho,gamma) = delta T_delta + rho T_rho + gamma T_gamma`.

This is the smallest exact source class that can realize generic nonzero
breaking data on the canonical active PMNS branch.

## Atlas and axiom inputs

This theorem reuses:

- `PMNS global Hermitian mode package`
- `PMNS EWSB residual-Z2 Hermitian core`
- `PMNS EWSB alignment nonforcing`
- `PMNS EWSB breaking-slot nonrealization`
- `PMNS intrinsic completion boundary`

The point is not that the current bank already gives `delta`, `rho`, or
`gamma`.
The point is that the breaking sector is now organized into the smallest exact
source class that could carry them.

## Exact source decomposition

Start from the exact global Hermitian package

`H = H_core + B(delta,rho,gamma)`,

with aligned real core

`H_core = [[a,b,b],[b,c,d],[b,d,c]]`

and breaking matrix

`B(delta,rho,gamma) = [[0,rho,-rho-i gamma],[rho,delta,0],[-rho+i gamma,0,-delta]]`.

Then one checks directly that

`B(delta,rho,gamma) = delta T_delta + rho T_rho + gamma T_gamma`.

So the breaking sector is not a loose vector of coordinates.
It is an exact 3-real source space with a canonical basis.

## Why this is minimal

The aligned core is the residual-`Z_2` admissible surface.
Away from that surface, the breaking sector is exactly three-real-dimensional.

The three canonical source generators are linearly independent over `R`, so
any exact source class that can generate generic breaking data must have at
least three real degrees of freedom.

Therefore no one-parameter or two-parameter source law can be the smallest
exact positive extension class for generic nonzero breaking data.

In other words:

- the aligned core is codimension three
- the breaking sector is exactly three-real-dimensional
- so the smallest exact source/bridge class is the 3-real breaking triplet

## Theorem-level statement

**Theorem (Minimal exact source class for the PMNS breaking triplet).**
Assume the exact global Hermitian decomposition
`H = H_core + B(delta,rho,gamma)`, the exact EWSB residual-`Z_2` core theorem,
the exact EWSB alignment nonforcing theorem, and the exact breaking-slot
nonrealization theorem. Then any positive source realization of generic
nonzero breaking data must:

1. lie outside the current retained support-plus-scalar bank
2. leave the aligned residual-`Z_2` core
3. have at least three real source directions
4. reduce on the canonical basis to
   `delta T_delta + rho T_rho + gamma T_gamma`

Therefore the smallest exact source/bridge class that can produce nonzero
triplet data is the 3-real breaking-source space
`span_R{T_delta,T_rho,T_gamma}`.

## What this closes

This closes the extension-class question for the breaking triplet.

It is now exact that:

- the breaking data are not a single hidden scalar
- they are not a two-parameter deformation of the aligned core
- they are the canonical 3-real source complement to the aligned surface

So the minimal new science object is not a new aligned core.
It is the breaking-source triplet itself.

## What this does not close

This note does **not** derive:

- the values of `delta`, `rho`, or `gamma` from the axiom bank
- a microscopic law selecting a particular nonzero breaking source
- the selected-branch Hermitian data law

So this is a minimal exact extension theorem, not a full positive derivation of
the breaking-triplet values.

## Command

```bash
python3 scripts/frontier_pmns_new_breaking_source_construction.py
```
