# Review History — 24h axiom-first derivations campaign (Block 09)

**Date:** 2026-05-01

This branch (block09) contains only the Block 09 self-review record.
For Blocks 01-08, see PRs #257, #259, #261, #263, #265, #266, #269, #272.

## Block 09 — Birkhoff theorem on framework GR

### Branch-local self-review (2026-05-01)

- **theorem note:** [docs/AXIOM_FIRST_BIRKHOFF_THEOREM_NOTE_2026-05-01.md](../../../../docs/AXIOM_FIRST_BIRKHOFF_THEOREM_NOTE_2026-05-01.md)
- **runner:** [scripts/axiom_first_birkhoff_check.py](../../../../scripts/axiom_first_birkhoff_check.py)
- **log:** [outputs/axiom_first_birkhoff_check_2026-05-01.txt](../../../../outputs/axiom_first_birkhoff_check_2026-05-01.txt)

#### Findings

- **F1 (no-issue):** all 6 runner tests pass.
- **F2 (no-issue):** ODE residual `r dA/dr + A - 1` for
  `A = 1 - 2GM/r` vanishes at <1e-15 across all tested (M, r) pairs.

#### Disposition

- **disposition:** pass.
- **proposal-allowed:** false.
- **branch action:** commit, push, open independent PR.

#### Runner results summary (2026-05-01)

```text
Test 1 (ansatz structure):                          PASS
Test 2 (R_tr = 0 -> partial_t B = 0):               PASS
Test 3 (R_tt/A + R_rr/B = 0 -> AB = const):         PASS
Test 4 ((rA)' = 1 -> A = 1 - 2GM/r):                PASS  max resid <1e-15
Test 5 (Schwarzschild satisfies all R_munu = 0):    PASS
Test 6 (Schwarzschild radius r_s = 2GM):            PASS

OVERALL: PASS
```
