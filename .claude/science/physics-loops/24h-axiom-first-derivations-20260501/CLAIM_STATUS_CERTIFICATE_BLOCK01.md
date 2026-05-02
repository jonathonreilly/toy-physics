# Claim Status Certificate — Block 01 (KMS condition)

**Date:** 2026-05-01
**Block:** 01 — KMS condition from RP + spectrum condition
**Slug:** `24h-axiom-first-derivations-20260501`
**Branch:** `physics-loop/24h-axiom-first-block01-kms-20260501`
**Note:** [docs/AXIOM_FIRST_KMS_CONDITION_THEOREM_NOTE_2026-05-01.md](../../../../docs/AXIOM_FIRST_KMS_CONDITION_THEOREM_NOTE_2026-05-01.md)
**Runner:** [scripts/axiom_first_kms_condition_check.py](../../../../scripts/axiom_first_kms_condition_check.py)
**Log:** [outputs/axiom_first_kms_condition_check_2026-05-01.txt](../../../../outputs/axiom_first_kms_condition_check_2026-05-01.txt)

## Status fields

```yaml
actual_current_surface_status: support
conditional_surface_status: derived support theorem on A_min + retained RP + retained spectrum condition
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "Depends on retained-RP and retained-spectrum-condition support notes that are themselves audit-pending support claims (per `docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md` line 4: 'support — branch-local theorem note on A_min; runner passing; audit-pending'). Per the physics-loop SKILL retained-proposal certificate item 4 ('Every dependency is retained, a retained corollary, or explicitly allowed exact support on the current authority surface'), proposed_retained / proposed_promoted is not allowed until those upstream support notes are ratified to retained on the current authority surface."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Dependency classes

| Dep | Class | Source |
|---|---|---|
| A1 (Cl(3) local algebra) | A_min axiom | `docs/MINIMAL_AXIOMS_2026-04-11.md` |
| A2 (Z^3 substrate) | A_min axiom | `docs/MINIMAL_AXIOMS_2026-04-11.md` |
| A3 (finite Grassmann staggered Dirac) | A_min axiom | `docs/MINIMAL_AXIOMS_2026-04-11.md` |
| A4 (canonical normalization) | A_min axiom | `docs/MINIMAL_AXIOMS_2026-04-11.md` |
| RP transfer matrix (R3) | retained support, audit-pending | `docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md` |
| Spectrum condition (SC1, SC2) | retained support, audit-pending | `docs/AXIOM_FIRST_SPECTRUM_CONDITION_THEOREM_NOTE_2026-04-29.md` |
| Wick rotation convention | admitted-context input | already paid for by RP reconstruction |
| Cyclic-trace identity | basic linear algebra | not an import |

## Open imports

None beyond the explicit admitted-context list above. The Wick-rotation
convention is the same one already paid for by the upstream RP note.

## Review-loop disposition

- branch-local self-review: `pass` (theorem note matches runner output;
  KMS direction explicitly verified by runner Test 1 on a generic
  finite-dim H >= 0; detailed-balance corollary at z = i β_th cross-checks
  the same identity at the strip endpoint).
- formal `/review-loop` execution: deferred to integration-time per the
  campaign mode (block-local self-review in REVIEW_HISTORY.md).

## Status conclusion

This block is a **derived support theorem** on `A_min` plus the retained
axiom-first foundations (RP + spectrum condition). It is suitable for
future integration into the package's thermal-state language as a
support-grade theorem.

It is **not** suitable for `proposed_retained` / `proposed_promoted`
status until the upstream RP and spectrum-condition support notes are
ratified to retained / proposed_retained on the current authority surface.

The PR title and body should use `support` (or `support theorem`) and
make explicit that bare `retained` / `promoted` is not allowed.

## Audit hand-off requirement

If a later integration / review process wants to promote this note to
`proposed_retained`, it needs:

1. The upstream RP note (`docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`)
   ratified to retained / proposed_retained on the current authority
   surface.
2. The upstream spectrum condition note (`docs/AXIOM_FIRST_SPECTRUM_CONDITION_THEOREM_NOTE_2026-04-29.md`)
   ratified to retained / proposed_retained on the current authority
   surface.
3. Independent audit of the theorem note's Steps 1–5.
4. Independent verification of the runner's 5-test pass on a clean
   environment.

Until then this note remains `support` per the controlled vocabulary.
