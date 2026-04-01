# Physics Autopilot Handoff

## 2026-04-01 15:55 America/New_York

### Seam class
- directional-measure gravity `b` lane
- review fix plus overlap-onset local-density compare

### What this loop did
- acquired the `physics-science` cooperative lock for a review/fix pass
- verified that the directional-`b` center-offset helpers were clamping nonpositive `actual_b` to `1e-9`
- fixed that normalization bug in the directional-`b` helper stack so overlap cases become singular instead of fabricating huge `response / b` values
- reran the affected directional-`b` science cards:
  - `directional_b_denominator_geometry_diagnostic.py`
  - `directional_b_mass_window_transfer.py`
  - `directional_b_h_over_b_crossover_card.py`
  - `directional_b_overlap_margin_card.py`
- corrected the repo narrative and card wording to match the fixed results
- added `directional_b_overlap_onset_local_density_compare.py`
- ran it and wrote `logs/2026-04-01-directional-b-overlap-onset-local-density-compare.txt`
- refreshed the shared handoff and work log

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
- the new low-`b` onset mechanism read is:
  - weak target-band occupancy plus coarse local `y` spacing
  - tree controls densify near the target plane and keep compact source windows
  - dense random-DAG layers keep only about `1-2` nodes in the target band and therefore stretch widened source windows across larger `y` gaps
- the new best bounded overlap rule is:
  - `same_side_mean_gap >= 0.7504 and selected_span_step >= 1.1301`
  - `tp/fp/fn/tn = 7/0/2/14`
  - accuracy `0.9130`

### Git / sync state
- review/fix edits are still local in the shared checkout at the time of this handoff
- changed tracked files include:
  - `README.md`
  - `docs/ARCHITECTURE_NOTE_DIRECTIONAL_MEASURE.md`
  - `AUTOPILOT_WORKLOG.md`
  - directional-`b` helper/card scripts
  - refreshed directional-`b` logs
- untracked local work still exists in:
  - `scripts/three_d_modular_gravity_mass_scaling.py`
- that 3D mass-scaling script was corrected locally to stop drifting the source centroid while claiming fixed `b`, but it was not rerun or published in this loop

### Strongest confirmed conclusion
The widened-family `response / b` failure was a helper bug, not a retained science result. After the fix, the gravity lane is cleaner: `1/b` remains the leading bounded term, `b - h_mass` is the safer finite-source correction near overlap, and overlap onset itself is now explained by sparse target-band occupancy plus coarse local spacing.

### Exact next step
- keep the corrected propagator and corrected directional-`b` hierarchy fixed
- test whether the new overlap-onset observables transfer onto one second dense-family control:
  - same-side local `y` spacing
  - target-band fill
  - selected span per source step
- only if that transfers, promote the local-density explanation into the retained asymptotic architecture

### New log paths
- `/Users/jonreilly/Projects/Physics/logs/2026-04-01-directional-b-denominator-geometry-diagnostic.txt`
- `/Users/jonreilly/Projects/Physics/logs/2026-04-01-directional-b-mass-window-transfer.txt`
- `/Users/jonreilly/Projects/Physics/logs/2026-04-01-directional-b-h-over-b-crossover-card.txt`
- `/Users/jonreilly/Projects/Physics/logs/2026-04-01-directional-b-overlap-margin-card.txt`
- `/Users/jonreilly/Projects/Physics/logs/2026-04-01-directional-b-overlap-onset-local-density-compare.txt`
