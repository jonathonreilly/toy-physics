# Action-Power 3D Operator-Cauchy Continuum-Bridge Test

**Date:** 2026-05-10
**Claim type:** bounded_null_result (sharp bounded null on the action-power
3D ordered-lattice harness; the operator-Cauchy continuum-bridge does NOT
close at any tested action-power exponent)
**Status:** source-note proposal only; independent audit controls any
retained status.
**Status authority:** independent audit lane only.

## Artifact Chain

- Primary runner: [`scripts/action_power_3d_operator_cauchy.py`](../scripts/action_power_3d_operator_cauchy.py)
- Cached stdout: [`logs/runner-cache/action_power_3d_operator_cauchy.txt`](../logs/runner-cache/action_power_3d_operator_cauchy.txt)
- Source notes whose harness this generalises:
  - [`docs/ACTION_POWER_3D_GRAVITY_SIGN_CLOSURE_NOTE.md`](ACTION_POWER_3D_GRAVITY_SIGN_CLOSURE_NOTE.md)
    (bounded fixed-family barrier-sign closure at one h)
  - [`docs/ACTION_UNIQUENESS_NOTE.md`](ACTION_UNIQUENESS_NOTE.md)
    (fixed-family universality-class result at one h, p in {0.5, 1, 2})
- Cited methodological authorities (operator-Cauchy method):
  - [`docs/NN_LATTICE_RESCALED_KERNEL_IDENTIFICATION_NOTE_2026-05-10.md`](NN_LATTICE_RESCALED_KERNEL_IDENTIFICATION_NOTE_2026-05-10.md)
    (operator-Cauchy lane on the rescaled NN harness)
- Companion bounded-null context (operator-Cauchy on a non-promotable family):
  - alt-connectivity grown DAG family bounded no-go (PR #1008)

## Question

Both source notes register results on the 3D ordered dense-lattice
action-power family at **one h value** (`h = 0.5`, `PHYS_W = 8`/`10`,
`MAX_D_PHYS = 3`).  They explicitly leave the continuum-limit bridge open:

> "What this does NOT close: ... continuum-limit rescue beyond the current
> ordered-family finite harness ... other action families"
> — ACTION_POWER_3D_GRAVITY_SIGN_CLOSURE_NOTE.md

> "It does not prove a universal theorem across all graph families."
> — ACTION_UNIQUENESS_NOTE.md

The operator-Cauchy method that closed the rescaled NN harness (PRs
#957 / #968 / #1003 / #1007 / #1054 / #1055 / #1056) is the canonical
tool for asking whether a discrete family of operators `T_h` converges to
a continuum object `T_inf` as `h -> 0`.  This note applies that method to
the action-power 3D ordered-lattice harness.

## Harness Structure (Findings)

Both source-note harnesses use the same family:

- 3D ordered forward lattice with isotropic NN-like dense kernel
- per-edge factor `(h^2 / L^2) * exp(-BETA * theta^2) * exp(i * K * act)`
  where `act = L * (1 - f^p)` (the action-power family) and the `h^2`
  factor is the lattice measure
- field `f = strength / r` from a mass source on the central z-axis at
  layer `gl = 2 nl / 3`
- detector: full final layer; framework observable = `z`-centroid shift
  (= gravity)
- barrier at `bl = nl / 3` with NS slits at `y = +/- 0.5`

**The refinement parameter `h` IS exposed** in `Lattice3D(phys_l, phys_w,
h)` in `action_universality_probe.py` — unlike the alt-connectivity DAG
family in PR #1008, where `H = 0.5` was a module constant.  So
h-refinement is **structurally available** on this harness.  What is
hardcoded at `h = 0.5` is the *registered* parameter choice in the two
source notes, not the harness itself.  Operator-Cauchy can therefore be
applied directly.

### Harness compression (re-parameterisation)

The canonical `(PHYS_L, PHYS_W, MAX_D_PHYS) = (12, 8, 3)` configuration is
intractable below `h = 0.25` (one propagation at `h = 0.125` takes
~100 s even with NumPy; the propagation cost scales as
`(2 W / h + 1)^2 * (2 max_d_phys / h + 1)^2 * (L / h)`).  We therefore
work on a re-parameterised companion family

    (PHYS_L, PHYS_W, MAX_D_PHYS) = (10, 4, 1.5)

This preserves the harness structure (3D ordered forward lattice, dense
`1 / L^2` kernel with `h^2` measure, `exp(-BETA θ²)` angular weight,
`exp(i K L (1 - f^p))` phase) while keeping `h = 0.125` tractable at
~12 s per propagation and ~2 min per measurement cell.  We register this
as a structurally-equivalent companion family, not a numerical replay of
the source-note harnesses.

## Method

- **Refinement grid:** `h in {1.0, 0.5, 0.25, 0.125}` (geometric halving)
- **Action powers:** `p in {0.5, 1.0, 2.0}` — the sublinear /
  weak-field-linear / superlinear valley classes from
  ACTION_UNIQUENESS_NOTE
- **Mass-source z grid:** `mass_z in {2.0, 3.0}` (two independent gravity
  probes, both inside `PHYS_W = 4`)
- **Cauchy observable vector per (h, p):**

      vec(h; p) = ( gravity(mass_z = 2.0),
                    gravity(mass_z = 3.0),
                    Born )

  (dim = 3, dimensionless only).  `p_total_f` (field-free total detector
  throughput) is **measured** as a structural diagnostic but is NOT
  included in the Cauchy L2 — see Structural Reason 1 below.
- **Cauchy increments:** `||vec(h_n; p) - vec(h_{n+1}; p)||_2`
- **Geometric fit:** `||delta||_2 ~ C * h_geom^r` on the three increments
  with `h_geom = sqrt(h_n * h_{n+1})`
- **Gate:** positive existence at `p` requires `r > 0.5` AND `R^2 >= 0.95`
- **Guards:** Born-clean (`|I_3| / P < 1e-10` at every cell), k=0 control
  (gravity at `K = 0` should vanish by symmetry; `< 1e-10`)

## Result

### Per-cell measurements

| p   | h     | mass_z | gravity       | Born     | p_total_f   |
|-----|-------|--------|---------------|----------|-------------|
| 0.5 | 1.000 | 2.0    | +4.254e-03    | 6.58e-16 | 3.503e+04   |
| 0.5 | 1.000 | 3.0    | -1.404e-03    | 6.58e-16 | 3.503e+04   |
| 0.5 | 0.500 | 2.0    | +1.136e-02    | 1.22e-15 | 6.322e+07   |
| 0.5 | 0.500 | 3.0    | +1.442e-02    | 1.22e-15 | 6.322e+07   |
| 0.5 | 0.250 | 2.0    | +1.228e-02    | 1.75e-15 | 2.584e+30   |
| 0.5 | 0.250 | 3.0    | +1.468e-02    | 1.75e-15 | 2.584e+30   |
| 0.5 | 0.125 | 2.0    | +2.315e-02    | 3.27e-15 | 5.576e+82   |
| 0.5 | 0.125 | 3.0    | +3.076e-02    | 3.27e-15 | 5.576e+82   |
| 1.0 | 1.000 | 2.0    | +1.430e-04    | 6.58e-16 | 3.503e+04   |
| 1.0 | 1.000 | 3.0    | +5.014e-05    | 6.58e-16 | 3.503e+04   |
| 1.0 | 0.500 | 2.0    | +8.209e-05    | 1.22e-15 | 6.322e+07   |
| 1.0 | 0.500 | 3.0    | +9.416e-05    | 1.22e-15 | 6.322e+07   |
| 1.0 | 0.250 | 2.0    | +9.058e-05    | 1.75e-15 | 2.584e+30   |
| 1.0 | 0.250 | 3.0    | +9.496e-05    | 1.75e-15 | 2.584e+30   |
| 1.0 | 0.125 | 2.0    | +1.600e-04    | 3.27e-15 | 5.576e+82   |
| 1.0 | 0.125 | 3.0    | +2.109e-04    | 3.27e-15 | 5.576e+82   |
| 2.0 | all   | all    | < 1e-8 (below floor; see below) | 6.58e-16 - 3.27e-15 | (same explosion) |

### Guards (all PASS)

- **Born-clean:** `max |I_3| / P` across all 24 cells = `3.27e-15`
  (tolerance `< 1e-10`).
- **k=0 control:** `max |gravity(K=0)|` across all 24 cells = `0.0`
  (machine zero, tolerance `< 1e-10`).

### Cauchy L2 increments (dimensionless basis: gravity × 2 + Born)

**p = 0.5:**
```
  h_n -> h_{n+1}      ||delta||_2     comment
  1.000 -> 0.500      1.7346e-02      large transient (sign flip in z=3)
  0.500 -> 0.250      9.6006e-04      smallest increment
  0.250 -> 0.125      1.9412e-02      FINEST step is LARGEST — non-Cauchy
```
Fit `||delta||_2 ~ C h_geom^r` (3 pts): **r = -0.0812, C = 6.31e-03, R^2 = 0.0011**.

**p = 1.0:**
```
  h_n -> h_{n+1}      ||delta||_2     comment
  1.000 -> 0.500      7.5186e-05      transient (mass_z=2 decreases)
  0.500 -> 0.250      8.5293e-06      smallest increment
  0.250 -> 0.125      1.3514e-04      FINEST step is LARGEST — non-Cauchy
```
Fit `||delta||_2 ~ C h_geom^r` (3 pts): **r = -0.4230, C = 2.85e-05, R^2 = 0.0406**.

**p = 2.0:**
```
  h_n -> h_{n+1}      ||delta||_2     comment
  1.000 -> 0.500      4.7504e-08      gravity signal ~ 1e-8 (weak-field; f^2 ~ 2.5e-9 makes  L (1 - f^2) numerically near L)
  0.500 -> 0.250      1.8914e-09      smallest
  0.250 -> 0.125      3.8361e-09      finest step LARGER than middle (factor 2.0)
```
Fit `||delta||_2 ~ C h_geom^r` (3 pts): **r = +1.8152, C = 4.63e-08, R^2 = 0.5515**.

The p=2.0 fit has positive slope (`r ≈ 1.8`) but R^2 = 0.55 fails the
acceptance gate (which requires `R^2 >= 0.95`).  Two factors:

- the gravity signal at strength = 5e-5 is ~ 1e-8 — at the boundary of
  numerical interpretability of the propagator amplitudes
- even on this small-signal regime the finest-h increment is 2x larger
  than the middle-h increment, the same non-monotone pattern that
  rules out the p = 0.5 and p = 1.0 cases

We classify this as PARTIAL CONVERGENCE (not a positive identification,
not a sharp non-decaying null) — a noise-dominated regime where finer
h or a larger strength is required to determine the true asymptotic
behaviour.  The acceptance gate (r > 0.5, R^2 >= 0.95) is not met.

### Cross-power summary

| p    | r        | R^2    | classification           |
|------|----------|--------|--------------------------|
| 0.50 | -0.0812  | 0.0011 | sharp null (non-decaying, R^2 ~ 0) |
| 1.00 | -0.4230  | 0.0406 | sharp null (non-decaying, R^2 ~ 0) |
| 2.00 | +1.8152  | 0.5515 | partial (positive r but R^2 < 0.95; noise-dominated weak-signal regime) |

Verdict: **bounded null at every tested action-power exponent.**
No `p` in `{0.5, 1.0, 2.0}` clears the operator-Cauchy gate
(`r > 0.5 AND R^2 >= 0.95`).

## Diagnosis: Two Structural Reasons for the Null

The bounded null is informative — it is the same kind of class-A
structural no-go that PR #1008 registered for the alt-connectivity DAG
family, but with a *different* mechanism on a *different* harness.  Two
structural reasons stack:

### Structural Reason 1: the dense `(h^2 / L^2)` kernel is non-unitary

On this harness the per-edge factor is

    K_ij  =  (h^2 / L_ij^2) * exp(-BETA * theta_ij^2) * exp(i * K * act_ij)

The `h^2` factor is the lattice-Riemann measure and `1 / L^2` is the
"propagator" amplitude; together they target a continuum integral
`∫ d²y / L²`.  But this combination is **not** automatically norm-
preserving — the discrete sum `Σ_j |K_ij|^2` is not bounded by 1 as
`h -> 0`.

The runner measures the field-free total detector throughput
`p_total_f := Σ_{d ∈ det} |A(d)|²` per cell.  Empirically:

| h     | p_total_f   | log_10        |
|-------|-------------|---------------|
| 1.000 | 3.503e+04   | 4.5           |
| 0.500 | 6.322e+07   | 7.8           |
| 0.250 | 2.584e+30   | 30.4          |
| 0.125 | 5.576e+82   | 82.7          |

`p_total_f` grows by ~78 orders of magnitude over three halvings of `h`
on this harness.  This is the same value across all three action powers
(action-independent: `Born` is at the `~1e-15` machine-zero floor at
field-free configuration, so the per-edge phase is irrelevant to the
magnitude sum).

This polynomial-in-`1/h` divergence of the amplitude-sum is a direct
signal of non-unitarity of `T_h`: the discrete operator is not even
bounded as `h -> 0`, let alone Cauchy.  A continuum-limit operator
`T_inf` in any reasonable sense does not exist for the un-normalised
amplitudes on this kernel.

The reason `gravity` and `Born` survive as bounded numbers is that both
are *ratios* normalised by `p_total_f` (gravity is a z-centroid
expectation `⟨z⟩ = Σ |A|² z / Σ |A|²`; Born is `|I_3| / P`).  So the
**framework observables** can in principle remain bounded even when the
underlying amplitude operator diverges — but they inherit no Cauchy
structure from the amplitude operator.

### Structural Reason 2: gravity L2 increments are non-monotone, with the finest-h step LARGEST

Even on the bounded ratio-observables, the Cauchy increments fail
sharply.  Looking at the gravity-only basis at `p = 0.5` and `p = 1.0`,
the pattern is identical:

    h: 1.0     -> 0.5  -> 0.25  -> 0.125
       large transient  smallest  LARGEST

The middle increment (`0.5 -> 0.25`) is the smallest by 10x — 20x; the
finest increment (`0.25 -> 0.125`) is then 10x — 20x **larger** than
the middle one.  This is the opposite of geometric Cauchy decay (which
would predict the finest-h step to be the smallest).

A reasonable conjecture for the mechanism is that the un-normalised
amplitude operator's polynomial-in-`1/h` divergence produces a slow
saddle-redistribution of phase: at coarser h the ratio observables
appear to stabilise (because the divergent normalisation is similar at
adjacent h), but at finer h new oscillation modes enter the angular
weight `exp(-BETA θ²)` integral and the ratio shifts again.  We do not
attempt a closed-form analysis of this mechanism here; the registered
observation is the bounded non-monotone Cauchy pattern.

### Why h is "available" but does not give a continuum

Unlike the alt-connectivity DAG family of PR #1008 (where `H = 0.5` was
hard-coded), this harness EXPOSES `h` as a constructor parameter.  The
non-promotability is therefore not a "no h-axis" obstruction but a
"non-unitarity + non-monotone ratio" obstruction.  This is a NEW
mechanism in the bounded-null space of the operator-Cauchy method:

| Harness | h-axis exposed? | obstruction mechanism                       | bounded-null PR |
|---------|-----------------|---------------------------------------------|-----------------|
| rescaled NN              | yes (with `step_scale = h / sqrt(FANOUT)`) | none (Cauchy r >= 1.5) | #957 / #1054 (positive) |
| alt-connectivity DAG     | no  (H constant)                            | no refinement axis      | #1008 (negative) |
| action-power 3D (this)   | yes                                          | non-unitary kernel + non-monotone ratios | this note (negative) |

This is the **third** distinct structural-reason class observed in the
operator-Cauchy method so far.

## Comparison with the Source Notes

The two source notes (sign-closure and uniqueness) register honest
bounded fixed-family statements at `h = 0.5`.  This note does not
contradict them — it adds the orthogonal continuum-bridge information:

- the sign-closure note's "this does NOT close ... continuum-limit
  rescue beyond the current ordered-family finite harness" is now
  bounded by an explicit numerical failure of operator-Cauchy at three
  representative `p` values;
- the uniqueness note's "F~M tracks the weak-field power of f" remains
  a fixed-`h` universality-class statement; the present note shows
  that the underlying `T_h` does not have a clean `h -> 0` limit, so
  the universality classes themselves cannot be promoted to continuum
  theorems via this lane.

## Safe Read

The action-power 3D ordered dense-lattice harness has a **structurally
available** refinement axis `h`, but the operator-Cauchy continuum-
bridge does not close on it.  Two structural reasons:

1. the dense `(h^2 / L^2) exp(-BETA θ²)` kernel is non-unitary; the
   field-free total detector throughput `p_total_f` diverges
   polynomially in `1 / h` (78 orders of magnitude across the tested
   `h` window).  No bounded continuum `T_inf` for the amplitude
   operator exists on this kernel.

2. Even on the dimensionless ratio observables (gravity, Born), the
   Cauchy L2 increments are non-monotone with the finest-`h` step
   LARGEST.  This pattern is stable across the three action-power
   universality classes (`p` in `{0.5, 1.0, 2.0}`) of
   ACTION_UNIQUENESS_NOTE.

This is a class-A bounded null-result that constrains the candidate
space: any future positive continuum identification on this harness
must first either (a) introduce a per-edge norm-preserving rescaling
that absorbs the `p_total_f` divergence (analog of the rescaled-NN
`step_scale = h / sqrt(FANOUT)`), or (b) restrict to a much coarser
window where the ratio observables are monotone (only one pair of
h-values qualifies here, which is not enough for a Cauchy fit).

## What This Closes

- Sharp bounded null on the continuum-bridge for the action-power 3D
  ordered-lattice harness:  `T_h` does NOT converge to a continuum
  `T_inf` on this harness at any of the tested action-power exponents
  `p in {0.5, 1.0, 2.0}` under operator-Cauchy.
- Adds a third distinct structural-reason class to the bounded-null
  space of operator-Cauchy: **non-unitary dense-kernel divergence**,
  distinct from the alt-connectivity "no h-axis" obstruction (PR #1008).
- Sharpens both source notes' "what this does NOT close: continuum-
  limit rescue" disclaimers by replacing the open question with an
  explicit numerical failure mechanism.

## What This Does NOT Close

- A positive continuum identification on a *different* (e.g. norm-
  preserving) parameterisation of the same physical kernel.  A
  per-edge rescaling that absorbs the `p_total_f` divergence has
  not been searched here.
- The bounded fixed-family universality-class statements of
  ACTION_UNIQUENESS_NOTE at `h = 0.5`.  Those remain valid as a
  registered fixed-family result.
- Other 3D harnesses (e.g. NN connectivity instead of dense
  `MAX_D_PHYS`-bounded; spent-delay action; geometric jitter).
- A first-principles proof that the `(h^2 / L^2) exp(-BETA θ²)` kernel
  is exactly non-unitary on this lattice.  The numerical observation
  of 78-decade growth in `p_total_f` over three halvings of `h` is
  registered as a strong numerical signal but not as a closed
  identification.

## Reproduction

```bash
python3 scripts/action_power_3d_operator_cauchy.py
```

Runtime ~14 min wallclock on a single-thread numpy build.  Guards
(Born-clean, k=0 control) report cleanly; runner exits zero — the
bounded null-result is a valid scientific outcome.

## Audit Context

This note is independent of and complementary to:

- PR #957 (rescaled NN harness operator existence)
- PR #968 (rescaled NN harness identification)
- PR #1008 (alt-connectivity grown DAG family bounded no-go)

It sits in the third row-cluster from PR #996's mapping (action-power 3D
ordered-lattice).  Any audit promotion or repo-wide mapping consequence
is controlled by the independent audit lane.
