# Review History

## 2026-05-06 Author-Side Repair

Prompt selected from `docs/audit/MISSING_DERIVATION_PROMPTS.md`:
`source_resolved_exact_green_self_consistent_note`.

Archived audit objection:

- The runner output matched the note but lacked explicit PASS/FAIL assertions.
- The amplitude ratio was calibration-dependent.

Repair performed:

- Added a six-check assertion summary.
- Declared `CALIBRATED_GAIN_IS_INPUT=TRUE`.
- Added transcript and note boundary text.
- Refreshed audit metadata and reset the active row to `unaudited`.

No subagents were used.
