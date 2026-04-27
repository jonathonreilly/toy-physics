# Fresh Look Requirements

**Status:** binding rule for the audit lane.

The CKM audit revealed that self-declared `retained` tiers can hide
definition-as-derivation patterns when the audit is performed by the same
context that produced the claim. This file specifies the minimum
independence conditions an audit must satisfy before `audit_status =
audited_clean` is permitted.

## 1. Auditor identity must differ from author identity

For each claim, the audit ledger records:

- `author` — the agent / human / session that produced the source note
  (extracted from git blame on the note's load-bearing section, or from the
  note's own `Date` / `Branch` metadata when blame is ambiguous).
- `auditor` — the agent / human / session that performed the audit.
- `auditor_family` — the model family of the auditor (e.g., `codex-gpt-5.5`,
  `claude-opus-4.x`, `human`). Used to enforce cross-family independence.

`auditor` must not equal `author`. Strength tiers:

- `independence: weak` — same model family, different session. Permitted
  but flagged in the ledger; should not be the only audit for a
  critical claim (criticality is computed from transitive descendants).
- `independence: cross_family` — different model family from the author.
  This is the standard for the audit lane.
- `independence: strong` — human auditor with no prior involvement in the
  note.
- `independence: external` — off-repo reviewer with no project context.
  This is the only form that satisfies external-impact requirements; the
  audit lane does not produce these on its own.

### Designated auditor for this repo

The bulk of existing notes were produced by Claude via the autopilot
lane (see `docs/ai_methodology/`). To satisfy `independence: cross_family`
by construction, the audit lane uses **Codex GPT-5.5** as the designated
independent auditor. Codex is a different model family from Claude, runs
in a separate session with no autopilot context, and is invoked via the
prompt template in `AUDIT_AGENT_PROMPT_TEMPLATE.md`.

This does not preclude human auditors or other independent agents — those
strengthen the audit when available and are recorded with their own
`auditor_family` value. It establishes Codex GPT-5.5 as the baseline
independent auditor that the mechanical pipeline routes work to.

A claim audited only by Claude (any session, any version) records
`independence: weak` and is not eligible to land `effective_status =
retained` unless cross-confirmed by Codex or a human auditor.

## 2. Context restriction at audit time

The audit agent must not be primed with the publication-facing framing of
the claim. The auditor receives:

- the source note in full;
- the source note's directly cited authorities (one hop upstream);
- the runner script and its current output;
- the audit rubric (`AUDIT_AGENT_PROMPT_TEMPLATE.md`);
- the runner classification breakdown for this claim, if computed.

The auditor must not receive:

- `CLAIMS_TABLE.md`, `PUBLICATION_MATRIX.md`, `ARXIV_DRAFT.md`, or any
  other publication-facing summary that has already labeled this claim as
  `retained`;
- the broader status taxonomy explanation framed as advocacy;
- prior audit results for the same claim (these are added only at the
  cross-confirmation step, not at first audit).

The intent is to remove the social pressure of "this is already retained,
find a way to confirm it" and replace it with "given only the cited
inputs, does the derivation close?"

## 3. The audit question

The auditor answers exactly five questions per claim:

1. **What is the load-bearing step?** Quote the one sentence (or
   equation) that does the actual work. If you cannot find one, the claim
   is `audited_failed`.
2. **What kind of step is it?** Pick from:
   - `(A)` algebraic identity check on existing inputs
   - `(B)` cross-note input verification (reads value from another note)
   - `(C)` first-principles compute from the axiom (`Cl(3)` on `Z^3` plus
     accepted normalizations) producing a number not present in any input
   - `(D)` external comparator check against PDG / lattice QCD / observation
   - `(E)` definition (introduces a new symbol)
   - `(F)` renaming (asserts symbol identity between two existing concepts)
   - `(G)` numerical match at a tuned input scale
3. **Does the chain close?** Given the source note plus its one-hop deps,
   does the conclusion follow without appeal to anything else?
4. **What does the runner actually check?** Classify each runner PASS as
   A/B/C/D using the same rubric.
5. **Verdict.** One of the `audit_status` values from
   `README.md`.

Each answer is a short field in the audit ledger row. No long prose.

## 4. Cross-confirmation for critical claims

A claim is `criticality = critical` if it crosses either topology
threshold in `compute_load_bearing.py` (currently direct in-degree >= 15
or transitive descendants >= 250). The audit lane intentionally does NOT
use author-declared "flagship" status to drive criticality — doing so
would let unratified author framing set the audit cost on upstream
support, which is the bootstrap problem this lane exists to break.
Criticality is graph topology only.

For critical claims:

- The first `audited_clean` audit lands `audit_status = audit_in_progress`
  with `blocker = awaiting_cross_confirmation`.
- A second independent auditor must come from a different
  `auditor_family` than the first.
- Both must return matching `verdict` and matching
  `load_bearing_step_class` before the row may move to `audited_clean`.
- Disagreement on `load_bearing_step_class` promotes the claim to a
  third-auditor review and logs the disagreement in
  `cross_confirmation.status = disagreement`.

Claims at `criticality = high` (`transitive_descendants >= 30`)
require `independence != weak` but do not require cross-confirmation by
default. Claims at `medium` and `leaf` follow the standard rules.

## 5. Author self-audit prohibition

If the only available auditor for a claim shares author identity, the
audit is recorded as `audit_status = unaudited` with `blocker:
self_audit_only_available`. It is not permitted to land any other status
in this case. The claim then waits for an independent auditor.

This rule exists because the AI methodology lane's existing self-review
loops, while well-intentioned, do not satisfy the independence condition;
the same model context that generated the renaming has a measurable bias
toward confirming it.

In practice this means: a Claude-produced note (the dominant case in this
repo) requires Codex GPT-5.5 (or a human, or any non-Claude agent) to
satisfy the rule. A Codex-produced note requires Claude or a human. A
human-produced note requires any independent agent or another human.

## 6. Audit re-runs

An audit row has a `note_hash` field — the SHA of the source note at the
time of audit. If the note changes, the row is automatically reset to
`audit_status = unaudited` (with the prior verdict preserved in
`previous_audits`) and must be re-audited. This prevents drift where a
note is edited after audit and silently inherits the prior clean tag.

## 7. What this does not require

The audit lane does not require a reproduction of the underlying
mathematics from scratch. The auditor checks whether the derivation as
presented closes from its cited inputs, not whether an alternative
derivation exists. Independent re-derivation is a separate, stronger
check that belongs to external peer review.
