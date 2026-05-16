# y_t Interacting Bridge Locality Proxy Note

**Date:** 2026-04-15 (demoted 2026-05-16)
**Claim type:** bounded_theorem
**Status:** bounded numerical-match proxy (target-conditioned scan against imported endpoint)
**Audit class:** G — load-bearing step is a target-conditioned numerical comparator, not a derivation
**Primary runner:** `scripts/frontier_yt_interacting_bridge_locality.py`

## Scope (honest framing)

This note is **not** a derivation that the exact interacting lattice bridge is
forced into a UV-localized window. It is a bounded *target-conditioned*
consistency scan: given an imported physical endpoint `y_t(v) = 0.9176` and a
chosen smooth profile family that already preserves the exact endpoint data,
the scan reports which profiles in that family reproduce the imported endpoint
within `1%` versus which overshoot it by more than `5%`.

Three load-bearing inputs are imported, not derived inside this note:

1. the physical target `y_t(v) = 0.9176`,
2. the SM-like reference transport anchored at the low-energy strong coupling
   (one-loop QCD beta), and
3. the chosen smooth sigmoid-blend profile family parameterized by
   `(center_frac, width_frac)`.

The runner's `1c` PASS — "profiles within 1% exist only in the UV-localized
window `center >= 0.95`, `width <= 0.03`" — is therefore a statement about
*this scanned family against this imported target*, not a statement that the
exact interacting bridge is forced to lie in that window.

This is therefore an `audited_numerical_match` / class-G proxy in the project's
audit taxonomy, not a closed first-principles derivation of UV-localization.
The remaining structural gaps are recorded below in "What remains open".

## Previous-scan context (informational)

The runner scans a family of smooth bridge profiles that all preserve the same
exact endpoint data:

- `g_3(v)` fixed by the coupling-map theorem
- `g_3(M_Pl)` fixed by the lattice coupling
- `y_t(M_Pl) = g_3(M_Pl) / sqrt(6)` fixed by the Ward identity

The family interpolates between:

1. an SM-like transport anchored at the accepted low-energy strong coupling,
   and
2. a lattice-side UV bridge profile satisfying the exact UV endpoint.

So the scan does not ask whether the endpoints are right. It asks, *for the
imported physical target*, how the shape of a bridge inside this chosen
sigmoid-blend family can vary while reproducing that target within `1%`.

## Numerical result

The runner reports, for the scanned profile family against the imported
target `y_t(v) = 0.9176`:

- `9 / 70` profiles land within `1%` of the imported central value, and all of
  them occur only for `center_frac >= 0.95` and `width_frac <= 0.03`
- all early/diffuse profiles with `center_frac <= 0.85` overshoot the imported
  target by more than `5%`
- both `g_3(v)` and `g_3(M_Pl)` exact endpoints are preserved across all
  scanned profiles by construction
- the best smooth profile in the scan gives `y_t(v) = 0.9159` (`-0.18%` from
  the imported target)

The honest interpretation is that, **conditional on** the imported endpoint
target, **conditional on** the chosen sigmoid-blend profile family, and
**conditional on** the SM-like reference background, only the profiles whose
deformation is concentrated in a narrow UV-localized window near `M_Pl`
reproduce the imported target within `1%`.

It does not establish that the exact interacting lattice bridge actually
belongs to that UV-localized window, nor that this profile family fairly
samples the admissible bridge class outside of it.

## Meaning (bounded)

The bounded claim this note licenses is narrow:

> *Conditional on* the imported endpoint `y_t(v) = 0.9176`, *conditional on*
> the chosen sigmoid-blend profile family parameterized by
> `(center_frac, width_frac)`, and *conditional on* the SM-like reference
> transport, the profiles in this family that reproduce the imported endpoint
> within `1%` are exactly those with `center_frac >= 0.95` and
> `width_frac <= 0.03`; profiles with `center_frac <= 0.85` overshoot the
> imported endpoint by more than `5%`.

It does **not** establish:

- that the exact interacting lattice bridge is forced into that UV-localized
  window,
- that the current `~3%` bridge surrogate envelope disappears, or
- that the operator-level interacting bridge theorem is closed.

A structurally consistent reason to expect UV-localization for *positive*
bridge surplus on the accepted background is recorded separately in
[YT_BRIDGE_REARRANGEMENT_PRINCIPLE_NOTE.md](YT_BRIDGE_REARRANGEMENT_PRINCIPLE_NOTE.md):
the linearized endpoint-response kernel is positive and monotone increasing
toward the IR, so equal-area surplus has less endpoint leverage when placed
closer to the UV. That rearrangement statement is itself conditioned on the
same accepted background and on positivity of the bridge surplus; it is not
yet a derivation that the exact interacting lattice bridge is forced into the
UV-localized window. The two notes are mutually supporting target-conditioned
proxies, not a joint derivation.

## What remains open (load-bearing gaps)

To upgrade the locality conclusion from `audited_conditional` / class-G to
`audited_clean`, the following structural gaps must be closed; none are
addressed by the present runner:

1. derive the endpoint `y_t(v) = 0.9176` from the framework axioms rather
   than importing it as the comparator target;
2. derive why the interacting lattice bridge must lie in (or near) the
   UV-localized window from operator content alone, rather than reading the
   window off a target-conditioned scan;
3. derive why the chosen sigmoid-blend profile family is representative of the
   admissible smooth bridge class, rather than treating it as a convenient
   analytic placeholder;
4. derive the SM-like reference transport from a closed two-loop (or higher)
   QCD beta on the framework's physical lattice surface, rather than using the
   one-loop QCD beta as a proxy.

All four are operator/theorem problems and are out of scope for this note.
The note therefore stops at the bounded target-conditioned consistency claim
and does not attempt to upgrade beyond it.

## Audit history

The 2026-05-02 audit recorded this row as `audited_numerical_match` with
Class-G load-bearing step ("target-conditioned scan locality"). The 2026-05-05
re-audit re-classified it as `audited_conditional` with Class-D load-bearing
step on a `critical`-criticality re-audit, with the same substantive
observation that the conclusion depends on imported endpoint data, the
accepted target value, one-loop transport choices, and the chosen bridge
family. The 2026-05-16 demotion edit (this revision) rewrites the headline
"Scope", "Result", and "Meaning" sections so the framing matches the auditor
verdict instead of relying on a trailing addendum. No runner, audit-data, or
publication file is changed by the demotion; the bounded target-conditioned
proxy status is preserved. This brings the headline framing of this note into
agreement with the parallel 2026-05-16 demotion of its sister
[YT_CONSTRUCTIVE_UV_BRIDGE_NOTE.md](YT_CONSTRUCTIVE_UV_BRIDGE_NOTE.md), which
runs the same scope correction on the three-family endpoint-stability scan.

## Audit dependency repair links

This graph-bookkeeping section records the upstream notes the locality
scan and endpoint data depend on. It does not promote this note or
change the audited claim scope.

- [YT_BOUNDARY_THEOREM.md](YT_BOUNDARY_THEOREM.md)
  for the v boundary used as the IR endpoint reference.
- [YT_EW_COUPLING_BRIDGE_NOTE.md](YT_EW_COUPLING_BRIDGE_NOTE.md)
  for the EW-coupling inputs that fix the scan's endpoint data.
- [YT_BRIDGE_OPERATOR_CLOSURE_NOTE.md](YT_BRIDGE_OPERATOR_CLOSURE_NOTE.md)
  for the EW-window proxy that excludes diffuse rescues, complementary
  to the locality scan.
- [YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md](YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md)
  for the QFP-stability bound on the SM-like transport over most of the
  interval.
- [YT_BRIDGE_REARRANGEMENT_PRINCIPLE_NOTE.md](YT_BRIDGE_REARRANGEMENT_PRINCIPLE_NOTE.md)
  for the structurally consistent rearrangement argument that, *conditional
  on* the same accepted background and positive bridge surplus, equal-area
  surplus near the UV gives the smallest endpoint response. This is a
  target-conditioned structural support for why the UV-localized window of
  the present scan is the smallest-response rearrangement, not an
  independent derivation that the exact interacting bridge is forced into
  that window.
