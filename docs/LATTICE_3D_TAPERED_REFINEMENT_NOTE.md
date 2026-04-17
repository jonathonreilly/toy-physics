# 3D Tapered Refinement Note

**Date:** 2026-04-04  
**Status:** retained bounded negative on a new 3D topology branch

## Purpose

This note freezes the y-tapered 3D refinement branch as a separate topology
test. It is **not** a continuation of the retained dense 3D card.

The question is narrow:

- can a y-only tapered 3D ordered lattice preserve Born, `k=0`, MI,
  decoherence, gravity hierarchy, and distance behavior under refinement from
  `h = 1.0` to `h = 0.5`?

## Fixed family and harness

- graph family: 3D ordered lattice with y-only taper
- taper: dense near center, sparse toward the edges
- z connectivity: uniform
- action: original spent-delay
- field strength: `5e-5`
- geometry: `L = 12`, `W = 6`
- spacings tested: `h = 1.0`, `h = 0.5`
- barrier card: same-family upper/lower slit partition on the barrier layer
- gravity readout: canonical hierarchy using centroid, `P_near`, and side bias

Primary artifact chain:

- [`scripts/lattice_3d_tapered_refinement.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_3d_tapered_refinement.py)
- [`logs/2026-04-04-lattice-3d-tapered-refinement.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-lattice-3d-tapered-refinement.txt)

## Retained card

| property | `h = 1.0` | `h = 0.5` | read |
|---|---:|---:|---|
| Born | `5.42e-16` | `1.91e-15` | machine-clean |
| `k=0` | `0.000000` | `0.000000` | exact on this harness |
| MI | `0.0789` | `0.6714` | strong improvement with refinement |
| `d_TV` | `0.2612` | `0.8668` | strong improvement with refinement |
| decoherence | `18.2%` | `49.9%` | strong improvement with refinement |
| gravity centroid | `-0.024838` | `-0.005891` | away |
| `P_near` | `-0.001740` | `-0.001281` | away |
| side bias | `-0.474054` | `-0.001667` | away |
| distance law | insufficient positive support | insufficient positive support | no retained positive fit |

## Gravity hierarchy

On both tested spacings, all three gravity observables remain negative:

- centroid drift is away
- `P_near` is away
- side bias is away

So this branch does **not** recover hierarchy-clean attraction.

## What is retained

- the tapered branch is a real new topology branch
- Born survives at machine precision
- `k=0` survives exactly on the same harness
- MI, `d_TV`, and decoherence all improve strongly at `h = 0.5`
- the branch is useful as a negative control for refinement under topology change

## What is not retained

- not a rescue of the dense 3D branch
- not hierarchy-clean attraction
- not a positive distance-law branch
- not a promoted refinement theorem

## Interpretation

The main value of this branch is that it separates topology change from the
current dense card:

- the dense 3D spent-delay branch remains the canonical ordered-lattice 3D
  result
- the tapered branch shows that y-only tapering alone does not restore
  attractive gravity under refinement

That makes this a clean negative branch, not a promotion.
