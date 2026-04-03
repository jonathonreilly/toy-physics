# Mirror Mutual Information Note

**Date:** 2026-04-03  
**Status:** review-safe mirror MI comparison complete, bounded small-N support only

This note freezes the mirror-specific mutual-information question on the exact
linear mirror chokepoint family.

Script:
[`scripts/mirror_mutual_information.py`](/Users/jonreilly/Projects/Physics/scripts/mirror_mutual_information.py)

Log:
[`logs/2026-04-03-mirror-mutual-information.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-mirror-mutual-information.txt)

## Question

Does the exact mirror lane retain which-slit information more slowly than a
matched random chokepoint baseline, while staying on the same linear
propagator and the same slit/detector geometry?

## Setup

- families: exact mirror chokepoint, random chokepoint baseline
- `16` seeds
- `N = 15, 25, 40, 60, 80, 100`
- `npl_half = 25`
- `connect_radius = 4.0`
- `layer2_prob = 0.0`
- MI evaluated on the same exact linear propagator as the retained mirror pocket
- `k` band: `3, 5, 7`

## Retained Interpretation

The mirror MI lane is review-safe only as a bounded small-N comparison. The
exact mirror family does keep a higher MI than the matched random baseline at
`N = 15, 25`, and it remains usable at `N = 40`, but the comparison does not
extend cleanly to `N = 60+` in this harness.

## Narrow Read

- exact mirror is compared against a matched random baseline
- the output should be read jointly with the retained mirror chokepoint note
- the MI lane is bounded and small-N only in this harness
- do **not** generalize this to all mirror variants or to a retained large-N
  law without a new artifact chain

## Frozen Rows

Representative retained rows from the log:

| N | random MI | mirror MI | random pur_min | mirror pur_min |
|---|---:|---:|---:|---:|
| 15 | `0.853765` | `0.923088` | `0.5265` | `0.5107` |
| 25 | `0.470743` | `0.719153` | `0.6361` | `0.5492` |
| 40 | FAIL | `0.926967` | FAIL | `0.5022` |

Fit summary:

- mirror MI fit on the retained rows is effectively flat and not review-grade
- mirror purity depth fit is also effectively flat in this harness
- the main retained fact is the bounded small-N advantage, not a clean
  asymptotic law
