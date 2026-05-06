# Assumptions And Imports

## Retained Inputs

- Existing Koide no-go notes and objection-review packet matched by the guard's
  `DOC_GLOBS`.
- Existing Koide no-go scripts matched by the guard's `SCRIPT_GLOBS`.
- Existing audit pipeline scripts under `docs/audit/scripts/`.

## New Assumptions

None.  The block does not add a physics axiom or a retained theorem.

## Import Boundary

The guard now imports executable behavior from each target no-go script by
running it with the current Python interpreter and inspecting stdout.  It does
not import those scripts' verdicts as proof of Koide closure.

## Nonzero Target Runner Boundary

One target no-go runner currently returns nonzero while emitting the expected
negative closeout and residual labels.  This block treats return code as
evidence metadata, not as the hygiene predicate, because the guard's audited
claim is about emitted labels and non-promotion, not about each target no-go
attempt proving internally clean.
