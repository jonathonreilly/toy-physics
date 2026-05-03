# EW Current Matching Rule Open Gate Note

**Date:** 2026-05-03
**Type:** open_gate
**Claim scope:** the package-level electroweak color-projection coefficient
has one retained exact ingredient, the group-theory channel ratio
`(N_c^2 - 1) / N_c^2 = 8/9` at `N_c = 3`, but the separate physical
matching rule that selects the connected color trace as the electroweak
readout is not closed by that arithmetic. Until a standalone theorem derives
that readout selection or the disconnected-current coefficient, downstream
claims using the exact `9/8` correction remain matching-rule conditioned.
**Status authority:** independent audit lane only. This source note is a
citeable open gate, not a retained theorem and not a verdict.

## Cited Authority

- [EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md](EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md)
  derives the exact representation-theoretic ratio
  `(N_c^2 - 1) / N_c^2` and states the separate matching-rule premise.

## Boundary

The exact Fierz-channel theorem supplies the channel-count arithmetic. It does
not by itself prove that the physical electroweak vacuum polarization reads
only the connected color trace after CMT factorization.

The older `RCONN_DERIVED_NOTE.md` and
`EW_CURRENT_MATCHING_OZI_SUPPRESSION_THEOREM_NOTE_2026-04-27.md` provide
bounded context for the same route, but they do not close the exact
coefficient. They are plain-text context here rather than dependencies of this
open gate.

## What Remains Open

A retained-grade closure would need at least one of:

- a framework-native theorem deriving the connected-trace electroweak readout
  from the lattice current construction;
- an exact derivation of the disconnected-current coefficient needed for the
  package-level `9/8` factor;
- a bounded-theorem restatement that keeps the electroweak normalization lane
  explicitly conditional on the unmatched coefficient.

Until one of those exists and passes audit, this open gate is the citeable
object that should block downstream retained propagation for claims that use
the exact electroweak `9/8` matching rule.
