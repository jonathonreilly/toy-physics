# Synthesis Note: Emergent Physics on Discrete Causal DAGs

**Date:** 2026-04-02 (final)
**Status:** Architecture locked. Scaling laws quantified. Emergence closed.

## The model

**Ontology:** Discrete events (nodes) connected by directed causal
links (edges). No pre-existing spacetime.

**Propagator:** Three ingredients:
1. Geometric attenuation: 1/L (L = edge length)
2. Directional measure: exp(-0.8 × theta²) (theta = off-axis angle)
3. Phase from action: exp(i×k×S) where S = spent delay (field-dependent)

**Gravity:** Mass nodes create a 1/r scalar field. The spent-delay
action DECREASES near mass (phase valley), deflecting amplitude toward
mass via constructive interference. Pure phase effect.

**Decoherence:** Caldeira-Leggett bath coupled to spatial y-bins.
D = exp(-lambda² × S) where S is bin-resolved contrast of per-slit
amplitude distributions.

## Quantitative results

### Gravity (24 seeds, paired per-seed SE)

On **uniform DAGs**:
```
N=18: delta/SE = 2.1  (significant)
N=25: delta/SE = 2.5  (significant)
N=30: delta/SE = 5.1  (highly significant)
N=40: delta/SE = 3.3  (significant)
N=60: delta/SE = 0.5  (lost to CLT)
```

Gravity does NOT require channel separation. Signal peaks at N=30.

**Distance scaling:** delta peaks at b ≈ 6 (half beam width),
falloff in far field: delta ~ b^(-1.93) (near 1/b²).
At b = 30: delta ≈ 0 (gravity vanishes at 2.5× beam width).

### Decoherence (24 seeds)

**Scaling law:**
```
(1 - pur_min) = 1.64 × N^(-1.01)    R² = 0.83
(1 - overlap) = 2.36 × N^(-0.84)    R² = 0.76
```

Decoherence decays as **1/N**. Half-life: pur_min = 0.99 at N ≈ 156.

```
N=30:  (1-pur_min) ≈ 0.053  (5.3% decoherence)
N=60:  (1-pur_min) ≈ 0.028  (2.8%)
N=100: (1-pur_min) ≈ 0.014  (1.4%)
N=156: (1-pur_min) ≈ 0.01   (effectively coherent)
```

**Ceiling diagnosis:** pur_min itself → 1 (bath-independent floor).
Lambda=100 gives pur_cl = pur_min (bath already at max strength).
Full env_depth (53 layers) doesn't help. The limit is CLT convergence
of detector-state overlap, not bath parameters.

### Joint test (24 seeds, same graph instances)

All gap values 0.0-5.0 pass both criteria at N=25 and N=40:
```
gap=0 (uniform): gravity +1.49, pur_min 0.945
gap=5 (modular):  gravity +3.47, pur_min 0.889
```
Larger gaps improve both metrics monotonically.

### 3D generalization

Decoherence survives in 3D (modular gap=4, N=25: pur_min=0.942).
Gravity present but weaker (signal diluted by extra dimension).

### Gravity completions

**Mass scaling:** delta = 0.13 × M^0.82 (alpha ≈ 1, consistent with F∝M).
Saturates at M>8 when mass covers half the layer.

**Distance scaling:** Peak deflection at b ≈ 6 (half beam width).
Falloff: delta ~ b^(-1.93) in far field (near 1/b²).
Zero at b = 30 (2.5× beam width).

### Regulated propagator (per-layer normalization)

**Corrected with proper Sorkin I₃ = ... - P(∅)** (Codex bugfix).
The earlier |I₃|/P ≈ 1 was a harness bug, not real Born violation.

Four propagator variants tested at N=80 (corrected Born):
```
Linear:         pur_min = 0.982  |I₃|/P = 1.1e-15  (machine zero)
Layer norm:     pur_min = 0.948  |I₃|/P = 4.1e-16  (machine zero!)
Saturation:     pur_min = 0.902  |I₃|/P = 6.9e-03  (small real cost)
Phase equalize: pur_min = 0.893  |I₃|/P = 6.1e-01  (genuinely bad)
```

**Layer normalization is the clean winner.** It shifts the decoherence
ceiling by ~5x while preserving Born at machine precision:
```
         Linear    Layer norm    Improvement
N=25:    0.958     0.811         -0.147
N=40:    0.953     0.801         -0.152  ← massive
N=60:    0.970     0.876         -0.094
N=80:    0.982     0.948         -0.034  ← ceiling returns
```

Layer normalization is physically a per-layer wavefunction
renormalization — standard in quantum mechanics and lattice field
theory. It prevents runaway amplitude concentration (the mechanism
behind CLT convergence) without breaking linearity of the path sum.

The ceiling still returns at large N, but the effective model range
extends from N~50 (linear) to N~80+ (layer norm).

## Emergence program: closed (9 approaches)

| # | Approach | Type | Result |
|---|----------|------|--------|
| 1 | Locality bias (3 sigmas) | Connection | CLT at N=40 |
| 2 | Reinforcement | Connection | No separation |
| 3 | Repulsive placement | Connection | No channels |
| 4 | Pre-barrier amplitude feedback | Connection | Source y-symmetric |
| 5 | Post-barrier slit-conditioned | Connection | CLT makes D≈0.5 |
| 6 | Distinguishability placement (mild) | Placement | Gap but no improvement |
| 7 | Distinguishability placement (strong) | Placement | Gap too large |
| 8 | Calibrated alpha sweep | Placement | No alpha beats uniform |
| 9 | Node removal (prune=0.10) | Removal | Marginal at N=40, ceiling at N=80 |

**Connection rules fail:** CLT operates on any connected graph.
**Placement rules fail:** can't control gap size/location.
**Node removal:** only approach to beat baseline, but marginal and
ceiling returns at N=80.

**Structural conclusion:** the missing ingredient is hard geometry
(node absence), not softer filtering. Local growth rules cannot
produce topological barriers because barriers are defined by the
ABSENCE of nodes, not by node properties.

## What is established

1. **Gravity** on uniform DAGs at N=18-40 (up to 5.1 SE). Distance
   scaling ~1/b² in far field. Mass scaling F∝M (alpha=0.82).
   Born rule I₃/P = 4e-16 (machine zero).

2. **Decoherence** at intermediate N with 1/N power-law decay
   (linear propagator). CL bath framework validated. 14 alternative
   architectures fail.

3. **Regulated propagator:** per-layer normalization shifts the
   ceiling ~5x (pur_min 0.80 at N=40 vs 0.95 linear) while
   preserving Born at machine precision. Extends effective range
   from N~50 to N~80+.

4. **Unification:** gravity + decoherence work simultaneously on
   same graphs, same propagator. Broad parameter window.

5. **Ceiling:** asymptotically fundamental even with regulation.
   Both linear and layer-norm propagators trend pur_min → 1 at
   large N, but layer norm delays the onset.

6. **3D:** decoherence transfers directly. Gravity present but weak.

### Combined propagator: layer norm + modular topology

The two mechanisms STACK (attack different aspects of CLT):
```
                          N=25    N=40    N=80    pur_min=0.99 at
Linear + uniform:         0.958   0.953   0.982   N ≈ 235
LayerNorm + uniform:      0.811   0.801   0.948   —
Linear + modular gap=4:   0.942   0.933   0.951   —
LayerNorm + gap=2:        0.619   0.769   0.852   N ≈ 1355
LayerNorm + gap=4:        0.704   0.805   0.878   N ≈ 6188
```

**pur_min = 0.603 at N=25** (40% decoherence, 24 seeds) is the strongest
ever measured. Born = 5e-16 (machine zero).

24-seed combined scaling law (R²=0.946, cleanest fit in program):
```
(1-pur_min) = 5.88 × N^(-0.88)
```

| N | Linear+uniform | LN+gap=2 | LN+gap=4 |
|---|---|---|---|
| 25 | 0.957 | **0.603** | 0.685 |
| 40 | 0.944 | **0.777** | 0.758 |
| 60 | 0.972 | **0.861** | 0.786 |
| 100 | 0.986 | **0.892** | 0.897 |

Gravity survives on combined propagator:
  LN+gap=4, N=50: delta=+1.57 (3.4 SE)

Effective range: pur_min=0.90 at N≈101, pur_min=0.99 at N≈1375.

### Stochastic collapse at mass nodes

Random dephasing at mass nodes (p_collapse=0.2, MC over realizations):

Born: |I₃|/P = 2.3e-5 (practically clean).

**Correction (N=200 test):** The apparent positive exponent (+0.21)
was dominated by k-band averaging, not the collapse mechanism itself.
When the collapse-specific contribution is isolated (collapse minus
no-collapse baseline at each N):

```
N=25:  collapse adds +0.070 to 1-pur
N=80:  collapse adds +0.021
N=200: collapse adds +0.002
```

The collapse-specific decoherence SHRINKS with N, following the same
CLT-driven convergence as the CL bath. More mass encounters at larger
N doesn't help because the per-encounter dephasing effect diminishes
as amplitudes become more uniform.

The positive total (1-pur) growing at large N comes from k-band
averaging (different k values produce different ψ, and the average ρ
is increasingly mixed), not from the collapse mechanism.

### Dimensional scaling: promising 4D flattening, not a clean escape theorem

The retained 4D modular large-`N` lane is still important, but the safe
claim is narrower than the older “4D escapes the ceiling” wording.

What is solid:
```
4D modular gap=3/5, densified large-N harness:
pur_cl stays bounded away from 1 through N=100
```

What is still provisional:
```
2D uniform:       alpha = -1.58  (rapid decay)
4D modular gap=3: alpha = -0.22  (12-seed provisional fit, R²=0.40)
```

That exponent comparison is not yet apples-to-apples, because the retained
4D lane also changes topology and connectivity regime (modular channels,
more nodes per layer, tighter spatial range, larger connect radius) in
order to stay connected through `N=100`.

The exponent also appears to depend on wavenumber `k` inside the tested 2D
family, but that result is still fit-sensitive:
```
k=3:  alpha = -0.32  (shallowest in the current mean-curve fit)
k=10: alpha = -2.52  (steepest in the current mean-curve fit)
```

So the correct current interpretation is:
- 4D modular geometry is the strongest retained large-`N` CL-bath lane on disk
- k likely matters inside the tested 2D family
- neither result is yet a clean universal exponent law

## What is NOT established

1. **4D exponent confirmation** — the provisional `-0.22` fit is from
   12 seeds with `R²=0.40` on a densified modular 4D harness. It still
   needs a same-family matched comparison and more seeds / larger `N`
   before it can be promoted as a dimensional law.

2. **Dynamic emergence** — 9 approaches tested, all fail. The gap
   may be a boundary condition on emergent spacetime.

3. **Continuum limit** — the power-law scaling suggests a connection
   to decoherence rates in quantum gravity, but the formal bridge
   is not built.

## Honest assessment

This is a toy model with **five locked quantitative results plus two live
frontier leads**:

1. **Gravity signal from phase:** statistically real deflection exists
   on retained graph families, but the exact distance law and fixed-position
   mass law are still unresolved.

2. **Decoherence from CL bath:** `(1-pur_min)` falls roughly like a power
   law in `N`, typically around `N^(-0.7 .. -1.0)` on the retained 2D/3D
   linear lanes. This is the cleanest current structural limit.

3. **Regulated propagator:** per-layer normalization can be Born-clean on
   retained lanes and materially shifts the finite-`N` decoherence prefactor.

4. **Combined stacking:** layer norm + hard/modular geometry are genuinely
   complementary. The strongest retained 2D/3D bounded lanes push the useful
   decoherence window far beyond the linear baseline.

5. **Joint coexistence:** bounded same-propagator / same-family gravity +
   decoherence pockets are real on retained hard-geometry lanes.

Frontier leads that are still interesting but not locked:

6. **4D modular large-`N` lane:** strong bounded decoherence through `N=100`
   is real, but the provisional exponent flattening is not yet a clean
   dimensional theorem.

7. **4D + regulation / k-dependence:** these are promising frontier hints,
   but the current `alpha` claims are not yet hardened enough to promote as
   canonical results without matched reruns and anchored artifacts.

So the safest current summary is:
- bounded coexistence and bounded ceiling-shifting are real
- the asymptotic ceiling remains the main structural limit
- 4D / k / 4D+LN are frontier leads, not yet foundation-level theorems

The open question: does a growth law exist where nodes fail to
nucleate in low-distinguishability regions? This is causal set
dynamics, not parameter sweeping, and requires theoretical work
beyond the computational program completed here.
