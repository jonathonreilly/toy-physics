# Claim Status Certificate — Block 08 (Unruh temperature)

**Date:** 2026-05-01 (originally) / 2026-05-02 (reframed under scope-aware classification)
**Block:** 08 — Unruh T_U = a/(2π)
**Slug:** `24h-axiom-first-derivations-20260501`
**Branch:** `physics-loop/24h-axiom-first-block08-unruh-20260501`
**Stacked PR base:** `physics-loop/24h-axiom-first-block01-kms-20260501`
**Note:** [docs/AXIOM_FIRST_UNRUH_TEMPERATURE_THEOREM_NOTE_2026-05-01.md](../../../../docs/AXIOM_FIRST_UNRUH_TEMPERATURE_THEOREM_NOTE_2026-05-01.md)
**Runner:** [scripts/axiom_first_unruh_temperature_check.py](../../../../scripts/axiom_first_unruh_temperature_check.py)
**Log:** [outputs/axiom_first_unruh_temperature_check_2026-05-01.txt](../../../../outputs/axiom_first_unruh_temperature_check_2026-05-01.txt)

## Framework

Reframed under scope-aware classification (audit-lane proposal #291).

## Author classification (non-authoritative hint to auditor)

```yaml
claim_type_author_hint: bounded_theorem
claim_scope: "For a uniformly accelerated observer with proper acceleration a in the framework Minkowski-limit Rindler wedge on the retained Lorentz kernel surface, the regular Wick-rotated Rindler period is 2π and the Minkowski vacuum appears as Gibbs at proper-time inverse temperature β_th(a) = 2π/a, i.e. T_Unruh = a/(2π) (U1)-(U4); also Bisognano-Wichmann modular operator identity Δ_R = exp(-2πK)."
admitted_context_inputs:
  - standard Rindler coordinate construction (basic SR)
  - Bisognano-Wichmann modular argument (admitted-context)
  - Wick-rotation regularity (already paid for by Block 02 / upstream Wald-Noether)
upstream_dependencies:
  - block_01_kms_condition (this PR's stacked base)
  - lorentz_kernel_positive_closure_note (retained)
  - emergent_lorentz_invariance_note (retained)
  - anomaly_forces_time_theorem (retained)
runner_classified_passes: 5 PASS at machine precision (Wick-rotation period 2π, T_U sweep, SI Earth gravity ~4×10⁻²⁰ K, universal 1/(2π), Bisognano-Wichmann Δ = exp(-2πK))
```

## Why bounded_theorem

The Bisognano-Wichmann modular argument is admitted-context input. Same
admission already paid for by Block 02 (Hawking T_H) for analogous Wick-
rotation reasoning. `bounded_theorem` honestly captures this.

## Audit handoff

Audit status is set only by the independent audit lane. Review-loop does not
prefill an `audit_status` or promise an `effective_status`; after any clean
independent audit, the pipeline derives effective status from `claim_type` plus
dependency closure. If upstream deps remain non-retained-grade, the row remains
pending/blocked until those deps are repaired and audited.

## Dependency chain status snapshot (2026-05-02)

| Dep | Today's `effective_status` |
|---|---|
| Block 01 KMS | proposed_retained |
| Lorentz kernel + emergent Lorentz | retained |

## Review-loop disposition

- branch-local self-review: `pass` (5/5 tests; Earth-gravity Unruh
  ~4×10⁻²⁰ K matches textbook).
- formal Codex audit: pending.

## Audit hand-off

This block completes the framework's horizon-temperature theorem family
together with Block 02 (Hawking T_H). The Bisognano-Wichmann result (U4)
largely subsumes what would be a separate Block 11.
