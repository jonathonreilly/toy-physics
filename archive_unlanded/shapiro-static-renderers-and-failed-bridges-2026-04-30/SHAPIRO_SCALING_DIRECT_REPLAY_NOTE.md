# Shapiro Scaling Direct Replay Note

**Date:** 2026-04-08  
**Status:** RETRACTED 2026-04-30 — audit failed; this note is archived under `archive_unlanded/shapiro-static-renderers-and-failed-bridges-2026-04-30/`. Claims below are NOT supported by current runners or current audit lane. See `## Retraction` section.

## Retraction

- **Date archived:** 2026-04-30
- **Archive directory:** `archive_unlanded/shapiro-static-renderers-and-failed-bridges-2026-04-30/` (the directory name encodes the failure reason: static renderers and failed bridges).
- **Audit verdict_rationale (quoted verbatim from `docs/audit/data/audit_ledger.json`):**

  > Issue: The direct replay script is a static data renderer whose s, b, and k laws are imported from SHAPIRO_EXPERIMENTAL_CARD.md, which is unaudited/unknown, and it also cites the failed Shapiro diamond frequency bridge. Why this blocks: freezing unaudited table entries is not a retained replay unless the source card is audit-clean or the runner recomputes the laws from raw inputs with zero-control checks. Repair target: audit SHAPIRO_EXPERIMENTAL_CARD.md or replace this with a runner that directly recomputes the s, b, and k scaling sweeps and asserts the source-off and instantaneous-field controls. Claim boundary until fixed: it is safe to say the script renders the stored scaling and portable-delay tables; it is not safe to claim retained Shapiro scaling-law closure from this row.

- **Do not cite warning:** Do NOT cite the numerical results, tables, or threshold values in the original content below as live framework claims. The runners referenced in this note have been superseded or are no longer reproducible at the time of audit. If a future investigation revisits this physics, treat it as starting from scratch rather than as continuation of a "closed no-go".

## Artifact Chain

- [`scripts/shapiro_scaling_direct_replay.py`](/Users/jonreilly/Projects/Physics/scripts/shapiro_scaling_direct_replay.py)
- [`scripts/shapiro_scaling_probe.py`](/Users/jonreilly/Projects/Physics/scripts/shapiro_scaling_probe.py)
- [`logs/2026-04-08-shapiro-scaling-direct-replay.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-08-shapiro-scaling-direct-replay.txt)
- [`docs/SHAPIRO_EXPERIMENTAL_CARD.md`](/Users/jonreilly/Projects/Physics/docs/SHAPIRO_EXPERIMENTAL_CARD.md)
- [`logs/2026-04-06-shapiro-delay-portable.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-shapiro-delay-portable.txt)
- [`docs/SHAPIRO_DIAMOND_FREQUENCY_BRIDGE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SHAPIRO_DIAMOND_FREQUENCY_BRIDGE_NOTE.md)

## What Is Being Replayed

This is not a reconstruction from the anchor commit. It is a direct freeze of
the retained in-repo data:

- `s` law from the experimental card
- `b` law from the experimental card
- `k` law from the experimental card
- exact zero controls from the experimental card and portable delay log

## Exact Controls

- `s = 0 -> phase = 0.000 rad`
- `c = inst -> phase = 0.000000 rad`
- `b` is not an exact-zero law; it is a monotone tail law that approaches
  zero at large separation

## Direct Scaling Laws

| law | control | direct readout | source |
| --- | --- | --- | --- |
| `phase ~ s^1.000` | `s = 0 -> phase = 0` | verified over `s = 0.001` to `0.016` | `docs/SHAPIRO_EXPERIMENTAL_CARD.md` |
| phase decreases with `b` | large `b -> phase -> 0` | `b = 3.0 -> +0.062 rad`; `b = 5.0 -> +0.049 rad`; `b = 7.0 -> +0.040 rad` | `docs/SHAPIRO_EXPERIMENTAL_CARD.md` |
| `phase ~ k` | instantaneous field -> phase = 0 | `k = 2.0 -> +0.030 rad`; `k = 5.0 -> +0.062 rad`; `k = 10.0 -> +0.200 rad` | `docs/SHAPIRO_EXPERIMENTAL_CARD.md` |

## Portable Delay Table

| c | fam1 | fam2 | fam3 | mean |
| ---: | ---: | ---: | ---: | ---: |
| inst | -0.000000 | +0.000000 | -0.000000 | +0.000000 |
| 2.00 | +0.040233 | +0.040431 | +0.040130 | +0.040265 |
| 1.00 | +0.050011 | +0.050325 | +0.049930 | +0.050089 |
| 0.50 | +0.061643 | +0.061958 | +0.061700 | +0.061767 |
| 0.25 | +0.067893 | +0.068326 | +0.067886 | +0.068035 |

## Narrow Read

- the source-mass law stays linear over the retained 16x sweep
- the impact-parameter law stays ordered on the retained sampled rows
- the chromatic law stays direct in the retained k table
- the exact zero controls survive in both the source-off and instantaneous-field gates
- the portable delay log keeps the zero control explicit while showing the finite-c phase table

## Final Verdict

**the Shapiro scaling lane can close as a direct data-bearing replay: the retained s, b, and k laws are frozen from repo data, and the exact zero controls remain explicit**
