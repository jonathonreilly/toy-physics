# Physics Autopilot Handoff

## 2026-03-28 22:07 America/New_York

### Seam class
- generated-family transfer
- non-guarded anchor-balance boundary

### Science impact
- science advanced; the surviving generated pair-only failures are now pinned to a second nearby domain boundary after the zero-support guard, not a shifted continuation of the historical frozen `pair-only-sensitive` branch

### Current state
- Resumed from synced `main` at `8bd72db` under the `physics-science` lock and stayed on the active generated-family transfer thread.
- Added and ran:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_order_parameter_generated_non_guarded_pair_compare.py`
- Canonical log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-28-low-overlap-order-parameter-generated-non-guarded-pair-compare.txt`

### Strongest confirmed conclusion
- The surviving generated failures after the zero-support guard split across opposite load regimes:
  - `base:skew-wrap:local-morph-c` and `base:skew-wrap:mode-mix-d` are over-supported/high-closure but low-density
  - `base:taper-wrap:mode-mix-f` is sparse/low-closure but high-density
- So no single load, closure, or density threshold exact-separates that whole generated failure family from the historical frozen `pair-only-sensitive` rows.
- But all `11` surviving generated failures do exact-close into one compact anchor-balance band:
  - `anchor_closure_intensity_gap >= -2.000 and anchor_closure_intensity_gap <= 2.333`
  - empirical generated values are only `0/1/2`
  - every historical frozen `pair-only-sensitive` row lies outside that band (`-9.667 -> -4.000` or `2.667 -> 6.000`)
- So the post-guard transfer break is now best read as a second nearby domain boundary: moderate anchor balance, absent from the historical frozen `pair-only-sensitive` branch.

### Files/logs changed
- Repo-facing code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_order_parameter_generated_non_guarded_pair_compare.py`
- Updated narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- New log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-28-low-overlap-order-parameter-generated-non-guarded-pair-compare.txt`
- Validation:
  - `python3 -m py_compile /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_order_parameter_generated_non_guarded_pair_compare.py`

### Remaining review seams
- closed: decide whether the surviving non-guarded generated failures are just shifted historical `pair-only-sensitive` load/density rows
- open: determine whether the anchor-balance band is a true generated-domain boundary or only a contrast against historical frozen `pair-only-sensitive` rows

### Exact next step
- Project the new `anchor_closure_intensity_gap` band onto historical frozen `add1-sensitive` rows plus nearby generated non-failures that survive the zero-support guard.

### First concrete action
- Extend `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_order_parameter_generated_non_guarded_pair_compare.py` to add the historical `add1-sensitive` cohort and the guarded generated non-failure rows, then check whether the anchor-balance band stays exact or needs one more physical clause.
