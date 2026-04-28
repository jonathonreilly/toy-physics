# Mirror Mutual Information Chokepoint Note

**Date:** 2026-04-03 (downgraded 2026-04-28 per audit-lane verdict)
**Status:** bounded finite mid-N exact-mirror MI diagnostic on a single dense chokepoint parameter card. Not a clean asymptotic theorem; not a whole-window mirror MI advantage.

This note freezes the mirror-specific mutual-information diagnostic on a
single dense exact-mirror chokepoint parameter card, using the same linear
propagator and same slit/detector geometry as the bounded mirror chokepoint
pocket. The audit-lane verdict (`audited_conditional`,
[`docs/MIRROR_CHOKEPOINT_NOTE.md`](MIRROR_CHOKEPOINT_NOTE.md) is itself the
upstream conditional family) restricts the safe reading to a finite N
diagnostic at the named parameter card; the canonical retained line has been
narrowed to match.

Script:
[`scripts/mirror_mutual_information_chokepoint.py`](/Users/jonreilly/Projects/Physics/scripts/mirror_mutual_information_chokepoint.py)

Log:
[`logs/2026-04-03-mirror-mutual-information-chokepoint-n60-r5p0.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-mirror-mutual-information-chokepoint-n60-r5p0.txt)

## Question

Does the exact mirror chokepoint family retain which-slit information more
strongly than a matched random chokepoint baseline, and if so, does that hold
cleanly enough to support an asymptotic law?

## Setup

- families: exact mirror chokepoint, matched random chokepoint baseline
- `16` seeds
- `N = 40, 60, 80, 100`
- `npl_half = 60` (`120` total nodes per layer for the mirror family)
- `connect_radius = 5.0`
- `layer2_prob = 0.0`
- MI evaluated on the same exact linear propagator as the retained mirror pocket
- `k = 5.0`

## Retained Rows

The exact mirror family keeps a clear mid-N MI advantage over the matched
random baseline, but the comparison is not monotone and does not support a
clean slower-decay theorem:

| N | random MI | mirror MI | random pur_cl | mirror pur_cl |
|---|---:|---:|---:|---:|
| 40 | `0.1774±0.034` | `0.4295±0.068` | `0.8368±0.04` | `0.8608±0.03` |
| 60 | `0.0846±0.032` | `0.1973±0.041` | `0.8928±0.03` | `0.8440±0.03` |
| 80 | `0.0564±0.018` | `0.1385±0.021` | `0.9509±0.02` | `0.8182±0.03` |
| 100 | `0.0574±0.021` | `0.0408±0.011` | `0.9188±0.03` | `0.9043±0.02` |

## Descriptive Fits

These fits summarize the retained window, but they are not a clean asymptotic
law:

```text
mirror MI      ~= 2973.2137 × N^(-2.363)   R²=0.909
random MI      ~= 19.3325 × N^(-1.299)     R²=0.918
mirror 1-pur   ~= 0.3906 × N^(-0.246)      R²=0.126
random 1-pur   ~= 6.3099 × N^(-1.010)      R²=0.629
```

Interpretation:

- The exact mirror family clearly beats the matched random baseline in MI at
  `N = 40, 60, 80`.
- The advantage is not monotone, because the `N = 100` row falls below the
  random baseline in MI.
- The CL-bath purity tells a slightly different story: mirror is more
  decohering than random at `N = 60, 80, 100`, but slightly less decohering at
  `N = 40`.
- The MI and CL-bath metrics are therefore related but not identical on this
  family.

## Bounded Conclusion

- The exact mirror chokepoint family has a real, finite, bounded MI
  advantage over the matched random baseline at `N = 40, 60, 80` on the
  named parameter card; the advantage **fails** at `N = 100`.
- The strongest supported statement is a **finite mid-N diagnostic**, not a
  clean asymptotic law and not a whole-window mirror MI advantage.
- If you need one canonical line, it is:
  - **on the single parameter card `npl_half = 60, connect_radius = 5.0,
    k = 5.0, layer2_prob = 0.0, 16 seeds`, mirror MI exceeds matched
    random MI at `N = 40, 60, 80` and falls below matched random MI at
    `N = 100`; the descriptive power-law fits are not a global
    slower-decay theorem.**

## Audit boundary (2026-04-28)

Audit verdict (`audited_conditional`, leaf criticality):

> Issue: the finite MI table is live-reproducible, but the proposed-retained
> claim rests on the dense exact-mirror chokepoint family rather than an
> independently audited family theorem, and its canonical-line wording can
> be read as a whole-window mirror advantage even though the `N = 100` row
> has mirror MI 0.0408 below random MI 0.0574.

> Why this blocks: a hostile auditor can certify the printed mid-N
> diagnostic rows, but cannot promote the artifact chain to a clean
> retained claim while the underlying mirror-chokepoint family is
> conditional and the pass criteria for mid-N advantage, `N = 100`
> reversal, purity interpretation, and non-asymptotic exponent use are not
> assertion-gated.

The canonical retained sentence has been narrowed to a single parameter
card with explicit `N = 40 / 60 / 80` advantage and explicit `N = 100`
non-advantage. The descriptive power-law fits are now labeled descriptive
only.

## What this note does NOT claim

- A clean retained asymptotic mirror MI law.
- A whole-retained-window mirror MI advantage (the `N = 100` row falls
  below the matched random baseline on the same parameter card).
- That the mirror exponent fit (`N^{−2.363}`, `R^2 = 0.909`) is anything
  more than a descriptive summary of the four-row table; it is **not** an
  asymptotic slower-decay claim.
- A mirror purity advantage on this family — mirror `pur_cl` is in fact
  lower than random `pur_cl` at `N = 60, 80, 100`.
- An independent retained mirror chokepoint family — the parent family
  ([`docs/MIRROR_CHOKEPOINT_NOTE.md`](MIRROR_CHOKEPOINT_NOTE.md)) is itself
  `audited_conditional`, so this note inherits that condition.

## What would close this lane (Path A future work)

A future worker pursuing reinstatement of a clean mirror MI claim would
need to land all of the following:

1. An independently audited mirror chokepoint family theorem upstream of
   this note (currently the parent is `audited_conditional`).
2. Hard runner-side pass/fail gates for the mid-N rows (`N = 40 / 60 /
   80` mirror MI > random) and explicit fail-gate for the `N = 100`
   reversal, with seed counts, `npl_half`, `connect_radius`, `k`, and
   `layer2_prob` recorded inline in the runner's PASS line.
3. A registered single primary parameter card per row, not a stitched
   table.
4. A defensible interpretation of the fitted power-law exponent (either
   labeled descriptive-only as it is now, or upgraded to an asymptotic
   law with an explicit asymptotic-region argument).
5. A reconciliation between the mirror MI advantage and the lower mirror
   `pur_cl` on the same family — currently the two metrics tell
   different stories at `N = 60, 80, 100`.
