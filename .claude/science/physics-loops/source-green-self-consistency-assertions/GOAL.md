# Goal

Resolve the missing-derivation prompt for
`source_resolved_exact_green_self_consistent_note`.

Target prompt:

- Source note: `docs/SOURCE_RESOLVED_EXACT_GREEN_SELF_CONSISTENT_NOTE.md`
- Runner: `scripts/source_resolved_exact_green_self_consistent.py`
- Audit status before repair: `audited_numerical_match`

Block objective:

- Add explicit PASS/FAIL assertions for the frozen numerical pocket.
- Assert zero-source exactness, TOWARD sign, source-strength exponent
  tolerances, and frozen table reproduction.
- Declare the calibrated gain as a frozen setup input, not as an independent
  physical amplitude prediction.
- Reset the active audit row to `unaudited` for independent re-audit.
