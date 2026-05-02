# Cycle 49 Claim Status Certificate — Koide-Cone Completing-Root Narrow Theorem (Pattern A)

**Block:** physics-loop/koide-cone-completing-root-narrow-block49-20260502
**Note:** docs/KOIDE_CONE_COMPLETING_ROOT_NARROW_THEOREM_NOTE_2026-05-02.md
**Runner:** scripts/frontier_koide_cone_completing_root_narrow.py (PASS=10/0)
**Parent row carved from:** koide_scale_selector_reparameterization_theorem_note_2026-04-20 (claim_type=positive_theorem, audit_status=audited_conditional, td=69, load_bearing_step_class=A)

## Block type

**Pattern A — narrow rescope as new claim row.** New audit-pending
positive_theorem candidate carving out the load-bearing class-(A) algebraic
core: explicit `u_{small,large}` roots of the Koide-cone quadratic
satisfy the cone identically with Vieta relations.

Zero ledger dependencies — `(v, w)` abstract positive reals; explicit
quadratic-formula roots.

## Claim-Type Certificate

```yaml
target_claim_type: positive_theorem
proposed_claim_scope: |
  Pure polynomial algebra: explicit closed-form roots
  u_{small,large}(v, w) = 2(v+w) ∓ sqrt(3 (v^2 + 4 v w + w^2)) of the
  Koide-cone quadratic in u; both satisfy the cone exact; Vieta;
  standard ratio form 2/3 at u_small; positivity regime.
proposed_load_bearing_step_class: A
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## 7-criteria check

| # | Criterion | Pass? |
|---|---|---|
| 1 | target_claim_type named | YES (`positive_theorem`) |
| 2 | No open imports | YES (zero ledger deps; (v, w) abstract; explicit quadratic) |
| 3 | No load-bearing observed/fitted/admitted | YES (purely polynomial algebra) |
| 4 | Every dep retained-grade | YES (vacuously — zero deps) |
| 5 | Runner verifies at exact precision | YES (sympy Rational, sqrt, simplify, solve, expand; symbolic identity check + Vieta + concrete instances + positivity regime) |
| 6 | Review-loop disposition | proposed pass as audit-pending narrow theorem |
| 7 | PR body says independent audit required | YES |

## Cited deps

(none) — abstract `(v, w)` positive reals, explicit quadratic-formula roots.

## Explicitly NOT cited (intentional narrowing)

- **Selected-line `H_sel(m)` framework** that produces the parent's
  `v, w` from charged-lepton dynamics.
- **Native-vs-completed slot distinction**.
- **Physical-point near-miss / `m_*` selector inputs**.
- **Charged-lepton sqrt-mass identification**.

## Audit-graph effect

If independent audit ratifies this row, downstream lanes that need only
the algebraic Koide-cone completing-root identity can re-target this
narrow theorem without invoking selected-line / charged-lepton /
physical-point framework upstreams.

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.

## What this proposes

A new audit-pending positive_theorem candidate. Zero ledger dependencies;
ratifiable independently.
