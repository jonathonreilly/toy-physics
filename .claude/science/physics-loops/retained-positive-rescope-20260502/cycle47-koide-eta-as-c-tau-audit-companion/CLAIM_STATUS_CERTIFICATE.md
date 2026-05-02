# Cycle 47 Claim Status Certificate — Koide eta_AS / C_tau Audit Companion (Pattern B)

**Block:** physics-loop/koide-eta-as-c-tau-audit-companion-block47-20260502
**Runner:** scripts/audit_companion_koide_eta_as_c_tau_exact.py (PASS=9/0)
**Target row:** koide_explicit_calculations_note (claim_type=positive_theorem, audit_status=audited_conditional, td=69, load_bearing_step_class=C)

## Block type

**Pattern B — audit-acceleration runner.** Provides exact-precision sympy
verification of two class-(C) numerical / character-arithmetic claims in the
parent:

  R1: |eta_AS(Z_3, (1, 2))| = 2/9 via the AS 1968 Lefschetz character formula;
  R2: C_tau = 3/4 + 1/4 = 1 (SU(2)_L Casimir + (Y/2)^2 hypercharge contribution).

## What the companion verifies

1. **Cube-root-of-unity sanity:** `omega^3 = 1`, `1 + omega + omega^2 = 0`
   exact via sympy cos-rewrite + complex expand.
2. **Lefschetz character at k = 1:** `L(g^1) = 1/3` exact (numerator
   `(1 + omega)(1 + omega^2) = 1`, denominator `(1 - omega)(1 - omega^2) = 3`).
3. **Lefschetz character at k = 2:** `L(g^2) = 1/3` exact (complex
   conjugate identity).
4. **eta_AS = 2/9:** `(L(g^1) + L(g^2)) / 3 = 2/9` exact.
5. **|eta_AS| = 2/9** (positive value).
6. **C_tau = 1:** `3/4 + 1/4 = 1` exact rational.
7. **Algebraic resonance:** `(N_color - 1)/N_color^2 = 2/9` at `N_color = 3`
   (same closed form as eta_AS, distinct physical contexts).
8. **Parent row class-C ledger check.**

## Claim-Type Certificate (Pattern B)

```yaml
target_claim_type: meta  # audit-companion runner
proposed_load_bearing_step_class: C
introduces_new_claim_row: false
introduces_new_source_note: false
modifies_parent_audit_status: false  # audit-lane decides
```

## 7-criteria check (adapted)

| # | Criterion | Pass? |
|---|---|---|
| 1 | Block type named | YES |
| 2 | No new claim rows or new source notes | YES |
| 3 | No load-bearing observed/fitted/admitted in companion | YES (purely symbolic cube-root-of-unity arithmetic) |
| 4 | Parent row's deps unchanged | YES |
| 5 | Runner verifies parent's load-bearing step at exact precision | YES |
| 6 | Review-loop disposition | proposed pass as audit-companion meta artifact |
| 7 | PR body says audit-lane to ratify | YES |

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.

## Audit-graph effect

Meta artifact. Provides exact-precision verification of the parent's local
class-(C) character / Casimir arithmetic. The parent's `audited_conditional`
verdict identifies the unclosed physical bridges (delta_physical = eta_APS,
Q source-law, etc.) — those gaps are NOT addressed here.

## What this proposes

A standalone audit-companion runner verifying eta_AS = 2/9 (via Lefschetz
character) and C_tau = 1 (via Casimir combination) at exact sympy precision.
