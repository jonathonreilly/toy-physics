# Cycle 17 Claim Status Certificate — DM Neutrino Z3 Character Transfer Audit Companion (Pattern B)

**Block:** physics-loop/dm-neutrino-z3-character-audit-companion-block17-20260502
**Runner:** scripts/audit_companion_dm_neutrino_z3_character_exact.py (PASS=24/0)
**Target row:** dm_neutrino_z3_character_transfer_theorem_note_2026-04-15 (claim_type=positive_theorem, audit_status=audited_conditional, td=134, load_bearing_step_class=A)

## Block type

**Pattern B — audit-acceleration runner.** This block does NOT introduce a new
claim row, a new source note, or a new positive theorem. It contributes a
focused exact-precision verification companion to the existing
`dm_neutrino_z3_character_transfer_theorem_note_2026-04-15` row, providing
audit-lane evidence at sympy symbolic precision (rather than 1e-12 numpy
float).

The parent's load-bearing step is the algebraic identity:

```
exp(i lambda * 2pi/3) is a Z3 character (chi^3 = 1) iff lambda is an integer;
on the continuity strip |lambda| <= 1 the only source-faithful branches are
{-1, 0, +1}.
```

The existing primary runner verifies this at numpy float precision; this
companion verifies it as a sympy closed-form identity (`exp(I * 2 * pi * n)`
reduces symbolically to `1` for integer `n`, and the Z3 character sum
`omega + omega-bar + 1` reduces symbolically to `0`).

## Claim-Type Certificate (Pattern B)

```yaml
target_claim_type: meta  # audit-companion runner; not a claim row
proposed_load_bearing_step_class: A
introduces_new_claim_row: false
introduces_new_source_note: false
modifies_parent_audit_status: false  # audit-lane decides
audit_required_before_effective_retained: true  # parent row only; companion is meta
bare_retained_allowed: false
```

## 7-criteria check (adapted for Pattern B)

| # | Criterion | Pass? |
|---|---|---|
| 1 | Block type named | YES (Pattern B audit-acceleration runner) |
| 2 | No new claim rows or new source notes introduced | YES (runner-only; provides class-A exact-precision breakdown evidence) |
| 3 | No load-bearing observed/fitted/admitted in the companion | YES (purely symbolic sympy verification of cube-root-of-unity arithmetic; no PDG/literature numerical comparators) |
| 4 | Parent row's deps unchanged by this block | YES (does not modify ledger row state; only adds runner artifact) |
| 5 | Runner verifies parent's load-bearing step at exact precision | YES (sympy symbolic exp/cos/sin reductions on integer / non-integer lambda; closed-form omega-arithmetic) |
| 6 | Review-loop disposition | proposed pass as audit-companion meta artifact; audit-lane decides whether the parent row's `audited_conditional` verdict can be tightened |
| 7 | PR body says audit-lane to ratify | YES (block proposes companion evidence only; does not assert any retained-status promotion) |

## What the companion verifies

1. **Integer lambda gives chi^3 = 1 exactly.** For lambda in {-2, -1, 0, 1, 2},
   `exp(i * 2pi * lambda)` reduces to `1` symbolically.
2. **Non-integer lambda fails Z3.** For lambda in {1/2, 1/3, 2/3, 1/4, 3/4},
   `chi(lambda)^3` evaluates symbolically to a non-1 closed form
   (-1, omega, omega^2, i, -i respectively).
3. **Continuity strip.** `chi(0) = 1`, `chi(+1) = omega = exp(2pi i/3)`,
   `chi(-1) = omega-bar = exp(-2pi i/3) = conjugate(chi(+1))`, all exact.
4. **Cube-root-of-unity identities.** `omega^3 = 1`, `omega-bar^3 = 1`,
   `omega + omega-bar + 1 = 0`, `omega * omega-bar = 1`, all exact.
5. **Parent row class-(A) check.** Confirms the audit ledger records the
   parent's load-bearing step class as `A` (consistent with the algebraic
   nature of the identity).

## Audit-graph effect

This companion is **meta** — it does not move the parent row by itself.
The parent row currently sits at `audited_conditional` because the verdict
identifies the upstream phase-lift family, weak-only source delta_src, and
source-orientation branch selection authorities as not provided as ledger
deps. The companion's role is to give the audit lane focused exact-precision
evidence that the parent's load-bearing class-(A) algebraic step (the
discretization itself) holds at exact symbolic precision, useful when
revisiting the conditional verdict.

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.

The companion is pure symbolic algebra on `exp(I * 2 * pi * n)` for various
rational `n`, with closed-form omega-arithmetic.

## What this proposes

A standalone audit-companion runner that complements the existing primary
runner by providing exact symbolic verification of the Z3 character-transfer
discretization. The block proposes nothing about any retained-status change;
the audit lane is the authority for that.
