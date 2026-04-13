# Exact `O_h`-Symmetric Local Source Class and Strong-Field Residual Floor

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_oh_source_class_scan.py`  
**Status:** Exact local source-class theorem plus bounded residual-floor scan

## Purpose

The previous Codex gravity work had already shown:

- exact source closure for rank-one, finite-support diagonal, and finite-rank
  support operators
- exact `O_h` symmetry inheritance and bounded asymptotic monopole reduction
  for the cubic-symmetric source class
- a nonzero 4D Einstein residual for the direct common-source metric
  candidate, together with a much smaller residual for its monopole/isotropic
  projection

That left one obvious remaining objection:

> maybe the residual is still just an artifact of choosing the wrong local
> cubic-symmetric source law on the support

This note answers that objection directly.

## Exact theorem: the local cubic-symmetric source class is five-plus-two dimensional

Take the star support

`S = {0, ±e_x, ±e_y, ±e_z}`

with induced cubic-group representation on the support basis. Then:

1. the most general real symmetric `O_h`-invariant source operator on `S`
   has dimension `5`
2. the most general `O_h`-invariant bare source vector on `S`
   has dimension `2`
3. the symmetry-adapted decomposition is

   `A1g(center) ⊕ A1g(arms-sum) ⊕ Eg ⊕ T1u`

4. the exact commutant is therefore:
   - one arbitrary symmetric `2x2` block on the two `A1g` sectors
   - one scalar on `Eg`
   - one scalar on `T1u`

The script verifies all of this exactly:

- commutant dimension = `5`
- the explicit five-parameter basis spans the full exact commutant
- invariant bare-source vector space dimension = `2`

So the local static cubic source family is no longer ambiguous.

## Bounded result: scanning the full exact local source class does not close the metric

The script then scans the full exact `O_h` local source class:

- arbitrary positive `2x2` `A1g` block
- arbitrary nonnegative `Eg` and `T1u` eigenvalues
- arbitrary `O_h`-invariant bare source vector

For each admissible source law:

1. compute the exact support-renormalized source
2. compute the exact lattice field
3. rescale to fixed support-scale strong-field amplitude
4. build the direct common-source metric candidate from the same field
5. evaluate the sampled 4D Einstein residual

## What the scan finds

Best result over `162` admissible exact `O_h` source laws:

- best sampled direct-metric residual:

  `max |G_{mu nu}| = 2.98e-2`

- this is materially smaller than the earlier direct finite-rank example
  (`~9.85e-2`)
- but it is still far from theorem-grade vacuum closure

So source-class freedom helps, but it does **not** remove the residual.

## Interpretation

This is a useful negative result.

It means the remaining strong-field gravity gap is **not**:

- “we only tested a point source”
- “we only tested a diagonal support potential”
- “we only tested one arbitrary cubic source law”

Those objections are now gone.

The remaining gravity blocker is sharper:

> even after scanning the full exact local cubic-symmetric source class, the
> direct common-source metric candidate still carries a nonzero 4D vacuum
> residual

So the next problem is no longer source-family ambiguity. It is one of:

1. a near-source matching theorem is missing
2. the correct nonlinear exterior metric law is not the current direct
   common-source ansatz
3. the physical matter source must be coarse-grained / renormalized beyond the
   local static source class before metric closure appears

## What this closes

This closes another real sub-gap:

> the exact local `O_h`-symmetric source family has now been fully classified
> and tested, and source-class freedom alone does not close the strong-field
> metric

## What this does not close

This note does **not** close:

1. the physical many-body source law
2. the near-source matching problem
3. the theorem-grade nonlinear 4D metric
4. full nonlinear GR

## Practical next step

The strongest next Codex move is now:

1. derive a coarse-grained / effective physical source law that lands in a
   narrower exterior-equivalent class than the full local `O_h` family
2. or derive the corrected nonlinear exterior metric law from the same exact
   harmonic field rather than forcing the current direct common-source ansatz
