# Analysis: Irregular Network Interference

## Date
2026-03-30

## Source
- Log: `logs/2026-03-30-interference-irregular-network.txt`

## Key Findings

### 1. Record suppression is perfectly robust to grid irregularity
record_leak = 0.000000 at ALL perturbations (0.0 to 0.4), ALL seeds. The record mechanism's all-or-nothing suppression does not depend on grid regularity.

### 2. V(y=0) drops from 1.0 as perturbation increases — symmetry protection breaks
| pert | V(y=0) range across seeds |
|------|--------------------------|
| 0.0 | 1.000 (all seeds identical) |
| 0.1 | 0.914 - 0.986 |
| 0.2 | 0.415 - 0.942 |
| 0.3 | 0.035 - 0.989 |
| 0.4 | 0.100 - 0.779 |

Confirms that V(y=0)=1 was symmetry-protected on the regular grid. Perturbing edge lengths breaks path-length equality between slits → V drops.

### 3. Interference SURVIVES on irregular grids
Even at pert=0.4 (edges vary by ±40%), mean_V remains nonzero: 0.22 to 0.48 across seeds. The model's interference is not a regular-grid artifact — it's a genuine property of the path-sum that persists on irregular networks.

### 4. Visibility becomes stochastic at high perturbation
At pert=0.0: all seeds give identical results (deterministic).
At pert=0.3+: V varies dramatically between seeds. The specific random geometry determines the interference pattern. This is expected — each random realization creates a different path-length structure.

## Verdict
**Key result: interference and record suppression both survive grid irregularity.** The topological features (slit reachability, record suppression) are robust. The quantitative features (specific V values, symmetry at y=0) are geometry-dependent, as expected.
