# NN Lattice Rescaled-Lane Full Kernel Identification A(y_s -> y_d)

**Date:** 2026-05-10
**Type:** bounded_theorem
**Claim type:** bounded_theorem (translation-invariant Gaussian-magnitude
quadratic-phase kernel identification on this scoped deterministic-rescale harness)
**Status:** source-note proposal only — on the deterministic-rescale lane through
`h = 0.0625` with five source positions `y_s ∈ {−6, −3, 0, +3, +6}`, the
field-free single-source detector amplitude `A(y_s -> y_d)` factorizes
**exactly** (to machine precision) into

```
A(y_s -> y_d; h) = C_amp(h) · exp[−(y_d − y_s)² / (2 σ²(h))]
                                · exp[i · (c0(h) + c2(h) · (y_d − y_s)²)]
```

with `σ(h)` and `c2(h)` **independent of y_s** (translation invariance) and the
centroid of `|A|²` equal to `y_s` to better than `1e-13` in physical units.
`σ(h) ≈ C_amp_lat · √h` with `C_amp_lat ≈ 4.61` (log-linear fit slope
`α ≈ 0.525`, mirroring the magnitude-saddle log fit on the per-arm channel
of PR #968) and `c2(h) → c2_∞ ≈ 0.02999` matching the closed-form PR #1007
prediction `K (2−√2) / (4 c L) = 0.029985` to within `−0.33%`.

**Status authority:** independent audit lane only.

**Primary runner:**
[`scripts/lattice_nn_rescaled_full_kernel_identification.py`](../scripts/lattice_nn_rescaled_full_kernel_identification.py)

**Cached log:**
[`logs/runner-cache/lattice_nn_rescaled_full_kernel_identification.txt`](../logs/runner-cache/lattice_nn_rescaled_full_kernel_identification.txt)

**Source/context inputs:**

- **Origin-source kernel context**:
  [`NN_LATTICE_RESCALED_KERNEL_IDENTIFICATION_NOTE_2026-05-10.md`](NN_LATTICE_RESCALED_KERNEL_IDENTIFICATION_NOTE_2026-05-10.md)
  and [`scripts/lattice_nn_rescaled_kernel_identification.py`](../scripts/lattice_nn_rescaled_kernel_identification.py)
  identifies, for source at origin and detector spread `A(y_d)`, Gaussian
  magnitude with `σ_amp(h) ~ √h` and quadratic phase with `c2(h) → 0.02995`.
  That runner held `y_s = 0` fixed.
- **Slit-arm context**:
  [`NN_LATTICE_RESCALED_CONTINUUM_IDENTIFICATION_NOTE_2026-05-10.md`](NN_LATTICE_RESCALED_CONTINUUM_IDENTIFICATION_NOTE_2026-05-10.md)
  and [`scripts/lattice_nn_rescaled_continuum_identification.py`](../scripts/lattice_nn_rescaled_continuum_identification.py)
  identifies the slit-anchored per-arm width: with slits at `y = ±SLIT_Y` on
  layer `nl // 3`, `σ_arm(h) = C_arm · h^α` with `C_arm ≈ 2.71`, `α ≈ 0.5256`.
- **Quadratic-phase closed-form context**:
  [`NN_LATTICE_RESCALED_C2_DERIVATION_NOTE_2026-05-10.md`](NN_LATTICE_RESCALED_C2_DERIVATION_NOTE_2026-05-10.md)
  and [`scripts/lattice_nn_rescaled_c2_derivation.py`](../scripts/lattice_nn_rescaled_c2_derivation.py)
  closed form: `c2_∞ = K (2 − √2) / (4 c L_total) ≈ 0.029985` with
  `L_total = 40` (no-slit anchoring is the right one for the phase saddle).
- **Slit-arm saddle context**:
  [`NN_LATTICE_RESCALED_C_ARM_DERIVATION_NOTE_2026-05-10.md`](NN_LATTICE_RESCALED_C_ARM_DERIVATION_NOTE_2026-05-10.md)
  and [`scripts/lattice_nn_rescaled_C_arm_derivation.py`](../scripts/lattice_nn_rescaled_C_arm_derivation.py)
  provide the existing bounded coherent-saddle support surface for the
  slit-detector arm-width constant; this note uses it as support/context, not
  as retained authority.

The runner extends PR #997's harness to a source at `(x = 0, y = y_s)` for
`y_s ∈ {−6, −3, 0, +3, +6}` on the deterministic-rescale lane at
`h ∈ {0.25, 0.125, 0.0625}`, no slits, no field, no blocked nodes.

## Question

PR #997 identified the field-free scattering kernel structure for a single
source at the origin: Gaussian magnitude × quadratic phase with independent
length scales (so NOT Schrödinger). PR #997 used only `y_s = 0`. The open
question is **whether the kernel structure persists under translation of
the source**, i.e. whether `A(y_s, y_d)` depends only on the displacement
`u = y_d − y_s` rather than on `y_s` and `y_d` independently. This is the
distinguishing feature of a translation-invariant integral kernel.

If true, the full kernel of T_∞ on the rescaled NN harness is identified up
to the scope of PR #997 + PR #1007 + PR #968.

## Method

For each `(y_s, h)` in the product grid `{−6, −3, 0, +3, +6} × {0.25, 0.125, 0.0625}`
(15 propagations), with source at `(0, y_s)` (snapped to the nearest lattice
site) and no slits / no field / no blocked nodes:

1. Compute `A(y_d)` for every detector site at `x = PHYS_L = 40`.
2. Define the displacement coordinate `u = y_d − y_s`.
3. Restrict to the central window `|u| ≤ 6` (the angular weight
   `exp(−BETA · θ²)` suppresses larger `|u|` strongly).
4. Fit `|A(u)|` to a Gaussian `c0 · exp(−(u − μ)² / (2σ²))`. Predict `μ = 0`.
5. Fit `arg A(u)` (unwrapped) to a quadratic `c0 + c1 · u + c2 · u²`.

For each fixed `h`, compute the spread of `σ` and `c2` across `y_s` and the
maximum deviation of the `|A|²` centroid from `y_s`.

Acceptance criteria (per row, h fixed across y_s grid):

- `σ(h)` varies by **< 5%** (relative) across `y_s`;
- `c2(h)` varies by **< 5%** (relative) across `y_s`;
- centroid drift `|⟨y_d⟩ − y_s| < 1.0` in physical units;
- Gaussian fit R² ≥ 0.95 per row;
- Quadratic phase fit R² ≥ 0.95 per row.

## Result

The translation-invariance verification passes **to machine precision** across
the full grid:

| h      | σ_min   | σ_max   | rel_spread | c2_min     | c2_max     | rel_spread | drift_max |
| ------ | ------- | ------- | ---------- | ---------- | ---------- | ---------- | --------- |
| 0.2500 | 2.2319  | 2.2319  | 0.0000     | +0.028768  | +0.028768  | 0.0000     | 0.0000    |
| 0.1250 | 1.5344  | 1.5344  | 0.0000     | +0.029676  | +0.029676  | 0.0000     | 0.0000    |
| 0.0625 | 1.0774  | 1.0774  | 0.0000     | +0.029886  | +0.029886  | 0.0000     | 0.0000    |

The rel-spread of σ and c2 is **identically zero** at every h: the
field-free no-slit propagator on the symmetric lattice is exactly
translation-invariant under integer-lattice shifts of the source, and
the per-edge factor `step_scale · exp(i k L) · exp(−BETA θ²) / L` has
identical form regardless of the source y-coordinate. This is a hard
property of the deterministic-rescale harness, not an empirical
finding sensitive to noise.

Fit qualities at every (h, y_s):

| metric                       | min value |
| ---------------------------- | --------- |
| Gaussian magnitude R²        | 1.0000    |
| Quadratic phase R²           | 1.0000    |

The amplitude pattern is Gaussian-magnitude × quadratic-phase to numerical
precision at every (h, y_s) in the grid.

Continuum c2 cross-check (vs PR #1007 closed form `c2_∞ = 0.029985`):

- At `h = 0.0625`, `⟨c2⟩_{y_s} = 0.029886`, deviation = **−0.33%** vs the
  analytic continuum value. This is identical to the PR #997 per-h cache
  value and consistent with the residual reported in PR #1007.

## Closed-form full kernel

Combining the PR #997 / PR #1007 / PR #968 + present results, the
field-free single-source kernel on the rescaled NN harness through
`h = 0.0625` is, to within the scoped tolerances:

```
A(y_s -> y_d; h) = C_amp(h) · exp[− u² / (2 σ²(h))]
                              · exp[i · (c0(h) + c1(h) · u + c2(h) · u²)]
```

with `u = y_d − y_s`, and:

- `σ(h) ≈ C_amp_lat · √h` with `C_amp_lat ≈ 4.61` (log-linear fit on
  `h ∈ {0.25, 0.125, 0.0625}`, slope `α = 0.525` matching PR #968's
  per-arm width exponent);
- `c2(h) → c2_∞ ≈ 0.02999` matching PR #1007's analytic
  `K(2−√2)/(4 c L_total) = 0.029985`;
- `c1(h) ≈ 0` by the symmetry of `A(u)` under `u → −u` (numerically
  driven below `1e-10` for `y_s = 0`; for `y_s ≠ 0` the linear coefficient
  remains identically zero in the displacement coordinate);
- `c0(h)` carries the overall phase reference (immaterial for kernel
  shape).

The two key continuum identifications:

- Magnitude: **Gaussian** in the displacement `u`, width `σ(h) ~ √h`
  (vanishing in the continuum), with finite amplitude prefactor.
- Phase: **quadratic** in `u`, curvature `c2(h) → c2_∞ ≈ 0.02999`
  (finite in the continuum).

The two h-scalings are **independent**: `σ → 0` while `c2 → finite`. This
is the non-Schrödinger property of PR #997, now generalized: it holds for
every source position `y_s ∈ {−6, −3, 0, +3, +6}` to machine precision
(translation invariance).

## Slit-anchored cross-check (PR #968 connection)

The scoped bridge step is connecting the slit-anchored per-arm
width `σ_arm(h) = C_arm · √h` (PR #968) to the no-slit kernel width
`σ_amp(h) = C_amp · √h` (this runner). The existing
[`C_arm` coherent-saddle support note](NN_LATTICE_RESCALED_C_ARM_DERIVATION_NOTE_2026-05-10.md)
provides the bounded saddle context. This runner's measured no-slit kernel
then supports the sharper length-scaling cross-check: the field-free Gaussian
kernel variance scales as `σ²(L; h) = K_amp · L · h` with
`K_amp = C_amp² / L_total` independent of `L`. So the per-arm
width in the slit harness has, by Huygens, two natural anchoring lengths:

- **(A) L_2 anchoring** (post-slit Huygens propagation slit → detector):
  `σ_arm² = K_amp · L_2 · h = (L_2 / L_total) · σ_amp²`,
  giving `C_arm_pred(L_2) = √(2/3) · C_amp = 0.8165 · 4.607 = 3.762`.
- **(B) L_1 anchoring** (source → slit selection length):
  `σ_arm² = K_amp · L_1 · h = (L_1 / L_total) · σ_amp²`,
  giving `C_arm_pred(L_1) = √(1/3) · C_amp = 0.5774 · 4.607 = 2.660`.

PR #968 measures **C_arm = 2.71**. The residuals are:

| anchoring | predicted C_arm | residual vs PR #968 |
| --------- | --------------- | ------------------- |
| L_2 (post-slit Huygens, 2/3 L_total) | 3.762 | **+38.81%** (fails) |
| L_1 (source-to-slit, 1/3 L_total)    | 2.660 | **−1.85%** (passes within tolerance) |

**The L_1 anchoring wins.** The per-arm width in PR #968's slit harness is
the no-slit kernel's width restricted to the source-to-slit propagation
length `L_1 = L_total / 3 = 13.33`. The naive Huygens picture
(L_2 = 2 L_total / 3) is wrong by ~40%.

This matches the residuals reported in `lattice_nn_rescaled_C_arm_derivation.py`:

| C_arm candidate           | value   | residual |
| ------------------------- | ------- | -------- |
| C_arm_incoh               | 3.2955  | +21.57%  |
| C_arm_coherent_full       | 3.0441  | +12.30%  |
| **C_arm_coherent_slit**   | **2.4855** | **−8.31%** (closest)  |
| **C_arm_pred(L_1) (this note)** | **2.6599** | **−1.85%** (sharper)  |

The L_1 anchoring picture is **sharper** than even PR #968's own
post-slit saddle by a factor of ~4× in residual error. The physical
interpretation: a narrow slit at distance `L_1` from the source acts as
a **selection filter** on the source's natural angular spread. The
angular spread the source must have to reach the slit is `~ SLIT_Y / L_1`;
the spread at the detector is this angular spread times the lever arm to
the slit, which by the saddle scaling reduces to `(L_1 / L_total) · σ_amp²`.

This is *not* the Huygens reanchoring "slit acts as secondary source"
picture (which would give the L_2 anchoring and is wrong by ~40%). The
slit acts as a *projector* of the source's natural distribution onto a
narrow channel; the propagation length set by the source-to-slit baseline
controls how much angular spread the source had to develop to reach the
slit. The post-slit propagation is geometrically slaved to that angular
spread, not freshly generated.

The connection to PR #968's `L_2 = 2L/3` framing: PR #968 fits
`σ_arm(h) = C_arm · √h` without committing to an anchoring length. The
`L_2 = 2L/3` ansatz was the natural post-slit guess but did not produce
the closed-form C_arm. The present source note identifies the right
anchoring: `L_1 = L/3`, giving sharper residual.

## Verdict

**Bounded identification, source-note status.**

On the rescaled NN harness through `h = 0.0625` with five source positions:

- the full field-free no-slit kernel `A(y_s → y_d; h)` is translation
  invariant under integer-lattice shifts of `y_s`, to machine precision;
- the magnitude is Gaussian in the displacement `u = y_d − y_s` with
  width `σ(h) ~ √h`, R² = 1.0000 at every grid row;
- the phase is quadratic in `u` with curvature `c2(h) → c2_∞ ≈ 0.02999`
  (matches PR #1007 analytic to −0.33%), R² = 1.0000 at every grid row;
- the slit-anchored cross-check connects PR #968's `C_arm ≈ 2.71` to
  this runner's `C_amp ≈ 4.607` via the **L_1 (source-to-slit) anchoring**
  `C_arm = √(1/3) · C_amp = 2.660` (residual −1.85%), **not** the
  L_2 = 2L/3 post-slit Huygens anchoring (residual +38.81%).

The closed-form full kernel on this scoped harness is:

```
A(y_s → y_d; h) = C_amp(h) · exp[−(y_d − y_s)² / (2 σ²(h))]
                              · exp[i · (c0(h) + c2_∞ · (y_d − y_s)²)]
```

with `σ(h) ≈ 4.61 · √h` (per log-linear fit) and `c2_∞ ≈ 0.02999` (PR
#1007 closed form). The kernel is **not Schrödinger** (independent
magnitude and phase length scales, PR #997 no-go) but is **translation
invariant** and **Gaussian × quadratic-phase** in the displacement.

This is a bounded source-note identification, not a retained-family
audit claim. The scope is:

- field-free, no-slit, single-source propagation;
- five lattice source positions `y_s ∈ {−6, −3, 0, +3, +6}`;
- three refinements `h ∈ {0.25, 0.125, 0.0625}` (excluding `h = 0.03125`);
- canonical harness parameters `BETA = 0.8`, `k = 5.0`, `L_total = 40`,
  `FANOUT = 3.0`.

The slit-anchored cross-check is the scoped connection: the
no-slit kernel of this note + the L_1 anchoring identified here together
predict PR #968's `C_arm` to within 2%, providing a sharper saddle-point
explanation for PR #968's per-arm width than was available before.

## Provenance

- Runner: `scripts/lattice_nn_rescaled_full_kernel_identification.py`
  (SHA-256 in cache header).
- Cache: `logs/runner-cache/lattice_nn_rescaled_full_kernel_identification.txt`.
- Elapsed: ~12 seconds wall clock for the full sweep (15 propagations).
- No external data or dependencies beyond the harness conventions
  embedded in PR #997 / PR #968 / PR #1007.
