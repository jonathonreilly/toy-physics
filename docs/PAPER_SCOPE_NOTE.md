# Paper Scope Note

**Date:** 2026-04-04  
**Status:** public scope note for the current action-law fork

## Recommended paper scope

The cleanest paper-shaped result in the current repo is not "gravity solved."
It is:

- a bounded same-family action-law comparison on a fixed ordered lattice
- with the geometry, kernel, and detector readout held fixed
- and only the action law changed

In practice, that means the current valley-linear lane should be written as:

- spent-delay `S = dl - sqrt(dl^2 - L^2)` versus
- valley-linear `S = L(1-f)`

on the retained 3D ordered-lattice `1/L^2` family.

That is a real scientific result. It is also much narrower than the branch
headlines that can arise in commit text or chat.

## Safe claim shape

The strongest safe claim is:

- on the retained fixed family, valley-linear preserves Born and `k=0`
- valley-linear improves the tested mass-law exponent relative to spent-delay
- valley-linear also changes the retained distance-tail behavior on that family
- the result is bounded to the retained family and the retained window

This is a same-family action-fork comparison, not a universal gravity theorem.

## What the paper should not claim

Do **not** frame the current result as:

- "Newtonian gravity is established"
- "the action follows from the axioms"
- "the continuum bridge is closed"
- "the result is universal across graph families"
- "the valley-linear action replaces the flagship mirror lane"
- "the 3D ordered-lattice family proves the full physical law"

Those claims outrun the retained artifact chain.

## Likely reviewer objections

Expect the following objections immediately:

1. The action choice looks ad hoc.
2. The result may be family-specific to the ordered lattice.
3. The code path can drift away from the claim surface unless the log / note
   chain is frozen with the script.
4. The same-family comparison is strong, but it does not by itself derive a
   fundamental law.
5. Companion checks at a different `h` are useful, but they are not the same
   thing as a single fixed-resolution theorem card.

The right answer is not to overpromise. It is to keep the comparison narrow,
frozen, and easy to replay.

## Closest neighboring frameworks to cite later

The paper is closest to these conversations:

- discrete propagator / lattice regularization / finite-volume scaling
- quantum measure / Sorkin-style interference diagnostics
- open quantum systems / collision models, if the decoherence lane is discussed
- causal-set / sequential-growth ideas, if the future dynamics lane is discussed
- Regge / CDT-style continuum-limit language, but only for the asymptotic
  bridge sections

The important point is not equivalence. It is that these are the nearest
technical neighborhoods a reviewer will expect to see acknowledged.

## Exact discriminator tests

The paper should anchor itself to these tests:

1. Same-harness action comparison
   - fixed family
   - fixed geometry
   - fixed kernel
   - fixed detector
   - only the action law changes

2. Refinement replay
   - same family
   - same width and fit window
   - compare `h = 0.5` to `h = 0.25` only as a refinement check

3. Robustness appendix
   - width sweep
   - connectivity sweep
   - length sweep
   - these should be treated as robustness, not the headline claim

4. Negative control
   - keep the linear-hill action `S = Lf` as the "no gravity" control
   - this helps show that the phase valley matters

5. Branch discipline
   - if the action law changes again, treat it as a new branch
   - do not inherit the current action-fork claim automatically

## Recommended paper wording

Use language like:

- "bounded same-family comparison"
- "action-law fork"
- "retained ordered-lattice family"
- "same-harness result"
- "review-safe comparison"

Avoid language like:

- "final"
- "universal"
- "derived"
- "solved"
- "established"

## Relation to the rest of the repo

This paper scope should live alongside, not instead of:

- the flagship mirror story
- the structured chokepoint bridge
- the continuum / asymptotic notes
- the reproduction harnesses

That keeps the repo honest about what has been retained and what is still
frontier work.
