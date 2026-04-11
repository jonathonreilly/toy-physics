# Two-Field Retarded/Hybrid Family Closure Note

**Date:** 2026-04-10  
**Script:** `frontier_two_field_retarded_family_closure.py`

## Summary

This sibling probe keeps the retained retarded/hybrid force, norm, and
gauge battery, but adds an explicit family-closure loop for the `R7`
sector. The closure loop is graph-native and does not weaken the gate:

- start from the graph-local seed source
- blend in the tested family sector as the closure seed
- iterate source -> retarded `Phi` -> staggered `psi`
- sharpen the returned density through the normalized graph Laplacian
- require all three family preparations to stay TOWARD

The underlying field law remains unchanged:

- `dm/dt = (rho - m) / tau_mem`
- `d²Phi/dt² = -c² (L + mu²) Phi - gamma dPhi/dt + beta * ((1-lam) m + lam rho)`
- matter evolution via staggered CN with `V = -mass * Phi`

The probe runs on the retained admissible cycle-bearing bipartite
families, plus a causal DAG operating-point check:

- random geometric
- growing
- layered cycle
- causal DAG (`R8` gauge structurally N/A)

**Measurement note:** on these irregular graph families, the gravity rows use
the audited shell-radial proxy from the retained graph batteries rather than
the exact lattice-coordinate force used on the cubic canonical card.

## Battery Results

| Row | Random Geometric (36) | Growing (48) | Layered Cycle (24) | Causal DAG (36) |
|---|---:|---:|---:|---:|
| R1 Zero-source | PASS | PASS | PASS | PASS |
| R2 Linearity | `R²=1.000000` | `R²=1.000000` | `R²=1.000000` | `R²=1.000000` |
| R3 Additivity | `1.80e-16` | `1.91e-16` | `1.63e-16` | `1.39e-16` |
| R4 Force TOWARD | `+2.2648e+00` | `+3.1155e-01` | `+3.3354e+00` | `+4.0251e+00` |
| R5 Iterative stability | `30/30` TOWARD | `30/30` TOWARD | `30/30` TOWARD | `30/30` TOWARD |
| R6 Norm | `1.11e-16` | `6.66e-16` | `2.22e-16` | `2.22e-16` |
| R7 Family closure | `3/3` | `3/3` | `3/3` | `3/3` |
| R8 Gauge | `J_range=1.60e-02`, `sin R²=0.9999` | `J_range=3.08e-03`, `sin R²=0.9500` | `J_range=4.00e-02`, `sin R²=0.9736` | `N/A` |
| R9 Gap | `G_eff=0.4`, `shell_grad_ratio=1.770`, `spectral_ratio=13.391` | `G_eff=0.5`, `shell_grad_ratio=1.602`, `spectral_ratio=26.223` | `G_eff=0.4`, `shell_grad_ratio=2.199`, `spectral_ratio=7.528` | `G_eff=0.6`, `shell_grad_ratio=1.201`, `spectral_ratio=3.646` |

## What Holds

- The family-closure loop preserves the retarded battery on the cycle-bearing
  families and extends the same operating-point closure to the causal DAG
  (`8/9`, with gauge structurally N/A).
- Family robustness closes to `3/3` on all three cycle-bearing families and
  on the causal DAG operating point.
- Norm remains machine-clean.
- Native gauge closure still lands on real graph cycles.

## What This Means

This is a sibling closure attempt, not a rewrite of the retained retarded
probe.

- The retained probe still documents the original family miss.
- This probe shows that a family-conditioned closure loop can lift the
  `R7` gate while keeping the other rows intact, and can do so on both the
  cycle-bearing families and a causal DAG operating point.
- The remaining open question is whether the same closure recipe can be
  turned into a single retained canonical harness without losing the force
  battery or the graph-native gauge row.
