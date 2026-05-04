# Universal GR Lorentzian Global Atlas Closure on `PL S^3 x R`

**Status:** support - structural or confirmatory support note
**Date:** 2026-04-14  
**Primary runner:** [`scripts/frontier_universal_gr_lorentzian_global_atlas_closure.py`](../scripts/frontier_universal_gr_lorentzian_global_atlas_closure.py) (PASS=5/0)
**Branch:** `codex/review-active`  
**Role:** direct universal route / finite-atlas global theorem

## Verdict

The direct-universal Lorentzian route now patches globally across a finite
atlas of the discrete spacetime `PL S^3 x R`.

This is the global strengthening that the positive-background local theorem was
still missing.

The exact local Lorentzian action family is not merely chartwise valid. It
glues across overlaps by exact congruence covariance, so compatible local
stationary fields define a unique global stationary section on the finite
atlas.

## Exact patching mechanism

The exact local bilinear form is

`B_D(h,k) = -Tr(D^-1 h D^-1 k)`.

Under an invertible chart/frame change `S`,

`D' = S^T D S`,
`h' = S^T h S`,
`k' = S^T k S`,

and therefore

`B_{D'}(h',k') = B_D(h,k)`.

So the local Hessian is not merely covariant in a bookkeeping sense. It is an
exact overlap-invariant quadratic density.

If `T_S` is the induced representation on symmetric `3+1` coefficient vectors,
then the local operator matrices obey the exact overlap relation

`G_{D'} = T_S^{-T} G_D T_S^-1`,

and the glued operator family

`K_GR(D) = H_D ⊗ Lambda_R`

transforms accordingly on overlaps.

## Global stationary section

Because:

- each local Lorentzian operator `K_GR(D)` is nondegenerate;
- the local action densities agree exactly on overlaps;
- the source/field pairing transforms compatibly;

the local stationary solutions transform compatibly across the atlas.

So on a finite atlas of the discrete spacetime route, the local family defines
one exact global stationary section.

This is the right discrete-global theorem on the current branch:

> the direct-universal Lorentzian Einstein/Regge action family is globally
> well-defined on finite atlases of `PL S^3 x R`, and its local stationary
> representatives patch exactly into a unique global stationary section.

## Why this is stronger than local closure

The earlier positive-background and Lorentzian signature-class theorems were
still local/operator-family statements:

- choose a background `D`
- choose a source `J`
- solve one exact stationary problem

This note goes further:

- local chart representatives are no longer independent objects
- their overlap compatibility is exact
- the route therefore has a genuine finite-atlas global solution-class theorem

That is the first honest global direct-universal theorem on the branch.

## Honest status

Within the project’s discrete `3+1` Einstein/Regge setting, this is the
strongest direct-universal gravity theorem currently supported:

- exact local operator family
- exact Lorentzian signature-class extension
- exact finite-atlas global stationary closure on `PL S^3 x R`

If one insists on an even stronger claim beyond this, it is no longer a local
operator or atlas-gluing problem. It is a further interpretation step beyond
the exact discrete global theorem already in hand.
