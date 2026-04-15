# Historical Stale Authority Audit

**Date:** 2026-04-14  
**Purpose:** quarantine stale or misleading authority surfaces outside the
curated publication package.

This file does not delete older work. It marks what must no longer outrank the
matrix-driven package.

## Audit rule

A document is stale authority if it does one or more of the following:

- promotes a bounded lane as closed
- mixes retained, bounded, and open claims without status labels
- acts as a repo front door while bypassing the current package
- serves as a branch-local scorecard or strategy memo rather than science
  authority

These files may still be useful historically. They are not safe publication
authority.

## Quarantined families

### 1. Old closure packets and closure-language notes

Examples:

- `claude/youthful-neumann: YT_FLAGSHIP_CLOSURE_NOTE.md`
- `claude/youthful-neumann: YT_FULL_CLOSURE_NOTE.md`
- `claude/youthful-neumann: DM_FLAGSHIP_CLOSURE_NOTE.md`
- `claude/youthful-neumann: CKM_FULL_CLOSURE_NOTE.md`
- `claude/youthful-neumann: CKM_CLOSURE_NOTE.md`
- `claude/youthful-neumann: DM_CLOSURE_CASE_NOTE.md`

Status:

- historical / branch-local only
- may be cited in [FROZEN_OUT_REGISTRY.md](./FROZEN_OUT_REGISTRY.md), not as
  current paper authority

### 2. Review packets and reviewer summaries

Examples:

- `claude/youthful-neumann: CODEX_REVIEW_PACKET_2026-04-12.md`
- `claude/youthful-neumann: REVIEW_RESUBMISSION_2026-04-12.md`
- `claude/youthful-neumann: REVIEW_THREAD_SUMMARY_2026-04-12.md`
- `claude/youthful-neumann: REVIEWER_SUMMARY.md`
- `historical publication-prep working copy: REVIEWER_SUMMARY.md`

Status:

- context/history only
- never cite as current claim authority

### 3. Cards, scorecards, inventories, and strategy memos

Examples:

- `claude/youthful-neumann: PUBLICATION_CARD_2026-04-12.md`
- `claude/youthful-neumann: PUBLICATION_CARD_FINAL_2026-04-12.md`
- `claude/youthful-neumann: MASTER_DERIVATION_SCORECARD.md`
- `claude/youthful-neumann: STANDALONE_PREDICTIONS_INVENTORY_2026-04-12.md`
- `claude/youthful-neumann: PAPER_STRATEGY_2026-04-12.md`
- `historical publication-prep working copy: COMPLETE_DISCOVERY_SCORECARD_2026-04-11.md`
- `historical publication-prep working copy: PREDICTION_CARD.md`

Status:

- useful for capture/history
- frozen into family `F08`
- not current science authority

### 4. Old root entry surfaces and historical lane front doors

These are not wrong as history, but they are unsafe as current paper entry
surfaces if read first.

Examples:

- `historical publication-prep working copy: PAPER_OUTLINE_2026-04-12.md`
- `historical publication-prep working copy: FLAGSHIP_PAPER_CONTRIBUTION_STATEMENT_NOTE.md`
- `historical publication-prep working copy: lane-specific historical cards in docs/`

Current safe replacements:

- [CURRENT_FLAGSHIP_ENTRYPOINT_2026-04-14.md](../../CURRENT_FLAGSHIP_ENTRYPOINT_2026-04-14.md)
- [README.md](./README.md)
- [PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md)
- [FULL_CLAIM_LEDGER.md](./FULL_CLAIM_LEDGER.md)

## Operational rule

For publication work:

- use the matrix as the hard gate
- use the ledger as the narrative explanation
- use the claims table plus derivation/validation map for manuscript-facing
  claims
- use this audit and [FROZEN_OUT_REGISTRY.md](./FROZEN_OUT_REGISTRY.md) to
  keep older surfaces from outranking the current package
