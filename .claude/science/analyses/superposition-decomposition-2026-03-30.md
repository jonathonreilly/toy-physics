# Analysis: Superposition Decomposition

## Date
2026-03-30

## Key Finding: The superposition failure has TWO sources

### 1. Field nonlinearity (~3.7% contribution)
field(A+B) ≠ field(A) + field(B), with max deviation 0.028 (3.7% of field). The (1-support) × avg(neighbors) relaxation rule is nonlinear when two masses' support regions interact with the diffused field. This is a small effect concentrated near the mass sources.

### 2. Action nonlinearity (~48% contribution — the dominant source)
The action formula `delay - sqrt(delay² - link_length²)` where `delay = link_length × (1 + field)` is NONLINEAR in the field value. Doubling the field does NOT double the action. This is the spent-delay (proper-time-deficit) formula — it's a relativistic-looking expression where action is the difference between coordinate time and proper time.

For small fields (field << 1): action ≈ link_length × field²/2 (QUADRATIC in field). So doubling the field QUADRUPLES the action, not doubles it. This explains why ad_both ≈ ad_sum/1.5 rather than ad_sum — the combined field is smaller than the sum of fields (due to field nonlinearity), and the action function amplifies this difference.

### Decomposition

| Component | Contribution to 51.6% failure |
|-----------|------------------------------|
| Field nonlinearity (relaxation) | ~3.7% |
| Action nonlinearity (spent delay) | ~48% |
| Path optimization (shape change) | ~0% (path is straight by symmetry for y=0 target) |

### The action formula's nonlinearity is STRUCTURAL

The spent-delay action `S = delay - sqrt(delay² - L²)` expands as:
- S ≈ L²/(2×delay) for delay >> L
- S ≈ delay - L×sqrt(1 - (L/delay)²) in general

This is the same formula as `dt - sqrt(dt² - dx²)` — the proper-time deficit. It's inherently nonlinear in the delay (which is proportional to 1 + field). This nonlinearity is not a bug — it's the model's version of the nonlinear coupling between geometry and matter in general relativity.

## Significance
The superposition failure is predominantly (~48 out of 51.6 percentage points) from the action formula's nonlinearity, not from field interactions or path changes. The action is the model's "proper time deficit" — a relativistic-looking quantity that is inherently nonlinear in the gravitational potential. This is analogous to how GR's Einstein equations are nonlinear even though the linearized (weak-field) approximation superposes.
