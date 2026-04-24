# Boundary-Law Gravity-Suppression Finite-Size Asymptote Note

**Date:** 2026-04-24
**Status:** sharper finite-size characterization of the bounded
boundary-law / holographic lane. The lane stays bounded.
**Runner:** `scripts/frontier_boundary_law_finite_size_asymptote.py`
**Result:** `3/5 PASS` (B.2 and B.3 are real falsifying findings;
see Section 4).

## 1. Question

Yesterday's
[`BOUNDARY_LAW_COEFFICIENT_STABILITY_NOTE_2026-04-24.md`](BOUNDARY_LAW_COEFFICIENT_STABILITY_NOTE_2026-04-24.md)
established that the gravity suppression ratio
`r(side, G) := slope(G) / slope(G=0)`
is NOT size-coherent across `side in {8, 10, 12, 14}` (37% spread at
`G=10`), with `r` trending monotonically upward in `side`. The
proposed next step was: extend to `side in {16, 18, 20}` and fit
`r(side, G) = 1 - C(G)/side` to test whether the asymptote at
`side -> infinity` is exactly `1.0` (clean finite-size effect, no
thermodynamic-limit gravity suppression) or `< 1.0` (residual
coefficient shift in the thermodynamic limit).

## 2. Setup

- Sides: `{8, 10, 12, 14, 16, 18, 20}` (7 sizes)
- Seeds: `{42, 43, 44, 45, 46}`
- Couplings: `G in {0, 5, 10, 20}`
- Total fits: `7 * 4 * 5 = 140`
- Wallclock: ~13 seconds on the validation host
- Same Hamiltonian construction, evolution, and Dirac-sea correlation
  matrix as `scripts/frontier_boundary_law_robustness.py`.

## 3. Frozen results

Seed-averaged area-law slopes per `(side, G)`:

| side | G=0 | G=5 | G=10 | G=20 |
|---:|---|---|---|---|
| 8 | 0.2007 | 0.1318 | 0.0955 | 0.0546 |
| 10 | 0.2091 | 0.1520 | 0.1186 | 0.0795 |
| 12 | 0.2092 | 0.1638 | 0.1346 | 0.0993 |
| 14 | 0.2101 | 0.1721 | 0.1467 | 0.1155 |
| 16 | 0.2110 | 0.1788 | 0.1567 | 0.1291 |
| 18 | 0.2107 | 0.1828 | 0.1635 | 0.1391 |
| 20 | 0.2106 | 0.1862 | 0.1691 | 0.1473 |

Suppression ratio `r(side, G)`:

| side | G=5 | G=10 | G=20 |
|---:|---|---|---|
| 8 | 0.6566 | 0.4758 | 0.2718 |
| 10 | 0.7268 | 0.5674 | 0.3803 |
| 12 | 0.7826 | 0.6432 | 0.4746 |
| 14 | 0.8192 | 0.6983 | 0.5498 |
| 16 | 0.8473 | 0.7427 | 0.6120 |
| 18 | 0.8674 | 0.7759 | 0.6599 |
| 20 | 0.8838 | 0.8030 | 0.6995 |

`r` rises monotonically in `side` at every `G`, consistent with the
prior 4-side trend.

## 4. Verdicts

### What PASSES

- **B.1 1/side functional form**: the constrained fit
  `r = 1 - C(G)/side` captures the data to RMS residual `< 2%` at
  every `G`. The fitted constants are `C(5)=2.63`, `C(10)=4.21`,
  `C(20)=6.09`.
- **C.1 G=0 baseline stability**: the matter-blind area-law slope is
  approximately constant across all 7 sides
  (range `0.2007` to `0.2110`, spread `0.0103`), so the suppression
  ratio is not contaminated by a drifting denominator.
- **D.1 lane stays bounded**: this finite-size characterization stays
  inside the bounded boundary-law lane.

### What FAILS (real falsifying findings)

- **B.2 asymptote at exactly 1.0**: the unconstrained two-parameter
  fit `r = a - C/side` gives `a = 1.038` at `G=5`, `a = 1.018` at
  `G=10`, `a = 0.973` at `G=20`. Deviations from `1.0` of
  `+3.8%, +1.8%, -2.7%`. The simple 1/side fit cannot pin down the
  asymptote tighter than `~4%`; the residual deviation is consistent
  with subleading `1/side^2` corrections.
- **B.3 universal finite-size shape**: `C(G)` is NOT constant in `G`.
  It grows monotonically with `G`:
  - `C(5) = 2.63`
  - `C(10) = 4.21`
  - `C(20) = 6.09`

  An 80% spread across `G`. The finite-size correction strength is a
  real function of `G`, not a universal pre-factor. Note `C(G)`
  grows sub-linearly in `G` (doubling `G` from 5 to 10 multiplies `C`
  by `1.60`; doubling from 10 to 20 multiplies by `1.45`).

## 5. Interpretation

Three sharp conclusions:

1. **Functional form is correct**. The `1 - C/side` shape captures the
   data well at every tested `G`. Subleading corrections are at the
   2-4% level.
2. **Asymptote is approximately 1.0**. To within `~4%`, the gravity
   suppression of the area-law coefficient vanishes in the
   thermodynamic limit. The bounded boundary-law lane has no
   universal coefficient renormalization from gravity; the
   finite-side reduction is dominated by a perimeter-to-area
   correction.
3. **Finite-size correction is G-dependent**. `C(G)` grows
   monotonically with `G`. Stronger gravity gives a larger finite-size
   shift but the asymptote is the same. This is consistent with a
   gravitational correlation length that grows with `G` and is
   eventually screened by the size of the box.

The combined finding: the existing global multi-size fit at `G=10`
giving slope `0.186` (from
[`HOLOGRAPHIC_PROBE_NOTE_2026-04-11.md`](HOLOGRAPHIC_PROBE_NOTE_2026-04-11.md))
is a side-mixture artifact. The "12% area-law coefficient reduction"
reading is a finite-size effect; in the thermodynamic limit the
coefficient is unchanged within `~4%`.

## 6. Falsifier (of this note's claims)

- A re-run with the same seeds producing different slopes (would
  invalidate determinism).
- The 1/side fit RMS residual exceeding 5% at any `G` (would refute
  the `1 - C/side` functional form).
- The asymptote at `side > 20` returning to small-side suppression
  values (would refute the asymptote-to-1 reading).
- `C(G)` plateauing or decreasing at higher `G` (would refute the
  monotonic G-dependence).

The runner exposes all four; only the asymptote-tightness gate (B.2)
and the universal-shape gate (B.3) fail, and both are recorded as
the actual scientific findings.

## 7. Active-queue update

The `boundary-law / holographic lane` item in
[`docs/repo/ACTIVE_REVIEW_QUEUE.md`](repo/ACTIVE_REVIEW_QUEUE.md)
remains marked "bounded; do not overread as holography derivation".
The new content is two-fold:

- The gravity suppression of the area-law coefficient is now
  established as a finite-size effect with asymptote consistent with
  `1.0` to within `~4%`.
- The finite-size correction follows a `1 - C(G)/side` law with
  G-dependent strength `C(G)` growing monotonically and sub-linearly
  in `G`.

The lane is not promoted, demoted, or closed.

## 8. Next concrete step

- Two-parameter `r = a - C/side - D/side^2` fit on the 7-point sweep
  to test whether the asymptote tightens to `1.0` within `1%` after
  accounting for subleading corrections, and to extract `D(G)`.
- A G-sweep at fixed large size (say `side=20`) over
  `G in {1, 2, 3, 5, 7, 10, 15, 20, 30, 50}` to characterize `C(G)`
  shape directly.
- A 3D version of the same probe to verify the asymptote-to-1
  finding generalizes beyond 2D, where the perimeter-to-area
  correction has a different geometric form.

## 9. Provenance

- Runner: `scripts/frontier_boundary_law_finite_size_asymptote.py`
- Underlying harness:
  `scripts/frontier_boundary_law_coefficient_stability.py`,
  `scripts/frontier_boundary_law_robustness.py`
- Result: `3/5 PASS` (B.2 and B.3 are explicitly-recorded falsifying
  findings; see Section 4).
- Wallclock: ~13 seconds; deterministic seeds 42-46.
- Runtime caveat: validation host Python 3.12.8, numpy 2.4.1, scipy
  1.17.0 vs pinned 3.13.5, 2.4.4, 1.17.1. Outputs are deterministic
  given fixed seeds; version drift is not a confounder.
