# DM Neutrino Source-Surface Global Dominance Completeness Obstruction

**Date:** 2026-04-17  
**Status:** exact obstruction note for the carrier side of the top-down selector
attack; publishable even without selector closure  
**Primary runner:** `scripts/frontier_dm_neutrino_source_surface_global_dominance_completeness_obstruction.py`

## Question

Once the selector class is compressed to the canonical positive-probe extremal
law, can the preferred recovered point already be promoted to a full
exact-carrier winner?

## Bottom line

No.

After the representation-theorem compression, the live blocker is not more
selector-family freedom. It is exactly **global dominance / exact-carrier
completeness**.

The branch does support:

- a unique least-repair winner on the recovered five-lift carrier,
- a positive recovered-carrier gap above the next recovered competitor,
- a strong local endpoint dominance candidate on the exact shift-quotient
  bundle over the broad tested box
  `m in [-1.899713, -1.87]`, `delta in [-2.5, 2.5]`, `r31 in [0.5, 4.0]`,
  with tested minimum repair `3.027555919409 > 1.586874714730`,
- a strong local split-1 dominance candidate on the exact shift-quotient
  bundle over the broad tested box
  `m in [-1.16, -1.10]`, `delta in [-2.5, 2.5]`, `r31 in [0.5, 4.0]`,
  with tested minimum repair `2.308603400914 > 1.586874714730`,
- a split-2 boundary-band transition candidate on the same broad bundle domain:
  on the active slack chart `s = q_+ - q_floor(delta)`, the split-2 undercut is
  confined to a narrow low-slack band `0.195 <= s_* <= 0.1975`, and the tested
  split-2 broad box is already above the preferred recovered floor once
  `s >= 0.2`,
- an edge-profile refinement of that split-2 story: on the tested broad bundle,
  the split-2 danger reduces to the one-dimensional profile
  `R_split2(s) = min_delta Lambda_+(-0.14, delta, s)` with threshold
  `s_* ~= 0.195041737783`, while the preferred recovered point sits at
  `s_pref = 0.215677476525`,
- and a rival-window edge-profile hierarchy on the tested broad bundle:
  endpoint and split-1 are already dominated from `s = 0` upward, so the
  tested broad-window carrier pressure collapses entirely to the split-2 edge
  interval `0 <= s < s_*`,
- and a split-2 edge transport-lane obstruction candidate on that same tested
  edge interval: the broad low-slack undercut does not realize the preferred
  recovered transport lane, since on the tested interval its best
  `eta/eta_obs` stays below `0.847299300834` while the preferred recovered lane
  sits at `1.052220313052`, and its winning packet columns stay separated from
  the preferred small-leakage quotient,
- and a broader split-2 low-slack transport incompatibility candidate on the
  tested box `m in [-0.19,-0.14]`, `delta in [-2.5,2.5]`, `0 <= s <= s_*`:
  under the lower-repair constraint `Lambda_+ <= Lambda_+(x_*)`, no tested
  sample reaches `eta/eta_obs >= 1`, seeded global searches keep the best
  lower-repair transport rival below `0.884523453538`, and the closest tested
  lower-repair packet lane still stays at distance at least `0.233468501596`
  from the preferred quotient,
- and a localized rival-window picture with exactly three exposed unresolved
  windows:
  `[-1.899713, -1.87]`, `[-1.16, -1.10]`, and `[-0.19, -0.14]`.

But the branch does **not** yet prove:

- that the recovered carrier already exhausts the full exact carrier,
- that every unsampled point inside those windows is attached to a dominated
  known sheet,
- or that every unrecovered exact point must have larger `Lambda_+`
  than the preferred point.

So the honest exact obstruction is:

> representation is compressed, but the branch still stops at
> exact-carrier completeness / global dominance.

## Exact obstruction shape

### 1. Recovered-carrier dominance is already real

On the recovered bank the preferred point

`(m, delta, slack) = (1.021038842009447, 1.380791428981559, 0.215677476525045)`

is the unique least-repair lift and therefore the recovered-bank winner for the
canonical extremal score as well.

That part is no longer the live ambiguity.

### 2. The rival-side uncertainty is localized, not diffuse

The rebuilt transport picture is no longer “search everywhere.” The unresolved
carrier geometry is concentrated in three exposed windows:

- endpoint window: `m in [-1.899713, -1.87]`
- split-1 window: `m in [-1.16, -1.10]`
- split-2 window: `m in [-0.19, -0.14]`

Outside those windows, the present branch explanation is already stable. Inside
them, the branch supports a genuine local multi-sheet picture on the sampled
regime, including the still-underresolved split-2 slice.

On the compact branch, endpoint and split-1 are no longer the sharpest
low-repair suspects on the tested exact bundle domain: their current broad-box
minima sit well above the preferred recovered floor, and the tested
high-`r31` and high-|`delta`| tails are higher still. That strengthens the
support picture, but it is still not a certified local dominance theorem for
either window.

At the same time, the broad exact shift-quotient bundle is now known to be too
coarse to serve as the final dominance theorem domain: on the same broad tested
bundle boxes, split-2 already carries a boundary-controlled minimum below the
preferred recovered floor. But the compact branch now knows more than that raw
counterexample: on the active slack chart the broad split-2 undercut is
localized first to a narrow low-slack boundary band, and then further to the
one-dimensional edge interval `0 <= s < s_*` on the tested edge profile
`R_split2(s)`. So the remaining useful carrier theorem really does have to use
the finer exact carrier restriction, and on split-2 it only needs to exclude or
dominate that low-slack edge interval rather than every broad-bundle point.
And even that edge interval is now sharper than a generic broad undercut:
on the tested split-2 edge it is transport-incompatible with the preferred
recovered lane, so the remaining carrier theorem only needs to rule out a
lower-repair, transport-compatible lane there, not just any lower-repair broad
bundle point. The branch now goes a bit further on the tested broad split-2
low-slack box as well: no lower-repair transport-compatible lane is currently
visible there either. So the remaining carrier theorem target is no longer a
generic broad split-2 search, but interval-style exclusion or dominance on the
exact carrier inside the residual split-2 low-slack region.

### 3. The missing theorem is interval-certified completeness or dominance

To promote the recovered winner to a full exact-carrier winner, the branch
would need at least one of:

1. an exact completeness theorem for the carrier;
2. an interval-certified exclusion theorem for every unresolved rival window;
3. a global lower-bound theorem proving every unrecovered exact point has
   larger `Lambda_+` than the preferred point.

The current branch proves none of those.

### 4. Therefore global dominance cannot be promoted honestly

The correct branch verdict is not “carrier search continues.” It is narrower:

- current recovered-carrier dominance is fixed,
- current unresolved rival geometry is localized,
- but interval-certified completeness/global dominance is still unproved.

That is the exact point where this branch stops.

## Practical consequence

The next carrier-side work should be only one of:

1. prove exact-carrier completeness;
2. prove a rival-window dominance theorem strong enough to avoid full
   completeness, now especially on a lower-repair, transport-compatible lane
   inside the residual exact-carrier part of the low-slack split-2 region;
3. prove a no-go theorem that current exact methods cannot certify those
   windows.

Anything broader is below the current reduction surface.

## Canonical validation

- [DM_NEUTRINO_SOURCE_SURFACE_MICROSCOPIC_POSITIVE_PROBE_REPRESENTATION_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_MICROSCOPIC_POSITIVE_PROBE_REPRESENTATION_THEOREM_NOTE_2026-04-17.md)
- [DM_NEUTRINO_SOURCE_SURFACE_SPLIT2_BOUNDARY_BAND_TRANSITION_CANDIDATE_NOTE_2026-04-18.md](./DM_NEUTRINO_SOURCE_SURFACE_SPLIT2_BOUNDARY_BAND_TRANSITION_CANDIDATE_NOTE_2026-04-18.md)
- [DM_NEUTRINO_SOURCE_SURFACE_SPLIT2_EDGE_PROFILE_TRANSITION_CANDIDATE_NOTE_2026-04-18.md](./DM_NEUTRINO_SOURCE_SURFACE_SPLIT2_EDGE_PROFILE_TRANSITION_CANDIDATE_NOTE_2026-04-18.md)
- [DM_NEUTRINO_SOURCE_SURFACE_RIVAL_WINDOW_EDGE_PROFILE_HIERARCHY_CANDIDATE_NOTE_2026-04-18.md](./DM_NEUTRINO_SOURCE_SURFACE_RIVAL_WINDOW_EDGE_PROFILE_HIERARCHY_CANDIDATE_NOTE_2026-04-18.md)
- [DM_NEUTRINO_SOURCE_SURFACE_SPLIT2_EDGE_TRANSPORT_LANE_OBSTRUCTION_CANDIDATE_NOTE_2026-04-18.md](./DM_NEUTRINO_SOURCE_SURFACE_SPLIT2_EDGE_TRANSPORT_LANE_OBSTRUCTION_CANDIDATE_NOTE_2026-04-18.md)
- [DM_NEUTRINO_SOURCE_SURFACE_SPLIT2_LOW_SLACK_TRANSPORT_INCOMPATIBILITY_CANDIDATE_NOTE_2026-04-18.md](./DM_NEUTRINO_SOURCE_SURFACE_SPLIT2_LOW_SLACK_TRANSPORT_INCOMPATIBILITY_CANDIDATE_NOTE_2026-04-18.md)
- [frontier_dm_neutrino_source_surface_microscopic_positive_probe_representation_theorem.py](../scripts/frontier_dm_neutrino_source_surface_microscopic_positive_probe_representation_theorem.py)
- [frontier_dm_neutrino_source_surface_split2_boundary_band_transition_candidate.py](../scripts/frontier_dm_neutrino_source_surface_split2_boundary_band_transition_candidate.py)
- [frontier_dm_neutrino_source_surface_split2_edge_profile_transition_candidate.py](../scripts/frontier_dm_neutrino_source_surface_split2_edge_profile_transition_candidate.py)
- [frontier_dm_neutrino_source_surface_rival_window_edge_profile_hierarchy_candidate.py](../scripts/frontier_dm_neutrino_source_surface_rival_window_edge_profile_hierarchy_candidate.py)
- [frontier_dm_neutrino_source_surface_split2_edge_transport_lane_obstruction_candidate.py](../scripts/frontier_dm_neutrino_source_surface_split2_edge_transport_lane_obstruction_candidate.py)
- [frontier_dm_neutrino_source_surface_split2_low_slack_transport_incompatibility_candidate.py](../scripts/frontier_dm_neutrino_source_surface_split2_low_slack_transport_incompatibility_candidate.py)
- [frontier_dm_neutrino_source_surface_global_dominance_completeness_obstruction.py](../scripts/frontier_dm_neutrino_source_surface_global_dominance_completeness_obstruction.py)
