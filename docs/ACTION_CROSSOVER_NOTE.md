# Action Crossover: Spent-delay → Valley-linear with Regularity

**Date:** 2026-04-04
**Status:** exploratory regularity-crossover memo; dedicated sweep harness not yet frozen

## Reported finding

The current branch-side result reports that the better-performing action
switches from spent-delay to valley-linear as graph geometry becomes more
regular:

| Regularity | Valley-linear | Spent-delay | Winner |
|-----------|--------------|-------------|--------|
| 0.0 (random) | 44% TOWARD | **67%** | Spent-delay |
| 0.2 | 56% | **67%** | Spent-delay |
| 0.4 | **67%** | 42% | Valley-linear |
| 0.6 | **61%** | 42% | Valley-linear |
| 0.8 | 61% | 61% | Tied |

Crossover is reported near regularity `≈ 0.3 - 0.4`.

## Bounded interpretation

- **Spent-delay** S = dl - sqrt(dl^2 - L^2) is the better action on
  random DAGs because the sqrt(f) response handles the varied path
  lengths of irregular geometry.

- **Valley-linear** S = L(1-f) is the better action on regular geometry
  because the linear response gives coherent phase accumulation when
  paths have uniform structure.

- The **lattice** is the maximally regular limit in the current exploratory
  story, where valley-linear performs better on the retained same-family
  action comparison.

## Why this is interesting

If this crossover survives a dedicated frozen replay, it would support a more
unified interpretation of the current split:

- Spent-delay = lattice-scale / UV effective action
- Valley-linear = continuum-scale / IR effective action

That is still a **hypothesis**, not a retained theorem.

At the moment, the review-safe read is only:

- the reported crossover is scientifically interesting
- it is compatible with a one-mechanism / scale-dependent-action story
- it does not yet prove that story

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

Until that exists, this should be read as a bounded branch memo rather than a
promoted unification result.
