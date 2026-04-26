# Audit Lane

**Status:** infrastructure lane on `audit-lane` branch.
This lane does not produce physics claims. It audits existing ones.

## What this lane does

The publication package's `retained / promoted / bounded / open` tiers are
**self-declared** by the note that introduces each claim. The audit lane adds
an outside check: a separate `audit_status` per claim, propagated through the
citation graph, and a hard rule that nothing presents as `retained` to the
outside world unless its audit chain is clean.

The first repo-wide trace (CKM atlas) showed three failure modes that
self-declared tiers do not catch:

1. **Definition-as-derivation** — a new symbol is defined as a small-integer
   ratio, then "shown" to match data by name substitution.
2. **Conditional-on-open-work** — a `retained` note depends on a `support` or
   `open` note for the load-bearing identification step.
3. **Algebraic decoration** — many `retained` corollaries are consequences of
   a single upstream parameter choice and add no independent physical content.

The audit lane mechanizes detection of all three.

## Layout

```
docs/audit/
  README.md                          # this file
  FRESH_LOOK_REQUIREMENTS.md         # who may audit what, and how
  ALGEBRAIC_DECORATION_POLICY.md     # how to identify and prune decoration
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

## Status fields

Two parallel status fields per claim:

- `current_status` — what the source note declares (`retained`, `promoted`,
  `bounded`, `support`, `open`).
- `audit_status` — what the audit found:
  - `unaudited` — no audit yet (default for every seeded row)
  - `audit_in_progress`
  - `audited_clean` — derivation actually closes from cited inputs
  - `audited_renaming` — load-bearing step is a definition / symbol rename
  - `audited_conditional` — depends on a `support` / `open` upstream node
  - `audited_decoration` — algebraic consequence of an upstream claim with no
    new physical content
  - `audited_failed` — derivation does not close on its own terms
  - `audited_numerical_match` — depends on a tuned numerical input rather than
    a structural identity

And one derived field:

- `effective_status` — the minimum of `current_status`, this row's
  `audit_status`, and every dependency's `effective_status`.

## The hard rules

1. **Retained requires audited_clean.** A claim with `current_status =
   retained` but `audit_status != audited_clean` reports as
   `effective_status = support` to all downstream consumers.

2. **Inheritance is monotone-down.** A claim's `effective_status` cannot
   exceed the minimum of its dependencies' `effective_status`. One renaming
   near a root demotes everything that inherits from it.

3. **No self-audit.** The auditor of a claim must not be the same agent (same
   model session, same repo author, etc.) that produced the claim. See
   `FRESH_LOOK_REQUIREMENTS.md`.

4. **Decoration must be boxed.** Claims tagged `audited_decoration` cannot
   appear as separate `retained` rows in the publication-facing tables; they
   roll up under their parent claim. See `ALGEBRAIC_DECORATION_POLICY.md`.

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

For high-stakes claims (anything gating a flagship), a second independent
agent runs the same audit; the two must agree before `audited_clean` lands.

### Pruning phase (per decoration cluster)

When a claim is marked `audited_decoration`, the pruning policy
(`ALGEBRAIC_DECORATION_POLICY.md`) decides whether it gets:

- **Boxed** as a corollary inside its parent note, or
- **Removed** if it adds no falsifiability and no compression.

## Reading the publication package after audit

External readers should read `effective_status`, not `current_status`. The
audit ledger is the canonical surface for claim strength. The existing
`CLAIMS_TABLE.md` and `FULL_CLAIM_LEDGER.md` continue to record self-declared
tiers but should be cross-referenced against `AUDIT_LEDGER.md` before any
external claim of "retained."

## What this lane is not

- Not a physics result.
- Not a replacement for peer review (it is the strongest internal check that
  is feasible without external reviewers; external review remains the
  separate, missing ingredient for actual disciplinary impact).
- Not a re-derivation of the physics — the audit checks whether the existing
  derivations close, not whether alternative derivations exist.
