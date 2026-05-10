# `y_t` Bridge UV Class Uniqueness Note

**Date:** 2026-04-15
**Status:** bounded support note
**Primary runner:** `scripts/frontier_yt_bridge_uv_class_uniqueness.py`

## Role

This note asks the narrowest remaining question after the rearrangement,
moment-closure, Hessian-selector, and correction-control passes:

> if we assume the current support hypotheses already established on the current
> bridge stack, is any acceptable bridge still free to leave the same
> UV-localized class and moment band?

The current support hypotheses are the current support stack, not the theorem itself:

- the accepted endpoint-response kernel is positive on the forced UV window
- the local-Hessian selector is stable and positive on that window
- higher-order local corrections are subleading on the viable family
- nonlocal corrections beyond the affine local model are small

Those hypotheses already narrow the bridge substantially. This note adds a
scanned uniqueness certificate on top of them.

## What was tested

The runner performs a broad scan over the current constructive bridge family
space:

- shapes: logistic, erf, smoothstep
- UV centers from diffuse to UV-localized
- UV widths from broad to narrow

For each candidate it measures:

- physical endpoint `y_t(v)`
- response moment `J_aff`
- UV centroid `c_2`
- nonlocal residual against the accepted affine kernel model

The scan is then filtered by the current support hypotheses and by the endpoint
closeness criterion.

## Result

The scan now certifies a stronger and cleaner result than the earlier
center/width-box read.

What it shows is:

- the current support hypotheses cut the broad family down sharply
- the apparent “outside the UV box” survivors are not truly diffuse; they are
  artifacts of a coarse parametric width cutoff
- every broad-scan survivor still falls inside the same **intrinsic
  UV-centered class**, identified by the response-weighted centroid / moment
  side rather than by an arbitrary `(center, width)` box
- that intrinsic class shares one tight common `J_aff` band and one tight
  `c_2` band

In the present run:

- total scanned candidates: `168`
- preliminary survivors after endpoint/nonlocal filtering: `6`
- higher-order survivors after the local selector check: `6`
- survivors inside the old coarse parametric box: `2`
- survivors outside the old coarse parametric box: `4`
- survivors inside the intrinsic UV-centered class: `6`
- survivors outside the intrinsic class: `0`

So the current package support is stronger than “UV-localized is preferred.”
At the level of the broad scanned constructive family, once the branch
hypotheses are imposed, the survivors are forced into the same intrinsic
UV-centered class/band. The old failure was a box-definition artifact, not a
true diffuse-family escape.

## Honest boundary

This is still **not** a full proof over all exact microscopic bridge
functionals, but it **is** now a broad-family uniqueness certificate inside
the scanned constructive family.

It is a theorem-style certificate inside the currently scanned constructive
family, conditioned on the current support hypotheses from the rearrangement,
moment-closure, Hessian-selector, higher-order, and nonlocal-correction
notes.

The remaining gap is the same microscopic one:

- prove that the exact interacting lattice bridge lies in this scanned class,
  not just in the proxy family
- or derive the class directly from the microscopic operator content

So the current result is best read as:

> the current support hypotheses narrow the scanned bridges to one intrinsic
> UV-centered class with a tight moment band; the remaining gap is no longer
> broad-family diffuse survivors, but the microscopic derivation of that class
> for the exact bridge itself.

## Honest auditor read

The 2026-05-05 audit recorded this row as `audited_conditional` with the
substantive observation that the certificate depends on fixed physical
input constants, an imported target `y_t`, chosen proxy bridge
families, and runner-defined thresholds rather than deriving the class
from the axiom. The note already states above that the result is a
broad-family uniqueness certificate inside the scanned constructive
family, conditioned on the upstream support hypotheses.

This addendum is graph-bookkeeping only. It does not change the
conditional status, does not promote the row, and does not modify the
scan survivor counts or the intrinsic-class identification.

## Audit dependency repair links

This graph-bookkeeping section records the upstream authorities the
support hypotheses cite. It does not promote this note or change the
audited claim scope.

- [YT_CONSTRUCTIVE_UV_BRIDGE_NOTE.md](YT_CONSTRUCTIVE_UV_BRIDGE_NOTE.md)
  for the constructive bridge family the scan filters.
- [YT_BRIDGE_HESSIAN_SELECTOR_NOTE.md](YT_BRIDGE_HESSIAN_SELECTOR_NOTE.md)
  for the leading positive local quadratic selector hypothesis.
- [YT_BRIDGE_HIGHER_ORDER_CORRECTIONS_NOTE.md](YT_BRIDGE_HIGHER_ORDER_CORRECTIONS_NOTE.md)
  for the subleading higher-order hypothesis used as a filter.
- [YT_BRIDGE_NONLOCAL_CORRECTIONS_NOTE.md](YT_BRIDGE_NONLOCAL_CORRECTIONS_NOTE.md)
  for the small-nonlocal-residual hypothesis used as a filter.
- [YT_BRIDGE_REARRANGEMENT_PRINCIPLE_NOTE.md](YT_BRIDGE_REARRANGEMENT_PRINCIPLE_NOTE.md)
  and [YT_BRIDGE_MOMENT_CLOSURE_NOTE.md](YT_BRIDGE_MOMENT_CLOSURE_NOTE.md)
  for the rearrangement and moment-closure inputs that justify the
  `J_aff` / `c_2` band reading.
