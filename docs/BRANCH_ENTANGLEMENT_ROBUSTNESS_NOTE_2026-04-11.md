# Branch Entanglement Robustness Note

**Date:** 2026-04-11  
**Status:** bounded companion robustness addendum

Primary artifact:
- `/Users/jonreilly/Projects/Physics/scripts/frontier_branch_entanglement_robustness.py`

Companion notes:
- [`BMV_ENTANGLEMENT_NOTE_2026-04-11.md`](BMV_ENTANGLEMENT_NOTE_2026-04-11.md)
- [`BMV_THREEBODY_NOTE_2026-04-11.md`](BMV_THREEBODY_NOTE_2026-04-11.md)

## What Was Rerun

Rerun command:

```bash
source /tmp/physics_venv/bin/activate && python scripts/frontier_branch_entanglement_robustness.py
```

Audited surfaces:
- 2-body separation sweep: `5` couplings × `4` separations = `20` configs
- 2-body source-position sweep: `5` couplings × `5` source positions = `25` configs
- 2-body size sweep: `3` sizes × `5` couplings = `15` configs
- 3-body source/coupling sweep: `5` source positions × `5` couplings = `25` configs

## Exact Rerun Numbers

This note reflects the current-main minimum-image rerun on the periodic surface.

### 2-body branch-entanglement

- `delta_S > 0`: `60/60`
- overall `delta_S`:
  - min: `0.000507`
  - max: `0.416917`
  - mean: `0.039757`

Side `12` persistence:
- `G=1`: `0.01202 ± 0.00044` (`27.1σ`)
- `G=5`: `0.06966 ± 0.00335` (`20.8σ`)
- `G=10`: `0.03315 ± 0.00387` (`8.6σ`)
- `G=20`: `0.00312 ± 0.00166` (`1.9σ`)
- `G=50`: `0.00219 ± 0.00098` (`2.2σ`)

### 3-body branch-entanglement

- `GHZ-type` theorem check: `0/25`
- `W` or `W-asym` classification: `25/25`
- `tau_3`:
  - min: `0.000000`
  - max: `0.000000`
  - mean: `0.000000`

The `0/25` GHZ row is not an empirical discovery metric on this surface. For
the fixed two-branch ansatz used by the canonical robustness harness,
`tau_3 = 0` is theorem-implied by the overlap algebra, so the GHZ count is
only a sanity check that the implementation stays on the intended ansatz.

Representative rerun rows:
- `G=20, src=(6,6)`: `S_1|23=0.69302`, `S_2|13=0.69291`, `S_3|12=0.69299`, `tau_3=0.00000`, class `W`
- `G=50, src=(6,3)`: `0.69299`, `0.69240`, `0.68959`, `tau_3=0.00000`, class `W`

## Strongest Honest Claims

For 2-body:

> On the audited fixed-adjacency two-branch staggered-lattice protocol, the
> 2-body branch-entanglement signal is robust: `delta_S > 0` in `60/60`
> audited configurations across seeds, separations, source positions, and
> sizes. This remains a bounded branch-mediated entanglement result on an
> externally imposed two-branch protocol, not a full BMV witness.

For 3-body:

> On the audited fixed-adjacency two-branch staggered-lattice protocol, the
> 3-body branch-entanglement surface is W-type, not GHZ-type: `tau_3 = 0`
> and `W/W-asym` classification in `25/25` audited source/coupling
> configurations, with all bipartite entropies positive.

## What This Retires

- Earlier GHZ-style wording from the standalone three-body runner should not
  be treated as canonical.
- The canonical 3-body read is now the robustness harness:
  pairwise-distributed W-type branch entanglement, not genuine GHZ structure.
