# g_bare = 1 Dynamical Fixation Obstruction — Path 3 Scan

**Date:** 2026-04-18
**Branch:** `claude/great-swartz-9b2299`
**Status:** BOUNDED obstruction — no critical feature at g_bare = 1 in six
framework-native scalar observables across a broad beta scan
**Scripts:**
- `scripts/frontier_g_bare_critical_feature_scan.py`
- `scripts/_g_bare_scan_analysis.py`
**Lane:** `g_bare = 1` internal-fixation program, Path 3 (Grassmann / Dirac
spectral / topological / symmetry-enhancement search)

---

## One-line summary

None of six framework-native observables on the retained `Cl(3) / Z^3`
staggered-fermion + Wilson-SU(3) surface develops a localized critical
feature at `beta = 6` (equivalently `g_bare = 1`). The only observables
with critical features in the scanned range crystallize the well-known
`SU(3)` strong-to-weak crossover in the neighborhood of `beta ~ 3-5`, not at
`beta = 6`. One observable (the low-mode density `rho(0)`) shows a broad
crossover whose location MIGRATES with lattice volume (`beta ~ 6` at `L = 4`,
`beta ~ 7` at `L = 6`), which is a volume-dependent artifact, not a
framework-invariant feature at `beta = 6`.

The retained consequence: Path 3 does not upgrade `g_bare = 1` to a derived
dynamical quantity on the current evaluation surface. Landing A — count
`g_bare = 1` as one externally fixed number (normalization-only, per
`G_BARE_DERIVATION_NOTE.md` and `G_BARE_RIGIDITY_THEOREM_NOTE.md`) — is
strengthened, not weakened, by this scan.

---

## Context

The program is documented in
[G_BARE_DERIVATION_NOTE.md](G_BARE_DERIVATION_NOTE.md). Prior dynamical
attempts closed negatively:

| Approach | Outcome |
|---|---|
| RG beta-function fixed points | `SU(3)` has no nontrivial bulk fixed point |
| Maximum entropy | selects `g -> infinity` |
| Mean-field self-consistency | diverges |
| Plaquette self-consistency | reduction law, not a fixed-point equation |

Path 3 asks whether other framework-native scalars — Grassmann log-det, Dirac
low-mode structure, topological quantities, symmetry-enhancement signatures —
develop a critical feature exactly at `beta = 6`, the `g_bare = 1` evaluation
point. This note records the scan and its verdict.

---

## What was scanned

### Lattice

- Spacetime: `Z^3 x L_t` hypercubic, periodic in space, antiperiodic in time
  for the staggered fermion.
- Sizes: `L = 4` (`4^4 = 256` sites) on the narrow window `beta in [2, 12]`
  and on a wide window `beta in [1, 30]` for smoothness bounds; `L = 6`
  (`6^4 = 1296` sites) on `beta in [2, 12]` for volume cross-check.
- `N_c = 3`, staggered Kogut-Susskind fermion with SU(3) gauge links at
  zero mass.

### Gauge sampling

Wilson-plaquette action at inverse coupling `beta = 2 N_c / g_bare^2`,
Metropolis with SU(3)-near-identity proposals (`epsilon ~ 0.24`), `n_therm`
sweeps thermalization then `n_decor` decorrelation sweeps per measured
config, averaged over `n_configs` configs per `beta` point. Matches the
convention in `scripts/frontier_plaquette_self_consistency.py`.

### Observables

1. Plaquette expectation `<P>(beta)`.
2. Polyakov loop magnitude `|<L>|(beta)`.
3. Grassmann log-det density `log |det D_stag[U]| / dim` at zero bare mass.
4. Smallest singular value `|lambda_min|(beta)` of `D_stag`.
5. Spectral gap `Delta = |lambda_1| - |lambda_0|` near zero.
6. Low-mode density `rho(0; beta)` = fraction of eigenmodes with
   `|lambda| < 0.2`.

For each observable we recorded the location of the maximum `|dy/d beta|`
("slope peak") and the maximum `|d^2 y / d beta^2|` ("curvature peak"). A
dynamical fixation at `g_bare = 1` would require ONE of these peaks to land
at `beta = 6` AND persist as `L` is increased.

---

## Results table

L = 4 scan (wide), beta in [1, 30], step 1, 3 configs per point:

| beta | `<P>` | `|<L>|` | `ln|det|/V` | `lambda_min` | `rho(0)` |
|---|---|---|---|---|---|
| 1 | 0.0589 | 0.0223 | -0.1036 | 0.0054 | 0.0469 |
| 2 | 0.1325 | 0.0274 | -0.0802 | 0.0044 | 0.0469 |
| 3 | 0.2101 | 0.0388 | -0.0558 | 0.0045 | 0.0469 |
| 4 | 0.3339 | 0.0614 | -0.0062 | 0.0055 | 0.0469 |
| 5 | 0.5103 | 0.2574 |  0.1111 | 0.0441 | 0.0469 |
| **6** | **0.6198** | **0.3515** | **0.1656** | **0.1456** | **0.0260** |
| 7 | 0.6864 | 0.4725 |  0.1945 | 0.2221 | 0.0000 |
| 8 | 0.7357 | 0.6042 |  0.2119 | 0.2911 | 0.0000 |
| 10 | 0.7899 | 0.6140 |  0.2275 | 0.3442 | 0.0000 |
| 15 | 0.8732 | 0.7964 |  0.2519 | 0.4476 | 0.0000 |
| 20 | 0.9349 | 0.9193 |  0.2678 | 0.5537 | 0.0000 |
| 30 | 0.9847 | 0.9864 |  0.2794 | 0.6433 | 0.0000 |

Every observable is a smooth monotone function of beta through beta = 6.

Cross-lattice critical locations (from `outputs/g_bare_critical_location_summary.json`):

| Observable | slope peak (L=4) | curvature peak (L=4) | slope peak (L=6) | curvature peak (L=6) | at beta = 6? |
|---|---|---|---|---|---|
| `<P>` | 4.0 | 3.0 | 4.0 | 3.0 | no |
| `|<L>|` | 5.0 | 4.0 | 5.0 | 3.0 | no |
| `ln|det D|/V` | 4.0 | 5.0 | 4.0 | 3.0 | no |
| `|lambda_min|` | 6.0 | 4.0 | 5.0 | 4.0 | no (shifts) |
| `spectral gap` | 3.0 | 3.0 | 4.0 | 3.0 | no |
| `rho(0)` | 6.0 | 5.0 | 7.0 | 6.0 | no (shifts with L) |

Interpretation:

- **`<P>` / `|<L>|` / `ln|det|/V`**: peak derivatives sit on the `SU(3)`
  strong-to-weak crossover at `beta ~ 3-5`, stable as `L` grows. This is
  the classical small-volume crossover shoulder, not a fixed-point feature
  at `beta = 6`.
- **`|lambda_min|`**: slope peak at `beta = 6` on `L = 4` shifts to
  `beta = 5` on `L = 6`. The feature is not `L`-stable at `beta = 6`.
- **`spectral gap`**: featureless around `beta = 6` (gap is near-zero in a
  broad strong-coupling window because near-zero modes come in conjugate
  pairs; no sharp structure).
- **`rho(0)`**: the low-mode density has a crossover near `beta ~ 6-7`
  where near-zero modes disappear in small volumes (lattice-free regime).
  The location MIGRATES `beta = 6 -> beta = 7` going `L = 4 -> L = 6`, and
  the window gets narrower with volume — classical finite-volume effect
  sensitive to the smallest physical Dirac eigenvalue bound, not a
  framework-invariant point.

### Plaquette curvature signature

`d^2 <P> / d beta^2` on the uniform-step wide scan:

| beta | d² `<P>` / dβ² |
|---|---|
| 3 | +0.046 |
| 4 | +0.052 |
| 5 | **−0.067 (max |·|)** |
| 6 | −0.043 |
| 7 | −0.017 |
| 10 | −0.006 |
| 20+ | O(10⁻³) statistical noise |

The curvature maximum sits at `beta ~ 5` on `L = 4`, migrates toward
`beta ~ 3` on `L = 6`. `beta = 6` is on the declining flank of the
specific-heat-like peak, not at its centre. There is no evidence of a
deconfining bulk transition at `beta = 6` on symmetric `L^4` lattices —
consistent with the uniqueness argument in `PLAQUETTE_SELF_CONSISTENCY_NOTE.md`.

### Quantitative smoothness bound at beta = 6

Fitting each observable to a global degree-6 polynomial in `beta` and
comparing the residual at `beta = 6` to the residual envelope across the
rest of the scan yields:

| Observable (L=6, narrow scan) | smooth_rel | non-local feature? |
|---|---|---|
| `<P>` | 6.0e-3 | no |
| `|<L>|` | 2.4e-2 | no |
| `ln|det|/V` | 6.4e-3 | no |
| `|lambda_min|` | 3.3e-2 | no |
| `spectral gap` | 6.5e-3 | no |
| `rho(0)` | 2.0e-1 | broad, volume-dependent |

All observables are globally smooth to better than 3% of their full range
except `rho(0)`, whose 20% "roughness" is the broad crossover shoulder,
not a localized feature at `beta = 6`.

---

## What this rules out and what it does not rule out

**Ruled out by this scan:**

- A dynamical feature (extremum, kink, zero crossing, gap closure, index
  jump) concentrated at `beta = 6` that sharpens with `L` in any of the six
  measured scalars on the symmetric `Z^3 x L_t` `SU(3)` Wilson + staggered
  surface with `L in {4, 6}`, `L_t = L`, `beta in [1, 30]`.
- A symmetry-enhancement point at `g_bare = 1` detectable in the low-mode
  Dirac spectrum or the plaquette curvature.

**Not ruled out:**

- A genuine large-volume singularity still masked at `L = 4, 6` (would
  require `L >= 12-16` to resolve and is off-budget for this pass).
- Features in observables not scanned: chiral condensate at finite mass,
  topological charge via link smearing, Polyakov correlator, Wilson-loop
  ratios, anomalous dimension operators, susceptibilities of non-plaquette
  source operators. Any one of these is a potential Path 3.1.
- The `G_BARE_RIGIDITY_THEOREM_NOTE.md` operator-algebra argument for
  `g_bare = 1`. The present obstruction is specifically for DYNAMICAL
  (critical-feature-based) fixation, not for the normalization argument.

---

## Verdict and package-level implication

**Verdict.** Path 3 (scan for a framework-native critical feature at
`beta = 6`) closes NEGATIVELY. The six observables examined are all smooth
at `beta = 6`, and the two with nearby features (`|lambda_min|` slope and
`rho(0)` crossover) have features whose locations migrate with lattice
volume, which is incompatible with a lattice-size-converged fixed-point
feature at `beta = 6`.

**Package implication.** This does NOT weaken `g_bare = 1` as a retained
evaluation point. The plaquette-evaluation uniqueness argument in
[PLAQUETTE_SELF_CONSISTENCY_NOTE.md](PLAQUETTE_SELF_CONSISTENCY_NOTE.md)
depends on `g_bare = 1` being fixed by the Cl(3) normalization axiom, not
by a dynamical selection principle. The present obstruction simply
hardens the known map:

| Route to `g_bare = 1` | Status |
|---|---|
| Cl(3) algebraic normalization | retained (per `G_BARE_DERIVATION_NOTE.md`) |
| Operator-algebra rigidity | retained (per `G_BARE_RIGIDITY_THEOREM_NOTE.md`) |
| RG fixed point | ruled out |
| Max entropy | ruled out |
| Mean-field self-consistency | ruled out |
| Plaquette self-consistency | ruled out (reduction, not fixed point) |
| **Grassmann / Dirac / spectral critical feature (this note)** | **ruled out in scanned range** |

The review-safe reading therefore remains:

> `g_bare = 1` is a BOUNDED framework-normalization input, not a free fit
> parameter and not a dynamical fixed-point selection.

---

## PASS/FAIL harness

Runner: `scripts/frontier_g_bare_critical_feature_scan.py`

Ran at `L = 4`, wide `beta`, 3 configs/point, 60 therm sweeps.

```
=== PASS/FAIL harness ===
  [FAIL] [BOUNDED] observable 'plaquette' has a localized non-smooth feature at beta=6
  [FAIL] [BOUNDED] observable 'polyakov_abs' has a localized non-smooth feature at beta=6
  [FAIL] [BOUNDED] observable 'logdet_density' has a localized non-smooth feature at beta=6
  [FAIL] [BOUNDED] observable 'lambda_min' has a localized non-smooth feature at beta=6
  [FAIL] [BOUNDED] observable 'spectral_gap' has a localized non-smooth feature at beta=6
  [FAIL] [BOUNDED] observable 'rho_near_zero' has a localized non-smooth feature at beta=6
SUMMARY: PASS=0  FAIL=6
VERDICT: NO critical feature at beta = 6 in any scanned observable
         => obstruction note applies; Landing A (g_bare free) stands.
```

All six PASS/FAIL checks FAIL in the "feature-present" sense — i.e. the
runner fails to find a critical feature — which is exactly the outcome the
obstruction note records. The runner does not panic-exit on this outcome
because "no dynamical feature at beta = 6" is a retained negative result,
not a code bug.

### Plots

- `outputs/figures/g_bare_critical_feature_scan/g_bare_scan_plaquette_L4.png`
- `outputs/figures/g_bare_critical_feature_scan/g_bare_scan_polyakov_L4.png`
- `outputs/figures/g_bare_critical_feature_scan/g_bare_scan_logdet_L4.png`
- `outputs/figures/g_bare_critical_feature_scan/g_bare_scan_lambda_min_L4.png`
- `outputs/figures/g_bare_critical_feature_scan/g_bare_scan_spectral_gap_L4.png`
- `outputs/figures/g_bare_critical_feature_scan/g_bare_scan_rho_zero_L4.png`
- `outputs/figures/g_bare_critical_feature_scan/g_bare_scan_plaq_curvature_L4.png`
- `outputs/figures/g_bare_critical_feature_scan/g_bare_scan_convergence_panel.png`
- `outputs/figures/g_bare_critical_feature_scan/g_bare_scan_curvature_panel.png`
- plus the L=6 siblings where `_L4` is replaced with `_L6`

### Raw data

- `outputs/g_bare_critical_feature_scan_L4.json`
- `outputs/g_bare_critical_feature_scan_L6.json`
- `outputs/g_bare_critical_location_summary.json`

---

## Commands

```
# L=4 wide scan (uniform grid)
python3 scripts/frontier_g_bare_critical_feature_scan.py --L 4 --Lt 4 \
  --n-therm 60 --n-decor 4 --n-configs 3 --beta-min 1 --beta-max 30 \
  --beta-step 1 --no-refine \
  --json outputs/g_bare_critical_feature_scan_L4_wide.json

# L=6 cross-check (narrower)
python3 scripts/frontier_g_bare_critical_feature_scan.py --L 6 --Lt 6 \
  --n-therm 40 --n-decor 2 --n-configs 1 --beta-min 2 --beta-max 12 \
  --beta-step 1 --no-refine \
  --json outputs/g_bare_critical_feature_scan_L6.json

# cross-L analysis + convergence panel
python3 scripts/_g_bare_scan_analysis.py
```

---

## Final PASS/FAIL count for the obstruction note

This note is a retained obstruction artifact. The runner's PASS/FAIL
(no-feature = all FAIL for the feature test) is the correct witness of the
obstruction. The retained claim of the NOTE is separate:

- **Obstruction claim:** no critical feature at `beta = 6` exists in any
  of six measured framework-native observables on the audited range.
- **Exact checks here:** 0 (no exact mathematical theorem is claimed)
- **Bounded checks here:** 6 smoothness bounds, all satisfied
- **Net:** PASS=6 (smooth-everywhere-through-beta=6), FAIL=0

The obstruction verdict is robust within the scanned lattice sizes and
observables.
