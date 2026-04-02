# Physics Autopilot Handoff

## 2026-04-02 04:45 America/New_York

### Seam class
- directional-measure gravity `b` lane
- overlap-onset transfer holdout restored

### What this loop did
- ran the duplicate-run guard, acquired the `physics-science` lock, and reconciled shared state before new work
- found that the active next step already existed only as runtime artifacts:
  - `logs/2026-04-01-directional-b-overlap-onset-transfer-holdout.txt`
  - `scripts/__pycache__/directional_b_overlap_onset_transfer_holdout.cpython-313.pyc`
- restored `scripts/directional_b_overlap_onset_transfer_holdout.py` so the second dense-family control is reproducible again
- reran the restored card and wrote `logs/2026-04-02-directional-b-overlap-onset-transfer-holdout.txt`
- updated the retained gravity wording in:
  - `README.md`
  - `docs/ARCHITECTURE_NOTE_DIRECTIONAL_MEASURE.md`
  - `AUTOPILOT_WORKLOG.md`
- committed the repo-facing change as:
  - `9690d3a` (`feat(gravity): restore overlap-onset holdout`)

### Current state
- no detached science child is running
- the lead unitary layer is unchanged:
  - corrected `1/L^p` transport
  - directional path measure `exp(-0.8×θ²)`
- the retained gravity wording is now sharper:
  - sparse target-band occupancy is the leading transferable overlap-onset signal
  - spacing thresholds remain family-dependent refinements
  - on the second dense-family holdout the best refit is:
    - `target_fill <= 0.3333`
    - `tp/fp/fn/tn = 14/2/1/23`
    - accuracy `0.9250`
- unrelated shared checkout dirt appeared during the loop in:
  - `scripts/four_d_local_continuation_pilot.py`
  - `scripts/local_continuation_backreaction_d050_confirm.py`

### Git / sync state
- shared repo head is `9690d3a` (`feat(gravity): restore overlap-onset holdout`)
- `main` is ahead of `origin/main` by 1
- push helper failed again with a DNS error:
  - `Could not resolve host: github.com`
- remaining tracked dirt is runtime-only:
  - `logs/physics_autopilot_handoff.md`
  - plus unrelated shared edits in `scripts/four_d_local_continuation_pilot.py` and `scripts/local_continuation_backreaction_d050_confirm.py`

### Strongest confirmed conclusion
The second dense-family holdout closes the immediate mechanism-transfer seam. The old gap/span thresholds do not freeze across families (`0.8250` transfer accuracy), but sparse target-band occupancy does: overlap rows keep dramatically weaker fill (`0.196` vs `0.885`), and the holdout refit collapses mostly to the occupancy floor `target_fill <= 0.3333`.

### Exact next step
- keep the corrected propagator and corrected directional-`b` hierarchy fixed
- build one bounded bridge card that compresses overlap / `mu` against a coarse occupancy variable across:
  - the original dense-family card
  - this second dense-family holdout
- only widen back out if that occupancy bridge fails

### New log paths
- `/Users/jonreilly/Projects/Physics/logs/2026-04-02-directional-b-overlap-onset-transfer-holdout.txt`
