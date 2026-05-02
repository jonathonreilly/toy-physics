# No Per-Site γ_5 Chirality Operator on Cl(3) Pauli Rep

**Date:** 2026-05-02
**Type:** positive_theorem (no-go form)
**Claim scope:** on the framework's per-site Hilbert H_x ≅ C² (Pauli rep by
retained per-site uniqueness), the Cl(3) volume element ω = γ_1 γ_2 γ_3 acts
as the central scalar i·I_2. Therefore there is **no element of M_2(C) that
anticommutes with all three Cl(3) generators σ_i**, and in particular no
γ_5 candidate satisfying γ_5² = +I_2 with {γ_5, σ_i} = 0. Per-site chirality
operators do not exist in the framework's odd-spatial Cl(3) algebra.
**Status:** awaiting independent audit.
**Loop:** `positive-only-r6-20260502`
**Cycle:** 1 (Block 1)
**Branch:** `physics-loop/positive-only-r6-block01-no-per-site-chirality-20260502`
**Runner:** `scripts/no_per_site_chirality_check.py`
**Log:** `outputs/no_per_site_chirality_check_2026-05-02.txt`

## Cited authorities (one hop)

- [`AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md)
  — `effective_status: retained`. Provides:
  - **(U2)** Per-site Hilbert H_x ≅ C² with γ_i ↦ σ_i (Pauli) is the unique
    faithful 2-dim Cl(3) representation up to unitary equivalence.

This is the only load-bearing one-hop dependency.

## Admitted-context inputs

- **Standard Clifford-algebra volume-element identity.** In Cl(p, q) with
  n = p + q, the volume element ω = e_1 e_2 ... e_n satisfies
  ω · e_μ = (-1)^(n-1) e_μ · ω. For n = 3 (odd), ω commutes with every
  generator. Standard reference: Lawson–Michelsohn, *Spin Geometry*, Ch. I.
- **Pauli matrices are a C-linear basis for M_2(C).** Standard fact: any
  2x2 complex matrix decomposes uniquely as a·I + b·σ_1 + c·σ_2 + d·σ_3.

Both are pure mathematical facts; no admitted physics conventions.

## Statement

Let H_x ≅ C² be the per-site Hilbert space at any site x ∈ Z^3 of the
framework, with Cl(3) generators acting as Pauli matrices `γ_i ↦ σ_i`
(retained per-site uniqueness). Define the Cl(3) volume element

```text
    ω  :=  γ_1 γ_2 γ_3.                                                     (1)
```

Then:

**(N1) ω is central in Pauli rep.** ω = i·I_2; in particular [ω, σ_i] = 0
for every i.

**(N2) ω² = -I_2.** Direct computation (i·I)² = -I.

**(N3) No γ_5 candidate exists.** There is no element γ_5 ∈ M_2(C) such
that
- γ_5² = +I_2 (involution), and
- {γ_5, σ_i} = 0 for every i (anticommutes with all Cl(3) generators).

Equivalently, the only M ∈ M_2(C) satisfying {M, σ_i} = 0 for all i is
M = 0 (which fails the involution condition).

**(N4) Even/odd subalgebras coincide on Pauli rep.** The Z_2-graded
subalgebras Cl(3)_even = span{I, σ_iσ_j} and Cl(3)_odd = span{σ_i, ω}
each span the full M_2(C) when projected to Pauli rep. There is no
internal Z_2 grading, hence no chirality projector P_± = (1 ± γ_5)/2.

## Proof

### Step 1 — Pauli rep is the per-site Hilbert (cited)

By the retained per-site uniqueness theorem (U2), H_x ≅ C² with
γ_i ↦ σ_i.

### Step 2 — Volume element computation (N1, N2)

Direct multiplication in the Pauli basis:

```text
    ω  =  σ_1 σ_2 σ_3
       =  σ_1 · (σ_2 σ_3)
       =  σ_1 · (i σ_1)
       =  i · σ_1²
       =  i · I_2.                                                          (2)
```

Hence ω = i·I_2 is a scalar (proportional to identity), so it commutes
with every σ_i — establishing (N1). Squaring: ω² = (i·I)² = -I_2 —
establishing (N2).

### Step 3 — No M anticommutes with all σ_i (N3)

Suppose M ∈ M_2(C) satisfies {M, σ_i} = 0 for all i. Decompose M in the
Pauli basis:

```text
    M  =  a·I  +  b₁·σ_1  +  b₂·σ_2  +  b₃·σ_3                            (3)
```

with a, b_k ∈ C. Computing the anticommutator with σ_j and using
{σ_j, σ_k} = 2 δ_{jk} I:

```text
    {M, σ_j}  =  2a · σ_j  +  Σ_k b_k · {σ_k, σ_j}
              =  2a · σ_j  +  2 b_j · I_2.                                  (4)
```

For this to vanish, we need both 2a = 0 (coefficient of σ_j) and
2 b_j = 0 (coefficient of I_2). Since this must hold for all j ∈ {1,2,3},
we get a = b_1 = b_2 = b_3 = 0, i.e. M = 0.

The zero matrix has 0² = 0 ≠ I_2, so it fails the involution condition
γ_5² = +I_2. Therefore no γ_5 candidate exists — establishing (N3).

### Step 4 — Even/odd subalgebra collapse (N4)

In Pauli rep:
- Even subalgebra basis (degree 0 + degree 2): {I, σ_1σ_2 = i σ_3,
  σ_2σ_3 = i σ_1, σ_3σ_1 = i σ_2}, which as a C-span equals
  span{I, σ_1, σ_2, σ_3} = M_2(C).
- Odd subalgebra basis (degree 1 + degree 3): {σ_1, σ_2, σ_3,
  σ_1σ_2σ_3 = i I}, which also as a C-span equals M_2(C).

Both subalgebras span all of M_2(C) when extended to C-coefficients.
The Z_2 grading, real and nontrivial in Cl(3) over R, becomes invisible
in the complex Pauli rep — the rep "doesn't see" the chirality split.
Hence there is no projector P_± = (1 ± γ_5)/2 internal to the per-site
Hilbert — establishing (N4). ∎

## Hypothesis set used

- `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` (retained):
  provides Pauli rep on per-site Hilbert.
- Standard Clifford volume-element identity (mathematical, admitted-context).
- Pauli matrices span M_2(C) (mathematical, admitted-context).

No fitted parameters. No observed values. No physics conventions admitted
beyond the retained per-site uniqueness theorem.

## Corollaries

C1. **No per-site chirality projector.** A "left/right" projection of
elementary fermions cannot be defined intrinsically at the per-site
Cl(3) level. Chirality must enter from a structure beyond per-site
Cl(3) — e.g. by extending the Clifford algebra to include a temporal
generator (Cl(3,1) with n=4 even, where ω anticommutes with all four
generators and yields a true γ_5).

C2. **Connection to anomaly_forces_time.** This per-site no-chirality
result is the local instance of the well-known "no chirality in odd
total dimension" fact (`docs/ANOMALY_FORCES_TIME_THEOREM.md` Step 3).
Adding one temporal direction (n_total = 3 + 1 = 4 even) is exactly
the algebraic step required to recover a γ_5 — confirming that the
framework's 3+1 spacetime signature is forced by the anomaly + chirality
combination at the algebraic level.

C3. **Per-site fermion content is "vector-like" in 3D.** Without a
chirality operator at the site level, every Cl(3) per-site fermion looks
like a vector-like (non-chiral) Dirac doublet from a 3D-only viewpoint.
The physical chirality grading is generated only after lifting to a
3+1D Cl(3,1) algebra, where the temporal direction supplies the missing
generator that anticommutes with the spatial three.

C4. **Algebraic no-go: no internal "left-handed" subspace at single
site.** The framework's Standard Model gauge content (left-handed weak
doublets vs. right-handed weak singlets) cannot be implemented as a
*site-local* projection. It enters only after the temporal direction
is in play — consistent with the framework's overall axiom-cascade
narrative.

## Honest status

Positive theorem (in no-go form) on the framework's per-site Hilbert
space, derived from a single retained one-hop dependency by elementary
matrix algebra in the Pauli basis. The volume element identity is
standard Clifford theory; the no-γ_5 conclusion follows by exhausting
the Pauli basis decomposition.

```yaml
claim_type_author_hint: positive_theorem
claim_scope: "Cl(3) volume element ω = i·I in Pauli rep; no per-site γ_5 chirality operator exists in M_2(C)."
upstream_dependencies:
  - axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29 (retained)
admitted_context_inputs:
  - Clifford volume-element commutation identity (Lawson–Michelsohn)
  - Pauli matrices span M_2(C) (basic linear algebra)
```
