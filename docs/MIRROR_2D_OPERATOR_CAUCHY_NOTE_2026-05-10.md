# 2D Mirror Operator-Cauchy Continuum-Bridge Probe (sharp bounded null)

**Date:** 2026-05-10
**Status:** sharp bounded null-result — the operator-Cauchy continuum-bridge
method does NOT extend cleanly to the exact 2D mirror harness on the
layer-count refinement axis. The 5-dim observable vector is non-Cauchy in N
and four of five components are non-monotone in N. The structural reason
is that the 2D mirror harness has no spacing-refinement knob: increasing
N adds layers at fixed physical density and rescales the chokepoint /
gravity-layer indices, so successive N sample different geometric
configurations rather than refining a single one.
**Primary runner (load-bearing):** [`scripts/mirror_2d_operator_cauchy.py`](../scripts/mirror_2d_operator_cauchy.py)
**Primary runner cached log:** [`logs/runner-cache/mirror_2d_operator_cauchy.txt`](../logs/runner-cache/mirror_2d_operator_cauchy.txt)
**Companion artifact:** [`docs/MIRROR_2D_GRAVITY_LAW_NOTE.md`](MIRROR_2D_GRAVITY_LAW_NOTE.md)
(the pre-existing bounded null on gravity-side power-law fits; this note
structurally diagnoses that bounded null).

## Context

The rescaled NN harness closed a long chain of operator-Cauchy continuum-
bridge results across 16 PRs (existence #957, geodesic identification
#968, magnitude / phase closed forms #1003 and #1007, parameter
universality #1054, full kernel #1055, NNLO alpha-residual #1056). A
parallel attempt on the alt-connectivity grown DAG family (#1008) closed
as a sharp null because that harness has no h-like refinement axis.

This note records the analogous probe on the **2D mirror harness** retained
in `scripts/mirror_2d_validation.py` (the `gen_2d_mirror` family).

## Harness

`gen_2d_mirror(nl, npl_half, yr, cr, seed)`:

- `nl`: number of layers along the propagation axis
- `npl_half = 12`: half-density of nodes per non-source layer (24 total per
  layer, mirrored across `y = 0`)
- `yr = 10.0`: transverse half-extent of the random node ordinates
- `cr = 2.5`: connect radius (fixed physical units)
- chokepoint at layer `bl = nl // 3` (single-layer connectivity at that
  layer; two-layer connectivity elsewhere)

All four of `npl_half`, `yr`, `cr`, and the chokepoint relative position
(`1/3`) are fixed. The only refinement knob exposed is `nl`. Increasing
`nl` adds layers at fixed transverse density.

## Refinement-axis decision

The 2D mirror harness has NO clean h-like spacing-refinement parameter:

- the inter-layer spacing along x is unit (lattice convention), not a knob
- `npl_half` controls density rather than spacing; refining it would
  rebuild the harness rather than refine an existing one
- `cr` is in fixed physical units (a smoothing-radius analog)

We therefore test operator-Cauchy along the only available refinement axis,
the layer count `N -> infinity`, on a geometric-ish grid
`N in {25, 40, 60, 80, 100, 150, 200}`. The first five values reproduce
the primary-runner grid from MIRROR_2D_GRAVITY_LAW_NOTE; 150 and 200
extend the lane to probe whether the non-monotonicity in observables damps
at larger N.

## Observable basis

Five framework observables matching the existing
`mirror_2d_validation.py` runner, averaged over 8 seeds and over the
k-band `{3.0, 5.0, 7.0}`:

| symbol | meaning |
|--------|---------|
| `MI` | slit-detector mutual information (bits) |
| `decoh` | `1 - pur_min`, branch density-matrix decoherence |
| `dTV` | total-variation distance between branch outcome distributions |
| `gravity` | signed Born-weighted detector centroid shift under a mass layer |
| `born` | corrected three-slit Sorkin `|I_3| / P` (Born floor) |

The vec(N) is the 5-tuple of those quantities at fixed N. Cauchy is tested
on the pairwise increments `||vec(N_i) - vec(N_{i+1})||_2`.

## Result

Seed-mean observable table (from
`logs/runner-cache/mirror_2d_operator_cauchy.txt`):

| N | MI | decoh | dTV | gravity | born |
|---|----|-------|-----|---------|------|
| 25 | 5.02e-01 | 3.03e-01 | 6.00e-01 | +2.71 | 5.87e-16 |
| 40 | 5.37e-01 | 3.01e-01 | 6.22e-01 | +3.89 | 9.07e-16 |
| 60 | 7.56e-01 | 4.42e-01 | 8.57e-01 | +2.57 | 1.19e-15 |
| 80 | 5.65e-01 | 3.46e-01 | 6.74e-01 | +3.41 | 1.68e-15 |
| 100 | 3.46e-01 | 2.87e-01 | 5.46e-01 | +1.86 | 2.19e-15 |
| 150 | 4.90e-01 | 3.33e-01 | 6.25e-01 | +3.27 | 2.53e-15 |
| 200 | 3.08e-01 | 2.40e-01 | 4.72e-01 | +3.80 | 2.49e-15 |

Joint Cauchy fit on the 5-dim vector:

| N1 -> N2 | `||vec(N1) - vec(N2)||_2` |
|---|---|
| 25 -> 40 | 1.176 |
| 40 -> 60 | 1.366 |
| 60 -> 80 | 0.884 |
| 80 -> 100 | 1.566 |
| 100 -> 150 | 1.415 |
| 150 -> 200 | 0.587 |

Power-law fit:

- `||vec(N_i) - vec(N_{i+1})||_2 ~ C * N^r`
- `r = -0.249`, `C = 3.27`, `R^2 = 0.173`
- Cauchy gate `r < -0.4 AND R^2 >= 0.85`: **FAIL**

Per-component decay rates:

| observable | r | C | R^2 | Cauchy? |
|------------|---|---|-----|---------|
| MI | +0.686 | 7.25e-3 | 0.355 | FAIL |
| decoh | +1.556 | 4.96e-5 | 0.349 | FAIL |
| dTV | +0.626 | 7.03e-3 | 0.200 | FAIL |
| gravity | -0.286 | 3.70 | 0.190 | FAIL |
| born | -0.806 | 8.65e-15 | 0.287 | FAIL |

Per-component monotonicity in N:

| observable | monotonicity |
|------------|--------------|
| MI | non-monotone (peak at N=60) |
| decoh | non-monotone (peak at N=60) |
| dTV | non-monotone (peak at N=60) |
| gravity | non-monotone (oscillates) |
| born | inc (at the linear-propagator precision floor; rises from 6e-16 to 4e-15 with N, reflecting floating-point accumulation rather than physical signal) |

## Guards

- Born floor: max `|I_3| / P` across all (N, seed) pairs is `4.21e-15`,
  well below any non-trivial Born violation. The linear propagator is
  intact across the entire sweep.
- Seed success: 8/8 at N=25, 40, 60; 7/8 at N=80, 150, 200; 5/8 at N=100.
  All N have at least 5 surviving seeds; the seed-mean entries are not
  data-starved.

## Verdict

**Sharp bounded null.** The 2D mirror harness does NOT admit a clean
operator-Cauchy continuum bridge on the layer-count refinement axis. The
joint 5-dim Cauchy fit has `r = -0.249, R^2 = 0.17`, both far below the
PASS gate. Zero of five components pass the per-component Cauchy gate.

## Structural diagnosis

The failure has a clean structural reading:

1. **No spacing-refinement knob.** `npl_half`, `yr`, `cr` are all held
   fixed; refining them would build a different harness, not the same
   harness at finer resolution. The only available refinement axis is
   adding layers at FIXED physical density.

2. **The chokepoint position changes with N.** The chokepoint sits at
   layer `nl // 3`. As N goes 25 -> 40 -> 60 -> ... -> 200, the chokepoint
   moves from layer 8 to 13 to 20 to 26 to 33 to 50 to 66. Its physical
   distance to source and detector grows linearly with N. The
   path-integral saddles around the chokepoint do not have a fixed
   continuum target; each N samples a different geometric configuration.

3. **Gravity-layer index moves with N.** `grav_layer = 2 * nl // 3` moves
   from 16 (at N=25) to 132 (at N=200). The mass-source position relative
   to detector is rescaled at every N. This is the structural inverse of
   what a continuum-bridge refinement needs: the underlying physical
   geometry must converge, not walk.

4. **The 5-dim observable vector samples a family of harnesses, not a
   single harness refining.** This is structurally distinct from the
   rescaled NN harness, which keeps the physical domain fixed and refines
   the edge spacing `h`. There, vec(h) refines the SAME observable on the
   SAME geometry. Here, vec(N) reports the observable on a DIFFERENT
   geometry at each N.

5. **The non-monotonicity at N=60 is geometric.** MI/decoh/dTV all peak at
   N=60 because that geometric configuration happens to maximize slit-
   barrier interference. Surrounding N values sample geometries with less
   interference. There is no continuum target this can converge to in the
   usual sense, because there is no continuum object being approximated.

## Reconciliation with MIRROR_2D_GRAVITY_LAW_NOTE

The pre-existing bounded null in
[`MIRROR_2D_GRAVITY_LAW_NOTE`](MIRROR_2D_GRAVITY_LAW_NOTE.md) reports

- gravity scaling `R^2 = 0.015` (weak)
- mass window `R^2 = 0.167` (weak)
- distance tail `R^2 = 0.075` (weak)

on the same harness over the same `N in {25, 40, 60, 80, 100}` grid. Those
weak fits are now structurally explained: they are not a measurement-noise
issue and not a window-choice issue. They reflect the harness's lack of a
single continuum target. The operator-Cauchy probe formalizes the
structural reason: vec(N) does not converge in N because the underlying
geometric configuration changes with N.

This extends the lane to `N=150` and `N=200` and confirms that the bounded
null does not narrow at larger N; if anything, the joint increment
`||vec(N_i) - vec(N_{i+1})||_2` stays O(1) across the entire sweep, with
no power-law decay.

## Comparison with the alt-connectivity null (#1008)

PR #1008 closed a structurally similar null on the alt-connectivity grown
DAG family. The mechanism there was hardcoded module-scope `H` and an
intrinsically stochastic construction with no spacing-refinement knob;
the adapted ensemble-Cauchy substitute also failed.

The 2D mirror null here is closer in shape but has a different structural
locus:

| family | refinement axis tried | failure mode |
|--------|----------------------|---------------|
| rescaled NN (#957 + chain) | spacing `h -> 0` | PASS (continuum bridge exists) |
| alt-connectivity (#1008) | seed ensemble `N_seeds -> infinity` | FAIL (seed-selective sign-orientation boundary) |
| 2D mirror (this note) | layer count `N -> infinity` | FAIL (geometry changes with N; no fixed continuum target) |

Both #1008 and this note land in the same bounded category: the
operator-Cauchy method requires a harness that exposes a refinement axis
along which a single physical configuration is approximated. Harnesses
without such an axis cannot host the bridge.

## What this note does NOT claim

- That the 2D mirror harness is scientifically useless. It remains a
  review-safe bounded coexistence pocket per MIRROR_2D_GRAVITY_LAW_NOTE.
- That no continuum bridge of any kind exists on a 2D-mirror-like
  construction. A redesigned 2D mirror family with a fixed physical
  domain and a refinable lattice spacing might admit one; that is a
  different harness, not this one.
- A negative theoretical statement about the existence of T_inf on the
  abstract concept of "the 2D mirror." Only the existing concrete
  harness `gen_2d_mirror` is scoped.

## What would close a positive 2D-mirror operator-Cauchy lane (future work)

A redesigned 2D mirror runner with:

1. A fixed physical domain `[0, L]` along the propagation axis, with
   layer count `N` and inter-layer spacing `h = L / N`.
2. Density `npl_half` scaled so node density per unit physical length is
   fixed: `npl_half(N) = const * N`.
3. Chokepoint and gravity layer pinned at fixed physical fractions of
   `L`, i.e., at layer indices `round(N / 3)` and `round(2 * N / 3)`.
4. Connect radius `cr` scaled with `h` so it represents a fixed physical
   smoothing length.

This redesigned harness would have N as a legitimate spacing-refinement
axis (`h -> 0` as `N -> infinity` with `L` and `cr` fixed). The
operator-Cauchy probe would then be testable. The present runner does
not do this; it tests the existing harness as it stands and records the
structural null.

## Registered runner artifacts

- Primary runner: [`scripts/mirror_2d_operator_cauchy.py`](../scripts/mirror_2d_operator_cauchy.py)
- Primary runner cache: [`logs/runner-cache/mirror_2d_operator_cauchy.txt`](../logs/runner-cache/mirror_2d_operator_cauchy.txt)
  (registered cached stdout; exit_code=0; 42 s wallclock; runner
  sha256 = `1ee1832498baae71bd10e9cbfcf1f33407ea8f320aa04fb746f0e78e89194bff`)
- Companion: [`docs/MIRROR_2D_GRAVITY_LAW_NOTE.md`](MIRROR_2D_GRAVITY_LAW_NOTE.md)
  (the pre-existing bounded null this note structurally explains).
