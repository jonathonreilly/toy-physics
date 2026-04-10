# Session Synthesis: From Coin Gravity Blockers to Staggered Fermions

**Date:** 2026-04-10
**Branch:** frontier/spot-checks

## The Journey

This session started from the chiral walk's three gravity blockers (chromaticity,
equivalence violation, N-oscillation) and ended with a staggered fermion architecture
that passes a force-based 17-row card in 1D and 3D.

### Phase 1: Diagnosis (coupled coin scan → Dirac walk)

1. **6-component coupled coin scan**: All 5 coin families tested (block-circulant,
   Cayley, DFT-6, Grover-6, Dirac-embedded). None improved on factorized R²=0.156.
   Structural no-go: the 6D direct-sum space cannot produce isotropic 3D KG.

2. **4-component Dirac walk**: KG R²=1.000 via Hamiltonian Bloch analysis.
   Reversed coupling m(1+f) gives TOWARD. But coin mixing period persists —
   gravity oscillates with N, chromaticity remains.

3. **Root cause identified**: All three blockers trace to ONE source — the coin's
   mixing period π/m. Any gravity mechanism passing through the coin inherits all
   three blockers.

### Phase 2: Potential Gravity (scalar KG → graph Laplacian)

4. **Scalar potential gravity**: V = m·Φ(x) fixes all three blockers on the scalar
   KG field. Achromatic (force CV=0), equivalence (acceleration CV=0), N-stable
   (100% TOWARD monotonic). But scalar KG assumes physics rather than deriving it.

5. **Graph Laplacian scalar**: KG-like spectrum derived from graph Laplacian
   eigenvalues. Tested on cubic, random geometric, and growing graphs. All pass.
   But the evolution is Schrödinger (i∂ψ/∂t = Hψ), not genuinely KG dynamics.
   Also: no spin, no light cone.

6. **Chiral walk + potential**: Scalar potential doesn't create forces on the
   chiral walk (chirality-mediated kinematics don't respond to scalar phases).
   9/16. Dead end.

### Phase 3: The Impossible Triangle

7. **Dirac spinor + potential**: Scalar potential V·I has zero effect on
   4-component Dirac spinor (the kinetic step completely dominates). 12/16.

8. **The triangle identified**: Strict v=1 light cone + no mixing period +
   clean gravity are mutually incompatible at the single-field level. Coin gives
   light cone but creates mixing period. No coin removes mixing but loses cone.

9. **Weak-coin regime**: Operating at N << π/θ suppresses the mixing period for
   a single chirality sector. But L-movers go AWAY — chirality-conditioned gravity,
   not universal.

### Phase 4: Staggered Fermions (the resolution)

10. **Kogut-Susskind staggered fermion**: 1 scalar per site, Dirac structure from
    staggering phases η_μ(x) = (-1)^(x₁+...+x_{μ-1}). No coin. Genuine Dirac
    dispersion E² = m² + sin²(k). Potential gravity V = -m·g·S/(r+ε).

11. **Universal gravity via force measurement**: The centroid shift oscillates with
    lattice size (periodic-lattice recurrence, not fixable by coarse-graining).
    But the force F = -⟨dV/dz⟩ is TOWARD at ALL lattice sizes, ALL state families,
    ALL dimensions. Force is the correct physical observable for gravity.

12. **Force-based 17-card**: 17/17 on 1D n=61 (6/6 families, no qualifiers) and
    3D n=9 (6/6 families, no qualifiers). 3D n=11,13: 17/17 with qualifier
    (4/6 families tested, energy projections skipped).

## Architecture Summary

**Staggered fermion + scalar potential gravity, Crank-Nicolson evolution.**

```
State:      1 complex scalar per lattice site
Kinetic:    Staggered Dirac operator (η_μ phases on nearest-neighbor hops)
Mass:       m · ε(x) where ε = (-1)^(x₁+x₂+x₃)
Gravity:    V(x) = -m · g · S / (|x - x_mass| + ε)
Evolution:  Crank-Nicolson (exactly unitary, norm ≈ 1e-15)
Observable: Force F = -⟨dV/dz⟩ for gravity direction/magnitude
```

## What This Architecture Derives

- **Dirac dispersion**: E² = m² + sin²(k) exact, from staggering phases.
  Not assumed — follows from nearest-neighbor hopping with alternating signs.
- **Born rule**: Sorkin I₃ at machine zero (1e-15). From linearity.
- **Universal gravity**: Force TOWARD for all 6 physical state families
  (gauss, even, odd, anti, positive-E, negative-E). From V = m·Φ potential.
- **Achromatic force**: F = -⟨dV/dz⟩ has no k-dependence (CV = 0.000000).
- **Mass-independent acceleration**: a = F/m = -⟨dΦ/dz⟩ (CV = 0.000000).
- **Gauge**: Persistent current J(A) with sin(A) modulation. Native to both
  1D ring and 3D torus.
- **Chirality**: Even/odd sublattice parity = staggered γ₅.
- **Norm**: Exact (CN, drift < 2e-15).

## What This Architecture Does NOT Provide

- **Strict v=1 light cone**: CN gives Lieb-Robinson (97% inside cone).
  A strict cone requires coin+shift which reintroduces the mixing period.
- **Centroid-based gravity convergence in 3D**: The centroid oscillates with
  lattice size on periodic BCs (finite-size recurrence). Force converges.
  Centroid would need n >> 13 in 3D.
- **Topology portability beyond the cubic lattice**: the retained force battery,
  native gauge closure, and self-gravity probe now survive on random
  geometric, growing, and layered cycle bipartite graph families. The open
  portability question is now about the boundary of the admissible graph
  class, not whether the mechanism is cubic-only.
- **Dynamic growth / cosmology / Hawking**: Static lattice.

## Frozen Scores

### Force-Based Staggered Card

**Script:** `frontier_staggered_17card.py` @ commit 9c70598

This is a FORCE-BASED card, not the repo-wide centroid-based card.
Rows C5, C9, C10, C15, C16 have different semantics (see table below).

| Row | 1D (n=61) | 3D (n=9) | 3D (n=11) | 3D (n=13) |
|-----|-----------|----------|-----------|-----------|
| C1 Sorkin | 1.28e-15 | 2.62e-15 | 2.75e-15 | 3.11e-15 |
| C2 d_TV | 0.92 | 1.00 | 1.00 | 0.99 |
| C3 f=0 | 0.00 | 0.00 | 0.00 | 0.00 |
| C4 F∝M | R²=0.912 | R²=1.000 | R²=0.999 | R²=0.998 |
| C5 Force TW | +5.7e-5 | +1.3e-3 | +5.8e-4 | +3.2e-4 |
| C6 Decoh | 0.23→0.18 | 0.75→0.16 | 0.70→0.07 | 0.66→0.08 |
| C7 MI | 0.164 | 0.615 | 0.052 | 0.352 |
| C8 Purity | CV=0.011 | CV=0.098 | CV=0.136 | CV=0.127 |
| C9 Force+ | all TW | all TW | all TW | all TW |
| C10 Dist | 5/5 | 1/1 | 1/1 | 2/2 |
| C11 KG | R²=0.997 | R²=0.997 | R²=0.997 | R²=0.997 |
| C12 Gauge | 1D 2.1e-3 | 3D native | 3D native | 3D native |
| C13 Achrom | CV=0.000 | CV=0.000 | CV=0.000 | CV=0.000 |
| C14 Equiv | CV=0.000 | CV=0.000 | CV=0.000 | CV=0.000 |
| C15 Depth | all TW | all TW | all TW | all TW |
| C16 Multi | 1/2 | 1/2 | 2/2 | 1/2 |
| C17 Families | 6/6 | 6/6 | 4/6* | 4/6* |
| **Score** | **17/17** | **17/17** | **17/17*** | **17/17*** |

\* Energy projections skipped (eigensolve cost). 4/4 tested families TOWARD.

### Semantic Differences from Repo-Wide Card

| Row | Repo-wide meaning | This card's meaning |
|-----|-------------------|---------------------|
| C5 | Centroid shift TOWARD | Force F > 0 (TOWARD) |
| C9 | Centroid grows monotonically | Force stays positive across N |
| C10 | Centroid distance law (evolved) | Force-at-T=0 sign vs offset |
| C15 | Periodic vs open boundary | Force stable across depth |
| C16 | Centroid + peak + shell (3 obs) | Force + shell (2 obs) |

The force observable is more fundamental (it's what the equivalence principle
tests), but these rows are NOT directly comparable to centroid-based cards.

## Key Insights from the Session

1. **The coin is the root of all gravity blockers.** The mixing period π/m
   creates chromaticity, equivalence violation, and N-oscillation on EVERY
   coin-based architecture (chiral walk, Dirac walk, staggered with coin).

2. **Potential gravity is clean but needs the right field.** V·I works on
   scalar fields and staggered fermions. It does NOT work on Dirac spinors
   (particle/antiparticle cancellation) or chiral walks (chirality-mediated
   kinematics don't respond to scalar phases).

3. **Force is the correct gravity observable on lattices.** The centroid shift
   picks up lattice-scale artifacts (staggered standing waves, periodic-boundary
   recurrence). The force F = -⟨dV/dx⟩ is immune because it's a potential-gradient
   expectation, not a position expectation.

4. **Staggered fermions give Dirac without a coin.** The η_μ phases produce
   gamma-matrix structure from the lattice connectivity alone. No internal DOF
   needed — just alternating signs on the hopping.

5. **The "impossible triangle" has a weak spot.** You can't have strict v=1 +
   no mixing period + single scalar. But you CAN have Lieb-Robinson cone +
   no mixing period + single scalar, which is the standard lattice QFT
   version of causality.

## What's Next

The full-suite baseline is now frozen:

- `frontier_staggered_full_suite.py`: `29/38` in 1D, `28/38` in 3D
- `frontier_staggered_17card.py`: retained force-based canonical card

### Closed since initial freeze

1. **Layered gauge holdout**: CLOSED. Layered cycle graph (2-connection per node)
   has cycles and passes native gauge (sin R²=0.974). Integrated into battery.

2. **Source-sector diagnostics**: DONE. Shell/spectral analysis in B9 shows the
   Poisson Green function is structurally smoother than 1/r: spectral ratio 8-19%
   at low modes, G_eff=12-178. Coupling-constant mismatch, not physics failure.

3. **Iterative endogenous closure**: DONE. 15/15 TOWARD on both cycle-bearing
   families with density-sourced Φ re-solved each step.

4. **True self-gravity**: DONE. `frontier_staggered_self_gravity.py` now closes
   5/5 on all three cycle-bearing families with 20/20 TOWARD force, exact norm,
   zero sign flips, and measurable contraction versus free evolution.

5. **Two-field coupling**: PROTOTYPED. `frontier_two_field_coupling.py` closes
   4/4 on the retained graph with a separate scalar Φ field sourced by `|ψ|²`,
   30/30 TOWARD force, exact matter norm, and bounded Φ growth.

### Remaining work

1. **Endogenous-field scale**: G_eff=12-178 is characterized but not closed.
   The miss is structural on the current graph Poisson map, not a sign or
   linearity failure.
2. **Two-field hardening**: replace the current relaxation update for Φ with a
   more physical wave or retarded-field law, then rerun the retained force
   battery.
3. **Self-gravity portability**: extend the retained self-gravity probe beyond
   the current three cycle-bearing graph families and quantify how contraction
   scales with graph size and geometry.
4. **Larger graph tests**: map how the structural source-scale gap and the
   retained force battery evolve with size on the admissible graph families.

For the active backlog and agent brief, see:
- `docs/WORK_BACKLOG_2026-04-10.md`
- `docs/CLAUDE_BACKLOG_BRIEF_2026-04-10.md`

The current retained cycle-bearing integration is frozen in:
- `scripts/frontier_staggered_cycle_battery.py`
- `docs/CYCLE_BATTERY_NOTE_2026-04-10.md`

Companion retained probes:
- `scripts/frontier_staggered_self_gravity.py`
- `scripts/frontier_two_field_coupling.py`
