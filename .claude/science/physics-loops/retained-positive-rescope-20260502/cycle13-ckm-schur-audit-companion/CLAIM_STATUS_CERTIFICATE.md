# Cycle 13 Claim Status Certificate — CKM Schur Complement Audit Companion (Pattern B)

**Block:** physics-loop/ckm-schur-audit-companion-block13-20260502
**Runner:** scripts/audit_companion_ckm_schur_complement_exact.py (PASS=11/0)
**Target row:** ckm_schur_complement_theorem

## Block type

**Pattern B — audit-acceleration runner.** This block does NOT introduce a new
claim row, a new source note, or a new positive theorem. It contributes a
focused exact-precision verification companion to the existing
`ckm_schur_complement_theorem` row, providing audit-lane evidence for the
load-bearing step at sympy `Rational` precision (rather than machine epsilon).

The parent row's load-bearing step is the algebraic identity

```text
    c_13^eff  =  c_12 · c_23
```

obtained from the Schur complement of the generation-2 block in the
NNI geometric-mean-normalized mass matrix. This is class (A) on the
audit rubric — pure algebraic identity on abstract NNI matrix structure,
no external observed/fitted/literature input.

## Claim-Type Certificate (Pattern B)

```yaml
artifact_type: audit_companion_meta
proposed_load_bearing_step_class: A
introduces_new_claim_row: false
introduces_new_source_note: false
modifies_parent_status: false
status_authority: independent audit lane only
bare_retained_allowed: false
```

## 7-criteria check (adapted for Pattern B)

| # | Criterion | Pass? |
|---|---|---|
| 1 | Block type named | YES (Pattern B audit-acceleration runner) |
| 2 | No new claim rows or new source notes introduced | YES (runner-only; provides class-A breakdown evidence on existing row) |
| 3 | No load-bearing observed/fitted/admitted in the companion | YES (purely symbolic sympy verification; no PDG/literature numerical comparators) |
| 4 | Parent row's deps unchanged by this block | YES (does not modify ledger row state; only adds runner artifact) |
| 5 | Runner verifies parent's load-bearing step at exact precision | YES (sympy Rational; symbolic matrix; concrete rational test point; independence-of-(m_1,m_3) sweep) |
| 6 | Review-loop disposition | proposed pass as audit-companion meta artifact; independent audit lane decides whether the parent row changes |
| 7 | PR body says audit-lane to ratify | YES (block proposes companion evidence only; does not assert status) |

## Audit-graph effect

This companion is **meta** — it does not move the parent row by itself.
The role is to give the audit lane focused class-(A) breakdown evidence that
the parent's load-bearing identity holds at exact precision, useful when
revisiting the parent row.

If the audit lane revisits ckm_schur_complement_theorem with this companion
in scope, the conditional may tighten — but that decision belongs to the
audit lane, not to this proposal.

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on the companion.
- No same-surface family arguments.

The companion is pure symbolic algebra on `(m_1, m_2, m_3, c_12, c_23)` with
sympy `Rational` test substitutions for sanity checks.

## What this proposes

A standalone audit-companion runner that complements the existing primary
runner for the parent row by providing exact rational verification of the
Schur complement identity. The block proposes nothing about the broader
theorem's Wolfenstein cascade, NNI coefficients, absolute s_23, or
mass-ratio projection — those remain separate downstream claims.
