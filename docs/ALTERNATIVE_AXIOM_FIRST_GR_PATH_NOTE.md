# Alternative Axiom-First GR Path After the `A1` Blindness Result

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Status:** architecture verdict

## Verdict

There **is** a cleaner axiom-first path than continuing to treat
`eta_floor_tf` as the primitive object.

The current tensor-boundary-drive program was useful for localization, but the
new exact blindness result changes the architecture:

- the retained shell/junction stack is exact
- that same stack is projectively blind to the remaining `A1` shape ratio
- the current `eta_floor_tf` observable is still numerical

So the last theorem should not be attacked as:

- “derive the scalar renormalization law of `eta_floor_tf` from shell data”

That route is now blocked.

## Best cleaner path

The best alternative is a **microscopic support-block derivation**.

### Theorem sequence

1. **Exact support reduction**
   - use the exact star-support decomposition
     - `A1(center) ⊕ A1(shell) ⊕ E ⊕ T1`
   - reduce the scalar background to the exact `2 x 2` `A1` block

2. **Exact shell-blindness theorem**
   - prove the current shell/junction stack factors the `A1` background only
     through total charge `Q`
   - this is now done in
     [TENSOR_A1_SHELL_PROJECTIVE_BLINDNESS_NOTE.md](./TENSOR_A1_SHELL_PROJECTIVE_BLINDNESS_NOTE.md)

3. **Support-side mixed response operator**
   - derive the exact microscopic mixed operator on
     - scalar background block `A1`
     - bright non-scalar channels `{E_x, T1x}`
   - this is the first place the missing projective datum `r = s/e0` can
     survive honestly

4. **Exact tensor boundary observable**
   - derive the tensor observable from that support-side operator
   - not from the current sampled Einstein-residual quantity
   - the right target is an exact support/block coefficient or exact Schur /
     Dirichlet Hessian dual to the tensor channels

5. **Tensor boundary action / completion**
   - once that exact observable is in hand, derive the tensor boundary action
   - then close the restricted tensor completion theorem on the current class

## Why this is cleaner

This route is cleaner than the current `eta_floor_tf` program because:

1. it starts from the axiom-side microscopic support block, not from a
   downstream numerical diagnostic
2. it avoids trying to extract `r` from shell data that provably cannot see it
3. it aligns with the atlas pattern that successful retained derivations close
   by exact symmetry reduction to the minimal invariant block

## What this means for the current route

The current route was still useful.

It already established:

- scalar-only completion fails
- the tensor gap is rank-two
- the active directions are exactly `E_x` and `T1x`

So it localized the problem correctly.

But after the new blindness theorem, it is no longer the cleanest primitive for
closure.

## Practical conclusion

The best alternative path is now:

> derive the exact support-side mixed response operator on
> `A1 x {E_x, T1x}`, then derive the tensor boundary observable from that
> operator, and only then close the tensor boundary action.

If gravity closes from the axiom on the current restricted class, this is the
most credible route.
