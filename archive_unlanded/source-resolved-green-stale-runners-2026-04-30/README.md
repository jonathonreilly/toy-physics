# Archive: source-resolved retarded Green's function pocket — mislabeled column

**Archived:** 2026-04-30 (README added 2026-05-01)
**Audit verdict:** audited_failed (terminal; ACCEPT)

## Why this is here

`SOURCE_RESOLVED_RETARDED_GREEN_POCKET_NOTE.md` claimed a retained
finite-lag retarded-like update giving a small positive correction
relative to a same-site-memory control. The audit found a load-bearing
column mislabeling:

- `scripts/source_resolved_retarded_green_pocket.py` prints a column
  labeled `ret/same` but **fills it with `ret_delta / inst_delta`** —
  i.e. the comparator is the *instantaneous* control, not the
  *same-site memory* control.
- The note then froze those mislabeled values around `ret/same ≈ 1.20`
  and treated this as the headline same-site improvement.
- The true `ret/same` ratio computed from the printed rows is
  approximately **1.026**, and `mean(ret support − same support)` is
  exactly **0.000e+00** (no support broadening).

So the headline ratio in the note does not measure what it claims to
measure. The safe-claim boundary (per the audit) is:
- zero-source shifts are 0
- 4/4 TOWARD
- linear fitted exponents
- positive ret−same differences of 6.32e-05 to 5.09e-04
- true ret/same ≈ 1.026
- unchanged support fraction
- mean N_eff increase of +4.493e-02

The "ret/same ~1.20 same-site improvement" and "retained
retarded-pocket result" are NOT safe to claim.

The repair target is to correct the runner and the note to compute and
label `ret/same`, `ret/inst`, `ret-same`, `support_frac delta`, and
`N_eff delta` separately, then add explicit assertion thresholds for
which of those observables constitutes a finite-lag positive. That
repair has not been done.

## Status

Archived as a terminal-failed historical record. The audit row
`source_resolved_retarded_green_pocket_note` will remain
`audited_failed` until the repair above is completed. The companion file
`SOURCE_RESOLVED_TRANSVERSE_PROPAGATING_GREEN_NOTE.md` is preserved here
as the related sibling that was archived in the same 2026-04-30 sweep.
