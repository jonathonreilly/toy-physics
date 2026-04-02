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

1. **Gravity signal:** phase-induced deflection on uniform DAGs is
   statistically real at intermediate `N` (up to `5.1 SE` on the
   retained setups). The existence of the signal is established; the
   exact distance-law exponent and a fixed-position mass law are not
   yet review-safe.

2. **Linear ceiling:** on the clean random-DAG benchmarks, decoherence
   capacity decays roughly like `1/N`. The CL bath and related purity
   probes agree that finite-`N` gains exist, but linear path sums wash
   out asymptotically.

3. **Regulated propagator:** per-layer normalization is Born-clean on
   the validated harness and materially shifts the finite-`N`
   decoherence floor (`pur_min ~ 0.80` at `N=40` versus `~0.95`
   linear).

4. **Combined stacking:** layer norm and imposed modular topology are
   complementary. The strongest retained finite-`N` result remains
   `pur_min = 0.619` at `N=25`, with a clear gain still present at
   `N=80`.

5. **Topology-native decoherence:** 3D topological path-count
   asymmetry is a real graph-theoretic observable, and pruning low-
   asymmetry nodes improves `pur_cl` through `N=60` on the original
   setup and through `N=100` on denser graphs. The effect weakens with
   `N`, but it is no longer just a branch-local curiosity.

6. **Asymptotic limit:** all retained lanes still trend back toward
   recoherence at large `N`. Regulation and topology shift the
   prefactor and usable window, but they do not yet produce a clean
   asymptotic escape.

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

## What is NOT established

1. **Exact gravity law** — the current repo does not yet lock a
   review-safe `1/b^p` distance law or a frozen-position `F(M)` law.
   The gravity signal is real, but the force law is still the main
   missing piece.

2. **Asymptotic escape** — all retained propagators and graph-side
   improvements still decay back toward coherence. The best current
   wins are finite-`N` and prefactor-based.

3. **Dynamic hard geometry** — many soft emergence rules fail, and the
   surviving topology-native lanes still work by removing or excluding
   nodes rather than generating a hard gap from a local nucleation law.

4. **Continuum bridge** — the discrete results are now quantitatively
   sharper, but the formal bridge to continuum gravity/decoherence is
   not built.

## Honest assessment

This is a toy model with a growing set of quantitative results, but the
honest center of gravity is still “strong finite-`N` structure, missing
force law”:

1. **Gravity from phase:** a statistically real deflection signal
   survives on retained uniform-DAG setups, up to `5.1 SE`.

2. **Linear ceiling:** on random DAGs, decoherence capacity decays
   approximately like `1/N`, making the washout problem quantitative.

3. **Born-clean regulation:** per-layer normalization preserves the
   validated Sorkin test while materially lowering `pur_min` at finite
   `N`.

4. **Stacked finite-`N` gain:** layer norm plus modular topology is the
   strongest retained decoherence lane on disk (`pur_min = 0.619` at
   `N=25`, still `0.852` at `N=80`).

5. **Topology-native emergence:** topological path-count asymmetry is a
   real graph-theoretic route to decoherence and survives to larger `N`
   once graph density is increased.

6. **Bounded coexistence:** there are real bounded windows where the
   same discrete structure supports gravity-like deflection and
   decoherence-like loss of purity, but the exact law-level gravity
   story remains unresolved.

The model's limitation is now clearer than before: the finite-`N`
structure is real and surprisingly rich, but the asymptotic ceiling
and the missing clean gravity law remain central. Truly scalable
decoherence or law-like gravity may require a deeper architecture
beyond the current linear path-sum / imposed-geometry framework.

The open question is no longer “is there any mechanism at all?” It is
which deeper mechanism, if any, can generate hard geometry or a stable
force law rather than merely shifting the prefactor of the existing
ceiling.
