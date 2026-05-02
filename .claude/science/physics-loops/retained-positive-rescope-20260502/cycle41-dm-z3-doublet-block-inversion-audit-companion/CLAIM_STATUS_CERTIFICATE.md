# Cycle 41 Claim Status Certificate — DM Z_3 Doublet-Block Inversion Audit Companion (Pattern B)

**Block:** physics-loop/dm-z3-doublet-block-inversion-audit-companion-block41-20260502
**Runner:** scripts/audit_companion_dm_z3_doublet_block_inversion_exact.py (PASS=12/0)
**Target row:** dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem_note_2026-04-16 (claim_type=positive_theorem, audit_status=audited_conditional, td=126, load_bearing_step_class=A)

## Block type

**Pattern B — audit-acceleration runner.** Provides exact-precision sympy
verification of the parent's class-(A) algebraic inversion of the
Z_3-doublet-block parametrization.

## What the companion verifies

1. **Difference identity:** `K22 - K11 = 1/sqrt(3)` exact.
2. **Average identity:** `(K11 + K22)/2 = -q_+ + 2 sqrt(2)/9` exact.
3. **Inversion of q_+:** `q_+ = 2 sqrt(2)/9 - (K11 + K22)/2` recovers
   q_+ exact.
4. **Im(K12) parametric form** and **inversion of delta:**
   `Im(K12) = sqrt(3) delta - 4 sqrt(2)/3`;
   `delta = (Im K12 + 4 sqrt(2)/3) / sqrt(3)` exact.
5. **Re(K12) parametric form** and **inversion of m:**
   `Re(K12) = m - 4 sqrt(2)/9`; `m = Re K12 + 4 sqrt(2)/9` exact.
6. **Concrete round-trip** at `(m, delta, q_+) = (1, 0, 0)`: full
   recovery exact.
7. **Parent row class-(A) ledger check.**

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
| 5 | Runner verifies parent's load-bearing step at exact precision | YES (sympy `Rational`, `simplify`, `im`, `re`) |
| 6 | Review-loop disposition | proposed pass as audit-companion meta artifact |
| 7 | PR body says audit-lane to ratify | YES |

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.

## Out of scope

- The singlet-doublet slot equalities `K01 = a_*, K02 = b_*` (intrinsic-slot
  theorem, separate authority).
- The `m = Tr(K_Z3)` identification (requires `K00 = a_*` from
  intrinsic-slot theorem).
- The upstream post-canonical positive-polar section / singlet-doublet
  CP slot tool / active-affine point-selection boundary authorities.

## What this proposes

A standalone audit-companion runner verifying the parent's algebraic
inversion of the Z_3-doublet-block parametrization at exact symbolic
precision. The block proposes nothing about any retained-status change;
the audit lane is the authority for that.
