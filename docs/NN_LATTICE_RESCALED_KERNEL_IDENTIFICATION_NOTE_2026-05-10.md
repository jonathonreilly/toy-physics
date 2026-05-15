# NN Lattice Rescaled-Lane Kernel Identification

**Date:** 2026-05-10
**Claim type:** no_go (bounded numerical no-go for the Schrödinger
free-particle identification on this harness)
**Status:** source-note proposal only — on the deterministic-rescale
lane through `h = 0.0625`, the single-source field-free
amplitude pattern `A(y_d)` has a Gaussian magnitude with
`σ(h) → 0` as `h → 0` AND a quadratic phase whose Hessian curvature
`c2(h) → c2_∞ ≈ 0.0299` is finite. The two would have to give the
same effective mass for a Schrödinger free-particle identification;
they do not. T_∞'s scattering kernel is therefore **not** the
Schrödinger free-particle propagator on this scoped harness.
**Status authority:** independent audit lane only.
**Primary runner:** [`scripts/lattice_nn_rescaled_kernel_identification.py`](../scripts/lattice_nn_rescaled_kernel_identification.py)
**Cached log:** [`logs/runner-cache/lattice_nn_rescaled_kernel_identification.txt`](../logs/runner-cache/lattice_nn_rescaled_kernel_identification.txt)

**Source/context inputs:**

- `LATTICE_NN_HIGH_PRECISION_NOTE.md` is context-only for the
  deterministic-rescale convention. The runner embeds the harness
  convention directly with `step_scale = h / sqrt(FANOUT)`; this
  source note does not cite that legacy note as load-bearing authority
  and does not promote its audit status.
- PR #957, PR #968, and PR #945 are companion-context references for
  the broader `T_infinity` program. They are not load-bearing
  dependencies for this no-go. This note's load-bearing evidence is the
  paired runner's direct harness computation.

## Question

In the broader `T_infinity` program, an open question is:
**what continuum operator is T_∞ on observables that are NOT the
decoherence vector?** The cleanest probe is the single-source
detector amplitude pattern.

## Method

For each refinement `h ∈ {0.5, 0.25, 0.125, 0.0625}` on the
deterministic-rescale lane (`step_scale = h / sqrt(FANOUT)`), with
a single point source at `(0, 0)`, no slits, no blocked nodes, and
no field, compute `A(y_d)` for every detector site at `x = PHYS_L`.
Per-edge factor: `step_scale · exp(i·K_PHYS·L) · exp(-BETA·θ²) / L`
with `BETA = 0.8`, `K_PHYS = 5.0`, `L = PHYS_L = 40`.

Restrict to the central window `|y_d| ≤ 6` (where the angular weight
`exp(-BETA·θ²)` keeps the signal above floating-point noise) and
fit:

- **Magnitude candidates** to `|A(y_d)|`:
  - Gaussian: `c0 · exp(-(y_d − μ)² / (2σ²))`
  - Constant: `c0`
  - Power law: `c0 · |y_d|^(−α)`

- **Phase candidates** to `arg(A(y_d))` after unwrapping:
  - Quadratic: `c0 + c1·y_d + c2·y_d²`
  - Linear: `c0 + c1·y_d`
  - Constant: `c0`

`R²` reported per-candidate. Best candidate per `h` is the highest
`R²`; identification requires the same best candidate at the three
finest `h`'s (stability) and `R² ≥ 0.95`.

## Result (data, central window)

|   h    | best_mag | R² (mag) | σ        | best_phase | R² (phase) | c2         |
|:------:|:--------:|:--------:|:--------:|:----------:|:----------:|:----------:|
| 0.5    | gaussian | 1.0000   | 3.5582   | quadratic  | 1.0000     | +0.025062  |
| 0.25   | gaussian | 1.0000   | 2.2319   | quadratic  | 1.0000     | +0.028768  |
| 0.125  | gaussian | 1.0000   | 1.5344   | quadratic  | 1.0000     | +0.029676  |
| 0.0625 | gaussian | 1.0000   | 1.0774   | quadratic  | 1.0000     | +0.029886  |

Both shape candidates fit to machine precision at every measured
`h`, and the best-candidate winner is stable across all four `h`'s.

**Magnitude shape is Gaussian; phase shape is quadratic.**

### Refinement scaling

- **Width:** log-linear fit `σ(h) = C_σ · h^p` gives
  `p = 0.5711, C_σ = 5.121, R² = 0.9956` (4 points). The exponent
  `p ≈ 0.5` is consistent with a `√h` geodesic-spreading pattern,
  with finite-h corrections consistent with the discrete lattice.
  Therefore `σ → 0` as `h → 0` and the kernel collapses to a δ in
  `y_d` in the continuum.

- **Phase Hessian:** the quadratic coefficient `c2(h)` converges
  rapidly to a finite limit. Differences from the empirical
  asymptote `c2_∞ ≈ 0.02995` go `4.9e-3 → 1.2e-3 → 2.7e-4 → 6.4e-5`
  across the four `h`-values — a clean ≈ 4× per halving (consistent
  with `O(h²)` convergence). Therefore `c2 → c2_∞ ≈ 0.0299` is a
  finite continuum number.

## The Schrödinger free-particle test

If the kernel were the Schrödinger free-particle propagator

```text
K(y; L) = sqrt(m_eff / (2πi·L)) · exp(i·m_eff·y² / (2L))
```

then the quadratic phase coefficient would imply
`m_eff_phase = 2·L·c2`, and the Gaussian width via free-particle
spreading from a point source `σ²(L) ≈ (L/m_eff)²` would imply
`m_eff_width = L/σ`. The two extractions must agree.

|   h    | c2         | m_eff_phase = 2L·c2 | σ      | m_eff_width = L/σ |
|:------:|:----------:|:-------------------:|:------:|:-----------------:|
| 0.5    | +0.025062  | +2.0050             | 3.5582 | +11.24            |
| 0.25   | +0.028768  | +2.3015             | 2.2319 | +17.92            |
| 0.125  | +0.029676  | +2.3741             | 1.5344 | +26.07            |
| 0.0625 | +0.029886  | +2.3909             | 1.0774 | +37.13            |

`m_eff_phase` is converging to a finite limit `≈ 2.39`. **`m_eff_width`
is diverging as `1/√h`** because `σ → 0` while `L` is held fixed.
Their relative disagreement at the finest `h` is `1453%`, not `5%`.
The two `m_eff` extractions are not the same physical mass scale —
they are not even the same order of magnitude, and they diverge
from each other as `h → 0`.

**Verdict:** T_∞'s scattering kernel is **not** the Schrödinger
free-particle propagator on the rescaled NN harness with
`K_PHYS = 5.0`.

## Scoped continuum-limit constraints (bounded content of the null)

The bounded null is informative — it constrains the candidate space
for T_∞'s scattering kernel:

1. **Magnitude is Gaussian (R² = 1.0)** with `σ → 0` as `√h`
   on the measured refinement ladder. The bounded extrapolation is a
   δ-supported detector profile in `y_d` at the geodesic arrival point
   for this slit-free single-source probe.

2. **Phase is quadratic (R² = 1.0)** with finite Hessian curvature
   `c2_∞ ≈ 0.02995`. The phase Hessian survives the continuum
   limit even though the magnitude collapses to a δ.

3. **Empirical relation:** `c2_∞ ≈ K_PHYS / (4 L) = 0.03125`
   (observed `0.02995` is 4% below this, the difference attributable
   to the BETA-weighted angular integral). The naive ray-optics
   path-length expansion `L_path(y) ≈ L + y²/(2L)` would give
   `c2 = K_PHYS / (2 L) = 0.0625`; the observed value is half of
   that. Equivalently `m_eff_phase ≈ K_PHYS / 2 ≈ 2.5` versus
   observed `2.39`. The factor-of-two reduction is consistent with
   the Gaussian-weighted angular kernel `exp(-BETA·θ²)` averaging
   the path-length over the cone of directions reaching `y_d`,
   not with the single-geodesic ray-optics phase. (We register this
   as bounded numerical support, not as a closed-form derivation.)

4. **The bounded limiting ansatz suggested by this probe is**

   ```text
   K_∞(y_d) ∝ δ(y_d) · exp(i·c2_∞·y_d²)
   ```

   in the distributional sense, where `c2_∞ = lim_{h→0} c2(h)`,
   if the measured scaling persists. The δ kills the spatial extent;
   the surviving `exp(i·c2_∞·y²)` factor is a phase ramp evaluated
   against the δ-support, so it contributes a single phase value to
   the continuum amplitude. Operationally, the measured ladder leaves
   only the on-axis amplitude `A(0)` and a vanishing neighborhood
   structure in this harness.

5. **No Schrödinger free-particle fit is consistent.** Any
   continuum candidate for T_∞'s scattering kernel must
   simultaneously reproduce: (a) Gaussian magnitude with
   `σ ∝ √h`, (b) quadratic phase with finite `c2_∞`, and
   (c) the resulting incompatibility between width-based and
   phase-based effective masses. The Schrödinger free-particle
   propagator does not reproduce (c).

## Why the geodesic and Schrödinger pictures disagree here

- **Geodesic-collapse comparison:** `σ ∝ √h` arises from the
  `√h · √L` per-step variance of the discrete random-walk-of-
  fan-out-3, with `L` fixed. As `h → 0`, the arrival distribution
  collapses onto the classical geodesic, hence `σ → 0`.
- **Schrödinger free-particle:** `σ²(L) = σ_0² + (L/m_eff)²` from
  a point source has `σ → L/m_eff > 0` for any finite `m_eff` —
  no `h` parameter at all. The Schrödinger propagator is
  intrinsically continuum and cannot have `σ → 0` at fixed `L`
  unless `m_eff → ∞`.

These two pictures are incompatible *unless* `m_eff = m_eff(h) → ∞`
as `h → 0`. The phase-derived `m_eff_phase` does **not** diverge:
it converges to `≈ 2.39`. So the kernel inherits its phase
structure from the framework's path-integral phase factor (the
`exp(i·K_PHYS·L)` per-edge term), but its width from the
geodesic-collapse mechanism. **These are independent dynamical
sources.** A single Schrödinger free-particle propagator cannot
produce both with consistent `m_eff`.

## Guards (all PASS on cached log)

- **Born-clean amplitude:** `sum |A|^2` positive and free of
  NaN/inf at every measured `h`.
- **k=0 control:** at `K_PHYS = 0` with single source at origin,
  the centroid drift of `|A(y_d)|²` is `+1.6e-17` (machine zero),
  consistent with the y-symmetry of the lattice and zero-field
  configuration. The K_PHYS=0 phase and imaginary amplitude component
  are exactly zero (real-valued amplitudes) — confirming that the
  quadratic phase observed at
  `K_PHYS = 5.0` is contributed by the framework's path-integral
  factor `exp(i·K_PHYS·L)`, not by lattice geometry alone.
- **Fit convergence:** R² = 1.0000 (machine clean) for both the
  best magnitude (Gaussian) and best phase (quadratic) at every
  `h`. Tolerance threshold 0.95 satisfied with full margin.
- **Cross-validation:** `m_eff_phase` and `m_eff_width` extracted
  independently from phase and magnitude. Disagreement = 1453%
  at finest `h`, far exceeding the 5% tolerance. **This is the
  observation that delivers the null-result.**

## What this closes

- Scoped non-Schrödinger constraint on the scattering response on this
  harness: any continuum operator candidate proposed for the rescaled NN
  harness's field-free single-source response must reproduce both the
  fitted Gaussian magnitude / quadratic-phase shape AND their incompatible
  `m_eff`. The Schrödinger free-particle propagator is ruled out as such
  a candidate on this checked window.
- Independently observes `√h` width scaling from a slit-free probe,
  giving a direct check that the `σ ∝ √h` collapse is a feature of
  this scoped rescaled NN computation.
- Provides a kernel-shape decomposition for the 19-row lattice-
  action / refinement / continuum-limit cluster: the magnitude
  side is geodesic-like, the phase side is path-integral-
  phase-derived, and the two cannot be unified into a single
  Schrödinger free-particle operator.

## What this does NOT close

- A **positive** identification of a continuum scattering kernel for
  this harness. The fitted shape `K(y_d) ∝ δ(y_d) · exp(i·c2_∞·y_d²)`
  on this checked window is observationally consistent with the
  measured data, but it is not a conventional PDE propagator and is
  not claimed as a closed-form Trotter / resolvent identification.
- Universal continuum claim across the framework. This applies
  to the **rescaled NN harness with `BETA = 0.8`, `K_PHYS = 5.0`,
  `L = 40`** and a single source at the origin. Other parameter
  choices may give different `c2_∞` and different `σ`-scaling
  prefactors.
- A first-principles derivation of the empirical
  `c2_∞ ≈ K_PHYS/2 / (2L) = K_PHYS/(4L)` ratio. Numerically it
  is the dominant term, but the derivation from the BETA-weighted
  angular integral is left open. The closed-form analytic value
  is a candidate for a follow-up note.

## Reproduction

```bash
python3 scripts/lattice_nn_rescaled_kernel_identification.py
```

Runtime ~2 s wallclock through `h = 0.0625`. All audit guards
(Born-clean, k=0 control, fit convergence, expected
cross-validation failure) report cleanly. The runner exits zero only
when the proposed no-go is observed; an unexpected positive
Schrödinger identification or missing no-go prerequisite exits
nonzero.

## Audit context

This is a bounded numerical no-go that constrains the candidate space
for the scoped scattering subblock. It does not depend on the landing
or audit status of PR #957, PR #968, or PR #945. Those companion
threads may later supply broader context, but the no-go here is the
direct mismatch between the phase-derived and width-derived
Schrödinger effective masses.

```yaml
proposed_claim_type: no_go
proposed_claim_scope: |
  On the deterministic-rescale NN lane with BETA=0.8, K_PHYS=5.0,
  PHYS_L=40, single source, no slits, no blocked nodes, and no field,
  the measured central detector amplitude has Gaussian magnitude and
  quadratic phase, but the width-derived and phase-derived
  Schrödinger effective masses disagree by 1453% at h=0.0625 and
  separate further as h -> 0. This rules out the Schrödinger
  free-particle propagator as the continuum scattering kernel for
  this scoped harness.
status_authority: independent audit lane only
forbidden_imports_used: false
audit_required_before_effective_status_change: true
```
