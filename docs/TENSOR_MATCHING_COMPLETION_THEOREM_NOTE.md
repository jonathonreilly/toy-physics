# Minimal Tensor Matching/Completion Theorem on the Retained Gravity Stack

**Date:** 2026-04-14  
**Script:** `scripts/frontier_tensor_matching_completion_theorem.py`  
**Status:** exact localization of the minimal tensor boundary data on the current restricted class

## Purpose

This note treats the gravity problem on the strongest retained surface already
present on the branch, not as a narrow local patch:

- `Cl(3)` on `Z^3` is the working axiom
- anomaly/selector closure already organizes the framework as `3+1`
- the shell/junction law is already exact on the current restricted class
- the microscopic Schur/Dirichlet boundary action is already exact
- the restricted discrete Einstein/Regge lift is already exact
- scalar-only completion is already ruled out

So the remaining question is narrower:

> what is the smallest genuinely tensor-valued boundary data required to extend
> the current scalar shell trace / Schur data toward a full `3+1` completion?

## What the retained stack already forces

The broader retained stack removes several fake degrees of freedom:

1. the completion data must be **shell-local** on the current bridge surface,
   because the restricted lift is already a stationary shell action
2. the completion data must be **observable-level boundary data**, not another
   bulk reparameterization, because the scalar shell trace is already the exact
   boundary observable extracted by the Schur/Dirichlet machinery
3. the completion must respect the already-retained `3+1` split, so the new
   channels must live in the non-scalar lapse/shift/spatial-tensor sector
4. the completion must reduce to the exact scalar package when those new
   channels vanish

That means the missing principle is not an arbitrary new metric ansatz. It must
be a tensor-valued extension of the current shell observable package.

## Exact theorem

On the current restricted probe family already on the branch:

- scalar bridge
- vector shift perturbation
- traceless-shear perturbation
- mixed vector+tensor perturbation

the exact microscopic scalar Schur boundary action is unchanged across all four
probes on both:

- the exact local `O_h` class
- the broader finite-rank class

At the same time:

- the vector perturbation activates an independent `G_{0i}` channel
- the traceless-shear perturbation activates an independent traceless
  `G_{ij}` channel

Therefore the full tensor completion cannot live in the current scalar shell
trace alone. At least **two** additional non-scalar boundary coordinates are
required on the retained restricted class:

1. one shift-like / vector boundary coordinate
2. one traceless-shear boundary coordinate

That lower bound is exact on the current branch.

## Bounded local sufficiency result

The companion verifier then checks the mixed perturbation.

Result:

- on the exact local `O_h` class, the mixed probe is locally additive in the
  two non-scalar channel deltas with errors
  - `dG_0i`: `3.059e-08`
  - `dG_TF`: `8.023e-18`
- on the finite-rank class, the same additivity persists with errors
  - `dG_0i`: `6.850e-08`
  - `dG_TF`: `6.191e-11`

So on the currently audited restricted family, the smallest tensor extension
that closes the tested tangent directions is:

- the exact scalar Schur data
- plus one shift-like tensor coordinate
- plus one traceless-shear tensor coordinate

This is not yet a full GR theorem, because the branch still lacks the
microscopic source-to-channel map and the tensor boundary kernel itself.

## Minimal tensor boundary action forced by the retained stack

The retained shell-action picture now forces the missing object into one narrow
form.

The smallest possible tensor extension compatible with the current stack is a
shell-local quadratic action

`I_tensor(f, a_vec, a_tf ; j, eta) = I_scalar(f ; j)
  + 1/2 [a_vec, a_tf] K_tensor [a_vec, a_tf]^T - eta^T [a_vec, a_tf]`

with:

- `f` the already-exact scalar shell trace
- `a_vec` the shift-like tensor boundary coordinate
- `a_tf` the traceless-shear boundary coordinate
- `K_tensor` a symmetric positive-definite `2 x 2` tensor boundary kernel
- `eta` the microscopic source-to-tensor-channel drive

Everything except `K_tensor` and `eta` is already forced by the retained stack.

## What this closes

This closes the ambiguity in the remaining gravity search space.

The missing gravity principle is no longer:

- a better scalar bridge
- a better scalar shell action
- a more clever static conformal ansatz
- an unspecified “tensor correction”

It is specifically:

> derive the microscopic source-to-`(a_vec, a_tf)` map and the tensor boundary
> kernel `K_tensor` on the current restricted class.

## What remains open

This still does **not** close:

1. the microscopic derivation of `eta`
2. the microscopic derivation of `K_tensor`
3. extension beyond the currently audited restricted class
4. full nonlinear GR in full generality

## Practical conclusion

The positive path to gravity closure is now exact enough to state cleanly:

- the retained stack already forces a shell-local tensor boundary extension
- the missing data are minimally rank-two beyond the scalar shell trace
- the only honest remaining theorem family is the derivation of the tensor
  source map and tensor boundary kernel

That is much tighter than the previous generic “find a tensor completion”
framing.
