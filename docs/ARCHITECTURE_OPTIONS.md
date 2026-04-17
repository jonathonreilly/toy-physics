# Architecture Options

## Current Architecture (baseline)

```
Propagator: exp(i*k*S_spent) / L^p
Environment: last mass node index (fine-grained)
Partial trace: P(det) = Σ_env |ψ(det,env)|²
```

Produces: gravity (sign correct), interference, Born rule, decoherence (universal but wrong-scaling).

## Gravity Fix Candidates

### G1: Path-multiplicity-renormalized action

```
S_eff(edge) = S(edge) / n_paths_through(edge)^α
```

Divide the action by the local path multiplicity raised to some power α. Edges with many paths contribute less action per effective path. This prevents saturation because high-multiplicity edges (which dominate on large graphs) get renormalized down.

**Pros:** Directly addresses the averaging-out mechanism. Preserves k=0→0.
**Cons:** Requires computing local path counts (expensive). New parameter α.
**Test:** Does R(b) fall off with b?

### G2: Coarse-grained propagator

```
amplitude = Σ_coarse_paths exp(i*k*S_coarse) / L_coarse^p
```

Instead of summing over all microscopic paths, group paths into "bundles" by their coarse trajectory (e.g., which y-bin they pass through at each layer). Each bundle contributes one amplitude. Near-degenerate paths within a bundle interfere internally but the bundle acts as one effective path.

**Pros:** Naturally reduces path multiplicity. Scale-independent by construction.
**Cons:** Requires defining coarse-graining scheme. May break Born rule.
**Test:** Does shift×b stabilize?

### G3: k-dependent attenuation

```
amplitude = exp(i*k*S) / L^(p + β*k*f)
```

Make the attenuation field-dependent but controlled by k. At small k (perturbative): standard 1/L^p. At large k: field-dependent attenuation kicks in, preventing saturation.

**Pros:** Smooth interpolation. Preserves k=0→0.
**Cons:** Reintroduces field-dependent attenuation (which we removed for good reason). May reintroduce repulsion.
**Test:** Does the saturation point k_sat increase?

## Decoherence Fix Candidates

### D1: Multi-local tensor environment

```
env = (env_cell_1, env_cell_2, ..., env_cell_M)
```

Divide the mass region into M spatial cells. Each cell has its own local env register. The full env state is the tensor product. Paths through different cell configurations get different env labels.

**Pros:** Env dimension grows as d^M (exponential in M). Naturally matches path multiplicity growth.
**Cons:** State space explodes. Need truncation/approximation.
**Test:** Does purity decrease with graph size at fixed M/N ratio?

### D2: Edge-sector records

```
env_cell = histogram of (incoming_angle_bin, outgoing_angle_bin) at cell
```

Each mass-region cell records a coarse histogram of edge directions. Different slit paths create different histograms because they arrive from different angles.

**Pros:** Direction-dependent without explicit directional coupling. Grows with path diversity.
**Cons:** Histogram comparison for env labeling is complex. Binning choices.
**Test:** Does direction specificity increase with graph size?

### D3: Continuous bath variable

```
env = continuous phase θ ∈ [0, 2π)
```

No binning — the environment is a continuous variable. The partial trace becomes an integral:
`P(det) = ∫ |ψ(det, θ)|² dθ`

**Pros:** Infinite-dimensional env. No binning artifacts.
**Cons:** Requires discretization for numerical work. How does θ couple to system?
**Test:** Does purity decrease monotonically with coupling strength?

### D4: Irreversible spatial coarse-graining

```
P(det) = Σ_region Tr_region(|ψ⟩⟨ψ|) for spatial regions
```

Instead of tracing over env labels, trace over entire spatial regions. The mass region is "integrated out" — its internal state is not observed. This is closer to real-world decoherence where the environment is a spatial region, not a label.

**Pros:** Physically motivated. No env labels needed.
**Cons:** Requires defining the spatial trace. Non-trivial for path-sum.
**Test:** Compare with two-register at matched parameters.

## Priority Order

1. **D1 (multi-local tensor)** — most likely to fix decoherence scaling
2. **G2 (coarse-grained propagator)** — most likely to fix gravity scaling
3. **D4 (spatial coarse-graining)** — most physically motivated decoherence
4. **G1 (path-multiplicity renormalization)** — simplest gravity fix to test
