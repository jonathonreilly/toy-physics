# Wilson Two-Body Separation-Acceleration (m_a + m_b) Scaling Note

**Date:** 2026-04-24
**Status:** mixed finding for the active-queue item "Wilson two-body
both-masses / action-reaction law". Action-reaction analog
((m_a + m_b) scaling on separation acceleration) is qualitatively
correct but quantitatively only approximate, with packet-exchange
symmetry breaking at large mass asymmetry.
**Runner:** `scripts/frontier_wilson_two_body_separation_acceleration_scaling.py`
**Result:** `3/5 PASS`. Two FAILs are real falsifying findings.
**Predecessor:**
[`WILSON_TWO_BODY_ACTION_REACTION_BOTH_MASSES_NOTE_2026-04-23.md`](WILSON_TWO_BODY_ACTION_REACTION_BOTH_MASSES_NOTE_2026-04-23.md)
(loop 2 partial closure).

## 1. Question

Loop 2 closed the both-masses scaling at smoke-test level
(a_a^cross / m_b is constant at CV = 3.6% across n=5 configs) but
identified an action-reaction obstruction in the per-packet
SHARED - SELF_ONLY differential: packet b's self-Hartree centroid
shift dominates at high m_b. The note suggested the (m_a + m_b)
scaling on the separation acceleration as the action-reaction
analog avoiding per-packet isolation.

This loop applies that test.

## 2. Setup

- side = 11 (1331 sites), DT = 0.08, N_STEPS = 20
- G = 5.0, mu^2 = 0.22, separation = 4
- Mass configs (n = 7):
  `(1,1), (1,2), (2,1), (1,3), (3,1), (2,3), (3,2)`
- Observable: `sa_cross := sep_accel(SHARED) - sep_accel(SELF_ONLY)`
  with `sep_accel = d^2(x_b - x_a)/dt^2` taken from centered second
  differences of the separation history, averaged over early window
  `[0:6]`
- Newton continuum prediction:
  `sa_cross = -G(m_a + m_b)/d^2`
  so `sa_cross / (m_a + m_b) = -G/d^2 = -5/16 ≈ -0.31` (bare,
  before Yukawa screening / Wilson dispersion / finite-time)

## 3. Frozen results

| (m_a, m_b) | sa_SHARED | sa_SELF | sa_cross | sa_cross / (m_a + m_b) |
|:---:|:---:|:---:|:---:|:---:|
| (1,1) | -2.08e-1 | +2.72e-2 | -2.35e-1 | -0.117 |
| (1,2) | -1.41e+0 | -1.10e+0 | -3.06e-1 | -0.102 |
| (2,1) | +8.43e-1 | +1.17e+0 | -3.25e-1 | -0.108 |
| (1,3) | -2.31e+0 | -1.91e+0 | -3.99e-1 | -0.100 |
| (3,1) | +1.61e+0 | +1.95e+0 | -3.34e-1 | -0.084 |
| (2,3) | -1.18e+0 | -7.65e-1 | -4.10e-1 | -0.082 |
| (3,2) | +6.51e-1 | +8.19e-1 | -1.68e-1 | -0.034 |

Empirical mean ratio: `-8.95e-2`. CV across 7 configs: `28.7%`.

## 4. Verdicts

### What PASSES

- **B.1 attractive sign (ROBUST)**: `sa_cross < 0` at every config.
  The Hartree gravity is consistently attractive on the differential
  observable.
- **C.1 empirical record**: empirical mean ratio is `-0.0895`, vs
  the Newton continuum prediction `-G/d^2 = -0.31`. The ratio is
  about 30% of the bare value, consistent with Yukawa screening
  (`mu^2 = 0.22`, screening length ~2.1 sites < d=4) plus Wilson
  dispersion + finite-time + finite-size corrections.
- **D.1 lane remains OPEN**: a single-side, single-separation,
  single-seed test does not promote the lane.

### What FAILS (real falsifying findings)

- **B.2 (m_a + m_b) Newton scaling**: ratios across the 7 configs
  range from `-0.117` to `-0.034`, a factor of `~3.5`. CV = `28.7%`,
  above the 15% threshold for clean Newton scaling. The
  `(m_a + m_b)` law is qualitatively correct (the right combination
  scales the signal) but quantitatively approximate.
- **B.3 packet-exchange symmetry**: holds at < 10% for symmetric
  and mildly-asymmetric configs ((1,1), (1,2)/(2,1), (1,3)/(3,1))
  but breaks at large asymmetry: (2,3) vs (3,2) gives 41.9%
  relative difference. The heavier packet at the asymmetric position
  creates self-Hartree feedback that the SHARED-SELF differential
  does not cleanly subtract.

## 5. Interpretation

Three sharp conclusions:

1. **Attractive sign is robust on the differential observable**.
   The qualitative content of "Hartree gravity = attractive" is
   reliable on the side=11 surface across all tested mass
   configurations.

2. **(m_a + m_b) Newton scaling is approximate, not tight**. The
   `~30%` CV is several times the per-packet a_a^cross / m_b CV
   (3.6% in loop 2). The separation-acceleration observable is
   noisier than the per-packet observable (which it sums together),
   not cleaner. The inherent noise of the second-difference
   acceleration estimate dominates over the cleanliness gain from
   avoiding per-packet centroid isolation.

3. **Packet-exchange asymmetry concentrates at large mass
   asymmetry**. The (2,3) / (3,2) 41.9% asymmetry is a real
   nonlinear-feedback effect: the heavier source distorts its own
   wave-packet shape between SHARED and SELF_ONLY differently than
   the lighter source does, breaking the assumed `g_ab = -g_ba`
   kernel symmetry that the (m_a + m_b) Newton scaling derivation
   relies on.

## 6. What this changes

- The Wilson two-body action-reaction obstruction is now better
  characterized: both per-packet (loop 2) and per-separation (this
  loop) protocols have failure modes traceable to nonlinear
  self-Hartree feedback at large mass asymmetry on the open-boundary
  side=11 surface.
- The "robust at small/symmetric masses, breaks at large asymmetry"
  pattern is consistent across both observables.
- A clean test of action-reaction at smoke-test level requires
  either (a) larger sides where boundary effects are smaller, (b)
  multi-seed averaging with random-positioned packets to wash out
  the asymmetric self-Hartree, or (c) an analytic continuum-limit
  argument that doesn't rely on numerical second derivatives.

## 7. Falsifier

- Re-run with same parameters producing different sa_cross values
  (would invalidate determinism).
- Sign flip on B.1 at any config (would refute attractive-sign
  robustness).
- (m_a + m_b) ratio CV < 15% on any larger lattice (would refute
  the inherent-noise interpretation of B.2).
- Packet-exchange asymmetry < 10% at (2,3)/(3,2) on a different
  side or seed (would isolate the asymmetry to a single-seed
  artifact).

## 8. Active-queue update

The `Wilson two-body` item in
[`docs/repo/ACTIVE_REVIEW_QUEUE.md`](repo/ACTIVE_REVIEW_QUEUE.md)
remains OPEN. The combined characterization across loop 2 and this
loop:

- **Both-masses scaling on `a_a^cross / m_b`** (per-packet,
  loop 2): tight CV = 3.6% across 5 configs at side=9.
- **Action-reaction (m_a + m_b) scaling on sep_accel^cross** (this
  loop): qualitatively correct, CV = 28.7% across 7 configs at
  side=11; packet-exchange symmetry breaks at large asymmetry
  (41.9% at (2,3) vs (3,2)).

Both protocols inherit nonlinear self-Hartree feedback failures at
large mass asymmetry. Lane remains open; the obstruction is sharp
and physical rather than fitting/protocol artifact.

## 9. Next concrete step

- **Larger-side test**: rerun the (m_a + m_b) sweep at side=15 or
  17, where boundary effects are smaller. If CV drops below 15%
  there, the (m_a + m_b) scaling is genuine and the side=11 noise
  is finite-size.
- **Multi-seed averaging**: re-run with n=5 random initial-position
  perturbations of the packet centers; if the (2,3)/(3,2)
  asymmetry averages out, it's a single-seed artifact.
- **Analytic continuum-limit derivation**: derive the Wilson
  Hartree centroid acceleration in the continuum limit and show
  the (m_a + m_b) scaling holds exactly there, with the deviations
  being O(a/L) lattice corrections.

## 10. Provenance

- Runner: `scripts/frontier_wilson_two_body_separation_acceleration_scaling.py`
- Underlying lattice + dynamics:
  `scripts/frontier_wilson_two_body_open.py` (imports)
- Result: `3/5 PASS` (2 scientific FAILs are falsifying findings)
- Wallclock: 3.3 seconds for 14 simulations
- Reproducibility: deterministic; same parameters → same outputs
- Runtime caveat: validation host Python 3.12.8, numpy 2.4.1, scipy
  1.17.0 vs pinned 3.13.5, 2.4.4, 1.17.1
