# Two-Body Attraction Temporal Robustness Note

**Date:** 2026-04-11  
**Status:** bounded positive on early/mid windows only; not a late-time or full-trace law  
**Script:** `frontier_two_body_attraction_temporal_robustness.py`

## Question

Does the bounded low-screening open-Wilson mutual-attraction law remain
near-inverse-square when the same trajectories are scored on alternate time
windows, not just the original early window?

## Intended Surface

This note stays on the same audited open-Wilson surface as the existing
side/placement robustness note:

- open 3D Wilson lattice
- `MASS = 0.3`
- `WILSON_R = 1.0`
- `G = 5`
- `mu^2 = 0.001`
- `REG = 1e-3`
- `sigma = 1.0`
- sides `18, 20, 22`
- placement families `centered`, `face_offset`, `corner_offset`
- separations `d = 4, 6, 8, 10, 12`

Temporal extension:

- trace length increased from `15` to `35` steps
- fixed windows:
  - `w02_10 = [2, 11)`
  - `w05_13 = [5, 14)`
  - `w08_16 = [8, 17)`
  - `w11_19 = [11, 20)`
  - `w14_22 = [14, 23)`
  - `w17_25 = [17, 26)`

## Observable

As before, the retained object is the shared-vs-self-only separation residual:

`a_mutual = a_sep(shared) - a_sep(self_only)`

For each fixed window, the runner records:

- sign of the mean residual acceleration
- `SNR = |mean| / std`
- whether both packets move inward relative to `self_only` over that window
- a bounded early-/mid-/late-window fit of `|a_mutual| ~ d^alpha`

## Retention Boundary

This lane is bounded even if it stays positive.

It can support at most:

> On the audited open-Wilson surface, the mutual-channel residual remains
> attractive and near inverse-square on specific fixed early-time windows of a
> longer trace.

It cannot by itself support:

- full-trace Newton closure
- both-masses closure
- action-reaction closure
- cross-architecture robustness
- a claim that the late-time tail is stable unless the rerun actually shows it

## Rerun Result

The early/mid-window law survives cleanly on the full audited surface, but the
late windows do not.

Global window table:

- `w02_10 = [2, 11)`
  - attract `45/45`
  - clean `45/45`
  - inward `45/45`
  - strong `45/45`
  - `|a_mut| ~ d^-1.952`, `R^2 = 0.9986`
- `w05_13 = [5, 14)`
  - attract `45/45`
  - clean `45/45`
  - inward `45/45`
  - strong `45/45`
  - `|a_mut| ~ d^-1.943`, `R^2 = 0.9976`
- `w08_16 = [8, 17)`
  - attract `45/45`
  - clean `45/45`
  - inward `45/45`
  - strong `45/45`
  - `|a_mut| ~ d^-1.967`, `R^2 = 0.9933`
- `w11_19 = [11, 20)`
  - attract `45/45`
  - clean `11/45`
  - inward `45/45`
  - strong `11/45`
  - no retained global fit
- `w14_22 = [14, 23)`
  - attract `14/45`
  - clean `0/45`
  - inward `45/45`
  - strong `0/45`
  - no retained fit
- `w17_25 = [17, 26)`
  - attract `8/45`
  - clean `0/45`
  - inward `42/45`
  - strong `0/45`
  - no retained fit

Placement-family fits on the surviving windows stay close to inverse square:

- `w02_10`
  - `centered`: `-1.977`, `R^2 = 0.9994`
  - `face_offset`: `-1.952`, `R^2 = 0.9992`
  - `corner_offset`: `-1.927`, `R^2 = 0.9989`
- `w05_13`
  - `centered`: `-1.962`, `R^2 = 0.9984`
  - `face_offset`: `-1.943`, `R^2 = 0.9982`
  - `corner_offset`: `-1.925`, `R^2 = 0.9978`
- `w08_16`
  - `centered`: `-1.981`, `R^2 = 0.9947`
  - `face_offset`: `-1.967`, `R^2 = 0.9940`
  - `corner_offset`: `-1.953`, `R^2 = 0.9929`

## Exact Boundary

The honest bounded statement is:

> On the audited low-screening open-Wilson surface, the shared-vs-self-only
> mutual-channel residual remains attractive, clean, inward, and near
> inverse-square on fixed windows through `w08_16 = [8, 17)`.

And the exact failure boundary is:

- by `w11_19`, the signal stays negative everywhere but loses clean SNR on most
  rows, so the law is no longer retainable
- by `w14_22` and `w17_25`, the sign itself is no longer stable, so there is no
  late-window or full-trace force-law claim here

## Honest Read

This strengthens the Wilson side lane in one specific way:

- the near-`1/r^2` law is not confined to one single early slice
- it survives three distinct early/mid windows on the full `45`-row audited
  side/placement/separation surface

This also closes an important loophole:

- the retained Wilson law is **not** a full-trace statement
- it is an early-/mid-window statement on this observable family
- later windows lose first SNR, then sign stability

So the correct bounded retention candidate is:

> early-/mid-window near-inverse-square mutual-channel attraction on the
> audited open-Wilson surface

and not:

> a globally stable Newtonian two-body law over the full trace.
