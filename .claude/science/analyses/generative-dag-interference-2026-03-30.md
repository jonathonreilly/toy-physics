# Analysis: Interference on a Generated Causal DAG

## Date
2026-03-30

## Key Finding: Interference EMERGES on a randomly generated causal DAG

A randomly grown graph (481 nodes, 25 layers, ~4000 directed edges) produces interference when a barrier with two slit-like gaps is placed at the midpoint. The path-sum over the generated DAG shows phase-dependent visibility up to V=0.99 at the center detector. The control (no barrier) gives V=0.000 exactly.

### Results across 5 random seeds

| Seed | V(y=0) | mean_V | Active detectors |
|------|--------|--------|-----------------|
| 42 | 0.920 | 0.495 | 16 |
| 123 | 0.078 | 0.169 | 17 |
| 456 | 0.988 | 0.559 | 16 |
| 789 | -1.0 (no signal) | 0.620 | 16 |
| 1000 | 0.081 | 0.224 | 17 |

Interference strength varies with the random graph but is present in every seed that has signal at y=0. The variation reflects different random path structures — some geometries produce better amplitude balance between slits.

### What was NOT pre-built
- No rectangular grid
- No coordinate axes
- No uniform spacing
- No pre-defined neighbor structure
- Just: random node positions + proximity-based directed edges

### What WAS put in
- Complex amplitudes and linear path-sum (the 5 irreducible assumptions)
- A barrier region with slit gaps (the "experiment" setup)
- The spawn-layer structure provides a natural time direction

### Significance
This is the transition from "phenomena survive on a graph" to "the graph generates the phenomena." The random causal DAG provides enough path diversity for the path-sum to produce interference. The barrier selects which paths contribute, and the phase sweep reveals the interference pattern.

The generated graphs have very different structure from rectangular grids (irregular spacing, varying connectivity, random topology), yet interference still emerges. This suggests interference is a ROBUST property of path-sums on causal DAGs with sufficient path diversity — not a special feature of regular lattices.
