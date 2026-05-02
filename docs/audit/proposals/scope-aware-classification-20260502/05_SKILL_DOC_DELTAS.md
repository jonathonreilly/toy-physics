# Skill Doc Deltas

**Date:** 2026-05-02

Edits to two skill docs that govern how authors and reviewers interact with
the audit lane during day-to-day work.

1. [`docs/ai_methodology/skills/physics-loop/SKILL.md`](../../../ai_methodology/skills/physics-loop/SKILL.md)
2. [`docs/ai_methodology/skills/review-loop/SKILL.md`](../../../ai_methodology/skills/review-loop/SKILL.md)

---

## 1. `physics-loop/SKILL.md`

### Section: "Claim-Status Firewalls"

This entire section currently bans bare `retained` / `promoted` and lists
the allowed source-note `Status:` vocabulary. Under the proposal, source
notes do not have `Status:` lines, so the section reduces drastically.

#### Before (~40 lines)

> Hard wording bans in branch-local physics-loop artifacts:
>
> - bare `retained` / `promoted` in source-note `Status:` lines;
> - `retained branch-local`
> - `would become retained`
> - `promoted to retained`
> - `retained on the actual surface` when a required premise is conditional, hypothetical, admitted, fitted, or human-judgment-only.
>
> `proposed_retained` / `proposed_promoted` are allowed only when the certificate supports a theorem-grade author proposal and marks the later independent audit requirement.
>
> Allowed replacements include `exact negative boundary`, `exact support`, `bounded support`, `conditional / support`, `open`, `demotion`, and `hypothetical consequence map`.

#### After (~10 lines)

> The author writes the science. The audit lane records the audit-grade
> label. Branch-local physics-loop notes do not assert audit-grade tiers
> in their own body text.
>
> Authors may include a single optional `Type:` hint at the top of a new
> note (`positive_theorem` | `bounded_theorem` | `no_go` | `open_gate` |
> `decoration` | `meta`) — this is non-authoritative; the auditor classifies.
>
> Branch-local notes may freely describe scope, residuals, and admitted
> inputs in prose — those are the inputs the auditor reads. They must not
> claim `retained`, `retained_bounded`, or `retained_no_go` status in body
> prose without citing the `AUDIT_LEDGER.md` row that ratifies that status.

### Section: "Retained-Proposal Certificate"

This section currently lists 7 conditions for `proposed_retained` /
`proposed_promoted`. Under the proposal, `proposed_retained` is no longer
author-set — it is a computed transient state. The section becomes:

#### After (~15 lines)

> The audit lane decides retention. Per-block science notes do not need a
> `proposed_retained` certificate; the audit pipeline will produce the
> equivalent record automatically once the block lands and Codex audits the
> chain.
>
> What the per-block branch should still produce, for downstream audit
> ergonomics:
>
> 1. A `claim_scope` sentence at the top of the note that the auditor can
>    quote verbatim.
> 2. A clear list of admitted-context inputs, separated from retained
>    upstream citations.
> 3. A runner with classified PASS lines (A/B/C/D per
>    `classify_runner_passes.py`) so the auditor's `runner_check_breakdown`
>    is unambiguous.
> 4. An `open dependencies` callout if the chain depends on rows currently
>    `audited_conditional` or below.
>
> All of (1)-(4) are inputs the audit lane consumes. None require the
> author to assign a tier.

### Section: "Status Discipline" / "Honest Status" patterns in workflow steps

Replace all instances of `proposed_retained` / `proposed_promoted` /
`support` / `bounded` author-tier language with:

> Author scope discipline. State the precise scope the proof closes for in
> the note's opening section as the `claim_scope`. The auditor will set
> `claim_type` based on the note body. Avoid asserting audit-grade tiers
> in body prose; the audit ledger is canonical.

### Other minor edits

- Replace any reference to `current_status` with `claim_type` (`audit-grade`).
- Replace "support theorem" with "positive_theorem" or
  "bounded_theorem" depending on the audit it would pass.
- Replace "bounded support" prose markers with "claim_scope: …" prose.

These are mechanical — counting current usages: ~32 in `physics-loop/SKILL.md`.
A grep + sed pass during migration handles them.

---

## 2. `review-loop/SKILL.md`

### Section: "Required Reviewers" — `ClaimSurfaceReviewer`

Currently the reviewer's job description includes detecting unsupported
`proposed_retained` / `proposed_promoted` author-tier claims. Update:

#### Before (excerpt)

> If the branch introduces `proposed_retained` / `proposed_promoted` rows,
> report those claim IDs and assert that the author has produced a passing
> retained-proposal certificate per the physics-loop SKILL.

#### After

> The author no longer assigns audit-grade tiers. The reviewer's role on
> claim status becomes:
>
> - Verify each new note has a `claim_scope` opening sentence the auditor
>   can quote verbatim.
> - Verify each new note's admitted-context inputs are explicitly listed
>   (so the auditor reads them as admitted, not as hidden imports).
> - Verify no body prose asserts `retained` / `retained_bounded` /
>   `retained_no_go` status without a corresponding ratified row in
>   `AUDIT_LEDGER.md`.
> - Verify the optional `Type:` hint, if present, is internally consistent
>   with the note body. (The auditor will catch mismatches; the reviewer
>   surfaces them earlier.)

### Section: "What review-loop is not"

Update the existing line:

> "This skill is **review only**. It may make branch/package hygiene
> changes that allow the independent audit system to parse and queue
> claims, but it must not apply audit verdicts, write `audited_clean`, or
> run the audit worker."

#### After

> Same restriction, plus: the reviewer **must not** add or edit
> `claim_type` or `claim_scope` fields on audit-ledger rows. Those are
> auditor-set. The reviewer may suggest a `Type:` hint addition to the
> note, which the author can then add to the source.

### Section: "Reviewer Fanout" — runner classification

Currently the reviewers compare runner output to claim language. The
review-loop should now also flag:

- Notes where the author hint says `positive_theorem` but the body
  describes a narrow restriction (audit will likely demote to
  `bounded_theorem`).
- Notes where the author hint says `bounded_theorem` but the body actually
  proves the full positive scope (audit will likely promote — wasted scope
  on the author's side).
- Notes where the author hint is missing for new claims.

These are early-warning surfaces, not blockers. The reviewer flags them; the
auditor decides.

### Other minor edits

- Replace references to `current_status` checks with `claim_type` checks.
- Replace "bare `retained`" wording-ban references with the updated wording
  rule from `04_POLICY_DOC_DELTAS.md` §1.

---

## What this delta package does *not* touch

- The skill argument parsers (`--mode`, `--runtime`, etc.) — unchanged.
- The campaign continuation policy — unchanged.
- The deep-work / stretch-attempt / stuck-fan-out rules — unchanged.
- The PR opening / stacking conventions — unchanged.
- The `--no-pr` / `--no-review-loop` overrides — unchanged.
