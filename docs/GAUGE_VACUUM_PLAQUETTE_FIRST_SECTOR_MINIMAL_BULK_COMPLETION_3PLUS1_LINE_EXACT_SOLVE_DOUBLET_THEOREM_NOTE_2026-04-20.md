# Gauge-Vacuum Plaquette First-Sector Minimal-Bulk Completion `3d+1` Exact-Solve Doublet Theorem

**Status:** bounded - bounded or caveated result note
**Date:** 2026-04-20 (originally); 2026-05-03 (audit-driven repair)

## Audit-driven repair (2026-05-03)

The 2026-05-03 audit (codex-fresh-audit-loop) flagged that the original
runner used 175 seeds (7×5×5) of `least_squares` to count roots in the
bounded positive-angle chart, which certifies only that two LOCAL
solutions exist with small residuals and nondegenerate Jacobians — not
that the bounded chart has no ADDITIONAL roots. The repair adds a
**dense Monte-Carlo + structured-grid root-count certificate**:

  [`scripts/gauge_vacuum_plaquette_doublet_dense_root_count_certificate_2026_05_03.py`](../scripts/gauge_vacuum_plaquette_doublet_dense_root_count_certificate_2026_05_03.py)

uses a 15×12×12 = 2160-point structured grid PLUS 1500 uniform-random
seeds (3660 seeds total, ~20× the original 175). Every converged seed
(60% of the 3660 reach |residual| < 1e-10) clusters onto exactly the
**same two distinct roots** the original runner found. No additional
cluster emerges from the dense seed bath. Per-cell volume is
~8.5e-3 rad³, vs the chart volume ~31 rad³.

The dense certificate is **empirical** evidence (high seed density →
no missed root cluster), not a symbolic proof of global
exhaustiveness. Strict symbolic root-count via resultants or interval
arithmetic remains genuine open work for a subsequent pass — the
target equation involves transcendental functions of three angles
(via `compressed_local_block_from_line`), so polynomial reduction
isn't immediate. Until then, the audit row records:

- Local exact-solve: original runner finds 2 nondegenerate roots
  (small residuals, well-conditioned Jacobians).
- Empirical global root-count: dense seed bath finds the same 2
  roots with no additional cluster.
- **Open**: symbolic / interval-arithmetic certificate of global
  exhaustiveness on the bounded chart.

The honest scope of the bounded theorem is therefore: **on the
selected least-positive-bulk Wilson branch, dense Monte-Carlo
exhaustion finds exactly two roots in the bounded positive-angle
chart**. The "exactly two" claim is empirically certified at much
higher confidence than the original sparse seeding, but is not yet
rigorously closed.

## Statement

On the selected least-positive-bulk Wilson branch, the retained `3d+1`
complement-line problem is solved on the bounded positive-angle chart by an
audited exact target equation whose isolated solution set contains exactly two
nondegenerate retained-line roots.

Those two chart solutions form the concrete orientation doublet later used by
the selector law. This replaces the old named-witness import by a bounded
exact-solve theorem on the selected retained ambient.

No closed-form symbolic classification beyond this bounded chart is claimed
here.

## Authority

- Local exact-solve runner (original):
  `scripts/frontier_gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_3plus1_line_exact_solve_doublet_theorem_2026_04_20.py`
- Dense root-count certificate (2026-05-03 audit repair):
  `scripts/gauge_vacuum_plaquette_doublet_dense_root_count_certificate_2026_05_03.py`
