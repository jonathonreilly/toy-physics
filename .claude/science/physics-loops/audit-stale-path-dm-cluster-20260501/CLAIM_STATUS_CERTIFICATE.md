# Claim Status Certificate — DM Runner Stale-Path Cleanup

**Block:** audit-stale-path-dm-cluster-block01-20260501
**Branch:** physics-loop/audit-stale-path-dm-cluster-block01-20260501
**Artifact:** docs/AUDIT_DM_RUNNER_STALE_PATH_CLEANUP_NOTE_2026-05-01.md
**Files modified:** 8 runners + 1 support note

## Status

```yaml
actual_current_surface_status: support / audit-hygiene-cleanup
conditional_surface_status: null
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "Pure runner-cleanup: removes stale read() calls to notes deleted by commit d2e754fdc on 2026-04-16. Does not introduce new physics, retire any claim, or propose retention."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Disposition

The artifact is a coherent **audit-hygiene cleanup**: 8 runners had stale
`read("docs/X.md")` calls referencing notes deliberately deleted by a 2026-04-16
trim commit. Removing the dead read() calls + their dependent checks restores
each runner to FAIL=0 without introducing new physics or reverting the trim.

This block does NOT promote any claim to retained. The 8 affected claim rows
are all leaf-criticality with author-declared `support` or `bounded` status;
the cleanup only removes their noise-floor `audited_conditional` /
`audited_failed` verdicts caused by the FileNotFoundError.

## Allowed PR/Status Wording

- "audit-hygiene cleanup"
- "stale-path runner fix"
- "removes stale read() calls"
- "no load-bearing physics check removed"
- "consistent with the 2026-04-16 trim commit intent"

## Forbidden PR/Status Wording

- bare "retained" / "promoted"
- "proposed_retained" / "proposed_promoted"
- "lane closure"
- "audit cleared on physics merits"

## Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_breaking_triplet_axiom_law_attempt.py
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_triplet_normalization_target.py
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_triplet_character_source_theorem.py
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_triplet_even_response_theorem.py
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_breaking_triplet_cp_theorem.py
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_veven_bosonic_normalization_theorem.py
PYTHONPATH=scripts python3 scripts/frontier_dm_leptogenesis_projection_theorem.py
PYTHONPATH=scripts python3 scripts/frontier_dm_leptogenesis_washout_axiom_boundary.py
```

All 8 runners pass with **69 PASS / 0 FAIL** total.

## Independent Audit

Audit must verify:

1. Every removed `check()` references content that genuinely no longer exists
   on the trimmed DM surface (verified by `git show d2e754fdc --stat`).
2. The redirect for `DM_LEPTOGENESIS_FULL_AXIOM_CLOSURE_NOTE_2026-04-16.md` to
   `docs/work_history/dm/...` points to the correct relocated file.
3. No load-bearing physics check was removed — only checks that consumed
   deleted-note content.
4. The runner-internal arithmetic checks (parts that don't touch the deleted
   notes) are unchanged and continue to pass.
