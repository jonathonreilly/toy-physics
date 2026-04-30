# Artifact Plan

## Cycle 1

- Add `docs/HADRON_LANE1_SQRT_SIGMA_B2_GATE_REPAIR_AUDIT_NOTE_2026-04-30.md`.
- Add `scripts/frontier_hadron_lane1_sqrt_sigma_b2_gate_repair.py`.
- Run the script and store output under `outputs/`.
- Record proposed Lane 1 open-science and canonical harness integration in
  `HANDOFF.md` for the later review/integration pass.
- Update this loop pack with the Cycle 1 state and handoff.

## Cycle 2

- External static-energy bridge scout for `N_f=2+1` / `N_f=2+1+1`
  force scales and effective tension values.
- Output a residual table separating observable-definition, scale
  setting, chiral/continuum, string-breaking window, and B5 linkage.

Status: complete in
`docs/HADRON_LANE1_SQRT_SIGMA_B2_STATIC_ENERGY_BRIDGE_SCOUT_NOTE_2026-04-30.md`
with runner
`scripts/frontier_hadron_lane1_sqrt_sigma_b2_static_energy_bridge.py`.

## Cycle 3

- B5 current-surface framework-link audit.
- Close the shortcut "structural `SU(3)` + `beta=6` + `4^4` check retains
  framework-to-standard-QCD bridge".
- Name the next B5 executable route: local finite-volume scout or compute
  budget.

Status: complete in
`docs/HADRON_LANE1_SQRT_SIGMA_B5_FRAMEWORK_LINK_AUDIT_NOTE_2026-04-30.md`
with runner
`scripts/frontier_hadron_lane1_sqrt_sigma_b5_framework_link_audit.py`.

## Cycle 4

- Finite-volume ladder compute budget.
- Decide whether `L=4,6,8` can materially close B5.
- Name the first compute class that can close B5.

Status: complete in
`docs/HADRON_LANE1_SQRT_SIGMA_B5_LADDER_BUDGET_NOTE_2026-04-30.md`
with runner
`scripts/frontier_hadron_lane1_sqrt_sigma_b5_ladder_budget.py`.

## Cycle 5

- Low-stat finite-volume pure-gauge scout at `L=4,6,8`.
- Validate plaquette, Wilson-loop, and Creutz-ratio measurement plumbing.
- Keep the result explicitly below B5-closure status.

Status: complete in
`docs/HADRON_LANE1_SQRT_SIGMA_B5_LOWSTAT_SCOUT_NOTE_2026-04-30.md`
with runner
`scripts/frontier_hadron_lane1_sqrt_sigma_b5_lowstat_scout.py`.

## Cycle 6

- Add a resumable B5 Wilson/Creutz ladder runner.
- Provide append-only JSONL measurements and per-volume state checkpoints.
- Smoke-verify the runner while keeping B5 non-closing until production
  `L=8,12,16` statistics are accumulated.

Status: complete in
`docs/HADRON_LANE1_SQRT_SIGMA_B5_RESUMABLE_LADDER_NOTE_2026-04-30.md`
with runner
`scripts/frontier_hadron_lane1_sqrt_sigma_b5_resumable_ladder.py`.

## Cycle 7

- Run the production profile under the first wall-clock checkpoint.
- Preserve JSONL production records for `L=8`.
- Aggregate the checkpoint and keep B5 open until `L=12` and `L=16` exist.

Status: complete in
`docs/HADRON_LANE1_SQRT_SIGMA_B5_PRODUCTION_CHECKPOINT_NOTE_2026-04-30.md`
with runner
`scripts/frontier_hadron_lane1_sqrt_sigma_b5_production_aggregator.py`.
