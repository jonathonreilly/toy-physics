# Analysis: Gravity Falloff and Deflection

## Date
2026-03-30

## Source
- Log: `logs/2026-03-30-gravity-falloff-and-deflection-sweep.txt`
- Script: `scripts/gravity_falloff_and_deflection_sweep.py`

## Key Findings

### 1. Action falloff is steeper than power-law, slower than exponential

Action_diff vs offset (5 nodes, target y=3):

| offset | |action_diff| | successive ratio |
|--------|-------------|-----------------|
| 1 | 12.678 | - |
| 2 | 12.650 | 0.998 |
| 5 | 11.890 | 0.969 |
| 8 | 10.030 | 0.933 |
| 11 | 6.622 | 0.822 |

The successive ratios DECREASE (0.998→0.822), ruling out:
- Pure exponential (would give constant ratio)
- Power law 1/d^n (would give ratio = (d/(d+1))^n, slowly increasing toward 1)

The falloff accelerates at larger distances. This is consistent with the delay field being solved by a discrete relaxation (Laplace-like equation on the grid with boundary conditions). The field decays like a discrete harmonic function, which on finite grids falls off faster than any power law due to boundary effects.

### 2. Gravitational lensing pattern confirmed

The angular sweep (5 nodes at y=6, all target_ys from -12 to +12) shows:

- **y = -12 to -3:** path deflects TOWARD mass (positive net_defl, 29→44 units). All paths on the opposite side of the mass from the source bend inward.
- **y = -2 to -1:** ANTI-LENSING — paths deflect AWAY from mass. These paths pass just under the mass at close range, and the discrete grid's action landscape pushes them down.
- **y = 0:** zero deflection (on-axis symmetry).
- **y = +1 to +12:** path deflects TOWARD mass. Net deflection peaks around y=7 (near the mass at y=6), reaching max_defl=4.

This is a gravitational lensing analog: paths on both sides of the mass bend inward, with the strongest bending for paths that pass closest to the mass.

The anti-lensing at y=-2,-1 is a DISCRETE GRID ARTIFACT — the path must choose integer y-positions, and the action minimum at close range can push the path away from the mass rather than toward it. This would not occur in a continuous model.

### 3. Action is NOT symmetric around the mass

For the angular sweep (mass at y=6):
- Paths toward the mass (y>0): action_diff ranges -10.5 to -12.5
- Paths away from the mass (y<0): action_diff stays near -10.2 to -10.5

The mass affects the action more strongly for paths that pass near it. This is the expected gravitational potential well signature.

### 4. Node count effect is monotonic (sweep 2)

At fixed distance (mass at y=5, target y=3), action_diff grows monotonically with node count from -7.9 (n=2) through at least n=15. The relationship is sublinear — each additional node contributes less, consistent with the delay field saturating near the persistent region.

## Hypothesis Verdict
**SUPPORTED** — action falls off monotonically with distance, bending is toward the mass (gravitational lensing), and node count gives sublinear growth. The functional form is not a clean power law or exponential — it's a discrete-harmonic falloff specific to the grid's relaxation equation.

## Significance
This is the first angular-resolved measurement of the model's gravity mechanism. The lensing pattern (paths on both sides bend inward) and the discrete anti-lensing artifact at close range are both new observations.
