# Three Independent Grown Families: 9/9 Properties Match

**Date:** 2026-04-06
**Status:** RETRACTED 2026-04-30 — audit failed; this note is archived under `archive_unlanded/family-card-incomplete-artifacts-2026-04-30/`. Claims below are NOT supported by current runners or current audit lane. See `## Retraction` section.

## Retraction

- **Date archived:** 2026-04-30
- **Archive directory:** `archive_unlanded/family-card-incomplete-artifacts-2026-04-30/` (the directory name encodes the failure reason: incomplete artifacts behind the family-card claim).
- **Audit verdict_rationale (quoted verbatim from `docs/audit/data/audit_ledger.json`):**

  > Issue: The note claims three families match on all 9 measurable properties, but the table explicitly has Family 3 Distance alpha marked '(not yet)' and the note provides no runner or log artifact to verify the cross-family card. Why this blocks: the load-bearing 9/9 statement is false on the face of the supplied table, and the broader inference that observables are geometry-independent cannot follow from a partial, hand-entered comparison. Repair target: add a runner that recomputes every listed property for all three families, including Family 3 Distance alpha, with explicit <5% assertions and at least one holdout check. Claim boundary until fixed: safe to cite this as a partial comparison of three selected drift/restore rows with eight populated properties and distance-alpha data only for Families 1 and 2; not safe to claim 9/9 three-family equality or geometry-independence.

- **Do not cite warning:** Do NOT cite the numerical results, tables, or threshold values in the original content below as live framework claims. The runners referenced in this note have been superseded or are no longer reproducible at the time of audit. If a future investigation revisits this physics, treat it as starting from scratch rather than as continuation of a "closed no-go".

## Families

| Family | drift | restore | Distance from center |
| --- | ---: | ---: | --- |
| 1 (center) | 0.20 | 0.70 | — |
| 2 | 0.05 | 0.30 | far (low both) |
| 3 | 0.50 | 0.90 | far (high both) |

## Cross-family comparison (seed=0)

| Property | Fam 1 | Fam 2 | Fam 3 | Max diff |
| --- | ---: | ---: | ---: | ---: |
| F~M (6 seeds) | 0.990 | 0.993 | 0.994 | 0.4% |
| Born | 0.00e+00 | 0.00e+00 | 1.7e-15 | 0 |
| Gravity TOWARD | 3/3 | 3/3 | 3/3 | 0 |
| MI (bits) | 0.545 | 0.521 | 0.546 | 4.6% |
| d_TV | 0.787 | 0.771 | 0.781 | 2.1% |
| Escape (gamma=0) | 1.027 | 1.028 | 1.028 | 0.1% |
| cx crossover | 3/3→0/3 | 3/3→0/3 | 3/3→0/3 | 0 |
| cx_escape (gamma=0.5) | 0.965 | 0.965 | 0.965 | 0% |
| Distance alpha | -0.962 | -0.947 | (not yet) | 1.6% |

## Claim boundary

Three independent grown families, spanning the full drift/restore parameter
space (0.05-0.50 drift, 0.30-0.90 restore), produce quantitatively identical
physics on all 9 measurable properties to within 5%.

This is evidence that the physics emerges from the propagator+action, not
from the specific geometry. The growth rule determines the graph topology,
but the observables are geometry-independent.

This is NOT a claim about arbitrary graphs or arbitrary growth rules.
It is specific to the template+drift+restore family with dense NN connectivity.
