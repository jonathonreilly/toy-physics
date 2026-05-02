# Claim Status Certificate — Block 02 (Hawking temperature)

**Date:** 2026-05-01 (originally) / 2026-05-02 (reframed under scope-aware classification)
**Block:** 02 — Hawking T_H = κ/(2π) from Wick-rotated Killing horizon + KMS
**Slug:** `24h-axiom-first-derivations-20260501`
**Branch:** `physics-loop/24h-axiom-first-block02-hawking-20260501`
**Stacked PR base:** `physics-loop/24h-axiom-first-block01-kms-20260501`
**Note:** [docs/AXIOM_FIRST_HAWKING_TEMPERATURE_THEOREM_NOTE_2026-05-01.md](../../../../docs/AXIOM_FIRST_HAWKING_TEMPERATURE_THEOREM_NOTE_2026-05-01.md)
**Runner:** [scripts/axiom_first_hawking_temperature_check.py](../../../../scripts/axiom_first_hawking_temperature_check.py)
**Log:** [outputs/axiom_first_hawking_temperature_check_2026-05-01.txt](../../../../outputs/axiom_first_hawking_temperature_check_2026-05-01.txt)

## Framework

Reframed under scope-aware classification (audit-lane proposal #291).

## Author classification (non-authoritative hint to auditor)

```yaml
claim_type_author_hint: bounded_theorem
claim_scope: "For any non-degenerate Killing horizon of surface gravity κ on the framework's retained discrete GR action surface, the regular Wick-rotated Euclidean continuation has period β_th = 2π/κ; equivalently the asymptotic state is Hartle-Hawking-Israel Gibbs at T_H = κ/(2π) (H1)-(H4). Conditional on admitted-context Killing-vector / surface-gravity / Wick-rotation-regularity vocabulary already paid for by the retained Wald-Noether composition."
admitted_context_inputs:
  - surface gravity κ definition (already admitted by upstream BH 1/4)
  - Wick-rotation regularity at the bolt (already admitted by upstream BH 1/4)
  - asymptotic-time identification (standard stationary GR)
upstream_dependencies:
  - block_01_kms_condition (this PR's stacked base)
  - bh_quarter_wald_noether_framework_carrier_theorem_note_2026-04-29 (audited_conditional today)
  - universal_gr_discrete_global_closure_note (retained)
  - universal_qg_canonical_textbook_geometric_action_equivalence_note (retained)
runner_classified_passes: 6 PASS at machine precision (Wick-rotation periodicity, Schwarzschild benchmark, first-law differential, Rindler preview)
```

## Why bounded_theorem

The Killing-horizon / Wick-rotation-regularity vocabulary is admitted-
context — it's the same admission already paid for by the retained Wald-
Noether composition, but it's load-bearing for the claim. `bounded_theorem`
honestly captures this. The bound becomes the canonical `claim_scope`.

## Expected `effective_status` after audit

If Codex returns `audit_status = audited_clean` and `claim_type =
bounded_theorem`:

- **Path A** (Block 01 promotes to retained AND BH 1/4 promotes to
  retained_bounded): `effective_status = retained_bounded`.
- **Path B** (any upstream still pending): `effective_status =
  proposed_retained` (transient).

## Dependency chain status snapshot (2026-05-02)

| Dep | Today's `effective_status` |
|---|---|
| Block 01 KMS | proposed_retained (pending RP + spectrum cond) |
| BH 1/4 carrier | audited_conditional (gating) |
| Framework GR action | retained |

## Review-loop disposition

- branch-local self-review: `pass` (6/6 tests; Schwarzschild T_H = 1/(8πGM)
  recovered exactly).
- formal Codex audit: pending under new prompt template.

## Audit hand-off

Block 02 opens the BH thermodynamics chain. Successful clean audit unlocks
Block 05 (first law) and Block 10 (GSL).
