# Cycle 19 Claim Status Certificate — CKM Magnitudes Structural-Counts Narrow Theorem (Pattern A)

**Block:** physics-loop/ckm-magnitudes-structural-counts-narrow-block19-20260502
**Note:** docs/CKM_MAGNITUDES_STRUCTURAL_COUNTS_NARROW_THEOREM_NOTE_2026-05-02.md
**Runner:** scripts/frontier_ckm_magnitudes_structural_counts_narrow.py (PASS=16/0)
**Parent row carved from:** ckm_magnitudes_structural_counts_theorem_note_2026-04-25 (claim_type=positive_theorem, load_bearing_step_class=A)

## Block type

**Pattern A — narrow rescope as new claim row.** This block introduces a new
audit-pending positive_theorem candidate row by isolating the purely
algebraic-substitution implication of the parent CKM magnitudes
structural-counts note from the upstream supply of the parametric input
identities, the canonical `alpha_s(v)` value, and the PDG comparators.

The narrow theorem states only that the four parametric input identities
plus the count constraint `n_quark = n_pair * n_color` algebraically force
the closed-form expressions (M1)-(M5) for the five Wolfenstein-leading
squared off-diagonal CKM-style magnitudes. Pure substitution.

The narrow note has **zero** ledger dependencies because the input
identities enter as hypotheses, `alpha_s` is treated as an abstract symbol,
and no PDG comparator appears.

## Claim-Type Certificate

```yaml
proposed_claim_type: positive_theorem
proposed_claim_scope: |
  Pure algebraic-substitution implication: the four parametric input
  identities plus n_quark = n_pair * n_color force closed-form expressions
  (M1)-(M5) for the five Wolfenstein-leading squared off-diagonal CKM-style
  magnitudes in (alpha_s, n_pair, n_color, n_quark). The framework-specific
  (n_pair, n_color, n_quark) = (2, 3, 6) is one concrete instance; the
  algebra closes for any other count tuple satisfying the same input
  identities.
proposed_load_bearing_step_class: A
status_authority: independent_audit_lane
source_sets_audit_outcome: false
```

## 7-criteria check

| # | Criterion | Pass? |
|---|---|---|
| 1 | proposed_claim_type named | YES (`positive_theorem`) |
| 2 | No open imports for the claimed target | YES (zero ledger deps; the four parametric input identities and the count constraint enter as hypotheses, not ledger imports) |
| 3 | No load-bearing observed/fitted/admitted | YES (`alpha_s` is an abstract positive symbol; no PDG / literature / fitted / admitted-convention input) |
| 4 | Every dep accounted for | YES (vacuously: zero deps) |
| 5 | Runner verifies the algebraic substitution at exact precision | YES (sympy symbolic substitution + simplify on each of (M1)-(M5); two corollary ratios; framework instance (2,3,6); non-framework instance (3,4,12); parent row class-A check) |
| 6 | Review-loop disposition | proposed pass as audit-pending narrow theorem; independent audit pending |
| 7 | PR body says independent audit required | YES |

## Cited deps

(none) — the narrow theorem is dep-free; the four parametric input
identities, `alpha_s` symbolic role, and the count constraint are all
hypotheses, not ledger imports. The framework's `(n_pair, n_color, n_quark)
= (2, 3, 6)` is shown as a special case, not as a load-bearing input.

## Explicitly NOT cited (intentional narrowing)

- `wolfenstein_lambda_a_structural_identities_theorem_note_2026-04-24` —
  parent row's upstream supplying `lambda^2 = alpha_s/n_pair` and `A^2 =
  n_pair/n_color`. Dropped by stating those as input hypotheses.
- `ckm_cp_phase_structural_identity_theorem_note_2026-04-24` — parent row's
  upstream supplying `rho = 1/n_quark` and `eta^2 = (n_quark - 1)/n_quark^2`.
  Dropped by stating `rho^2 + eta^2 = 1/n_quark` as input hypothesis.
- `ckm_atlas_triangle_right_angle_theorem_note_2026-04-24` — parent row's
  upstream supplying the Thales relation. Dropped by stating
  `(1-rho)^2 + eta^2 = (n_quark - 1)/n_quark` as input hypothesis.
- `alpha_s_derived_note` — parent row's upstream supplying the canonical
  `alpha_s(v) = 0.103303...` value. Dropped by treating `alpha_s` as an
  abstract positive symbol.

## What this proposes

A new audit-pending positive_theorem candidate carving out the
purely-algebraic core of the parent
`ckm_magnitudes_structural_counts_theorem_note_2026-04-25`. The narrow
theorem can be ratified independently of any CKM-specific authority,
since it has zero ledger dependencies.

## Forbidden imports check

- No PDG observed values consumed (`|V_us|^2` etc. PDG comparators are not
  present in the narrow note).
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on the claim.
- No same-surface family arguments.

## Audit-graph effect

If independent audit ratifies this row, downstream lanes that need only the
algebraic substitution `(M1)-(M5)` can re-target this narrow theorem
without waiting on any of the four conditional upstreams listed above. The
CKM-physical readouts still require the parent row's supply of the input
identities and the canonical `alpha_s` value, but the
algebraic substitution itself becomes audit-able as a standalone primitive.
