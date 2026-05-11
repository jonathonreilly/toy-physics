# Koide A1 Route E — Kostant Weyl-Vector / A_1 Root System Bounded Obstruction

**Date:** 2026-05-08
**Type:** bounded_theorem (sharpened obstruction; no positive closure)
**Claim type:** bounded_theorem
**Scope:** review-loop source-note proposal — Route E closure attempt for
the A1 √2 equipartition admission on the charged-lepton Koide lane.
**Status:** source-note proposal for a negative Route E closure —
shows that the candidate structural identification
`|b|²/a² = |ρ_{A_1}|² = 1/2` cannot be derived from retained
Cl(3)/Z³ content. Five independent structural barriers each block
the proposed identification. The A1 admission count is UNCHANGED.
**Authority role:** source-note proposal — audit verdict and
downstream status set only by the independent audit lane.
**Loop:** koide-a1-route-e-kostant-weyl-20260508
**Primary runner:** [`scripts/cl3_koide_a1_route_e_kostant_weyl_2026_05_08_routee.py`](../scripts/cl3_koide_a1_route_e_kostant_weyl_2026_05_08_routee.py)
**Cache:** [`logs/runner-cache/cl3_koide_a1_route_e_kostant_weyl_2026_05_08_routee.txt`](../logs/runner-cache/cl3_koide_a1_route_e_kostant_weyl_2026_05_08_routee.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived status is generated
only after the independent audit lane reviews the claim, dependency
chain, and runner. The `claim_type`, scope, named admissions, and
bounded-obstruction classification are author-proposed; the audit lane
has full authority to retag, narrow, or reject the proposal.

## Question

`KOIDE_A1_DERIVATION_STATUS_NOTE.md`
identifies "Route E" (A_1 Weyl-vector / Kostant strange formula
coincidence) as one of the **strongest structural hints** for axiom-native
closure of the A1 √2 equipartition admission. The proposed structural
identification is:

> `|b|² / a²  =  |ρ_{A_1}|²  =  1/2`

where on the LHS `(a, b)` are the C_3-equivariant circulant amplitudes
on the retained `hw=1` generation sector
([`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)),
and on the RHS `|ρ_{A_1}|²` is the squared norm of the half-sum of
positive roots of the A_1 = sl(2) root system, given by Kostant's
strange formula

> `|ρ|²  =  h̄ · (h̄+1) · r / 12`

with `r = 1`, `h̄ = 2` for A_1, and standard Cartan-Killing
normalization `|α|² = 2`.

If proven, this structural identification would give axiom-native A1
from:

  - `Cl⁺(3) ≅ ℍ ⟹ Spin(3) = SU(2) = A_1` (retained
    [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md)),
    so the A_1 root system is present in retained content as the
    EW gauge sector;
  - Kostant strange formula gives `|ρ_{A_1}|² = 1/2` (textbook math);
  - The proposed structural map ⟹ `|b|²/a² = 1/2` ⟹ A1 forced.

The existing scout runners
[`scripts/frontier_koide_a1_weyl_vector_kostant_coincidence.py`](../scripts/frontier_koide_a1_weyl_vector_kostant_coincidence.py),
[`scripts/frontier_koide_a1_a2_weyl_double_match.py`](../scripts/frontier_koide_a1_a2_weyl_double_match.py),
and
[`scripts/frontier_koide_a1_lie_theoretic_triple_match.py`](../scripts/frontier_koide_a1_lie_theoretic_triple_match.py)
verify the **numerical match** (and the deeper "double match" in which
`c² = 2 = |ρ_{A_2}|²` and `Q = 2/3 = |ω_{A_2,fund}|²` extend the
coincidence to A_2 = sl(3)). They flag the structural identification
as the open lemma.

**Question:** Can the structural identification
`|b|²/a² = |ρ_{A_1}|²` be **derived** from retained Cl(3)/Z³ content
alone — no empirical loading, no new axioms, and crucially without
falling into the same convention-dependence trap that killed Route F
(per
[`KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md`](KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md))?

## Answer

**No.** The identification cannot close from retained content alone.
Five independent structural barriers each independently block the
proposed derivation. The barriers are structurally analogous to those
that closed Route F negatively, with one additional barrier (B5)
specific to Route E's "double-match" extension:

1. **Cartan-Killing normalization dependence (B1).** `|ρ_{A_1}|² = 1/2`
   only with the textbook normalization `|α|² = 2`. Under the equivalent
   convention `|α|² = 1` (unit-length roots), `|ρ_{A_1}|² = 1/4`; under
   `|α|² = 4`, `|ρ_{A_1}|² = 1`. The retained framework does not select
   one Cartan-Killing normalization over another. This is the **direct
   analog of Route F's Y_L = -1 vs +1/2 trap**: a quantity that takes
   different numerical values under different equivalent conventions
   cannot be a structural identity in its proposed form.

2. **A_1 representation-dimension mismatch with hw=1 (B2).** The A_1
   fundamental representation is 2-dim (spinor); the framework's
   generation sector hw=1 is 3-dim. The 3-dim irrep of A_1 (the adjoint /
   spin-1) has integer weights `{-2, 0, +2}` which do NOT match the
   C_3 character decomposition of hw=1 (`trivial ⊕ ω ⊕ ω̄`). There is
   no canonical isomorphism between an A_1 irrep and the retained hw=1
   generation sector.

3. **Cross-sector orthogonality (B3).** The retained `A_1 ⊂ Cl⁺(3)` is a
   GAUGE-sector statement (SU(2)_L acts on the doublet). The
   circulant coefficients `(a, b)` live entirely in the FLAVOR /
   generation sector (hw=1 with C_3[111] cycle). These are orthogonal
   sectors in the framework; no retained theorem provides a structural
   bridge transferring Lie-algebraic length-squared values from one to
   the other. This barrier is identical to Route F's B3.

4. **Category mismatch (B4).** LHS `|b|²/a²` is an operator-coefficient
   ratio in a Hermitian decomposition. RHS `|ρ_{A_1}|²` is a
   Cartan-Killing length-squared, an invariant of the Lie-algebraic data
   alone. The Weyl vector ρ appears in the Weyl character formula and
   in Freudenthal/Kostant formulas as a **highest-weight shift** for
   representation characters, NOT as an "amplitude ratio". Equating LHS
   and RHS requires a structural normalization principle (a rule
   prescribing how operator coefficients inherit Lie-algebraic
   lengths) which retained content does not supply.

5. **Hidden A_2 = sl(3) family is NOT retained (B5).** The "double-match"
   extension to A_2 (Lie-theoretic triple match per
   [`scripts/frontier_koide_a1_lie_theoretic_triple_match.py`](../scripts/frontier_koide_a1_lie_theoretic_triple_match.py))
   relies on the framework carrying both A_1 = sl(2) AND A_2 = sl(3)
   structure on the generation sector. The retained framework has A_1
   via `Cl⁺(3) ≅ ℍ`, but only `Z_3 ⊂ SU(3)` (the center as a discrete
   subgroup). `Z_3` does NOT generate the rank-2 root system of A_2;
   sl(3) is 8-dim, of which **zero generators** are retained on hw=1.
   The "double match" therefore is not a structural framework prediction
   but a numerical observation about `Z_3 ⊂ SU(3)` plus an
   uninstantiated hidden-SU(3)_family hypothesis.

The combined picture: **Route E is structurally barred**. Each of the
three numerically-matched quantities (Kostant `|ρ_{A_1}|²`, framework
`|b|²/a²`, and SM Casimir-difference) is defined in an independent
sector / convention, and the equality among them is a numerical
coincidence among independently-defined values, not a derivation. Closing
A1 via this route would require either (a) a new retained primitive
selecting the Cartan-Killing normalization, AND a structural map
between gauge-sector Lie data and flavor-sector operator coefficients,
AND a hidden A_2 = sl(3) on hw=1; (b) explicit user-approved A3-class
admission(s) for these gaps; or (c) an alternative Lie-algebraic lemma
not based on the Weyl-vector / Casimir-related numerology.

## Setup

### Premises (A_min for Route E closure attempt)

| ID | Statement | Class |
|---|---|---|
| A1 | Cl(3) local algebra | framework axiom; see `MINIMAL_AXIOMS_2026-05-03.md` |
| A2 | Z³ spatial substrate | framework axiom; same source |
| Embed | Cl⁺(3) ≅ ℍ → SU(2)_L; ω pseudoscalar → U(1)_Y; Y_L, Y_H fixed | retained: [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md) |
| GS | One-Higgs gauge selection: Y_e is arbitrary 3×3 complex matrix | retained: [`SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md`](SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md) |
| WardFree | No direct Ward lift forces y_τ; Y_e remains free 3×3 | retained: [`CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md`](CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md) |
| Circulant | C_3-equivariant Hermitian on hw=1 is `aI + bU + b̄U^{-1}` | retained: [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md) R1 |
| C3Pres | C_3[111] is preserved (not broken) on hw=1 in retained content | retained: [`C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md`](C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md) |
| 3GenObs | hw=1 BZ-corner triplet has M_3(C) algebra; C_3[111] cycles corners | retained-bounded: [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md) |
| Substep4 | AC_φλ remains the explicit identification residual on hw=1 | retained-bounded: [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md) |
| KoideAlg | Koide Q = 2/3 ⟺ a₀² = 2|z|² ⟺ |b|²/a² = 1/2 (algebraic) | retained: [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md) |
| RouteE_RHS | `|ρ_{A_1}|² = 1/2` numerically holds in `|α|²=2` Kostant convention | textbook Lie theory; existing scouts [`scripts/frontier_koide_a1_weyl_vector_kostant_coincidence.py`](../scripts/frontier_koide_a1_weyl_vector_kostant_coincidence.py), [`scripts/frontier_koide_a1_a2_weyl_double_match.py`](../scripts/frontier_koide_a1_a2_weyl_double_match.py), [`scripts/frontier_koide_a1_lie_theoretic_triple_match.py`](../scripts/frontier_koide_a1_lie_theoretic_triple_match.py) |

### Forbidden imports

- NO PDG observed mass values used as derivation input (anchor-only at
  end, clearly marked per
  [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)).
- NO lattice MC empirical measurements
- NO fitted matching coefficients
- NO same-surface family arguments
- **NO new axioms** (Route E's promise was axiom-native; any A3-class
  admission requires explicit user approval and is not proposed here)
- NO admitted SM Yukawa-coupling pattern as derivation input
- NO hidden SU(3)_family structure (this is exactly what B5 forbids
  importing tacitly)

## The structural identification at issue

**Proposed identification (Route E):**

```
|b|² / a²  =  |ρ_{A_1}|²       on circulant Hermitian on hw=1 ≅ ℂ³
```

where:

- `(a, b)` are the coefficients of the circulant decomposition
  `H = aI + bU + b̄U^{-1}` (a real, b complex), forced on hw=1 by
  C_3-equivariance.
- `|ρ_{A_1}|²` is the squared norm of the half-sum of positive roots
  of A_1 = sl(2), under standard Cartan-Killing normalization
  `|α|² = 2`.
- Kostant's strange formula gives `|ρ_{A_1}|² = h̄(h̄+1)r/12 = 2·3·1/12 = 1/2`.
- The A1 target value is `|b|²/a² = 1/2`, matching numerically.

The "double match" extension further posits

```
c²  =  |ρ_{A_2}|²  =  2,    Q  =  |ω_{A_2,fund}|²  =  2/3
```

via Brannen `c = 2|b|/a` and Koide `Q = 1/3 + c²/6`. This requires the
framework to carry not just A_1 (= retained SU(2)_L) but also A_2 (= a
hidden SU(3)_family on hw=1).

**The runners** verify the **numerical values** of the RHS quantities
(Kostant for A_1 and A_2) and the matches with the LHS (Brannen forms)
but do NOT prove the structural identification. This note investigates
whether that derivation is possible from retained content.

## Theorem (Route E bounded obstruction)

**Theorem.** On A1+A2 + retained CL3_SM_EMBEDDING + retained
gauge-selection + retained C_3-equivariance + retained
KoideCone-algebraic-equivalence + retained C_3-preservation + admissible
standard math machinery (Lie theory, root systems, Kostant strange
formula):

```
The structural identification

  |b|² / a²  =  |ρ_{A_1}|²  =  1/2

cannot be derived from retained Cl(3)/Z³ content alone. Five
independent structural barriers each block the identification:

  (B1) Cartan-Killing normalization dependence: |ρ_{A_1}|² takes 3
       distinct values {1/4, 1/2, 1} under three equivalent root-length
       conventions {|α|²=1, 2, 4}; framework does not select one.
  (B2) Representation dimension mismatch: A_1 fundamental is 2-dim;
       hw=1 generation sector is 3-dim; no canonical A_1 irrep
       isomorphism with hw=1 exists.  The 3-dim adjoint of A_1 has
       weights {-2, 0, +2} ≠ C_3 characters {1, ω, ω̄}.
  (B3) Sector orthogonality: A_1 ⊂ Cl⁺(3) is the GAUGE sector;
       (a, b) live in the orthogonal FLAVOR (generation) sector.
       No retained cross-sector bridge exists.  (B3 is structurally
       identical to Route F's B3.)
  (B4) Category mismatch: |ρ|² is a Cartan-Killing length;
       |b|²/a² is an operator-coefficient ratio.  Equating them
       requires a structural normalization map not supplied by
       retained content.  ρ appears in the Weyl character formula
       as a highest-weight shift, not as an amplitude.
  (B5) Hidden A_2 = sl(3) is not retained.  The 'double match'
       extension to (|ρ_{A_2}|² = 2, |ω_{A_2,fund}|² = 2/3) requires
       the framework to carry an SU(3)_family Lie algebra on hw=1.
       Z_3 ⊂ SU(3) center is retained (as C_3[111]), but sl(3) has
       8 generators of which exactly 0 are retained on hw=1.

Therefore Route E closure of A1 is structurally barred under the
stated retained-content surface. The A1 admission count is unchanged.
```

**Proof.** Each barrier is verified independently in the paired runner;
combining them establishes that no derivation chain from retained
content reaches `|b|²/a² = |ρ_{A_1}|²`.

### Barrier 1: Cartan-Killing normalization dependence

The Kostant strange formula `|ρ|² = h̄(h̄+1)r/12` gives `1/2` for A_1
**only with the textbook normalization** `|α|² = 2` (long-root squared
length 2). Under different equivalent normalizations, the value differs:

| Normalization | `|α|²` | `|ρ_{A_1}|²` |
|---|---|---|
| Unit-length roots | 1 | 1/4 |
| Standard textbook | 2 | 1/2 |
| Double-length | 4 | 1 |

The framework's retained content does not derive a preferred
Cartan-Killing normalization on the A_1 ⊂ Cl⁺(3) Lie algebra. The
retained
[`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md)
embeds A_1 = su(2) in Cl⁺(3) via the bivector basis
`{e_{12}, e_{13}, e_{23}}` with each squaring to `−I_8`. The induced
Killing-form normalization is determined by the embedding, but **its
relation to the convention used by Kostant's strange formula is itself
a convention choice** — there is no retained theorem fixing
`|α|² = 2` rather than `|α|² = 1` for the framework's A_1.

The runner verifies `|ρ_{A_1}|² ∈ {1/4, 1/2, 1}` under three
equivalent conventions while the same physical Lie algebra A_1 = sl(2)
underlies all three. A genuine structural identity must be
normalization-invariant; this identification is not.

This barrier is the **direct analog of Route F's B1** (where
`T(T+1) − Y² = 1/2` held only in PDG convention `Y_L = -1/2`, while
the framework's retained
[`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md)
uses `Y_L = -1`, giving `−1/4`). In both cases the proposed
"structural identity" turns out to depend on a choice of normalization
not fixed by retained content.

### Barrier 2: Representation dimension mismatch with hw=1

The A_1 = sl(2) Lie algebra has a unique fundamental representation of
dimension 2 (the spinor representation, spin-1/2). It also has irreps
of dimension 3 (the adjoint = vector representation = spin-1), 4
(spin-3/2), 5 (spin-2), etc.

The framework's generation sector hw=1 is 3-dim, carrying the C_3[111]
cyclic permutation. The C_3 character decomposition is
`hw=1 ≅ trivial ⊕ ω ⊕ ω̄` where `ω = e^{2πi/3}`.

**The 3-dim irrep of A_1 (adjoint) has weights `{-2, 0, +2}`** in
α-units, NOT the C_3 characters `{1, ω, ω̄}`. The two 3-dim
representations are fundamentally different:

| Sector | Weights / characters | Group action |
|---|---|---|
| A_1 adjoint (spin-1) | `{-2, 0, +2}` (real integer weights) | SU(2) ≅ SO(3) |
| hw=1 (C_3 triplet) | `{1, ω, ω̄}` (complex C_3 characters) | C_3 ⊂ S_3 ⊂ U(3) |

There is no canonical Lie-algebra-isomorphism mapping an A_1 irrep onto
the hw=1 generation sector. The Weyl-vector ρ ∈ A_1 root space lives
in a different Cartan subalgebra than the C_3 character data on hw=1.

The runner verifies the dimension mismatch and prints the explicit
non-correspondence of weights versus C_3 characters.

### Barrier 3: Cross-sector orthogonality (gauge vs flavor)

The retained `A_1 ⊂ Cl⁺(3)` is a **gauge-sector statement**: SU(2)_L
acts on the 2-dim doublet (e.g., `(ν_L, e_L)`) carrying weak isospin.
The Cartan-Killing data of A_1 (root system, Weyl vector, fundamental
weights) belongs to this gauge sector.

The Brannen-Rivero amplitudes `(a, b)` live in the **flavor sector**:
the C_3-equivariant Hermitian operator `H = aI + bU + b̄U^{-1}` acts
on the hw=1 generation triple, encoding generation-space dynamics.

These are **orthogonal mathematical sectors** in the framework:

- SU(2)_L acts trivially on generation indices (gauge symmetry
  commutes with flavor; this is a textbook SM property and is
  consistent with retained content).
- The C_3 cycle acts trivially on doublet indices.
- Tensor product structure: full state space = doublet (2-dim) ⊗
  generation (3-dim), with gauge-symmetric operators acting as
  scalars on the flavor sector and C_3-equivariant operators acting as
  scalars on the doublet sector.

The Weyl-vector `ρ ∈ A_1` lives entirely in the gauge-sector Cartan
subalgebra. The circulant coefficients `(a, b)` live entirely in the
flavor-sector Hermitian decomposition. **There is no retained theorem
mapping gauge-sector Cartan-Killing length-squareds to flavor-sector
operator-coefficient ratios.**

The runner verifies that A_1 generators acting on the doublet commute
with circulant operators on the generation sector (max commutator
< 10⁻¹²).

This barrier is **structurally identical to Route F's B3** — both
proposed routes attempt to transfer a gauge-sector quantity to a
flavor-sector quantity without a retained cross-sector bridge.

### Barrier 4: Category mismatch (length-squared vs amplitude ratio)

The two sides of the proposed identification are mathematical objects
of different categories:

- **LHS** `|b|²/a²`: a ratio of operator coefficients in the Hermitian
  decomposition `H = aI + bU + b̄U^{-1}`. Under uniform rescaling
  `(a, b) → (λa, λb)` it is invariant; under independent rescaling
  `(a, b) → (λa, μb)` it scales as `(μ/λ)²`. The value depends on the
  *operator content* of `H` (e.g., on its eigenvalue structure).

- **RHS** `|ρ_{A_1}|²`: a Cartan-Killing length-squared. It is an
  invariant of the Lie-algebraic data alone — independent of any
  operator structure. Its appearances in standard Lie theory:

  - **Weyl character formula:**
    `χ_λ(g) = (Σ_w ε(w) e^{w(λ+ρ)}) / (Σ_w ε(w) e^{w(ρ)})` — ρ is
    a highest-weight shift, NOT an amplitude.
  - **Kostant multiplicity formula:** ρ appears in the index of an
    alternating sum over the Weyl group.
  - **Freudenthal's strange formula:** `|ρ|² = (h̄/24) · dim(g)` —
    relates ρ-norm to dimensions, but again does not give an
    "amplitude ratio".
  - **Affine Lie algebra central charge:** `c = (k · dim(g))/(k+h̄)`
    where ρ enters the Sugawara construction — no "amplitude" reading.

  In NONE of these standard roles is `|ρ|²` an "amplitude ratio".

Equating LHS and RHS requires a **structural normalization principle**:
a rule prescribing how operator coefficients in a Hermitian
decomposition inherit values from Lie-algebraic Cartan-Killing
lengths. The Route E proposal does not supply such a principle.

For comparison, the retained `C_τ = T(T+1) + Y² = 1` theorem
([`KOIDE_EXPLICIT_CALCULATIONS_NOTE.md`](KOIDE_EXPLICIT_CALCULATIONS_NOTE.md)
Section "Deliverable 2") DOES have a normalization principle: the
Casimir SUM is the coefficient of a specific 1-loop self-energy
diagram. For `|ρ|²` no analogous diagrammatic principle exists in the
retained content.

The runner verifies the rescaling-invariance asymmetry and constructs
two distinct circulants with the same `|b|²/a² = 1/2` but different
operator content (different eigenvalues), confirming that the
operator-coefficient ratio is not a Lie-algebraic invariant.

### Barrier 5: Hidden A_2 = sl(3) is NOT retained content

The "double-match" extension to A_2 (per
[`scripts/frontier_koide_a1_a2_weyl_double_match.py`](../scripts/frontier_koide_a1_a2_weyl_double_match.py)
and
[`scripts/frontier_koide_a1_lie_theoretic_triple_match.py`](../scripts/frontier_koide_a1_lie_theoretic_triple_match.py))
enriches the structural picture with two additional matches:

```
c²    =  4 |b|²/a²   =  2     =  |ρ_{A_2}|²       (Kostant for A_2)
Q     =  1/3 + c²/6  =  2/3   =  |ω_{A_2,fund}|²   (A_2 fund weight)
```

both via A_2 = sl(3) Lie-theoretic data.

**This requires the framework to carry a sl(3) Lie algebra structure on
the generation sector hw=1.** The retained framework provides:

- C_3[111] cyclic permutation: yes (per
  [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)).
- Z_3 = generator of C_3: yes.
- sl(3) = A_2 Lie algebra (8-dim): **NO**.

The relationship: `Z_3 = ZC(SU(3))` (the center of SU(3)), since
sl(3) has center generated by `exp(2πiY/3)` for the appropriate U(1)
inside SU(3). But "having Z_3" is enormously weaker than "having
sl(3)":

- Z_3 is a discrete 3-element group;
- sl(3) is a continuous 8-dim Lie algebra (Gell-Mann generators);
- Z_3 alone does NOT generate the rank-2 root system of A_2 nor any
  A_2 representation theory.

The retained framework retains **zero** of the 8 generators of sl(3) on
hw=1 from A1+A2 alone. The C_3[111] cycle is a finite cyclic
permutation (a subgroup of S_3, of order 3), which gives a single
discrete generator — and even that, in the form of an infinitesimal
generator, is a u(1) (1-dim), not su(3) (8-dim).

The runner verifies that the framework retains 0 of 8 sl(3) generators
on hw=1.

This barrier is **specific to Route E**: Route F invoked only A_1 (via
SU(2)_L) and U(1)_Y, both retained. Route E's "double match" extension
additionally invokes A_2, which is not retained.

The "double match" `(|ρ_{A_1}|² = 1/2, |ρ_{A_2}|² = 2)` therefore is
not a structural framework prediction. It is a numerical observation
about Z_3 ⊂ SU(3) inclusion plus an uninstantiated SU(3)_family
hypothesis.

## Why the three-way numerical match is a coincidence

Within the SM, the values `T(T+1) − Y²` (for L doublet) and
`|ρ_{A_1}|²` (for SU(2)_L Cartan data) all evaluate to `1/2` in their
standard textbook conventions. The match arises because:

- `|ρ_{A_1}|² = 1/2` is fixed by Kostant + textbook normalization
  `|α|² = 2`. (Lie theory)
- `T(T+1) − Y² = 1/2` is fixed by SM gauge structure of the lepton
  doublet in PDG hypercharge convention. (SM phenomenology / textbook)
- `|b|²/a² = 1/2` is required to algebraically force Koide Q = 2/3,
  which is observed empirically. (PDG charged-lepton masses)

All three values are encoded by independent textbook / phenomenological
data, none of which is derived from Cl(3)/Z³ axioms. They match
because they all encode information about charged-lepton SM structure
— but that information was input, not derived. The numerical match is
therefore evidence of consistency with SM phenomenology, not evidence
of an axiom-native derivation.

This is a Type-I admission per
`feedback_consistency_vs_derivation_below_w2.md`: "consistency
equality is not derivation."

## Counterfactuals

The runner constructs explicit counterfactuals demonstrating the
non-uniqueness of the value `1/2` as an output of Lie theory:

1. **D_2 ≅ A_1 × A_1**: each A_1 factor's Weyl vector has
   `|ρ|² = 1/2` with `|α|² = 2`. So D_2 ALSO carries `|ρ|² = 1/2`,
   showing 1/2 is not unique to A_1.

2. **A_2 with non-standard normalization `|α|² = 1/2`**:
   `|ρ_{A_2}|² = 1/2` (rescaled). With freedom in Cartan-Killing
   normalization, ANY Lie algebra can be made to give `|ρ|² = 1/2`.

If `1/2 = |ρ_{A_1}|²` were a structural Cl(3)/Z³ output, it would be
uniquely picked out by Lie-algebraic data plus retained content.
Instead, the value `1/2` is achieved by an INFINITE family of (Lie
algebra, normalization) pairs. The "uniqueness of A_1 in retained
framework" depends on the embedding `Cl⁺(3) ≅ ℍ ⟹ Spin(3) = SU(2)`,
not on the value 1/2.

## Comparison to Route F (and prior routes)

| Prior closure attempt | Status | Comment |
|---|---|---|
| Route A (Koide-Nishiura U(3) quartic) | open; outside Theorem 6 | trace-based 4th-order; needs derivation |
| Route B (Clifford torus on S³) | does not match Koide cone | 45° latitude vs equator |
| Route C (AS Lefschetz cot²) | parallel numeric identity | 2/3 = 2/3 coincidence |
| Route D (Newton-Girard) | open; trace-poly form | `6 = n(n+1)/2` coefficient unforced |
| Route E (A_1 Weyl-vector / Kostant) | **THIS NOTE: bounded obstruction** | **five-barrier negative closure** |
| Route F (Yukawa Casimir-difference) | bounded obstruction | per [`KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md`](KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md) (four-barrier) |
| Numerical match runner (Apr 2026, Weyl-vector coincidence) | establishes RHS arithmetic | does NOT establish structural identification |

### Side-by-side: Route F vs Route E barriers

| Barrier | Route F | Route E |
|---|---|---|
| B1 (convention) | Y_L = -1 vs +1/2 → 1/2 vs -1/4 | `|α|² = 2` vs 1 vs 4 → 1/2 vs 1/4 vs 1 |
| B2 (free coefficients) | Y_e arbitrary; (a, b) free | A_1 fund 2-dim ≠ hw=1 dim 3 |
| B3 (sector orthogonality) | gauge vs flavor | gauge vs flavor (identical) |
| B4 (category mismatch) | op-coeff vs gauge-Casimir scalar | op-coeff vs Cartan-Killing length |
| B5 (additional, Route E only) | (no analog) | A_2 = sl(3) is not retained |

Both routes fail at the same place structurally: the proposed
"identity" turns out to be two convention-dependent quantities defined
in independent sectors of the framework, equated only by an
arithmetic coincidence. Route E inherits Route F's gauge-vs-flavor and
category-mismatch barriers, replaces Route F's hypercharge-convention
barrier with a Cartan-Killing-normalization barrier, replaces Route
F's free-Yukawa barrier with a representation-dimension-mismatch
barrier, and adds a NEW barrier (B5) for the "double match" extension's
unretained A_2 = sl(3) requirement.

This note **complements** the existing Route E numerical-match runners
by establishing that the structural identification cannot be derived
even though the numerical match holds.

## What this closes

- **Route E negative closure** (bounded obstruction). Five
  independent structural barriers verified.
- **Sharpens the "strongest structural hint" status**: prior status was
  "open candidate lemma — would close A1 if proved." This note
  demonstrates the lemma cannot close from retained content. Future
  re-attempts must supply at least one of: (a) a retained
  Cartan-Killing normalization principle, (b) a retained gauge-to-flavor
  bridge mapping Lie-algebraic lengths to operator-coefficient ratios,
  (c) a retained A_2 = sl(3) on hw=1, OR (d) a fundamentally different
  Lie-algebraic identification not based on the Weyl-vector numerology.
- **Sister-route implications**: Route E should not be cited as an
  axiom-native closure path going forward; companion Route A and Route D
  notes independently close their own candidate mechanisms negatively.
- **Audit-defensibility**: explicit normalization-dependent values for
  `|ρ_{A_1}|²`, demonstrating that the "1/2 match" is not a
  structural prediction of A_1 Lie theory but a consequence of choosing
  one Cartan-Killing normalization among many.

## What this does NOT close

- A1 admission count is unchanged. A1 remains a load-bearing non-axiom
  step on the Brannen circulant lane.
- Routes A (Koide-Nishiura quartic) and D (Newton-Girard) are not
  closed by this note; they are handled by their own companion
  bounded-obstruction notes.
- Charged-lepton Koide closure remains a bounded observational-pin
  package (status from
  [`CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md`](CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md)
  unchanged).
- The numerical-match runners
  [`scripts/frontier_koide_a1_weyl_vector_kostant_coincidence.py`](../scripts/frontier_koide_a1_weyl_vector_kostant_coincidence.py),
  [`scripts/frontier_koide_a1_a2_weyl_double_match.py`](../scripts/frontier_koide_a1_a2_weyl_double_match.py),
  [`scripts/frontier_koide_a1_lie_theoretic_triple_match.py`](../scripts/frontier_koide_a1_lie_theoretic_triple_match.py)
  retain their PASS counts for the *numerical* checks. This note does
  NOT retract those — it adds a structural-derivation analysis that the
  numerical checks by themselves do not provide.
- AC_φλ residual (substep 4) is unaffected.
- L3a trace-surface bounded obstruction status unchanged.

## Empirical falsifiability

| Claim | Falsifier |
|---|---|
| Cartan-Killing convention dependence (B1) | Demonstrate a Cartan-Killing-invariant reformulation that gives 1/2 for A_1 in all standard normalization conventions — refutes B1. |
| Representation-dimension mismatch (B2) | Construct a canonical A_1 irrep isomorphism with the retained hw=1 generation sector — refutes B2. |
| Sector orthogonality (B3) | Construct a retained operator that maps A_1 Cartan-Killing data to hw=1 circulant coefficient ratio — refutes B3. |
| Category mismatch (B4) | Supply a retained normalization principle that fixes operator-coefficient inheritance from Lie-algebraic length-squareds — refutes B4. |
| Hidden A_2 = sl(3) (B5) | Derive an sl(3) Lie algebra acting on hw=1 from A1+A2 alone — refutes B5. (This would be a major framework extension and is currently absent.) |
| Numerical match (anchor) | Falsified if charged-lepton Koide Q deviates significantly from 2/3 in updated PDG; the representative anchor values used by the paired runner give Q = 0.666661 (sub-0.001% match). |

## Review boundary

This note proposes `claim_type: bounded_theorem` for the independent
audit lane. The bounded theorem is the negative Route E boundary: the
Kostant Weyl-vector / A_1 root system structural identification is
blocked by Cartan-Killing normalization dependence, representation-
dimension mismatch, sector orthogonality, category mismatch, and
unretained A_2 = sl(3) hidden structure unless new retained content
or explicit user-approved A3-class admissions supply the missing maps.

No new admissions are proposed. A1 remains unchanged at its prior
load-bearing non-axiom status on the Brannen circulant lane. The
independent audit lane may retag, narrow, or reject this proposal.

## Promotion-Value Gate (V1-V5)

| # | Question | Answer |
|---|---|---|
| V1 | Verdict-identified obstruction closed? | The "Route E is the strongest structural hint" claim is sharpened from "open candidate lemma" to "structurally barred under retained content; needs explicit Cartan-Killing convention selector AND gauge-to-flavor bridge AND retained A_2 = sl(3)." |
| V2 | New derivation? | The five-barrier obstruction argument applied to Route E is new structural content. Prior status notes enumerated the candidate but did not prove the obstruction. |
| V3 | Audit lane could complete? | Yes — the audit lane can review (i) Cartan-Killing convention dependence, (ii) representation-dimension mismatch with hw=1, (iii) sector orthogonality (already audited for Route F), (iv) category mismatch, (v) hidden A_2 absence, and (vi) the five-barrier conjunction. |
| V4 | Marginal content non-trivial? | Yes — the Cartan-Killing-convention finding (1/4 vs 1/2 vs 1 under three conventions) and the A_1-rep-dim-mismatch finding (2 ≠ 3) and the A_2-hidden-Lie-algebra finding (0 of 8 generators retained) are non-obvious from prior Route E scout runners and directly challenge Route E. |
| V5 | One-step variant? | No — the five-barrier argument is structural across multiple sectors (gauge, flavor, convention, normalization, hidden Lie-algebra), not a relabel of any prior Koide route. The novel B5 (hidden A_2) is unique to Route E's "double match" extension. |

**Source-note V1-V5 screen: pass for bounded-obstruction audit
seeding.**

## Why this is not "corollary churn"

Per `feedback_physics_loop_corollary_churn.md`, the user-memory rule
is to avoid one-step relabelings of already-landed cycles. This note:

- Is NOT a relabel of Route F. The five-barrier obstruction argument
  applied to Route E shares B3 and B4 with Route F (sector orthogonality
  and category mismatch — these are general, structural barriers
  applicable to any cross-sector identification), but B1, B2, B5 are
  Route-E-specific and address the Lie-algebraic content (Cartan-Killing
  normalization, representation dimensions, hidden A_2) NOT addressed
  by Route F's gauge-Casimir analysis.
- Identifies a NEW STRUCTURAL OBSTRUCTION (Barrier 5 = hidden A_2 =
  sl(3) absent) not present in the prior `KOIDE_A1_DERIVATION_STATUS_NOTE`
  treatment of Route E (which described the "double match" as a
  strong hint without flagging that A_2 is unretained).
- Sharpens the "strongest structural hint" claim from "open" to
  "closed-negatively", with a clear list of what would be required to
  reopen it.
- Provides explicit normalization-dependent counterexamples that
  demonstrate the convention-dependence status of `|ρ_{A_1}|²` —
  these were not present in prior Route E discussions.

## Cross-references

- A1 derivation status (parent): `KOIDE_A1_DERIVATION_STATUS_NOTE.md`
- Route F obstruction note (sister): [`KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md`](KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md)
- Existing Route E numerical runners:
  [`scripts/frontier_koide_a1_weyl_vector_kostant_coincidence.py`](../scripts/frontier_koide_a1_weyl_vector_kostant_coincidence.py),
  [`scripts/frontier_koide_a1_a2_weyl_double_match.py`](../scripts/frontier_koide_a1_a2_weyl_double_match.py),
  [`scripts/frontier_koide_a1_lie_theoretic_triple_match.py`](../scripts/frontier_koide_a1_lie_theoretic_triple_match.py)
- Circulant character derivation: [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
- Charged-lepton Koide-cone algebraic equivalence: [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)
- CL3 SM embedding: [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md)
- Koide explicit calculations (C_τ = 1): [`KOIDE_EXPLICIT_CALCULATIONS_NOTE.md`](KOIDE_EXPLICIT_CALCULATIONS_NOTE.md)
- One-Higgs gauge selection: [`SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md`](SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md)
- Direct Ward-free Yukawa no-go: [`CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md`](CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md)
- Substep 4 AC narrowing: [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)
- Three-generation observable: [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- C_3 symmetry preserved baseline: [`C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md`](C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md)
- Physical lattice baseline: [`PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md`](PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md)
- Higher-order structural theorems: [`HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md`](HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md)
- MINIMAL_AXIOMS: `MINIMAL_AXIOMS_2026-05-03.md`

## Validation

```bash
python3 scripts/cl3_koide_a1_route_e_kostant_weyl_2026_05_08_routee.py
```

Expected output: structural verification of (i) numerical Lie-algebraic
match (Kostant for A_1, A_2; A1-condition target reproduces),
(ii) Barrier 1 Cartan-Killing normalization dependence (1/4, 1/2, 1
under three conventions), (iii) Barrier 2 representation-dimension
mismatch (2 vs 3), (iv) Barrier 3 sector orthogonality
(commutator < 10⁻¹²), (v) Barrier 4 category mismatch (rescaling-
asymmetry; Weyl character formula context), (vi) Barrier 5 hidden A_2
absence (0 of 8 sl(3) generators retained), (vii) counterexample
sweep (D_2 also gives 1/2; A_2 with rescaled `|α|²` also gives 1/2),
(viii) falsifiability anchor (PDG values, anchor-only),
(ix) bounded-obstruction theorem statement, (x) comparison table with
Route F. Total: 21 PASS / 0 FAIL.

Cached: [`logs/runner-cache/cl3_koide_a1_route_e_kostant_weyl_2026_05_08_routee.txt`](../logs/runner-cache/cl3_koide_a1_route_e_kostant_weyl_2026_05_08_routee.txt)

## User-memory feedback rules respected

- `feedback_consistency_vs_derivation_below_w2.md`: this note
  specifically applies the "consistency equality is not derivation"
  rule. The numerical match `|ρ_{A_1}|² = 1/2 = |b|²/a²` is a
  consistency equality among independently-defined quantities, not a
  structural Lie-algebraic identity, and the proposed identification
  cannot load-bear A1 closure on this basis.
- `feedback_hostile_review_semantics.md`: this note stress-tests the
  semantic claim that "`|ρ_{A_1}|²` is the right Lie-algebraic
  invariant to identify with the Brannen amplitude ratio" by showing
  that the action-level identification (operator coefficient ratio =
  Cartan-Killing length-squared) is not a derivable identity — it
  requires a normalization map that retained content does not supply.
- `feedback_retained_tier_purity_and_package_wiring.md`: no automatic
  cross-tier promotion. This note is a bounded obstruction; the
  parent A1 admission remains at its prior bounded status. No
  retained-tier promotion implied.
- `feedback_physics_loop_corollary_churn.md`: the five-barrier
  argument with explicit normalization counterexamples and Lie-algebraic
  analysis is substantive new structural content, not a relabel of
  prior Koide routes. B5 (hidden A_2 absence) is uniquely Route E's.
- `feedback_compute_speed_not_human_timelines.md`: alternative routes
  (A, D) characterized in terms of WHAT additional content would be
  needed (gauge-to-flavor bridge, normalization principle, retained
  Lie algebra, hidden symmetry) — not how-long-they-would-take.
- `feedback_special_forces_seven_agent_pattern.md`: this note packages
  a multi-angle attack (five independent barriers) on a single
  load-bearing structural identification, with sharp PASS/FAIL
  deliverables in the runner.
- `feedback_physics_loop_corollary_churn.md`: this is not corollary
  churn — it is a closure attempt on a previously-open candidate
  identified as "strongest structural hint" and its proper structural
  evaluation. The negative result is informative.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them.

- [koide_a1_derivation_status_note](KOIDE_A1_DERIVATION_STATUS_NOTE.md)
- [koide_a1_route_f_casimir_difference_bounded_obstruction_note_2026-05-08_routef](KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md)
- [koide_circulant_character_derivation_note_2026-04-18](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
- [charged_lepton_koide_cone_algebraic_equivalence_note](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)
- [cl3_sm_embedding_theorem](CL3_SM_EMBEDDING_THEOREM.md)
- [staggered_dirac_substep4_ac_narrow_bounded_note_2026-05-07_substep4ac](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)
- [c3_symmetry_preserved_interpretation_note_2026-05-08](C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md)
- [minimal_axioms_2026-05-03](MINIMAL_AXIOMS_2026-05-03.md)
