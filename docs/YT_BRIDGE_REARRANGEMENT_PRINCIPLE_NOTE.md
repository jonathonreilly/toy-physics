# `y_t` Bridge Rearrangement Principle Note

**Date:** 2026-04-15
**Status:** bounded support note
**Primary runner:** `scripts/frontier_yt_bridge_rearrangement_principle.py`

## Role

This note turns the new UV-localized bridge class from an empirical pattern
into a structural consequence of the endpoint flow.

Before this note, the branch already had:

- a no-go for broad / diffuse bridges
- a no-go for hiding the gap in broad EW-side operator freedom
- a constructive UV-localized bridge class
- a dominant bridge action invariant `I_2`

But one question remained open:

> why should the exact interacting bridge be UV-localized at all, rather than
> some other positive bridge surplus with the same rough integrated size?

## Derivation

Write the accepted downward transport in UV-to-IR time `tau`, so that
`tau = 0` is the UV boundary and `tau = Delta tau` is the physical endpoint.

Linearizing the downward Yukawa flow around the accepted bridge gives

`d(delta y)/d tau = A(tau) delta y + 8 c y_*(tau) delta(g_3^2)(tau)`

for `c = 1 / (16 pi^2)` and the accepted background solution `y_*(tau)`.

Because this is a scalar linear Volterra problem, the endpoint response has the
form

`delta y_t(v) = integral K(tau) delta(g_3^2)(tau) d tau`

with a positive kernel `K(tau)`.

The runner then checks two things on the accepted branch bridge:

1. the kernel is positive everywhere
2. the kernel is monotone increasing toward the IR endpoint

So equal positive surplus inserted earlier in the flow has **less** endpoint
leverage than the same surplus inserted later.

## Result

That gives a real rearrangement principle:

> for a fixed nonnegative bridge-surplus action, the smallest endpoint shift is
> achieved by placing the surplus as far toward the UV as allowed.

The runner verifies this directly by equal-area Gaussian perturbations of
`delta(g_3^2)` centered at different positions along the flow:

- the observed endpoint response is strictly ordered with the perturbation
  center
- UV-centered perturbations give the smallest endpoint shift
- IR-centered perturbations give more than twice the endpoint shift of the
  UV-centered ones for the same added action
- the linear kernel prediction tracks the nonlinear finite perturbations with
  correlation above `0.995`

## Meaning

This is the missing explanation for the earlier locality scans.

The accepted endpoint does not merely *happen* to prefer UV-localized bridges.
Once the bridge surplus is positive, broad or IR-heavy bridges are disfavored
for a structural reason: they carry too much endpoint leverage.

So the branch now has:

1. a no-go for broad bridges
2. a no-go for hiding the gap in broad EW freedom
3. a constructive UV-localized bridge class
4. a dominant bridge action invariant
5. a rearrangement principle explaining why the viable bridge must localize
   near the UV boundary

## What remains open

This still does **not** finish the unbounded theorem.

The remaining target is narrower now:

- not “why UV-localized?”
- but “why this exact UV-localized invariant band and centroid?”

So the remaining gap is no longer generic bridge shape or generic localization.
It is the invariant-selection rule inside the UV-localized class.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [yt_constructive_uv_bridge_note](YT_CONSTRUCTIVE_UV_BRIDGE_NOTE.md)
- [yt_bridge_action_invariant_note](YT_BRIDGE_ACTION_INVARIANT_NOTE.md)
- [yt_ew_coupling_bridge_note](YT_EW_COUPLING_BRIDGE_NOTE.md)
- [yt_exact_interacting_bridge_transport_note](YT_EXACT_INTERACTING_BRIDGE_TRANSPORT_NOTE.md)
