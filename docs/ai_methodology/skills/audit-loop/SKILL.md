---
name: audit-loop
description: Run the cl3-lattice-framework audit lane as an adversarial Nature-grade claim auditor. Use when the user asks to audit scoped retained-grade science, process the audit backlog/queue, run an auditor loop, update audit results, apply audit verdicts, or push claim-audit outcomes directly to main.
---

# Audit Loop

Use this skill to audit one claim at a time from the repository audit queue and land the audit result. The standard is hostile field review: the claim must survive an adversarial physicist looking for hidden imports, circular logic, definition-as-derivation, stale numerics, misidentified observables, and overstated closure.

## Non-Negotiables

- Audit; do not repair the science. If a claim fails, record a physicist-actionable failure handoff so someone else can fix it.
- Work one claim per commit. This keeps audit verdicts reversible and reviewable.
- Prefer a clean temporary worktree based on `origin/main`. Do not use a dirty shared checkout for audit commits.
- Push routine audit commits directly to `main`. This project has authorized direct-main audit operation for ordinary `apply_audit.py`-accepted verdicts; do not open PRs for routine clean, conditional, renaming, decoration, numerical-match, or non-controversial failed verdicts.
- Do not read broad publication framing while judging the claim. Use the source note, one-hop cited authorities, runner, runner output, and the audit rubric.
- Preserve fresh-context integrity. Do not read prior audit rationales, previous audit entries, rendered `AUDIT_LEDGER.md` history, PR text, publication framing, or downstream summaries while judging a claim.
- Do not grant `audited_clean` unless the derivation closes without hidden premises, unsupported physical identifications, circular dependency, or tuned comparator matching.
- Apply the No-Go Discipline gate (`no-go-discipline` skill, checks N1-N8) before recording any verdict on a row with `claim_type: no_go`, a `bounded_theorem` whose source note names walls/admissions, or an `audited_conditional` whose `verdict_rationale` would name walls. Negative-claim overclaims foreclose investigation paths permanently and require the same scrutiny as positive-claim overclaims. If any N1-N8 check fails on the source note, choose the more conservative non-clean verdict whose `verdict_rationale` reflects the honest narrower claim scope; do not record `audited_clean`, and do not transcribe the source note's inflated wall list into the ledger.
- If the author family appears to be Codex and the current auditor is Codex, do not let the current context self-ratify a clean result. Restart the claim in a distinct restricted-input sub-agent when sub-agents are available, and record a clean result only as `independence: fresh_context` with a distinct `auditor` identity if `apply_audit.py` accepts it. If no sub-agent is available, skip clean application and report that a non-Codex, human, or fresh-context agent audit is required.
- Do not stop after producing an audit JSON unless the user explicitly asks for a dry run, no-apply, or JSON-only result. If the user asks to "return JSON" as part of an audit-loop task, treat that as the required verdict format and still apply, verify, commit, and push the audit result according to this skill.

## Setup For Each Session

1. Fetch `origin/main`.
2. Create or reuse a clean worktree based on `origin/main`.
3. Run:

```bash
bash docs/audit/scripts/run_pipeline.sh
python3 docs/audit/scripts/audit_lint.py --strict
```

The graph-cycle warning is currently expected. Treat any error as a blocker.

## Clean-Context Guards

- Do not run broad content searches over `docs/audit/data/audit_ledger.json`, `docs/audit/AUDIT_LEDGER.md`, or other audit-history files. Use exact `jq` field extraction for selected rows and dependencies.
- When reading `audit_ledger.json`, extract only operational metadata such as `claim_id`, `note_path`, `runner_path`, statuses, `criticality`, `deps`, `note_hash`, and graph-degree fields. Do not print or inspect `verdict_rationale`, `chain_closure_explanation`, `previous_audits`, `audit_history`, or prior auditor notes.
- File-name listing is allowed when needed, but do not search file contents in audit data/history to find alternate candidate sources or prior conclusions.
- If fresh-context contamination occurs before a verdict is applied, discard the current context's judgment for that claim and restart the claim in a distinct restricted-input sub-agent when sub-agents are available. Do not pass the contamination, prior conclusion, or audit-history text to the sub-agent. If no sub-agent is available, stop before applying any audit and report the contamination.

## Blocked-Row Loop Guard

- If applying a verdict and rerunning the pipeline immediately invalidates that same row, returns it to the ready queue, or creates a dependency-status cycle that cannot be resolved by the audit verdict alone, do not keep retrying the row in the same audit loop.
- Restore the pre-claim generated audit diff for that row, record a session-local blocked/skip entry with the claim id and the exact tooling reason, and continue with the next ready row.
- Do not write an unsupported blocked verdict into the ledger unless `apply_audit.py` provides such a route. Report skipped blocked rows at the end of the loop and require upstream dependency/status repair before retrying them.

## Long-Running Runner / Timeout Guard

- A wall-time timeout, missing stdout, or noncompletion of a runner is not scientific evidence against the claim. Do not apply `audited_conditional`, `audited_failed`, or any other terminal non-clean verdict solely because the runner may need a long compute run.
- When analysis needs runner stdout, use `python3 scripts/cached_runner_output.py <runner_path>` instead of running the runner directly. This reuses a fresh SHA-pinned cache, or writes one if the cache is missing/stale, so later audits and non-audit analysis do not rerun the same expensive computation.
- If the load-bearing step cannot be judged without a long run and there is no completed log, cached certificate, sliced deterministic runner, or independent derivation in the restricted packet, record a session-local `compute_required` skip with the claim id, runner path, timeout/budget used, and the exact artifact needed; then continue with the next ready row.
- Apply a non-clean verdict only when there is a substantive audit reason beyond wall-time noncompletion, such as a completed output mismatch, stale number, unsupported dependency, import/API failure, hard-coded contested premise, or an over-broad claim not supported by completed finite evidence.
- If a prior audit row appears to have used timeout/noncompletion as the primary reason for a terminal verdict, do not treat that prior verdict as settled science. Queue it for policy repair or re-audit under this guard.
- Do not blanket-reset older rows just because the rationale mentions a timeout. If the same rationale contains an independent blocker, re-audit the blocker under restricted inputs; if timeout/noncompletion is the primary or only reason, leave the row pending for compute or policy repair instead of citing it as non-clean science.

## Legacy Claim-Type Re-Audits

- `claim_type_backfill_reaudit` rows are migration cleanup under the PR291 regime. Audit the current scoped claim, not the old source-note status prose.
- For critical rows with already confirmed legacy clean cross-confirmation whose summaries predate `claim_type`, a restricted-input re-audit may own the scoped `claim_type` and `claim_scope`; missing `claim_type` in the old summaries is not by itself a cross-confirmation disagreement.
- If the new restricted-input audit changes the actual clean/non-clean verdict, or if `apply_audit.py` records a real cross-confirmation disagreement, follow the normal escalation path.

## Pick The Next Claim

If the user names a candidate file or other constrained selection source, that source is authoritative. After the pipeline, check the exact path exists. If it is absent, stop and report the missing file; do not search for substitutes or fall back to the default queue unless the user explicitly authorizes that fallback.

Default selection is the highest-priority ready scoped claim:

1. Read `docs/audit/data/audit_queue.json`.
2. Pick the first row with `ready = true`, `audit_status` in `{unaudited, audit_in_progress}`, and `claim_type` in `{positive_theorem, bounded_theorem, no_go, open_gate}`.
3. If the user explicitly says strict queue order, take the top queue row even if `claim_type` is unset.
4. Exclude any claim id recorded in the current session's blocked/skip set by the Blocked-Row Loop Guard.
5. If only `meta` or `decoration` rows remain, process them only when the user explicitly asks for those classes.

Use this snippet when useful:

```bash
python3 - <<'PY'
import json
q=json.load(open("docs/audit/data/audit_queue.json"))["queue"]
for e in q:
    if e.get("ready") and e.get("claim_type") in {"positive_theorem","bounded_theorem","no_go","open_gate"}:
        print(e["claim_id"], e["note_path"], e.get("runner_path") or "-")
        break
PY
```

## Context To Read

For the selected claim, read only:

- source note at `note_path`;
- one-hop dependency notes listed in `docs/audit/data/audit_ledger.json` under `deps`;
- the primary runner, if any;
- current runner output, if the runner can be executed safely;
- `docs/audit/README.md`, `FRESH_LOOK_REQUIREMENTS.md`, `AUDIT_AGENT_PROMPT_TEMPLATE.md`, and `ALGEBRAIC_DECORATION_POLICY.md`.

When writing the verdict, also load `references/nature-grade-rubric.md` from this skill.

Do not use `CLAIMS_TABLE.md`, `PUBLICATION_MATRIX.md`, `ARXIV_DRAFT.md`, or earlier review summaries to bias the verdict.

## Audit Questions

Answer these before choosing a verdict:

- What exact sentence/equation is load-bearing?
- Is the claimed observable the same observable being compared or derived?
- Does the result follow from cited inputs, or is a symbol identity being introduced?
- Are any physical carriers, unit maps, source laws, boundary conditions, sectors, normalizations, or readouts selected without a retained theorem?
- Are dependencies unaudited, open gates, retained-pending-chain, stale, or themselves conditional?
- Does the runner compute the hard bridge, or does it hard-code the contested premise and check consistency afterward?
- Is this an independent theorem, or algebraic decoration of an upstream claim?
- Are numerical values current with the runner and the source note?
- Would a hostile specialist be able to reject the conclusion without making a mistake?
- If the claim is a `no_go`, a wall-naming `bounded_theorem`, or its rationale would cite walls: have at least 5 distinct attack routes against the no-go been considered (N1)? Are the named walls actually independent (N2)? Are any hidden in "bridge context" / "we assume" / "standard QFT" / "registered" prose (N3)? Do cited witness residuals match the claim's residual (N4)? Are "X is not a Y-fact" phrases verified at every named resolution (N5)? Is the "needs new axiom" framing actually a convention-reframe / labeling ratification (N6)? Can a steelman against the no-go be made convincing (N7)? Has a structurally similar prior wall been retired by a mechanism not considered here (N8)? See `no-go-discipline` skill.

## Verdict Rules

Use the audit-lane verdict enum exactly:

- `audited_clean`: derivation closes from the cited inputs; no hidden physical identification; runner checks the load-bearing step or the proof is purely exact algebra over independent retained inputs. Effective status is derived from ledger `claim_type` plus dependency closure, not source-note status prose. `support` is not a claim class, and old support prose neither grants nor blocks retained status after a clean audit.
- `audited_conditional`: depends on an unaudited dependency, open gate, retained-pending-chain row, unratified physical bridge, or an explicit premise not closed by the cited authorities.
- `audited_renaming`: the load-bearing step defines/renames the target quantity or identifies two concepts without derivation.
- `audited_decoration`: exact algebraic corollary with no independent comparator, falsifiability, compression, or new physical content beyond an upstream parent.
- `audited_numerical_match`: result depends on tuned/calibrated input or chosen scale/value rather than a structural theorem.
- `audited_failed`: chain is wrong, stale relative to the runner, mismatches the observable, contradicts dependencies, or does not close on its own terms.

When in doubt, choose the more conservative non-clean verdict.

For claims with `claim_type: no_go`, `bounded_theorem` whose source note names walls/admissions, or any verdict that would record walls in `verdict_rationale`, apply the No-Go Discipline gate (`no-go-discipline` skill, N1-N8) before recording. Any FAIL forbids `audited_clean`; instead, choose the non-clean verdict whose `verdict_rationale` reflects the corrected narrower claim scope. Specifically:

- if N1 fails (fewer than 5 distinct attack routes considered against the no-go), record `audited_conditional` with `notes_for_re_audit_if_any: scope_too_broad — alternative attack routes not exhausted`;
- if N2/N3 fails (walls not independent, or hidden walls promoted), record `audited_conditional` with the collapsed/expanded honest wall list;
- if N4 fails (witness-residual mismatch in cited authorities), record `audited_conditional` with `notes_for_re_audit_if_any: missing_dependency_edge — cited witness residual does not match the claim residual`;
- if N5/N6 fails (over-broad phrasing, or convention-reframe misclassified as new axiom), record `audited_renaming` if the failure is purely scope/framing, or `audited_conditional` with a sharper wall list;
- if N7/N8 fails (convincing steelman exists, or prior-wall retirement mechanism not considered), record `audited_conditional` with `notes_for_re_audit_if_any: scope_too_broad — named alternative not foreclosed`.

See [`docs/ai_methodology/skills/no-go-discipline/SKILL.md`](../no-go-discipline/SKILL.md). The audit lane must not transcribe a source note's inflated no-go into the ledger as `audited_clean` — that cements the overclaim and forecloses investigation paths permanently.

## Required Failure Handoff

For any verdict other than `audited_clean`, make the ledger useful to the physicist who fixes the science. Put this structure inside `verdict_rationale` and keep `chain_closure_explanation` short but specific:

```text
Issue: <exact failed step, stale number, hidden premise, or observable mismatch>.
Why this blocks: <why the conclusion cannot be claimed from current inputs>.
Repair target: <specific theorem, derivation, runner computation, or dependency status needed>.
Claim boundary until fixed: <what may still be safely said>.
```

For `audited_clean`, still explain why the load-bearing step closes and what residual risk remains.

## Conditional Repair Surfacing

For every `audited_conditional` result, make the next repair lane sortable.
Prefix `notes_for_re_audit_if_any` with exactly one repair class:

- `missing_dependency_edge`: a needed source note or authority exists or is
  named, but is not wired as a direct dependency for the audited claim.
- `dependency_not_retained`: a direct dependency exists but is not retained
  grade.
- `missing_bridge_theorem`: the claim needs a new theorem for a physical
  carrier, readout, unit map, boundary condition, sector choice,
  normalization, or observable bridge.
- `scope_too_broad`: a clean bounded core exists, but the current claim scope
  includes an unclosed extension.
- `runner_artifact_issue`: a runner, log, classifier, threshold, import, or
  pass/fail accounting problem blocks closure despite otherwise local scope.
- `compute_required`: closure needs a completed long run, sliced runner,
  cached certificate, or independent derivation.
- `other`: use only when none of the above fits, and state why.

After the class, name the cheapest next repair action, such as adding an
explicit citation/dependency edge, auditing a named dependency first, creating
an open bridge theorem, splitting the clean bounded core from the conditional
extension, or repairing/slicing the runner. Do not repair during the audit
unless the user explicitly asks for repair work.

## Apply The Audit

Create an audit JSON matching `docs/audit/scripts/apply_audit.py`. Returning this JSON to the user is not the end of the task unless they explicitly requested dry-run/no-apply behavior. Required metadata:

- `claim_type`: one of `positive_theorem`, `bounded_theorem`, `no_go`, `open_gate`, `decoration`, `meta`.
- `claim_scope`: a short citeable statement of exactly what was audited.
- `auditor`: use a stable string such as `codex-audit-loop`.
- `auditor_family`: use the actual family if known; otherwise use `codex-current`. Do not claim `codex-gpt-5.5` unless that is true for the session.
- `independence`: use `cross_family` for non-Codex-authored claims, `weak` for same-family audits, `strong` for independent human review, `external` for off-project review.

Apply it:

```bash
python3 docs/audit/scripts/apply_audit.py --file /tmp/audit-result.json
bash docs/audit/scripts/run_pipeline.sh
python3 docs/audit/scripts/audit_lint.py --strict
git diff --check
```

For critical claims, the first clean audit records `audit_in_progress` and awaits cross-confirmation. That is expected.

`apply_audit.py` is the gate. If it records a cross-confirmation disagreement, do not stop by default. Run a fresh judicial third auditor in the same loop using the restricted source packet plus the two prior audit arguments. Apply the judicial JSON through `apply_audit.py`; if the third auditor explicitly sides with the first or second audit, the script accepts the judgment, the pipeline refresh passes, `audit_lint.py --strict` passes, and `git diff --check` passes, treat the resolved judicial review as an ordinary landable audit result and continue the loop.

Only stop for human review when the judicial auditor sides with neither, introduces a three-way disagreement, the tooling rejects the judgment, strict lint fails, or another hard-rule/exceptional routing case remains after the judicial review.

If `apply_audit.py` accepts the JSON and `audit_lint.py --strict` passes after the pipeline refresh, land the audit by direct push to `main` for these routine cases:

| Verdict / state | Audit-loop action |
| --- | --- |
| First or second `audited_clean` in the cross-confirmation flow | Direct push to `main` |
| Cross-confirmation disagreement recorded before judicial review | Direct push only if immediately followed by an accepted judicial resolution in the same claim commit; otherwise stop for human review |
| Judicial third-auditor review that confirms first or second verdict | Direct push to `main` |
| `audited_conditional`, `audited_renaming`, `audited_decoration`, or `audited_numerical_match` | Direct push to `main` |
| `audited_failed` on a non-controversial claim | Direct push to `main` |

Open a PR and flag for human review only when there is an unresolved hard-rule conflict or exceptional routing case:

| Exception | Audit-loop action |
| --- | --- |
| Judicial third auditor sides with neither, creates a three-way disagreement, or leaves the row blocked | Open PR; flag for human |
| `apply_audit.py` rejects the verdict JSON or blocks on a hard rule | Open PR; flag for human |
| `audit_lint.py --strict` fails after applying the verdict | Open PR; flag for human |

## Commit And Push

Review the diff. It should normally touch only:

- `docs/audit/data/audit_ledger.json`;
- `docs/audit/data/effective_status_summary.json`;
- `docs/audit/data/audit_queue.json`;
- `docs/audit/AUDIT_LEDGER.md`;
- `docs/audit/AUDIT_QUEUE.md`;
- possibly generated load-bearing/runner files if the pipeline refreshed them.

Commit:

```bash
git add docs/audit
git commit -m "audit: <claim-id> <verdict>"
```

Before pushing, fetch and confirm `origin/main` is still the parent or rebase cleanly and rerun the pipeline:

```bash
git fetch origin main
git push origin HEAD:main
```

If the push is rejected, fetch/rebase onto `origin/main`, rerun pipeline/lint/diff-check, amend only if it is the same audit commit and no one else has consumed it, then push.

## Loop Control

After each successful direct-main push:

1. Report the claim id, verdict, and one-sentence reason.
2. If time and user intent allow, fetch `origin/main`, refresh the queue, exclude any session-local blocked/skip rows, and start the next claim.
3. Stop if there is an ambiguous independence issue, source-note hash drift that cannot be resolved mechanically, or an audit requiring domain expertise beyond the provided authorities.

For unresolved exception cases listed above, create a branch/PR instead of pushing to `main`, flag the reason for human review in the PR body, and stop the loop until the human decision lands. Do not stop merely because a third-auditor review occurred; stop only if the review remains unresolved or the tooling/verification gates fail.
