# Migration Plan — From today's schema to the proposed model

**Date:** 2026-05-02

The migration is split into five phases, each with explicit rollback. The
phases are designed so that **the live audit pipeline keeps working at every
step** — there is no flag day. New work uses the new model; legacy rows
backfill or get re-audited as they age out.

## Inventory at start of migration

From `docs/audit/AUDIT_LEDGER.md` summary as of 2026-05-02:

- 1572 ledger rows
- 76 `effective_status = retained`
- 71 `effective_status = retained_no_go`
- 1 `effective_status = proposed_retained`
- 151 `effective_status = bounded`
- 122 `effective_status = support`
- 6 `effective_status = open`
- 1145 in various failure / unaudited states
- 985 source notes are `current_status = unknown` (mostly README-style)
- ~454 source notes have a `Status:` line that needs handling
- 1601 total source notes

## Phase 1 — Schema additive (1 PR, ~1 day, no behavior change)

### Goal
Add new fields to `audit_ledger.json` without removing existing fields.
Pipeline scripts read both during the transition.

### Changes

1. Bump `schema_version` in `audit_ledger.json`.
2. Add per-row fields:
   - `claim_type: string | null` (default null until backfilled)
   - `claim_scope: string | null` (default null)
   - `claim_type_provenance: "audited" | "backfilled" | "author_hint" | null`
   - `claim_type_author_hint: string | null` (extracted from new optional `Type:` line)
3. `seed_audit_ledger.py` learns to extract optional `Type:` hint from
   source notes (no source notes have one yet, so extraction is a no-op).
4. `apply_audit.py` learns to write the two new fields when an audit
   response includes them.
5. `compute_effective_status.py` keeps using the current rule (reads
   `current_status` + `audit_status`).
6. `audit_lint.py` emits warnings (not errors) when a clean-audit row has a
   null `claim_type`.

### Output
Schema is forward-compatible. New audit responses can include `claim_type`;
old ones don't and pipeline doesn't care.

### Rollback
Revert the migration commit; schema is additive so nothing downstream
breaks.

## Phase 2 — New audit prompt template lands (1 PR, ~1 day)

### Goal
Audit agent (Codex GPT-5.5) starts returning `claim_type` and `claim_scope`
on every new audit. Existing audited rows are unaffected.

### Changes

1. Replace `docs/audit/AUDIT_AGENT_PROMPT_TEMPLATE.md` with the proposed
   replacement from this proposal directory.
2. Update the audit-runner wrapper script (whichever script POSTs to Codex)
   to validate the JSON response against the new schema (the new fields
   are required).
3. Update `apply_audit.py` to require `claim_type` on accepted responses.

### Output
- All audits performed *after* this PR include `claim_type` and
  `claim_scope`.
- Audits performed *before* this PR retain `claim_type = null`.

### Rollback
Revert the prompt template + apply_audit.py commit. The two new fields
become null again on subsequent audits; the validation requirement loosens.
Phase 1 schema-additive changes stay in place harmlessly.

## Phase 3 — Backfill `claim_type` for existing audited rows (1 PR, ~1 day)

### Goal
Avoid re-auditing 1572 rows from scratch. Backfill `claim_type` from a
deterministic inference rule, mark `claim_type_provenance = backfilled`.

### Inference rule

For each row with `audit_status != null` and `claim_type = null`:

```python
def backfill_claim_type(row):
    note_in_archive = row.note_path.startswith("archive_unlanded/")
    if row.audit_status == "audited_decoration":
        return "decoration"
    if row.audit_status == "audited_failed" and note_in_archive:
        return "no_go"   # ratified failure record
    if row.current_status in {"unknown"} and looks_like_meta(row.note_path):
        return "meta"
    if row.current_status in {"open"}:
        return "open_gate"
    if row.current_status in {"bounded", "proposed_bounded"}:
        return "bounded_theorem"
    if row.current_status in {"proposed_no_go"}:
        return "no_go"
    if row.current_status in {"support", "proposed_retained", "proposed_promoted"}:
        return "positive_theorem"   # default; audit-clean cases get full retained, others stay where they are
    return None  # leave for explicit re-audit

def looks_like_meta(note_path):
    name = note_path.split("/")[-1].upper()
    return any(name.endswith(suffix) for suffix in ["README.MD", "INDEX.MD", "_GUIDE.MD"]) \
        or "/lanes/" in note_path \
        or "/repo/" in note_path
```

### Critical-row protection

For `criticality = critical` rows (currently 91 rows), do **not** backfill
silently. Instead:

- mark `claim_type_provenance = backfill_pending_critical`
- enqueue at the top of `AUDIT_QUEUE.md` for an explicit re-audit
- the next audit pass produces a properly-set `claim_type` from the new
  prompt template

This protects the highest-stakes rows from inheriting a wrong
classification through backfill. Non-critical rows accept the deterministic
backfill.

### Validation

After backfill, run `audit_lint.py --strict` to confirm:

- No `audited_clean` row has `claim_type = null`.
- No `audited_decoration` row has `claim_type != decoration`.
- All critical rows have `claim_type_provenance ∈ {audited,
  backfill_pending_critical}`.

### Rollback
The backfill script also writes `previous_claim_type = null` so the row's
state before backfill is preserved. Rollback resets `claim_type` to null on
all `claim_type_provenance = backfilled` rows. Audited rows from phase 2
keep their `claim_type` (those are real audit results, not backfill).

## Phase 4 — Switch `compute_effective_status.py` to new rule (1 PR, ~2 days)

### Goal
Stop using `current_status` for `effective_status` computation. Use the new
rule from [`02_PROPAGATION_RULES.md`](02_PROPAGATION_RULES.md).

### Changes

1. Rewrite `compute_effective_status.py` per the new rule.
2. Update `audit_lint.py` to enforce the new rule:
   - `audited_clean` + `claim_type = null` is now an error, not a warning
     (every row should have a backfilled or audited `claim_type` after
     phase 3).
3. Update `render_audit_ledger.py` to render the new `effective_status`
   enum (adds `retained_bounded`, `open_gate`, removes `support`/`bounded`/`open`).

### Expected ledger summary changes after phase 4

| effective_status | before phase 4 | after phase 4 |
|---:|---:|---:|
| `retained` | 76 | 76 + 122 (currently support+audited_clean) − any that have unaudited deps + new audit-clean rows from phase 2-3 ≈ 180-200 |
| `retained_no_go` | 71 | unchanged or slightly higher |
| `retained_bounded` | (new) | ~150 (most current `bounded` rows that are clean for narrow scope) |
| `proposed_retained` | 1 | dynamic; small (just rows with clean audit but unaudited deps) |
| `support` | 122 | 0 (gone) |
| `bounded` | 151 | 0 (gone, became `retained_bounded` or `audited_conditional`) |
| `open` | 6 | 0 (became `open_gate`) |
| `open_gate` | (new) | 6 + new-style open-work rows |
| `unaudited` | 428 | 428 + meta moved out |
| `meta` | (new) | ~985 (the previously-`unknown` README rows) |

### Rollback
Revert the compute_effective_status.py rewrite. The script returns to
reading `current_status`. The new fields stay in the schema as no-ops
(they continue to be populated but ignored).

## Phase 5 — Strip `Status:` lines from source notes (1 PR, ~half a day)

### Goal
Remove the now-vestigial `Status:` lines from `docs/*.md`. The audit ledger
is canonical.

### Changes

1. Extend `docs/audit/scripts/relabel_status_lines.py` with a new mode
   `--strip` that removes `**Status:**` and `Status:` lines entirely.
2. Run with `--dry-run` first; sanity-check the diff.
3. Apply. ~454 source notes touched.
4. The script is idempotent (re-run is a no-op).
5. `seed_audit_ledger.py` no longer needs to extract `current_status` from
   source notes.
6. The `current_status` field can be dropped from the schema in this PR or
   the next (it has been unused since phase 4).

### Optional: Replace stripped Status lines with auto-rendered banner

Some source notes are easier to read with a status banner. The pipeline can
auto-render one at the top of each source note from the ledger row's
`effective_status` and `claim_type`, in a clearly-marked
`<!-- AUDIT_BANNER_START -->...<!-- AUDIT_BANNER_END -->` block. This is
optional and can land as a follow-on PR.

### Rollback
The relabel script's regex is reversible. Rollback re-inserts a default
`**Status:** unknown` line where one was stripped. Authors can then re-edit.

## Phase 6 — Drop `current_status` from schema (1 PR, optional, ~1 hour)

### Goal
Remove the `current_status` field from `audit_ledger.json` rows entirely.

### Changes

1. Bump `schema_version` again.
2. `seed_audit_ledger.py` stops writing `current_status`.
3. `apply_audit.py`, `compute_effective_status.py`, `audit_lint.py`,
   `render_audit_ledger.py` stop reading `current_status`.
4. Migration script removes `current_status` from existing rows.

### Rollback
Schema is now strictly smaller. To rollback, restore the field with a
default value (`unknown`). The post-rollback compute_effective_status.py
would need to read it again, which is the phase-4-rollback path.

## Total scope estimate

- 6 PRs over ~1 week of focused work
- ~120 lines of Python edits to existing scripts
- ~80-150 line new prompt template
- ~30 lines of doc deltas to README.md, FRESH_LOOK_REQUIREMENTS.md, vocabulary
- ~70 lines of doc deltas to two SKILL files
- 1601 source notes touched mechanically (Status line strip)
- 0 new audits required by the migration (backfill handles existing rows;
  new audits naturally use the new template)

## Critical-path constraints

- Phase 2 (new prompt template) can only land after phase 1.
- Phase 3 (backfill) can only land after phase 1, 2 — needs the new fields
  in place.
- Phase 4 (new compute rule) can only land after phase 3 — needs every row
  to have a `claim_type`.
- Phase 5 (strip Status lines) can land any time after phase 4.
- Phase 6 (drop `current_status`) is optional cleanup; defer indefinitely
  if the field's continued presence is harmless.

## Success criteria

After phase 4 lands:

- Every row in `audit_ledger.json` has a `claim_type`.
- Every clean-audited row whose dependency chain is clean has
  `effective_status ∈ {retained, retained_no_go, retained_bounded}`.
- The 122-row backlog of `support + audited_clean` is gone.
- The audit pipeline is at least as strict as before; no failure-mode-of-
  original-CKM-trace can land an `audited_clean` verdict that wouldn't have
  been caught under the old system.
- The `physics-loop` and `review-loop` SKILLs work without referring to
  `current_status` or `proposed_retained` author tiers.
