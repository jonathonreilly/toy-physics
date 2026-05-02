# Claim Status Certificate — Block 02 (Hawking temperature)

**Date:** 2026-05-01
**Block:** 02 — Hawking T_H = κ/(2π) from Wick-rotated Killing horizon + KMS
**Slug:** `24h-axiom-first-derivations-20260501`
**Branch:** `physics-loop/24h-axiom-first-block02-hawking-20260501`
**Stacked PR base:** `physics-loop/24h-axiom-first-block01-kms-20260501`
**Note:** [docs/AXIOM_FIRST_HAWKING_TEMPERATURE_THEOREM_NOTE_2026-05-01.md](../../../../docs/AXIOM_FIRST_HAWKING_TEMPERATURE_THEOREM_NOTE_2026-05-01.md)
**Runner:** [scripts/axiom_first_hawking_temperature_check.py](../../../../scripts/axiom_first_hawking_temperature_check.py)
**Log:** [outputs/axiom_first_hawking_temperature_check_2026-05-01.txt](../../../../outputs/axiom_first_hawking_temperature_check_2026-05-01.txt)

## Status fields

```yaml
actual_current_surface_status: support
conditional_surface_status: derived support theorem on retained framework GR + retained BH 1/4 carrier (admitted Wald-Noether) + Block 01 KMS support
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "Inherits upstream support classification: depends on Block 01 KMS support theorem which is itself audit-pending support (depends on retained-but-audit-pending RP and spectrum-condition support notes). Per physics-loop SKILL retained-proposal certificate item 4, a chain of support cannot promote to proposed_retained until all dependencies are ratified retained on the current authority surface. Note also: Killing-horizon and Wick-rotation-regularity vocabulary is admitted-context input (same as upstream Wald-Noether composition); not a new admission, but counts toward audit-required."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Dependency classes

| Dep | Class | Source |
|---|---|---|
| A1-A4 | A_min axiom (inherited via Block 01) | `docs/MINIMAL_AXIOMS_2026-04-11.md` |
| Framework GR action surface | retained | `docs/UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md` and family |
| Canonical Einstein-Hilbert equivalence | retained | `docs/UNIVERSAL_QG_CANONICAL_TEXTBOOK_GEOMETRIC_ACTION_EQUIVALENCE_NOTE.md` |
| BH 1/4 carrier composition | retained (with admitted Wald formula) | `docs/BH_QUARTER_WALD_NOETHER_FRAMEWORK_CARRIER_THEOREM_NOTE_2026-04-29.md` |
| Block 01 KMS support theorem | support, audit-pending | `docs/AXIOM_FIRST_KMS_CONDITION_THEOREM_NOTE_2026-05-01.md` (this PR base) |
| Surface gravity κ definition | admitted-context | standard differential geometry; same admission as Wald-Noether composition |
| Wick-rotation regularity at the bolt | admitted-context | standard Hawking-Gibbons argument; same admission as Wald-Noether composition |
| Asymptotic-time identification | admitted-context | standard stationary GR |

## Open imports

The Killing-horizon vocabulary (κ definition, Wick-rotation regularity)
is the same admitted-context input already paid for by the retained
BH 1/4 carrier composition. No new imports.

## Review-loop disposition

- branch-local self-review: `pass` (theorem note matches runner output;
  Wick-rotation regularity argument matches Step 2 algebra; Schwarzschild
  benchmark T_H = 1/(8 π G M) recovered exactly).
- formal `/review-loop` execution: deferred to integration-time.

## Status conclusion

This block is a **derived support theorem** on the framework's retained
GR action surface plus Block 01 KMS support. It is suitable for future
integration into the package's gravitational thermodynamics surface as a
support-grade theorem.

It is **not** suitable for `proposed_retained` / `proposed_promoted`
status until:

1. Upstream RP and spectrum-condition support notes are ratified retained.
2. Block 01 KMS support is ratified retained.
3. Independent audit of Steps 1–4 of the proof.

The PR title and body should use `support` (or `support theorem`) and
make explicit that bare `retained` / `promoted` is not allowed.

## Audit hand-off requirement

If a later integration / review process wants to promote this note to
`proposed_retained`, it needs:

1. The full upstream chain (RP + spectrum cond + Block 01 KMS) ratified
   retained on the current authority surface.
2. Independent audit of the theorem note's Steps 1–4.
3. Independent verification of the runner's 6-test pass on a clean
   environment.
4. Optional: independent Bogoliubov-coefficient derivation of T_H
   (Hawking 1975 original method) on the framework's QFT-on-curved-
   spacetime surface as a cross-check.

Until then this note remains `support` per the controlled vocabulary.
