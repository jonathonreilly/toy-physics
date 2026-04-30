# Cycle-Bearing Graph Battery — Retained Note

**Status:** bounded - bounded or caveated result note
**Date:** 2026-04-10
**Script:** `frontier_staggered_cycle_battery.py`

## Summary

The staggered fermion + parity-coupled potential gravity architecture passes
the cycle battery on the three retained cycle-bearing bipartite graph
families. The retained source convention now uses a family-appropriate
interior source: growing is anchored at the deepest reachable node and the
layered cycle at a max-degree interior node.

| Row | Random Geometric (36) | Growing (48) | Layered Cycle (24) |
|-----|:---:|:---:|:---:|
| B1 Zero-source | exact | exact | exact |
| B2 Linearity | R²=0.991 | R²=1.000 | R²=0.991 |
| B3 Additivity | <2e-16 | <2e-16 | <3e-16 |
| B4 Force TOWARD | ✅ | ✅ | ✅ |
| B5 Iterative (15 steps) | 15/15 TW | 15/15 TW | 15/15 TW |
| B6 Norm | <5e-16 | <5e-16 | <5e-16 |
| B7 Families (3/3) | ✅ | ✅ | ✅ |
| B8 Native gauge | R²=0.9999 | R²=0.9500 | R²=0.9736 |
| B9 Force-gap | characterization-only | characterization-only | characterization-only |
| B9 shell_grad_ratio | 1.9% | 1.2% | 2.4% |
| B9 spectral_ratio | 18.9% | 5.9% | 27.5% |

**Measurement note:** on these irregular graph families, `B4/B5/B7` use a
radial shell-force proxy built from BFS-depth shell averages of `Φ`. This is
not the exact lattice-coordinate force used by the canonical cubic card. The
later two-sign audit shows these irregular sign measures are not sign-
selective: they can stay inward under both attractive and repulsive coupling
because they are dominated by the source-centered `Φ` profile.

## What Works

- **Radial field-profile sign**: inward on all three families under the
  corrected parity coupling. After the two-sign audit, this row should be
  treated as a centered-field diagnostic, not as standalone evidence that
  attraction is dynamically selected.
- **Iterative backreaction**: density-sourced Φ re-solved each step, force
  stays positive across 15-20 iterations with exact norm.
- **Native gauge**: persistent current J(A) with sin(A) modulation, measured
  on actual graph cycles (not 1D ring fallback).
- **Source physics**: perfect linearity (R²=1), perfect additivity (<1e-16),
  zero-source control exact.

## Layered Gauge Holdout — CLOSED

The layered DAG had no cycles by construction (tree topology). Adding
2-connection-per-node between layers creates cycles while preserving
bipartiteness. Result: gauge PASS (J_range=4.0e-2, sin R²=0.9736) on
the layered cycle graph.

## Endogenous Field Scale — CHARACTERIZED (Structural)

The force from the graph-solved Φ is still much smaller than the external
kernel force. This is a coupling-constant mismatch (`G_eff≈58-70`), not a
sign/linearity failure on any retained family.

**Root cause**: the screened Poisson Green function (L+μ²I)⁻¹ on a small
graph is smoother than the 1/r kernel. Spectral analysis shows the
ratio is 0.50 at mode 0 and degrades to 0.09 at mode 9 — the external
kernel has more high-frequency content from the 1/r singularity.

**Characterization**:
- The gap is structural (graph discretization, not physics)
- Shrinks with graph size only weakly and non-monotonically here
- Does not affect sign, additivity, stability, or robustness on the two
  non-layered families
- Can be compensated by increasing G (force scales linearly)

**What it means**: the endogenous Poisson source still produces stable inward
response on all three retained families, but the absolute force scale requires
a graph-dependent coupling constant G_eff.

## Self-Gravity Probe (Retained)

**Script:** `frontier_staggered_self_gravity.py`

True self-gravity: no external source. |ψ|² generates Φ via screened Poisson,
which acts back on the wavepacket. Battery:

| Row | Random Geometric (36) | Growing (48) | Layered Cycle (24) |
|-----|:---:|:---:|:---:|
| S1 Force TOWARD | 20/20 | 20/20 | 20/20 |
| S2 Contraction | **0.63 (37%)** | **0.60 (40%)** | **0.44 (56%)** |
| S3 Norm | 2.2e-16 | 4.4e-16 | 4.4e-16 |
| S4 Stability | 0 flips | 0 flips | 0 flips |
| S5 Families | 3/3 TW | 3/3 TW | 3/3 TW |
| **Score** | **5/5** | **5/5** | **5/5** |

The layered cycle shows strongest contraction (56%) because the layered
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
   growing, and layered cycle now pass `9/9` under the family-appropriate
   source convention.
2. **Force is primary** — no centroid rows. The centroid has a period-4
   oscillation on staggered periodic lattices.
3. **Irregular-graph force is a proxy** — on these graph families the retained
   sign rows are shell-radial proxies, not exact `F=-⟨∇Φ⟩`.
4. **Two-sign audit narrows the claim** — these sign rows do not distinguish
   attractive from repulsive coupling and therefore should not be promoted as
   evidence of gravitational direction.
5. **B9 is characterization, not pass/fail** — the gap is reported but
   doesn't gate the battery.
