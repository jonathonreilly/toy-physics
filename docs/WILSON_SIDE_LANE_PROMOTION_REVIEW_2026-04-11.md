# Wilson Side-Lane Promotion Review

**Date:** 2026-04-11  
**Scope:** `TWO_BODY_ATTRACTION_RETAINED_NOTE_2026-04-11.md`, `TWO_BODY_ATTRACTION_ROBUSTNESS_NOTE_2026-04-11.md`, `TWO_BODY_ATTRACTION_TEMPORAL_ROBUSTNESS_NOTE_2026-04-11.md`, `frontier_two_body_attraction.py`, `frontier_two_body_attraction_robustness.py`, `frontier_two_body_attraction_temporal_robustness.py`

## Verdict

**Hold.** The Wilson mutual-attraction side lane is a strong bounded result, but it is **not yet safe for `main`** because the missing frozen/static-source control still leaves the causal interpretation underdetermined.

The audited family now supports:

- a robust open-Wilson mutual-channel attraction on one geometry class
- a side/placement robustness surface with `45/45` attractive, `45/45` clean
- a temporally bounded early/mid-early near-inverse-square law through `w10_18`

What it does **not** yet support:

- a promotion to repo-wide Newton closure
- a claim that the mutual channel is distinguished from a frozen or static-source control
- a claim that the temporal law survives once the source field is decoupled from the evolving packets

## Why It Is Held

The current Wilson family still compares `SHARED` against `SELF_ONLY` only. That is a useful subtraction, but it does not answer the remaining question:

> does the mutual-channel signal persist when the gravitational field is frozen or sourced statically from the initial density?

Without that control, the lane can still be read as a self-consistent Hartree-style effect on one open Wilson surface. That is bounded and interesting, but not enough to promote the side lane to `main`.

## Exact Next Control

Run a **frozen/static-source control** on the same audited Wilson surface:

- same open 3D Wilson lattice
- same `side=18,20,22` robustness surface
- same centered and offset placement families
- same separations `d=4,6,8,10,12`
- same `G=5`, `mu^2=0.001`, `MASS=0.3`, `WILSON_R=1.0`, `DT=0.08`
- same early-time windows used in the temporal note

Required comparison:

- `SHARED`
- `SELF_ONLY`
- `FROZEN_SOURCE` or equivalent static-field control

Promotion criteria after that control:

- attraction remains positive and clean versus the frozen/static baseline
- the near-inverse-square exponent remains close to `-2`
- the result still survives the side/placement robustness surface

## Retainable Now

Retain as bounded Wilson-side evidence only:

- the robustness note
- the temporal robustness note
- the open-Wilson mutual attraction result

Do not retain as `main` truth yet:

- full Newton closure
- both-masses closure
- action-reaction closure
- a causal claim that excludes frozen/static-source explanations

