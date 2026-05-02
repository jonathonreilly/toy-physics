# Cycle 29 Claim Status Certificate — CKM Bernoulli 2/9 Audit Companion (Pattern B)

**Block:** physics-loop/ckm-bernoulli-2-9-audit-companion-block29-20260502
**Runner:** scripts/audit_companion_ckm_bernoulli_two_ninths_exact.py (PASS=14/0)
**Target row:** ckm_bernoulli_two_ninths_koide_bridge_support_note_2026-04-25 (claim_type=positive_theorem, audit_status=audited_conditional, td=85, load_bearing_step_class=A)

## Block type

**Pattern B — audit-acceleration runner.** This block does NOT introduce a new
claim row, a new source note, or a new positive theorem. It contributes a
focused exact-precision verification companion to the existing
`ckm_bernoulli_two_ninths_koide_bridge_support_note_2026-04-25` row, providing
audit-lane evidence at sympy `Rational` exact precision for the algebraic
content of the K1, K2, K3, K5, K6 identities.

The parent's load-bearing class-(A) content includes:

- four forward identities `K1, K2, K5, K6 = 2/9` at `(N_pair, N_color) = (2, 3)`;
- the K3 consistency converse: over positive integer pair/color counts,
  `K1 = K2 = K5 = K6 = 2/9` is **equivalent** to `(N_pair, N_color) = (2, 3)`.

The existing primary runner uses Python `Fraction` for the forward direction
at the retained counts. This Pattern B companion adds:

(a) sympy-symbolic verification of the four forward identities parameterized
    over abstract `(p, c)` positive integers;
(b) symbolic solution of the K3 converse via `sympy.solve` of the quadratic
    `2c^2 - 9c + 9 = 0`, exhibiting solutions `{3, 3/2}` with positive-integer
    constraint forcing `c = 3` and then `K5 = 2/9` forcing `p = 2`;
(c) exhaustive enumeration over `(p, c) in {1, ..., 8}^2 \ {(2, 3)}` confirming
    that all 63 off-target pairs break at least one of `K1, K2, K5, K6 = 2/9`.

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
| 3 | No load-bearing observed/fitted/admitted in the companion | YES (purely symbolic algebra and number-theoretic enumeration; no PDG/literature/fitted/admitted-convention input) |
| 4 | Parent row's deps unchanged by this block | YES (does not modify ledger row state; only adds runner artifact) |
| 5 | Runner verifies parent's load-bearing step at exact precision | YES (sympy `Rational`, `simplify`, `solve` for K3 converse, `subs` and exhaustive enumeration for K3 forward) |
| 6 | Review-loop disposition | proposed pass as audit-companion meta artifact; audit-lane decides |
| 7 | PR body says audit-lane to ratify | YES (block proposes companion evidence only; does not assert any retained-status promotion) |

## What the companion verifies

1. **Forward at (2, 3):** `K1, K2, K5, K6 = 2/9` exact at `(N_pair, N_color) = (2, 3)`.
2. **Parametric closed forms:** `K1(p,c) = p(c-p)/c^2`, `K2(p,c) = 2/c^2`,
   `K5(p,c) = p/c^2`, `K6(p,c) = (c-1)/c^2`, all symbolic in `(p, c)`.
3. **K3 converse rational solutions:** `K6 = 2/9` solved by sympy gives
   `{3, 3/2}`; the unique positive integer is `c = 3`.
4. **K3 converse uniqueness for p:** with `c = 3`, `K5 = 2/9` forces
   `p = 2` uniquely.
5. **K3 forward enumeration:** all 63 off-target pairs `(p, c) in {1,...,8}^2 \
   {(2, 3)}` break at least one of `K1, K2, K5, K6 = 2/9`.
6. **K3 backward (consistency at (2, 3)):** at `(p, c) = (2, 3)` all four
   identities symbolically agree.
7. **Parent row class-(A) ledger check.**

## Audit-graph effect

This companion is **meta** — it does not move the parent row by itself. The
parent's `audited_conditional` verdict identifies the upstream Wolfenstein,
CP-phase, and magnitudes-counts authorities (each itself audited_conditional)
as the unratified deps that prevent retained-grade status. None of those
upstream gaps are addressed by this companion; the companion only verifies
that the parent's local class-(A) algebraic content holds at exact symbolic
precision and that the K3 converse is rigorously closed via sympy `solve`,
useful when audit-lane reviewers revisit the conditional verdict on the
local-algebra portion of the row.

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.

The companion is pure symbolic algebra + integer enumeration, with K3
converse verified via sympy quadratic-equation solving.

## What this proposes

A standalone audit-companion runner that complements the existing primary
runner by providing exact symbolic verification of the K3 converse via
`sympy.solve` and exhaustive integer enumeration confirming the K3 forward
direction. The block proposes nothing about any retained-status change;
the audit lane is the authority for that.
