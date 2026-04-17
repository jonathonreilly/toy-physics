# `y_t` Bridge Moment Closure Note

**Date:** 2026-04-15
**Status:** bounded support note
**Primary runner:** `scripts/frontier_yt_bridge_moment_closure.py`

## Role

This note sharpens the remaining YT bridge problem from a profile-selection
 problem to a weighted moment-selection problem.

The branch already had:

- a constructive UV-localized bridge class
- a dominant action invariant `I_2`
- a rearrangement principle explaining why the viable bridge must localize
  toward the UV boundary

The natural next question was:

> once the bridge is forced into that UV-localized window, does the endpoint
> still depend on the whole function shape, or only on a few moments?

## Result

On the accepted branch bridge, the endpoint-response kernel from the
rearrangement derivation is nearly affine on the viable UV-localized window.

That matters because an affine kernel reduces the weighted endpoint response to
two moments of the bridge surplus:

1. `I_2`, the gauge-surplus action
2. `c_2`, the UV centroid of that surplus

Equivalently, the endpoint is controlled by one narrow response-weighted moment
band

`J_aff = I_2 * (a c_2 + b)`

with `a, b` fixed by the accepted response kernel.

## What the runner checks

The runner shows:

- the accepted response kernel is nearly affine on the UV-localized window
- `I_2` still controls the viable class strongly
- near-target rows collapse into a narrow common `J_aff` band
- the best row from each independent shape family also lands in that same
  narrow `J_aff` band
- the near-target `c_2` band remains tight

So even in proxy form, the remaining bridge problem is no longer a free choice
of profile shape.

## Meaning

This is stronger than the earlier invariant note.

Before, the branch could say:

> the endpoint is overwhelmingly controlled by `I_2`

Now it can say:

> on the forced UV-localized window, the endpoint problem closes to a
> two-moment system `(I_2, c_2)`, or equivalently to one narrow
> response-weighted moment band `J_aff`

So the remaining theorem target is narrower again:

- not “which profile works?”
- not even “why UV-localized?”
- but “why does the exact interacting lattice bridge select this weighted
  moment band?”

## Honest boundary

This still does **not** finish the unbounded theorem.

The weighted moment band is derived only on the current constructive proxy
class, not yet from a full microscopic operator theorem.

But it means the residual gap is now a moment-selection rule rather than a
profile-selection problem.
