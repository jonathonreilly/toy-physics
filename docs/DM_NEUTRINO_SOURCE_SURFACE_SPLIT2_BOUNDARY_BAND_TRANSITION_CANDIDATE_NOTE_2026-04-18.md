# DM Neutrino Source-Surface Split-2 Boundary-Band Transition Candidate

**Date:** 2026-04-18  
**Status:** compact-branch carrier-side refinement candidate  
**Primary runner:** `scripts/frontier_dm_neutrino_source_surface_split2_boundary_band_transition_candidate.py`

## Question

On the compact branch, is the broad-bundle split-2 failure really spread across
the whole split-2 rival window, or is it concentrated near the active
boundary?

## Bottom line

It is concentrated near the active boundary.

On the broad exact shift-quotient bundle, rewrite the split-2 box in the exact
active slack coordinate

`s = q_+ - q_floor(delta) >= 0`.

Then on the tested split-2 broad box

- `m in [-0.19, -0.14]`,
- `delta in [-2.5, 2.5]`,
- `s in [s_min, sqrt(16 - 1/4)]`,

the tested minimum repair is monotone in the slack floor `s_min`, and every
tested minimizer stays pinned to the same boundary corner:

- upper `m` edge: `m = -0.14`,
- lower slack edge: `s = s_min`.

The preferred recovered floor is

`Lambda_+(x_*) = 1.586874714730`.

The broad split-2 minimum crosses that floor inside a narrow low-slack band:

- at `s_min = 0.1950`, the tested minimum is `1.586853268538 < 1.586874714730`
- at `s_min = 0.1975`, the tested minimum is `1.588139902559 > 1.586874714730`

So on the tested broad split-2 box, the undercut is confined to

`0.195 <= s_* <= 0.1975`.

In particular, once the broad split-2 box is restricted to

`q_+ - q_floor(delta) = s >= 0.2`,

its tested minimum is already

`1.589430707582 > 1.586874714730`.

## Why this matters

This sharpens the carrier-side obstruction materially.

Before this refinement, the compact branch only knew that the broad exact
bundle was too coarse because split-2 on that domain dipped below the preferred
recovered floor.

After this refinement, the compact branch knows more:

- endpoint broad exact-bundle dominance is safely above the preferred floor,
- split-1 broad exact-bundle dominance is safely above the preferred floor,
- split-2 broad exact-bundle failure is not diffuse across the window,
- it is localized to a narrow low-slack boundary band on the active chart.

So the useful remaining carrier-side theorem target is no longer “control all
of split-2 on the broad bundle.” It is closer to:

> prove that the exact carrier cannot enter the low-slack split-2 boundary band,
> or prove local dominance there directly on the finer exact carrier.

## Sample transition table

| slack floor `s_min` | tested minimum repair |
| --- | --- |
| `0.00` | `1.500442491658` |
| `0.05` | `1.519822893168` |
| `0.10` | `1.541184222341` |
| `0.15` | `1.564422362358` |
| `0.19` | `1.584292566963` |
| `0.20` | `1.589430707582` |
| `0.25` | `1.616102220815` |
| `0.30` | `1.644331050529` |

## Boundary

This is still a numerical candidate on broad exact-bundle boxes in the active
slack chart. It is **not an interval-certified dominance theorem** on the true
exact carrier, and it is **not flagship closure**.

What it does honestly support is a sharper statement of the remaining compact
carrier obstruction:

- the broad split-2 danger is now localized to a narrow low-slack boundary band,
- so the next exact theorem only has to eliminate or dominate that band, not
  the whole broad split-2 window.
