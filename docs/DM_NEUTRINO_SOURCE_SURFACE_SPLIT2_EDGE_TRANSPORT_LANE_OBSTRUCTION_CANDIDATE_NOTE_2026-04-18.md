# DM Neutrino Source-Surface Split-2 Edge Transport-Lane Obstruction Candidate

**Date:** 2026-04-18  
**Status:** bounded - bounded or caveated result note
**Primary runner:** `scripts/frontier_dm_neutrino_source_surface_split2_edge_transport_lane_obstruction_candidate.py`

## Inputs

This note depends on:

- [DM_NEUTRINO_SOURCE_SURFACE_CARRIER_NORMAL_FORM_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_CARRIER_NORMAL_FORM_THEOREM_NOTE_2026-04-16.md)
- [DM_NEUTRINO_SOURCE_SURFACE_SHIFT_QUOTIENT_BUNDLE_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_SHIFT_QUOTIENT_BUNDLE_THEOREM_NOTE_2026-04-16.md)
- [DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md)
- [DM_NEUTRINO_SOURCE_SURFACE_SPLIT2_BOUNDARY_BAND_TRANSITION_CANDIDATE_NOTE_2026-04-18.md](./DM_NEUTRINO_SOURCE_SURFACE_SPLIT2_BOUNDARY_BAND_TRANSITION_CANDIDATE_NOTE_2026-04-18.md)
- [DM_NEUTRINO_SOURCE_SURFACE_SPLIT2_EDGE_PROFILE_TRANSITION_CANDIDATE_NOTE_2026-04-18.md](./DM_NEUTRINO_SOURCE_SURFACE_SPLIT2_EDGE_PROFILE_TRANSITION_CANDIDATE_NOTE_2026-04-18.md)

The carrier and bundle theorems supply the active slack chart and the shift
quotient; the split-2 boundary-band and edge-profile transitions supply the
preferred lift, the edge interval, and the edge minimization scan that this
transport-lane comparison is phrased on.

## Question

After reducing the broad split-2 bundle pressure to the one-dimensional edge
interval

\[
0 \le s \le s_*^{\mathrm{edge}} \approx 0.195041737783,
\]

with

\[
m = -0.14, \qquad
\delta = \delta_{\mathrm{edge}}(s)
\]

chosen by minimizing \(\Lambda_+\) on that edge, does this dangerous edge
already realize the same transport-selected packet lane as the preferred
recovered point?

## Answer

No, on the tested interval.

The preferred recovered point remains

\[
x_* = (m_*,\delta_*,s_*)
= (1.021038842009,\;1.380791428982,\;0.215677476525),
\]

with

\[
q_{+*} = 0.467879209399,
\qquad
\eta_{\mathrm{best}}(x_*)/\eta_{\mathrm{obs}} = 1.052220313052,
\]

and preferred winning transport column

\[
Q_{\mathrm{pref}}
= \operatorname{sort}(P_{\mathrm{best}}(x_*))
= (0.035644251472,\;0.035644362528,\;0.928711385999).
\]

By contrast, on the tested dangerous split-2 edge:

- at \(s=0\),
  \[
  \delta_{\mathrm{edge}} = 0.997049893395,\quad
  q_+ = 0.635943268461,\quad
  \eta_{\mathrm{best}}/\eta_{\mathrm{obs}} = 0.847299300834,
  \]
  with winning column
  \[
  \operatorname{sort}(P_{\mathrm{best}})
  = (0.026383373029,\;0.429667915741,\;0.543948711230);
  \]

- at \(s=0.1\),
  \[
  \delta_{\mathrm{edge}} = 1.032895484591,\quad
  q_+ = 0.700097677265,\quad
  \eta_{\mathrm{best}}/\eta_{\mathrm{obs}} = 0.794943196720,
  \]
  with winning column
  \[
  \operatorname{sort}(P_{\mathrm{best}})
  = (0.017335713126,\;0.439872968303,\;0.542791318571);
  \]

- at the edge threshold \(s=s_*^{\mathrm{edge}}\),
  \[
  \delta_{\mathrm{edge}} = 1.064222961126,\quad
  q_+ = 0.763811938512,\quad
  \eta_{\mathrm{best}}/\eta_{\mathrm{obs}} = 0.771460755068,
  \]
  with winning column
  \[
  \operatorname{sort}(P_{\mathrm{best}})
  = (0.122813493967,\;0.185772584379,\;0.691413921653).
  \]

On the full tested dangerous interval \(0 \le s \le s_*^{\mathrm{edge}}\), the
best winning transport column stays decisively off the preferred lane:

- maximum winning transport value:
  \[
  \max \eta_{\mathrm{best}}/\eta_{\mathrm{obs}}
  = 0.847299300834,
  \]
  so the whole tested edge stays at least
  \[
  1.052220313052 - 0.847299300834 = 0.204921012218
  \]
  below the preferred recovered lane;

- minimum packet distance to the preferred winning quotient:
  \[
  \min \left\| \operatorname{sort}(P_{\mathrm{best}}) - Q_{\mathrm{pref}} \right\|_2
  = 0.293939334980;
  \]

- minimum leakage asymmetry:
  \[
  \min |p_2 - p_1| = 0.057100889715,
  \]
  which is far from the preferred near-symmetric small-leakage pair
  \((0.035644251472,0.035644362528)\);

- maximum dominant entry:
  \[
  \max p_3 = 0.691413921653,
  \]
  still far below the preferred dominant entry \(0.928711385999\).

## Interpretation

This does **not** close the carrier problem. It does sharpen it.

The broad split-2 low-slack undercut is a real broad-bundle phenomenon, but on
the tested edge interval it is **transport-incompatible** with the preferred
recovered lane. So the remaining carrier-side question is no longer:

> can any broad split-2 low-slack point undercut the preferred repair floor?

It is now:

> can the exact transport carrier itself enter a lower-repair,
> transport-compatible lane inside that low-slack split-2 interval?

That is a much smaller target than generic broad-window global dominance.

## Boundary

This is still a numerical candidate on the tested broad split-2 edge. It is
not interval-certified exact-carrier closure, and it is not flagship closure.
