# Exact 2D Mirror Validation Note

**Date:** 2026-04-03 (registered-dependency citation tightened 2026-05-10 per audit `missing_dependency_edge` repair target).
**Status:** bounded review-safe exact 2D mirror coexistence pocket; no gravity-law promotion.
**Claim type:** bounded_theorem
**Primary runner (load-bearing):** [`scripts/mirror_2d_validation.py`](../scripts/mirror_2d_validation.py) (2D exact mirror linear propagator on three-slit Sorkin).
**Primary runner cache (load-bearing):** [`logs/runner-cache/mirror_2d_validation.txt`](../logs/runner-cache/mirror_2d_validation.txt) — registered cached stdout (`exit_code=0`, `status=ok`) backing every row in the bounded table below.
**Imported authority (load-bearing dependency):** [`scripts/mirror_born_audit.py`](../scripts/mirror_born_audit.py) — provides `gen_2d_mirror` (exact 2D mirror generator) and `propagate_LINEAR` (strictly linear propagator) imported by the primary runner.
**Imported authority cache (load-bearing dependency):** [`logs/runner-cache/mirror_born_audit.txt`](../logs/runner-cache/mirror_born_audit.txt) — registered cached stdout (`exit_code=0`, `status=ok`) verifying the imported generator and propagator on the strict mirror Born family.

This note freezes the exact 2D mirror validation lane. Both the primary
runner and the imported `mirror_born_audit.py` authority are recorded as
direct registered dependencies (one-hop), so the load-bearing exact-2D
mirror generator and linear propagator can be verified from the supplied
audit packet without delegating to a non-registered companion script.

Log:
[`logs/2026-04-03-mirror-2d-validation.txt`](../logs/2026-04-03-mirror-2d-validation.txt)

The exact 2D family uses the strict linear propagator only. Born safety is
verified on the same family via the corrected three-slit Sorkin audit.

## Setup

- exact 2D mirror generator from `scripts/mirror_born_audit.py`
- `npl_half = 12` (`24` total nodes per layer)
- `yr = 10.0`
- `connect_radius = 2.5`
- `8` seeds
- `k`-band: `[3, 5, 7]`
- `N = 25, 40, 60, 80, 100`

## Retained Rows

The exact 2D mirror family is Born-clean and retains a strong bounded joint
coexistence pocket. The strongest retained row is `N = 60`.

| N | `MI` | `1-pur_min` | `d_TV` | gravity | Born `|I3|/P` | `k=0` |
|---|---:|---:|---:|---:|---:|---:|
| 25 | `0.502150` | `0.3029` | `0.6002` | `+2.7134` | `5.34e-16` | `0.00e+00` |
| 40 | `0.536689` | `0.3012` | `0.6217` | `+3.8891` | `7.75e-16` | `0.00e+00` |
| 60 | `0.756118` | `0.4420` | `0.8572` | `+2.5687` | `1.08e-15` | `0.00e+00` |
| 80 | `0.565264` | `0.3465` | `0.6740` | `+3.4065` | `2.60e-15` | `0.00e+00` |
| 100 | `0.346218` | `0.2865` | `0.5459` | `+1.8627` | `1.89e-15` | `0.00e+00` |

For comparison, the matched random chokepoint baseline at `N = 60` is much
weaker:

- `MI = 0.050745`
- `1 - pur_min = 0.0596`
- `d_TV = 0.1090`
- gravity `+0.7867`

So the exact 2D mirror family preserves substantially more which-slit
information and decoherence structure than the matched random baseline.

## Gravity Follow-Up

The same family was probed for a narrow gravity-side mass window and a
distance tail. Those fits are positive but not clean enough to promote as a
law.

### Fixed-Anchor Mass Window

- fit:
  - `delta ~= 0.8720 * M^0.132`
  - `R^2 = 0.167`

### Distance Sweep

- tail fit:
  - `delta ~= 0.3418 * b^0.320`
  - `R^2 = 0.075`

### Narrow read

- the exact 2D mirror family is review-safe for Born, MI, decoherence, and a
  positive gravity read
- the gravity-side fit quality is weak, so no mass-law or distance-law claim
  is promoted here
- the best retained statement is a **bounded exact 2D mirror coexistence
  pocket**, strongest at `N = 60`

## What this note does NOT claim

- A promoted 2D mirror gravity law (mass or distance).
- That the bounded coexistence pocket holds beyond the retained sweep
  `N ∈ {25, 40, 60, 80, 100}` at the stated parameter card.
- Any conclusion that depends on a non-registered companion script; the
  load-bearing computation closes from the primary runner cache plus the
  registered imported-authority cache (`mirror_born_audit.py`).

## Audit boundary (2026-05-10 — registered-dependency citation tightened)

This revision addresses the generated-audit repair target:

> missing_dependency_edge — add scripts/mirror_born_audit.py and its cached
> stdout as a direct audited dependency for this claim, then re-audit the
> bounded runner-backed pocket.

This revision lifts `scripts/mirror_born_audit.py` and its registered cache
`logs/runner-cache/mirror_born_audit.txt` into the note header as direct
load-bearing dependencies, so the audit packet has both one-hop authorities
on hand: the primary runner cache for the table rows, and the imported
generator/propagator cache for the exact-mirror linear-propagator premise.
The bounded-row table itself is unchanged.

## Registered runner artifacts

The 2D mirror validation lane uses the exact 2D mirror generator and linear
propagator from a registered companion script. Both runner sources and both
caches are present in the worktree as direct one-hop dependencies:

- Primary runner: `scripts/mirror_2d_validation.py` (registered runner whose
  cached stdout backs every bounded row in this note's table).
- Primary runner cache: `logs/runner-cache/mirror_2d_validation.txt`
  (registered cached stdout; `exit_code=0`, `status=ok`).
- Imported generator/propagator authority: `scripts/mirror_born_audit.py`
  (provides `gen_2d_mirror` and `propagate_LINEAR`, imported by the primary
  runner — load-bearing for the exact-2D mirror linear-propagator premise).
- Imported authority cache: `logs/runner-cache/mirror_born_audit.txt`
  (registered cached stdout; `exit_code=0`, `status=ok`).

Both authorities are registered in `logs/runner-cache/`. The bounded table
rows close from the primary runner cache; the exact-2D-mirror linear-
propagator premise closes from the imported-authority cache.
