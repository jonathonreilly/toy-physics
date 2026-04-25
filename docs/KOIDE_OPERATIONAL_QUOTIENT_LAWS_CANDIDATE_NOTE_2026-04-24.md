# Koide operational quotient laws candidate

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_operational_quotient_laws_candidate.py`  
**Status:** unified candidate law packet; conditional closure, not retained closure

## Candidate Physical Principle

A retained source or boundary endpoint may depend only on quotient-internal
operational structure.  Embedding data removed by the physical quotient is not
a source label and not an endpoint complement.

This gives two concrete laws:

```text
Q law:
  source states are natural on the Morita-normalized quotient-center source
  object.  Its two components are unlabeled, so automorphism naturality forces
  equal weights.

Delta law:
  endpoint phases are computed on the quotient APS boundary segment.  If the
  selected Brannen line is that full segment, gluing is the identity unit and
  tau = 0.
```

## Executable Consequences

The runner verifies:

```text
swap(w, 1-w) = (w, 1-w) -> w = 1/2
K_TL = 0
Q = 2/3
```

and:

```text
eta_closed = delta_open + tau
tau = 0 -> delta_open = eta_closed
eta_APS = 2/9 -> delta_open = 2/9.
```

## Why This Is Not Just Target Import

- The Q side derives equal weights from automorphism naturality on a two-point
  quotient source object.
- The delta side proves a symbolic transfer law for arbitrary `eta_closed`.
  The value `2/9` enters only through the independent APS fixed-point
  computation.
- The runner includes explicit countermodels showing how the packet fails if
  the quotient principle is not physically retained.

## Falsifiers

The law packet is falsified as retained closure by either of the following:

```text
C3 orbit type remains source-visible:
  {0} versus {1,2} may be weighted as 1:2, giving Q = 1 and K_TL = 3/8.

An endpoint complement remains source-visible:
  eta_APS = 2/9, tau = 1/9, delta_open = 1/9.
```

## Reviewer Objections Answered

- **"This is just the missing primitive renamed."**  It would be if
  operational quotient noncontextuality is not independently retained.  The
  packet is therefore marked as conditional, not closure.
- **"The original C3 carrier distinguishes the sectors."**  Correct.  The Q
  law applies only after proving that the physical source object is the
  Morita-normalized quotient source, not the embedded carrier.
- **"Closed APS eta and open Brannen phase may differ by a boundary term."**
  Correct.  The delta law applies only after proving that the selected line is
  the full quotient APS boundary segment.

## Remaining Positive Task

Derive or retain operational quotient noncontextuality for:

```text
source labels:       C3 orbit type is not source-visible after reduction;
boundary endpoints:  endpoint complements are not source-visible after APS
                     boundary quotienting.
```

## Verification

Run:

```bash
python3 scripts/frontier_koide_operational_quotient_laws_candidate.py
```

Expected closeout:

```text
KOIDE_OPERATIONAL_QUOTIENT_LAWS_CANDIDATE=TRUE
KOIDE_CONDITIONAL_Q_CLOSURE_UNDER_OPERATIONAL_QUOTIENT=TRUE
KOIDE_CONDITIONAL_DELTA_CLOSURE_UNDER_OPERATIONAL_QUOTIENT=TRUE
KOIDE_RETAINED_FULL_CLOSURE_CLAIM=FALSE
Q_REVIEW_BARRIER=derive_source_label_operational_quotient
DELTA_REVIEW_BARRIER=derive_endpoint_complement_operational_quotient
FALSIFIER=source_visible_labels_or_endpoint_complements
```
