# Hermitian-Circulant Response Master Identity Narrow Theorem

**Date:** 2026-05-02
**Type:** positive_theorem
**Claim scope:** the standalone linear-algebra identity that, for the
Hermitian circulant family `G(g_0, g_1) = g_0 I + g_1 C + g_1_bar C^2`
on `M_3(C)` and the cyclic basis `B_0 = I, B_1 = C + C^2, B_2 = i(C - C^2)`,
the Frobenius-pairing responses `r_i = Re Tr(G B_i)` evaluate to
`(r_0, r_1, r_2) = (3 g_0, 6 Re g_1, 6 Im g_1)` and the master identity
`2 r_0^2 - (r_1^2 + r_2^2) = 18 (g_0^2 - 2 |g_1|^2)` holds exactly. Hence
the Koide cone `2 r_0^2 = r_1^2 + r_2^2` is exactly equivalent to the
one-scalar equation `kappa := g_0^2 / |g_1|^2 = 2`. This is purely a
fact of linear algebra; no Koide / charged-lepton / observable-principle
/ second-order-return framework input is consumed.
**Status:** audit pending. Under the scope-aware classification framework,
`effective_status` is computed by the audit pipeline from `audit_status` +
`claim_type` + dependency chain; no author-side tier is asserted in source.
Audit-lane ratification is required before any retained-grade status applies.
**Runner:** [`scripts/frontier_circulant_response_master_identity_narrow.py`](./../scripts/frontier_circulant_response_master_identity_narrow.py)
**Authority role:** Pattern A narrow rescope of the load-bearing class-(A)
algebraic core of [`KOIDE_ONE_SCALAR_OBSTRUCTION_TRIANGULATION_THEOREM_NOTE_2026-04-18`](KOIDE_ONE_SCALAR_OBSTRUCTION_TRIANGULATION_THEOREM_NOTE_2026-04-18.md).

## Statement

Let `C` be the 3x3 cyclic permutation matrix on `C^3` (`C e_k = e_{k+1 mod 3}`),
so that `C^3 = I_3`, `Tr(C) = Tr(C^2) = 0`, `Tr(C^3) = 3`. Define the
Hermitian circulant family

```text
G(g_0, g_1)  =  g_0 I  +  g_1 C  +  conjugate(g_1) C^2,                    (1)
                  g_0 ∈ R, g_1 ∈ C.
```

With cyclic basis `B_0 = I`, `B_1 = C + C^2`, `B_2 = i (C - C^2)` (all Hermitian
on `M_3(C)`), define the Frobenius-pairing responses

```text
r_0  =  Re Tr(G B_0),
r_1  =  Re Tr(G B_1),                                                       (2)
r_2  =  Re Tr(G B_2).
```

**Conclusion (T1).** The responses evaluate to

```text
r_0  =  3 g_0,
r_1  =  6 Re(g_1),                                                          (3)
r_2  =  6 Im(g_1).
```

**Conclusion (T2) (master identity).**

```text
2 r_0^2  -  (r_1^2 + r_2^2)  =  18 (g_0^2  -  2 |g_1|^2).                  (4)
```

**Conclusion (T3) (Koide cone reduction).** The condition `2 r_0^2 = r_1^2 + r_2^2`
is exactly equivalent to `g_0^2 = 2 |g_1|^2`, i.e., to the one-scalar equation
`kappa := g_0^2 / |g_1|^2 = 2`.

## Proof

`(T1)` Direct trace computation:

- `Tr(G B_0) = Tr(G) = g_0 Tr(I) + g_1 Tr(C) + g_1_bar Tr(C^2) = 3 g_0` (using
  `Tr(C) = Tr(C^2) = 0`). Real part: `r_0 = 3 g_0`.

- `Tr(G B_1) = Tr(G C) + Tr(G C^2)`. Compute `Tr(G C) = g_0 Tr(C) + g_1 Tr(C^2)
  + g_1_bar Tr(C^3) = 0 + 0 + 3 g_1_bar = 3 g_1_bar`. Similarly
  `Tr(G C^2) = 3 g_1`. So `Tr(G B_1) = 3 (g_1 + g_1_bar) = 6 Re(g_1)`.
  Real part: `r_1 = 6 Re(g_1)`.

- `Tr(G B_2) = i (Tr(G C) - Tr(G C^2)) = i (3 g_1_bar - 3 g_1) = -6 Im(g_1) i^2 / ...`
  Wait: `i (3 g_1_bar - 3 g_1) = 3 i (g_1_bar - g_1) = 3 i \cdot (-2 i Im(g_1))
  = 6 Im(g_1)`. Real part: `r_2 = 6 Im(g_1)`.

`(T2)` Direct substitution into `(T1)`:

```text
2 r_0^2 - (r_1^2 + r_2^2)
  =  2 (3 g_0)^2  -  ((6 Re g_1)^2 + (6 Im g_1)^2)
  =  18 g_0^2  -  36 ((Re g_1)^2 + (Im g_1)^2)
  =  18 g_0^2  -  36 |g_1|^2
  =  18 (g_0^2 - 2 |g_1|^2).
```

`(T3)` From `(T2)`, `2 r_0^2 = r_1^2 + r_2^2` iff `18 (g_0^2 - 2 |g_1|^2) = 0`
iff `g_0^2 = 2 |g_1|^2`. ∎

## What this claims

- `(T1)`-`(T3)` for any choice of real `g_0` and complex `g_1`.

## What this does NOT claim

- Does **not** identify `(g_0, g_1)` with any specific physical Koide /
  charged-lepton / observable-principle response. The narrow theorem
  treats them as abstract scalar parameters.
- Does **not** consume the upstream A0–A3 axiom base of the parent (the
  Cl(3)/Z^3 axiom, the retained `hw=1` triplet, the observable-principle
  scalar generator, the second-order-return shape).
- Does **not** consume any PDG observed value, literature numerical
  comparator, fitted selector, or admitted unit convention.

## Relation to the parent one-scalar obstruction triangulation note

[`KOIDE_ONE_SCALAR_OBSTRUCTION_TRIANGULATION_THEOREM_NOTE_2026-04-18`](KOIDE_ONE_SCALAR_OBSTRUCTION_TRIANGULATION_THEOREM_NOTE_2026-04-18.md)
applies this master identity to the Koide / charged-lepton context with
`G = D^{-1}` for a `Cl(3)/Z^3`-covariant retained Hermitian source `D`.
Per the audit verdict, the upstream A1 (retained `hw=1` triplet), A2
(observable principle), A3 (second-order return shape), and the three
"independent triangulation routes" cited in the parent are admitted-context
inputs from upstream authorities not currently registered in the ledger
under the cited paths.

This narrow theorem isolates the underlying linear-algebra master identity
from the Koide-specific framing. The identity can be ratified
independently of any upstream authority.

## Cited dependencies

None. This narrow note has zero ledger dependencies because it states
only elementary linear algebra on the Hermitian-circulant family and
the cyclic basis.

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.

## Validation

Primary runner: [`scripts/frontier_circulant_response_master_identity_narrow.py`](./../scripts/frontier_circulant_response_master_identity_narrow.py)
verifies (PASS=17/0):

1. `C^3 = I` exact, `Tr(C) = Tr(C^2) = 0`, `Tr(C^3) = 3`.
2. `G` is Hermitian (symbolic in `g_0, g_1_re, g_1_im`).
3. `B_0, B_1, B_2` Hermitian.
4. `r_0 = 3 g_0`, `r_1 = 6 g_1_re`, `r_2 = 6 g_1_im` symbolic.
5. Master identity `(T2)` symbolic.
6. Cone reduction `(T3)`: at `g_0 = sqrt(2) |g_1|`, LHS = 0 exact.
7. Concrete instance `(g_1_re, g_1_im) = (1/3, 1/5)` on cone gives kappa = 2.
8. Trace identities used in derivation (Tr(C·C^2) = 3, etc.).
9. Parent row class-A check.

## Cross-references

- [`KOIDE_ONE_SCALAR_OBSTRUCTION_TRIANGULATION_THEOREM_NOTE_2026-04-18`](KOIDE_ONE_SCALAR_OBSTRUCTION_TRIANGULATION_THEOREM_NOTE_2026-04-18.md) —
  parent bundled note that applies this master identity to the
  Koide / charged-lepton context.
- [`CYCLIC_PROJECTOR_COMPRESSION_NARROW_THEOREM_NOTE_2026-05-02`](CYCLIC_PROJECTOR_COMPRESSION_NARROW_THEOREM_NOTE_2026-05-02.md) —
  sister Pattern A narrow theorem (cycle 28) covering the orthogonal
  projector `P_cyc` onto the cyclic-invariant subspace of `Herm(3)`,
  spanned by the same `{B_0, B_1, B_2}` basis used here.
