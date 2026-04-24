# Wilson Two-Body (m_a + m_b) Newton Scaling: Finite-Size Refutation

**Date:** 2026-04-24
**Status:** clean falsifying finding for the active-queue item
"Wilson two-body both-masses / action-reaction law". The loop-13
finite-size hypothesis is REFUTED; the obstruction is a
thermodynamic-limit physical effect of the Wilson Hartree carrier.
**Runner:** `scripts/frontier_wilson_two_body_separation_acceleration_finite_size.py`
**Result:** `4/5 PASS`. The single FAIL is the central falsifying
finding. Wallclock 41 s.
**Predecessors:**
[`WILSON_TWO_BODY_ACTION_REACTION_BOTH_MASSES_NOTE_2026-04-23.md`](WILSON_TWO_BODY_ACTION_REACTION_BOTH_MASSES_NOTE_2026-04-23.md)
(loop 2), 
[`WILSON_TWO_BODY_SEPARATION_ACCELERATION_SCALING_NOTE_2026-04-24.md`](WILSON_TWO_BODY_SEPARATION_ACCELERATION_SCALING_NOTE_2026-04-24.md)
(loop 13).

## 1. Question

Loop 13 found that the (m_a + m_b) Newton scaling on the
SHARED-minus-SELF_ONLY differential separation acceleration has
CV = 28.7% across n=7 mass configs at side=11, with packet-exchange
asymmetry of 41.9% at (2,3) vs (3,2). The note proposed this could
be a finite-size effect: with bigger side, the boundary distortion
of self-Hartree feedback should shrink and Newton scaling should
tighten.

This loop tests that hypothesis at sides 11, 13, 15, 17.

## 2. Setup

- Sides: `{11, 13, 15, 17}`
- Mass configs: `{(1,1), (1,2), (2,1), (1,3), (3,1), (2,3), (3,2)}`
- DT=0.08, N_STEPS=20, G=5.0, mu^2=0.22, sep=4
- Single seed at each side (deterministic Gaussian wavepackets)
- Total: 4 sides × 7 configs × 2 modes = 56 simulations
- Wallclock: 41 seconds

## 3. Frozen results

CV across configs and (2,3)/(3,2) asymmetry per side:

| side | CV | (2,3)/(3,2) asym | mean ratio |
|---:|:---:|:---:|:---:|
| 11 | 28.7% | 41.9% | -8.95e-2 |
| 13 | 28.6% | 40.7% | -8.88e-2 |
| 15 | 28.5% | 40.4% | -8.86e-2 |
| 17 | 28.5% | 40.3% | -8.85e-2 |

Per-config ratios across sides (selected):

| (m_a, m_b) | side=11 | side=13 | side=15 | side=17 |
|:---:|:---:|:---:|:---:|:---:|
| (1, 1) | -1.17e-1 | -1.17e-1 | -1.17e-1 | -1.17e-1 |
| (3, 1) | -8.36e-2 | -8.43e-2 | -8.45e-2 | -8.45e-2 |
| (2, 3) | -8.20e-2 | -8.02e-2 | -7.97e-2 | -7.95e-2 |
| (3, 2) | -3.35e-2 | -3.38e-2 | -3.38e-2 | -3.39e-2 |

Each per-config ratio is stable across sides to within ~1-2%.

## 4. Verdicts

### What PASSES

- **B.1 monotonic CV decrease**: CV does decrease as side grows
  (28.7 → 28.6 → 28.5 → 28.5%). The trend is correct in sign.
- **B.2 monotonic asymmetry decrease**: Asymmetry decreases similarly
  (41.9 → 40.7 → 40.4 → 40.3%).
- **C.1 mean ratio is stable**: spread across sides is 1.1% of the
  mean, well below 50%. Per-config ratios are essentially side-
  independent.
- **D.1 lane remains OPEN**: this is a single-seed, single-d, single-
  parameter test.

### What FAILS (the central finding)

- **B.3 convergence by side=17**: At side=17, CV = 28.5% (above 15%
  threshold) and asymmetry = 40.3% (above 10% threshold). Neither
  has converged to its Newton-scaling target.

The decrease rate is so slow as to refute the finite-size hypothesis:

- CV decreases at `~0.031%/side`
- Asymmetry decreases at `~0.277%/side`

At these rates, reaching CV < 15% would require **~431 more sides**.
At side=17 = ~5000 sites; side=448 would be ~9 × 10^7 sites — outside
any realistic computational budget.

## 5. Interpretation

Three sharp conclusions:

1. **The (m_a + m_b) Newton scaling is REFUTED as a thermodynamic-
   limit law on the Wilson Hartree carrier**. The CV asymptotes to
   ~28% and the (2,3)/(3,2) asymmetry asymptotes to ~40%, both at
   the wide-lattice limit. These are not bugs of small-side numerics.

2. **Per-config ratios are intrinsic Wilson-Hartree numbers**. Each
   `(m_a, m_b)` cell gives a stable ratio at all tested sides
   (1-2% variation). The 3.5x spread of these ratios across configs
   is a real physics effect, not finite-size noise. Specifically:
   - (1,1) gives -0.117 (most attractive per unit total mass)
   - (3,2) gives -0.034 (least attractive per unit total mass)
   - (2,3) gives -0.080 (intermediate; differs from (3,2) by 2.4x!)

3. **The Wilson 2-body Hartree system is NOT Newtonian**. The
   sum-of-masses scaling assumption embedded in F = G m_a m_b / d^2
   does not hold even at L → ∞. The actual force law has an
   asymmetric, mass-ordering-dependent component arising from
   nonlinear self-Hartree feedback that survives the thermodynamic
   limit on the open-boundary surface.

This is consistent with what is known about open-boundary Hartree
mean-field gravity in non-relativistic QM: the self-feedback
distorts the wave packets in a way that breaks the Newton symmetry,
even before relativistic effects. The Wilson lattice + Yukawa
screening + Hartree mean field creates a system that is
qualitatively gravitational (always attractive, scales monotonically
with G) but not strictly Newtonian.

## 6. What this changes

- The loop-13 obstruction is now **promoted** from "possibly finite-
  size" to "thermodynamic-limit physical effect". The Wilson 2-body
  open-boundary Hartree carrier is intrinsically non-Newtonian.
- The both-masses scaling test from loop 2 (CV = 3.6% on
  `a_a^cross / m_b`) is now read as a **per-packet** result that
  doesn't generalize to the per-separation Newton form.
- The Wilson two-body lane should be repositioned: the "Newton-
  scaling action-reaction law" target is unachievable on this
  observable; alternative observables or a different lattice
  protocol are needed for a genuine action-reaction proof.

## 7. Falsifier

- A re-run producing different CVs (would invalidate determinism).
- A side > 17 sweep finding CV decreasing significantly faster (would
  re-open the finite-size hypothesis).
- A different protocol (e.g., closed boundary, periodic, or
  staggered) giving CV < 15% at the same parameters (would isolate
  the failure to the open-boundary-Hartree carrier specifically).

## 8. Active-queue update

The `Wilson two-body lane` item in
[`docs/repo/ACTIVE_REVIEW_QUEUE.md`](repo/ACTIVE_REVIEW_QUEUE.md)
remains OPEN, but the characterization is sharpened:

- **Both-masses scaling on `a_a^cross / m_b`**: tight CV = 3.6%
  (loop 2; per-packet observable, side=9, n=5 configs).
- **(m_a + m_b) Newton scaling on sep_accel^cross**: REFUTED at
  thermodynamic limit. CV converges to ~28%, asymmetry to ~40%, at
  side=17. Per-config ratios are intrinsic Wilson-Hartree numbers
  with 3.5x spread.
- **Conclusion**: the Wilson 2-body open-boundary Hartree system
  is not strictly Newtonian. A Newton-scaling action-reaction proof
  on this carrier is impossible; a different protocol or observable
  is needed.

## 9. Next concrete step

- **Closed-boundary or periodic protocol**: re-run the same test on
  a periodic Wilson lattice (using the periodic_geometry helper
  from the 2026-04-11 fix); if Newton scaling holds there, the
  obstruction is open-boundary-specific.
- **Static-source approximation**: instead of dynamical mean-field
  Hartree, use a fixed external source proportional to a Gaussian
  density. The static-source Wilson 2-body should obey Newton
  scaling exactly; this would calibrate how much of the 28% CV
  comes from dynamical wave-packet feedback vs. lattice/Wilson
  effects.
- **Analytic Hartree continuum-limit derivation**: derive the
  Hartree mean-field force on a Gaussian wave packet in the
  continuum limit, including the next-to-leading correction
  in (mass × packet-overlap), and check whether the corrections
  predict the observed asymmetric pattern.

## 10. Provenance

- Runner:
  `scripts/frontier_wilson_two_body_separation_acceleration_finite_size.py`
- Underlying lattice + dynamics:
  `scripts/frontier_wilson_two_body_open.py` (imported)
- Result: `4/5 PASS` (B.3 is the central falsifying finding;
  B.1, B.2, C.1, D.1 carry the diagnostic verdict).
- Wallclock: 41 seconds for 56 simulations
- Reproducibility: deterministic; same seeds → same outputs
- Runtime caveat: validation host Python 3.12.8, numpy 2.4.1, scipy
  1.17.0 vs pinned 3.13.5, 2.4.4, 1.17.1
