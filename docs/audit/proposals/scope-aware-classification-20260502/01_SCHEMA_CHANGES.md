# Schema Changes — Audit Ledger Row

**Date:** 2026-05-02

## Per-row fields, before vs after

### Removed

| Field | Type | Today | Removed because |
|---|---|---|---|
| `current_status` | enum (8 values) | author-declared author tier | superseded by auditor-set `claim_type` |

### Added

| Field | Type | Set by | Purpose |
|---|---|---|---|
| `claim_type` | enum (6 values: see below) | auditor | what kind of claim is this |
| `claim_scope` | string (free text) | auditor | the precise statement the proof closes for, if it differs from the note's framing |

### Modified

| Field | Today | After |
|---|---|---|
| `effective_status` | enum (~12 values) | enum (~10 values; `support`/`bounded`/`open` removed; `retained_bounded` added — see [`02_PROPAGATION_RULES.md`](02_PROPAGATION_RULES.md)) |

### Unchanged

All of the following stay exactly as they are:

- `claim_id`
- `note_path`
- `note_hash`
- `dependencies` (one-hop citations)
- `audit_status` (vocabulary unchanged)
- `auditor`, `auditor_family`, `independence`
- `criticality` (topology-driven, unchanged)
- `direct_in_degree`, `transitive_descendants`
- `load_bearing_step`, `load_bearing_step_class`
- `chain_closes`, `chain_closure_explanation`
- `runner_check_breakdown`, `runner_classification`
- `decoration_parent_claim_id`
- `verdict_rationale`
- `auditor_confidence`, `notes_for_re_audit_if_any`
- `open_dependency_paths`
- `previous_audits` (history)
- `cross_confirmation` (status, paired auditors)

## `claim_type` enum

| Value | Meaning | Example claims under recent campaigns |
|---|---|---|
| `positive_theorem` | Full closure of a positive statement on the retained authority surface. | RP, spectrum cond, cluster decomp, spin-statistics axiom-first notes; Block 01 KMS; Block 04 microcausality |
| `bounded_theorem` | Narrow / region-restricted positive closure with explicit boundary. The note is honest about what it does and does not claim. | BH 1/4 Wald-Noether composition; Block 02 Hawking T_H (conditional on Killing-horizon admission); DM eta freezeout-bypass |
| `no_go` | Proven negative result. Symmetric to `positive_theorem` but for impossibility statements. | Charged-lepton direct Ward-free Yukawa no-go; AREA_LAW_*_NO_GO_NOTE family |
| `open_gate` | Problem statement, partial reduction, or stretch attempt with named remaining residual. Honestly not a closure. | Koide stretch attempts; Hubble C1 carrier-metrology audit; neutrino quantitative work-in-progress |
| `decoration` | Algebraic consequence of a single upstream parent with no new physical content. Boxed under parent. | Most "M_β² = m₂² + …" style consequence-of-consequence rows |
| `meta` | README, lane index, methodology note, navigation surface — not an audit target. | `docs/lanes/*/README.md`, `docs/repo/REPO_ORGANIZATION.md`, the 985 currently-`unknown` overview rows |

Pinning these at the auditor side means the publication-table renderer can
say "show me all `positive_theorem` rows that are `effective_status =
retained`" without needing to consult any author tier.

## Concrete row example, before and after

### Before (today's ledger row for `axiom_first_reflection_positivity_theorem_note_2026-04-29`)

```json
{
  "claim_id": "axiom_first_reflection_positivity_theorem_note_2026-04-29",
  "note_path": "docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md",
  "note_hash": "abc123...",
  "current_status": "support",
  "dependencies": ["minimal_axioms_2026-04-11"],
  "audit_status": "audited_clean",
  "auditor": "codex-audit-loop:leaf-bottomup-2026-04-30",
  "auditor_family": "codex-current",
  "independence": "cross_family",
  "load_bearing_step": "Axiom-First Reflection Positivity for the Canonical CL3-on-Z3 Action: ...",
  "load_bearing_step_class": "C",
  "chain_closes": true,
  "runner_check_breakdown": {"A": 0, "B": 0, "C": 21, "D": 0, "total_pass": 21},
  "decoration_parent_claim_id": null,
  "criticality": "high",
  "direct_in_degree": 5,
  "transitive_descendants": 47,
  "effective_status": "support"
}
```

### After (same row, recomputed under proposal)

```json
{
  "claim_id": "axiom_first_reflection_positivity_theorem_note_2026-04-29",
  "note_path": "docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md",
  "note_hash": "abc123...",
  "dependencies": ["minimal_axioms_2026-04-11"],
  "audit_status": "audited_clean",
  "claim_type": "positive_theorem",
  "claim_scope": "RP holds for canonical staggered Cl(3)-on-Z^3 action at g_bare=1; (R1)-(R4) on A_min",
  "auditor": "codex-audit-loop:leaf-bottomup-2026-04-30",
  "auditor_family": "codex-current",
  "independence": "cross_family",
  "load_bearing_step": "Axiom-First Reflection Positivity for the Canonical CL3-on-Z3 Action: ...",
  "load_bearing_step_class": "C",
  "chain_closes": true,
  "runner_check_breakdown": {"A": 0, "B": 0, "C": 21, "D": 0, "total_pass": 21},
  "decoration_parent_claim_id": null,
  "criticality": "high",
  "direct_in_degree": 5,
  "transitive_descendants": 47,
  "effective_status": "retained"
}
```

`current_status` removed; `claim_type` and `claim_scope` added; nothing else
changed; `effective_status` propagates to `retained` because the chain
(rooted at `minimal_axioms_2026-04-11` which is itself eligible for
`retained`) is clean.

## JSON schema impact

Schema version bumps from current to next. The migration script
([`06_MIGRATION_PLAN.md`](06_MIGRATION_PLAN.md)) writes both old and new
fields during the transition window, then strips old fields after rollout
is verified.
