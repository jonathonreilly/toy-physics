# Synthesis Note: Emergent Physics on Discrete Causal DAGs

**Date:** 2026-04-01
**Status:** retained architecture note with metric caveats tightened and pruning lane narrowed

This note is now mainly the **2D / topology-pivot synthesis**. For the current
3D / 4D / 5D state, see
[HIGHER_DIMENSION_STATUS_2026-04-01.md](/Users/jonreilly/Projects/Physics/docs/HIGHER_DIMENSION_STATUS_2026-04-01.md).

## The current claim

On discrete causal DAGs with path-sum amplitude propagation:

1. **Gravity** from the corrected propagator produces positive deflection
   toward mass on the retained graph families. The effect is clearest on the
   modular / channelized family, while the exact significance numbers in older
   notes should be treated as provisional until the paired per-seed delta
   calculation is used everywhere.

2. **Decoherence** from the CL bath is real in the retained non-unitary lane.
   The actual traced detector purity `pur_cl` reaches the `~0.93-0.96` range
   in the best current runs, while `pur_min` is the lower bound achieved in
   the fully decohered limit. Some older phase-diagram notes blurred those two
   quantities; this note keeps them separate.

3. **Topology matters.** Within the modular / gap-controlled family, widening
   the imposed gap generally lowers the achievable decoherence floor and
   strengthens gravity until connectivity breaks. `gap=0` in the current
   modular generator now behaves as the true uniform-style baseline.

So the strongest current statement is:

- the corrected unitary core and the IF / CL decoherence route can coexist on
  the same modular topology family
- the decisive control variable is topology
- the remaining open issue is dynamic generation of the good topology
- the true large-`N` single-vs-double-slit visibility gain on the retained
  modular bath lane is weak and does not remain high

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
| Graph family | N=25 mean delta | N=40 mean delta | Current read |
|---|---|---|---|
| Uniform random | positive | positive | works, but noisier |
| Modular gap=4 | positive | positive | strongest retained lane |
| Modular gap sweep | larger gap -> larger delta | larger gap -> larger delta | topology-sensitive |

Gravity works on both uniform and modular-style families, but the modular lane
is presently the clearest place where the effect survives alongside the
decoherence story. Earlier `SE` numbers in repo notes were slightly optimistic
because they were not always computed from paired per-seed deltas.

### Decoherence
| Graph family / metric | N=25 | N=40 | Current read |
|---|---|---|---|
| Uniform random `pur_cl` | `~0.94-0.95` | `~0.94` in current best runs | moderate |
| Modular family `pur_min` floor | below uniform | lower again at larger gaps | stronger achievable floor |
| Modular family `pur_cl` | broadly similar or slightly better than uniform in the retained range | improves on the best modular settings | retained non-unitary lane |

The 24-seed revision removed the earlier over-strong “uniform DAG ceiling at
0.986” story. Uniform random DAGs can already reach `pur_cl ~ 0.95` in the
current CL-bath runs. What topology changes most clearly, under the current
audited scripts, is the **achievable decoherence floor** `pur_min` and the
stability of the retained non-unitary lane.

### Joint test (24 seeds, same graph instances)
| modular gap | gravity at N=40 | `pur_min` floor at N=40 | current read |
|---|---|---|---|
| 0.0 | positive | below 0.96 | still modular, not uniform |
| 2.0 | stronger | lower floor | good retained regime |
| 3.0 | stronger again | similar floor | broad window |
| 5.0 | strongest current signal | lowest current floor | best tested modular point |

**The unification window is broad within the modular family.** Under the
current refined phase-diagram scripts, all tested gaps `0.0..5.0` retain
positive gravity and `pur_cl < 0.96` on the audited sweep, with stronger gaps
generally helping until connectivity breaks.

## What the topology parameter controls

Inside the modular family, the imposed gap behaves like a control dial:
- more gap usually means stronger channel separation
- stronger channel separation usually improves the decoherence floor
- the same structure also tends to strengthen gravity
- too much gap eventually breaks connectivity

So the retained tradeoff is not gravity versus decoherence, but branch
preservation versus graph connectivity.

## What is established

1. **Gravity:** The corrected propagator still supports positive mass-side
   deflection and remains compatible with the fixed-DAG Born/interference
   checks. The modular family is currently the clearest gravity lane.

2. **Decoherence:** The IF / CL route is retained. Uniform dense DAGs can show
   moderate decoherence, but the modular family gives a better controlled
   topology and a lower achievable decoherence floor.

3. **Unification:** Gravity and decoherence coexist on the same modular graph
   instances with the same retained propagator.

4. **Architecture:** The earlier graph-local environment search on dense random
   DAGs still fails as a generic route. The positive non-unitary story now runs
   through IF / CL plus the right topology.

## Large-N read

The strongest current large-`N` statement is more modest than some older notes:

- dense connected families still show CLT-style convergence pressure
- the modular family delays or softens that problem by preserving branch
  structure better
- the old both-slits-open contrast proxy stays high, but the newer true
  single-vs-double-slit visibility gain is only `+0.023` at `N=12`, drops to
  `+0.002` at `N=18`, and is near zero or negative by `N>=25`

## Emergence status: local endogenous generation still open

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
| 9 | **Node removal (prune=0.10)** | **Node removal** | **Intermediate-N improvement only** |

**Approach 9 (node removal)** is the first emergence-adjacent surrogate that
improves the dense-random baseline at intermediate `N`. But it does so by
building the full graph, globally ranking post-barrier nodes by
distinguishability, and then pruning them. The effect is not asymptotically
stable: by `N=80..100` the ceiling returns, and stronger or adaptive pruning
pushes the graph toward disconnection. So it should be read as a **nonlocal
pruning construction**, not as a solved local growth law.

The first hard-gap placement-only diagnostic is also now explicitly
`not-ready`: the best candidate (`alpha=1`) reaches a useful gap width
(`gap ~ 2.3`) only with a badly misplaced center (`|gap_ctr| ~ 4.2`), while
stronger placement drives the graphs toward near-disconnection and
`pur_cl -> 1.0`.

## What is NOT established

1. **Scalable emergence:** no local endogenous growth law yet reproduces the
   good modular topology. Global post-hoc node removal helps only at
   intermediate `N` and is not an asymptotic fix.

2. **3D generalization:** All tests are 2D (1 spatial + 1 causal).

3. **Continuum limit:** Discrete channel separation ↔ spatial
   locality connection is informal.

4. **Strong decoherence:** pur_min ~ 0.93 at best (N=40 with
   removal or modular gap=5). Never reaches << 0.5. The linear
   path-sum may fundamentally limit decoherence depth.

## Honest assessment (revised)

This is a toy model demonstrating that **path-sum propagation on discrete
causal DAGs can support gravity and decoherence under one retained
architecture**, provided the topology preserves branch structure well enough.

The older story that “uniform fails, modular alone works” was too sharp.
Uniform random DAGs can already show moderate CL-bath decoherence in larger
seed runs. The stronger retained claim is instead:

- topology materially changes the achievable decoherence floor
- the modular family is presently the clearest joint gravity+decoherence lane
- on the asymptotic modular bath lane, true interference gain is weak/gone
  even though the older contrast proxy stayed high
- the emergence question remains open because the good topology is still
  imposed; the best pruning surrogate helps only at intermediate `N` and does
  not generate a stable local hard-gap rule
