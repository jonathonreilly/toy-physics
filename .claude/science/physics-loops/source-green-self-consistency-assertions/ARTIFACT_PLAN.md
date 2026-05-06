# Artifact Plan

## Edited Artifacts

- `scripts/source_resolved_exact_green_self_consistent.py`
  - Adds explicit assertion summary.
  - Freezes calibrated gain as setup input.
  - Exits nonzero if any bounded check fails.

- `docs/SOURCE_RESOLVED_EXACT_GREEN_SELF_CONSISTENT_NOTE.md`
  - States calibrated-gain boundary.
  - Links the 2026-05-06 assertion transcript.
  - Narrows the safe read to the frozen calibrated setup.

## Generated Artifacts

- `outputs/source_resolved_exact_green_self_consistent_assertions_2026-05-06.txt`

## Audit Data

- Refresh citation graph, runner classification, audit ledger, and effective
  status summary.
- Archive prior `audited_numerical_match` verdict and reset row to
  `unaudited`.
