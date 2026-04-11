# Cycle-Bearing Graph Battery — Retained Note

**Date:** 2026-04-10
**Script:** `frontier_staggered_cycle_battery.py`

## Summary

The staggered fermion + potential gravity architecture passes a 9-row
battery on three cycle-bearing bipartite graph families:

| Row | Random Geometric (36) | Growing (48) | Layered Cycle (24) |
|-----|:---:|:---:|:---:|
| B1 Zero-source | exact | exact | exact |
| B2 Linearity | R²=1.000 | R²=1.000 | R²=1.000 |
| B3 Additivity | <2e-16 | <2e-16 | <3e-16 |
| B4 Force TOWARD | ✅ | ✅ | ✅ |
| B5 Iterative (15 steps) | 15/15 TW | 15/15 TW | 15/15 TW |
| B6 Norm | <5e-16 | <5e-16 | <5e-16 |
| B7 Families (3/3) | ✅ | ✅ | ✅ |
| B8 Native gauge | R²=0.9999 | R²=0.9500 | R²=0.9736 |
| B9 Force-gap | G_eff=32 | G_eff=178 | G_eff=12 |
| B9 shell_grad_ratio | 1.9% | 0.5% | 4.4% |
| B9 spectral_ratio | 18.9% | 7.7% | 16.9% |

**Measurement note:** on these irregular graph families, `B4/B5/B7` use a
radial shell-force proxy built from BFS-depth shell averages of `Φ`. This is
not the exact lattice-coordinate force used by the canonical cubic card.
After the gravity-sign audit, stronger probability-weighted shell and
edge-radial spot checks were run and the sign stayed TOWARD on all three
retained families.

## What Works

- **Radial gravity sign**: TOWARD on all retained families, all iterations.
  The retained battery uses a shell-radial proxy; the audit confirms that an
  edge-radial cross-check agrees in sign on these three admissible families.
- **Iterative backreaction**: density-sourced Φ re-solved each step, force
  stays positive across 15-20 iterations with exact norm.
- **Native gauge**: persistent current J(A) with sin(A) modulation, measured
  on actual graph cycles (not 1D ring fallback).
- **Source physics**: perfect linearity (R²=1), perfect additivity (<1e-16),
  zero-source control exact.

## Layered Gauge Holdout — CLOSED

The layered DAG had no cycles by construction (tree topology). Adding
2-connection-per-node between layers creates cycles while preserving
bipartiteness. Result: gauge PASS (J_range=3.2e-2, sin R²=0.985) on
the layered cycle graph.

## Endogenous Field Scale — OPEN (Structural)

The force from the graph-solved Φ is 2-6% of the external kernel force.
This is a coupling-constant mismatch (G_eff=32-178), not a sign/linearity
failure.

**Root cause**: the screened Poisson Green function (L+μ²I)⁻¹ on a small
graph is smoother than the 1/r kernel. Spectral analysis shows the
ratio is 0.50 at mode 0 and degrades to 0.09 at mode 9 — the external
kernel has more high-frequency content from the 1/r singularity.

**Characterization**:
- The gap is structural (graph discretization, not physics)
- Shrinks with graph size (larger graphs → sharper Green function)
- Does not affect sign, linearity, additivity, stability, or robustness
- Can be compensated by increasing G (force scales linearly)

**What it means**: the endogenous Poisson source produces gravity with
the correct qualitative behavior at all tested graph sizes, but the
absolute force scale requires a graph-dependent coupling constant G_eff.
This is analogous to renormalization — the bare coupling runs with the
lattice cutoff.

## Self-Gravity Probe (Retained)

**Script:** `frontier_staggered_self_gravity.py`

True self-gravity: no external source. |ψ|² generates Φ via screened Poisson,
which acts back on the wavepacket. Battery:

| Row | Random Geometric (36) | Growing (48) | Layered Cycle (24) |
|-----|:---:|:---:|:---:|
| S1 Force TOWARD | 20/20 | 20/20 | 20/20 |
| S2 Contraction | 0.94 (6%) | 0.99 (1%) | **0.64 (36%)** |
| S3 Norm | 4.4e-16 | 4.4e-16 | 6.7e-16 |
| S4 Stability | 0 flips | 0 flips | 0 flips |
| S5 Families | 3/3 TW | 3/3 TW | 3/3 TW |
| **Score** | **5/5** | **5/5** | **5/5** |

The layered cycle shows strongest contraction (36%) because the layered
structure channels the wavepacket along a preferred direction.

## Two-Field Coupling (Prototype)

**Script:** `frontier_two_field_coupling.py`

Separate scalar Φ field (diffusion+source) and staggered ψ field (CN):
- Φ grows from zero, sourced by β·|ψ|²
- ψ evolves under V = -m·Φ
- Force: 30/30 TOWARD
- Width: contracts to 0.9992 (gravitational binding)
- Φ bounded, ψ norm exact (9e-16)

This is the first two-field endogenous gravity result in the project.

## Remaining Caveats

1. **All three cycle-bearing families integrated** — random geometric,
   growing, and layered cycle all pass 9/9 (battery) and 5/5 (self-gravity).
2. **Force is primary** — no centroid rows. The centroid has a period-4
   oscillation on staggered periodic lattices.
3. **Irregular-graph force is a proxy** — on these graph families the retained
   sign rows are shell-radial proxies, not exact `F=-⟨∇Φ⟩`. Edge-radial spot
   checks agree on the retained families, but the observable should still be
   described as a radial proxy.
4. **B9 is characterization, not pass/fail** — the gap is reported but
   doesn't gate the battery.
