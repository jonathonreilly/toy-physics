# 3D Staggered Self-Gravity Contraction / Sign Note

**Date:** 2026-04-11  
**Script:** `scripts/frontier_staggered_3d_self_gravity_sign.py`  
**Status:** bounded retained positive/negative split on `main`

## Question

On the **primary staggered architecture** itself, can a genuine 3D trajectory-side
self-gravity observable be made clean without touching the active both-masses
or self-consistent two-body lanes?

More specifically:

1. does an open 3D cubic staggered lattice show robust self-gravity contraction
   under the corrected parity coupling, and
2. if we flip the self-source sign in a matched centered control, do any
   blocked trajectory observables separate cleanly enough to claim sign closure?

## Surface

- open 3D cubic staggered lattice
- centered Gaussian packet
- parity-coupled scalar law:
  - `H_diag = (m + Phi) * epsilon(x)`
- self-field from the packet density:
  - `Phi = (L + mu^2)^(-1) (sign * G_self * |psi|^2)`
- parameters:
  - `mass = 0.30`
  - `G_self = 50.0`
  - `mu^2 = 0.001`
  - `dt = 0.10`
  - `N_steps = 20`
  - `sigma = 1.35`
- sizes:
  - `side = 9, 11, 13`

The readouts are deliberately symmetry-safe:

- **blocked `2x2x2` width ratio** versus the matched free run
- **core probability excess** inside radius `r <= 2.5` versus free
- **blocked-centroid drift** as a sanity check
- **shell-averaged potential gradient sign** as a field-side sign control

## Exact outputs

| side | sign | `w_self / w_free` | core excess | shell-grad sign | mean shell grad | max blocked drift | final blocked drift | norm drift |
|---|---|---:|---:|---|---:|---:|---:|---:|
| 9 | attract | `0.640444` | `+0.428363` | `20/20 > 0` | `+9.212495e-01` | `1.113307e-02` | `+1.108302e-02` | `2.220e-16` |
| 9 | repulse | `0.640430` | `+0.428364` | `0/20 > 0` | `-9.212474e-01` | `1.113461e-02` | `+1.108143e-02` | `2.220e-16` |
| 11 | attract | `0.634800` | `+0.429278` | `20/20 > 0` | `+9.400751e-01` | `1.129134e-02` | `-1.109208e-02` | `2.220e-16` |
| 11 | repulse | `0.634770` | `+0.429244` | `0/20 > 0` | `-9.400566e-01` | `1.128297e-02` | `-1.101589e-02` | `2.220e-16` |
| 13 | attract | `0.632080` | `+0.428541` | `20/20 > 0` | `+9.479870e-01` | `1.196830e-02` | `+1.039967e-02` | `4.441e-16` |
| 13 | repulse | `0.631604` | `+0.428475` | `0/20 > 0` | `-9.478437e-01` | `1.192501e-02` | `+1.004570e-02` | `4.441e-16` |

Aggregate comparisons:

- contraction holds for **both** signs at all sizes
- width-ratio separation is tiny:
  - `side=9`: `|Δ ratio| = 1.394913e-05`
  - `side=11`: `|Δ ratio| = 3.016553e-05`
  - `side=13`: `|Δ ratio| = 4.756634e-04`
- the field-side shell gradient flips perfectly:
  - attract: `20/20` positive
  - repulse: `0/20` positive

## What is real

This closes one narrow but important gap on the primary staggered lane:

- there is a **genuine 3D trajectory-level self-gravity contraction signal**
  on the open cubic staggered architecture
- the contraction is strong and stable:
  - blocked width ratios are `0.632 -> 0.640`
  - core probability gains are `+0.428 -> +0.429`
- norm stays machine-clean

So the primary staggered architecture is not limited to exact-force card rows;
it also supports a clean envelope-level 3D self-gravity contraction observable.

## What does not close

This lane does **not** produce a sign-selective 3D trajectory observable.

The matched sign-flip control is informative:

- the **field profile** knows the sign:
  - shell gradient flips exactly
- the **trajectory envelope** does not:
  - blocked width ratio and core concentration are effectively unchanged
  - blocked-centroid drift stays tiny and symmetric

That means the honest conclusion is:

> in centered 3D self-gravity on the primary staggered architecture, contraction
> is robust but sign-selective trajectory closure still fails.

This is consistent with the broader parity-coupling story:

- sign information can survive in force/field observables
- but centered packet-envelope dynamics can absorb the sign at the trajectory
  level

## Why this note is useful

This lane is deliberately separate from the active Newton / both-masses work.
It answers a different question:

- **Can the primary staggered architecture do anything trajectory-level in 3D
  besides external-source Newton fits?**

The answer is yes, but narrowly:

- **self-gravity contraction** is clean
- **sign-selective trajectory closure** is not

## Bottom line

Retain this as a bounded positive / negative split:

- **positive:** the primary staggered architecture has a real 3D blocked-envelope
  self-gravity contraction observable
- **negative:** the same centered self-gravity surface does not yield an honest
  sign-selective trajectory observable under a matched sign-flip control

So this lane strengthens the 3D staggered trajectory story without pretending
to close the remaining sign or Newton gaps.
