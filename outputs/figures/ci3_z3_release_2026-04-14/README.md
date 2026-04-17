# CI(3) / Z^3 Figure Input Freeze

**Date:** 2026-04-14  
**Pinned package commit:** `26edb60e805faed94ffb587250b8dd521e877dde`

This directory records the figure-input freeze for the current selective
reproducibility pass.

## Rule

Not every figure in the current package is a rendered numeric plot. Several are
schematic or composite figures that still need final design work. This freeze
therefore pins the **inputs** for runner-backed figures rather than pretending
every figure is already fully rendered.

## Figure-input map

| Figure | Status | Pinned input |
|---|---|---|
| Figure 1. Framework and derivation map | schematic only | manuscript synthesis; no numeric artifact in this freeze |
| Figure 2. Graph-first `SU(3)` closure | runner-backed | [logs/retained/release_2026-04-14/frontier_graph_first_su3_integration.stdout](/private/tmp/physics-publication-prep/logs/retained/release_2026-04-14/frontier_graph_first_su3_integration.stdout) |
| Figure 3. Anomaly-forced `3+1` | runner-backed | [logs/retained/release_2026-04-14/frontier_anomaly_forces_time.stdout](/private/tmp/physics-publication-prep/logs/retained/release_2026-04-14/frontier_anomaly_forces_time.stdout) |
| Figure 4. Three-generation matter structure | runner-backed | [logs/retained/release_2026-04-14/frontier_generation_axiom_boundary.stdout](/private/tmp/physics-publication-prep/logs/retained/release_2026-04-14/frontier_generation_axiom_boundary.stdout) |
| Quantitative hierarchy anchor | runner-backed | [logs/retained/release_2026-04-14/frontier_hierarchy_observable_principle_from_axiom.stdout](/private/tmp/physics-publication-prep/logs/retained/release_2026-04-14/frontier_hierarchy_observable_principle_from_axiom.stdout) |

## Release note

When the final rendered figure set exists, it should be generated from these
pinned inputs or from explicitly versioned replacements, not from ad hoc reruns
whose commit state is not recorded.
