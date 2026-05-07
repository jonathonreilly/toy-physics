# Staggered + Wilson Determinant-Positivity Bridge Theorem Note

**Date:** 2026-05-05
**Type:** positive_theorem
**Claim scope:** Under the symmetric-canonical surface consisting of the
canonical conventions used by
`docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`
(Wilson term `M_W` commutes with the staggered chirality `ε`, mass term
`m · I` proportional to the identity, balanced sublattice block
`Λ = (Z/L_τ Z) × (Z/L_s Z)^{d_s}` with even site count and
`n_+ = n_- = n/2`) plus the explicit structural restriction
`M_W = r · d · I`, the Dirac operator `M = M_KS + M_W + m · I` satisfies
`det(M) > 0` configuration-by-configuration on every SU(3) gauge
background for any `m > 0`. The proof is a structural two-sublattice
block decomposition; no per-configuration numerical input is required.
**Status authority:** independent audit lane only.
**Primary runner:** `scripts/frontier_staggered_wilson_det_positivity_bridge_2026_05_05.py`

## Why this note exists

The parent note
`docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`
records, in its Step 3a, that the staggered-only sector has a closed-form
`det(M_KS + m · I) ≥ 0` derivation but the staggered + Wilson sector is
only runner-supported via Exhibit E6. The independent-audit lane flagged
this as `missing_bridge_theorem`, with the alternative narrowing path of
"narrow the claim to staggered-only theorem plus explicitly finite
numerical support for the Wilson extension."

This note supplies the missing bridge for the symmetric-canonical
subsurface rather than a general Wilson-laplacian result. It proves
`det(M_KS + M_W + m · I) > 0` in closed form when the parent conventions
(`ε M_W ε = M_W`, parent §3a; mass term `m · I`, parent eq. (1) and the
A3 carrier) are supplemented by `M_W = r · d · I`.

The proof is a sublattice block decomposition; the resulting structure is
isomorphic to the BdG / chiral-pair form, and the determinant is a
product of strictly positive numbers `α² + σ_i²` for the singular values
`σ_i` of the off-diagonal staggered-hop block. Positivity is therefore
unconditional in `m > 0` and in any SU(3) gauge background on that
symmetric-canonical surface.

## Setup and conventions

Adopt the parent-note conventions verbatim:

- **A1 / A2 / A3 / A4** as in
  [`MINIMAL_AXIOMS_2026-04-11.md`](MINIMAL_AXIOMS_2026-04-11.md) and the
  parent reflection-positivity note. The lattice block is
  `Λ = (Z/L_τ Z) × (Z/L_s Z)^{d_s}` with **even** total site count `n`
  and balanced sublattice partition `n_+ = n_- = n/2` under the staggered
  chirality `ε(x) = (-1)^{x_1 + ... + x_d}` (the lattice block has even
  side lengths in every direction).
- Staggered Dirac hop `M_KS` is the canonical Kogut-Susskind staggered
  operator with phases `η_μ`. It is **anti-Hermitian** and satisfies the
  staggered-chirality anticommutation `{ε, M_KS} = 0` (parent Exhibit E5).
- Wilson term `M_W` is the canonical-A_min Wilson contribution that
  commutes with `ε`, i.e., `ε M_W ε = M_W` (parent §3a, line 360).
- Mass term is `m · I` with `m > 0` real (parent eq. (1)).
- Gauge background is an SU(3) link configuration `{U_μ(x)}`. The bridge
  proof does not depend on any specific gauge configuration; it holds
  for every link assignment compatible with the canonical surface.

The full canonical-surface Dirac operator is

```text
    M  =  M_KS  +  M_W  +  m · I                                       (1)
```

and is `γ_5`-Hermitian (`γ_5 ≡ ε`) under these conventions:

```text
    ε M ε  =  ε M_KS ε  +  ε M_W ε  +  m · I  =  -M_KS  +  M_W  +  m · I  (2)
```

so `ε M ε = M^†` (using `M_KS^† = -M_KS` and `M_W^† = M_W`).

## Block decomposition

Order the lattice sites so that the `n_+` sites with `ε = +1` come first
and the `n_-` sites with `ε = -1` come second. In this basis,

```text
    ε  =  diag(+I_{n_+}, -I_{n_-}).                                    (3)
```

Each operator decomposes:

- `M_KS` connects only sites in opposite sublattices (every staggered hop
  changes parity), so its only non-zero block is off-diagonal:

  ```text
      M_KS  =  [[ 0,    K  ],
                [ -K^†, 0  ]]                                          (4)
  ```

  The block `K` is the `n_+ × n_-` matrix of staggered hops from `+1`
  to `-1` sites. Anti-Hermiticity of `M_KS` is the condition that the
  bottom-left block is `-K^†`; equivalently, `M_KS^† = -M_KS`.

- `M_W` commutes with `ε` (assumption), so its only non-zero blocks are
  diagonal:

  ```text
      M_W  =  [[ D_+,  0   ],
               [ 0,    D_- ]]                                          (5)
  ```

  with `D_+` Hermitian on the `+1` sublattice and `D_-` Hermitian on the
  `-1` sublattice.

- `m · I` is a multiple of the identity, contributing `m · I_{n_+}` and
  `m · I_{n_-}` to each diagonal block:

  ```text
      m · I  =  [[ m I_{n_+}, 0       ],
                  [ 0,         m I_{n_-} ]]                            (6)
  ```

Combining (4)-(6),

```text
    M  =  [[ A,   K   ],
            [ -K^†, B  ]]                                              (7)
```

with `A := D_+ + m · I_{n_+}` and `B := D_- + m · I_{n_-}`, both Hermitian
on their respective sublattices.

## Symmetric-canonical case: A = B

The parent note's load-bearing setup (parent §3a, line 444 of the
hypothesis-match table: "A3: M_W with r = 1 (canonical)") fixes the
Wilson coefficient at the symmetric value `r = 1`, and the Wilson term in
its `ε`-commuting projection is invariant under the lattice translation
that swaps sublattices. Concretely, the diagonal block `D_+` and `D_-`
are unitarily equivalent under the staggered translation `T_x : x ↦ x + ê`
(which carries `ε = +1` sites to `ε = -1` sites for any unit vector `ê`).
Composing with the gauge-link rotation, `T_x` acts within
`Aut(M_W^{ε-commuting projection})` and therefore `D_+ ≃ D_-` as
operators. After choosing the basis on each sublattice consistently,
this gives

```text
    A  =  D_+ + m · I  =  D_- + m · I  =  B                            (8)
```

so we may write `A = B = α` where `α` is a Hermitian operator on
either sublattice, equal in operator norm and spectrum to its image
under the sublattice swap. **In the simplest canonical case where
`M_W` reduces to a sublattice-uniform diagonal multiple of the identity
(e.g., `M_W = r · d · I` from the diagonal contribution of the standard
Wilson Laplacian), we have `α = (r · d + m) · I`** and the rest of the
proof is exact and basis-independent.

The general case `D_+ ≃ D_- ≠ const · I` requires a slightly more careful
argument; we handle the symmetric-canonical case here and record the
generalisation in the open frontier.

## Bridge theorem

**Theorem (det positivity on the canonical staggered + Wilson surface).**
Under the conventions above, with the additional symmetric-canonical
constraint `A = B = α · I` for a real number `α := (M_W diagonal value) + m`,
the determinant of `M` is

```text
    det(M)  =  ∏_{i=1}^{n/2}  ( α²  +  σ_i² )                          (9)
```

where `σ_1 ≥ σ_2 ≥ ... ≥ σ_{n/2} ≥ 0` are the singular values of the
off-diagonal staggered-hop block `K` from equation (4). For any `m > 0`
and any SU(3) gauge background, every factor `α² + σ_i²` is strictly
positive, so

```text
    det(M)  >  0                                                       (10)
```

configuration-by-configuration.

### Proof

Using `γ_5 ≡ ε = diag(+I, -I)`, the operator

```text
    γ_5 M  =  [[ +α · I,   +K     ],
                [ +K^†,    -α · I ]]                                   (11)
```

is Hermitian (since `α` is real, `K` is a complex matrix, and the
block structure of `γ_5 M` is its own Hermitian conjugate). Take the
singular-value decomposition `K = U Σ V^†` with `Σ = diag(σ_1, ..., σ_{n/2})`,
`U` an `n/2 × n/2` unitary on the `+` sublattice, and `V` an `n/2 × n/2`
unitary on the `-` sublattice. Conjugate `γ_5 M` by the block-diagonal
unitary `W = diag(U, V)`:

```text
    W^† (γ_5 M) W  =  [[ +α · I,   +Σ      ],
                        [ +Σ,        -α · I ]]                          (12)
```

This unitary conjugation preserves both spectrum and determinant. The
right-hand-side block matrix decomposes further via the basis-permutation
that interleaves `(e_i^+, e_i^-)` pairs, giving `n/2` independent `2 × 2`
blocks:

```text
    block_i  =  [[ +α,  +σ_i ],
                  [ +σ_i, -α  ]]                                       (13)
```

Each `2 × 2` block has eigenvalues `± √(α² + σ_i²)` (exact from the
trace-zero, determinant `= -(α² + σ_i²)` characterisation), and its
determinant is

```text
    det(block_i)  =  -α²  -  σ_i²                                      (14)
```

Multiplying over all `n/2` blocks,

```text
    det(γ_5 M)  =  (-1)^{n/2}  ·  ∏_{i=1}^{n/2}  ( α²  +  σ_i² )       (15)
```

The chirality determinant on the balanced lattice is

```text
    det(γ_5)  =  det(ε)  =  (+1)^{n_+}  ·  (-1)^{n_-}  =  (-1)^{n/2}   (16)
```

and the multiplicativity of `det` gives

```text
    det(M)  =  det(γ_5)^{-1}  ·  det(γ_5 M)
            =  (-1)^{n/2}  ·  (-1)^{n/2}  ·  ∏ ( α²  +  σ_i² )
            =  ∏_{i=1}^{n/2}  ( α²  +  σ_i² )                          (17)
```

For `α = (M_W diagonal) + m` with `m > 0` (the canonical mass surface)
every factor `α² + σ_i² ≥ α² > 0` since `α ≠ 0` whenever `m > 0`. Hence

```text
    det(M)  >  0                                                       (18)
```

configuration-by-configuration on every SU(3) gauge background. ∎

### What the proof depends on

- (D1) `M_KS` is anti-Hermitian and `{ε, M_KS} = 0`. **Verified** by
  the parent note's Exhibit E5 across `L_t ∈ {4, 6, 8}` and
  `L_s ∈ {3, 4}` (parent runner output).
- (D2) `ε M_W ε = M_W`. **Asserted** by the parent note (parent §3a,
  line 360); the asserted convention is the one used in this bridge.
  Whether the standard Wilson Laplacian (with `r = 1` and full
  nearest-neighbour hops) reduces to this `ε`-commuting form on the
  canonical surface is the parent note's own structural assertion and
  is not re-derived here.
- (D3) Mass term is `m · I`. **Asserted** in parent eq. (1) and the
  A3 carrier.
- (D4) The diagonal blocks of `M_W + m · I` are equal: `A = B = α · I`.
  **Holds** in the symmetric-canonical case where `M_W` reduces to a
  sublattice-uniform diagonal multiple of the identity. The
  generalisation is recorded as the open frontier below.

The bridge takes (D1)-(D4) as inputs and proves (10) in closed form on
the symmetric-canonical surface. The independent audit lane must decide
whether that subsurface is enough to repair any broader parent claim.

## What this does not close

This bridge proves `det(M) > 0` per-configuration on the
**symmetric-canonical** surface where the diagonal blocks of `M_W + m · I`
are equal multiples of the identity (D4). It does not by itself decide
whether the parent note's broader reflection-positivity row can be
retained; that depends on independent audit of the parent scope and of
the dependency chain.

The following are **not** in scope:

- **Asymmetric `M_W`.** If `D_+ ≠ D_-` as operators (e.g., a
  sublattice-asymmetric Wilson coefficient or an `ε`-commuting `M_W`
  with non-trivial sublattice anisotropy), the unconditional
  `det(M) = ∏(α² + σ²)` factorisation no longer holds. A sufficient
  condition for positivity in the asymmetric case is `min eig(A) ·
  min eig(B) > σ_max(K)²`; this is a runner-verifiable bound but is
  not pursued here.
- **`M_W` with off-diagonal nearest-neighbour hops.** A standard
  Wilson Laplacian `M_W = (r/2) · (2d · I − sum of NN hops)` has both
  a diagonal (`ε`-commuting) part and an off-diagonal (`ε`-anti-commuting)
  part. The off-diagonal NN-hop part of such a Wilson term breaks
  (D2). The parent note's own assertion `ε M_W ε = M_W` excludes this
  case; if a future repair of the parent note adopts the standard
  Wilson-Laplacian convention, this bridge does not apply directly and
  the per-configuration positivity question is then the SU(3) sign-problem
  question that does not have an unconditional closed-form answer.
- **`m · ε` mass.** A staggered-mass convention with `m · ε(x)` on the
  diagonal (rather than `m · I`) gives `A ≠ B` even for symmetric
  `M_W`, breaking the BdG-pair structure. This is the convention used
  in some staggered-fermion literature; the parent note explicitly
  uses `m · I` (parent eq. (1)), so this case is not in scope here.

## Falsifiers

The bridge theorem is falsified if any of the following holds:

1. The parent note's assertion `ε M_W ε = M_W` is replaced by the
   standard Wilson-Laplacian operator (with NN hops); in that case,
   (D2) is lost and a different bridge is needed.
2. A direct numerical exhibit on a small SU(3) lattice with the
   symmetric-canonical convention shows `det(M_KS + M_W + m · I) ≤ 0`
   for some configuration with `m > 0`; this would invalidate either
   the proof or the setup.
3. The balanced-sublattice assumption fails (an odd-side lattice block
   gives `n_+ ≠ n_-`) and the closed-form factorisation no longer holds.
4. The sublattice-equivalence assumption (D4) fails on the asserted
   canonical surface.

The companion runner explicitly tests (1)-(3) by checking the block
structure (4) numerically on small lattices and computing
`det(M_KS + (m + r·d) · I)` under the symmetric-canonical convention.

## Import and support inventory

- **Computed inputs:** none. The bridge is closed-form.
- **Admitted inputs (asserted by parent note, used here without
  re-derivation):** (D1) `{ε, M_KS} = 0`; (D2) `ε M_W ε = M_W`; (D3)
  `mass = m · I`; (D4) `D_+ ≃ D_- = const · I` on the canonical surface.
- **Standard mathematical facts used:** singular-value decomposition
  of complex matrices, multiplicativity of `det` under unitary
  conjugation, eigenvalues of a `2 × 2` Hermitian trace-zero block.
- **Comparator-only:** none. No literature value is fitted or compared.
- **No new axiom introduced.**

## Relation to existing authority

This bridge is **strictly additive** on the parent
`docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`.
It supplies a closed-form theorem for the symmetric-canonical `M_W = r · d · I`
subsurface. It should be read as a dependency candidate for parent
re-audit, not as an author-side retained-status update.

The parent's Exhibits E5 and E6 remain in force as additional numerical
support; the bridge below makes that support an **exhibit of an already
proven theorem**, not the load-bearing input.

## Citations

- Parent integration target:
  `docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`
  (not a load-bearing dependency of this bridge note; the dependency edge
  is parent-to-bridge)
- A_min carrier:
  [`MINIMAL_AXIOMS_2026-04-11.md`](MINIMAL_AXIOMS_2026-04-11.md)
- Standard linear-algebra fact (SVD, BdG block structure): textbook
  matrix analysis (Horn-Johnson; not a numerical or fitted import).

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [axiom_first_reflection_positivity_theorem_note_2026-04-29](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md)
