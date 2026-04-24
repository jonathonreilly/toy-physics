# Irregular Off-Lattice Sign Lane — Family-Portability Sweep Note

**Date:** 2026-04-24
**Status:** mixed finding for the active-queue item "irregular
off-lattice sign lane: portability beyond the bounded centered
core-packet surface remains open". Family-portability is
**observable-dependent**, not uniform across observables.
**Runner:** `scripts/frontier_irregular_sign_family_portability_sweep.py`
**Result:** `3/5 PASS`. Two explicit FAILs characterize the
observable-dependent boundary.
**Predecessor:**
[`IRREGULAR_SIGN_G_PORTABILITY_SWEEP_NOTE_2026-04-24.md`](IRREGULAR_SIGN_G_PORTABILITY_SWEEP_NOTE_2026-04-24.md)
(established G-portability on 3 families at mu^2=0.1).

## 1. Question

Yesterday's G-portability sweep showed the sign separator passes at
every `G in {1, 3, 5, 10, 20}` at `mu^2=0.1` across 3 existing
bipartite graph families. The natural next-step question: does
portability extend to a topologically orthogonal 4th graph family?

## 2. Setup

New family: `bipartite_erdos_renyi`

- 2 sublattices, 32 nodes per side (64 total)
- color-0 nodes on y=0, color-1 nodes on y=1 (allows meaningful
  "depth" interpretation)
- nearest-neighbor bipartite link (connectivity guarantee)
- random bipartite edges with probability `p_edge = 0.18`
  (expected long-range degree ~6 per node)

This topology class is genuinely different from the three existing
families:

- `random_geometric`: square-lattice-like with small jitter and
  distance cutoff
- `growing`: preferential-attachment-like with 4 nearest opposite
  neighbors
- `layered_cycle`: structured layered graph with cyclic cross-links

The Erdős–Rényi random bipartite has the highest
clustering-coefficient randomness and longest typical path.

Sweep: `G in {1, 3, 5, 10, 20}` at `mu^2 = 0.1`, seeds 42-46.
Total: 25 rows.

## 3. Frozen results

| G | ball1_pos | ball2_pos | depth_pos | median ball1 | median ball2 | median depth |
|---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1.0 | 3/5 | 5/5 | 5/5 | +3.74e-2 | +6.71e-3 | +2.07e-2 |
| 3.0 | 3/5 | 5/5 | 5/5 | +9.98e-2 | +1.88e-2 | +5.56e-2 |
| 5.0 | 3/5 | 5/5 | 5/5 | +1.31e-1 | +2.75e-2 | +8.99e-2 |
| 10.0 | 4/5 | 5/5 | 5/5 | +6.77e-2 | +2.91e-2 | +9.00e-2 |
| 20.0 | 3/5 | 5/5 | 3/5 | +8.57e-3 | +3.03e-3 | +7.51e-3 |

## 4. Verdicts

### What PASSES

- **B.2 ball2 family-portable**: at every G, 5/5 seeds give a
  positive ball2 margin. The ball2 observable is topology-robust.
- **C.1 median ball1 positive**: median ball1 margin is positive at
  every G (+8.6e-3 to +1.3e-1). The SIGN of the separator is correct
  on average on the new family.
- **D.1 lane remains OPEN**: this is a 1-family extension; broader
  portability remains untested.

### What FAILS (real falsifying findings)

- **B.1 ball1 pass rate ≥ 80%**: ball1 pass rate is 60% at `G in
  {1, 3, 5, 20}` and 80% at G=10. 2 of 5 seeds consistently give the
  WRONG SIGN on ball1 at most G values.
- **B.3 depth pass rate ≥ 80%**: depth pass rate is 100% at G=1, 3,
  5, 10 but drops to 60% at G=20. The depth observable also has a
  topology-dependent boundary.

## 5. Interpretation

Three sharp conclusions:

1. **Family-portability is observable-dependent.** On the 4th
   (Erdős–Rényi) family:
   - `ball2_margin` is fully portable (100% per cell).
   - `ball1_margin` has 60% pass rate at most G values — 2 of 5 seeds
     give the wrong sign.
   - `depth_margin` fails only at G=20.

2. **The SIGN of ball1 is still correct on average.** Median
   positivity is preserved at every G. The 2 sign-wrong seeds are
   individual topology realizations, not a structural signal
   inversion.

3. **Ball2 is the most topology-robust observable.** It passes
   uniformly on this 4th family just as it passed uniformly on the
   original 3 families' mu^2=0.1 surface. For publication-grade use,
   ball2 should be promoted over ball1 as the primary sign separator.

## 6. What this changes

- Family-portability is **partially refuted**: 2 of 3 observables
  (ball1, depth) show seed-fragility on the Erdős–Rényi family that
  they did NOT show on the original 3 families.
- Family-portability is **partially confirmed**: 1 of 3 observables
  (ball2) is uniformly robust.
- The "core-packet sign separator" is therefore not a single
  observable — it's a family of observables with different
  topology-robustness characteristics.

## 7. Falsifier

- A re-run producing different pass rates (invalidates determinism).
- Ball2 failing at some G on this new family (would refute the
  "ball2 is topology-robust" reading).
- A different Erdős–Rényi `p_edge` value giving uniform ball1 pass
  (would isolate the failure to a specific topology parameter).
- Running on a 5th family and finding that ball2 ALSO fails there
  (would refute the observable-robustness reading).

## 8. Active-queue update

The `irregular off-lattice sign lane` item in
[`docs/repo/ACTIVE_REVIEW_QUEUE.md`](repo/ACTIVE_REVIEW_QUEUE.md)
remains OPEN. The new content: family-portability is observable-
dependent. `ball2` is topology-robust; `ball1` and `depth` have
seed-fragility boundaries on the Erdős–Rényi topology.

## 9. Next concrete step

- **Ball2 single-observable re-gate**: extend to 5+ families, multiple
  packet shapes, off-center placement, all at mu^2=0.1, using ball2
  only. If ball2 stays uniformly robust, promote it as the primary
  sign separator.
- **Parameter scan on p_edge**: sweep Erdős–Rényi `p_edge` values to
  map where ball1 transitions from uniform-pass (at small p_edge,
  close to nearest-neighbor) to the observed 60%-pass region (at
  p_edge=0.18) and possibly to full failure (at high p_edge).
- **Seed-level diagnosis**: inspect the 2/5 seeds that give negative
  ball1 at G=1, 3, 5 to identify the topology feature that causes
  sign inversion.

## 10. Provenance

- Runner: `scripts/frontier_irregular_sign_family_portability_sweep.py`
- Underlying gate:
  `scripts/frontier_irregular_sign_core_packet_gate.py` (imported)
- Result: `3/5 PASS` (2 scientific FAILs are falsifying findings)
- Wallclock: 1.1 seconds, 25 rows
- Reproducibility: deterministic; same seeds → same outputs.
- Runtime caveat: validation host Python 3.12.8, numpy 2.4.1, scipy
  1.17.0 vs pinned 3.13.5, 2.4.4, 1.17.1.
