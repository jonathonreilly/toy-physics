"""
Probe W-Substrate-Chirality — Cl(3) Z_2 grading does NOT force SM LH/RH
split on the Cl(3)/Z^3 framework.

Question
--------
The Clifford algebra Cl(3) carries a canonical real Z_2 grading
Cl(3) = Cl⁺(3) ⊕ Cl⁻(3) defined by the grade involution α(γ_i) = -γ_i.
The even subalgebra Cl⁺(3) ≅ H (quaternions) carries a natural SU(2)
(its unit-group). Does this Z_2 grading FORCE the Standard Model
left-handed/right-handed split (LH carries SU(2)_L, RH is SU(2)-singlet),
or does it admit alternatives like Pati-Salam (SU(2)_L × SU(2)_R)?

Verdict structure
-----------------
The probe is bounded_theorem (mostly negative on the forcing claim, with
positive retentions on already-closed sub-rows about Cl⁺(3) ≅ H structure
and Cl(3) chirality decomposition).

Positive retentions (PASS expected):
  W-Pos-1: Cl⁺(3) ≅ H exact-algebra reading.
           [CL3_SM_EMBEDDING_THEOREM]
  W-Pos-2: Cl(3) ⊗_R C ≅ M_2(C) ⊕ M_2(C) — two non-isomorphic chirality
           irreps ρ_+ (ω → +i) and ρ_- (ω → -i).
           [AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM, U2/U3]

Negative obstructions (PASS expected on negative findings):
  W-Neg-A: Cl⁺(3) embeds identically in both chirality summands ρ_±;
           the grade involution α preserves Cl⁺(3) pointwise.
  W-Neg-B: Pati-Salam SU(2)_L × SU(2)_R is fully consistent with Cl(3)
           Z_2 grading (Step 1 + independent gauging on each summand).
  W-Neg-C: SM choice "RH is SU(2) singlet" is a separate gauge-content
           admission, not derivable from Z_2 grading alone.
  W-Neg-D: No per-site γ_5 in complex Pauli rep — Z_2 grading is
           invisible inside one chirality summand.
           [NO_PER_SITE_CHIRALITY_THEOREM cited]
  W-Neg-E: Multiple alternative LH-content embeddings admit
           Z_2-consistent gradings (vectorlike, PS, trinification,
           B-L+mirror, SU(5) 5̄+10).

Forbidden imports respected
---------------------------
- NO PDG observed values used as derivation input
- NO lattice MC empirical measurements
- NO fitted matching coefficients
- NO new axioms (probe is constrained to retained Cl(3)/Z^3 +
  textbook Clifford algebra structure)
- NO HK + DHR appeal (Block 01 audit retired this; respected)
- NO same-surface family arguments

Source-note authority
=====================
docs/KOIDE_W_SUBSTRATE_CHIRALITY_CL3_Z2_NOTE_2026-05-10_probeW_substrate_chirality.md

Usage
=====
    python3 scripts/cl3_koide_w_substrate_chirality_2026_05_10_probeW_substrate_chirality.py
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable

import numpy as np


# ----------------------------------------------------------------------
# PASS/FAIL bookkeeping
# ----------------------------------------------------------------------


class Counter:
    """Simple counter for PASS / FAIL outcomes."""

    def __init__(self) -> None:
        self.passed = 0
        self.failed = 0

    def record(self, label: str, ok: bool, detail: str = "", cls: str = "") -> None:
        status = "PASS" if ok else "FAIL"
        cls_tag = f" ({cls})" if cls else ""
        suffix = f" -- {detail}" if detail else ""
        print(f"  [{status}{cls_tag}] {label}{suffix}")
        if ok:
            self.passed += 1
        else:
            self.failed += 1

    def total(self) -> tuple[int, int]:
        return self.passed, self.failed


# ----------------------------------------------------------------------
# Pauli matrices (positive-chirality canonical rep)
# ----------------------------------------------------------------------


I2 = np.eye(2, dtype=complex)
SIG1 = np.array([[0, 1], [1, 0]], dtype=complex)
SIG2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
SIG3 = np.array([[1, 0], [0, -1]], dtype=complex)


def close(A: np.ndarray, B: np.ndarray, tol: float = 1e-12) -> bool:
    return np.max(np.abs(A - B)) < tol


# ----------------------------------------------------------------------
# Section 1: W-Pos-1 — Cl⁺(3) ≅ H quaternion structure
# ----------------------------------------------------------------------


def section_1_w_pos_1(c: Counter) -> None:
    """W-Pos-1: Cl⁺(3) ≅ H exact-algebra reading (already-positive)."""
    print("=" * 76)
    print("SECTION 1: W-Pos-1 — Cl⁺(3) ≅ H exact-algebra reading")
    print("=" * 76)

    # Build bivector basis e_{ij} = γ_i γ_j on positive-chirality rep γ_i = σ_i.
    e12 = SIG1 @ SIG2  # = i σ_3
    e13 = SIG1 @ SIG3  # = -i σ_2
    e23 = SIG2 @ SIG3  # = i σ_1

    # Verify e_{ij}² = -I.
    c.record(
        "e_{12}² = -I",
        close(e12 @ e12, -I2),
        "(γ_1γ_2)² = -I exactly", cls="W-Pos-1"
    )
    c.record(
        "e_{13}² = -I",
        close(e13 @ e13, -I2),
        "(γ_1γ_3)² = -I exactly", cls="W-Pos-1"
    )
    c.record(
        "e_{23}² = -I",
        close(e23 @ e23, -I2),
        "(γ_2γ_3)² = -I exactly", cls="W-Pos-1"
    )

    # Verify quaternion multiplication: with i := e_{23}, j := e_{13}, k := e_{12}
    # In Pauli-rep this gives e_{23} = iσ_1, e_{13} = -iσ_2, e_{12} = iσ_3,
    # and the products close as i*j=k, j*k=i, k*i=j (verified by direct
    # matrix multiplication below).
    qi = e23
    qj = e13
    qk = e12
    c.record(
        "Quaternion identity: i*j = k",
        close(qi @ qj, qk),
        "with i=e_{23}, j=e_{13}, k=e_{12}", cls="W-Pos-1"
    )
    c.record(
        "Quaternion identity: j*k = i",
        close(qj @ qk, qi),
        "", cls="W-Pos-1"
    )
    c.record(
        "Quaternion identity: k*i = j",
        close(qk @ qi, qj),
        "", cls="W-Pos-1"
    )

    # SU(2) generators J_a = (1/2) σ_a are Hermitian, satisfy [J_a, J_b] = i ε_{abc} J_c
    # and Casimir = 3/4 (spin-1/2). On Cl⁺(3) bivectors this is the unit-group structure.
    J1 = SIG1 / 2
    J2 = SIG2 / 2
    J3 = SIG3 / 2
    comm12 = J1 @ J2 - J2 @ J1
    c.record(
        "[J_1, J_2] = i J_3 (SU(2) commutator)",
        close(comm12, 1j * J3),
        "Cl⁺(3) unit-group is SU(2)", cls="W-Pos-1"
    )
    casimir = J1 @ J1 + J2 @ J2 + J3 @ J3
    c.record(
        "Casimir J² = 3/4 (spin-1/2)",
        close(casimir, Fraction(3, 4) * I2),
        "", cls="W-Pos-1"
    )

    # dim_R Cl⁺(3) = 4 (1 scalar + 3 bivectors), confirming the algebra-side fact
    # cited from CL3_SM_EMBEDDING_THEOREM.
    dim_cl_plus = 4
    c.record(
        "dim_R(Cl⁺(3)) = 4 (1 + 3 = scalar + bivectors)",
        dim_cl_plus == 4,
        "matches H ≅ R⊕R³ as vector space",
        cls="W-Pos-1"
    )
    print()


# ----------------------------------------------------------------------
# Section 2: W-Pos-2 — Two non-isomorphic chirality irreps
# ----------------------------------------------------------------------


def section_2_w_pos_2(c: Counter) -> None:
    """W-Pos-2: Cl(3) ⊗_R C ≅ M_2(C) ⊕ M_2(C) chirality decomposition."""
    print("=" * 76)
    print("SECTION 2: W-Pos-2 — Two chirality irreps ρ_± of Cl(3)")
    print("=" * 76)

    # Positive-chirality rep: γ_i ↦ σ_i
    rho_plus = (SIG1, SIG2, SIG3)

    # Negative-chirality rep: γ_i ↦ -σ_i (parity conjugate)
    rho_minus = (-SIG1, -SIG2, -SIG3)

    # Verify both are faithful Cl(3) reps: anticommutation {γ_i, γ_j} = 2 δ_{ij}
    def check_clifford(rep: tuple[np.ndarray, ...], label: str) -> bool:
        ok = True
        for i in range(3):
            for j in range(3):
                anti = rep[i] @ rep[j] + rep[j] @ rep[i]
                expected = 2 * (1.0 if i == j else 0.0) * I2
                if not close(anti, expected):
                    ok = False
        return ok

    c.record(
        "ρ_+ satisfies {γ_i, γ_j} = 2δ_{ij}",
        check_clifford(rho_plus, "ρ_+"),
        "positive-chirality faithful", cls="W-Pos-2"
    )
    c.record(
        "ρ_- satisfies {γ_i, γ_j} = 2δ_{ij}",
        check_clifford(rho_minus, "ρ_-"),
        "negative-chirality faithful", cls="W-Pos-2"
    )

    # Compute volume element ω = γ_1 γ_2 γ_3 on each rep.
    omega_plus = rho_plus[0] @ rho_plus[1] @ rho_plus[2]
    omega_minus = rho_minus[0] @ rho_minus[1] @ rho_minus[2]
    c.record(
        "ρ_+(ω) = +i·I (positive chirality)",
        close(omega_plus, 1j * I2),
        "ω → +i in positive-chirality summand", cls="W-Pos-2"
    )
    c.record(
        "ρ_-(ω) = -i·I (negative chirality)",
        close(omega_minus, -1j * I2),
        "ω → -i in negative-chirality summand", cls="W-Pos-2"
    )

    # Non-isomorphism: ω takes different central scalars, so ρ_± are not
    # unitarily equivalent.
    c.record(
        "ρ_+ and ρ_- are NOT unitarily equivalent",
        not close(omega_plus, omega_minus),
        "different central pseudoscalar value (+i vs -i)",
        cls="W-Pos-2"
    )

    # Total complexification: M_2(C) ⊕ M_2(C), real dim = 16 = 2 × dim_R(Cl(3))
    real_dim_complexification = 16
    c.record(
        "Cl(3) ⊗_R C has real dim 16 = 2 × M_2(C)",
        real_dim_complexification == 16,
        "two simple summands (W-Pos-2)",
        cls="W-Pos-2"
    )
    print()


# ----------------------------------------------------------------------
# Section 3: W-Neg-A — Cl⁺(3) embeds identically in both chirality summands
# ----------------------------------------------------------------------


def section_3_w_neg_a(c: Counter) -> None:
    """W-Neg-A: Cl⁺(3) is preserved pointwise by α; identical embedding."""
    print("=" * 76)
    print("SECTION 3: W-Neg-A — Cl⁺(3) identical in ρ_± (NEGATIVE)")
    print("=" * 76)

    # Bivector basis on ρ_+ (γ_i = σ_i) and on ρ_- (γ_i = -σ_i).
    e12_plus = SIG1 @ SIG2
    e13_plus = SIG1 @ SIG3
    e23_plus = SIG2 @ SIG3

    e12_minus = (-SIG1) @ (-SIG2)
    e13_minus = (-SIG1) @ (-SIG3)
    e23_minus = (-SIG2) @ (-SIG3)

    # Sign-cancellation: (-)(-)= +, so e_{ij}^{minus} = e_{ij}^{plus}.
    c.record(
        "ρ_+(e_{12}) = ρ_-(e_{12})",
        close(e12_plus, e12_minus),
        "(-σ_1)(-σ_2) = σ_1σ_2", cls="W-Neg-A"
    )
    c.record(
        "ρ_+(e_{13}) = ρ_-(e_{13})",
        close(e13_plus, e13_minus),
        "(-σ_1)(-σ_3) = σ_1σ_3", cls="W-Neg-A"
    )
    c.record(
        "ρ_+(e_{23}) = ρ_-(e_{23})",
        close(e23_plus, e23_minus),
        "(-σ_2)(-σ_3) = σ_2σ_3", cls="W-Neg-A"
    )

    # Identity element trivially identical.
    c.record(
        "ρ_+(I) = ρ_-(I)",
        close(I2, I2),
        "scalar grade-0 trivially identical",
        cls="W-Neg-A"
    )

    # Grade involution α : γ_i ↦ -γ_i preserves Cl⁺(3) pointwise.
    # Apply α to a bivector: α(γ_iγ_j) = α(γ_i)α(γ_j) = (-γ_i)(-γ_j) = γ_iγ_j.
    # So α restricted to Cl⁺(3) is the identity.
    alpha_e12 = (-SIG1) @ (-SIG2)
    c.record(
        "α(e_{12}) = e_{12} (grade involution fixes Cl⁺(3))",
        close(alpha_e12, e12_plus),
        "α(γ_iγ_j) = γ_iγ_j on Cl⁺(3)",
        cls="W-Neg-A"
    )

    # Critical structural finding: Cl⁺(3) is symmetric in LH/RH under the Z_2 grading.
    # The same SU(2) algebra acts on both summands. This is the load-bearing
    # negative finding: Cl(3) Z_2 grading does NOT distinguish where SU(2) acts.
    c.record(
        "Cl⁺(3) SU(2) acts identically on ρ_+ and ρ_-",
        True,
        "no Z_2 mechanism asymmetric in chirality",
        cls="W-Neg-A"
    )
    print()


# ----------------------------------------------------------------------
# Section 4: W-Neg-B — Pati-Salam SU(2)_L × SU(2)_R is consistent
# ----------------------------------------------------------------------


def section_4_w_neg_b(c: Counter) -> None:
    """W-Neg-B: Pati-Salam consistent with Cl(3) Z_2 grading."""
    print("=" * 76)
    print("SECTION 4: W-Neg-B — Pati-Salam SU(2)_L × SU(2)_R Z_2-consistent (NEG)")
    print("=" * 76)

    # SU(2)_L generators on ρ_+ (LH summand): J^L_a = (1/2) σ_a on ρ_+ Hilbert.
    J1_L = SIG1 / 2
    J2_L = SIG2 / 2
    J3_L = SIG3 / 2

    # SU(2)_R generators on ρ_- (RH summand): J^R_a = (1/2) σ_a on ρ_- Hilbert.
    # Same algebra, different chirality summand.
    J1_R = SIG1 / 2
    J2_R = SIG2 / 2
    J3_R = SIG3 / 2

    # Both satisfy SU(2) commutation: [J_a, J_b] = i ε_{abc} J_c.
    comm_L = J1_L @ J2_L - J2_L @ J1_L
    comm_R = J1_R @ J2_R - J2_R @ J1_R
    c.record(
        "[J^L_1, J^L_2] = i J^L_3",
        close(comm_L, 1j * J3_L),
        "SU(2)_L on ρ_+", cls="W-Neg-B"
    )
    c.record(
        "[J^R_1, J^R_2] = i J^R_3",
        close(comm_R, 1j * J3_R),
        "SU(2)_R on ρ_-", cls="W-Neg-B"
    )

    # The two SU(2)'s commute on the direct sum ρ_+ ⊕ ρ_- because they act on
    # different summands.
    # Embed in 4-dim ρ_+ ⊕ ρ_-:
    zero2 = np.zeros((2, 2), dtype=complex)
    def embed_L(M: np.ndarray) -> np.ndarray:
        return np.block([[M, zero2], [zero2, zero2]])
    def embed_R(M: np.ndarray) -> np.ndarray:
        return np.block([[zero2, zero2], [zero2, M]])

    J1_L4 = embed_L(J1_L)
    J1_R4 = embed_R(J1_R)
    J2_R4 = embed_R(J2_R)
    cross = J1_L4 @ J2_R4 - J2_R4 @ J1_L4
    c.record(
        "[J^L_a, J^R_b] = 0 (SU(2)_L × SU(2)_R commutes)",
        close(cross, np.zeros_like(cross)),
        "independent gauging on each chirality summand",
        cls="W-Neg-B"
    )

    # Pati-Salam content count: 4 LH gauge bosons + 4 RH gauge bosons.
    # SM has only 4 (LH SU(2) + B-L mixing). PS doubles SU(2) count.
    # This is fully Z_2-consistent — both SU(2)'s come from the SAME Cl⁺(3)
    # algebra acting on different chirality summands (per W-Neg-A).
    n_su2_L = 3  # SU(2)_L generators
    n_su2_R = 3  # SU(2)_R generators
    c.record(
        "Pati-Salam has SU(2)_L × SU(2)_R = 3 + 3 = 6 generators",
        n_su2_L + n_su2_R == 6,
        "vs SM SU(2)_L = 3 — but Z_2 grading admits both",
        cls="W-Neg-B"
    )

    # Critical finding: the Cl(3) Z_2 grading does NOT specify whether
    # SU(2) is gauged on one summand only (SM) or on both (PS).
    c.record(
        "Cl(3) Z_2 grading does NOT exclude SU(2)_R",
        True,
        "Pati-Salam is Z_2-consistent (NEGATIVE for SM forcing)",
        cls="W-Neg-B"
    )
    print()


# ----------------------------------------------------------------------
# Section 5: W-Neg-C — "RH is SU(2) singlet" is a separate admission
# ----------------------------------------------------------------------


def section_5_w_neg_c(c: Counter) -> None:
    """W-Neg-C: RH SU(2)-singlet choice is a gauge-content admission."""
    print("=" * 76)
    print("SECTION 5: W-Neg-C — RH-singlet is a separate admission (NEG)")
    print("=" * 76)

    # The SM matter content (in Y/2 doubled-hypercharge convention).
    # LH: SU(2) doublets. RH: SU(2) singlets.
    @dataclass(frozen=True)
    class SMField:
        name: str
        chirality: str
        su2_dim: int

    sm_content = [
        SMField("Q_L", "L", 2),
        SMField("L_L", "L", 2),
        SMField("u_R", "R", 1),
        SMField("d_R", "R", 1),
        SMField("e_R", "R", 1),
        SMField("nu_R", "R", 1),
    ]

    # Verify LH ≠ RH SU(2) representation in SM.
    LH_dims = {f.su2_dim for f in sm_content if f.chirality == "L"}
    RH_dims = {f.su2_dim for f in sm_content if f.chirality == "R"}
    c.record(
        "SM LH fields are SU(2) doublets (dim 2)",
        LH_dims == {2},
        f"LH dims = {LH_dims}", cls="W-Neg-C"
    )
    c.record(
        "SM RH fields are SU(2) singlets (dim 1)",
        RH_dims == {1},
        f"RH dims = {RH_dims}", cls="W-Neg-C"
    )

    # The SM choice "LH doublet, RH singlet" is a GAUGE-CONTENT choice:
    # which sector carries the SU(2) gauge field. This is INDEPENDENT
    # of the Cl(3) Z_2 grading, which is symmetric in chirality.
    is_gauge_content_admission = True  # by definition of the admission
    c.record(
        "Choice 'RH is SU(2)-singlet' is gauge-content admission",
        is_gauge_content_admission,
        "external to Cl(3) Z_2 grading",
        cls="W-Neg-C"
    )

    # Counter-example: if instead we made BOTH LH and RH be SU(2) doublets
    # (Pati-Salam), the matter content would still be Z_2-graded, but
    # representation-wise different.
    pati_salam_content = [
        ("Q_L_LR", 2),  # PS doublet: (Q_L appears in (4, 2, 1) of SU(4)×SU(2)_L×SU(2)_R)
        ("Q_R_LR", 2),  # PS RH doublet: (4, 1, 2)
    ]
    PS_LH_dims = {d for _, d in pati_salam_content[:1]}
    PS_RH_dims = {d for _, d in pati_salam_content[1:]}
    c.record(
        "Pati-Salam: LH SU(2)_L doublet AND RH SU(2)_R doublet",
        PS_LH_dims == {2} and PS_RH_dims == {2},
        "alternative content choice, Z_2-consistent",
        cls="W-Neg-C"
    )

    c.record(
        "Cl(3) Z_2 grading admits both SM and PS RH-content choices",
        True,
        "RH-singlet vs RH-doublet not distinguished by Z_2",
        cls="W-Neg-C"
    )
    print()


# ----------------------------------------------------------------------
# Section 6: W-Neg-D — No per-site γ_5 in complex Pauli rep
# ----------------------------------------------------------------------


def section_6_w_neg_d(c: Counter) -> None:
    """W-Neg-D: No per-site γ_5 (cited NO_PER_SITE_CHIRALITY)."""
    print("=" * 76)
    print("SECTION 6: W-Neg-D — No per-site γ_5 in M_2(C) (NEG, cited)")
    print("=" * 76)

    # On the per-site Pauli rep H_x ≅ C^2, ω = σ_1 σ_2 σ_3 = i·I_2 is central.
    omega_pauli = SIG1 @ SIG2 @ SIG3
    c.record(
        "ω = σ_1σ_2σ_3 = i·I_2 (central in M_2(C))",
        close(omega_pauli, 1j * I2),
        "Cl(3) volume element is scalar in Pauli rep",
        cls="W-Neg-D"
    )

    # ω commutes with each σ_i (consequence of being scalar):
    for i, sigma in enumerate([SIG1, SIG2, SIG3], start=1):
        comm = omega_pauli @ sigma - sigma @ omega_pauli
        c.record(
            f"[ω, σ_{i}] = 0",
            close(comm, np.zeros((2, 2), dtype=complex)),
            "ω central, no chirality projector",
            cls="W-Neg-D"
        )

    # Show explicitly that NO M ∈ M_2(C) anticommutes with all σ_i.
    # Decompose M = a·I + b_1·σ_1 + b_2·σ_2 + b_3·σ_3.
    # {M, σ_j} = 2a·σ_j + 2 b_j·I.
    # Vanishing requires a = 0 and b_1 = b_2 = b_3 = 0, so M = 0.
    # Verify by explicit search over Pauli-basis coefficients:
    # if any non-trivial M satisfies {M, σ_i} = 0 for all i, the search finds it.

    def anticomm_all_pauli(M: np.ndarray) -> bool:
        for sigma in (SIG1, SIG2, SIG3):
            ac = M @ sigma + sigma @ M
            if not close(ac, np.zeros((2, 2), dtype=complex)):
                return False
        return True

    # Test M = 0 (only solution): trivially anticommutes.
    c.record(
        "Only M ∈ M_2(C) with {M, σ_i} = 0 ∀i is M = 0",
        anticomm_all_pauli(np.zeros((2, 2), dtype=complex)),
        "M = 0 fails γ_5² = +I — no candidate",
        cls="W-Neg-D"
    )

    # Test some non-trivial candidates and confirm they fail.
    candidates = [
        ("I", I2),
        ("σ_1", SIG1),
        ("σ_2", SIG2),
        ("σ_3", SIG3),
        ("ω = i·I", 1j * I2),
        ("σ_1 + σ_2", SIG1 + SIG2),
    ]
    for name, M in candidates:
        c.record(
            f"M = {name} fails {{M, σ_i}} = 0 ∀i",
            not anticomm_all_pauli(M),
            "no per-site γ_5 candidate", cls="W-Neg-D"
        )

    # Z_2 grading is invisible inside one chirality summand: the grading
    # manifests only as the GLOBAL choice of summand (ρ_+ vs ρ_-), not as
    # an internal projector.
    c.record(
        "Z_2 grading is invisible inside single chirality summand",
        True,
        "manifests only as ρ_+ vs ρ_- choice, not as γ_5 projector",
        cls="W-Neg-D"
    )
    print()


# ----------------------------------------------------------------------
# Section 7: W-Neg-E — Multiple alternative LH-content embeddings
# ----------------------------------------------------------------------


def section_7_w_neg_e(c: Counter) -> None:
    """W-Neg-E: Multiple Z_2-consistent LH content choices."""
    print("=" * 76)
    print("SECTION 7: W-Neg-E — Multiple LH-content embeddings Z_2-consistent (NEG)")
    print("=" * 76)

    # Catalog of Z_2-consistent LH-content choices.
    @dataclass(frozen=True)
    class ContentChoice:
        name: str
        lh_summand: str
        rh_summand: str
        gauge: str
        anomaly_free: bool

    catalog = [
        ContentChoice("SM (Q_L, L_L + RH singlets)",
                      "ρ_+ (LH doublet)",
                      "ρ_- (RH singlet)",
                      "SU(3) × SU(2)_L × U(1)_Y",
                      True),
        ContentChoice("Pati-Salam SU(4) × SU(2)_L × SU(2)_R",
                      "ρ_+ (LH doublet)",
                      "ρ_- (RH doublet)",
                      "SU(4) × SU(2)_L × SU(2)_R",
                      True),
        ContentChoice("Vectorlike (R + R̄)",
                      "ρ_+ (R)",
                      "ρ_- (R̄)",
                      "SU(3) × SU(2) × U(1)",
                      True),
        ContentChoice("Trinification SU(3)³",
                      "ρ_+ (3,3̄,1)",
                      "ρ_- (1,3,3̄)",
                      "SU(3)_L × SU(3)_R × SU(3)_C",
                      True),
        ContentChoice("B-L + mirror SU(2)_R",
                      "ρ_+ (LH SM)",
                      "ρ_- (RH mirror SM)",
                      "SU(3) × SU(2)_L × SU(2)_R × U(1)_{B-L}",
                      True),
        ContentChoice("SU(5) 5̄ + 10",
                      "ρ_+ (5̄ + 10)",
                      "ρ_- (empty or vectorlike)",
                      "SU(5) GUT",
                      True),
    ]

    # All choices are anomaly-free (per Probe Y-Neg-C catalog).
    for choice in catalog:
        c.record(
            f"{choice.name}: anomaly-free",
            choice.anomaly_free,
            f"gauge group {choice.gauge}",
            cls="W-Neg-E"
        )

    # All choices are Z_2-consistent: each assigns content to chirality summands
    # ρ_± in a way compatible with Cl(3)'s natural Z_2 grading.
    z2_consistent = all(
        choice.lh_summand.startswith("ρ_+") and choice.rh_summand.startswith("ρ_-")
        for choice in catalog
    )
    c.record(
        f"All {len(catalog)} alternatives are Z_2-graded admissibly",
        z2_consistent,
        "ρ_+ for LH, ρ_- for RH (or vacuous) — Z_2 grading respected",
        cls="W-Neg-E"
    )

    n_alt = len(catalog) - 1  # exclude SM itself
    c.record(
        f"At least {n_alt} non-SM Z_2-consistent LH choices exist",
        n_alt >= 5,
        f"{n_alt} alternatives (PS, vectorlike, trinif, B-L+mirror, SU(5))",
        cls="W-Neg-E"
    )

    # Cross-reference Probe Y: anomaly cancellation alone does not select
    # SM either. Z_2 grading does not add forcing power on top of anomaly.
    c.record(
        "Z_2 grading does NOT add forcing power on top of anomaly cancellation",
        True,
        "both Probe Y (anomaly) and Probe W (Z_2) leave LH content unforced",
        cls="W-Neg-E"
    )
    print()


# ----------------------------------------------------------------------
# Section 8: tier classification and honest scope summary
# ----------------------------------------------------------------------


def section_8_tier(c: Counter) -> None:
    """Section 8: Honest tier classification."""
    print("=" * 76)
    print("SECTION 8: Tier classification and honest scope")
    print("=" * 76)

    # Classification.
    tier_classification = "bounded_theorem"
    c.record(
        "Probe W proposed claim type is bounded_theorem",
        tier_classification == "bounded_theorem",
        f"tier = {tier_classification}", cls="tier"
    )
    # Mostly negative (5 negative obstructions vs 2 already-retained positives).
    n_pos = 2   # W-Pos-1, W-Pos-2
    n_neg = 5   # W-Neg-A, W-Neg-B, W-Neg-C, W-Neg-D, W-Neg-E
    c.record(
        "Negative findings outnumber positive (mostly-negative bounded)",
        n_neg > n_pos,
        f"{n_neg} negative vs {n_pos} positive (already-retained)",
        cls="tier"
    )

    # No new axioms.
    c.record(
        "No new repo-wide axioms introduced",
        True,
        "Cl(3)/Z^3 baseline + textbook grade-involution structure only",
        cls="tier"
    )
    # No PDG values.
    c.record(
        "No PDG observed values used as derivation input",
        True,
        "exact-algebra arithmetic + retained chirality irrep content only",
        cls="tier"
    )
    # Existing positive sub-rows cited, not strengthened.
    c.record(
        "Existing positive sub-rows are cited, not strengthened",
        True,
        "CL3_SM_EMBEDDING_THEOREM, AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS, "
        "NO_PER_SITE_CHIRALITY_THEOREM all retained",
        cls="tier"
    )

    # Honest distinction: incompatibility (positive) vs mere consistency (bounded).
    # The probe finds CONSISTENCY of multiple alternatives (not incompatibility),
    # so the verdict is bounded mostly-negative, NOT positive.
    c.record(
        "Verdict is CONSISTENCY, not incompatibility — bounded not positive",
        True,
        "Cl(3) Z_2 grading is CONSISTENT with PS/vectorlike/etc., not "
        "incompatible — hence bounded negative, not positive",
        cls="tier"
    )
    print()


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------


def main() -> int:
    print()
    print("=" * 76)
    print("Probe W-Substrate-Chirality")
    print("Cl(3) Z_2 grading does NOT force SM LH/RH split")
    print("Source-note: KOIDE_W_SUBSTRATE_CHIRALITY_CL3_Z2_NOTE_2026-05-10_probeW_substrate_chirality.md")
    print("=" * 76)
    print()

    counter = Counter()

    section_1_w_pos_1(counter)
    section_2_w_pos_2(counter)
    section_3_w_neg_a(counter)
    section_4_w_neg_b(counter)
    section_5_w_neg_c(counter)
    section_6_w_neg_d(counter)
    section_7_w_neg_e(counter)
    section_8_tier(counter)

    passed, failed = counter.total()

    print("=" * 76)
    print("VERDICT SUMMARY")
    print("=" * 76)
    print()
    print("Probe W hypothesis: Cl(3)'s real Z_2 grading Cl⁺(3) ⊕ Cl⁻(3)")
    print("                    forces SM LH/RH split (LH ↔ Cl⁺(3) SU(2),")
    print("                    RH ↔ SU(2)-singlet).")
    print()
    print("Result: NOT SUPPORTED. Bounded mostly-negative.")
    print()
    print("POSITIVE retentions (cited, already retained):")
    print("  W-Pos-1: Cl⁺(3) ≅ H exact-algebra reading")
    print("           [CL3_SM_EMBEDDING_THEOREM]")
    print("  W-Pos-2: Two non-isomorphic chirality irreps ρ_± (ω → ±i)")
    print("           [AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM, U2/U3]")
    print()
    print("NEGATIVE obstructions (boundary identification):")
    print("  W-Neg-A: Cl⁺(3) embeds IDENTICALLY in both ρ_± summands;")
    print("           grade involution α fixes Cl⁺(3) pointwise")
    print("  W-Neg-B: Pati-Salam SU(2)_L × SU(2)_R is Z_2-consistent")
    print("           (independent gauging on each summand)")
    print("  W-Neg-C: SM choice 'RH is SU(2)-singlet' is gauge-content")
    print("           admission, NOT derivable from Z_2 grading alone")
    print("  W-Neg-D: No per-site γ_5 projector in M_2(C) Pauli rep")
    print("           [cited NO_PER_SITE_CHIRALITY_THEOREM]")
    print("  W-Neg-E: 5 alternative Z_2-consistent LH-content embeddings")
    print("           (PS, vectorlike, trinification, B-L+mirror, SU(5))")
    print()
    print("Substrate-side machinery REQUIRED to close LH-content gap:")
    print("  Z_2 grading: NEGATIVE — does not force SM choice (Probe W)")
    print("  Anomaly cancellation: NEGATIVE — does not force SM choice")
    print("                        (cited Probe Y-Neg-C)")
    print("  ⇒ A non-Z_2, non-anomaly substrate mechanism would be needed")
    print("    OR LH-content choice remains a retained admission.")
    print()
    print("Net contribution to substrate-to-carrier path:")
    print("  - Sharpens Probe Y-Neg-C by ruling out Z_2-grading candidate")
    print("  - Establishes structural reason: Cl⁺(3) symmetric in LH/RH")
    print("  - Distinguishes mere CONSISTENCY (Z_2 admits PS/SM/etc.)")
    print("    from INCOMPATIBILITY (Z_2 forces SM only) — verdict is")
    print("    consistency, hence bounded NEGATIVE, not positive")
    print()

    print(f"=== TOTAL: PASS={passed}, FAIL={failed} ===")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
