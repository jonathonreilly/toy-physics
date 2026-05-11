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

## Honest auditor read

The 2026-05-04 audit recorded this row as `audited_numerical_match`. The
honest read is that the runner's three-family scan is a numerical match
within a tuned constructive class against the imported physical endpoint
`y_t(v) = 0.9176`, not a first-principles derivation that the exact
interacting lattice bridge belongs to the UV-localized class. The note
already states the remaining derivation gap explicitly above.

This addendum is graph-bookkeeping only. It does not change the
numerical match status, does not promote the row, and does not add new
content to the constructive-class result.

## Audit dependency repair links

This graph-bookkeeping section records the upstream notes the runner
and bridge stack depend on, so the audit citation graph can track them.
It does not promote this note or change the audited claim scope.

- [YT_INTERACTING_BRIDGE_LOCALITY_NOTE.md](YT_INTERACTING_BRIDGE_LOCALITY_NOTE.md)
- [YT_BRIDGE_OPERATOR_CLOSURE_NOTE.md](YT_BRIDGE_OPERATOR_CLOSURE_NOTE.md)
- `YT_BRIDGE_REARRANGEMENT_PRINCIPLE_NOTE.md` (see-also cross-reference,
  not a load-bearing dependency — backticked to break cycle-0005 in the
  citation graph. The rearrangement note explains the UV-localization
  structurally and is downstream of this constructive-class note; this
  note's three-family endpoint-stability runner does not consume the
  rearrangement-kernel result, so the dependency arrow runs from
  rearrangement back to this note, not vice versa.)
- `YT_BOUNDARY_THEOREM.md` (see-also cross-reference, not a load-bearing
  dependency — backticked to break the residual yt cluster cycle in the
  citation graph. The boundary theorem establishes that `v` is the
  physical crossover endpoint; this constructive bridge note's
  three-family runner targets that endpoint empirically but does not
  consume the boundary theorem's domain-separation proof as a logical
  premise of the three-family endpoint-stability result.)
