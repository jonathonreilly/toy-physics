# DM Neutrino Source-Surface Rival-Window Edge-Profile Hierarchy Candidate

**Date:** 2026-04-18  
**Status:** compact-branch carrier-side refinement candidate  
**Primary runner:** `scripts/frontier_dm_neutrino_source_surface_rival_window_edge_profile_hierarchy_candidate.py`

## Question

Once split-2 is reduced to a one-dimensional edge profile on the tested broad
bundle, what remains of endpoint and split-1 on the same footing?

## Bottom line

On the tested broad exact shift-quotient bundle, the three rival windows obey a
strict edge-profile hierarchy

`R_endpoint(s) > R_split1(s) > R_split2(s)`

across the tested slack range, with all three profiles strictly increasing in
the active slack coordinate `s`.

At zero slack:

- `R_endpoint(0) = 3.027555846610`
- `R_split1(0) = 2.308603400914`
- `R_split2(0) = 1.500442491658`

against the preferred recovered floor

`Lambda_+(x_*) = 1.586874714730`.

So endpoint and split-1 are already dominated from `s = 0` upward on the
tested broad bundle, while split-2 alone crosses the preferred floor, at the
previously isolated threshold

`s_* ~= 0.195041737783`.

Therefore, on the tested broad exact bundle, broad-window carrier pressure
collapses entirely to the one-dimensional split-2 edge interval

`0 <= s < s_*`.

## Why this matters

This is a cleaner carrier-side reduction than the earlier three-window phrasing.

It means the compact branch is no longer carrying three comparable broad-window
threats on the tested broad bundle:

- endpoint is not live there,
- split-1 is not live there,
- split-2 alone is live there,
- and even split-2 is reduced to one edge interval rather than a full box.

So the carrier-side theorem target is now much sharper:

> move from broad-bundle control to finer exact-carrier control on the single
> split-2 edge interval `0 <= s < s_*`.

## Boundary

This is still a numerical candidate on broad exact-bundle edge profiles. It is
**not an interval-certified theorem** on the finer exact carrier, and it is
**not flagship closure**.

What it honestly supports is the next carrier-side compression:

- the broad-bundle rival geometry is no longer a three-window problem,
- it is no longer a full split-2 box problem,
- it is only a split-2 edge-interval problem on the tested broad bundle.
