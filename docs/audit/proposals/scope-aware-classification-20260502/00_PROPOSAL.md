# Scope-Aware Audit Classification — Proposal

**Date:** 2026-05-02
**Type:** architecture proposal for `docs/audit/`
**Status:** awaiting independent review.

## What is being proposed

Replace the current two-axis system

```
author-declared current_status × auditor-set audit_status → effective_status
```

with a single auditor-controlled two-field classification

```
auditor-set claim_type × auditor-set audit_status → effective_status
```

where:

- `claim_type ∈ {positive_theorem, bounded_theorem, no_go, open_gate, decoration, meta}`
  describes *what kind of claim* the note is making.
- `audit_status` retains its current vocabulary — it describes *whether the
  proof closes* for the stated scope.

Both fields are set by the independent auditor (Codex GPT-5.5 by default).
Authors no longer self-assign tiers. The author writes the science; the
auditor records what the science actually accomplishes.

The retained library that the audit lane outputs becomes:

- `retained` — clean positive theorems
- `retained_no_go` — clean negative-result theorems and ratified failed
  archived attempts
- `retained_bounded` — clean theorems with explicit narrow scope (new tier)

Plus the existing terminal demotion verdicts (`audited_renaming`,
`audited_conditional`, `audited_decoration`, `audited_failed`,
`audited_numerical_match`) and the transient `proposed_retained` state for
clean rows whose dependencies are still unaudited.

## Why

Three concrete problems with the current model.

### Problem 1 — author tier creates clean-audited paperwork backlog

As of 2026-05-02, the audit ledger has 122 rows at
`current_status = support` AND `audit_status = audited_clean`. Their
`effective_status` is held at `support` only because the author has not
relabeled the source-note `Status:` line to `proposed_retained`. The audit is
already clean. The chain is already clean. The author tier is the only thing
preventing the row from propagating to `retained`.

Yesterday's 24-hour axiom-first derivation campaign produced 10 such rows in
one session. Each is genuine first-principles work; each is held at `support`
solely because the upstream chain (RP, spectrum cond, cluster decomp,
spin-statistics) is in the same paperwork-stuck state.

This is not a defensible safety property. It is a paperwork bottleneck.

### Problem 2 — author tier and audit verdicts overlap on the failure modes

The audit lane was built (`docs/audit/README.md`) to catch four CKM-style
failure modes:

| Failure mode | Audit verdict that catches it | Does author tier add a check? |
|---|---|---|
| Definition-as-derivation | `audited_renaming` | No |
| Conditional-on-open-work | `audited_conditional` | No |
| Algebraic decoration | `audited_decoration` | No |
| Numerical match at tuned input | `audited_numerical_match` | No |

The author tier provides no independent defense against any of the four
patterns the audit lane was created to catch. It is mechanically redundant.

### Problem 3 — bounded and open work get tagged ambiguously

The current vocabulary has both `bounded` and `audited_conditional` and they
mean different things:

- `bounded` (author-declared) — "I am only claiming this narrow thing."
- `audited_conditional` (audit verdict) — "the chain depends on a
  support/open upstream that has not closed."

A bounded note that *cleanly proves what it claims to prove* gets
`current_status = bounded` and `audit_status = audited_clean` and an
`effective_status = bounded` that under-states what was actually shown. The
note is honest, the audit is clean, but the publication-facing tier suggests
incompleteness rather than correctness within scope.

Same problem for `open` — currently used both for "active gate not yet
closed" (problem statement) and for "I'm not sure if my proof closes"
(verdict-pending).

## What we keep

This proposal preserves every defense the current audit lane provides:

- **Citation graph computation** (`build_citation_graph.py`): topology only,
  unchanged.
- **Criticality computation** (`compute_load_bearing.py`): topology only,
  unchanged.
- **Cross-confirmation for critical claims** (250+ descendants): two
  independent auditors must match on `verdict` *and* `load_bearing_step_class`
  *and* (new) `claim_type`. Same escalation to a third auditor on
  disagreement.
- **Independence requirements** (`FRESH_LOOK_REQUIREMENTS.md`): unchanged.
  Claude cannot audit Claude. Codex GPT-5.5 remains the designated
  cross-family auditor.
- **Hash-drift invalidation**: unchanged. Note edits trigger re-audit.
- **Decoration boxing under parent**: unchanged in policy
  (`ALGEBRAIC_DECORATION_POLICY.md`); now visible in `claim_type` enum.
- **`previous_audits` history**: unchanged. Audit trail preserved.
- **Author dispute → third-auditor escalation**: unchanged.
- **Stale narrative archival** (`STALE_NARRATIVE_POLICY.md`): unchanged.

## What we drop

- `current_status` field on audit ledger rows — removed.
- `Status:` line on source notes — stripped (or replaced by an optional
  one-token `audit-pending` marker that the pipeline maintains).
- The 8-value author-tier vocabulary (`support`, `bounded`, `open`,
  `unknown`, `proposed_retained`, `proposed_promoted`, `proposed_no_go`,
  `proposed_bounded`) — replaced by the 6-value auditor-set `claim_type`
  enum.
- The author's "I'm staking the paper on this" implicit signal — moves to
  paper layer (separately, when papers are written; not part of this
  proposal).

## What changes for the science workflow

### Author writing a new note

Author writes the note describing the proof and the scope of the claim.
Optionally adds a single-line hint at the top:

```markdown
Type: positive_theorem      # or bounded_theorem / no_go / open_gate / decoration / meta
```

The hint is not authoritative. The auditor reads the note body and may
override it.

The author no longer writes `Status: support` or `Status: proposed_retained`.

### Auditor (Codex GPT-5.5 by default)

Existing audit prompt asks: load-bearing step? chain closes? what does the
runner actually check? verdict?

Two new questions added:

> What is the claim type? Pick from {positive_theorem, bounded_theorem,
> no_go, open_gate, decoration, meta}.
>
> Does the note's stated scope match what the proof actually closes for? If
> not, what scope does the proof actually close for?

The auditor records `claim_type` and (when it differs) the actual
`claim_scope`. If the note over-claims (says positive_theorem but only proves
a bounded sub-claim), the audit returns `audited_conditional` with the
bounded scope as the repair target.

### Critical claims still require cross-confirmation

For a `critical` row (250+ descendants), two independent auditors must agree
on:

- `verdict` (already)
- `load_bearing_step_class` (already)
- `claim_type` (new)

Disagreement on any of these escalates to a third auditor. This makes
`claim_type` a first-class part of the cross-confirmed audit, not an
auditor-side annotation.

### Reclassification

Reclassification is the natural output of any audit. If a note that was
previously `claim_type = positive_theorem, audited_clean` is re-audited (e.g.
because the note hash changed) and the new audit returns `claim_type =
bounded_theorem, audited_clean`, the row's `effective_status` is recomputed
and downstream rows propagate the demotion via the existing monotone-down
inheritance rule. No special reclassification protocol — it's just an audit
verdict change.

The author's choices when the audit returns a narrower scope than they
intended:

| Auditor finds | Author can | Mechanic |
|---|---|---|
| Note over-claims | edit note to narrow scope | hash drift triggers re-audit |
| Note over-claims | extend proof to cover full scope | hash drift triggers re-audit |
| Note over-claims | accept the bounded reclassification | no edit needed; row sits at the narrower tier |

## What this looks like end-to-end

```
                          author writes note
                                  │
                                  ▼
                       (optional Type: hint)
                                  │
                                  ▼
                          pipeline picks up
                                  │
                                  ▼
                  build_citation_graph.py runs
                                  │
                                  ▼
              criticality computed (topology-only)
                                  │
                                  ▼
                   audit agent (Codex GPT-5.5)
                  reads note + 1-hop deps + runner
                                  │
                                  ▼
              returns: claim_type, claim_scope,
                       audit_status, load-bearing
                       step + class, runner check
                       breakdown, verdict_rationale
                                  │
                                  ▼
              if criticality = critical: cross-confirm
                                  │
                                  ▼
                  apply_audit.py writes row
                                  │
                                  ▼
              compute_effective_status.py propagates
                                  │
                                  ▼
              retained library updated automatically
```

No author relabel step. No paperwork bottleneck. No schema gate that an
audit-clean chain can fail to cross.

## Anchor file

The full drop-in replacement for the audit agent prompt template is in
[`PROPOSED_AUDIT_AGENT_PROMPT_TEMPLATE.md`](PROPOSED_AUDIT_AGENT_PROMPT_TEMPLATE.md).
That is the single most-important file change. Everything else flows from it.
