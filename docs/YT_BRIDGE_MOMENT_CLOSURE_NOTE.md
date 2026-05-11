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

## Honest auditor read

The 2026-05-05 audit recorded this row as `audited_numerical_match` with
the substantive observation that the runner performs real computation
but uses a calibrated proxy scan with hard-coded physical inputs, target
value, accepted logistic bridge, UV window, and pass thresholds. The
load-bearing claim is a numerical proxy match on the selected inputs
rather than a closed first-principles theorem; the note already calls
itself bounded support above. The honest read is that the moment-band
collapse `J_aff` is verified within the scanned family, not derived from
the axiom.

This addendum is graph-bookkeeping only. It does not change the
numerical match status, does not promote the row, and does not modify
the moment-band fit results or their bounded scope.

## Audit dependency repair links

This graph-bookkeeping section records the upstream notes the
moment-closure result reuses. It does not promote this note or change
the audited claim scope.

- [YT_INTERACTING_BRIDGE_LOCALITY_NOTE.md](YT_INTERACTING_BRIDGE_LOCALITY_NOTE.md)
  for the forced UV-localized class premise.
- [YT_CONSTRUCTIVE_UV_BRIDGE_NOTE.md](YT_CONSTRUCTIVE_UV_BRIDGE_NOTE.md)
  for the constructive UV-localized bridge family the kernel reuses.
- [YT_BRIDGE_REARRANGEMENT_PRINCIPLE_NOTE.md](YT_BRIDGE_REARRANGEMENT_PRINCIPLE_NOTE.md)
  for the rearrangement derivation of the endpoint-response kernel.
- [YT_BRIDGE_ACTION_INVARIANT_NOTE.md](YT_BRIDGE_ACTION_INVARIANT_NOTE.md)
  for the dominant `I_2` invariant the moment closure refines into a
  two-moment system `(I_2, c_2)`.
- [YT_BOUNDARY_THEOREM.md](YT_BOUNDARY_THEOREM.md)
  for the v boundary used as the IR endpoint reference.
