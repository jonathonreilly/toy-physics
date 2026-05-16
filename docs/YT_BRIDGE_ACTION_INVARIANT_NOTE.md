# `y_t` Bridge Action Invariant Note

**Date:** 2026-04-15 (demoted 2026-05-16)
**Claim type:** bounded_theorem
**Status:** bounded numerical-match scan (target-conditioned correlation across selected profile families)
**Audit class:** G — load-bearing step is a target-conditioned numerical scan, not a derivation
**Primary runner:** `scripts/frontier_yt_bridge_action_invariant.py`

## Scope (honest framing)

This note is **not** a derivation that the low-energy endpoint is structurally
controlled by the normalized gauge-surplus action `I_2`. It is a bounded
*target-conditioned numerical scan*: given the imported physical endpoint
`y_t(v) = 0.9176`, a chosen SM-like reference transport, a chosen lattice-side
UV bridge profile, and three pre-selected endpoint-preserving profile families
(logistic, error-function, smoothstep), the runner scans
`(center_frac, width_frac)` on a fixed grid inside a pre-selected UV-localized
window and reports the correlation between the normalized gauge-surplus action
`I_2` and the endpoint deviation across profiles retained inside
`|dev| < 0.5%`.

Five load-bearing inputs are imported, not derived inside this note:

1. the physical target `y_t(v) = 0.9176`,
2. the SM-like reference transport anchored at the low-energy strong coupling
   (one-loop QCD beta), used as the `g_3,SM` reference in the `I_2`
   definition,
3. the constructive lattice-side UV bridge profile the family deforms toward,
4. the three pre-selected smooth profile families parameterized by
   `(center_frac, width_frac)`, and
5. the `|dev| < 0.5%` retention cut that selects the "viable class" the
   correlation is reported on.

The runner's PASS rows
(`1a–1f`) — including `corr(I_2, dev) = +0.999889`, `centroid_2` band
`0.978 +/- 0.004`, family-wise `I_2` monotonicity violations
`{logistic: 0, erf: 3, smoothstep: 0}`, and the top-10 `I_2` band width
`0.000357` — are therefore statements about *these scanned profile families
inside this pre-selected UV-localized window against this imported target*,
not statements that the exact interacting lattice bridge is forced to be
controlled by `I_2` or to land in this UV centroid band.

This is therefore an `audited_numerical_match` / class-G proxy in the
project's audit taxonomy, not a closed first-principles derivation. The
remaining structural gaps are recorded below in "What remains open".

## Previous-scan context (informational)

Earlier YT-cluster scans established (under the same imported endpoint and
the same SM-like reference transport):

- broad / diffuse bridges fail to reproduce the imported endpoint
  (`YT_INTERACTING_BRIDGE_LOCALITY_NOTE.md`)
- only a narrow UV-localized window admits any fit
  (`YT_INTERACTING_BRIDGE_LOCALITY_NOTE.md`)
- subleading EW-side deformations do not rescue diffuse bridges
  (`YT_BRIDGE_OPERATOR_CLOSURE_NOTE.md`)
- three endpoint-preserving profile families tuned inside the pre-selected
  UV-localized window agree on the imported endpoint with cross-family
  spread `<= 0.0252%` (`YT_CONSTRUCTIVE_UV_BRIDGE_NOTE.md`)

All four of those upstream notes have been honestly framed as
target-conditioned numerical proxies; this note does not re-derive them. This
note's scan is downstream of them and conditions on the same UV-localized
window.

A structurally consistent reason to expect monotonic endpoint response to
positive bridge surplus on the accepted background is recorded separately in
`YT_BRIDGE_REARRANGEMENT_PRINCIPLE_NOTE.md`: the linearized endpoint-response
kernel is positive and monotone increasing toward the IR, so equal-area
surplus near the UV gives the smallest endpoint response. That rearrangement
statement is itself conditioned on the same accepted background and on
positivity of the bridge surplus; it is not a derivation that the exact
interacting bridge is controlled by `I_2`. The rearrangement note and this
note are mutually supporting target-conditioned proxies, not a joint
derivation.

## Numerical result

Against the imported target `y_t(v) = 0.9176`, scanning
`center_frac in linspace(0.955, 0.985, 7)` and
`width_frac in linspace(0.012, 0.026, 8)` for each of the three profile
families and retaining only `|dev| < 0.5%`, the runner reports:

- `83` profiles retained inside the `|dev| < 0.5%` viable class,
- `corr(I_2, dev) = +0.999889` on the retained class,
- viable-class `I_2` coefficient of variation `11.78%`,
- viable-class `centroid_2` band `0.978185 +/- 0.004250`,
- top-10 `I_2` band width `0.000357`,
- `|dev| < 0.1%` `I_2` band width `0.002059`,
- per-family `I_2` monotonicity violations
  `{logistic: 0, erf: 3, smoothstep: 0}`.

The honest interpretation is that, **conditional on** the imported endpoint
target, **conditional on** the chosen SM-like reference transport,
**conditional on** the chosen lattice-side UV bridge profile,
**conditional on** the three pre-selected profile families, and
**conditional on** the `|dev| < 0.5%` retention cut, the endpoint deviation
inside this retained class is tightly correlated with `I_2` and the retained
class shares a narrow UV centroid.

It does **not** establish that the exact interacting lattice bridge is
controlled by `I_2`, that `I_2` and the UV centroid are uniquely selected by
any axiom in the framework, or that the three scanned profile families
fairly sample the admissible bridge class outside the pre-selected
UV-localized window.

## Meaning (bounded)

The bounded claim this note licenses is narrow:

> *Conditional on* the imported endpoint `y_t(v) = 0.9176`,
> *conditional on* the chosen SM-like reference transport and lattice-side UV
> bridge profile, *conditional on* the three pre-selected endpoint-preserving
> profile families
> (logistic, error-function, smoothstep) parameterized by
> `(center_frac, width_frac)` on the scanned grid, and
> *conditional on* the `|dev| < 0.5%` retention cut, the normalized
> gauge-surplus action `I_2` is tightly correlated with endpoint deviation
> (`corr = +0.999889`), the retained class shares a tight UV centroid
> (`centroid_2 = 0.978 +/- 0.004`), and per-family ordering in `I_2` is
> nearly monotone (`{logistic: 0, erf: 3, smoothstep: 0}` violations).

It does **not** establish:

- that the exact interacting lattice bridge is controlled by `I_2`,
- that the UV centroid band is uniquely selected by any axiom in the
  framework,
- that `I_2` is the structurally correct invariant (rather than a convenient
  functional that happens to dominate inside this scanned family), or
- that the bridge action invariant follows from the framework axioms.

## What remains open (load-bearing gaps)

To upgrade this row from `audited_numerical_match` to a clean derivation,
the following structural gaps must be closed, none of which the present
runner addresses:

1. derive the endpoint `y_t(v) = 0.9176` from the framework axioms rather
   than importing it as the comparator target;
2. derive why the exact interacting lattice bridge must be controlled by the
   normalized gauge-surplus action `I_2` from operator content alone, rather
   than reading the `I_2` correlation off a target-conditioned scan inside a
   pre-selected UV-localized window;
3. derive why the UV centroid `0.978 +/- 0.004` is the structurally selected
   value, rather than the empirical centroid of the retained class against
   the imported target;
4. derive why the three pre-selected profile families exhaust (or fairly
   sample) the admissible smooth bridge class, rather than treating them as
   convenient analytic placeholders;
5. derive the SM-like reference transport that defines `g_3,SM` in `I_2`
   from a closed two-loop (or higher) QCD beta on the framework's physical
   lattice surface, rather than the one-loop QCD beta as a proxy.

All five are operator/theorem problems and are out of scope for this note.
The note therefore stops at the bounded target-conditioned numerical-scan
claim and does not attempt to upgrade beyond it.

## Audit history

The 2026-05-05 audit recorded this row as `audited_numerical_match` with
Class-G load-bearing step, with the substantive observation that the runner
performs a real numerical scan rather than printing constants but the
load-bearing result depends on hard-coded physical inputs, a selected
constructive bridge ansatz, a target endpoint, and finite profile-family
scans rather than a first-principles derivation. The 2026-05-16 demotion
edit (this revision) rewrites the headline "Status", "Role", "Result", and
"Meaning" sections so the framing matches the auditor verdict instead of
relying on a trailing addendum. The runner output is unchanged; the current
audit status is owned by the regenerated audit pipeline and the next
independent re-audit. This brings the headline framing of this note into
agreement with the parallel 2026-05-16 demotions of its sister
`YT_CONSTRUCTIVE_UV_BRIDGE_NOTE.md` (three-family endpoint-stability scan)
and `YT_INTERACTING_BRIDGE_LOCALITY_NOTE.md` (target-conditioned locality
scan).

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
