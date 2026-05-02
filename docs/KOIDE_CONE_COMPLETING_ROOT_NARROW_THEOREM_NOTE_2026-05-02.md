# Koide-Cone Completing-Root Narrow Theorem

**Date:** 2026-05-02
**Type:** positive_theorem
**Claim scope:** the standalone polynomial-algebra identity that, for any
abstract positive reals `v, w`, the pair of explicit roots
`u_{small,large}(v, w) = 2(v + w) ∓ sqrt(3 (v^2 + 4 v w + w^2))` are the
unique two values of `u` placing `(u, v, w)` on the Koide cone
`u^2 + v^2 + w^2 = 4(u v + u w + v w)`. Each root satisfies the cone
identically, and Vieta's relations hold. This is purely a fact of
quadratic-formula polynomial algebra; no Koide / charged-lepton mass /
sqrt(m) / selected-line `H_sel(m)` framework input is consumed.
**Status:** audit pending. Under the scope-aware classification framework,
`effective_status` is computed by the audit pipeline from `audit_status` +
`claim_type` + dependency chain; no author-side tier is asserted in source.
Audit-lane ratification is required before any retained-grade status applies.
**Runner:** [`scripts/frontier_koide_cone_completing_root_narrow.py`](./../scripts/frontier_koide_cone_completing_root_narrow.py)
**Authority role:** Pattern A narrow rescope of the load-bearing class-(A)
algebraic core of [`KOIDE_SCALE_SELECTOR_REPARAMETERIZATION_THEOREM_NOTE_2026-04-20`](KOIDE_SCALE_SELECTOR_REPARAMETERIZATION_THEOREM_NOTE_2026-04-20.md).

## Statement

Let `v, w > 0`. Define

```text
u_small(v, w)  =  2 (v + w)  -  sqrt(3 (v^2 + 4 v w + w^2)),               (1)
u_large(v, w)  =  2 (v + w)  +  sqrt(3 (v^2 + 4 v w + w^2)).               (2)
```

**Conclusion (T1).** `u_small` and `u_large` are the two roots of the
quadratic in `u`

```text
u^2  -  4(v + w) u  +  (v^2 + w^2 - 4 v w)  =  0,                          (3)
```

obtained by rearranging the Koide-cone equation
`u^2 + v^2 + w^2 = 4(u v + u w + v w)` as a quadratic in `u`.

**Conclusion (T2).** Each root satisfies the cone identically:

```text
(u_{small/large})^2 + v^2 + w^2  =  4 (u_{small/large} v + u_{small/large} w + v w).
```

**Conclusion (T3).** Vieta's relations:

```text
u_small + u_large  =  4 (v + w),
u_small * u_large  =  v^2 + w^2 - 4 v w.
```

**Conclusion (T4).** At the small root, the standard Koide ratio holds:

```text
(u_small^2 + v^2 + w^2) / (u_small + v + w)^2  =  2/3.                     (4)
```

**Conclusion (T5).** `u_small > 0` iff `|v - 2 w| > w sqrt(3)`. So
positivity holds in regimes like `(v, w) = (4, 1)` but not at the
uniform point `(v, w) = (1, 1)` (where `u_small = 4 - 3 sqrt(2) < 0`).

## Proof

`(T1)` Direct: rearranging `(u_small_or_large)^2 - 4(v+w)(u_small_or_large) + (v^2 + w^2 - 4 v w) = 0`
into the standard quadratic-formula form gives discriminant
`16(v+w)^2 - 4(v^2 + w^2 - 4 v w) = 12 (v^2 + 4 v w + w^2)`, with
`sqrt(12 (v^2 + 4 v w + w^2)) = 2 sqrt(3 (v^2 + 4 v w + w^2))`.

`(T2)` Direct identity check (verified at exact precision in the runner).

`(T3)` Standard Vieta on the quadratic in `(3)`.

`(T4)` From the cone identity `(T2)` plus the algebraic equivalence
between the cone form and the ratio form (cf. cycle 43 narrow theorem),
the ratio at `(u_small, v, w)` equals `2/3` exactly.

`(T5)` Setting `u_small > 0` and squaring (allowed since both sides
non-negative) gives `4(v+w)^2 > 3(v^2 + 4 v w + w^2)`, equivalently
`v^2 - 4 v w + w^2 > 0`. Treating this as a quadratic in `v` with `w`
fixed, the discriminant is `16 w^2 - 4 w^2 = 12 w^2`, so the roots are
`v = 2w +/- w sqrt(3)`. The quadratic is positive outside `[2w - w sqrt(3), 2w + w sqrt(3)]`,
i.e., when `|v - 2w| > w sqrt(3)`. ∎

## What this claims

- `(T1)`-`(T5)` for any positive real `(v, w)`.

## What this does NOT claim

- Does **not** identify `(u_small, v, w)` with charged-lepton
  sqrt-mass amplitudes.
- Does **not** consume the upstream selected-line `H_sel(m)` framework,
  the native-vs-completed slot distinction, or any specific physical
  point identification.
- Does **not** consume any PDG observed value, literature numerical
  comparator, fitted selector, or admitted unit convention.

## Relation to the parent Koide scale-selector reparameterization note

[`KOIDE_SCALE_SELECTOR_REPARAMETERIZATION_THEOREM_NOTE_2026-04-20`](KOIDE_SCALE_SELECTOR_REPARAMETERIZATION_THEOREM_NOTE_2026-04-20.md)
applies this completing-root identity to the selected-line context to
argue that `u_small v w = 1` is a Koide-completed reparameterization
condition rather than a native pre-Koide forcing law. Per the audit
verdict on the parent row, the selected-line H_sel(m) inputs and the
near-miss / physical-point comparisons depend on unregistered
conditional inputs.

This narrow theorem isolates the underlying polynomial-algebra
completing-root identity from the selected-line framework. The
algebra-only content can be ratified independently of any selected-line
authority.

## Cited dependencies

None. This narrow note has zero ledger dependencies because it states
only elementary polynomial algebra on positive real `(v, w)`.

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.

## Validation

Primary runner: [`scripts/frontier_koide_cone_completing_root_narrow.py`](./../scripts/frontier_koide_cone_completing_root_narrow.py)
verifies (PASS=10/0):

1. Roots of `u^2 - 4(v+w) u + (v^2 + w^2 - 4 v w) = 0` match
   `{u_small, u_large}` exact.
2. `u_small` satisfies the cone identity exact (symbolic).
3. `u_large` satisfies the cone identity exact (symbolic).
4. Vieta sum: `u_small + u_large = 4(v + w)` exact.
5. Vieta product: `u_small * u_large = v^2 + w^2 - 4 v w` exact.
6. Standard Koide ratio at `u_small`: `(sum sq)/(sum)^2 = 2/3` exact.
7. Concrete `(v, w) = (1, 1)`: `u_small = 4 - 3 sqrt(2)`,
   `u_large = 4 + 3 sqrt(2)` exact.
8. Positivity regime: `u_small > 0` at `(v, w) = (4, 1)`, < 0 at `(1, 1)`.
9. Parent row class-A check.

## Cross-references

- [`KOIDE_SCALE_SELECTOR_REPARAMETERIZATION_THEOREM_NOTE_2026-04-20`](KOIDE_SCALE_SELECTOR_REPARAMETERIZATION_THEOREM_NOTE_2026-04-20.md) —
  parent bundled note that applies this completing-root identity to the
  selected-line context.
- [`KOIDE_CONE_THREE_FORM_EQUIVALENCE_NARROW_THEOREM_NOTE_2026-05-02`](KOIDE_CONE_THREE_FORM_EQUIVALENCE_NARROW_THEOREM_NOTE_2026-05-02.md) —
  sister Pattern A narrow theorem (cycle 43) covering the three-form
  equivalence on the same Koide cone (orbit-slot, cyclic basis-change,
  and standard ratio forms).
