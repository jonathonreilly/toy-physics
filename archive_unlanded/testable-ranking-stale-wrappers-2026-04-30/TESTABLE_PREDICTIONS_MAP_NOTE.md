# Testable Predictions Map

**Date:** 2026-04-05  
**Status:** RETRACTED 2026-04-30 — audit failed; this note is archived under `archive_unlanded/testable-ranking-stale-wrappers-2026-04-30/`. Claims below are NOT supported by current runners or current audit lane. See `## Retraction` section.

## Retraction

- Date archived: 2026-04-30
- Archive directory: `archive_unlanded/testable-ranking-stale-wrappers-2026-04-30/`
- Audit verdict (`verdict_rationale` from [audit_ledger.json](../../docs/audit/data/audit_ledger.json), claim_id `testable_predictions_map_note`, `audit_status: audited_failed`, `effective_status: retained_no_go`):

> "Issue: The map claims to rank current candidate retained-grade testables and to record what is already retained, but its cited authorities include bounded or conditional notes such as the diamond protocol/prediction lane, the wavefield escalation note, the growing-graph expansion card, and the generated-family bridge; the note also lists seven ranked entries but the later current ranking drops the grown-trapping and growing-expansion entries and reorders the list. Why this blocks: a retained catalog cannot assert current retained status or a stable ranking when the one-hop sources and the note's own ranking sections disagree. Repair target: regenerate the map from the audit ledger, separating audited-clean/retained, conditional, bounded, and unaudited items, and make the numbered ranking, top-3, and bottom-line sections mechanically consistent. Claim boundary until fixed: safe to treat this as a stale editorial snapshot of candidate testable lanes; not safe to cite it as a retained current map of audit-clean testable predictions."

Do NOT cite the numerical results, tables, or threshold values in the original content below as live framework claims. The runners referenced in this note have been superseded or are no longer reproducible at the time of audit. If a future investigation revisits this physics, treat it as starting from scratch rather than as continuation of a "closed no-go".

---

## Purpose

This note is a compact, adversarial map of the best current testable
predictions across the retained science on `main`.

The ranking is by **external testability and discriminator quality**, not by
how exciting the lane feels internally.

Each entry records:

- observable
- standard null
- what is already retained
- what still needs hardening
- platform class: tabletop, analog-simulator, or theory-only

## 1. Diamond / NV lock-in quadrature protocol

- Observable: `X`, `Y`, `phi = atan2(Y, X)`, and optionally a spatial phase
  ramp across the NV image
- Standard null: after calibration and static-background subtraction, the
  quasi-static instantaneous baseline gives `Y ≈ 0`, `phi ≈ 0`, and a flat
  phase profile
- Already retained:
  - [`docs/DIAMOND_SENSOR_PREDICTION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DIAMOND_SENSOR_PREDICTION_NOTE.md)
  - [`docs/DIAMOND_SENSOR_PROTOCOL_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DIAMOND_SENSOR_PROTOCOL_NOTE.md)
  - [`docs/DIAMOND_NV_PHASE_RAMP_SIGNAL_BUDGET_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DIAMOND_NV_PHASE_RAMP_SIGNAL_BUDGET_NOTE.md)
  - the retarded / wavefield lane gives the motivation for a phase-sensitive
    discriminator
- Still needs hardening:
  - an ideal-detector forward model before any lab-specific noise or bandwidth claims
  - a calibrated signal budget
  - an explicit source geometry / drive protocol
  - a lab-specific noise-floor estimate
- Platform class: **tabletop-testable**

Why it ranks first:

- it is the cleanest lab-facing discriminator
- it naturally fits an NV / lock-in measurement stack
- it is differential, not a raw absolute-amplitude claim

## 2. Electrostatics scalar sign-law card

- Observable: sign antisymmetry, exact cancellation/null, dipole directionality,
  charge-scaling exponent, and screening ratio
- Standard null: exact opposite-sign superposition at the same node must cancel
  to printed precision; a separated +/- pair is a dipole, not a null
- Already retained:
  - [`docs/ELECTROSTATICS_CARD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ELECTROSTATICS_CARD_NOTE.md)
  - sign antisymmetry ratio: `-1.000`
  - exact null: `PASS`
  - dipole orientation flip ratio: `-0.999`
  - charge scaling: `|delta| ~ q^1.000`
  - screening ratio: `0.018`
- Still needs hardening:
  - a concrete lab protocol if this is going to be claimed outside the ordered
    lattice
  - a stronger mapping from the scalar sign law to a real electrostatic
    measurement stack
- Platform class: **theory-only**

Why it ranks this high:

- it is a clean, review-safe scalar sign law on a retained family
- it gives five separate observables without inflating into full EM
- it is a plausible bridge to a lab conversation later

## 3. Exact-lattice wavefield phase-ramp discriminator

- Observable: detector-line phase-ramp slope and span, plus the wave/same-site
  response ratio
- Standard null: the same-site-memory control or zero-source baseline should
  give no coherent phase ramp and no large wave/same separation
- Already retained:
  - [`docs/SOURCE_RESOLVED_WAVEFIELD_ESCALATION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SOURCE_RESOLVED_WAVEFIELD_ESCALATION_NOTE.md)
  - exact zero-source reduction survives
  - the detector-line ramp is coherent (`R^2 ~ 0.96`)
  - weak-field sign is `TOWARD`
  - `F~M` stays near `1.00`
- Still needs hardening:
  - transfer off the exact lattice
  - a stronger experimental mapping if it is going to be claimed outside the current bounded computational model
- Platform class: **analog-simulator-testable** in spirit, **theory-only** as
  a literal lattice claim

Why it ranks high:

- it is the strongest exact-lattice wave signature
- it gives a cleaner phase observable than the older compact pocket
- it is the nearest theory-side bridge to the diamond protocol

## 4. Grown trapping / frontier transport

- Observable: escape ratio and frontier-radius shift versus trap coupling
- Standard null: `eta = 0` must reproduce the retained grown baseline exactly
- Already retained:
  - [`docs/GATE_B_GROWN_TRAPPING_FRONTIER_V2_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_GROWN_TRAPPING_FRONTIER_V2_NOTE.md)
  - escape falls monotonically with coupling
  - frontier-radius shift rises monotonically with coupling
- Still needs hardening:
  - a stronger structural observable than frontier radius alone
  - a more horizon-like interpretation only if a sharper no-return signature appears
- Platform class: **analog-simulator-testable**

Why it ranks above the broader theory lanes:

- it has an exact reduction check
- it is stronger than escape-only transport
- it is a live generated-geometry strong-field knob

## 5. Growing graph expansion proxy

- Observable: node-count growth, frontier growth, mean radius growth, max
  radius growth
- Standard null: the static control should stay flat in count and radius
- Already retained:
  - [`docs/GROWING_GRAPH_EXPANSION_CARD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GROWING_GRAPH_EXPANSION_CARD_NOTE.md)
  - node count grows from `35` to `1369` over 16 steps
  - mean radius grows from `2.2837` to `14.1520`
  - log-slope fit for node count: `1.041` with `R^2 = 0.970`
  - log-slope fit for mean radius: `0.519` with `R^2 = 0.970`
- Still needs hardening:
  - a more de Sitter-like or inflation-like control story if this is going to
    be promoted beyond a graph-growth proxy
  - a clearer mapping from the graph-growth observable to any cosmology
    analogy
- Platform class: **theory-only**

Why it ranks here:

- it is a clean graph-growth proxy with a flat static control
- it is the closest thing we have right now to a spreading analogue
- it is still only an analog-proxy, not a cosmology derivation

## 6. Wide-lattice distance law

- Observable: far-tail exponent `alpha` from the ordered 3D `1/L^2` family
- Standard null: a far-tail fit that does not remain stable in the promoted
  window, or a near-field-only slope that fails the far-tail check
- Already retained:
  - [`docs/WIDE_LATTICE_H2T_DISTANCE_LAW_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/WIDE_LATTICE_H2T_DISTANCE_LAW_NOTE.md)
  - Born is machine-clean
  - `k = 0` is clean
  - all tested rows are `TOWARD`
  - far-tail fit is `b^(-1.05)` with `R^2 = 0.990`
  - `F~M = 1.000`
- Still needs hardening:
  - a stronger asymptotic / wider-window statement
  - a clearer separation between finite-lattice replay and any continuum claim
- Platform class: **theory-only** for now

Why it still matters:

- it is the cleanest retained far-tail law on `main`
- it is a strong finite-lattice prediction even if the continuum status is not
  yet settled

## 7. Generated-family bridge

- Observable: support width `N_eff`, `TOWARD` counts, and weak-field `F~M`
  on the split-shell family
- Standard null: the compact bridge family and the static baseline should not
  be promoted as a closure if the weak-field law stays weak
- Already retained:
  - [`docs/SOURCE_RESOLVED_GENERATED_NEW_FAMILY_V2_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SOURCE_RESOLVED_GENERATED_NEW_FAMILY_V2_NOTE.md)
  - the split-shell family widens support
  - `F~M` improves to `0.500` under the fixed-weight wavefield
- Still needs hardening:
  - a real weak-field closure, not just a broader bridge
  - a geometry rule that restores the law rather than only widening support
- Platform class: **theory-only** right now, with a possible analog-simulator
  path later

Why it is still worth tracking:

- it is the first real reopening after the compact bridge closure
- it shows that support geometry can be changed without losing exact
  zero-source reduction

## Current ranking

1. Diamond / NV lock-in quadrature protocol
2. Electrostatics scalar sign-law card
3. Exact-lattice wavefield phase-ramp discriminator
4. Wide-lattice distance law
5. Generated-family bridge

## Top 3 testables

- Diamond / NV lock-in quadrature protocol
- Electrostatics scalar sign-law card
- Exact-lattice wavefield phase-ramp discriminator

## Bottom line

The cleanest current path to an outside experiment is the diamond protocol.
The cleanest retained theory-side scalar sign-law discriminator is the
electrostatics card.
The cleanest retained theory-side phase discriminator is the exact-lattice
wavefield phase ramp.
The cleanest retained graph-growth spreading proxy is the growing-graph
expansion card.
The cleanest grown-geometry strong-field observable is the trapping/frontier
moment shift.

The wide-lattice distance law is the best pure theory prediction in the set,
but it is not yet a tabletop protocol.
