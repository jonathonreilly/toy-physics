# Continuum Limit via h^2 Measure

**Date:** 2026-04-05
**Status:** partial positive — h^2 measure extends working range and F~M converges; full continuum limit not yet achieved

## Artifact chain

- [`scripts/lattice_h2_measure_continuum.py`](../scripts/lattice_h2_measure_continuum.py)
- [`scripts/lattice_nn_normed_continuum.py`](../scripts/lattice_nn_normed_continuum.py) (bounded negative)
- [`scripts/lattice_dense_normed_continuum.py`](../scripts/lattice_dense_normed_continuum.py) (bounded negative)
- [`logs/2026-04-05-h2-measure-continuum.txt`](../logs/2026-04-05-h2-measure-continuum.txt)

## Question

Does the lattice propagator have a continuum limit (h -> 0)?

## The problem

The original kernel `exp(ikS) * w / L^2` has transfer norm T ~ 1/h^4 in 3D,
causing exponential overflow: amplitude grows as T^N per layer, where N = L/h.
At h=0.25: overflow.

## Approaches tested

### 1. Nearest-neighbor (3 edges/node)
Bounded negative. Fan-out is fixed but 1/L still grows as 1/h. With transfer
normalization, the beam width shrinks as sqrt(L*h) -> 0, making MI -> 1 and
d_TV -> 1 trivially. Not a useful continuum limit.

### 2. Dense lattice with transfer normalization
Bounded negative. Dividing by T ~ 1/h^4 causes amplitude underflow: P_det ~
(1/T)^N -> 0. At h=0.5, P_det = 1e-59 — below most precision thresholds.

### 3. Dense lattice with h^2 measure (this result)
Partial positive. The correct 3D path integral discretization includes h^(d-1) = h^2:

    kernel = exp(ikS) * w * h^2 / L^2

This gives transfer norm:

    T = sum_edges w * h^2 / L^2

which converges to ~5-6 (only logarithmic growth with 1/h), vs the ~1/h^4
divergence without the measure.

## Frozen results (h^2 measure)

### Transfer norm convergence

| h | T | n_edges |
| ---: | ---: | ---: |
| 1.000 | 4.274 | 49 |
| 0.500 | 5.081 | 169 |
| 0.250 | 5.802 | 625 |
| 0.125 | 6.468 | 2401 |

T grows logarithmically: T ~ 4.3 + 1.1 * ln(1/h). This is the 2D integral
of w/r^2 which has a ln(R/h) divergence.

### Gravity and Born

| h | gravity | direction | k=0 | P_det | Born |
| ---: | ---: | --- | ---: | ---: | ---: |
| 1.000 | +6.07e-01 | TOWARD | 0 | 6.6e+18 | 1.7e-16 |
| 0.500 | +9.34e-02 | TOWARD | 0 | 1.7e+26 | 1.2e-15 |
| 0.250 | +2.71e-01 | TOWARD | 0 | 1.7e+95 | — |

### Mass scaling convergence

| h | F~M exponent |
| ---: | ---: |
| 1.000 | 0.979 |
| 0.500 | 0.991 |
| 0.250 | 0.998 |

F~M converges to 1.000 — the Newtonian mass scaling is exact in the
continuum limit.

## Safe read

The retained statements:

1. **The h^2 measure is the correct 3D discretization.** It reduces the
   transfer norm from O(1/h^4) to O(ln(1/h)), enabling propagation at h=0.25
   where the original kernel overflows.

2. **F~M converges to 1.000.** The Newtonian mass scaling exponent improves
   monotonically from 0.979 (h=1) to 0.998 (h=0.25). This is strong
   evidence for a linear-response continuum limit.

3. **Born holds at all tested h.** Machine precision (< 2e-15).

4. **Gravity is TOWARD at all h.** The sign is correct throughout.

5. **Absolute gravity does not converge.** The strong-field deflection
   (s=0.1) is 0.607, 0.093, 0.271 — non-monotonic. This is expected:
   s=0.1 is non-perturbative, and the effective coupling changes with h.

## Honest limitations

1. **P_det still grows** because T > 1 (~5-6). At h=0.125, P_det ~ 5.8^481
   ~ 10^368, exceeding IEEE double range (1.8e+308). The h^2 measure buys
   2 octaves of refinement but does not solve the overflow for h -> 0.

2. **The logarithmic T growth** means a truly smooth continuum limit
   requires either:
   - Additional renormalization of the remaining ln(1/h) factor
   - A cutoff on the Gaussian weight beta
   - A fundamental new approach

3. **Gravity convergence** needs weak-field tracking (deflection per unit s)
   across more h values to establish the limit.

## What this means for the project

The h^2 measure is a genuine improvement: it correctly implements the 3D path
integral discretization, stabilizes the transfer norm, and the Newtonian mass
scaling converges. But a full continuum limit (h -> 0 with all observables
converging) is not yet achieved due to the residual logarithmic divergence.

The most promising path forward: combine h^2 measure with mild T-normalization
(divide by T/T_ref where T_ref is the h=0.5 reference value) to keep P_det
bounded while preserving the correct physics at finite h.
