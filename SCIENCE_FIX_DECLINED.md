# SCIENCE_FIX_DECLINED — dm_wilson_direct_descendant_schur_feshbach_boundary_variational_theorem_note_2026-04-25

**Claim ID:** `dm_wilson_direct_descendant_schur_feshbach_boundary_variational_theorem_note_2026-04-25`
**Note:** `docs/DM_WILSON_DIRECT_DESCENDANT_SCHUR_FESHBACH_BOUNDARY_VARIATIONAL_THEOREM_NOTE_2026-04-25.md`
**Runner:** `scripts/frontier_dm_wilson_direct_descendant_schur_feshbach_boundary_variational.py`

## Why declined

The science-fix prompt at
`/tmp/science-fix-2026-05-16/b6-dm-wilson-direct-descendant-schur-feshbach-boundary-variatio/PROMPT.md`
targets this note as `category: open_gate`, `claim_type: open_gate`, drawn from the
`MISSING_DERIVATION_PROMPTS.md` / `missing_derivation_difficulty.json` snapshot.

The current `docs/audit/data/audit_ledger.json` `rows[claim_id]` entry — which is the
load-bearing structured audit record, not the prompt-generator snapshot — shows the
claim is already cross-confirmed retained at retained-grade. Key fields from that row:

| field | value |
|---|---|
| `intrinsic_status` | `retained` |
| `effective_status` | `retained` (reason: `self`) |
| `claim_type` | `positive_theorem` (provenance: `audited`) |
| `chain_closes` | `true` |
| `load_bearing_step_class` | `A` |
| `cross_confirmation.status` | `confirmed` |
| `deps` | `[]` |
| `note_hash` | `48293be312e68e18b7df06fef4348069e9dd05889f09cb538f5f2842dc343fac` |

The on-disk note's SHA-256 hash matches `note_hash` exactly, so no note-text drift
has invalidated the audit since 2026-05-07.

## Three independent audits already converged

`previous_audits` plus the current cross-confirmation block record three independent
fresh-context audits, all reaching `audited_clean`, `chain_closes: true`, class `A`:

1. **2026-05-02** — `claude-opus-4.7-1m:open-gates-2026-05-02-c1-01`, high
   confidence. Invalidation reason `criticality_increased:high->critical` (i.e.,
   re-audit requirement triggered by descendant count rising, not by scope error).
2. **2026-05-07 first audit** —
   `codex-gpt-5.5-xhigh-dm-wilson-schur-feshbach-audit-1-2026-05-07`,
   fresh_context, `audited_clean`, class A.
3. **2026-05-07 second audit (current)** —
   `codex-gpt-5.5-xhigh-dm-wilson-schur-feshbach-audit-2-2026-05-07`,
   fresh_context, `audited_clean`, class A, high confidence. Cross-confirmation
   block records `status: confirmed` against audit 2.

The 2026-05-07 second auditor's recorded rationale already addresses the
prompt's stated concern: "The finite-dimensional algebra closes under the
note's explicit hypotheses: invertible F and L_e for the resolvent identity,
and D_- = D_-^* > 0 for the variational and monotonicity statements... The
runner consistently checks exact Schur/Feshbach/Dirichlet algebra and scope
hygiene, with 46 PASS and 0 FAIL in the supplied live summary. Residual risk
is limited to scope discipline."

## Note contents are a closed algebraic chain

The note itself is a four-theorem-plus-four-corollary chain, each with an
explicit proof and `QED`. The load-bearing step quoted by the auditor —

> The exact Schur factorization gives `I_e^* D_-^(-1) I_e = L_e^(-1)`, and
> under `D_- = D_-^* > 0` the completed-square identity gives
> `u^* L_e u = min_v [u; v]^* D_- [u; v]`.

— is finite-dimensional block linear algebra and a positive-definite quadratic
completion, with no imported physical bridge. The four reviewer-pressure
clauses explicitly disclaim DM-selector closure, microscopic `D_-` evaluation,
Wilson-native support construction, and any final flagship-lane closure.

The "What this does not close" section enumerates the exact open items
(microscopic `D_-` evaluation from `Cl(3)` on `Z^3`, Wilson-native support,
right-sensitive selector, 3-real source fiber, final DM lane) — all of which
live on sibling notes, not on this one. There is no orphaned bridge or hidden
claim inside the scoped finite-dimensional theorem.

## Runner is currently green

A live run of `scripts/frontier_dm_wilson_direct_descendant_schur_feshbach_boundary_variational.py`
on this worktree printed:

```
PASSED: 46/46
FAILED: 0/46
DM_WILSON_DIRECT_DESCENDANT_SCHUR_FESHBACH_BOUNDARY_VARIATIONAL=TRUE
DM_BOUNDARY_RESOLVENT_CERTIFICATE=TRUE
DM_POSITIVE_DIRICHLET_CERTIFICATE=TRUE
DM_MICROSCOPIC_D_MINUS_EVALUATED_BY_THIS_THEOREM=FALSE
DM_FINAL_SELECTOR_CLOSED_BY_THIS_THEOREM=FALSE
DM_FLAGSHIP_LANE_CLOSED_BY_THIS_THEOREM=FALSE
```

The runner's class breakdown in `docs/audit/data/runner_classification.json`
matches the audit verdict: 21 A-class plus 4 B-class checks, zero C/D, no
assert-based skips. Package-wiring sub-block (9 checks) confirms the note is
linked from every canonical harness and ci3_z3 publication-matrix index file,
and the negative-closure flag is asserted (no forbidden final-DM-closure flag
set).

## Source of the prompt's stale `open_gate` field

`docs/audit/data/missing_derivation_difficulty.json` `ratings[claim_id]`
carries `"category": "open_gate"` and labels the difficulty `"easy"` with
reason "The missing derivation is a standard Schur-complement identity and
quadratic completion already backed by passing checks." This snapshot
pre-dates the 2026-05-07 dual audit reclassifying the note as
`positive_theorem` / retained, and the generator that produces
`MISSING_DERIVATION_PROMPTS.md` reads from this stale snapshot rather than
from `audit_ledger.json::rows`. The downstream prompt-generation pipeline is
the appropriate place to fix the discrepancy, not the audited note or its
runner.

## What is and is not in this PR

This PR contains only this `SCIENCE_FIX_DECLINED.md` at the worktree root.

- No `docs/**` modified.
- No `scripts/**` modified.
- No `docs/audit/**` modified (no audit-data writes).
- No publication-control-plane indexes touched.
- No verdict claimed on behalf of an auditor.
- No retained-tier promotion claimed.

The intent is to surface the stale prompt for human triage and record the
ledger-vs-prompt mismatch, not to assert a new audit outcome.
