# Wave Direct-dM H=0.25 Two-Point Synthesis Note

**Date:** 2026-04-08
**Status:** bounded narrow synthesis on the controlled first fine-`H` `Fam1` pair
**Claim type:** bounded_theorem

**Review repair perimeter (judicial review, post-2026-04-30 generated-audit context):**
Generated-audit context identified this chain-closure blocker: "the note depends on a missing artifact-chain provenance and
the current runner did not complete under the audit timeout, so the
numerical synthesis is conditional rather than independently closed.
The selected H=0.25 values can remain a reported narrow synthesis,
not an audit-clean numerical theorem." This rigorization edit only
sharpens the boundary of the repair perimeter; nothing here
promotes audit status. The runner registered for this note is
[`scripts/wave_direct_dm_h025_point_runner.py`](../scripts/wave_direct_dm_h025_point_runner.py)
(see `docs/audit/data/runner_classification.json`); its current
runner cache is at
[`logs/runner-cache/wave_direct_dm_h025_point_runner.txt`](../logs/runner-cache/wave_direct_dm_h025_point_runner.txt)
and reports `status: ok`, `elapsed_sec: 141.13`,
`timeout_sec: 1800` (the runner declares `AUDIT_TIMEOUT_SEC = 1800`,
so the audit-lane precompute now allows the full Fam1/seed=0 row to
complete rather than hitting the 120 s default ceiling that drove
the original `runner did not complete under the audit timeout`
flag). The cited authority chain is registered explicitly in
"Cited authority chain (2026-05-10)" below.

This note freezes the first honest fine-`H` claim surface for the
direct-`dM` matched-schedule lane:

> Start from the retained direct-`dM` portability batch plus the seed-band
> diagnosis, then compare exactly the two planned `H = 0.25` `Fam1`,
> `S = 0.004` replays (`seed = 0`, `1`) before widening into any broader
> family, seed, or strength batch.

## Fine-`H` pair

| seed | dM(early) | dM(late) | delta_hist | R_hist | late gain |
| ---: | ---: | ---: | ---: | ---: | ---: |
| `0` | `+0.004989` | `+0.006246` | `-0.001256` | `-20.12%` | `+0.001257` |
| `1` | `+0.004411` | `+0.006255` | `-0.001843` | `-29.47%` | `+0.001844` |

Control-ladder summaries:

| seed | null max `|delta_hist|` | sign pattern | `|delta_hist / s|` spread |
| ---: | ---: | --- | ---: |
| `0` | `0.000e+00` | `- - -` | `7.77%` |
| `1` | `0.000e+00` | `- - -` | `5.22%` |

## Coarse-to-fine comparison

| seed | coarse-`H` `R_hist` band (`0.5`, `0.35`) | `H = 0.25` `R_hist` | coarse-`H` late-gain band | `H = 0.25` late gain | read |
| ---: | ---: | ---: | ---: | ---: | --- |
| `0` | `-43.59%`, `-42.36%` | `-20.12%` | `+0.004162`, `+0.003535` | `+0.001257` | old high band closes |
| `1` | `-25.33%`, `-19.98%` | `-29.47%` | `+0.001897`, `+0.001625` | `+0.001844` | low band retains |

## Headline read

- Both seeds keep exact null, common negative sign, and bounded
  weak-field linearity at `H = 0.25`, so the first-family fine-`H` pair is
  now controlled rather than one-strength.
- The old coarse-`H` seed ordering is **not** refinement-stable:
  at `H = 0.25`, the seed-`1` row is now the stronger of the two.
- The flip is driven by uneven late-gain compression:
  seed `0` loses most of its extra late-branch gain, while seed `1` stays
  close to its old lower-band late-gain level.
- This is not an absolute-response continuation:
  both fine-`H` rows shift downward in raw `dM(early)` / `dM(late)` compared
  with the larger coarse-`H` values, so the stable feature is the sign plus
  the late-minus-early separation, not a frozen amplitude package.

So the narrow promotion rule is:

> On the current controlled `Fam1` fine-`H` pair, the
> direct-`dM` matched-history effect survives in sign on both seeds, but the
> old coarse-`H` seed ordering is not refinement-stable. Seed `1` retains the
> lower-magnitude branch at `R_hist = -29.47%`, while seed `0` collapses to a
> boundary at `R_hist = -20.12%` because its extra late-branch gain compresses
> sharply. This is a controlled single-family cross-seed reordering / uneven
> late-gain-compression result, not an `H = 0.25` portability extension.

## What this does not support

- not an `H = 0.25` portability batch
- not a family-wide fine-`H` seed law
- not a refinement-stable amplitude package
- not a weaker-strength or third-seed rule yet

## Next honest move

- Keep the existing direct-`dM` base fixed:
  matched-history note, bounded family scout, `H = 0.25` feasibility note,
  and bounded portability batch.
- The second-family pair is already controlled in
  `WAVE_DIRECT_DM_H025_FAM2_TWO_POINT_SYNTHESIS_NOTE.md`.
- If the lane continues next, the honest move is now a narrow controlled
  `Fam1`/`Fam2` family-pair synthesis before any `Fam3`, third-seed, or
  weaker-strength reserve point.
- Keep comparator work demoted unless a materially different exact
  `c = infinity` construction appears.

## Artifact chain

- `docs/WAVE_DIRECT_DM_SEED_BAND_DIAGNOSIS_NOTE.md`
- `docs/WAVE_DIRECT_DM_H025_FEASIBILITY_NOTE.md`
- `docs/WAVE_DIRECT_DM_H025_HIGH_BAND_BOUNDARY_NOTE.md`
- `docs/WAVE_DIRECT_DM_H025_LOW_BAND_RETENTION_NOTE.md`
- `docs/WAVE_DIRECT_DM_H025_FAM1_SEED0_CONTROL_NOTE.md`
- `docs/WAVE_DIRECT_DM_H025_FAM1_SEED1_CONTROL_NOTE.md`
- `docs/WAVE_DIRECT_DM_H025_FAM2_SEED0_BOUNDARY_NOTE.md`
- `docs/WAVE_DIRECT_DM_H025_FAM2_SEED1_FOLLOWUP_NOTE.md`
- `docs/WAVE_DIRECT_DM_H025_FAM2_TWO_POINT_SYNTHESIS_NOTE.md`
- `docs/WAVE_DIRECT_DM_PORTABILITY_BATCH_NOTE.md`
- [`scripts/wave_direct_dm_h025_point_runner.py`](../scripts/wave_direct_dm_h025_point_runner.py)
- [`logs/2026-04-08-wave-direct-dm-h025-control-fam1-seed0.txt`](../logs/2026-04-08-wave-direct-dm-h025-control-fam1-seed0.txt)
- [`logs/2026-04-08-wave-direct-dm-h025-control-fam1-seed1.txt`](../logs/2026-04-08-wave-direct-dm-h025-control-fam1-seed1.txt)
- [`logs/2026-04-08-wave-direct-dm-h025-high-band.txt`](../logs/2026-04-08-wave-direct-dm-h025-high-band.txt)
- [`logs/2026-04-08-wave-direct-dm-h025-low-band.txt`](../logs/2026-04-08-wave-direct-dm-h025-low-band.txt)

## Cited authority chain (2026-05-10)

The judicial-review verdict (cited at top) flagged `missing
artifact-chain provenance` and a `runner did not complete under the
audit timeout` issue. The cited-authority chain on this row is
registered explicitly below so the audit-graph one-hop edges from
the synthesis to its load-bearing inputs are visible in the source
note. Each numerical row in the headline tables is sourced from one
of these authorities; the synthesis itself does not introduce new
numerical claims beyond aggregation.

| Cited authority | File / log | Provenance role | Audit-lane state (2026-05-10) |
|---|---|---|---|
| Active runner | [`scripts/wave_direct_dm_h025_point_runner.py`](../scripts/wave_direct_dm_h025_point_runner.py) | declares `AUDIT_TIMEOUT_SEC = 1800`; produces the single-point Fam1/seed=0 row used in the headline H=0.25 dM(early)/dM(late)/delta_hist values | runner cache regenerated (`status: ok`, `elapsed_sec: 141.13`); see [`logs/runner-cache/wave_direct_dm_h025_point_runner.txt`](../logs/runner-cache/wave_direct_dm_h025_point_runner.txt) |
| Frozen seed=0 control log | [`logs/2026-04-08-wave-direct-dm-h025-control-fam1-seed0.txt`](../logs/2026-04-08-wave-direct-dm-h025-control-fam1-seed0.txt) | preserves the seed=0 Fam1 single-point row that anchors the `dM(early)=+0.004989`, `dM(late)=+0.006246`, `delta_hist=-0.001256`, `R_hist=-20.12%` table entry | frozen log; matches active runner cache |
| Frozen seed=1 control log | [`logs/2026-04-08-wave-direct-dm-h025-control-fam1-seed1.txt`](../logs/2026-04-08-wave-direct-dm-h025-control-fam1-seed1.txt) | preserves the seed=1 Fam1 single-point row that anchors the `dM(early)=+0.004411`, `dM(late)=+0.006255`, `delta_hist=-0.001843`, `R_hist=-29.47%` table entry | frozen log |
| Coarse-`H` seed band log (high) | [`logs/2026-04-08-wave-direct-dm-h025-high-band.txt`](../logs/2026-04-08-wave-direct-dm-h025-high-band.txt) | preserves the coarse-`H` `R_hist` band rows (`-43.59%`, `-42.36%` at seed=0; `-25.33%` at seed=1) cited in the coarse-to-fine comparison table | frozen log |
| Coarse-`H` seed band log (low) | [`logs/2026-04-08-wave-direct-dm-h025-low-band.txt`](../logs/2026-04-08-wave-direct-dm-h025-low-band.txt) | preserves the coarse-`H` low-band rows (`-19.98%` at seed=1) cited in the coarse-to-fine comparison table | frozen log |
| Fam1 seed=0 control note | [`WAVE_DIRECT_DM_H025_FAM1_SEED0_CONTROL_NOTE.md`](WAVE_DIRECT_DM_H025_FAM1_SEED0_CONTROL_NOTE.md) | one-hop dependency row covering the seed=0 control-ladder summary (null `0.000e+00`, sign pattern `- - -`, spread `7.77%`) | source-note dependency |
| Fam1 seed=1 control note | [`WAVE_DIRECT_DM_H025_FAM1_SEED1_CONTROL_NOTE.md`](WAVE_DIRECT_DM_H025_FAM1_SEED1_CONTROL_NOTE.md) | one-hop dependency row covering the seed=1 control-ladder summary (null `0.000e+00`, sign pattern `- - -`, spread `5.22%`) | source-note dependency |
| Fam2 two-point synthesis (controlled second-family pair) | [`WAVE_DIRECT_DM_H025_FAM2_TWO_POINT_SYNTHESIS_NOTE.md`](WAVE_DIRECT_DM_H025_FAM2_TWO_POINT_SYNTHESIS_NOTE.md) | parallel second-family controlled pair referenced in "Next honest move"; not load-bearing for the Fam1 headline | parallel-family register |
| Cache contract | [`scripts/runner_cache.py`](../scripts/runner_cache.py) | declares the cache header format, the `AUDIT_TIMEOUT_SEC` declaration mechanism, and the SHA-pinned cache regeneration that addresses the audit-stated timeout flag | infrastructure |

The narrow promotion rule and the headline reads remain unchanged:
this synthesis aggregates two predeclared single-point Fam1 rows
plus two control-ladder summaries, and explicitly disclaims (a) an
H=0.25 portability batch, (b) a family-wide fine-`H` seed law,
(c) a refinement-stable amplitude package, and (d) a weaker-strength
or third-seed rule. The review repair perimeter is exactly the
narrow-synthesis status of this aggregation. This rigorization edit
only sharpens the conditional perimeter and registers the cited
authority chain; it does not set audit status, hand-author audit
JSON, or expand the synthesis scope beyond the controlled
single-family pair.
