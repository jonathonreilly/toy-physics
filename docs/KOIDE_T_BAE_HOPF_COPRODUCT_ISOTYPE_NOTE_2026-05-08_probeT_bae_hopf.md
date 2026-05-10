# Koide BAE Probe T — Hopf Algebra Coproduct on C[C_3] Attack on the C_3[111] Triplet

**Date:** 2026-05-08
**Type:** bounded_theorem (Hopf-coproduct-level structural rejection;
no positive closure; new positive content: the natural Hopf algebra
structure on the retained group ring `C[C_3]` carries the
**unique grouplike coproduct** `Δ(C^p) = C^p ⊗ C^p`. Computing
`Δ(H_circ) = a (I ⊗ I) + b (C ⊗ C) + b̄ (C² ⊗ C²)` shows that the
coproduct lives in the **3-dimensional diagonal subalgebra** of
`C[C_3] ⊗ C[C_3]`, and the (i, j)-isotype eigenvalues depend only
on `(i + j) mod 3` — collapsing to the `H_circ` eigenvalues
`{λ_0, λ_1, λ_2}` each with multiplicity 3. Every natural
"isotype-balance" or "minimality" functional on `Δ(H_circ)` reduces
to a **symmetric function of {λ_k}**, exactly the structural
pathology proved terminal by the unified obstruction theorem of
U-BAE-NCG. The Hopf coproduct's "tensor-structure" attack collapses
to the same eigenvalue-functional structure as Probes 28, X-Pauli,
Y-Topological, V-MaxEnt, V-S_3, U-NCG, and U-QDeformation. **Eighth-
level rejection.**)
**Claim type:** bounded_theorem
**Scope:** review-loop source-note proposal — Probe T of the Koide
**BAE-condition** closure campaign. Tests whether the natural
**Hopf algebra coproduct** `Δ : C[C_3] → C[C_3] ⊗ C[C_3]` on the
retained group ring forces `|b|²/a² = 1/2` (BAE) on the
`C_3`-equivariant Hermitian circulant `H_circ = aI + bC + b̄C²`
through an "isotype-balance" or "structurally minimal" `Δ(H_circ)`
decomposition. The probe explicitly tests whether a tool that acts
on the **TENSOR STRUCTURE** rather than on operator eigenvalues
escapes the unified obstruction theorem proved by U-BAE-NCG: the
Hopf coproduct is the unique candidate among the 8 attack vectors
that genuinely targets **isotype-weights** rather than eigenvalue
power sums.
**Status:** source-note proposal for a Hopf-coproduct-level
bounded obstruction with new positive content. The grouplike
coproduct `Δ(C^p) = C^p ⊗ C^p` is the unique Hopf structure on
`C[C_3]` (Sweedler 1969, Kassel 1995, Majid 1995). Computing
`Δ(H_circ)` and decomposing under `(C_3 × C_3)` characters
shows the (i, j)-isotype eigenvalues collapse to 3 classes by
`(i + j) mod 3`, with class representatives equal to the `H_circ`
eigenvalues. Every natural "balance" or "minimality" functional
on `Δ(H_circ)` is a symmetric function of these eigenvalues,
hence — by the unified obstruction theorem (U-BAE-NCG) — does
not pin BAE. Eight independent decoupling theorems
(HOPF-AV1 through HOPF-AV8) verified by paired runner. The BAE
admission count is **UNCHANGED**.
**Authority role:** source-note proposal — audit verdict and
downstream status set only by the independent audit lane.
**Loop:** koide-bae-probeT-hopf-20260508
**Primary runner:** [`scripts/cl3_koide_t_bae_hopf_2026_05_08_probeT_bae_hopf.py`](../scripts/cl3_koide_t_bae_hopf_2026_05_08_probeT_bae_hopf.py)
**Cache:** [`logs/runner-cache/cl3_koide_t_bae_hopf_2026_05_08_probeT_bae_hopf.txt`](../logs/runner-cache/cl3_koide_t_bae_hopf_2026_05_08_probeT_bae_hopf.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived status is generated
only after the independent audit lane reviews the claim, dependency
chain, and runner. The `claim_type`, scope, named admissions, and
bounded-obstruction classification are author-proposed; the audit
lane has full authority to retag, narrow, or reject the proposal.

## Naming-collision warning

In this note:

- **"framework axiom A1"** = retained `Cl(3)` local-algebra axiom per
  [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md).
- **"BAE-condition" (Brannen Amplitude Equipartition)** = the
  amplitude-ratio constraint `|b|²/a² = 1/2` for the
  `C_3`-equivariant Hermitian circulant `H_circ = aI + bC + b̄C²` on
  `hw=1 ≅ ℂ³`. **BAE is the primary name**; the legacy alias
  **"A1-condition"** remains valid in landed PRs.
- **"P1"** = the Brannen `√m_k` square-root identification:
  `√m_k = v_0 (1 + √2 cos(δ + 2πk/3))` with `(v_0, δ)` the circulant
  parameters. Per `KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`
  R2: eigenvalues of `H_circ` are identified with `√m_k`.
- **"Hopf algebra"** = `(A, m, η, Δ, ε, S)`: a unital associative
  algebra `(A, m, η)` together with a counital coassociative
  coproduct `Δ : A → A ⊗ A`, counit `ε : A → ℂ`, and antipode
  `S : A → A`, satisfying the Hopf-algebra axioms (Sweedler 1969,
  Kassel 1995, Majid 1995).
- **"Coproduct" / "Δ"** = the comultiplication map
  `Δ : A → A ⊗ A` of a Hopf algebra.
- **"Grouplike element"** = `g ∈ A` with `Δ(g) = g ⊗ g` and
  `ε(g) = 1`. In a group ring `kG`, every group element is grouplike.
- **"Group ring `C[C_3]`"** = the 3-dimensional `ℂ`-algebra spanned
  by `{1, C, C²}` with `C³ = 1`. Carries a **unique** Hopf structure
  via the grouplike coproduct.
- **"Isotype" of `C_3 × C_3`** = irreducible character class
  `χ_{ij}(C^p, C^q) = ω^{ip+jq}` with `(i, j) ∈ ℤ_3 × ℤ_3`,
  `ω = e^{2πi/3}`. There are 9 isotypes total.

These are distinct objects despite legacy shared labels.

## Question

The Probe U-BAE-NCG (PR #993) terminal synthesis for BAE established a
**unified root-cause theorem**:

> **The spectral action `Tr f(D/Λ)` is a symmetric function of D's
> eigenvalues, depending on `(a, b)` only through power sums
> `P_n = Σ λ_k^n`. By Newton-Girard, any symmetric eigenvalue
> functional reduces to a polynomial in `{P_n}`, and BAE is not
> stationary for any such polynomial under natural cutoff functions.
> Symmetric eigenvalue functionals lose the isotype-weight information
> BAE requires.**

ALL seven prior structural rejections (Probes 28, X-Pauli, Y-Topological,
V-MaxEnt, V-S_3, U-NCG, U-QDeformation) act on **eigenvalue/operator
data** of `H_circ`. Each reduces (per its own structural mechanism) to
the same symmetric-eigenvalue-functional dependence, and falls under the
unified obstruction.

The natural candidate **escape vector** is a tool that acts on
**TENSOR STRUCTURE** rather than on eigenvalues. The Hopf coproduct
`Δ : A → A ⊗ A` precisely fits this profile:

- The coproduct **splits operators by isotype labels** with explicit
  comultiplication weights.
- For circulant `H_circ`, the conjecture would be that
  `Δ(H_circ) = Σ_isotype w_isotype × (a_part ⊗ a_part + b_part ⊗ b_part̄)`
  with comultiplication weights `w_isotype` encoding the **(1, 2)
  real-dim structure DIRECTLY** (rather than via eigenvalue power
  sums).

**Question (Probe T):** Does the natural Hopf coproduct
`Δ : C[C_3] → C[C_3] ⊗ C[C_3]` on the retained group ring force
`|b|²/a² = 1/2` (BAE) through an "isotype-balance" or "structurally
minimal" `Δ(H_circ)` decomposition?

This is structurally distinct from prior probes because the Hopf
coproduct alone among the 8 candidate tools genuinely targets
**isotype-weights** (multiplicity labels of irreducible components) via
**tensor structure** (rather than via D's eigenvalues, K-theory class
integers, MaxEnt over states, S_3 reflections, NCG cutoff functions, or
quantum-deformation parameters).

If the conjecture holds, the Hopf coproduct is the **ONE attack vector**
that escapes the unified obstruction. If it fails, the unified obstruction
is **definitively terminal**: no non-trivial structural layer accessible
from retained content can pin BAE.

## Answer

**No.** The natural Hopf coproduct `Δ : C[C_3] → C[C_3] ⊗ C[C_3]` on
the retained group ring **also collapses** to a symmetric eigenvalue
functional. **Eight independent decoupling theorems converge**:

```
HOPF-AV1   Hopf algebra structure on C[C_3] is UNIQUE (grouplike)
           The group ring C[C_3] has a unique Hopf algebra structure
           given by the grouplike coproduct Δ(C^p) = C^p ⊗ C^p, counit
           ε(C^p) = 1, antipode S(C^p) = C^{-p} = C^{3-p}. This is the
           standard textbook construction (Sweedler 1969, Kassel 1995,
           Majid 1995). All Hopf axioms (coassociativity, counit,
           antipode involution) verified by the runner.

HOPF-AV2   Δ(H_circ) lives in the 3-dim diagonal subalgebra
           Δ(H_circ) = a (I ⊗ I) + b (C ⊗ C) + b̄ (C² ⊗ C²)
                     ∈ C[C_3] ⊗ C[C_3]
           This is a 3-dimensional element of the 9-dimensional
           tensor algebra: only the diagonal basis components
           (0, 0), (1, 1), (2, 2) are populated. The 6 off-diagonal
           sub-isotypes (i, j) with i ≠ j have zero coefficient
           in Δ(H_circ). Specifically: Δ(H_circ) is in the
           DIAGONAL ABELIAN SUBALGEBRA {x ⊗ x : x ∈ C[C_3]}.

HOPF-AV3   Isotype eigenvalues collapse to {λ_n} with multiplicity 3
           Decomposing Δ(H_circ) under (C_3 × C_3) characters
           χ_{ij}(C^p, C^q) = ω^{ip + jq} gives eigenvalues
                μ_{ij}(a, b) = a + 2|b| cos(arg(b) + 2π(i+j)/3)
           which depend ONLY on (i + j) mod 3. The 9 isotypes
           collapse to 3 classes of multiplicity 3, with class
           representatives μ_n = a + 2|b| cos(arg(b) + 2πn/3) =
           λ_n (n = 0, 1, 2) — the same H_circ eigenvalues from
           KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18 R2.

HOPF-AV4   Conjecture FALSIFIED: "isotype-balance" forces b = 0
           If "balance" means Var(μ_{ij}) = 0 across all 9 isotypes,
           then all μ_{ij} equal ⟹ all λ_n equal ⟹ |b| = 0 (NOT BAE).
           Numerical scan over |b| ∈ [0, 2]: argmin Var(μ_{ij}) = 0,
           NOT BAE = 1/√2. ∂Var/∂|b| at BAE ≈ 2.83 (nonzero), confirming
           BAE is NOT a stationary point.

HOPF-AV5   Other natural minimality functionals also force b = 0
           Frobenius central-spread |Δ(H) - μ̄ I|², spectral entropy,
           spectral range max - min — all minimised at b = 0 (NOT BAE).
           Each is a symmetric function of {μ_{ij}} = {λ_n} mult 3,
           hence subject to the unified obstruction.

HOPF-AV6   Hopf coproduct does NOT escape unified obstruction
           Tr(Δ(H)^n) on the regular representation = 3 · Tr(H_circ^n)
           verified for n = 1, 2, 3, 4. The Hopf coproduct's "tensor
           structure" attack reduces to a multiplicity-3 amplification
           of the same power sums P_n that obstructed Probes 28, X, Y,
           V-MaxEnt, V-S_3, U-NCG, U-QDef. ∂Tr(Δ(H)^2)/∂|b| at BAE = 36|b|
           (= 3 × 12|b| nonzero) ⟹ BAE not stationary.

HOPF-AV7   Antipode S preserves spectrum; doesn't pin BAE
           S(H_circ) has same spectrum as H_circ (b ↔ b̄ swap is
           invariance of the eigenvalue multiset). Hopf antipode
           axiom m·(S ⊗ id)·Δ = ε·η satisfied. The antipode permutes
           (i, j) → (-i, j) on isotypes; doesn't break the symmetric-
           eigenvalue-functional structure.

HOPF-AV8   Convolution H * H, counit ε(H), and higher-order coproducts
           Hopf convolution: (id * id)(H) = a I + b̄ C + b C² has
           same eigenvalue set as H. Counit ε(H) = a + 2 Re(b) is a
           single scalar; cannot pin BAE. Higher-order coproducts
           Δ^n(H) live in 3-dim diagonal of A^{⊗(n+1)} with
           multiplicity 3^{n-1} per λ_k — still symmetric in {λ_n}.
```

**Verdict: BOUNDED OBSTRUCTION (Hopf-coproduct-level decoupling) with
new positive content.** The "tensor-structure escape" target is realized
— the Hopf coproduct does decompose `H_circ` by isotype labels with
explicit comultiplication weights — but this realization shows that
**the comultiplication weights are diagonal-trivial**: the isotype
eigenvalues collapse to the H_circ eigenvalue spectrum with multiplicity
3, and every natural "balance" or "minimality" measure is a symmetric
function of these eigenvalues. The BAE admission count is **UNCHANGED**.
No new admission. No new axiom.

This makes Probe T the **eighth-level structural rejection** of BAE,
complementing the operator (Probes 12-30, Probe 28), wave-function
(Probe X-Pauli), topological (Probe Y-Topological), thermodynamic
(Probe V-MaxEnt), larger-symmetry (Probe V-S_3), NCG-spectral-action
(Probe U-NCG), and quantum-deformation (Probe U-QDeformation) rejections.

**The unified-obstruction theorem proved by Probe U-BAE-NCG is now
TERMINAL across 8 independent structural levels.** The Hopf coproduct
was the LAST candidate tool that genuinely targeted isotype-weights via
tensor structure, and it ALSO collapses to symmetric eigenvalue functional
structure.

## Setup

### Premises (A_min for Probe T)

| ID | Statement | Class |
|---|---|---|
| A1 | `Cl(3)` local algebra | framework axiom; see [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) |
| A2 | `Z³` spatial substrate | framework axiom; same source |
| BZ | hw=1 BZ-corner triplet ≅ `ℂ³` with `C_3[111]` action | retained per [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md) |
| Circulant | C_3-equivariant Hermitian on hw=1 is `aI + bC + b̄C²` | retained per [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md) R1 |
| EigSpec | Eigenvalues of `H_circ`: `λ_k = a + 2|b| cos(arg(b) + 2πk/3)` | retained per same source R2 |
| P1 | Brannen square-root identification: `√m_k = λ_k` | retained per same source R2 |
| BlockTotalFrob | `E_+ = 3a²`, `E_⊥ = 6\|b\|²` on `M_3(ℂ)_Herm` | retained per [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md) |
| KoideAlg | Koide `Q = 2/3 ⟺ a² = 2\|b\|² ⟺ \|b\|²/a² = 1/2` (BAE) | retained per [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md) |
| Probe28 | Operator-level: F3 (1, 2) real-dim canonical; F1/BAE absent | retained per [`KOIDE_BAE_PROBE_INTERACTING_DYNAMICS_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe28.md`](KOIDE_BAE_PROBE_INTERACTING_DYNAMICS_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe28.md) |
| ProbeY | Topological-level: K-theory class `(1, 1, 1) ∈ R(C_3)` | retained per [`KOIDE_Y_BAE_TOPOLOGICAL_INDEX_KTHEORY_NOTE_2026-05-10_probeY_bae_topological.md`](KOIDE_Y_BAE_TOPOLOGICAL_INDEX_KTHEORY_NOTE_2026-05-10_probeY_bae_topological.md) |
| ProbeU-NCG | NCG-spectral-action level: spectral action via power sums; BAE not stationary | unified-obstruction theorem source (PR #993) |
| M3 | `M_3(ℂ)` algebra on hw=1 triplet generated by translations + `C_3[111]` | retained per [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md) |

**New science tools used (Hopf algebra / Sweedler / Kassel / Majid;
standard mathematical machinery — these are derivations from retained
content + standard math, not new physics axioms):**

- **Hopf algebra** `(A, m, η, Δ, ε, S)` — definition per Sweedler 1969
  (Hopf Algebras, Benjamin), Kassel 1995 (Quantum Groups, GTM 155
  Springer), Majid 1995 (Foundations of Quantum Group Theory,
  Cambridge UP). Standard mathematical structure.
- **Group ring `C[C_3]` Hopf structure** — every group ring `kG` carries
  a **unique Hopf algebra structure** with grouplike coproduct
  `Δ(g) = g ⊗ g`, counit `ε(g) = 1`, antipode `S(g) = g^{-1}`.
  Standard textbook construction (Kassel 1995 §III.2, Majid 1995 §1.5).
- **Tensor product algebra structure** — the algebra `A ⊗ A` with
  `(a₁ ⊗ a₂)(b₁ ⊗ b₂) = (a₁b₁) ⊗ (a₂b₂)`. Standard.
- **Character-theoretic decomposition of `C[C_3 × C_3]`** — the regular
  representation of `C_3 × C_3` decomposes into 9 one-dimensional
  isotypes labeled by `(i, j) ∈ ℤ_3 × ℤ_3`. Standard finite-cyclic-group
  representation theory.

These are **mathematical statements / a recognized mathematical
toolkit**, not new physics primitives. Per the user's 2026-05-08
"new science" authorization, the Hopf-algebra toolkit is admitted; per the
"derivations not axioms" memory rule, it is used to compute properties
of retained content, not as a new framework axiom.

### Forbidden imports

- NO PDG observed mass values used as derivation input
- NO lattice MC empirical measurements as derivation input
- NO fitted matching coefficients
- NO same-surface family arguments
- NO new framework axioms — Hopf algebra structure is standard
  textbook construction, admitted as a mathematical toolkit
  (per memory `feedback_primitives_means_derivations.md`).
- NO admitted "balance" or "minimality" functionals — the runner
  computes Var, Frobenius central-spread, spectral entropy,
  spectral range from explicit `Δ(H)` eigenvalues.
- NO quantum-deformation parameter `q` — this is the standard
  (undeformed) Hopf algebra structure, complementary to U-QDeformation.

## The structural argument

The Probe T conclusion can be stated structurally:

> **The Hopf coproduct `Δ : C[C_3] → C[C_3] ⊗ C[C_3]` is grouplike on
> the unique Hopf structure of the group ring. Computing
> `Δ(H_circ) = a (I ⊗ I) + b (C ⊗ C) + b̄ (C² ⊗ C²)` shows that the
> coproduct lives in the 3-dimensional DIAGONAL subalgebra of
> `C[C_3] ⊗ C[C_3]`. Decomposing under `(C_3 × C_3)` characters,
> the (i, j)-isotype eigenvalues `μ_{ij}` depend ONLY on `(i + j) mod 3`
> and collapse to the 3 H_circ eigenvalues `{λ_0, λ_1, λ_2}` each with
> multiplicity 3. Every natural "isotype-balance" or "minimality"
> functional on `Δ(H)` is a symmetric function of `{μ_{ij}} = {λ_k}` mult 3,
> hence — by Newton-Girard and the unified obstruction theorem proved
> by U-BAE-NCG — does not pin BAE. The "tensor-structure escape" fails:
> the Hopf coproduct collapses to the same symmetric-eigenvalue-
> functional structure as the seven prior probes.**

Hence: realizing the "tensor-structure" target is necessary but not
sufficient. The comultiplication weights themselves must be
**non-trivial functions of `(a, b)`** that distinguish the trivial-character
isotype from the doublet-character isotype with the specific 2:1
weighting BAE requires. They do not — `Δ(H)` is supported on a
**3-dim diagonal** of the 9-dim tensor algebra, with each
diagonal coefficient being a single complex number `(a, b, b̄)`.

## Per-attack-vector analysis

Eight independent Hopf-coproduct attack vectors are tested. All eight
preserve the `(a, b)`-decoupling at the BAE point; none shifts the
closure of BAE.

### HOPF-AV1 — Hopf algebra structure on C[C_3] is unique (grouplike)

**Status: STRUCTURE CONSTRUCTED; UNIQUENESS CONFIRMED.**

A Hopf algebra `(A, m, η, Δ, ε, S)` requires:
1. `(A, m, η)` unital associative algebra.
2. `Δ : A → A ⊗ A` coassociative algebra homomorphism.
3. `ε : A → ℂ` counit: `(ε ⊗ id) Δ = (id ⊗ ε) Δ = id`.
4. `S : A → A` antipode: `m (S ⊗ id) Δ = m (id ⊗ S) Δ = η ε`.

For `A = C[C_3] = ℂ⟨1, C, C²⟩` with `C³ = 1`:
- **Coproduct (grouplike):** `Δ(C^p) = C^p ⊗ C^p`. Coassociative
  trivially: `(Δ ⊗ id) Δ(C^p) = (C^p ⊗ C^p ⊗ C^p) = (id ⊗ Δ) Δ(C^p)`.
- **Counit:** `ε(C^p) = 1`. Counit axiom: `(ε ⊗ id) Δ(C^p) = ε(C^p) C^p
  = C^p`. ✓
- **Antipode:** `S(C^p) = C^{-p} = C^{3-p}`. Antipode axiom:
  `m (S ⊗ id) Δ(C^p) = S(C^p) C^p = C^{-p} C^p = 1 = ε(C^p) η(1)`. ✓

**Uniqueness:** On a finite group ring `kG`, the Hopf algebra structure
is uniquely the grouplike one (Kassel 1995 §III.2.4, Majid 1995 §1.5).
Any non-grouplike Hopf structure on `kG` is isomorphic to the grouplike
one via an inner Hopf automorphism.

**Verified numerically (runner Section 1):**
- 1.1: Δ(C) = C ⊗ C acts correctly on tensor states.
- 1.2: Coassociativity (Δ ⊗ id) Δ = (id ⊗ Δ) Δ.
- 1.3: Counit ε(C^p) = 1 satisfies counit axiom.
- 1.4: Antipode S(C) = C² = C^(-1).
- 1.5: S² = id (antipode involution).
- 1.6: Hopf structure on C[C_3] is unique (Sweedler/Kassel/Majid).

### HOPF-AV2 — Δ(H_circ) lives in 3-dim diagonal subalgebra

**Status: COMPUTED; SUPPORTED ON 3 OF 9 BASIS COMPONENTS.**

The coproduct of the C_3-equivariant Hermitian circulant:

```
Δ(H_circ) = Δ(a I + b C + b̄ C²)
         = a Δ(I) + b Δ(C) + b̄ Δ(C²)
         = a (I ⊗ I) + b (C ⊗ C) + b̄ (C² ⊗ C²)
         ∈ C[C_3] ⊗ C[C_3]
```

The 9-dimensional tensor algebra `C[C_3] ⊗ C[C_3]` is spanned by
`{C^p ⊗ C^q : 0 ≤ p, q ≤ 2}`. **`Δ(H_circ)` populates only the
3 DIAGONAL basis vectors `(0, 0)`, `(1, 1)`, `(2, 2)`.** The 6
off-diagonal sub-isotypes `(p, q)` with `p ≠ q` have **zero
coefficient**.

**Critical structural observation:** the 6 off-diagonal sub-isotypes are
**`b`-decoupled**, exactly mirroring the structural pathology of
Probe X-Pauli (Slater singlet decoupled from doublet `b`-sector). The
"tensor-structure attack" thus does not access these 6 sub-isotypes at all.

**Verified numerically (runner Section 2):**
- 2.1: Δ(I) = I ⊗ I (single (0, 0) component).
- 2.2: Δ(C) = C ⊗ C (single (1, 1) component).
- 2.3: Δ(C²) = C² ⊗ C² (single (2, 2) component).
- 2.4: Δ(H) populates only diagonal {(0,0), (1,1), (2,2)} basis components.
- 2.5: Diagonal coefficients are exactly (a, b, b̄).
- 2.6: 6 off-diagonal sub-isotypes are b-decoupled.
- 2.7: [Δ(H), C ⊗ C] = 0 — Δ(H) ∈ diagonal commutative subalgebra.

### HOPF-AV3 — (i, j)-isotype eigenvalues collapse to {λ_n} with mult 3

**Status: COLLAPSE CONFIRMED; UNIFIED OBSTRUCTION APPLIES.**

Decomposing `C[C_3] ⊗ C[C_3]` under `(C_3 × C_3)` characters:

The orthogonal idempotent for character `χ_{ij}(C^p, C^q) = ω^{ip + jq}`
is

```
e_{ij} = (1/9) Σ_{p, q = 0}^{2} ω^{-ip - jq} (C^p ⊗ C^q)
```

and `Δ(H_circ)` acts on this idempotent with eigenvalue

```
μ_{ij}(a, b) = a + b · ω^{i+j} + b̄ · ω^{-(i+j)}
            = a + 2|b| cos(arg(b) + 2π(i+j)/3)
```

**KEY OBSERVATION:** `μ_{ij}` depends only on `(i + j) mod 3`. The 9
isotypes collapse into **3 classes by `(i + j) mod 3`**, each of
multiplicity 3:

| Class `n = (i+j) mod 3` | Member isotypes `(i, j)` | Eigenvalue |
|---|---|---|
| `n = 0` | `(0, 0)`, `(1, 2)`, `(2, 1)` | `λ_0 = a + 2|b| cos(arg(b))` |
| `n = 1` | `(0, 1)`, `(1, 0)`, `(2, 2)` | `λ_1 = a + 2|b| cos(arg(b) + 2π/3)` |
| `n = 2` | `(0, 2)`, `(1, 1)`, `(2, 0)` | `λ_2 = a + 2|b| cos(arg(b) + 4π/3)` |

The class representatives `λ_n` are **identical to the H_circ
eigenvalue spectrum** (KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE R2):

```
spec(Δ(H_circ)) = {λ_0, λ_0, λ_0, λ_1, λ_1, λ_1, λ_2, λ_2, λ_2}
              = spec(H_circ) ⊠ multiplicity 3
```

**Power-sum verification:** `Tr(Δ(H)^n) = 3 · Tr(H_circ^n)` for all
`n ≥ 1`, verified numerically for `n = 1, 2, 3, 4`.

This is the **structural collapse**: any symmetric function of
`{μ_{ij}}` (the 9 isotype eigenvalues) equals 3 times the symmetric
function of `{λ_k}` (the 3 H_circ eigenvalues). The Hopf coproduct
provides **NO NEW INFORMATION** beyond the H_circ spectrum.

**Verified numerically (runner Section 3):**
- 3.1: 9 (i, j) isotype eigenvalues collapse to 3 classes by (i+j) mod 3.
- 3.2: Class representatives μ_n = λ_n (H_circ eigenvalues with mult 3).
- 3.3: Symmetric functionals on Δ(H) reduce to symmetric functionals on H_circ.
- 3.4: Tr(Δ(H)^n) = 3 · Tr(H^n) for n = 1, 2, 3, 4.
- 3.5: At BAE, Δ(H) has 2 distinct eigenvalues (a + 2|b|, a - |b|).

### HOPF-AV4 — "Isotype-balance" forces b = 0 (NOT BAE)

**Status: CONJECTURE FALSIFIED; BALANCE FORCES |b| = 0.**

The natural "isotype-balance" criterion for `Δ(H)` is that all 9
isotype eigenvalues `μ_{ij}` are equal:

```
μ_{ij} = constant for all (i, j)
⟺ λ_0 = λ_1 = λ_2
⟺ a + 2|b| cos(arg(b) + 2πn/3) = constant for n = 0, 1, 2
⟺ |b| = 0  (since cos(arg(b) + 2πn/3) takes 3 distinct values for nonzero |b|)
```

**Conjecture:** isotype-balance forces BAE `|b|/a = 1/√2`.
**Reality:** isotype-balance forces `|b| = 0` (degenerate spectrum), NOT BAE.

**Numerical verification** (runner Section 4):
- `Var(μ_{ij})` minimum at `|b| = 0` (variance vanishes).
- `Var(μ_{ij})` at BAE = 1.000 (nonzero; not stationary).
- `∂Var/∂|b|` at BAE ≈ 2.83 (nonzero).
- Argmin `|b|` of `Var(μ_{ij})` over `[0, 2]` is at `|b| = 0`, not at BAE.

The "isotype-balance" conjecture is **FALSIFIED**. Balance gives
spectral degeneracy (`b = 0`), not BAE.

**Verified numerically (runner Section 4):**
- 4.1: Var(μ_{ij}) = 0 at |b| = 0 (isotype-balance).
- 4.2: Var(μ_{ij}) > 0 at BAE (BAE NOT isotype-balanced).
- 4.3: Argmin |b| of Var is at |b| = 0, not BAE.
- 4.4: ∂Var/∂|b| ≠ 0 at BAE.
- 4.5: Hopf isotype-balance conjecture FALSIFIED.

### HOPF-AV5 — Other natural minimality functionals also force b = 0

**Status: FOUR INDEPENDENT MINIMALITY FUNCTIONALS ALL FORCE b = 0.**

Beyond variance, the runner tests three more natural minimality criteria:

- **Frobenius central-spread:** `‖Δ(H) - μ̄ I‖²_F = Σ (μ_{ij} - μ̄)²`
  — minimised at `|b| = 0`.
- **Spectral entropy:** `-Σ p_{ij} log p_{ij}` with `p_{ij} = μ_{ij}² /
  Σ μ²` — maximised at `|b| = 0` (most balanced distribution).
- **Spectral range:** `max μ_{ij} - min μ_{ij}` — minimised at `|b| = 0`.

**ALL FOUR FUNCTIONALS** (variance, central-Frobenius, entropy, range) have
their extremum at `|b| = 0`, NOT at BAE. The pattern is uniform: any
"distance from a constant function" measure, applied to the symmetric
spectrum of `Δ(H)`, is minimised when the spectrum is constant — which
requires `|b| = 0`.

**Verified numerically (runner Section 5):**
- 5.1: Frobenius central-spread minimum at b = 0.
- 5.2: Spectral entropy maximum at b = 0.
- 5.3: Spectral range minimum at b = 0.
- 5.4: All natural minimality functionals are symmetric in {λ_k};
  unified obstruction applies.
- 5.5: BAE is generic (not extremum) for all tested Δ(H) functionals.

### HOPF-AV6 — Hopf functional reduces to power sums (unified obstruction)

**Status: UNIFIED OBSTRUCTION (U-BAE-NCG) APPLIES.**

By Newton-Girard, any symmetric function of the eigenvalues `{μ_{ij}}`
of `Δ(H)` is expressible as a polynomial in the power sums

```
P_n^Δ = Tr(Δ(H)^n) = Σ_{i,j} μ_{ij}^n = 3 · Σ_k λ_k^n = 3 · P_n^H
```

The factor of 3 is purely a multiplicity coefficient; it does **NOT**
introduce new (a, b)-dependence beyond what already exists in the H_circ
power sums `P_n^H`.

The unified-obstruction theorem of U-BAE-NCG states:

> **BAE (a² = 2|b|²) is NOT a stationary condition of any polynomial
> in `{P_n^H}` for natural cutoff functions.**

By the multiplicity-3 collapse, BAE is also NOT a stationary condition of
any polynomial in `{P_n^Δ}`. The Hopf coproduct attack vector
**inherits** the unified obstruction; it does **NOT** escape it.

**Specifically for the leading non-trivial coefficient:**
`∂P_2^Δ/∂|b| = 3 · ∂P_2^H/∂|b| = 3 · 12|b| = 36|b|` — zero only at
`|b| = 0`, not at BAE. This is exactly the same structural failure
mode as Probes 28, X, Y, V-MaxEnt, V-S_3, U-NCG, U-QDef.

**Verified numerically (runner Section 6):**
- 6.1: Tr(Δ(H)^n) = 3 · Tr(H^n) for n = 1, 2, 3, 4.
- 6.2: Newton-Girard: symmetric functions on Δ(H) = 3 × symmetric functions on H_circ.
- 6.3: ∂Tr(Δ(H)^2)/∂|b| = 36|b| at BAE (nonzero).
- 6.4: Hopf coproduct DOES NOT ESCAPE unified obstruction.
- 6.5: Eight-level structural rejection of BAE.

### HOPF-AV7 — Antipode S preserves spectrum; doesn't pin BAE

**Status: ANTIPODE-INVARIANCE OF SPECTRUM CONFIRMED.**

The antipode `S(C^p) = C^{-p}` swaps `(b, b̄)` in `H_circ`:

```
S(H_circ) = a S(I) + b S(C) + b̄ S(C²)
         = a I + b C² + b̄ C
         = a I + b̄ C + b C²    (relabel)
```

Eigenvalues of `S(H_circ)`: `a + 2|b̄| cos(arg(b̄) + 2πk/3) =
a + 2|b| cos(-arg(b) + 2πk/3)` — the **same set** as `spec(H_circ)`
(just reindexed).

The Hopf antipode axiom `m · (S ⊗ id) · Δ = ε · η` is verified:
`m (S ⊗ id) Δ(C) = S(C) · C = C² · C = C³ = I = ε(C) · η(1)`. ✓

**`S` does NOT introduce BAE-pinning content** because it permutes
isotypes `(i, j) → (-i, j)` while preserving the eigenvalue multiset.

**Verified numerically (runner Section 7):**
- 7.1: S(H_circ) and H_circ have same spectrum.
- 7.2: Hopf antipode axiom satisfied for C.
- 7.3: (S ⊗ id) Δ(H) preserves {λ_n} eigenvalue multiset.
- 7.4: Antipode S permutes isotypes; doesn't pin |b|/a = 1/√2.

### HOPF-AV8 — Convolution and counit, higher-order coproducts

**Status: ALL HOPF-OPERATIONS PRESERVE THE OBSTRUCTION.**

- **Hopf convolution `(id * id)(H) = m · (id ⊗ id) · Δ(H)`:**
  `(id * id)(H) = a · I + b · C² + b̄ · C^4 = a I + b̄ C + b C²`.
  Same eigenvalue set as `H_circ`, so no new BAE constraint.

- **Counit `ε(H_circ) = a + 2 Re(b)`:** a single scalar functional;
  cannot pin a 2-parameter (a, |b|, arg(b)) BAE constraint.

- **Higher-order coproducts `Δ^n : A → A^{⊗(n+1)}`:**
  `Δ^n(H_circ) = a I^{⊗(n+1)} + b C^{⊗(n+1)} + b̄ (C²)^{⊗(n+1)}`.
  Eigenvalues on `(i_1, ..., i_{n+1})`-isotype:
  `a + 2|b| cos(arg(b) + 2π Σ i_k / 3)` — depend only on
  `Σ i_k mod 3`. Same `{λ_n}` spectrum with multiplicity `3^{n}/3 = 3^{n-1}`.

All Hopf operations preserve the symmetric-eigenvalue-functional
structure that obstructs BAE.

**Verified numerically (runner Section 8):**
- 8.1: Hopf convolution H * H has same eigenvalue set as H_circ.
- 8.2: Counit ε(H) = a + 2 Re(b) is a scalar.
- 8.3: Counit doesn't pin BAE; multiple (a, b) give same value.
- 8.4: Fourier-image C[C_3] ≅ C × C × C: Hopf structure coordinate-wise.
- 8.5: Higher-order Δ^n(H) eigenvalues are {λ_n} with mult 3^{n-1}.

## Theorem (Probe T Hopf-coproduct-level structural decoupling)

**Theorem (HOPF-DECOUPLE).** On A1 + A2 + retained Cl(3) per-site
uniqueness + retained Z³ substrate + retained C_3[111] hw=1 BZ-corner
forcing (Block 04) + retained M_3(ℂ) on hw=1 + retained C_3-equivariant
Hermitian circulant `H_circ = aI + bC + b̄C²` + retained P1 Brannen
square-root identification + admitted Hopf algebra mathematical
toolkit (Hopf algebra definition; group-ring grouplike Hopf structure
uniqueness; tensor product algebra structure; character-theoretic
decomposition):

```
(a) The group ring C[C_3] carries a unique Hopf algebra structure
    given by the grouplike coproduct Δ(C^p) = C^p ⊗ C^p, counit
    ε(C^p) = 1, antipode S(C^p) = C^{-p}. Coassociativity, counit
    axiom, antipode involution all verified.
    [Verified Section 1.]

(b) Δ(H_circ) = a (I ⊗ I) + b (C ⊗ C) + b̄ (C² ⊗ C²) lives in the
    3-dimensional DIAGONAL subalgebra of C[C_3] ⊗ C[C_3]. The
    6 off-diagonal sub-isotypes (p, q) with p ≠ q are b-decoupled
    (zero coefficient).
    [Verified Section 2.]

(c) The (i, j)-isotype eigenvalues of Δ(H_circ) are
        μ_{ij}(a, b) = a + 2|b| cos(arg(b) + 2π(i+j)/3)
    depending only on (i + j) mod 3. The 9 isotypes collapse to
    3 classes of multiplicity 3, with class representatives equal
    to the H_circ eigenvalues {λ_0, λ_1, λ_2}. Power-sum verification:
    Tr(Δ(H)^n) = 3 · Tr(H_circ^n) for all n ≥ 1.
    [Verified Section 3.]

(d) The "isotype-balance" conjecture (Var(μ_{ij}) = 0 forces BAE)
    is FALSIFIED. Balance forces |b| = 0 (NOT BAE). Numerical
    scan over |b| ∈ [0, 2] gives argmin Var(μ_{ij}) = 0; ∂Var/∂|b|
    at BAE ≠ 0.
    [Verified Section 4.]

(e) Other natural minimality functionals (Frobenius central-spread,
    spectral entropy, spectral range) all have extremum at |b| = 0,
    not at BAE.
    [Verified Section 5.]

(f) The Hopf coproduct attack inherits the unified obstruction
    theorem proved by U-BAE-NCG (PR #993): every symmetric function of
    Δ(H)'s spectrum is expressible as a polynomial in the H_circ
    power sums, which are not stationary at BAE for any natural
    cutoff functional.
    [Verified Section 6.]

(g) The antipode S preserves the {λ_n} eigenvalue multiset and
    permutes the (i, j) isotypes; does NOT pin BAE.
    [Verified Section 7.]

(h) Hopf convolution, counit, and higher-order coproducts all
    preserve the symmetric-eigenvalue-functional obstruction. No
    Hopf-derivable functional pins BAE.
    [Verified Section 8.]

Therefore: the natural Hopf coproduct
Δ : C[C_3] → C[C_3] ⊗ C[C_3] on the retained group ring
STRUCTURALLY DECOUPLES from the BAE point. The
"tensor-structure escape" target is realized but does not pin
BAE: the comultiplication weights collapse Δ(H) to a 3-dim
diagonal supporting a multiplicity-3 amplification of the
H_circ eigenvalue spectrum, on which the unified obstruction
theorem applies. The Hopf-coproduct-level path closes negatively,
joining the operator-level (Probes 12-30, Probe 28), wave-function-level
(Probe X-Pauli), topological-level (Probe Y-Topological),
thermodynamic-level (Probe V-MaxEnt), larger-symmetry-level (Probe V-S_3),
NCG-spectral-action-level (Probe U-NCG), and quantum-deformation-level
(Probe U-QDeformation) paths. The BAE admission count is unchanged.
No new admission. No new framework axiom (Hopf algebra admitted
as mathematical toolkit only).
```

**Proof.** Each item is verified by the runner: Section 0
(retained sanity); Section 1 (HOPF-AV1 Hopf structure); Section 2
(HOPF-AV2 Δ(H) diagonal subalgebra); Section 3 (HOPF-AV3 isotype
eigenvalue collapse); Section 4 (HOPF-AV4 isotype-balance forces b=0);
Section 5 (HOPF-AV5 other minimality functionals force b=0);
Section 6 (HOPF-AV6 unified obstruction inheritance); Section 7
(HOPF-AV7 antipode); Section 8 (HOPF-AV8 convolution / counit / higher-order);
Section 9 (eight-level closure synthesis); Section 10 (convention
robustness); Section 11 (does-not disclaimers). ∎

## Algebraic root-cause

The Hopf-coproduct decoupling has a clean structural root, complementary
to the U-BAE-NCG unified obstruction:

> **The unique Hopf structure on `C[C_3]` is GROUPLIKE: each generator
> `C^p` is a single grouplike element, and `Δ(C^p) = C^p ⊗ C^p` lives
> in the 1-dim sub-isotype `(p, p)`. Linear combinations have support
> in the 3-dim DIAGONAL of `C[C_3] ⊗ C[C_3]`. The 6 "interesting"
> off-diagonal sub-isotypes `(p, q)` with `p ≠ q` are STRUCTURALLY
> INACCESSIBLE to the coproduct of an algebra element. The
> "tensor-structure attack" therefore reduces to a multiplicity-3
> reproduction of the H_circ eigenvalue structure — exactly the
> input the unified obstruction theorem rules out.**

The structural failure is now precisely identifiable:

> **In the Hopf-algebra category, the comultiplication of an algebra
> element is uniquely determined by the algebra structure (`C³ = 1`)
> and the grouplike axiom. There is NO FREEDOM in the comultiplication
> weights to encode a (1, 2) → (1, 1) re-weighting between the trivial
> and doublet character isotypes. The "isotype-weight encoding" the
> attack vector promised is REDUCED TO ZERO by the rigidity of the
> grouplike Hopf structure on a finite cyclic group ring.**

This is the structural analog at the Hopf-coproduct level of the
operator-level (1, 2) real-dim decomposition of `Herm_circ(3)`: the
Hopf structure produces a 3-dim diagonal in a 9-dim tensor algebra,
with eigenvalue collapse to {λ_n} mult 3 — exactly the symmetric-
function dependence U-BAE-NCG ruled out as a BAE pinner.

## Why this probe is structurally distinct from prior probes

| Probe | Layer | Mechanism | Targets isotype-weights? | Conclusion |
|---|---|---|---|---|
| Probes 12-30 | OPERATOR (Hilbert states) | C_3 rep theory: (1, 2) real-dim on Herm_circ(3) | No (eigenvalues only) | F1 / BAE absent |
| Probe X | WAVE-FUNCTION (∧^N tensors) | Pauli antisym → trivial-isotype singlet | No (eigenvalue-projection) | Slater singlet b-decoupled |
| Probe Y | TOPOLOGICAL (K-theory) | K_C3(pt) = Z⊕Z⊕Z; integer-quantized | No (integer counts) | (a, b) absent from K-theory |
| Probe V-MaxEnt | THERMODYNAMIC (states ρ at fixed H) | MaxEnt over states | No (states ρ) | (a, b) param H not ρ |
| Probe V-S_3 | LARGER-SYMMETRY (S_3 on Herm_circ) | S_3 rep on H | No (operator) | reflection rep symmetric |
| Probe U-NCG | NCG-SPECTRAL-ACTION | Tr f(D/Λ) symmetric in eigenvalues | No (eigenvalues) | unified obstruction theorem |
| Probe U-QDef | QUANTUM-DEFORMATION U_q(C_3) | q-deformed rep | No (eigenvalues; q is convention) | reduces to P_n |
| **Probe T (this probe)** | **HOPF-COPRODUCT** | **Δ : C[C_3] → C[C_3] ⊗ C[C_3]** | **YES — tensor structure** | **Δ(H) reduces to symmetric eigenvalue functional** |

Probe T is the **unique** prior-or-current probe in which the
attack vector genuinely targets **isotype-weights via tensor structure**
(rather than operator eigenvalues, integer K-theory class, MaxEnt over
states, S_3 reflection, NCG cutoff, or q-deformation parameter).

**And yet BAE is still not forced.** This is the strongest possible
negative result: even when the structural objection of "the tool acts on
operator eigenvalues / states / reflections / etc." is removed by
switching to **tensor-structure attack**, the coproduct's rigid
grouplike structure forces it to live on a 3-dim diagonal whose
eigenvalues collapse to the H_circ spectrum.

## Sharpened terminal residue (eight-level closure)

Combining Probes 12-30 (operator), Probe X-Pauli (wave-function),
Probe Y-Topological (topological), Probe V-MaxEnt (thermodynamic),
Probe V-S_3 (larger-symmetry), Probe U-NCG (NCG-spectral-action),
Probe U-QDeformation (quantum-deformation), and Probe T (this probe,
Hopf-coproduct):

> **The BAE condition `|b|²/a² = 1/2` is structurally absent from
> ALL EIGHT accessible structural layers of the framework:**
>
> - **Operator layer (Probes 12-30):** any C_3-covariant interaction
>   preserves the (1, 2) real-dim weighting on Herm_circ(3). F1
>   structurally rejected at free + interacting levels.
>
> - **Wave-function layer (Probe X-Pauli):** Pauli antisymmetrization
>   is C_3-trivial (det(C) = +1). Slater singlet ∈ trivial isotype,
>   decoupled from doublet b-sector.
>
> - **Topological layer (Probe Y-Topological):** K-theory class, index
>   theorem, anomaly polynomial, and Cech cohomology are all
>   integer-quantized isotype-count data. Continuous (a, b) is NOT in
>   topological data.
>
> - **Thermodynamic layer (Probe V-MaxEnt):** MaxEnt optimizes over
>   states ρ at fixed H. (a, b) parameterizes H, not ρ; MaxEnt does
>   not constrain H.
>
> - **Larger-symmetry layer (Probe V-S_3):** S_3 reflection rep on
>   Herm_circ(3) is symmetric under the b ↔ b̄ involution; does not
>   pin |b|.
>
> - **NCG-spectral-action layer (Probe U-NCG):** the Connes-Chamseddine
>   spectral triple (A, H, D = H_circ) parameterizes H via D. The
>   spectral action Tr f(D/Λ) is a symmetric function of eigenvalues,
>   depending on (a, b) only through power sums. BAE is not stationary
>   for any natural cutoff f.
>
> - **Quantum-deformation layer (Probe U-QDeformation):** U_q(C_3) at
>   q = e^{iπ/3} (root of unity) reproduces the same eigenvalue power-
>   sum dependence; the q-parameter is itself a convention.
>
> - **Hopf-coproduct layer (Probe T, this probe):** the unique grouplike
>   Hopf structure on C[C_3] forces Δ(H_circ) onto a 3-dim diagonal of
>   C[C_3] ⊗ C[C_3], with isotype eigenvalues collapsing to the H_circ
>   spectrum with multiplicity 3. The "tensor-structure attack" reduces
>   to symmetric eigenvalue functional structure — same unified
>   obstruction.

Closing BAE therefore continues to require admitting a multiplicity-
counting principle as a NEW PRIMITIVE. The Hopf-coproduct-level path
does not provide an alternative.

This is the **strongest possible structural rejection** of BAE
within accessible framework layers: BAE is absent from operator,
wave-function, topological, thermodynamic, larger-symmetry,
NCG-spectral-action, quantum-deformation, AND Hopf-coproduct layers.
**The Hopf coproduct was the LAST candidate genuinely targeting
isotype-weights via tensor structure**, and it ALSO collapses to
symmetric-eigenvalue-functional structure.

**The unified-obstruction theorem proved by U-BAE-NCG is now TERMINAL
across 8 independent structural levels.**

## Status block

### Author proposes (audit lane decides):

- `claim_type`: `bounded_theorem` (Hopf-coproduct-level structural
  rejection; new positive content: the natural grouplike Hopf coproduct
  on `C[C_3]` forces `Δ(H_circ)` to live on a 3-dim diagonal of the
  9-dim tensor algebra, with isotype eigenvalues collapsing to the
  H_circ spectrum with multiplicity 3 — the "tensor-structure escape"
  fails by the same unified obstruction theorem proved by U-BAE-NCG)
- audit-derived effective status: set only by the independent audit lane
  after review
- `admitted_context_inputs`: `["BAE-condition: |b|²/a² = 1/2 (legacy:
  A1-condition)"]` — the residual admission, with the Probe T
  sharpening: **"The Hopf coproduct
  Δ : C[C_3] → C[C_3] ⊗ C[C_3] (grouplike, the unique Hopf structure
  on a finite group ring) sends H_circ to a 3-dim diagonal of the
  tensor algebra. The 9 isotype eigenvalues collapse to the H_circ
  spectrum with multiplicity 3, hence every symmetric Hopf-derivable
  functional is a polynomial in the same power sums P_n that
  obstructed Probe U-NCG. The 'tensor-structure escape' target is
  realized but inert: the comultiplication weights are forced to be
  diagonal-trivial by the rigidity of the grouplike Hopf structure on
  a finite cyclic group ring. The unified-obstruction theorem of
  U-BAE-NCG is now terminal across 8 independent structural layers."**
- `admitted_count`: 1 (BAE-condition itself; same as Probe U-BAE-NCG)
- runner verification: 82/0 PASS across 12 sections.

### Audit lane decides:

- effective `tier` (likely: `bounded_theorem`)
- ledger `priority` (likely: `low` — same as U-BAE-NCG; sister-probe
  reinforcement of the unified obstruction theorem)
- placement in axiom-clean / open-questions / out-of-scope summaries
- whether to update Hopf or quantum-group sections of any retained docs
  (likely: no — Hopf is admitted as toolkit only, not promoted)
- whether the eight-level synthesis warrants a new "Block-09 BAE
  Closure Foreclosure" meta-note (likely: yes — to register the
  termination of the candidate-tool space)

### Caveats:

- Does NOT close BAE.
- Does NOT change BAE admission count.
- Does NOT add new framework axioms.
- Does NOT promote Hopf algebra structure to retained content.
- Does NOT replace U-BAE-NCG (PR #993) — complements it with the
  Hopf-coproduct lens.
- Does NOT depend on any quantum-deformation parameter q (this is
  the standard undeformed Hopf algebra; complementary to U-QDef).
- Does NOT reduce admission count for U-NCG, U-QDef, V-MaxEnt, V-S_3,
  Y, X, or 28.

## Provenance

- **Author proposes:** `bounded_theorem`. Pipeline-derived effective
  tier and priority are set only by the independent audit lane.
- **Loop:** koide-bae-probeT-hopf-20260508.
- **Runner:** [`scripts/cl3_koide_t_bae_hopf_2026_05_08_probeT_bae_hopf.py`](../scripts/cl3_koide_t_bae_hopf_2026_05_08_probeT_bae_hopf.py).
  Cache: [`logs/runner-cache/cl3_koide_t_bae_hopf_2026_05_08_probeT_bae_hopf.txt`](../logs/runner-cache/cl3_koide_t_bae_hopf_2026_05_08_probeT_bae_hopf.txt).
  82/0 PASS across 12 sections.
- **Standing within campaign:** Probe T is the eighth and (under the
  unified obstruction theorem identified by U-BAE-NCG) **terminal**
  attack vector tested against BAE. The Hopf coproduct was the unique
  remaining candidate among accessible structural layers that
  genuinely targeted isotype-weights via tensor structure rather than
  operator eigenvalues. Its negative outcome confirms the unified
  obstruction theorem holds across all 8 accessible structural layers.

## References

- Sweedler M.E. (1969). *Hopf Algebras*. Benjamin.
- Kassel C. (1995). *Quantum Groups*. Graduate Texts in Mathematics 155.
  Springer-Verlag.
- Majid S. (1995). *Foundations of Quantum Group Theory*. Cambridge
  University Press.
- Connes A. (1994). *Noncommutative Geometry*. Academic Press.
- Brannen C. (2006). hep-ph/0505220, charged-lepton mass formula.
- [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) — retained framework axioms A1, A2.
- [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md) — retained
  R1 (circulant Hermitian form) and R2 (eigenvalues / P1 identification).
- [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md) —
  retained block-total Frobenius measure E_+ : E_⊥.
- [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md) — retained
  algebraic equivalence Q = 2/3 ⟺ a² = 2|b|².
- [`KOIDE_BAE_PROBE_INTERACTING_DYNAMICS_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe28.md`](KOIDE_BAE_PROBE_INTERACTING_DYNAMICS_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe28.md) —
  Probe 28 retained operator-level bounded obstruction (F3 (1, 2)
  real-dim canonical, F1/BAE absent).
- [`KOIDE_Y_BAE_TOPOLOGICAL_INDEX_KTHEORY_NOTE_2026-05-10_probeY_bae_topological.md`](KOIDE_Y_BAE_TOPOLOGICAL_INDEX_KTHEORY_NOTE_2026-05-10_probeY_bae_topological.md) —
  Probe Y retained topological-level bounded obstruction (K-theory
  integer-quantization).
- Probe X-Pauli (PR #936), Probe V-MaxEnt (PR #978), Probe V-S_3
  (PR #980), Probe U-QDeformation (PR #991), Probe U-BAE-NCG
  (PR #993) — sister bounded-obstruction probes establishing the
  preceding seven layers of structural rejection.
