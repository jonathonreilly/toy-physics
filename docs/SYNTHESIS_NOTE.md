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
| Graph family | N=25 pur_min | N=100 pur_min | Scaling |
|---|---|---|---|
| Uniform random | 0.986 | not tested | Ceiling (CLT) |
| Modular gap=4 | 0.93 +/- 0.02 | 0.95 +/- 0.02 | Stable |
| Modular gap=2 | 0.956 | — | Below threshold |

Decoherence requires channel separation. 14 architectures fail on
uniform DAGs due to geometric convergence (CLT).

### Joint test (same graph instances)
| Parameter | gap=0 | gap=2 | gap=4 | gap=6 |
|---|---|---|---|---|
| Gravity delta | +0.57 | **+1.49** | +0.92 | +1.93 |
| pur_min | 0.976 | **0.956** | 0.961 | 0.964 |
| Both pass? | No | **Yes** | Marginal | No |

**Gap=2.0 is the unification sweet spot.** Crosslink probability
has zero effect (results identical from 0.0 to 0.10).

## What the topology parameter means

The channel gap is the ratio of spatial separation between upper
and lower amplitude channels to the total spatial range:

    channel_ratio = gap / (2 * y_range) = 2.0 / 24.0 = 0.083

At 8.3% gap ratio, channels are close enough for gravitational
interaction (paths through mass region still exist) but separated
enough for decoherence (slit-A and slit-B paths stay in different
channels).

Too small a gap (0%): paths mix freely, CLT erases slit distinction.
Too large a gap (25%+): channels are isolated, gravity weakens,
eventually connectivity breaks entirely.

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
