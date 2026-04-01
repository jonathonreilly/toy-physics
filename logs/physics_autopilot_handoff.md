# Physics Autopilot Handoff

## 2026-04-01 17:14 America/New_York

### Seam class
- directional-measure gravity `b` lane
- overlap-onset transfer holdout

### What this loop did
- ran the required duplicate-run guard and cooperative lock checks before reading shared state
- reconciled the canonical repo and found that the earlier push to `origin/main` is still blocked in this sandbox by DNS (`Could not resolve host: github.com`)
- added `scripts/directional_b_overlap_onset_transfer_holdout.py`
- ran it and wrote `logs/2026-04-01-directional-b-overlap-onset-transfer-holdout.txt`
- updated the retained directional-`b` narrative so the overlap-onset claim is promoted only at the feature level
- refreshed the tracked work log and this handoff

### Current state
- no detached science child is running
- the lead unitary layer is unchanged:
  - corrected `1/L^p` transport
  - directional path measure `exp(-0.8×θ²)`
- the corrected directional-`b` hierarchy is now:
  - leading term `response / b`
  - safer finite-source correction `response / (b - h_mass)`
  - packet-support correction secondary
- widened dense random-DAG families do cross into `mu <= 0`, but pure `response / b` still passes on the bounded family once singular center-offset trials are excluded
- the second dense-family holdout keeps the same qualitative overlap-onset split:
  - overlap rows still have much weaker target-band fill (`0.196` vs `0.885`)
  - same-side spacing stays coarser (`1.035` vs `0.869`)
  - selected span per source step stays larger (`1.193` vs `0.498`)
- the exact original gap/span rule is only partial on that holdout:
  - `same_side_mean_gap >= 0.7504 and selected_span_step >= 1.1301`
  - `tp/fp/fn/tn = 9/1/6/24`
  - accuracy `0.8250`
- the promoted retained statement is therefore:
  - sparse target-band occupancy is the leading transferable overlap-onset signal
  - same-side gap/span thresholds stay family-dependent refinements

### Git / sync state
- `main` and `codex/distance-law-closure-and-higher-d-status` both point at `6fc649f`
- the required push helper failed earlier in the loop with DNS against `origin/main`
- this loop's directional-`b` edits are local in the shared checkout until a later push succeeds
- unrelated untracked local work still exists in:
  - `scripts/five_d_dense_joint_pilot.py`
  - `scripts/source_resolved_green_pilot.py`

### Strongest confirmed conclusion
The overlap-onset mechanism now transfers one step beyond the original compare, but only at the feature level. Sparse target-band occupancy is the leading cross-family signal for `mu <= 0`; the spacing cuts still help, but their exact thresholds are not universal once the dense family is widened and softened.

### Exact next step
- keep the corrected propagator and corrected directional-`b` hierarchy fixed
- test whether the target-band occupancy floor transfers onto one more geometry-varied control that changes the mid-layer sampling law without changing the overlap diagnostic
- only if that still holds, translate target-band occupancy into a cleaner asymptotic bridge variable

### New log paths
- `/Users/jonreilly/Projects/Physics/logs/2026-04-01-directional-b-overlap-onset-transfer-holdout.txt`
