# Physics Autopilot Handoff

## 2026-04-01 06:32 America/New_York

### Seam class
- decoherence architecture reconciliation
- janitor integrity repair

### What this loop did
- reconciled the synced `00030df` / `04196f5` merge state into the tracked handoff
- confirmed `docs/DECOHERENCE_DECISION_NOTE.md` now matches the retained repo direction
- ran `python3 scripts/base_confidence_check.py` (`PASS`)
- made `/Users/jonreilly/Projects/Physics/scripts/three_d_angle_weight_unitary_smoke.py` fall back to sequential execution when multiprocessing is unavailable

### Current state
- no detached science child is running
- `main` is synced to `origin/main` at `788860d`
- the directional path measure still stands as the retained unitary layer
- the larger finite-env follow-up did **not** reopen a retained decoherence lane:
  - qubit-per-mass env reaches `127` populated detector env states by `N=18`
  - detector purity still wrong-scales (`0.6298 -> 0.8517` from `N=12 -> 18`)
  - the older node-label comparison remains same-order (`0.6429 -> 0.8023`)
- the bounded 3D smoke runner is now safe to rerun from restricted automation environments

### Strongest confirmed conclusion
More finite env states are not enough. The unitary side stays fixed on the directional measure, and the next non-unitary move should remain a mesoscopic durable-record / region-trace architecture rather than another larger discrete register.

### Exact next step
- keep the propagator fixed and prototype one durable local record or bounded region-trace mechanism
- do not spend the next cycle on another “bigger finite env” variant unless the record mechanism is qualitatively different

## 2026-04-01 14:02 America/New_York

### Seam class
- 3D angle-weight architecture validation
- bounded unitary smoke closure

### What this loop did
- extended `/Users/jonreilly/Projects/Physics/scripts/three_d_angle_weight.py` with amplitude-level reuse
- added `/Users/jonreilly/Projects/Physics/scripts/three_d_angle_weight_unitary_smoke.py`
- ran one bounded fixed-DAG 3D smoke test for the angle-weight candidate

### Current state
- no detached science child is running
- the directional path measure still stands as the lead provisional unitary architecture
- the main 3D wording gap is now closed:
  - zero-field coherent visibility: `max V_coh = 0.9963`
  - coherent vs incoherent detector-profile contrast across the canonical band: `min TV = 0.1104`
  - amplitude linearity residual: `3.178e-14`
  - detector normalization error: `0`

### Strongest confirmed conclusion
The angle-weight candidate now has bounded 3D unitary support, not just 3D gravity-side support. The honest remaining caveat is narrower: this is still a fixed-DAG smoke package rather than a full 3D Born/Sorkin theorem.

### Exact next step
- keep the propagator fixed and move the next architecture cycle back to scalable record/environment formation instead of broadening the 3D transport search

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
