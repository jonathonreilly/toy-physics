# Cycle 35 Claim Status Certificate — CKM n/9 Structural Family Audit Companion (Pattern B)

**Block:** physics-loop/ckm-n9-structural-family-audit-companion-block35-20260502
**Runner:** scripts/audit_companion_ckm_n9_structural_family_exact.py (PASS=36/0)
**Target row:** ckm_n9_structural_family_koide_bridge_support_note_2026-04-25 (claim_type=positive_theorem, audit_status=audited_conditional, td=84, load_bearing_step_class=A)

## Block type

**Pattern B — audit-acceleration runner.** This block does NOT introduce a new
claim row, a new source note, or a new positive theorem. It contributes a
focused exact-precision verification companion to the existing
`ckm_n9_structural_family_koide_bridge_support_note_2026-04-25` row, providing
audit-lane evidence at sympy `Rational` exact precision for the full F_1
through F_9 ladder.

The parent's load-bearing class-(A) content is the complete `n/9` ladder of
algebraically distinct CKM-native readouts plus the G1 sum identity
(`sum F_n = N_quark - 1`) and the universal-denominator G2.

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
| 2 | No new claim rows or new source notes introduced | YES (runner-only; provides class-A breakdown evidence on existing row) |
| 3 | No load-bearing observed/fitted/admitted in the companion | YES (purely symbolic algebra; no PDG/literature/fitted/admitted-convention input) |
| 4 | Parent row's deps unchanged by this block | YES (does not modify ledger row state; only adds runner artifact) |
| 5 | Runner verifies parent's load-bearing step at exact precision | YES (sympy `Rational`, `simplify`, parametric expressions over abstract `(p, c, q)` plus framework instance verification) |
| 6 | Review-loop disposition | proposed pass as audit-companion meta artifact; audit-lane decides |
| 7 | PR body says audit-lane to ratify | YES (block proposes companion evidence only; does not assert any retained-status promotion) |

## What the companion verifies

1. **F_1 closed form:** `A^2 rho = 1/c^2` under `q = p c`.
2. **F_2 four closed forms:** `A^2 (1 - A^2) = (c-1)/c^2` at `p = c-1`;
   `2 rho A^2 = 2/c^2` under `q = pc`; `A^2 / c = p/c^2`;
   `(1/c)(1 - 1/c) = (c-1)/c^2`.
3. **F_3 closed forms:** `1 - A^2 = (c - p)/c`; `1/c`.
4. **F_4 closed form:** `A^4 = p^2/c^2`.
5. **F_5 three closed forms:** `(1 - A^2)(1 + A^2) = 1 - A^4`;
   `eta^2 N_pair^2 = (pc - 1)/c^2` under `q = pc`.
6. **F_6 closed forms:** `A^2 = p/c`; `q/c^2 = p/c` under `q = pc`.
7. **F_7, F_8, F_9 closed forms** symbolic over `(p, c)`.
8. **Framework instance** (p, c, q) = (2, 3, 6): all `F_n = n/9` exact.
9. **G1 sum identity:** `sum F_n = 45/9 = 5 = N_quark - 1` exact.
10. **G2 universal denominator:** all `F_n * 9 = n` exact (universal
    denominator `c^2 = 9`).
11. **Parent row class-(A) ledger check.**

## Audit-graph effect

This companion is **meta** — it does not move the parent row by itself.
The parent's `audited_conditional` verdict identifies the upstream
Wolfenstein / CP-phase / magnitudes-counts / Bernoulli authorities (each
itself audited_conditional) as the unratified deps. None of those gaps
are addressed here; the companion only verifies the parent's local
class-(A) `n/9`-ladder identities at exact symbolic precision over both
the framework instance and the parametric family, useful when audit-lane
reviewers revisit the conditional verdict on the local-algebra portion
of the row.

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.

## What this proposes

A standalone audit-companion runner that complements the existing primary
runner by providing exact symbolic verification of the F_1-F_9 ladder
parametrically over (p, c, q) and at the framework instance, plus the G1
sum identity and the universal-denominator G2. The block proposes
nothing about any retained-status change; the audit lane is the
authority for that.
