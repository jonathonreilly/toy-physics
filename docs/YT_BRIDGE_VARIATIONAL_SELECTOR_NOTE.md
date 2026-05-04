# `y_t` Bridge Variational Selector Note

**Date:** 2026-04-15
**Status:** bounded support note
**Primary runner:** `scripts/frontier_yt_bridge_variational_selector.py`

## Role

This note turns the weighted-moment reduction into a concrete conditional
selector.

The branch already had:

- a forced UV-localized bridge class
- a narrow weighted-moment band

The natural next question was:

> if the microscopic bridge selector is local and positive on that forced UV
> window, what does it actually select?

## Conditional derivation

Assume the bridge selector on the UV window is a positive local quadratic
action on the bridge surplus.

Then minimizing that quadratic action at fixed endpoint moment is a standard
Lagrange-multiplier problem. On the same UV window where the accepted response
kernel is nearly affine, the unique minimizer is proportional to the affine
response kernel.

So this no longer leaves an arbitrary family of admissible bridge shapes:

> the local quadratic selector picks one explicit minimizer.

## Result

The runner compares that selector against the empirically best rows from the
three constructive shape families.

It finds:

- the affine-kernel selector uses the same `J_aff` band as the best-family rows
- the selector sits immediately adjacent to the best-family `I_2` band at the
  same scale
- the selector lands inside the best-family `c_2` band
- sampled constraint-preserving perturbations all increase the quadratic action

So the branch no longer needs to think about the residual YT problem as
profile freedom at all.

## Meaning

This is still **conditional**.

It does **not** prove that the exact microscopic lattice bridge already comes
from that positive local quadratic selector.

What it does show is narrower and useful:

> if the microscopic completion supplies a positive local quadratic selector on
> the forced UV window, then the selector is already fixed and it matches the
> observed best-family bridge band.

That means the remaining theorem target is now:

- not “which bridge profile?”
- not “which weighted moment band?”
- but “why does the exact interacting lattice bridge induce this positive local
  quadratic selector?”

## Honest boundary

So the branch is still not fully unbounded.

But the residual gap has been compressed again, from a weighted moment rule to
the microscopic origin of one concrete variational selector.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [yt_bridge_moment_closure_note](YT_BRIDGE_MOMENT_CLOSURE_NOTE.md)
- [yt_bridge_hessian_selector_note](YT_BRIDGE_HESSIAN_SELECTOR_NOTE.md)
- [yt_constructive_uv_bridge_note](YT_CONSTRUCTIVE_UV_BRIDGE_NOTE.md)
- [yt_exact_interacting_bridge_transport_note](YT_EXACT_INTERACTING_BRIDGE_TRANSPORT_NOTE.md)
