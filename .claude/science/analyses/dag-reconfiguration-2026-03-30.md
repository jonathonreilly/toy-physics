# Analysis: DAG Reconfiguration Measurement

## Date
2026-03-30

## Source
- Log: `logs/2026-03-30-dag-reconfiguration-measure.txt`

## Key Findings

### 1. I₃ magnitude correlates with DAG change magnitude

| Config | I₃/P | edge_change% | max_Δt | shifted_nodes% |
|--------|------|-------------|--------|---------------|
| Close | 9.2×10¹ | 1.28% | 1.17 | 10.7% |
| Symmetric | 1.7×10⁶ | 2.09% | 2.34 | 10.2% |
| Wide | 4.6×10⁹ | 2.57% | 3.51 | 9.0% |

I₃ grows by 8 orders of magnitude while DAG change grows by only 2×. The relationship is highly nonlinear — small DAG changes produce enormous probability differences because the path-sum amplitudes scale exponentially with the grid.

### 2. Adding one slit changes ~1 node but shifts ~10% of all arrival times

Opening a slit adds 1 node and ~8 edges to the ~1484-edge DAG. But arrival times propagate: 9-11% of all nodes get shifted arrival times. The DAG reconfiguration is NONLOCAL — a local topology change affects distant parts of the network.

### 3. The B slit (center, y=0) causes the most disruption

Adding slit B (center) consistently causes more change than adding A or C (off-center):
- AC → ABC (add B): 16-25% shifted nodes
- AB → ABC (add C): 9-11% shifted nodes

The center slit sits on the main propagation axis from source (1,0), so opening it creates the shortest new paths, maximally shifting arrival times downstream.

### 4. Going from 1 slit to 3 slits shifts ~33-37% of nodes

A → ABC changes 28-37% of arrival times, vs AB → ABC changing only 9-11%. The DAG reconfiguration is roughly additive in slit count but sublinear.

## Significance

This quantifies the mechanism behind the original Sorkin I₃ ≠ 0: adding/removing barrier nodes creates nonlocal arrival-time shifts that reconfigure the causal DAG. The effect is small topologically (~2% edge change) but amplified exponentially in the path-sum amplitudes, explaining why I₃/P reaches 10⁹ while edge changes are only a few percent.

This is a distinctly discrete-network phenomenon: on a continuum, opening a new aperture adds paths without changing existing ones. On the discrete causal DAG, it changes the temporal ordering of events across the entire network.
