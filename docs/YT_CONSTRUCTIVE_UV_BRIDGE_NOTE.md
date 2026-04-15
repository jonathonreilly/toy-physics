# Constructive UV-Localized Bridge Class for `y_t`

**Date:** 2026-04-15
**Status:** bounded support note
**Primary runner:** `scripts/frontier_yt_constructive_uv_bridge.py`

## Role

This note upgrades the branch from pure exclusions to a real candidate bridge
class.

The previous scans established:

- broad / diffuse bridges fail
- only a narrow UV-localized window is viable
- subleading EW-side deformations do not rescue diffuse bridges

The remaining question was whether that narrow UV-localized window still hides
large shape ambiguity.

## Result

Inside that UV-localized window, the answer is no.

The runner builds three independent endpoint-preserving bridge families:

1. logistic
2. error-function
3. smoothstep

Each family scans the UV-localized window and selects its best fit to the
accepted endpoint `y_t(v)=0.9176`.

All three families land essentially on the same answer:

- each best fit stays within `0.05%` of the accepted endpoint
- the best-fit center fractions lie in the same narrow range
- the best-fit widths lie in the same narrow range
- the normalized bridge area is stable across families

So the accepted endpoint is not an artifact of a single hand-chosen profile.

## Meaning

This gives the branch a constructive candidate bridge class:

> a UV-localized endpoint-preserving bridge family exists, and once the bridge
> is forced into that class, the accepted low-energy endpoint is effectively
> shape-stable.

That is materially stronger than the earlier state, where the branch only knew
how to say what *fails*.

## What remains open

This still does **not** make `y_t` unbounded.

The remaining gap is now sharper:

- not endpoint numerics
- not broad profile ambiguity
- not broad EW-side operator ambiguity

The remaining gap is:

> derive why the exact interacting lattice bridge belongs to this
> UV-localized constructive class.

That is an operator/theorem problem, not a curve-fitting problem.
