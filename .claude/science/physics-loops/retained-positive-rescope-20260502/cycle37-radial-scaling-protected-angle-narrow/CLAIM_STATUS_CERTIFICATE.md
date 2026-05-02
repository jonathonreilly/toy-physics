# Cycle 37 Claim Status Certificate — Radial-Scaling Protected-Angle Narrow Theorem (Pattern A)

**Block:** physics-loop/radial-scaling-protected-angle-narrow-block37-20260502
**Note:** docs/RADIAL_SCALING_PROTECTED_ANGLE_NARROW_THEOREM_NOTE_2026-05-02.md
**Runner:** scripts/frontier_radial_scaling_protected_angle_narrow.py (PASS=10/0)
**Parent row carved from:** ckm_nlo_barred_triangle_protected_gamma_theorem_note_2026-04-25 (claim_type=positive_theorem, audit_status=audited_conditional, td=96, load_bearing_step_class=A)

## Block type

**Pattern A — narrow rescope as new claim row.** This block introduces a new
audit-pending positive_theorem candidate row by isolating the load-bearing
class-(A) plane-geometry / similar-triangles core of the parent CKM NLO
barred-triangle protected-gamma theorem.

The narrow theorem states only:

- a positive radial scaling `(rho, eta) -> (mu rho, mu eta)` preserves the
  slope `eta / rho` exactly, hence the angle at the origin is protected;
- the doubled-angle `(sin 2gamma, cos 2gamma)` is exactly preserved;
- the radial distance scales linearly as `mu`;
- the angle at `(1, 0)` is **not** in general preserved (only `mu = 1`
  preserves it).

The narrow note has **zero** ledger dependencies because it states elementary
plane geometry on abstract `(rho, eta, mu)` positive real symbols.

## Claim-Type Certificate

```yaml
target_claim_type: positive_theorem
proposed_claim_scope: |
  Pure plane geometry / similar-triangles identity: a positive radial
  scaling preserves the origin-angle and doubled-angle exactly, scales
  the radial distance linearly as mu, and does NOT in general preserve
  the angle at (1, 0). No CKM-specific input.
proposed_load_bearing_step_class: A
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## 7-criteria check

| # | Criterion | Pass? |
|---|---|---|
| 1 | target_claim_type named | YES (`positive_theorem`) |
| 2 | No open imports for the claimed target | YES (zero ledger deps; `(rho, eta, mu)` are abstract positive real symbols) |
| 3 | No load-bearing observed/fitted/admitted | YES (purely Euclidean geometry; no PDG / literature / fitted / admitted-convention input) |
| 4 | Every dep retained-grade | YES (vacuously — zero deps) |
| 5 | Runner verifies the algebraic identity at exact precision | YES (sympy `Rational`, `sqrt`, `simplify`, `atan`; symbolic slope preservation, arctan-equivalence, doubled-angle preservation, radial-distance scaling, counter-illustration of non-protection at `(1, 0)`, framework-instance verification) |
| 6 | Review-loop disposition | proposed pass as audit-pending narrow theorem; independent audit pending |
| 7 | PR body says independent audit required | YES |

## Cited deps

(none) — the narrow theorem is dep-free; `(rho, eta, mu)` enter as
abstract positive real symbols. The framework instance
`(rho, eta) = (1/6, sqrt(5)/6)` at NLO scaling is shown as one
application case.

## Explicitly NOT cited (intentional narrowing)

- **Wolfenstein `lambda^2 = alpha_s(v)/2, A^2 = 2/3`** — not consumed;
  the narrow theorem treats `mu` as abstract.
- **CP-phase `rho = 1/6, eta = sqrt(5)/6`** — not consumed; abstract
  `(rho, eta)`.
- **Atlas-triangle `alpha_0 = pi/2`** — not consumed; the narrow
  theorem makes no claim about origin/apex angles in any specific
  triangle.
- **Canonical `alpha_s(v)` value** — not consumed; abstract `mu`.
- **Textbook NLO Wolfenstein relation** `(rho_bar, eta_bar) = (rho, eta)(1
  - lambda^2/2)` — not consumed; the narrow theorem starts from the
  abstract radial scaling, not from any specific Wolfenstein expansion.

## What this proposes

A new audit-pending positive_theorem candidate carving out the
purely-geometric core of the parent
`ckm_nlo_barred_triangle_protected_gamma_theorem_note_2026-04-25`. The
narrow theorem can be ratified independently of any CKM / Wolfenstein
/ atlas-triangle / alpha_s upstream because it has zero ledger
dependencies.

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.

## Audit-graph effect

If independent audit ratifies this row, downstream lanes that need only
the radial-scaling protected-angle identity can re-target this narrow
theorem without invoking CKM-specific upstreams. The CKM-specific
NLO barred-triangle conclusions still require the parent's Wolfenstein /
CP-phase / atlas-triangle / alpha_s authorities, but the
protected-angle invariant itself becomes audit-able as a standalone
primitive reusable across any radial-scaling analysis.
