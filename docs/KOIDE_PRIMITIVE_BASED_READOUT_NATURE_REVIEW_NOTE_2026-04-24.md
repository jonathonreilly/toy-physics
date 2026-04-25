# Koide primitive-based readout Nature review

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_primitive_based_readout_nature_review.py`  
**Status:** passes as new-law closure; fails as retained-only closure

## Review Question

Does the primitive-based readout theorem close the dimensionless Koide lane
without hidden target import, while preserving the boundary that the law is new
rather than retained-only?

## Verdict

The packet passes as a positive closure theorem under one explicit new physical
law:

```text
primitive_based_operational_boundary_readout
```

It does not pass as retained-only closure.  The existing no-go artifacts remain
part of the review packet.

## Why It Passes Under The New Law

- The Q theorem is finite-orbit descent: a descended source state is uniform on
  a quotient orbit.  The two-object case gives `w_plus = w_perp = 1/2`; then
  `K_TL = 0` and `Q = 2/3` are computed.
- The delta theorem is primitive based boundary readout:

```text
selected_channel = 1
spectator_channel = 0
c = 0
```

so `delta_open = eta_closed`.  The value `2/9` comes from the independent APS
fixed-point computation.

## Why It Does Not Pass As Retained-Only Closure

Without the new law, exact countermodels remain:

```text
source-visible quotient labels;
spectator boundary channels;
unbased endpoint lifts.
```

The recent no-go runners show these are not removed by retained
`Cl(3)/Z3`, Wilson, APS, relative-cobordism, or boundary-grammar data.

## Reviewer Decision

The review decision is now reduced to one physical question:

```text
Should charged-lepton source and boundary endpoint readouts be required to be
primitive and based functors on the operational quotient?
```

If yes, the dimensionless Koide lane closes.  If no, the no-go countermodels
remain.

## Verification

Run:

```bash
python3 scripts/frontier_koide_primitive_based_readout_nature_review.py
```

Expected closeout:

```text
KOIDE_PRIMITIVE_BASED_READOUT_NATURE_REVIEW=PASS
PRIMITIVE_BASED_READOUT_PACKET_PASSES_AS_NEW_LAW_CLOSURE=TRUE
PRIMITIVE_BASED_READOUT_PACKET_PASSES_AS_RETAINED_ONLY_CLOSURE=FALSE
NEW_PHYSICAL_LAW=primitive_based_operational_boundary_readout
REVIEWER_DECISION=accept_or_reject_primitive_based_readout_law
```
