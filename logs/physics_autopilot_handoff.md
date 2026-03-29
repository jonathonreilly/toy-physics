# Physics Autopilot Handoff

## 2026-03-28 23:54 America/New_York

### Seam class
- generated-family transfer
- anchor-band projection

### Science impact
- science advanced; the moderate anchor-balance band now survives the queued historical `add1-sensitive` projection, and the immediate taper/skew generated neighborhood remains failure-only after the support-collapse guard

### Current state
- Resumed the active generated-family transfer thread while the repo was still locally ahead at `7c446d8` after the earlier DNS-blocked helper push.
- Refactored and reran:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_order_parameter_exact_law_generated_ensemble_transfer_check.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_order_parameter_generated_non_guarded_pair_compare.py`
- Canonical log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-28-low-overlap-order-parameter-generated-anchor-band-nearby-projection-v3.txt`

### Strongest confirmed conclusion
- The same moderate anchor-balance band still exact-separates the surviving generated failures from the two frozen historical cohorts now tested on this thread:
  - `anchor_closure_intensity_gap >= -2.000 and anchor_closure_intensity_gap <= 2.333`
  - generated failures: `11/11` hits
  - historical frozen `pair-only-sensitive`: `0/9` hits
  - historical frozen `add1-sensitive`: `0/15` hits
- Historical frozen `add1-sensitive` rows sit entirely on the negative side of that boundary:
  - `anchor_closure_intensity_gap = -12.000 -> -2.667`
- The bounded immediate generated basin (`taper-wrap`, `skew-wrap`, `taper-hard`, `skew-hard` through `mega`) contributes no guard-surviving correctly classified counterexample rows:
  - `generated_stable_nearby_rows = 0`
  - every non-collapse row in that basin is itself another transfer failure

### Files/logs changed
- Repo-facing code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_order_parameter_exact_law_generated_ensemble_transfer_check.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_order_parameter_generated_non_guarded_pair_compare.py`
- Updated narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- New log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-28-low-overlap-order-parameter-generated-anchor-band-nearby-projection-v3.txt`
- Validation:
  - `python3 -m py_compile /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_order_parameter_exact_law_generated_ensemble_transfer_check.py /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_order_parameter_generated_non_guarded_pair_compare.py`
  - `python3 -u /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_order_parameter_generated_non_guarded_pair_compare.py > /Users/jonreilly/Projects/Physics/logs/2026-03-28-low-overlap-order-parameter-generated-anchor-band-nearby-projection-v3.txt`

### Remaining review seams
- closed: determine whether the anchor-balance band is only a contrast against frozen historical `pair-only-sensitive` rows
- open: determine whether the band is a broader subtype basin that also captures frozen `add4-sensitive` structure, or whether one extra support-layout clause restores a more specific pair-only boundary

### Exact next step
- Project the anchor-balance band onto the frozen `add4-sensitive` cohort, starting with the few in-band cases, to test whether the current band is a subtype-specific boundary or a broader basin marker.

### First concrete action
- Extend `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_order_parameter_generated_non_guarded_pair_compare.py` to add frozen `add4-sensitive` rows, then test whether one compact support-layout clause separates those rows from the generated pair-only basin without reopening the historical `pair-only`/`add1` boundary.
