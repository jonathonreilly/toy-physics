# Cycle 50 Claim Status Certificate — Koide Z³ Scalar Potential Audit Companion (Pattern B)

**Block:** physics-loop/koide-z3-scalar-potential-audit-companion-block50-20260502
**Runner:** scripts/audit_companion_koide_z3_scalar_potential_exact.py (PASS=14/0)
**Target row:** koide_z3_scalar_potential_support_note_2026-04-19 (claim_type=positive_theorem, audit_status=audited_conditional, td=70, load_bearing_step_class=A)

## Block type

**Pattern B — audit-acceleration runner.** Provides exact-precision sympy
verification of the parent's class-(A) Clifford-trace algebra:

  - T_m^2 = I_3 (Clifford involution);
  - Tr(T_m) = Tr(T_m^3) = 1, Tr(T_m^2) = 3;
  - g_2 = (1/2) Tr(T_m^2) = 3/2 and g_3 = (1/6) Tr(T_m^3) = 1/6
    (scalar-potential coefficient assignments);
  - m^2 cross term in Tr(K^3) = 3 Tr(K_frozen) (vanishes under traceless K_f);
  - V(m) = V_0 + (linear) m + (3/2) m^2 + (1/6) m^3 exact form.

## Claim-Type Certificate (Pattern B)

```yaml
target_claim_type: meta  # audit-companion runner
proposed_load_bearing_step_class: A
introduces_new_claim_row: false
introduces_new_source_note: false
modifies_parent_audit_status: false  # audit-lane decides
```

## 7-criteria check (adapted)

| # | Criterion | Pass? |
|---|---|---|
| 1 | Block type named | YES |
| 2 | No new claim rows or new source notes | YES |
| 3 | No load-bearing observed/fitted/admitted | YES |
| 4 | Parent row's deps unchanged | YES |
| 5 | Runner verifies parent's load-bearing step at exact precision | YES (sympy `Matrix`, `Rational`, `expand`, `coeff`; explicit involution + trace identities + V(m) coefficient extraction) |
| 6 | Review-loop disposition | proposed pass as audit-companion meta artifact |
| 7 | PR body says audit-lane to ratify | YES |

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.

## Audit-graph effect

Meta artifact. The parent's `audited_conditional` verdict identifies
upstream selected-slice / frozen-bank / K_Z3 machinery as the
unratified deps. None of those gaps are addressed here; the companion
verifies the parent's local class-(A) Clifford-trace algebra.

## What this proposes

A standalone audit-companion runner verifying the Clifford-trace
algebra at exact symbolic precision.
