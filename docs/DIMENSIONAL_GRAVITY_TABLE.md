# Dimensional Gravity Table

**Status:** bounded - bounded or caveated result note
**Date:** 2026-04-04
**Action:** Valley-linear S = L(1-f)
**Kernel:** 1/L^(d-1) with h^(d-1) measure

## Complete results

| d | Kernel | F∝M | Distance tail | Born | Decoh | TOWARD |
|---|--------|-----|---------------|------|-------|--------|
| 2 | 1/L | **1.00** | varies (2D = log) | <6e-16 | →50% | 7/7 at h≤0.5 |
| 3 | 1/L² | **1.00** | **b^(-0.93)** | <4e-15 | →50% | 8/8 at h≤0.5 |
| 4 | 1/L³ | **0.99-1.00** | bounded, width-limited (`W=7:-0.96`, `W=8:-0.54` companions) | 1.5e-15 .. 4.4e-15 | TBD | `3/3 .. 6/6` at h=0.5 |

## Newtonian predictions

| d | Newtonian deflection | Model (valley-linear) | Match? |
|---|---------------------|----------------------|--------|
| 2 | ln(b) | varies with h | consistent |
| 3 | 1/b | b^(-0.93) | **yes (~7% off)** |
| 4 | 1/b² | supportive but width-limited | needs wider lattice |

## Key properties

**F∝M = 1.00 is universal** across all dimensions, all h values,
all parameter variations. This is the strongest retained result:
linear mass scaling from the linear-in-f valley action.

**Decoherence is action-independent.** Valley-linear and spent-delay
give identical d_TV, MI, CL purity at all h. Decoherence depends on
geometry, not the action formula.

**Born holds at machine precision** across all dimensions and kernels.
This is a mathematical property of the linear propagator.

## Spent-delay comparison

| Property | Spent-delay | Valley-linear |
|----------|------------|---------------|
| F∝M | 0.50 (√M) | **1.00 (linear)** |
| 3D distance | b^(-0.52) | **b^(-0.93)** |
| Decoherence | identical | identical |
| Born | identical | identical |
| Gravity sign | identical | identical |

The ONLY difference is the mass/distance scaling. Everything else
is the same because decoherence and Born don't depend on the action.

## Update: Dimensional field profile (2026-04-04)

The field profile must also scale with dimension:
  f = s / r^(d-2) where d = number of spatial dimensions

| d | f(r) | Newtonian deflection | Measured tail |
|---|------|---------------------|---------------|
| 3 | s/r | 1/b | b^(-0.93) |
| 4 | s/r² | 1/b² | b^(-0.29) (early, W=7) |

The 4D tail is still at an early stage. The current frozen width note keeps
`W = 5..7`, and a heavier raw `W = 8` companion strengthens the support but
does not yet close the asymptotic law.

The complete dimensional prescription:
  Kernel: 1/L^(d-1)
  Field: s/r^(d-2)
  Action: S = L(1-f)
  Measure: h^(d-1)

All four ingredients scale with dimension d.

## 4D distance law frozen result (2026-04-04)

4D W=7, L=15, h=0.5, field f=s/r^2, valley-linear + 1/L^3:

| z | deflection | direction |
|---|-----------|-----------|
| 2 | +0.0000424 | TOWARD |
| 3 | +0.0000708 | TOWARD |
| 4 | +0.0000762 | TOWARD (peak) |
| 5 | +0.0000740 | TOWARD |
| 6 | +0.0000674 | TOWARD |

Tail from peak (z>=4): b^(-0.29), R²=0.884, 3 points
Far tail (z>=5): b^(-0.51), 2 points

This is at the SAME early stage as 3D when it showed -0.35
(which later improved to -1.07 at W=12). The 4D tail needs
W>=10 (~3M nodes in 4D) for a definitive measurement.

The honest read: 4D gravity is TOWARD with the correct field
profile and near-Newtonian mass scaling (F∝M=0.99), but the
distance exponent is unresolved due to lattice width limits.

Heavier same-family raw companion:

- `W = 8`, `L = 15`, `h = 0.5`
- Born: `4.43e-15`
- `F∝M = 1.00`
- `6/6` TOWARD on `z = 2..7`
- early tail from `z >= 4`: `b^(-0.54)`

That row is supportive, but still width-limited.
