# Audit Lane

**Status:** infrastructure lane for `main`.
This lane does not produce physics claims. It audits existing ones.

## What this lane does

The publication package's `retained / promoted / bounded / open` tiers are
**self-declared** by the note that introduces each claim. The audit lane adds
an outside check: a separate `audit_status` per claim, propagated through the
citation graph, and a hard rule that nothing presents as `retained` to the
outside world unless its audit chain is clean.

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

## Status fields and the propose / ratify split

The audit lane separates the **science work** of proposing a strong claim
from the **sign-off work** of ratifying it. Authors propose; the audit lane
ratifies.

Three parallel fields per claim:

- `current_status` — what the source note declares. Authors may set:
  - `proposed_retained` — "I have done the science work and believe this
    should be retained, pending audit." This is the strongest tier an
    author may self-assign.
  - `proposed_promoted`, `proposed_bounded` — same idea for those tiers.
  - `support`, `open` — unchanged; these do not require audit ratification.
- `audit_status` — what the audit found. Set only by the audit lane:
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
- `effective_status` — derived. The publication-facing tables read this:
  - `retained` — `current_status = proposed_retained` AND `audit_status =
    audited_clean` AND every dependency's `effective_status` is `retained`
    or `retained_no_go`.
  - `retained_no_go` — `audit_status = audited_failed` AND the note has been
    moved to `archive_unlanded/`. The original positive claim failed audit;
    the project has accepted the lane is closed and archived the note as a
    durable negative-result theorem (Coleman-Mandula style). Sits at the
    same tier as `retained` for downstream propagation: depending on a
    no-go theorem does not weaken downstream rows.
  - `proposed_retained` — author has proposed retained, audit not yet clean
    (or upstream not yet ratified). Honest pending state.
  - `support` / `bounded` / `open` — as declared, or demoted by audit verdict.
  - `audited_<failure_mode>` — terminal state from a failed audit on an
    **active** claim (note still in `docs/`). Distinct from `retained_no_go`
    which represents an archived no-go.

The landing migration rewrites legacy source-note Status lines from bare
`retained` / `promoted` to `proposed_retained` /
`proposed_promoted`. The graph builder also preserves the same
interpretation rule for any older branch that has not yet been relabeled:
pre-audit bare `retained` is read as `proposed_retained` until audited.

## The hard rules

1. **`retained` is audit-only.** No author may directly write `retained` as
   `current_status`. The strongest author-settable state is
   `proposed_retained`. `audit_status = audited_clean` records the audit
   verdict on the chain as written, regardless of author tier. Only proposed
   rows can promote publication-facing status: the audit lane may grant
   `effective_status = retained` only when this row's `current_status =
   proposed_retained`, this row's `audit_status = audited_clean`, and every
   dependency's `effective_status = retained`. A clean `support`, `bounded`,
   `open`, or `unknown` row keeps that effective tier unless an author later
   re-tiers the source note.

2. **Inheritance is monotone-down.** A claim's `effective_status` cannot
   exceed the minimum of its dependencies' `effective_status`. One renaming
   near a root demotes everything that inherits from it.

3. **No self-audit.** The auditor of a claim must not share identity with
   the claim's author. Codex GPT-5.5 is the designated independent auditor
   for this repo (see `FRESH_LOOK_REQUIREMENTS.md`); using a different
   model family from the one that produced most existing notes satisfies
   the cross-family condition, while same-family confirmation must be
   recorded as `fresh_context` from a distinct restricted-input session.

4. **Decoration must be boxed.** Claims tagged `audited_decoration` cannot
   appear as separate `proposed_retained` or `retained` rows in the
   publication-facing tables; they roll up under their parent claim. See
   `ALGEBRAIC_DECORATION_POLICY.md`.

5. **Publication tables must not blur proposed and ratified tiers.**
   Until a renderer consumes `audit_ledger.json` directly, public tables
   may render source-note declarations (`proposed_retained`,
   `proposed_promoted`, etc.) but must not present them as audit-ratified
   `retained` / `promoted`. External readers should be pointed to
   `AUDIT_LEDGER.md` for the canonical `effective_status` surface.

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

For high-stakes claims (`criticality = critical` by transitive-descendant
count; the audit lane does not use author-declared flagship status), a second independent
agent runs the same audit; the two must agree before `audited_clean` lands.

### Pruning phase (per decoration cluster)

When a claim is marked `audited_decoration`, the pruning policy
(`ALGEBRAIC_DECORATION_POLICY.md`) decides whether it gets:

- **Boxed** as a corollary inside its parent note, or
- **Removed** if it adds no falsifiability and no compression.

## Reading the publication package after audit

External readers should read `effective_status`, not `current_status`.
The audit ledger is the canonical surface for claim strength. During the
transition, public tables that still render source-note declarations must
show `proposed_*` language plainly and cross-reference `AUDIT_LEDGER.md`
before any external claim of "retained."

## What this lane is not

- Not a physics result.
- Not a replacement for peer review (it is the strongest internal check that
  is feasible without external reviewers; external review remains the
  separate, missing ingredient for actual disciplinary impact).
- Not a re-derivation of the physics — the audit checks whether the existing
  derivations close, not whether alternative derivations exist.
