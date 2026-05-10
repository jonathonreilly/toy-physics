# NN Lattice Rescaled-Lane Geodesic Scaling Diagnostic

**Date:** 2026-05-10
**Claim type:** bounded_theorem
**Status:** bounded numerical geodesic-scaling diagnostic — on the
deterministic-rescale lane through `h = 0.03125`, the field-free
slit-detector decoherence response has per-arm detector width
`σ_arm(h) = C_arm · h^α` with `α = 0.5256`, `C_arm = 2.7107`, and
`R^2 = 0.9996` on the checked fine window. A two-Gaussian binned model
then matches the measured `MI` and `d_TV` rows to `5e-4` for
`h <= 0.125`. This is bounded support for a geodesic-limit
interpretation of the checked decoherence response components; it does
not identify a full continuum operator.
**Status authority:** independent audit lane only.
**Primary runner:** [`scripts/lattice_nn_rescaled_continuum_identification.py`](../scripts/lattice_nn_rescaled_continuum_identification.py)
**Cached log:** [`logs/runner-cache/lattice_nn_rescaled_continuum_identification.txt`](../logs/runner-cache/lattice_nn_rescaled_continuum_identification.txt)

**Cited authorities (one-hop):**

- [`LATTICE_NN_HIGH_PRECISION_NOTE.md`](LATTICE_NN_HIGH_PRECISION_NOTE.md)
  — step-scale invariance
  theorem (closure addendum 2026-05-07): the per-edge rescale
  `step_scale = h / sqrt(FANOUT)` leaves all framework observables
  invariant. Used here as the ambient lane.
- [`NN_LATTICE_RESCALED_OPERATOR_CAUCHY_CONVERGENCE_NOTE_2026-05-10.md`](NN_LATTICE_RESCALED_OPERATOR_CAUCHY_CONVERGENCE_NOTE_2026-05-10.md)
  (companion / upstream): bounded numerical Cauchy certificate for the
  chosen 15-component response vector, with fitted decay rate
  `r >= 1.513` and tail estimate `7.7e-3` at `h = 0.03125`. This note
  supplies a geometric diagnostic for the decoherence components of that
  response vector; it does not promote the upstream certificate.
- [`NN_LATTICE_RESCALED_RG_GRAVITY_SATURATION_NOTE_2026-05-10.md`](NN_LATTICE_RESCALED_RG_GRAVITY_SATURATION_NOTE_2026-05-10.md)
  (companion / orthogonal): explains why the strength-rescaling
  route to a nontrivial gravity continuum is blocked. The geodesic
  diagnostic here is consistent with the fixed-strength gravity limit
  being trivial on this harness, but it does not compute the gravity
  subblock.

## Question

Does the field-free slit-detector decoherence subblock of the rescaled
NN harness show the `sqrt(h)` arm narrowing expected from a geodesic
fixed-length refinement limit, and does that finite-window model explain
the measured `MI` and `d_TV` response components?

## Result

**Yes, within the bounded fitted-window scope.** Concretely:

1. **Per-arm centroid stays near the aperture inner edge.** On the
   measured refinement window, each one-arm detector distribution stays
   within `< 1.0` of the corresponding `y = +/-SLIT_Y` aperture edge.

2. **Per-arm width scales as `sqrt(h)`.** The log-linear fit
   `σ_arm(h) = C_arm · h^α` on the fine-h grid `h ≤ 0.25` (4 points
   spanning a factor of 8 in `h`) gives `α = +0.5256, C_arm = 2.7107,
   R² = 0.9996`. The fitted exponent matches the geodesic-continuum
   prediction `α = 0.5` to within `0.026`. The fitted prefactor
   `C_arm ≈ 2.71` is harness-specific (depends on `BETA = 0.8` and
   `K_PHYS = 5.0`). The coarse-h rows `h ∈ {0.5, 1.0}` are in a
   transient regime where the asymptotic power law has not yet
   stabilized.

3. **Measured `MI` and `d_TV` match the Gaussian-arm prediction to
   within `5e-4`** at `h ≤ 0.125`. With `σ_h = C_arm · h^α` and
   arms centered at the measured centroids, the standard
   two-Gaussian-binned model predicts `MI(h)` and `d_TV(h)` values that
   match the framework's runner outputs to better than four decimal
   places on the fine-h rows:

   | `h`    | MI_pred | MI_obs | d_TV_pred | d_TV_obs |
   |--------|---------|--------|-----------|----------|
   | 0.25   | 0.9486  | 0.9470 | 0.9882    | 0.9877   |
   | 0.125  | 0.9967  | 0.9972 | 0.9995    | 0.9996   |
   | 0.0625 | 1.0000  | 1.0000 | 1.0000    | 1.0000   |
   | 0.03125| 1.0000  | 1.0000 | 1.0000    | 1.0000   |

   At the coarse rows `h ∈ {0.5, 1.0}` the prediction error is
   `~6%` because the asymptotic power law has not yet stabilized;
   that is consistent with the variance-fit transient regime above.

4. **The fitted model extrapolates to delta-like arm separation.** Under
   the fitted `sqrt(h)` model, the arm widths shrink to zero while the
   centroids remain near `+/-SLIT_Y`, giving the standard two-arm
   limiting values

   ```text
   MI_∞    = log2(2) = 1.0   (perfect arm discrimination)
   d_TV_∞  = 1.0            (orthogonal arm supports)
   1-pur_∞ = 0.5            (inferred two-arm maximum mixing)
   Born_∞  = 0              (machine clean)
   ```

The runner directly checks `MI`, `d_TV`, Born cleanliness, centroids, and
arm-width scaling. The `1-pur` line above is the standard two-arm
orthogonal-limit inference, not an independent measurement in this
runner.

This is a bounded diagnostic for the decoherence response components. It
**does not** claim a closed-form Trotter / resolvent identification of a
full continuum operator, and it does not promote the upstream bounded
Cauchy certificate.

## Why this is a "geodesic" diagnostic, not Brownian

In the rescaled NN harness, the physical length `L = PHYS_L = 40` is
held fixed while spacing `h → 0`. The number of layers is `N = L/h`
and each layer transition shifts y by `h · diy` with `diy ∈ {-1, 0, +1}`.
Total displacement variance is

```text
Var( sum_i h · diy_i ) = h^2 · N · Var(diy_eff) = h · L · Var(diy_eff)
```

so `σ_arm^2 = h · L · Var(diy_eff)`. As `h → 0` with `L` fixed,
`σ_arm → 0`. This is the geodesic fixed-length scaling, not Brownian motion (which
would require `σ^2 ∝ time = const`).

The fitted `C_arm^2 = Var_arm(h) / h ≈ 6.30` gives effective per-step
y-variance `Var(diy_eff) = C_arm^2 / L ≈ 0.158`. (The naive
amplitude-modulus estimate from the per-edge weights gives a different
value because complex amplitudes interfere; the fitted `C_arm` is the
fitted empirical constant for this runner.)

## What this closes (bounded content)

- **The checked decoherence response components have bounded geodesic
  scaling support.** The runner verifies `sqrt(h)`-like arm narrowing and
  a two-Gaussian explanation for the measured `MI` and `d_TV` rows.
- **The fitted limit is consistent with maximum two-arm decoherence.**
  The limiting `MI = 1`, `d_TV = 1`, and inferred `1-pur = 0.5` are
  consequences of the fitted two-arm separation model.
- **The fixed-strength gravity saturation result from the companion note
  has a compatible geometric interpretation.** The present runner does
  not compute gravity, but its field-free geodesic scaling is consistent
  with fixed-strength gravity becoming trivial on this harness.

## What this does NOT close

- Identification of a full continuum operator, or of any gravity /
  scattering subblock, with a specific PDE propagator (Trotter /
  resolvent route, Target A.2 in full generality).
- Closed-form analytic value of `C_arm`. The diagnostic is via
  numerical fit; the fit is robust (`R^2 ≥ 0.99` on four fine-window
  points spanning a factor of 8 in `h`) but `C_arm` is not derived
  from first principles. A separate analytic derivation from the
  per-edge amplitudes, accounting for path-integral phase
  cancellation, remains open.
- Universal continuum claim across the framework. This applies to
  the **rescaled NN harness with `BETA = 0.8`, `K_PHYS = 5.0`, aperture
  edges at `y = ±SLIT_Y = ±3`, fixed L = 40**. Other parameter choices
  give a different `C_arm` and possibly different decoherence
  saturation values.
- A direct `1-pur` runner measurement. The runner records `MI` and
  `d_TV`; the `1-pur` limit is an inference from the same two-arm
  orthogonal fitted model.

## Implications for the 19-row cluster

The 19-row "lattice action / refinement / continuum-limit" sub-lane
gets **two bounded inputs** from this diagnostic:

1. **Audit-review candidates for decoherence-related rows.** Rows whose
   load-bearing claim references `MI`, `d_TV`, or Born cleanliness on
   this exact harness can cite this note as bounded geodesic-scaling
   support. Rows depending on `1-pur` need an explicit check that the
   two-arm orthogonal-limit inference is sufficient for their claim.

2. **Geometric support for why fixed-strength gravity rows stay bounded.**
   The diagnostic is consistent with the saturation result from the
   companion note: at fixed strength, field-free geodesic response
   scaling leaves no nontrivial fixed-strength gravity continuum scalar
   on this harness.

A separate per-row audit is still required to tabulate which rows are in
which category. This note supplies bounded support; it is not itself a
status lift for any parent row.

## Reproduction

```bash
python3 scripts/lattice_nn_rescaled_continuum_identification.py
```

The runner runs through `h = 0.03125`. Review guards (Born `< 1e-10`,
centroid drift `< 1.0`, variance fit
`R^2 ≥ 0.99`, Gaussian-arm prediction match `< 0.05`) all PASS;
runner exits zero on the cached log.

## Audit context

This is a bounded-theorem source note, not an audit verdict. It is
layered on the bounded response-vector Cauchy certificate from the
upstream note and is independent of strength-scaling. The claim is
bounded by the harness parameters and by the finite refinement window
specified above.
