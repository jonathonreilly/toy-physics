# Tensor Source-to-Channel Map `eta` on the Restricted Gravity Class

**Date:** 2026-04-14  
**Script:** `scripts/frontier_tensor_source_map_eta.py`  
**Status:** exact rank-two source response on the current restricted class; not full nonlinear GR

## Purpose

The retained gravity stack already forces a sharp split:

- the scalar shell trace / Schur boundary data are exact on the current class
- scalar-only completion is ruled out
- the first tensor correction exists but does not close the bridge gap

So the remaining microscopic object is not another scalar shell law. It is the
smallest tensor-valued source-to-channel map that feeds the non-scalar Einstein
sectors.

Here `eta` denotes the restricted Jacobian from microscopic tensor source drives
into the two non-scalar boundary channels:

- shift-like vector channel `G_0i`
- traceless spatial-shear channel `G_ij^TF`

## Definition on the retained class

Use the already-audited scalar bridge as the base point, then turn on the two
minimal microscopic tensor probes:

- a shift-like vector source drive `eps_vec`
- a traceless shear source drive `eps_tf`

The restricted source-to-channel map is the `2 x 2` Jacobian

`eta = d( G_0i , G_ij^TF ) / d( eps_vec , eps_tf )`

evaluated on the scalar bridge for the current restricted source class.

This is the smallest tensor completion compatible with the branch evidence.

## Exact constrained result

The scalar Schur boundary action is unchanged under the tensor probes on both
tested restricted classes:

- exact local `O_h`
- broader exact finite-rank

That means the tensor response really sits beyond the scalar shell trace.

On the same restricted classes, the non-scalar Einstein channels respond with
an exact rank-two source map:

`eta_O_h =
[[4.442009e-03, 1.004149e-03],
 [0.000000e+00, 3.666789e-02]]`

`eta_finite_rank =
[[4.049376e-03, 2.465364e-04],
 [2.544108e-10, 4.973095e-02]]`

Interpretation:

- the vector source drive produces a clean `G_0i` response
- the tensor source drive produces a clean `G_ij^TF` response
- the tensor source also leaks into `G_0i`, but only at the `10^-3` to
  `10^-4` level on this restricted class
- the vector source leaks into `G_ij^TF` only at the `10^-10` level on the
  finite-rank class and vanishes on the exact `O_h` class

So the tensor source map is not scalar-degenerate, and it is not a single
channel. It is the minimal rank-two source block required by the current
restricted gravity data.

## Linear response consistency

The mixed vector+tensor probe is locally additive in the two channel
directions on both restricted families:

- exact local `O_h`
  - `dG_0i` additivity error: `3.059e-08`
  - `dG_ij^TF` additivity error: `8.023e-18`
- finite-rank
  - `dG_0i` additivity error: `6.850e-08`
  - `dG_ij^TF` additivity error: `6.191e-11`

That makes `eta` a well-defined local Jacobian on the retained probe family,
not just a qualitative statement about "some tensor correction."

## What this closes

This closes the last ambiguity in the microscopic tensor source question:

> the retained strong-field package requires at least two non-scalar boundary
> coordinates, and the corresponding source-to-channel map is rank-two on the
> audited restricted class.

The scalar shell trace alone is insufficient, but the new tensor source block
is now explicitly constrained.

## What remains open

This still does **not** close:

1. the microscopic derivation of the tensor kernel `K_tensor`
2. extension beyond the audited restricted class
3. full nonlinear GR in full generality

## Practical conclusion

The remaining gravity problem is now narrowed to one concrete operator family:

> derive the microscopic tensor source map `eta` and the matching tensor
> boundary kernel on top of the exact scalar shell action.

The scalar bridge is no longer the missing object.
