# Quark Up-Amplitude Scalar-Comparison Bridge

**Date:** 2026-04-19
**Status:** bounded scalar-comparison bridge / no-go on the reduced quark
up-amplitude lane
**Primary runner:** `scripts/frontier_quark_up_amplitude_scalar_comparison_bridge.py`

## Safe statement

The current branch still does **not** derive the remaining reduced up-sector
amplitude `a_u` from the CKM scalar-comparison package alone.

But the scalar-comparison package is stronger than a single isolated
candidate. On the exact-support anchored surface it defines a natural bridge
family

```text
a_u = sin(delta_std) * (1 - rho_scalar * kappa)
```

with

```text
kappa in [sqrt(6/7), 1].
```

This note shows three things:

1. the exact scalar-comparison package constrains the anchored branch to a
   narrow amplitude band;
2. the continuous scalar bridge beats the current external refit baseline on
   one `kappa` window and beats the current external anchored baseline on a
   different `kappa` window;
3. those windows are disjoint, and the exact theorem stack already blocks
   promoting the scalar surface to the actual bright/tensor `1 -> 3`
   amplitude.

So the honest endpoint is a **tight bounded bridge plus a clean no-go**, not a
retained derivation.

## Exact scalar-comparison bridge data

The exact scalar-comparison CKM package supplies

- `sin(delta_std) = sqrt(5/6)`
- `rho_scalar = 1/sqrt(42)`
- `eta_scalar = sqrt(5/42)`
- `sqrt(rho_scalar^2 + eta_scalar^2) = 1/sqrt(7)`

and the exact scalar contraction factor

```text
kappa_cp = |V_ub|_scalar / |V_ub|_atlas
         = J_scalar / J_atlas
         = sqrt(6/7).
```

That already gives two exact bridge endpoints:

```text
lower: a_u = sin(delta_std) * (1 - rho_scalar)
      = 0.772011886721

upper: a_u = sin(delta_std) * (1 - rho_scalar * kappa_cp)
      = sin(delta_std) * (6/7)
      = 0.782460796436
```

The second identity is exact:

```text
1 - rho_scalar * kappa_cp = 6/7.
```

So the support-native ceiling can be rewritten entirely inside the
scalar-comparison CKM package.

## Theorem obstruction

The scalar package still does **not** become the theorem carrier.

[CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](./CKM_ATLAS_AXIOM_CLOSURE_NOTE.md) states
that the scalar democratic contraction `1/sqrt(7)` is an exact scalar support
comparison surface, but not the theorem value for the bright/tensor `1 -> 3`
amplitude.

[S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE.md](./S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE.md)
then sharpens the reason: the exact carrier columns keep unit leading bright
amplitude,

```text
[[1,0],[delta_A1,0]]
[[0,1],[0,delta_A1]]
```

with only lower-row `delta_A1` dressing.

That means any scalar-comparison route is structurally comparison-side or
bridge-side. It cannot by itself be promoted to the theorem value for the
bright/tensor slot.

## Exact bridge band on the anchored branch

Using the exact-support anchored reduced solve gives

```text
a_u(anchor) = 0.778161628656
```

and therefore

```text
kappa_anchor = 0.956341163278.
```

This anchored branch lies inside the exact scalar bridge band

```text
[0.772011886721, 0.782460796436]
```

with total width

```text
0.010448909715
```

which is only

```text
1.343%
```

of the anchored amplitude.

So the scalar-comparison package does not derive `a_u`, but it already
compresses the remaining scalar to a narrow interval.

## Continuous scalar bridge family

The runner then treats

```text
a_u(kappa) = sin(delta_std) * (1 - rho_scalar * kappa)
```

as a continuous bridge family on

```text
kappa in [sqrt(6/7), 1].
```

This is the cleanest non-arbitrary bridge allowed by the exact scalar package:

- `kappa = 1` gives the pure scalar-comparison endpoint;
- `kappa = sqrt(6/7)` gives the support-side ceiling rewritten in
  scalar-comparison language.

### Best refit bridge point

The best refit point is

```text
kappa_refit = 0.956351495950
a_u = 0.778160173206
```

with

- refit objective `0.052726636368`
- anchored score `0.851778972074%`

This is slightly better on the refit axis than the current external `7/9`
baseline.

### Best anchored bridge point

The best anchored point is

```text
kappa_anchor-best = 0.978801550649
a_u = 0.774997879998
```

with

- anchored score `0.716062228229%`
- refit objective `0.054274764615`

This is slightly better on the anchored axis than the current external
`sqrt(3/5)` baseline.

### Disjoint windows

The decisive negative result is the window structure:

- refit-better window:
  `kappa in [0.953432293478, 0.959066224231]`
- anchored-better window:
  `kappa in [0.978225881627, 0.981649866377]`

These windows are disjoint.

So the scalar-comparison bridge can beat the current best external baselines
**separately**, but not **simultaneously**.

That is the cleanest scalar-comparison no-go on this branch.

## Interpretation

This lane ends in a mixed but useful place:

- the exact scalar-comparison package does impose a real and narrow bridge band;
- the anchored reduced solve lands essentially on the refit-optimal scalar
  bridge, with
  `|kappa_anchor - kappa_refit| = 1.03 x 10^-5`;
- but the theorem obstruction remains active, and the scalar bridge still
  splits into incompatible refit-first and anchor-first windows.

So the scalar-comparison package now **tightly constrains** the anchored quark
branch, but it still does **not** derive a single theorem-grade up-amplitude
law.

## Validation

Run:

```bash
python3 scripts/frontier_quark_up_amplitude_scalar_comparison_bridge.py
```

Current expected result on this branch:

- `frontier_quark_up_amplitude_scalar_comparison_bridge.py`: `PASS=11 FAIL=0`
