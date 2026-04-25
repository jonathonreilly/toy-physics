# Koide delta identity endpoint-gluing law candidate

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_identity_endpoint_gluing_law_candidate.py`  
**Status:** candidate physical law; conditional closure, not retained closure

## Candidate Law

The selected Brannen open line is physically the full APS boundary segment.
There is no additional endpoint complement.  In the relative eta/phase group,
gluing that open segment to the closed APS boundary is the identity morphism:

```text
eta_closed = delta_open + tau
tau(identity endpoint gluing) = 0.
```

## Executable Theorem

The runner verifies the value-independent theorem:

```text
eta_closed = delta_open + tau
tau = 0
therefore delta_open = eta_closed.
```

Then the independent retained APS fixed-point computation supplies:

```text
eta_APS = 2/9
therefore delta_open = 2/9.
```

## Why This Is Not Just Numerology

The gluing law does not select `2/9`.  It transfers any closed APS value to
the open selected-line phase.  The value `2/9` enters only from the independent
Z3 APS fixed-point computation.

## Nature-Grade Boundary

The hard premise is:

```text
the selected Brannen line is the full APS boundary segment, not a subsegment
requiring a nontrivial endpoint transition.
```

If that premise is not derived, the law is still a renamed endpoint primitive.

## Falsifier

A nonzero endpoint transition preserves the same closed APS value while
changing the open delta:

```text
eta_APS = 2/9
tau = 1/9
delta_open = 1/9
delta_open + tau = 2/9.
```

Thus retained APS support alone does not force the Brannen delta.

## Reviewer Objections Answered

- **"You imported delta equals 2/9."**  The runner first proves
  `delta_open = eta_closed` with a symbolic `eta_closed`; the numerical value
  enters later from APS.
- **"Closed eta and open Brannen phase can differ by a boundary term."**
  Correct.  The candidate law is exactly the identity-gluing theorem that
  would remove that term.
- **"Selected-line matching is not a physical endpoint law."**  Correct.
  The remaining task is to derive that the selected line is the full APS
  boundary segment.

## Verification

Run:

```bash
python3 scripts/frontier_koide_delta_identity_endpoint_gluing_law_candidate.py
```

Expected closeout:

```text
KOIDE_DELTA_IDENTITY_ENDPOINT_GLUING_LAW_CANDIDATE=TRUE
KOIDE_DELTA_CONDITIONAL_CLOSURE_UNDER_IDENTITY_GLUING=TRUE
KOIDE_DELTA_RETAINED_CLOSURE_CLAIM=FALSE
DELTA_LAW_REVIEW_BARRIER=derive_selected_line_is_full_APS_boundary_segment
DELTA_LAW_FALSIFIER=nonzero_endpoint_transition_preserves_closed_APS
```
