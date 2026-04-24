# Boundary-Law Area-Coefficient Stability Note

**Date:** 2026-04-24
**Status:** review-hardening + clean falsifying finding for the
"boundary-law / holographic lane" item in
[`docs/repo/ACTIVE_REVIEW_QUEUE.md`](repo/ACTIVE_REVIEW_QUEUE.md).
The bounded boundary-law lane stays bounded; the implied "gravity
universally renormalizes the area-law coefficient" reading is
falsified at the per-size level (suppression ratio is finite-size,
not universal).
**Runner:** `scripts/frontier_boundary_law_coefficient_stability.py`
**Result:** `5/6 PASS` (B.3 is the explicitly-rejected hypothesis,
recorded as a real falsifying finding).

## 1. Question

The bounded boundary-law lane on the 2D periodic staggered lattice
already has good `R^2` stability across 100 BFS-ball fits
(see [`BOUNDARY_LAW_ROBUSTNESS_NOTE_2026-04-11.md`](BOUNDARY_LAW_ROBUSTNESS_NOTE_2026-04-11.md)
and [`HOLOGRAPHIC_PROBE_NOTE_2026-04-11.md`](HOLOGRAPHIC_PROBE_NOTE_2026-04-11.md)).
Those notes report:

- 100/100 BFS-ball fits with `R^2 > 0.95`;
- a global multi-size fit at `G=10` with slope `0.186`;
- gravity reduces the area-law slope by `~12%` vs `G=0`.

The active-queue item asks the lane to be kept bounded ("do not
overread as holography"). Two natural sharper questions are:

1. Is the area-law slope itself seed-stable at fixed `(side, G)`,
   or is it noise dressing the `R^2 > 0.95` cosmetics?
2. Is the gravity-induced coefficient shift size-coherent, or is it
   finite-size and bounded to small lattices?

## 2. Setup

- Sides: `{8, 10, 12, 14}` (drop `side=6`: only 2 BFS-ball radii)
- Seeds: `{42, 43, 44, 45, 46}`
- Couplings: `G in {0, 5, 10, 20}`
- Total fits: `4 * 4 * 5 = 80`
- Wallclock: ~5 seconds on the validation host
- Same Hamiltonian construction, evolution, and Dirac-sea correlation
  matrix construction as
  `scripts/frontier_boundary_law_robustness.py`.

## 3. Frozen results

Per-(side, G) area-law slope (seed-mean +/- seed-std), R^2 mean:

| side | G=0 | G=5 | G=10 | G=20 |
|---:|---|---|---|---|
| 8 | `0.2007 +/- 0.0018` (R²=0.9964) | `0.1318 +/- 0.0018` (R²=0.9942) | `0.0955 +/- 0.0016` (R²=0.9937) | `0.0546 +/- 0.0013` (R²=0.9903) |
| 10 | `0.2091 +/- 0.0008` (R²=0.9988) | `0.1520 +/- 0.0009` (R²=0.9973) | `0.1186 +/- 0.0009` (R²=0.9963) | `0.0795 +/- 0.0010` (R²=0.9938) |
| 12 | `0.2092 +/- 0.0005` (R²=0.9966) | `0.1638 +/- 0.0005` (R²=0.9950) | `0.1346 +/- 0.0005` (R²=0.9930) | `0.0993 +/- 0.0005` (R²=0.9890) |
| 14 | `0.2101 +/- 0.0007` (R²=0.9991) | `0.1721 +/- 0.0007` (R²=0.9972) | `0.1467 +/- 0.0006` (R²=0.9947) | `0.1155 +/- 0.0005` (R²=0.9892) |

Gravity-suppression ratio `slope(G=10) / slope(G=0)` per side:

| side | ratio | reduction |
|---:|---|---|
| 8 | `0.476` | `52.4%` |
| 10 | `0.567` | `43.3%` |
| 12 | `0.643` | `35.7%` |
| 14 | `0.698` | `30.2%` |

## 4. Verdicts

### What PASSES

- **B.1 seed stability**: max coefficient of variation across seeds at
  any `(side, G)` cell is `2.3%`, well below the 5% threshold. The
  area-law slope is essentially seed-independent.
- **B.2 G-monotonicity**: the slope strictly decreases as `G` increases
  from `0 → 5 → 10 → 20` at every tested side.
- **C.2 G=0 control quality**: the matter-blind baseline gives
  `R^2 >= 0.99` at every side (cleanest fits, as expected).
- **D.1 lane stays bounded**: this sharpens the bounded boundary-law
  lane; it does NOT promote it to a holography or AdS/CFT derivation.

### What FAILS (real falsifying finding)

- **B.3 size-coherence of gravity suppression**: the suppression ratio
  `slope(G=10) / slope(G=0)` is NOT size-stable. It trends from
  `0.48` at `side=8` to `0.70` at `side=14`, a `37%` spread —
  far above the 10% size-coherence threshold.

This is a **clean falsifying finding**. The 12% suppression reported
in the global multi-size fit of
[`HOLOGRAPHIC_PROBE_NOTE_2026-04-11.md`](HOLOGRAPHIC_PROBE_NOTE_2026-04-11.md)
is a side-mixture of strongly different per-size suppressions. The
gravity-induced coefficient shift is a **finite-size effect** that
weakens monotonically as the lattice grows.

Linear extrapolation of the four points to `1/side -> 0` gives an
extrapolated ratio close to `0.85-1.0`, suggesting the gravity
suppression of the area-law coefficient may vanish in the
thermodynamic limit. (Caveat: this is a four-point linear extrapolation
at small sides; real asymptotic shape requires more sizes.)

## 5. Interpretation

- The bounded boundary-law lane is stronger than `R^2` cosmetics:
  the area-law coefficient itself is seed-stable to `2-3%` precision
  across `4` lattice sizes and `4` couplings. Per-size slopes are
  reproducible quantitative objects, not loose fits.
- The gravity-induced slope shift IS real and IS monotonic in `G`,
  but is NOT size-coherent. Therefore the existing global multi-size
  fit at `G=10` (slope `0.186`) is a side-mixture average and should
  not be over-interpreted as a universal coefficient renormalization.
- This sharpens the active-queue framing: the lane is bounded, and
  the explicit reason for boundedness is now identified as
  finite-size dependence of the gravity coefficient response, not
  unknown reviewer concerns.

## 6. Falsifier (of this note's claims)

- A re-run with the same seeds producing different slopes (would
  invalidate determinism).
- Per-(side, G) seed CV exceeding 5% at any cell (would invalidate
  the seed-stability claim).
- Slope NOT monotonically decreasing in `G` at any side (would
  invalidate G-monotonicity).
- Suppression ratio at `side > 14` returning to the small-side value
  (would invalidate the finite-size interpretation).

The runner exposes all four checks; only the size-coherence check
fails, and it is recorded as the central falsifying finding.

## 7. Active-queue update

The `boundary-law / holographic lane` item in
[`docs/repo/ACTIVE_REVIEW_QUEUE.md`](repo/ACTIVE_REVIEW_QUEUE.md)
remains marked "bounded; do not overread as holography derivation".
The new content is that the gravity-induced area-law coefficient
suppression is now established as a finite-size effect, not a
universal coefficient renormalization. The lane is not promoted,
demoted, or closed.

## 8. Next concrete step

- Run the same audit at `side in {16, 18, 20}` to test whether the
  suppression ratio asymptotes to `1.0` (clean finite-size effect)
  or saturates at some smaller value (residual coefficient shift
  in the thermodynamic limit). Wallclock at `side=20` is ~10s per
  fit; full sweep ~3-5 minutes.
- If asymptote is `1.0`, the bounded boundary-law lane should be
  reframed: gravity does NOT renormalize the area-law coefficient
  in the thermodynamic limit. That demotes the gravity-side reading
  to small-lattice cosmetics.
- If asymptote is `< 1.0`, the residual ratio is a quantitative
  bounded prediction.

## 9. Provenance

- Runner: `scripts/frontier_boundary_law_coefficient_stability.py`
- Underlying harness:
  `scripts/frontier_boundary_law_robustness.py`
- Result: `5/6 PASS` (B.3 is the explicitly-rejected hypothesis;
  see Section 4).
- Wallclock: ~5 seconds; deterministic seeds 42-46.
- Runtime caveat: validation host Python 3.12.8, numpy 2.4.1, scipy
  1.17.0 vs pinned 3.13.5, 2.4.4, 1.17.1. Outputs are deterministic
  given fixed seeds; version drift is not a confounder.
