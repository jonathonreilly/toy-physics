# Handoff

## Current State

Cycle 1 complete. The branch selected Lane 1 route 3E B2 because
higher-priority open-science loops on `origin/main` already record
honest-stop state.

The landed result is negative/progress:

- the rough x0.96 screening factor cannot promote `sqrt(sigma)`;
- a PDG backsolve is circular;
- a literal asymptotic full-QCD string-tension target is underdefined
  because full QCD strings break;
- B2 is repaired into B2a/B2b;
- modern static-energy literature gives a bounded bridge, not a retained
  screening closure. TUMQCD fit-window `sqrt(sigma)` gives about
  `467.39 +/- 9.57 MeV` or `481.71 +/- 9.70 MeV` depending the
  static-potential convention; CLS `N_f=2+1` gives clean `r0`/`r1`
  force scales but not a unique `sqrt(sigma)` map;
- B5 current-surface shortcut is closed negatively: structural `SU(3)` +
  `g_bare -> beta=6` + current `4^4` check supports the bridge but does
  not retain it;
- B5 ladder budget is now explicit: `L=4,6,8` is a scout, not closure;
  `L=8,12,16` is the first compute class that can close B5.
- the fixed low-stat `L=4,6,8` pure-gauge scout validates local
  plaquette/Wilson-loop/Creutz measurement plumbing but remains explicitly
  non-closing.
- a resumable B5 Wilson/Creutz ladder runner now exists. Its smoke
  profile is verified; production `L=8,12,16` statistics remain to be
  accumulated before B5 can be promoted.
- the first four production intervals produced `532` `L=8` JSONL records
  after `5548` sweeps. This is a useful checkpoint, but it is not B5
  closure because `L=12` and `L=16` are still missing.

Skill-correction checkpoint:

- the user clarified that the 12-hour request is a campaign budget, not a
  permission to stop after a PR-ready block;
- this branch should not weave science results through repo-wide authority
  surfaces before review. Proposed `docs/CANONICAL_HARNESS_INDEX.md` and
  Lane 1 open-science-file updates are recorded below for later integration
  rather than applied in the science PR.

Verification:

```bash
PYTHONPATH=scripts python3 scripts/frontier_hadron_lane1_sqrt_sigma_b2_gate_repair.py
# PASS=16 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_hadron_lane1_sqrt_sigma_b2_static_energy_bridge.py
# PASS=14 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_hadron_lane1_sqrt_sigma_b5_framework_link_audit.py
# PASS=16 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_hadron_lane1_sqrt_sigma_b5_ladder_budget.py
# PASS=13 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_hadron_lane1_sqrt_sigma_b5_lowstat_scout.py
# PASS=9 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_hadron_lane1_sqrt_sigma_b5_resumable_ladder.py \
  --profile smoke \
  --fresh \
  --checkpoint-dir outputs/frontier_hadron_lane1_sqrt_sigma_b5_resumable_ladder_checkpoints_smoke
# PASS=13 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_hadron_lane1_confinement_to_mass_firewall.py
# PASS=16 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_hadron_lane1_sqrt_sigma_b5_production_aggregator.py
# PASS=11 FAIL=0
```

Branch-local artifacts:

- `docs/HADRON_LANE1_SQRT_SIGMA_B2_GATE_REPAIR_AUDIT_NOTE_2026-04-30.md`
  with `scripts/frontier_hadron_lane1_sqrt_sigma_b2_gate_repair.py`.
- `docs/HADRON_LANE1_SQRT_SIGMA_B2_STATIC_ENERGY_BRIDGE_SCOUT_NOTE_2026-04-30.md`
  with `scripts/frontier_hadron_lane1_sqrt_sigma_b2_static_energy_bridge.py`.
- `docs/HADRON_LANE1_SQRT_SIGMA_B5_FRAMEWORK_LINK_AUDIT_NOTE_2026-04-30.md`
  with `scripts/frontier_hadron_lane1_sqrt_sigma_b5_framework_link_audit.py`.
- `docs/HADRON_LANE1_SQRT_SIGMA_B5_LADDER_BUDGET_NOTE_2026-04-30.md`
  with `scripts/frontier_hadron_lane1_sqrt_sigma_b5_ladder_budget.py`.
- `docs/HADRON_LANE1_SQRT_SIGMA_B5_LOWSTAT_SCOUT_NOTE_2026-04-30.md`
  with `scripts/frontier_hadron_lane1_sqrt_sigma_b5_lowstat_scout.py`.
- `docs/HADRON_LANE1_SQRT_SIGMA_B5_RESUMABLE_LADDER_NOTE_2026-04-30.md`
  with `scripts/frontier_hadron_lane1_sqrt_sigma_b5_resumable_ladder.py`.
- `docs/HADRON_LANE1_SQRT_SIGMA_B5_PRODUCTION_CHECKPOINT_NOTE_2026-04-30.md`
  with `scripts/frontier_hadron_lane1_sqrt_sigma_b5_production_aggregator.py`.

## Next Exact Action

Pick one of two next blocks:

1. Resume the resumable B5 ladder from the local production checkpoint until
   the `L=8` target is complete and `L=12,16` statistics can start.
2. Retained-with-budget draft that chooses `r0`/`r1` as the Lane 1
   force-scale observable and keeps `sqrt(sigma)` as a bounded
   comparator, with static-potential convention split explicit.

## Proposed Review Integration

Do not apply these directly from the science branch. If the review PR lands,
the later integration pass may:

- add the B2/B5 repair packet to `docs/CANONICAL_HARNESS_INDEX.md`;
- update the Lane 1 open-science file to replace the rough `(B2)`
  target with the repaired `(B2a)/(B2b)` target;
- add support bullets for the B5 framework-link audit, ladder budget,
  low-stat scout, and resumable ladder runner.

## Do Not Reopen

- Rough x0.96 promotion.
- PDG backsolve factor.
- Pure quenched large-volume route as a direct B2 closure.
