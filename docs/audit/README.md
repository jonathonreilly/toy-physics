# Audit Lane

**Status:** infrastructure lane for `main`.
This lane does not produce physics claims. It audits existing ones.

## What this lane does

The publication package historically mixed author-facing status labels with
claim strength. The audit lane now separates those concerns: the auditor sets
`claim_type`, the auditor sets `audit_status`, and the pipeline derives
`effective_status` through the citation graph. Nothing presents as retained
to the outside world unless the scoped audit chain is clean.

The first repo-wide trace (CKM atlas) showed several failure modes that
self-declared tiers do not catch:

1. **Definition-as-derivation** — a new symbol is defined as a small-integer
   ratio, then "shown" to match data by name substitution.
2. **Conditional-on-open-work** — a `retained` note depends on a `support` or
   `open` note for the load-bearing identification step.
3. **Algebraic decoration** — many `retained` corollaries are consequences of
   a single upstream parameter choice and add no independent physical content.
4. **Stale narrative wrappers** — a failed wrapper frame remains easy to cite
   even after its audit verdict invalidates the global story.

The audit lane mechanizes detection of these patterns.

## Layout

```
docs/audit/
  README.md                          # this file
  FRESH_LOOK_REQUIREMENTS.md         # who may audit what, and how
  ALGEBRAIC_DECORATION_POLICY.md     # how to identify and prune decoration
  STALE_NARRATIVE_POLICY.md          # how to archive failed wrapper frames
  AUDIT_AGENT_PROMPT_TEMPLATE.md     # the prompt template for cold auditors
  AUDIT_LEDGER.md                    # human-readable ledger
  data/
    citation_graph.json              # generated: doc -> cited authorities
    audit_ledger.json                # generated/edited: per-claim audit rows
    runner_classification.json       # generated: A/B/C/D per runner PASS line
  scripts/
    build_citation_graph.py          # parse all .md docs into the graph
    seed_audit_ledger.py             # initialize ledger rows from claim notes
    classify_runner_passes.py        # classify runner outputs by check type
    compute_effective_status.py      # propagate audit results down the graph
    audit_lint.py                    # validate ledger consistency
```

## Scope-aware fields

The audit lane separates **classification** from **verdict**. Authors may
write whatever status prose they need inside source notes, but the retained
library is driven only by auditor-owned fields:

- `claim_type` — what kind of object the auditor says the row is:
  - `positive_theorem`
  - `bounded_theorem`
  - `no_go`
  - `open_gate`
  - `decoration`
  - `meta`
- `claim_scope` — the auditor's short, citeable statement of what was
  actually audited. This is required for applied audits.
- `audit_status` — what the audit found:
  - `unaudited`
  - `audit_in_progress`
  - `audited_clean`
  - `audited_renaming`
  - `audited_conditional`
  - `audited_decoration`
  - `audited_failed`
  - `audited_numerical_match`
- `effective_status` — derived, publication-facing status:
  - `retained` for `claim_type = positive_theorem` plus
    `audit_status = audited_clean` plus retained-grade dependencies.
  - `retained_no_go` for `claim_type = no_go` plus
    `audit_status = audited_clean` plus retained-grade dependencies.
  - `retained_bounded` for `claim_type = bounded_theorem` plus
    `audit_status = audited_clean` plus retained-grade dependencies.
  - `retained_pending_chain` for a clean theorem/no-go/bounded row whose
    upstream chain is not yet retained-grade.
  - `open_gate` for a clean open gate; this blocks retained propagation.
  - `decoration_under_<parent_claim_id>` for an audited decoration whose
    parent is retained-grade.
  - `meta` for non-claim infrastructure rows.
  - `audited_<failure_mode>` for terminal non-clean audit verdicts on active
    claims.

Generated audit data must not contain legacy source-status authority fields.
The graph builder may use old source-note status prose as a one-way migration
hint when seeding `claim_type`, but the ledger, queue, prompt, and rendered
audit surfaces are `claim_type` / `audit_status` / `effective_status` only.
`support` is not a claim class. Once a legacy support-labeled note has an
`audited_clean` verdict, it retains according to its ledger `claim_type` and
dependency closure; old source-note prose neither grants nor blocks retained
status.
Legacy critical rows whose confirmed clean cross-confirmation predates
`claim_type` may clear `claim_type_backfill_reaudit` with a restricted-input
audit that writes the scoped `claim_type`; missing `claim_type` fields in the
old confirmation summaries are migration debt, not a cross-confirmation
disagreement.

## The hard rules

1. **Retained grade is audit-only.** The audit lane may grant
   `effective_status = retained`, `retained_no_go`, or `retained_bounded`
   only from `claim_type + audited_clean + retained-grade dependencies`.
   Author labels and source-note status prose do not promote rows.

2. **Open gates block propagation.** `open_gate`, `unaudited`,
   `audit_in_progress`, `retained_pending_chain`, and terminal non-clean
   audit verdicts are not retained-grade dependencies.

3. **No self-audit.** The auditor of a claim must not share identity with
   the claim's author. Codex GPT-5.5 is the designated independent auditor
   for this repo (see `FRESH_LOOK_REQUIREMENTS.md`); using a different
   model family from the one that produced most existing notes satisfies
   the cross-family condition, while same-family confirmation must be
   recorded as `fresh_context` from a distinct restricted-input session.

4. **Decoration must be boxed.** Claims tagged `audited_decoration` cannot
   appear as separate retained rows in the publication-facing tables; they
   roll up under their parent claim. See `ALGEBRAIC_DECORATION_POLICY.md`.

5. **Publication tables consume effective status.** Public tables must read
   `effective_status` from the audit ledger or an artifact derived from it,
   not source-note status prose.

6. **Runner timeout is not a verdict.** A wall-time timeout, missing stdout,
   or noncompletion of a long-running runner is not evidence that the
   scientific claim is wrong, conditional, or failed. If the load-bearing
   step cannot be judged without that run, the row remains pending with a
   compute-required blocker or is skipped in the current audit loop until a
   completed log, faster/sliced runner, cached certificate, or independent
   derivation is supplied. A terminal non-clean verdict may cite concrete
   runner evidence such as a completed mismatch or an executable/import error,
   but not mere long compute.

   This rule is retroactive as an audit policy check. A legacy terminal
   non-clean row whose primary rationale is only wall-time exhaustion,
   missing stdout, or another compute-budget limit must be treated as a
   policy-repair/re-audit candidate, not as settled scientific evidence. Do
   not mechanically reset rows that also contain an independent substantive
   blocker; repair those by re-auditing the actual blocker under the current
   restricted-input process.

## Workflow

### Mechanical phase (cron-able)

```bash
python3 docs/audit/scripts/build_citation_graph.py
python3 docs/audit/scripts/seed_audit_ledger.py
python3 docs/audit/scripts/classify_runner_passes.py   # optional, slow
python3 docs/audit/scripts/compute_effective_status.py
python3 docs/audit/scripts/audit_lint.py
```

This (a) keeps the graph in sync with the docs, (b) seeds new claim notes as
`unaudited`, (c) classifies runner PASSes by check type, (d) recomputes
`effective_status` everywhere, (e) lints for cycles, dangling citations, and
inconsistent inheritance.

### Audit phase (per claim, semi-automated)

For each `unaudited` claim, an audit agent is spawned with
`AUDIT_AGENT_PROMPT_TEMPLATE.md`. The agent receives only:

- the source note,
- the source note's directly cited authorities (one hop),
- the rubric,
- the runner's classification breakdown.

The agent does **not** receive the broader publication framing or the
publication-facing claim status. That is the "fresh look" requirement. The
agent returns a fill of the audit row.

If the primary runner is load-bearing but does not complete inside the
current audit budget, the audit is not applied as `audited_conditional` or
`audited_failed` for that reason alone. The loop records a local
`compute_required` skip, or tooling records `audit_in_progress` with a
compute blocker when supported, and then continues to the next ready row.
Rows skipped this way need a completed run artifact, reduced deterministic
runner, or proof-level replacement before re-audit.

For every `audited_conditional` result, the auditor must make the repair lane
machine-sortable by prefixing `notes_for_re_audit_if_any` with one repair
class:

- `missing_dependency_edge` — a needed source note or authority exists or is
  named, but is not wired as a direct dependency for the audited claim.
- `dependency_not_retained` — a direct dependency exists but is not retained
  grade.
- `missing_bridge_theorem` — the claim needs a new theorem for a physical
  carrier, readout, unit map, boundary condition, sector choice,
  normalization, or observable bridge.
- `scope_too_broad` — a clean bounded core exists, but the current claim scope
  includes an unclosed extension.
- `runner_artifact_issue` — a runner, log, classifier, threshold, import, or
  pass/fail accounting problem blocks closure despite otherwise local scope.
- `compute_required` — closure needs a completed long run, sliced runner,
  cached certificate, or independent derivation.
- `other` — none of the above fits; the note must state why.

After the class, the auditor names the cheapest next repair action. Examples:
add an explicit citation/dependency edge, audit a named dependency first,
create/open a bridge theorem, split a clean bounded core from a conditional
extension, or repair/slice a runner. The audit lane surfaces these repairs; it
does not perform them unless explicitly asked.

For high-stakes claims (`criticality = critical` by transitive-descendant
count; the audit lane does not use author-declared flagship status), a second independent
agent runs the same audit; the two must agree before `audited_clean` lands.
If the two audits disagree, the next step is a judicial third-auditor
review: a fresh auditor reads the restricted source packet and both audit
arguments, then explicitly ratifies the first audit, the second audit, or
neither. The ledger records that decision in `cross_confirmation.status`
and the row's current verdict must match the ratified side.

### Pruning phase (per decoration cluster)

When a claim is marked `audited_decoration`, the pruning policy
(`ALGEBRAIC_DECORATION_POLICY.md`) decides whether it gets:

- **Boxed** as a corollary inside its parent note, or
- **Removed** if it adds no falsifiability and no compression.

## Reading the publication package after audit

External readers should read `effective_status`. The audit ledger is the
canonical surface for claim strength.

## What this lane is not

- Not a physics result.
- Not a replacement for peer review (it is the strongest internal check that
  is feasible without external reviewers; external review remains the
  separate, missing ingredient for actual disciplinary impact).
- Not a re-derivation of the physics — the audit checks whether the existing
  derivations close, not whether alternative derivations exist.
