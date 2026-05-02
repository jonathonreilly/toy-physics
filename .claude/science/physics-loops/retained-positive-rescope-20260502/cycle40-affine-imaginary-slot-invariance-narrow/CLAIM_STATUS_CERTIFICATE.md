# Cycle 40 Claim Status Certificate — Affine Imaginary-Slot Invariance Narrow Theorem (Pattern A)

**Block:** physics-loop/affine-imaginary-slot-invariance-narrow-block40-20260502
**Note:** docs/AFFINE_IMAGINARY_SLOT_INVARIANCE_NARROW_THEOREM_NOTE_2026-05-02.md
**Runner:** scripts/frontier_affine_imaginary_slot_invariance_narrow.py (PASS=24/0)
**Parent row carved from:** dm_neutrino_source_surface_active_affine_point_selection_boundary_note_2026-04-16 (claim_type=positive_theorem, audit_status=audited_conditional, td=130, load_bearing_step_class=A)

## Block type

**Pattern A — narrow rescope as new claim row.** New audit-pending
positive_theorem candidate carving out the load-bearing class-(A)
Hermitian-matrix-algebra core: trace structure + imaginary-slot
invariance under the explicit affine generators `T_m, T_delta, T_q`.

Zero ledger dependencies — three matrices explicitly defined, `H_base`
abstract Hermitian.

## Claim-Type Certificate

```yaml
target_claim_type: positive_theorem
proposed_claim_scope: |
  Pure Hermitian-matrix algebra: trace structure (Tr(T_m)=1,
  Tr(T_delta)=Tr(T_q)=0, hence Tr(H) = Tr(H_base) + m) plus
  imaginary-slot invariance Im(H_ij) = Im(H_base_ij) under the
  affine generators T_m, T_delta, T_q (all real-symmetric). Linear
  independence of the three generators over R.
proposed_load_bearing_step_class: A
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## 7-criteria check

| # | Criterion | Pass? |
|---|---|---|
| 1 | target_claim_type named | YES (`positive_theorem`) |
| 2 | No open imports | YES (zero ledger deps; matrices defined explicitly; H_base abstract Hermitian) |
| 3 | No load-bearing observed/fitted/admitted | YES (purely linear algebra) |
| 4 | Every dep retained-grade | YES (vacuously — zero deps) |
| 5 | Runner verifies at exact precision | YES (sympy `Matrix`, `Rational`, exact rank check, exact trace, exact Im check, framework-instance verification) |
| 6 | Review-loop disposition | proposed pass as audit-pending narrow theorem |
| 7 | PR body says independent audit required | YES |

## Cited deps

(none) — three matrices explicitly defined by their entries; `H_base`
is abstract Hermitian.

## Explicitly NOT cited (intentional narrowing)

The parent's five upstream DM-neutrino source-surface deps are dropped:
- active half-plane theorem (covered by cycle 25's Pattern A);
- m-spectator theorem;
- intrinsic-slot theorem;
- slot-torsion-boundary theorem;
- shift-quotient bundle theorem.

## Audit-graph effect

If independent audit ratifies this row, downstream lanes that need only
the affine-imaginary-slot-invariance algebra can re-target this narrow
theorem without invoking DM-neutrino source-surface upstreams. The
DM-side identification of `(delta, q_+)` as the minimal mainline datum
still requires the parent's five upstream authorities, but the
underlying linear-algebra content becomes audit-able as a standalone
primitive.

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.

## What this proposes

A new audit-pending positive_theorem candidate carving out the
purely-algebraic core of the parent
`dm_neutrino_source_surface_active_affine_point_selection_boundary_note_2026-04-16`.
The narrow theorem can be ratified independently because it has zero
ledger dependencies.
