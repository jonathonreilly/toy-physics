# Persistent Object Inward Boundary Floor Diagnosis

**Date:** 2026-04-16  
**Status:** bounded local negative; widening the compact-object floor from `top4`
to `top5`, `top6`, or `top8` does not reopen the residual inward-source misses,
so the live exact-lattice limit is directional/source placement rather than a
too-narrow self-maintaining floor

**Audit-conditional perimeter (2026-05-07):**
The audit lane has classified this row `audited_conditional` with
`auditor_confidence = high`, `chain_closes = false`, and load-bearing
step class `C`. The audit chain-closure explanation is exact: "the
retained top4 dependency and current cache support only the top_keep=4
widened-pocket result. The decisive top5/top6/top8 inward-source runs
are cited as logs, but those log paths are absent in this checkout and
no completed cache for those invocations is provided." The
audit-stated repair target is: "compute_required: rerun or supply
cached completed top_keep=5, top_keep=6, and top_keep=8 inward-source
sweep artifacts covering the four cited inward rows." This
rigorization edit supplies those cached top5/top6/top8 inward-source
artifacts (see "Cached top5/top6/top8 inward-source artifacts" below)
so the audit's `compute_required` repair can be picked up on a
re-audit pass. Nothing here promotes audit status. The retained
runner [`scripts/persistent_object_top4_multistage_transfer_sweep.py`](../scripts/persistent_object_top4_multistage_transfer_sweep.py)
sha256 remains
`c9f10056bf35ed16e0baa7806e5dcd0c3d7bae12412229b5527a837c3dca206d`,
unchanged by this edit; the artifact additions are pure cache deposits
of `--top-keep 5`, `--top-keep 6`, and `--top-keep 8` invocations on
the four-case inward-source sweep.

## Artifact chain

- Script: [`scripts/persistent_object_top4_multistage_transfer_sweep.py`](../scripts/persistent_object_top4_multistage_transfer_sweep.py)
- Prior `top4` transfer note: [`docs/PERSISTENT_OBJECT_TOP4_MULTISTAGE_TRANSFER_SWEEP_NOTE_2026-04-16.md`](PERSISTENT_OBJECT_TOP4_MULTISTAGE_TRANSFER_SWEEP_NOTE_2026-04-16.md)
- `top5` inward-source sweep cache: [`outputs/persistent_object_top5_inward_source_sweep_2026-05-10.txt`](../outputs/persistent_object_top5_inward_source_sweep_2026-05-10.txt)
- `top6` inward-source sweep cache: [`outputs/persistent_object_top6_inward_source_sweep_2026-05-10.txt`](../outputs/persistent_object_top6_inward_source_sweep_2026-05-10.txt)
- `top8` inward-source sweep cache: [`outputs/persistent_object_top8_inward_source_sweep_2026-05-10.txt`](../outputs/persistent_object_top8_inward_source_sweep_2026-05-10.txt)

## Question

The widened-pocket multistage transfer sweep left a narrow residual boundary:

> `source0.75` and `source1.00` still closed, while `source1.25` and `source1.50`
> reopened under the first self-maintaining floor `top4`

That left one honest discriminator:

> are those two remaining inward misses just a floor-width issue, or do they
> mark a deeper directional/source-placement limit of the exact-lattice route?

## Frozen setup

Held fixed:

- exact lattice with `h = 0.25`
- retained blended readout `blend = 0.25`
- same multistage protocol: `3` updates per segment, `3` chained segments
- same inward-source rows only: `source0.75`, `source1.00`, `source1.25`, `source1.50`

Varied only:

- compact-object floor width `top_keep in {4, 5, 6, 8}`

## Frozen result

### Headline

Broadening the floor does **not** reopen the inward boundary.

The inward-side totals are:

- `top4`: `2 / 4`
- `top5`: `2 / 4`
- `top6`: `2 / 4`
- `top8`: `2 / 4`

The same rows stay open throughout:

- `source1.25`: open
- `source1.50`: open

The same rows stay closed throughout:

- `source0.75`: closed
- `source1.00`: closed

### Row-by-row read

| inward row | `top4` | `top5` | `top6` | `top8` | retained read |
| --- | --- | --- | --- | --- | --- |
| `source0.75` | closed | closed | closed | closed | overlap, carry, alpha, and drift all stay clean; the remaining miss is directional rather than width |
| `source1.00` | closed | closed | closed | closed | response-law miss persists; `alpha = 1.11` at `top4`, then `alpha = 0.76` at `top5/6/8` |
| `source1.25` | open | open | open | open | stable reopened inward row |
| `source1.50` | open | open | open | open | stable reopened inward row |

### Why `source0.75` is not a width miss

At broader widths `top5`, `top6`, and `top8`, the `source0.75` row keeps:

- stage overlap `[0.980, 1.000, 1.000]`
- carry `[1.000, 1.000]`
- stage alpha `[1.02, 1.02, 1.02]`
- drift `0.000%`

So the row is no longer failing any width-like self-maintenance gate. The
remaining retained miss is directional: the sourced response does not stay on
the admissible sign/toward branch under this deep inward placement.

### Why `source1.00` is a different failure

`source1.00` does not reopen either, but for a different reason:

- at `top4` it already misses high with `alpha = [1.11, 1.11, 1.11]`
- at `top5`, `top6`, and `top8` it flips to a low-exponent miss
  `alpha = [0.76, 0.76, 0.76]`

So `source1.00` is not “almost open with a slightly wider object.” Its
response law itself is unstable under deeper inward source placement.

## Safe read

This closes the cheapest remaining floor-width loophole.

The strongest honest statement is now:

> the exact-lattice compact-object route has a real transferable multistage
> floor at `top4`, but the residual inward-source boundary is not cured by
> broadening to `top5`, `top6`, or `top8`; the live local limit is
> directional/source placement, not narrow-floor width.

That is still materially below matter closure, but it is strong enough to stop
pretending that one more small compactness retune is likely to fix the branch.

## What this proves

- `top4` is a real self-maintaining floor, not just a lucky narrow optimum
- the two surviving inward misses are not repaired by broader compact floors
- the remaining exact-lattice limit is now sharper: directional/source
  placement rather than floor width

## What it does not prove

- full local-pocket universality
- beyond-pocket transfer
- a self-maintaining inertial-mass law
- matter closure

## Branch verdict

The exact-lattice branch should now be read as:

> a bounded transferable multistage compact-object floor with a persistent
> inward-source directional boundary

not as:

> a route that is still obviously waiting for one slightly broader floor.

## Best next move

Only two next moves still look honest:

1. one farther transfer sweep beyond the widened local pocket, to see whether
   the branch has any portability beyond this neighborhood at all
2. if that fails quickly, freeze the exact-lattice route cleanly and move the
   science budget to a different self-maintaining object architecture

## Cached top5/top6/top8 inward-source artifacts (2026-05-10)

The 2026-05-07 audit verdict explicitly required cached `top_keep = 5`,
`top_keep = 6`, and `top_keep = 8` inward-source sweep artifacts
covering the four cited inward rows
(`source0p75`, `source1p00`, `source1p25`, `source1p50`).

Those artifacts now exist as deterministic re-runs of the retained
runner [`scripts/persistent_object_top4_multistage_transfer_sweep.py`](../scripts/persistent_object_top4_multistage_transfer_sweep.py)
under the `--top-keep <N>` and `--case-labels <inward>` switches:

```bash
python3 scripts/persistent_object_top4_multistage_transfer_sweep.py \
  --top-keep 5 --case-labels source0p75,source1p00,source1p25,source1p50

python3 scripts/persistent_object_top4_multistage_transfer_sweep.py \
  --top-keep 6 --case-labels source0p75,source1p00,source1p25,source1p50

python3 scripts/persistent_object_top4_multistage_transfer_sweep.py \
  --top-keep 8 --case-labels source0p75,source1p00,source1p25,source1p50
```

The captured outputs are at
[`outputs/persistent_object_top5_inward_source_sweep_2026-05-10.txt`](../outputs/persistent_object_top5_inward_source_sweep_2026-05-10.txt),
[`outputs/persistent_object_top6_inward_source_sweep_2026-05-10.txt`](../outputs/persistent_object_top6_inward_source_sweep_2026-05-10.txt),
and
[`outputs/persistent_object_top8_inward_source_sweep_2026-05-10.txt`](../outputs/persistent_object_top8_inward_source_sweep_2026-05-10.txt).

Each cache reproduces the note's frozen 2/4 inward-source split and
the same row-level pattern reported in section "Frozen result":

| inward row | `top5` | `top6` | `top8` | matches frozen note? |
|---|---|---|---|---|
| `source0p75` | admissible = False, overlap = `[0.980, 1.000, 1.000]`, carry = `[1.000, 1.000]`, alpha = `[1.02, 1.02, 1.02]`, drift = `0.000%` | identical | identical | yes |
| `source1p00` | admissible = False, overlap = `[0.970, 1.000, 1.000]`, carry = `[1.000, 1.000]`, alpha = `[0.76, 0.76, 0.76]`, drift = `0.004%` | identical | identical | yes (matches note's `alpha = 0.76` at `top5/6/8`) |
| `source1p25` | admissible = True, overlap = `[0.966, 1.000, 1.000]`, carry = `[1.000, 1.000]`, alpha = `[0.99, 0.99, 0.99]` | identical | identical | yes |
| `source1p50` | admissible = True, overlap = `[0.968, 1.000, 1.000]`, carry = `[1.000, 1.000]`, alpha = `[1.02, 1.02, 1.02]` | identical | identical | yes |
| **Total inward-side admissible** | 2/4 | 2/4 | 2/4 | yes (matches the note's frozen 2/4 at every width) |

The wall time per width was approximately 180 s on this checkout; all
three runs returned exit code 0.

These cached artifacts close the audit's `compute_required` repair
target literally as stated. They do not change the conditional
perimeter scope: the live local limit remains directional / source
placement rather than narrow-floor width, and the note continues to
disclaim full local-pocket universality, beyond-pocket transfer, a
self-maintaining inertial-mass law, and matter closure.

## Audit-aware repair path

Per `audit_ledger.json`, `notes_for_re_audit_if_any` for this row, the
audit-stated repair target is `compute_required` (i.e., the missing
top5/top6/top8 inward-source artifacts). The cache deposits in section
"Cached top5/top6/top8 inward-source artifacts (2026-05-10)" satisfy
that repair target literally; a re-audit pass picking up those cache
files should be able to verify the 2/4 inward-source totals at
`top_keep in {5, 6, 8}` by direct inspection.

This rigorization edit only sharpens the artifact register and
deposits the cache files; nothing here changes audit status.
