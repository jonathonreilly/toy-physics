# Assumption / Import Ledger — Staggered-Dirac Realization Gate Loop

**Date:** 2026-05-07
**Loop:** staggered-dirac-realization-gate-20260507

## A1+A2 — Retained framework axioms (only)

| ID | Statement | Status |
|---|---|---|
| A1 | Local algebra is `Cl(3)` per [`MINIMAL_AXIOMS_2026-05-03.md`](../../../../docs/MINIMAL_AXIOMS_2026-05-03.md) | retained |
| A2 | Spatial substrate is cubic lattice `Z^3` | retained |

## Retained primitives directly relevant to staggered-Dirac

| Primitive | Statement | Authority |
|---|---|---|
| Cl(3) per-site uniqueness | Two non-isomorphic complex spinor irreps of Cl(3), each dim 2, distinguished by central pseudoscalar `ω = γ₁γ₂γ₃` | [`AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md`](../../../../docs/AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md) (chirality-aware repair 2026-05-03) |
| Per-site Hilbert dim | `dim_C H_x = 2` exactly; Pauli realization | [`CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md`](../../../../docs/CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md) |
| Spin-statistics (S2) | Bosonic 2nd quantization on Cl(3) site → infinite-dim Fock incompatible with finite-dim Cl(3) module → Grassmann is forced | [`AXIOM_FIRST_SPIN_STATISTICS_THEOREM_NOTE_2026-04-29.md`](../../../../docs/AXIOM_FIRST_SPIN_STATISTICS_THEOREM_NOTE_2026-04-29.md) — KEY: provides obstruction-1 forcing |
| Three-generation observable theorem | Exact M_3(C) algebra on retained `hw=1` triplet; no proper quotient | [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](../../../../docs/THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md) |
| Three-generation no-proper-quotient | Narrowed exact statement | [`THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02.md`](../../../../docs/THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02.md) |
| No-rooting irreducibility | No proper taste projection preserves Hamiltonian Cl(3) on Z³ | `scripts/frontier_generation_rooting_undefined.py` |
| BZ-corner spectral / orbit structure | Exact `1 + 1 + 3 + 3` corner structure | `scripts/frontier_generation_fermi_point.py` |
| C^8 = 4 A_1 + 2 E (S_3) | Full taste-cube S_3 carrier content | [`S3_TASTE_CUBE_DECOMPOSITION_NOTE.md`](../../../../docs/S3_TASTE_CUBE_DECOMPOSITION_NOTE.md) |
| Site-phase cube-shift intertwiner | Exact BZ-corner / taste-cube bridge | [`SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md`](../../../../docs/SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md) |
| Fermion parity Z_2 grading | Exact Z_2 grading from chirality | [`FERMION_PARITY_Z2_GRADING_THEOREM_NOTE_2026-05-02.md`](../../../../docs/FERMION_PARITY_Z2_GRADING_THEOREM_NOTE_2026-05-02.md) |
| Physical-lattice necessity | Substrate-level physical-lattice reading on Hilbert/locality/info surface | [`PHYSICAL_LATTICE_NECESSITY_NOTE.md`](../../../../docs/PHYSICAL_LATTICE_NECESSITY_NOTE.md) |
| CPT exact | T H T^{-1} = H reality | [`CPT_EXACT_NOTE.md`](../../../../docs/CPT_EXACT_NOTE.md) |
| Reflection positivity A11 | Transfer matrix + OS reconstruction | [`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](../../../../docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md) |
| Lieb-Robinson bound | Microcausality | [`AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md`](../../../../docs/AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md) |

## Open gates (admitted-context only, not load-bearing for derivation)

| Item | Class | Authority |
|---|---|---|
| Staggered-Dirac realization (A3) | OPEN GATE — THIS IS WHAT WE'RE CLOSING | [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](../../../../docs/STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md) |
| g_bare = 1 normalization (A4) | OPEN GATE | `MINIMAL_AXIOMS_2026-05-03.md` |
| Physical-color identification | deferred bridge | `CL3_COLOR_AUTOMORPHISM_THEOREM.md` |

## Standard mathematical infrastructure (admissible non-derivation)

| Item | Role | Source |
|---|---|---|
| Lie-algebra rep theory + Schur orthogonality | Standard math machinery | textbook |
| Brillouin zone / momentum-space analysis on Z^3 | Standard math machinery | textbook |
| Kawamoto-Smit staggered-fermion construction | Standard lattice gauge theory | Kawamoto & Smit 1981 |
| Finite Grassmann calculus | Standard QFT machinery | textbook (Berezin, Slavnov-Faddeev) |
| Spectral analysis of bilinear operators | Standard math | textbook |

## Forbidden imports (no load-bearing role)

- NO PDG observed values (Higgs mass, fermion masses, mixing angles, etc.)
- NO lattice MC empirical measurements as derivation inputs
- NO fitted matching coefficients
- NO same-surface family arguments
- NO load-bearing literature numerical comparators
- NO new axioms beyond A1+A2 (no-new-axiom rule)

## A_min for the staggered-Dirac realization gate

The minimal allowed premise set for closing the gate:

```
A_min(staggered-Dirac) = {
  A1 (Cl(3) local algebra),
  A2 (Z^3 spatial substrate),
  Cl(3) per-site uniqueness (retained),
  Per-site Hilbert dim = 2 (retained),
  Cl(3) chirality central pseudoscalar ω (retained),
  Spin-statistics S2 forcing (retained, support tier),
  No-rooting irreducibility (retained),
  BZ-corner spectral structure (retained),
  Fermion parity Z_2 grading (retained),
  CPT exact reality (retained),
  Reflection positivity A11 (retained),
  Lieb-Robinson microcausality (retained),
  Standard math infrastructure (admissible)
}
```

## Counterfactual pass

For each implicit modeling choice, what does the alternative open?

| Choice | Standard | Alternative | Direction opened |
|---|---|---|---|
| Matter algebra | Grassmann | Bosonic Fock | Spin-statistics S2 RULES OUT (incompatible with finite Cl(3) dim 2) |
| Site representation | Pauli σ_i | Higher-dim Cl(3) module | Per-site uniqueness theorem RULES OUT (Cl(3) faithful irrep is dim 2 only) |
| Lattice geometry | Z³ | Other lattices | A2 retained as axiom; not subject to alternative |
| Chirality grading | sublattice parity ε(x)=(−1)^{Σx_i} | Other Z_2 gradings | FERMION_PARITY_Z2_GRADING_THEOREM forces sublattice parity |
| Kinetic structure | Kawamoto-Smit phases | Other staggered phase choices | Block 03 target — IS this forced from chirality grading? |
| Taste-cube emergence | C^8 → 4 A_1 + 2 E | Other group decompositions | S3_TASTE_CUBE_DECOMPOSITION retained |
| BZ corner labeling | 1+1+3+3 by Hamming weight | Other corner labelings | Block 04 target — IS this forced from staggered structure? |
| Three-generation reading | hw=1 triplet | Other reading | THREE_GENERATION_OBSERVABLE_THEOREM retained |

## Counterfactual conclusion

Most counterfactuals are RULED OUT by retained primitives. The remaining
forcing-vs-compatibility gaps are:

1. **Substep 1 (Grassmann partition forcing):** EFFECTIVELY CLOSED by
   spin-statistics theorem (S2). Block 02 packages this explicitly.
2. **Substep 2 (Kawamoto-Smit phase forcing):** OPEN. Block 03 attacks.
3. **Substep 3 (BZ-corner three-generation forcing):** PARTIALLY CLOSED
   (1+1+3+3 retained, M_3(C) on hw=1 retained, no-proper-quotient retained).
   Block 04 packages.
4. **Substep 4 (Physical-species bridge):** OPEN with admitted-context.
   Block 05 attacks.
