# DM Neutrino Source-Surface Split-2 Lower-Repair Upper-Face Extremals Candidate

**Date:** 2026-04-18  
**Status:** positive-path carrier reduction candidate on the tested split-2
lower-repair box  
**Primary runner:** `scripts/frontier_dm_neutrino_source_surface_split2_lower_repair_upper_face_extremals_candidate.py`

## Question

On the tested split-2 low-slack box, under the lower-repair constraint
`Lambda_+ <= Lambda_+(x_*)`, does the remaining transport pressure still fill a
region, or does it already collapse to explicit upper-face extremals?

## Bottom line

On the tested box, it already collapses sharply.

First, on sampled lower-repair slices of the tested split-2 box, both
transport-facing objectives drift monotonically toward the upper-`m` face
`m = -0.14`:

- slice-wise best lower-repair `eta/eta_obs` values increase from
  `0.872788884919` at `m=-0.19` to `0.884471224505` at `m=-0.14`,
- slice-wise closest-lane distances decrease from `0.299621069662` at
  `m=-0.19` to `0.233486690453` at `m=-0.14`.

Second, on the sampled upper face `m=-0.14`, the lower-repair best-eta problem
collapses to the repair-cap boundary

```text
Lambda_+(-0.14, delta_cap(s), s) = Lambda_+(x_*).
```

On the sampled cap profile:

- `delta_cap(s)` decreases monotonically with `s`,
- the sampled cap-eta profile is unimodal,
- the sampled peak occurs at
  `s ~= 0.0195041737783`,
  `delta_cap ~= 1.188513342509166`,
  `eta/eta_obs ~= 0.884523189582`.

That is still far below transport closure.

Third, the sampled closest-lane point on the whole upper-face feasible region
is not that cap-eta peak. It is the slack-floor endpoint:

```text
(m, s, delta) = (-0.14, 0, 1.188955544069478)
```

with

```text
||sort(P_best) - Q_pref||_2 ~= 0.233274467128
eta/eta_obs ~= 0.883631424817.
```

So the tested broad split-2 low-slack pressure is no longer a diffuse box and
no longer merely a vague upper-`m` ridge. It is already reduced to **two
explicit upper-face extremals**:

1. a best-eta cap point at small positive slack;
2. a closest-lane slack-floor endpoint.

Both remain transport-incompatible with the preferred recovered lane.

## What is new here

The previous compact branch only said that tested lower-repair transport
pressure drifts toward an upper-`m`, low-slack ridge.

This note sharpens that further:

- broad-box lower-repair transport pressure drifts monotonically to `m=-0.14`,
- on that upper face the best-eta search is governed by a one-dimensional
  repair-cap profile,
- and the closest-lane point is already pinned to the slack-floor endpoint.

So the tested broad split-2 transport threat is now compressed to two explicit
upper-face extremals rather than a whole box or even a full ridge.

## What this does not prove

This is **not** interval-certified exact-carrier closure.

It does not prove:

- that the true exact carrier is exhausted by this sampled upper-face picture,
- that no unsampled exact-carrier point near those two extremals can do better,
- or that exact-carrier completeness / global dominance is closed.

It only says the tested broad split-2 lower-repair pressure is now concentrated
at two explicit upper-face extremals, both still transport-incompatible.

## Command

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_source_surface_split2_lower_repair_upper_face_extremals_candidate.py
```
