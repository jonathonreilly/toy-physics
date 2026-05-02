# Cycle 34 Claim Status Certificate — Hermitian Circulant Parity + CP-Tensor Narrow Theorem (Pattern A)

**Block:** physics-loop/circulant-parity-cp-tensor-narrow-block34-20260502
**Note:** docs/CIRCULANT_PARITY_CP_TENSOR_NARROW_THEOREM_NOTE_2026-05-02.md
**Runner:** scripts/frontier_circulant_parity_cp_tensor_narrow.py (PASS=14/0)
**Parent row carved from:** dm_neutrino_odd_circulant_z2_slot_theorem_note_2026-04-15 (claim_type=positive_theorem, audit_status=audited_conditional, td=111, load_bearing_step_class=C)

## Block type

**Pattern A — narrow rescope as new claim row.** This block introduces a new
audit-pending positive_theorem candidate row by isolating the load-bearing
class-(C) linear-algebra core of the parent DM-neutrino odd-circulant Z_2
slot theorem.

The narrow theorem states only:

- the residual-Z_2 transposition `P_{23}` swaps `S ↔ S^2` on the 3x3
  cyclic permutation matrix;
- on the Hermitian circulant family `K = d I + c_even (S + S^2) + i c_odd (S
  - S^2)`, the parity decomposition sends `c_odd → -c_odd` while leaving
  `d, c_even` invariant;
- `Im[(K_{01})^2] = 2 c_even c_odd` exact (CP-tensor formula);
- `c_odd = 0 ⇒ Im[(K_{01})^2] = 0` (CP vanishing on even-only sector).

The narrow note has **zero** ledger dependencies because it states
elementary linear algebra on 3x3 Hermitian circulants.

## Claim-Type Certificate

```yaml
target_claim_type: positive_theorem
proposed_claim_scope: |
  Pure linear algebra on 3x3 Hermitian circulants and the residual-Z_2
  transposition: parity-decomposition of the (d, c_even, c_odd) basis,
  P_{23} K P_{23} sends c_odd -> -c_odd, exact CP-tensor formula
  Im[(K_{01})^2] = 2 c_even c_odd. No DM-side / Wilson / weak-axis /
  two-Higgs / CP-tensor-readout framing.
proposed_load_bearing_step_class: C
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## 7-criteria check

| # | Criterion | Pass? |
|---|---|---|
| 1 | target_claim_type named | YES (`positive_theorem`) |
| 2 | No open imports for the claimed target | YES (zero ledger deps; the matrices `S`, `P_{23}` are defined explicitly; `(d, c_even, c_odd)` are abstract real symbols) |
| 3 | No load-bearing observed/fitted/admitted | YES (purely linear algebra; no PDG / literature / fitted / admitted-convention input) |
| 4 | Every dep retained-grade | YES (vacuously — zero deps) |
| 5 | Runner verifies the algebraic identity at exact precision | YES (sympy `Matrix`, `Rational`, exact symbolic checks for `P_{23} S P_{23} = S^2`, parity-decomposition of basis, CP-tensor formula `Im[(K_{01})^2] = 2 c_even c_odd`, CP-vanishing at `c_odd = 0`, concrete instance `(1, 1/3, 1/5)`) |
| 6 | Review-loop disposition | proposed pass as audit-pending narrow theorem; independent audit pending |
| 7 | PR body says independent audit required | YES |

## Cited deps

(none) — the narrow theorem is dep-free; matrices and parameters are
defined explicitly.

## Explicitly NOT cited (intentional narrowing)

The parent's authority-stack inputs are dropped:

- **DM minimal Z_3 circulant CP tool** — replaced by the abstract
  Hermitian-circulant family parametrization.
- **Two-Higgs right-Gram bridge** — not needed; `K` is treated as an
  abstract Hermitian circulant.
- **Exact weak-axis `1+2` split** — not needed; the parity-decomposition
  + CP-tensor formula hold for any `(d, c_even, c_odd) ∈ R^3`.
- **Standard CP tensor readout** — replaced by the explicit identity
  `Im[(K_{01})^2] = 2 c_even c_odd`.

## What this proposes

A new audit-pending positive_theorem candidate carving out the
purely-algebraic core of the parent
`dm_neutrino_odd_circulant_z2_slot_theorem_note_2026-04-15`. The narrow
theorem can be ratified independently of any DM-side / Wilson / weak-axis
authority because it has zero ledger dependencies.

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.

## Audit-graph effect

If independent audit ratifies this row, downstream lanes that need only
the circulant parity decomposition + CP-tensor formula
`Im[(K_{01})^2] = 2 c_even c_odd` can re-target this narrow theorem
without invoking DM-neutrino, two-Higgs, weak-axis, or other
framework-specific upstreams. The DM-side identification of the unique
odd slot still requires the parent's authority-stack inputs, but the
underlying linear-algebra identity becomes audit-able as a standalone
primitive reusable across any Hermitian-circulant CP analysis.
