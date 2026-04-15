# Submission Sequence

**Date:** 2026-04-14  
**Purpose:** ordered cleanup plan from the current package state to submission.

This file answers one question:

> what should be done, in order, so the package is clean and stable before
> public arXiv release and any downstream private journal adaptation?

## Phase 1. Lock the authority surface

1. keep the package matrix-driven
   - [PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md) is the canonical capture surface
2. keep the claim surface narrow
   - [CLAIMS_TABLE.md](./CLAIMS_TABLE.md) defines the retained flagship claims
3. keep the evidence contract explicit
   - [DERIVATION_VALIDATION_MAP.md](./DERIVATION_VALIDATION_MAP.md)
4. keep excluded work documented
   - [FROZEN_OUT_REGISTRY.md](./FROZEN_OUT_REGISTRY.md)

## Phase 2. Normalize the reviewer path

1. root repo points to the current flagship entrypoint
2. publication package README points to the reviewer guide
3. reviewer guide points to:
   - state doc
   - matrix
   - claims table
   - ledger
   - frozen-out registry

## Phase 3. Normalize manuscript structure

### Public arXiv manuscript

- retained core only
- derived `v` as the closed quantitative flagship result
- weak-field gravity plus restricted strong-field companion
- one disciplined paragraph on live gates

### Private journal adaptation

- derived from the public arXiv surface
- shorter presentation where needed
- no competing public draft on `main`

## Phase 4. Add the missing reviewer-facing tables

1. keep [QUANTITATIVE_SUMMARY_TABLE.md](./QUANTITATIVE_SUMMARY_TABLE.md) current
2. ensure every row there is represented in:
   - the matrix
   - the ledger
3. ensure every retained row there is also represented in:
   - the claims table
   - the derivation/validation map

## Phase 5. Clean stale authority

1. rewrite or quarantine old closure-language notes
2. do not allow branch-local scorecards to outrank the matrix
3. keep stale review packets out of the manuscript path
4. maintain [STALE_AUTHORITY_AUDIT_2026-04-14.md](./STALE_AUTHORITY_AUDIT_2026-04-14.md)

## Phase 6. Reproducibility freeze

1. archive logs for retained runners
2. archive figure-prep artifacts
3. pin one public commit hash
4. record exact runner pass summaries
5. maintain a release-freeze note like
   [REPRODUCIBILITY_FREEZE_2026-04-14.md](./REPRODUCIBILITY_FREEZE_2026-04-14.md)

## Phase 7. Fold in late scientific closures cleanly

When DM or other live lanes advance:

1. update science authority note + runner
2. classify in matrix
3. update ledger
4. if retained, update:
   - claims table
   - derivation/validation map
   - results index
   - drafts

Do not update manuscript prose first.

## Current remaining cleanup after this package pass

- build a final manuscript-facing quantitative table into the drafts if desired
- align figure plan and captions to the matrix wording where needed
- perform one final stale-authority sweep before submission freeze
