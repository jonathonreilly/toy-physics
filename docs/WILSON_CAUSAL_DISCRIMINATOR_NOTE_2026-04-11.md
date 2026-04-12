# Wilson Causal Discriminator Note

**Date:** 2026-04-11  
**Status:** held on the review branch; not promoted to `main`  
**Script:** `scripts/frontier_wilson_causal_discriminator.py`

## Question

Does a genuinely causal source-refresh intervention separate the open-Wilson
mutual channel from a purely adiabatic explanation on the same open 3D Wilson
surface?

This probe is intentionally different from the already-failed
`SHARED`/`SELF_ONLY`/`FROZEN_SOURCE` comparison. Instead of freezing the field,
it delays source refresh by one or two steps:

- `SHARED_NOW`: current density sources the field each step
- `LAG1`: source density is one step old
- `LAG2`: source density is two steps old

The discriminator is the early-time mutual acceleration of the packet
separation on the same open surface used by the Wilson side lane.

## Surface

- open 3D Wilson lattice
- `side = 20`
- `G = 5`
- `mu^2 = 0.001`
- `mass = 0.30`
- `sigma = 1.0`
- `dt = 0.08`
- `N_STEPS = 15`
- `separation = 8`
- `5` phase-jitter repeats

## Results

Per-seed early-time mutual acceleration means:

| seed | SHARED_NOW | LAG1 | LAG2 |
| --- | --- | --- | --- |
| 0 | -5.786847e-02 | -6.080209e-02 | -6.269494e-02 |
| 1 | -4.958371e-02 | -5.524903e-02 | -5.864580e-02 |
| 2 | -4.823018e-02 | -5.363451e-02 | -5.682465e-02 |
| 3 | -6.238052e-02 | -6.445891e-02 | -6.632449e-02 |
| 4 | -6.627674e-02 | -6.500916e-02 | -6.532786e-02 |

Aggregate:

- `SHARED_NOW`: mean `-5.686792e-02`, std `7.036843e-03`
- `LAG1`: mean `-5.983074e-02`, std `4.659719e-03`
- `LAG2`: mean `-6.196355e-02`, std `3.695593e-03`
- `LAG1 - SHARED_NOW`: mean `-2.962818e-03`, std `2.527597e-03`
- `LAG2 - SHARED_NOW`: mean `-5.095626e-03`, std `3.630688e-03`
- relative lag1 gap: `5.21%`
- relative lag2 gap: `8.96%`

## Verdict

The lagged source refresh does **not** cleanly separate the mutual channel on
this surface.

The lagged modes stay attractive, and the gap relative to `SHARED_NOW` is small
enough that the response looks adiabatic rather than causally discriminating.
That is a cleaner reason to hold the Wilson side lane than the older
frozen-source-only narrative.

## Retainable Reading

Retain as bounded Wilson-side evidence only:

- robust mutual attraction on the open surface
- a small but nonzero lag sensitivity
- no clean causal proof on this surface

Do not promote to `main`:

- causal-discriminator closure
- full Newton closure
- action-reaction closure

## Next Credible Step

If this lane is reopened, the next observable should be a stronger
intervention-style readout on the same surface, not another source-lag sweep:

- local momentum flux across the mid-plane
- packet-specific impulse after source ablation
- or a similarly direct causal-masking observable

