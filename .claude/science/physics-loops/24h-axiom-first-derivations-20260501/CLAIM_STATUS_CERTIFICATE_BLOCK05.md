# Claim Status Certificate — Block 05 (First law of BH mechanics)

**Date:** 2026-05-01 (originally) / 2026-05-02 (reframed under scope-aware classification)
**Block:** 05 — first law of BH mechanics dM = T_H dS_BH
**Slug:** `24h-axiom-first-derivations-20260501`
**Branch:** `physics-loop/24h-axiom-first-block05-firstlaw-20260501`
**Stacked PR base:** `physics-loop/24h-axiom-first-block02-hawking-20260501`
**Note:** [docs/AXIOM_FIRST_FIRST_LAW_BH_MECHANICS_THEOREM_NOTE_2026-05-01.md](../../../../docs/AXIOM_FIRST_FIRST_LAW_BH_MECHANICS_THEOREM_NOTE_2026-05-01.md)
**Runner:** [scripts/axiom_first_first_law_bh_mechanics_check.py](../../../../scripts/axiom_first_first_law_bh_mechanics_check.py)
**Log:** [outputs/axiom_first_first_law_bh_mechanics_check_2026-05-01.txt](../../../../outputs/axiom_first_first_law_bh_mechanics_check_2026-05-01.txt)

## Framework

Reframed under scope-aware classification (audit-lane proposal #291).

## Author classification (non-authoritative hint to auditor)

```yaml
claim_type_author_hint: bounded_theorem
claim_scope: "For stationary axially-symmetric solutions of the framework's GR action with non-degenerate Killing horizon, dM = T_H dS_BH + Ω_H dJ + Φ_H dQ (F1)-(F2); Smarr formula M = 2 T_H S_BH + 2 Ω_H J + Φ_H Q (F3); Schwarzschild specialization dM = (κ/8πG) dA recovered exactly (F4)."
admitted_context_inputs:
  - Wald-Noether identity (already admitted by upstream BH 1/4)
  - ADM mass identification (standard stationary GR)
  - Bardeen-Carter-Hawking 1973 integrability argument (admitted-context)
upstream_dependencies:
  - block_02_hawking_temperature (this PR's stacked base)
  - bh_quarter_wald_noether_framework_carrier_theorem_note_2026-04-29 (audited_conditional today)
  - universal_gr_discrete_global_closure_note (retained)
runner_classified_passes: 6 PASS (dM = T_H dS_BH at finite-diff precision; Smarr at <1e-12; integral form at <1e-15; negative specific heat verified)
```

## Why bounded_theorem

Inherits Block 02's bounded scope (Killing-horizon admission) plus admits
the Bardeen-Carter-Hawking 1973 integrability argument as load-bearing
admitted-context. `bounded_theorem` honestly captures the chain.

## Expected `effective_status` after audit

If Codex returns `audit_status = audited_clean` and `claim_type =
bounded_theorem`:

- **Path A** (Block 02 reaches retained_bounded AND BH 1/4 promotes):
  `effective_status = retained_bounded`.
- **Path B** (any upstream still pending): `effective_status =
  proposed_retained` (transient).

## Dependency chain status snapshot (2026-05-02)

| Dep | Today's `effective_status` |
|---|---|
| Block 02 Hawking T_H | proposed_retained (pending Block 01 + BH 1/4) |
| BH 1/4 carrier | audited_conditional |
| Framework GR action | retained |

## Review-loop disposition

- branch-local self-review: `pass` (6/6 tests; Schwarzschild dM = T_H dS_BH
  at finite-diff precision).
- formal Codex audit: pending.

## Audit hand-off

Block 05 is the second-to-last node in the BH thermodynamics chain.
Successful clean audit unlocks Block 10 (GSL) for promotion.
