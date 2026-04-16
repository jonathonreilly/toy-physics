# `y_t` Bridge Action Invariant Note

**Date:** 2026-04-15
**Status:** bounded support note
**Primary runner:** `scripts/frontier_yt_bridge_action_invariant.py`

## Role

This note reduces the constructive bridge class to a smaller theorem target.

The previous branch state already had:

- diffuse bridges fail
- EW-side freedom does not rescue them
- a constructive UV-localized bridge class exists

The remaining question was whether the viable class is still too functionally
large to be useful.

## Result

It is not.

Inside the viable UV-localized class, the low-energy endpoint is controlled
almost entirely by one functional:

> the normalized gauge-surplus action
> `I_2 = (1/Delta t) ∫ (g_3^2 - g_{3,SM}^2) dt`

The runner shows:

- the endpoint deviation is almost perfectly correlated with `I_2`
- `I_2` is the overwhelmingly dominant control variable for the endpoint; the
  logistic and smoothstep families are strictly monotone in the scan, while the
  erf proxy shows only a few coarse-grid ordering defects
- the viable class also shares a tight UV centroid for the same surplus
- the best rows across shape families collapse into a narrow `I_2` band
- rows within `0.1%` of the accepted endpoint share an especially narrow
  common `I_2` band

So the branch no longer needs to think about the bridge as an arbitrary
function of scale.

## Meaning

The remaining theorem problem is now sharper:

- not “derive the whole bridge profile from scratch”
- but rather “derive why the exact interacting bridge selects the observed
  action invariant and UV centroid”

That is a much smaller target.

## Practical reading

The current package therefore has:

1. a no-go for broad / diffuse bridges
2. a no-go for hiding the problem in broad EW freedom
3. a constructive UV-localized bridge class
4. a quantitative reduction of that class to a dominant bridge action
   invariant
5. near-monotone ordering of the endpoint with that action inside the scanned
   profile families

That is not yet full unbounded closure, but it is a real theorem vector rather
than a loose numerical story.
