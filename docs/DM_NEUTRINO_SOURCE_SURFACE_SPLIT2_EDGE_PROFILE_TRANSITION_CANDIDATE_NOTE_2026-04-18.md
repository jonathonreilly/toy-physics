# DM Neutrino Source-Surface Split-2 Edge-Profile Transition Candidate

**Date:** 2026-04-18  
**Status:** bounded - bounded or caveated result note
**Primary runner:** `scripts/frontier_dm_neutrino_source_surface_split2_edge_profile_transition_candidate.py`

## Question

Can the compact-branch split-2 broad-bundle failure be reduced from a
three-real rival window to a one-dimensional active-slack edge profile?

## Bottom line

Yes, on the tested broad exact shift-quotient bundle.

The previous split-2 boundary-band scan already showed that the broad-box
minimum is pinned to

- the upper `m` edge `m = -0.14`,
- the lower active-slack edge `s = q_+ - q_floor(delta) = s_min`.

So the tested split-2 broad failure reduces to the one-dimensional profile

`R_split2(s) = min_delta Lambda_+(-0.14, delta, s)`.

On the tested compact branch, this profile is strictly increasing and crosses
the preferred recovered floor

`Lambda_+(x_*) = 1.586874714730`

at the explicit threshold

`s_* ~= 0.195041737783`.

The preferred recovered point has active slack

`s_pref = 0.215677476525`,

so it lies outside the tested split-2 broad danger interval by the positive
margin

`s_pref - s_* ~= 0.020635738742`.

Equivalently, on the tested broad split-2 edge the only undercut region is the
one-dimensional interval

`0 <= s < s_*`.

## Why this matters

This is a stronger carrier-side reduction than the earlier broad-window scan.

Before this refinement, the compact branch only knew:

- endpoint broad-bundle dominance is safely above the preferred floor,
- split-1 broad-bundle dominance is safely above the preferred floor,
- split-2 broad-bundle failure is confined to a narrow low-slack band.

After this refinement, the split-2 broad-bundle obstruction is sharper again:

- it is not a three-real box problem,
- it is not even a two-real low-slack strip problem,
- on the tested broad bundle it is a one-dimensional edge interval.

So the remaining useful carrier-side theorem target is now closer to:

> exclude or dominate the low-slack split-2 edge interval on the finer exact
> carrier.

## Sample profile values

| `s` | minimizing `delta_*` on the edge | `R_split2(s)` |
| --- | --- | --- |
| `0.0000` | `0.997049893395` | `1.500442491658` |
| `0.0500` | `1.015340586826` | `1.519822893168` |
| `0.1000` | `1.032895484591` | `1.541184222341` |
| `0.1500` | `1.049709935161` | `1.564422358252` |
| `0.1900` | `1.062628221090` | `1.584292566963` |
| `0.1950` | `1.064209774218` | `1.586853268538` |
| `0.1975` | `1.064997803629` | `1.588139902559` |
| `0.2000` | `1.065783976339` | `1.589430707582` |

## Boundary

This is still a numerical candidate on the broad exact shift-quotient bundle.
It is **not an interval-certified theorem** on the true exact carrier, and it
is **not flagship closure**.

What it does honestly establish is that the compact-branch carrier obstruction
has become much narrower:

- broad split-2 failure now reduces to the one-dimensional edge interval
  `0 <= s < s_*`,
- with `s_* ~= 0.195041737783`,
- while the preferred recovered point already sits at
  `s_pref = 0.215677476525 > s_*`.
