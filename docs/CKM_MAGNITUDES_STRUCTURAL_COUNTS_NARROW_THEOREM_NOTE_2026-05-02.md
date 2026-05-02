# CKM Magnitudes Structural-Counts Narrow Theorem

**Date:** 2026-05-02
**Type:** positive_theorem
**Claim scope:** the standalone algebraic-substitution implication that, given
the four parametric input identities for `lambda^2`, `A^2`, `rho^2 + eta^2`,
`(1 - rho)^2 + eta^2` plus the count constraint `n_quark = n_pair * n_color`,
the five Wolfenstein-leading squared off-diagonal CKM-style magnitudes
`(|V_us|_0^2, |V_cb|_0^2, |V_ts|_0^2, |V_ub|_0^2, |V_td|_0^2)` are forced
closed-form expressions in `(alpha_s, n_pair, n_color, n_quark)`. This is
purely a statement about algebraic substitution; no atlas/Wolfenstein/CP-phase
authority is consumed, no value of `alpha_s` is supplied or assumed, no
physical-CKM identification is claimed, and no PDG comparator enters.
**Status:** audit pending. Under the scope-aware classification framework,
`effective_status` is computed by the audit pipeline from `audit_status` +
`claim_type` + dependency chain; no author-side tier is asserted in source.
Audit-lane ratification is required before any retained-grade status applies.
**Runner:** [`scripts/frontier_ckm_magnitudes_structural_counts_narrow.py`](./../scripts/frontier_ckm_magnitudes_structural_counts_narrow.py)
**Authority role:** Pattern A narrow rescope of the load-bearing algebraic core
of [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md).

## Statement

Let `alpha_s, lambda, A, rho, eta, n_pair, n_color, n_quark` be abstract
positive symbols satisfying the four parametric input identities

```text
lambda^2                  =  alpha_s / n_pair,
A^2                       =  n_pair / n_color,
rho^2 + eta^2             =  1 / n_quark,
(1 - rho)^2 + eta^2       =  (n_quark - 1) / n_quark,
```

together with the integer-counts constraint

```text
n_quark  =  n_pair * n_color.
```

Then the five Wolfenstein-leading squared off-diagonal CKM-style magnitudes
are the closed-form expressions

```text
|V_us|_0^2  =  alpha_s / n_pair,                                          (M1)
|V_cb|_0^2  =  alpha_s^2 / (n_pair * n_color),                            (M2)
|V_ts|_0^2  =  alpha_s^2 / (n_pair * n_color),                            (M3)
|V_ub|_0^2  =  alpha_s^3 / (n_pair^3 * n_color^2),                        (M4)
|V_td|_0^2  =  (n_quark - 1) * alpha_s^3 / (n_pair^3 * n_color^2).        (M5)
```

The framework-specific instance `(n_pair, n_color, n_quark) = (2, 3, 6)`
gives the concrete numerical readouts

```text
|V_us|_0^2  =  alpha_s / 2,
|V_cb|_0^2  =  alpha_s^2 / 6,
|V_ub|_0^2  =  alpha_s^3 / 72,
|V_td|_0^2  =  5 * alpha_s^3 / 72.
```

This special case is shown for sanity, not as a load-bearing input. The
algebra also closes for any other count tuple that satisfies the same
parametric input identities (e.g. `(3, 4, 12)` is verified in the runner).

## Proof

Pure substitution.

`(M1)`. `|V_us|_0^2 = lambda^2 = alpha_s / n_pair` by the first input
identity.

`(M2)`, `(M3)`. `|V_cb|_0^2 = |V_ts|_0^2 = A^2 lambda^4`. Substitute:

```text
A^2 lambda^4  =  (n_pair / n_color) * (alpha_s / n_pair)^2
              =  alpha_s^2 / (n_pair * n_color).
```

`(M4)`. `|V_ub|_0^2 = A^2 lambda^6 (rho^2 + eta^2)`. Substitute:

```text
A^2 lambda^6 (rho^2 + eta^2)
  =  (n_pair / n_color) * (alpha_s / n_pair)^3 * (1 / n_quark)
  =  alpha_s^3 / (n_pair^2 * n_color * n_quark).
```

Apply `n_quark = n_pair * n_color` to get

```text
|V_ub|_0^2  =  alpha_s^3 / (n_pair^3 * n_color^2).
```

`(M5)`. `|V_td|_0^2 = A^2 lambda^6 ((1 - rho)^2 + eta^2)`. Substitute:

```text
A^2 lambda^6 ((1-rho)^2 + eta^2)
  =  (n_pair / n_color) * (alpha_s / n_pair)^3 * ((n_quark - 1) / n_quark)
  =  (n_quark - 1) * alpha_s^3 / (n_pair^2 * n_color * n_quark).
```

Apply `n_quark = n_pair * n_color`:

```text
|V_td|_0^2  =  (n_quark - 1) * alpha_s^3 / (n_pair^3 * n_color^2).
```

∎

## Derivable corollaries

```text
|V_cb|_0^2 / |V_us|_0^2  =  alpha_s / n_color   (= A^2 lambda^2)
|V_td|_0^2 / |V_ub|_0^2  =  n_quark - 1         (purely combinatorial ratio)
```

Both follow algebraically from `(M1)`-`(M5)`.

## What this claims

- The closed-form expressions `(M1)`-`(M5)` for the five Wolfenstein-leading
  squared off-diagonal CKM-style magnitudes, **conditional on** the four
  parametric input identities and the count constraint.
- Two derived ratio identities that follow algebraically.
- The framework-specific `(n_pair, n_color, n_quark) = (2, 3, 6)` reduces
  these to the rational closed forms `(alpha_s/2, alpha_s^2/6, alpha_s^2/6,
  alpha_s^3/72, 5 alpha_s^3/72)`.

## What this does NOT claim

- Does **not** derive `lambda^2 = alpha_s / n_pair`, `A^2 = n_pair / n_color`,
  `rho^2 + eta^2 = 1/n_quark`, or the Thales relation
  `(1-rho)^2 + eta^2 = (n_quark - 1)/n_quark`. Those are CKM atlas/Wolfenstein
  / CP-phase / Thales authorities carried by separate notes (specifically
  [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md),
  [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md),
  and [`CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24`](CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md)),
  whose audit status is decided by the audit lane on those rows.
- Does **not** supply or claim any value of `alpha_s`. `alpha_s` is treated
  as an abstract positive symbol; no [`ALPHA_S_DERIVED_NOTE`](ALPHA_S_DERIVED_NOTE.md)
  authority is consumed.
- Does **not** identify the framework's `(n_pair, n_color, n_quark)` with any
  physical Standard-Model assignment.
- Does **not** consume any PDG observed value, literature numerical
  comparator, fitted selector, or admitted unit convention.
- Does **not** claim `n_quark = n_pair * n_color` is forced; it is a
  hypothesis on the count tuple, supplied by the framework's count surface
  but not derived here.

## Relation to the parent CKM magnitudes structural-counts note

[`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md) bundles
the algebraic substitution above with several distinct downstream items:

1. The parametric input identities themselves, supplied by the unratified
   atlas/Wolfenstein/CP-phase/Thales authorities.
2. The canonical `alpha_s(v) = 0.103303...` value supplied by an audit-pending
   `ALPHA_S_DERIVED_NOTE` chain.
3. PDG comparators `|V_us|^2 = 5.031e-2` etc. for downstream observable
   matching.
4. The pure algebraic substitution (M1)-(M5).

The audit-lane verdict on the parent row is `audited_conditional` because
items 1-3 are unratified upstream / audit-comparator-only inputs.

This narrow theorem isolates item 4 from items 1-3. The four input parametric
identities enter as hypotheses; `alpha_s` is an abstract symbol; no PDG
comparator appears. The algebraic substitution can be ratified independently
of any CKM-specific upstream.

## Cited dependencies

None. This narrow note has zero ledger dependencies because it states only
algebraic substitution on abstract positive symbols satisfying the four
parametric input identities and the count constraint.

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.

## Validation

Primary runner: [`scripts/frontier_ckm_magnitudes_structural_counts_narrow.py`](./../scripts/frontier_ckm_magnitudes_structural_counts_narrow.py)
verifies (PASS=16/0):

1. Each of `(M1)`-`(M5)` reduces by sympy `simplify` to the claimed
   closed-form expression in `(alpha_s, n_pair, n_color, n_quark)`.
2. The two corollary ratios reduce to the claimed forms.
3. The framework-specific `(2, 3, 6)` instance reproduces the rational
   closed forms `(alpha_s/2, alpha_s^2/6, alpha_s^3/72, 5 alpha_s^3/72)`.
4. The non-framework `(3, 4, 12)` instance reproduces the corresponding
   rational closed forms `(alpha_s/3, alpha_s^2/12, alpha_s^3/432,
   11 alpha_s^3/432)`, confirming independence from the framework count
   choice.
5. Parent row's `load_bearing_step_class == 'A'` ledger check.

## Cross-references

- [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md) — parent
  bundled note that supplies the parametric input identities, `alpha_s` value,
  and PDG comparators.
- [`THALES_RIGHT_ANGLE_NARROW_THEOREM_NOTE_2026-05-02`](THALES_RIGHT_ANGLE_NARROW_THEOREM_NOTE_2026-05-02.md) — sister
  Pattern A narrow theorem carving out the geometric implication used in
  deriving `(1-rho)^2 + eta^2 = (n_quark-1)/n_quark` from `rho^2 + eta^2 =
  1/n_quark`.
