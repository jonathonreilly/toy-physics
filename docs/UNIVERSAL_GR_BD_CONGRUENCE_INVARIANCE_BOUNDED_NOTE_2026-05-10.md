# Universal-GR `B_D` Congruence-Invariance Trace Identity — Bounded Note

**Date:** 2026-05-10
**Claim type:** bounded_theorem
**Status authority:** source-note proposal only; audit verdict and
effective status are set by the independent audit lane.
**Primary runner:** [`scripts/frontier_universal_gr_bd_congruence_invariance.py`](../scripts/frontier_universal_gr_bd_congruence_invariance.py)

## Claim

Bounded note implementing the second of two repair-target options
named by the 2026-05-10 audit verdict on
`UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE.md`:

> *Repair target: add direct retained-grade dependency edges proving
> those inputs, **or split the pure trace identity into a separate
> clean algebraic row**.*

This note is the **split note for the pure trace identity**. It does
**not** claim the parent's bookkeeping consequence ("compatible local
stationary representatives patch compatibly into a global stationary
section"), and it does **not** import any of the parent's four
admitted-context hypotheses (atlas, transition cocycle, source/field
pairing covariance, operator nondegeneracy). The note claims only the
class-A algebraic identity that the parent's §"Audit boundary"
explicitly identifies as "closed in-note" linear algebra.

**Identity.** For finite-dimensional real square matrices `D, S, h, k`
of compatible dimension, with `D` and `S` invertible, define the
bilinear functional

```text
B_D ( h, k )   :=   - Tr ( D^{-1} · h · D^{-1} · k ).                     (1)
```

Define the congruence transformation under `S`:

```text
D'   :=   S^T · D · S,                                                    (2)
h'   :=   S^T · h · S,
k'   :=   S^T · k · S.
```

Then the identity

```text
B_{D'} ( h', k' )   =   B_D ( h, k )                                      (3)
```

holds **exactly** as a matrix-algebra identity over `R`.

**Proof** (one line, by cyclic trace and inverse-of-product):

```text
B_{D'} ( h', k' )
   =  - Tr ( ( S^T D S )^{-1} ( S^T h S ) ( S^T D S )^{-1} ( S^T k S ) )
   =  - Tr ( S^{-1} D^{-1} ( S^T )^{-1} · S^T h S · S^{-1} D^{-1} ( S^T )^{-1} · S^T k S )
   =  - Tr ( S^{-1} · D^{-1} · h · S · S^{-1} · D^{-1} · k · S )    [( S^T )^{-1} S^T = I]
   =  - Tr ( S^{-1} · D^{-1} h D^{-1} k · S )                  [S · S^{-1} = I]
   =  - Tr ( D^{-1} h D^{-1} k )                               [cyclic Tr: move S past]
   =  B_D ( h, k ).                                                       (4)
```

Equation (3) is the pure trace identity flagged by the parent note's
§"Audit boundary" as the in-note class-A claim. The runner verifies it
numerically at full numpy double-precision tolerance for sampled
random invertible `D, S` and arbitrary `h, k` of dimensions `4 × 4`
(matching the parent's `3 + 1` symmetric-coefficient setting) and
several other sizes (`2 × 2`, `3 × 3`, `5 × 5`, `8 × 8`).

## Bounded admissions

(BA-1) **Finite-dimensional real matrix algebra over `R`.** Cyclic
trace property `Tr(AB) = Tr(BA)` and the inverse-of-product identity
`(AB)^{-1} = B^{-1} A^{-1}` for invertible `A`, `B`. These are
elementary linear-algebra facts; the note admits them as bounded
textbook inputs rather than deriving them from the physical Cl(3)
local algebra plus Z^3 spatial substrate baseline.
This is an ordinary bounded import, not a new repo-wide axiom and not
a new interpretation of the physical Cl(3) local algebra plus Z^3
spatial substrate baseline.

(BA-1) is the only bounded admission. The note does **not** import any
of the parent's atlas / cocycle / nondegeneracy / pairing-covariance
hypotheses; those remain the parent's own load-bearing inputs on the
parent's audit ledger row.

## Proof-Walk

| Step | Argument | Load-bearing input |
|---|---|---|
| Eq. (2): congruence definition `D' = S^T D S`, etc. | definition | none |
| Apply `(AB)^{-1} = B^{-1} A^{-1}` to `( S^T D S )^{-1}` | (BA-1) inverse-of-product | (BA-1) |
| `( S^T )^{-1} S^T = I` simplifies inside the trace | (BA-1) elementary | (BA-1) |
| Cyclic permutation moves the leading `S^{-1}` past the trailing `S` | (BA-1) cyclic Tr property | (BA-1) |
| Result `B_{D'}(h',k') = B_D(h,k)` | direct substitution | none beyond (BA-1) |

Every load-bearing step is an elementary matrix-algebra fact in (BA-1).
The chain closes from (BA-1) plus eq. (2)'s definitional substitution.

## Exact Numerical Check

The runner verifies, at numpy double precision over multiple matrix
dimensions and sampled random matrices:

(A) **Invariance for `4 × 4` matrices** (matching the parent's `3 + 1`
symmetric-coefficient setting): random invertible `D, S` plus arbitrary
`h, k`; the residual `|B_{D'}(h',k') − B_D(h,k)|` is `< 10⁻¹⁰` over `100`
random trials.

(B) **Invariance across multiple dimensions**: same check at
`n × n` for `n ∈ {2, 3, 5, 8}` (different from the parent's primary
size, to confirm the identity is dimension-independent).

(C) **Conjugate-symmetry sanity**: `B_D(h, k) = B_D(k, h)` when
`D, h, k` are symmetric (a consequence of cyclic trace and symmetry of
inputs). This is a sanity check on (1), not a separate load-bearing
property.

(D) **Symmetric-input invariance**: when `h, k` are symmetric
matrices, the congruence-transformed `h', k'` also satisfy `B_{D'}(h',
k') = B_D(h, k)`. Confirms the parent's `3 + 1` symmetric-coefficient
use case.

(E) **Failure mode under partial transformation**: applying the
congruence to `D` alone (`D' = S^T D S`) but leaving `h, k`
untransformed gives `B_{D'}(h, k) ≠ B_D(h, k)` in general. The
runner verifies a sampled counterexample with `|B_D(h,k) −
B_{D'}(h,k)| ≫ 0` to confirm the identity requires the **full**
congruence on all three matrices `D, h, k`, not just on `D`. (Note:
applying a *consistent* similarity `D' = S D S^{-1}`, `h' = S h
S^{-1}`, `k' = S k S^{-1}` actually does preserve `B_D` by cyclic
Tr — that is a different, equally-trivial invariance, not a
counterexample. The substantive failure mode is the partial
transformation above.)

(F) **Forbidden-import audit**: imports limited to `numpy` plus stdlib.

## Provenance and Non-Dependencies

- `UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE.md` provides
  provenance only: this bounded note implements the 2026-05-10
  repair-target option (b) ("split the pure trace identity into a
  separate clean algebraic row") for the parent's class-A in-note
  content. The parent's bookkeeping consequence (compatible local
  stationary representatives glue to a global stationary section,
  conditional on the imported atlas + cocycle + nondegeneracy +
  pairing-covariance hypotheses) remains the parent's own claim on its
  own audit row.
- `MINIMAL_AXIOMS_2026-05-03.md` records the physical Cl(3) local
  algebra plus Z^3 spatial substrate baseline. This bounded note does
  **not** invoke that baseline directly; it imports finite-dimensional
  real matrix algebra (BA-1) as a bounded textbook input.

## Boundaries

This note does **not**:

- claim the parent note's bookkeeping consequence about compatible
  local stationary representatives patching into a global stationary
  section. That remains the parent's own load-bearing claim on its
  own audit row;
- import or otherwise depend on the parent's four admitted-context
  hypotheses (finite atlas of `PL S^3 × R`, transition cocycle,
  source/field pairing covariance, chart-wise `K_GR(D)`
  nondegeneracy);
- derive (BA-1) from the physical Cl(3) local algebra plus Z^3
  spatial substrate baseline. Linear algebra over `R` is admitted as
  bounded textbook input;
- close the unconditional global stationary closure theorem flagged
  by the parent;
- promote any sister authority's effective status. The parent
  `UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE.md` remains at
  its current audit verdict on its own row.

What this note **does**: implement the 2026-05-10 verdict's named
repair-target option (b) — split the parent's class-A in-note trace
identity into a separate clean algebraic row that closes from
elementary matrix algebra (BA-1) alone, with no imported hypotheses.

## Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_universal_gr_bd_congruence_invariance.py
```

Expected:

```text
TOTAL: PASS=N FAIL=0
VERDICT: the trace identity B_{D'}(h',k') = B_D(h,k) under congruence
D' = S^T D S, h' = S^T h S, k' = S^T k S verified at numpy double-
precision tolerance over multiple matrix dimensions (n = 2, 3, 4, 5, 8)
and 100 random trials per dimension. The identity is a class-A
algebraic identity over (BA-1) finite-dimensional real matrix algebra
(cyclic trace + inverse-of-product); no hypotheses beyond (BA-1) are
imported. The parent's bookkeeping consequence about global stationary
sections is NOT claimed here; this is a split-note algebraic row only.
```
