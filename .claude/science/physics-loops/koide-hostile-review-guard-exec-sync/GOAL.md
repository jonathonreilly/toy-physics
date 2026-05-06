# Goal

Resolve the missing-derivation prompt for
`koide_hostile_review_guard_note_2026-04-24`.

Target prompt:

- Source note: `docs/KOIDE_HOSTILE_REVIEW_GUARD_NOTE_2026-04-24.md`
- Runner: `scripts/frontier_koide_hostile_review_guard.py`
- Audit failure: the guard claimed script print verification, but checked only
  source-text substrings for `CLOSES`, `FALSE`, and `RESIDUAL`.

Block objective:

- Replace shallow source-text script checks with executed-script stdout checks.
- Preserve the guard's narrow boundary: packet hygiene only, not positive
  Koide `Q` or `delta` closure.
- Reset the stale failed audit row to `unaudited` for independent re-audit.
