# Loop Goal — 3+1D Native Closure (Iter 2: Routes a + b)

**Slug:** `3plus1d-native-closure-2026-05-02`
**Iteration:** 2 (parallel to iter 1 working routes c+d)
**Date:** 2026-05-02
**Worker branch:** `claude/axiom-first-rp-microcausality-elevate-2026-05-02`

## Drive `anomaly_forces_time_theorem` toward retained-positive closure

Iter 1 owns:
- Route (c): lattice Wess-Zumino theorem
- Route (d): gauge-broken implication

Iter 2 (this loop) owns the upstream review/hygiene rows that must be
retained-clean to serve as inputs:

- **Route (a):** `axiom_first_reflection_positivity_theorem_note_2026-04-29`
  - Currently `effective_status=unaudited` (was `audited_clean`,
    invalidated by `criticality_increased:leaf->medium`).
  - Dependencies: `deps=[]`, no chain blockers.
  - Target outcome: ledger row audit-ready and queue-positioned for
    Codex re-audit; runner classified PASS lines visible.

- **Route (b):** `axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01`
  - Currently `effective_status=unaudited`.
  - Dependencies: 6 rows (RP, spectrum-condition, lorentz_kernel,
    emergent_lorentz_invariance, cluster_decomposition, minimal_axioms).
  - Target outcome: ledger row audit-ready; will resolve to
    `retained_pending_chain` until upstream deps are retained-grade.

## Honest scope for this iteration

The audit verdict (`audited_clean` → `retained`) is owned by independent
auditors (Codex GPT-5.5 via the AUDIT_AGENT_PROMPT_TEMPLATE.md path).
This iteration cannot mechanically promote these rows to
`effective_status=retained`. What it CAN do:

1. Tighten note Status / scope / load-bearing-step language so Codex
   re-audit lands `audited_clean` cleanly with `chain_closes=true` and
   explicit class-C runner classification.
2. Confirm runners pass and emit classified PASS lines.
3. Set `Type:` / `Claim type:` metadata fields to remove ambiguity.
4. Run the audit pipeline; verify `audit_lint OK`.
5. Land scope-tight notes on a review branch and open a PR so Codex can
   re-audit.

Honest target effective_status by the close of this iteration:

- Route (a): `unaudited` -> ready for re-audit; will become `retained`
  on next Codex pass since `deps=[]` and prior audit was already
  `audited_clean` class-C.
- Route (b): `unaudited` -> ready for audit; will become
  `retained_pending_chain` after Codex audit (depends on RP +
  spectrum-condition + cluster + lorentz being retained first).

## Stop condition

- Both notes hygiene-clean and runner-passing.
- `bash docs/audit/scripts/run_pipeline.sh` reports audit_lint OK.
- PR opened for Codex review.
- Honest "what's needed to land retained-clean" recorded in HANDOFF.md.
