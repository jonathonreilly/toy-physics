# Publication Control Plane

**Date:** 2026-04-14  
**Purpose:** define how the publication package is organized and how new work
enters it without creating drift.

This file is the package architecture doc. It is not a science authority by
itself. Its job is to tell contributors and reviewers where each kind of claim
belongs.

## 1. Package layers

The package has four layers.

### A. Retained flagship core

These are the claims the paper may state directly as retained.

Canonical files:

- [CLAIMS_TABLE.md](./CLAIMS_TABLE.md)
- [DERIVATION_VALIDATION_MAP.md](./DERIVATION_VALIDATION_MAP.md)
- [CI3_Z3_PUBLICATION_STATE_2026-04-12.md](../../CI3_Z3_PUBLICATION_STATE_2026-04-12.md)

### B. Observation-facing bounded portfolio

These are quantitatively important results that reviewers will ask about even
when they are not promoted.

Canonical files:

- [PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md)
- [FULL_CLAIM_LEDGER.md](./FULL_CLAIM_LEDGER.md)
- [QUANTITATIVE_SUMMARY_TABLE.md](./QUANTITATIVE_SUMMARY_TABLE.md)

### C. Live flagship gates

These are open lanes whose closure would materially change the paper.

Canonical files:

- [PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md)
- [FULL_CLAIM_LEDGER.md](./FULL_CLAIM_LEDGER.md)
- [CI3_Z3_PUBLICATION_STATE_2026-04-12.md](../../CI3_Z3_PUBLICATION_STATE_2026-04-12.md)

### D. Frozen-out families

These are significant workstreams that are intentionally excluded from the
flagship surface but documented so they are not lost.

Canonical files:

- [FROZEN_OUT_REGISTRY.md](./FROZEN_OUT_REGISTRY.md)
- [PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md)
- [FULL_CLAIM_LEDGER.md](./FULL_CLAIM_LEDGER.md)

## 2. File roles

| File | Role |
|---|---|
| [README.md](./README.md) | package front door |
| [EXTERNAL_REVIEWER_GUIDE.md](./EXTERNAL_REVIEWER_GUIDE.md) | fast orientation for new readers |
| [PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md) | canonical one-line capture surface |
| [FULL_CLAIM_LEDGER.md](./FULL_CLAIM_LEDGER.md) | narrative explanation of the matrix |
| [FROZEN_OUT_REGISTRY.md](./FROZEN_OUT_REGISTRY.md) | explicit registry of excluded but important work |
| [CLAIMS_TABLE.md](./CLAIMS_TABLE.md) | retained flagship claim surface only |
| [DERIVATION_VALIDATION_MAP.md](./DERIVATION_VALIDATION_MAP.md) | evidence contract for retained/manuscript-facing claims |
| [QUANTITATIVE_SUMMARY_TABLE.md](./QUANTITATIVE_SUMMARY_TABLE.md) | reviewer-facing prediction/observation table |
| [RESULTS_INDEX.md](./RESULTS_INDEX.md) | manuscript section to note/runner map |
| [GRAVITY_PUBLICATION_PACKAGE_SUMMARY_2026-04-15.md](./GRAVITY_PUBLICATION_PACKAGE_SUMMARY_2026-04-15.md) | compact gravity-package overview and theorem ladder |
| [REPRODUCIBILITY_FREEZE_2026-04-14.md](./REPRODUCIBILITY_FREEZE_2026-04-14.md) | current pinned release slice |
| [STALE_AUTHORITY_AUDIT_2026-04-14.md](./STALE_AUTHORITY_AUDIT_2026-04-14.md) | quarantine list for stale authority |
| [NATURE_PACKAGE.md](./NATURE_PACKAGE.md) | letter package rule set |
| [ARXIV_PACKAGE.md](./ARXIV_PACKAGE.md) | long-form package rule set |
| [SUBMISSION_CHECKLIST.md](./SUBMISSION_CHECKLIST.md) | final pre-submission operational checklist |
| [SUBMISSION_SEQUENCE_2026-04-14.md](./SUBMISSION_SEQUENCE_2026-04-14.md) | ordered cleanup plan from now to submission |

## 3. Entry rules for new results

Any new result that might matter for publication should enter the package in
this order:

1. add or update the authority note and runner on the science branch
2. classify the result in [PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md)
3. explain that classification in [FULL_CLAIM_LEDGER.md](./FULL_CLAIM_LEDGER.md)
4. if retained, also add it to:
   - [CLAIMS_TABLE.md](./CLAIMS_TABLE.md)
   - [DERIVATION_VALIDATION_MAP.md](./DERIVATION_VALIDATION_MAP.md)
   - [RESULTS_INDEX.md](./RESULTS_INDEX.md)
5. if important but excluded, add or update the family in
   [FROZEN_OUT_REGISTRY.md](./FROZEN_OUT_REGISTRY.md)
6. only then update manuscript prose

## 4. Hard-gate policy for new science

No new science result should enter the package out of order.

- No manuscript claim unless it appears in
  [PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md).
- No retained claim unless it also appears in
  [CLAIMS_TABLE.md](./CLAIMS_TABLE.md).
- No retained manuscript-facing claim unless it also appears in
  [DERIVATION_VALIDATION_MAP.md](./DERIVATION_VALIDATION_MAP.md).
- No draft-only promotion. Update the matrix and ledger before updating the
  drafts.

## 5. Reviewer-safety rules

- If a result is not in the matrix, it is not publication-captured.
- If it is in the matrix but not in the claims table, it is not on the
  retained flagship claim surface.
- If it is important but excluded, it should appear in the frozen-out registry.
- If a result is in the manuscript, it must also appear in the derivation /
  validation map.

## 6. Current package shape

As of this date:

- the retained core is broad and real
- the bounded quantitative portfolio is large enough that it must be surfaced,
  not hidden
- the live gates are now sharply concentrated in:
  - DM relic mapping
  - renormalized `y_t`
  - CKM / quantitative flavor

That is the package architecture the drafts must follow.
