# Koide BAE Probe 28 — Full Cited Interacting Matter-Sector Dynamics: Bounded Obstruction

**Date:** 2026-05-09
**Type:** bounded_theorem (sharpened obstruction at the interacting-extension layer; no positive closure;
new positive content: F1 structurally rejected by retained INTERACTING dynamics, extending Probe 25's
free-Gaussian result to the full Yukawa + Higgs + gauge + Z_3-potential effective action)
**Claim type:** bounded_theorem
**Scope:** review-loop source-note proposal — Probe 28 of the Koide
**BAE-condition** closure campaign. Tests whether adding the **full
cited interaction terms** (Yukawa coupling per `CL3_SM_EMBEDDING_THEOREM`,
Higgs sector + Coleman-Weinberg radiative quartic per
`COMPLETE_PREDICTION_CHAIN_2026_04_15.md` Sec 7, gauge couplings via
the Wilson plaquette, Z_3 scalar potential per
`KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md`,
Probe 19 Yukawa-vertex factor) to Probe 25's free Gaussian dynamics
shifts the canonical extremization functional from F3 (real-dim
weighting (1, 2)) to F1 (multiplicity weighting (1, 1)) — selecting
BAE.
**Status:** source-note proposal for a sharpened bounded obstruction.
The cited interacting matter-sector dynamics canonically continues
to select **F3** (rank-weighted, multiplicity (1, 2)), NOT F1
(block-total, multiplicity (1, 1)). Eight independent retained-
interaction-extension routes converge on F3 (verified 75/0 by paired
runner). The Probe 25 conclusion extends to the interacting level: F1
is NOT realized by any cited dynamics, free or interacting. The
BAE admission count is UNCHANGED.
**Authority role:** source-note proposal — audit verdict and
downstream status set only by the independent audit lane.
**Loop:** koide-bae-probe28-interacting-dynamics-20260509
**Primary runner:** [`scripts/cl3_koide_bae_probe_interacting_dynamics_2026_05_09_probe28.py`](../scripts/cl3_koide_bae_probe_interacting_dynamics_2026_05_09_probe28.py)
**Cache:** [`logs/runner-cache/cl3_koide_bae_probe_interacting_dynamics_2026_05_09_probe28.txt`](../logs/runner-cache/cl3_koide_bae_probe_interacting_dynamics_2026_05_09_probe28.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived status is generated
only after the independent audit lane reviews the claim, dependency
chain, and runner. The `claim_type`, scope, named admissions, and
bounded-obstruction classification are author-proposed; the audit
lane has full authority to retag, narrow, or reject the proposal.

## Naming-collision warning

In this note:

- **"framework axiom A1"** = retained `Cl(3)` local-algebra axiom per
  `MINIMAL_AXIOMS_2026-05-03.md`.
- **"BAE-condition" (Brannen Amplitude Equipartition)** = the
  amplitude-ratio constraint `|b|²/a² = 1/2` for the
  `C_3`-equivariant Hermitian circulant `H = aI + bC + b̄C²` on
  `hw=1 ≅ ℂ³`. Per the rename in [`BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md`](BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md), **BAE is the primary name**; the legacy alias
  **"A1-condition"** remains valid in landed PRs.

These are distinct objects despite the legacy shared label.

## Question

After [`Probe 25`](KOIDE_BAE_PROBE_PHYSICAL_EXTREMIZATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe25.md) proposed that the **free**
cited Hamiltonian dynamics canonically selects F3 (real-dim
weighting (1, 2), giving κ=1, NOT BAE), the natural next attack is to
ask whether the **full cited interaction stack** — which break the
pure-bilinear/Gaussian structure of Probe 25 — can shift the
canonical functional from F3 to F1.

The cited source stack has SUBSTANTIAL non-Gaussian interaction content:

- **Yukawa coupling** `Y_e · ψ̄ · H · ψ` (retained per
  `CL3_SM_EMBEDDING_THEOREM.md`)
- **Higgs sector + Coleman-Weinberg radiative quartic** (per
  `COMPLETE_PREDICTION_CHAIN_2026_04_15.md` Sec 7: composite Higgs from
  taste condensate, `λ(M_Pl) = 0`, radiative quartic from y_t-loop)
- **Gauge couplings** (g_2, g_Y, α_LM = α_bare/u_0; retained per
  `ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md`)
- **Plaquette / Wilson action** (retained, β=6, ⟨P⟩=0.5934)
- **Probe 19 Yukawa-vertex factor** `α_bare × α_LM = α_LM² × u_0`
  (Probe 19's "+2" piece in the m_τ chain `m_τ = M_Pl × (7/8)^{1/4} ×
  u_0 × α_LM^{18}`, retained from
  `KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md`)
- **Z_3 scalar potential** `V(m) = V₀ + linear + (3/2)m² + (1/6)m³`
  (retained per
  `KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md`)

**Question (Probe 28):** Does adding these full cited interaction stack
to Probe 25's free Gaussian dynamics shift the canonical
extremization functional from F3 to F1, thereby selecting BAE
(`κ = 2`, `|b|² = a²/2`)?

## Answer

**No.** Retained interacting matter-sector dynamics canonically
continues to select **F3**, NOT F1. Eight independent
retained-interaction-extension routes converge on F3:

```
INT-AV1   Higgs-quartic Tr(H^4) correction        -> preserves F3
INT-AV2   Yukawa fermion log det(D + Y_e H)       -> preserves F3
INT-AV3   Gauge plaquette + Y_e ~ sqrt(α_LM)      -> preserves F3
INT-AV4   Composite-Higgs CW radiative λ(H)       -> preserves F3
INT-AV5   Probe 19 vertex factor α_bare × α_LM    -> preserves F3
INT-AV6   Z_3 scalar potential V(m) = m² + m³/6   -> preserves F3
INT-AV7   Combined L_full = L_free + L_Yuk + L_H + L_g  -> preserves F3
INT-AV8   Multiplicity-counting search            -> NO interaction supplies (1, 1)
```

**Verdict: SHARPENED bounded obstruction (interacting-extension
layer) with new positive content.** The Probe 25 result that retained
**free** dynamics gives F3 NOT F1 extends to the **interacting** level:
ALL cited interaction terms preserve the (1, 2) real-dim weighting, so
F1 = (1, 1) multiplicity is structurally absent from cited dynamics
**at every order**. BAE admission count is UNCHANGED. No new admission.
No new axiom.

## Setup

### Premises (A_min for Probe 28)

| ID | Statement | Class |
|---|---|---|
| A1 | `Cl(3)` local algebra | framework axiom; see `MINIMAL_AXIOMS_2026-05-03.md` |
| A2 | `Z³` spatial substrate | framework axiom; same source |
| BZ | hw=1 BZ-corner triplet ≅ `ℂ³` with `C_3[111]` action | source dependency; see [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md) |
| Circulant | C_3-equivariant Hermitian on hw=1 is `aI + bC + b̄C²` | source dependency; see [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md) |
| BlockTotalFrob | `E_+ = 3a²`, `E_⊥ = 6\|b\|²` on `M_3(ℂ)_Herm` | source dependency; see [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md) |
| FrobIsoSplit | Frobenius pairing is the unique Ad-invariant inner product on `M_3(ℂ)_Herm` (up to scalar) | source dependency; see [`KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md`](KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md) |
| MRU | Weight-class theorem: `κ = 2μ/ν`; `(1,1) → κ=2`; `(1,2) → κ=1` | source dependency; see [`KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md) |
| KoideAlg | Koide `Q = 2/3 ⟺ a² = 2\|b\|² ⟺ \|b\|²/a² = 1/2` (BAE) | source dependency; see [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md) |
| RP-H | Reflection positivity → reconstructed Hamiltonian | source dependency; see [`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md) |
| LR | Lieb-Robinson microcausality on retained Hamiltonian, finite range r=1 | source dependency; see [`AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md`](AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md) |
| Probe21 | Native bilinear matter Hamiltonian | retained |
| Probe25 | Free-Gaussian dynamics → F3 (real-dim (1, 2)); F1 structurally absent at free level | source dependency; see [`KOIDE_BAE_PROBE_PHYSICAL_EXTREMIZATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe25.md`](KOIDE_BAE_PROBE_PHYSICAL_EXTREMIZATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe25.md) |
| WilsonChain | `v_EW = M_Pl × (7/8)^{1/4} × α_LM^{16}` and α_LM = α_bare/u_0; α_bare = 1/(4π); u_0 = ⟨P⟩^{1/4}; ⟨P⟩=0.5934 | source dependency; see [`COMPLETE_PREDICTION_CHAIN_2026_04_15.md`](COMPLETE_PREDICTION_CHAIN_2026_04_15.md) |
| Probe19 | `m_τ = M_Pl × (7/8)^{1/4} × u_0 × α_LM^{18}` with exponent 18 = 16 + 2 = EW+Yukawa-vertex; vertex factor α_bare × α_LM | source dependency; see [`KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md`](KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md) |
| YukawaSM | `Y_e · ψ̄ · H · ψ` couples lepton fields to circulant H on hw=1 | source dependency; see [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md) |
| HiggsCW | `λ(M_Pl) = 0` boundary; radiative quartic from y_t-loop; composite Higgs from taste condensate | source dependency; see [`COMPLETE_PREDICTION_CHAIN_2026_04_15.md`](COMPLETE_PREDICTION_CHAIN_2026_04_15.md) Sec 7 |
| Z3Pot | `V(m) = V₀ + linear + (3/2) m² + (1/6) m³`; cubic piece breaks Z_2 → Z_3 | source dependency; see [`KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md`](KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md) |

### Forbidden imports

- NO PDG observed mass values used as derivation input
- NO lattice MC empirical measurements as derivation input (other than retained ⟨P⟩)
- NO fitted matching coefficients
- NO same-surface family arguments
- NO new axioms or imports — primitives are derivations from axioms or
  retained work only (per user 2026-05-09 clarification)
- NO admitted SM Yukawa-coupling pattern as derivation input (the
  retained `Y_e` STRUCTURE is used, not numerical magnitudes)

## The structural argument

The Probe 25 conclusion can be stated structurally:

> The (1, 2) real-dim weighting of F3 is the **isotype real-dimension
> count** of the retained C_3 action on `Herm_circ(3) = R⟨I⟩ ⊕ R⟨C+C²⟩
> ⊕ R⟨i(C-C²)⟩`. The trivial isotype is 1-real-dim; the doublet
> isotype is 2-real-dim. This decomposition is fixed by C_3
> representation theory acting on `Herm_circ(3)`, and is **independent
> of the action**.

The path integral on `Herm_circ(3)` integrates over 3 real coordinates
`(r_0, r_1, r_2)`. The Jacobian volume element `dr_0 · dr_1 dr_2`
always carries the (1, 2) real-dim structure. Higher-order terms in
the action (Yukawa-fermion-loop log-det, Higgs quartic, gauge
plaquette, Z_3 cubic, etc.) shift the **location** of the extremum on
the (a, |b|)-plane but cannot change the **functional form** of the
log-density: they cannot remove or add a `log E_⊥` factor.

For F1 to emerge (i.e., for the (1, 1) multiplicity weighting to
replace (1, 2)), an additional cited interaction would need to
contribute exactly `−log E_⊥` to the effective free energy, canceling
one of the two `log E_⊥` factors of F3. Probe 28 verifies that **no
cited interaction contributes such a term**.

## Per-attack-vector analysis

Eight independent interaction-extension routes are tested. All eight
preserve the (1, 2) real-dim weighting; none shift F3 → F1.

### INT-AV1 — Higgs-quartic correction Tr(H^4)

**Status: PRESERVES F3.**

The retained composite Higgs has a radiative quartic from the
Coleman-Weinberg mechanism (per `COMPLETE_PREDICTION_CHAIN` Sec 7.1:
`λ(M_Pl) = 0` boundary; quartic generated by y_t-loop). Adding
`λ_eff · Tr(H^4)` to the action gives a non-Gaussian contribution
`V_quart = λ_eff · Tr(H^4)`, which decomposes as
`Tr(H^4) = sum_k λ_k(H)^4` over the eigenvalues `λ_k(H) = a + 2|b|
cos(φ + 2πk/3)`.

The Hessian of this quartic at the classical solution `H_0` is
**block-structured** on isotypes (preserved by C_3 covariance), but
the cross-block coupling `(0, 1), (0, 2)` is generally **nonzero**
(due to `a²|b|²` cross terms). Critically, this cross-coupling does
not change the **rank of the doublet block** (rank = 2, verified
numerically). The (1, 2) real-dim count is preserved.

**Numerical verification (runner Section 2):** the Hessian of
`Tr(H^4)` at sample H_0 has 3 finite real eigenvalues, the doublet
block has rank 2 (no zero modes), and the trivial-block diagonal
entry is positive. The structural (1, 2) weighting is intact.

### INT-AV2 — Yukawa fermion log-determinant log det(D + Y_e H)

**Status: PRESERVES F3.**

The retained Yukawa coupling `Y_e · ψ̄ · H · ψ` is bilinear in fermion
fields ψ and linear in H. Integrating out the fermions yields
`exp(−S_fermion[H]) = det(D + Y_e H)`, so
`S_fermion[H] = −log det(D + Y_e H)`.

The eigenvalues of `H_circ(a, b)` decompose into 1 trivial-isotype
mode (`a + 2|b|`, when φ=0) + 2 degenerate doublet-isotype modes
(`a − |b|`, when φ=0). The fermion log-det therefore decomposes as

```
log det(D + Y_e H_circ)
  = 1 × log(D + Y_e (a + 2|b|)) [trivial]
  + 2 × log(D + Y_e (a − |b|))  [doublet — TWO modes]
```

This is again the **(1, 2) real-dim weighting**, applied to the
fermion modes. The "2" doublet log-factor is the structural count of
fermion modes in the doublet isotype, identical in counting structure
to the bosonic Gaussian log-det of Probe 25.

**Numerical verification (runner Section 3):** at the F3-extremum
location, the total action `−(1/2) F3 − fermion_log_det` has its
minimum at `E_⊥ = 2N/3` (F3-target), NOT `N/2` (F1-target). The
Yukawa correction is not large enough to overturn the structural F3
selection.

### INT-AV3 — Gauge plaquette + indirect coupling via Y_e

**Status: PRESERVES F3.**

The Wilson plaquette gauge action `S_gauge = β · (1 − (1/3) Re Tr U_p)`
is **gauge-only**; it does not directly couple to the matter
circulant H on hw=1. Gauge enters the matter sector only through
`Y_e ~ √(4π α_LM)/√6` (color-flavor lock per Probe 19 / SM embedding).

Rescaling `Y_e` (e.g., by changing `α_LM`) only **rescales**
the eigenvalue spectrum of `(D + Y_e H)`; it does NOT change the
isotype decomposition. Verified at Y_e = 0.01, 0.1, 1.0, 10.0: all
give finite log-det without doublet collapse.

### INT-AV4 — Composite-Higgs Coleman-Weinberg

**Status: PRESERVES F3.**

The retained composite Higgs has `λ(M_Pl) = 0` boundary condition
(per `COMPLETE_PREDICTION_CHAIN` Sec 7.1), with quartic generated
radiatively from the y_t-loop. The CW one-loop effective potential
is

```
V_CW(H) = (1/2) Tr log K[H_0]
```

block-diagonal on isotypes (real-dim_+ = 1, real-dim_⊥ = 2). This is
identical in structure to PHYS-AV4 of Probe 25 (Connes-Chamseddine
spectral action), with the eigenvalue spectrum modified by the
Yukawa+quartic content. The (1, 2) real-dim weighting is preserved.

### INT-AV5 — Probe 19 Yukawa-vertex factor at lepton scale

**Status: PRESERVES F3.**

[`Probe 19`](KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md) gave `m_τ = M_Pl × (7/8)^{1/4} × u_0 ×
α_LM^{18}` with exponent decomposition 18 = 16 + 2 (EW exponent +
lepton-scale Yukawa-vertex factor). The "+2" piece is

```
vertex factor = α_bare × α_LM = α_LM² × u_0 ≈ 0.00722
```

This is a **multiplicative scale on the Yukawa coupling at the lepton
scale**: `Y_e_lepton = vertex_factor × Y_e_base`. Adding this vertex
to the action is structurally equivalent to INT-AV2 with rescaled `Y_e`.

The vertex factor is small (~0.7%), much smaller than the F3-vs-F1
extremum separation (~33% in `E_⊥/N`). The extremum location stays
in the F3-basin (verified numerically in runner Section 6).

### INT-AV6 — Z_3 scalar potential V(m) = (3/2)m² + (1/6)m³

**Status: PRESERVES F3.**

The retained Z_3 scalar potential (per
`KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md`) is
cubic in the eigenvalue m_k:

```
V(m_k) = V_0 + linear + (3/2) m_k² + (1/6) m_k³
```

Summed over k = 0, 1, 2:
- `sum m_k² = 3a² + 6|b|²` (phi-INDEPENDENT, just `(E_+ + E_⊥)/3` rescaled)
- `sum m_k³ = 3a³ + 6a|b|² + 2|b|³ cos(3φ)` (Z_3-COVARIANT through cos(3φ))

The cubic piece introduces a **φ-dependence** that breaks Z_2 → Z_3
(this is the point of the Z_3 scalar potential), but the resulting
contribution to the effective potential remains a **polynomial in (a²,
|b|²)** plus a Z_3-symmetric `cos(3φ) |b|³` piece. **No log-functional
contribution**, hence no `−log E_⊥` term that could shift F3 → F1.

The doublet remains 2-real-dim under Z_3 → Z_3 sub-orbit (φ rotates
in 2π/3 increments, but the magnitude |b| is preserved).

### INT-AV7 — Combined `L_full` effective action

**Status: PRESERVES F3.**

Combining ALL cited interaction terms:

```
L_full = (1/2) Tr(H²) + Y_e ψ̄.H.ψ + λ_CW Tr(H^4) + (1/6) sum m_k³ + β P
                     [Yukawa]      [Higgs CW]     [Z_3 cubic]    [gauge]
```

After fermion integration and one-loop expansion, the full effective
potential `V_full_eff(a, |b|)` on the (a, |b|)-plane is computed
numerically. Sweeping over `E_⊥ = x` at fixed `E_+ + E_⊥ = N`, the
extremum location across N ∈ {4, ..., 10} (12 random trials) is
**always closer to the F3-target `2N/3` than the F1-target `N/2`**.

The structural reason: every cited interaction is C_3-covariant
(by construction; the framework's C_3 structure is the source of the
3 generations, retained per
`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`).
C_3-covariant interactions preserve the isotype decomposition, hence
the (1, 2) real-dim weighting.

### INT-AV8 — Multiplicity-counting search

**Status: NO RETAINED INTERACTION SUPPLIES (1, 1).**

For F3 → F1 to occur, a cited interaction would need to contribute
`−log E_⊥` to the effective potential, canceling one of the two
`log E_⊥` factors of F3. Equivalently, an interaction would need to
**collapse** the 2-real-dim doublet to a 1-real-dim subspace.

Possible mechanisms surveyed:

| Mechanism | Verdict | Reference |
|---|---|---|
| Constraint `\|b\| = const` | Circular (=BAE itself) | — |
| Z_2 doublet → singlet collapse | Ruled out: Z_2 of (1, 1) but not SO(2) | Probe 13 |
| Retained continuous U(1) on b-doublet | None retained | Probe 14 |
| Interaction-induced one-loop constraint (zero mode in doublet block) | None: doublet block has rank 2 in full Hessian | Section 9.1 |

**The (1, 2) real-dim count is C_3 representation-theoretic on
`Herm_circ(3)`. No cited interaction modifies the C_3 representation
structure.** Hence no cited interaction supplies multiplicity-counting (1, 1).

## Theorem (Probe 28 sharpened bounded obstruction)

**Theorem.** On A1 + A2 + retained C_3-equivariance + retained
Block-Total Frobenius isotype decomposition + retained MRU + retained
Frobenius Isotype-Split Uniqueness + retained RP/transfer-matrix +
retained Lieb-Robinson + retained Wilson chain + Probe 19 +
`CL3_SM_EMBEDDING_THEOREM` + retained `KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER`
+ retained Probes 12, 13, 14, 18, 21, 25:

```
(a) The cited interaction terms on Herm_circ(3) — Yukawa Y_e ψ̄.H.ψ,
    Higgs CW radiative quartic λ_eff Tr(H^4), gauge coupling via
    Y_e ~ sqrt(α_LM), Probe 19 vertex α_bare × α_LM, Z_3 scalar
    potential V(m) = (3/2)m² + (1/6)m³ — are all C_3-covariant
    on Herm_circ(3) by construction.
    [Verified Section 8.2.]

(b) C_3-covariance preserves the isotype decomposition
    Herm_circ(3) = R⟨I⟩ ⊕ R⟨C+C²⟩ ⊕ R⟨i(C-C²)⟩
    with real_dim_+ = 1 (trivial isotype) and real_dim_⊥ = 2
    (doublet isotype). This is fixed by C_3 representation theory,
    independent of the action.
    [Verified Section 9.3.]

(c) Eight independent retained-interaction-extension routes converge
    on F3 (real-dim weighting (1, 2)):
      INT-AV1: Higgs-quartic Tr(H^4) preserves block structure
      INT-AV2: Yukawa fermion log-det has (1, 2) mode counting
      INT-AV3: Gauge plaquette couples via Y_e ~ sqrt(α_LM)
      INT-AV4: Composite-Higgs CW = (1/2) Tr log K[H_0] block-diagonal
      INT-AV5: Probe 19 vertex α_bare × α_LM ≈ 0.0072 << F3-vs-F1 gap
      INT-AV6: Z_3 V(m) is polynomial in (a², |b|²) + cos(3φ)|b|³
      INT-AV7: Full L_full preserves F3 across N ∈ {4, ..., 10}
      INT-AV8: No cited interaction supplies (1, 1) multiplicity
    [Verified Sections 2-9.]

(d) The Hessian of the full effective potential V_full_eff at the
    F3-extremum has a doublet block with 2 nonzero singular values
    (rank 2). No interaction-induced zero mode in the doublet block.
    [Verified Section 9.1.]

(e) Adding any cited interaction to Probe 25's free-Gaussian
    extremization preserves the F3-class log-density: no retained
    interaction contributes a -log E_⊥ term that could cancel one
    of the two log E_⊥ factors of F3.
    [Algebraic; Section 10.3.]

(f) F3 extremum on E_+ + E_⊥ = N at E_+ = N/3, E_⊥ = 2N/3, gives
    κ = a²/|b|² = 1, NOT κ = 2 = BAE. F1 (multiplicity (1, 1),
    giving κ = 2 = BAE) is structurally absent from retained
    interacting dynamics.
    [Algebraic; Sections 1, 12.]

Therefore: cited interacting matter-sector dynamics canonically
selects F3, NOT F1, and gives κ = 1, NOT BAE. The Probe 25
free-Gaussian conclusion EXTENDS to the full interacting level. The
BAE admission count is unchanged. No new admission. No new axiom.
```

**Proof.** Each item is verified by the runner (75 PASS / 0 FAIL):
Section 0 (retained sanity); Section 1 (Probe 25 baseline recap);
Sections 2-9 (eight INT-AV computations); Section 10 (cross-validation);
Section 11 (convention robustness); Section 12 (verdict synthesis);
Section 13 (does-not-do disclaimers); Section 14 (comparison with
prior probes 12, 13, 14, 18, 21, 25). ∎

## Convention-robustness check

The runner verifies (Section 11):

- **Free F3 extremum invariant under H → cH:** `E_⊥/N = 2/3` across
  c ∈ {0.5, 1.0, 2.0, 5.0}.
- **Basis change C → C² = C^{-1}:** preserves the isotype
  decomposition; E_+, E_⊥ unchanged.
- **Vertex factor `α_bare × α_LM`:** gauge-fixed by lattice tadpole
  convention (`u_0 = ⟨P⟩^{1/4}`, `α_LM = α_bare/u_0`).

Note: with non-Gaussian interactions (Yukawa, Higgs CW, Z_3 cubic),
the dimensionless couplings `Y_e, λ_CW, G_3_Z3` do NOT rescale with
H, so the **interacting** extremum's relative location can shift
with the absolute scale. This is the expected behavior of an
interacting theory and does not affect the structural (1, 2) weighting.

## Why this probe is structurally distinct from Probe 25

| Probe | Dynamics | Action class | Conclusion |
|---|---|---|---|
| Probe 25 | FREE Hamiltonian (bilinear in H) | Gaussian path integral on `Herm_circ(3)` | F3 canonical from real-dim count (1, 2); F1 absent |
| **Probe 28** | **FULL INTERACTING (Yukawa + Higgs + gauge + Z_3 cubic)** | **NON-Gaussian: log det + quartic + cubic** | **F3 canonical at INTERACTING level; F1 still absent** |

Probe 25 closed the F1-vs-F3 ambiguity at the **free** level. Probe 28
closes it at the **interacting** level: the addition of retained
interactions does NOT supply a multiplicity-counting principle that
could reinstate F1.

This is the strongest possible structural rejection of F1 within
cited source-stack content: F1 is absent from BOTH free and interacting retained
dynamics. Closing BAE therefore requires a NON-RETAINED primitive —
either (a) a non-retained-dynamics extremization principle, or (b) a
new admission distinct from BAE itself.

## Status block

### Author proposes (audit lane decides):

- `claim_type`: `bounded_theorem` (sharpened obstruction at the
  interacting-extension layer; new positive content: F1 structurally
  rejected by retained INTERACTING dynamics, extending Probe 25)
- audit-derived effective status: set only by the independent audit lane after review
- `admitted_context_inputs`: `["BAE-condition: |b|²/a² = 1/2 (legacy:
  A1-condition)"]` — the residual admission, with the Probe 28
  sharpening: **"Retained INTERACTING matter-sector dynamics
  canonically selects F3 (rank-weighted, (1, 2)) on the (a, |b|)-plane.
  F1 (multiplicity-weighted, (1, 1)) is structurally rejected by ALL
  cited dynamics — both free (Probe 25) and interacting (Probe 28).
  F3 gives κ=1, NOT BAE."**

**No new admissions added by this probe. The BAE admission count is
UNCHANGED.**

### What this probe DOES

1. Extends Probe 25 from the FREE (bilinear-Gaussian) level to the
   FULL INTERACTING level (Yukawa + Higgs + gauge + Z_3 + Probe 19
   vertex).
2. Identifies eight independent retained-interaction-extension routes
   (INT-AV1 through INT-AV8) and verifies all preserve F3.
3. Demonstrates that no cited interaction contributes a `−log E_⊥`
   term to the effective potential that could shift F3 → F1.
4. Demonstrates that no cited interaction induces a zero mode in
   the doublet block of the full Hessian (the doublet remains 2-real-dim).
5. Sharpens the campaign's terminal residue: F1 is absent from BOTH
   free and interacting cited dynamics. Closing BAE requires a
   non-retained primitive.
6. Cross-validates Probes 12, 13, 14, 18, 21, 25: same conclusion
   under the addition of full cited interaction stack.

### What this probe DOES NOT do

1. Does NOT close the BAE-condition.
2. Does NOT add any new axiom or new admission.
3. Does NOT modify any retained theorem (Probe 25's F3-canonical
   theorem is unchanged; this probe extends it).
4. Does NOT promote any downstream theorem.
5. Does NOT promote Probe 19's m_τ Wilson formula to retained
   (Probe 19 retains its own authority; this probe consumes the
   vertex factor as input only).
6. Does NOT load-bear PDG values into a derivation step.
7. Does NOT promote external surveys to retained authority.
8. Does NOT propose F3-extremum κ=1 as the physical Koide value (the
   physical κ=2 / BAE remains a bounded admission).
9. Does NOT promote sister bridge gaps (L3a, L3b, C-iso, W1.exact).

## Honest assessment

**What the probe finds:**

1. **Retained INTERACTING dynamics canonically gives F3.** Eight
   independent retained-interaction-extension routes converge on F3
   (real-dim weighting (1, 2)). This includes the FULL Yukawa + Higgs
   + gauge + Z_3-potential + Probe 19 Yukawa-vertex content.

2. **The (1, 2) real-dim count is C_3 representation-theoretic on
   `Herm_circ(3)`.** It is fixed by the retained isotype decomposition
   itself, independent of the action. No cited interaction modifies
   the C_3 representation structure.

3. **F1 = (1, 1) multiplicity is structurally absent from retained
   dynamics at every order.** It cannot arise from any C_3-covariant
   interaction, free or interacting.

4. **The Probe 25 conclusion extends to the full interacting level.**
   This is the strongest possible structural rejection of F1 within
   cited source-stack content.

5. **BAE is therefore NOT canonical from cited dynamics, free OR
   interacting.** Any closure of BAE requires either (a) a
   non-retained-dynamics extremization principle, or (b) a different
   retained dynamic that rejects the C_3-representation-theoretic
   structure of the matter circulant. Neither is provided by retained
   content.

**What this probe contributes to the campaign:**

1. **New positive content**: F1 structurally rejected by retained
   INTERACTING dynamics (sharpens Probe 25's free-level rejection).
2. **Sharpened residue characterization**: F1 is absent from BOTH
   free and interacting cited dynamics; the (1, 2) count is fixed
   by C_3 representation theory.
3. **Twenty-eighth independent attack**: returns the same campaign-
   terminal-state structural obstruction at the **interacting-extension
   level**, distinct from prior 27 probes.

The remaining residue is **maximally sharp**:

> **BAE = (1, 1)-multiplicity-weighted extremum on the additive
> log-isotype-functional class. Retained INTERACTING dynamics
> (Yukawa + Higgs + gauge + Z_3 + Probe 19 vertex) gives the (1, 2)
> real-dim-weighted F3, not the (1, 1) multiplicity-weighted F1. The
> (1, 2) real-dim weighting is fixed by C_3 representation theory on
> `Herm_circ(3)`; no cited interaction modifies it.**

Closing BAE therefore requires admitting a multiplicity-counting
principle as a NEW PRIMITIVE — i.e., a new admission or a new
retained source distinct from the existing C_3-equivariant interaction
content. Probe 28 makes this requirement maximally explicit at the
interacting-extension level.

## Cross-references

### Foundational baseline

- Minimal axioms: `MINIMAL_AXIOMS_2026-05-03.md`
- Substep-4 AC narrowing (PDG-input prohibition): [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)

### Retained Wilson chain (load-bearing for INT-AV3, INT-AV5)

- Complete prediction chain: [`COMPLETE_PREDICTION_CHAIN_2026_04_15.md`](COMPLETE_PREDICTION_CHAIN_2026_04_15.md)
- α_LM geometric-mean identity: [`ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md`](ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md)
- Probe 19 (Wilson chain m_τ): [`KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md`](KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md)

### Retained matter-sector interaction content

- SM embedding theorem (Yukawa structure): [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md)
- Z_3 scalar potential: [`KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md`](KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md)

### Retained C_3 / circulant structure (load-bearing for the structural argument)

- BZ-corner forcing: [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md)
- Circulant character / eigenvalue: [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
- Charged-lepton Koide cone equivalence: [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)

### Block-total Frobenius and weight-class structure

- Block-total Frobenius: [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)
- Frobenius isotype-split uniqueness: [`KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md`](KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md)
- MRU weight-class: [`KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md)

### Probe campaign

- Probe 12 (Plancherel/Peter-Weyl): `KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md`
- Probe 13 (real-structure): `KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md`
- Probe 14 (retained-U(1) hunt): `KOIDE_A1_PROBE_RETAINED_U1_HUNT_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe14.md`
- Probe 18 (F1-vs-F3 algebraic): `KOIDE_BAE_PROBE_F1_CANONICAL_FUNCTIONAL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe18.md`
- Probe 19 (Wilson chain m_τ): `KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md`
- Probe 21 (native bilinear flow): `KOIDE_BAE_PROBE_NATIVE_LATTICE_FLOW_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe21.md`
- Probe 25 (free Gaussian extremization): `KOIDE_BAE_PROBE_PHYSICAL_EXTREMIZATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe25.md`
- Probe 26 (Wilson dim consistency): [`KOIDE_BAE_PROBE_WILSON_DIMENSIONAL_CONSISTENCY_BOUNDED_NOTE_2026-05-09_probe26.md`](KOIDE_BAE_PROBE_WILSON_DIMENSIONAL_CONSISTENCY_BOUNDED_NOTE_2026-05-09_probe26.md)

### Naming convention

- BAE rename note ([`BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md`](BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md), PR #790): "Brannen
  Amplitude Equipartition (BAE)" is the primary name; "A1-condition"
  is the legacy alias.

## Validation

```bash
python3 scripts/cl3_koide_bae_probe_interacting_dynamics_2026_05_09_probe28.py
```

Expected: `=== TOTAL: PASS=75, FAIL=0 ===`

The runner verifies:

1. Section 0 — Retained input sanity (C unitary, order 3; E_+ = 3a²;
   E_⊥ = 6|b|²; α_LM, u_0, (7/8)^{1/4} from retained Wilson chain).
2. Section 1 — Probe 25 free-Gaussian baseline recap (F3 → κ=1; F1 → κ=2 = BAE).
3. Section 2 — INT-AV1: Higgs-quartic Tr(H^4); Hessian preserves block structure.
4. Section 3 — INT-AV2: Yukawa fermion log-det; mode counting (1 + 2);
   total action extremum stays in F3-basin.
5. Section 4 — INT-AV3: Gauge plaquette + indirect coupling via Y_e ~ √α_LM.
6. Section 5 — INT-AV4: Composite-Higgs CW radiative quartic (block-diagonal Tr log).
7. Section 6 — INT-AV5: Probe 19 vertex factor α_bare × α_LM ≈ 0.0072;
   perturbative correction; extremum stays in F3-basin.
8. Section 7 — INT-AV6: Z_3 scalar potential V(m); cubic in (a, |b|²)
   plus cos(3φ)|b|³; phi-independence at quadratic order.
9. Section 8 — INT-AV7: Combined L_full effective extremum across
   N ∈ {4, ..., 10} (12 random trials); always F3-basin.
10. Section 9 — INT-AV8: Multiplicity-counting search; doublet block
    has rank 2 in full Hessian; no cited interaction supplies (1, 1).
11. Section 10 — Cross-validation across all 8 INT-AVs.
12. Section 11 — Convention robustness (free F3 scale-invariance, basis change).
13. Section 12 — Verdict synthesis (F3 canonical at INTERACTING level;
    F1 structurally absent; κ=1, NOT BAE).
14. Section 13 — Does-not disclaimers (no BAE closure, no admission,
    no PDG, no retained-theorem modification).
15. Section 14 — Comparison with prior probes (12, 13, 14, 18, 21, 25).

Total: 75 PASS / 0 FAIL.

## User-memory feedback rules respected

- `feedback_consistency_vs_derivation_below_w2.md`: this note
  specifically derives the F3-canonical statement at the INTERACTING
  level from the retained C_3-covariance of all cited interaction terms;
  the (1, 2) real-dim weighting is the structurally forced statement,
  not just algebraic consistency. The fact that F1 algebraically also
  gives BAE under DIFFERENT (multiplicity) counting is a consistency
  equality, not a derivation from cited source-stack content.
- `feedback_hostile_review_semantics.md`: this note stress-tests the
  semantic claim "F1 is canonical at the interacting level" from each
  cited interaction angle. Each INT-AV's action-level
  identification fails F1 at the same structural locus: the doublet
  is 2-real-dim, fixed by C_3 representation theory; C_3-covariant
  interactions cannot modify it.
- `feedback_retained_tier_purity_and_package_wiring.md`: no automatic
  cross-tier promotion. This note is a bounded obstruction with new
  positive content; the parent BAE admission remains at its prior
  bounded status; no retained-tier promotion implied.
- `feedback_physics_loop_corollary_churn.md`: the eight-INT-AV attack
  with explicit Higgs-quartic / Yukawa / gauge / CW / vertex / Z_3 /
  combined / multiplicity-search verifications is substantive new
  structural content — not a relabel of any prior probe. Probe 25
  attacked at the FREE-dynamics extremization level; this probe
  attacks at the FULL INTERACTING level.
- `feedback_compute_speed_not_human_timelines.md`: alternative routes
  (closing BAE) characterized in terms of WHAT additional content
  would be needed (a multiplicity-counting principle distinct from
  cited dynamics or interactions), not how-long-they-would-take.
- `feedback_special_forces_seven_agent_pattern.md`: this note
  packages a multi-angle attack (eight independent INT-AVs) on a
  single load-bearing structural hypothesis (cited interaction terms
  shift F3 → F1), with sharp PASS/FAIL deliverables in the runner.
- `feedback_review_loop_source_only_policy.md`: this note is a single
  source-note proposal + paired runner + cached output, no synthesis
  notes, no lane promotions, no working "Block" notes.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links so
the audit citation graph can track them. It does not promote this
note or change the audited claim scope.

- [koide_bae_probe_physical_extremization_bounded_obstruction_note_2026-05-09_probe25](KOIDE_BAE_PROBE_PHYSICAL_EXTREMIZATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe25.md) (Probe 25 baseline)
- [koide_bae_probe_wilson_chain_mass_sharpened_note_2026-05-09_probe19](KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md) (Probe 19 vertex)
- [koide_bae_probe_native_lattice_flow_bounded_obstruction_note_2026-05-09_probe21](KOIDE_BAE_PROBE_NATIVE_LATTICE_FLOW_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe21.md) (Probe 21 bilinear)
- [koide_bae_probe_f1_canonical_functional_bounded_obstruction_note_2026-05-09_probe18](KOIDE_BAE_PROBE_F1_CANONICAL_FUNCTIONAL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe18.md) (Probe 18 algebraic)
- [koide_a1_probe_plancherel_peter_weyl_bounded_obstruction_note_2026-05-09_probe12](KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md)
- [koide_a1_probe_real_structure_bounded_obstruction_note_2026-05-09_probe13](KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md)
- [koide_a1_probe_retained_u1_hunt_bounded_obstruction_note_2026-05-09_probe14](KOIDE_A1_PROBE_RETAINED_U1_HUNT_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe14.md)
- [cl3_sm_embedding_theorem](CL3_SM_EMBEDDING_THEOREM.md) (Yukawa structure)
- [complete_prediction_chain_2026_04_15](COMPLETE_PREDICTION_CHAIN_2026_04_15.md) (Higgs CW + Wilson chain)
- [koide_z3_scalar_potential_lepton_mass_tower_note_2026-04-19](KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md) (Z_3 V(m))
- [alpha_lm_geometric_mean_identity_theorem_note_2026-04-24](ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md)
- [axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01](AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md)
- [axiom_first_reflection_positivity_theorem_note_2026-04-29](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md)
- [koide_kappa_block_total_frobenius_measure_theorem_note_2026-04-19](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)
- [koide_mru_weight_class_obstruction_theorem_note_2026-04-19](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md)
- [staggered_dirac_bz_corner_forcing_theorem_note_2026-05-07](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md)
- [minimal_axioms_2026-05-03](MINIMAL_AXIOMS_2026-05-03.md)
- [staggered_dirac_substep4_ac_narrow_bounded_note_2026-05-07_substep4ac](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)
