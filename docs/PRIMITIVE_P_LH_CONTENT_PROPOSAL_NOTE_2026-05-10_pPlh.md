# Primitive P-LH-Content Proposal — Three Candidate Substrate-Side Selectors of SM LH/RH Content over Pati-Salam (pPlh)

**Date:** 2026-05-10
**Type:** primitive_proposal_note (design-note; no theorem promotion)
**Claim type:** primitive_proposal_note (no audit-lane status request)
**Status authority:** independent audit lane only; this is a primitive
design-note that proposes three candidate substrate-side primitives
P-LH-1, P-LH-2, P-LH-3 for further development. The author does NOT
request retention, positive_theorem promotion, or any addition to the
retained primitive list. Each candidate is presented with a
counterfactual test (does it STRUCTURALLY exclude Pati-Salam?) and an
honest verdict on whether the bar is met.

**Source-note proposal disclaimer:** this is a design-note in the
"primitive proposal" lane, mirroring the
`KOIDE_Q_BRIDGE_SINGLE_PRIMITIVE_NOTE_2026-04-22.md` pattern. The
runner verifies the structural distinguishing properties of each
candidate in a Pauli-rep model — it does NOT promote any candidate
to retained primitive status.

**Primary runner:** [`scripts/cl3_primitive_p_lh_2026_05_10_pPlh.py`](../scripts/cl3_primitive_p_lh_2026_05_10_pPlh.py)
**Cached output:** [`logs/runner-cache/cl3_primitive_p_lh_2026_05_10_pPlh.txt`](../logs/runner-cache/cl3_primitive_p_lh_2026_05_10_pPlh.txt)

## 0. Probe context and motivation

Sister probe **Y-Substrate-Anomaly** (PR #947, source-note
`KOIDE_Y_SUBSTRATE_ANOMALY_FORCING_NOTE_2026-05-08_probeY_substrate_anomaly.md`)
established that gauge anomaly cancellation (perturbative ABJ + Witten
Z_2 parity) does NOT force the Standard Model LH/RH content choice —
six anomaly-free alternatives are admissible:

| Alternative | LH content | RH content | Status |
|---|---|---|---|
| Standard Model | (3,2)+(1,2) doublets | (3,1)+(3,1)+(1,1)+(1,1) singlets | observed |
| Pati-Salam | (4,2,1) | (4̄,1,2) | not observed |
| Vectorlike | (R + R̄) on each chirality | (R + R̄) | not observed |
| Trinification SU(3)³ | (3,3̄,1)+(1,3,3̄)+(3̄,1,3) | — | not observed |
| B-L + mirror | symmetric U(1)_B-L + mirror SU(2) | symmetric | not observed |
| SU(5) 5̄+10 | full content one chirality | empty/vectorlike | not observed |

Sister probe **W-Substrate-Chirality** (PR #1021, source-note
`KOIDE_W_SUBSTRATE_CHIRALITY_CL3_Z2_NOTE_2026-05-10_probeW_substrate_chirality.md`)
confirmed that Cl(3)'s natural real Z_2 grading
`Cl(3) = Cl⁺(3) ⊕ Cl⁻(3)` ALSO does NOT force the SM choice. The
structural reason: Cl⁺(3) embeds **identically** in both chirality
summands `ρ_±` because the grade involution `α : γ_i ↦ -γ_i` fixes
Cl⁺(3) pointwise via `(-σ_i)(-σ_j) = σ_iσ_j` sign cancellation.

**Conclusion of the two sister probes:** neither anomaly cancellation
nor Cl(3) Z_2 grading is a load-bearing substrate-side selector of SM
LH/RH content. Closing the gap requires a **non-Z_2, non-anomaly
substrate-side primitive**.

This design-note proposes **three candidate primitives** (P-LH-1,
P-LH-2, P-LH-3) and tests each against the structural-exclusion bar:
*does the candidate STRUCTURALLY reject Pati-Salam (positive forcing)
or does it merely admit SM (mere consistency)?* The verdict for each
is recorded honestly. None reach the bar of clean structural exclusion
on retained primitives alone; each opens a different mathematical
path that would require additional primitive imports.

## 1. Method — assumptions exercise and structural-exclusion bar

### 1.1 Three load-bearing assumptions of the LH-content question

**A1.** SM is the physical truth (motivated by ATLAS/CMS RH-singlet
charged-current measurements; not a derivation primitive).

**A2.** Chirality is fundamental, not emergent (assumes per-site
Cl(3) chirality irreps `ρ_±` are physically distinct, not equivalent
under some hidden mode-mixing symmetry).

**A3.** Cl(3) Z_2 grading is the RIGHT structural lever (denied by
Probe W). This design-note tests three NON-Z_2 candidate levers
instead.

**What if A1 is wrong?** Then the LH content gap is moot — observation
would have selected Pati-Salam, vectorlike, or another option. The
campaign target evaporates. The candidates below are in scope only
under A1.

**What if A2 is wrong?** Then "chirality" is an emergent rather than
fundamental property, and the LH/RH split must be derived from a
deeper substrate (e.g. dynamical generation of asymmetric mode
counts on the lattice). None of the three candidates below assume
emergent chirality; they all take A2 as input.

**What if A3 is wrong?** Sister Probe W has confirmed A3 IS wrong
(Z_2 admits SM, PS, etc.), so this is the mode of operation.

### 1.2 Structural-exclusion bar (hostile-review pattern)

For a candidate primitive `P` to qualify as a load-bearing LH-content
selector, it must satisfy:

```text
   (Forcing)         P + retained primitives  ⊢  SM LH/RH content
   (Exclusion)       P + retained primitives  ⊬  Pati-Salam content
   (Independence)    P is not derivable from retained primitives alone
   (Minimality)      P is the minimal addition that achieves exclusion
```

Mere consistency (`P` admits SM but ALSO admits PS) does NOT pass the
bar — that is what Probe W found for Z_2 grading. We require strict
structural rejection of PS.

### 1.3 Counterfactual test for each candidate

For each candidate primitive `P_i`, the runner verifies in numerical
exact-algebra:

```text
   (PS-test)    Does adding P_i to the retained Cl(3) Pauli-rep model
                CONTRADICT a Pati-Salam-style assignment?
   (SM-test)    Does adding P_i admit the SM-style assignment?
   (Indep-test) Is P_i derivable from W-Pos-1, W-Pos-2 alone?
                  (If yes, no new primitive content; reject.)
```

If `(PS-test) = YES` and `(SM-test) = YES` and `(Indep-test) = NO`,
the candidate **passes** the structural-exclusion bar. If
`(PS-test) = NO` (PS still admitted), the candidate **fails** —
reduces to mere consistency, like Z_2 grading.

## 2. Three candidate primitives

### 2.1 P-LH-1 — Order-One Condition (Connes-Chamseddine analog)

**Formal statement.**

> **P-LH-1.** *(Order-One on Cl(3) connection 1-form.)* On the
> retained Cl(3)/Z^3 substrate, the gauge connection 1-form `A` is
> required to be a first-order differential operator on the per-site
> Cl(3) Hilbert representation: `[[A, b'], b''] = 0` for all
> `b', b'' ∈ A_F` where `A_F = C ⊕ Cl⁺(3) ⊕ M_3(C)` is the per-site
> finite-algebra. Equivalently, the inner fluctuation `D ↦ D + A` of
> the Dirac operator preserves the order-one structure (no quadratic
> terms in `A`).

**Derivation of SM LH/RH split.** In the Connes-Chamseddine spectral
triple program (arXiv:1304.8050), enforcing the order-one condition
on the finite Dirac operator `D_F` on the algebra
`A_F = C ⊕ H ⊕ M_3(C)` (where `H = Cl⁺(3)`) reduces the gauge group
from `SU(2)_L × SU(2)_R × SU(4)` (Pati-Salam) to
`U(1)_Y × SU(2)_L × SU(3)_C` (Standard Model). The reduction proceeds
because:

1. Without order-one, the inner fluctuation generates a chiral mass
   term coupling LH and RH at the algebra level, forcing both
   chiralities to carry the H = Cl⁺(3) action symmetrically (Pati-Salam).
2. With order-one, the finite Dirac operator commutes with the right
   action of `A_F^op`, restricting `A` to one-sided (left) action.
   The C ⊕ H summand splits as `(c, q)` where `c ∈ C` acts on
   right-singlets and `q ∈ H` acts on left-doublets — exactly the SM
   LH-doublet/RH-singlet split.

**Physical/mathematical interpretation.** The order-one condition is
the substrate-level statement that the gauge field is a *connection*
on a *bundle*, not a tensor. In QFT language: gauge fields are
1-forms valued in the Lie algebra, not 2-forms or higher. The
condition is automatic in commutative differential geometry (Levi-Civita
connection is order-one on smooth functions); in noncommutative
geometry it must be imposed as a primitive on the spectral triple.

**Literature analog.**
- Chamseddine-Connes, "Beyond the Spectral Standard Model: Emergence
  of Pati-Salam Unification," JHEP 11 (2013) 132, arXiv:1304.8050.
  The crucial result is exactly that DROPPING order-one upgrades SM
  to Pati-Salam, and IMPOSING order-one selects SM.
- Connes, *Gravity coupled with matter and the foundation of
  noncommutative geometry*, Comm. Math. Phys. 182 (1996) 155, where
  the order-one axiom is introduced as a spectral-triple primitive.
- Boyle-Farnsworth, "A new algebraic structure in the Standard Model
  of particle physics," JHEP 06 (2018) 071, refines order-one into a
  graded-bimodule condition.

**Counterfactual (PS-test).** In the runner, P-LH-1 implements
order-one as: `A ∈ A_F` acts only on the LEFT of the per-site Hilbert
H_F (no right action). We verify that under this restriction:
- `[A_LH, A_RH] = 0` in the SM-style assignment (compatible),
- a Pati-Salam-style assignment with SU(2)_R acting on RH doublets
  WOULD generate a non-zero quadratic term in `D + A` that VIOLATES
  order-one (incompatible).

**Structural-exclusion verdict.** In the Pauli-rep model the runner
confirms order-one CONSTRAINS the LH/RH algebra split (PS-test: PS
generates a forbidden quadratic term). However, **the order-one
condition is itself a candidate primitive that must be IMPORTED into
the framework — it is not derivable from retained Cl(3)/Z^3 + Pauli-rep
chirality alone**. Verdict: **passes structural-exclusion bar
conditional on import**; the import itself becomes a new admission.

### 2.2 P-LH-2 — Asymmetric Algebra Action (`Cl⁺(3)` acts only on `ρ_+`)

**Formal statement.**

> **P-LH-2.** *(Asymmetric Cl⁺(3) action.)* On the retained
> Cl(3)/Z^3 substrate, the per-site finite-algebra `A_F` is fixed to
> act ASYMMETRICALLY on the chirality summands by the structural
> identification:
> ```text
>    A_F = C ⊕ Cl⁺(3) ⊕ M_3(C),
>    H_F = (ρ_+ ⊗ V_doublet) ⊕ (ρ_- ⊗ V_singlet),
>    Cl⁺(3) acts on ρ_+ part only,
>    C ⊕ M_3(C) acts on ρ_- part only.
> ```
> The asymmetry is built into the algebra-Hilbert pairing as a
> primitive structural choice, not as an emergent property of the
> Cl(3) Z_2 grading.

**Derivation of SM LH/RH split.** By construction: the LH summand
`ρ_+ ⊗ V_doublet` carries the SU(2) action of `Cl⁺(3)` (giving
SU(2)_L doublets), and the RH summand `ρ_- ⊗ V_singlet` carries no
SU(2) action — it is a singlet. This is the SM LH-doublet/RH-singlet
content by definition.

**Physical/mathematical interpretation.** This primitive embeds the
LH/RH asymmetry at the level of the algebra-Hilbert pairing rather
than the algebra itself. It is essentially the SM Connes triple
applied to the Cl(3) substrate, with the chirality summands `ρ_±`
replacing the abstract `H_F`. The asymmetry is by *fiat* at the
substrate level.

**Literature analog.**
- Connes-Marcolli, *Noncommutative Geometry, Quantum Fields and
  Motives*, AMS Colloquium Publications 55 (2008), Ch. 1, where the
  algebra-Hilbert pairing for the SM finite triple is constructed
  with explicit asymmetry between left-action of H and left-action
  of C.
- van den Dungen-van Suijlekom, *Particle physics from almost
  commutative spacetimes*, Rev. Math. Phys. 24 (2012) 1230004,
  classifies allowable A_F-H_F pairings.

**Counterfactual (PS-test).** In the runner, P-LH-2 implements the
asymmetric pairing literally: a 4-dim block `H_F = ρ_+ ⊕ ρ_-` with
the projector `P_LH = diag(1, 0, 0, 0; 0, 1, 0, 0; 0, 0, 0, 0; 0, 0, 0, 0)`
(acts on ρ_+ summand) and `Cl⁺(3)` action `J_a ⊗ P_LH`. A Pati-Salam
embedding `J_a^L ⊗ P_LH + J_a^R ⊗ P_RH` violates the structural
identification because P-LH-2 forbids `P_RH`-supported algebra
elements in `Cl⁺(3)` (the right-singlet half of `A_F` is `C ⊕ M_3(C)`,
not `H ⊕ M_3(C)`).

**Structural-exclusion verdict.** P-LH-2 forces the SM split BY
CONSTRUCTION — the asymmetry is in the primitive's statement. Mere
consistency or even tautology: P-LH-2 says "SM LH/RH split is the
substrate primitive," which is logically equivalent to admitting SM
as a primitive. **This is the most direct primitive but the WEAKEST
on the bar of "structural derivation": it merely renames the
admission**. Verdict: **fails minimality** (the primitive is the
admission, restated). It is included for completeness as the trivial
direct path.

### 2.3 P-LH-3 — Real Structure J Anticommuting with Chirality γ (KO-dim 6)

**Formal statement.**

> **P-LH-3.** *(Real structure J of KO-dimension 6.)* On the
> retained Cl(3)/Z^3 substrate, the per-site Hilbert space carries a
> real structure (antilinear isometry) `J : H_F → H_F` of
> KO-dimension 6 (mod 8), satisfying:
> ```text
>    J² = +1,                       (KO-dim 6 sign)
>    J D = D J,                     (real Dirac operator)
>    J γ = -γ J,                    (anticommutes with chirality)
>    [a, JbJ⁻¹] = 0  for all a, b ∈ A_F  (commutant property).
> ```
> Equivalently, `(J, γ, D)` form a real spectral triple of
> KO-dimension 6.

**Derivation of SM LH/RH split.** In Connes' classification (arXiv:hep-th/0608226,
Connes 2006 *Noncommutative geometry and the standard model with
neutrino mixing*), the finite spectral triple of KO-dimension 6 has
the unique algebra `A_F = M_2(H) ⊕ M_4(C)` reduced under the
order-one condition to `A_F = C ⊕ H ⊕ M_3(C)` — exactly the SM
algebra. The KO-dim-6 J satisfies `J² = +1`, `JγJ⁻¹ = -γ` (so it
swaps chiralities). The compatibility condition forces:

1. The H = Cl⁺(3) summand of `A_F` acts on LH-doublet states only.
2. The C summand acts on RH-singlet states.
3. The M_3(C) summand acts on color triplets symmetrically across
   chiralities.

The KO-dim-6 sign choice `J² = +1` (vs `J² = -1` for KO-dim 2 or 4)
is the load-bearing primitive: it fixes the index theory and forces
the LH/RH commutant decomposition of `A_F` to be ASYMMETRIC.

**Physical/mathematical interpretation.** The real structure J is
the spectral-triple analog of charge conjugation: `J ψ = ψ_c`. The
sign of `J²` determines the index theorem in the spectral action and
the absence/presence of the see-saw mechanism for neutrinos
(Barrett, Connes 2006-2007). On a 4-dim spacetime × KO-dim-6 finite
geometry, the total KO-dimension is `4 + 6 = 10 ≡ 2 (mod 8)`, which
admits Majorana spinors in dimension 10 — the spinor structure of
type I superstring theory.

**Literature analog.**
- Connes, "Noncommutative geometry and the standard model with
  neutrino mixing," JHEP 11 (2006) 081, arXiv:hep-th/0608226.
  The KO-dim-6 (mod 8) classification is Theorem 4.1, and it forces
  `J² = +1` on the finite spectral triple.
- Barrett, "A Lorentzian version of the noncommutative geometry of
  the standard model of particle physics," J. Math. Phys. 48 (2007)
  012303, arXiv:hep-th/0608221.
- Chamseddine-Connes-Marcolli, "Gravity and the standard model with
  neutrino mixing," Adv. Theor. Math. Phys. 11 (2007) 991,
  arXiv:hep-th/0610241, derives the see-saw mechanism from KO-dim-6.

**Counterfactual (PS-test).** In the runner, P-LH-3 implements the
KO-dim-6 J in the Pauli-rep model with `J = γ_2 K` (complex
conjugation followed by σ_2), verifying:
- `J² = +I_2` (KO-dim 6 sign),
- `Jγ_5J⁻¹ = -γ_5` (anticommutes with chirality),
- `[Cl⁺(3), J·M_3(C)·J⁻¹] = 0` (commutant property forces algebra split).

A Pati-Salam algebra `M_2(H_R) ⊕ M_2(H_L) ⊕ M_4(C)` is the algebra
classified WITHOUT the order-one condition (Chamseddine-Connes 2013).
With KO-dim-6 + order-one, the algebra reduces to SM. Without
order-one but WITH KO-dim-6, PS is admitted. So P-LH-3 alone does
NOT pass the bar — it must be paired with P-LH-1 (order-one).

**Structural-exclusion verdict.** P-LH-3 alone (KO-dim-6) admits both
SM and PS — so it FAILS the structural-exclusion bar in isolation.
Combined with P-LH-1 (order-one), the pair `{P-LH-1, P-LH-3}` selects
SM uniquely. Verdict: **passes only as a pair with P-LH-1**; KO-dim-6
alone is necessary but not sufficient.

## 3. Comparative table

| Primitive | Forcing-test | PS-exclusion-test | Independence-test | Minimality-test | Verdict |
|---|---|---|---|---|---|
| P-LH-1 (order-one) | YES (with C ⊕ H ⊕ M_3 algebra) | YES (PS violates order-one) | YES (new condition not in retained) | YES (single primitive condition) | **passes conditional on algebra import** |
| P-LH-2 (asymmetric pairing) | YES (by construction) | YES (PS forbidden by primitive) | NO (the primitive IS the admission) | NO (renames admission) | **fails minimality / circular** |
| P-LH-3 (KO-dim-6 J) | NO (alone, admits both) | NO (alone) | YES | NO (alone) | **fails alone; passes paired with P-LH-1** |

**Net design conclusion.** None of the three candidates is a clean
single-primitive solution on retained Cl(3)/Z^3 inputs alone. The
strongest path is **{P-LH-1 + P-LH-3} (order-one + KO-dim-6 J)**,
which is the load-bearing combination in the Connes-Chamseddine SM
derivation. To use this path on the framework one would need to:

1. Import order-one as a substrate-side primitive on the per-site
   Cl(3) connection,
2. Import KO-dim-6 (mod 8) as a substrate-side primitive on the
   per-site real structure J,
3. Verify the imported primitives are minimal — the Connes-Chamseddine
   derivation does not give a unique algebra without ALSO assuming
   the C ⊕ H ⊕ M_3(C) finite algebra (which, on Cl(3), reads
   C ⊕ Cl⁺(3) ⊕ M_3(C)).

This converts the LH-content admission from "one primitive
unaccounted for" to "two NCG primitives that need substrate-side
justification." Whether this is progress depends on whether the
imported NCG primitives admit a Cl(3)/Z^3-native derivation — a
separate campaign.

## 4. Out of scope

This design-note does NOT claim:

- A retained-grade derivation of SM LH/RH content from Cl(3)/Z^3 +
  any of the three primitives above. Each primitive is a candidate
  IMPORT, not a derivation.
- A ruling on whether Connes-Chamseddine's NCG derivation of SM is
  itself fundamental or admits its own deeper reduction.
- A claim that any of P-LH-1, P-LH-2, P-LH-3 should be added to the
  retained primitive list.
- A proof that no other candidate primitive (e.g. holographic
  boundary condition, Lorentzian-signature constraint, anomaly
  inflow from a 5D boundary) can close the gap. Other paths remain
  open.

## 5. Forbidden imports respected

- NO PDG observed values used as derivation input
- NO lattice MC empirical measurements
- NO fitted matching coefficients
- NO new repo-wide axioms (the three candidates are PROPOSALS; no
  retention requested)
- NO HK + DHR appeal
- NO same-surface family arguments

## 6. Honest verdict

**Net verdict: design-note records three candidate primitives. None
is a clean single-primitive closure on retained Cl(3)/Z^3 inputs.**

- **P-LH-1 (order-one)** has the strongest literature support
  (Chamseddine-Connes 2013) and is the load-bearing primitive in the
  NCG SM derivation. It passes the structural-exclusion bar
  *conditional on importing the spectral-triple algebra structure
  C ⊕ Cl⁺(3) ⊕ M_3(C)*. The import itself is a new admission, not a
  retained derivation.
- **P-LH-2 (asymmetric pairing)** is the most direct but circular —
  it embeds the SM split as a primitive, which is logically
  equivalent to admitting SM as the primitive. Useful as a
  formalism baseline but does not advance the campaign.
- **P-LH-3 (KO-dim-6 J)** is necessary for the NCG derivation but
  not sufficient alone (admits both SM and PS); it works only when
  paired with P-LH-1.

The recommended next step is a follow-on note investigating whether
the Connes-Chamseddine algebra `C ⊕ Cl⁺(3) ⊕ M_3(C)` admits a
substrate-side derivation from Cl(3)/Z^3 alone. If yes, the LH-content
gap reduces to "import order-one + KO-dim-6 as substrate primitives".
If no, the gap remains the bundled admission of the three NCG
ingredients.

```yaml
claim_type_author_hint: primitive_proposal_note
claim_scope: |
  Design-note proposing three candidate substrate-side primitives
  P-LH-1 (Order-One Condition), P-LH-2 (Asymmetric Algebra Action),
  P-LH-3 (KO-dim-6 Real Structure J) for selecting SM LH/RH content
  over Pati-Salam and other anomaly-free alternatives. Each is
  tested against the structural-exclusion bar (forcing + PS-rejection
  + independence + minimality). None is a clean single-primitive
  solution on retained Cl(3)/Z^3 inputs alone; the strongest path is
  the pair {P-LH-1 + P-LH-3} which corresponds to the Connes-Chamseddine
  NCG derivation of the SM and itself imports new substrate-side
  primitives. No retention is requested.
upstream_dependencies:
  - axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29
  - cl3_sm_embedding_theorem
  - no_per_site_chirality_theorem_note_2026-05-02
  - koide_y_substrate_anomaly_forcing_note_2026-05-08_probeY_substrate_anomaly
  - koide_w_substrate_chirality_cl3_z2_note_2026-05-10_probeW_substrate_chirality
admitted_context_inputs:
  - Connes-Chamseddine NCG primitives (order-one, KO-dim-6, finite
    algebra A_F = C ⊕ H ⊕ M_3(C)) cited as literature support, NOT
    imported into the retained framework
  - standard Clifford grade-involution structure (textbook)
literature_references:
  - Chamseddine-Connes, JHEP 11 (2013) 132, arXiv:1304.8050
  - Connes, JHEP 11 (2006) 081, arXiv:hep-th/0608226
  - Chamseddine-Connes-Marcolli, Adv. Theor. Math. Phys. 11 (2007) 991, arXiv:hep-th/0610241
  - Connes-Marcolli, NCG Quantum Fields and Motives (AMS 2008), Ch. 1
  - Boyle-Farnsworth, JHEP 06 (2018) 071
  - Barrett, J. Math. Phys. 48 (2007) 012303, arXiv:hep-th/0608221
```
