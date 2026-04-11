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

---

## Follow-up: packet-local antisymmetrized force-balance probe

**Date:** 2026-04-11  
**Script:** `frontier_wilson_both_masses_local_balance.py`

The natural next question was whether the remaining force-balance failure was
still a **whole-packet centroid artifact**. To test that directly, I kept the
same open Wilson surface and replaced the global centroid readout with
**packet-local centroids** measured in fixed Gaussian windows anchored to the
initial packet centers.

Surface:

- open 3D Wilson lattice
- `side = 20`
- `d = 8`
- `G = 5`
- `mu^2 = 0.001`
- packet width `sigma = 1.0`
- local-window width `window_sigma = 1.5`
- `N_steps = 15`
- same mass grid `M_A, M_B in {0.5, 1.0, 1.5, 2.0}`

Local observables:

- `x_A^loc`, `x_B^loc` = packet-local `x` centroids in fixed Gaussian windows
- `a_A^loc = +(x_A^loc,shared - x_A^loc,self)''`   inward positive
- `a_B^loc = -(x_B^loc,shared - x_B^loc,self)''`   inward positive
- `F_A^loc = M_A * a_A^loc`
- `F_B^loc = M_B * a_B^loc`

### Exact output

```
M_A   M_B |     a_A^loc     a_B^loc       a_sym |     F_A^loc     F_B^loc     relΔF
-------------------------------------------------------------------------------------
0.5   0.5 | +2.695361e-02 +2.288492e-02 +2.491926e-02 | +1.347681e-02 +1.144246e-02    8.16%
0.5   1.0 | +5.328165e-02 +1.749512e-02 +3.538838e-02 | +2.664083e-02 +1.749512e-02   20.72%
0.5   1.5 | +7.906763e-02 +1.313349e-02 +4.610056e-02 | +3.953381e-02 +1.970023e-02   33.48%
0.5   2.0 | +1.043679e-01 +7.651463e-03 +5.600969e-02 | +5.218396e-02 +1.530293e-02   54.65%
1.0   0.5 | +2.642239e-02 +4.634807e-02 +3.638523e-02 | +2.642239e-02 +2.317403e-02    6.55%
1.0   1.0 | +5.253931e-02 +3.537605e-02 +4.395768e-02 | +5.253931e-02 +3.537605e-02   19.52%
1.0   1.5 | +7.842673e-02 +2.606695e-02 +5.224684e-02 | +7.842673e-02 +3.910042e-02   33.46%
1.0   2.0 | +1.041381e-01 +1.450444e-02 +5.932126e-02 | +1.041381e-01 +2.900889e-02   56.43%
1.5   0.5 | +2.370239e-02 +7.024398e-02 +4.697318e-02 | +3.555358e-02 +3.512199e-02    0.61%
1.5   1.0 | +4.785434e-02 +5.353283e-02 +5.069358e-02 | +7.178151e-02 +5.353283e-02   14.56%
1.5   1.5 | +7.251310e-02 +3.872472e-02 +5.561891e-02 | +1.087697e-01 +5.808707e-02   30.37%
1.5   2.0 | +9.772259e-02 +2.051158e-02 +5.911708e-02 | +1.465839e-01 +4.102315e-02   56.27%
2.0   0.5 | +1.242658e-02 +9.444066e-02 +5.343362e-02 | +2.485316e-02 +4.722033e-02   31.03%
2.0   1.0 | +2.614387e-02 +7.186485e-02 +4.900436e-02 | +5.228774e-02 +7.186485e-02   15.77%
2.0   1.5 | +4.120603e-02 +5.104260e-02 +4.612431e-02 | +8.241206e-02 +7.656389e-02    3.68%
2.0   2.0 | +5.766435e-02 +2.564218e-02 +4.165327e-02 | +1.153287e-01 +5.128436e-02   38.44%
```

Grid runtime on this surface: `159.2s`.

Anchor slices:

- `a_A^loc` vs `M_B` at `M_A = 1.0`:
  - fit `a_A^loc = 5.180690e-02 * M_B + 6.230023e-04`
  - `R^2 = 0.999988`
- `a_B^loc` vs `M_A` at `M_B = 1.0`:
  - fit `a_B^loc = 3.625320e-02 * M_A - 7.492856e-04`
  - `R^2 = 0.999969`

Full-grid checks:

- `a_A^loc / M_B`: mean `4.509904e-02`, std `1.075406e-02`, `CV = 23.845%`
- `a_B^loc / M_A`: mean `3.050808e-02`, std `1.198348e-02`, `CV = 39.280%`
- local force-balance mismatch
  - mean `|F_A^loc - F_B^loc| / (|F_A^loc| + |F_B^loc|) = 26.482%`
  - max `= 56.426%`

### Comparison to the global acceleration proxy

The packet-local observable does improve the narrow target a bit:

- old mean relative mismatch: `28.113%`
- new mean relative mismatch: `26.482%`

So the force-balance failure is **not** just a trivial whole-packet-centroid
artifact.

What *does* remain true is:

- anchor-slice partner-mass linearity is still essentially exact
- the global full-grid drift problem survives localization
- equal-and-opposite force balance still does not close

### Updated honest verdict

This follow-up strengthens the diagnosis more than it strengthens the claim.

It shows that even after localizing the readout around each packet:

- partner-mass linearity on the anchor slices remains real
- full both-masses closure still fails on the same side-20 Wilson surface

So the lane remains frontier-only:

> real mutual attraction, real distance-law calibration, real anchor-slice
> partner-mass scaling, but no retained full `F ∝ M_A M_B / r^2` closure yet.
