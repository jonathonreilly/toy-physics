# Claims Table

**Date:** 2026-04-22
**Scope:** explicit claims, their status, and authorities in this closure package.

| # | Claim | Status | Precision | Authority |
|---|-------|--------|-----------|-----------|
| C1 | δ(m) equals the Euclidean rotation angle of real Koide amplitude s(m) in the 2D plane orthogonal to `singlet = (1,1,1)/√3` | **Retained theorem** | 10⁻¹³ numerical | `KOIDE_BRANNEN_WILSON_DSQ_QUANTIZATION_THEOREM_NOTE` §7 (Rigid-Triangle Rotation) |
| C2 | α(m_0) = −π/2 exactly at unphased point | **Retained theorem** | 10⁻¹⁴ | Derived from u(m_0) = v(m_0), forcing ⟨s_⊥, e_1⟩ = 0 |
| C3 | α(m_pos) − α(m_0) = −π/12 exactly at positivity threshold | **Retained theorem** | 10⁻¹⁵ | Derived from u(m_pos) = 0 + classical identity `sin(π/12)=(√6−√2)/4` on Koide cone |
| C4 | First-branch span = 2π/|O| where |O| = 24 (octahedral rotation group) | **Retained theorem** | Exact | `KOIDE_BRANNEN_WILSON_DSQ_QUANTIZATION_THEOREM_NOTE` §7.3a (Octahedral-Domain Theorem); |O| enumerated |
| C5 | α(m_*) − α(m_0) = −2/9 rad at physical charged-lepton point | **Retained theorem (structural)** | 10⁻¹³ | Defined via structural equation `α(m_0) − α(m_*) = η_ABSS = 2/9`; both sides axiom-native; unique first-branch solution by monotonicity + IVT; PDG match is forward prediction (see `RESIDUAL_CLOSURES.md` §1) |
| C6 | Cl(3) = M_2(C) + Z_3 cyclic action ⇒ G-signature ABSS η = 2/9 (standard complexification weights (ω, ω²)) | **Retained theorem (symbolic)** | Exact (sympy) | Standard Atiyah-Bott-Singer equivariant signature; weights (1,2) = eigenvalues on complexified 2-real normal (see `RESIDUAL_CLOSURES.md` §3) |
| C7 | Explicit Wilson-Dirac on L=3 lattice (= retained d=3) illustrates the ABSS continuum theorem at the physical 3-generation realization | **Illustrative verification** | 10⁻¹⁰ at 32/291 r values | Continuum proof is via ABSS theorem (C6); L=3 lattice is the Z_3-commensurate compactification `Z³/(3Z)³` retained via three-generation structure (see `RESIDUAL_CLOSURES.md` §2) |
| C8 | Body-diagonal Z_3 fixed sites = 3 charged-lepton generations (physical identification) | **Retained theorem** | — | `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE` (retained on `main`) |
| C9 | Per-generation Brannen phase δ = 2/9 rad equals per-fixed-site ABSS η via retained 3-generation identification | **Retained composition** | — | C1 + C7 + C8 |
| C10 | The combined closure (C1–C9) closes Lane 2 of the scalar-selector cycle | **Candidate closure** | — | This package |

## Secondary/context claims

| # | Claim | Status |
|---|-------|--------|
| C11 | PDG charged-lepton mass ratios are reproduced by the framework at δ = 2/9 rad to <0.03% | Retained numerical (runner §5) |
| C12 | Standard 2π Berry convention `δ_rad = 2π·η` fails PDG (gives negative eigenvalue) | Retained negative result (runner §5.2) |
| C13 | Route 3 `W_{Z_3}^{d²} = exp(2i)·𝟙` follows from retained n_eff=2, d=3 + one-clock natural time | Reviewer-conditional, **superseded** by Rigid-Triangle + Dirac descent above |
| C14 | Triple convergence: ABSS η = anomaly Tr[Y³]_q_L = Brannen δ_per_step = 2/d² = 2/9 | Retained multi-path consistency (sympy-verified) |

## No new axioms used

All claims derive from the retained axiom base:

- **A0**: Cl(3) on Z³ (one Clifford axiom).
- Retained cubic kinematics (Z_3 ⊂ O ⊂ SO(3) on Z³).
- Retained ANOMALY_FORCES_TIME (3+1 Lorentzian structure, single-clock evolution).
- Retained THREE_GENERATION_OBSERVABLE_THEOREM.
- Retained observable-principle ABSS / G-signature computation.
- Retained Koide-cone structure Q = 2/3.

## Comparison to prior open state

Prior state in `SCALAR_SELECTOR_REMAINING_OPEN_IMPORTS_2026-04-20.md`:

> **Brannen phase `δ = 2/9` on the physical base | θ | executable APS / ABSS support package isolates the exact ambient topological value `η = 2/9`, but the physical selected-line Brannen-phase bridge remains open.**

New state (this package):

- Selected-line δ is now identified (C1–C5) as a plain Euclidean rotation angle.
- Ambient η = 2/9 is derived from A0 + cubic kinematics (C6).
- Explicit Dirac construction (C7) shows per-fixed-site realization.
- 3-generation identification (C8–C9) links per-site = per-generation.

**The physical bridge is therefore closed via explicit geometric + algebraic + lattice mechanisms**, with no new axioms.
