# Unit-Singlet Overlap Narrow Theorem

**Date:** 2026-05-02
**Type:** positive_theorem
**Claim scope:** the standalone combinatorial / Wick-algebra identity that,
given positive integers `N_iso, N_c` and the unit-normalized scalar-singlet
operator `H_unit = (1 / sqrt(N_iso * N_c)) * sum_{alpha, a} E_{alpha, a}` on
the `(N_iso * N_c)`-dimensional pair-Hilbert space (with `E_{alpha, a}` the
elementary diagonal Wick contractor on basis pair `(alpha, a)`), the
tree-level matrix element with any single basis pair-state is
`1 / sqrt(N_iso * N_c)`. The result is identically independent of any
gauge-coupling parameter because `H_unit` has no gauge-field content in its
definition. This is purely combinatorial; no Wolfenstein, gauge-vacuum, or
Ward-identity authority is consumed, and no specific physical assignment of
`(N_iso, N_c)` is claimed.
**Status:** audit pending. Under the scope-aware classification framework,
`effective_status` is computed by the audit pipeline from `audit_status` +
`claim_type` + dependency chain; no author-side tier is asserted in source.
Audit-lane ratification is required before any retained-grade status applies.
**Runner:** [`scripts/frontier_unit_singlet_overlap_narrow.py`](./../scripts/frontier_unit_singlet_overlap_narrow.py)
**Authority role:** Pattern A narrow rescope of the load-bearing combinatorial
core of [`G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19`](G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md).

## Statement

Let `N_iso, N_c` be positive integers, and let

```text
H_unit  =  (1 / sqrt(N_iso * N_c)) * I_{N_iso * N_c}
```

be the operator on the `(N_iso * N_c)`-dimensional pair-Hilbert space
spanned by basis pair-states `|alpha, a>` with `1 <= alpha <= N_iso` and
`1 <= a <= N_c`. (Equivalently, `H_unit = (1 / sqrt(N_iso * N_c)) *
sum_{alpha, a} |alpha, a><alpha, a|` in the diagonal Wick-contractor basis.)

Then, for any basis pair-state `|alpha_0, a_0>`, the tree-level matrix
element is

```text
F_overlap  :=  <0 | H_unit | tbar_{alpha_0, a_0} t_{alpha_0, a_0}>_tree
            =  1 / sqrt(N_iso * N_c).                                       (T1)
```

Moreover, `F_overlap` is identically **independent** of any gauge-coupling
parameter, because `H_unit` has no gauge-field content in its definition
(it is purely the diagonal sum of basis-pair Wick contractors, normalized
by `1 / sqrt(N_iso * N_c)`).

## Proof

By definition of `H_unit` and the canonical normalization of the
basis-pair states `|alpha_0, a_0>`,

```text
<basis pair (alpha_0, a_0) | H_unit | basis pair (alpha_0, a_0)>
  =  (1 / sqrt(N_iso * N_c)) * <basis pair (alpha_0, a_0) | basis pair (alpha_0, a_0)>
  =  (1 / sqrt(N_iso * N_c)) * 1
  =  1 / sqrt(N_iso * N_c).
```

The factor `1` is the canonical norm of the pair state. The factor
`1 / sqrt(N_iso * N_c)` is the explicit normalization of `H_unit` from its
definition. No gauge-field operator appears anywhere in this calculation.

`(T1)` is therefore an exact combinatorial identity, independent of any
auxiliary parameter that does not appear in `H_unit`. ∎

## What this claims

- The overlap identity `(T1)` for any positive integers `(N_iso, N_c)` and
  any basis pair `(alpha_0, a_0)`.
- The framework instance `(N_iso, N_c) = (2, 3)` gives
  `F_overlap = 1 / sqrt(6)`.
- The result is identically independent of any gauge-coupling parameter
  `g_bare` at tree order.

## What this does NOT claim

- Does **not** derive `H_unit`'s normalization from the free-theory
  two-point function residue. The narrow theorem states the operator
  definition explicitly. Whether the normalization arises from the residue
  argument is the load-bearing content of [`YT_WARD_IDENTITY_DERIVATION_THEOREM`](YT_WARD_IDENTITY_DERIVATION_THEOREM.md),
  whose audit status is decided by the audit lane on that row.
- Does **not** identify `(N_iso, N_c) = (2, 3)` with any specific physical
  Standard-Model assignment.
- Does **not** claim that the parent's `g_bare = 1` selection is forced by
  the same-`Gamma^(4)` coefficient identity. That is the load-bearing
  content of [`G_BARE_TWO_WARD_SAME_1PI_PINNING_THEOREM_NOTE_2026-04-19`](G_BARE_TWO_WARD_SAME_1PI_PINNING_THEOREM_NOTE_2026-04-19.md).
- Does **not** consume any PDG observed value, literature numerical
  comparator, fitted selector, or admitted unit convention.

## Relation to the parent g_bare two-Ward Rep-B independence note

[`G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19`](G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md) bundles
three components:

1. The operator-normalization identity `Z^2 = N_c * N_iso = 6`, derived
   from the free-theory two-point function residue (depends on
   `YT_WARD_IDENTITY_DERIVATION_THEOREM`).
2. The combinatorial / group-theory overlap `<top-pair | S> = 1 / sqrt(6)`.
3. The structural QFT statement that `H_unit` at tree order has no
   gauge-coupling insertion.

The audit-lane verdict on the parent row is `audited_conditional` because
component (1) imports the unratified `YT_WARD_IDENTITY_DERIVATION_THEOREM`
upstream.

This narrow theorem isolates components (2)-(3) from component (1). The
operator definition (and hence the normalization) is **stated** rather
than derived. The combinatorial overlap and the gauge-coupling
independence then follow directly from the operator's definition.

## Cited dependencies

None. This narrow note has zero ledger dependencies because it states the
operator `H_unit` as an explicit definition and derives the overlap
identity by direct evaluation in the Wick-contractor basis.

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.

## Validation

Primary runner: [`scripts/frontier_unit_singlet_overlap_narrow.py`](./../scripts/frontier_unit_singlet_overlap_narrow.py)
verifies (PASS=19/0):

1. Framework instance `(N_iso, N_c) = (2, 3)`: at every basis pair
   `(alpha_0, a_0)` the matrix element evaluates to `1 / sqrt(6)`.
2. Alternative instance `(N_iso, N_c) = (3, 4)`: `F = 1 / sqrt(12)` for
   each basis pair.
3. Degenerate instance `(N_iso, N_c) = (1, 1)`: `F = 1`.
4. Explicit 6x6 matrix-form verification at the framework instance
   (`H_unit = (1 / sqrt(6)) * I_6`, diagonal element `1 / sqrt(6)`,
   off-diagonal `0`).
5. Symbolic verification that the matrix element contains no `g_bare`
   parameter (gauge-coupling independence).
6. Parent row's `load_bearing_step_class == 'A'` ledger check.

## Cross-references

- [`G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19`](G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md) —
  parent bundled note that combines this overlap identity with the
  free-theory two-point function residue argument and the structural
  QFT no-gauge-insertion fact.
- [`YT_WARD_IDENTITY_DERIVATION_THEOREM`](YT_WARD_IDENTITY_DERIVATION_THEOREM.md) —
  upstream authority for the operator-normalization derivation, which
  this narrow note does not consume.
