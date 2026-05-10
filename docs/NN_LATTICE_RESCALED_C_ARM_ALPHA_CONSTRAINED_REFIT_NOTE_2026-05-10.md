# Rescaled NN Lattice C_arm Alpha-Constrained Refit Note

**Date:** 2026-05-10
**Claim type:** bounded_theorem (alpha-constrained residual-closure diagnostic
  for the apparent 8.3 % gap between the upstream numerical fit and
  coherent-saddle support note; sharpens the scoped harness comparison
  without promoting either upstream surface)
**Status authority:** source-note proposal only; audit verdict and
  effective status are set by the independent audit lane.
**Primary runner:** [`scripts/lattice_nn_rescaled_C_arm_alpha_constrained_refit.py`](../scripts/lattice_nn_rescaled_C_arm_alpha_constrained_refit.py)
**Cached log:** [`logs/runner-cache/lattice_nn_rescaled_C_arm_alpha_constrained_refit.txt`](../logs/runner-cache/lattice_nn_rescaled_C_arm_alpha_constrained_refit.txt)
**Trigger:** the
  [`NN_LATTICE_RESCALED_CONTINUUM_IDENTIFICATION_NOTE_2026-05-10.md`](NN_LATTICE_RESCALED_CONTINUUM_IDENTIFICATION_NOTE_2026-05-10.md)
  numerical fit (`C_arm = 2.7107`, `alpha = 0.5256`) and the
  [`NN_LATTICE_RESCALED_C_ARM_DERIVATION_NOTE_2026-05-10.md`](NN_LATTICE_RESCALED_C_ARM_DERIVATION_NOTE_2026-05-10.md)
  coherent-saddle support constant (`C_arm_analytic = 2.4855`), whose
  apparent residual is
  `(C_arm_analytic - C_arm_unconstrained) / C_arm_unconstrained = -8.31 %`.

## TL;DR

Within this bounded harness comparison, the 8.3 % residual is removed by the
alpha-constrained extraction and is consistent with a finite-window
fit-protocol artifact rather than a leading-order disagreement. Both upstream
source notes are sharpened, neither is overturned:

- the coherent-saddle constant `C_arm_analytic = 2.4855` is recovered
  pointwise at the finest measured spacing `h = 0.015625` with residual
  `+0.27 %`,
- the numerical fit `C_arm_unconstrained = 2.7107` is an unconstrained
  2-parameter regression that lets `alpha` drift to `0.5256` on the checked
  finite-h window, which absorbs the finite-h cosine phase factor in the
  saddle and biases the prefactor upward by the observed 8 %.

When imposing the upstream geodesic constraint `alpha = 1/2` as the scoped
comparison protocol, the per-h estimator
`C_arm(h) := sigma_arm(h) / sqrt(h)` converges monotonically to the
analytic value:

| `h` | `sigma_arm` | `C_arm(h) = sigma_arm/sqrt(h)` | residual vs `2.4855` |
|---:|---:|---:|---:|
| 0.250000 | 1.3147 | 2.6294 | +5.788 % |
| 0.125000 | 0.8984 | 2.5412 | +2.240 % |
| 0.062500 | 0.6282 | 2.5128 | +1.097 % |
| 0.031250 | 0.4416 | **2.4981** | **+0.504 %** |
| 0.015625 | 0.3115 | **2.4922** | **+0.268 %** |

The residual shrinks with each factor-of-two refinement (5.79, 2.24,
1.10, 0.50, 0.27 %), consistent with a sub-leading `O(h)` correction
to the leading bounded saddle model, not a missing leading-order mechanism
inside this scoped harness.

## Why the unconstrained fit overshot

The coherent-saddle support note retains a phase factor:

```text
C_arm^2(h) = L_2 / [ ( sqrt(2)/c ) * cos( k h (sqrt(2)-1) ) + 2 ].
```

For `h > 0` the cosine is `< 1`, the denominator shrinks, and
`C_arm(h)` rises slightly above the `h -> 0` asymptote `2.4855`. A
log-linear fit of `sigma_arm = C * h^alpha` in this finite-h window
sees `sigma_arm(h)` rising slightly faster than `sqrt(h)` and pays
for it with `alpha = 0.5256 > 1/2`. The two-parameter optimum then
forces `C_unconstrained > C_analytic` to balance: at any `h` in the
fit window,

```text
C_unconstrained * h^alpha_unconstrained  ~  sigma_arm(h)
C_unconstrained                          ~  sigma_arm(h) / h^alpha_unconstrained
```

which puts `C_unconstrained` at the geometric extrapolation to
`h = 1`, not at the geodesic prefactor of `sqrt(h)`. The 0.026
overshoot in `alpha` produces the 8 % overshoot in `C` because the
fit window spans a factor of 8 in `h` and `8^0.026 ~ 1.055` while
the prefactor compensates further to fit the actual data. Numerically:

```text
2.7107 / 2.4855 = 1.0906   (8.06 % apparent gap on log-axis)
```

Imposing `alpha = 1/2` removes both biases at once.

## What the new finer point adds

A new measurement at `h = 0.015625` (one factor of 2 beyond the upstream
continuum note's finest grid point) using the same `measure_arm_distribution(...)`
function from `scripts/lattice_nn_rescaled_continuum_identification.py`
gives

```text
n_nodes      = 6,558,721           (factor 2.41 in nodes vs h=0.03125)
sigma_a      = 0.3115
sigma_b      = 0.3115              (perfect symmetry, no Born violation)
mu_a         = +3.0239
mu_b         = -3.0239             (centroid drift = 0.024, slit at +/-3)
MI_obs       = 1.000000
d_TV_obs     = 1.000000
Born         = 1.43e-15
elapsed      = 73.5 s              (single arm-pair pass, no MI/dTV scan)
```

so `C_arm_constrained_extrap = 0.3115 / sqrt(0.015625) = 2.4922` and
the residual against the analytic `2.4855` is `+0.268 %`. Combined
with the existing `+0.504 %` at `h = 0.03125`, the analytic value is
recovered well inside measurement noise, and the residual continues
to halve under one more factor of 2 in `h`, consistent with a
sub-leading `O(h)` correction.

The runner does NOT extend MI / d_TV / Born identification to the
new point: the cached log confirms `MI = d_TV = 1.0` and
`Born = 1.43e-15` at `h = 0.015625`, which match the saturation
values established by the upstream cache to machine precision; no
new continuum identification is being claimed at this point. The
companion identification cache
`logs/runner-cache/lattice_nn_rescaled_continuum_identification.txt`
is intentionally NOT modified by this PR — extending it would require
re-running the full upstream runner with a new `H_VALUES` list and
producing a single coherent log.

## Comparison table

| Source | Method | `C_arm` | residual vs analytic |
|---|---|---:|---:|
| C_arm support note | Closed-form coherent saddle, `h -> 0` | 2.4855 | 0 (reference) |
| Continuum diagnostic note | Unconstrained log-linear fit, h <= 0.25 | 2.7107 | +9.06 % |
| **This PR** | **Constrained estimator at h = 0.03125** | **2.4981** | **+0.504 %** |
| **This PR** | **Constrained estimator at h = 0.015625** | **2.4922** | **+0.268 %** |

## Outcome class

This is a bounded residual-closure diagnostic: the residual at the new
finer point is `0.27 %`, well inside `1 %`. The residual at `h = 0.03125`
is `0.504 %`, also inside `1 %`. Under the scoped alpha-constrained
comparison, the apparent 8.3 % gap is explained by the finite-window
fit protocol, and the analytic and numerical constants agree pointwise at
the finest measured `h`.

## Imported authorities

| Authority | Role |
|---|---|
| [`docs/NN_LATTICE_RESCALED_CONTINUUM_IDENTIFICATION_NOTE_2026-05-10.md`](NN_LATTICE_RESCALED_CONTINUUM_IDENTIFICATION_NOTE_2026-05-10.md) | provides the per-h `sigma_arm` data and the `alpha = 1/2` geodesic-continuum identification used as the constraint here |
| [`docs/NN_LATTICE_RESCALED_C_ARM_DERIVATION_NOTE_2026-05-10.md`](NN_LATTICE_RESCALED_C_ARM_DERIVATION_NOTE_2026-05-10.md) | provides the closed-form `C_arm_analytic = 2.4855` and the cosine phase factor that explains the residual sign |
| [`scripts/lattice_nn_rescaled_continuum_identification.py`](../scripts/lattice_nn_rescaled_continuum_identification.py) | supplies the `measure_arm_distribution(...)` function used unchanged for the new `h = 0.015625` point |

This note does not introduce a new axiom, does not modify any
retained theorem family, does not promote any status row, and does
not supersede the upstream source notes. It sharpens both: the upstream
geodesic-scaling diagnostic remains the source of the `alpha = 1/2`
comparison protocol, and the coherent-saddle support note's analytic
prefactor is now recovered numerically pointwise. The
8.3 % residual at the strict saddle is no longer left unexplained:
it is the fit-protocol bias from letting `alpha` float to absorb
sub-leading phase corrections.

## Reproducibility

```bash
python3 scripts/lattice_nn_rescaled_C_arm_alpha_constrained_refit.py
```

The runner takes ~75 s (dominated by the single `h = 0.015625`
arm-distribution measurement; the rest is closed-form arithmetic on
the upstream hardcoded cache values). It exits 0 if the residual at the
finest measured `h` is `<= 2 %`. Set `MEASURE_FINER_H = False` near
the top of the runner to skip the new measurement and run in
sub-second time using the verified fallback value.

## Bounded scope

This note inherits all bounded scope from the two upstream notes:

- harness parameters frozen at `BETA = 0.8`, `K_PHYS = 5.0`,
  `L_total = 40`, `FANOUT = 3`, slit at layer `nl // 3`;
- field-free (no gravity / scattering subblock); per-arm width only;
- the cosine phase factor is the leading sub-`sqrt(h)` correction;
  higher-order saddle terms (the `O((q h)^4)` term dropped in
  the coherent-saddle support note) are not separately quantified here. The observed
  `O(h)` halving of the residual is consistent with that order being
  sub-leading at the measured grid.

## Status

This source note is a bounded residual-closure proposal layered on the two
upstream bounded source notes. The audit lane sets the effective status
after independent review of the runner, the constrained-estimator
formula, and the new `h = 0.015625` measurement.
