# Two-Body Attraction Temporal Robustness Note

**Date:** 2026-04-11  
**Status:** bounded positive on the open-Wilson side lane; temporal boundary now frozen  
**Script:** `scripts/frontier_two_body_attraction_temporal_robustness.py`

## Question

Does the current low-screening open-Wilson near-inverse-square mutual-channel
law survive alternate analysis windows or longer traces on the same audited
surface?

This note does **not** widen the geometry class. It keeps the same narrow
surface and only changes the trace length and windowing:

- open 3D Wilson lattice
- `side = 20`
- centered placement family
- separations `d = 4, 6, 8, 10, 12`
- `MASS = 0.3`
- `WILSON_R = 1.0`
- `G = 5`
- `mu^2 = 0.001`
- `sigma = 1.0`
- `DT = 0.08`

Retained observable:

- `a_mutual(t) = a_sep(shared) - a_sep(self_only)`

The distance-law fit in this note is always:

- an **early-time** fit
- on `|a_mutual|`, not signed `a_mutual`
- on the named window only
- on rows that remain attractive on that same window

## Main Result

The low-screening open-Wilson law is **temporally robust only in the early and
mid-early windows**. It is not a full-trace law.

What survives:

- `15`-step trace:
  - `w2_10`: `5/5` attractive, `5/5` clean, `|a_mut| ~ d^-1.965`, `R^2 = 0.9999`
  - `w3_11`: `5/5` attractive, `5/5` clean, `|a_mut| ~ d^-1.957`, `R^2 = 0.9999`
  - `w6_14`: `5/5` attractive, `5/5` clean, `|a_mut| ~ d^-1.936`, `R^2 = 0.9997`
- `25`-step trace:
  - `w2_10`: `5/5` attractive, `5/5` clean, `|a_mut| ~ d^-1.965`, `R^2 = 0.9999`
  - `w6_14`: `5/5` attractive, `5/5` clean, `|a_mut| ~ d^-1.936`, `R^2 = 0.9997`
  - `w10_18`: `5/5` attractive, `5/5` clean, `|a_mut| ~ d^-1.997`, `R^2 = 0.9996`
- `35`-step trace:
  - `w2_10`: `5/5` attractive, `5/5` clean, `|a_mut| ~ d^-1.965`, `R^2 = 0.9999`
  - `w10_18`: `5/5` attractive, `5/5` clean, `|a_mut| ~ d^-1.997`, `R^2 = 0.9996`

What fails:

- `25`-step `w14_22`: only `1/5` attractive, `0/5` clean
- `35`-step `w18_26`: only `1/5` attractive, `0/5` clean
- `35`-step `w26_34`: `5/5` attractive but `0/5` clean, with a flattened fit
  `|a_mut| ~ d^-1.199`, `R^2 = 0.7017`

So the near-inverse-square law is robust through the early/mid-early part of
the trace and then breaks.

## Physical Boundary

With `DT = 0.08`, the last still-retainable window is:

- `w10_18 = [10:19]`, roughly `t ≈ 0.80` to `1.44`

Past that:

- the sign is no longer stable by `w14_22` / `w18_26`
- and the very late `w26_34` window is too noisy and too flat to count as the
  same law even though it remains weakly attractive on this surface

This is the exact temporal boundary for the current bounded Wilson lane:

> the near-inverse-square mutual-channel law is an early-to-mid-early trace
> result, not a full-trace result.

## Additional Read

A separate, weaker statement remains true even after the fit collapses:

- both packets still end inward relative to `self_only` on every audited row
  for `15`, `25`, and `35` steps

But that final-displacement fact is **not** enough to extend the distance-law
claim. The law itself only survives through the windows above.

## Honest Bounded Statement

The correct retained wording for this lane is:

> On the low-screening open-Wilson centered surface (`side=20`, `d=4..12`,
> `G=5`, `mu^2=0.001`), the shared-vs-self-only mutual-channel attraction keeps
> a near-inverse-square early-time law through windows up to `w10_18`
> (`t ≈ 0.80..1.44`), but the law does not survive as a clean full-trace or
> very-late-window statement.

That is stronger than the earlier single-window read because it freezes the
temporal boundary exactly. It is still:

- one Wilson architecture
- one geometry family
- one observable family
- not both-masses closure
- not action-reaction closure
- not repo-wide Newton closure
