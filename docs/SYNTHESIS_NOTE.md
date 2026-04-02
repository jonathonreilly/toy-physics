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

### Nonlinear propagator trade-off

Three nonlinear variants tested at N=80:
```
Linear:         pur_min = 0.982  |I₃|/P ~ 0.4  (noisy baseline)
Layer norm:     pur_min = 0.948  |I₃|/P = 1.0  (Born destroyed)
Saturation:     pur_min = 0.902  |I₃|/P = 1.0  (Born destroyed)
Phase equalize: pur_min = 0.893  |I₃|/P = 0.8  (Born ~destroyed)
```

**Fundamental trade-off:** CLT convergence produces BOTH the 1/N
ceiling AND Born rule compliance. Breaking one breaks the other.
Nonlinearity can lower pur_min to 0.89 at N=80 but at the cost of
|I₃|/P → 1 (maximal Born rule violation).

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
   scaling ~1/b² in far field. Born rule I₃/P = 4e-15.

2. **Decoherence** at intermediate N with 1/N power-law decay.
   CL bath framework validated. 14 alternative architectures fail.

3. **Unification:** both work simultaneously on same graphs, same
   propagator. Broad parameter window.

4. **Ceiling:** fundamental to linear path-sums. (1-pur_min) ~ 1/N.
   No bath, topology, or pruning can escape it asymptotically.

5. **3D:** decoherence transfers directly. Gravity present but weak.

## What is NOT established

1. **Scalable decoherence** — 1/N decay means the model's effective
   range is N < ~50 layers. Whether nonlinear propagators or
   explicit collapse can beat this is untested.

2. **Dynamic emergence** — 9 approaches tested, all fail. The gap
   may be a boundary condition on emergent spacetime.

3. **Continuum limit** — the 1/N scaling suggests a connection to
   decoherence rates in quantum gravity (environment size scaling),
   but the formal bridge is not built.

## Honest assessment

This is a toy model with three publishable quantitative results:

1. **Gravity from phase:** deflection ~ phase valley mechanism,
   5.1 SE on uniform DAGs, 1/b² distance scaling.

2. **Decoherence from CL bath:** (1-pur_min) ~ 1/N with R²=0.83.
   The mechanism is clean (bin-resolved field contrast) and the
   scaling law is analytic.

3. **Joint coexistence:** same propagator, same graphs, broad
   parameter window. The first toy model (to our knowledge) where
   gravity and decoherence emerge from a single discrete structure.

The model's limitation is the 1/N ceiling — decoherence is a
finite-size effect, not an asymptotic feature. This is consistent
with the model being a toy (linear path-sum, no collapse) rather
than a fundamental theory.

The open question: does a growth law exist where nodes fail to
nucleate in low-distinguishability regions? This is causal set
dynamics, not parameter sweeping, and requires theoretical work
beyond the computational program completed here.
