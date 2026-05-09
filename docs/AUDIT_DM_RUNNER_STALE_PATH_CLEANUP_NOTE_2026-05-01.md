# Audit DM Runner Stale-Path Cleanup

**Type:** meta

**Date:** 2026-05-01
**Status:** support / audit-hygiene cleanup. This note does **not** propose
retention for any claim. It documents a surgical removal of stale `read()`
calls from 8 DM-cluster runners whose target files were intentionally
deleted by commit `d2e754fdc` (2026-04-16, "Trim DM package to science-only
surface").
**Lane:** audit-hygiene. No physics claim is added or removed.

## Inputs (registered runners with caches)

The hygiene claim "69 PASS / 0 FAIL across 8 affected runners" is
verified by the eight runners' own SHA-pinned caches under
`logs/runner-cache/`. Each runner is registered with its own audit row
and cache; this hygiene note does not add a new aggregating runner. The
cited per-runner caches are:

- `logs/runner-cache/frontier_dm_neutrino_breaking_triplet_axiom_law_attempt.txt`
- `logs/runner-cache/frontier_dm_neutrino_triplet_normalization_target.txt`
- `logs/runner-cache/frontier_dm_neutrino_triplet_character_source_theorem.txt`
- `logs/runner-cache/frontier_dm_neutrino_triplet_even_response_theorem.txt`
- `logs/runner-cache/frontier_dm_neutrino_breaking_triplet_cp_theorem.txt`
- `logs/runner-cache/frontier_dm_neutrino_veven_bosonic_normalization_theorem.txt`
- `logs/runner-cache/frontier_dm_leptogenesis_projection_theorem.txt`
- `logs/runner-cache/frontier_dm_leptogenesis_washout_axiom_boundary.txt`

Each cache reports its own per-runner PASS/FAIL summary; the aggregate
"69 PASS / 0 FAIL" line in §2 is the sum of those eight per-runner
summaries (13+6+6+6+8+10+10+10 = 69). The hygiene note does not gate
on a single aggregating runner; the per-runner caches are the audit
trail.

---

## 0. Why this note exists

Eight runners under `scripts/` carried `read("docs/X.md")` calls referencing
notes deleted by the 2026-04-16 trim commit. Each runner's audit row was
landing with a non-clean verdict because:

- The audit pipeline's restricted environment (and any local rerun) raised
  `FileNotFoundError` for the deleted-note path.
- The verdict text said "primary runner returned nonzero in the restricted
  audit environment" without naming the underlying cause.

The runners' load-bearing physics content does **not** require the deleted
notes. The deleted-note `check()` calls were verifying historical content
(e.g., the YUKAWA blocker's `gamma`/`A + b - c - d` triplet structure, the
DM_LEPTOGENESIS_NOTE's `0.30` Davidson-Ibarra benchmark) that has since
been deliberately retired from the canonical surface.

This cleanup removes the stale calls and their dependent checks, restoring
each runner to FAIL=0 without introducing new physics or reverting the
2026-04-16 trim. It is hygiene consistent with the original trim's intent.

## 1. Affected runners and changes

| runner | stale path(s) removed | redirect | check(s) removed |
|---|---|---|---|
| `frontier_dm_neutrino_breaking_triplet_axiom_law_attempt.py` | `DM_NEUTRINO_YUKAWA_BLOCKER_NOTE_2026-04-14.md`, `DM_LEPTOGENESIS_NOTE.md` | none (deleted) | "blocker note records the triplet as the live last-mile object", "leptogenesis note records the 0.30 benchmark", "atlas carries the DM triplet axiom-boundary row" (atlas row also trimmed) |
| `frontier_dm_neutrino_triplet_normalization_target.py` | `DM_NEUTRINO_YUKAWA_BLOCKER_NOTE_2026-04-14.md`, `DM_LEPTOGENESIS_BENCHMARK_DECOMPOSITION_NOTE_2026-04-15.md` | none (deleted) | "branch records 0.30 shortfall is mainly CP-kernel suppression", "remaining normalization law must populate gamma" |
| `frontier_dm_neutrino_triplet_character_source_theorem.py` | `DM_NEUTRINO_YUKAWA_BLOCKER_NOTE_2026-04-14.md` | none (deleted) | "blocker note carries the phase-fixed triplet-side object" |
| `frontier_dm_neutrino_triplet_even_response_theorem.py` | `DM_NEUTRINO_YUKAWA_BLOCKER_NOTE_2026-04-14.md` | none (deleted) | "blocker note points at the even response channels" |
| `frontier_dm_neutrino_breaking_triplet_cp_theorem.py` | `DM_NEUTRINO_YUKAWA_BLOCKER_NOTE_2026-04-14.md` | none (deleted) | "atlas carries the breaking-triplet CP theorem row" (also trimmed), "blocker note now points at gamma and the two interference channels" |
| `frontier_dm_neutrino_veven_bosonic_normalization_theorem.py` | `DM_NEUTRINO_YUKAWA_BLOCKER_NOTE_2026-04-14.md`, `DM_LEPTOGENESIS_NOTE.md` | none (deleted) | "blocker note still records E1 and E2", "leptogenesis note still records benchmark remains bounded" |
| `frontier_dm_leptogenesis_projection_theorem.py` | `docs/DM_LEPTOGENESIS_FULL_AXIOM_CLOSURE_NOTE_2026-04-16.md` | redirected to `docs/work_history/dm/DM_LEPTOGENESIS_FULL_AXIOM_CLOSURE_NOTE_2026-04-16.md` | none (path redirect preserves all checks) |
| `frontier_dm_leptogenesis_washout_axiom_boundary.py` | `DM_LEPTOGENESIS_EXACT_KERNEL_AUDIT_NOTE_2026-04-15.md` (deleted) plus stale substring check `"m_tilde_eV = Y0_SQ * V_EW**2 / M1 * 1e9"` | none | "earlier audit recorded retained thermal dilution / strong-washout fit", "closure runner used pre-projection m_tilde without K00" (refactored to `pkg.m_tilde_exact_eV`) |

In every runner the change is a docstring-style comment block describing
which checks were removed and why (with reference to commit `d2e754fdc`),
followed by the removal of the corresponding `read()` calls and `check()`
lines. No load-bearing physics check is removed.

## 2. Verification

Every affected runner is independently re-runnable and now passes:

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_breaking_triplet_axiom_law_attempt.py
# PASS=13 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_triplet_normalization_target.py
# PASS=6 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_triplet_character_source_theorem.py
# PASS=6 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_triplet_even_response_theorem.py
# PASS=6 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_breaking_triplet_cp_theorem.py
# PASS=8 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_veven_bosonic_normalization_theorem.py
# PASS=10 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_dm_leptogenesis_projection_theorem.py
# PASS=10 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_dm_leptogenesis_washout_axiom_boundary.py
# PASS=10 FAIL=0
```

Total: **69 PASS / 0 FAIL** across the cluster.

## 3. What this changes for the audit ledger

Each affected claim row previously carried an audit verdict tied to the
runner failing in the restricted audit environment. After this hygiene
repair, the independent audit lane owns any future verdict; this note only
removes the stale-path runner noise so future reviews can decide on the
substantive content.

Importantly: **all eight affected claim rows are leaf-criticality with
author-declared `current_status` of `support` or `bounded`.** Clearing the
stale-path conditional does NOT promote any claim to `retained`. It simply
removes a noise floor of "audit fails because the runner can't open a file
that was deliberately deleted" verdicts.

## 4. Out of scope

- Restoring the deleted notes. The 2026-04-16 trim was deliberate; this
  cleanup respects that decision.
- Re-deriving the deleted-note content elsewhere. If any of the deleted
  content needs to be re-canonicalized, that is a separate science task,
  not audit hygiene.
- Promoting any of the affected leaf rows to `retained`. The author-declared
  `support`/`bounded` status is preserved; only the audit verdict noise is
  removed.
- Other stale-path runners. The campaign also identified
  `frontier_pmns_intrinsic_completion_boundary.py` (6 stale PMNS paths) and
  `frontier_gauge_vacuum_plaquette_first_sector_zero_extension_factorized_class_theorem_2026_04_19.py`
  (1 stale path to an archive_unlanded note). Those are not addressed here
  because their notes' content may still be needed in the live runner; they
  warrant a separate audit-hygiene block.

## 5. Forbidden-import role

This note introduces no new physical content, no new numerical comparators,
no new admitted observations. It is structural cleanup of runner code only.

## 6. Safe wording

**Can claim:**
- "Stale `read()` calls to deleted notes were removed."
- "Each affected runner now passes with FAIL=0 from a clean checkout."
- "No load-bearing physics check was removed."
- "The fix is consistent with the 2026-04-16 trim commit's intent."

**Cannot claim:**
- "Retained" / "promoted" — bare retention language is not allowed.
- "Lane closure." (it isn't)
- "Audit cleared on physics merits." — the audit must independently re-rate
  these rows; this PR removes only the stale-path failure mode.
