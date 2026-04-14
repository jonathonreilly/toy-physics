# Stale Authority Audit

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

- [/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/YT_FLAGSHIP_CLOSURE_NOTE.md](/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/YT_FLAGSHIP_CLOSURE_NOTE.md)
- [/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/YT_FULL_CLOSURE_NOTE.md](/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/YT_FULL_CLOSURE_NOTE.md)
- [/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/DM_FLAGSHIP_CLOSURE_NOTE.md](/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/DM_FLAGSHIP_CLOSURE_NOTE.md)
- [/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/CKM_FULL_CLOSURE_NOTE.md](/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/CKM_FULL_CLOSURE_NOTE.md)
- [/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/CKM_CLOSURE_NOTE.md](/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/CKM_CLOSURE_NOTE.md)
- [/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/DM_CLOSURE_CASE_NOTE.md](/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/DM_CLOSURE_CASE_NOTE.md)

Status:

- historical / branch-local only
- may be cited in [FROZEN_OUT_REGISTRY.md](./FROZEN_OUT_REGISTRY.md), not as
  current paper authority

### 2. Review packets and reviewer summaries

Examples:

- [/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/CODEX_REVIEW_PACKET_2026-04-12.md](/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/CODEX_REVIEW_PACKET_2026-04-12.md)
- [/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/REVIEW_RESUBMISSION_2026-04-12.md](/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/REVIEW_RESUBMISSION_2026-04-12.md)
- [/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/REVIEW_THREAD_SUMMARY_2026-04-12.md](/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/REVIEW_THREAD_SUMMARY_2026-04-12.md)
- [/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/REVIEWER_SUMMARY.md](/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/REVIEWER_SUMMARY.md)
- [REVIEWER_SUMMARY.md](/private/tmp/physics-publication-prep/docs/REVIEWER_SUMMARY.md)

Status:

- context/history only
- never cite as current claim authority

### 3. Cards, scorecards, inventories, and strategy memos

Examples:

- [/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/PUBLICATION_CARD_2026-04-12.md](/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/PUBLICATION_CARD_2026-04-12.md)
- [/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/PUBLICATION_CARD_FINAL_2026-04-12.md](/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/PUBLICATION_CARD_FINAL_2026-04-12.md)
- [/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/MASTER_DERIVATION_SCORECARD.md](/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/MASTER_DERIVATION_SCORECARD.md)
- [/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/STANDALONE_PREDICTIONS_INVENTORY_2026-04-12.md](/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/STANDALONE_PREDICTIONS_INVENTORY_2026-04-12.md)
- [/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/PAPER_STRATEGY_2026-04-12.md](/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/PAPER_STRATEGY_2026-04-12.md)
- [COMPLETE_DISCOVERY_SCORECARD_2026-04-11.md](/private/tmp/physics-publication-prep/docs/COMPLETE_DISCOVERY_SCORECARD_2026-04-11.md)
- [PREDICTION_CARD.md](/private/tmp/physics-publication-prep/docs/PREDICTION_CARD.md)

Status:

- useful for capture/history
- frozen into family `F08`
- not current science authority

### 4. Old root entry surfaces and historical lane front doors

These are not wrong as history, but they are unsafe as current paper entry
surfaces if read first.

Examples:

- [PAPER_OUTLINE_2026-04-12.md](/private/tmp/physics-publication-prep/docs/PAPER_OUTLINE_2026-04-12.md)
- [FLAGSHIP_PAPER_CONTRIBUTION_STATEMENT_NOTE.md](/private/tmp/physics-publication-prep/docs/FLAGSHIP_PAPER_CONTRIBUTION_STATEMENT_NOTE.md)
- lane-specific historical cards in `/private/tmp/physics-publication-prep/docs/`

Current safe replacements:

- [CURRENT_FLAGSHIP_ENTRYPOINT_2026-04-14.md](/private/tmp/physics-publication-prep/docs/CURRENT_FLAGSHIP_ENTRYPOINT_2026-04-14.md)
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
