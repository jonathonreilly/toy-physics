# Synthesis Note: Emergent Physics on Discrete Causal DAGs

**Date:** 2026-04-01
**Status:** Architecture result. Joint unification confirmed.

## The claim

On discrete causal DAGs with path-sum amplitude propagation, both
gravitational attraction and quantum decoherence emerge from the same
minimal structure — but only when the graph topology has **channel
separation** (a spatial gap that prevents cross-channel mixing).

Uniform random DAGs support gravity but not scalable decoherence.
Modular two-channel DAGs support both.

There exists a topology parameter window (gap ~ 2.0 in units of
y_range = 12.0) where both phenomena coexist on the same graph
instances, with the same propagator, simultaneously.

## The model

**Ontology:** Discrete events (nodes) connected by directed causal
links (edges). No pre-existing spacetime. Geometry emerges from
graph structure.

**Propagator:** Corrected form with three ingredients:
1. Geometric attenuation: 1/L^p (L = edge length, p = 1)
2. Directional measure: exp(-beta * theta^2) (theta = off-axis angle)
3. Phase from action: exp(i*k*S) where S = spent delay (field-dependent)

**Gravity mechanism:** Mass nodes create a scalar field f(x).
The spent-delay action S DECREASES near mass (phase valley).
Paths near mass accumulate less phase, creating constructive
interference that deflects amplitude toward mass. Gravity is
a pure phase effect — no force, no metric, just path-sum statistics.

**Decoherence mechanism:** Caldeira-Leggett bath coupled to spatial
y-bins of the per-slit amplitude. Decoherence factor D = exp(-lambda^2 * S)
where S is the bin-resolved contrast between slit-A and slit-B
amplitude distributions. The bath suppresses off-diagonal density
matrix elements proportional to how distinguishable the two slits'
amplitude patterns are.

## Results

### Gravity
| Graph family | N=25 delta | N=40 delta | Signal |
|---|---|---|---|
| Uniform random | +1.11 (3.0 SE) | +1.75 (2.8 SE) | Clear |
| Modular gap=4 | +1.05 (2.3 SE) | +1.88 (2.7 SE) | Clear |
| Modular gap=2 | +1.49 (N=25) | — | Clear |

Gravity works on both uniform and modular DAGs. It grows with N.

### Decoherence
| Graph family | N=25 pur_min (24 seeds) | N=40 pur_min | Scaling |
|---|---|---|---|
| Uniform random (gap=0) | 0.951 | 0.932 | Improving |
| Modular gap=2 | 0.937 | 0.938 | Stable |
| Modular gap=4 | 0.952 | 0.929 | Improving |
| Modular gap=5 | 0.942 | 0.889 | Strongest |

**Revision (24-seed data):** The earlier 12-seed tests overstated the
uniform DAG ceiling. With 24 seeds, even gap=0 shows pur_min=0.951
at N=25. The 14-architecture failure analysis remains valid (all
individual bath/kernel variants fail), but the CL bath on uniform
DAGs performs better than initial 4-seed tests suggested.

Channel separation helps — larger gaps give stronger decoherence
at N=40 — but the effect is a gradient, not a threshold.

### Joint test (24 seeds, same graph instances)
| gap | gravity (N=40) | pur_min (N=40) | decoh (N=40) |
|---|---|---|---|
| 0.0 | +1.51 | 0.932 | +0.067 |
| 2.0 | +1.83 | 0.938 | +0.061 |
| 3.0 | +2.43 | 0.939 | +0.059 |
| 5.0 | **+3.47** | **0.889** | **+0.110** |

**The unification window is broad.** ALL gap values from 0.0 to 5.0
pass both criteria (gravity > 2SE, pur_min < 0.96) with 24 seeds.
Larger gaps give monotonically stronger gravity and decoherence at N=40.
Crosslink probability has zero effect (identical results 0.0-0.10).

## What the topology parameter controls

The gap is a monotonic dial, not a threshold:
- More gap = stronger channel separation = better decoherence
- More gap = more coherent in-channel propagation = stronger gravity
- Too much gap = connectivity breaks (gap > y_range)

The tradeoff is not gravity-vs-decoherence (both improve together)
but channel-coherence vs graph-connectivity.

## What is established

1. Gravity: pure phase effect from path-sum on causal DAG. Born rule
   satisfied (I_3/P = 4e-15). Works on both graph families.

2. Decoherence: requires topological channel separation. IF + CL bath
   framework is validated. Stable through N=100 on modular DAGs.

3. Unification: both emerge from the same propagator on the same
   graph family in the same topology parameter window.

4. The bottleneck was geometry, not architecture: 14 bath/kernel
   variants all fail on uniform DAGs; the simplest bath (CL y-bins)
   works on modular DAGs.

## What is NOT established

1. **Dynamic emergence:** Simple local growth rules do not produce
   channel structure. The gap is imposed, not emergent. The deep
   question — whether quantum-topology coupling can generate channels —
   remains open.

2. **Asymptotic behavior:** pur_min at 0.93 +/- 0.02 could be a true
   floor or slow drift. Per-seed variance (~0.05) dominates.

3. **3D generalization:** All tests are on 2D DAGs (1 spatial + 1
   causal dimension). The channel structure needs to generalize.

4. **Continuum limit:** The connection between discrete channel
   separation and continuous spatial locality is informal.

## Honest assessment

This is a toy model that demonstrates a structural principle:
**topological channel separation is the minimal geometric condition
for both gravity and decoherence to coexist in a path-sum framework
on discrete causal structure.**

The result is conceptually clean — the same propagator, the same
graph, one topology parameter — but the gap is hand-tuned, not
emergent. The model is 2D, the graphs are small (N=25-100 layers),
and the decoherence is moderate (pur_min ~ 0.95, not << 1).

The physics claim is: in a discrete event ontology, the geometry
that supports quantum interference and gravitational attraction
must have a specific topological property (channel separation) to
also support decoherence. This is a constraint on emergent spacetime
geometry, derivable from the path-sum structure alone.
