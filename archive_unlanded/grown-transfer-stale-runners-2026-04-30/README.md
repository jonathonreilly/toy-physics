# Archive: grown transfer basin — stale runner criterion

**Archived:** 2026-04-30 (README added 2026-05-01)
**Audit verdict:** audited_failed (terminal; ACCEPT)

## Why this is here

`GROWN_TRANSFER_BASIN_NOTE.md` claimed a retained narrow grown-row basin
positive based on "signed-source sign law + complex-action TOWARD → AWAY
crossover + near-linear F~M" preserved on nearby grown rows. The audit
found a contradictory artifact chain:

- The headline retained basin claim depends on a same-row signed-source
  plus complex-action survival decision.
- `scripts/GROWN_TRANSFER_BASIN_TARGETED.py` still applies the rejected
  exact criterion `abs(row.action_gamma0) < 1e-12`, which the source note
  itself said is the wrong selection rule.
- That runner reports "nearby rows surviving both observables: 0/4" and
  "the retained positives do not survive this nearby basin" — directly
  contradicting the note's "narrow grown-row basin is retained" claim.

So the artifact chain is internally inconsistent for the plural basin
promotion. The safe-claim boundary (per the audit) is: only the central
retained grown row and the single middle diagnostic row at
drift=0.20, restore=0.60 pass the corrected signed-source and
complex-action checks. The plural "narrow grown-row basin" claim is NOT
retained.

The repair target is to patch the targeted basin checker to use the
source note's stated criterion, require same-row intersection of
signed-source and complex-action survival, rerun and archive the
targeted and full basin outputs, and rewrite the note only after the
executable SAFE READ matches the retained claim. That repair has not
been done.

## Status

Archived as a terminal-failed historical record. The audit row
`grown_transfer_basin_note` will remain `audited_failed` until the
repair above is completed; it should not be cited as a retained
multi-row basin result in the meantime.
