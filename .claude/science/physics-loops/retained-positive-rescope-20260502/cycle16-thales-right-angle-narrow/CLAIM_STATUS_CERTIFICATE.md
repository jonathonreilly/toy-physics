# Cycle 16 Claim Status Certificate — Thales Right-Angle Narrow Theorem (Pattern A)

**Block:** physics-loop/ckm-thales-right-angle-narrow-block16-20260502
**Note:** docs/THALES_RIGHT_ANGLE_NARROW_THEOREM_NOTE_2026-05-02.md
**Runner:** scripts/frontier_thales_right_angle_narrow.py (PASS=18/0)
**Parent row carved from:** ckm_atlas_triangle_right_angle_theorem_note_2026-04-24 (claim_type=positive_theorem, audit_status=audited_conditional, td=116, load_bearing_step_class=A)

## Block type

**Pattern A — narrow rescope as new claim row.** This block introduces a new
positive-theorem candidate row by isolating the purely geometric / arctan-algebra
implication of the parent CKM atlas right-angle note from the upstream supply
of the CKM-specific `(rho, eta) = (1/6, sqrt(5)/6)` values.

The narrow theorem states only:

> If `0 < rho < 1`, `eta > 0`, `eta^2 = rho(1 - rho)`, then the triangle
> `(0,0)-(1,0)-(rho, eta)` has a right angle at `(rho, eta)`.

This is one-line elementary plane geometry (Pythagoras / dot-product).
The narrow note has **zero** ledger dependencies because the Thales
hypothesis enters as a hypothesis, not as a load-bearing import.

## Claim-Type Certificate

```yaml
target_claim_type: positive_theorem
proposed_claim_scope: |
  Pure Euclidean / arctan-algebra implication: any (rho, eta) on the upper
  half of the Thales circle on diameter [0, 1] sees that diameter under a
  right angle. The CKM atlas instance (rho, eta) = (1/6, sqrt(5)/6) is one
  point on this circle, but is not a load-bearing input to this note's
  implication.
proposed_load_bearing_step_class: A
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## 7-criteria check

| # | Criterion | Pass? |
|---|---|---|
| 1 | target_claim_type named | YES (`positive_theorem`) |
| 2 | No open imports for the claimed target | YES (zero ledger deps; the Thales hypothesis is a stated premise, not an import) |
| 3 | No load-bearing observed/fitted/admitted | YES (purely Euclidean / arctan-algebra; no PDG / literature / fitted / admitted-convention input) |
| 4 | Every dep retained-grade | YES (vacuously — zero deps) |
| 5 | Runner checks the algebraic identity at exact precision | YES (sympy symbolic dot-product reduction + 50-digit arctan-sum check + four concrete rational instances) |
| 6 | Review-loop disposition | proposed pass as audit-pending narrow theorem; independent audit pending |
| 7 | PR body says independent audit required | YES |

## Cited deps

(none) — the narrow theorem is dep-free; the Thales hypothesis is a premise,
not a ledger import. The CKM atlas instance `(rho, eta) = (1/6, sqrt(5)/6)`
is shown as a special case of the general statement, not as a load-bearing
input.

## Explicitly NOT cited (intentional narrowing)

- `ckm_cp_phase_structural_identity_theorem_note_2026-04-24` — the parent
  row's unratified upstream that supplies the CKM atlas/Wolfenstein
  values. By narrowing to the Thales hypothesis as a premise, this dep is
  dropped entirely.

## What this proposes

A new audit-pending positive_theorem candidate carving out the
purely-geometric core of the parent `ckm_atlas_triangle_right_angle_theorem_note_2026-04-24`.
The narrow theorem can be ratified independently of any CKM-specific
authority because it has zero ledger dependencies.

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.

## Audit-graph effect

If independent audit ratifies this row, downstream lanes that need only the
geometric implication (Thales-circle ⇒ right angle) can re-target this
narrow theorem without waiting on
`ckm_cp_phase_structural_identity_theorem_note_2026-04-24` or any other
CKM-specific upstream. The CKM-specific atlas right-angle conclusion still
requires the parent row's upstream supply, but the geometric implication
itself is now audit-able as a standalone primitive.
