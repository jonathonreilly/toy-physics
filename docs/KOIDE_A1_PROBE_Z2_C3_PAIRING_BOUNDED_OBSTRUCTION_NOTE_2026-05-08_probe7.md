# Koide A1 Probe 7 — Retained Z_2 × C_3 Pairing Bounded Obstruction

**Date:** 2026-05-08
**Type:** bounded_theorem (sharpened obstruction; no positive closure)
**Claim type:** bounded_theorem
**Scope:** review-loop source-note proposal — Probe 7 closure attempt for
the A1 √2 equipartition admission via Survey-2-motivated retained
Z_2 × C_3 = Z_6 pairing on the charged-lepton Koide lane.
**Status:** source-note proposal for a **negative closure** — none of the
five retained-grade Z_2 candidates produces a Z_2-equivariance
constraint that canonically forces `|b|²/a² = 1/2` on C_3-equivariant
Hermitian circulants on hw=1. The A1 admission count is UNCHANGED.
**Authority role:** source-note proposal — audit verdict and downstream
status set only by the independent audit lane.
**Loop:** koide-a1-probe7-z2-c3-pairing-20260508
**Primary runner:** [`scripts/cl3_koide_a1_probe_z2_c3_pairing_2026_05_08_probe7.py`](../scripts/cl3_koide_a1_probe_z2_c3_pairing_2026_05_08_probe7.py)
**Cache:** [`logs/runner-cache/cl3_koide_a1_probe_z2_c3_pairing_2026_05_08_probe7.txt`](../logs/runner-cache/cl3_koide_a1_probe_z2_c3_pairing_2026_05_08_probe7.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived status is generated
only after the independent audit lane reviews the claim, dependency
chain, and runner. The `claim_type`, scope, named admissions, and
bounded-obstruction classification are author-proposed; the audit lane
has full authority to retag, narrow, or reject the proposal.

## Naming-collision warning

In this note:
- "framework axiom A1" = retained Cl(3) local-algebra axiom per
  `MINIMAL_AXIOMS_2026-05-03.md`.
- "**A1-condition**" = the Brannen-Rivero amplitude-ratio constraint
  `|b|²/a² = 1/2` on the C_3-equivariant Hermitian circulant
  `H = a·I + b·U + b̄·U^{-1}` (the Frobenius equipartition).

These are distinct objects despite the shared label.

## Question

A Survey-2 finding (external) frames the A1-condition obstruction as:

> **`C_3`-symmetry alone CANNOT produce a Z_2-flavored rational like
> 1/2.** Pure C_3 gives 1/3, 2/3, 1/9, etc. The 1/2 in A1 is a **Z_2
> fact riding on a C_3-symmetric vector**. Any closure of A1 must
> identify a retained **Z_2 paired with C_3** giving a composite
> **Z_6 = Z_2 × C_3** that canonically forces equal-modulus eigenvalues
> on the C_3-symmetric subspace.

This redirects from "find the right C_3 mechanism" (which the prior 9
no-go theorems cover negatively) to "find the retained Z_2 that pairs
with C_3 on hw=1 to force the multiplicity-weighted ratio."

**Question:** does any retained Z_2 candidate, paired with the
retained C_3[111] on hw=1, canonically force the A1-condition?

## Answer

**No.** None of the 5 retained-grade Z_2 candidates produces such a
forcing. Each candidate fails the structural test for one of three
reasons:

  (a) **Trivial action on the operator algebra of hw=1**: the Z_2
      acts as identity on the C_3-circulant subspace, so it imposes
      no constraint on `(a, b)`. (Candidates 3, 4, 5: pseudoscalar
      ω-flip, fermion parity F, APBC twist.)

  (b) **Z_2 acts non-trivially but with semidirect (not direct)
      product structure**: the Z_2 anticommutes with C_3, generating
      the symmetric group `S_3 = Z_3 ⋊ Z_2`, NOT the direct product
      Z_6 = Z_2 × C_3 that Survey 2 framed. (Candidates 1, 2:
      inversion Z_2 and (12)-transposition.)

  (c) **Even when (b) is sidestepped by restricting to the
      Z_2-equivariant circulant subspace, the resulting constraint
      reduces only to "b ∈ ℝ" — a 2-real-parameter family in which
      the A1-condition `|b|²/a² = 1/2` is a codim-1 surface, NOT
      a forced point.**

The combined picture: **Probe 7 is structurally barred**. Survey 2's
"Z_2 fact riding on C_3" framing partially captures the structural
landscape (the 1/2 IS a multiplicity ratio, distinct from pure C_3
arithmetic outputs 1/3, 2/3, etc.) but it identifies the wrong
locus: the 1/2 in A1 is the C_3 multiplicity ratio
`(dim trivial-χ Hermitian) / (dim non-trivial-χ Hermitian) = 3/6 = 1/2`,
not a Z_2-derived halving.

## Setup

### Premises (A_min for Probe 7 closure attempt)

| ID | Statement | Class |
|---|---|---|
| A1 | Cl(3) local algebra | framework axiom; see `MINIMAL_AXIOMS_2026-05-03.md` |
| A2 | Z³ spatial substrate | framework axiom; same source |
| Embed | Cl⁺(3) ≅ ℍ → SU(2)_L; ω = Γ_1 Γ_2 Γ_3 pseudoscalar central with ω² = -I | retained: [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md) |
| Circulant | C_3-equivariant Hermitian on hw=1 is `aI + bU + b̄U^{-1}` | retained: [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md) R1 |
| KoideAlg | Koide Q = 2/3 ⟺ a₀² = 2|z|² ⟺ |b|²/a² = 1/2 (algebraic) | retained: [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md) |
| FermPar | F = (-1)^Q̂_total is positive_theorem on framework Fock; Z_2-EVEN on bilinears | retained: [`FERMION_PARITY_Z2_GRADING_THEOREM_NOTE_2026-05-02.md`](FERMION_PARITY_Z2_GRADING_THEOREM_NOTE_2026-05-02.md) F7 |
| CircParity | P_{23}-Z_2 acts on Hermitian-circulant family decomposing it into even (real-b) and odd (imaginary-b) parts | retained: [`CIRCULANT_PARITY_CP_TENSOR_NARROW_THEOREM_NOTE_2026-05-02.md`](CIRCULANT_PARITY_CP_TENSOR_NARROW_THEOREM_NOTE_2026-05-02.md) T1, T2 |
| Z2HW1 | Z_2 = ⟨(12)⟩ acting on hw=1 ordered basis (X_3, X_1, X_2) gives 5-real-parameter Hermitian normal form | proposed_retained: [`Z2_HW1_MASS_MATRIX_PARAMETRIZATION_NOTE.md`](Z2_HW1_MASS_MATRIX_PARAMETRIZATION_NOTE.md) |
| APBC | Anti-periodic boundary conditions on Λ ⊂ Z³ are framework substrate convention | retained per [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md) APBC premise |
| APBC_var | Z_3 phase variants on closed-cube APBC reduce to PBC (uniform twists cancel globally) | retained-bounded: [`SU3_Z3_APBC_VARIANT_PROBE_2026-05-04.md`](SU3_Z3_APBC_VARIANT_PROBE_2026-05-04.md) |
| Substep4 | AC_φλ remains the explicit identification residual on hw=1 | retained-bounded: [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md) |
| RouteFObst | Route F (Yukawa Casimir-difference) is structurally barred | retained: [`KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md`](KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md) |

### Forbidden imports

- NO PDG observed mass values used as derivation input (anchor-only at
  end, clearly marked per
  [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)).
- NO lattice MC empirical measurements
- NO fitted matching coefficients
- NO same-surface family arguments
- **NO new axioms** (Probe 7's promise was retained-content closure;
  any A3-class admission requires explicit user approval and is not
  proposed here).
- NO admitted SM Yukawa-coupling pattern as derivation input
- NO Survey-2 promotion: Survey 2 is external scoping context, NOT a
  retained authority. Its framing motivated the question; it does not
  load-bear any conclusion here.

## The structural lemma at issue (Probe 7 framing)

**Proposed lemma (Probe 7, Survey 2-motivated):**
```
There exists a retained Z_2 acting on hw=1 that, paired with the
retained C_3[111] action, generates a Z_6 = Z_2 × C_3 representation
whose Z_6-equivariance on Hermitian operators forces

  |b|² / a²  =  1/2
```
on the C_3-equivariant circulant subspace.

This note investigates whether ANY retained Z_2 candidate satisfies
this proposal.

## Theorem (Probe 7 bounded obstruction)

**Theorem.** On A1+A2 + retained CL3_SM_EMBEDDING + retained
KOIDE_CIRCULANT_CHARACTER + retained CIRCULANT_PARITY_CP_TENSOR +
retained FERMION_PARITY_Z_2_GRADING + retained APBC convention +
retained Z2_HW1_MASS_MATRIX parametrization + admissible standard
math:

```
None of the 5 retained-grade Z_2 candidates {inversion (S↔S²),
(12)-axis-transposition, pseudoscalar ω-flip, fermion parity F,
APBC↔PBC twist} paired with C_3[111] forces |b|²/a² = 1/2 on
C_3-equivariant Hermitian circulants on hw=1.

Five independent structural barriers — one per candidate — each block
the proposed Z_6 closure.
```

**Proof sketch.** Each barrier is verified independently in the paired
runner. The barriers fall into three categories:

  - **Trivial-action barriers** (candidates 3, 4, 5): the Z_2 commutes
    with C_3 (so does generate Z_6 abstractly) but acts as identity
    on the C_3-circulant subspace. No (a, b) constraint imposed.

  - **Semidirect-product barriers** (candidates 1, 2): the Z_2 does not
    commute with C_3; instead `Z_2 · U_C3 · Z_2 = U_C3^{-1}`. This
    generates `S_3 = Z_3 ⋊ Z_2`, NOT the direct product `Z_6`. Survey
    2's Z_2 × C_3 framing is structurally inapplicable.

  - **Codimension barriers** (when sidestepping into the
    Z_2-equivariant subspace of S_3-action): the imposed constraint
    reduces circulants to "b ∈ ℝ" (2-real-parameter family). The
    A1-condition is a codim-1 algebraic surface within this 2D plane —
    not a forced point.

A unifying barrier (Section 6 of the runner): scale-invariance defeats
any LINEAR Z_2. The A1-condition `|b|² = a²/2` is a quadratic
constraint on (a, b); a linear involution `P` with `P² = I` has fixed-
point set `ker(I - P)` — a LINEAR SUBSPACE, hence a CONE, hence
contains either no ratio or a continuum of ratios. Picking out the
SPECIFIC ratio 1/2 requires non-linear input (e.g., a quadratic-form
equipartition principle).

### Barrier 1: Z_2 inversion (S ↔ S²) — semidirect, no Z_6

The C_3 character group has an outer involution sending each character
`ω^k → ω^{-k}`. The implementing matrix is the transposition `P_{23}`
(swap indices 2, 3 of the corner basis), satisfying

```
P_{23} · U · P_{23} = U^{-1}        [retained CIRCULANT_PARITY T1]
```

This Z_2 does NOT commute with C_3. Rather, it generates the
semidirect product `S_3 = Z_3 ⋊ Z_2`, which is NOT the direct product
`Z_6 = Z_2 × C_3` Survey 2's framing assumed.

If we restrict to `P_{23}`-invariant Hermitian circulants:

```
P_{23} · (aI + bU + b̄U^{-1}) · P_{23}  =  aI + bU^{-1} + b̄U
                                      =  aI + b̄U + bU^{-1}
```

So `P_{23}`-invariance ⟹ `b = b̄` ⟹ `b ∈ ℝ`. This restricts the
3-real-parameter circulant family `(a, Re b, Im b)` to a
2-real-parameter family `(a, b ∈ ℝ)`.

Within this 2D family, `|b|²/a² = b²/a²` is unconstrained: the runner
exhibits explicit `P_{23}`-invariant circulants with ratios 0.01, 0.25,
1.0, 4.0, AND 0.5 — A1 is just one point in a continuous moduli, not
forced.

### Barrier 2: (12)-axis-transposition Z_2 — same fate as Barrier 1

The Z_2 = ⟨(12)⟩ fixing axis 3 of hw=1 (per
[`Z2_HW1_MASS_MATRIX_PARAMETRIZATION_NOTE.md`](Z2_HW1_MASS_MATRIX_PARAMETRIZATION_NOTE.md))
is implemented by `P_{12}` (swap indices 1, 2) which also satisfies
`P_{12} U P_{12} = U^{-1}`.

The runner verifies that `P_{12}` and `P_{23}` produce the same
constraint on the circulant subspace (`b ∈ ℝ`) — both are Z_2
candidates inside `S_3`, both yield semidirect not direct product.

The Z2_HW1 normal form (5-real-parameter Hermitian operators with
`(12)`-symmetry on `hw=1`) is BROADER than the C_3-equivariant
circulants — the 5D family includes non-circulant operators. The
intersection (operators that are both `C_3`-equivariant AND
`P_{12}`-invariant) collapses to the 2-real-parameter real-b
circulants of Barrier 1. Same conclusion: A1 not forced.

### Barrier 3: Pseudoscalar ω-flip orientation Z_2 — trivial action

Per [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md)
Section B, ω = Γ_1 Γ_2 Γ_3 is **central** in Cl(3,0): it commutes with
all Γ_i (and all even-grade elements). The orientation Z_2 sends
ω → -ω, but this acts only on the Cl(3) taste sector.

The hw=1 corner sector lives in a SPATIAL sector orthogonal to the
Cl(3) taste sector (per
[`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md)
the C_3[111] cycle acts on spatial corner indices, not Cl(3) taste).
Therefore the ω-flip acts as identity on the C_3-circulant operators
on hw=1.

Trivial action ⟹ no (a, b) constraint. The runner verifies all
ratios pass `ω`-flip equivariance. Z_6 is generated abstractly (Z_2
trivial × C_3) but the Z_2 contributes no information.

### Barrier 4: Fermion parity F = (-1)^Q̂_total — trivial on bilinears

Per [`FERMION_PARITY_Z2_GRADING_THEOREM_NOTE_2026-05-02.md`](FERMION_PARITY_Z2_GRADING_THEOREM_NOTE_2026-05-02.md)
property F7: `[F, a_x^† a_y] = 0`. F is **Z_2-EVEN on bilinears**.

The hw=1 generation triplet lives in the bilinear sector (per the
staggered-Dirac realization, the BZ-corner states correspond to
fermion-bilinear occupation patterns). On the bilinear sector, F acts
as +I (Z_2-charge 0).

Trivial action ⟹ no constraint. Z_6 generated trivially as in
Barrier 3. The runner verifies all ratios are F-equivariant.

### Barrier 5: APBC↔PBC boundary-condition Z_2 — substrate-level only

APBC is part of the framework's retained substrate convention (per
[`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md)
APBC premise). The Z_2 here is the substrate-level choice "APBC vs
PBC".

This Z_2 acts at the level of choosing WHICH 8 BZ corners exist (with
what phases), not on the M_3(ℂ) operator algebra on hw=1 once the
corners are fixed. Per
[`SU3_Z3_APBC_VARIANT_PROBE_2026-05-04.md`](SU3_Z3_APBC_VARIANT_PROBE_2026-05-04.md):
uniform Z_3 twists cancel globally on closed lattices (`P(β=6)`
identical for PBC and Z_3-symmetric APBC).

Therefore APBC↔PBC does not constrain the C_3-circulant `(a, b)` on
hw=1. No information is contributed.

### Universal barrier: scale-invariance + linearity

The A1-condition `|b|²/a² = 1/2` is invariant under uniform rescaling
`(a, b) → (λa, λb)`. It is a quadratic constraint on `(a, b)`, not a
linear one.

Any linear Z_2 action `P` on `(a, b)` (with `P² = I`) has fixed-point
set `ker(I - P)` — a linear subspace. A linear subspace of `ℝ²` (or
`ℂ⊕ℝ` for complex `b`) closed under scale is a CONE: it contains
either no nontrivial ratio or a continuum thereof.

To single out `|b|²/a² = 1/2` specifically, one needs either:
  (i) a NON-LINEAR action (not a Z_2-style symmetry — Z_2 is by
      definition involutive linear), or
  (ii) a NORMALIZATION PRINCIPLE external to Z_2-equivariance (e.g., a
       fixed multiplicity-weighted Frobenius equality, max-entropy
       principle, RMT measure) — exactly the open candidates per
       [`HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md`](HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md)
       Theorem 5.

Probe 7's framing — "the Z_2 paired with C_3 forces 1/2" — runs into
this universal barrier independently of which specific Z_2 candidate
is tried.

The runner makes the barrier explicit: testing reflection-Z_2 across
the line `b = m·a` gives ratio `m²` for any real `m`; the choice
`m = 1/√2` (giving 1/2) is unmotivated by Z_2 structure alone.
Admitting `m = 1/√2` IS the A1 admission; circular.

## Why Survey 2's framing partially redirected but did not close

Survey 2 correctly observed that pure C_3 multiplication on its
1-dimensional irreps produces only the rationals `1/3, 2/3, 1/9, 2/9,
…` (powers of `1/3` from `|χ_trivial|² = 1, |χ_nontrivial|² = 1` with
multiplicity-3 dimension). The 1/2 in A1 is NOT in this set, so a
"more than C_3" structure is needed.

But the resolution is **not** "find the right Z_2 paired with C_3";
the resolution is **"recognize that 1/2 is the C_3-multiplicity ratio
3:6 from the Hermitian-algebra decomposition `M_3(ℂ)_Herm = 3 trivial
⊕ 3 ω ⊕ 3 ω̄`."**

Specifically:
```
1/2  =  (dim of trivial-character Hermitian subspace) /
        (dim of non-trivial-character Hermitian subspace)
     =  3 / 6
```

This 1/2 comes from the C_3 representation theory ON the 9-dimensional
Hermitian algebra `M_3(ℂ)_Herm`, not from any external Z_2. The A1
equipartition `3a² = 6|b|²` IS the equality of multiplicity-weighted
Frobenius norms of these two subspaces.

The genuine open question for A1 closure remains: **what retained
PRINCIPLE chooses equipartition between trivial and non-trivial
character sectors?** Candidates surveyed but not derived:
  - Random-matrix (GOE/GUE) measure equipartition
  - Max-entropy principle on isotypic decomposition
  - Schur orthogonality-derived weight (this gives the `3:6` weights
    themselves, but not equipartition between them)
  - 2nd-order phase-transition equipartition (analogue of classical
    equipartition theorem)

None of these is a Z_2 structure; they are normalization principles.
This is consistent with the 9 prior no-go theorems and with the Route
F bounded obstruction
([`KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md`](KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md)
B4 category mismatch).

## Sharpening over prior work

| Prior closure attempt | Status | Comment |
|---|---|---|
| Route A (Koide-Nishiura U(3) quartic) | open; outside Theorem 6 | trace-based 4th-order; needs derivation |
| Route B (Clifford torus on S³) | does not match Koide cone | 45° latitude vs equator |
| Route C (AS Lefschetz cot²) | parallel numeric identity | 2/3 = 2/3 coincidence |
| Route D (Newton-Girard) | open; trace-poly form | 6 = n(n+1)/2 coefficient unforced |
| Route E (A_1 Weyl-vector / Kostant) | three-way exact match | `|ρ_{A_1}|² = 1/2` matches but no derivation |
| Route F (Yukawa Casimir-difference) | bounded obstruction | four-barrier negative closure (RouteFObst) |
| **Probe 7 (Z_2 × C_3 = Z_6)** | **THIS NOTE: bounded obstruction** | **five-candidate negative closure** |

This note **complements** the Route F bounded obstruction by ruling
out the structurally distinct "Z_2-paired-with-C_3" closure family.
Together, Route F + Probe 7 establish that:
  - "Gauge-Casimir → flavor coefficient" maps fail (Route F)
  - "Discrete-symmetry → flavor coefficient" maps fail (Probe 7)

Both fail under the same meta-pattern: the framework's retained content
does NOT supply a normalization principle on the matter-sector C_3
moduli. The remaining open candidates (A, D, E) all require either an
imported potential (Koide-Nishiura), a new normalization principle
(equipartition-by-physics), or explicit user-approved A3-class admission.

## Convention robustness check

The Route F obstruction (B1) showed that `T(T+1) − Y² = 1/2` is
convention-dependent (PDG vs SU(5)). For Probe 7 candidates, the
runner verifies:

- Z_2 (1) inversion: NOT invariant under global phase `b → e^{iα}b`
  (fails outside `α ∈ {0, π}`).
- Z_2 (2) (12)-transposition: same as (1) — fails phase rotation.
- Z_2 (3) ω-flip: phase-invariant by triviality (no constraint).
- Z_2 (4) F: phase-invariant by triviality (no constraint).
- Z_2 (5) APBC: substrate-level, no operator action on hw=1.

**Universal: NO Z_2 candidate produces `|b|²/a² = 1/2` in
convention-invariant form** — either trivial constraint or breaks
under phase rotation.

## What this closes

- **Probe 7 negative closure** (bounded obstruction). Five
  retained-grade Z_2 candidates ruled out as Survey-2 closure paths.
- **Survey 2 framing reframed**: Survey 2's "Z_2 fact riding on
  C_3-symmetric vector" is corrected to "1/2 is a C_3-MULTIPLICITY
  ratio (3:6) on `M_3(ℂ)_Herm`", not a Z_2-derived halving. The
  correct open question is which RETAINED NORMALIZATION PRINCIPLE
  selects equipartition between trivial- and non-trivial-character
  sectors.
- **Audit-defensibility**: explicit numerical counterexamples to each
  Z_2 candidate's putative closure — every claimed Z_2 has a
  retained-compatible circulant violating A1.
- **Route F + Probe 7 meta-conclusion**: both "gauge-side" and
  "discrete-symmetry-side" closure paths fail; remaining open candidates
  (A, D, E) all require explicit normalization-principle work.

## What this does NOT close

- A1 admission count is unchanged. A1 remains a load-bearing non-axiom
  step on the Brannen circulant lane.
- Routes A (Koide-Nishiura quartic), D (Newton-Girard), E
  (Kostant Weyl-vector) remain open candidates.
- Charged-lepton Koide closure remains a bounded observational-pin
  package (status from
  [`CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md`](CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md)
  unchanged).
- AC_φλ residual (substep 4) is unaffected.
- L3a trace-surface bounded obstruction status unchanged.
- The Route F numerical-match runner
  [`scripts/frontier_koide_a1_yukawa_casimir_identity.py`](../scripts/frontier_koide_a1_yukawa_casimir_identity.py)
  retains its prior PASS for the *numerical* check.

## Empirical falsifiability

| Claim | Falsifier |
|---|---|
| Inversion-Z_2 obstruction (B1) | Construct a derivation in which the inversion-Z_2 ON THE CIRCULANT FAMILY (not on the broader 9-dim algebra) imposes a quadratic constraint linking `a²` and `|b|²` — refutes the linear-action argument. |
| Axis-transposition obstruction (B2) | Same — exhibit non-linear S_3 action that singles out `m = 1/√2`. |
| Pseudoscalar-trivial obstruction (B3) | Exhibit a retained primitive in which ω acts non-trivially on the spatial corner sector — refutes sector-orthogonality. |
| Fermion-parity-trivial obstruction (B4) | Exhibit a Z_2-odd operator in the hw=1 generation triplet sector — refutes bilinear-only F action. |
| APBC-substrate obstruction (B5) | Construct an APBC-twist Z_2 that acts non-trivially on the M_3(ℂ) operator algebra of hw=1 (not just on sector selection) — refutes substrate-level argument. |
| Universal scale-invariance barrier | Construct a non-linear Z_2 action (e.g., Möbius-style) that singles out `|b|²/a² = 1/2` — refutes linearity-based barrier. |
| Numerical anchor | Falsified if charged-lepton Koide Q deviates significantly from 2/3 in updated PDG; the representative anchor values used by the paired runner give Q = 0.666661 (sub-0.001% match). |

## Review boundary

This note proposes `claim_type: bounded_theorem` for the independent
audit lane. The bounded theorem is the negative Probe 7 boundary: no
retained-grade Z_2 candidate produces a Z_2-equivariance constraint
that canonically forces `|b|²/a² = 1/2`. The five candidate fates are
verified independently in the runner.

No new admissions are proposed. A1 remains unchanged at its prior
load-bearing non-axiom status on the Brannen circulant lane. The
independent audit lane may retag, narrow, or reject this proposal.

## Promotion-Value Gate (V1-V5)

| # | Question | Answer |
|---|---|---|
| V1 | Verdict-identified obstruction closed? | The "Z_2 paired with C_3 = Z_6 forces 1/2" Survey-2 framing is sharpened from "open candidate path" to "structurally barred under retained content; needs non-linear action or external normalization principle." |
| V2 | New derivation? | The five-candidate enumeration with explicit fates (trivial / semidirect / scale-invariance) is new structural content. Prior status note enumerated none of these candidates explicitly. |
| V3 | Audit lane could complete? | Yes — the audit lane can review (i) inversion semidirect, (ii) (12)-transposition semidirect, (iii) ω-flip triviality, (iv) F-bilinear-triviality, (v) APBC substrate-level, and the universal scale-invariance barrier. |
| V4 | Marginal content non-trivial? | Yes — the C_3-multiplicity reframing of 1/2 (= 3/6) replaces Survey 2's "Z_2 halving" framing with a derivable arithmetic identity, redirecting the open-question scope away from Z_2-symmetry-finding to normalization-principle finding. |
| V5 | One-step variant? | No — Probe 7 attacks a structurally distinct closure family from Routes A-F (discrete symmetries, not gauge-Casimir, trace-polynomial, or Lie-algebra Weyl coincidences). Five distinct candidate Z_2's plus universal barrier. |

**Source-note V1-V5 screen: pass for bounded-obstruction audit
seeding.**

## Why this is not "corollary churn"

Per `feedback_physics_loop_corollary_churn.md`, the user-memory rule
is to avoid one-step relabelings of already-landed cycles. This note:

- Is NOT a relabel of Route F (which attacked gauge-Casimir-difference)
  or any of Routes A-E. The five Z_2 candidates and their per-candidate
  obstructions are distinct closure-class arguments.
- Identifies a NEW STRUCTURAL OBSERVATION (the C_3-multiplicity 3:6
  reframing of 1/2) that wasn't present in
  [`KOIDE_A1_DERIVATION_STATUS_NOTE.md`](KOIDE_A1_DERIVATION_STATUS_NOTE.md)
  or in Route F.
- Provides explicit numerical counterexamples for each Z_2 candidate
  (multiple A1-violating ratios passing each candidate's putative
  symmetry).
- Sharpens Survey 2's framing from "open Z_2 × C_3 closure path" to
  "structurally barred Z_2 family; redirect to normalization principle."

## Cross-references

- A1 derivation status (parent): [`KOIDE_A1_DERIVATION_STATUS_NOTE.md`](KOIDE_A1_DERIVATION_STATUS_NOTE.md)
- Route F bounded obstruction (sister): [`KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md`](KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md)
- Circulant character derivation (R1, R2 source): [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
- Charged-lepton Koide-cone algebraic equivalence: [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)
- CL3 SM embedding (ω, Cl⁺(3) source): [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md)
- Fermion parity Z_2 grading (F source): [`FERMION_PARITY_Z2_GRADING_THEOREM_NOTE_2026-05-02.md`](FERMION_PARITY_Z2_GRADING_THEOREM_NOTE_2026-05-02.md)
- Circulant parity CP-tensor (P_{23} source): [`CIRCULANT_PARITY_CP_TENSOR_NARROW_THEOREM_NOTE_2026-05-02.md`](CIRCULANT_PARITY_CP_TENSOR_NARROW_THEOREM_NOTE_2026-05-02.md)
- Z_2 hw=1 parametrization (P_{12} source): [`Z2_HW1_MASS_MATRIX_PARAMETRIZATION_NOTE.md`](Z2_HW1_MASS_MATRIX_PARAMETRIZATION_NOTE.md)
- BZ-corner forcing (APBC + hw=1 source): [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md)
- SU(3) Z_3 APBC variant probe: [`SU3_Z3_APBC_VARIANT_PROBE_2026-05-04.md`](SU3_Z3_APBC_VARIANT_PROBE_2026-05-04.md)
- Substep 4 AC narrowing: [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)
- Higher-order structural theorems (Theorem 5 = no-variational, source for normalization-principle gap): [`HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md`](HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md)
- Three-generation observable: [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- MINIMAL_AXIOMS: `MINIMAL_AXIOMS_2026-05-03.md`

## Validation

```bash
python3 scripts/cl3_koide_a1_probe_z2_c3_pairing_2026_05_08_probe7.py
```

Expected output: structural verification of (i) baseline circulant /
C_3 primitives (Section 0), (ii) per-candidate Z_2 fate (Sections 1-5),
(iii) universal scale-invariance barrier (Section 6), (iv) Z_6 = Z_2 ×
C_3 representation theory (Section 7), (v) C_3-multiplicity reframing of
1/2 (Section 8), (vi) convention robustness (Section 9), (vii)
falsifiability anchor (Section 10), (viii) bounded-obstruction theorem
statement (Section 11). Total: 70 PASS / 0 FAIL.

Cached: [`logs/runner-cache/cl3_koide_a1_probe_z2_c3_pairing_2026_05_08_probe7.txt`](../logs/runner-cache/cl3_koide_a1_probe_z2_c3_pairing_2026_05_08_probe7.txt)

## User-memory feedback rules respected

- `feedback_consistency_vs_derivation_below_w2.md`: this note applies
  the "consistency equality is not derivation" rule to the Survey-2
  Z_2-pairing framing. The C_3-multiplicity reframing of 1/2 = 3/6 is
  a CONSISTENCY identity (a fact about `M_3(ℂ)_Herm` decomposition);
  the SELECTION of equipartition between the two character sectors is
  the genuine open question.
- `feedback_hostile_review_semantics.md`: stress-tested the
  semantic claim "Z_2 paired with C_3 forces 1/2" by enumerating
  five Z_2 candidates with explicit per-candidate algebraic action
  and verifying that no candidate's Z_2-equivariance produces the
  required quadratic constraint.
- `feedback_retained_tier_purity_and_package_wiring.md`: no automatic
  cross-tier promotion. This note is a bounded obstruction; the
  parent A1 admission remains at its prior bounded status.
- `feedback_physics_loop_corollary_churn.md`: the five-candidate
  enumeration with distinct algebraic fates and the C_3-multiplicity
  reframing are substantive new structural content, not relabelings.
- `feedback_compute_speed_not_human_timelines.md`: alternative routes
  characterized in terms of WHAT additional content would be needed
  (non-linear Z_2 action, normalization principle, A3-class admission),
  not how-long-they-would-take.
- `feedback_special_forces_seven_agent_pattern.md`: this note packages
  a multi-angle attack (five candidate Z_2's + universal barrier) on a
  single load-bearing structural lemma, with sharp PASS/FAIL
  deliverables in the runner.
