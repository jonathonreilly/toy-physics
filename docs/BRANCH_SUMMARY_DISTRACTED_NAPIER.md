# Branch Summary: claude/distracted-napier

**Date:** 2026-04-04
**Focus:** Continuum limit and dimension-dependent kernel

## Key Results

### 1. 3D gravity with 1/L kernel is a LATTICE ARTIFACT
The 3D dense lattice 10/10 card at h=1.0 showed TOWARD gravity, but
it collapses to AWAY at h=0.5. The gravity did not survive refinement.
(Script: `lattice_2d3d_continuum_check.py`)

### 2. 2D gravity CONVERGES genuinely
TOWARD strengthens h=1.0→0.25. MI→0.95, d_TV→0.99, decoherence→50%.
Distance tail b^(-1.08) matches 2+1D prediction of 1/b.
Born: machine precision at all h.
(Script: `lattice_nn_continuum.py`)

### 3. Dimension-dependent kernel: 1/L^(d-1) is uniquely selected
Confirmed across three dimensions:
- 2D: 1/L — gravity persists and strengthens with L
- 3D: 1/L^2 — gravity persists and strengthens with L; 1/L dies
- 4D: 1/L^3 — gravity persists and strengthens with L; 1/L^2 weakens

Selection mechanism: p=d-1 is the boundary between "beam too spread"
(p<d-1, T_eff→const) and "amplitude overflows" (p>d-1, T_eff→exp).
The p=d-1 norm grows logarithmically — marginally divergent.
(Scripts: `lattice_3d_l2_fast.py`, `lattice_4d_kernel_test.py`,
`transfer_norm_and_born.py`)

### 4. RG scaling stabilizes gravity magnitude
s(h) = s₀ × h^0.92 keeps deflection finite as h→0.
Distance exponent is INDEPENDENT of field strength — geometric property.
(Inline test, documented in sanity audit)

### 5. Born rule holds at all dimensions and kernel powers
- 2D 1/L: 2.3e-16
- 3D 1/L^2: 4.0e-15
- 4D 1/L^3: 1.3e-15

### 6. Kernel does NOT transfer to random DAGs
On random/mirror DAGs, all kernel powers give similar (noisy) gravity.
The dimension-dependent kernel is lattice-specific.
(Script: `dag_kernel_transfer.py`)

## Sanity Audit
Verdict: SUSPICIOUS (weak)
- FLAG 1 (axiom fork): Softened — 3-dimension empirical selection
- FLAG 2 (diverging gravity): Resolved — RG scaling works
- FLAG 3 (sign discontinuity): Inherent — lattice entering scaling regime

## Scripts Created
| Script | Purpose |
|--------|---------|
| `lattice_2d3d_continuum_check.py` | 2D vs 3D gravity refinement |
| `lattice_2d_continuum_distance.py` | 2D distance law convergence |
| `lattice_3d_continuum_convergence.py` | 3D continuum (negative with 1/L) |
| `lattice_3d_fixes.py` | 5 fix strategies compared |
| `lattice_3d_tapered_card.py` | Tapered lattice (TOWARD but breaks distance) |
| `lattice_3d_ytaper_card.py` | Y-only taper (ALL AWAY) |
| `lattice_3d_kernel_l2.py` | First 1/L^2 test |
| `lattice_3d_l2_numpy.py` | Numpy-optimized 1/L^2 |
| `lattice_3d_l2_fast.py` | Layer-by-layer with h^2 measure |
| `lattice_3d_l2_wide.py` | Wide lattice distance law |
| `lattice_4d_kernel_test.py` | 4D 1/L^3 prediction test |
| `transfer_norm_and_born.py` | Transfer norm + 4D Born |
| `dag_kernel_transfer.py` | Kernel transfer to random DAGs |

## Merge Notes
This branch is ready to merge. It contributes:
- Negative result: 3D 1/L gravity is artifact (essential for honesty)
- Positive result: 1/L^(d-1) kernel fixes 3D and 4D gravity
- Transfer norm theory explaining the selection
- Born verification at all dimensions
- Honest non-transfer to random DAGs
