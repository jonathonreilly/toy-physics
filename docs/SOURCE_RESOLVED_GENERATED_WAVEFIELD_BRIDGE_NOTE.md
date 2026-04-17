# Source-Resolved Generated Wavefield Bridge

This probe tests whether the retained exact-lattice wavefield idea can be transferred onto the compact generated-family bridge, rather than only using static or causal smoothing.

## Setup

The harness evaluates the compact generated 3D DAG family in two forms:

- baseline connectivity
- retained k-nearest floor augmentation on next-layer edges

For each family it compares three field modes:

- static Green
- causal parent-averaged Green
- wavefield candidate

The wavefield candidate is intentionally minimal:

1. build the causal parent-averaged field
2. apply one same-layer transverse smoothing pass using local same-layer geometry

## Gates

The probe reports:

- exact zero-source reduction
- centroid sign counts
- weak-field mass-scaling exponent `F~M`
- detector effective support `N_eff`
- a wavefield-vs-static observable on the same family

## Result

The zero-source reduction is exact across all rows: `zero = 0.000e+00`.

The compact generated family remains mixed:

- baseline/static: `4/16` TOWARD, `F~M = 0.199`, `N_eff = 2.69`
- baseline/causal: `3/16` TOWARD, `F~M = -0.308`, `N_eff = 2.50`
- baseline/wavefield: `0/16` TOWARD, `F~M = 0.655`, `N_eff = 2.53`

The retained k-nearest floor support tweak is a real partial rescue, but not closure:

- tweak/static: `9/16` TOWARD, `F~M = -0.316`, `N_eff = 5.31`
- tweak/causal: `9/16` TOWARD, `F~M = 0.444`, `N_eff = 5.67`
- tweak/wavefield: `6/16` TOWARD, `F~M = 0.098`, `N_eff = 5.14`

The wavefield-vs-static observable is distinguishable, but it does not beat the static bridge on the aggregate centroid gain:

- baseline: `delta_gain = -1.585344e-01`, `N_eff_gain = -0.16`
- tweak: `delta_gain = -9.286995e-02`, `N_eff_gain = -0.18`

## Safe Read

The wavefield update is a real generated-family bridge observable, but it is not generated-family closure.

The safest claim is:

- the exact zero-source reduction survives
- the k-nearest floor rescue broadens support and can move the centroid sign back toward TOWARD
- the wavefield update is distinguishable from static/causal smoothing
- however, on this compact generated family, it remains a bridge result rather than a stable weak-field transfer

