# Lattice Synthesis Guard Note

**Date:** 2026-04-03  
**Status:** synthesis unchanged pending canonical mass/purity artifact chains

This note records the integration guard for the ordered-lattice branch after the
weak-field reopening.

## Canonical lattice state

The retained lattice story currently has three distinct pieces:

- a standard-strength negative decision on the dense ordered-lattice symmetry
  window
- a narrow weak-field retained pocket on the same ordered-lattice family
- a separate lattice complementarity story showing a tradeoff between
  decoherence / which-slit structure and distance-law quality

The weak-field reopening is real, but it is still narrow and bounded. The
project-level synthesis should not be upgraded beyond that without a canonical
artifact chain for the later mass-scaling and purity-scaling claims.

## Why synthesis should stay unchanged

The repo currently retains the following lattice claims in canonical notes:

- the standard-strength dense ordered-lattice symmetry decision is negative
- the weak-field pocket is narrow and does not yet imply a blanket one-family
  theorem
- the lattice complementarity result is a same-family, two-harness bridge, not
  a single fixed-geometry unification card

The newer `F∝M^0.38` and purity-exponent `-0.25` claims exist in commit-message
history, but they are not yet frozen in a dedicated script/log/note chain. Until
those artifacts are retained on `main`, they should not be used to widen the
project synthesis.

## Safe synthesis wording

The safest current project-level wording is:

- exact mirror remains the flagship coexistence lane
- ordered lattice is a retained secondary branch for distance-law work
- ordered lattice has a narrow weak-field pocket, but not yet a promoted
  one-family theorem
- the later mass-scaling and purity-scaling claims require canonical freeze
  before they can affect the synthesis note

## Promotion rule

Only update `docs/UNIFIED_PROGRAM_NOTE.md` if all of the following are true:

- the new mass-scaling chain is frozen in a dedicated script, log, and note
- the new purity-scaling chain is frozen in a dedicated script, log, and note
- the promoted language stays narrow about the weak-field pocket and does not
  claim a full one-family lattice theorem unless the evidence truly supports it

Until then, keep the synthesis unchanged.
