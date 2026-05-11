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

## Honest auditor read

The 2026-05-05 audit recorded this row as `audited_numerical_match` with
the substantive observation that the runner performs a real numerical
scan rather than printing constants, but the load-bearing result depends
on hard-coded physical inputs, a selected constructive bridge ansatz, a
target endpoint, and finite profile-family scans rather than a
first-principles derivation from the stated axiom. The note already
frames the remaining theorem target above as deriving why the exact
interacting bridge selects the observed action invariant and UV centroid;
the audited claim here is a numerical reduction inside the scanned
families, not closure.

This addendum is graph-bookkeeping only. It does not change the
numerical match status, does not promote the row, and does not modify
the action-invariant correlation results or their bounded scope.

## Audit dependency repair links

This graph-bookkeeping section records the upstream notes the runner
and bridge stack depend on, so the audit citation graph can track them.
It does not promote this note or change the audited claim scope.

- [YT_INTERACTING_BRIDGE_LOCALITY_NOTE.md](YT_INTERACTING_BRIDGE_LOCALITY_NOTE.md)
  for the forced UV-localized class premise.
- [YT_CONSTRUCTIVE_UV_BRIDGE_NOTE.md](YT_CONSTRUCTIVE_UV_BRIDGE_NOTE.md)
  for the constructive UV-localized bridge family the action scan deforms.
- [YT_BRIDGE_REARRANGEMENT_PRINCIPLE_NOTE.md](YT_BRIDGE_REARRANGEMENT_PRINCIPLE_NOTE.md)
  for the rearrangement step that pushes the surplus toward the UV.
- [YT_BRIDGE_OPERATOR_CLOSURE_NOTE.md](YT_BRIDGE_OPERATOR_CLOSURE_NOTE.md)
  for the EW-side scan that excludes diffuse rescues.
- [YT_BOUNDARY_THEOREM.md](YT_BOUNDARY_THEOREM.md)
  for the v boundary used as the IR endpoint reference.
