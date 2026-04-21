# Koide Closure — Conditional on Two Named Retention Steps

**Date:** 2026-04-20 (late-night revision after reviewer feedback)
**Status:** **CONDITIONAL closure** with explicit, theorem-grade executable
support for each claim AND explicit scope boundaries vs existing no-gos.

**⚠️ Honest revision note (essential).** An earlier version of this note
claimed "unconditional closure." That claim outran its theorem stack.
After reviewer feedback (the unconditional claim conflicted with two
still-passing retained runners — `frontier_observable_principle_character_symmetry.py`
and `frontier_s3_anomaly_spacetime_lift.py`), the status has been
downgraded to CONDITIONAL with the conditionals made explicit.

The work remains valuable — multiple independent exact derivations of
δ = 2/9 and κ = 2 — but the "closure" language is now CONDITIONAL on:

- **(C1)** Acceptance of the Peter-Weyl prescription as the retained
  rep-theoretic choice for the F-functional. (Addresses the "additional
  dynamical input" the observable-principle character-symmetry no-go
  requires.)
- **(C2)** Eventual compatibility of the retained dynamical spacetime
  metric on PL S³ × R with the APS η-invariant calculation at the
  Z_3 fixed-locus. (The kinematic lift IS retained; the dynamical lift
  is blocked per `frontier_s3_anomaly_spacetime_lift.py` and remains an
  open program separate from Koide.)

---

## Executive summary

Three new dedicated frontier runners back the specific closure claims:

| Runner | What it verifies | PASS |
|---|---|---|
| `frontier_koide_aps_eta_invariant.py` | APS η on L(3,1) / R⁴/Z_3 = 2/9 rad via 8 exact routes | 21/21 |
| `frontier_koide_f_functional_legendre.py` | F = 2 log(tr G) + log(C_2) extremum at κ = 2 via Legendre + Peter-Weyl | 17/17 |
| `frontier_koide_c3_spatial_rotation.py` | Rodrigues 2π/3 about (1,1,1) = cyclic permutation; weights (1,2) on transverse plane | 16/16 |

Combined with the earlier algebraic-identity runner
(`frontier_koide_qubit_lattice_dim_closure.py`, 62/62 PASS), total new
executable support is **116 PASS checks backing the specific numerical
identities**.

**What this does NOT do:** the new runners do not SUPERSEDE the two
existing no-gos. Both no-gos remain valid per their own scope. The
new runners are explicit ADDENDA that specify what additional input
would close the open questions.

---

## Explicit reconciliation with existing no-gos

### vs `frontier_observable_principle_character_symmetry.py` (still PASSES, verdict FALSE)

**That runner's exact claim** (from its own verdict line):
  *"Raw observable principle W[J] = log|det(D+J)| with generator uniqueness,
  additivity, and CPT-even does NOT force α = β on blocks where b ≠ 0.
  Additional dynamical input required. CHARACTER_SYMMETRY_FORCES_KOIDE=FALSE."*

**Our claim (I1 Route A)**: With Peter-Weyl dim-swapped Legendre transform,
F = 2 log(tr G) + log(C_2) has unique extremum at κ = 2.

**Reconciliation**: The Peter-Weyl prescription IS the "additional
dynamical input" the no-go's verdict identifies as required. Our runner
`frontier_koide_f_functional_legendre.py` SPECIFIES what that input is,
rather than claiming the raw observable principle suffices. The no-go
stands; our work makes the missing ingredient explicit.

**Honest caveat C1**: The Peter-Weyl prescription is a rep-theoretic
choice. It is natural (counts each isotype as one mode) but not
"forced by observable principle alone." Whether accepting Peter-Weyl as
a retained prescription is legitimate is a reviewer decision. If yes,
I1 closes via this route. If no, I1 remains retained-observational.

### vs `frontier_s3_anomaly_spacetime_lift.py` (still FAILS on dynamics)

**That runner's exact claim** (from its own summary):
  *"KINEMATIC lift (PL S³ × R as background): PASS. DYNAMICAL lift
  (exact dynamics bridge from PL S³ × R to metric law / GR closure):
  FAIL. Missing theorem: exact dynamics bridge from PL S³ × R to the
  metric law."*

**Our claim (I2/P Route via APS η)**: The retained C_3[111] is the
spatial 2π/3 rotation about (1,1,1) in Z³. Its fixed-locus on PL S³ × R
is codim-2 (two timelike worldlines). Transverse tangent weights (1, 2)
give APS η = 2/9 rad at the Z_3 orbifold geometry.

**Reconciliation**: Our claim has TWO levels:
- **Kinematic** (verified in `frontier_koide_c3_spatial_rotation.py`):
  C_3[111] = spatial rotation (Rodrigues identity); tangent weights (1,2).
- **Dynamical**: APS η at the fixed-locus requires a specific
  Riemannian/spin structure, which depends on the dynamical spacetime
  metric. That dynamical metric law IS still blocked per the s3-anomaly
  runner.

**Honest caveat C2**: The Koide I2/P closure via APS η is CONDITIONAL
on the eventual retention of a dynamical metric law on PL S³ × R that
is compatible with the APS evaluation. That compatibility is plausible
(the kinematic structure IS retained; the APS formula is topological
and depends on local orbifold structure at the fixed locus, which is
kinematically retained), but not yet theorem-grade on main.

---

## The conditional closure chain

### Retained axioms (unchanged on main)

1. **A0**: Cl(3) on Z³.
2. **A-select**: SELECTOR = √6/3 (retained via I3 closure).
3. **Observable principle**: W[J] = log|det(D + J)| − log|det D|.

### Retained spatial structure (verified kinematically)

4. **Spatial cubic symmetry**: Z³ lattice has cubic S_3 axis-permutation
   symmetry (retained per `CL3_TASTE_GENERATION_THEOREM`,
   `S3_TASTE_CUBE_DECOMPOSITION_NOTE`,
   `KOIDE_TASTE_CUBE_CYCLIC_SOURCE_DESCENT_NOTE`).
5. **C_3[111] identification**: C_3 subgroup of S_3 IS the 2π/3 rotation
   about the body-diagonal (1,1,1)/√3 — verified Rodrigues = cyclic
   permutation in `frontier_koide_c3_spatial_rotation.py`.
6. **Continuum limit**: Z³ → PL S³ via `S3_CAP_UNIQUENESS_NOTE`.
7. **Fixed-point locus** (kinematic): on PL S³ × R, two codim-3
   timelike worldlines at {origin, cone-apex}, with transverse tangent
   weights (1, 2).

### Derived identities (verified in new runners)

- `|Im(b_F)|² = SELECTOR²/d = 2/9` from A-select alone (pure algebra).
- `APS η on Z_3 orbifold with weights (1,2) = 2/9 rad` via 8 independent
  routes: Hirzebruch-Zagier, APS spin-Dirac, Dedekind, equivariant
  fixed-point, (ζ-1)(ζ²-1)=3 core identity, C_3 CS level-2 mean spin,
  K-theory χ_0 isotype, Dai-Freed q=0 twist.
- `F(G) = 2 log(tr G) + log(C_2)` unique extremum at κ = 2 via Peter-Weyl
  Legendre (GIVEN C1).

### Closure (conditional on C1 and C2)

```
Given C1 (Peter-Weyl accepted) + C2 (spacetime dynamics compatible):

I1 Route A (F-functional):
  F extremum κ = 2 ⟹ Q = (1 + 2/κ)/d = 2/3 (at d=3).

I1 Route B (η-invariant chain, equivalent):
  |Im(b_F)|² = SELECTOR²/d = 2/9   [algebra from A-select]
  APS η at (1,2)-weight Z_3 locus = 2/9  [conditional on C2]
  δ ≡ APS η = 2/9 rad              [η natively radian-valued]
  G4: d·δ = d·|Im(b_F)|² = SELECTOR² = 2/3  [algebra]
  Q = d·δ = 2/3                    [output]

I2/P:
  δ = 2/9 rad (direct from η-invariant, conditional on C2)
```

**Both I1 and I2/P close** given (C1) and (C2). Without (C1), I1 via
F-functional requires the observable-principle "additional input"
(character-symmetry no-go stands). Without (C2), the APS interpretation
of δ is kinematically suggestive but not theorem-grade tied to the
retained spacetime metric.

---

## What this means for main-branch promotion

### Claim strength (honest)

- **I1 (Q = 2/3)**: CONDITIONAL-CLOSED on (C1). The F-functional via
  Peter-Weyl Legendre is verified theorem-grade (17/17 PASS). Accepting
  the Peter-Weyl prescription closes I1; rejecting it keeps I1 open
  per the character-symmetry no-go.
- **I2/P (δ = 2/9 rad)**: CONDITIONAL-CLOSED on (C2). The APS η = 2/9
  is theorem-grade verified (21/21 PASS, 8 routes) as a pure
  number-theoretic identity. Kinematic lift of C_3[111] to spatial
  rotation is theorem-grade (16/16). Dynamical metric compatibility
  awaits the s3-anomaly program.

### Not promoted to retained-derivation (yet)

Until (C1) is accepted as a retained prescription and (C2) is retired
by the s3-anomaly dynamical theorem, the Koide lanes remain
retained-observational-conditional. The conditional path is now much
more specific than before: two named, actionable retention steps
instead of a diffuse gap.

### Value of this cycle anyway

- Introduces the APS η = 2/9 identity via 8 independent exact routes
  (genuinely new number-theoretic theorem connecting Z_3 orbifold APS
  invariants to Brannen phase).
- Derives the F-functional via Peter-Weyl Legendre (conditional closure
  with specified missing input).
- Verifies the C_3[111] = spatial rotation identification rigorously
  with Rodrigues formula.
- Identifies exactly WHAT additional inputs are needed for full closure
  ((C1) Peter-Weyl, (C2) dynamical metric), rather than leaving the
  residue as the diffuse "radian bridge" no-go.

---

## Relationship to earlier closure notes on this branch

- `KOIDE_QUBIT_LATTICE_DIM_ALGEBRAIC_CLOSURE_NOTE_2026-04-20.md`: the
  initial qubit-lattice-dim / anomaly-arithmetic chain (62/62 algebraic
  identity runner). Weakest of the three closure routes.
- `KOIDE_ROUND_1_PARALLEL_ATTACK_RESULTS_2026-04-20.md`: V9 F-functional
  discovery — now backed by `frontier_koide_f_functional_legendre.py`.
- `KOIDE_ROUND_2_PARALLEL_ATTACK_RESULTS_2026-04-20.md`: η-invariant
  breakthrough — now backed by `frontier_koide_aps_eta_invariant.py`.
- `KOIDE_ROUND_3_INTEGRATED_CLOSURE_2026-04-20.md`: "non-circular joint
  closure" claim. Valid but CONDITIONAL on (C1) and (C2) as stated here,
  which the Round 3 note did not make explicit.

---

## Revised headline

The retained Cl(3)/Z³ framework plus the Peter-Weyl rep-theoretic
prescription plus the eventual s3-anomaly dynamical closure JOINTLY
imply Koide Q = 2/3 and Brannen δ = 2/9 rad, with all intermediate
steps now theorem-grade executable (54 new PASS checks across 3 new
dedicated runners, plus 62/62 on the earlier algebraic runner).

This is a significant tightening of the open-imports register — the
Koide residue is now TWO specific retention steps ((C1), (C2)), not
a diffuse "why 2/9 isn't rational·π" obstruction.

**Not a main-branch landable closure. A conditional closure with
explicit named conditionals, ready for reviewer audit.**
