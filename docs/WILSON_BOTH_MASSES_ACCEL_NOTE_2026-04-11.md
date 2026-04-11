# Wilson Both-Masses Acceleration Note

**Date:** 2026-04-11  
**Status:** exploratory but stronger than the older momentum-residual test  
**Script:** `frontier_wilson_both_masses_accel.py`

## Question

Can the open weak-screening Wilson lane support a genuine both-masses law once
the old shared-minus-self **momentum residual** is replaced by a cleaner
short-time observable?

The earlier runner, `frontier_newton_both_masses.py`, failed because the
integrated velocity residual was dominated by a common Wilson-gap slowdown once
both inertial masses varied.

## New Observable

This follow-up keeps the same architecture but switches to inward-positive early
accelerations on the clean side-20 open surface:

- open 3D Wilson lattice
- `side = 20`
- `G = 5`
- `mu^2 = 0.001`
- fixed separation `d = 8`
- mass grid `M_A, M_B in {0.5, 1.0, 1.5, 2.0}`

Each orbital is evolved in:

- `SHARED`: both densities source one common `Phi`
- `SELF_ONLY`: each orbital sees only its own `Phi`

Retained observables:

- `a_A^mut = +(a_A^shared - a_A^self)`  (inward positive)
- `a_B^mut = -(a_B^shared - a_B^self)`  (inward positive)
- `F_A = M_A * a_A^mut`
- `F_B = M_B * a_B^mut`

This is cleaner than the old momentum residual because it measures the mutual
channel before the common slowdown has integrated into a large velocity offset.

## Exact Output

```
M_A   M_B |     a_A^mut     a_B^mut     a_close |         F_A         F_B     relΔF
-------------------------------------------------------------------------------------
0.5   0.5 | +3.627029e-02 +2.811494e-02 +3.219261e-02 | +1.813514e-02 +1.405747e-02   12.67%
0.5   1.0 | +7.159914e-02 +2.139352e-02 +4.649633e-02 | +3.579957e-02 +2.139352e-02   25.19%
0.5   1.5 | +1.060821e-01 +1.574252e-02 +6.091233e-02 | +5.304107e-02 +2.361378e-02   38.39%
0.5   2.0 | +1.397772e-01 +1.008380e-02 +7.493048e-02 | +6.988859e-02 +2.016759e-02   55.21%
1.0   0.5 | +3.524908e-02 +5.703002e-02 +4.613955e-02 | +3.524908e-02 +2.851501e-02   10.56%
1.0   1.0 | +7.003766e-02 +4.337666e-02 +5.670716e-02 | +7.003766e-02 +4.337666e-02   23.51%
1.0   1.5 | +1.044619e-01 +3.146506e-02 +6.796349e-02 | +1.044619e-01 +4.719759e-02   37.76%
1.0   2.0 | +1.385871e-01 +1.949610e-02 +7.904162e-02 | +1.385871e-01 +3.899219e-02   56.08%
1.5   0.5 | +3.134267e-02 +8.655841e-02 +5.895054e-02 | +4.701400e-02 +4.327920e-02    4.14%
1.5   1.0 | +6.307994e-02 +6.580564e-02 +6.444279e-02 | +9.461991e-02 +6.580564e-02   17.96%
1.5   1.5 | +9.528623e-02 +4.706643e-02 +7.117633e-02 | +1.429293e-01 +7.059965e-02   33.87%
1.5   2.0 | +1.280175e-01 +2.816846e-02 +7.809299e-02 | +1.920263e-01 +5.633692e-02   54.63%
2.0   0.5 | +1.958396e-02 +1.165305e-01 +6.805724e-02 | +3.916791e-02 +5.826526e-02   19.60%
2.0   1.0 | +4.050598e-02 +8.854894e-02 +6.452746e-02 | +8.101196e-02 +8.854894e-02    4.44%
2.0   1.5 | +6.282604e-02 +6.245859e-02 +6.264231e-02 | +1.256521e-01 +9.368789e-02   14.57%
2.0   2.0 | +8.659848e-02 +3.605020e-02 +6.132434e-02 | +1.731970e-01 +7.210040e-02   41.21%
```

Grid time on this surface: `130.2s`.

## What Improved

The anchor mass slices are now extremely clean:

- `a_A^mut` vs `M_B` at `M_A = 1.0`: `R^2 = 0.999981`
- `a_B^mut` vs `M_A` at `M_B = 1.0`: `R^2 = 0.999942`

Exact fits:

- `a_A^mut = 6.888768e-02 * M_B + 9.743476e-04`
- `a_B^mut = 4.477905e-02 * M_A - 1.192624e-03`

So the acceleration observable fixes the worst weakness of the older
momentum-transfer runner: the partner-mass dependence on the anchor slices is
now effectively linear on this surface.

## What Still Fails

Two full-closure requirements still fail:

### 1. Full-grid normalization drift

- `a_A^mut / M_B`: mean `6.139848e-02`, std `1.206706e-02`, `CV = 19.654%`
- `a_B^mut / M_A`: mean `3.784776e-02`, std `1.419161e-02`, `CV = 37.497%`

That is too much drift to claim one clean global both-masses law across the
entire mass grid.

### 2. Equal-and-opposite force balance

Using the force proxy

- `F_A = M_A * a_A^mut`
- `F_B = M_B * a_B^mut`

the relative mismatch

`|F_A - F_B| / (|F_A| + |F_B|)`

has:

- mean `28.113%`
- max `56.085%`

So the force-balance side of the Newton closure still does not survive.

## Honest Interpretation

This follow-up materially strengthens the Wilson both-masses lane:

- the earlier failure was partly the observable
- the clean short-time acceleration read recovers near-perfect anchor-slice
  partner-mass linearity

But it still does **not** close a retained both-masses Newton law because:

- the normalized response drifts too much across the full grid
- the force-balance proxy is not stable enough

So the honest state is:

> On the clean side-20 open Wilson surface, early antisymmetrized inward
> accelerations are almost perfectly linear in the partner mass on the anchor
> slices, but full-grid both-masses closure still fails because the response is
> not globally separable and the force-balance proxy remains poor.

## Practical Consequence

The Wilson lane is now stronger in a narrow, useful way:

- distance-law calibration is real
- mutual attraction is real
- anchor-slice partner-mass scaling is real

But the retained statement is still **not** full `F ∝ M_A M_B / r^2`.

The next honest observable, if this lane is pushed further, should target the
force-balance failure specifically:

- weaker masses / weaker coupling to stay more perturbative
- a direct local momentum-flux or mid-plane current observable
- or a surface where the common slowdown mode is even smaller
