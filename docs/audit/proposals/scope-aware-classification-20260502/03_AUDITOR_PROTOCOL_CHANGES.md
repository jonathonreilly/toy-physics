# Auditor Protocol Changes

**Date:** 2026-05-02

The audit agent's job grows by two questions, both of which the auditor
already needs to answer implicitly under the existing rubric. Making them
explicit forces the auditor to scope-match, not just chain-check.

## Today's audit prompt asks (5 questions)

(From `docs/audit/AUDIT_AGENT_PROMPT_TEMPLATE.md` and
`FRESH_LOOK_REQUIREMENTS.md` §3.)

1. What is the **load-bearing step**? Quote the sentence.
2. What **kind of step** is it? Pick from {A, B, C, D, E, F, G}.
3. Does the **chain close**?
4. What does the **runner actually check**? Classify each runner PASS as
   A/B/C/D.
5. **Verdict.** One of the `audit_status` values.

## Proposed audit prompt asks (7 questions, +2)

Same 1-5 above, plus:

6. **What is the claim type?** Pick exactly one from {`positive_theorem`,
   `bounded_theorem`, `no_go`, `open_gate`, `decoration`, `meta`}. Definitions
   in [`01_SCHEMA_CHANGES.md`](01_SCHEMA_CHANGES.md).
7. **Does the note's stated scope match what the proof actually closes
   for?** If yes, restate the scope in one sentence. If no, write the
   correct scope as `claim_scope`, and the verdict must be
   `audited_conditional` with the corrected scope as the repair target.

The auditor returns these two new fields in the JSON response.

## Updated JSON response schema

```json
{
  "claim_id": "{{CLAIM_ID}}",
  "load_bearing_step": "<sentence>",
  "load_bearing_step_class": "<A|B|C|D|E|F|G>",
  "chain_closes": <bool>,
  "chain_closure_explanation": "<sentences>",
  "runner_check_breakdown": {"A": int, "B": int, "C": int, "D": int, "total_pass": int},
  "verdict": "<audit_status value>",
  "verdict_rationale": "<sentences>",
  "decoration_parent_claim_id": "<id or null>",

  "claim_type": "<positive_theorem|bounded_theorem|no_go|open_gate|decoration|meta>",
  "claim_scope": "<one-sentence statement of the precise claim the proof closes for>",

  "open_dependency_paths": ["<path>"],
  "auditor_confidence": "<low|medium|high>",
  "notes_for_re_audit_if_any": "<text>"
}
```

The two new fields are required. Pipeline rejects responses missing them.

## Tie-breaking on `claim_type`

If the auditor is torn between two `claim_type` values:

- `positive_theorem` vs `bounded_theorem` → choose `bounded_theorem`. The
  burden is on the proof to close for the full positive scope without
  qualifier.
- `bounded_theorem` vs `decoration` → choose `decoration` if the chain
  reduces to a single upstream parent plus standard mathematics with no
  new physical content.
- `positive_theorem` vs `no_go` → never ambiguous; the load-bearing
  conclusion is either positive or negative.
- `positive_theorem` vs `open_gate` → choose `open_gate` if the note's own
  text identifies a remaining residual the proof does not close.
- Anything vs `meta` → `meta` only when the note has no load-bearing step
  (README, lane index, methodology).

Same conservative-verdict bias as the existing tie-breaking rules in
`AUDIT_AGENT_PROMPT_TEMPLATE.md` §7.

## Cross-confirmation impact

For `criticality = critical` (250+ descendants), the existing rule requires
two independent auditors to match on `verdict` and `load_bearing_step_class`.
This proposal extends the matching requirement to `claim_type`.

So a critical claim is `audited_clean` only when:

- both auditors return `verdict = audited_clean`, AND
- both return the same `load_bearing_step_class`, AND
- both return the same `claim_type`.

Disagreement on any of the three escalates to a third auditor and is logged
as `cross_confirmation.status = disagreement` with the disagreement type
recorded.

This is the strongest defense against scope-mismatch on critical claims: two
independent readers must independently arrive at the same scope.

## What does *not* change

- The auditor's input is unchanged: source note + one-hop cited authorities
  + runner output + rubric. No publication-facing context. No prior audit
  verdicts.
- The fresh-look context restriction (`FRESH_LOOK_REQUIREMENTS.md` §2) is
  unchanged.
- The author/auditor identity separation is unchanged.
- The runner classification step (`classify_runner_passes.py`) is unchanged.

## Migration of historical audits

All ~361 currently-`audited_clean` rows are missing the new `claim_type`
field. The pipeline can populate `claim_type` from a deterministic
inference rule for backfill (see [`06_MIGRATION_PLAN.md`](06_MIGRATION_PLAN.md)
phase 3) or queue the rows for re-audit. The cheapest correct path:
backfill from `current_status` heuristic, mark `claim_type_provenance =
backfilled`, queue critical rows for explicit re-audit at the next pass.
Non-critical rows stay backfilled until they next change.
