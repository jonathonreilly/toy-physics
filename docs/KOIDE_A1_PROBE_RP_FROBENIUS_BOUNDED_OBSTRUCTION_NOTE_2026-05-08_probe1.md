# Koide A1 Probe — RP + GNS → Frobenius Pairing Bounded Obstruction

**Date:** 2026-05-08
**Type:** bounded_theorem (sharpened obstruction; no positive closure)
**Claim type:** bounded_theorem
**Scope:** review-loop source-note proposal — RP+GNS probe of the
canonical-Frobenius-pairing route to closing the A1 √2 equipartition
admission on the charged-lepton Koide lane.
**Status:** source-note proposal for a negative probe-1 closure —
shows that retained reflection positivity (RP) plus the implicit
Gel'fand–Naimark–Segal (GNS) construction in OS reconstruction
cannot, by themselves, force the multiplicity-weighted (1,1)
Frobenius pairing as canonical on `M_3(C)`-acting-on-hw=1. Five
independent structural barriers each block the proposed chain. The
A1 admission count is UNCHANGED.
**Authority role:** source-note proposal — audit verdict and
downstream status set only by the independent audit lane.
**Loop:** koide-a1-probe-rp-frobenius-20260508
**Primary runner:** [`scripts/cl3_koide_a1_probe_rp_frobenius_2026_05_08_probe1.py`](../scripts/cl3_koide_a1_probe_rp_frobenius_2026_05_08_probe1.py)
**Cache:** [`logs/runner-cache/cl3_koide_a1_probe_rp_frobenius_2026_05_08_probe1.txt`](../logs/runner-cache/cl3_koide_a1_probe_rp_frobenius_2026_05_08_probe1.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived status is generated
only after the independent audit lane reviews the claim, dependency
chain, and runner. The `claim_type`, scope, named admissions, and
bounded-obstruction classification are author-proposed; the audit
lane has full authority to retag, narrow, or reject the proposal.

## Question

Four prior closure routes for the A1 amplitude-ratio admission
`|b|²/a² = 1/2` (on circulant Hermitians `H = aI + bC + b̄C²` on
hw=1 ≅ ℂ³) all hit the same structural meta-pattern:

| Route | Specific barrier | Underlying meta-pattern |
|---|---|---|
| F (Casimir-difference `T(T+1) − Y² = 1/2`) | `Y²` convention dependence + sector orthogonality | normalization not fixed |
| E (Kostant `\|ρ_{A_1}\|² = 1/2`) | Cartan–Killing `\|α\|²` convention | normalization not fixed |
| A (Koide–Nishiura U(3) quartic) | Wilson-coefficient circularity | normalization not fixed |
| D (Newton–Girard polynomial) | weight-class `(1,1)` vs `(1,2)` ambiguity | normalization not fixed |

The shared meta-trap is that the framework's retained content does
not fix a *canonical normalization* on the relevant operator algebra.

This probe asks whether the framework already has the
canonical-normalization fixer hiding in retained
[`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md)
plus the implicit GNS construction in OS reconstruction:

> Hypothesis (probe 1): RP + GNS together force the multiplicity-
> weighted (1,1) Frobenius pairing on `M_3(C)`-acting-on-hw=1, which
> would propagate to fix `|b|²/a² = 1/2` and dissolve Route D's
> weight-class ambiguity.

This is structurally analogous to how
`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`
extended retained anomaly cancellation to fix SM hypercharges
(pure derivation, no new primitives).

**Question:** Can retained RP + GNS (without new axioms) force the
(1,1) Frobenius pairing on hw=1, and through that force `|b|²/a² = 1/2`?

## Answer

**No.** The hypothesis fails on five independent structural barriers
(each verified numerically in the paired runner with explicit
counterexamples). RP gives a positive sesquilinear form
`G(F, F') = ⟨Θ(F)·F'⟩` on the algebra of polynomial observables, and
the GNS quotient produces `H_phys = A_+ / Null(G)`. But this form,
restricted to the `M_3(C)`-on-hw=1 subalgebra, depends on a chain of
choices (vacuum reduction, reduction-map prescription, log-functional
selection) that retained content does not fix.

**Verdict: STRUCTURAL OBSTRUCTION (bounded_obstruction).** Same
meta-pattern as Routes F/E/A/D: a normalization is needed and is not
supplied by retained content. The probe also identifies one **new**
barrier not present in the prior four — vacuum-state freedom in the
GNS construction — which makes RP/GNS a strictly worse (more
underdetermined) candidate than the four prior routes.

The five barriers (each verified numerically):

1. **Vacuum-state freedom under C_3 invariance.** The GNS inner
   product is `⟨A, B⟩_GNS = Tr(ρ_Ω · B^† A)`, where `ρ_Ω` is the
   reduced density matrix of the RP vacuum on hw=1. C_3-invariance
   forces `ρ_Ω` diagonal in the C_3-character basis, but does NOT
   force `ρ_Ω = I/3` (tracial). Different `ρ_Ω` (e.g., `(0.6, 0.2,
   0.2)`, `(0.2, 0.6, 0.2)`, `(0.1, 0.45, 0.45)`) give different
   GNS-equipartition `|b|/a` values; the runner shows only the
   tracial choice recovers `|b|/a = 1/√2` (the A1 condition).

2. **Yukawa–vacuum circularity.** The vacuum `|Ω⟩` is selected by
   the FULL action `S = S_gauge + S_Yukawa(Y_e)`, where `Y_e` is the
   3×3 charged-lepton Yukawa matrix whose generation-space structure
   is precisely `(a, b)`. So the GNS metric depends on `Y_e`, and
   we are trying to derive `(a, b)` from a metric that DEPENDS ON
   `(a, b)`. This is the same selector-circularity that blocked
   Route A (Wilson-coefficient circularity).

3. **Inner-product vs log-functional choice.** Even granting tracial
   `ρ_Ω = I/3`, the GNS inner product is a *scalar multiple* of
   the Frobenius pairing: `⟨A, B⟩_GNS = (1/3) ⟨A, B⟩_Frobenius`.
   The (1,1) multiplicity weight is preserved at the inner-product
   level. But the open residue from
   [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)
   §4 is a choice of LOG-FUNCTIONAL (extremal principle):
       block-total `log E_+ + log E_perp` → `kappa = 2` (A1)
       det `log E_+ + 2 log E_perp`       → `kappa = 1` (NOT A1)
   Both are natural functionals on the Frobenius geometry. The GNS
   inner product alone does NOT select between them.

4. **Spatial-vs-flavor sector orthogonality (reduction map).** RP is
   defined on path integrals over the FULL spatial Z³ lattice with
   temporal reflection. The hw=1 sector is a momentum-space restriction
   (BZ corners) on which `M_3(C)` acts as a flavor-like generation
   algebra. The RP form on field polynomials does not directly induce
   a unique inner product on the abstract `M_3(C)`; it depends on a
   CHOICE of reduction map (momentum-projection + tracing out non-hw=1
   modes), and different reduction maps give different effective
   metrics on `M_3(C)` (and can break C_3-equivariance).

5. **Cyclicity is not metric-pinning.** Retained
   [`AXIOM_FIRST_REEH_SCHLIEDER_THEOREM_NOTE_2026-05-01.md`](AXIOM_FIRST_REEH_SCHLIEDER_THEOREM_NOTE_2026-05-01.md)
   states the vacuum is cyclic-and-separating for any `A(O)`. But
   cyclicity is a TOPOLOGICAL property (density of `A(O)|Ω⟩`); it
   does NOT pin the metric on `A(O)`. Different cyclic vacua for
   `M_3(C)` on `ℂ³` (e.g., `(1,1,1)/√3` vs `(1,0,0)` vs
   `(1, 0.5, 0.5)/norm`) give different GNS norms.

The combined picture: **the chain [RP + GNS → canonical Frobenius
pairing on hw=1 → A1] cannot be forced from retained content.** RP/GNS
produces a sesquilinear form on field polynomials, but its restriction
to the M_3(C)-on-hw=1 subalgebra requires (a) a vacuum, (b) a
reduction map, and (c) a log-functional, none of which are pinned
by retained content. This is the same shape of obstruction as
Routes F/E/A/D, with the additional novel barrier of vacuum-state
freedom.

## Setup

### Premises (A_min for probe 1)

| ID | Statement | Class |
|---|---|---|
| A1 | Cl(3) local algebra | framework axiom; see `MINIMAL_AXIOMS_2026-05-03.md` |
| A2 | Z³ spatial substrate | framework axiom; same source |
| RP | Reflection positivity → sesquilinear `G(F, F') = ⟨Θ(F)·F'⟩` ≥ 0; `H_phys = A_+/Null(G)` | retained: [`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md) |
| RS | Reeh–Schlieder cyclicity-and-separating vacuum | retained: [`AXIOM_FIRST_REEH_SCHLIEDER_THEOREM_NOTE_2026-05-01.md`](AXIOM_FIRST_REEH_SCHLIEDER_THEOREM_NOTE_2026-05-01.md) |
| 3GenObs | hw=1 BZ-corner triplet has `M_3(C)` algebra; `C_3[111]` cycle | retained-bounded: [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md) |
| Circulant | C_3-equivariant Hermitian on hw=1 is `aI + bC + b̄C²` | retained: [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md) |
| BlockTotalFrob | Block-total Frobenius measure realizes (1,1) weights, kappa=2 at extremum | retained: [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md) |
| MRU | Weight-class theorem: kappa = 2μ/ν; (1,1) → kappa=2; (1,2) → kappa=1 | retained: [`KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md) |
| MRUDemot | MRU SO(2)-quotient is not derivable from retained observable principle | retained: [`KOIDE_MRU_DEMOTION_NOTE_2026-04-20.md`](KOIDE_MRU_DEMOTION_NOTE_2026-04-20.md) |
| KoideAlg | Koide Q = 2/3 ⟺ a₀² = 2|z|² ⟺ |b|²/a² = 1/2 | retained: [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md) |
| Substep4 | AC_φλ remains the explicit identification residual on hw=1 | retained-bounded: [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md) |
| RouteF | Route F is structurally barred (4 barriers) | retained: [`KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md`](KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md) |
| FreeYukawa | Y_e is arbitrary 3×3 (gauge-allowed); circulant under C_3, with (a,b) free | retained: [`CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md`](CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md) |

### Forbidden imports

- NO PDG observed mass values used as derivation input (anchor-only at
  end, clearly marked per
  [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md))
- NO lattice MC empirical measurements
- NO fitted matching coefficients
- NO same-surface family arguments
- **NO new axioms** (probe-1's promise was axiom-native; any A3-class
  admission requires explicit user approval and is not proposed here)
- NO admitted SM Yukawa-coupling pattern as derivation input

## The structural lemma at issue

**Probe-1 hypothesis:**

> Retained RP + GNS together force the multiplicity-weighted (1,1)
> Frobenius pairing on `M_3(C)`-acting-on-hw=1, which propagates to
> fix `|b|²/a² = 1/2` (A1).

**Required chain of derivations:**

1. RP gives positive sesquilinear `G` on field polynomials. ✓ (retained)
2. GNS quotient yields `H_phys` with cyclic vacuum `|Ω⟩`. ✓ (retained, via OS reconstruction)
3. Reduction to hw=1: vacuum induces a reduced density matrix
   `ρ_Ω` on hw=1.
4. Restriction to M_3(C): the GNS inner product on operators in
   M_3(C) is `⟨A, B⟩_GNS = Tr(ρ_Ω B^† A)`.
5. Pin `ρ_Ω` to tracial `I/3`.
6. Conclude `⟨A, B⟩_GNS = (1/3) ⟨A, B⟩_Frobenius`, i.e. (1,1)
   multiplicity weighting up to scalar.
7. Choose log-functional (block-total vs det): use block-total.
8. Conclude kappa = 2, i.e. `|b|²/a² = 1/2` (A1).

**Steps 3, 5, 7 each fail on retained content alone**, and Step 4
inherits ambiguity from Step 3's reduction-map choice. This note
demonstrates each failure with explicit counterexamples in the
runner.

## Theorem (probe-1 bounded obstruction)

**Theorem.** On A1+A2 + retained RP + retained Reeh–Schlieder +
retained C_3-equivariance + retained KoideCone-algebraic-equivalence
+ retained Block-Total-Frobenius (at the (1,1) leaf, conditional on
log-functional choice) + admissible standard math machinery:

```
The probe-1 hypothesis "RP+GNS forces canonical (1,1) Frobenius
pairing on M_3(C)-on-hw=1, hence A1" cannot be derived from retained
Cl(3)/Z³ content alone. Five independent structural barriers each
block the proposed chain:

  (B1) Vacuum-state freedom: rho_Omega is not pinned to tracial.
  (B2) Yukawa–vacuum circularity: rho_Omega depends on (a,b) we want
       to derive.
  (B3) Log-functional choice: (1,1) vs (1,2) extremal principle is
       not selected by the inner product alone.
  (B4) Reduction-map ambiguity: RP form on field polynomials does
       not uniquely induce an inner product on abstract M_3(C).
  (B5) Cyclicity is not metric-pinning: density of A(O)|Omega> does
       not select a metric.

Therefore probe-1 closure of A1 is structurally barred under the
stated retained-content surface. The A1 admission count is unchanged.
```

**Proof.** Each barrier is verified independently in the paired
runner with explicit numerical counterexamples; combining them
establishes that no derivation chain from retained content reaches
`|b|²/a² = 1/2` via the RP+GNS route.

### Barrier 1: Vacuum-state freedom under C_3 invariance

The GNS construction associates to a state `ω` (here, the path-
integral vacuum `|Ω⟩`) the inner product

```
⟨A, B⟩_GNS = ω(B^† A) = Tr(ρ_ω · B^† · A)
```

on operators, where `ρ_ω` is the density matrix representing `ω`
restricted to the relevant operator subalgebra (here, `M_3(C)` on
hw=1).

**Claim.** Under retained C_3-invariance of the framework, `ρ_Ω` is
forced to be **diagonal in the C_3-character basis**, but is NOT
forced to be **tracial** (`I/3`).

**Demonstration.** Let `e_+ = (1,1,1)/√3`, `e_ω = (1, ω, ω²)/√3`,
`e_{ω²} = (1, ω², ω)/√3` be the C_3-character basis vectors. The
runner verifies:

- `C e_+ = e_+`, `C e_ω = ω · e_ω`, `C e_{ω²} = ω² · e_{ω²}` (T1.1–1.3).
- The diagonal density matrix
  `ρ(p_+, p_ω, p_{ω²}) = p_+ · |e_+⟩⟨e_+| + p_ω · |e_ω⟩⟨e_ω| + p_{ω²} · |e_{ω²}⟩⟨e_{ω²}|`
  is C_3-invariant for ANY `(p_+, p_ω, p_{ω²}) ≥ 0` with sum 1 (T1.4–1.7).
- At the A1 point `H = I + (1/√2)·(C + C²)`, the GNS-equipartition
  ratio `E_+/E_perp` under tracial is exactly 1 (T1.8), but under
  skewed states `(0.6, 0.2, 0.2)`, `(0.2, 0.6, 0.2)`, `(0.1, 0.45,
  0.45)` it deviates by 0.29, 0.25, 0.54 respectively from 1 (T1.9–1.11).
- The `|b|/a` value at GNS-equipartition is `1/√2 ≈ 0.7071` under
  tracial (T1.12), but `0.5982` and `0.7912` under skewed states
  (T1.13). So the "A1 condition under GNS" is state-dependent.

**Consequence.** The GNS inner product, hence the implicit weighting
of the trivial vs doublet sectors, depends on the choice of `ρ_Ω`.
Retained content does not select tracial.

### Barrier 2: Yukawa–vacuum circularity

The vacuum `|Ω⟩` (and hence its reduction `ρ_Ω` to hw=1) is selected
by the FULL Euclidean action

```
S = S_gauge + S_fermion_kinetic + S_Yukawa(Y_e) + ...
```

The Yukawa term `S_Yukawa(Y_e)` contains the charged-lepton Yukawa
matrix `Y_e`, whose generation-space coefficient structure is
parametrized by `(a, b)` (the very coefficients we want to derive).

**Demonstration.** The runner uses a mock Yukawa-vacuum

```
ρ(a, b) ∝ exp(-β · H(a,b)^† · H(a,b)) / Z
```

(structural mock; we use it only to demonstrate that different `(a,b)`
give different `ρ`). It verifies:

- `ρ(a=1, b=0.3)`, `ρ(a=1, b=1/√2)`, `ρ(a=1, b=1)` are all valid
  density matrices (Hermitian, trace 1, eigenvalues ≥ 0) (T2.1–2.3).
- `‖ρ(a=1, b=0.3) − ρ(a=1, b=1/√2)‖_F = 0.0707` (T2.4).
- `‖ρ(a=1, b=0.3) − ρ(a=1, b=1)‖_F = 0.0726` (T2.4).
- Different `(a,b)` give different vacuum reductions (T2.5).

**Consequence.** The GNS metric on M_3(C)-on-hw=1 depends on `Y_e`,
which depends on `(a, b)`. To use the GNS metric to *derive* `(a, b)`
is selector-circularity — the same trap that blocked Route A
(Wilson-coefficient circularity).

### Barrier 3: Inner-product vs log-functional choice

Even granting tracial `ρ_Ω = I/3` (which is itself unsupported per
B1), the GNS inner product becomes

```
⟨A, B⟩_GNS = Tr((I/3) · B^† A) = (1/3) Tr(B^† A) = (1/3) · ⟨A, B⟩_Frobenius
```

The (1,1) multiplicity weighting is preserved at the inner-product
level (up to the overall scalar 1/3) (T3.1).

But the open residue from
[`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)
§4 is a choice of LOG-FUNCTIONAL (extremal principle) on the same
Frobenius geometry. Two natural functionals exist:

```
S_block(H) = log E_+ + log E_perp        (1,1 weights — kappa=2 at extremum)
S_det(H)   = log E_+ + 2 log E_perp      (1,2 weights — kappa=1 at extremum)
```

The runner verifies (T3.2–3.4):

- Block-total log-law extremum: `kappa = 2.0098` (target A1: 2.0).
- Det log-law extremum: `kappa = 1.0040` (target: 1.0).
- Difference: 0.99 (substantial separation).

**Consequence.** The GNS inner product alone does NOT select between
the (1,1) and (1,2) log-laws. Both are natural functionals on the
Frobenius geometry; selecting block-total is an additional structural
choice not pinned by RP+GNS.

### Barrier 4: Reduction-map ambiguity

RP is defined on path integrals over the FULL spatial Z³ lattice
with temporal reflection. The hw=1 sector is a momentum-space
restriction (BZ corners), and `M_3(C)` acts on the three corners as
a flavor-like generation algebra (per
[`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)).
The RP sesquilinear form on field polynomials does not directly
induce a unique inner product on the abstract `M_3(C)`; it depends
on a CHOICE of reduction map.

**Demonstration.** The runner exhibits two reduction maps:

- Map A: identity on M_3(C) (treat M_3(C) directly).
- Map B: modular twist (conjugation by `D = diag(1, √2, √3)`).

Under these:

- `‖H‖²_A = 4.5000` vs `‖H‖²_B = 5.0000` for `H = I + 0.5(C + C²)` (T4.1).
- Map B's image is NOT circulant under the standard `C` (breaks
  C_3-equivariance) (T4.2).

**Consequence.** The choice of reduction map is unconstrained by RP
on field polynomials (T4.3). Different maps give different effective
metrics on `M_3(C)`. Selecting "the canonical reduction" is an
additional structural choice not supplied by retained content.

### Barrier 5: Cyclicity is not metric-pinning

Retained
[`AXIOM_FIRST_REEH_SCHLIEDER_THEOREM_NOTE_2026-05-01.md`](AXIOM_FIRST_REEH_SCHLIEDER_THEOREM_NOTE_2026-05-01.md)
states that the vacuum `|Ω⟩` is cyclic-and-separating for any local
algebra `A(O)`. But cyclicity is a TOPOLOGICAL property — density of
`A(O)|Ω⟩` in `H_phys` — not a METRIC property.

**Demonstration.** Different cyclic vectors for `M_3(C)` on `ℂ³`
give different GNS norms. The runner exhibits three cyclic vacua:

- `v_1 = (1,1,1)/√3` (symmetric): `⟨H, H⟩_{v_1} = 4.5000`
- `v_2 = (1,0,0)` (corner): `⟨H, H⟩_{v_2} = 1.5000`
- `v_3 = (1, 0.5, 0.5)/norm` (skewed): `⟨H, H⟩_{v_3} = 3.5833`

(T5.4) for `H = I + 0.5(C + C²)`. All three are cyclic for `M_3(C)`
on `ℂ³` (any nonzero vector is cyclic for the full matrix algebra)
(T5.1–5.3).

**Consequence.** Cyclicity is preserved across all three vacua, but
the induced GNS norms differ substantially. The Reeh–Schlieder
theorem alone does not select a unique metric on `A(O)`.

## Why the (1,1) Frobenius pairing is not forced by RP+GNS

The chain of required derivations:

```
RP form on field polynomials (retained ✓)
    ↓
GNS quotient gives H_phys with vacuum |Ω⟩ (retained ✓)
    ↓
Reduce |Ω⟩ to hw=1: ρ_Ω = ?       — Barrier 4 (reduction map choice)
    ↓
Restrict to M_3(C): ⟨A, B⟩_GNS = Tr(ρ_Ω B^†A)
    ↓
ρ_Ω = I/3 (tracial)?              — Barrier 1 (vacuum freedom)
    ↓                              — Barrier 5 (cyclicity not enough)
ρ_Ω depends on Y_e?                — Barrier 2 (circularity)
    ↓
GNS = (1/3) Frobenius (granted ρ_Ω tracial)
    ↓
Choose extremal log-functional     — Barrier 3 (block vs det)
    ↓
Conclude kappa = 2 → A1
```

Every transition labeled "Barrier" requires an additional structural
input not supplied by retained content. The chain breaks at multiple
independent points — even fixing one barrier does not unlock the next.
The probe-1 hypothesis fails comprehensively.

## Comparison to Routes F/E/A/D

| Route | Specific obstruction | Meta-pattern | Barriers |
|---|---|---|---|
| F (Casimir-difference) | Y² convention dep; sector orthogonality | Normalization not fixed | 4 |
| E (Kostant Weyl-vector) | Cartan–Killing convention | Normalization not fixed | 3 |
| A (Koide–Nishiura U(3) quartic) | Wilson-coefficient circularity | Normalization not fixed (squaring trap) | 4 |
| D (Newton–Girard polynomial) | (1,1) vs (1,2) weight-class | Normalization not fixed | 3 |
| **Probe 1 (RP+GNS)** | **Vacuum freedom + log-functional + reduction map + cyclicity ≠ metric + circularity** | **Normalization not fixed** | **5** |

**Probe 1 has the MOST barriers (5), not fewer.** The hoped-for
"RP+GNS supplies the canonical normalization fixer" hypothesis is
*more* underdetermined than the four prior routes, not less. The
reason: RP/GNS gives a positive form on field polynomials, but
restricting that form to a *finite-dimensional flavor algebra* (M_3(C)
on hw=1) requires additional structure (vacuum, reduction, log-law)
that the framework's general-purpose RP+GNS theorems do not address.

The hoped-for analogy with `STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`
(retained anomaly cancellation → SM hypercharge uniqueness) does not
hold because anomaly cancellation provides a discrete *constraint*
on a finite parameter space, while RP+GNS provides a positive
*sesquilinear form on a function space* — which becomes a metric on
the flavor algebra only after multiple intermediate choices.

## What this closes

- **Probe-1 negative closure** (bounded obstruction). Five independent
  structural barriers verified.
- **Sharpens the "RP+GNS is the canonical-normalization fixer"
  hypothesis**: prior status was open-conjectural; this note shows
  the hypothesis is structurally barred.
- **Identifies one new barrier** (vacuum-state freedom in GNS) not
  present in Routes F/E/A/D.
- **Confirms the meta-pattern**: all five routes hit the same
  "canonical normalization not fixed by retained content" trap.
- **Audit-defensibility**: explicit numerical counterexamples (skewed
  C_3-invariant density matrices, alternative cyclic vectors,
  alternative reduction maps, alternative log-functionals).

## What this does NOT close

- A1 admission count is unchanged. A1 remains a load-bearing
  non-axiom step on the Brannen circulant lane.
- Routes A (Koide–Nishiura quartic), D (Newton–Girard), E (Kostant
  Weyl-vector) remain bounded-obstructed candidates (per their
  obstruction notes). No new positive route to A1 is opened.
- Charged-lepton Koide closure remains a bounded observational-pin
  package (status from
  [`CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md`](CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md)
  unchanged).
- AC_φλ residual (substep 4) is unaffected.
- L3a trace-surface bounded obstruction status unchanged.
- The retained block-total Frobenius theorem
  ([`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md))
  retains its theorem status. This note does NOT retract that — it
  shows that the choice of block-total over det (the open residue
  flagged in §4 of that theorem) is NOT closed by RP+GNS.

## Empirical falsifiability

| Claim | Falsifier |
|---|---|
| Vacuum freedom (B1) | Demonstrate a retained theorem that forces ρ_Ω = I/3 on hw=1 from purely structural (non-Yukawa-dependent) input. |
| Yukawa circularity (B2) | Construct a vacuum-on-hw=1 prescription that does not depend on Y_e coefficients (a, b). |
| Log-functional choice (B3) | Derive a retained extremal principle that selects block-total over det log-law (e.g., free-energy minimization with explicit coefficient). |
| Reduction-map ambiguity (B4) | Supply a retained theorem that uniquely induces an inner product on M_3(C) from the RP form on field polynomials (e.g., a canonical momentum-projection map with retained-grade derivation). |
| Cyclicity ≠ metric (B5) | Show that combining cyclicity with another retained property (e.g., translation invariance, energy minimization) forces a unique metric. |
| Numerical match (anchor) | PDG anchor `Q ≈ 0.666661` matches `2/3` to sub-0.001%. The probe is consistent with the empirical anchor; falsification would require Q deviation from 2/3 in updated PDG. |

## Review boundary

This note proposes `claim_type: bounded_theorem` for the independent
audit lane. The bounded theorem is the negative probe-1 boundary: the
hypothesis "RP+GNS forces canonical (1,1) Frobenius pairing on
M_3(C)-on-hw=1, hence A1" is blocked by vacuum-state freedom,
Yukawa-vacuum circularity, log-functional choice, reduction-map
ambiguity, and cyclicity-not-metric-pinning unless additional
retained content (vacuum-fixing principle, reduction-map theorem,
extremal-principle selector) is supplied.

No new admissions are proposed. A1 remains unchanged at its prior
load-bearing non-axiom status on the Brannen circulant lane. The
independent audit lane may retag, narrow, or reject this proposal.

## Promotion-Value Gate (V1-V5)

| # | Question | Answer |
|---|---|---|
| V1 | Verdict-identified obstruction closed? | The "RP+GNS is the canonical-normalization fixer" hypothesis is sharpened from "open conjecture" to "structurally barred under retained content; needs vacuum-fixing + reduction-map + extremal-principle inputs." |
| V2 | New derivation? | The five-barrier obstruction argument applied to RP+GNS is new structural content. Prior status notes did not enumerate the GNS-vacuum freedom barrier (B1) or the cyclicity≠metric barrier (B5). |
| V3 | Audit lane could complete? | Yes — the audit lane can review (i) vacuum-state freedom, (ii) Yukawa-circularity, (iii) log-functional choice, (iv) reduction-map ambiguity, (v) cyclicity-not-metric, plus the five-barrier conjunction. |
| V4 | Marginal content non-trivial? | Yes — the vacuum-state-freedom finding (skewed C_3-invariant ρ giving non-tracial GNS metric, with explicit (a,b) deviation) is non-obvious from prior notes and directly challenges the probe-1 hypothesis. |
| V5 | One-step variant? | No — the five-barrier argument addresses a structurally NEW route (RP/GNS) not covered by prior Routes F/E/A/D. The barriers are specific to RP/GNS internals (vacuum, reduction map, GNS form), distinct from the prior routes' barriers. |

**Source-note V1-V5 screen: pass for bounded-obstruction audit
seeding.**

## Why this is not "corollary churn"

Per `feedback_physics_loop_corollary_churn.md`, the user-memory rule
is to avoid one-step relabelings of already-landed cycles. This note:

- Is NOT a relabel of prior Koide routes. The five-barrier obstruction
  argument applied to RP+GNS is new structural content with explicit
  numerical counterexamples for each barrier.
- Identifies a NEW barrier (B1 = vacuum-state freedom in GNS) not
  present in the prior 4 routes' obstruction notes.
- Sharpens the "RP+GNS could be the fixer" hypothesis from open-
  conjectural to closed-negatively, with a clear list of what would
  be required to reopen it.
- Provides explicit numerical counterexamples (skewed C_3-invariant
  density matrices with computed deviations from tracial GNS-
  equipartition) — these were not present in any prior Koide route
  discussion.
- Confirms the meta-pattern across now-five routes: framework's
  retained content does not fix a canonical normalization on the
  relevant operator algebra.

## Cross-references

- A1 derivation status (parent): `KOIDE_A1_DERIVATION_STATUS_NOTE.md`
- Route F obstruction (sister): [`KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md`](KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md)
- Retained RP: [`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md)
- Retained Reeh–Schlieder: [`AXIOM_FIRST_REEH_SCHLIEDER_THEOREM_NOTE_2026-05-01.md`](AXIOM_FIRST_REEH_SCHLIEDER_THEOREM_NOTE_2026-05-01.md)
- Retained block-total Frobenius theorem (the (1,1) leaf, conditional on log-functional choice): [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)
- MRU weight-class theorem (the formula `kappa = 2μ/ν`): [`KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md)
- MRU demotion: [`KOIDE_MRU_DEMOTION_NOTE_2026-04-20.md`](KOIDE_MRU_DEMOTION_NOTE_2026-04-20.md)
- Charged-lepton Koide-cone algebraic equivalence: [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)
- Three-generation observable: [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- Substep 4 AC narrowing: [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)
- One-Higgs gauge selection: [`SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md`](SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md)
- Direct Ward-free Yukawa no-go: [`CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md`](CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md)
- Circulant character derivation: [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
- MINIMAL_AXIOMS: `MINIMAL_AXIOMS_2026-05-03.md`

## Validation

```bash
python3 scripts/cl3_koide_a1_probe_rp_frobenius_2026_05_08_probe1.py
```

Expected output: structural verification of (i) C_3 setup sanity,
(ii) Barrier 1 vacuum-state freedom (skewed C_3-invariant density
matrices give non-tracial GNS metrics; A1 condition becomes
state-dependent), (iii) Barrier 2 Yukawa-vacuum circularity (mock
vacuum dependence on (a,b)), (iv) Barrier 3 log-functional choice
(block-total kappa=2 vs det kappa=1, both natural functionals),
(v) Barrier 4 reduction-map ambiguity (Map A vs Map B with C_3-
breaking), (vi) Barrier 5 cyclicity-not-metric (different cyclic
vacua give different GNS norms), (vii) meta-pattern verification
(prior 4 routes + this probe all hit canonical-normalization gap),
(viii) PDG anchor (anchor-only). Total: 41 PASS / 0 FAIL.

Cached: [`logs/runner-cache/cl3_koide_a1_probe_rp_frobenius_2026_05_08_probe1.txt`](../logs/runner-cache/cl3_koide_a1_probe_rp_frobenius_2026_05_08_probe1.txt)

## User-memory feedback rules respected

- `feedback_consistency_vs_derivation_below_w2.md`: this note
  specifically applies the "consistency equality is not derivation"
  rule. The fact that tracial-vacuum GNS gives kappa=2 (consistent
  with A1) is a consistency equality conditional on tracial; the
  underlying structural derivation (forcing tracial from retained
  content) is what fails.
- `feedback_hostile_review_semantics.md`: this note stress-tests the
  semantic claim "RP+GNS supplies canonical normalization on
  M_3(C)-on-hw=1" by showing that the action-level identification
  (sesquilinear form on field polynomials = inner product on flavor
  algebra) is not derivable — it requires a chain of intermediate
  choices that retained content does not supply.
- `feedback_retained_tier_purity_and_package_wiring.md`: no automatic
  cross-tier promotion. This note is a bounded obstruction; the
  parent A1 admission remains at its prior bounded status. No
  retained-tier promotion implied.
- `feedback_physics_loop_corollary_churn.md`: the five-barrier
  argument with explicit counterexamples (skewed C_3-invariant
  density matrices, alternative cyclic vectors, alternative
  reduction maps, alternative log-functionals) is substantive new
  structural content, not a relabel of any prior Koide route.
- `feedback_compute_speed_not_human_timelines.md`: alternative
  routes characterized in terms of WHAT additional content would be
  needed (vacuum-fixing principle, reduction-map theorem,
  extremal-principle selector), not how-long-they-would-take.
- `feedback_special_forces_seven_agent_pattern.md`: this note
  packages a multi-angle attack (five independent barriers) on a
  single load-bearing structural hypothesis, with sharp PASS/FAIL
  deliverables in the runner.
- `feedback_review_loop_source_only_policy.md`: this note is a
  source theorem note; the paired runner produces cached output;
  no output-packets, lane promotions, or synthesis notes are
  introduced.
