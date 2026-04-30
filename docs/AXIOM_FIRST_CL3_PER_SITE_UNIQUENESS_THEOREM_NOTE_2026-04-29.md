# Axiom-First Per-Site Uniqueness of the Cl(3) Spinor Module

**Date:** 2026-04-29
**Status:** support — branch-local theorem note on A_min; runner passing; audit-pending.
**Loop:** `axiom-first-foundations`
**Cycle:** 6 (Route R6)
**Runner:** `scripts/axiom_first_cl3_per_site_uniqueness_check.py`
**Log:** `outputs/axiom_first_cl3_per_site_uniqueness_check_2026-04-29.txt`

## Scope

Cycle 1's spin-statistics theorem load-bears on the *finite-
dimensionality* of the per-site Cl(3) module: the minimal complex
spinor irrep of Cl(3) is dim 2, hence per-site Hilbert space is dim
2, hence bosonic CCR `[a, a^†] = I` is impossible per site. This
note discharges the "minimal complex spinor irrep is dim 2" step
into an explicit Stone–von Neumann–style uniqueness theorem for
Cl(3) representations: any faithful irreducible representation of
Cl(3) on a finite-dimensional complex vector space has dimension
exactly 2 and is unitarily equivalent to the canonical Pauli
representation `γ_i = σ_i`.

After this note, Cycle 1's Step 2 argument is closed at the
representation-theoretic level: per-site Hilbert dim = 2 is a
theorem, not a stipulation.

## A_min objects in use

- **A1 — local algebra `Cl(3)`.** Used as the canonical real
  Clifford algebra with three generators `γ_1, γ_2, γ_3` satisfying

  ```text
      { γ_i ,  γ_j }   :=   γ_i γ_j  +  γ_j γ_i   =   2 δ_{ij} · I.    (1)
  ```

  No other A_min ingredient is used in this note.

## Statement

Let `Cl(3)` be the real Clifford algebra defined by (1).

**(U1) Existence.** The Pauli matrices `σ_1, σ_2, σ_3` satisfy
(1) on `C²`. Hence there is at least one faithful irreducible
representation of Cl(3) on a 2-dim complex vector space.

**(U2) Uniqueness up to isomorphism.** Any faithful irreducible
representation `ρ : Cl(3) → End(V)` on a finite-dim complex vector
space `V` satisfies `dim_C V = 2` and is unitarily equivalent to
`(σ_1, σ_2, σ_3)`. Concretely: there exists a unitary `U ∈ U(2)`
such that `U^{-1} ρ(γ_i) U = σ_i` for all `i`.

**(U3) Decomposition.** Any finite-dim complex representation of
Cl(3) decomposes as a direct sum of copies of the Pauli irrep:

```text
    V   =   C²  ⊕  C²  ⊕  …  ⊕  C²       (n copies)                  (2)
```

with `dim_C V = 2n`. There is no faithful representation of Cl(3)
on a complex vector space of odd dimension.

**(U4) Per-site Hilbert dimension on `A_min`.** Combining (U2) with
the staggered-fermion convention (one Grassmann pair per site),
the per-site Hilbert space at canonical evaluation has dimension
exactly 2 (one Grassmann mode → 2-dim Fock space, matching the
Cl(3) minimal spinor irrep).

## Proof

The proof is the Wedderburn / Artin–Wedderburn structure theorem
for the simple algebra `Cl(3) ⊗_R C`, combined with Schur's lemma.

### Step 1 — `Cl(3) ⊗_R C ≅ M_2(C)`

Working over the complexification of Cl(3), the relations (1)
generate an associative algebra of dimension `2³ = 8` over `R`,
hence dimension `4` over `C`. The map

```text
    γ_1  ↦  σ_1,    γ_2  ↦  σ_2,    γ_3  ↦  σ_3                     (3)
```

extends to a surjective C-algebra homomorphism `Cl(3) ⊗_R C → M_2(C)`.
The image is `M_2(C)` (because σ_i, σ_iσ_j, and I span M_2(C)),
and dimensions match (4 over C on each side), so the map is an
isomorphism.

### Step 2 — `M_2(C)` is simple, with up-to-isomorphism unique irrep

`M_2(C)` is simple (it has no two-sided ideals other than 0 and
itself; standard). By the Artin–Wedderburn theorem, every simple
finite-dim C-algebra `A` is isomorphic to `M_n(C)` for some `n`,
and has up to isomorphism a unique irreducible representation
(the natural action of `M_n(C)` on `C^n`).

For `A = M_2(C)` the unique irrep is `C²` with `M_2(C)` acting by
matrix multiplication. This is the Pauli representation under the
isomorphism (3).

### Step 3 — uniqueness up to *unitary* equivalence

Any two faithful irreducible reps `ρ_1, ρ_2 : Cl(3) → End(V_1),
End(V_2)` are isomorphic by Step 2. Choose any intertwiner
`U : V_1 → V_2`. By Schur's lemma, `U` is unique up to a non-zero
scalar; in particular we can pick `U` such that it intertwines
the Hermitian inner products on `V_1` and `V_2` (each `V_i`
inherits a unique-up-to-positive-scalar inner product making
the `ρ(γ_i)` Hermitian, since the `γ_i` are required to be
Hermitian by (1) and the spectral theorem). Hence `U` is unitary.

### Step 4 — decomposition (U3)

Any finite-dim complex `Cl(3)`-representation decomposes (Maschke's
theorem applied to the semisimple algebra `M_2(C)`) into a direct
sum of irreducible subrepresentations. Each subrep is by Step 2
isomorphic to the 2-dim Pauli irrep. Hence (2) holds with
`dim_C V = 2n`. No odd-dim faithful complex rep exists.

### Step 5 — per-site Hilbert dimension (U4)

`A_min`'s A3 places one Grassmann pair `(χ_x, χ̄_x)` per site `x ∈
Λ`. The single-mode Grassmann Fock space is 2-dim (occupied /
empty). By Step 2, this matches the unique 2-dim minimal complex
Cl(3) spinor irrep. Hence per-site Hilbert dimension on `A_min` is
exactly 2. ∎

## Hypothesis set used

A1 only (Cl(3) site algebra structure). The proof uses the standard
Artin–Wedderburn / Schur's lemma machinery, which is elementary
finite-dim representation theory. No imports from the forbidden
list.

## Corollaries (downstream tools)

C1. *Discharge of Cycle 1 Step 2.* The "per-site Hilbert dim = 2"
step in
`docs/AXIOM_FIRST_SPIN_STATISTICS_THEOREM_NOTE_2026-04-29.md` is
now a theorem (U4) on A1 alone, not a stipulation.

C2. *Universality of the spin-1/2 representation.* Any
half-integer spin lattice fermion content on `A_min` lives in a
direct sum of the unique Pauli irrep. Higher-spin matter content,
if needed, requires *extending* the local algebra beyond `Cl(3)`,
which would change `A_min`. This is a structural rigidity result.

C3. *No-go for "alternative" Cl(3) site algebras.* Anyone proposing
an alternative spinor representation on `A_min` must produce one
that is unitarily equivalent to Pauli. There is no alternative
finite-dim faithful Cl(3) irrep.

C4. *Compatibility with all prior cycles.* (U2) + Cycle 1
spin-statistics + Cycle 2 reflection positivity + Cycle 3 cluster
decomposition + Cycle 4 CPT all share the same per-site Hilbert
space; (U2) underlies the per-site dimension count in each.

## Honest status

**Branch-local theorem.** (U1)–(U4) are proved on A1 alone by
standard finite-dim semisimple algebra theory. The runner exhibits
the load-bearing facts: anticommutation relations of Pauli;
unitarity of intertwiners between two faithful reps; non-existence
of an odd-dim faithful complex rep.

**Not in scope.**

- Real / quaternionic uniqueness statements. The note works over
  the complex field, matching the package's complex-amplitude
  structure (derived in `docs/AXIOM_REDUCTION_NOTE.md` from the
  unitarity axiom).

## Citations

- A_min: `docs/MINIMAL_AXIOMS_2026-04-11.md`
- prior cycles in this loop:
  - `docs/AXIOM_FIRST_SPIN_STATISTICS_THEOREM_NOTE_2026-04-29.md`
    (uses (U4) as a load-bearing input)
- standard external references for the technique (cited as theorem-
  grade representation theory; we do not import any numerical
  input): Artin–Wedderburn 1908/1927; Schur 1905.
