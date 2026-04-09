# Lensing β Sweep — Fourth Failed Moonshot, Explicit Retraction

**Date:** 2026-04-07
**Status:** retained NEGATIVE — the lensing β sweep produced what looked like an exact canonical 1/b law at β = 5 (slope = −1.0114, R² = 0.9995, per-point `kubo·b` constant to 1.7%) but the sanity checks falsified it immediately. Denser β sampling shows β = 5 is an isolated island of clean shape surrounded by messy slopes at nearby β values (β=3 gives −1.25, β=7 gives −1.39), and the H=0.35 refinement at β=5 gives NEGATIVE kubo values (gravity away from mass) with slope −0.79. This is the FOURTH "moonshot positive" in the lensing lane that has failed under scrutiny in a single session. The retained finding now is that the program does not have a clean gravitational-lensing signature anywhere in tested parameter space. Each of the attempted explanations (ray integral, finite-path transition, narrow-beam limit) has been falsified.

## Artifact chain

- [`scripts/lensing_beta_sweep.py`](../scripts/lensing_beta_sweep.py)
- [`logs/2026-04-07-lensing-beta-sweep.txt`](../logs/2026-04-07-lensing-beta-sweep.txt)

## Question

After Lane L++ falsified the finite-path ray-integral explanation
([`LENSING_LONG_PATH_TEST_NOTE.md`](LENSING_LONG_PATH_TEST_NOTE.md)),
the hypothesis was that the measured slope ≈ −1.43 comes from
**wave-mechanical diffraction**, because the default angular weight
`β = 0.8` gives a 1/e angular width of ~45° (heavily diffracted beam).

If this is the mechanism, varying β should change the slope:
- Large β (narrow angular window): beam approaches a localized ray,
  so slope should approach the analytical ray-deflection prediction
- Small β (delocalized beam): slope should be different again

The β sweep directly tests this prediction.

## Apparent result (before sanity checks)

| β | slope | R² |
| ---: | ---: | ---: |
| 0.1 | −1.93 | 0.58 (noisy) |
| 0.4 | −1.11 | 0.81 |
| 0.8 | −1.28 | 0.97 |
| 2.0 | −1.45 | 0.998 |
| **5.0** | **−1.0114** | **0.9995** |

At β = 5, the slope was **−1.01** — essentially exact canonical 1/b
lensing. The per-point `kubo · b` products were constant to **1.7%**:

| b | kubo | kubo · b | rel dev |
| ---: | ---: | ---: | ---: |
| 3.0 | 0.0189 | 0.0567 | +0.93% |
| 4.0 | 0.0139 | 0.0556 | −1.02% |
| 5.0 | 0.0112 | 0.0560 | −0.31% |
| 6.0 | 0.0094 | 0.0564 | +0.40% |

This looked like the moonshot — canonical 1/b lensing in the narrow-beam
limit, recovered by the expected mechanism.

## Sanity check 1: is β=5 really an asymptote?

Dense β sweep at H=0.5 T=15 on the same b ∈ {3..6}:

| β | slope | R² | per-point `kubo·b` spread |
| ---: | ---: | ---: | ---: |
| 1.5 | −1.56 | 0.995 | 40.41% |
| 3.0 | −1.25 | 0.999 | 17.89% |
| **5.0** | **−1.01** | **0.9995** | **1.71%** |
| 7.0 | −1.39 | 0.997 | 27.15% |
| 10.0 | −1.27 | 0.999 | 18.69% |
| 20.0 | −1.31 | 0.999 | 21.47% |

**β = 5 is an isolated spike**, not an asymptote. Nearby β values give
wildly different slopes and 1/b shapes. β=3 gives −1.25 with 18%
spread, β=7 gives −1.39 with 27% spread, β=20 gives −1.31 with 21%
spread. None of them is near −1.

If the β=5 result were a true asymptotic limit (narrow beam →
canonical 1/b), we would expect β=7, 10, 20 to give slopes close to
−1 with similarly clean spreads. They don't. **β=5 is a coincidence
at one specific parameter value.**

## Sanity check 2: does β=5 survive H refinement?

At H=0.5 (same coarse lattice as the main result) β=5 gave positive
kubo values: 0.0189, 0.0139, 0.0112, 0.0094.

At H=0.35 (finer lattice, same β=5):

| b | kubo (H=0.35, β=5) |
| ---: | ---: |
| 3.0 | **−0.0343** |
| 4.0 | **−0.0276** |
| 5.0 | **−0.0231** |
| 6.0 | **−0.0198** |

**All four values are NEGATIVE** — the sign of the gravity response
flipped. At H=0.5 the beam deflects TOWARD the mass (positive); at
H=0.35 it deflects AWAY (negative). Slope = −0.79 with 14% per-point
spread.

The entire "canonical 1/b at β=5" result is an artifact of the
H=0.5 coarse lattice at one specific β value. It does not survive
refinement.

## Honest interpretation

This is the **fourth failed moonshot in the lensing lane** in a
single session:

1. **Lane L**: "matches 1/b lensing" at H=0.35 — downgraded by Lane L+
   (H=0.25 shows slope −1.43, not −1.03)
2. **Finite-path explanation note**: "analytical formula matches at
   1.5%" — falsified by Lane L++ (the T=7.5 short-path gives the
   same slope, not the T-dependent slope the formula predicts)
3. **Lane L++ reverse claim** (brief): "L-independent slope ≈ −1.43
   IS the physics" — this stood but was already a retreat from the
   previous claims
4. **β sweep**: "canonical 1/b at β=5" — falsified by the two sanity
   checks in this note (β=5 is not an asymptote, and the result
   doesn't survive H refinement)

Each time the pattern has been: initial measurement looks clean →
headline claim → one more test (refinement, different parameter,
or wider sample) destroys the claim → retraction. Four cycles in
one session.

**The retained finding about the lensing lane is now:**

- The program does NOT have a clean gravitational-lensing signature
- The kubo_true(b) slope at b ∈ {3..6} is strongly dependent on β,
  H, and T_phys, ranging from about −0.79 to −1.93 depending on
  configuration
- The most stable single number is at (β=0.8, H=0.25, T_phys=15):
  **slope ≈ −1.43 with R² = 0.998**. This is reproducible at the same
  setup but has no known physical mechanism and no simple analytical
  match
- Multiple explanations have been tried (ray integral, finite-path
  transition, narrow-beam ray limit) and all falsified
- The model is NOT doing canonical weak-field gravitational lensing
  in any tested regime

## What was almost shipped but got caught

I was about to claim: "the program reproduces canonical 1/b
gravitational lensing in the narrow-beam limit (β = 5) with per-point
agreement to 2%." This would have been the fifth bogus moonshot of
the session if not caught by:

1. Denser β sampling (β = 5 is not an asymptote)
2. Refinement check at H = 0.35 (sign flips!)

The sanity-check discipline is the ONLY thing preventing these
coincidence-based headlines from becoming retained claims. The
session has demonstrated repeatedly that 2-refinement or
2-parameter-point "matches" are unreliable, and any apparent
positive needs (a) dense sampling in parameter space and (b)
refinement in H before being claimed.

## Frontier map adjustment (Update 17)

| Row | Before | Lane L# β sweep |
| --- | --- | --- |
| Strength against harshest critique | clean power law exponent ≈ −1.43 of unknown origin | **no change** — the β sweep did not find a clean mechanism |
| Compact underlying principle | empirical slope at default config | **no change** — β=5 "canonical 1/b" is an artifact |
| Gravitational lensing signature | not yet found | **not found** — multiple attempts falsified |
| Scorecard pattern | periodic premature claims | **this pattern documented as a lane constraint** |

## What to attack next

This lane exhausts the "tweak parameters to find lensing" approach.
Further searches in (β, k, b, T, H) space are unlikely to produce a
result that survives sanity checks, given the pattern observed in
this session.

The remaining legitimate next moves are:

1. **Direct analytical derivation of `kubo_true(b)` from the
   wave-mechanical Kubo formula**, integrating over the actual
   propagator's amplitude distribution rather than a geometric-optics
   integral. This is the pen-and-paper version of the explanation
   that actually matches the data.
2. **Pivot away from the lensing lane entirely.** The retained
   physics (Lanes 4–8b wave equation, Lane α static Kubo continuum
   limit on Fam1) is unaffected by any of this chaos. The right move
   might be to stop chasing the lensing mirage and return to
   Codex's matrix-free comparator work or to Born derivation.
3. **Document the session's moonshot-failure pattern as a finding
   in its own right.** The systematic pattern of 2-measurement
   matches collapsing under sanity checks is itself information
   about what the program can and cannot support empirically.

## Bottom line

> "The β sweep produced an apparent canonical 1/b lensing match at
> β = 5 (slope = −1.0114, R² = 0.9995, per-point kubo·b constant
> to 1.7%), but two sanity checks falsified it: (a) denser β
> sampling shows β=5 is an isolated spike, not an asymptote —
> β = 3, 7, 10, 20 give slopes in the −1.25 to −1.56 range with
> 17–40% per-point spreads; (b) refinement to H=0.35 at β=5 gives
> NEGATIVE kubo values (sign flip) with slope −0.79. The entire
> 'canonical 1/b at narrow β' result is a coincidence at one
> specific (β, H) pair that does not survive any sanity check.
> This is the fourth failed moonshot in the lensing lane in this
> session. The retained finding is that the program does not
> have a clean gravitational-lensing signature anywhere in tested
> parameter space; the most stable number is slope ≈ −1.43 at
> the default configuration (β=0.8, H=0.25, T=15), and its
> mechanism remains unknown."
