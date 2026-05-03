# Z_3 Fourier Diagonalization of C3[111] on Framework hw=1 Triplet

**Date:** 2026-05-03
**Type:** positive_theorem
**Claim scope:** the C3[111] cyclic operator on the framework's retained
hw=1 generation triplet H_{hw=1} ≅ C^3 (supplied by retained
three_generation_observable_theorem_note as cycling X_1 → X_2 → X_3 → X_1)
admits an explicit Z_3 Fourier diagonalization. The Fourier basis
Y_k = (1/√3) Σ_a ω^{-k(a-1)} X_a (k = 0, 1, 2; ω = exp(2πi/3)) is
orthonormal, complete, and diagonalizes C3[111] with eigenvalues {1, ω, ω²}
each with multiplicity 1. The hw=1 triplet decomposes as the direct sum
of three Z_3-isotypic components, each 1-dimensional.
**Status:** awaiting independent audit.
**Loop:** continuation of audit-backlog campaign / new positive closure
**Cycle:** 6 (after cycle 5's negative outcome on yt_ew M residual)
**Branch:** `physics-loop/three-gen-z3-fourier-diagonalization-20260503`
**Runner:** `scripts/three_gen_z3_fourier_diagonalization_check.py`
**Log:** `outputs/three_gen_z3_fourier_diagonalization_check_2026-05-03.txt`

## Cited authorities (one hop)

- [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
  — `effective_status: retained`. Provides:
  - The retained hw=1 generation triplet sectors {X_1, X_2, X_3} on
    H_{hw=1} ≅ C^3.
  - The cyclic action of C3[111]: X_a → X_{a+1 mod 3}.
  - Joint claim that translation projectors + C3[111] generate the full
    operator algebra M_3(C) on H_{hw=1}.

This is the only load-bearing one-hop dependency.

## Admitted-context inputs

- **Standard finite-Fourier transform construction.** For any cyclic group
  Z_N acting on C^N by regular representation, the Fourier basis
  Y_k = (1/√N) Σ_a ω^{-k(a-1)} X_a (with ω = exp(2πi/N)) diagonalizes the
  generator. Standard discrete-Fourier-transform construction.
- **Spectral theorem for unitary operators on finite-dim Hilbert.** Standard.

Both are pure mathematical / linear-algebraic facts; no admitted physics
conventions.

## Statement

Let H_{hw=1} ≅ C^3 with basis {X_1, X_2, X_3} (retained per the cited
three-generation observable theorem). Let ω = exp(2πi/3) be the primitive
3rd root of unity. Define the **Z_3 Fourier basis**:

```text
    Y_k  :=  (1/√3) Σ_{a=1}^{3} ω^{-k(a-1)} X_a    for k = 0, 1, 2.        (1)
```

Then:

**(F1) C3[111] is order 3.** (C3[111])^3 = I_3 on H_{hw=1}.

**(F2) C3[111] eigenvalues = {1, ω, ω²}.** Each eigenvalue has multiplicity 1.

**(F3) Fourier diagonalization.** For k = 0, 1, 2:

```text
    C3[111] · Y_k  =  ω^k · Y_k.                                            (2)
```

**(F4) Orthonormality.** ⟨Y_k, Y_j⟩ = δ_{kj}.

**(F5) Completeness.** span_C{Y_0, Y_1, Y_2} = H_{hw=1}; equivalently
Σ_k Y_k Y_k^† = I_3.

**(F6) Inverse Fourier.** For a = 1, 2, 3:

```text
    X_a  =  (1/√3) Σ_{k=0}^{2} ω^{k(a-1)} Y_k.                             (3)
```

**(F7) Isotypic decomposition.**

```text
    H_{hw=1}  =  V_0  ⊕  V_1  ⊕  V_2,    with dim V_k = 1 each.            (4)
```

V_k = span{Y_k} is the k-th Z_3-isotypic component (eigenspace of C3[111]
with eigenvalue ω^k).

**(F8) Diagonal form.** In the Y_k basis, C3[111] = diag(1, ω, ω²). Equivalently:

```text
    Y^† · C3[111] · Y  =  diag(1, ω, ω²)                                    (5)
```

where Y is the unitary matrix with columns Y_0, Y_1, Y_2.

**(F9) Cyclic-average projector.** P_cyc := (1/3)(I + C3[111] + C3[111]²)
is a rank-1 orthogonal projector onto V_0 (the Z_3-trivial subspace). It
satisfies P_cyc² = P_cyc, P_cyc · Y_0 = Y_0, P_cyc · Y_k = 0 for k ≠ 0.

## Proof

### Step 1 — C3[111] cycles (cited)

By three_generation_observable_theorem_note (retained): C3[111] acts on
H_{hw=1} as the cyclic permutation X_a → X_{a+1 mod 3}. In matrix form on
the {X_1, X_2, X_3} basis (X_a as standard basis vector e_{a-1}):

```text
    C3[111]  =  | 0  0  1 |
                | 1  0  0 |
                | 0  1  0 |.                                                (6)
```

### Step 2 — Order 3 (F1)

Direct matrix multiplication: C3² = (cyclic permutation by 2 steps), C3³ =
(cyclic permutation by 3 steps) = identity. Hence C3³ = I_3. ∎ (F1)

### Step 3 — Eigenvalues (F2)

C3[111] is unitary (permutation matrix, all entries 0 or 1, columns
orthogonal). Its characteristic polynomial is

```text
    det(λI - C3) = λ³ - 1                                                   (7)
```

(sum of cyclic permutation matrix's eigenvalues equals trace = 0; product
equals determinant = 1; standard result for cyclic permutation).

The roots of λ³ = 1 are exactly {1, ω, ω²} where ω = exp(2πi/3), each
simple. ∎ (F2)

### Step 4 — Fourier diagonalization (F3)

For each k ∈ {0, 1, 2}, compute C3[111] · Y_k:

```text
    C3 · Y_k  =  C3 · (1/√3) Σ_a ω^{-k(a-1)} X_a
              =  (1/√3) Σ_a ω^{-k(a-1)} C3 · X_a
              =  (1/√3) Σ_a ω^{-k(a-1)} X_{a+1 mod 3}
              =  (1/√3) Σ_b ω^{-k(b-2)} X_b      (b = a+1 mod 3)
              =  (1/√3) ω^{k} Σ_b ω^{-k(b-1)} X_b
              =  ω^k · Y_k.                                                 (8)
```

Establishing (F3). ∎

### Step 5 — Orthonormality (F4)

```text
    ⟨Y_k, Y_j⟩  =  Σ_a Y_k(a)^* · Y_j(a)
                =  (1/3) Σ_a ω^{k(a-1)} ω^{-j(a-1)}
                =  (1/3) Σ_a ω^{(k-j)(a-1)}
                =  (1/3) · 3 · δ_{kj}     (cyclic Σ_a ω^{m(a-1)} = 3 if m≡0 mod 3, 0 else)
                =  δ_{kj}.                                                  (9)
```

Establishing (F4). ∎

### Step 6 — Completeness (F5)

By (F4), {Y_k} is an orthonormal set of 3 vectors in H_{hw=1} ≅ C^3.
Since dim H_{hw=1} = 3 = number of vectors, the set is a complete
orthonormal basis. Therefore span{Y_k} = H_{hw=1} and Σ_k |Y_k⟩⟨Y_k| =
I_3 (resolution of identity). ∎ (F5)

### Step 7 — Inverse Fourier (F6)

By orthonormality (F4) and completeness (F5): X_a = Σ_k ⟨Y_k, X_a⟩ · Y_k
where ⟨Y_k, X_a⟩ = (1/√3) ω^{k(a-1)}. Therefore X_a = (1/√3) Σ_k ω^{k(a-1)}
Y_k. ∎ (F6)

### Step 8 — Isotypic decomposition (F7)

By (F3), each Y_k is an eigenvector of C3 with distinct eigenvalue ω^k.
The corresponding eigenspaces V_k = ker(C3 - ω^k I) are pairwise
orthogonal (different eigenvalues of unitary operator), each
1-dimensional, and sum to H_{hw=1}. ∎ (F7)

### Step 9 — Diagonal form (F8)

By (F3), Y diagonalizes C3 in the Y basis with eigenvalues (1, ω, ω²)
on the diagonal. ∎ (F8)

### Step 10 — Cyclic-average projector (F9)

Compute P_cyc · Y_k for each k:

```text
    P_cyc · Y_k  =  (1/3)(I + C3 + C3²) · Y_k
                =  (1/3)(Y_k + ω^k Y_k + ω^{2k} Y_k)
                =  (1/3)(1 + ω^k + ω^{2k}) · Y_k.                          (10)
```

For k = 0: 1 + 1 + 1 = 3, so P_cyc · Y_0 = Y_0.
For k ≠ 0: 1 + ω^k + ω^{2k} = 0 (sum of all three cube roots of unity is 0).
So P_cyc · Y_k = 0 for k ≠ 0.

Hence P_cyc projects onto the 1-dim subspace V_0 spanned by Y_0. P_cyc²
= P_cyc and rank(P_cyc) = 1. ∎ (F9)

## Hypothesis set used

- `three_generation_observable_theorem_note` (retained): provides the
  framework's hw=1 triplet H_{hw=1} ≅ C^3 with cyclic C3[111] action.
- Standard finite-Fourier transform construction (mathematical,
  admitted-context).
- Spectral theorem for unitary operators on finite-dim Hilbert
  (mathematical, admitted-context).

No fitted parameters. No observed values. No physics conventions admitted
beyond the retained three-generation observable theorem.

## Corollaries

C1. **Three Z_3-isotypic generation labels.** Every state in the framework's
hw=1 triplet decomposes uniquely into the three Z_3 character components
indexed by k = 0, 1, 2. The k = 0 sector V_0 = span{Y_0} is the
"symmetric" (Z_3-singlet) generation; V_1 and V_2 are the two
non-trivial Z_3 character sectors.

C2. **Cyclic-symmetric subspace is rank-1.** The Z_3-cyclic-invariant
subspace of H_{hw=1} is exactly the 1-dim line V_0 = span{Y_0}, where
Y_0 = (X_1 + X_2 + X_3)/√3 is the totally symmetric generation.

C3. **Cyclic-average projector P_cyc structure.** The cyclic average
P_cyc = (I + C3 + C3²)/3 is the explicit rank-1 projector onto V_0.
This is the H_{hw=1}-restricted analog of the framework's
koide_dweh_cyclic_compression P_cyc on Herm(3) — the same Z_3 Fourier
structure applies at multiple framework levels.

C4. **Fourier basis is the canonical generation eigenbasis.** Y_k is the
unique-up-to-overall-phase orthonormal eigenbasis of C3[111]. Any other
diagonalization is related to {Y_k} by a diagonal unitary phase U =
diag(e^{iθ_0}, e^{iθ_1}, e^{iθ_2}).

C5. **Combined with translation algebra.** Per the cited theorem, T_{x,y,z}
+ C3[111] generate M_3(C). In the Fourier basis, C3[111] is diagonal;
the translation projectors mix the Y_k basis vectors. The full M_3(C)
algebra factors as (Z_3 character labels) ⊗ (translation labels) at the
Hilbert-space level, providing an explicit Schur-decomposition route for
any operator on H_{hw=1}.

C6. **No proper Z_3-invariant subspace except V_0.** The only proper
non-zero Z_3-invariant subspaces of H_{hw=1} are the 1-dim isotypic
components V_0, V_1, V_2 (each a non-trivial irrep / trivial irrep of
Z_3). No 2-dim Z_3-invariant subspace exists. This sharpens the
"no-proper-quotient" content of the upstream theorem: no proper
Z_3-equivariant quotient exists at the irrep level.

## Honest status

Positive theorem on the framework's hw=1 generation triplet, derived
from a single retained one-hop dependency by the standard discrete
Fourier transform of Z_3. The runner exhibits all 9 facts (F1)–(F9) at
machine precision. Content is genuinely framework-specific because it
uses the framework's specific X_1, X_2, X_3 sectors and C3[111]
construction (not a generic 3-dim cyclic group action).

This theorem extracts the Fourier-eigenbasis structure that is implicit
in the upstream theorem's "C3[111] generates Z_3 action" statement but
not explicitly written down. Provides a tool for downstream lanes that
need to label generation states by Z_3 character (k = 0, 1, 2).

```yaml
claim_type_author_hint: positive_theorem
claim_scope: "C3[111] on H_{hw=1} ≅ C^3 has eigenvalues {1, ω, ω²} with explicit Fourier basis Y_k diagonalizing it; hw=1 triplet decomposes into three 1-dim Z_3-isotypic components."
upstream_dependencies:
  - three_generation_observable_theorem_note (retained)
admitted_context_inputs:
  - finite-Fourier-transform construction (mathematical)
  - spectral theorem for unitary operators (mathematical)
```
