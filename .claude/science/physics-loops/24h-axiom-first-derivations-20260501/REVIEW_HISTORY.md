# Review History — 24h axiom-first derivations campaign (Block 04)

**Date:** 2026-05-01

This branch (block04) contains only the Block 04 self-review record.
For Blocks 01-03 review history, see PRs #257, #259, #261.

## Block 04 — Microcausality / Lieb-Robinson on A_min

### Branch-local self-review (2026-05-01)

- **theorem note:** [docs/AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md](../../../../docs/AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md)
- **runner:** [scripts/axiom_first_microcausality_check.py](../../../../scripts/axiom_first_microcausality_check.py)
- **log:** [outputs/axiom_first_microcausality_check_2026-05-01.txt](../../../../outputs/axiom_first_microcausality_check_2026-05-01.txt)

#### Findings

- **F1 (no-issue):** all 4 runner tests pass on first run.
- **F2 (no-issue):** small-t scaling `||[α_t(O_0), O_d]|| ~ t^d`
  agrees with the Lieb-Robinson commutator-nesting prediction to
  3-4 significant figures (d=2: 4.000 vs 4.000, d=3: 8.005 vs 8.000,
  d=4: 16.012 vs 16.000).
- **F3 (no-issue):** outside-lightcone exponential decay verified
  with monotone log decrease across d=2 to 7 (slopes consistent
  with `1/r = 1` decay).
- **F4 (no-issue):** Lieb-Robinson upper bound holds with sometimes-
  large slack (ratio ~1e-3 to 1e-11). The bound is qualitatively
  correct; the constant prefactor in (10) is loose, as expected for
  a bound derived via Stirling's inequality.

#### Disposition

- **disposition:** pass.
- **proposal-allowed:** false (per CLAIM_STATUS_CERTIFICATE_BLOCK04.md).
- **branch action:** commit, push, open independent PR with `support`
  honest status.
- **integration action:** record in HANDOFF.md as the framework's
  spacetime-locality theorem, complementary to the existing retained
  cluster-decomposition theorem (which gives spatial decay).

#### Runner results summary (2026-05-01)

```text
Test 1 (equal-time strict locality M1):       PASS  max ||[O_x, O_y]|| = 0
Test 2 (Lieb-Robinson bound M2):              PASS  all (d, t) within bound
Test 3 (outside-lightcone exponential decay): PASS  monotone log decrease
Test 4 (small-t scaling t^d):                 PASS  3/3 fits within 2x

OVERALL: PASS
```
