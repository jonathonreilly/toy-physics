# Claim Status Certificate — Block 10 (Generalized Second Law)

**Date:** 2026-05-01 (originally) / 2026-05-02 (reframed under scope-aware classification)
**Block:** 10 — GSL δ(S_BH + S_matter) ≥ 0
**Slug:** `24h-axiom-first-derivations-20260501`
**Branch:** `physics-loop/24h-axiom-first-block10-gsl-20260501`
**Stacked PR base:** `physics-loop/24h-axiom-first-block05-firstlaw-20260501`
**Note:** [docs/AXIOM_FIRST_GENERALIZED_SECOND_LAW_THEOREM_NOTE_2026-05-01.md](../../../../docs/AXIOM_FIRST_GENERALIZED_SECOND_LAW_THEOREM_NOTE_2026-05-01.md)
**Runner:** [scripts/axiom_first_gsl_check.py](../../../../scripts/axiom_first_gsl_check.py)
**Log:** [outputs/axiom_first_gsl_check_2026-05-01.txt](../../../../outputs/axiom_first_gsl_check_2026-05-01.txt)

## Framework

Reframed under scope-aware classification (audit-lane proposal #291).

## Author classification (non-authoritative hint to auditor)

```yaml
claim_type_author_hint: bounded_theorem
claim_scope: "Generalized Second Law δ(S_BH + S_matter) ≥ 0 (GSL3) on the framework's retained gravity surface plus the upstream chain (KMS, Hawking T_H, first law); equivalently the Hawking 1971 area theorem δA ≥ 0 under NEC (GSL1) plus matter Gibbs H-theorem δS_matter ≥ 0 (GSL2) sum to GSL3, with Bekenstein bound enforcement (GSL4) as cross-link."
admitted_context_inputs:
  - Hawking 1971 area theorem (classical GR with NEC)
  - NEC (universal-physics input for ordinary matter)
  - quantum H-theorem (already in K2/K4 of Block 01)
upstream_dependencies:
  - block_05_first_law_bh_mechanics (this PR's stacked base)
  - block_02_hawking_temperature
  - block_01_kms_condition
  - bh_quarter_wald_noether_framework_carrier_theorem_note_2026-04-29 (audited_conditional)
  - universal_gr_discrete_global_closure_note (retained)
runner_classified_passes: 6 PASS (Hawking area theorem; matter Gibbs H-theorem; GSL combined; Bekenstein saturation tight; Hawking evaporation respects GSL; 100-sample random sweep with 0 violations)
```

## Why bounded_theorem

Inherits the bounded scope from upstream Block 05 plus admits the Hawking
1971 area theorem (NEC) as load-bearing admitted-context. Bounded scope
captures both honestly.

## Expected `effective_status` after audit

If Codex returns `audit_status = audited_clean` and `claim_type =
bounded_theorem`:

- **Path A** (full upstream chain reaches retained / retained_bounded):
  `effective_status = retained_bounded`.
- **Path B** (any upstream pending): `effective_status = proposed_retained`
  (transient).

## Dependency chain status snapshot (2026-05-02)

| Dep | Today's `effective_status` |
|---|---|
| Block 05 first law | proposed_retained |
| Block 02 Hawking T_H | proposed_retained |
| Block 01 KMS | proposed_retained |
| BH 1/4 carrier | audited_conditional (gating) |
| Framework GR action | retained |

## Review-loop disposition

- branch-local self-review: `pass` (6/6 tests; 100-sample random sweep with
  0 GSL violations).
- formal Codex audit: pending.

## Audit hand-off

Block 10 is the **terminal node in the BH thermodynamics chain**. Together
with retained BH 1/4 + Block 05 (first law) + Block 02 (Hawking T_H) +
Block 01 (KMS), this PR completes the framework's BH thermodynamics
derivation program (zeroth, first, generalized-second laws). Combined
with Block 03 (Bekenstein), it provides the holographic information bound.
