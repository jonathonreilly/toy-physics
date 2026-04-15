# Historical Remote Branch Audit

**Date:** 2026-04-14  
**Status:** historical branch-capture audit; not part of the live front-door
authority path
**Scope:** repo-wide publication audit across all current remote branches and
live workstreams.

This file answers one question:

> If a reviewer only reads the publication package, what result families would
> they miss that still exist on a remote branch or branch-local workstream?

The answer before this audit was: too many. The package had a good retained
theorem spine, but it under-surfaced the broader quantitative portfolio and did
not document frozen-out work in one canonical place.

This audit is the repo-level fix.

## Branches audited

The following remote branches were scanned against `origin/main`:

| Branch | Role | Audit result |
|---|---|---|
| `origin/main` | repo baseline | baseline only; not the current publication authority |
| `origin/review-active` | older frontier aggregation branch | important legacy source for bounded phenomenology and older prediction inventories; not current authority |
| `origin/codex/main-graph-first` | first clean Codex publication package | still useful for early package structure and graph-first framing; superseded by `codex/publication-prep` |
| `origin/codex/publication-prep` | current publication package | canonical publication-facing package after this audit |
| `origin/codex/review-active` | current Codex retained-claim and hardening branch | current authority for hierarchy closure and restricted strong-field gravity companion |
| `origin/claude/youthful-neumann` | current Claude bounded-lane and companion-results branch | current authority for DM / `y_t` / CKM bounded work, plus many companion predictions and theorem attempts |

## Main audit findings

### 1. The package was theorem-complete but portfolio-incomplete

The existing package already surfaced the retained core:

- weak-field gravity
- anomaly-forced `3+1`
- graph-first structural gauge sector
- one-generation and three-generation matter structure
- electroweak hierarchy / `v`
- exact companions (`I_3 = 0`, CPT)
- restricted strong-field gravity companion

What it did **not** surface clearly enough:

- the observation-facing bounded quantitative portfolio
- the branch-local prediction inventories that reviewers are actually likely to
  ask about
- the explicit frozen-out registry for results that exist but are not promoted

### 2. The strongest missing capture object was the observation-facing portfolio

The old quantitative portfolio existed, but was scattered across:

- older outline tables
- review-active notes
- Claude worktree notes
- branch-local scorecards and strategy docs

The most important examples were:

- dark matter ratio `R`
- `\Omega_\Lambda` conditional chain
- Cabibbo / Jarlskog bounded matches
- `n_s`
- `w = -1`
- `\alpha_s(M_Z)` and `m_t`
- CKM magnitude package
- Higgs / BH entropy / proton-lifetime / Lorentz / monopole / echo companion lanes

These were scientifically present but publication-invisible.

### 3. Gravity companion status was under-surfaced

The publication package already retained restricted strong-field gravity, but it
did not explain the ladder clearly enough. The following workstream is now part
of the audited capture:

- exact shell source
- exact same-charge bridge
- exact local static-constraint lift
- exact microscopic Schur boundary action
- discrete Einstein/Regge-style restricted lift
- support-class widening beyond the original benchmark
- explicit scalar-only tensor-completion no-go

This does **not** promote full nonlinear GR in full generality. It does make
the restricted strong-field theorem legible.

### 4. Several branch-local inventories exist but are not safe authority

Examples:

- `STANDALONE_PREDICTIONS_INVENTORY_2026-04-12.md`
- `MASTER_DERIVATION_SCORECARD.md`
- `PAPER_STRATEGY_2026-04-12.md`

These are useful capture documents, but they mix retained, bounded, fitted,
conditional, and stale claims. They must therefore be referenced as branch
inventories or frozen-out sources, not as publication authority.

## Branch-by-branch harvest map

### `origin/codex/publication-prep`

**Role:** canonical publication package.  
**Use:** final publication-facing package after this audit.

Key retained inputs from this branch:

- `CI3_Z3_PUBLICATION_STATE_2026-04-15.md`
- `CLAIMS_TABLE.md`
- `DERIVATION_VALIDATION_MAP.md`
- `RESULTS_INDEX.md`
- `FULL_CLAIM_LEDGER.md`
- `NATURE_DRAFT.md`
- `ARXIV_DRAFT.md`

### `origin/codex/review-active`

**Role:** current Codex hardening branch.  
**Use:** primary source for current retained hierarchy and gravity companion state.

Key harvest from this branch:

- hierarchy observable-principle chain and exact `v` closure
- restricted strong-field gravity theorem package
- bridge-widening and support-class sharpening
- tensor-completion obstruction / no-go chain

### `origin/claude/youthful-neumann`

**Role:** current bounded-lane and companion-results branch.  
**Use:** primary source for:

- current DM relic and ratio notes
- current `y_t` / `\alpha_s` bounded notes, including the coupling-map theorem
  and the 2-loop zero-import `m_t = 169.4 GeV` chain
- current CKM bounded notes
- current `S^3` theorem notes used by the publication package
- many companion prediction notes

Important caution:

- this branch also contains overpromoted closure notes and branch-local
  scorecards
- publication capture must therefore distinguish cleaned authorities from
  branch-internal strategy / summary files

### `origin/review-active`

**Role:** older broad frontier aggregation branch.  
**Use:** source of legacy quantitative inventory and candidate-missed work.

This branch matters because it preserved older workstreams that were never
fully carried into the new publication package, especially:

- cosmology windows
- experimental prediction cards
- older gravity and gauge phenomenology bundles
- broad “distinctive predictions” framing

It is **not** the authority for current promotion state.

### `origin/codex/main-graph-first`

**Role:** earlier Codex package branch.  
**Use:** useful historical package structure and graph-first framing.

This branch is mostly superseded by `codex/publication-prep`, but it remains a
useful source for:

- package organization patterns
- graph-first gauge framing
- early publication-card work

### `origin/main`

**Role:** baseline repo branch.  
**Use:** not a publication authority branch by itself.

## What was missing before this audit

Before this audit, the publication package was missing three canonical objects:

1. a branch-audited **master publication matrix**
2. a **frozen-out registry** for excluded or bounded-only work
3. a **remote-branch audit** showing where every current workstream lives

Those objects now exist in:

- [PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md)
- [FROZEN_OUT_REGISTRY.md](./FROZEN_OUT_REGISTRY.md)
- this file

## Residual blind spots after the audit

There are still branch-local files that should not be treated as authority:

- older scorecards
- old strategy memos
- stale closure notes
- historical prediction cards

Those are now explicitly tracked in the frozen-out registry instead of being
silently ignored.

## Audit rule

From this point on:

- if a result family is publication-relevant, it must appear in
  [PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md)
- if it is intentionally excluded, it must appear in
  [FROZEN_OUT_REGISTRY.md](./FROZEN_OUT_REGISTRY.md)
- if it lives only on one branch, that branch ownership must be clear in this
  audit file

If a result is in none of those places, it is not publication-captured yet.
