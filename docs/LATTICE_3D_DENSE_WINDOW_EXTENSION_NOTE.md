# 3D Dense Spent-Delay Window Extension Note

**Date:** 2026-04-04  
**Status:** bounded extension proposed_retained on the ordered 3D dense spent-delay family

## Purpose

This note freezes the narrow window-extension question for the retained 3D
dense spent-delay branch:

- can the hierarchy-clean attractive window extend to a larger tested `z`
  while staying inside the same action law?
- can slit-threshold / detector-window adjustments extend that window without
  losing meaningful MI / decoherence?

The answer on the canonical family is:

- **yes, but only boundedly**
- the retained attractive window extends cleanly to `z = 6`
- `z = 7` is signal-free / mixed
- wider slit thresholds do **not** extend the window further on this family

## Fixed family and harness

- graph family: ordered 3D dense lattice
- forward span: `max_d = 3` (`49` edges per node)
- action: original spent-delay
- field strength: `5e-5`
- geometry: `L = 12`, `W = 6`, `h = 1.0`
- canonical slit threshold: `0.5`
- detector-window scan: `half-width = 0.5, 1.0, 1.5, 2.0`
- slit-threshold spot checks: `0.5, 1.5, 2.5`

Primary artifact chain:

- [`scripts/lattice_3d_dense_window_extension.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_3d_dense_window_extension.py)
- [`logs/2026-04-04-lattice-3d-dense-window-extension.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-lattice-3d-dense-window-extension.txt)

## Canonical sweep

| z | centroid | P_near | bias | Born | MI | decoh | dTV | read |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| 2 | `+0.003101` | `+0.001469` | `+0.107097` | `5.20e-16` | `0.134` | `0.140` | `0.368` | attractive |
| 3 | `+0.001941` | `+0.000374` | `+0.176381` | `6.17e-16` | `0.135` | `0.140` | `0.370` | attractive |
| 4 | `+0.001157` | `+0.000626` | `+0.113676` | `4.48e-16` | `0.135` | `0.139` | `0.371` | attractive |
| 5 | `+0.000693` | `+0.000715` | `+0.048601` | `5.17e-16` | `0.136` | `0.138` | `0.372` | attractive |
| 6 | `+0.000572` | `+0.000536` | `+0.000112` | `6.02e-16` | `0.137` | `0.138` | `0.373` | attractive |
| 7 | `+0.000000` | `+0.000000` | `nan` | `7.39e-16` | `0.141` | `0.135` | `0.379` | mixed |

## Detector-window sensitivity at z=6

On the canonical geometry, widening the detector-side window does not change
the sign of the hierarchy observables at `z = 6`:

| half-width | centroid | P_near | bias | read |
|---|---:|---:|---:|---|
| 0.5 | `+0.000572` | `+0.000173` | `+0.000112` | attractive |
| 1.0 | `+0.000572` | `+0.000536` | `+0.000112` | attractive |
| 1.5 | `+0.000572` | `+0.000536` | `+0.000112` | attractive |
| 2.0 | `+0.000572` | `+0.000830` | `+0.000112` | attractive |

The local mass-side gain grows, but the sign stays stable.

## Slit-threshold spot checks at z=6

Wider slit thresholds do not extend the window further:

| thresh | centroid | P_near | bias | read |
|---|---:|---:|---:|---|
| 0.5 | `+0.000572` | `+0.000536` | `+0.000112` | attractive |
| 1.5 | `-0.000082` | `+0.000531` | `-0.026969` | mixed |
| 2.5 | `+0.000097` | `+0.000453` | `-0.015331` | mixed |

So the canonical threshold `0.5` remains the best retained geometry.

## Retained read

- the 3D dense spent-delay branch is still the same-family ordered-lattice
  branch
- the hierarchy-clean attractive window extends cleanly to `z = 6`
- `z = 7` is the boundary: signal-free / mixed
- MI and decoherence remain meaningful on the retained window
- this is a bounded extension, not an all-distances theorem

## Not retained

- not a change of action law
- not a 4D result
- not an NN result
- not a promoted asymptotic theorem for all `z`
- not a claim that wider slit thresholds improve the retained window

## Program read

This extension strengthens the ordered-lattice branch without changing the
project ranking:

- **mirror remains the flagship**
- **ordered lattice remains the secondary branch**
- **NN refinement remains the continuum-side bridge**

## Next question

The only remaining meaningful question for this branch is whether another
same-family geometry change can push the attractive window beyond `z = 6`
without losing the hierarchy-clean sign or collapsing MI / decoherence.

