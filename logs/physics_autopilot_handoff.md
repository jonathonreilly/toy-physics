# Physics Autopilot Handoff

## 2026-04-01 05:37 America/New_York

### Seam class
- gravity scaling
- packet-local support-structure translation

### What this loop did
- added `/Users/jonreilly/Projects/Physics/scripts/gravity_packet_local_support_structure_compare.py`
- ran a bounded support-structure compare on the same two-family gravity readout benchmark:
  - layered random DAG scaling family
  - branching-tree control
- updated `/Users/jonreilly/Projects/Physics/README.md`

### Current state
- no detached science child is running
- `main` was synced to `origin/main` before this step
- the packet-local transfer split is now physically explained:
  - on random DAGs, the retained packet captures a growing mass-side carried-flow share:
    - upper share `0.287 -> 0.382` from `N=12 -> 25`
    - lower share `0.272 -> 0.162`
    - share gap `+0.015 -> +0.220`
  - the random-DAG probe support remains materially broader than the retained packet:
    - flow support compression `3.258x/2.046x -> 3.053x/3.464x` (upper/lower)
  - on the branching-tree control, both probe sides stay nearly symmetric:
    - upper share `0.263 -> 0.250`
    - lower share `0.290 -> 0.250`
    - flow support compression stays only about `~2x`

### Strongest confirmed conclusion
Packet-local flow is a real dense-route refinement because random-DAG probe support broadens and then refocuses into a narrower mass-side carrier while the opposite side diffuses. The branching-tree control never enters that regime, so the retained shared gravity observable is still the broader near-mass `action_channel`.

### Exact next step
- compress the support-width / carried-flow split into one coarse regime observable that decides when packet-local flow should replace the broader `action_channel`, then test that switch on the existing two-family benchmark without touching transport

### First concrete action
- prototype one regime score from mass-side carried-flow share gap and packet-support compression, then compare a gated or blended readout against raw `action_channel` and `packet_flow_action`
