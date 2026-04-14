# Reproducibility Freeze

**Date:** 2026-04-14  
**Purpose:** selective reproducibility freeze for the current publication
package before full submission freeze.

This is not the final full release freeze. It is the first pinned package slice
that makes the current paper surface reproducible in a controlled way.

## Freeze base

- package branch: `codex/publication-prep`
- pinned public commit hash:
  `26edb60e805faed94ffb587250b8dd521e877dde`

All logs listed below were generated from that pinned package state.

## Frozen runner logs

### Retained quantitative / figure-facing logs

| Lane | Runner | Archived log | Result summary | SHA-256 |
|---|---|---|---|---|
| Electroweak hierarchy / `v` | [frontier_hierarchy_observable_principle_from_axiom.py](../../../scripts/frontier_hierarchy_observable_principle_from_axiom.py) | [logs/retained/release_2026-04-14/frontier_hierarchy_observable_principle_from_axiom.stdout](/private/tmp/physics-publication-prep/logs/retained/release_2026-04-14/frontier_hierarchy_observable_principle_from_axiom.stdout) | `13/13` pass, `v = 245.080424447914 GeV`, `-0.462828%` vs `246.22 GeV` | `39f6dbb4664685ea63cfe70a17b151e5778166ca4fd2557c00d8e6a9c3ad6d41` |
| Graph-first structural `SU(3)` | [frontier_graph_first_su3_integration.py](../../../scripts/frontier_graph_first_su3_integration.py) | [logs/retained/release_2026-04-14/frontier_graph_first_su3_integration.stdout](/private/tmp/physics-publication-prep/logs/retained/release_2026-04-14/frontier_graph_first_su3_integration.stdout) | `PASS=111 FAIL=0` | `14f87bef1507289642647565f10c029928f79dc2bf86bc2452c71cc17818df20` |
| Anomaly-forced `3+1` | [frontier_anomaly_forces_time.py](../../../scripts/frontier_anomaly_forces_time.py) | [logs/retained/release_2026-04-14/frontier_anomaly_forces_time.stdout](/private/tmp/physics-publication-prep/logs/retained/release_2026-04-14/frontier_anomaly_forces_time.stdout) | `85` computed pass, `2` assertion, `0` fail | `3f075f970bb8b215fe640122899ee58fc36ac03473e324a715cd093acb78b8a9` |
| Three-generation matter structure | [frontier_generation_axiom_boundary.py](../../../scripts/frontier_generation_axiom_boundary.py) | [logs/retained/release_2026-04-14/frontier_generation_axiom_boundary.stdout](/private/tmp/physics-publication-prep/logs/retained/release_2026-04-14/frontier_generation_axiom_boundary.stdout) | `PASS=31 FAIL=0` | `ee6064570ad67af0d12c3a662ef1f23be61ef1ee1e49bf3254cd0c3e1a539528` |

### Bounded quantitative log

| Lane | Runner | Archived log | Result summary | SHA-256 |
|---|---|---|---|---|
| `\alpha_s(M_Z)` bounded zero-import route | [/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/scripts/frontier_alpha_s_determination.py](/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/scripts/frontier_alpha_s_determination.py) | [logs/bounded/release_2026-04-14/frontier_alpha_s_determination.stdout](/private/tmp/physics-publication-prep/logs/bounded/release_2026-04-14/frontier_alpha_s_determination.stdout) | bounded comparison band with `\alpha_s(M_Z) = 0.1182` route still under review | `c6e5fffe9ed082b842912bd296d22acd807610f43a046562aa8b92fb4a7decf6` |

## Figure-data freeze

The current package still mixes schematic figures and runner-backed figures.
This selective freeze pins the runner-backed inputs only.

See:

- [outputs/figures/ci3_z3_release_2026-04-14/README.md](/private/tmp/physics-publication-prep/outputs/figures/ci3_z3_release_2026-04-14/README.md)

Current freeze scope:

- Figure 1: schematic only, no numeric artifact pinned yet
- Figure 2: pinned by `frontier_graph_first_su3_integration.stdout`
- Figure 3: pinned by `frontier_anomaly_forces_time.stdout`
- Figure 4: pinned by `frontier_generation_axiom_boundary.stdout`
- hierarchy quantitative anchor: pinned by `frontier_hierarchy_observable_principle_from_axiom.stdout`

## Selective-freeze rule

- This freeze is enough to support package review and draft hardening.
- It is not the final public-release freeze.
- A final submission freeze should add:
  - one retained log per manuscript-facing retained runner
  - one bounded log per manuscript-facing bounded quantitative row
  - final figure artifacts regenerated from pinned inputs
  - a submission commit hash after the manuscript text is locked
