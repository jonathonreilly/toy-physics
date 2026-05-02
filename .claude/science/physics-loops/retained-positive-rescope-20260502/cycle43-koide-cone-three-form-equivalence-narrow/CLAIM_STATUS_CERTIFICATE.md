# Cycle 43 Claim Status Certificate — Koide-Cone Three-Form Equivalence Narrow Theorem (Pattern A)

**Block:** physics-loop/koide-cone-three-form-equivalence-narrow-block43-20260502
**Note:** docs/KOIDE_CONE_THREE_FORM_EQUIVALENCE_NARROW_THEOREM_NOTE_2026-05-02.md
**Runner:** scripts/frontier_koide_cone_three_form_equivalence_narrow.py (PASS=11/0)
**Parent row carved from:** koide_gamma_orbit_selector_bridge_note_2026-04-18 (claim_type=positive_theorem, audit_status=audited_conditional, td=74, load_bearing_step_class=A)

## Block type

**Pattern A — narrow rescope as new claim row.** New audit-pending
positive_theorem candidate carving out the load-bearing class-(A)
polynomial-algebra equivalence:

- F_orbit = 4(uv + uw + vw) - (u^2 + v^2 + w^2);
- F_cyclic = 2 r0^2 - r1^2 - r2^2 (with linear basis change);
- F_ratio = (u^2 + v^2 + w^2)/(u + v + w)^2 - 2/3.

All three are pairwise equivalent on R^3, with the algebraic identity
F_cyclic = 2 F_orbit holding for ALL (u, v, w).

Zero ledger dependencies — (u, v, w) abstract real symbols, linear
basis-change defined explicitly.

## Claim-Type Certificate

```yaml
target_claim_type: positive_theorem
proposed_claim_scope: |
  Pure polynomial-algebra three-form equivalence on R^3 between
  (F_orbit), (F_cyclic), and (F_ratio) forms of the Koide cone.
  Treats (u, v, w) as abstract real symbols; no physical mass
  identification.
proposed_load_bearing_step_class: A
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## 7-criteria check

| # | Criterion | Pass? |
|---|---|---|
| 1 | target_claim_type named | YES (`positive_theorem`) |
| 2 | No open imports | YES (zero ledger deps; (u, v, w) abstract; linear map explicit) |
| 3 | No load-bearing observed/fitted/admitted | YES (purely polynomial algebra) |
| 4 | Every dep retained-grade | YES (vacuously — zero deps) |
| 5 | Runner verifies at exact precision | YES (sympy `Rational`, `simplify`, `expand`, `solve`; symbolic identity verified plus concrete cone-on / cone-off instances) |
| 6 | Review-loop disposition | proposed pass as audit-pending narrow theorem |
| 7 | PR body says independent audit required | YES |

## Cited deps

(none) — three forms expressed in terms of abstract `(u, v, w)` and the
explicit linear basis-change `(r0, r1, r2)`.

## Explicitly NOT cited (intentional narrowing)

- **Gamma/orbit-return law** that produces the physical orbit-slot
  triple `(u, v, w)` from charged-lepton dynamics (parent row's
  unaudited upstream).
- **Cyclic basis identity** derivation `(u, v, w) → (r0, r1, r2)`
  on the C_3 representation — the linear map enters here as an
  explicit definition.
- **Charged-lepton sqrt-mass identification** `(u, v, w) = (sqrt(m_e), sqrt(m_mu), sqrt(m_tau))`.

## Audit-graph effect

If independent audit ratifies this row, downstream lanes that need only
the algebraic three-form equivalence can re-target this narrow theorem
without invoking Gamma/orbit-return / charged-lepton / sqrt-mass
upstreams. The Koide-physical interpretation still requires the
parent's upstream authorities, but the polynomial-algebra equivalence
itself becomes audit-able as a standalone primitive.

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.

## What this proposes

A new audit-pending positive_theorem candidate carving out the
purely-algebraic core of the parent
`koide_gamma_orbit_selector_bridge_note_2026-04-18`. Zero ledger
dependencies; ratifiable independently of any Koide-side authority.
