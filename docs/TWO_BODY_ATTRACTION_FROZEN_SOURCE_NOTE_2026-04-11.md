# Two-Body Attraction Frozen-Source Control Note

**Date:** 2026-04-11  
**Status:** bounded control result; hold for `main`  
**Script:** `scripts/frontier_two_body_attraction_frozen_source.py`

## Question

Does the audited low-screening open-Wilson mutual-attraction lane still beat a
frozen/static-source explanation when the source field is frozen from the
initial packet density on the same surface?

This control keeps the same surface as the retained temporal Wilson note:

- open 3D Wilson lattice
- centered placement family
- side `20`
- separations `d = 4, 6, 8, 10, 12`
- `MASS = 0.3`
- `WILSON_R = 1.0`
- `G = 5`
- `mu2 = 0.001`
- `DT = 0.08`
- `SIGMA = 1.0`
- trace lengths `15`, `25`, `35`
- windows:
  - `w2_10 = [2, 11)`
  - `w3_11 = [3, 12)`
  - `w6_14 = [6, 15)`
  - `w10_18 = [10, 19)`
  - `w14_22 = [14, 23)`
  - `w18_26 = [18, 27)`
  - `w26_34 = [26, 35)`

## Retained Comparisons

The script compares three pairings on the same retained windows:

- `SHARED - SELF_ONLY`
- `SHARED - FROZEN_SOURCE`
- `SELF_ONLY - FROZEN_SOURCE`

The key control question is whether `SHARED` continues to separate cleanly from
`FROZEN_SOURCE` on the early/mid windows.

## Result

### `SHARED - SELF_ONLY`

The original mutual-channel subtraction remains strong on the retained
early/mid windows:

- `w2_10`: `5/5` attractive, `5/5` clean, `|a_mut| ~ d^-1.965`, `R^2 = 0.9999`
- `w3_11`: `5/5` attractive, `5/5` clean, `|a_mut| ~ d^-1.957`, `R^2 = 0.9999`
- `w6_14`: `5/5` attractive, `5/5` clean, `|a_mut| ~ d^-1.936`, `R^2 = 0.9997`
- `w10_18`: `5/5` attractive, `5/5` clean, `|a_mut| ~ d^-1.997`, `R^2 = 0.9996`

That part of the lane is unchanged.

### `SHARED - FROZEN_SOURCE`

The frozen-source control does **not** reproduce a clean retained law.

On the same windows:

- `w2_10`: `3/5` attractive, `0/5` clean, `|a_mut| ~ d^-2.903`, `R^2 = 0.9698`
- `w3_11`: `3/5` attractive, `0/5` clean, `|a_mut| ~ d^-2.755`, `R^2 = 0.9736`
- `w6_14`: `3/5` attractive, `0/5` clean, `|a_mut| ~ d^-2.620`, `R^2 = 0.9755`
- `w10_18`: `3/5` attractive, `1/5` clean, `|a_mut| ~ d^-2.779`, `R^2 = 0.9812`
- `w14_22`: `2/5` attractive, `0/5` clean, fit not retained
- `w18_26`: `2/5` attractive, `0/5` clean, fit not retained
- `w26_34`: `3/5` attractive, `0/5` clean, `|a_mut| ~ d^-0.934`, `R^2 = 0.9833`

So the frozen-source baseline does not stay clean on the retained surface,
and it does not preserve the early/mid-window law as a mainline-quality result.

### `SELF_ONLY - FROZEN_SOURCE`

This pair does not produce a retained attractive law on the early windows:

- `w2_10`: `0/5` attractive
- `w3_11`: `0/5` attractive
- `w6_14`: `0/5` attractive

That is useful as a negative control, but it is not strong enough to promote
on its own.

## Exact Boundary

The bounded honest read is:

> The shared-vs-self-only Wilson signal remains a strong early/mid-window
> mutual-channel attraction on the audited open surface, but a frozen-source
> control does not produce a clean competing law on the same surface.

What this means for promotion:

- retain the `SHARED - SELF_ONLY` Wilson result as a bounded side-lane
- retain the frozen-source run only as a control note
- do **not** promote this control as evidence of full Newton closure

## Retain / Hold

Retain:

- the original Wilson side-lane mutual-channel result as a bounded early/mid
  window statement
- the frozen-source control as a bounded negative control

Hold:

- full Newton closure
- both-masses closure
- action-reaction closure
- any claim that the frozen baseline alone explains the mutual-channel signal

## Implication

This control narrows the Wilson blocker, but it does not remove it:

- `SHARED` is still the only mode that gives the strong clean near-`1/r^2`
  result across the audited early/mid windows
- `FROZEN_SOURCE` weakens, loses cleanliness, and eventually loses the retained
  law
- therefore the Wilson lane is still a bounded side-lane result, not a
  promotion to repo-wide Newton closure

