# Cycle 25 Claim Status Certificate — Half-Plane Chart Equivalence Narrow Theorem (Pattern A)

**Block:** physics-loop/half-plane-chart-equivalence-narrow-block25-20260502
**Note:** docs/HALF_PLANE_CHART_EQUIVALENCE_NARROW_THEOREM_NOTE_2026-05-02.md
**Runner:** scripts/frontier_half_plane_chart_equivalence_narrow.py (PASS=14/0)
**Parent row carved from:** dm_neutrino_source_surface_active_half_plane_theorem_note_2026-04-16 (claim_type=positive_theorem, audit_status=audited_conditional, td=131, load_bearing_step_class=A)

## Block type

**Pattern A — narrow rescope as new claim row.** This block introduces a new
audit-pending positive_theorem candidate row by isolating the load-bearing
class-(A) algebraic core of the parent DM-neutrino source-surface active
half-plane theorem.

The narrow theorem states only the pure two-variable real-algebra
equivalence: for any positive constant `c > 0`, the parametric map
`(delta, r) -> (delta, c - delta + sqrt(r^2 - 1/4))` on `r >= 1/2` bijects
its domain with the closed half-plane `q >= c - delta`, with explicit
inverse chart `r = sqrt((q - c + delta)^2 + 1/4)`.

The narrow note has **zero** ledger dependencies because the constant `c`
enters as an abstract positive parameter, and no DM-neutrino-specific
source-surface upstream is consumed.

## Claim-Type Certificate

```yaml
target_claim_type: positive_theorem
proposed_claim_scope: |
  Pure algebraic / inverse-chart equivalence: the parametric map
  f(delta, r) = (delta, c - delta + sqrt(r^2 - 1/4)) on r >= 1/2
  bijects with the closed half-plane q >= c - delta, with explicit
  inverse g(delta, q) = (delta, sqrt((q - c + delta)^2 + 1/4)). The
  framework instance c = sqrt(8/3) is one concrete case; the
  implication holds for any c > 0.
proposed_load_bearing_step_class: A
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## 7-criteria check

| # | Criterion | Pass? |
|---|---|---|
| 1 | target_claim_type named | YES (`positive_theorem`) |
| 2 | No open imports for the claimed target | YES (zero ledger deps; `c > 0` is a hypothesis, not a ledger import) |
| 3 | No load-bearing observed/fitted/admitted | YES (purely two-variable real algebra; no PDG / literature / fitted / admitted-convention input) |
| 4 | Every dep retained-grade | YES (vacuously — zero deps) |
| 5 | Runner verifies the algebraic identity at exact precision | YES (sympy symbolic image inclusion; symbolic `g compose f = id`; symbolic `f compose g = id` on H_c; boundary correspondence; monotonicity; three concrete rational instances; framework instance `c = sqrt(8/3)`) |
| 6 | Review-loop disposition | proposed pass as audit-pending narrow theorem; independent audit pending |
| 7 | PR body says independent audit required | YES |

## Cited deps

(none) — the narrow theorem is dep-free. The parametric map and the
constant `c > 0` are stated; no DM-neutrino source-surface authority is
consumed.

## Explicitly NOT cited (intentional narrowing)

The parent row's five upstream deps are all dropped:

- `dm_neutrino_source_surface_shift_quotient_bundle_theorem_note_2026-04-16`
- `dm_neutrino_source_surface_carrier_normal_form_theorem_note_2026-04-16`
- `dm_neutrino_source_surface_m_spectator_theorem_note_2026-04-16`
- `dm_neutrino_source_surface_intrinsic_slot_theorem_note_2026-04-16`
- `dm_neutrino_source_surface_slot_torsion_boundary_theorem_note_2026-04-16`

These five upstream theorems carry the DM-neutrino source-surface-specific
construction that produces the specific parametric formula
`q_+ = sqrt(8/3) - delta + sqrt(r31^2 - 1/4)`. The narrow theorem here
parametrizes over the abstract constant `c`, so none of the five upstream
constructions is needed to state or prove the chart equivalence.

## What this proposes

A new audit-pending positive_theorem candidate carving out the
purely-algebraic core of the parent
`dm_neutrino_source_surface_active_half_plane_theorem_note_2026-04-16`.
The narrow theorem can be ratified independently of any DM-neutrino
source-surface authority because it has zero ledger dependencies.

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.

## Audit-graph effect

If independent audit ratifies this row, downstream lanes that need only
the chart equivalence (parametric `(delta, r)` <-> half-plane `(delta, q)`
bijection) can re-target this narrow theorem without waiting on any of
the five DM-neutrino source-surface upstreams. The DM-neutrino-specific
significance of the half-plane domain still requires the parent row's
source-surface construction, but the chart equivalence itself becomes
audit-able as a standalone primitive.
