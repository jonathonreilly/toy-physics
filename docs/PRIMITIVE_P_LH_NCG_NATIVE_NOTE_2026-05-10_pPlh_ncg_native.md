# P-LH NCG-Native Open Gate — KO-dim-6 J Realization and Order-One Obstruction on the Physical Cl(3)/Z^3 Baseline (pPlh_ncg_native)

**Date:** 2026-05-10
**Type:** open_gate follow-on; no theorem promotion.
**Claim type:** open_gate
**Status authority:** independent audit lane only. This source note
does not add a new primitive, does not promote a status surface, and
does not approve order-one or any NCG import.

**Source-note boundary:** this is an open-gate follow-on
note to [`PRIMITIVE_P_LH_CONTENT_PROPOSAL_NOTE_2026-05-10_pPlh.md`](PRIMITIVE_P_LH_CONTENT_PROPOSAL_NOTE_2026-05-10_pPlh.md).
It tests whether the two NCG primitives identified as the best path to
closing the LH-content open gate — **P-LH-1 (Order-One Condition)** and
**P-LH-3 (KO-dim-6 Real Structure J)** — are forced by the current
physical Cl(3) local algebra on the Z^3 spatial substrate, or whether
they remain candidate imports requiring explicit user approval before
they could become load-bearing.

**Primary runner:** [`scripts/cl3_primitive_p_lh_ncg_native_2026_05_10_pPlh_ncg_native.py`](../scripts/cl3_primitive_p_lh_ncg_native_2026_05_10_pPlh_ncg_native.py)
**Cached output:** [`logs/runner-cache/cl3_primitive_p_lh_ncg_native_2026_05_10_pPlh_ncg_native.txt`](../logs/runner-cache/cl3_primitive_p_lh_ncg_native_2026_05_10_pPlh_ncg_native.txt)

**Net verdict (honest).** The result is an **open-gate diagnostic, not closure**:

| Primitive | Current-source-stack disposition |
|---|---|
| **D2 (KO-dim-6 J)** | **Bounded realization** — a J with KO-dim-6 signs (ε=+1, ε'=+1, ε''=−1) on the chosen per-site model `(H_F = ρ_+ ⊕ ρ_-, γ, D_F = swap)` exists and is constructed explicitly. This is an existence/support calculation, not a proof that the framework uniquely forces that real structure. |
| **D1 (Order-One Condition)** | **Open obstruction** — order-one is not forced by the current physical Cl(3)/Z^3 baseline on three independent grounds. It is a structural constraint on the joint `(A_F, D_F, J)` data, and the current source stack does not select the required `A_F` or `D_F`. |

**Consequence.** The pair {P-LH-1 + P-LH-3} remains an open NCG route.
The runner supports a concrete KO-dim-6-compatible `J` realization and
sharpens the order-one obstruction, but it does not derive LH content
from the framework and does not approve any new primitive.

---

## 0. Notation and standing assumptions

Throughout this note:

- **Cl(3)** denotes the real Clifford algebra `Cl(3,0)` with three
  generators `γ_1, γ_2, γ_3` satisfying `{γ_i, γ_j} = 2δ_{ij}·I`.
- **Cl⁺(3)** denotes the even sub-algebra spanned by
  `{I, γ_1γ_2, γ_1γ_3, γ_2γ_3}`. Context note
  `CL3_SM_EMBEDDING_THEOREM.md`: **Cl⁺(3) ≅ ℍ** (quaternions).
- **ρ_±** denote the two non-isomorphic 2-dim faithful complex irreps
  of Cl(3), distinguished by the central pseudoscalar
  `ω = γ_1γ_2γ_3 → ±i`. Context:
  `AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md`
  (legacy U1-U3 chirality decomposition).
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
   (Derivation)   physical Cl(3)/Z^3 source context  ⊢  P
   (Negation)     physical Cl(3)/Z^3 source context  ⊬  ¬P
   (Forcing)      physical Cl(3)/Z^3 source context allows exactly one P
                  modulo unitary equivalence
```

Passing all three: **derivable** (P closes into source context).
Failing (Derivation): **not derivable**; P remains an open candidate
that would require explicit approval before use as a primitive.
Failing (Forcing): P is a *choice* among admissible options;
derivation is degenerate (the framework does not single one out).

This is strictly stronger than the "structural-exclusion bar" used in
the upstream P-LH proposal, which merely required `P + existing context ⊢
SM-LH and P + existing context ⊬ PS`. Derivability requires that **the
primitive itself emerges**, not merely that it is consistent.

## 2. D2: KO-dim-6 J — bounded realization on the chosen finite model

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

This **J exists on H_F** under
the constraints (a) antilinear, (b) compatible with the chirality
grading, (c) swaps the two ρ_± summands. The construction is useful
bounded support for a KO-dim-6-compatible real structure, but the
current framework has not proved that this is the unique or forced
real structure.

### 2.3 Independence of J from order-one

The construction of J above uses:
- the physical Cl(3) local algebra,
- the chosen two-chirality finite model H_F = ρ_+ ⊕ ρ_-,
- the block-swap σ_x_4 (a permutation matrix, no additional structure),
- standard complex conjugation K (universal in the complex category).

**No use of D_F's order-one structure. No use of A_F's algebra
choice. No use of any spectral triple primitive other than (γ, J).**

### 2.4 D2 verdict: bounded realization, not forced derivation

The KO-dim-6 real structure J is **realized explicitly** on the
chosen `ρ_+ ⊕ ρ_-` Pauli model. The runner verifies the KO-dim-6 sign
triple exactly.

This does **not** close D2 as a theorem. The current source
stack still needs an independent argument that the framework forces
this real structure, or explicit user approval to use it as a
load-bearing import.

## 3. D1: Order-One Condition — not forced on the physical Cl(3)/Z^3 baseline

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

### 3.2 First obstruction: no canonical D_F in the current context

**Lemma 3.2.1 (D_F is not determined by the physical Cl(3)/Z^3 baseline).**
The framework baseline specifies the local algebra (Cl(3)) and
spatial substrate (Z^3). It does NOT specify:

- A Dirac operator D on the substrate.
- A finite Dirac operator D_F on the per-site Hilbert space.
- A spectral triple structure on H_F.

The "staggered-Dirac realization" — which would give a candidate
D_lat on the lattice and induce a D_F — is explicitly outside the
physical Cl(3)/Z^3 baseline
per `MINIMAL_AXIOMS_2026-05-03.md`: it is an open gate
(`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`).

**Consequence.** Even if a unique D_F were FORCED by Cl(3) + Z^3,
the proof of forcing is itself an open gate. Order-one cannot be
derived from the current source context alone because the *operator on
which the condition is stated* is itself not fixed.

### 3.3 Second obstruction: A_F is not determined by the physical Cl(3)/Z^3 baseline

The Connes-Chamseddine algebra `A_F = ℂ ⊕ ℍ ⊕ M_3(ℂ)` has three
direct summands — only one of which (ℍ ≅ Cl⁺(3)) is identified by
existing context `CL3_SM_EMBEDDING_THEOREM.md`. The other two
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
is itself an import, not a derivation. The literature's "input
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

**Now ask the derivability question.** Is order-one forced from
Cl(3)/Z^3 alone? Equivalently: is there a structural reason on
Cl(3)/Z^3 to FORBID the larger PS algebra?

**Answer: no.**

The upstream proposal note `PRIMITIVE_P_LH_CONTENT_PROPOSAL_NOTE_2026-05-10_pPlh.md`
*states this conclusion* (section 2.1, structural-exclusion verdict):

> *"the order-one condition is itself a candidate primitive that
> would require explicit approval — it is not derivable from the
> physical Cl(3) local algebra / Z^3 baseline + Pauli-rep
> chirality alone."*

This follow-on note ASKS whether it can be derived — i.e., whether
there exists some current-source mechanism that FORCES the order-one
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
There is no current-source-stack reason to prefer order-one-compatible
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

### 3.5 D1 verdict: not forced

**Order-one is NOT forced by the physical Cl(3)/Z^3 source context**
on three independent grounds:

1. The Dirac operator on which it is stated is not fixed (open
   gate dependency on staggered-Dirac).
2. The algebra A_F = ℂ ⊕ ℍ ⊕ M_3(ℂ) on which it operates is not
   derived (only the ℍ ≅ Cl⁺(3) factor is represented by the current
   context).
3. Even modulo (1) and (2), order-one is a non-trivial *selection*
   among admissible D_F's — Chamseddine-Connes 2013 explicitly
   shows that without it, Pati-Salam emerges, NOT SM.

**Consequence.** P-LH-1 remains an open primitive candidate. It cannot
be used as a load-bearing framework primitive without explicit user
approval or a future derivation.

## 4. Compatibility with current context

Both P-LH-1 (order-one) and P-LH-3 (KO-dim-6 J) are
**consistent** with the current physical Cl(3)/Z^3 context — i.e.,
the runner does not find a contradiction when they are considered as
candidate imports. This is weaker than derivation.

This note refines that result by separating:
- **D2 = KO-dim-6 J: bounded realization exists** on the chosen
  finite Pauli model.
- **D1 = order-one: consistent but not forced** by the current source
  stack.

## 5. Comparison with the upstream proposal verdict

The upstream proposal note recorded the open-gate verdict:
> *"This converts the LH-content open gate from 'one primitive
> unaccounted for' into 'two NCG primitives that would need substrate-side
> justification.'"*

This follow-on note refines that to:

> **The NCG route has one bounded KO-dim-6 J realization and one
> unresolved order-one primitive candidate that still needs
> substrate-side justification or explicit approval.**

This is partial progress because the route is sharper. It is **NOT
closure** and does not approve order-one.

## 6. Implications for the LH-content campaign

The NCG-native path for closing LH content reduces to a single
remaining sub-question:

> **Can the order-one condition `[[D, a], JbJ⁻¹] = 0` be derived
> from a deeper substrate principle on Cl(3)/Z^3 (or explicitly
> approved as a framework-level primitive on the basis of physical necessity)?**

Two possible paths forward:

### 6.a Explicitly approve order-one as a substrate primitive

This is an available governance path, but it is **not taken here**.
If the user explicitly approves this primitive later, the status of
the gap would become:

```text
   LH-content open gate   →   order-one as named NCG primitive candidate
   (generic gap)              (explicitly approved import, if approved)
```

The order-one condition is well-motivated:
- It is automatic on commutative differential geometry.
- It is the natural extension to noncommutative geometry preserving
  the "gauge field as 1-form" content.
- It is what *Chamseddine-Connes 2013* identify as the load-bearing
  discriminator selecting SM from PS.

Approving order-one as a substrate primitive would be a targeted,
single, well-studied import. This note records that option without
approving it.

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

None of these is currently source-stack content. Each would itself be
a campaign target.

### 6.c Current review-loop path

This note does **not** recommend or apply a primitive approval.
It records why order-one is a named candidate if the user later wants
to approve it. The order-one condition is:
- a single well-studied NCG primitive;
- the canonical Connes 1995/Chamseddine-Connes 2013 discriminator;
- strictly weaker than approving "LH-content as primitive" (which
  would carry no structural content beyond observation);
- compatible with the current physical Cl(3)/Z^3 context in this
  bounded runner.

## 7. Honest scoping caveats

This note explicitly does NOT claim:

- That order-one is derivable on Cl(3)/Z^3. The derivation
  attempts in section 3 all FAIL, on independent grounds.
- That KO-dim-6 J derivation closes the LH-content gap alone. It
  does NOT — section 3 of the upstream proposal note shows
  KO-dim-6 alone permits both SM and PS.
- That the recommended path 6.a is the FINAL state of the
  LH-content campaign. Future work may find a deeper derivation
  (6.b paths remain open).
- That this note's verdict on order-one (NOT derivable) is the
  final word. A more clever derivation argument may exist; the
  three obstructions in section 3 are exhaustive on the *current*
  current source surface, not on all possible derivation attempts.

The honest scope of THIS note is: **the simplest NCG-native
attempt — taking the physical Cl(3)/Z^3 baseline plus the Pauli-rep
chirality decomposition as inputs — does NOT close order-one.** A
KO-dim-6-compatible J is realized on the chosen finite model.

## 8. Forbidden imports respected

- NO PDG observed values used as derivation input
- NO lattice MC empirical measurements
- NO fitted matching coefficients
- NO new repo-wide axioms (order-one is not approved here)
- NO HK + DHR appeal
- NO same-surface family arguments

## 9. Net verdict

**Honest verdict: open-gate diagnostic, not closure.**

- **D2 (KO-dim-6 J): bounded realization** on the chosen
  physical Cl(3)/Z^3 Pauli-rep model. This is useful support, not a
  framework derivation.
- **D1 (Order-One Condition): NOT forced** by the current physical
  Cl(3)/Z^3 source context. P-LH-1 remains an open primitive
  candidate requiring future derivation or explicit user approval.

The LH-content closure path via Connes-Chamseddine NCG is:

```text
   {P-LH-1 (order-one), P-LH-3 (KO-dim-6 J)}
        ↓
   {P-LH-1 (order-one)} still unresolved after this note
        ↓
   future derivation or explicit approval required
```

This is the current review-loop state of the LH-content gap until a
deeper substrate-side derivation of order-one is found or the user
explicitly approves order-one as a primitive.

```yaml
claim_type_author_hint: open_gate
claim_scope: |
  Follow-on open-gate note to PRIMITIVE_P_LH_CONTENT_PROPOSAL_NOTE
  testing whether the two NCG primitives in the {P-LH-1 + P-LH-3}
  pair are forced by the current physical Cl(3)/Z^3 source context.
  Result: D2 (KO-dim-6 J) has a bounded realization on the chosen
  finite Pauli model; D1 (Order-One) is not forced by the current
  source context and remains an open primitive candidate. No status
  promotion or primitive approval is requested.
upstream_dependencies:
  - primitive_p_lh_content_proposal_note_2026-05-10_pPlh
contextual_imports_not_approved:
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
