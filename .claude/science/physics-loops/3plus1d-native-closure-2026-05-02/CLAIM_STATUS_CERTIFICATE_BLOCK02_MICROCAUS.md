# Claim Status Certificate — Block 02 (Route b) — Microcausality / Lieb-Robinson

**Block:** 02
**Route:** (b)
**Date:** 2026-05-02
**Branch:** `claude/axiom-first-rp-microcausality-elevate-2026-05-02`
**Note:** `docs/AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md`
**Runner:** `scripts/axiom_first_microcausality_check.py`
**Runner result:** PASS (T1, T2, T3, T4 all PASS — strict locality, Lieb-Robinson bound, lightcone decay, t^d small-t scaling)

## Status fields

```yaml
actual_current_surface_status: support
target_claim_type: positive_theorem
conditional_surface_status: |
  branch-local theorem note on A_min + retained RP transfer matrix
  + retained spectrum-condition + retained cluster-decomposition
  + retained emergent Lorentz invariance; runner passing on 1D toy
  chain (4/4 tests PASS); ready for independent audit; will resolve
  to retained_pending_chain post-audit until upstream RP and
  spectrum-condition rows reach effective_status: retained.
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: |
  Per physics-loop SKILL retained-proposal certificate item 4, a chain
  of support cannot promote to proposed_retained until all dependencies
  are ratified retained on the current authority surface. RP and
  spectrum-condition are currently effective_status: unaudited (RP was
  audited_clean and was invalidated by criticality_increased; spectrum
  has not yet been audited). Microcausality is therefore queue-blocked
  on RP + spectrum-condition reaching retained-grade.
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Dependency analysis

Listed deps (per ledger):

- `axiom_first_reflection_positivity_theorem_note_2026-04-29` — currently `unaudited` (was `audited_clean`, invalidated). Block 01 of this PR makes it audit-ready.
- `axiom_first_spectrum_condition_theorem_note_2026-04-29` — `unaudited`.
- `lorentz_kernel_positive_closure_note` — `unaudited`.
- `emergent_lorentz_invariance_note` — `audited_conditional`.
- `axiom_first_cluster_decomposition_theorem_note_2026-04-29` — `unaudited`.
- `minimal_axioms_2026-04-11` — `meta` (allowed).

Until all dep statuses reach `retained` / `retained_no_go` / `retained_bounded`, the row's `compute_effective_status.py` outcome will be `retained_pending_chain` — that is the honest target for this iteration.

## What this block contributes

1. Note hygiene: explicit `Type:` / `Claim type:` / `Claim scope:`
   metadata; load-bearing-step class explicitly named (C); status
   tightened from "awaiting independent audit" to "audit-ready
   (chain closure requires upstream RP and spectrum-condition rows
   to be retained-grade first)".
2. Branch lineage clarified ("current branch: ..." + original
   physics-loop branch).
3. The runner is verified to pass and statically classifies as
   dominant_class C (6 hits, no D). This is the right signal for a
   first-principles compute.

## Independent audit requirement

YES — required. Expected verdict on first audit, given the proof's
soundness: `audited_clean` with `load_bearing_step_class: C`
(eigenvalue / Hamiltonian-construction / Heisenberg-evolution
compute) and `chain_closes: true`. Effective status resolves to
`retained_pending_chain` on first audit, then to `retained` once the
six upstream deps are all retained-grade.

## Review-loop disposition

Hygiene-only: pass for the audit-readiness goal. No new derivation,
no new load-bearing step, no new runner. Status changes are
metadata-only and do not affect the science argument.

## Imports retired or newly exposed

- None retired.
- None newly exposed.

## Open imports / blockers

- RP retained (Block 01 in flight; will be retained on next Codex
  audit since deps=[]).
- Spectrum condition retained (separate row; not part of this PR).
- Cluster decomposition retained (separate row; not part of this PR).
- Lorentz kernel positive closure retained (separate row; not part
  of this PR).
- Emergent Lorentz invariance — currently `audited_conditional`;
  will need a new audit cycle to upgrade to retained-bounded or
  retained.

## Next exact action

Push branch, open PR. Request Codex audit of:
1. `axiom_first_reflection_positivity_theorem_note_2026-04-29` (Block 01 - this PR)
2. `axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01` (Block 02 - this PR)
3. (separately) the four upstream support notes listed above.
