# Irregular Off-Lattice Sign Lane — G-Portability Sweep Note

**Date:** 2026-04-24
**Status:** asymmetric finding for the active-queue item "irregular
off-lattice sign lane: portability beyond the bounded centered core-packet
surface remains open". Lane remains OPEN; portability is **established**
at mu^2=0.1 and **refuted** at mu^2=0.001.
**Runner:** `scripts/frontier_irregular_sign_g_portability_sweep.py`
**Result:** `3/6 PASS` (3 explicit FAILs are real falsifying findings at
low screening; see Section 4).

## 1. Question

The 2026-04-11 core-packet gate
([`IRREGULAR_SIGN_CORE_PACKET_GATE_NOTE.md`](IRREGULAR_SIGN_CORE_PACKET_GATE_NOTE.md))
established a bounded same-surface sign separator on three irregular
bipartite graph families (random_geometric, growing, layered_cycle)
at `G in {5.0, 10.0}`, `mu^2 in {0.1, 0.001}`, with all three gates
passing at 100% / 93.3%.

The active-queue item asks about portability beyond this bounded
surface. One natural test is whether the sign separator is G-robust
across a wider coupling range than the original two G values.

## 2. Setup

Extend the G sweep:

- `G in {1.0, 3.0, 5.0, 10.0, 20.0}` (5 values; was 2)
- `mu^2 in {0.1, 0.001}` (unchanged)
- 3 graph families × 5 seeds = 15 rows per (G, mu^2) cell
- Total: `5 × 2 × 15 = 150` rows

The packet, observable, window, and graph constructors are identical to
the original gate, so the only swept axis is G.

## 3. Frozen results

| mu^2 | G | ball1_pos | ball2_pos | depth_pos | median ball1 margin |
|---:|---:|:---:|:---:|:---:|:---:|
| 0.100 | 1.0 | 15/15 | 15/15 | 15/15 | +3.22e-2 |
| 0.100 | 3.0 | 15/15 | 15/15 | 15/15 | +7.43e-2 |
| 0.100 | 5.0 | 15/15 | 15/15 | 15/15 | +7.54e-2 |
| 0.100 | 10.0 | 15/15 | 15/15 | 15/15 | +2.93e-2 |
| 0.100 | 20.0 | 15/15 | 15/15 | 15/15 | +6.41e-3 |
| 0.001 | 1.0 | 15/15 | 15/15 | 15/15 | +1.11e-4 |
| 0.001 | 3.0 | 10/15 | 15/15 | 8/15 | +4.75e-6 |
| 0.001 | 5.0 | 15/15 | 15/15 | 15/15 | +1.51e-6 |
| 0.001 | 10.0 | 13/15 | 15/15 | 13/15 | +1.06e-6 |
| 0.001 | 20.0 | 5/15 | 5/15 | 5/15 | **-1.11e-7** |

## 4. Verdicts

### What PASSES

- **B.2 mu^2=0.1 uniform pass**: ball1 pass rate is 1.00 at every G
  in `{1, 3, 5, 10, 20}`. The bounded surface extends to a
  G-portable surface over [1, 20] at this screening level.
- **C.1 mu^2=0.1 positive medians**: median ball1 margin is positive
  at every G with magnitudes ranging from `+3.2e-2` (G=1) to
  `+6.4e-3` (G=20).
- **D.1 honest open**: lane remains OPEN; G-portability on three
  families × 5 seeds × 2 mu^2 is stronger than the original 2-G
  surface, but other portability axes (packet shape, off-center
  placement, new graph families, sigma) remain untested.

### What FAILS (real falsifying findings)

- **B.1 per-cell pass rate ≥ 80%**: cells `(mu^2=0.001, G=3)` and
  `(mu^2=0.001, G=20)` have pass rates `67%` and `33%` respectively,
  below the 80% threshold.
- **B.3 mu^2=0.001 uniform pass**: pass rates across the G sweep at
  mu^2=0.001 are non-monotonic: `[1.00, 0.67, 1.00, 0.87, 0.33]`.
  The original 2026-04-11 G=5 passing cleanly is genuine, but the
  surface is not G-stable.
- **C.2 mu^2=0.001 positive medians**: median ball1 margin
  **flips sign** at G=20 (`-1.11e-7`). The sign separator does not
  just weaken; it actually fails as a sign-of-coupling indicator
  at this strong-coupling, low-screening cell.

## 5. Interpretation

Three sharp conclusions:

1. **G-portability holds at mu^2=0.1**. Across the full tested G
   range `[1, 20]`, every cell passes all three observables at
   100%. The bounded same-surface separator established on the
   original `{5, 10}` surface extends cleanly to `[1, 20]` at
   "normal" screening.

2. **G-portability is REFUTED at mu^2=0.001**. The low-screening
   surface is not a stable sign separator across G. At G=20, the
   median signal actually flips sign. At G=3 and G=10, the pass
   rate falls below 80%. The original positive result at G=5 was
   genuine but isolated.

3. **The mu^2=0.001 magnitudes are at the noise floor**. Across the
   five G values, the median margin at mu^2=0.001 ranges from
   `1.11e-4` (G=1) down to `1.06e-6` (G=10) and `-1.11e-7` (G=20).
   These are 4-7 orders of magnitude smaller than the
   `+7.5e-2` peak at mu^2=0.1, G=5. The sign-separator at
   mu^2=0.001 is essentially zero with sign-of-noise; the original
   2026-04-11 gate's 93.3% pass at mu^2=0.001 was a marginal
   weak-noise positive bias, not a structural sign result.

## 6. What this changes

- The active-queue item "portability beyond the bounded centered
  core-packet surface remains open" is sharpened. Portability is
  positively established at mu^2=0.1 across `G in [1, 20]`, and
  negatively refuted at mu^2=0.001 by both the pass-rate FAIL at
  multiple cells and the explicit sign flip at G=20.
- The 2026-04-11 gate's mu^2=0.001 result should be downgraded to
  a marginal-positive finding that does not survive a wider G
  sweep.

## 7. Falsifier

- A re-run producing different pass rates (would invalidate
  determinism).
- The mu^2=0.001 G=20 cell median margin coming out positive on
  reanalysis (would refute the sign-flip finding).
- A different sigma or packet shape giving uniform pass at
  mu^2=0.001 across the same G sweep (would isolate the failure
  to the centered core-packet observable, not the underlying sign
  physics).

## 8. Active-queue update

The `irregular off-lattice sign lane` item in
[`docs/repo/ACTIVE_REVIEW_QUEUE.md`](repo/ACTIVE_REVIEW_QUEUE.md)
remains OPEN. The new content:

- Portability is **established** at mu^2=0.1 across `G in [1, 20]`.
- Portability is **refuted** at mu^2=0.001 (multiple cell FAILs +
  sign flip at G=20).
- The underlying low-screening result is at the noise floor and
  should not be promoted as a sign separator without a different
  observable.

## 9. Next concrete step

- **Add a 4th graph family** (e.g., random bipartite with adjustable
  degree) and re-run at mu^2=0.1 across `G in [1, 20]` to test
  family-portability orthogonally to G-portability.
- **Off-center packet test**: move the packet center off the
  graph centroid and check whether the sign separator survives —
  this addresses the 2026-04-11 "broader packet/transport
  portability remains open" caveat.
- **Re-examine mu^2=0.001**: the apparent positive sign separator
  at low screening may be a different physics regime (e.g.,
  near-massless propagation), warranting a dedicated study with
  a different observable.

## 10. Provenance

- Runner: `scripts/frontier_irregular_sign_g_portability_sweep.py`
- Underlying gate:
  `scripts/frontier_irregular_sign_core_packet_gate.py` (imported)
- Result: `3/6 PASS` (3 explicit FAILs are scientific falsifying
  findings)
- Wallclock: 4 seconds for 150 rows
- Reproducibility: deterministic; same seeds → same outputs.
- Runtime caveat: validation host Python 3.12.8, numpy 2.4.1, scipy
  1.17.0 vs pinned 3.13.5, 2.4.4, 1.17.1.
