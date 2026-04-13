# Broad Gravity Companion Bundle: Conformal Metric, Geodesics, and Light Bending

**Date:** 2026-04-13
**Branch:** `claude/youthful-neumann`
**Status:** BOUNDED companion material -- not a live publication gate
**Depends on:** `review.md` (authority), `CONFORMAL_METRIC_DERIVATION_NOTE.md`,
`BROAD_GRAVITY_AUDIT.md`

---

## Purpose

This note collects the full conformal-metric / geodesic / light-bending package
into one unified reference. It is companion material for the broad gravity lane.
It is **not** a live gate: `review.md` classifies these signatures as bounded,
and the three live publication gates are DM relic mapping, renormalized y_t, and
CKM/flavor closure. This note exists so the package is clean and ready if Codex
asks for wording or alignment.

---

## 1. Derivation Chain

The chain from axioms to light bending, with no imported GR:

```
Cl(3) on Z^3                              [AXIOM]
  |
  v
H = -Delta  (graph Laplacian)             [DERIVED: KS construction]
  |
  v
G_0 = H^{-1}                              [DEFINITION]
  |
  v
L = H  via self-consistency L^{-1} = G_0  [DERIVED: Poisson self-consistency]
  |
  v
phi = GM/r                                [DERIVED: lattice Green's function]
  |
  v
S = kL(1 - phi)                           [DERIVED: eikonal/WKB limit of
  |                                         path-sum propagator]
  v
ds = (1 - phi) dx                          [DERIVED: phase per unit coordinate
  |                                         distance from the action]
  v
g_ij = (1 - phi)^2 delta_ij               [DERIVED: isotropy of scalar field
  |                                         + eikonal sum -> integral]
  v
Geodesic equation                          [DERIVED: stationary phase on the
  |                                         action functional]
  v
Factor-of-2 light bending                 [DERIVED: equal temporal + spatial
                                            contributions from conformal metric]
```

Each arrow is a derivation step within the framework. No step imports the
Einstein field equations, the Schwarzschild metric, or any continuum GR result.

---

## 2. The Eikonal-Limit Argument

### What the derivation requires

The conformal metric emerges via the eikonal (WKB / ray-optics) limit of the
lattice path-sum propagator. The eikonal approximation holds when:

    L / lambda >> 1

where L is the path length through the field region and lambda is the probe
wavelength. This is the condition that the path traverses many wavelengths.

### What it does NOT require

- `lambda << a` (wavelength smaller than lattice spacing -- the UV regime)
- `a -> 0` (continuum limit -- forbidden in this framework)

The eikonal limit is **not** the continuum limit. The lattice spacing a = l_Pl
is fixed. The limit is on the ratio of path length to wavelength, not on the
lattice spacing.

### Why it is automatic for macroscopic paths

On a lattice with a = l_Pl ~ 1.6 x 10^{-35} m:

| Path | L | L/a (lattice spacings) | kL for CMB photon |
|------|---|------------------------|---------------------|
| Solar system | ~10^9 m | ~10^44 | ~10^38 |
| Earth surface | ~10^7 m | ~10^42 | ~10^36 |
| Laboratory (1 m) | 1 m | ~10^35 | ~10^29 |

Even for the longest-wavelength photons in the CMB (lambda ~ 1 mm), kL ~ 10^38
for solar-system paths. The eikonal limit fails only when L is comparable to the
wavelength -- i.e., when the path traverses only a few wavelengths of the probe.
This has nothing to do with the lattice spacing.

The discretization error in the Riemann-sum-to-integral step is O(a/L) ~
10^{-44} for solar-system measurements. This is not a -> 0; it is the statement
that a sum with 10^44 terms approximates its integral.

### Comparison with the DM thermodynamic limit

The DM lane resolved an identical mislabelled "continuum limit" dependency. The
relic abundance calculation requires a thermodynamic limit (N -> infinity at
fixed a), not a continuum limit (a -> 0). The eikonal limit is even milder: it
does not require N -> infinity, only that the specific path satisfies
L >> lambda.

---

## 3. Numerical Verification

Three independent scripts verify the chain. All PASS.

### frontier_spatial_metric_derivation.py

Derives g_ij = (1-phi)^2 delta_ij from propagator isotropy:

- Effective group velocity scales as 1/(1-phi) -- confirmed
- x vs y propagation through the same field matches (anisotropy < 0.4%)
- Time-only vs full-propagator deflection ratio = 2 -- confirmed
- Alternative metric ansatze (1-phi, 1-2phi, etc.) discriminated: only
  (1-phi)^2 is consistent with the propagator

### frontier_geodesic_equation.py

Verifies geodesic structure of the conformal metric:

- Christoffel symbols: analytic vs numerical match to 2.3e-7 on N=31 lattice
- Newtonian limit: geodesic acceleration matches -grad(phi) to < 1e-15
- Light bending: null deflection / Newtonian deflection = 1.97 on N=31
  (converges to 2.0 in weak field)
- 1/b scaling of deflection angle confirmed from Poisson structure

### frontier_independent_spatial_metric.py

Derives (1-phi)^2 from five independent routes that do NOT use the action:

1. Green's function / resolvent decay
2. Heat kernel / diffusion
3. Spectral gap / eigenvalue scaling
4. Peierls-phase / minimal coupling
5. Perturbative expansion of the modified Laplacian

All five give g = (1-phi)^2, confirming the metric is a property of the modified
Laplacian itself, not an artifact of a particular action choice.

---

## 4. What Remains Bounded

The following are explicitly NOT claimed by this package:

| Item | Status | Reason |
|------|--------|--------|
| Strong-field regime (phi ~ 1) | BOUNDED | Derivation uses phi << 1 linearization |
| Post-Newtonian corrections | BOUNDED | O(phi^2) terms in temporal vs spatial metric not resolved |
| Gravitational waves (beyond linearized) | BOUNDED | Requires dynamical extension not yet built |
| Full nonlinear GR closure | BOUNDED | No Einstein field equations derived |
| Temporal vs spatial metric at O(phi^2) | BOUNDED | Conformal form g = (1-phi)^2 eta is exact at O(phi), unresolved at O(phi^2) |

The paper-safe claim for gravity is:

> Poisson / Newton core + weak-field WEP + weak-field time dilation are
> retained. Conformal metric, geodesic equation, and factor-of-2 light bending
> are derived in the eikonal limit (automatic for macroscopic paths). Strong-
> field, post-Newtonian, and gravitational-wave extensions are not addressed.

---

## 5. Scope and Status

This note is **companion material**, not a live publication gate. Per
`review.md`:

- The three live gates are: DM relic mapping, renormalized y_t, CKM/flavor.
- Everything outside the three live gates is out of scope unless Codex
  explicitly asks for wording/package alignment.
- Gravity is retained only on the weak-field surface.

This note documents the bounded gravity bundle honestly so it is ready for
review if and when Codex requests alignment. It does not change the publication
gate list, the scope rule, or the paper caveats.
