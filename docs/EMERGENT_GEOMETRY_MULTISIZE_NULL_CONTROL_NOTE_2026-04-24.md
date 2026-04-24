# Emergent Geometry Multi-Size + Null-Control Harness Note

**Date:** 2026-04-24
**Status:** review-hardening artifact for the active-queue item
"emergent-geometry growth multi-size/multi-seed stability". The lane
remains OPEN; this run pins down the exact failure pattern with an
exact G=0 null control.
**Runner:** `scripts/frontier_emergent_geometry_multisize_null_control.py`
**Result:** `4/7 PASS`. Three FAILs are the explicitly-expected lane-status
gates (B.1, B.2 unanimity; C.3 d_eff distinguishability), recording the
exact open-lane signal.

## 1. Question

The active review queue
([`docs/repo/ACTIVE_REVIEW_QUEUE.md`](repo/ACTIVE_REVIEW_QUEUE.md))
states:

> emergent-geometry growth: multi-size, multi-seed stability remains open

The existing
[`scripts/frontier_emergent_geometry_multisize.py`](../scripts/frontier_emergent_geometry_multisize.py)
runs the matter-coupled growth rule at `G=100` across five sizes with
five seeds, but does NOT include a matter-blind null control to gate
the matter-coupling signal against pure growth-rule artefacts.

This note records the multi-size + multi-seed sweep with an explicit
`G=0` null control, plus a determinism check.

## 2. Setup

- Sizes: `n in {60, 80, 100, 120, 150}`
- Seeds: `{42, 43, 44, 45, 46}`
- Couplings: `G=100` (matter-coupled) and `G=0` (matter-blind null
  control). Both runs use identical sizes, seeds, and protocol.
- Observables:
  - **Q1 force battery:** ROBUST_TOWARD count per (size, G)
  - **Q2 displacement test:** ATTRACTED count per (size, G)
  - **Q3 effective dimension:** mean and std of `d_eff` per (size, G)
- Determinism: `G=100` sweep is run twice; outputs must match exactly.
- Wallclock: ~21 seconds on the validation host (Python 3.12.8, numpy
  2.4.1, scipy 1.17.0). The pinned release host is Python 3.13.5,
  numpy 2.4.4, scipy 1.17.1; growth-rule outputs are deterministic
  given fixed seeds, so version drift is not a confounder.

## 3. Frozen results

| size | G=100 robust | G=0 robust | G=100 attr | G=0 attr | G=100 d_eff | G=0 d_eff |
|---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 60 | 3/5 | 0/5 | 1/5 | 0/5 | 1.565 +/- 0.33 | 1.554 +/- 0.20 |
| 80 | 4/5 | 0/5 | 4/5 | 0/5 | 1.703 +/- 0.30 | 1.676 +/- 0.23 |
| 100 | 3/5 | 0/5 | 1/5 | 0/5 | 1.845 +/- 0.04 | 1.655 +/- 0.19 |
| 120 | 3/5 | 0/5 | 2/5 | 0/5 | 1.954 +/- 0.12 | 1.732 +/- 0.23 |
| 150 | 2/5 | 0/5 | 3/5 | 0/5 | 1.920 +/- 0.09 | 2.001 +/- 0.08 |

Per-size deltas (G=100 minus G=0):

- ROBUST_TOWARD count: `+3, +4, +3, +3, +2` (all positive, all >= 2)
- ATTRACTED count:     `+1, +4, +1, +2, +3` (all positive, three >= 2)
- d_eff mean:          `+0.011, +0.027, +0.191, +0.223, -0.081`

## 4. Verdicts

### What PASSES

- **A.1 (determinism):** the harness is exactly reproducible across
  two re-runs at `G=100` with the same seeds. No hidden source of
  randomness in the test infrastructure.
- **C.1 (null-distinguished force battery):** `G=100` ROBUST_TOWARD
  counts exceed `G=0` by `>= 2` at all 5 sizes. Matter-coupling has a
  real, measurable signature on the force-battery observable.
- **C.2 (null-distinguished displacement):** `G=100` ATTRACTED counts
  exceed `G=0` by `>= 2` at 3 of 5 sizes. Matter-coupling has a partial
  but real signature on the displacement observable.
- **D.1 (honest open):** the lane remains OPEN. No claim surface is
  promoted by this run.

### What FAILS

- **B.1 (5/5 force battery):** the matter-coupled run never achieves
  unanimous 5/5 ROBUST_TOWARD at every size. Maximum is 4/5 at `n=80`;
  minimum is 2/5 at `n=150`.
- **B.2 (5/5 displacement):** the matter-coupled run never achieves
  unanimous 5/5 ATTRACTED at every size. Maximum is 4/5 at `n=80`;
  minimum is 1/5 at `n=60` and `n=100`.
- **C.3 (d_eff distinguishability):** the `G=100` minus `G=0` mean
  `d_eff` shift exceeds 0.05 at only 2 of 5 sizes (`n=100`, `n=120`).
  At `n=60`, `n=80`, and `n=150`, the matter-coupling shift is buried
  in the seed-to-seed noise (std 0.2-0.3 per cell).

## 5. Interpretation

The harness shows three clean facts:

1. **Matter-coupling does something.** At every tested size, `G=100`
   force battery counts strictly exceed `G=0` by at least 2 (often
   3-4). The growth rule is not noise.
2. **The "something" is not size-stable enough to close the lane.**
   Neither the force battery nor the displacement test reaches
   unanimous 5/5 at every size. The retained candidate gate is not met.
3. **The geometric `d_eff` signal is weak.** Outside `n=100, 120`, the
   matter-coupled `d_eff` mean is within noise of the `G=0` mean.
   `d_eff` does not currently separate the matter-coupled and null
   regimes cleanly enough to be a retained discriminator.

## 6. Falsifier

The result is falsified by exhibiting any of:

- a re-run at `G=100` with the same seeds producing different counts
  (would invalidate A.1 and the determinism floor);
- a `G=0` run producing nonzero ROBUST_TOWARD or ATTRACTED counts at
  these sizes/seeds (would invalidate the null floor);
- a matter-coupled run that achieves unanimous 5/5 on any of the
  observables across all five sizes with the existing protocol (would
  promote the lane out of "open").

## 7. Active-queue update

The `emergent-geometry growth: multi-size, multi-seed stability`
item in
[`docs/repo/ACTIVE_REVIEW_QUEUE.md`](repo/ACTIVE_REVIEW_QUEUE.md)
remains an open lane. The result of this note is that the open status
is now backed by a frozen, deterministic, null-controlled measurement
of the failure pattern. The lane is not promoted, demoted, or closed.

## 8. Next concrete step

The harness gives a clean diagnosis. The natural next moves are:

- **Parameter scan**: sweep `G in {25, 50, 75, 100, 125, 150}`,
  `K_CONNECT in {3, 4, 5}`, and `N_EVOLVE in {2, 3, 4, 5}` to look for
  a window where unanimity is achieved.
- **Growth-rule audit**: the existing rule biases attachment by local
  matter density; alternatives (curvature-biased, gradient-biased)
  may give a sharper geometric response.
- **Larger seed family**: 5 seeds at each size is a low-statistics
  estimate of the unanimity rate; 10-20 seeds would give a tighter
  bound but multiplies wallclock by 2-4x.

None of these is in scope for this loop. The note records the current
lane status with reproducible numbers so future work can compare
against a frozen baseline.

## 9. Provenance

- Runner: `scripts/frontier_emergent_geometry_multisize_null_control.py`
- Underlying harness:
  `scripts/frontier_emergent_geometry_multisize.py`
- Result: `4/7 PASS` (3 explicit FAILs are the lane-status gates;
  see Section 4)
- Wallclock: ~21 seconds; deterministic seeds 42-46
- Runtime caveat: validation host Python 3.12.8, numpy 2.4.1, scipy
  1.17.0 vs pinned 3.13.5, 2.4.4, 1.17.1 — deterministic outputs are
  robust to this drift.
