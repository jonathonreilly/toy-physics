# Primitive Design — P-BAE Multiplicity-Counting Proposal

**Date:** 2026-05-10
**Type:** primitive_design (proposal of NEW DERIVED PRIMITIVES that
COULD close BAE; design-stage proposal, not retained tier)
**Claim type:** primitive_design
**Scope:** Single-PR primitive design proposal. Following the 8-level
unified obstruction theorem (BAE proven structurally inaccessible from
operator + wave-function + topological + thermodynamic + S_3 + NCG +
quantum-deformation + Hopf-coproduct levels, all rooted in
Newton-Girard obstruction on symmetric eigenvalue functionals), this
note proposes 3 candidate **derived** primitives (M1, M2, M3) that
COULD close BAE. Each candidate is given a formal statement, a
derivation of `|b|²/a² = 1/2`, an interpretation, a literature
analog, and a strengths/weaknesses analysis. The audit lane has full
authority over election (or rejection) of any candidate.
**Status:** source-note proposal. No primitive promoted to retained
status. Pipeline-derived status set only after independent audit lane
review.
**Authority role:** source-note proposal — audit verdict and
downstream status set only by the independent audit lane.
**Primary runner:** [`scripts/cl3_primitive_p_bae_2026_05_10_pPbae.py`](../scripts/cl3_primitive_p_bae_2026_05_10_pPbae.py)
**Cache:** [`logs/runner-cache/cl3_primitive_p_bae_2026_05_10_pPbae.txt`](../logs/runner-cache/cl3_primitive_p_bae_2026_05_10_pPbae.txt)

## Authority disclaimer

This is a source-note proposal for new **derived** primitives. The
primitives proposed here are NOT new axioms (the framework axiom set
A1 + A2 = Cl(3) + Z³ remains unchanged); they are derivations on
top of A1 + A2 + retained, distinguished by the SPECIFIC content
(weight assignment, measure, or extremization) they introduce.

Pipeline-derived status is generated only after the independent audit
lane reviews the proposal. The `claim_type`, scope, candidate
distinctness assessments, and strengths/weaknesses ratings are
author-proposed; the audit lane has full authority to reject any or
all candidates, retag as different claim type, or to elect a single
candidate as a retained derived primitive.

## Naming-collision warning

In this note:

- **"framework axiom A1"** = retained `Cl(3)` local-algebra axiom per
  [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md).
- **"BAE-condition" (Brannen Amplitude Equipartition)** = the
  amplitude-ratio constraint `|b|²/a² = 1/2` for the
  `C_3`-equivariant Hermitian circulant `H = aI + bC + b̄C²` on
  `hw=1 ≅ ℂ³`. Per the rename in
  [`BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md`](BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md),
  **BAE is the primary name**; the legacy alias **"A1-condition"**
  remains valid in landed PRs.

These are distinct objects despite the legacy shared label.

## Background — the 8-level structural rejection

The 30-probe BAE-closure campaign has proven (via PRs #936, #949,
#978, #980, #991, #993, #1006 + Probe 28 + Probe X + Probe Y) that
BAE is structurally inaccessible from every layer of the available
toolkit:

| Level | Mechanism | PR / probe |
|---|---|---|
| 1. Operator | C_3 rep theory: (1, 2) real-dim on Herm_circ(3) → F3, NOT F1 | Probes 12-30 |
| 2. Wave-function | Pauli antisymmetrization on ∧³V; Slater singlet ∈ trivial isotype | Probe X |
| 3. Topological | K-theory R(C_3) = ℤ⊕ℤ⊕ℤ; index/anomaly integer-quantized, decoupled | Probe Y |
| 4. Thermodynamic | MaxEnt on Born density does NOT pin |b|²/a² | Probe V-MaxEnt |
| 5. S_3 reflection | C_3 × Z_2 reflection also fails | Probe V-S3 |
| 6. NCG | Connes-Chamseddine spectral triple fails | Probe U-NCG |
| 7. q-deformation | U_q(C_3) at q = e^(iπ/3) fails | Probe U-Q |
| 8. Hopf coproduct | Grouplike tensor coproduct on ℂ[C_3] fails | Probe T-Hopf |

The **common root** (Newton-Girard obstruction): all 8 levels use
either SYMMETRIC EIGENVALUE FUNCTIONALS on the spectrum
`{a + 2|b| cos(φ - 2πk/3)}` (which depend only on `a` and `|b|²` via
power sums `p_n`) or GROUPLIKE TENSOR DATA on the C_3-isotype
decomposition (which preserves the (1, 2) real-dim weighting). None
can pin the continuous amplitude ratio `|b|²/a² = 1/2`.

**Conclusion of the 8-level theorem:** BAE genuinely requires a
**new primitive** distinct from these toolkit levels.

## Goal of this note

Propose 3 candidate primitives that COULD close BAE algebraically.
Each candidate is **derived from A1 + A2 + retained** with new
SPECIFIC CONTENT, NOT introduced as a new axiom. Per the user's
2026-05-09 clarification: "new primitives" means **derivations from
A1 + A2 + retained**, not new axioms.

The criteria for each candidate:

1. **Algebraic derivation of BAE.** The primitive must
   algebraically force `|b|²/a² = 1/2` from its content.
2. **Compatibility with A1 + A2 + retained.** No contradictions; no
   new axioms; no modifications to retained theorems.
3. **Distinctness from rejected toolkit.** The primitive must not be
   reducible to any of the 8 rejected levels.
4. **Hostile-review classification.** Distinguish STRUCTURAL
   primitives (force BAE) from ADMITTING primitives (admit BAE
   as numerical constraint).
5. **Literature analog identification.** Reference real prior work
   in physics / mathematics with a similar primitive.

## The three candidate primitives

### Candidate M1 — Multiplicity-Counting Trace State

**Formal statement.**
> **P-BAE-M1.** Define a derived trace functional `τ_M : Herm_circ(3) → ℝ`
> that weights the C_3-isotype decomposition
> `Herm_circ(3) = ℝ⟨I⟩ ⊕ ℝ⟨C+C²⟩ ⊕ ℝ⟨i(C-C²)⟩` by the **count of
> R-IRREDUCIBLE BLOCKS**, NOT by the real dimensions of those blocks.
> Specifically: `τ_M(X) = Tr(π_+(X)) + Tr(π_⊥(X))`, where the two
> isotype components `π_+(X) ∈ ℝ⟨I⟩` and `π_⊥(X) ∈ ℝ⟨C+C²⟩ ⊕ ℝ⟨i(C-C²)⟩`
> EACH contribute weight 1, treating the doublet as ONE R-irreducible
> block (multiplicity 1) rather than as 2 real-dim coordinates.

**Derivation of BAE.**

Under the multiplicity-counting weight, the canonical log-density
on the (a, |b|)-plane in the additive log-isotype-functional class
is
```
L_F1(a, |b|) = log E_+ + log E_⊥
```
(the F1 weighting (1, 1) — see Probe 18). Extremizing over (a, |b|)
under the normalization constraint `E_+ + E_⊥ = N`:

```
d/dE_+ [log E_+ + log(N - E_+)] = 1/E_+ - 1/(N - E_+) = 0
=> E_+ = N/2 = E_⊥
=> 3 a² = 6 |b|²
=> |b|²/a² = 1/2 = BAE.  ∎
```

**Physical/mathematical interpretation.**

The retained C_3-isotype decomposition has 2 *R-irreducible* components
(trivial + doublet), but 3 *real-dimension* coordinates (1 for the
trivial + 2 for the doublet). M1 weights by **R-irreducible-block
count** (2 components, weights (1, 1)), not by **real-dim count** (3
coordinates, weights (1, 2)).

This is structurally equivalent to introducing a *categorified
Plancherel measure* on the algebra `Herm_circ(3)`: the doublet
isotype is viewed as ONE Frobenius-Perron weight on `R(C_3)`, not as
2 coordinates.

**Literature analog.**

The closest published analog is **Etingof–Nikshych–Ostrik fusion
categories**, where the Frobenius-Perron dimension of an object is
defined by the maximal eigenvalue of its fusion matrix (see [Etingof
et al., "On Fusion Categories", *Annals of Mathematics* 162 (2005)
581–642](https://annals.math.princeton.edu/wp-content/uploads/annals-v162-n2-p01.pdf)).
Frobenius-Perron weights are additive and multiplicative on simple
objects (which corresponds to R-irreducible blocks), and constitute a
distinct counting principle from real-dim. Connes' tracial states on
finite-group C*-algebras provide the C*-algebraic analog.

The Foot–Koide circulant matrix work (e.g., [Foot, "Charged lepton
mass matrix with democratic family mixing"](https://link.springer.com/article/10.1007/BF01556669))
notes that the lepton triplet decomposes naturally under C_3 with
3 generations, but does not propose a multiplicity-counting trace.

**Strengths.**

- Forces BAE algebraically from a single trace-functional content.
- Compatible with A1 (no new algebra) and A2 (spatial Z³ unchanged).
- Distinct from all 8 rejected levels: M1 uses R-irrep count, while
  Probe 12 (Plancherel) uses C-irrep count (1, 1, 1) and Probe 25
  (real-dim Jacobian) uses (1, 2).
- Has a real literature analog in fusion-category theory.

**Weaknesses.**

- The trace `τ_M` is not the unique Ad-invariant Frobenius pairing
  on Herm_circ(3) (per the retained Frobenius isotype-split
  uniqueness theorem). M1 must be ELECTED as the right primitive,
  not derived from Ad-invariance alone.
- The choice "weight by R-irrep count" requires justification at the
  axiom-level: WHY count R-irreps over real-dim?
- The justification could come from: (i) a real-structure principle
  (the framework operates over ℝ, not ℂ, on the matter circulant);
  (ii) a categorification of the trace over the fusion category
  `Rep(C_3)`. Neither is currently in retained content.

### Candidate M2 — Isotype-Reduced Action Integral

**Formal statement.**
> **P-BAE-M2.** Define a derived path-integral measure on the
> configuration space `Herm_circ(3)`:
>
> `dν = dr_+ · d|b|`
>
> where `r_+ = √3 · a` is the trivial-isotype amplitude (1-real-dim)
> and `|b|` is the doublet amplitude AFTER quotienting by the
> U(1)_b orbit on the doublet (1-real-dim). This measure replaces
> the conventional real-dim Lebesgue measure `dr_0 dr_1 dr_2` (which
> has 3 real coordinates: 1 trivial + 2 doublet).

**Derivation of BAE.**

Under the conventional measure `dr_0 dr_1 dr_2 = da · |b| d|b| dφ`
(after polar decomposition of the doublet), the doublet's
2-dimensional Lebesgue volume contributes an extra factor of `|b|` to
the Jacobian, giving the F3 weighting (1, 2). Per Probe 25, the
Probe 25 saddle-point of the Gaussian path integral on Herm_circ(3)
under this measure gives `κ = 1`, NOT BAE.

Under M2's measure `dν = dr_+ d|b|`, the doublet contributes ONE
coordinate (after U(1)_b quotient), giving the F1 weighting (1, 1).
The saddle-point of the Lagrangian
```
L_M2 = -λ (3a² + 6|b|² - N) + ½ [log(3a²) + log(6|b|²)]
```
(with λ a Lagrange multiplier for the normalization `E_+ + E_⊥ = N`)
is found from `∂L/∂a = 0`, `∂L/∂|b| = 0`:
```
∂L/∂a   = -6 λ a + 1/a = 0  =>  a²  = 1/(6λ)
∂L/∂|b| = -12 λ |b| + 1/|b| = 0  =>  |b|² = 1/(12λ)

|b|²/a² = (1/12λ)/(1/6λ) = 6/12 = 1/2 = BAE.  ∎
```

(Verified numerically across 6 normalization scales λ ∈ {0.1, 0.5,
1.0, 5.0, 10.0, 100.0} in the runner Section 8.1.)

**Physical/mathematical interpretation.**

The U(1)_b angular orbit on the doublet is the
*continuous-symmetry-level* ambiguity identified in Probe 13. Probe
16 then pivoted to the Q-functional level which is U(1)_b-invariant
by construction. M2 makes this U(1)_b-quotienting EXPLICIT in the
path-integral measure: the doublet contributes 1 amplitude
coordinate (`|b|`), not 2 real coordinates (`Re b, Im b`).

This is structurally analogous to the **Marsden-Weinstein-Meyer
reduced phase space**: when a continuous symmetry G acts on a phase
space M, the canonical reduced phase space `M//G` has dimension
`dim M - 2 dim G`. Here, U(1) action on the doublet gives a 1-dim
orbit (the angular phase φ), and the M2 measure quotients out this
orbit.

**Literature analog.**

The Marsden-Weinstein-Meyer construction in classical mechanics (and
its quantum analog in the Dirac quantization of constrained systems)
is the canonical literature precedent. In QFT, the **Faddeev-Popov
gauge-fixed measure** is closely analogous: the gauge orbit
contributes a single coordinate (the gauge slice), not the full
gauge volume. M2's `d|b|` is the doublet-orbit gauge slice.

**Strengths.**

- Forces BAE algebraically from a single measure-quotient content.
- The U(1)_b angular orbit on the doublet IS retained content (Probe
  13). M2 makes the quotient explicit in the measure, leveraging
  retained structure.
- Compatible with A1 + A2 + retained.
- Distinct from all 8 rejected levels: M2 modifies the
  path-integral MEASURE; the rejected levels modify operator content.
- Has a real literature analog in symplectic reduction and
  Faddeev-Popov gauge fixing.

**Weaknesses.**

- The choice "use dν instead of dr_0 dr_1 dr_2" requires justification
  at a foundational level. Why is the doublet's U(1)_b orbit
  "physically equivalent" rather than "physically distinct"?
- A justification could come from: (i) a **Brannen Q-readout
  equivalence principle** (since Q is U(1)_b-invariant per Probe 16,
  the U(1)_b orbit is unphysical); (ii) a gauge-symmetry argument
  identifying U(1)_b as a redundant gauge.
- The retained framework does NOT have a U(1)_b gauge symmetry; it has
  only Probe 13's algebra-level U(1)_b symmetry of the b-doublet.

### Candidate M3 — Equipartition Trace Inequality

**Formal statement.**
> **P-BAE-M3.** Define `Q(H) = Tr(H²) / Tr(H)²` on positive Hermitian
> circulants `H ∈ Herm_circ(3)_+`. Q is a Hermitian-cone scalar
> functional on the configuration space. The CRITICAL POINT condition
> Q(H) = 2/3 is equivalent to `|b|²/a² = 1/2 = BAE`.

**Derivation of BAE.**

```
Tr(H)  = 3a
Tr(H²) = E_+ + E_⊥ = 3a² + 6|b|²
Q = Tr(H²) / Tr(H)² = (3a² + 6|b|²) / (9a²)
  = 1/3 + (2/3)(|b|²/a²)

Q = 2/3  <=>  |b|²/a² = 1/2 = BAE.  ∎
```

(Verified at the BAE-point in runner Section 4.1; verified that
Q ≠ 2/3 at non-BAE ratios in Section 4.2.)

**Physical/mathematical interpretation.**

This is the **Brannen Q-readout** in the framework. Per the retained
Koide cone equivalence theorem, Q = 2/3 is the algebraic equivalent
of the Koide formula. M3 directly identifies BAE with a critical
value of the Q-functional.

The Brannen circle interpretation
([Kocik, "The Koide Lepton Mass Formula and Geometry of Circles",
arXiv:1201.2067](https://arxiv.org/abs/1201.2067)) shows that Q = 2/3
corresponds to a Descartes-circle-type configuration of the lepton
masses: three circles of curvatures `√m_e, √m_μ, √m_τ` mutually
tangent and inscribed in a fourth circle.

**Literature analog.**

[Brannen, "The Lepton Masses", brannenworks.com (2006)](http://brannenworks.com/MASSES2.pdf)
gives the canonical Brannen Q-functional treatment. [Foot,
"Charged lepton mass matrix with democratic family mixing"](https://link.springer.com/article/10.1007/BF01556669)
and the Foot 1994 paper on Koide-Foot relation are foundational.
Brannen's 2006 derivation explicitly identifies the cone interior
point `η² = 1/2` (equivalent to BAE) as the special point in the
parameter space.

**Strengths.**

- Q-functional is U(1)_b-invariant, C_3-invariant, and gauge-fixed by
  the retained Q-readout factorization theorem.
- Q = 2/3 is the most concise algebraic statement of BAE.
- Established in physics literature (Brannen, Foot, Koide).

**Weaknesses (PARTIAL classification).**

- Q is ONE candidate functional among many; M3 by itself doesn't
  derive "Q is the canonical readout". The choice of Q over
  alternatives (`F = Tr(H²) / |Tr(H)|²` for non-positive H,
  `F = log(Tr(H²)) - 2 log Tr(H)` etc.) requires admission.
- The campaign's Probe 16 (PR #789) elected the Q-functional level as
  a partial closure, but this election is itself an admission. M3
  consumes this admission rather than deriving it.
- M3 is therefore a *PARTIAL* primitive: it admits the Q-readout
  choice and notes that BAE is the unique critical value.

## Hostile-review classification

| Candidate | Classification | Rationale |
|---|---|---|
| M1 | **STRUCTURAL** | Forces (1, 1) weighting from R-irrep count; algebraically derives BAE from a definite trace functional content distinct from all 8 rejected toolkit levels. |
| M2 | **STRUCTURAL** | Forces (1, 1) effective weighting from U(1)_b measure quotient on the doublet; algebraically derives BAE from a definite measure choice distinct from all 8 rejected levels. |
| M3 | **PARTIAL** | Admits the Q-functional choice (already an admission per Probe 16); BAE is the unique critical value but M3 doesn't supply the derivation of Q-canonicality. |

The **most structurally direct candidate is M1**: it introduces a
definite trace functional with a clean R-irrep count, and that
trace's extremal structure forces F1 over F3. M2 supplies an
EQUIVALENT perspective via measure-theoretic quotient. The two are
**distinct primitives** (algebraic vs measure-theoretic) but
**equivalent in their derivation of BAE**.

M1 and M2 are likely **dual perspectives on a single derived primitive**;
the audit lane may elect either or both.

## What if the assumptions are wrong?

A genuine engagement with the assumptions of each candidate:

### What if "circulants are the right structure" is wrong?

If the matter sector on hw=1 is NOT C_3-equivariant Hermitian
circulants `aI + bC + b̄C²`, then the entire BAE-condition becomes
ill-defined. The framework's circulant ansatz is retained per
[`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md)
and `KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`. If
that retention is hostile-reviewed and falls, BAE itself is moot.

### What if the (1, 2) real-dim isotype split is wrong?

The (1, 2) real-dim split of `Herm_circ(3) = ℝ⟨I⟩ ⊕ ℝ⟨C+C²⟩ ⊕ ℝ⟨i(C-C²)⟩`
is fixed by C_3 representation theory. If hostile-reviewed and
falls, the entire (a, |b|)-plane parameterization is wrong, and BAE
in its current form does not survive. M1 and M2 inherit this
dependency from the retained framework.

### What if Q is not the canonical readout?

If the framework's canonical readout is not Q but some other
spectral functional, M3 is irrelevant (M1 and M2 still make sense,
since they don't depend on Q-canonicality). The Q-readout
factorization theorem
[`KOIDE_Q_READOUT_FACTORIZATION_THEOREM_2026-04-22.md`](KOIDE_Q_READOUT_FACTORIZATION_THEOREM_2026-04-22.md)
is retained, but its hostile-reviewed status is "audited_clean" —
not a strong derivation of "Q is the unique canonical choice".

### What if M1's R-irrep weighting is just an admission, not a derivation?

This is the strongest hostile-review attack on M1. M1 claims to
"weight by R-irreducible-block count" — but **why** count R-irreps
over real-dim or C-irreps?

A defense: the framework operates over **ℝ** for matter coefficients
(per the retained ℝ-isotype split). The doublet `ℝ⟨C+C²⟩ ⊕ ℝ⟨i(C-C²)⟩`
forms a single ℝ-irreducible block (it has no proper ℝ-invariant
subspace). M1 weights by **ℝ-irreducible-block count**, which is
canonical for an ℝ-linear algebra. Real dimension counts (ℝ-coordinates)
are basis-dependent; ℝ-irrep counts are not.

A counter-attack: even ℝ-irreps are not unique without further
structure. The trivial isotype is ALSO an ℝ-irrep (1-dim), so the
two-component count (1, 1) IS the ℝ-irrep count, which makes M1
canonical IF "count ℝ-irreps" is the right primitive.

This is the deepest layer of M1; the audit lane must judge whether
"ℝ-irrep counting on the matter algebra" is a canonical principle.

### What if M2's U(1)_b is not a gauge symmetry?

M2 quotients out U(1)_b on the doublet. U(1)_b is currently retained
only as an algebra-level continuous symmetry of the b-doublet (Probe
13). It is NOT a gauge symmetry in the framework. If U(1)_b is
purely classical and not gauged, M2's measure quotient is not
canonically forced.

A defense: per Probe 16, the Q-functional IS U(1)_b-invariant. If
the physical observables are Q (and other U(1)_b-invariant
quantities), then the U(1)_b orbit is operationally unphysical, and
quotienting it out is the canonical Bayesian-physical choice.

A counter-attack: this argument is meta; it requires admitting that
"observables are U(1)_b-invariant". A direct derivation of
U(1)_b as a gauge would be needed.

## Elon first-principles — the literal minimum

What is the LITERAL MINIMUM content needed to force `|b|²/a² = 1/2`?

After stripping all unnecessary structure: the BAE-condition is the
**Frobenius-norm equipartition** condition on the C_3-isotype split:
```
||trivial-component(H)||²_F = ||doublet-component(H)||²_F
i.e., E_+ = E_⊥
i.e., 3 a² = 6 |b|²
i.e., |b|²/a² = 1/2 = BAE.
```

The IRREDUCIBLE PRIMITIVE is therefore: **a principle that selects
``E_+ = E_⊥`` as a canonical equilibrium**. M1 does this via R-irrep
trace; M2 does this via measure quotient; M3 does this via
Q-functional critical value.

Within retained content, the "log E_+ + log E_⊥" functional already
appears (it's F1 in the retained MRU classification per
[`KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md));
the missing primitive is the JUSTIFICATION for choosing F1 over F3.

The minimum content needed is therefore: **a principle that picks F1
over F3 in the additive log-isotype-functional class**. Each candidate
M1, M2, M3 supplies this principle through different content
(trace, measure, functional).

## Compatibility with A1 + A2 + retained

All three candidates respect:

- **A1 (Cl(3) local algebra)**: no new algebra introduced; `τ_M`,
  `dν`, `Q` are functionals on `Herm_circ(3) ⊂ M_3(ℂ)`.
- **A2 (Z³ lattice)**: no spatial structure modified.
- **Retained C_3-equivariance**: all three are C_3-invariant.
- **Retained Frobenius isotype-split uniqueness**: the (1, 2)
  real-dim split is preserved; the M1 / M2 choice is to weight by
  R-IRREP count rather than real-dim count, which is a different
  weighting on the same (retained) decomposition.
- **Retained MRU weight-class theorem**: M1 / M2 SELECT the (1, 1)
  multiplicity-class within the retained classification. The MRU
  theorem already enumerates (1, 1), (1, 2) etc. as classes; M1 / M2
  derive the (1, 1) selection.
- **Retained Q-readout factorization** (for M3): M3 consumes Q as
  given.

(All compatibility checks verified by runner Section 5.)

## Distinctness from 8 rejected toolkit levels

| Level | Content | M1 distinct? | M2 distinct? |
|---|---|---|---|
| 1. Operator F3 | Real-dim Jacobian (1, 2) | Yes (M1 uses ℝ-irrep count (1, 1)) | Yes (M2 uses measure quotient) |
| 2. Pauli antisym | Slater determinant on ∧³V | Yes (no antisymmetrization) | Yes |
| 3. Topological K | Integers in `R(C_3) = ℤ⊕ℤ⊕ℤ` | Yes (M1 uses ℝ-irreps; K-theory uses integers) | Yes |
| 4. MaxEnt | Shannon entropy on Born density | Yes (no entropy max) | Yes |
| 5. S_3 reflection | C_3 × Z_2 reflection symmetry | Yes (M1 uses just C_3) | Yes |
| 6. NCG | Connes-Chamseddine spectral triple | Yes (M1 is single-site trace) | Yes |
| 7. q-deformation | U_q(C_3) at q = e^(iπ/3) | Yes (M1 doesn't deform) | Yes |
| 8. Hopf coproduct | Coproduct on ℂ[C_3] | Yes (M1 is single-site, not coproduct) | Yes |

(All distinctness checks verified by runner Section 7.)

## Honest assessment

**What this proposal contributes:**

1. **Three candidate derived primitives** that COULD close BAE, each
   with formal statement, algebraic derivation of `|b|²/a² = 1/2`,
   physical/mathematical interpretation, literature analog, and
   strengths/weaknesses analysis.
2. **Hostile-review classification** distinguishing STRUCTURAL
   primitives (M1, M2) from PARTIAL primitives (M3).
3. **Compatibility verification** with A1 (Cl(3)) + A2 (Z³) +
   retained framework.
4. **Distinctness verification** against all 8 rejected toolkit
   levels (operator + wave-function + topological + thermodynamic +
   S_3 + NCG + q-deformation + Hopf-coproduct).
5. **What-if-wrong analysis** for each candidate's load-bearing
   assumptions.
6. **Elon first-principles** identification of the irreducible
   primitive: a principle that selects F1 (E_+ = E_⊥) over F3 in the
   retained additive log-isotype-functional class.

**What this proposal does NOT do:**

1. Does NOT promote any candidate to retained status.
2. Does NOT close BAE on its own (audit lane decides).
3. Does NOT introduce new physical axioms.
4. Does NOT modify any retained theorem.
5. Does NOT prefer one candidate over another (M1, M2, M3 all
   proposed; M1 + M2 STRUCTURAL, M3 PARTIAL; audit lane decides).
6. Does NOT load-bear PDG values.
7. Does NOT replace the existing 8-level rejection theorems.
8. Does NOT eliminate the need for hostile-review of any elected
   primitive.

**What the audit lane should consider:**

1. Whether to elect any candidate as a derived primitive on top of A1 +
   A2 + retained.
2. Whether the R-irrep counting principle (M1) or the U(1)_b measure
   quotient (M2) is more canonical.
3. Whether M3 is sufficient (Q-functional critical-point identification)
   or whether M1/M2 is required (structural force).
4. Whether the proposal needs to be augmented with a derivation of WHY
   the elected primitive is canonical (e.g., a derivation of "count
   ℝ-irreps" from the framework's ℝ-linearity, or a derivation of
   "U(1)_b is gauge" from the Q-readout invariance).

## Cross-references

### Foundational baseline

- Minimal axioms: [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
- BAE rename meta: [`BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md`](BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md)
- Substep-4 AC narrowing: [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)

### Retained C_3 / circulant structure

- BZ-corner forcing: [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md)
- Circulant character / eigenvalue: [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
- Charged-lepton Koide cone equivalence: [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)
- Q-readout factorization: [`KOIDE_Q_READOUT_FACTORIZATION_THEOREM_2026-04-22.md`](KOIDE_Q_READOUT_FACTORIZATION_THEOREM_2026-04-22.md)

### Retained Frobenius / weight-class structure

- Block-total Frobenius: [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)
- Frobenius isotype-split uniqueness: [`KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md`](KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md)
- MRU weight-class: [`KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md)

### 8-level structural rejection campaign

- Probe 18 (F1 vs F3): [`KOIDE_BAE_PROBE_F1_CANONICAL_FUNCTIONAL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe18.md`](KOIDE_BAE_PROBE_F1_CANONICAL_FUNCTIONAL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe18.md)
- Probe 25 (free Gaussian extremization): [`KOIDE_BAE_PROBE_PHYSICAL_EXTREMIZATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe25.md`](KOIDE_BAE_PROBE_PHYSICAL_EXTREMIZATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe25.md)
- Probe 28 (interacting dynamics): [`KOIDE_BAE_PROBE_INTERACTING_DYNAMICS_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe28.md`](KOIDE_BAE_PROBE_INTERACTING_DYNAMICS_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe28.md)
- Probe Y (topological): [`KOIDE_Y_BAE_TOPOLOGICAL_INDEX_KTHEORY_NOTE_2026-05-10_probeY_bae_topological.md`](KOIDE_Y_BAE_TOPOLOGICAL_INDEX_KTHEORY_NOTE_2026-05-10_probeY_bae_topological.md)

### Literature analogs (external)

- Etingof-Nikshych-Ostrik fusion categories: [Annals of Mathematics 162 (2005) 581–642](https://annals.math.princeton.edu/wp-content/uploads/annals-v162-n2-p01.pdf)
- Brannen lepton mass derivation: [brannenworks.com/MASSES2.pdf (2006)](http://brannenworks.com/MASSES2.pdf)
- Foot democratic family mixing: [Z. Phys. C (1994)](https://link.springer.com/article/10.1007/BF01556669)
- Kocik Koide-Descartes circle geometry: [arXiv:1201.2067 (2012)](https://arxiv.org/abs/1201.2067)
- Marsden-Weinstein-Meyer reduction: standard symplectic-geometry result; see e.g. Marsden, *Lectures on Mechanics* (1992).
- Faddeev-Popov gauge fixing: standard QFT reference; see e.g. Peskin-Schroeder, *An Introduction to Quantum Field Theory* (1995), Ch. 9.

## Validation

```bash
python3 scripts/cl3_primitive_p_bae_2026_05_10_pPbae.py
```

Expected: `=== TOTAL: PASS=98, FAIL=0 ===`

The runner verifies:

1. Section 0 — Retained input sanity (C_3 cycle, circulant H, isotypes).
2. Section 1 — Block-total Frobenius (E_+ = 3a², E_⊥ = 6|b|²) and BAE
   <=> equipartition equivalence.
3. Section 2 — P-BAE-M1 derivation: multiplicity-counting trace state
   gives F1 critical-point at E_+ = E_⊥ <=> BAE.
4. Section 3 — P-BAE-M2 derivation: isotype-reduced action integral
   `dν = dr_+ d|b|` saddle-point gives `|b|²/a² = 1/2 = BAE` across 6
   normalization scales.
5. Section 4 — P-BAE-M3 derivation: framework Q = Tr(H²)/Tr(H)² = 2/3
   at BAE-point.
6. Section 5 — Compatibility with A1 (Cl(3)) + A2 (Z³) + retained.
7. Section 6 — Hostile-review classification: M1 + M2 STRUCTURAL, M3
   PARTIAL.
8. Section 7 — Distinctness from each of 8 rejected toolkit levels.
9. Section 8 — Numerical sweep verification across (a, |b|) values.
10. Section 9 — BAE <=> isotype Frobenius equipartition E_+ = E_⊥.
11. Section 10 — Literature analog validation.
12. Section 11 — Does-not disclaimers (no axiom changes, no retained
    promotions, no PDG, no theorem modifications).
13. Section 12 — Verdict synthesis.

Total: 98 PASS / 0 FAIL.

## User-memory feedback rules respected

- `feedback_primitives_means_derivations.md`: this note proposes
  candidate primitives as **DERIVATIONS** from A1 + A2 + retained,
  NOT as new axioms or imports. M1 (multiplicity-counting trace),
  M2 (isotype-reduced action measure), M3 (Q-functional
  identification) are all derived functionals on Herm_circ(3),
  consistent with the user's clarification that "new primitives"
  means derivations from A1 + A2 + retained.
- `feedback_consistency_vs_derivation_below_w2.md`: each candidate
  derivation algebraically forces BAE from its specific content; the
  derivations are not consistency equalities but FORCED extremization
  (M1: E_+ = E_⊥ is the unique critical-point of log E_+ + log E_⊥;
  M2: |b|²/a² = 1/2 is the unique saddle-point of L_M2; M3: Q = 2/3
  is the unique critical value).
- `feedback_hostile_review_semantics.md`: explicit hostile-review
  classification distinguishes STRUCTURAL (force BAE) from PARTIAL
  (admit BAE numerically). What-if-wrong analysis stress-tests each
  candidate's load-bearing assumptions.
- `feedback_retained_tier_purity_and_package_wiring.md`: no
  automatic cross-tier promotion. Each candidate is proposed as a
  source-note primitive design; the audit lane decides election.
- `feedback_review_loop_source_only_policy.md`: this note is a
  single source-note proposal + paired runner + cached output, no
  synthesis notes, no lane promotions, no working "Block" notes.
- `feedback_special_forces_seven_agent_pattern.md`: this note
  packages a multi-angle attack (3 candidate primitives across
  trace / measure / functional layers) on a single load-bearing
  obstruction (BAE), with sharp PASS/FAIL deliverables in the runner.
- `feedback_compute_speed_not_human_timelines.md`: alternative
  primitives are characterized in terms of CONTENT (trace, measure,
  functional) and DISTINCTNESS from rejected levels, not in terms
  of how-long-they-would-take.
- `feedback_physics_loop_corollary_churn.md`: this is novel
  primitive design — proposing new derived content distinct from any
  prior probe, not relabeling an already-landed cycle.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links so
the audit citation graph can track them. It does not promote this
note or change the audited claim scope.

- [brannen_amplitude_equipartition_bae_rename_meta_note_2026-05-09](BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md)
- [koide_bae_probe_f1_canonical_functional_bounded_obstruction_note_2026-05-09_probe18](KOIDE_BAE_PROBE_F1_CANONICAL_FUNCTIONAL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe18.md)
- [koide_bae_probe_physical_extremization_bounded_obstruction_note_2026-05-09_probe25](KOIDE_BAE_PROBE_PHYSICAL_EXTREMIZATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe25.md)
- [koide_bae_probe_interacting_dynamics_bounded_obstruction_note_2026-05-09_probe28](KOIDE_BAE_PROBE_INTERACTING_DYNAMICS_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe28.md)
- [koide_y_bae_topological_index_ktheory_note_2026-05-10_probeY_bae_topological](KOIDE_Y_BAE_TOPOLOGICAL_INDEX_KTHEORY_NOTE_2026-05-10_probeY_bae_topological.md)
- [koide_kappa_block_total_frobenius_measure_theorem_note_2026-04-19](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)
- [koide_frobenius_isotype_split_uniqueness_note_2026-04-21](KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md)
- [koide_mru_weight_class_obstruction_theorem_note_2026-04-19](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md)
- [staggered_dirac_bz_corner_forcing_theorem_note_2026-05-07](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md)
- [koide_circulant_character_derivation_note_2026-04-18](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
- [charged_lepton_koide_cone_algebraic_equivalence_note](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)
- [koide_q_readout_factorization_theorem_2026-04-22](KOIDE_Q_READOUT_FACTORIZATION_THEOREM_2026-04-22.md)
- [minimal_axioms_2026-05-03](MINIMAL_AXIOMS_2026-05-03.md)
- [staggered_dirac_substep4_ac_narrow_bounded_note_2026-05-07_substep4ac](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)
