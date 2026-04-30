# Family Companion Compare Note

**Date:** 2026-04-06 (status line rephrased 2026-04-28 per audit-lane verdict)
**Status:** support / cross-family comparison card pointing to other notes for the fixed-companion weak-field law; static summary only, no audit-registered dependency chain, no runner that recomputes controls and `F~M` values.

## Artifact Chain

- [`scripts/FAMILY_COMPANION_COMPARE.py`](/Users/jonreilly/Projects/Physics/scripts/FAMILY_COMPANION_COMPARE.py)
- [`logs/2026-04-06-family-companion-compare.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-family-companion-compare.txt)
- retained source notes:
  - [`archive_unlanded/grown-transfer-stale-runners-2026-04-30/GROWN_TRANSFER_BASIN_NOTE.md`](/Users/jonreilly/Projects/Physics/archive_unlanded/grown-transfer-stale-runners-2026-04-30/GROWN_TRANSFER_BASIN_NOTE.md)
  - [`docs/ALT_CONNECTIVITY_FAMILY_BASIN_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ALT_CONNECTIVITY_FAMILY_BASIN_NOTE.md)
  - [`docs/SECOND_GROWN_FAMILY_COMPLEX_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SECOND_GROWN_FAMILY_COMPLEX_NOTE.md)

## Question

Do the retained grown-family, alternative connectivity family, and second-family slices share the same fixed-companion weak-field law at a review-safe level?

## Comparison

| family | slice | zero / neutral control | weak-field `F~M` | exact mismatch |
| --- | --- | --- | ---: | --- |
| Retained grown transfer basin | grown-row / nearby basin | exact zero-source and neutral same-point cancellation | `1.000` | none on the signed-source branch; companion gamma=0 baseline is exact |
| Alternative connectivity family | no-restore grown slice | exact zero-source and neutral same-point cancellation | `0.999994` | complex-action crossover fails on this slice; sign-law stays intact |
| Second grown-family complex | no-restore geometry-sector slice | not the active observable; gamma=0 baseline is exact | `1.000` | this branch is not on the same zero/neutral signed-source surface; it is compared by gamma=0 baseline plus crossover |

## Safe Read

- the retained grown basin preserves exact zero-source / neutral cancellation and stays at `F~M = 1.000` on the checked companion surface
- the alternative connectivity family also preserves exact zero / neutral controls and keeps weak-field `F~M` at `0.999994` across the full tested drift sweep
- the second-family complex anchor keeps `F~M = 1.000`, but its comparison surface is `gamma = 0` baseline plus crossover rather than the same zero / neutral signed-source surface

## Exact Mismatch

- the sign-law families share the same zero / neutral control surface
- the second-family complex lane does not: it is a complex-action branch, so the nearest analogue is `gamma = 0` baseline rather than zero-source cancellation
- that means the shared result is the weak-field law, not a universal identity of all controls

## Final Verdict

**retained narrow comparison positive: shared weak-field linearity, with control-surface mismatch isolated rather than averaged away**

## Audit boundary (2026-04-28)

Audit verdict (`audited_conditional`, leaf criticality):

> Issue: the retained cross-family comparison rests on a static
> summary of source notes, not on an audit-registered dependency
> chain or a runner that recomputes the controls and F~M values.
> Why this blocks: a hostile referee cannot accept a retained
> shared-law claim while two cited families are still unaudited
> proposed_retained and the second-family complex branch is
> compared by gamma=0/crossover rather than the same zero/neutral
> signed-source observable.

The note has been re-tiered to `support` (cross-family comparison
card).

## What this note does NOT claim

- A retained shared-law theorem.
- That the cited families are audit-clean dependencies.
- That the second-family complex branch was compared on the same
  zero/neutral signed-source observable.

## What would close this lane (Path A future work)

A retained shared-law theorem would require auditing or registering
the cited grown-transfer / second-family / connected-family
authorities, plus a runner that recomputes controls and `F~M`
values on the same signed-source observable.
