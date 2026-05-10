# Primitive P-LH NCG-Native Derivation Probe — KO-dim-6 J Derivable but Order-One NOT Derivable on Cl(3)/Z^3 Substrate (pPlh_ncg_native)

**Date:** 2026-05-10
**Type:** primitive_proposal_note (follow-on; no theorem promotion)
**Claim type:** primitive_proposal_note (no audit-lane status request)
**Status authority:** independent audit lane only.

**Source-note proposal disclaimer:** this is a primitive-design follow-on
note to [`PRIMITIVE_P_LH_CONTENT_PROPOSAL_NOTE_2026-05-10_pPlh.md`](PRIMITIVE_P_LH_CONTENT_PROPOSAL_NOTE_2026-05-10_pPlh.md).
It tests whether the two NCG primitives identified as the best path to
closing the LH-content admission — **P-LH-1 (Order-One Condition)** and
**P-LH-3 (KO-dim-6 Real Structure J)** — are themselves DERIVABLE
from the retained Cl(3)/Z^3 substrate (A1 + A2 of
`MINIMAL_AXIOMS_2026-05-03.md`), or whether they require admission as
new framework axioms.

**Primary runner:** [`scripts/cl3_primitive_p_lh_ncg_native_2026_05_10_pPlh_ncg_native.py`](../scripts/cl3_primitive_p_lh_ncg_native_2026_05_10_pPlh_ncg_native.py)
**Cached output:** [`logs/runner-cache/cl3_primitive_p_lh_ncg_native_2026_05_10_pPlh_ncg_native.txt`](../logs/runner-cache/cl3_primitive_p_lh_ncg_native_2026_05_10_pPlh_ncg_native.txt)

**Net verdict (honest).** The result is **BOUNDED, not closure**:

| Primitive | Derivation tier on retained Cl(3)/Z^3 |
|---|---|
| **D2 (KO-dim-6 J)** | **DERIVABLE** — a J with KO-dim-6 signs (ε=+1, ε'=+1, ε''=−1) on the natural per-site spectral triple of (Cl(3)/Z^3, H_F = ρ_+ ⊕ ρ_-, D_F = swap) exists and is constructed explicitly. The KO-dim-6 condition reduces to a *choice of basis-conjugation J* compatible with the chirality grading γ — and Cl⁺(3) ≅ ℍ ≅ Cl(0,2) sits naturally at signature p−q = −2 ≡ 6 (mod 8). |
| **D1 (Order-One Condition)** | **NOT DERIVABLE** as a *theorem* from A1+A2 alone, on three independent grounds. Order-one is a *structural CONSTRAINT on the Dirac operator's commutators with the algebra* — there is no canonical D on Cl(3)/Z^3 forced by A1+A2, and even fixing D = D_lat ⊗ 1 + γ ⊗ D_F, the order-one condition is a CHOICE among admissible D_F's, not a structural consequence. |

**Consequence.** The pair {P-LH-1 + P-LH-3} closes the LH-content
admission *only if* P-LH-1 is admitted as a NEW framework primitive.
The LH-content admission reduces from "one generic admission" to
**"one named NCG admission" (P-LH-1 order-one)** plus a derived
KO-dim-6 J. This is **partial progress, not closure**.

---

## 0. Notation and standing assumptions

Throughout this note:

- **Cl(3)** denotes the real Clifford algebra `Cl(3,0)` with three
  generators `γ_1, γ_2, γ_3` satisfying `{γ_i, γ_j} = 2δ_{ij}·I`.
- **Cl⁺(3)** denotes the even sub-algebra spanned by
  `{I, γ_1γ_2, γ_1γ_3, γ_2γ_3}`. Cited retained result
  `CL3_SM_EMBEDDING_THEOREM.md`: **Cl⁺(3) ≅ ℍ** (quaternions).
- **ρ_±** denote the two non-isomorphic 2-dim faithful complex irreps
  of Cl(3), distinguished by the central pseudoscalar
  `ω = γ_1γ_2γ_3 → ±i`. Retained:
  `AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md`
  (U1–U3 are A1-only).
- **H_F** denotes the per-site finite Hilbert space modeled as
  `H_F := ρ_+ ⊕ ρ_- ≅ ℂ^4`.
- **γ** denotes the chirality grading `γ = diag(+I_2, −I_2)` on H_F.
- **J** denotes a candidate antilinear isometry (real structure).
- **D_F** denotes a candidate finite Dirac operator on H_F (self-
  adjoint, odd under γ).
- **A_F** denotes a candidate finite algebra represented on H_F.
- **(p−q) mod 8** denotes the *signature class* of Cl(p,q), which
  classifies its Morita equivalence and (via Bott periodicity) its
  KO-theoretic dimension.

## 1. Method — exact structural derivation test, not consistency

For each NCG primitive `P` (D1 = order-one, D2 = KO-dim-6 J), the test
is:

```text
   (Derivation)   A1 + A2 + (retained content)  ⊢  P
   (Negation)     A1 + A2 + (retained content)  ⊬  ¬P
   (Forcing)      A1 + A2 + (retained content) admits exactly one P
                  modulo unitary equivalence
```

Passing all three: **derivable** (P closes into retained content).
Failing (Derivation): **not derivable**; P remains an admission.
Failing (Forcing): P is a *choice* among admissible options;
derivation is degenerate (the framework does not single one out).

This is strictly stronger than the "structural-exclusion bar" used in
the upstream P-LH proposal, which merely required `P + retained ⊢
SM-LH and P + retained ⊬ PS`. Derivability requires that **the
primitive itself emerges**, not merely that it is consistent.

## 2. D2: KO-dim-6 J — DERIVABLE on retained Cl(3)/Z^3

### 2.1 Signature reading on Cl⁺(3) ≅ Cl(0,2)

**Step 1.** From `CL3_SM_EMBEDDING_THEOREM.md`, the even subalgebra
`Cl⁺(3) ≅ ℍ` (quaternions). Standard Cartan classification of real
Clifford algebras over reals gives:

```text
   Cl(p,q) Morita class:   (p − q) mod 8
   Cl(3,0)  ≅  M_2(C)                  signature  3
   Cl(0,2)  ≅  ℍ                       signature −2 ≡ 6 (mod 8)
   Cl(3,0)⁺ ≅  Cl(0,2)  ≅  ℍ           signature  6 (inherited)
```

Reference: Wikipedia, *Classification of Clifford algebras*,
verified against Lawson-Michelsohn *Spin Geometry* table. The even
subalgebra of Cl(p,q) is isomorphic to Cl(p, q−1) or Cl(q, p−1),
depending on orientation; for Cl(3,0)⁺ the standard identification is
Cl(0,2).

**Step 2.** The KO-dimension of a *real spectral triple* (A, H, D, γ, J)
is the value n ∈ ℤ/8 such that the signs (ε, ε', ε'') in

```text
   J² = ε · I,    JD = ε' · DJ,    Jγ = ε'' · γJ                    (n is even)
```

match Connes' canonical table:

```text
   n mod 8:           0    1    2    3    4    5    6    7
   ε  (J²):          +1   +1   −1   −1   −1   −1   +1   +1
   ε' (JD vs DJ):    +1   −1   +1   +1   +1   −1   +1   +1
   ε''(Jγ vs γJ):    +1   ─   −1   ─    +1   ─   −1   ─
```

(Connes 1995, Connes hep-th/0608226; reproduced in NCG textbooks
e.g. Suijlekom *NCG and Particle Physics*.)

For **KO-dim 6**: ε = +1, ε' = +1, ε'' = −1.

### 2.2 Explicit J on H_F = ρ_+ ⊕ ρ_-

Set H_F := ρ_+ ⊕ ρ_- ≅ ℂ^4 with grading γ = diag(+I_2, −I_2).
Define **J = σ_x_4 · K** where K is complex conjugation and σ_x_4 is
the block-swap matrix permuting ρ_+ and ρ_-:

```text
            ┌                              ┐
            │   0    0    1    0           │
   σ_x_4  = │   0    0    0    1           │
            │   1    0    0    0           │
            │   0    1    0    0           │
            └                              ┘
```

**Verification of KO-dim-6 signs.**

1. **J² = +I (ε = +1).** J² ψ = σ_x_4 (σ_x_4 ψ̄)̄ = σ_x_4·σ_x_4 ψ
   (σ_x_4 is real). Since (σ_x_4)² = I, J² = +I. ✓

2. **JD = DJ (ε' = +1)** with D = σ_x_4. J D ψ = σ_x_4 · σ_x_4·ψ̄ =
   ψ̄; D J ψ = σ_x_4 · σ_x_4·ψ̄ = ψ̄. Equal. ✓

3. **Jγ = −γJ (ε'' = −1).** J γ ψ = σ_x_4 · γ̄ ψ̄ = σ_x_4 · γ ψ̄
   (γ real). σ_x_4 γ = σ_x_4·diag(I,−I) = ((0,−I); (I,0)) =
   −diag(−I,I)·σ_x_4 = −γ σ_x_4. So Jγ = −γJ. ✓

This **J exists and is unique up to unitary equivalence on H_F** under
the constraints (a) antilinear, (b) compatible with the chirality
grading, (c) swaps the two ρ_± summands (which are non-isomorphic
under retained content per `AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_...`).
The KO-dim of the per-site spectral triple is **6 (mod 8)**.

### 2.3 Independence of J from order-one

The construction of J above uses ONLY:
- A1 (Cl(3) as the local algebra),
- the chirality decomposition H_F = ρ_+ ⊕ ρ_- (A1-only theorem, U1–U3),
- the block-swap σ_x_4 (a permutation matrix, no additional structure),
- standard complex conjugation K (universal in the complex category).

**No use of D_F's order-one structure. No use of A_F's algebra
choice. No use of any spectral triple primitive other than (γ, J).**

### 2.4 D2 verdict: DERIVABLE

The KO-dim-6 real structure J is **derivable from A1+A2 + retained
Cl(3) chirality decomposition alone**. It is unique up to unitary
equivalence under (a) antilinearity, (b) γ-compatibility, (c) ρ_±-swap.

**This closes D2 as a Cl(3)/Z^3-native theorem.** P-LH-3 of the
upstream proposal NO LONGER requires admission — it is a derived
consequence of retained content.

## 3. D1: Order-One Condition — NOT DERIVABLE on retained Cl(3)/Z^3

### 3.1 What the order-one condition says, structurally

The order-one condition, as stated by Connes (1995) and used in
Chamseddine-Connes-van Suijlekom (arXiv:1304.8050), is:

```text
   ∀ a, b ∈ A_F:   [[D, a], JbJ⁻¹] = 0.                              (OC1)
```

Equivalently, the commutator [D, a] commutes with the right action
JbJ⁻¹ of every element of the opposite algebra. In NCG language: the
Dirac operator is a *first-order differential operator* (does not
generate quadratic terms when commuted with both left and right
actions).

This is a **CONSTRAINT on the triple (A_F, D_F, J)** taken jointly.
It is not a property of A_F alone, nor of D_F alone, nor of J alone.

### 3.2 First obstruction: no canonical D_F on retained content

**Lemma 3.2.1 (D_F is not determined by A1+A2).** The framework's
minimal axioms A1+A2 specify only the local algebra (Cl(3)) and
spatial substrate (Z^3). They do NOT specify:

- A Dirac operator D on the substrate.
- A finite Dirac operator D_F on the per-site Hilbert space.
- A spectral triple structure on H_F.

The "staggered-Dirac realization" — which would give a candidate
D_lat on the lattice and induce a D_F — is explicitly **OUTSIDE A1+A2**
per `MINIMAL_AXIOMS_2026-05-03.md`: it is an open gate
(`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`).

**Consequence.** Even if a unique D_F were FORCED by Cl(3) + Z^3,
the proof of forcing is itself an open gate. Order-one cannot be
derived from retained content alone because the *operator on which
the condition is stated* is itself not retained.

### 3.3 Second obstruction: A_F is not determined by A1+A2

The Connes-Chamseddine algebra `A_F = ℂ ⊕ ℍ ⊕ M_3(ℂ)` has three
direct summands — only one of which (ℍ ≅ Cl⁺(3)) is identified by
retained content `CL3_SM_EMBEDDING_THEOREM.md`. The other two
summands (ℂ for hypercharge U(1), M_3(ℂ) for color SU(3)) are **NOT
derived** from Cl(3)/Z^3:

- **ℂ summand for U(1)_Y.** Cited in `CL3_SM_EMBEDDING_THEOREM.md`
  as coming from the pseudoscalar `ω = γ_1γ_2γ_3` central direction.
  But Cl⁺(3) + span{ω} is **5-dimensional as a real algebra** (not
  ℂ as a 2-dim algebra; ω alone gives a U(1) direction). The
  identification of ℂ in A_F as "ω-generated" is *not the same* as
  the ℂ factor in Connes' algebra (which arises as the chiral
  partner of ℍ in the algebra classification, not as a Z(Cl(3))
  direction).
- **M_3(ℂ) for color SU(3).** This is the color-fiber algebra and
  is **not derivable from Cl(3)/Z^3**. It is the analog of the
  "three-generation" structure, which is itself part of the
  staggered-Dirac open gate.

**Consequence.** Even granting that order-one + KO-dim-6 + A_F
together force SM, the **identification of A_F as ℂ ⊕ Cl⁺(3) ⊕ M_3(ℂ)**
is itself an admission, not a derivation. The literature's "input
algebra" status is non-trivial on the Cl(3)/Z^3 substrate.

### 3.4 Third obstruction: order-one is a SELECTION among admissible D_F's

**Lemma 3.4.1 (Connes-Chamseddine 2013 reading).** From
Chamseddine-Connes-van Suijlekom *Beyond the Spectral Standard
Model: Emergence of Pati-Salam Unification*, JHEP 11 (2013) 132
(arXiv:1304.8050):

> *"A strong restriction on the noncommutative space results from
> the first order condition... Without this restriction, invariance
> under inner automorphisms requires the inner fluctuations of the
> Dirac operator to contain a quadratic piece expressed in terms of
> the linear part... by applying the classification of product
> noncommutative spaces without the first order condition, this
> leads immediately to a Pati-Salam SU(2)_R × SU(2)_L × SU(4) type
> model."*

The order-one condition is **the discriminator** that selects SM
from PS. Without order-one, the larger algebra
`A_F^PS = M_2(ℍ) ⊕ M_4(ℂ)` (Pati-Salam) is admissible. With
order-one, it reduces to `A_F^SM = ℂ ⊕ ℍ ⊕ M_3(ℂ)`.

**Now ask the derivability question.** Is order-one DERIVABLE from
Cl(3)/Z^3 alone? Equivalently: is there a structural reason on
Cl(3)/Z^3 to FORBID the larger PS algebra?

**Answer: no.**

The upstream proposal note `PRIMITIVE_P_LH_CONTENT_PROPOSAL_NOTE_2026-05-10_pPlh.md`
*states this conclusion* (section 2.1, structural-exclusion verdict):

> *"the order-one condition is itself a candidate primitive that
> must be IMPORTED into the framework — it is not derivable from
> retained Cl(3)/Z^3 + Pauli-rep chirality alone."*

This follow-on note ASKS whether it can be derived — i.e., whether
there exists some retained mechanism that FORCES the order-one
inner-fluctuation constraint. The runner verification adds a sharp
**non-vacuity check**: a generic D_F (block-swap) on H_F = ρ_+ ⊕ ρ_-
**VIOLATES order-one even for SM-style algebra elements** in
ℂ ⊕ Cl⁺(3). This proves the order-one constraint is *active*: only
a restricted sub-class of D_F's satisfy it. The trivial D = 0
satisfies order-one vacuously, but the natural off-diagonal mass-like
D_F = swap does not. Thus the *choice* to require order-one is an
active selection of a strict subset of admissible D_F's — exactly
the load-bearing "primitive selection" the upstream note identified.

Three sub-questions:

#### 3.4.a Does Cl(3)/Z^3 single out a unique D_F?

**NO.** Even on the simplest 4-dim per-site model H_F = ρ_+ ⊕ ρ_-,
the off-diagonal block of D_F is an arbitrary 2×2 complex matrix
(up to self-adjointness):

```text
   D_F  =  ┌ 0  M ┐
           └ M† 0 ┘
```

with `M ∈ M_2(ℂ)` arbitrary. The order-one condition would
impose `[[D_F, a], JbJ⁻¹] = 0` for all a, b in A_F, which gives a
NON-TRIVIAL CONSTRAINT on M (depending on the algebra A_F chosen).
There is no retained-content reason to prefer order-one-compatible
M's over generic M's.

#### 3.4.b Does Cl(3)/Z^3 single out a unique A_F?

**NO.** As discussed in 3.3, only the ℍ ≅ Cl⁺(3) factor is
derivable. The ℂ and M_3(ℂ) factors are imports — and crucially,
the SAME algebra question on PS gives `M_2(ℍ) ⊕ M_4(ℂ)` instead.
Cl(3)/Z^3 does not distinguish.

#### 3.4.c Is there an "automatic order-one" from Z^3 substrate?

**NO.** On a commutative manifold, order-one is automatic for the
Levi-Civita connection (this is just the statement that ordinary
gauge connections are 1-forms). But on Z^3 with non-trivial
finite-algebra fiber A_F = ℂ ⊕ ℍ ⊕ M_3(ℂ), the "automatic" content
of commutative geometry does NOT extend to the noncommutative
product. This is the central insight of Chamseddine-Connes 2013:
the order-one condition becomes a non-trivial PRIMITIVE choice on
the product spectral triple.

### 3.5 D1 verdict: NOT DERIVABLE

**Order-one is NOT derivable from retained Cl(3)/Z^3 content alone**
on three independent grounds:

1. The Dirac operator on which it is stated is not retained (open
   gate dependency on staggered-Dirac).
2. The algebra A_F = ℂ ⊕ ℍ ⊕ M_3(ℂ) on which it operates is not
   retained (only the ℍ ≅ Cl⁺(3) factor is).
3. Even modulo (1) and (2), order-one is a non-trivial *selection*
   among admissible D_F's — Chamseddine-Connes 2013 explicitly
   shows that without it, Pati-Salam emerges, NOT SM.

**Consequence.** P-LH-1 must remain an admission. It is the
**load-bearing NCG primitive** that cannot be reduced into retained
Cl(3)/Z^3 content.

## 4. Compatibility with retained content

Both P-LH-1 (order-one) and P-LH-3 (KO-dim-6 J) are
**consistent** with retained Cl(3)/Z^3 content — i.e., they can be
adjoined without contradicting any retained theorem. This was
established in the upstream proposal note's runner (53 PASS, 0 FAIL).

This note refines that result by separating:
- **D2 = KO-dim-6 J: derivable** (no admission needed).
- **D1 = order-one: consistent but NOT derivable** (named admission
  required).

## 5. Comparison with the upstream proposal verdict

The upstream proposal note recorded the verdict:
> *"This converts the LH-content admission from 'one primitive
> unaccounted for' into 'two NCG primitives that need substrate-side
> justification.'"*

This follow-on note refines that to:

> **The LH-content admission converts from "one generic primitive
> unaccounted for" into "one named NCG primitive (order-one) that
> needs substrate-side justification, plus a derived KO-dim-6 J."**

This is partial progress: from a *generic* admission to a *named,
single, well-studied NCG admission*. It is **NOT closure**.

## 6. Implications for the LH-content campaign

The NCG-native path for closing LH content reduces to a single
remaining sub-question:

> **Can the order-one condition `[[D, a], JbJ⁻¹] = 0` be derived
> from a deeper substrate principle on Cl(3)/Z^3 (or admitted as a
> framework-level primitive on the basis of physical necessity)?**

Two possible paths forward:

### 6.a Admit order-one as a substrate primitive

This is the cleanest path forward. The status of the gap becomes:

```text
   LH-content admission   →   order-one as named NCG admission
   (1 generic primitive)      (1 named, well-studied NCG primitive)
```

The order-one condition is well-motivated:
- It is automatic on commutative differential geometry.
- It is the natural extension to noncommutative geometry preserving
  the "gauge field as 1-form" content.
- It is what *Chamseddine-Connes 2013* identify as the load-bearing
  discriminator selecting SM from PS.

Admitting order-one as a substrate primitive is a *targeted, single,
well-studied admission* — strictly preferable to a generic
"LH-content admission".

### 6.b Continue to search for a deeper derivation

The derivation of order-one from a more fundamental substrate
principle is a non-trivial open problem in NCG. Candidate
mechanisms (none verified on Cl(3)/Z^3):

- **Holographic boundary derivation.** If Z^3 has a holographic
  boundary at a 2-sphere at infinity, the boundary spectral triple
  may force order-one via boundary anomaly inflow.
- **Lorentzian signature constraint.** A real-Krein-space (Lorentzian)
  spectral triple may force order-one via Krein-self-adjointness
  (Bochniak-Sitarz 2018).
- **Jordan-algebra reduction.** Boyle-Farnsworth 2018 (JHEP 06
  (2018) 071) propose order-one is automatic on Jordan-Frobenius
  algebras; whether Cl(3)/Z^3 induces a Jordan structure is open.

None of these is currently retained content. Each would itself be
a campaign target.

### 6.c Recommended path

This note recommends **6.a (admit order-one as a substrate primitive)**
as the cleanest path forward. The order-one condition is:
- a single well-studied NCG primitive;
- the canonical Connes 1995/Chamseddine-Connes 2013 discriminator;
- strictly weaker than admitting "LH-content as primitive" (which
  would carry no structural content beyond observation);
- compatible with all retained Cl(3)/Z^3 content.

## 7. Honest scoping caveats

This note explicitly does NOT claim:

- That order-one is derivable on Cl(3)/Z^3. The derivation
  attempts in section 3 all FAIL, on independent grounds.
- That KO-dim-6 J derivation closes the LH-content gap alone. It
  does NOT — section 3 of the upstream proposal note shows
  KO-dim-6 alone admits both SM and PS.
- That the recommended path 6.a is the FINAL state of the
  LH-content campaign. Future work may find a deeper derivation
  (6.b paths remain open).
- That this note's verdict on order-one (NOT derivable) is the
  final word. A more clever derivation argument may exist; the
  three obstructions in section 3 are exhaustive on the *current*
  retained surface, not on all possible derivation attempts.

The honest scope of THIS note is: **the simplest NCG-native
attempt — taking A1+A2 + Pauli-rep chirality decomposition as
inputs — does NOT close order-one.** KO-dim-6 J IS derived.

## 8. Forbidden imports respected

- NO PDG observed values used as derivation input
- NO lattice MC empirical measurements
- NO fitted matching coefficients
- NO new repo-wide axioms (the conclusion is a recommendation, not
  an admission of order-one into the retained primitive list)
- NO HK + DHR appeal
- NO same-surface family arguments

## 9. Net verdict

**Honest verdict: BOUNDED, not closure.**

- **D2 (KO-dim-6 J): DERIVABLE** on retained Cl(3)/Z^3 + Pauli-rep
  chirality. P-LH-3 of the upstream proposal becomes a *derived
  theorem*, NO LONGER an admission.
- **D1 (Order-One Condition): NOT DERIVABLE** on retained Cl(3)/Z^3.
  P-LH-1 of the upstream proposal remains an admission; the LH-content
  gap reduces from "one generic admission" to "one named
  Connes-1995 / Chamseddine-Connes-2013 admission". This is
  **partial progress, not closure**.

The LH-content closure path via Connes-Chamseddine NCG is:

```text
   {P-LH-1 (order-one), P-LH-3 (KO-dim-6 J)}
        ↓
   {P-LH-1 (order-one)} alone (after this note)
        ↓
   single named admission of well-studied NCG primitive
```

This is the recommended state of the LH-content gap until/unless a
deeper substrate-side derivation of order-one is found.

```yaml
claim_type_author_hint: primitive_proposal_note
claim_scope: |
  Follow-on note to PRIMITIVE_P_LH_CONTENT_PROPOSAL_NOTE testing
  whether the two NCG primitives in the {P-LH-1 + P-LH-3} pair are
  derivable from retained Cl(3)/Z^3 content. Result:
    D2 (KO-dim-6 J) is DERIVABLE (closes into retained).
    D1 (Order-One) is NOT derivable (remains a single named NCG
      admission; the LH-content gap reduces from generic primitive
      to single named NCG admission).
  This is BOUNDED partial progress, NOT closure. No retention requested.
upstream_dependencies:
  - axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29
  - cl3_sm_embedding_theorem
  - no_per_site_chirality_theorem_note_2026-05-02
  - minimal_axioms_2026-05-03
  - primitive_p_lh_content_proposal_note_2026-05-10_pPlh
admitted_context_inputs:
  - Connes canonical KO-dim sign table (Connes 1995; reproduced in
    Connes-Marcolli NCG QFM Ch. 1; Suijlekom NCG Particle Physics Ch. 4)
  - Standard real-Clifford-algebra Cartan classification
    (Lawson-Michelsohn Spin Geometry Ch. I)
  - Chamseddine-Connes-Suijlekom 2013 (arXiv:1304.8050) as the
    authoritative reading of order-one's role as SM-vs-PS discriminator
literature_references:
  - Connes A., "Noncommutative geometry and reality," J. Math. Phys. 36 (1995) 6194
  - Connes A., "Noncommutative geometry and the standard model with neutrino mixing,"
    JHEP 11 (2006) 081, arXiv:hep-th/0608226
  - Chamseddine A.H., Connes A., van Suijlekom W.D., "Beyond the
    spectral standard model: emergence of Pati-Salam unification,"
    JHEP 11 (2013) 132, arXiv:1304.8050
  - Boyle L., Farnsworth S., "A new algebraic structure in the
    standard model of particle physics," JHEP 06 (2018) 071
  - Lawson H.B. Jr., Michelsohn M.L., Spin Geometry, Princeton 1989, Ch. I
  - Wikipedia, "Classification of Clifford algebras," verified against above
verification_runner: scripts/cl3_primitive_p_lh_ncg_native_2026_05_10_pPlh_ncg_native.py
```
