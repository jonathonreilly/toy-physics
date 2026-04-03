# Derivation: Decoherence Exponent vs Dimension

**Date:** 2026-04-03
**Status:** Semi-analytical argument; useful as a frontier hypothesis, not yet
an established theorem.

## The observation

The decoherence ceiling exponent alpha in (1-pur_min) ~ C × N^alpha
depends on the spatial dimension d:

| d_spatial | alpha (measured) | Config |
|-----------|-----------------|--------|
| 1 (2D graph) | -1.5 ± 0.5 | Uniform, various params |
| 2 (3D graph) | ~-0.7 | 3D modular (limited data) |
| 3 (4D graph) | -0.2 to -0.5 | 4D modular gap=3 |

## The argument

### Setup

Consider a DAG with N layers, M nodes per layer, d_spatial transverse
dimensions. The barrier is at layer N/3, with two slits (upper/lower
in the first transverse coordinate y).

Amplitude from slit A at detector node j is:

    ψ_A(j) = Σ_{paths p: A→j} w(p) × exp(i × phase(p))

where w(p) includes 1/L attenuation and directional measure.

### Step 1: Effective independent path count

The number of geometrically distinct paths from a slit to a detector
grows exponentially with depth: n_paths ~ (connectivity)^N.

But the EFFECTIVE number of independent contributions to the amplitude
at a detector is much smaller. Paths that pass through the same
intermediate nodes contribute correlated amplitudes.

The effective independent path count at a detector scales with the
"bottleneck width" — the number of independent channels between
barrier and detector. In d_spatial dimensions with M nodes per layer:

    n_eff ~ M^((d_spatial-1)/d_spatial)

This is because in d spatial dimensions, the "cross-section" of
independent channels scales as the (d-1)-dimensional surface area
of the beam, while the total node count scales as the d-dimensional
volume.

### Step 2: CLT convergence of overlap

The overlap between slit-A and slit-B detector distributions is:

    O = |Σ_j ψ_A*(j) ψ_B(j)|² / (Σ_j |ψ_A(j)|² × Σ_j |ψ_B(j)|²)

By CLT, when both slits contribute to many paths reaching each
detector, the per-detector amplitudes become correlated Gaussians.
The overlap approaches 1 at a rate determined by how quickly the
slit-specific structure is washed out.

The key parameter is the "slit separation at detector" — how
structurally different the slit-A and slit-B path distributions
are at the detector layer. On a graph with N layers and d_spatial
transverse dimensions:

- In 1 spatial dim: paths from both slits must pass through the
  same intermediate nodes (no room to go around). The distributions
  converge as the graph grows because all paths merge.

- In d spatial dims (d > 1): paths from different slits can take
  routes through different transverse dimensions, maintaining
  structural separation even as N grows.

### Step 3: Dimensional scaling

The rate of overlap convergence O → 1 is controlled by the
fraction of SHARED intermediate nodes between slit-A and slit-B
paths.

In d_spatial dimensions, the "mixing zone" where slit-A and slit-B
paths overlap has d_spatial-dimensional extent. The fraction of
detector-relevant paths that pass through the mixing zone scales as:

    f_mix ~ (mixing_width / total_width)^(d_spatial)

For uniform random graphs with connect_radius r and extent L:

    f_mix ~ (r/L)^(d_spatial)

The overlap converges as:

    1 - O ~ f_mix^N_eff ~ (r/L)^(d_spatial × N_eff)

Taking logs and approximating N_eff ~ N (linear in depth):

    alpha ~ -d_spatial × log(L/r) / log(N)

This is a ROUGH scaling argument, but it predicts:
- Higher d_spatial → smaller |alpha| (flatter exponent)
- Larger L/r (sparser graphs) → larger |alpha| (steeper)
- The exponent should scale approximately as 1/d_spatial

### Step 4: Comparison with data

| d_spatial | Predicted alpha (relative) | Measured alpha |
|-----------|--------------------------|----------------|
| 1 | baseline | -1.5 |
| 2 | ~1/2 × baseline | ~-0.7 |
| 3 | ~1/3 × baseline | -0.2 to -0.5 |

The prediction alpha ~ 1/d_spatial gives:
- d=1: -1.5 (baseline)
- d=2: -0.75 (predicted) vs ~-0.7 (measured)
- d=3: -0.50 (predicted) vs -0.2 to -0.5 (measured)

The agreement is approximate but captures the right trend and
the right order of magnitude on the unmatched family-level summaries.
However, the matched comparison in
[docs/MATCHED_2D_4D_DECOHERENCE_NOTE.md](/Users/jonreilly/Projects/Physics/docs/MATCHED_2D_4D_DECOHERENCE_NOTE.md)
does **not** support a clean dimension-only escape claim, so this derivation
should currently be read as an organizing heuristic rather than as a retained
mechanism.

## Prediction

If this argument is correct:
- **5D (d_spatial=4):** alpha ~ -1.5/4 = -0.375
- **6D (d_spatial=5):** alpha ~ -1.5/5 = -0.30

And the exponent approaches zero as d_spatial → ∞, meaning
decoherence becomes truly scalable in high-dimensional graphs.

## Caveats

1. The "f_mix ~ (r/L)^d" step is hand-waving. A rigorous derivation
   would need the actual path-measure on the DAG.

2. The connect_radius / y_range dependence enters through r/L, which
   is consistent with the universality test showing exponent depends
   on connect_radius and y_range.

3. Layer normalization changes the effective amplitude distribution,
   which modifies the CLT convergence rate but not the dimensional
   scaling.

4. The old k-dependence story is now fit-sensitive. A review-safe
   fixed-window rerun on `N=[25,30,40,60,80]` with shared seeds gives
   overlapping bootstrap intervals across k, so the earlier `k=3` vs
   `k=10` exponent gap should be treated as an exploratory family
   effect rather than a clean exponent law. The likely interpretation
   is still phase-coherence-length driven, but the evidence does not yet
   support a hardened `alpha(k)` theorem.

5. The current 4D large-`N` lane is still topology- and connectivity-coupled.
   So even if the heuristic trend turns out to be right, it is not yet
   isolated as a pure dimensional law in the current codebase.
