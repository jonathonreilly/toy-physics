# Scalar-Trace-Only Tensor Completion No-Go

**Date:** 2026-04-14  
**Script:** `scripts/frontier_scalar_trace_tensor_nogo.py`  
**Status:** exact scalar-data degeneracy plus bounded tensor-channel witness

## Purpose

The current gravity branch already has a real restricted strong-field package:

- exact shell source
- exact same-charge bridge
- exact local static-conformal lift
- exact microscopic Schur boundary action
- exact microscopic Dirichlet principle
- exact restricted discrete Einstein/Regge lift

The remaining gap is no longer “find a better scalar bridge.” The real
question is narrower:

> can any completion principle that depends only on the current scalar shell
> trace / Schur boundary data determine the full `3+1` metric?

This note answers that sharply.

## Exact statement

On the current branch, the microscopic boundary functional is scalar:

- it depends only on the shell trace `f`
- equivalently, only on the Schur-complement scalar boundary data

The tensorial completion probes already added on the branch keep that scalar
boundary data fixed by construction while turning on:

- a shift-vector mode
- a traceless spatial shear mode
- a mixed vector+tensor mode

Therefore any purported completion principle that factors only through the
current scalar shell trace / Schur data must assign the same output to all of
those probes.

That is the exact degeneracy.

## Tensorial witness

The companion verifier evaluates the full 4D Einstein tensor on those probes.

Result:

- the scalar boundary action is unchanged across the scalar, vector, tensor,
  and mixed perturbations on both the exact local `O_h` and finite-rank
  source classes
- but the tensorial Einstein channels are not unchanged
  - vector perturbations activate independent `G_{0i}` residuals
  - traceless shear perturbations activate independent traceless
    `G_{ij}` residuals
  - mixed perturbations activate both

So the scalar data are insufficient to determine the full `3+1` metric.

## Why this is a no-go theorem

This is not just a bounded “the scalar bridge is incomplete” statement.

It is a genuine no-go for a whole class of hoped-for completions:

> no completion principle that factors only through the current scalar shell
> trace / Schur boundary data can determine the full 4D metric on this branch.

Equivalently:

> the remaining gravity gap cannot be closed by another scalar repackaging of
> the existing microscopic boundary action.

The next principle, if it exists, must be genuinely tensor-valued.

## What this closes

This closes one more tempting escape hatch:

1. the gravity gap is **not** hidden inside another scalar bridge channel
2. the gravity gap is **not** hidden inside the current scalar shell action
3. the gravity gap is **not** merely a better scalar completion of the same
   shell data

## What still remains open

This still does **not** close:

1. a genuinely tensor-valued microscopic matching / completion law
2. full nonlinear GR in full generality

## Practical conclusion

The gravity search space is now much tighter:

- restricted strong-field closure is real
- restricted Einstein/Regge lift is real
- broader support-class widening is real
- scalar-only completion is now sharply ruled out

So the only honest positive route left is a new tensor-valued matching law
beyond the current scalar shell data.
