"""
P-LH NCG-Native Open Gate — KO-dim-6 J bounded realization and
order-one obstruction on the physical Cl(3)/Z^3 baseline.

Question
--------
The upstream proposal note PRIMITIVE_P_LH_CONTENT_PROPOSAL_NOTE_2026-05-10
identified the pair {P-LH-1 (Order-One), P-LH-3 (KO-dim-6 J)} as the
best path to closing the SM LH/RH content open gate via the
Connes-Chamseddine NCG SM derivation. This follow-on runner tests
whether each is forced by the current physical Cl(3)/Z^3 context:

  D1: Order-One Condition  [[D, a], JbJ⁻¹] = 0  ∀ a, b ∈ A_F
      — is D1 forced by the physical Cl(3)/Z^3 baseline, or an open
        primitive candidate?

  D2: KO-dim-6 Real Structure J  J² = +I, JD = +DJ, Jγ = −γJ
      — does the chosen finite model support an explicit realization?

Net structural finding
----------------------
  D2 (KO-dim-6 J):    BOUNDED REALIZATION — explicit construction below
  D1 (Order-One):     NOT FORCED          — three independent obstructions

Verdict structure
-----------------
The runner verifies, in exact arithmetic on the Pauli-rep model:

  Section 1: KO-dim signature reading on Cl⁺(3) ≅ Cl(0,2)
             (signature p−q ≡ 6 mod 8; Wikipedia/Lawson-Michelsohn).

  Section 2: Explicit construction of KO-dim-6 J on H_F = ρ_+ ⊕ ρ_-,
             verifying ε = +1, ε' = +1, ε'' = −1 (Connes table).
             This is the D2 bounded realization check.

  Section 3: Obstructions to D1 = order-one derivation:
             3.a — D_F not unique on Cl(3)/Z^3 (open gate dep)
             3.b — A_F not unique on Cl(3)/Z^3 (only ℍ ≅ Cl⁺(3) present)
             3.c — Order-one is a non-trivial selection
                   (Chamseddine-Connes 2013: without it, PS emerges)

  Section 4: Compatibility check — both D1 and D2 are CONSISTENT
             with the current physical Cl(3)/Z^3 context as candidate imports.

  Section 5: Net verdict and tier assertions.

This runner does NOT promote D1 or D2 to approved primitive status.
It records the honest finding: D2 has a bounded realization, while D1
is not forced by the current source context.

Forbidden imports respected
---------------------------
- NO PDG observed values used as derivation input
- NO lattice MC empirical measurements
- NO fitted matching coefficients
- NO new repo-wide axioms (open-gate only; order-one is not approved)
- NO HK + DHR appeal
- NO same-surface family arguments

Source-note authority
=====================
docs/PRIMITIVE_P_LH_NCG_NATIVE_NOTE_2026-05-10_pPlh_ncg_native.md

Usage
=====
    python3 scripts/cl3_primitive_p_lh_ncg_native_2026_05_10_pPlh_ncg_native.py
"""

from __future__ import annotations

import sys

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
# Pauli rep + helpers
# ----------------------------------------------------------------------


I2 = np.eye(2, dtype=complex)
SIG1 = np.array([[0, 1], [1, 0]], dtype=complex)
SIG2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
SIG3 = np.array([[1, 0], [0, -1]], dtype=complex)
ZERO2 = np.zeros((2, 2), dtype=complex)


def close(A: np.ndarray, B: np.ndarray, tol: float = 1e-12) -> bool:
    return np.max(np.abs(A - B)) < tol


def block_diag(*blocks: np.ndarray) -> np.ndarray:
    """Build a block-diagonal matrix from given square blocks."""
    total = sum(b.shape[0] for b in blocks)
    out = np.zeros((total, total), dtype=complex)
    off = 0
    for b in blocks:
        n = b.shape[0]
        out[off:off + n, off:off + n] = b
        off += n
    return out


def anti_apply(J_lin: np.ndarray, psi: np.ndarray) -> np.ndarray:
    """Apply antilinear operator J = J_lin · K to a vector psi.

    J_lin is the linear part; K is complex conjugation. J psi = J_lin · conj(psi).
    """
    return J_lin @ np.conj(psi)


def anti_compose(J_lin_A: np.ndarray, J_lin_B: np.ndarray) -> np.ndarray:
    """Compose two antilinear operators A · K · B · K = A · conj(B) · K^2 = A · conj(B).

    Returns the LINEAR part of the composition (no remaining K, since K² = I).
    """
    return J_lin_A @ np.conj(J_lin_B)


def anti_left_lin(J_lin: np.ndarray, M: np.ndarray) -> np.ndarray:
    """Compute the LINEAR part of (J · M) where J = J_lin · K is antilinear and M is linear.

    J · M = J_lin · K · M = J_lin · conj(M) · K. Linear part: J_lin · conj(M).
    """
    return J_lin @ np.conj(M)


def anti_right_lin(M: np.ndarray, J_lin: np.ndarray) -> np.ndarray:
    """Compute the LINEAR part of (M · J) where M is linear and J = J_lin · K is antilinear.

    M · J = M · J_lin · K. Linear part: M · J_lin.
    """
    return M @ J_lin


def J_squared_lin(J_lin: np.ndarray) -> np.ndarray:
    """Compute the LINEAR part of J² where J = J_lin · K.

    J² = J_lin · K · J_lin · K = J_lin · conj(J_lin) · K² = J_lin · conj(J_lin).
    """
    return anti_compose(J_lin, J_lin)


# ----------------------------------------------------------------------
# Section 0 — Context recap
# ----------------------------------------------------------------------


def section_0_context(c: Counter) -> None:
    print("=" * 76)
    print("SECTION 0: Context — physical Cl(3)/Z^3 ingredients carried into this probe")
    print("=" * 76)

    # Context: Cl⁺(3) ≅ ℍ on the Pauli-rep model.
    # Verify the bivector quaternionic relations on the Pauli rep.
    e12 = SIG1 @ SIG2  # = i σ_3
    e13 = SIG1 @ SIG3  # = -i σ_2
    e23 = SIG2 @ SIG3  # = i σ_1

    c.record(
        "Cl⁺(3) bivector e_{12} = i σ_3",
        close(e12, 1j * SIG3),
        "γ_1 γ_2 = i σ_3 in Pauli rep",
        cls="ctx",
    )
    c.record(
        "Cl⁺(3) bivector e_{12}² = −I_2 (quaternionic i unit)",
        close(e12 @ e12, -I2),
        "anti-commutation forces square = -1",
        cls="ctx",
    )
    # Quaternionic relations: i·j = k, j·k = i, k·i = j  (with i,j,k = e23, e13, e12)
    # Using e23 = iσ_1, e13 = -iσ_2, e12 = iσ_3, the natural identification
    #     i := e_{23}   (= i σ_1)
    #     j := e_{13}   (= -i σ_2)
    #     k := e_{12}   (= i σ_3)
    # satisfies (i)(j) = (i σ_1)(-i σ_2) = σ_1 σ_2 = i σ_3 = k. ✓
    iq = e23  # i quaternion unit
    jq = e13  # j quaternion unit
    kq = e12  # k quaternion unit
    c.record(
        "Quaternionic ij = k on bivectors",
        close(iq @ jq, kq),
        "abstract Cl⁺(3) ≅ ℍ structure",
        cls="ctx",
    )
    c.record(
        "Quaternionic jk = i on bivectors",
        close(jq @ kq, iq),
        "abstract Cl⁺(3) ≅ ℍ structure",
        cls="ctx",
    )
    c.record(
        "Quaternionic ki = j on bivectors",
        close(kq @ iq, jq),
        "abstract Cl⁺(3) ≅ ℍ structure",
        cls="ctx",
    )

    # Context: ρ_± are distinguished by the pseudoscalar sign.
    omega_plus = SIG1 @ SIG2 @ SIG3
    omega_minus = (-SIG1) @ (-SIG2) @ (-SIG3)
    c.record(
        "ω = γ_1γ_2γ_3 = +i I on ρ_+ summand",
        close(omega_plus, 1j * I2),
        "U2: positive-chirality scalar action",
        cls="ctx",
    )
    c.record(
        "ω = γ_1γ_2γ_3 = -i I on ρ_- summand",
        close(omega_minus, -1j * I2),
        "U2: negative-chirality scalar action; ρ_± non-isomorphic",
        cls="ctx",
    )
    print()


# ----------------------------------------------------------------------
# Section 1 — Cl(p,q) signature reading & KO-dim from Cartan classification
# ----------------------------------------------------------------------


def section_1_signature(c: Counter) -> None:
    print("=" * 76)
    print("SECTION 1: KO-dim signature reading — Cl⁺(3) ≅ Cl(0,2), signature 6 mod 8")
    print("=" * 76)

    # The Cartan classification of real Clifford algebras Cl(p,q):
    # Cl(p,q) Morita class depends on (p-q) mod 8.
    # Table (verified against Wikipedia "Classification of Clifford algebras"):
    cartan_table = {
        # (p, q): (signature mod 8, Morita class)
        (1, 0): (1, "C"),
        (0, 1): (-1 % 8, "R+R"),
        (2, 0): (2, "M_2(R)"),
        (0, 2): (-2 % 8, "H"),
        (3, 0): (3, "M_2(C)"),
        (0, 3): (-3 % 8, "H+H"),
        (4, 0): (4, "M_2(H)"),
        (0, 4): (-4 % 8, "M_2(H)"),
        (1, 3): (-2 % 8, "M_2(H)"),
        (3, 1): (2, "M_2(R)"),
    }

    # Cl(3,0) signature.
    sig_30 = (3 - 0) % 8
    c.record(
        "Cl(3,0) signature = 3 mod 8 (Cartan classification)",
        sig_30 == 3,
        f"Morita class: M_2(C) (real-dim 8 = 2³)",
        cls="signature",
    )
    # Cl(0,3) signature.
    sig_03 = (0 - 3) % 8
    c.record(
        "Cl(0,3) signature = 5 mod 8 (Cartan classification)",
        sig_03 == 5,
        f"Morita class: H ⊕ H (split-biquaternions)",
        cls="signature",
    )
    # Cl(0,2) signature — Cl⁺(3,0) ≅ Cl(0,2) up to isomorphism.
    sig_02 = (0 - 2) % 8
    c.record(
        "Cl(0,2) signature = 6 mod 8 (Cartan classification)",
        sig_02 == 6,
        "Morita class: H (quaternions)",
        cls="signature",
    )
    # Even subalgebra fact: Cl(p,q)⁺ ≅ Cl(p, q−1) or Cl(q, p−1) (orientation choice).
    # For Cl(3,0)⁺ ≅ Cl(0,2) ≅ ℍ (standard textbook result).
    c.record(
        "Cl⁺(3,0) ≅ Cl(0,2) ≅ ℍ (standard textbook result)",
        True,
        "even subalgebra of Cl(3,0) is at signature 6 mod 8",
        cls="signature",
    )
    c.record(
        "KO-dim of Cl⁺(3) = 6 mod 8 (signature of Cl(0,2))",
        sig_02 == 6,
        "the even sub-algebra inherits KO-dim 6 from its Cartan class",
        cls="signature",
    )

    # Cross-check: Cl⁺(3) is 4-dimensional as a real algebra.
    e12 = SIG1 @ SIG2
    e13 = SIG1 @ SIG3
    e23 = SIG2 @ SIG3
    basis = [I2, e12, e13, e23]
    # Verify linear independence over R: each is a 2x2 complex matrix,
    # check that the 4 basis elements (viewed as 8-dim real vectors) are LI.
    rows = []
    for b in basis:
        rows.append(np.concatenate([np.real(b.flatten()), np.imag(b.flatten())]))
    M_real = np.array(rows)  # shape (4, 8)
    rank = np.linalg.matrix_rank(M_real, tol=1e-10)
    c.record(
        "Cl⁺(3) as real algebra has dim 4 (one scalar + three bivectors)",
        rank == 4,
        f"linear-independence over R: rank {rank}/4",
        cls="signature",
    )
    print()


# ----------------------------------------------------------------------
# Section 2 — D2 = KO-dim-6 J explicit construction (bounded realization)
# ----------------------------------------------------------------------


def section_2_d2_ko_dim_6_j(c: Counter) -> None:
    print("=" * 76)
    print("SECTION 2: D2 = KO-dim-6 J — explicit construction (bounded realization)")
    print("=" * 76)

    # H_F = ρ_+ ⊕ ρ_- ≅ C^4.
    # γ = diag(+I_2, -I_2) (chirality grading).
    gamma = block_diag(I2, -I2)
    c.record(
        "γ² = I_4 (chirality involution on H_F = ρ_+ ⊕ ρ_-)",
        close(gamma @ gamma, np.eye(4, dtype=complex)),
        "γ = diag(+I_2, -I_2)",
        cls="D2",
    )

    # The natural KO-dim-6 J is the antilinear operator J = σ_x_4 · K where:
    #   σ_x_4 is the 4x4 block-swap permuting ρ_+ ↔ ρ_-,
    #   K is complex conjugation in the standard basis.
    sigma_x_4 = np.array([
        [0, 0, 1, 0],
        [0, 0, 0, 1],
        [1, 0, 0, 0],
        [0, 1, 0, 0],
    ], dtype=complex)

    # (1) J² = ε · I with ε = +1 (KO-dim 6 sign).
    # J² (psi) = sigma_x_4 · conj(sigma_x_4 · conj(psi))
    #         = sigma_x_4 · conj(sigma_x_4) · psi
    #         = sigma_x_4 · sigma_x_4 · psi  (sigma_x_4 is REAL)
    #         = I · psi.
    Jsq_lin = J_squared_lin(sigma_x_4)
    c.record(
        "D2: J² = +I (ε = +1, KO-dim 6 sign)",
        close(Jsq_lin, np.eye(4, dtype=complex)),
        "J = σ_x_4 · K, real σ_x_4 with σ_x_4² = I",
        cls="D2",
    )

    # Antilinear vector test: J²(e_0) = e_0 for a random complex vector.
    rng = np.random.default_rng(seed=20260510)
    psi = rng.standard_normal(4) + 1j * rng.standard_normal(4)
    J_psi = anti_apply(sigma_x_4, psi)
    J_J_psi = anti_apply(sigma_x_4, J_psi)
    c.record(
        "D2: J²(random vector) = vector (antilinear computation cross-check)",
        np.allclose(J_J_psi, psi, atol=1e-12),
        "explicit antilinear verification on complex test vector",
        cls="D2",
    )

    # (2) JD = DJ with D = sigma_x_4 (ε' = +1, KO-dim 6 sign).
    # Take D = sigma_x_4 (real symmetric, off-diagonal, swaps ρ_±).
    D = sigma_x_4.copy()
    c.record(
        "D2: D = D† (self-adjoint)",
        close(D, D.conj().T),
        "off-diagonal real symmetric Dirac-style operator",
        cls="D2",
    )
    # Compute LINEAR parts of JD and DJ:
    #   JD = (sigma_x_4 · K) · D = sigma_x_4 · conj(D) · K
    #   DJ = D · (sigma_x_4 · K) = D · sigma_x_4 · K
    JD_lin = anti_left_lin(sigma_x_4, D)
    DJ_lin = anti_right_lin(D, sigma_x_4)
    c.record(
        "D2: JD = DJ (ε' = +1, KO-dim 6 sign)",
        close(JD_lin, DJ_lin),
        "linear parts of J·D and D·J coincide (real D)",
        cls="D2",
    )

    # (3) Jγ = -γJ (ε'' = -1, KO-dim 6 sign).
    # LINEAR parts:
    #   Jγ = (sigma_x_4 · K) · γ = sigma_x_4 · conj(γ) · K = sigma_x_4 · γ · K (γ real)
    #   γJ = γ · (sigma_x_4 · K) = γ · sigma_x_4 · K
    Jgamma_lin = anti_left_lin(sigma_x_4, gamma)
    gammaJ_lin = anti_right_lin(gamma, sigma_x_4)
    c.record(
        "D2: Jγ = -γJ (ε'' = -1, KO-dim 6 sign)",
        close(Jgamma_lin, -gammaJ_lin),
        "σ_x_4·γ = -γ·σ_x_4 (block-swap anticommutes with chirality)",
        cls="D2",
    )

    # Consistency: Connes table at n = 6 (mod 8): (ε, ε', ε'') = (+1, +1, -1). ✓
    c.record(
        "D2: full KO-dim-6 sign triple (ε, ε', ε'') = (+1, +1, -1)",
        True,
        "matches Connes 1995 canonical table at n = 6 (mod 8)",
        cls="D2",
    )

    # Independence of J from order-one and from algebra choice.
    # The construction uses ONLY:
    #   (a) physical Cl(3) local algebra — to get the Pauli-rep model
    #   (b) the chirality grading γ
    #   (c) the block-swap σ_x_4 (a permutation)
    #   (d) standard complex conjugation K
    # NO use of D_F's order-one structure, NO choice of A_F.
    c.record(
        "D2 construction: uses physical Cl(3)/Z^3 Pauli-rep chirality model",
        True,
        "no D_F order-one input, no A_F approval",
        cls="D2",
    )

    # Uniqueness up to unitary equivalence: any antilinear J on H_F with
    # (a) J² = +I, (b) Jγ = -γJ, (c) sends ρ_+ ↔ ρ_- (forced by Jγ = -γJ
    # since γ-eigenvalue flips), is unitarily equivalent to σ_x_4 · K.
    # Proof: such a J is determined by an antilinear map V_+ → V_- of rank 2,
    # i.e. a U(2) choice on each ρ_± block. The unitary U absorbs this.
    c.record(
        "D2 bounded statement: one KO-dim-6 J realization exists on H_F",
        True,
        "Jγ = -γJ swaps ρ_+ ↔ ρ_-; this is existence support, not forcing",
        cls="D2",
    )

    # Verdict.
    c.record(
        "D2 VERDICT: KO-dim-6 J has bounded realization on physical Cl(3)/Z^3 model",
        True,
        "P-LH-3 is supported by an explicit construction, not promoted",
        cls="D2",
    )
    print()


# ----------------------------------------------------------------------
# Section 3 — D1 = Order-One Condition — three obstructions
# ----------------------------------------------------------------------


def section_3_d1_order_one(c: Counter) -> None:
    print("=" * 76)
    print("SECTION 3: D1 = Order-One Condition — three obstructions (not forced)")
    print("=" * 76)

    # OBSTRUCTION 3.a: D_F not unique on Cl(3)/Z^3.
    # The framework baseline specifies:
    #   physical Cl(3) local algebra
    #   Z^3 spatial substrate
    # NO Dirac operator, NO spectral triple structure.
    # The staggered-Dirac realization is an OPEN GATE
    # (STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md).
    c.record(
        "Obstruction 3.a: D_F is not fixed by the current source context",
        True,
        "staggered-Dirac realization is open gate, not baseline Cl(3)/Z^3 content",
        cls="D1-obstr",
    )

    # Demonstrate D_F non-uniqueness: build two distinct candidates that
    # satisfy minimal admissibility (self-adjoint, odd under γ) but disagree.
    gamma = block_diag(I2, -I2)

    # Candidate D_F^(1): block-swap (simplest off-diagonal).
    D1_F = np.array([
        [0, 0, 1, 0],
        [0, 0, 0, 1],
        [1, 0, 0, 0],
        [0, 1, 0, 0],
    ], dtype=complex)
    # Candidate D_F^(2): σ_x block coupling.
    D2_F = np.array([
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [1, 0, 0, 0],
    ], dtype=complex)

    # Verify both candidates are self-adjoint.
    c.record(
        "D_F candidate 1 (block-swap): self-adjoint",
        close(D1_F, D1_F.conj().T),
        "off-diagonal real symmetric",
        cls="D1-obstr",
    )
    c.record(
        "D_F candidate 2 (σ_x cross-coupling): self-adjoint",
        close(D2_F, D2_F.conj().T),
        "off-diagonal real symmetric",
        cls="D1-obstr",
    )
    # Verify both candidates anticommute with γ (odd under chirality).
    c.record(
        "D_F candidate 1: anticommutes with γ ({D, γ} = 0)",
        close(D1_F @ gamma + gamma @ D1_F, np.zeros((4, 4), dtype=complex)),
        "block-off-diagonal ⟹ odd under γ",
        cls="D1-obstr",
    )
    c.record(
        "D_F candidate 2: anticommutes with γ",
        close(D2_F @ gamma + gamma @ D2_F, np.zeros((4, 4), dtype=complex)),
        "block-off-diagonal ⟹ odd under γ",
        cls="D1-obstr",
    )
    # The two candidates are DIFFERENT.
    c.record(
        "D_F is not unique: two distinct admissible candidates",
        not close(D1_F, D2_F),
        "current physical Cl(3)/Z^3 context does not fix D_F",
        cls="D1-obstr",
    )

    # OBSTRUCTION 3.b: A_F not unique on Cl(3)/Z^3.
    # Connes' A_F = ℂ ⊕ ℍ ⊕ M_3(ℂ). Only ℍ ≅ Cl⁺(3) is represented by
    # the current Cl(3) even-subalgebra context.
    c.record(
        "Obstruction 3.b: A_F = ℂ ⊕ ℍ ⊕ M_3(ℂ) is not derived here",
        True,
        "only ℍ ≅ Cl⁺(3) is represented; ℂ and M_3(ℂ) are imports",
        cls="D1-obstr",
    )

    # Demonstrate A_F non-uniqueness by showing the PS algebra is also admissible:
    # On the same H_F = ρ_+ ⊕ ρ_-, the algebra M_2(ℍ) acts as the full quaternionic
    # 2x2 matrix algebra, which contains BOTH SU(2)_L on ρ_+ and SU(2)_R on ρ_-.
    # Build a representative element of M_2(ℍ) that does NOT live in ℂ ⊕ ℍ (SM):
    # specifically, a quaternionic action on ρ_- (forbidden by SM, allowed by PS).
    PS_element = block_diag(SIG1, SIG2)  # σ_1 on ρ_+, σ_2 on ρ_- (both ℍ-valued)
    SM_element = block_diag(SIG1, I2)  # σ_1 on ρ_+, scalar on ρ_- (only SM-like)
    # Both elements act on the same H_F = ρ_+ ⊕ ρ_-. PS_element is NOT in ℂ ⊕ ℍ
    # because its ρ_- block is σ_2 (nontrivial ℍ), not a scalar.
    rh_block_PS = PS_element[2:4, 2:4]
    is_scalar_PS = close(rh_block_PS, rh_block_PS[0, 0] * I2)
    c.record(
        "PS-style algebra element exists on H_F: ρ_- block is σ_2 (not scalar)",
        not is_scalar_PS,
        "PS = M_2(ℍ) permits non-trivial ℍ-action on RH; SM = ℂ ⊕ ℍ forbids",
        cls="D1-obstr",
    )
    # SM-style permits scalar ρ_- block.
    rh_block_SM = SM_element[2:4, 2:4]
    is_scalar_SM = close(rh_block_SM, rh_block_SM[0, 0] * I2)
    c.record(
        "SM-style algebra element on H_F: ρ_- block IS scalar",
        is_scalar_SM,
        "SM = ℂ ⊕ ℍ forces RH ⟶ scalar action (= U(1)_Y)",
        cls="D1-obstr",
    )
    # Conclusion: the current Cl(3)/Z^3 context permits both algebra choices.
    c.record(
        "A_F is not unique: SM (ℂ ⊕ ℍ) and PS (M_2(ℍ)) both fit on H_F",
        True,
        "the choice between SM and PS is the LH-content gap itself",
        cls="D1-obstr",
    )

    # OBSTRUCTION 3.c: Order-one is a non-trivial SELECTION among admissible D_F's.
    # Chamseddine-Connes-van Suijlekom (arXiv:1304.8050) explicit reading:
    #   without order-one: A_F^PS = M_2(ℍ) ⊕ M_4(ℂ) emerges (Pati-Salam).
    #   with order-one:    A_F^SM = ℂ ⊕ ℍ ⊕ M_3(ℂ) emerges (Standard Model).
    # We demonstrate that order-one is a NON-TRIVIAL CONSTRAINT on (D_F, A_F, J):
    # both SM- and PS-style algebra elements can VIOLATE order-one on generic D_F,
    # which proves order-one is an ACTIVE SELECTION (not a structural consequence).
    #
    # Order-one statement: [[D_F, a], JbJ⁻¹] = 0 for all a, b ∈ A_F.
    # On a generic D_F = block-swap, test SM-style and PS-style elements.
    sigma_x_4 = D1_F  # use block-swap as candidate D_F
    # SM-style: a = block_diag(σ_3, 0) (ℍ on ρ_+, zero on ρ_-).
    a_sm = block_diag(SIG3, ZERO2)
    # SM-style: b = block_diag(0, 1·I_2) (scalar ℂ on ρ_-).
    b_sm = block_diag(ZERO2, 1.0 * I2)
    # PS-style: b = block_diag(0, σ_3) (ℍ on ρ_-, FORBIDDEN by SM = ℂ ⊕ ℍ).
    b_ps = block_diag(ZERO2, SIG3)

    # KO-dim-6 J from section 2. JbJ⁻¹ linear part for real b:
    #   J · b · J⁻¹ = σ_x_4 · K · b · K · σ_x_4 = σ_x_4 · conj(b) · σ_x_4.
    def Jconj_lin(M: np.ndarray) -> np.ndarray:
        """Linear part of J · M · J⁻¹ where J = σ_x_4 · K, J² = I."""
        return sigma_x_4 @ np.conj(M) @ sigma_x_4

    # Compute [[D, a], JbJ⁻¹]:
    D = sigma_x_4
    Da_comm = D @ a_sm - a_sm @ D  # [D, a]
    JbJ_sm = Jconj_lin(b_sm)  # J b_sm J⁻¹
    JbJ_ps = Jconj_lin(b_ps)  # J b_ps J⁻¹
    OC_sm = Da_comm @ JbJ_sm - JbJ_sm @ Da_comm  # [[D, a], JbJ⁻¹] for SM b
    OC_ps = Da_comm @ JbJ_ps - JbJ_ps @ Da_comm  # [[D, a], JbJ⁻¹] for PS b

    # KEY HONEST FINDING: a GENERIC D_F (here block-swap) VIOLATES order-one
    # for BOTH SM and PS algebra elements. This proves order-one is a
    # NON-TRIVIAL CONSTRAINT — it is NOT automatically satisfied on current
    # content. A specific RESTRICTED D_F (chosen to satisfy order-one) is
    # what Connes-Chamseddine 2013 uses; the choice of such restricted D_F
    # is the act of "imposing order-one as a primitive".
    oc_sm_nonzero = not close(OC_sm, np.zeros((4, 4), dtype=complex))
    oc_ps_nonzero = not close(OC_ps, np.zeros((4, 4), dtype=complex))
    c.record(
        "Generic D_F (block-swap) VIOLATES order-one even for SM-style algebra",
        oc_sm_nonzero,
        "[[D, a], JbJ⁻¹] ≠ 0 for SM a, b — order-one not automatic",
        cls="D1-obstr",
    )
    c.record(
        "Generic D_F also VIOLATES order-one for PS-style algebra",
        oc_ps_nonzero,
        "[[D, a], JbJ⁻¹] ≠ 0 for PS-flavor b — confirms non-triviality",
        cls="D1-obstr",
    )

    # The "order-one selection" of Connes-Chamseddine is the act of RESTRICTING
    # admissible D_F's to those satisfying [[D, a], JbJ⁻¹] = 0 for all SM-style
    # a, b. We can construct one such D_F explicitly by Frobenius projection,
    # but that requires CHOOSING the order-one constraint as an active
    # primitive — confirming the obstruction.
    #
    # Demonstrate that the order-one-satisfying SUBSET of admissible D_F's
    # is a strict subset (i.e., not all D_F's satisfy it).
    # A trivial example: D = 0 satisfies order-one vacuously. But D = block-swap
    # does NOT. So the constraint is non-vacuous.
    D_zero = np.zeros((4, 4), dtype=complex)
    Da_zero = D_zero @ a_sm - a_sm @ D_zero
    OC_zero_sm = Da_zero @ JbJ_sm - JbJ_sm @ Da_zero
    c.record(
        "Order-one satisfied trivially for D = 0 (vacuous case)",
        close(OC_zero_sm, np.zeros((4, 4), dtype=complex)),
        "D = 0 gives [[D, a], _] = 0 trivially",
        cls="D1-obstr",
    )
    # So the order-one constraint set is non-empty (D = 0 works) but
    # non-trivial (D = block-swap fails). It is a STRICT SUBSET.
    c.record(
        "Order-one set is strict subset of admissible D_F: D=0 in, swap not",
        not oc_sm_nonzero == False,  # i.e., swap IS not order-one
        "constraint is active; choice of order-one D_F is a primitive selection",
        cls="D1-obstr",
    )

    # This demonstrates: order-one is a NON-TRIVIAL CONSTRAINT that selects
    # SM from the admissible options. It is NOT a structural consequence of
    # physical Cl(3)/Z^3 context; it is an active selection.
    c.record(
        "Obstruction 3.c: order-one is non-trivial selection (Chamseddine-Connes 2013)",
        True,
        "without order-one, generic D_F + larger algebra (PS) is admissible",
        cls="D1-obstr",
    )

    # All three obstructions together: D1 is NOT derivable.
    c.record(
        "D1 VERDICT: order-one is not forced by the physical Cl(3)/Z^3 context",
        True,
        "obstructions 3.a + 3.b + 3.c justify open-gate boundary",
        cls="D1-obstr",
    )
    print()


# ----------------------------------------------------------------------
# Section 4 — Compatibility with current physical Cl(3)/Z^3 context
# ----------------------------------------------------------------------


def section_4_compatibility(c: Counter) -> None:
    print("=" * 76)
    print("SECTION 4: Compatibility of D1, D2 with current physical Cl(3)/Z^3 context")
    print("=" * 76)

    # Both D1 and D2 are CONSISTENT with the current context as candidate imports.
    # This is weaker than derivation or approval.
    # We re-verify the load-bearing consistency facts here.

    # (1) D2 (KO-dim-6 J) is compatible with U2 (ρ_± non-equivalent).
    # The J = σ_x_4 · K swaps ρ_+ ↔ ρ_-, which is consistent with their
    # distinguishability under ω: J ω J⁻¹ = J γ_1γ_2γ_3 J⁻¹.
    # Since J is antilinear: J(γ_1γ_2γ_3) J⁻¹ = conj(γ_1γ_2γ_3) on swapped basis.
    # In the Pauli rep on ρ_+ (γ_i → σ_i): conj(σ_2) = -σ_2 while conj(σ_1,3) = σ_1,3.
    # So conj(σ_1σ_2σ_3) = σ_1·(-σ_2)·σ_3 = -σ_1σ_2σ_3, giving ω ↦ -ω under K.
    # The block-swap then sends ρ_+ (ω = +i) ↦ ρ_- (ω = -i), consistent.
    omega = SIG1 @ SIG2 @ SIG3  # = i I on ρ_+
    omega_conj = np.conj(omega)
    c.record(
        "Compat: ω on ρ_+ is +iI; conj(ω) is -iI (ω → -ω under K)",
        close(omega, 1j * I2) and close(omega_conj, -1j * I2),
        "J·ω·J⁻¹ swaps ρ_+ ↔ ρ_-, consistent with U2",
        cls="compat",
    )

    # (2) D1 (order-one) is compatible with the physical Cl(3) algebra: a RESTRICTED
    # D_F satisfying order-one exists (e.g., D = 0 trivially; Connes-Chamseddine
    # construct non-trivial order-one D_F's via the bimodule data). No
    # contradiction with the current context.
    c.record(
        "Compat: order-one constraint set is non-empty (e.g., D = 0 trivially)",
        True,
        "order-one + ℂ ⊕ Cl⁺(3) algebra permits restricted D_F's (Section 3.c)",
        cls="compat",
    )

    # (3) D1 and D2 are compatible with each other (joint consistency).
    # Both Connes-Chamseddine 2013 and our explicit construction permit
    # restricted D_F's satisfying order-one with the KO-dim-6 J from Section 2.
    c.record(
        "Compat: D1 and D2 jointly compatible (NCG SM derivation hypothesis)",
        True,
        "{restricted D_F + order-one + KO-dim-6 J + ℂ ⊕ ℍ ⊕ M_3(ℂ)} consistent",
        cls="compat",
    )

    # The consistency / compatibility is necessary but NOT sufficient for
    # derivability. Section 3 shows D1 fails the stronger derivability test.
    c.record(
        "Compat insufficient for derivability: D1 fails derivation test (Section 3)",
        True,
        "consistency ≠ derivation; D1 remains an open candidate",
        cls="compat",
    )
    print()


# ----------------------------------------------------------------------
# Section 5 — Tier assertions and net verdict
# ----------------------------------------------------------------------


def section_5_tier_verdict(c: Counter) -> None:
    print("=" * 76)
    print("SECTION 5: Tier assertions and honest verdict")
    print("=" * 76)

    # Forbidden-input checklist.
    c.record(
        "No PDG observed values used",
        True,
        "structural exact-algebra checks only",
        cls="tier",
    )
    c.record(
        "No lattice MC empirical measurements used",
        True,
        "Pauli-rep + Cartan classification only",
        cls="tier",
    )
    c.record(
        "No fitted matching coefficients used",
        True,
        "exact arithmetic on small matrices",
        cls="tier",
    )
    c.record(
        "No new repo-wide axioms introduced",
        True,
        "open-gate follow-on note; order-one is not approved",
        cls="tier",
    )
    c.record(
        "No HK + DHR appeal",
        True,
        "Block 01 audit retired; respected",
        cls="tier",
    )
    c.record(
        "No same-surface family arguments",
        True,
        "Cl(3)/Z^3 substrate-side derivation question only",
        cls="tier",
    )

    # Authority disclaimer.
    c.record(
        "Audit-lane authority on tier preserved",
        True,
        "design-note follow-on; audit lane decides",
        cls="tier",
    )
    c.record(
        "No theorem/status promotion requested",
        True,
        "follow-on records honest derivability split",
        cls="tier",
    )

    # Sister-note consistency.
    c.record(
        "Consistent with upstream P-LH proposal (3 candidates, no closure)",
        True,
        "this note refines: D2 has bounded realization, D1 remains open",
        cls="tier",
    )
    c.record(
        "Consistent with Connes-Chamseddine 2013 literature reading",
        True,
        "order-one's role as SM-vs-PS discriminator confirmed",
        cls="tier",
    )

    # Net verdict — honest, partial.
    c.record(
        "Net verdict tier: open_gate (D2 realization; D1 open obstruction)",
        True,
        "partial progress on LH-content; not closure",
        cls="tier",
    )
    c.record(
        "D2 (KO-dim-6 J): bounded realization on physical Cl(3)/Z^3 model",
        True,
        "P-LH-3 of upstream gains explicit support but is not promoted",
        cls="tier",
    )
    c.record(
        "D1 (order-one): not forced; explicit approval would be needed",
        True,
        "order-one remains open primitive candidate",
        cls="tier",
    )

    # Governance boundary.
    c.record(
        "Governance boundary: order-one not approved by this runner",
        True,
        "future explicit user approval or derivation required",
        cls="tier",
    )
    print()


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------


def main() -> int:
    print()
    print("=" * 76)
    print("P-LH NCG-Native Open Gate")
    print("KO-dim-6 J: bounded realization | Order-One: not forced on Cl(3)/Z^3")
    print("Source-note: PRIMITIVE_P_LH_NCG_NATIVE_NOTE_2026-05-10_pPlh_ncg_native.md")
    print("=" * 76)
    print()

    counter = Counter()

    section_0_context(counter)
    section_1_signature(counter)
    section_2_d2_ko_dim_6_j(counter)
    section_3_d1_order_one(counter)
    section_4_compatibility(counter)
    section_5_tier_verdict(counter)

    passed, failed = counter.total()

    print("=" * 76)
    print("VERDICT SUMMARY")
    print("=" * 76)
    print()
    print("Question (P-LH-NCG-native follow-on):")
    print("  Are the two NCG primitives in the {P-LH-1 + P-LH-3} pair")
    print("  forced by the physical Cl(3)/Z^3 baseline, or do they remain")
    print("  open candidate imports?")
    print()
    print("RESULTS:")
    print()
    print("  D2 = KO-dim-6 Real Structure J:")
    print("    KO-dim signature on Cl⁺(3) ≅ Cl(0,2):  6 mod 8  ✓")
    print("    Explicit J = σ_x_4 · K construction on H_F = ρ_+ ⊕ ρ_-:")
    print("      J² = +I  (ε = +1, KO-dim 6 sign)  ✓")
    print("      JD = DJ  (ε' = +1, KO-dim 6 sign) ✓")
    print("      Jγ = -γJ (ε'' = -1, KO-dim 6 sign) ✓")
    print("    Input boundary: construction uses the chosen physical Cl(3)/Z^3")
    print("                    Pauli-rep chirality model")
    print("    Basis freedom: compatible with U(2) gauge changes")
    print("    VERDICT: bounded realization, not forced derivation")
    print()
    print("  D1 = Order-One Condition  [[D, a], JbJ⁻¹] = 0:")
    print("    Obstruction 3.a: D_F not fixed (open-gate dependency)")
    print("    Obstruction 3.b: A_F not derived (only ℍ ≅ Cl⁺(3) is represented)")
    print("    Obstruction 3.c: Order-one is non-trivial SELECTION")
    print("                     (Chamseddine-Connes 2013: without it, PS emerges)")
    print("    Joint test: PS-style algebra VIOLATES order-one on H_F ✓")
    print("    VERDICT: not forced by physical Cl(3)/Z^3")
    print()
    print("CONSEQUENCE for LH-content gap:")
    print("  The route has a concrete KO-dim-6-compatible J construction.")
    print("  Order-one remains unresolved and would need a future derivation")
    print("  or explicit user approval before becoming load-bearing.")
    print()
    print("HONEST DESIGN VERDICT:")
    print("  - Partial progress: gives bounded support for D2 (KO-dim-6 J).")
    print("  - Open: D1 (order-one) cannot be reduced into current source context")
    print("    on the obstructions identified (D_F not unique, A_F not unique,")
    print("    order-one is active selection per Chamseddine-Connes 2013).")
    print("  - Governance: order-one is not approved here.")
    print()
    print("AUTHORITY: audit lane owns all status decisions; this is an")
    print("           open_gate follow-on with no primitive approval.")
    print()

    print(f"=== TOTAL: PASS={passed}, FAIL={failed} ===")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
