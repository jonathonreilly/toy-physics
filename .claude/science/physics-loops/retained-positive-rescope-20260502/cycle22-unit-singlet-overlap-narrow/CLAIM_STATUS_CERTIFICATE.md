# Cycle 22 Claim Status Certificate — Unit-Singlet Overlap Narrow Theorem (Pattern A)

**Block:** physics-loop/g-bare-rep-b-overlap-narrow-block22-20260502
**Note:** docs/UNIT_SINGLET_OVERLAP_NARROW_THEOREM_NOTE_2026-05-02.md
**Runner:** scripts/frontier_unit_singlet_overlap_narrow.py (PASS=19/0)
**Parent row carved from:** g_bare_two_ward_rep_b_independence_theorem_note_2026-04-19 (claim_type=positive_theorem, audit_status=audited_conditional, td=292, load_bearing_step_class=A)

## Block type

**Pattern A — narrow rescope as new claim row.** This block introduces a new
audit-pending positive_theorem candidate row by isolating the load-bearing
combinatorial / Wick-algebra core of the parent g_bare two-Ward Rep-B
independence note from the upstream `YT_WARD_IDENTITY_DERIVATION_THEOREM`
operator-normalization derivation.

The narrow theorem states that, given an explicit definition of the
unit-normalized scalar-singlet operator `H_unit = (1 / sqrt(N_iso * N_c)) *
I_{N_iso * N_c}` on the diagonal Wick-contractor basis, the tree-level
matrix element with any basis pair-state is exactly `1 / sqrt(N_iso * N_c)`,
identically independent of any gauge-coupling parameter.

The narrow note has **zero** ledger dependencies because the operator
definition enters as a definitional input (not a derivation from the
free-theory two-point function residue).

## Claim-Type Certificate

```yaml
target_claim_type: positive_theorem
proposed_claim_scope: |
  Pure combinatorial / Wick-algebra implication: given positive integers
  (N_iso, N_c) and the explicit operator H_unit defined in the diagonal
  Wick-contractor basis, the tree-level matrix element with any basis
  pair-state is 1/sqrt(N_iso * N_c). Identically independent of any
  gauge-coupling parameter. The framework instance (N_iso, N_c) = (2, 3)
  giving F = 1/sqrt(6) is one concrete case; the algebra closes for any
  positive integer pair.
proposed_load_bearing_step_class: A
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## 7-criteria check

| # | Criterion | Pass? |
|---|---|---|
| 1 | target_claim_type named | YES (`positive_theorem`) |
| 2 | No open imports for the claimed target | YES (zero ledger deps; H_unit operator definition is stated, not derived from upstream) |
| 3 | No load-bearing observed/fitted/admitted | YES (purely combinatorial; no PDG / literature / fitted / admitted-convention input) |
| 4 | Every dep retained-grade | YES (vacuously — zero deps) |
| 5 | Runner verifies the algebraic identity at exact precision | YES (sympy `Rational`, `sqrt`, `Matrix`, `eye`; framework instance (2,3); alternative instance (3,4); degenerate (1,1); explicit 6x6 matrix verification; gauge-coupling independence symbolic check) |
| 6 | Review-loop disposition | proposed pass as audit-pending narrow theorem; independent audit pending |
| 7 | PR body says independent audit required | YES |

## Cited deps

(none) — the narrow theorem is dep-free; the operator `H_unit` is defined
explicitly. The framework instance `(N_iso, N_c) = (2, 3)` is shown as a
special case.

## Explicitly NOT cited (intentional narrowing)

- `yt_ward_identity_derivation_theorem` — parent row's unratified upstream
  that supplies the free-theory two-point function residue argument
  forcing `Z^2 = N_c * N_iso = 6`. Dropped by stating the operator
  `H_unit` definition explicitly with the `1 / sqrt(N_iso * N_c)`
  normalization built in.

## What this proposes

A new audit-pending positive_theorem candidate carving out the
combinatorial / Wick-algebra core of the parent
`g_bare_two_ward_rep_b_independence_theorem_note_2026-04-19`. The narrow
theorem can be ratified independently of any upstream Ward-identity
authority because it has zero ledger dependencies.

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.

## Audit-graph effect

If independent audit ratifies this row, downstream lanes that need only
the combinatorial overlap identity `F = 1 / sqrt(N_iso * N_c)` and its
gauge-coupling independence at tree order can re-target this narrow
theorem without waiting on `YT_WARD_IDENTITY_DERIVATION_THEOREM`. The
parent's full g_bare-independence claim still requires the operator
normalization argument from the upstream, but the combinatorial overlap
itself becomes audit-able as a standalone primitive.
