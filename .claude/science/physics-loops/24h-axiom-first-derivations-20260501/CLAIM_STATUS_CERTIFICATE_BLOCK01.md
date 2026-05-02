# Claim Status Certificate — Block 01 (KMS condition)

**Date:** 2026-05-01 (originally) / 2026-05-02 (reframed under scope-aware classification)
**Block:** 01 — KMS condition from RP + spectrum condition
**Slug:** `24h-axiom-first-derivations-20260501`
**Branch:** `physics-loop/24h-axiom-first-block01-kms-20260501`
**Note:** [docs/AXIOM_FIRST_KMS_CONDITION_THEOREM_NOTE_2026-05-01.md](../../../../docs/AXIOM_FIRST_KMS_CONDITION_THEOREM_NOTE_2026-05-01.md)
**Runner:** [scripts/axiom_first_kms_condition_check.py](../../../../scripts/axiom_first_kms_condition_check.py)
**Log:** [outputs/axiom_first_kms_condition_check_2026-05-01.txt](../../../../outputs/axiom_first_kms_condition_check_2026-05-01.txt)

## Framework

Reframed under the scope-aware classification framework adopted 2026-05-02
(audit-lane proposal #291). Pipeline-derived `effective_status`.

## Author classification (non-authoritative hint to auditor)

```yaml
claim_type_author_hint: positive_theorem
claim_scope: "Finite-temperature Gibbs state on the RP-reconstructed transfer-matrix Hilbert space H_phys satisfies KMS conditions (K1)-(K4) at inverse temperature β_th = L_τ·a_τ; periodic-Euclidean path integral on (Z/L_τ Z) × Z^3 equals tr T^{L_τ}; strip identity F(t + iβ_th) = G(t) holds for all bounded operators on the finite-dim H_phys."
admitted_context_inputs:
  - Wick rotation convention (already paid for by RP reconstruction)
  - cyclic-trace identity (basic linear algebra)
upstream_dependencies:
  - axiom_first_reflection_positivity_theorem_note_2026-04-29 (Codex clean audit record cross_family; awaiting framework-adoption sweep before any retained-grade pipeline derivation)
  - axiom_first_spectrum_condition_theorem_note_2026-04-29 (Codex audited_conditional — needs RP citation registered as ledger dep)
  - minimal_axioms_2026-04-11 (retained: A1-A4)
runner_classified_passes: 5 PASS at <1e-10 precision (KMS strip identity, strip continuity, equilibrium uniqueness, path-integral correspondence, detailed-balance at z = iβ_th)
```

## Audit handoff

Audit status is set only by the independent audit lane. Review-loop does not
prefill an `audit_status` or promise an `effective_status`; after any clean
independent audit, the pipeline derives effective status from `claim_type` plus
dependency closure. If upstream deps remain non-retained-grade, the row remains
pending/blocked until those deps are repaired and audited.

## Dependency chain status snapshot (2026-05-02)

| Dep | Today's `effective_status` (post adoption) |
|---|---|
| RP | support (Codex clean audit record; framework-adoption sweep required) |
| Spectrum cond | audited_conditional (RP dep registration repair pending) |
| A_min (A1-A4) | retained |

The spectrum-condition fix is the load-bearing repair. Once that lands,
Block 01 promotes immediately and unlocks downstream Blocks 02 (Hawking),
06 (Stefan-Boltzmann), 08 (Unruh), 10 (GSL).

## Review-loop disposition

- branch-local self-review: `pass` (5/5 tests at machine precision; KMS
  direction F(t+iβ) = G(t) explicitly verified).
- formal Codex audit: pending under new prompt template
  ([`PROPOSED_AUDIT_AGENT_PROMPT_TEMPLATE.md`](../../../../docs/audit/proposals/scope-aware-classification-20260502/PROPOSED_AUDIT_AGENT_PROMPT_TEMPLATE.md)).

## Audit hand-off

Block 01 is the root of the thermal-physics chain. Auditor should evaluate
under the new prompt template. Successful clean audit + clean upstream
chain unlocks Blocks 02, 06, 08, 10 for promotion.
