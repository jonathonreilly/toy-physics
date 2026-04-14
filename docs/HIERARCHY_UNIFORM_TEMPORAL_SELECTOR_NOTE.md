# Hierarchy Uniform Temporal Selector Note

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_hierarchy_uniform_temporal_selector.py`

## Question

Can the final hierarchy normalization be selected from the exact finite-`L_t`
family without introducing a new fitted constant?

## Proposed exact selector

Yes, provided the physical dimension-4 order parameter obeys the following
minimal locality rule:

> it should average over a full **time-resolved** APBC temporal orbit without
> mode-dependent weighting inside that minimal orbit.

On the exact minimal hierarchy block, that means the APBC temporal weights

`sin^2((2n+1) pi / L_t)`

must be constant across the chosen orbit.

## Exact solution

That uniformity condition is very restrictive.

Among even `L_t`, the only solutions are:

- `L_t = 2`
- `L_t = 4`

This follows already from the first two APBC modes:

`sin^2(pi / L_t) = sin^2(3 pi / L_t)`

whose even positive solutions are exactly `L_t = 2, 4`.

## Why `L_t = 4`

`L_t = 2` is the unresolved UV endpoint. It has only the single absolute
temporal gap `|sin omega| = 1`.

`L_t = 4` is the **unique minimal resolved uniform orbit**:

- it contains four distinct APBC phases
  `{pi/4, 3pi/4, 5pi/4, 7pi/4}`
- yet all of them carry the same temporal weight
  `sin^2 omega = 1/2`

So `L_t = 4` is the first orbit that is both:

1. genuinely time-resolved
2. exactly mode-uniform

That makes it the unique exact selector if the order parameter is required to
be local and mode-blind on its minimal temporal orbit.

## Consequence

The exact physical correction becomes:

`C_phys = C(4) = (A_2 / A_4)^(1/4) = (7/8)^(1/4)`

Numerically:

- `C_phys = (7/8)^(1/4) ~= 0.967168210`
- baseline hierarchy value `253.4 GeV`
- selected prediction
  `v_phys = 253.4 * (7/8)^(1/4) ~= 245.08 GeV`

This is within `0.5%` of the observed `246.22 GeV`.

## Honest status

This is the strongest exact closure route so far.

What is now exact:

1. the finite-`L_t` family
2. the selector equation for uniform temporal weight
3. the uniqueness of `L_t = 4` as the minimal resolved uniform orbit
4. the correction `C_phys = (7/8)^(1/4)`

What still remains an assumption is the physical selector principle itself:

> the EWSB order parameter should be local and mode-blind on the minimal
> time-resolved APBC orbit.

If that principle is accepted, the hierarchy normalization is effectively
closed on the exact minimal block. If one insists on deriving even that
selector from still deeper structure, then one last interpretive step remains.
