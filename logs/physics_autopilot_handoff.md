# Physics Autopilot Handoff

## 2026-03-31 15:40 America/New_York

### Seam class
- generated-DAG field coupling
- self sparse-25 config-local flip compare

### Science impact
- added `/Users/jonreilly/Projects/Physics/scripts/generated_dag_pattern_sourced_config_local_flip_compare.py`
- wrote the sparse self slice to `/Users/jonreilly/Projects/Physics/logs/2026-03-31-generated-dag-config-local-late-support-flip-compare-self-sparse-25.txt`
- the noisiest self config does tighten beyond the pooled self rule:
  - `8` retained rows total
  - `4` stay toward-source
  - `4` flip away under `last6_union`
- the pooled self separator only touches one row here:
  - `extra_packet_side_gap <= -0.0962` matches `1/8`
  - that one matched row flips, but it does not explain the whole slice
- the config-local slice is cleaner and more corridor-led:
  - stable rows keep far more added forward corridor support (`0.4527` vs `0.0439`)
  - flip rows carry stronger negative packet-side and fringe-side gaps
- the best config-local rules all tell the same story:
  - `extra_support_corridor_share <= 0.0000`
  - `extra_packet_side_gap <= 0.0000`
  - `extra_support_forward_share <= 0.1429`
  - each gives `0.8750` accuracy on the `8` rows

### Current state
- this loop stayed on the noisiest self residual slice only
- the unrelated local `README.md` edit remains intentionally untouched

### Strongest confirmed conclusion
The self residual compresses further on `sparse-25`: the sign flip there is best read as forward-corridor collapse, not just generic wrong-side packet bias.

### Exact next step
- compare the `wide` low-added-packet-field branch and the `self:sparse-25` corridor-collapse branch directly and test whether they are one smaller forward-packet-retiming language or two separate residual mechanisms

## 2026-03-31 15:14 America/New_York

### Seam class
- generated-DAG field coupling
- self-rule local sign-flip compare

### Science impact
- hardened `/Users/jonreilly/Projects/Physics/scripts/generated_dag_pattern_sourced_late_support_flip_compare.py` so sandboxed runs can fall back to serial execution instead of failing inside multiprocessing setup
- generalized `/Users/jonreilly/Projects/Physics/scripts/generated_dag_pattern_sourced_rule_local_flip_compare.py` so the interpretation text matches the selected target branch
- wrote the self-branch compare to `/Users/jonreilly/Projects/Physics/logs/2026-03-31-generated-dag-rule-local-late-support-flip-compare-self.txt`
- the `self` branch does not reuse the `wide` late-support mechanism:
  - `39` retained rows total
  - `11` flip to away under `last6_union`
  - `28` stay toward-source
  - best retained self-local separator: `extra_packet_side_gap <= -0.0962` (`0.8235` discovery, `0.6818` holdout)
  - matched side: `2/3` flips with mean `last6_shift = -4.3651`
  - unmatched side: `9/36` flips with mean `last6_shift = +2.7135`
  - noisiest self config: `sparse-25` (`4/8` flips)
- physical read:
  - `wide`: extra support fails to land enough field on the packet
  - `self`: extra support lands too much field on the opposite packet side

### Current state
- no detached science child is running
- unrelated local `README.md` edits remain untouched

### Strongest confirmed conclusion
The late-support residual is mover-rule-local. `wide` and `self` need different physical language: `wide` is a low-added-packet-field branch, while `self` is a weaker wrong-side packet-field branch.

### Exact next step
- split the `self` branch by config, starting with `sparse-25`, and test whether negative packet-side gap closes more cleanly there than on the pooled self rows
- first concrete action: extend the rule-local compare with a config-local self summary and render the `sparse-25` self slice
