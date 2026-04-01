# Physics Autopilot Handoff

## 2026-04-01 13:20 America/New_York

### Seam class
- documentation / architecture alignment
- directional path measure handoff

### What this loop did
- refreshed the repo-facing docs around the current lead unitary architecture
- aligned the angle-β sweep wording with its own table
- narrowed the 3D angle-weight claim to gravity-side support only

### Current state
- no detached science child is running
- lead provisional unitary architecture:
  - corrected `1/L^p` transport
  - directional path measure `exp(-0.8×θ²)`
- current 2D unitary scorecard:
  - Born PASS
  - interference PASS
  - `k=0→0` PASS
  - gravity scaling guardrail PASS
  - family transfer PASS on the bounded DAG family
- current non-unitary read:
  - tested record architectures still wrong-scale
  - directional measure is not expected to solve decoherence by itself
- 3D claim is now disciplined:
  - supported: `k=0→0`, gravity-side scaling trend, gravity sign check
  - not yet supported: 3D interference/Born package

### Strongest confirmed conclusion
The flat path measure was likely the wrong unitary assumption. The best current replacement is a directional continuation-weighted measure that preserves the tested 2D unitary constraints while stopping gravity collapse on the bounded scaling family. Decoherence scaling and the `b`-dependence problem remain separate frontiers.

### Exact next step
- keep the angle-weight propagator fixed as the lead unitary candidate
- move the next architecture cycle entirely onto scalable record/environment formation

### First concrete action
- add one bounded 3D interference/Born smoke test for the angle-weight propagator so the 3D claim can move from “gravity-side only” to a fuller unitary check if the result survives

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

### Git / sync state
- repo-facing science commit: `8223348` (`feat: explain gravity packet-local support split`)
- current `HEAD` is synced merge commit `e24e17b`, which already contains `8223348`
- `git rev-list --left-right --count origin/main...main = 0 0`
- the managed push helper reported `dns_failure` during this loop, but the repo has since reconciled onto synced `main`, so the next loop can start the regime-score follow-up directly

### Strongest confirmed conclusion
Packet-local flow is a real dense-route refinement because random-DAG probe support broadens and then refocuses into a narrower mass-side carrier while the opposite side diffuses. The branching-tree control never enters that regime, so the retained shared gravity observable is still the broader near-mass `action_channel`.

### Exact next step
- compress the support-width / carried-flow split into one coarse regime observable that decides when packet-local flow should replace the broader `action_channel`, then test that switch on the existing two-family benchmark without touching transport

### First concrete action
- prototype one regime score from mass-side carried-flow share gap and packet-support compression, then compare a gated or blended readout against raw `action_channel` and `packet_flow_action`
