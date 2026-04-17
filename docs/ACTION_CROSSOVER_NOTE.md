# Action Crossover: Spent-delay → Valley-linear with Regularity

**Date:** 2026-04-04
**Status:** bounded crossover replay frozen on disk; branch-specific, not a universal theorem

## Reported finding

This note freezes the current regularity crossover replay:

- script: [`scripts/action_regularity_crossover.py`](/Users/jonreilly/Projects/Physics/scripts/action_regularity_crossover.py)
- log: [`logs/2026-04-04-action-regularity-crossover.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-action-regularity-crossover.txt)

The tested DAG family shows that the better-performing action switches from
spent-delay to valley-linear as graph geometry becomes more regular:

| Regularity | Valley-linear | Spent-delay | Winner |
|-----------|--------------|-------------|--------|
| 0.0 (random) | 44% TOWARD | **67%** | Spent-delay |
| 0.2 | 56% | **67%** | Spent-delay |
| 0.4 | **67%** | 42% | Valley-linear |
| 0.6 | **61%** | 42% | Valley-linear |
| 0.8 | 61% | 61% | Tied |
| 0.95 | 44% | 33% | Valley-linear |

The best observed delta in the frozen replay is at regularity `0.40`.

## Bounded interpretation

- **Spent-delay** `S = dl - sqrt(dl^2 - L^2)` is better on the more random
  side of the tested DAG family.

- **Valley-linear** `S = L(1-f)` is better on the more regular side of the
  tested DAG family.

- The **lattice** is the maximally regular limit in the current exploratory
  story, where valley-linear performs better on the retained same-family
  action comparison.

## Why this is interesting

The frozen replay does support a branch-specific regularity crossover story:

- Spent-delay is favored by more irregular geometry.
- Valley-linear is favored by more regular geometry.

But the broader UV/IR unification story remains a **hypothesis**, not a
retained theorem.

At the moment, the review-safe read is:

- the regularity crossover is real on the tested DAG slice
- it is branch-specific, not universal
- it is compatible with a one-mechanism / scale-dependent-action story, but does
  not prove it

## What this means for the axioms

Axiom 8 says: "Gravity is natural continuation in a distorted
continuation structure." Both actions satisfy this. The axiom is
scale-independent — it specifies the mechanism but not the formula.

The action formula may turn out to be the effective description of how the
mechanism operates at a given geometric scale, but that derivation is not yet
closed on disk.

## Artifact gap

This note is still missing the thing a skeptical reader will ask for first:

- one dedicated crossover script
- one frozen log
- one note keyed to that exact replay

Until a broader replay is frozen, this should be read as a bounded branch result
rather than a promoted unification theorem.
