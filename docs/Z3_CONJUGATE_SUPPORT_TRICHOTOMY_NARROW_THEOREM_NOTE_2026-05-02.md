# Z_3 Conjugate-Pair Support Trichotomy Narrow Theorem

**Date:** 2026-05-02
**Type:** positive_theorem
**Claim scope:** the standalone Z_3 character-arithmetic identity that, for
any permutation `q_L` of `Z_3 = {0, 1, 2}` with pointwise conjugate `q_R = -q_L
mod 3`, the support of the bilinear constraint `q_L_i + q_H + q_R_j ≡ 0 mod 3`
on a 3x3 grid is a permutation pattern, and over `q_H ∈ {0, 1, 2}` the three
supports are pairwise disjoint and cover the full grid (and equal the
diagonal/forward-cycle/backward-cycle patterns in some order). This is purely
a fact of finite-group / Z_3-character arithmetic; no DM-neutrino /
charged-fermion / Higgs-doublet authority is consumed, and no specific
physical assignment of the charges is claimed.
**Status:** audit pending. Under the scope-aware classification framework,
`effective_status` is computed by the audit pipeline from `audit_status` +
`claim_type` + dependency chain; no author-side tier is asserted in source.
Audit-lane ratification is required before any retained-grade status applies.
**Runner:** [`scripts/frontier_z3_conjugate_support_trichotomy_narrow.py`](./../scripts/frontier_z3_conjugate_support_trichotomy_narrow.py)
**Authority role:** Pattern A narrow rescope of the load-bearing class-(A)
algebraic core of [`NEUTRINO_DIRAC_Z3_SUPPORT_TRICHOTOMY_NOTE`](NEUTRINO_DIRAC_Z3_SUPPORT_TRICHOTOMY_NOTE.md).

## Statement

Let `q_L = (q_L_1, q_L_2, q_L_3)` be a permutation of `Z_3 = {0, 1, 2}`
(i.e., the three values are distinct mod 3), and let `q_R = (q_R_1, q_R_2,
q_R_3)` be its pointwise conjugate `q_R_i = -q_L_i mod 3`. For any
`q_H ∈ Z_3`, define

```text
S(q_L, q_R, q_H)  =  { (i, j) ∈ {1, 2, 3}^2 : q_L_i + q_H + q_R_j ≡ 0 mod 3 }.
```

**Conclusion (T1).** `S` is a **permutation pattern**: it has exactly one
entry per row and one per column.

**Conclusion (T2).** Over `q_H ∈ {0, 1, 2}`, the three supports
`S(q_L, q_R, 0)`, `S(q_L, q_R, 1)`, `S(q_L, q_R, 2)` are **pairwise
disjoint**, and their **union is the full 3x3 grid**.

**Conclusion (T3).** The three supports are exactly the **diagonal**, the
**forward cyclic**, and the **backward cyclic** permutation patterns, in
some order determined by the permutation `q_L`.

## Proof

`(T1)` Fix `q_H ∈ Z_3`. For each row `i ∈ {1, 2, 3}`, the constraint
`q_L_i + q_H + q_R_j ≡ 0 mod 3` becomes a linear equation in `q_R_j`,
namely `q_R_j ≡ -(q_L_i + q_H) mod 3`. Since `q_R` is a permutation of
`Z_3` (it is the pointwise negation of the permutation `q_L`, hence still
a bijection from rows to `Z_3`), there is exactly one column `j(i)`
solving this equation. So each row contributes exactly one entry to `S`,
and dually each column contributes exactly one. Hence `|S| = 3` and `S`
is a permutation pattern.

`(T2)` For any `(i, j)` in the full 3x3 grid, the value `q_L_i + q_R_j`
is some element of `Z_3`. Setting `q_H = -(q_L_i + q_R_j) mod 3` puts
`(i, j)` into `S(q_L, q_R, q_H)`. So every grid point is in exactly one
support (the one with `q_H` chosen as above), proving disjointness +
cover.

`(T3)` Each of the three permutation patterns (diagonal, forward cycle,
backward cycle) is a permutation pattern, and there are exactly three
permutation patterns of `{1, 2, 3} -> {1, 2, 3}` whose union covers the
3x3 grid disjointly. By `(T2)` the three supports give such a triple of
patterns, so they must coincide with `{diagonal, forward cycle, backward
cycle}` as sets of patterns. The order in which these three patterns
appear over `q_H ∈ {0, 1, 2}` depends on the specific permutation `q_L`.
For the framework instance `q_L = (0, +1, -1)` (= `(0, 1, 2)` mod 3), the
order is: `q_H = 0 → diagonal`, `q_H = +1 → forward cycle`, `q_H = -1 →
backward cycle`. ∎

## What this claims

- `(T1)`: support is a permutation pattern, for any permutation `q_L` of
  `Z_3` and any `q_H ∈ Z_3`.
- `(T2)`: pairwise disjointness and cover over `q_H ∈ {0, 1, 2}`.
- `(T3)`: identification of the three patterns with diagonal/forward/
  backward cyclic patterns.

## What this does NOT claim

- Does **not** identify `q_L`, `q_R`, or `q_H` with any specific physical
  generation/Higgs charge assignment. The narrow theorem treats them as
  abstract `Z_3`-valued symbols.
- Does **not** derive the "single Higgs doublet with definite `Z_3`
  charge" hypothesis. That premise is a framework-specific input to the
  parent application and is admitted-context here only as a use-case
  description.
- Does **not** claim any neutrino-Yukawa, Dirac-lane, or charged-fermion
  significance for the resulting permutation patterns. These applications
  belong to the parent note.
- Does **not** consume any PDG observed value, literature numerical
  comparator, fitted selector, or admitted unit convention.

## Distinct-Z_3-values hypothesis is essential

At constant `q_L = (0, 0, 0)` (so `q_R = (0, 0, 0)`), the constraint
becomes `q_H ≡ 0 mod 3`. At `q_H = 0` the support is the **full 3x3
grid** (9 entries, not a permutation pattern). At `q_H ∈ {1, 2}` the
support is **empty**. The trichotomy fails. The runner verifies this
explicitly as Part 4 of the validation, confirming that the
distinct-Z_3-values hypothesis on `q_L` is necessary, not decorative.

## Relation to the parent neutrino Dirac Z_3 support trichotomy note

[`NEUTRINO_DIRAC_Z3_SUPPORT_TRICHOTOMY_NOTE`](NEUTRINO_DIRAC_Z3_SUPPORT_TRICHOTOMY_NOTE.md) bundles this
abstract Z_3-character arithmetic with three framework-specific inputs:

1. The retained generation charges `q_L = (0, +1, -1)`, `q_R = (0, -1, +1)`.
2. The reduction of the neutrino-mass problem to the Dirac-Yukawa lane.
3. The "single Higgs doublet with definite `Z_3` charge `q_H`" hypothesis.

Per the parent's audit-verdict-narrowed status (2026-04-28), all three are
explicitly admitted-context. The parent applies the abstract trichotomy to
this specific instance to produce a bounded conditional theorem.

This narrow theorem isolates the abstract Z_3-character arithmetic from
the framework-specific inputs. The trichotomy can be ratified independently
of any DM-neutrino, generation-charge, or Higgs-doublet authority.

## Cited dependencies

None. This narrow note has zero ledger dependencies because it states
only elementary Z_3-character arithmetic on abstract permutation triples.
The framework instance `q_L = (0, +1, -1), q_R = (0, -1, +1)` is one of
the 6 permutations of `(0, 1, 2)`.

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.

## Validation

Primary runner: [`scripts/frontier_z3_conjugate_support_trichotomy_narrow.py`](./../scripts/frontier_z3_conjugate_support_trichotomy_narrow.py)
verifies (PASS=13/0):

1. Framework instance at `q_L = (0, +1, -1), q_R = (0, -1, +1)`: at
   `q_H = 0` support is diagonal; at `q_H = +1` support is forward
   cyclic; at `q_H = -1` support is backward cyclic.
2. Each support at framework instance is a permutation pattern.
3. The three supports are pairwise disjoint and cover the full 3x3 grid.
4. **Distinct-Z_3-values hypothesis is essential:** at constant
   `q_L = (0, 0, 0)`, support at `q_H = 0` is the full grid (not a
   permutation), and supports at `q_H = 1, 2` are empty.
5. All 6 permutations of `(0, 1, 2)` for `q_L` give exactly the set
   `{diagonal, forward cycle, backward cycle}` over `q_H ∈ {0, 1, 2}`.
6. Parent row's `load_bearing_step_class == 'A'` ledger check.

## Cross-references

- [`NEUTRINO_DIRAC_Z3_SUPPORT_TRICHOTOMY_NOTE`](NEUTRINO_DIRAC_Z3_SUPPORT_TRICHOTOMY_NOTE.md) —
  parent bundled note that applies the abstract trichotomy to the
  framework's specific generation/Higgs `Z_3` charge assignment, producing
  a bounded conditional theorem on the neutrino Dirac Yukawa support.
