# Lattice Synthesis Guard Note

**Date:** 2026-04-03 (status line rephrased 2026-04-28 per audit-lane verdict)
**Status:** support / narrow synthesis guard note; NN refinement is a bounded bridge, not a continuum theorem and not a tier-ratifiable continuum claim.

This note records the integration guard for the ordered-lattice branch after the
weak-field reopening.

## Canonical lattice state

The retained lattice story currently has four distinct pieces:

- a standard-strength negative decision on the dense ordered-lattice symmetry
  window
- a narrow weak-field retained pocket on the same ordered-lattice family
- a canonical nearest-neighbor refinement branch that is Born-clean through
  `h = 0.25`, with a deterministic Born-safe extension through `h = 0.0625`
- a separate lattice complementarity story showing a tradeoff between
  decoherence / which-slit structure and distance-law quality

The weak-field reopening is real, but it is still narrow and bounded. The
project-level synthesis should not be upgraded beyond that without a canonical
artifact chain for the NN refinement / RG side as well.

## Why synthesis should stay unchanged

The repo currently retains the following lattice claims in canonical notes:

- the standard-strength dense ordered-lattice symmetry decision is negative
- the weak-field pocket is narrow, but it is now canonical and includes the
  retained mass-response and purity-scaling notes
- the lattice complementarity result is a same-family, two-harness bridge, not
  a single fixed-geometry unification card
- the NN refinement branch is Born-clean through `h = 0.25`, and the
  deterministic rescale path extends that refinement through `h = 0.0625`

The newer `F∝M^0.38` and purity-exponent `-0.25` claims are now frozen in
dedicated script/log/note chains, but they still support only the narrow
weak-field pocket rather than a blanket one-family theorem. The NN refinement
branch is similarly real but still bounded.

## Safe synthesis wording

The safest current project-level wording is:

- exact mirror remains the flagship coexistence lane
- ordered lattice is a retained secondary branch for distance-law work
- ordered lattice has a narrow weak-field pocket with retained mass-response and
  purity-scaling laws, but not yet a promoted one-family theorem
- the NN refinement branch is a promising Born-clean refinement path, not yet a
  finished continuum theorem
- the RG-style gravity question remains open and should not be promoted beyond
  the ambiguous narrow probe

## Promotion rule

`docs/UNIFIED_PROGRAM_NOTE.md` has now been updated narrowly enough to mention
the deterministic Born-safe continuation beyond `h = 0.25`.

Further promotion beyond that bounded bridge now requires all of the following:

- a canonical NN refinement / RG artifact chain that is review-safe and stays
  narrow about what is actually retained
- no mismatch between branch-history narrative claims and the artifact-backed
  notes on disk
- no blanket one-family lattice theorem language unless the evidence truly
  supports it

Until then, keep the synthesis conservative: the NN branch is a retained
refinement bridge, not a finished continuum theorem.

## Audit boundary (2026-04-28)

The earlier Status line read "NN refinement is a bounded bridge, not a
`proposed_promoted` continuum theorem". The audit-lane parser caught
the literal token even though the sentence asserts the opposite.

Audit verdict (`audited_failed`, leaf criticality):

> Issue: the source explicitly disclaims the promoted-continuum claim
> that caused it to enter the `proposed_promoted` queue, and it
> provides no independent runner or artifact chain for a project-level
> promotion. Why this blocks: an audit cannot ratify a promoted claim
> that the source itself says is not being made, especially when the
> cited synthesis note is effective `audited_failed` and the
> underlying lattice/NN branches remain bounded or conditional.

The note has been re-tiered to `support`.

## What this note does NOT claim

- A continuum theorem on the NN refinement branch.
- A project-level promotion of any lattice / NN claim.
- That the cited synthesis note is audit-clean (it is currently
  effective `audited_failed`).

## What would close this lane (Path A future work)

A continuum theorem would require auditing the cited synthesis note,
auditing the underlying lattice/NN branches, and registering an
independent runner / artifact chain for a project-level promotion.
