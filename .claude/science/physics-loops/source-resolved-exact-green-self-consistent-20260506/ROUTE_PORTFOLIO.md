# Route Portfolio

| Route | Status | Reason |
|---|---|---|
| A. Add assertions to runner | Already done | `scripts/source_resolved_exact_green_self_consistent.py` emits six PASS/FAIL checks and exits nonzero on failure. |
| B. Refresh note boundary language | Already done | The note declares the calibrated gain as input and excludes full self-consistent field theory. |
| C. Recompute runner output | Verified live | Rerun returned exit code 0 with `PASSED: 6/6` and marker booleans. |
| D. Edit source note again | Rejected | The live note hash is already tied to an audited-clean ledger row; editing it would create stale audit state without new content. |
| E. Record loop handoff | Selected | Branch-local state preserves the stale-prompt diagnosis and verification commands. |
