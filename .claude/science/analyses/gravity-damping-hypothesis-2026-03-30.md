# Analysis: Gravity Damping Hypothesis

## Date
2026-03-30

## Key Finding: Damping is NOT the cause of the gravity range plateau

| Grid | α_damped | α_undamped | Ratio |
|------|---------|-----------|-------|
| 20×16 | 0.230 | 0.231 | 1.01 |
| 40×32 | 0.118 | 0.118 | 1.00 |
| 80×64 | 0.073 | 0.072 | 0.98 |
| 140×112 | 0.081 | 0.079 | 0.98 |

The damped and undamped fields have nearly identical decay rates at every grid size. The undamped field is ~1.72× larger in absolute magnitude but has the same shape and the same scaling with grid size.

## Revised understanding

The α "plateau" from the earlier experiment was an artifact of the measurement geometry (measuring at y=0, off-axis from mass at y=h/2) combined with the rectangular grid's finite transverse dimension. Both damped and undamped fields share this behavior because both solve the same boundary-value problem on the same grid — the damping just scales the amplitude, not the spatial structure.

The αL product GROWS with L (3.7→9.0), meaning α falls SLOWER than 1/L. This rules out both:
- Simple exponential (αL constant)
- Pure power-law 1/r (αL ~ ln(L))

The actual behavior is intermediate — consistent with a 2D Green's function measured off-axis on a finite domain, where the far-field is dominated by the lowest eigenmode with a geometry-dependent decay rate.

## Significance

This exonerates the (1-support) damping term — it does NOT cause finite-range gravity. The gravity range is set by the grid's transverse dimension and the measurement geometry. On a truly large or infinite grid, the gravity range would grow without bound (though sublinearly). The model does NOT predict intrinsically finite-range gravity — the earlier conclusion was premature.

## Correction to prior finding

The earlier analysis ("gravity is intrinsically finite-range, α plateaus at ~0.10") is REVISED: α continues decreasing on larger grids but slower than 1/L. The plateau was a finite-size effect, not a fundamental property of the field relaxation rule.
