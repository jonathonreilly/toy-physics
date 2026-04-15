# Lambda from Representation Matching

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Scope:** lambda from the exact weight-1 lift family `L_lambda` under the residual `SO(2)` phase orbit

## Verdict

The current atlas does **not** canonically fix `lambda`.

Starting from the exact support-side dark phase and the universal
weight decomposition, the representation-theoretic matching problem leaves a
genuine multiplicity-space freedom. After the overall scale is normalized,
the surviving ambiguity is exactly the one-parameter family

`L_lambda(D) = (cos(lambda) D, sin(lambda) D)`.

So the exact answer is:

> the current atlas fixes the core decomposition and the residual `SO(2)`
> action, but it does not choose a canonical point in the weight-1
> multiplicity circle.

## Exact input

The starting data are already exact:

`D_R(q) = (d_y, d_z)`,

`rho_R = ||D_R||`,

`vartheta_R = atan2(d_z, d_y)`.

The support phase transforms under the residual connected dark-plane
`SO(2)`.

On the universal side, the shared-axis decomposition already isolates:

- the exact invariant core `Pi_A1`;
- the exact weight-1 universal doublets;
- the remaining weight-2 shear block.

So the only possible canonical lift target for the support dark phase is the
direct sum of the two universal weight-1 doublets.

## Representation-theoretic matching

Let the source representation be the standard weight-1 `SO(2)` doublet:

`rho_src(theta) = R(theta)`.

Let the target representation be the direct sum of two identical weight-1
doublets:

`rho_tgt(theta) = diag(R(theta), R(theta))`.

Then an exact equivariant lift is any linear map `L` satisfying

`rho_tgt(theta) L = L rho_src(theta)`.

In the raw real basis, the intertwiner space is 4-dimensional. That is
already too much freedom to pick a canonical lift from representation theory
alone.

After the atlas' bright-axis and phase conventions select the standard
weight-1 basis on the source and on each universal target doublet, the
remaining normalized section is exactly the one-parameter family

`L_lambda(D) = (cos(lambda) D, sin(lambda) D)`.

So the representation-theoretic matching does not fix `lambda`; it leaves a
circle of normalized lifts once the canonical basis choices are imposed.

## Normalization conventions

Normalization removes only the overall scale.

For the normalized lift family,

`||L_lambda(D)|| = ||D||`,

so the norm constraint does not determine `lambda`.

Equivalently, the multiplicity-space rotation

`M(phi) L_lambda = L_(lambda + phi)`

shows that `lambda` is just the coordinate of a residual `SO(2)` choice in the
target multiplicity space.

## Compatibility with `Pi_A1`

`Pi_A1` is exact and canonical, but it only fixes the invariant core:

`Pi_A1 = diag(1,0,0,0,1,0,0,0,0,0)`.

That projector does not act on the weight-1 multiplicity space that carries
`lambda`.

So `Pi_A1` fixes the core decomposition but does not pick a canonical
`lambda`.

## Compatibility with the shared bright axis

The shared bright axis fixes the residual connected gauge down to `SO(2)`.
That is enough to identify the phase orbit and the weight-1 target sectors,
but not enough to choose an origin in the weight-1 multiplicity circle.

So bright-axis compatibility also fails to canonically fix `lambda`.

## Exact conclusion

The current atlas proves three things:

1. the support phase is exact;
2. the universal target contains the correct weight-1 sectors;
3. the equivariant lift space is a normalized one-parameter family.

Therefore the exact one-parameter family survives:

`L_lambda(D) = (cos(lambda) D, sin(lambda) D)`.

No representation-theoretic matching, normalization convention, or
`Pi_A1`/bright-axis compatibility condition in the current atlas selects a
canonical `lambda`.

## Bottom line

The best exact statement supported by the current atlas is not a canonical
lambda theorem. It is a survival theorem:

> the weight-1 lift family remains exactly one-parameter after all currently
> available matching, normalization, and `Pi_A1` compatibility constraints.
