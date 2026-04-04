# Action / Architecture Matrix Note

**Date:** 2026-04-04  
**Status:** bounded reviewer-facing synthesis, not a unification theorem

## Purpose

This note is the cleanest current map of the architecture/action split on
`main`.

The project now has strong retained evidence for more than one lane, but the
evidence is still architecture-dependent. That is a feature of the current
state, not a bug to be hidden.

The right reading is:

- ordered lattices and irregular graphs reward different effective actions
- some results are robust on a fixed family
- no single claim should be promoted beyond its frozen artifact chain

## Matrix

| Lane | What it is good for | Retained artifact chain | What is still open |
|---|---|---|---|
| `Spent-delay` on irregular / mirror / DAG-like geometry | Best current read on irregular continuation structure; the action remains the stronger comparator on more random geometry and still edges the mirror transfer replay | [ACTION_CROSSOVER_NOTE.md](/Users/jonreilly/Projects/Physics/docs/ACTION_CROSSOVER_NOTE.md), [VALLEY_LINEAR_MIRROR_TRANSFER_NOTE.md](/Users/jonreilly/Projects/Physics/docs/VALLEY_LINEAR_MIRROR_TRANSFER_NOTE.md), [REPRODUCTION_AUDIT_NOTE.md](/Users/jonreilly/Projects/Physics/docs/REPRODUCTION_AUDIT_NOTE.md), [VALLEY_LINEAR_REPRO_NOTE.md](/Users/jonreilly/Projects/Physics/docs/VALLEY_LINEAR_REPRO_NOTE.md) | Does not dominate on regular ordered-lattice slices; does not by itself resolve the lattice-side Newtonian-like card |
| `Valley-linear` on ordered 3D lattice | Best retained action fork on the regular ordered-lattice family; improves the tested mass-law exponent and preserves the frozen same-family replay | [VALLEY_LINEAR_ACTION_NOTE.md](/Users/jonreilly/Projects/Physics/docs/VALLEY_LINEAR_ACTION_NOTE.md), [VALLEY_LINEAR_ROBUSTNESS_NOTE.md](/Users/jonreilly/Projects/Physics/docs/VALLEY_LINEAR_ROBUSTNESS_NOTE.md), [VALLEY_LINEAR_REPRO_NOTE.md](/Users/jonreilly/Projects/Physics/docs/VALLEY_LINEAR_REPRO_NOTE.md) | Gravity magnitude is still much smaller on the retained same-family slice; the action fork is real, but not a flagship replacement |
| `Regularity crossover` between the two actions | Shows a branch-specific switch as geometry becomes more regular; this is the strongest hint that the split is scale/geometry dependent | [ACTION_CROSSOVER_NOTE.md](/Users/jonreilly/Projects/Physics/docs/ACTION_CROSSOVER_NOTE.md), [VALLEY_LINEAR_ACTION_NOTE.md](/Users/jonreilly/Projects/Physics/docs/VALLEY_LINEAR_ACTION_NOTE.md) | It is still a crossover replay, not a derivation of a UV/IR bridge |
| `Gate B` evolving-network prototype | Gives a real generated-geometry signal and a cleaner imposed-control comparator than before | [EVOLVING_NETWORK_PROTOTYPE_V2_NOTE.md](/Users/jonreilly/Projects/Physics/docs/EVOLVING_NETWORK_PROTOTYPE_V2_NOTE.md), [EVOLVING_NETWORK_PROTOTYPE_V3_NOTE.md](/Users/jonreilly/Projects/Physics/docs/EVOLVING_NETWORK_PROTOTYPE_V3_NOTE.md), [REVIEW_HARDENING_BACKLOG.md](/Users/jonreilly/Projects/Physics/docs/REVIEW_HARDENING_BACKLOG.md) | Gate B is not closed; v3 improves the control discipline but remains a bounded negative / inconclusive audit |
| Reproduction / canonical harness layer | Lets a skeptical reader distinguish retained harnesses from exploratory drivers and replay the bounded frontier safely | [REPRODUCTION_AUDIT_NOTE.md](/Users/jonreilly/Projects/Physics/docs/REPRODUCTION_AUDIT_NOTE.md), [CANONICAL_HARNESS_INDEX.md](/Users/jonreilly/Projects/Physics/docs/CANONICAL_HARNESS_INDEX.md) | This layer improves trust, but it does not certify a universal claim by itself |

## What the split means

The current evidence does not support collapsing all lanes into one universal
story.

The safest synthesis is:

- irregular geometry and regular geometry appear to prefer different effective
  actions
- the regular ordered-lattice lane now has the strongest retained action-law
  replay
- the irregular / mirror / DAG lane still carries the best “random geometry”
  interpretation
- the crossover note is real, but it is still a branch-specific observation

So the project should be described as a set of retained, architecture-aware
results rather than a single settled theorem.

## What is retained

- The valley-linear action is a real bounded fork on the ordered 3D lattice.
- The spent-delay action remains the stronger comparator on irregular geometry.
- The mirror transfer replay is mixed in the expected way:
  - valley-linear improves the random-DAG slice
  - spent-delay still edges the mirror family
- The regularity crossover replay is frozen and review-safe as a branch result.
- The Gate B prototype remains open and bounded, with v3 improving the imposed
  control without closing the detector-signal gap.
- The reproduction harness now helps a skeptical reader separate retained
  harnesses from exploratory drivers.

## What is not retained

- A universal unification of the two actions.
- A theorem that the valley-linear action replaces the spent-delay lane.
- A theorem that the spent-delay action is the continuum limit of the
  valley-linear lane.
- A solved Gate B dynamics story.

## Practical reading

If you are trying to enter the project quickly:

1. Start with the reproduction harness and canonical harness index.
2. Read the valley-linear action note and robustness note as a bounded ordered
   lattice fork.
3. Read the mirror transfer and action crossover notes as geometry-dependent
   diagnostics, not theorems.
4. Read the Gate B v2/v3 notes as the current open dynamics gap and control
   audit.

The point is to keep the architecture split explicit while preserving the
strongest retained evidence from each lane.
