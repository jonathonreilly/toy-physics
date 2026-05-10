# Shapiro Diamond Bridge Note

**Date:** 2026-04-06  
**Status:** RETRACTED 2026-04-30 — audit failed; this note is archived under `archive_unlanded/shapiro-static-renderers-and-failed-bridges-2026-04-30/`. Claims below are NOT supported by current runners or current audit lane. See `## Retraction` section.

## Retraction

- **Date archived:** 2026-04-30
- **Archive directory:** `archive_unlanded/shapiro-static-renderers-and-failed-bridges-2026-04-30/` (the directory name encodes the failure reason: static renderers and failed bridges).
- **Audit verdict_rationale (quoted verbatim from `docs/audit/data/audit_ledger.json`):**

  > Issue: The bridge claim identifies the Shapiro phase lag with diamond/NV proxy phasor language without a runner or audit-clean causal and diamond-unit inputs. Why this blocks: failed causal-field dependencies cannot support a candidate retained-grade c-dependent phase lag, and unknown diamond bridge/unit notes cannot justify even proxy-level lab-facing translation beyond notation. Repair target: repair and audit the causal phase-lag derivation, audit the diamond phase-ramp and absolute-unit bridge notes, and add a runner constructing X, Y, phi, and phase-ramp quantities from the same data pipeline. Claim boundary until fixed: it is safe to say this note proposes X/Y/phi language as a handoff vocabulary for a supplied phase-lag table; it is not safe to claim a retained Shapiro-to-diamond bridge or lab-facing causal discriminator.

- **Do not cite warning:** Do NOT cite the numerical results, tables, or threshold values in the original content below as live framework claims. The runners referenced in this note have been superseded or are no longer reproducible at the time of audit. If a future investigation revisits this physics, treat it as starting from scratch rather than as continuation of a "closed no-go".

## Artifact Chain

- [`docs/DIAMOND_PHASE_RAMP_BRIDGE_CARD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DIAMOND_PHASE_RAMP_BRIDGE_CARD_NOTE.md)
- [`docs/DIAMOND_ABSOLUTE_UNIT_BRIDGE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DIAMOND_ABSOLUTE_UNIT_BRIDGE_NOTE.md)
- [`archive_unlanded/causal-field-stale-runners-2026-04-30/CAUSAL_PROPAGATING_FIELD_NOTE.md`](/Users/jonreilly/Projects/Physics/archive_unlanded/causal-field-stale-runners-2026-04-30/CAUSAL_PROPAGATING_FIELD_NOTE.md)
- [`docs/CAUSAL_FIELD_RECONCILIATION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/CAUSAL_FIELD_RECONCILIATION_NOTE.md)

## Question

How do we express the retained c-dependent phase lag in the same `X / Y / phi`
and phase-ramp language as the diamond/NV bridge card, while keeping the claim
surface lab-facing and review-safe?

## Retained Phase-Lag Result

The discrete Shapiro-style phase lag is the new causal-propagation observable:

- `c = inst`: phase lag `0.000 rad`
- `c = 2.0`: phase lag `+0.040 rad`
- `c = 1.0`: phase lag `+0.050 rad`
- `c = 0.5`: phase lag `+0.062 rad`
- `c = 0.25`: phase lag `+0.068 rad`

The key properties already retained are:

- the phase lag is monotone in slower field propagation
- the phase lag is stable across seeds to three significant figures
- the same table is portable across the three grown families
- static fields do not produce this c-dependent delay

## Bridge Language

The bridge card language is already the right one:

- `X` is the in-phase proxy channel
- `Y` is the quadrature proxy channel
- `phi = atan2(Y, X)` is the phase lag
- the phase-ramp slope is the cleanest calibration handle

The Shapiro-style phase lag should be read as the same class of observable:

- a detector-line phase shift, not just a centroid displacement
- a causal-delay signature, not just a static field-shape effect
- a proxy phasor that can be expressed in `X / Y / phi` form

In that language, the phase lag is the causal analog of the bridge-card
quadrature channel:

- `X` tracks the in-phase response
- `Y` tracks the delay-sensitive residue
- `phi` tracks the detector-facing causal delay
- the phase-ramp slope tracks how quickly that delay accumulates across the
  detector line

## Why This Is Different From Static Deflection

The retained causal-field work now separates two effects:

- a broad static or forward-only deflection shape
- a c-dependent detector-phase delay

Static fields can mimic the first class of observable, but they do not give a
clean c-dependent phase lag of the Shapiro type.

So the diamond-facing translation should emphasize:

- not just "the beam moves"
- but "the beam acquires a quadrature / phase-ramp signature that changes with
  propagation speed"

That is the cleanest lab-facing discriminator in the retained causal package.

## What Can Be Claimed In-Repo

The repo can defensibly say:

- the causal delay is expressible as a proxy phasor in `X / Y / phi` language
- the phase lag is coherent and seed-stable
- the phase lag is portable across the three retained grown families
- the causal phase observable remains a proxy, not an absolute NV readout

The repo cannot yet say:

- absolute NV counts
- a calibrated detectability threshold in a specific microscope
- a transfer coefficient from proxy units to lab units

## Recommended Handoff Sentence

The strongest review-safe handoff is:

**the retained causal phase lag is a proxy-level `phi`/phase-ramp observable
that is portable across the three grown families and is qualitatively different
from static deflection, but it still needs external calibration before it can
be translated into absolute NV units**

## Narrow Conclusion

The Shapiro-style result belongs in the diamond/NV story as a **phase-sensitive
causal discriminator**:

- it lives in the same `X / Y / phi` language as the bridge card
- it strengthens the phase-ramp handoff
- it does not yet replace the missing external calibration coefficient

So the correct bridge claim is:

**proxy-level causal phase lag, portable across the retained grown families,
expressible as `X / Y / phi` and phase-ramp slope, but still not an absolute
NV-unit prediction**
