# Mirror Chokepoint Note

**Date:** 2026-04-03 (downgraded 2026-04-28 per audit-lane verdict; narrowed 2026-05-09 per audit_failed re-flag; load-bearing artifacts re-cited at the top 2026-05-10 per audit `runner_artifact_issue` repair target).
**Status:** bounded finite mirror chokepoint diagnostic on the strict default `NPL_HALF=25` `connect_radius=4.0` card at `N=15` and `N=25` only; not a single-surface family theorem and not an asymptotic claim. The dense `NPL_HALF=60` `connect_radius=5.0` boundary card retention through `N=100` is covered by the separate retained boundary-fit note (see [`docs/MIRROR_CHOKEPOINT_BOUNDARY_FIT_NOTE.md`](MIRROR_CHOKEPOINT_BOUNDARY_FIT_NOTE.md)) and is not part of this note's retained scope.
**Claim type:** bounded_theorem

**Primary runner (load-bearing):** [`scripts/mirror_chokepoint_joint.py`](../scripts/mirror_chokepoint_joint.py) — registered strict-default scan runner for the `NPL_HALF=25, connect_radius=4.0, layer2_prob=0.0` card.
**Primary runner registered cache (load-bearing):** [`logs/runner-cache/mirror_chokepoint_joint.txt`](../logs/runner-cache/mirror_chokepoint_joint.txt) — registered cached stdout (`exit_code=0`, `status=ok`) from which the bounded `N=15`/`N=25` rows below are read directly, and which records `FAIL` for `N=40, 60, 80, 100` on this card.
**Certificate runner (load-bearing):** [`scripts/mirror_chokepoint_note_certificate_runner_2026_05_09.py`](../scripts/mirror_chokepoint_note_certificate_runner_2026_05_09.py) — registered assertion-gated certificate runner that mechanically verifies the bounded `N=15`/`N=25` table values against the strict joint cache, the strict-card header (`NPL_HALF=25`, `k=5.0`, 16 seeds), and the `N=40/60/80/100` FAIL markers; exits zero on PASS.
**Certificate runner registered cache (load-bearing):** [`logs/runner-cache/mirror_chokepoint_note_certificate_runner_2026_05_09.txt`](../logs/runner-cache/mirror_chokepoint_note_certificate_runner_2026_05_09.txt) — registered cached stdout (`exit_code=0`, `status=ok`) showing `PASS=5/5` for the certificate.

This note freezes the current review-safe mirror result on the strict
chokepoint family. All four artifacts above (primary runner source +
cache, certificate runner source + cache) are load-bearing one-hop
dependencies and are present in the worktree as registered files.

Historical exploratory log files (`logs/2026-04-03-mirror-chokepoint-*`) are
not part of the retained provenance for this note and are not relied upon
here. The dense `NPL_HALF=60` boundary card has its own registered
runner-cache (`logs/runner-cache/mirror_chokepoint_boundary_fit_certificate.txt`)
and is the scope of the separate boundary-fit note linked above.

## Setup

- strict layer-1 chokepoint connectivity
- `NPL_HALF = 25` (`50` total nodes per layer)
- `connect_radius = 4.0`
- `layer2_prob = 0.0`
- `k = 5.0`
- `16` seeds
- this note's retained scope: `N = 15, 25` only (default strict card)

## Retained Rows

This note's retained scope, after the 2026-05-09 narrowing, is the **default
strict card only**: `NPL_HALF=25`, `connect_radius=4.0`, `layer2_prob=0.0`,
16 seeds, and only at `N = 15` and `N = 25`. The dense `NPL_HALF=60`,
`connect_radius=5.0` boundary card retention through `N=100` is the scope of
the separate retained boundary-fit certificate
([`docs/MIRROR_CHOKEPOINT_BOUNDARY_FIT_NOTE.md`](MIRROR_CHOKEPOINT_BOUNDARY_FIT_NOTE.md))
and is not stitched into this note's retained table.

The retained rows below are read directly from one runner-cache artifact:

- `logs/runner-cache/mirror_chokepoint_joint.txt` — strict default card
  (`NPL_HALF=25`, `connect_radius=4.0`, `layer2_prob=0.0`, 16 seeds). The
  numbers below match this cache exactly.

The assertion-gated certificate runner that mechanically verifies these two
rows against the cache lives at:

- [`scripts/mirror_chokepoint_note_certificate_runner_2026_05_09.py`](../scripts/mirror_chokepoint_note_certificate_runner_2026_05_09.py)
  — exits zero on PASS, nonzero if the cache is missing or any retained
  row drifts from the cache.

| N | `d_TV` | `pur_cl` | `S_norm` | gravity | Born `|I3|/P` | `k=0` | seeds_ok | parameter card | runner-cache artifact |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| 15 | `0.9716` | `0.5769±0.02` | `1.0006` | `+1.2927±0.691` | `5.75e-16` | `0.00e+00` | `11/16` | `NPL_HALF=25`, `connect_radius=4.0`, `layer2_prob=0.0` | `logs/runner-cache/mirror_chokepoint_joint.txt` |
| 25 | `0.8014` | `0.7329±0.05` | `0.9986` | `+2.2748±0.525` | `6.92e-16` | `0.00e+00` | `13/16` | `NPL_HALF=25`, `connect_radius=4.0`, `layer2_prob=0.0` | `logs/runner-cache/mirror_chokepoint_joint.txt` |

The strict default runner-cache also records `FAIL` for `N = 40, 60, 80, 100`
on this card; those rows are out of this note's retained scope and are
explicitly NOT claimed here. The dense-card retention story for
`N = 40..100` is the scope of the boundary-fit note linked above.

The exploratory `NPL_HALF = 50` scaling probe and the sparse same-side
layer-2 rescue (`layer2_prob = 0.02`) are also out-of-scope — no
runner-cache artifact is presently checked in for those surfaces.

## Out-of-scope (historical exploratory surfaces)

The following surfaces are **out-of-scope for this note's bounded claim**
and have no runner-cache artifact in the repo. They are listed here only
to record what is excluded; no number from any of them is relied upon in
this note:

- `NPL_HALF=25`, `connect_radius=4.0`, `N=40, 60, 80, 100` — these rows
  FAIL on the strict default runner-cache and are explicitly not in the
  retained table.
- `NPL_HALF=50` scaling probe (any `N`).
- `NPL_HALF=55` boundary scan (any `connect_radius`, any `N`).
- Sparse same-side layer-2 rescue (`layer2_prob = 0.02`, any `N`).
- `NPL_HALF=60`, `connect_radius=5.0` boundary card at `N = 40, 60, 80,
  100, 120` — this dense card has its own runner-cache and is the scope
  of [`docs/MIRROR_CHOKEPOINT_BOUNDARY_FIT_NOTE.md`](MIRROR_CHOKEPOINT_BOUNDARY_FIT_NOTE.md).

## Narrow Read

- The mirror chokepoint lane is **real as a bounded pocket** at small `N`
  on the strict default card.
- It is Born-clean at machine precision on the retained `N=15` and `N=25`
  rows.
- It keeps a strong decoherence-side advantage at `N=15` and `N=25` on the
  strict default card.
- It also keeps positive gravity and the `k=0` control at zero on the
  retained rows.
- The strict default card does **not** retain `N=40, 60, 80, 100` (those
  fall to FAIL on the same card); the dense-card retention story is
  separately certified in the boundary-fit note and is **not** stitched
  into this note's retained table.
- The sparse layer-2 rescue is exploratory only and is not part of any
  retained scope here.

## Interpretation

The current safe statement, narrowed to this note's retained scope, is:

- **retained bounded mirror pocket on the strict default card:** yes, at
  `N=15` and `N=25`
- **strict default card large-N retention:** no — `N=40, 60, 80, 100`
  FAIL on this card per the registered runner-cache
- **dense-card retention through `N=100`:** out-of-scope here; covered by
  the separate retained boundary-fit certificate
- **strict `NPL_HALF = 50` scaling probe:** out-of-scope (no runner-cache
  artifact)
- **sparse same-side layer-2 rescue (`layer2_prob = 0.02`):** out-of-scope
  (no runner-cache artifact)

The dense large-`N` boundary extension is the scope of the separate
boundary-fit note and is reproducible directly from the live script with:

`python3 scripts/mirror_chokepoint_joint.py --npl-half 60 --connect-radius 5.0 --n-layers 40 60 80 100 120 --layer2-prob 0.0`

For review-hardening, the fast canonical regression gate keeps the strict
baseline check separate from that slower replay; use
[`scripts/canonical_regression_gate.py --slow`](/Users/jonreilly/Projects/Physics/scripts/canonical_regression_gate.py)
when you want both.

For the canonical fixed-family decoherence fit on the bounded dense boundary
mirror pocket, see:

[`docs/MIRROR_CHOKEPOINT_BOUNDARY_FIT_NOTE.md`](MIRROR_CHOKEPOINT_BOUNDARY_FIT_NOTE.md)

## Audit boundary (2026-05-10 — load-bearing artifacts re-cited at the top)

This revision addresses the generated-audit repair target:

> runner_artifact_issue — supply logs/runner-cache/mirror_chokepoint_joint.txt,
> scripts/mirror_chokepoint_note_certificate_runner_2026_05_09.py, and its
> cached PASS stdout as the direct runner artifacts for re-audit.

All four load-bearing artifacts are present in the repo (registered with
SHA-pinned `logs/runner-cache/` caches) and were already cited in the
"Registered runner artifacts" section. This revision lifts them into the
note header so the audit packet construction can pick them up as direct
one-hop registered dependencies without scrolling. The bounded-row
content is unchanged. The note is already as narrow as the certificate
runner enforces (`N=15`/`N=25` mirror p2=0 only on the strict default
card, with `N=40/60/80/100` explicitly recorded FAIL).

## Audit boundary (2026-04-28; re-narrowed 2026-05-09)

Audit verdict (`audited_conditional`, leaf criticality, 2026-04-28):

> Issue: the finite mirror-chokepoint pocket is partly reproducible, but
> the proposed-retained packet depends on a stitched table whose `N=40`/
> `N=60` values are not recovered by the strict `NPL_HALF=25` `radius=4.0`
> baseline or by `NPL_HALF=25` `radius=5.0`, and several cited log files
> for the joint, scaling, sparse-rescue, and boundary scans are missing.

> Why this blocks: a hostile auditor can verify `N=15`/`N=25` on the
> strict baseline and the dense `NPL_HALF=60` `radius=5.0`
> `N=40/60/80/100` positive-gravity window with `N=120` collapse, but
> cannot certify the exact retained table or the through-`N=100`
> retention story as a single closed claim without knowing which archived
> parameter surface supports each row and without assertion-gated
> retention criteria.

Re-flag verdict (`audited_failed`, 2026-05-08):

> Issue: the current note claims a specific retained stitched table, but
> the provided strict runner only recovers N=15/N=25 and the cited dense
> boundary authority gives different N=40/N=60 values than the table in
> this note. Repair target: land a per-row certificate or update the
> retained table so every row matches the named runner-cache artifact.
> Claim boundary until fixed: only the strict `N=15`/`N=25` rows and the
> separate retained_bounded dense boundary-card result can be cited, not
> this exact stitched retained table.

The 2026-05-09 narrowing applies the auditor's "narrow the note to cite
only the default `N=15/25` rows and the retained boundary-fit card" path:

- The retained table is now `N=15`/`N=25` only on the strict default card.
- The Born values match the strict joint runner-cache exactly
  (`5.75e-16`, `6.92e-16`).
- The dense `NPL_HALF=60` boundary card retention through `N=100` is
  delegated to the separately-retained boundary-fit certificate note and
  is no longer stitched into this note.
- An assertion-gated certificate runner
  (`scripts/mirror_chokepoint_note_certificate_runner_2026_05_09.py`)
  exits zero on PASS and nonzero if the retained rows drift from the
  cache.

## What this note does NOT claim

- A single-parameter-surface mirror chokepoint family theorem.
- A clean asymptotic retention law on the strict default card —
  `N=40, 60, 80, 100` FAIL on this card per the registered runner-cache.
- A through-`N=100` retention story on this note. The dense
  `NPL_HALF=60`, `connect_radius=5.0` boundary card retention through
  `N=100` is the scope of the separately retained boundary-fit
  certificate
  ([`docs/MIRROR_CHOKEPOINT_BOUNDARY_FIT_NOTE.md`](MIRROR_CHOKEPOINT_BOUNDARY_FIT_NOTE.md))
  and is not stitched into this note's retained table.
- That the `NPL_HALF=50` scaling probe, the `NPL_HALF=55` boundary
  scans, or the sparse layer-2 rescue (`layer2_prob = 0.02`) are part
  of any retained provenance here — no runner-cache artifact is
  presently checked in for those surfaces.

## What would close this lane (Path A future work)

A future worker pursuing reinstatement of a clean mirror chokepoint
family claim that goes beyond this note's narrow `N=15/25` strict-card
scope would need to land at least one of the following:

1. A single registered runner invocation that reproduces a per-row
   table on a single parameter surface (no stitching), with the
   canonical command line and per-row pass/fail gates registered in
   the note and a runner-cache artifact present.
2. A reconciliation between the strict `NPL_HALF=25` baseline (where
   `N=40, 60, 80, 100` FAIL) and the dense `NPL_HALF=60` boundary card
   (where they retain through `N=100`) as a single-surface theorem or
   as an explicit cross-card diagnostic with assertion-gated runners
   on both surfaces.
3. Hard runner-side pass/fail gates for seed counts, `NPL_HALF`,
   `connect_radius`, `layer2_prob`, Born tolerance, `k=0`,
   gravity positivity/significance, decoherence ceiling, and any
   collapse boundary (e.g. the `N=120` zero-gravity row on the dense
   card).

## Registered runner artifacts

The runner sources and cached stdout backing the `N=15`/`N=25` rows are
present in the worktree:

- Strict default scan runner: `scripts/mirror_chokepoint_joint.py` (registered
  source for the `NPL_HALF=25, connect_radius=4.0, layer2_prob=0.0` card).
- Strict default scan cache: `logs/runner-cache/mirror_chokepoint_joint.txt`
  (registered cached stdout from which the retained `N=15`/`N=25` rows above
  are read directly).
- Assertion-gated certificate runner:
  `scripts/mirror_chokepoint_note_certificate_runner_2026_05_09.py`
  (mechanically verifies the retained rows against the strict scan cache).
- Certificate runner cache:
  `logs/runner-cache/mirror_chokepoint_note_certificate_runner_2026_05_09.txt`
  (registered cached stdout from the certificate runner; PASS exit zero).

Both runners are in-tree; their caches are present in `logs/runner-cache/`.
This block records the exact registered runner sources and cached stdout.
