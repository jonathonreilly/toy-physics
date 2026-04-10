# Cycle-Bearing Graph Battery — Retained Note

**Date:** 2026-04-10
**Script:** `frontier_staggered_cycle_battery.py`

## Summary

The staggered fermion + potential gravity architecture passes a 9-row
battery on two cycle-bearing bipartite graph families:

| Row | Random Geometric (36) | Growing (48) |
|-----|:---:|:---:|
| B1 Zero-source | exact | exact |
| B2 Linearity | R²=1.000 | R²=1.000 |
| B3 Additivity | <2e-16 | <2e-16 |
| B4 Force TOWARD | ✅ | ✅ |
| B5 Iterative (15 steps) | 15/15 TW | 15/15 TW |
| B6 Norm | <5e-16 | <5e-16 |
| B7 Families (3/3) | ✅ | ✅ |
| B8 Native gauge | R²=0.9999 | R²=0.9500 |
| B9 Force-gap (characterization) | G_eff=32 | G_eff=178 |

## What Works

- **Force sign**: TOWARD on all families, all iterations, both graph types.
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

## Remaining Caveats

1. **Cycle-bearing families only** — the layered cycle graph needs to be
   integrated into the battery harness.
2. **Force is primary** — no centroid rows. The centroid has a period-4
   oscillation on staggered periodic lattices.
3. **B9 is characterization, not pass/fail** — the gap is reported but
   doesn't gate the battery.
