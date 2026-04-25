# Review: `lorentz-boost-covariance`

Date: 2026-04-25
Reviewed branch tip: `6e90d030`
Reviewer verdict: **not approved as-is for `main`**

## Summary

This branch contains a scientifically good **selective subset** and one
non-landable overreach.

The good subset has already been landed separately on `main` in the correct
form:

- `LORENTZ_BOOST_COVARIANCE_2D_THEOREM_NOTE.md`
- `LORENTZ_BOOST_COVARIANCE_3PLUS1D_THEOREM_NOTE.md`
- `ANGULAR_KERNEL_UNDERDETERMINATION_NO_GO_NOTE.md`

with the angular-kernel note landed conservatively as:

- bounded no-go on the directional-measure kernel
- retained routing clarification/support note for the boost-covariance lane

The part that is **not** approved is the Phase 5 positive kernel closure.

## Blocking findings

### 1. Phase 5 positive closure is a new primitive extension, not a retained consequence

File:
`docs/LORENTZ_KERNEL_POSITIVE_CLOSURE_NOTE.md`

The load-bearing move is not a consequence of the current retained stack.
The note explicitly upgrades the lane by **adopting new primitives**
`(P5a)-(P5d)` and then treats the resulting kernel closure as retained.
That is a proposal for a stronger primitive surface, not a retained theorem
on the already-accepted one.

So the current theorem status is overstated. At best, this is:

- a proposal note on a new primitive surface, or
- a bounded support note showing that the canonical kernel is compatible with
  the proposed primitive package

It is **not** a retained closure on the current stack.

### 2. The Phase 5 runner hard-codes the uniqueness certification

File:
`scripts/frontier_lorentz_kernel_positive_closure.py`

The load-bearing uniqueness step is not actually verified. The runner reaches
the claimed unique kernel by an unconditional `True` check:

- `check("Uniqueness: K̃(p) = exp(-i a E_lat(p)) is the unique solution", True, ...)`

So the replay only certifies:

- the canonical kernel is unitary,
- it matches the proposed continuum limit,
- the directional-measure examples are non-unitary,

but **not**:

- that `(P5a)-(P5d)` force uniqueness, or
- that the canonical kernel is the only admissible solution.

Until that step is replaced by a real derivation / verifier, the Phase 5
closure cannot be accepted as theorem-grade science.

## What is approved

The following science is solid and already landed on `main`:

1. 1+1D continuum-limit SO(1,1) boost covariance of the free-scalar 2-point
   function
2. 3+1D continuum-limit SO(3,1) boost covariance of the free-scalar 2-point
   function
3. the angular-kernel underdetermination no-go plus the routing clarification
   that the retained boost-covariance lane lives on the fixed
   staggered/Laplacian carrier and does not require a derivation of the
   empirical directional-measure kernel

These were landed selectively because they replay cleanly and do not depend on
the unsafe Phase 5 uniqueness upgrade.

## Required next step for this branch

If the worker wants to continue Phase 5 on this branch, the task is now
precise:

1. Either **derive uniqueness from an already-retained primitive stack**, or
2. explicitly **downgrade the note** to a proposal/new-primitive-surface note,
   and stop presenting it as retained closure.

And in either case:

3. replace the hard-coded uniqueness `True` check with an actual proof-grade
   verifier, or reduce the runner claim to what it really certifies

## Clean status call

- full branch as submitted: **reject**
- selective subset: **already accepted and landed on `main`**
- remaining worker task: **Phase 5 only**
