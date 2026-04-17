# Complex Action: Kernel-Generic vs Gravity-Specific

**Date:** 2026-04-06
**Status:** retained — clean separation of two distinct effects

## Artifact chain

- [`scripts/complex_action_kernel_vs_gravity.py`](../scripts/complex_action_kernel_vs_gravity.py)
- [`logs/2026-04-06-kernel-vs-gravity.txt`](../logs/2026-04-06-kernel-vs-gravity.txt)

## Question

The complex action S = L(1-f) + i*gamma*L*f produces both absorption
(escape < 1) and deflection direction change (TOWARD → AWAY). Are these
the same phenomenon, or two distinct effects?

## Result

They are distinct:

### Kernel-generic: absorption under ANY nonzero field

| Field | gamma=0 escape | gamma=0.5 escape |
| --- | ---: | ---: |
| ZERO | 1.000 | 1.000 |
| UNIFORM (f=0.005) | 1.204 | 0.789 |
| UNIFORM (f=0.01) | 1.450 | 0.623 |
| GRAVITY (s=0.004) | 1.030 | 0.961 |

Mechanism: exp(-k*gamma*L*f) < 1 whenever f > 0 and gamma > 0.
No spatial structure required. Any constant field triggers absorption.

### Gravity-specific: localized deflection crossover

| Field | gamma=0 direction | gamma=0.2 direction |
| --- | --- | --- |
| ZERO | — | — |
| UNIFORM | random (1/2) | random (1/2) |
| GRAVITY | **TOWARD (2/2)** | **AWAY (0/2)** |

Mechanism: the 1/r field gradient couples to the beam centroid.
Only the spatially structured (localized) field produces directional bias.

## Claim boundary

The complex action produces two separable effects:
1. **Kernel-generic absorption**: any f > 0 with gamma > 0 suppresses amplitude
2. **Gravity-specific crossover**: only 1/r field produces TOWARD → AWAY transition

These are NOT the same phenomenon. The absorption is trivial (exponential
decay from imaginary action). The crossover is non-trivial (requires field
gradient and beam-field coupling).
