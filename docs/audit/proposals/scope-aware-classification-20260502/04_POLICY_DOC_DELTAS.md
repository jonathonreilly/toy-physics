# Policy Doc Deltas

**Date:** 2026-05-02

This document specifies edits to four live policy docs that the proposal
would land. Each delta is presented as a before/after with a brief rationale
so the reviewer can evaluate the edits without applying them.

The four docs:

1. [`docs/audit/README.md`](../../README.md)
2. [`docs/audit/FRESH_LOOK_REQUIREMENTS.md`](../../FRESH_LOOK_REQUIREMENTS.md)
3. [`docs/audit/AUDIT_AGENT_PROMPT_TEMPLATE.md`](../../AUDIT_AGENT_PROMPT_TEMPLATE.md) — full replacement; see
   [`PROPOSED_AUDIT_AGENT_PROMPT_TEMPLATE.md`](PROPOSED_AUDIT_AGENT_PROMPT_TEMPLATE.md) in this directory
4. [`docs/repo/CONTROLLED_VOCABULARY.md`](../../../repo/CONTROLLED_VOCABULARY.md)

---

## 1. `docs/audit/README.md`

### Section: "Status fields and the propose / ratify split"

**Replace with:** "Status fields and the auditor-set classification."

#### Before

> Three parallel fields per claim:
>
> - `current_status` — what the source note declares. Authors may set:
>   - `proposed_retained` — "I have done the science work and believe this should be retained, pending audit."
>   - `proposed_no_go` — "I have proven a no-go theorem..."
>   - `proposed_promoted`, `proposed_bounded` — same idea for those tiers.
>   - `support`, `open` — unchanged; these do not require audit ratification.
> - `audit_status` — what the audit found. Set only by the audit lane: …
> - `effective_status` — derived. The publication-facing tables read this: …

#### After

> Two parallel fields per claim, both set by the independent auditor:
>
> - `claim_type` — what kind of claim this note is making. Set by the
>   auditor from note content. One of:
>   - `positive_theorem` — full closure of a positive statement.
>   - `bounded_theorem` — narrow / region-restricted positive closure with
>     explicit boundary recorded as `claim_scope`.
>   - `no_go` — proven negative result.
>   - `open_gate` — partial result or stretch attempt with a named
>     remaining residual; never propagates to retained.
>   - `decoration` — algebraic consequence of a single upstream parent
>     with no new physical content; boxed under parent.
>   - `meta` — README, lane index, methodology note; not an audit target.
> - `audit_status` — whether the proof closes for the stated `claim_type`.
>   Set only by the audit lane:
>   - `unaudited`, `audit_in_progress`, `audited_clean`, `audited_renaming`,
>     `audited_conditional`, `audited_decoration`, `audited_failed`,
>     `audited_numerical_match` (vocabulary unchanged).
>
> Plus a third derived field:
>
> - `effective_status` — computed by `compute_effective_status.py`. The
>   publication-facing surface reads this. See
>   `proposals/scope-aware-classification-20260502/02_PROPAGATION_RULES.md`.
>
> Authors no longer write `Status:` lines on source notes. The auditor
> reads the note body, classifies it, and records both fields.

### Section: "The hard rules"

#### Before (rule 1)

> 1. **`retained` is audit-only.** No author may directly write `retained`
>    as `current_status`. The strongest author-settable state is
>    `proposed_retained`. … Only proposed rows can promote publication-facing
>    status: the audit lane may grant `effective_status = retained` only when
>    this row's `current_status = proposed_retained`, this row's
>    `audit_status = audited_clean`, and every dependency's
>    `effective_status = retained`. A clean `support`, `bounded`, `open`, or
>    `unknown` row keeps that effective tier unless an author later re-tiers
>    the source note.

#### After (rule 1)

> 1. **`retained` is computed, not declared.** Authors do not assign tiers.
>    The audit lane grants `effective_status = retained` when (a) this
>    row's `audit_status = audited_clean`, (b) `claim_type =
>    positive_theorem`, and (c) every dependency's `effective_status ∈
>    {retained, retained_no_go, retained_bounded}`. Symmetric rules grant
>    `retained_no_go` (for `claim_type = no_go`) and `retained_bounded`
>    (for `claim_type = bounded_theorem`). All three are equally valid as
>    inputs to a downstream chain.

Rules 2-5 unchanged in substance. Wording adjusted to drop references to
`current_status` / `proposed_retained as author-settable`.

### Section: "What this lane is not"

Unchanged.

---

## 2. `docs/audit/FRESH_LOOK_REQUIREMENTS.md`

### Section: "The audit question" (§3)

#### Before

> The auditor answers exactly five questions per claim:
>
> 1. What is the load-bearing step?
> 2. What kind of step is it? (A-G)
> 3. Does the chain close?
> 4. What does the runner actually check?
> 5. Verdict.

#### After

> The auditor answers exactly seven questions per claim:
>
> 1. What is the load-bearing step?
> 2. What kind of step is it? (A-G)
> 3. Does the chain close?
> 4. What does the runner actually check?
> 5. Verdict (audit_status).
> 6. **What is the claim type?** (positive_theorem | bounded_theorem |
>    no_go | open_gate | decoration | meta)
> 7. **Does the note's stated scope match what the proof actually closes
>    for?** If not, what is the actual scope?

### Section: "Cross-confirmation for critical claims" (§4)

#### Before

> - Both must return matching `verdict` and matching `load_bearing_step_class`
>   before the row may move to `audited_clean`.

#### After

> - Both must return matching `verdict`, matching `load_bearing_step_class`,
>   and matching `claim_type` before the row may move to `audited_clean`.

### Section: "Author self-audit prohibition" (§5)

Unchanged. Independence rules apply identically — authors still cannot audit
their own notes; Claude still cannot grant `audited_clean` to a Claude-
authored note.

### New §8 — "Author hint at note-write time"

Add a short new section:

> Authors may include a single-line hint at the top of a new note:
>
> ```markdown
> Type: positive_theorem
> ```
>
> The hint is non-authoritative. The auditor reads the note body and may
> override the hint, in which case the row records both
> `claim_type_author_hint` and the auditor's `claim_type` for diff
> visibility. Persistent disagreement between author hints and audit
> verdicts in a single author's recent work is a signal worth tracking
> (e.g. for methodology improvement on the author side), not a defect.

---

## 3. `docs/audit/AUDIT_AGENT_PROMPT_TEMPLATE.md`

Full drop-in replacement provided in
[`PROPOSED_AUDIT_AGENT_PROMPT_TEMPLATE.md`](PROPOSED_AUDIT_AGENT_PROMPT_TEMPLATE.md).

Key edits:

- §4 rubric grows from one set of definitions (verdicts) to two
  (verdicts + claim_type).
- §5 required-answers JSON schema gains two fields (`claim_type` and
  `claim_scope`).
- §7 tie-breaking gains rules for ambiguous `claim_type`.
- §6 unchanged (what the auditor is not asked to do).

---

## 4. `docs/repo/CONTROLLED_VOCABULARY.md`

### Section: "Publication-Capture Dispositions"

#### Before

> | `retained` | live retained family on the current paper-authority surface |
> | `promoted` | main-paper publication-core family carried directly in the current paper package |
> | `bounded` | live captured family kept outside the main paper core with explicit caveats |
> | `open` | live gate / blocker that is not yet closed |
> | `frozen-out` | intentionally excluded from the main paper while still recorded |

#### After

These remain valid for *publication-capture* prose (paper-side language) but
do **not** represent audit-ratified `effective_status`. The audit-ratified
surface is the `effective_status` enum from
`docs/audit/AUDIT_LEDGER.md`, and the renderer must show that explicitly
when these labels appear in publication-facing tables.

Add an explicit note at the top of the section:

> **Publication-capture vs audit-grade.** This section's labels describe
> *which paper this claim belongs in*, not *whether the claim has been
> audit-ratified*. The audit lane (`docs/audit/README.md`) is the sole
> source of truth for audit grade. A row may have
> `effective_status = retained_bounded` (audit-ratified narrow theorem) and
> `publication_capture = bounded` (paper-team decision to keep it outside
> the main paper core) — these are independent.

### Section: "Claim-Strength / Release Labels"

#### Before

This section currently lists ~50 composite labels including
`retained`, `retained companion`, `retained support theorem`,
`retained corollary`, `retained exact theorem`, etc.

#### After

The composite-label vocabulary remains for *prose* on retained notes and
publication tables. But the audit-grade question is now answered by exactly
three labels:

- `retained` (audit-grade, positive, full scope)
- `retained_no_go` (audit-grade, negative)
- `retained_bounded` (audit-grade, narrow scope; replaces all
  `bounded support theorem` / `bounded support` / `bounded companion`
  composite forms when the claim has been audit-ratified for the bounded
  scope)

All composite forms in the existing vocabulary can still appear as *prose
qualifiers* — e.g. "retained exact structural theorem" — but they describe
the *flavor* of an `effective_status = retained` row, not a separate audit
tier. The audit lane only knows the three flavors above.

### Section: "Hard wording bans"

#### Before

> bare `retained` / `promoted` in source-note `Status:` lines

#### After

The wording-ban concept is moot under the proposal because source notes do
not have `Status:` lines. The replacement rule is: **no source note may
write any audit-grade label in its body prose without citing the
`AUDIT_LEDGER.md` row that ratifies it.** The pipeline lints for this.

---

## What this delta package does *not* touch

- `docs/audit/ALGEBRAIC_DECORATION_POLICY.md` — unchanged. Decoration
  detection moves into the audit prompt as a `claim_type` value, but the
  policy on what counts as decoration is the same.
- `docs/audit/STALE_NARRATIVE_POLICY.md` — unchanged. Archival path for
  failed wrappers is unchanged.
- `docs/audit/CI_INTEGRATION.md` — unchanged. CI workflow is identical.
- `docs/repo/REVIEW_FEEDBACK_WORKFLOW.md` — unchanged. Review queue still
  feeds into the audit pipeline the same way.
- `docs/repo/REPO_ORGANIZATION.md` — unchanged. Repo-wide navigation is
  unaffected.
