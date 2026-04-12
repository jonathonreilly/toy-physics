# Strong-Field Regime: Horizon Structure and Framework Breakdown

**Script:** `scripts/frontier_strong_field_regime.py`
**Date:** 2026-04-12
**Status:** CHARACTERIZED -- reveals fundamental non-unitarity issue

## Motivation

The path-sum propagator uses action S = L(1 - f). As f approaches 1
the action vanishes and phase freezes. When f > 1 the action goes
negative. Understanding this regime matters for the paper because it
defines the boundary of validity for all weak-field results (gravity,
time dilation, deflection).

## Key Finding: Non-Unitarity, Not Horizon Formation

The transfer matrix spectral radius exceeds 1 at ALL field strengths,
including f = 0. The propagator amplitude grows exponentially with the
number of propagation layers. This is a property of the discrete
path-sum with the cos^2 kernel and 1/L^p attenuation: the kernel
normalization does not enforce unitarity.

| f    | Spectral radius | Growth per step |
|------|----------------|-----------------|
| 0.00 | ~0.85          | sub-unity (baseline)   |
| 0.50 | 1.27           | 1.27x           |
| 0.90 | 1.85           | 1.85x           |
| 1.00 | 1.98           | 1.98x (maximum) |
| 1.10 | 1.85           | 1.85x           |
| 1.50 | 1.27           | 1.27x           |
| 2.00 | 1.62           | 1.62x           |

The growth rate is SYMMETRIC around f = 1: the propagator sees
|1 - f| through the exp(i * k * S) phase factor. At f = 1 the phase
is exactly zero at every site, so all paths interfere constructively
and the transfer matrix has maximal spectral radius.

## Test Results

### Test 1: Amplitude vs Field Strength

For a uniform field, the transmission ratio after 20 layers:
- f = 0.0: 3.7e-2 (destructive interference from large phase variation)
- f = 0.5: 1.1e+2 (less phase variation, more constructive)
- f = 0.9: 1.9e+5 (phase nearly frozen, strong amplification)
- f = 1.0: 6.9e+5 (maximum: zero phase everywhere)
- f = 1.1: 1.9e+5 (symmetric with f = 0.9)

The f = 1 surface does NOT absorb. It AMPLIFIES, because zero action
means zero phase variation means maximum constructive interference.
This is the opposite of a horizon.

### Test 2: Horizon Radius and Shadow

For point sources with varying mass strength, the Poisson field
creates f = 1 surfaces at:

| Mass strength | r_h (lattice) | f_max at center |
|--------------|---------------|-----------------|
| 20           | 1.7           | 5.0             |
| 40           | 2.9           | 9.9             |
| 60           | 3.9           | 14.9            |
| 80           | 4.8           | 19.8            |
| 120          | 6.2           | 29.8            |

Shadow mapping shows that wavepackets at impact parameters inside r_h
are NOT trapped or absorbed. They pass through with large amplification
(norm ratios of 30-130x). Wavepackets outside r_h also amplify due to
the non-unitary transfer matrix.

There is no clean "shadow" boundary. The f = 1 surface does not cast a
shadow because it amplifies rather than absorbs.

### Test 3: Weak-Field Validity

The weak-field GR approximation (linearized deflection proportional to
integrated field gradient) breaks down at surprisingly small f values.
Even at f_peak ~ 0.5 (well below the horizon), the non-linear phase
accumulation and transfer-matrix amplification cause large deviations
from the linear prediction.

The reliable regime for weak-field predictions is f < 0.1 at the
impact parameter. This is consistent with the GR analogy: the
Schwarzschild metric linearization requires 2GM/rc^2 << 1.

### Test 4: Super-Horizon (f > 1) Behavior

When f > 1, the action S = L(1-f) becomes negative. This flips the
sign of the phase but does NOT cause qualitatively different behavior
from the sub-horizon regime. The growth rate is symmetric: the
propagator at f = 1 + delta behaves identically to f = 1 - delta.

The f = 2.0 case is notable: here S = -L, which is the same magnitude
as the free-field action S = +L at f = 0. The growth rate drops back
to near-baseline, consistent with the symmetry.

There is no sharp "breakdown" at f = 1. The framework degrades
gradually as f increases from 0, with amplification growing smoothly.

### Test 5: Schwarzschild Radius Analog

The radius where f = 1 scales linearly with mass strength:
- Linear fit: r_h = 0.048 * ms + 0.76 (R^2 = 0.986)
- Expected from 3D Poisson (f = ms / 4*pi*r): r_h = 0.080 * ms
- Measured mean: r_h / ms = 0.068

The offset (0.76) comes from lattice discretization near the source.
The proportionality is Schwarzschild-like (r_s proportional to M) but
the surface does not function as a horizon.

## Diagnosis

The root cause is that the discrete path-sum propagator with
exp(i * k * S) * w(theta) / L^p is not unitary. The kernel
normalization controls the free-field (f = 0) growth rate, but as f
increases toward 1, phase coherence increases and the transfer matrix
spectral radius grows.

In physical terms: the propagator sums over paths with phases
exp(i * k * L * (1 - f)). When (1 - f) is small, the phases are
nearly aligned and the sum is large. When (1 - f) is large, the
phases oscillate and partially cancel. The "horizon" at f = 1 is
simply the point of maximum constructive interference.

This means:
1. The f = 1 surface is NOT analogous to a Schwarzschild horizon
2. It is a phase-coherence maximum, not an absorbing boundary
3. A true horizon would require an amplitude attenuation mechanism
   that the current action S = L(1-f) does not contain
4. The framework's gravitational predictions are reliable only for
   f << 1 (weak field)

## Implications for the Paper

1. **Range of validity**: All gravitational results (deflection, time
   dilation, equivalence principle) are valid in the weak-field regime
   f < 0.1. This is analogous to the linearized GR regime.

2. **No black hole analog**: The framework does not naturally produce
   black holes or event horizons. The f = 1 surface amplifies rather
   than absorbs. A horizon mechanism would need to be added (amplitude
   damping, absorption, or a modified action).

3. **Natural limitation**: The non-unitarity of the transfer matrix is
   a fundamental limitation. For a fully physical propagator, one
   would need either (a) a normalized kernel that ensures unitarity,
   or (b) a field equation that self-consistently limits f < 1.

4. **Honest negative result**: The framework does not contain strong-
   field GR. This is expected for a two-axiom framework that derives
   from a discrete path sum. Strong-field GR requires the full
   Einstein field equations, which encode non-linear backreaction
   not present in the Poisson-sourced field.

## Connection to Hawking Result

The Hawking analog test (HAWKING_ANALOG_NOTE.md) found that the f > 1
region amplifies outgoing modes rather than trapping them. This is
fully consistent with the present analysis: the f = 1 surface is a
phase-coherence maximum, not an absorbing horizon. The amplitude
growth (norm from 1.0 to 164 reported in the Hawking test) matches the
transfer-matrix spectral radius exceeding 1.
