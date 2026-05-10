# CKM CP-Phase Structural Trigonometric Narrow Theorem

**Date:** 2026-05-10
**Type:** positive_theorem
**Claim scope:** the standalone two-coordinate trigonometric and
monomial-algebraic identities on abstract real symbols `(rho, eta)`
and `(lambda, A, eta)` underlying the Wolfenstein CP-plane angle
`delta := arg(rho + i eta)` and the Jarlskog area factorisation
`J = lambda^6 A^2 eta`. This is purely a fact of trigonometry on
`R^2 \ {0}` plus monomial exponent algebra; no Cl(3), Z^3, CKM atlas,
quark-block projector split, alpha_s, Wolfenstein coordinate
identification, charged-lepton, or PDG observable is consumed.
**Status authority:** independent audit lane only. This source note
does not set or predict an audit outcome; later status is generated
by the audit pipeline after independent review.
**Runner:** [`scripts/frontier_ckm_cp_phase_structural_trig_narrow.py`](./../scripts/frontier_ckm_cp_phase_structural_trig_narrow.py)

## Statement

Let `(rho, eta)` be any abstract real pair with `rho > 0` and
`eta >= 0`, and let `r = sqrt(rho^2 + eta^2) > 0`. Define the
Wolfenstein-shape CP-plane angle

```text
delta := arg(rho + i eta)  =  atan2(eta, rho)  in  [0, pi/2].          (1)
```

Define the abstract weights

```text
w_A1   :=  rho^2 / (rho^2 + eta^2)  =  rho^2 / r^2,                     (2a)
w_perp :=  eta^2 / (rho^2 + eta^2)  =  eta^2 / r^2.                     (2b)
```

**Conclusion (T1) (cos-squared coordinate identity).** For all such
`(rho, eta)`,

```text
cos^2(delta)  =  rho^2 / (rho^2 + eta^2).                                (3)
```

**Conclusion (T2) (sin-squared coordinate identity).** For all such
`(rho, eta)`,

```text
sin^2(delta)  =  eta^2 / (rho^2 + eta^2).                                (4)
```

**Conclusion (T3) (tangent identity).** For all such `(rho, eta)`
with `rho > 0`,

```text
tan(delta)  =  eta / rho.                                                (5)
```

**Conclusion (T4) (weight-form rephrasing).** For all such `(rho, eta)`,

```text
w_A1 + w_perp  =  1,                                                     (6a)
cos^2(delta)   =  w_A1,                                                  (6b)
sin^2(delta)   =  w_perp,                                                (6c)
tan^2(delta)   =  w_perp / w_A1.                                         (6d)
```

**Conclusion (T5) (Jarlskog monomial factorisation identity).** For
all abstract real `(lambda, A, eta)` with `lambda > 0`,

```text
lambda^6 * A^2 * eta  =  (lambda^2)^3 * A^2 * eta.                       (7)
```

**Conclusion (T6) (rephasing-invariant arctangent / arccosine
equivalence on the principal branch).** For `(rho, eta)` with `rho > 0`
and `eta >= 0`,

```text
delta  =  arctan(eta / rho)  =  arccos( rho / sqrt(rho^2 + eta^2) ).     (8)
```

**Conclusion (T7) (cone is non-trivial).** The pair
`(rho, eta) = (1/6, sqrt(5)/6)` satisfies `r^2 = 1/6`, `cos^2(delta) = 1/6`,
`sin^2(delta) = 5/6`, `tan(delta) = sqrt(5)`, and
`delta = arccos(1/sqrt(6)) = arctan(sqrt(5))`. The pair
`(rho, eta) = (1, 0)` satisfies `delta = 0`, `cos^2(delta) = 1`,
`tan(delta) = 0`. The pair `(rho, eta) = (0, 1)` is excluded from `(T3)` /
`(T6)` (the `tan` form requires `rho > 0`), but `(T1)`, `(T2)`, `(T4)` still
hold and give `cos^2(delta) = 0`, `sin^2(delta) = 1`, `delta = pi/2`.

## Proof

`(T1), (T2), (T3)` Pure trigonometry. With `delta = atan2(eta, rho)`
on the open upper-right quadrant `rho > 0`, `eta >= 0`:

```text
cos(delta)  =  rho / r,
sin(delta)  =  eta / r,
where r = sqrt(rho^2 + eta^2) > 0.
```

Squaring gives `(T1)` and `(T2)` directly. Dividing `(T2)` by `(T1)` (or
forming `sin/cos`) gives `tan(delta) = eta/rho`, which is `(T3)`.
`atan2` is real-valued on the open quadrant and the chain of
identities is exact. ∎ (T1, T2, T3)

`(T4)` Direct substitution. Equation `(6a)` follows from
`w_A1 + w_perp = (rho^2 + eta^2)/(rho^2 + eta^2) = 1`. Equations `(6b)`
and `(6c)` are restatements of `(T1)` / `(T2)` after the substitution
`w_A1 := rho^2/r^2`, `w_perp := eta^2/r^2`. Equation `(6d)` follows from
`(T3)` squared: `tan^2(delta) = eta^2/rho^2 = (eta^2/r^2)/(rho^2/r^2) =
w_perp / w_A1`. ∎ (T4)

`(T5)` Monomial exponent algebra. `(lambda^2)^3 = lambda^(2*3) = lambda^6`
by the integer exponent law `(x^a)^b = x^(a*b)`. Therefore
`(lambda^2)^3 * A^2 * eta = lambda^6 * A^2 * eta`. ∎ (T5)

`(T6)` From `(T1)`, `cos(delta) = rho / sqrt(rho^2 + eta^2)` on the
principal branch where `delta in [0, pi/2]` and the cosine is
non-negative. So `delta = arccos(rho / sqrt(rho^2 + eta^2))`.
From `(T3)`, `delta = arctan(eta / rho)` on the same branch where
`rho > 0`. Both arccos and arctan agree on the open quadrant
`rho > 0`, `eta >= 0`, so the two expressions for `delta` are equal. ∎ (T6)

`(T7)` Direct verification. The runner checks each numerical
substitution exactly. ∎ (T7)

## What this claims

- `(T1)`: the symbolic identity `cos^2(delta) = rho^2 / (rho^2 + eta^2)`
  for all real `(rho, eta)` with `rho > 0`, `eta >= 0`.
- `(T2)`: the symbolic identity `sin^2(delta) = eta^2 / (rho^2 + eta^2)`
  on the same domain.
- `(T3)`: the symbolic identity `tan(delta) = eta / rho` on the same
  domain.
- `(T4)`: the four weight-form rephasings `(6a)`-`(6d)` after the
  substitution `w_A1 := rho^2/r^2`, `w_perp := eta^2/r^2`.
- `(T5)`: the symbolic identity `lambda^6 A^2 eta = (lambda^2)^3 A^2 eta`
  for all real `(lambda, A, eta)` with `lambda > 0`.
- `(T6)`: the principal-branch equivalence
  `arctan(eta/rho) = arccos(rho/sqrt(rho^2+eta^2))` on the open
  quadrant.
- `(T7)`: explicit non-trivial points on the identity surface, in
  particular the point `(rho, eta) = (1/6, sqrt(5)/6)` matching the
  parent-atlas readout `delta = arccos(1/sqrt(6))`.

## What this does NOT claim

- Does **not** identify `(rho, eta)` with the physical CKM
  CP-plane Wolfenstein coordinates produced by any specific
  framework derivation, atlas, projector split, or quark-block
  decomposition.
- Does **not** identify `delta` with the physical CKM CP phase
  `delta_CKM` as fixed by the Standard Model CKM matrix.
- Does **not** identify `(lambda, A)` with the physical Wolfenstein
  parameters produced by any specific framework derivation
  (`lambda^2 = alpha_s(v) / 2`, `A^2 = 2/3`, etc.).
- Does **not** identify `J = lambda^6 A^2 eta` with the physical
  Jarlskog invariant of the CKM matrix.
- Does **not** consume `r^2 = 1/6`, `w_A1 = 1/6`, or any other
  parent-atlas admission as a derivation input. The narrow
  theorem only states the algebraic identity that maps `(rho, eta)`
  to `delta` and the abstract Jarlskog-shape monomial factorisation;
  the parent atlas separately fixes the input values.
- Does **not** consume any Cl(3), Z^3, CKM atlas, quark-block
  projector split, alpha_s, charged-lepton, staggered-Dirac,
  three-generation, or PMNS authority.
- Does **not** consume any PDG observed value, literature
  numerical comparator, fitted selector, or admitted unit
  convention.

## Relation to the parent CKM CP-phase structural identity theorem

The parent note `CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`
uses the same trigonometric identity in the physical CKM atlas
context, identifying `(rho, eta)` with the physical Wolfenstein
CP-plane coordinates of the CKM matrix and reading `cos^2(delta) = 1/6`
as the structural CP-phase identity. The parent atlas separately
admits `r^2 = 1/6` (the bright/tensor CP radius), the `1 + 5`
center-excess projector split fixing `w_A1 = 1/6`, and `alpha_s(v)`
for the `J_0 = alpha_s(v)^3 sqrt(5)/72` factorisation. Those
physical-context inputs are admitted-context inputs that this
narrow note does not consume.

This narrow theorem isolates the underlying two-coordinate
trigonometric content (`(T1)`-`(T3)` plus the weight-form rephasing
`(T4)`) and the abstract Jarlskog monomial factorisation `(T5)` from
the physical CKM-atlas framing. The seven-fold conclusion above can
be ratified independently of any CKM atlas, projector-split,
alpha_s, or quark-block authority.

(Plain-text references in this section are pointers for readers,
not load-bearing upstream dependencies. Per PR #306 cleanup pattern,
markdown links to other notes in the body would be parsed as one-hop
upstream deps by the citation-graph builder, which is exactly what
this narrow theorem must avoid.)

## Cross-reference with prior narrow theorem on the same algebra

The sister narrow theorem
`KOIDE_CONE_THREE_FORM_EQUIVALENCE_NARROW_THEOREM_NOTE_2026-05-02.md`
addresses the equivalent extraction pattern for the Koide cone
three-form equivalence: strip the physical identification (Koide /
charged-lepton), keep only the elementary polynomial-algebra
equivalence on abstract `R^3`, ship as `positive_theorem` with
`deps: []`. The sister narrow theorem
`THREE_GENERATION_OBSERVABLE_M3C_BURNSIDE_NARROW_THEOREM_NOTE_2026-05-10.md`
performs the same extraction for the `M_3(C)` matrix-algebra core of
the three-generation observable theorem.

The present 2026-05-10 narrow theorem strips all physical-context
identifications from the parent CKM CP-phase structural identity
theorem and ships the elementary trigonometric and monomial-algebra
content as a `positive_theorem` with zero load-bearing upstream
dependencies. Pattern: strip the physical CKM atlas / projector /
alpha_s / charged-quark identifications, keep only the elementary
two-coordinate trigonometric identity on abstract `(rho, eta)`
and the elementary monomial exponent identity on abstract
`(lambda, A, eta)`, ship as `positive_theorem`.

## Cited dependencies

None. This narrow note has zero load-bearing dependencies because
it states only elementary two-coordinate trigonometry on abstract
`(rho, eta)` and elementary monomial exponent algebra on abstract
`(lambda, A, eta)`.

## Hypothesis set used

- standard real-variable trigonometry (universal mathematical
  infrastructure): `atan2`, `cos`, `sin`, `tan`, `arccos`, `arctan`
  on real arguments;
- the integer exponent law `(x^a)^b = x^(a*b)` for real `x > 0` and
  integer `a, b` (universal mathematical infrastructure).

Both are pure mathematical / arithmetic facts; no Cl(3), Z^3,
CKM atlas, projector-split, alpha_s, charged-lepton, staggered-Dirac,
three-generation, PMNS, or other framework hypothesis is consumed.

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.
- No Cl(3), Z^3, CKM atlas, projector-split, alpha_s, charged-lepton,
  staggered-Dirac, three-generation, PMNS, or quark-physics
  authorities consumed.

## Validation

Primary runner:
[`scripts/frontier_ckm_cp_phase_structural_trig_narrow.py`](./../scripts/frontier_ckm_cp_phase_structural_trig_narrow.py)
verifies at exact symbolic precision via sympy:

1. `(T1)` symbolic: `cos^2(atan2(eta, rho)) - rho^2/(rho^2 + eta^2) = 0`.
2. `(T2)` symbolic: `sin^2(atan2(eta, rho)) - eta^2/(rho^2 + eta^2) = 0`.
3. `(T3)` symbolic: `tan(atan2(eta, rho)) - eta/rho = 0` (assuming rho > 0).
4. `(T4a)` symbolic: `w_A1 + w_perp = 1` after substitution.
5. `(T4b)` symbolic: `cos^2(delta) - w_A1 = 0` after substitution.
6. `(T4c)` symbolic: `sin^2(delta) - w_perp = 0` after substitution.
7. `(T4d)` symbolic: `tan^2(delta) - w_perp/w_A1 = 0` after substitution.
8. `(T5)` symbolic: `lambda^6 A^2 eta - (lambda^2)^3 A^2 eta = 0`
   (monomial exponent identity).
9. `(T6)` symbolic: `arctan(eta/rho) - arccos(rho/sqrt(rho^2+eta^2)) = 0`
   on the open quadrant.
10. `(T7)` numerical, exact-rational: `(rho, eta) = (1/6, sqrt(5)/6)`
    gives `r^2 = 1/6`, `cos^2(delta) = 1/6`, `sin^2(delta) = 5/6`,
    `tan(delta) = sqrt(5)`, `delta = arccos(1/sqrt(6)) = arctan(sqrt(5))`.
11. `(T7)` boundary: `(rho, eta) = (1, 0)` gives `delta = 0`,
    `cos^2 = 1`, `tan = 0`.
12. `(T7)` boundary: `(rho, eta) = (0, 1)` excluded from `(T3)`;
    `(T1)`, `(T2)`, `(T4)` still hold and give `delta = pi/2`,
    `cos^2 = 0`, `sin^2 = 1`.
13. Forbidden-imports programmatic check: runner imports only
    `sympy`, no framework / audit / lattice modules.

Expected: PASS=N, FAIL=0.
