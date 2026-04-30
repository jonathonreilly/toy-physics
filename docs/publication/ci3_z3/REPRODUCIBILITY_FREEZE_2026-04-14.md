# Archival Reproducibility Freeze

**Date:** 2026-04-14  
**Purpose:** archival selective reproducibility freeze for an earlier
publication slice before full submission freeze.

This is not the current active package freeze and not the final full release
freeze. It is an earlier pinned package slice kept for provenance.
Current validation should start from `REPRODUCE.md` and the
current package surfaces rather than from this archival note alone.

## Freeze base

- package branch: `main`
- pinned public commit hash:
  `26edb60e805faed94ffb587250b8dd521e877dde`

All logs listed below were generated from that pinned package state.

## Frozen runner logs

### Retained quantitative / figure-facing logs

| Lane | Runner | Archived log | Result summary | SHA-256 |
|---|---|---|---|---|
| Electroweak hierarchy / `v` | [frontier_hierarchy_observable_principle_from_axiom.py](../../../scripts/frontier_hierarchy_observable_principle_from_axiom.py) | [logs/retained/release_2026-04-14/frontier_hierarchy_observable_principle_from_axiom.stdout](../../../logs/retained/release_2026-04-14/frontier_hierarchy_observable_principle_from_axiom.stdout) | historical `2026-04-14` retained run before canonical `v` unification; current mainline value is `246.282818290129 GeV` (`+0.025513%` vs `246.22 GeV`) | `39f6dbb4664685ea63cfe70a17b151e5778166ca4fd2557c00d8e6a9c3ad6d41` |
| Graph-first structural `SU(3)` | [frontier_graph_first_su3_integration.py](../../../scripts/frontier_graph_first_su3_integration.py) | [logs/retained/release_2026-04-14/frontier_graph_first_su3_integration.stdout](../../../logs/retained/release_2026-04-14/frontier_graph_first_su3_integration.stdout) | `PASS=111 FAIL=0` | `14f87bef1507289642647565f10c029928f79dc2bf86bc2452c71cc17818df20` |
| Anomaly-forced `3+1` | [frontier_anomaly_forces_time.py](../../../scripts/frontier_anomaly_forces_time.py) | [logs/retained/release_2026-04-14/frontier_anomaly_forces_time.stdout](../../../logs/retained/release_2026-04-14/frontier_anomaly_forces_time.stdout) | `85` computed pass, `2` assertion, `0` fail | `3f075f970bb8b215fe640122899ee58fc36ac03473e324a715cd093acb78b8a9` |
| Three-generation matter structure | [frontier_generation_axiom_boundary.py](../../../scripts/frontier_generation_axiom_boundary.py) | [logs/retained/release_2026-04-14/frontier_generation_axiom_boundary.stdout](../../../logs/retained/release_2026-04-14/frontier_generation_axiom_boundary.stdout) | `PASS=31 FAIL=0` | `ee6064570ad67af0d12c3a662ef1f23be61ef1ee1e49bf3254cd0c3e1a539528` |

### Bounded quantitative log

| Lane | Runner | Archived log | Result summary | SHA-256 |
|---|---|---|---|---|
| `\alpha_s(M_Z)` bounded zero-import route | [frontier_alpha_s_determination.py](../../../scripts/frontier_alpha_s_determination.py) | [logs/bounded/release_2026-04-14/frontier_alpha_s_determination.stdout](../../../logs/bounded/release_2026-04-14/frontier_alpha_s_determination.stdout) | bounded comparison band with `\alpha_s(M_Z) = 0.1182` route still under review | `c6e5fffe9ed082b842912bd296d22acd807610f43a046562aa8b92fb4a7decf6` |
| zero-import 2-loop `y_t` route | [frontier_yt_2loop_chain.py](../../../scripts/frontier_yt_2loop_chain.py) | [logs/bounded/release_2026-04-14/frontier_yt_2loop_chain.stdout](../../../logs/bounded/release_2026-04-14/frontier_yt_2loop_chain.stdout) | post-freeze bounded intake addendum on `main`: `m_t = 169.39 GeV`, `\alpha_s(M_Z) = 0.118069`, lane still bounded | `ccc33aa157b1dce74028550bb67562f9dd3eb51480e3bd46fbfebbef50c545df` |

## Figure-data freeze

The current package still mixes schematic figures and runner-backed figures.
This selective freeze pins the runner-backed inputs only.

See:

- [outputs/figures/ci3_z3_release_2026-04-14/README.md](../../../outputs/figures/ci3_z3_release_2026-04-14/README.md)

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
