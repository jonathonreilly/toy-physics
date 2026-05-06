# Route Portfolio

## Selected Route: Executed Stdout Verification

Replace script source substring checks with subprocess execution and stdout
parsing:

- `...CLOSES...=FALSE` must appear as an emitted stdout line.
- `RESIDUAL...=` must appear as an emitted stdout line.
- forbidden positive closure promotions are checked against emitted output.

Reason selected: it directly closes the auditor's objection and is stronger
than AST print-surface parsing because comments and dead strings are excluded.

## Alternative: AST Print-Path Parsing

Rejected for this block.  The prompt allowed AST/print-path parsing, but direct
execution was available and produced concrete output evidence.

## Alternative: Note Rescope Only

Rejected.  Narrowing the note to a shallow scan would not close the requested
missing-derivation prompt.
