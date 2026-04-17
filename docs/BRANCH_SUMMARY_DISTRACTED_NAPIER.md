# Branch Summary: claude/distracted-napier

**Date:** 2026-04-04
**Focus:** historical import memo for the continuum / dimension-dependent-kernel branch

This file is a branch-summary memo, not a canonical project-state note.

Use it as a historical import record only. For the current review-safe read of
the kernel branch on `main`, prefer:

- [`docs/CONTINUUM_CONVERGENCE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/CONTINUUM_CONVERGENCE_NOTE.md)
- [`docs/LATTICE_KERNEL_TRANSFER_NORM_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/LATTICE_KERNEL_TRANSFER_NORM_NOTE.md)
- [`docs/LATTICE_3D_L2_TAIL_STATS_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/LATTICE_3D_L2_TAIL_STATS_NOTE.md)

## Historical Branch Results

### 1. 3D gravity with the original 1/L kernel failed the refinement replay
The 3D dense lattice fixed-scale card at `h=1.0` showed TOWARD gravity, but
the corrected refinement replay on the same family flips that read negative by
`h=0.5`. This was the key negative result that reopened the propagator lane.
(Script: `lattice_2d3d_continuum_check.py`)

### 2. 2D ordered-lattice refinement remained the strongest retained success
TOWARD strengthens from `h=1.0` to `h=0.25`. `MI`, `d_TV`, and decoherence all
improve under refinement, and the 2D tail remains close to the expected
`1/b`-type falloff. Born stays at machine precision on the tested range.
(Scripts: `lattice_nn_continuum.py`, `lattice_2d_continuum_distance.py`)

### 3. The imported dimension-dependent-kernel branch became the strongest empirical persistence candidate on ordered lattices
The branch evidence suggested the following bounded pattern:
- 2D: `1/L` remains the strongest current persistence candidate
- 3D: `1/L^2` looks more persistent than `1/L` on the tested lattices
- 4D: `1/L^3` looks stronger than nearby lower powers on longer tested lattices

This was and remains an empirical persistence read, not a theorem of unique
selection. It also still needs reconciliation with the stricter local
transfer-norm probe already frozen on `main`.
(Scripts: `lattice_3d_l2_fast.py`, `lattice_4d_kernel_test.py`,
`transfer_norm_and_born.py`)

### 4. RG-style scaling looked promising but remained bounded
One exploratory lane suggested that a schedule of the form
`s(h) = s₀ × h^alpha` can keep the 3D inverse-square branch finite over the
tested refinement range. That result was useful enough to keep, but not strong
enough to promote as a closed RG theorem.

### 5. Born rule held at the tested dimensions and kernel powers
- 2D 1/L: 2.3e-16
- 3D 1/L^2: 4.0e-15
- 4D 1/L^3: 1.3e-15

### 6. Kernel transfer to random DAGs stayed negative
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
| `lattice_4d_kernel_test.py` | 4D kernel persistence comparison |
| `transfer_norm_and_born.py` | Transfer norm + 4D Born |
| `dag_kernel_transfer.py` | Kernel transfer to random DAGs |

## Historical Merge Notes
This branch contributed useful exploratory material to `main`, but it should
not be read as the canonical project state on its own. The most useful imports
were:
- the negative replay showing that refined 3D `1/L` does not hold up
- the stronger ordered-lattice persistence evidence for the `1/L^(d-1)` family
- Born checks at the tested dimensions
- the negative transfer result on random DAGs

For the current bounded read after cleanup, use the notes linked at the top of
this file instead of the historical branch language here.
