# Gap-as-Physics: Investigation Note

**Date:** 2026-04-02
**Branch:** claude/distracted-napier
**Status:** Complete. 8 experiments, 5 structural conclusions.

## Motivation

Nine attempts to dynamically generate the modular gap from local rules
failed. This investigation treats the gap as an object in its own right
and characterizes its properties.

## Experiments and results

### Exp 1: Gap stability under perturbation
Fill the gap with nodes at controlled densities.

| fill% | pur_cl (N=40) | S_norm | verdict |
|-------|---------------|--------|---------|
| 0     | 0.950         | 0.107  | baseline |
| 5     | 0.969         | 0.100  | mild degradation |
| 10    | 0.968         | 0.068  | S_norm drops |
| 25    | 0.984         | 0.044  | approaching uniform |
| 50    | 0.988         | 0.035  | nearly uniform |
| 100   | 0.992         | 0.028  | uniform ceiling |

**Finding:** Gradual degradation, no phase transition.

### Exp 2: Tapered gap profile
Gap width varies along causal direction.

**Finding:** All profiles (narrowing, widening, pinch, partial) within
~0.01 of uniform baseline. Gap location is weakly constrained.

### Exp 5a: Global amplitude penalty
Soft penalty `exp(-pen * exp(-y²/2σ²))` on all edges near y=0.

**Finding:** Works at N=40, collapses at N=60. Kills amplitude
throughput rather than creating channel separation.

### Exp 5b: Edge deletion (tension model)
Delete edges near y=0 with probability ~ tension.

**Finding:** Creates decoherence but breaks connectivity. At
sigma=2, tension=50: pur_cl=0.954 at N=40 but 0 connected seeds.

### Exp 5c: Cross-channel edge penalty
Penalize only edges crossing y=0, not all edges near y=0.

**Finding:** S_norm completely unchanged (0.0783 vs 0.0781 at N=25).
Single-slit amplitude still reaches all y-regions via within-channel
paths. Edge suppression alone cannot create which-path information.

### Exp 6: Physics-motivated node removal (D-threshold)
Remove nodes with low which-path distinguishability |D|.

**Finding:** |D| ≈ 0 for ALL nodes on uniform DAGs. 100% removal
at any threshold. The CLT bottleneck means no which-path information
exists at the node level before the gap creates it.

### Exp 3: Gap topology variants

| Variant | pur_cl (N=40) | Notes |
|---------|---------------|-------|
| hard-gap-4 | 0.950 | baseline |
| two-gap-w2-o2 | 0.938 | three channels, slightly better |
| angled-0.3 | 0.948 | tilted gap, matches baseline |
| angled-0.5 | 0.973 | steep tilt, mild degradation |
| gap-start-50% | 0.957 | partial: first half only |
| gap-end-50% | 0.975 | partial: last half only, weaker |
| bridge-1 | 0.954 | 1 bridge node/layer, robust |
| bridge-5 | 0.969 | 5 bridges, still works |

**Finding:** The gap is topologically robust. Angled gaps, partial
gaps, and bridged gaps all preserve decoherence. A few bridge nodes
do not break the effect.

### Exp 4: Gap codimension (2D gap in 3D)

| Variant | pur_cl (N=40) | pur_cl (N=60) |
|---------|---------------|---------------|
| no-gap | 0.967 | 0.980 |
| 1d-y4 | 0.951 | 0.969 |
| cyl-r4 | 0.958 | 0.958 |
| cyl-r6 | 0.928 | 0.953 |

**Finding:** Cylindrical exclusion (blocking z-leakage) gives
the best decoherence. Larger exclusion volume helps. Z-leakage
is real but modest.

## Five structural conclusions

### 1. The gap is about node absence
Edge suppression (cross-channel penalty) does not change S_norm.
Amplitude penalty kills throughput rather than creating separation.
Only removing nodes from the gap region creates which-path information.

### 2. The gap creates information, not preserves it
Node-level distinguishability |D| is zero on uniform DAGs. The hard
gap creates the which-path information that the CL bath then measures.
This is a chicken-and-egg: no local observable exists to threshold on
before the gap exists.

### 3. The gap is topologically robust
Angled gaps (up to slope 0.5), partial gaps (50% coverage), and
gaps with up to 5 bridge nodes per layer all preserve decoherence.
The gap doesn't need to be perpendicular, complete, or perfectly sealed.

### 4. Larger exclusion helps
Cylindrical gap (excluding a tube in y-z) outperforms 1D gap
(excluding a band in y only). More excluded volume means less
cross-channel amplitude leakage.

### 5. Degradation is gradual
Filling the gap with nodes produces smooth pur_cl increase with no
sharp transition. The gap is a quantitative mechanism: more gap
means more decoherence.

## Implications for the project

The gap cannot be generated from local amplitude-based rules because
the information it creates (which-path distinguishability) does not
exist before the gap does. This is a **topological boundary condition**
on the allowed event space.

The robustness findings (conclusions 3-5) are physically interesting:
the gap doesn't need fine-tuning. It works when tilted, partial,
leaky, or extended to higher codimension. This suggests the relevant
feature is **channel separation** (a topological property) rather than
**gap geometry** (a metric property).

The remaining open question: can channel separation be reframed as
a **selection rule on event persistence** (axiom 2) rather than an
imposed geometric constraint? The D-threshold experiment (Exp 6)
shows this cannot be done via amplitude-based observables on uniform
graphs. A different observable — perhaps topological (path connectivity,
community structure) rather than amplitude-based — would be needed.

## Scripts

| Script | Experiment |
|--------|-----------|
| gap_stability_perturbation.py | Exp 1 |
| gap_tapered_profile.py | Exp 2 |
| gap_tension_stability.py | Exp 5a, 5b |
| gap_cross_channel_penalty.py | Exp 5c |
| gap_penalty_scaling.py | Exp 5b scaling |
| gap_node_persistence.py | Exp 6 |
| gap_topology_variants.py | Exp 3 |
| gap_codimension.py | Exp 4 |
