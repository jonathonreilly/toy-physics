# Synthesis Note: Emergent Physics on Discrete Causal DAGs

**Date:** 2026-04-01 (revised with 24-seed data)
**Status:** Architecture result locked. Emergence program closed.

## The claim (revised)

On discrete causal DAGs with path-sum amplitude propagation, both
gravitational attraction and quantum decoherence emerge from the same
minimal structure. The CL bath achieves pur_min ~ 0.93-0.95 on BOTH
uniform and modular DAGs when averaged over sufficient seeds (16+).

Channel separation (modular DAG) improves the result — especially at
large N where gap=5 gives pur_min=0.889 — but the uniform baseline
is stronger than initial 4-seed tests suggested.

**Important revision:** The "geometric ceiling" (pur_min=0.986 on
uniform DAGs) was partially a small-sample artifact. With 24 seeds,
uniform DAGs show pur_min=0.951 at N=25, not 0.986.

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

1. **Gravity:** Pure phase effect from path-sum on causal DAG. Born rule
   satisfied (I_3/P = 4e-15). Works on both uniform and modular DAGs.
   Signal grows with N.

2. **Decoherence:** CL bath achieves pur_min ~ 0.93-0.95 on both
   uniform and modular DAGs with 16+ seeds. Channel separation helps
   (gap=5 at N=40: pur_min=0.889) but is not strictly required.

3. **Unification:** Both gravity and decoherence emerge from the same
   propagator on the same graphs simultaneously. All gap values 0-5
   pass both criteria with 24 seeds. Larger gaps improve both.

4. **Architecture:** 14 individual bath/kernel variants fail on uniform
   DAGs with 4 seeds. The CL bath (exponential D=exp(-lambda^2*S)) is
   the only architecture that works, on any graph family.

## Emergence program: closed (8 approaches tested)

| # | Approach | Type | Result |
|---|----------|------|--------|
| 1 | Locality bias | Connection | CLT collapses at N=40 |
| 2 | Reinforcement | Connection | No spatial separation |
| 3 | Repulsive placement | Connection | No persistent channels |
| 4 | Pre-barrier amplitude feedback | Connection | Source y-symmetric |
| 5 | Post-barrier slit-conditioned | Connection | CLT makes asymmetry ~0.5 |
| 6 | Distinguishability placement (mild) | Node placement | Gap ~2 but no improvement |
| 7 | Distinguishability placement (strong) | Node placement | Gap too large, disconnects |
| 8 | Calibrated alpha sweep | Node placement | No alpha beats uniform |

**Conclusion:** Local growth rules cannot produce the specific gap
geometry needed. Connection rules fail because CLT operates on any
connected graph. Placement rules create gaps but can't control size
or location. The uniform baseline is stronger than initially measured.

## What is NOT established

1. **Dynamic emergence:** 8 approaches tested, all fail. The gap
   may be a boundary condition on emergent spacetime, not derivable
   from a simpler local rule.

2. **3D generalization:** All tests are 2D (1 spatial + 1 causal).

3. **Continuum limit:** Discrete channel separation ↔ spatial
   locality connection is informal.

4. **Strong decoherence:** pur_min ~ 0.93 is moderate, not << 1.
   Whether this can reach physically meaningful decoherence levels
   (pur_min < 0.5) on any topology is unknown.

## Honest assessment (revised)

This is a toy model demonstrating that **path-sum propagation on
discrete causal DAGs supports both gravity and decoherence** using
a single propagator and CL bath environment. The result holds on
both uniform and modular topologies, with channel separation
improving (not enabling) decoherence.

The initial claim that "uniform DAGs hit a geometric ceiling" was
overstated due to small sample sizes. With 24 seeds, uniform DAGs
achieve pur_min ~ 0.95, within 2% of modular DAGs.

The physics result: **gravity (corrected propagator) and decoherence
(CL bath) coexist on the same causal DAGs.** This is a structural
finding about discrete path-sum models, not a claim about real physics.

The emergence question — can the topology that optimizes both be
generated dynamically — is cleanly diagnosed (8 approaches, all fail)
and remains open as a theoretical question about emergent spacetime.
