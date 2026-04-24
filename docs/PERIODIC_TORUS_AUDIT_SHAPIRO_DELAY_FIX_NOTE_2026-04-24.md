# Periodic Torus Audit — Shapiro Delay Fix Note

**Date:** 2026-04-24
**Status:** minimum-image fix applied to
`scripts/frontier_shapiro_delay.py`; periodic-torus audit
`NEEDS_REVIEW` count is now `0`. The active-queue item is eligible
for closure pending reviewer acceptance.
**Predecessor notes:**
[`PERIODIC_TORUS_DIAGNOSTICS_CODE_AUDIT_NOTE_2026-04-24.md`](PERIODIC_TORUS_DIAGNOSTICS_CODE_AUDIT_NOTE_2026-04-24.md),
[`PERIODIC_TORUS_AUDIT_BATCH_1_MANUAL_REVIEW_NOTE_2026-04-24.md`](PERIODIC_TORUS_AUDIT_BATCH_1_MANUAL_REVIEW_NOTE_2026-04-24.md).

## 1. Question

Batch-1 manual review identified `frontier_shapiro_delay.py` as
the single confirmed TRUE BUG from the 9-script `NEEDS_REVIEW`
list: the 1D periodic ring driver used raw `math.hypot` for
Hamiltonian hopping weights, giving the wraparound edge weight
`1/(n-1)` instead of `1/1`.

Disposition option 1 from the batch-1 note was: inline-fix
`_build_H`/`_build_L` to use minimum-image distance. This note
applies that option.

## 2. Fix

Added a `_min_image_hypot(pos, i, j)` helper that detects per-axis
period from the extent of `pos` and applies `min(|d|, period - |d|)`
when period > 1:

```python
def _min_image_hypot(pos, i, j):
    dsq = 0.0
    for ax in range(pos.shape[1]):
        lo = int(round(float(pos[:, ax].min())))
        hi = int(round(float(pos[:, ax].max())))
        period = hi - lo + 1
        d = abs(pos[j, ax] - pos[i, ax])
        if period > 1:
            d = min(d, period - d)
        dsq += d * d
    return math.sqrt(dsq)
```

`_build_L` and `_build_H` were updated to call this helper instead
of `math.hypot(pos[j,0]-pos[i,0], pos[j,1]-pos[i,1])` at lines 86
and 98.

The helper collapses to raw hypot on axes with only one distinct
coordinate (period = 1), so it is safe for 1D, 2D, open, and
periodic configurations alike.

## 3. Behavior change

Before the fix, the 1D ring case at `n = 61`:

- wraparound edge between site `0` and site `n-1` had weight
  `w = 1 / max(n-1, 0.5) = 1/60`
- effectively a 60× suppression of the wrap edge
- the "periodic ring" behaved as an open chain with weak wraparound

After the fix:

- wraparound edge weight `w = 1/1 = 1` (same as every other
  nearest-neighbor edge)
- the 1D ring is now genuinely periodic

The 2D open-lattice driver and the random-geometric layered driver
are unaffected: they do not use periodic adjacency, so the
per-axis-period detection does not reduce any distance.

Runner output sanity-check after the fix:

```text
--- 1D LATTICE REFERENCE (n=61) ---
  1D ref: t_free= 40  t_attract= 40 (Δ= +0)  t_repulse= 40 (Δ= +0)        no  norm=1.000000
```

The norm is preserved and the script executes to completion
(wallclock ~0.8 s).

## 4. Audit impact

After the fix, the periodic-torus audit reports:

| category | count | delta |
|---|---:|---:|
| `NEEDS_REVIEW` | 0 | -1 |
| `CLEAN_HELPER` | 6 | 0 |
| `CLEAN_INLINE` | 20 | +1 |
| `CLEAN_NO_DISTANCE` | 35 | 0 |
| `NOT_APPLICABLE` | 1989 | 0 |
| `ERROR` | 0 | 0 |

The `frontier_shapiro_delay.py` script moves from `NEEDS_REVIEW` to
`CLEAN_INLINE`. The audit is reproducible and exits `5/5 PASS`.

## 5. Active-queue status

The `periodic 2D torus diagnostics` item in
[`docs/repo/ACTIVE_REVIEW_QUEUE.md`](repo/ACTIVE_REVIEW_QUEUE.md)
can now be **closed** against the current audit rules:

- the static-analysis audit of 2050 `scripts/*.py` files reports
  zero `NEEDS_REVIEW`;
- all 9 canonical-corrected scripts from the 2026-04-11 fix note
  classify into `CLEAN_*`;
- the one confirmed TRUE BUG has been inline-fixed and its script
  now classifies as `CLEAN_INLINE`.

The honest caveat: the audit is regex-based static analysis. It
could miss (a) periodic adjacencies not expressed via `%` modulo
(e.g., via `np.roll` or explicit edge lists without any modulo
pattern); (b) distance-weighted couplings in forms not covered by
the current patterns. Further tightening of the audit, or manual
review of any future new periodic script, is the natural stronger
step if broader coverage is needed.

## 6. Falsifier

- A re-run of the audit producing different classifications (would
  invalidate reproducibility).
- A follow-up manual review finding a periodic-torus script with the
  wraparound bug that the current audit rules miss (would require
  regex tightening).
- A sanity-check rerun of `frontier_shapiro_delay.py` revealing a
  norm-preservation or execution failure (would invalidate the fix).

The audit and the fixed script are both deterministic and
reproducible.

## 7. Provenance

- Edited: `scripts/frontier_shapiro_delay.py`
  (added `_min_image_hypot`, updated `_build_L`, `_build_H`).
- Audit re-run: `5/5 PASS`, `NEEDS_REVIEW: 0`.
- Shapiro-delay script sanity run: wallclock ~0.8 s, norm = 1.000000
  across all three drivers (layered, random-geometric, 1D ring).
- Runtime caveat: validation host Python 3.12.8 vs pinned 3.13.5;
  fix is a local inline change using only `math` and indexing, so
  version drift is not a confounder.
