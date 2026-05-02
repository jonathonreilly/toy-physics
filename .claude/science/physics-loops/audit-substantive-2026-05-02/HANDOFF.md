# Handoff: audit-substantive-2026-05-02

Resolved 6 substantive `audited_failed` rows in a single PR by FIX/NARROW.
Each row is now `unaudited` and queued for fresh independent Codex audit.

## Per-row resolutions

1. **`koide_axiom_native_support_batch_note_2026-04-22`** — FIX
   Stale audit (subrunner repaired at 5097b492, 2026-04-30; now 23/23 and
   integrated regression 381/381). Added a 2026-05-02 audit re-check section.
2. **`action_normalization_note`** — NARROW
   "Convention-free light bending fixes c=1" was wrong; PPN gamma=1 holds
   for any c>0. Reused PR #245 narrowing: convention-locked instead.
3. **`monopole_derived_note`** — NARROW
   Reconciled note's stale `M~0.80 M_Pl` (placeholder alpha_inv=40) with
   runner's computed `M=1.43 M_Pl` (one-loop RG alpha_inv=72.1). Note now
   explicitly bounded; expects audit reclassification to bounded_theorem.
4. **`lorentz_violation_derived_note`** — FIX
   Runner used non-standard `(2/a^2) sin^2(pa/2)` but expanded as if
   `(4/a^2)`. Updated runner to standard `(4/a^2)` form; residuals dropped
   from 0.788 to 1.09e-6 at pa=0.1256.
5. **`self_gravity_backreaction_closure_note`** — FIX
   Reused PR #245 `--quick` patch (~23s vs ~110s full sweep), preserving
   exact eps=0 reduction + step-local Born + one nonzero-coupling row.
6. **`dimensional_gravity_table`** — NARROW
   Removed "F~M=1.00 universal across all dimensions/h/parameters" claim;
   replaced with finite-entry inventory scope.

## State change

| metric | origin/main | this branch |
|---|---|---|
| `audit_status=audited_failed` | 70 | 64 |
| `effective_status=audited_failed` | 26 | 20 |
| `audit_lint warnings` | 78 | 78 |
| `audit_lint errors` | 0 | 0 |

## Honest open items

- All 6 rows are `unaudited` pending fresh Codex audit. They will land at
  one of `audited_clean` / `audited_conditional` / `audited_decoration` /
  `audited_renaming` / `audited_failed` / `audited_numerical_match`
  depending on the audit verdict.
- `monopole_derived_note` still carries `claim_type=positive_theorem`;
  the note language has been narrowed to bounded (RG-window-dependent),
  so the Codex re-audit should reclassify it as `bounded_theorem`.
- `action_normalization_note` honest claim is now convention-locked
  rather than convention-free; same bounded_theorem class but with a
  cleaner load-bearing step.

## Files touched

Source notes:
- `docs/ACTION_NORMALIZATION_NOTE.md`
- `docs/DIMENSIONAL_GRAVITY_TABLE.md`
- `docs/KOIDE_AXIOM_NATIVE_SUPPORT_BATCH_NOTE_2026-04-22.md`
- `docs/LORENTZ_VIOLATION_DERIVED_NOTE.md`
- `docs/MONOPOLE_DERIVED_NOTE.md`
- `docs/SELF_GRAVITY_BACKREACTION_CLOSURE_NOTE.md`

Runners:
- `scripts/frontier_action_normalization.py` (narrowed Test 3 + Test 5 + Verdict)
- `scripts/frontier_lorentz_violation.py` (kinetic term `(2/a^2) -> (4/a^2)`)
- `scripts/frontier_monopole_derived.py` (synthesis label, header docstring)
- `scripts/poisson_self_gravity_loop_v3.py` (added `--quick` flag)

Audit data (regenerated mechanically by `bash docs/audit/scripts/run_pipeline.sh`):
- `docs/audit/AUDIT_LEDGER.md`
- `docs/audit/AUDIT_QUEUE.md`
- `docs/audit/data/*`
