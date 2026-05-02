# Cycle 26 Claim Status Certificate — DM Neutrino Dirac Bridge Audit Companion (Pattern B)

**Block:** physics-loop/dm-neutrino-dirac-bridge-audit-companion-block26-20260502
**Runner:** scripts/audit_companion_dm_neutrino_dirac_bridge_exact.py (PASS=29/0)
**Target row:** dm_neutrino_dirac_bridge_theorem_note_2026-04-15 (claim_type=positive_theorem, audit_status=audited_conditional, td=115, load_bearing_step_class=C)

## Block type

**Pattern B — audit-acceleration runner.** This block does NOT introduce a new
claim row, a new source note, or a new positive theorem. It contributes a
focused exact-precision verification companion to the existing
`dm_neutrino_dirac_bridge_theorem_note_2026-04-15` row, providing audit-lane
evidence at sympy `Rational` exact precision for the algebraic content of
the bridge theorem.

The parent's load-bearing step bundles two distinct components:

(a) **Algebraic content** (in-scope of this companion): Hermitian
    involutions `Gamma_i`, Clifford anticommutation, anticommute with
    `gamma_5`, `M(phi)` Hermitian and `M^2 = |phi|^2 I`, chiral
    off-diagonal property, axis-evaluation property.

(b) **Selector minima and upstream framework structure** (out-of-scope):
    `V_sel = 32 sum_{i<j} phi_i^2 phi_j^2` minima at axis vectors;
    Higgs family upstream; 3+1 chirality operator framework derivation;
    weak-axis branch convention. The audit verdict identifies these as
    requiring separate retained dependencies.

The companion verifies (a) at exact precision via the standard 4x4
Euclidean Cl(4) Dirac realization.

## Claim-Type Certificate (Pattern B)

```yaml
target_claim_type: meta  # audit-companion runner; not a claim row
proposed_load_bearing_step_class: C
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
| 2 | No new claim rows or new source notes introduced | YES (runner-only; provides class-C breakdown evidence on existing row) |
| 3 | No load-bearing observed/fitted/admitted in the companion | YES (purely symbolic linear algebra on Cl(4) Dirac matrices; no PDG/literature/fitted/admitted-convention input) |
| 4 | Parent row's deps unchanged by this block | YES (does not modify ledger row state; only adds runner artifact) |
| 5 | Runner verifies parent's algebraic content at exact precision | YES (sympy `Matrix`, `Rational`, explicit Kronecker product, exact equality checks for all eight algebraic identities) |
| 6 | Review-loop disposition | proposed pass as audit-companion meta artifact; audit-lane decides |
| 7 | PR body says audit-lane to ratify | YES (block proposes companion evidence only; does not assert any retained-status promotion) |

## What the companion verifies

1. **Hermitian involutions.** `Gamma_i = Gamma_i^dagger`, `Gamma_i^2 = I_4`
   for `i = 1, 2, 3` on the 4x4 Cl(4) realization.
2. **Cl(3) anticommutation.** `{Gamma_i, Gamma_j} = 2 delta_{ij} I_4`
   exact for all i, j.
3. **gamma_5 properties.** `gamma_5` Hermitian, `gamma_5^2 = I_4` exact.
4. **Chiral off-diagonal.** `{Gamma_i, gamma_5} = 0` exact for `i = 1, 2, 3`.
5. **M(phi) Hermitian and involution-squared.** Symbolic verification
   that `M(phi) = sum phi_i Gamma_i` is Hermitian and
   `M(phi)^2 = |phi|^2 I_4` exact.
6. **Chiral projector idempotents.** `P_L^2 = P_L`, `P_R^2 = P_R`,
   `P_L + P_R = I`, `P_L P_R = 0` exact.
7. **Chiral off-diagonal of M.** `P_L M(phi) P_L = P_R M(phi) P_R = 0`
   exact symbolic.
8. **Axis evaluation.** `M(e_i) = Gamma_i` exact for `i = 1, 2, 3`.
9. **Parent row class-(C) ledger check.**

## Audit-graph effect

This companion is **meta** — it does not move the parent row by itself.
The parent's `audited_conditional` verdict identifies four upstream gaps:

> Repair target: add retained dependencies or an integrated derivation
> for the Higgs family, selector, 3+1 chirality operator, and weak-axis
> convention before the Gamma_1 selection step.

None of those four items are addressed by this companion. The companion
only verifies the algebraic content of the bridge theorem at exact
precision, useful when audit-lane reviewers revisit the conditional
verdict on the local-algebra portion of the row.

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.

The companion is pure symbolic linear algebra on the standard 4x4
Euclidean Cl(4) Dirac realization
(`gamma_i = sigma_i (x) sigma_x` for `i = 1, 2, 3`,
`gamma_4 = I_2 (x) sigma_y`, `gamma_5 = gamma_1 gamma_2 gamma_3 gamma_4`).

## What this proposes

A standalone audit-companion runner that complements the existing primary
runner by providing exact symbolic verification of the bridge theorem's
algebraic content. The block proposes nothing about any retained-status
change; the audit lane is the authority for that, and the four
verdict-identified upstream gaps are not addressed here.
