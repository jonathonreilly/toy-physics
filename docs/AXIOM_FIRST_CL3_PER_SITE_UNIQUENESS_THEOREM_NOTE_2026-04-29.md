# Axiom-First Per-Site Uniqueness of the Cl(3) Spinor Module

**Date:** 2026-04-29 (originally); 2026-05-03 (audit-driven repair)
**Status:** support — branch-local theorem note on A_min; runner passing; awaiting re-audit after repair.
**Loop:** `axiom-first-foundations`
**Cycle:** 6 (Route R6)
**Runner:** `scripts/axiom_first_cl3_per_site_uniqueness_check.py`
**Log:** `outputs/axiom_first_cl3_per_site_uniqueness_check_2026-04-29.txt`

## Audit-driven repair (2026-05-03)

The original Step 1 misidentified `Cl(3) ⊗_R C` as `M_2(C)` by halving
the tensor-product dimension and ignoring the odd-complex-Clifford
split. The 2026-05-03 audit (fresh-agent-herschel) flagged this as
the load-bearing error: U2 and U3 relied on simplicity and unique
irreducibility of `M_2(C)`, but the correct complexification is
`M_2(C) ⊕ M_2(C)` (two simple summands distinguished by the central
pseudoscalar `ω = γ_1 γ_2 γ_3` taking eigenvalue `+i` or `-i`), so
there are **two** non-isomorphic 2-dim faithful complex irreps, not
one.

This repair:

- Replaces Step 1 with the correct identification: `Cl(3,0) ≅ M_2(C)`
  as a **real** algebra (real-dim 8 = real-dim of `M_2(C)`).
- Adds an explicit Step 2 on the central pseudoscalar `ω`,
  showing `ω² = -1` and `ω central` in `Cl(3)`.
- Adds an explicit Step 3 deriving the complexification
  `Cl(3) ⊗_R C ≅ M_2(C) ⊕ M_2(C)`, with the two summands indexed
  by the central character `ω = ±i`.
- Restates U2 as uniqueness-within-chirality: any faithful irreducible
  complex representation of `Cl(3)` has dimension exactly 2 and is
  unitarily equivalent **either** to the canonical positive-chirality
  Pauli irrep `ρ_+(γ_i) = σ_i` (`ω → +i`) **or** to its
  parity-conjugate negative-chirality irrep
  `ρ_-(γ_i) = -σ_i` (`ω → -i`). The two are not unitarily equivalent.
- Restates U3 to allow either chirality in the decomposition:
  every finite-dim complex Cl(3) representation is a direct sum
  of `n_+` copies of `ρ_+` and `n_-` copies of `ρ_-`, with total
  dim `2(n_+ + n_-)`.
- Preserves U4 (per-site Hilbert dim = 2): the dimensional
  conclusion holds in both chirality summands, so per-site Hilbert
  dim = 2 is independent of the chirality choice.
- Acknowledges that U4 uses A3 (one Grassmann pair per site →
  2-dim Fock space) for the Cl(3)-irrep-to-Hilbert-space bridge,
  not A1 alone. The hypothesis set is updated accordingly.

The canonical convention adopted in the rest of the package
(`γ_i = σ_i`, `ω = +i`) corresponds to the positive-chirality
summand. Downstream consumers that depend only on per-site Hilbert
dim = 2 (notably the spin-statistics chain) are unaffected; consumers
that assume "the unique 2-dim Cl(3) irrep" need to be aware of the
chirality choice.

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

**(U2) Uniqueness within chirality.** Any faithful irreducible
representation `ρ : Cl(3) → End(V)` on a finite-dim complex vector
space `V` satisfies `dim_C V = 2`, and the central pseudoscalar
`ω = γ_1 γ_2 γ_3` acts as a scalar `ω(ρ) = ε i` on `V` with
`ε ∈ {+1, -1}` fixed by `ρ`. Up to unitary equivalence there are
exactly two such irreps:

- the positive-chirality irrep `ρ_+(γ_i) = σ_i` (so `ω → +i`);
- the negative-chirality irrep `ρ_-(γ_i) = -σ_i` (so `ω → -i`).

Within each chirality summand, there is a unitary `U ∈ U(2)` such
that `U^{-1} ρ(γ_i) U = ε σ_i` for all `i`. The two chiralities are
**not** unitarily equivalent (they have different `ω`-eigenvalues).
The canonical convention adopted in the package is the
positive-chirality summand `ρ_+`.

**(U3) Decomposition.** Any finite-dim complex representation of
Cl(3) decomposes as a direct sum of copies of the two chirality
irreps:

```text
    V   =   ρ_+^{n_+}  ⊕  ρ_-^{n_-}                                  (2)
```

with `dim_C V = 2(n_+ + n_-)`. There is no faithful representation
of Cl(3) on a complex vector space of odd dimension. Under the
canonical positive-chirality convention only the `ρ_+` summand is
populated and the decomposition reduces to `n_+` copies of the
Pauli irrep.

**(U4) Per-site Hilbert dimension on `A_min`.** Combining (U2) with
A3's staggered-fermion canonical normalisation (one Grassmann pair
per site), the per-site Hilbert space has dimension exactly 2 (one
Grassmann mode → 2-dim Fock space, matching the dim-2 chirality
summand selected by the package convention). The dimensional
conclusion is independent of the chirality choice — both `ρ_+` and
`ρ_-` are 2-dim — so the chain into spin-statistics depends only on
the dimension, not on the chirality.

## Proof

The proof is the standard real-algebra classification of `Cl(3,0)`,
together with the explicit complexification splitting and Schur's
lemma in each chirality summand.

### Step 1 — `Cl(3,0) ≅ M_2(C)` as a real algebra

The relations (1) generate `Cl(3,0)` as a real algebra of dimension
`2³ = 8` (basis: `1, γ_1, γ_2, γ_3, γ_1γ_2, γ_1γ_3, γ_2γ_3, γ_1γ_2γ_3`).
The map

```text
    γ_1  ↦  σ_1,    γ_2  ↦  σ_2,    γ_3  ↦  σ_3                     (3)
```

extends to a real-algebra homomorphism `Cl(3,0) → M_2(C)`. The
image contains `σ_i, σ_iσ_j = i ε_{ijk} σ_k, σ_1σ_2σ_3 = i I, I`,
which span `M_2(C)` over `R` (`M_2(C)` has real-dim 8 = `dim_R Cl(3,0)`),
so the map is a real-algebra isomorphism. **Note that the codomain
is treated as a real algebra here**; the natural complex structure
on `M_2(C)` corresponds to multiplication by `ω = γ_1γ_2γ_3` (which
acts as `i I` under (3); see Step 2).

### Step 2 — central pseudoscalar `ω` with `ω² = -1`

Define `ω := γ_1 γ_2 γ_3 ∈ Cl(3)`. Direct calculation using (1):

```text
    ω²  =  γ_1 γ_2 γ_3 γ_1 γ_2 γ_3
        =  γ_1 γ_2 (-γ_1 γ_3) γ_2 γ_3        (γ_3γ_1 = -γ_1γ_3)
        =  -γ_1 (-γ_1 γ_2) γ_3 γ_2 γ_3       (γ_2γ_1 = -γ_1γ_2)
        =  γ_1² γ_2 γ_3 γ_2 γ_3
        =  γ_2 (-γ_2 γ_3) γ_3                (γ_3γ_2 = -γ_2γ_3)
        =  -γ_2² γ_3²
        =  -1.                                                       (4)
```

Centrality: `ω γ_i = γ_i ω` for `i = 1,2,3`. Direct computation:
e.g. `ω γ_1 = γ_1 γ_2 γ_3 γ_1 = γ_1 γ_2 (-γ_1 γ_3) = -γ_1 (-γ_1 γ_2) γ_3
= γ_1² γ_2 γ_3 = γ_2 γ_3`, and `γ_1 ω = γ_1 (γ_1 γ_2 γ_3) = γ_2 γ_3`.
The other directions are analogous. Hence `ω ∈ Z(Cl(3))`.

### Step 3 — complexification: `Cl(3) ⊗_R C ≅ M_2(C) ⊕ M_2(C)`

Tensor (3) with `C` over `R`. As a real algebra, `Cl(3) ⊗_R C` has
real-dim 16 and complex-dim 8 (NOT 4 — a real algebra of real-dim
`n` has complex-dim `n` after tensoring with `C`).

The central pseudoscalar `ω` extends to `ω ⊗ 1 ∈ Cl(3) ⊗_R C`,
still satisfying `(ω ⊗ 1)² = -(1 ⊗ 1)`. In the complexified algebra
`ω` and `i ⊗ 1 := 1 ⊗ i` both square to `-(1 ⊗ 1)`, so the
combinations

```text
    e_+  :=  (1 - i ω)/2,        e_-  :=  (1 + i ω)/2,                (5)
```

(with `i ω := (1⊗i)(ω⊗1)`) satisfy `e_+ + e_- = 1`, `e_+ e_- = 0`,
`e_+² = e_+`, `e_-² = e_-`. These are central orthogonal idempotents.
On `e_+ Cl(3)⊗_R C`, `ω` acts as `+i`; on `e_- Cl(3)⊗_R C`, `ω`
acts as `-i`. Hence

```text
    Cl(3) ⊗_R C   =   ( e_+  Cl(3)⊗_R C )   ⊕   ( e_-  Cl(3)⊗_R C ),  (6)
```

with each summand a complex algebra of complex-dim 4 (totals to
complex-dim 8, consistent with the count above). Each summand is
generated by the images `ε σ_i` of `γ_i` (with `ε = +1` on `e_+`,
`ε = -1` on `e_-`) and is isomorphic to `M_2(C)`. Hence
**`Cl(3) ⊗_R C ≅ M_2(C) ⊕ M_2(C)`**, with the two summands indexed
by the central character `ω = ±i`.

### Step 4 — uniqueness within each chirality summand (U2)

Each summand `e_ε Cl(3) ⊗_R C ≅ M_2(C)` is simple (`M_2(C)` has no
non-trivial two-sided ideals). By Artin–Wedderburn, each summand
has, up to isomorphism, a unique irreducible representation: the
natural action of `M_2(C)` on `C²`. Concretely:

- `ρ_+ : Cl(3) ⊗_R C → End(C²)`, `γ_i → σ_i`, `ω → +i I`;
- `ρ_- : Cl(3) ⊗_R C → End(C²)`, `γ_i → -σ_i`, `ω → -i I`.

Any faithful irreducible complex representation of `Cl(3)` factors
through one and only one of the two summands (since the central
pseudoscalar `ω` acts as a scalar on any irrep by Schur, and that
scalar is `+i` or `-i`). Within the chosen chirality summand,
uniqueness up to unitary equivalence follows from Schur as before:
choose any intertwiner `U : V_1 → V_2` between two faithful irreps
of the same chirality, and adjust `U` to intertwine the Hermitian
inner products (which exist uniquely up to positive scalar by the
Hermiticity of `γ_i`).

### Step 5 — decomposition (U3)

Apply Maschke / Wedderburn to the semisimple algebra
`M_2(C) ⊕ M_2(C)`. Any finite-dim complex `Cl(3)`-representation
decomposes uniquely into chirality components: a `+`-component
that factors through the `e_+` summand and a `-`-component that
factors through `e_-`. Each component further decomposes into
copies of its single irrep. Hence (2) holds with multiplicities
`(n_+, n_-)` and `dim_C V = 2(n_+ + n_-)`. No odd-dim faithful
complex rep exists.

### Step 6 — per-site Hilbert dimension (U4)

`A_min`'s A3 places one Grassmann pair `(χ_x, χ̄_x)` per site
`x ∈ Λ`. The single-mode Grassmann Fock space is 2-dim (`{|0⟩, χ̄|0⟩}`).
By Step 4, this 2-dim complex space is unitarily equivalent to the
canonical positive-chirality irrep `ρ_+` (the package convention).
Hence per-site Hilbert dimension on `A_min` is exactly 2. The
dimensional conclusion is the same in the negative-chirality summand;
only the chirality choice differs.

**Hypothesis subtlety.** Step 6 uses A1 (for the Cl(3) algebra and
its representation theory) AND A3 (for the staggered-fermion
canonical normalisation that gives the one-Grassmann-mode Fock
space). U4 cannot be derived from A1 alone — the bridge from
"abstract Cl(3) irrep" to "physical per-site Hilbert space" is the
A3 convention. This was implicit in the original note and is now
made explicit. ∎

## Hypothesis set used

A1 (Cl(3) site algebra structure) for U1–U3. A1 + A3 (the
one-Grassmann-pair-per-site canonical normalisation) for U4. The
proof uses the standard real-algebra classification of `Cl(3,0)`,
explicit complexification via the central pseudoscalar `ω`, and
Schur's lemma in each chirality summand. All elementary finite-dim
representation theory; no imports from the forbidden list.

## Corollaries (downstream tools)

C1. *Discharge of Cycle 1 Step 2.* The "per-site Hilbert dim = 2"
step in
`docs/AXIOM_FIRST_SPIN_STATISTICS_THEOREM_NOTE_2026-04-29.md` is
now a theorem (U4) on **A1 + A3** (not A1 alone, after the
2026-05-03 repair). The dimensional conclusion is independent of
the chirality choice — both summands give 2-dim irreps — so the
spin-statistics chain is unaffected by the chirality structure.

C2. *Universality of the spin-1/2 representation under the
canonical chirality choice.* Any half-integer spin lattice fermion
content on `A_min` (with the package convention `γ_i = σ_i`,
`ω = +i`) lives in a direct sum of the positive-chirality Pauli
irrep `ρ_+`. Higher-spin matter content, if needed, requires
*extending* the local algebra beyond `Cl(3)`, which would change
`A_min`. This is a structural rigidity result modulo the chirality
convention.

C3. *No-go for "alternative" Cl(3) site algebras within the chosen
chirality.* Anyone proposing an alternative spinor representation
on `A_min` must produce one that is unitarily equivalent to
`ρ_+ = (σ_1, σ_2, σ_3)` or, with an explicit parity flip, to
`ρ_- = (-σ_1, -σ_2, -σ_3)`. There are exactly two non-isomorphic
finite-dim faithful Cl(3) irreps and no others.

C4. *Compatibility with all prior cycles.* (U4) + Cycle 1
spin-statistics + Cycle 2 reflection positivity + Cycle 3 cluster
decomposition + Cycle 4 CPT all share the same per-site Hilbert
space dimension; (U4) underlies the per-site dimension count in
each. The chirality choice is fixed by the package convention and
does not change the dimensional content of any downstream cycle.

## Honest status

**Branch-local theorem.** (U1)–(U4) are proved on A1 (plus A3 for
U4 only) by standard real-algebra classification, explicit
complexification via the central pseudoscalar, and Schur's lemma in
each chirality summand. The runner exhibits the load-bearing facts:
anticommutation relations of Pauli; central-pseudoscalar identity
`ω² = -1` and centrality; chirality eigenvalue assignments
`ω → ±i` on `ρ_±`; non-existence of an odd-dim faithful complex
rep; and unitarity of intertwiners within each chirality summand.

**Not in scope.**

- Real / quaternionic uniqueness statements. The note works over
  the complex field, matching the package's complex-amplitude
  structure (derived in `docs/AXIOM_REDUCTION_NOTE.md` from the
  unitarity axiom).
- Derivation of the chirality convention from physical input. The
  package convention `γ_i = σ_i` (positive chirality) is adopted as
  a normalisation choice consistent with the standard Pauli sign
  conventions; the parity-conjugate negative-chirality irrep `ρ_-`
  is equally valid abstractly but is not the package convention.

## Load-bearing Dependencies

- A_min: [MINIMAL_AXIOMS_2026-04-11.md](MINIMAL_AXIOMS_2026-04-11.md)

## Citations

- downstream consumer in this loop:
  `docs/AXIOM_FIRST_SPIN_STATISTICS_THEOREM_NOTE_2026-04-29.md`
  (uses (U4) as a load-bearing input)
- standard external references for the technique (cited as theorem-
  grade representation theory; we do not import any numerical
  input): Artin–Wedderburn 1908/1927; Schur 1905.
