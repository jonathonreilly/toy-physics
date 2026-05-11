# Universal GR Invariant Nonlinear Completion on `PL S^3 x R`

**Status:** support - invariant nonlinear completion step
**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Role:** direct universal route / nonlinear invariant-family theorem step
**Runner:** `scripts/frontier_universal_gr_invariant_nonlinear_completion.py`
**Cache:** `logs/runner-cache/frontier_universal_gr_invariant_nonlinear_completion.txt`
  (registration only; runner numerically demonstrates the invariant-family
  glue identity but does not by itself close the audit dependency edges
  flagged below).

## Verdict

The direct universal route is now closed one rung higher than the exact
isotropic quadratic glue operator.

It already closes on the **full positive invariant background family**

`D = diag(a,b,b,b)`, with `a > 0`, `b > 0`,

not just at one fixed background point.

The reason is simple but load-bearing:

1. the observable-principle generator is exact at all orders;
2. on the invariant family, its restriction is explicitly

   `W_iso(a,b) = const + log a + 3 log b`;

3. its exact local Hessian at each background point is therefore the already
   identified isotropic supermetric weight matrix

   `M_D = a^-2 P_lapse + (ab)^-1 P_shift + b^-2 P_trace + b^-2 P_shear`;

4. the exact slice generator `Lambda_R` is already symmetric positive definite
   on the direct universal route;

5. so the already-proved glue law

   `K_GR^iso(D) = M_D ⊗ Lambda_R`

   is not merely a one-background quadratic approximation. It is an exact
   nonlinear family of covariant quadratic boundary actions over the whole
   positive invariant family.

## Exact invariant-family action

For any positive invariant background `D = diag(a,b,b,b)`, define

`I_GR^iso(F ; D, J) = 1/2 <F, K_GR^iso(D) F> - <J, F>`

with

`K_GR^iso(D) = M_D ⊗ Lambda_R`.

Because:

- `M_D` is exact for every positive `(a,b)`,
- `Lambda_R` is exact and symmetric positive definite,

the action is strictly convex for every positive invariant background.

So every invariant background in the direct universal family carries a unique
stationary bridge field

`F_* = K_GR^iso(D)^-1 J`

and the exact quadratic completion identity

`I_GR^iso(F_* + Δ ; D, J) - I_GR^iso(F_* ; D, J)
 = 1/2 <Δ, K_GR^iso(D) Δ>`

holds on the whole positive invariant family.

## Why this is genuinely nonlinear

This is not “still just the same quadratic theorem.”

The operator remains quadratic in the bridge field `F`, but the metric-side
weights are exact nonlinear functions of the invariant background:

- lapse: `a^-2`
- shift: `(ab)^-1`
- trace: `b^-2`
- shear: `b^-2`

So the direct universal route now has an exact family-level metric dependence,
not merely a tangent-space statement at one chosen background.

Equivalently:

> nonlinear completion on the invariant family is already forced by the exact
> all-orders observable generator plus the exact slice generator.

## What this closes

This discharges the old direct-universal blocker in its remaining invariant
form.

The direct universal route is now exact at:

- scalar observable level
- `3+1` lift level
- quotient-kernel level
- canonical block-localization level
- invariant-background Schur-localization level
- isotropic supermetric normal-form level
- isotropic quadratic Einstein/Regge glue-operator level
- invariant-family nonlinear completion level

## What remains open

The live remaining issue is now smaller:

> widening beyond the invariant background family `diag(a,b,b,b)`.

So the direct universal route is no longer honestly blocked on nonlinear
completion **within** the invariant family. It is blocked only on extension
outside that family if one wants full universal GR without qualification.

## Honest status

This is still not a full unrestricted-GR claim.

But it is stronger than the previous state in exactly the way that matters:

- the invariant direct universal branch is no longer merely quadratic at one
  background;
- it is an exact nonlinear family over all positive invariant backgrounds.

**Current audit-ledger conditional (per 2026-05-05 verdict):** the algebraic
convexity identity is accepted as written, but the three load-bearing imports
- exact all-orders observable generator giving `W_iso(a,b)=const+log a+3 log b`,
- exact SPD slice generator `Lambda_R`,
- invariant-family glue law `K_GR^iso(D)=M_D ⊗ Lambda_R`,
are referenced descriptively rather than wired to retained-grade direct
dependency edges in the audit ledger (`deps: []`, `direct_in_degree: 2`).
The verdict is therefore `audited_conditional` until those three premises
are either supplied as cited authorities (each retained-grade) or replaced
by a single self-contained restricted-packet derivation. Registering the
runner here does not move that verdict; it only documents that the
numerical invariant-family check is reproducible.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [observable_principle_from_axiom_note](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
- [s3_anomaly_spacetime_lift_note](S3_ANOMALY_SPACETIME_LIFT_NOTE.md)
- [universal_gr_isotropic_glue_operator_note](UNIVERSAL_GR_ISOTROPIC_GLUE_OPERATOR_NOTE.md)
- `DISCRETE_EINSTEIN_REGGE_LIFT_NOTE.md` (downstream consumer; backticked to avoid length-2 cycle — citation graph direction is *downstream → upstream*; the restricted strong-field discrete lift is a downstream specialisation, not an input to the invariant nonlinear completion family)
