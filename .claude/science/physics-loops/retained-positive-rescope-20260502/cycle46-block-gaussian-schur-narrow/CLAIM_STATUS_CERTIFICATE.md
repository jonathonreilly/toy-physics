# Cycle 46 Claim Status Certificate — Block-Gaussian Schur Marginalization Narrow Theorem (Pattern A)

**Block:** physics-loop/block-gaussian-schur-narrow-block46-20260502
**Note:** docs/BLOCK_GAUSSIAN_SCHUR_MARGINALIZATION_NARROW_THEOREM_NOTE_2026-05-02.md
**Runner:** scripts/frontier_block_gaussian_schur_narrow.py (PASS=11/0)
**Parent row carved from:** yt_exact_coarse_grained_bridge_operator_note (claim_type=bounded_theorem, audit_status=audited_conditional, td=69, load_bearing_step_class=C)

## Block type

**Pattern A — narrow rescope as new claim row.** New audit-pending
positive_theorem candidate carving out the load-bearing class-(C) abstract
block-Gaussian Schur-marginalization formula:

  K_eff = A - B C^{-1} B^T,  J_eff = eta - B C^{-1} xi,
  det(K) = det(C) det(K_eff),
  associativity of sequential marginalization.

Zero ledger dependencies — abstract block matrix and source.

## Claim-Type Certificate

```yaml
target_claim_type: positive_theorem
proposed_claim_scope: |
  Pure linear algebra on real symmetric PD block matrices: completing
  the square gives K_eff = A - B C^{-1} B^T as the Schur complement,
  with positivity, symmetry, block-determinant identity, and
  associativity. No YT / Cl(3) / Grassmann / coarse-graining framing.
proposed_load_bearing_step_class: A
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## 7-criteria check

| # | Criterion | Pass? |
|---|---|---|
| 1 | target_claim_type named | YES (`positive_theorem`) |
| 2 | No open imports | YES (zero ledger deps; abstract block matrix) |
| 3 | No load-bearing observed/fitted/admitted | YES (purely linear algebra) |
| 4 | Every dep retained-grade | YES (vacuously — zero deps) |
| 5 | Runner verifies at exact precision | YES (sympy; concrete `(2+1)`-block instance + symbolic parametric over abstract `(a_ij, b_i, c)`; completing-the-square symbolic identity; block-determinant identity) |
| 6 | Review-loop disposition | proposed pass as audit-pending narrow theorem |
| 7 | PR body says independent audit required | YES |

## Cited deps

(none) — abstract block matrix and source defined explicitly.

## Explicitly NOT cited (intentional narrowing)

The parent's YT-bridge-stack admitted-context items are dropped:
- forced UV class;
- local affine selector;
- higher-order budget;
- nonlocal budget;
- endpoint-shift budget;
- Cl(3)/Z^3 framework / Grassmann finite-partition surface.

## Audit-graph effect

If independent audit ratifies this row, downstream lanes that need only
the block-Gaussian Schur marginalization can re-target this narrow
theorem without invoking YT / Cl(3) bridge-stack upstreams. The YT
bridge claim still requires the parent's framework-specific upstreams,
but the abstract Schur algebra becomes audit-able as a standalone
primitive.

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.

## What this proposes

A new audit-pending positive_theorem candidate carving out the
purely-algebraic core. Zero ledger dependencies; ratifiable
independently.
