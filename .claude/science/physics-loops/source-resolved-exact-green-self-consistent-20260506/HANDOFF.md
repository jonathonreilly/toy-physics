# Handoff

## Summary

The prompt asked to repair an `audited_numerical_match` blocker for
`docs/SOURCE_RESOLVED_EXACT_GREEN_SELF_CONSISTENT_NOTE.md`. Current source is
already past that state.

The live runner has a real assertion wrapper:

- zero-source exactness
- calibrated gain boundary
- `TOWARD` sign in every source row
- instantaneous and self-consistent source-strength exponents
- frozen table reproduction

The note declares the calibrated gain as an input and keeps the amplitude
ratio out of standalone physical-observable status. The audit ledger records
the current note as `audited_clean` with effective status `retained_bounded`.
The live runner was rerun in this loop and returned exit code 0 with
`PASSED: 6/6`.

## Verification Commands

```bash
python3 scripts/source_resolved_exact_green_self_consistent.py
sed -n '147280,147430p' docs/audit/data/audit_ledger.json
```

Expected runner terminal markers:

```text
PASSED: 6/6
SOURCE_RESOLVED_EXACT_GREEN_SELF_CONSISTENT_ASSERTIONS=TRUE
CALIBRATED_GAIN_IS_INPUT=TRUE
SOURCE_RESOLVED_GREEN_FULL_SELF_CONSISTENT_FIELD_THEORY=FALSE
```

## Files

This loop intentionally edits only branch-local loop state:

- `.claude/science/physics-loops/source-resolved-exact-green-self-consistent-20260506/`

Source note, runner, output, and ledger were left unchanged to preserve the
current clean audit surface.
