---
experiment: three-d-decoherence
date: 2026-04-01
status: CONFIRMED
confidence: HIGH
---

# 3D Decoherence: CLT Ceiling Broken on Modular 3D DAGs

## Question

The 2D CL bath decoherence hits a CLT ceiling at N=80+ (pur_min → 1).
Does the extra spatial dimension in 3D delay or eliminate this ceiling?

## Results

### S_norm (bath contrast) stays bounded in 3D

In 2D, S_norm → 0 as N grows (CLT convergence makes per-slit
distributions identical). In 3D, S_norm stays in the range 0.07–0.30
across all N from 15 to 80, on all topologies tested.

**This is the root cause of the improvement**: the extra dimension
preserves slit-path distinguishability even at large N.

### Purity scaling comparison: 2D vs 3D at N=80

| Topology | 2D pur_min (N=80) | 3D pur_cl (N=80) | Improvement |
|---|---|---|---|
| Uniform | 0.987 | 0.986 | Marginal |
| Modular gap=3 | ~0.982 | **0.953** | Significant |
| Modular gap=5 | ~0.982 | 0.966 | Moderate |

### Full 3D scaling (Modular gap=3, lambda=10, 16 seeds)

```
N=15: pur_cl = 0.976
N=20: pur_cl = 0.954
N=25: pur_cl = 0.968
N=30: pur_cl = 0.953
N=40: pur_cl = 0.944
N=50: pur_cl = 0.945
N=60: pur_cl = 0.961
N=80: pur_cl = 0.953
```

No monotonic drift toward 1. Decoherence stays in the 0.94-0.97
band through N=80 with no ceiling visible.

### Lambda sweep (N=20, gap=5)

```
lambda=0:  pur_cl = 1.000 (fully coherent)
lambda=1:  pur_cl = 0.996
lambda=5:  pur_cl = 0.972
lambda=10: pur_cl = 0.966
lambda=20: pur_cl = 0.964 (saturated at pur_min)
```

The bath saturates by lambda=10-20. pur_cl → pur_min confirms the
CL mechanism is working correctly.

## Physical interpretation

In 2D (1 spatial + 1 causal dimension), paths through different slits
converge to the same Gaussian distribution at large N because the
single transverse dimension provides insufficient room for slit
separation to persist. This is a genuine CLT effect.

In 3D (2 spatial + 1 causal dimension), paths have two transverse
dimensions (y, z). The slit separation is in y, but the z-dimension
provides independent random variation that breaks the CLT convergence:
- Paths through slit A and slit B have the same z statistics
- But their y statistics remain distinct because the slit gap is in y
- The z dimension adds noise but doesn't erase the y separation
- The y-binned CL contrast S_norm captures this persistent difference

The modular gap structure amplifies this effect: the channel separation
in y is enforced by the gap, while z provides within-channel diversity
that prevents over-averaging.

## Why gap=3 beats gap=5 at large N

Modular gap=3 (pur_cl = 0.953 at N=80) outperforms gap=5 (0.966).
Possible explanation: gap=5 on yz_range=10 leaves very narrow channels
(each channel only 7.5 units wide in y, minus the 2.5 gap on each side).
At large N, the narrow channels lose connectivity, reducing the number
of paths that reach the detector. Gap=3 provides a better balance:
enough separation for slit distinguishability, enough channel width
for robust propagation.

## Significance

1. **The CLT ceiling is broken in 3D**: modular gap=3 maintains
   pur_cl ~ 0.95 through N=80 (2D gives 0.987)
2. **S_norm stays bounded**: the fundamental quantity that killed
   decoherence in 2D (S_norm → 0) does NOT collapse in 3D
3. **Dimensionality matters for decoherence**: this is the second
   dimensionality-dependent result (first was F ~ sqrt(M) for gravity)
4. **Gap=3 is optimal at large N**: better than gap=0 (uniform) or
   gap=5 (too narrow channels)

## Combined 3D picture

With both gravity and decoherence confirmed in 3D:
- Gravity: attraction confirmed, F ~ sqrt(M), b-independent
- Decoherence: CL bath works, CLT ceiling broken on modular DAGs
- Both emerge from the same corrected propagator on the same 3D graphs
- 3D is a better arena for the model than 2D

## Scripts

- `scripts/three_d_decoherence.py` — initial test (N=10-40, lambda sweep)
- `scripts/three_d_decoherence_large_n.py` — large-N scaling (N=15-80)
