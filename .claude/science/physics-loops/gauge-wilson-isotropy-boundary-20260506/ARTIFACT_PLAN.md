# Artifact Plan

## Files To Touch

| path | planned change |
|---|---|
| `docs/GAUGE_WILSON_ISOTROPY_BOUNDARY_NOTE_2026-05-04.md` | Retag as `no_go` and add the explicit route-specific negative derivation. |
| `docs/audit/data/citation_graph.json` | Regenerate to pick up the source note hash and `no_go` claim-type hint. |
| `docs/audit/data/audit_ledger.json` | Reseed so the prior open-gate audit is archived and the edited row is queued as `unaudited`. |
| `docs/audit/data/effective_status_summary.json` | Recompute after ledger reseed. |
| `.claude/science/physics-loops/gauge-wilson-isotropy-boundary-20260506/*` | Record loop state, imports, certificate, review history, and handoff. |

## Files Not To Touch

- `scripts/frontier_gauge_wilson_isotropy_boundary_2026_05_04.py`: existing
  runner already checks the load-bearing class-A facts.
- Repo-wide authority surfaces such as publication tables, lane registry, and
  publication matrices: independent audit/governance should update those after
  re-audit.
