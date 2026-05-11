# Koide BAE Probe X — Pauli Antisymmetrization on the C_3[111] Triplet

**Date:** 2026-05-08
**Claim type:** bounded_theorem
**Status:** bounded - wave-function-level structural obstruction; no
BAE closure, no downstream status change.
**Scope:** Probe X of the Koide **BAE-condition** closure campaign. It
tests whether Pauli antisymmetrization of the three-generation fermionic
wave-function on the hw=1 ≅ ℂ³ BZ-corner triplet, realized as a Slater
determinant, forces |b|²/a² = 1/2 (BAE) on the C_3-equivariant
Hermitian circulant `H = aI + bC + b̄C²`.
**Result:** Pauli antisymmetrization **structurally decouples** from the
circulant amplitude ratio. Three independent decoupling checks (PA-AV1,
PA-AV2, PA-AV3) are verified by the paired runner (53/0). The
Pauli-antisymmetric three-particle ground state lives in the C_3
**trivial isotype**, not the doublet, so it cannot constrain the
off-diagonal amplitude `b`. The BAE admission count is unchanged.
**Primary runner:** [`scripts/cl3_koide_x_bae_pauli_2026_05_08_probeX_bae_pauli.py`](../scripts/cl3_koide_x_bae_pauli_2026_05_08_probeX_bae_pauli.py)
**Cache:** [`logs/runner-cache/cl3_koide_x_bae_pauli_2026_05_08_probeX_bae_pauli.txt`](../logs/runner-cache/cl3_koide_x_bae_pauli_2026_05_08_probeX_bae_pauli.txt)

## Naming

The framework baseline is the physical `Cl(3)` local algebra on the
`Z^3` spatial substrate. This note treats that baseline as repo
semantics, not as a new axiom or optional theory language.

- **"BAE-condition" (Brannen Amplitude Equipartition)** = the
  amplitude-ratio constraint `|b|²/a² = 1/2` for the
  `C_3`-equivariant Hermitian circulant `H = aI + bC + b̄C²` on
  `hw=1 ≅ ℂ³`.
- **"A1-condition"** is a legacy alias for BAE only; it is not used as
  the primary name in this note.

## Question

After 30 prior probes attacked BAE at the **operator** level (RP, GNS,
character orthogonality, F1 vs F3 weighting, Plancherel, Peter-Weyl,
U(1) hunt, interacting-dynamics probes, etc.), all closed as
bounded obstructions or partial falsifications. The natural next attack
is at a structurally distinct layer.

Charged leptons are **fermions**; the framework's Grassmann partition
forcing theorem
([`STAGGERED_DIRAC_GRASSMANN_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_GRASSMANN_FORCING_THEOREM_NOTE_2026-05-07.md))
forces fermionic statistics on the matter sector. A 3-generation
fermionic wave-function on the hw=1 ≅ ℂ³ C_3[111] BZ-corner triplet,
filling the 3 mass eigenstates of `H = aI + bC + b̄C²`, must be a
Slater determinant by Pauli.

**Question (Probe X):** Does Pauli antisymmetrization on the C_3[111]
triplet force |b|²/a² = 1/2 (BAE)?

This is structurally distinct from any prior probe: prior probes
attacked H or its interaction terms at the **operator** level;
this probe attacks at the **wave-function** level via Pauli.

## Answer

**No.** Pauli antisymmetrization on the C_3[111] triplet **structurally
decouples** from the off-diagonal amplitude `b`. Three independent
decoupling theorems converge:

```
PA-AV1   Slater(3 fermions) total energy = tr(H) = 3a, b-INDEPENDENT
PA-AV2   Antisym ∧²V has Frobenius |b|² = 6|b|² (same as V; preserved)
PA-AV3   Slater ground state ∈ C_3 TRIVIAL isotype (det character +1)
```

**Result: bounded obstruction (wave-function-level decoupling) with
new positive content.** The Pauli antisymmetrization projects onto the
C_3 **trivial isotype**, which is exactly the diagonal (a-only) sector
of `H`. The off-diagonal `b` sector lives in the C_3 doublet isotype,
**untouched** by antisymmetrization. Hence Pauli is structurally
**incapable** of constraining |b|²/a². BAE admission count is
UNCHANGED. No new admission. No new axiom.

## Setup

### Dependencies

| Dependency | Role | Source |
|---|---|---|
| Physical `Cl(3)` local algebra | baseline local algebra | [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) |
| `Z^3` spatial substrate | baseline spatial substrate | [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) |
| hw=1 BZ-corner triplet ≅ `ℂ³` with `C_3[111]` action | representation being tested | [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md) |
| C_3-equivariant Hermitian on hw=1 is `aI + bC + b̄C²` | circulant operator form | [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md) |
| `E_+ = 3a²`, `E_⊥ = 6\|b\|²` on `M_3(ℂ)_Herm` | comparison to BAE weighting | [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md) |
| Frobenius pairing is the unique Ad-invariant inner product on `M_3(ℂ)_Herm` (up to scalar) | normalization context | [`KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md`](KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md) |
| Weight-class theorem: `κ = 2μ/ν`; `(1,1) → κ=2`; `(1,2) → κ=1` | identifies the missing BAE weighting | [`KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md) |
| Koide `Q = 2/3 ⟺ a² = 2\|b\|² ⟺ \|b\|²/a² = 1/2` (BAE) | target condition | [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md) |
| Grassmann matter measure | source of fermionic statistics | [`STAGGERED_DIRAC_GRASSMANN_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_GRASSMANN_FORCING_THEOREM_NOTE_2026-05-07.md) |
| Pauli antisymmetrization | fermionic wave-functions are antisymmetric under particle exchange | consequence of Grassmann matter plus canonical fermion second quantization |
| `M_3(C)` algebra on hw=1 triplet generated by translations + C_3[111] | operator arena | [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md) |

### Forbidden imports

- NO PDG observed mass values used as derivation input
- NO lattice MC empirical measurements as derivation input
- NO fitted matching coefficients
- NO same-surface family arguments
- NO new axioms or imports — primitives are derivations from the
  baseline framework and cited source notes only
- NO admitted fermion-statistics axiom — Pauli is a CONSEQUENCE of the
  Grassmann partition forcing theorem, not an independent admission

### Key fact: Pauli is forced, not admitted

The cited framework content forces fermionic statistics:

1. **Grassmann partition forcing**: the matter measure on
   `Cl(3) ⊗ Z³` is uniquely the finite Grassmann partition. Bosonic
   2nd-quantization is incompatible with the per-site Cl(3)
   module dimension 2 (would require infinite Fock space).

2. **Spin-statistics S2** (`AXIOM_FIRST_SPIN_STATISTICS_THEOREM_NOTE_2026-04-29.md`):
   half-integer-spin fields obey anticommutation relations.

3. **Pauli antisymmetrization** = the canonical statement that
   N-particle fermionic states span the totally antisymmetric subspace
   of the N-fold tensor power (Slater determinants).

So Pauli is a **derivation** from cited framework content, not a new axiom.

## Setup details

The 3 generations of charged leptons sit on the hw=1 ≅ ℂ³ BZ-corner
triplet (per the BZ-corner forcing theorem). The C_3-equivariant Hermitian
circulant Hamiltonian has the form

```
H = aI + bC + b̄C²,      a ∈ ℝ, b ∈ ℂ
```

with eigenvalues `λ_k = a + 2|b| cos(φ - 2πk/3)` (k = 0, 1, 2),
where `b = |b| e^(iφ)`. The eigenvectors are the C_3 Fourier basis
`e_k = (1/√3)(1, ω^k, ω^(2k))`, with C eigenvalue `ω^(-k)`.

A 3-fermion state filling all 3 mass eigenstates is the Slater
determinant `|Slater⟩ = c_0^† c_1^† c_2^† |0⟩ ∈ ∧³V`, where V = ℂ³.
By dimension count, dim(∧³V) = C(3, 3) = 1, so |Slater⟩ is **unique
up to phase**.

## The three decoupling theorems

### PA-AV1 — Slater total energy decouples from b

The expectation value `⟨Slater | H_total | Slater⟩` of the total
single-particle Hamiltonian on the filled-Slater state is

```
E_Slater = Σ_k λ_k = 3a + 2|b| Σ_k cos(φ - 2πk/3) = 3a
```

since `Σ_k cos(φ - 2πk/3) = 0` (Z_3 cosine identity). Hence
**`E_Slater = 3a`, INDEPENDENT of |b| and φ**.

Variational consequence: minimizing `E_Slater` (equivalently `tr(H)`)
gives `a → 0`, NOT BAE (κ = a²/|b|² = 2). Pauli total-energy
extremization does not select BAE.

**Verified numerically (runner Section 2):** 25 (|b|, φ) values all give
`E_Slater = 3 · 2.5 = 7.5` exactly; variance = 0.

**Verified algebraically (runner Section 5):** 66 (|b|, φ) test points,
max deviation < 1e-13.

### PA-AV2 — Antisymmetric 2-particle space ∧²V preserves |b|²

For the induced operator `∧²H` on `∧²V` (dim = 3, basis `e_i ∧ e_j`,
`i < j`), the eigenvalues are `λ_i + λ_j` (i < j). Algebraic identities:

```
tr(∧²H)         = 2 tr(H)             = 6a
tr((∧²H)²)     = (n-1) tr(H²) + (n-2) tr(H)² + ... = 12a² + 6|b|²
                 (specifically for n=3, see runner Section 3)

E_+(∧²H)       = tr(∧²H)² / 3        = 12a²
E_⊥(∧²H)       = tr((∧²H)²) − E_+    = 6|b|²

κ(∧²H)         = E_+(∧²H) / E_⊥(∧²H) = 12a² / 6|b|² = 4 κ(H)
```

So **antisymmetrization rescales κ by a factor of 4** — but does
**not pin** κ. The map `κ_H → κ_(∧²H) = 4 κ_H` is just
multiplicative; it does not select a specific value.

In particular: starting from BAE (`κ_H = 2`), antisymmetrization
gives `κ_(∧²H) = 8` (not BAE on ∧²V). Starting from `κ_H = 1/2`,
antisymmetrization gives `κ_(∧²H) = 2` (BAE on ∧²V), but this is
a transformation of an already-chosen `κ_H`, not a constraint that
**selects** BAE.

**Verified numerically (runner Section 3):** all algebraic identities
checked at sample (a, b).

### PA-AV3 — Pauli ground state is C_3-trivial

The totally antisymmetric tensor `ε_{ijk}` on V^⊗3 satisfies

```
(ε)_{σ(0)σ(1)σ(2)} = sign(σ) · ε_{012}
```

for any permutation σ ∈ S_3. Under the cyclic shift `C` (3-cycle (012)),
`sign(C) = +1` (3-cycle is even, ∈ alternating group A_3). Hence

```
(C ⊗ C ⊗ C) · ε = sign(C) · ε = +ε
```

Equivalently: `det(C) = +1`, so the antisymmetric volume form is
**C_3-invariant**.

**Consequence.** The 3-particle Pauli-antisymmetric subspace `∧³V`
(dim 1) carries the **trivial character** of the diagonal C_3 action.
The Pauli-antisymmetric ground state is in the C_3 **trivial isotype**.

This is exactly the diagonal (a-only) sector of `H`. It does **not
touch** the doublet isotype (b sector). Hence Pauli is structurally
**incapable** of constraining |b|²/a².

**Verified numerically (runner Section 4):** `(C ⊗ C ⊗ C) · ε = +ε`
exactly (norm difference < 1e-15).

## Theorem (Probe X structural decoupling)

**Theorem (PAULI-DECOUPLE).** On the physical `Cl(3)` local algebra,
the `Z^3` spatial substrate, the cited Cl(3) per-site uniqueness
surface, the Grassmann partition forcing theorem, the spin-statistics
surface, the `C_3[111]` hw=1 BZ-corner forcing theorem, the `M_3(ℂ)`
operator arena on hw=1, and the C_3-equivariant Hermitian circulant
`H = aI + bC + b̄C²`:

```
(a) The 3-fermion Slater-determinant ground state ψ_Slater ∈ ∧³V
    of the C_3[111] triplet on hw=1 ≅ ℂ³ has total energy

       ⟨ψ_Slater | Σ_i H_i | ψ_Slater⟩ = tr(H) = 3a

    INDEPENDENT of |b|, φ. Any variational principle on this energy
    selects a = 0, NOT BAE. [Verified Section 2, 5.]

(b) The induced operator ∧²H on the 2-particle antisymmetric subspace
    ∧²V has Frobenius mass-squared

       E_⊥(∧²H) = tr((∧²H)²) − tr(∧²H)²/3 = 6|b|²

    IDENTICAL to E_⊥(H) = 6|b|². Antisymmetrization PRESERVES |b|²
    but does not PIN it. The induced κ rescales as κ(∧²H) = 4 κ(H);
    no specific value is selected. [Verified Section 3.]

(c) The totally antisymmetric tensor ε_{ijk} on V^⊗3 transforms under
    the diagonal C_3 action by det(C) = +1 (3-cycle is even).
    Hence ∧³V (1-dim) is in the C_3 TRIVIAL ISOTYPE. The Pauli
    antisymmetric ground state lives in the diagonal (a-only) sector
    of the H decomposition; the off-diagonal b lives in the doublet
    isotype, untouched by Pauli. [Verified Section 4, 6, 8.]

(d) Wave-function extremization functionals built from Pauli:
      F_1 = ⟨Slater|H|Slater⟩       = 3a       (b-independent)
      F_2 = ⟨Slater|H²|Slater⟩      = 3a² + 6|b|²  (no κ constraint)
      F_3 = ⟨Slater|H³|Slater⟩      = polynomial + |b|² cos(3φ) cubic

    None pin κ = a²/|b|². [Verified Section 7.]

(e) Convention robustness: the Slater determinant on the C_3 Fourier
    basis (e_0, e_1, e_2) and on the site basis (|0⟩, |1⟩, |2⟩)
    both carry the trivial C_3 character (det(C) = +1). Pauli's
    C_3-triviality is basis-independent. [Verified Section 8.]

Therefore: Pauli antisymmetrization on the C_3[111] hw=1 triplet
STRUCTURALLY DECOUPLES from the circulant amplitude ratio |b|²/a².
It cannot supply a constraint that selects BAE. The wave-function-
level path (this probe) closes negatively, joining the operator-level
paths (Probes 12-30). The BAE admission count is unchanged. No new
admission. No new axiom.
```

**Proof.** Each item is verified by the runner (53 PASS / 0 FAIL).
Section 0 (setup sanity), Section 1 (eigenstructure), Section 2
(PA-AV1), Section 3 (PA-AV2), Section 4 (PA-AV3), Section 5 (Slater
matrix elements), Section 6 (Fourier-basis Slater), Section 7 (extrema),
Section 8 (convention robustness), Section 9 (Probe 28 comparison),
Section 10 (sharpened conclusion), Section 11 (does-not disclaimers). ∎

## Algebraic root-cause

The decoupling has a clean group-theoretic root. The cyclic group
C_3 = ⟨(012)⟩ ⊂ S_3 has the 3-cycle as its non-trivial generator.
The 3-cycle is an **even** permutation (it is a product of 2
transpositions: (012) = (01)(02)), hence sign(C) = +1.

The determinant character of the natural C_3 representation on V = ℂ³
is therefore `det(C^k) = +1` for all `k = 0, 1, 2`. Hence the
totally antisymmetric C_3-invariant subspace `∧³V` of V^⊗3 carries the
trivial character.

**More general:** for any n-cycle on n elements, `sign(n-cycle) =
(-1)^(n-1)`. For n odd (including n = 3, our case), the n-cycle is
even, and the totally antisymmetric volume form is C_n-invariant.
For n even (e.g., n = 2, 4), the n-cycle is odd, and the volume form
carries the sign character.

So the Pauli-decoupling is **specific to n = 3** (and other odd n) —
it is a feature of the cyclic structure, not an accident of the
Hamiltonian.

## Why this probe is structurally distinct from prior probes

| Probe | Layer | Conclusion |
|---|---|---|
| Probes 12-17 | RP / GNS / character orthogonality / F1 vs F3 (operator) | F1 ≠ canonical at operator level |
| Probes 18-25 | F1-vs-F3 algebra / native lattice / radian / extremization (operator) | F3 canonical from real-dim count |
| Probe 26-29 | Wilson dim / κ test / vertex factor / partial falsification | Same campaign-terminal residue |
| Probe 30 | Radian-from-dimensions (operator) | Same residue, dimensional |
| Probe 28 | INTERACTING dynamics (operator + interaction terms) | F1 absent at interacting level |
| **Probe X** | **WAVE-FUNCTION (Pauli antisymmetrization, Slater det)** | **Pauli is C_3-trivial, structurally decouples** |

Prior probes all attacked at operator level (F1 vs F3 functional,
character orthogonality, interaction terms, etc.). Probe X attacks
at a structurally distinct layer: the **wave-function** built from
Pauli antisymmetrization of fermionic states.

The conclusion is the same — F1 / BAE absent — but the **mechanism**
differs. At operator level, F3 is fixed by the (1, 2) real-dim count
of the C_3 isotype decomposition. At wave-function level, Pauli is
fixed by the **trivial character** of `∧³V` (since 3-cycle is even).

These are **two independent structural decouplings**, both rooted in
C_3 representation theory:

- Operator: real-dim of the C_3 isotype split on Herm_circ(3) is (1, 2).
- Wave-function: ∧³V carries the trivial character (det(C) = +1).

Both close the corresponding path against BAE.

## Sharpened terminal residue

Combining Probe 28 (operator-level) and Probe X (wave-function-level):

> **The (1, 1) multiplicity-counting principle required for F1 / BAE is
> structurally absent from BOTH the operator-level cited content
> (Probe 28: any C_3-covariant interaction preserves the (1, 2)
> real-dim weighting) AND the wave-function-level cited content
> (Probe X: Pauli antisymmetrization is C_3-trivial, decoupled from
> the doublet sector).**

Closing BAE therefore requires admitting a multiplicity-counting
principle as a NEW PRIMITIVE, which is the existing Brannen Amplitude
Equipartition admission. The wave-function-level path does not provide
an alternative.

## Audit scope

This is a bounded_theorem source row. The bounded claim is the
wave-function-level structural obstruction: Pauli antisymmetrization
on the `C_3[111]` triplet is C_3-trivial and decoupled from
`|b|²/a²`. It does not close BAE, does not change any downstream
theorem, and does not introduce a new axiom or admission.

### What this probe DOES

1. Tests whether Pauli antisymmetrization of the 3-generation
   fermionic wave-function on hw=1 ≅ ℂ³ forces |b|²/a² = 1/2 (BAE).
2. Identifies three independent decoupling theorems (PA-AV1, PA-AV2,
   PA-AV3), each verifying that Pauli is structurally incapable of
   constraining |b|²/a².
3. Identifies the algebraic root-cause: `det(C) = +1` (3-cycle is
   even) ⟹ `∧³V` is C_3-trivial ⟹ Pauli ground state in the
   trivial isotype, decoupled from the doublet.
4. Establishes a sharpened terminal residue: F1 / BAE absent from
   both operator-level (Probe 28) AND wave-function-level (Probe X)
   cited content.
5. Cross-references prior 30 probes; closes the wave-function-level
   gap as structurally distinct from all prior attacks.

### What this probe DOES NOT do

1. Does NOT close the BAE-condition.
2. Does NOT add any new axiom or new admission.
3. Does NOT modify any parent theorem.
4. Does NOT change any downstream theorem.
5. Does NOT load-bear PDG values into a derivation step.
6. Does NOT use external surveys as source authority.
7. Does NOT replace Probes 12-30 (it complements them at a structurally
   distinct layer).
8. Does NOT propose an alternative κ value as physical.
9. Does NOT change sister bridge gaps (L3a, L3b, C-iso, W1.exact).

## Honest assessment

**What the probe finds:**

1. **Pauli antisymmetrization on hw=1 ≅ ℂ³ is C_3-trivial.** The
   totally antisymmetric volume form `ε_{ijk}` carries the determinant
   character `det(C) = +1`. So `∧³V` is in the C_3 trivial isotype.

2. **The Pauli ground state lives in the diagonal (a-only) sector.**
   It does not touch the doublet isotype where the off-diagonal
   amplitude `b` resides. Hence Pauli cannot constrain |b|²/a².

3. **The Slater-determinant total energy is `3a` (b-independent).**
   Variational principles on this energy select `a = 0`, not BAE.
   The Frobenius mass-squared of the induced operator on ∧²V is the
   same `6|b|²` as on V; antisymmetrization preserves but does not
   pin.

4. **Wave-function-level extremization functionals do not pin κ.**
   `⟨Slater | H | Slater⟩ = 3a` (linear in a, no b), and
   `⟨Slater | H² | Slater⟩ = 3a² + 6|b|²` (no κ-selecting structure).

5. **The decoupling is rooted in `det(C) = +1`** (3-cycle is even).
   For odd n-cycles on n elements (including n = 3), the
   antisymmetric volume form is C_n-invariant. This is a clean
   group-theoretic fact, not a numerical accident.

**What this probe contributes to the campaign:**

1. **New positive content**: Pauli antisymmetrization is C_3-trivial
   (in the trivial isotype, decoupled from the doublet b-sector).
   This is structurally distinct from any prior 30 operator-level
   probe.
2. **Sharpened residue characterization**: F1 / BAE is absent from
   BOTH operator-level (Probe 28) AND wave-function-level (Probe X)
   cited content. The (1, 2) isotype real-dim count plus the
   trivial det character of ∧³V are TWO INDEPENDENT structural
   decouplings, both rooted in C_3 representation theory.
3. **Thirty-first independent attack**: returns the same campaign-
   terminal-state structural obstruction at a structurally distinct
   layer (wave-function vs operator).

The remaining residue is **maximally sharp**:

> **BAE = (1, 1)-multiplicity-weighted extremum on the additive
> log-isotype-functional class. The (1, 2) real-dim weighting
> (operator-level) is fixed by C_3 representation theory on
> Herm_circ(3); the trivial det character of ∧³V (wave-function-level)
> is fixed by the parity of the 3-cycle. Both close negatively;
> neither cited content layer supplies the (1, 1) multiplicity-
> counting principle required for BAE.**

Closing BAE therefore continues to require admitting a multiplicity-
counting principle as a NEW PRIMITIVE — i.e., a new admission or a
new source distinct from the existing C_3-equivariant operator
content AND the existing fermionic wave-function content. Probe X
makes this requirement maximally explicit at the wave-function-level
layer.

## Cross-references

### Foundational baseline

- Minimal axioms: [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
- Substep-4 AC narrowing (PDG-input prohibition): `STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`

### Fermionic statistics (load-bearing for Pauli)

- Grassmann partition forcing: [`STAGGERED_DIRAC_GRASSMANN_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_GRASSMANN_FORCING_THEOREM_NOTE_2026-05-07.md)
- Spin-statistics S2: [`AXIOM_FIRST_SPIN_STATISTICS_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_SPIN_STATISTICS_THEOREM_NOTE_2026-04-29.md)
- Cl(3) per-site uniqueness: [`AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md)

### C_3 / circulant structure

- BZ-corner forcing: [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md)
- Circulant character / eigenvalue: [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
- Three-generation observable (M_3 algebra on hw=1): [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- Charged-lepton Koide cone equivalence: [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)

### Block-total Frobenius and weight-class structure

- Block-total Frobenius: [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)
- Frobenius isotype-split uniqueness: [`KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md`](KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md)
- MRU weight-class: [`KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md)

### Probe campaign (operator-level)

- Probe 12 (Plancherel/Peter-Weyl): `KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md`
- Probe 13 (real-structure): `KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md`
- Probe 14 (U(1) hunt): `KOIDE_A1_PROBE_RETAINED_U1_HUNT_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe14.md`
- Probe 18 (F1-vs-F3 algebraic): `KOIDE_BAE_PROBE_F1_CANONICAL_FUNCTIONAL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe18.md`
- Probe 21 (native bilinear flow): `KOIDE_BAE_PROBE_NATIVE_LATTICE_FLOW_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe21.md`
- Probe 25 (free-Gaussian extremization): `KOIDE_BAE_PROBE_PHYSICAL_EXTREMIZATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe25.md`
- Probe 28 (interacting dynamics): `KOIDE_BAE_PROBE_INTERACTING_DYNAMICS_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe28.md`

## Validation

```bash
python3 scripts/cl3_koide_x_bae_pauli_2026_05_08_probeX_bae_pauli.py
```

Expected: `=== TOTAL: PASS=53, FAIL=0 ===`

The runner verifies:

1. Section 0 — Setup sanity (C_3 cycle is unitary, order 3,
   det = +1; H = aI + bC + b̄C² is Hermitian, C_3-equivariant).
2. Section 1 — Eigenstructure of H_circ (eigenvalues, sum identities).
3. Section 2 — PA-AV1: Slater(3 fillings) total energy = 3a
   (b-independent, verified across 25 (|b|, φ) values).
4. Section 3 — PA-AV2: ∧²H Frobenius statistics; E_⊥(∧²H) = 6|b|² =
   E_⊥(H); κ rescales by factor 4 but is not pinned.
5. Section 4 — PA-AV3: ε_{ijk} totally antisymmetric;
   (C ⊗ C ⊗ C) · ε = +ε (det(C) = +1 verified).
6. Section 5 — Slater matrix elements (66 (|b|, φ) test points,
   variance < 1e-20).
7. Section 6 — Slater on C_3 Fourier basis (e_0, e_1, e_2);
   C_3-invariance under diagonal action.
8. Section 7 — Wave-function extremization functionals; none pin κ.
9. Section 8 — Convention robustness (site basis vs Fourier basis;
   C_3-equivariant basis changes).
10. Section 9 — Comparison with Probe 28 (operator-level): both close
    negatively; combined sharpened residue.
11. Section 10 — Sharpened conclusion + algebraic root-cause
    (det(n-cycle) = (-1)^(n-1); n=3 case).
12. Section 11 — Does-not disclaimers (no BAE closure, no admission,
    no PDG, no parent-theorem modification).

Total: 53 PASS / 0 FAIL.
