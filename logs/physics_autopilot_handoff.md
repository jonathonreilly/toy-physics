# Physics Autopilot Handoff

## 2026-04-01 02:38 America/New_York

### Seam class
- gravity theory refinement
- packet-local action saturation diagnostic

### Science impact
- added `/Users/jonreilly/Projects/Physics/scripts/phase_valley_local_action_spread_compare.py`
- wrote `/Users/jonreilly/Projects/Physics/logs/2026-04-01-phase-valley-local-action-spread-compare.txt`
- updated `/Users/jonreilly/Projects/Physics/README.md`
- updated `/Users/jonreilly/Projects/Physics/scripts/nonunitary_theory_frontier_card.py`
- kept the corrected propagator, impact-parameter family, and near-mass action-gap numerator fixed, then replaced the pooled node-level action spread with packet-local windows around each valley peak on the same three bounded probes
- retained fit summary:
  - `near_mass_b local_action_q`: `R^2 = 0.4478`, `MAE = 0.3413`
  - `near_mass_b action_gap`: `R^2 = 0.4213`, `MAE = 0.3545`
  - `near_mass_b action_q`: `R^2 = 0.3983`, `MAE = 0.3528`
- guardrail note:
  - packet half-window `1` keeps the same winner (`R^2 = 0.4482`)
  - packet half-window `3` keeps the same winner (`R^2 = 0.4477`)
- detector-side probes still do not close under any tested action normalization

### Current state
- no detached science child is running
- packet-local near-mass normalization is now the retained gravity saturation read on the rectangular benchmark
- the pooled valley-wide spread read has been demoted to a weaker intermediate diagnostic

### Strongest confirmed conclusion
The first bounded support for the toy gravity saturation law is now real, but it is local to the near-mass packet: packet-local action `Q` beats both raw action gap and pooled-spread action `Q` only on the retained near-mass skirt probe.

### Exact next step
- translate the winning packet-local denominator into one adaptive coherence-width observable and test whether that physical-language spread transfers across nearby near-mass cuts without retuning the numerator

### First concrete action
- extend the local-action compare with one adaptive peak-centered spread rule and rerender the same near-mass probe family
