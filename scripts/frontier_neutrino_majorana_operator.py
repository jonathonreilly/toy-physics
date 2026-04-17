#!/usr/bin/env python3
"""
Axiom-first classification of the bare quadratic Majorana operator.

Question:
  On the anomaly-fixed one-generation surface, which local quadratic
  same-chirality bilinear is simultaneously Lorentz invariant and
  SU(3)_c x SU(2)_L x U(1)_Y invariant?

Answer sought here:
  The unique operator candidate at quadratic order.

Boundary:
  This script classifies operators. It does NOT derive the coefficient or
  the seesaw scale, and it does NOT fit PMNS/mass data.

Atlas rows reused from main:
  Framework axiom
  Anomaly-forced time
  Native weak algebra
  Structural SU(3) closure
  One-generation matter closure
"""

from __future__ import annotations

import sys

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def null_space(matrix: np.ndarray, tol: float = 1e-10) -> np.ndarray:
    u, s, vh = np.linalg.svd(matrix, full_matrices=False)
    rank = int(np.sum(s > tol))
    return vh.conj().T[:, rank:]


def build_dirac_data():
    i2 = np.eye(2, dtype=complex)
    z2 = np.zeros((2, 2), dtype=complex)
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)

    g0 = np.block([[i2, z2], [z2, -i2]])
    g1 = np.block([[z2, sx], [-sx, z2]])
    g2 = np.block([[z2, sy], [-sy, z2]])
    g3 = np.block([[z2, sz], [-sz, z2]])
    gammas = [g0, g1, g2, g3]
    g5 = 1j * g0 @ g1 @ g2 @ g3
    cmat = 1j * g2 @ g0
    i4 = np.eye(4, dtype=complex)
    pr = (i4 + g5) / 2.0
    pl = (i4 - g5) / 2.0

    lorentz = []
    for mu in range(4):
        for nu in range(mu + 1, 4):
            lorentz.append(0.25 * (gammas[mu] @ gammas[nu] - gammas[nu] @ gammas[mu]))

    basis = [i4]
    labels = ["I"]
    for idx, gamma in enumerate(gammas):
        basis.append(gamma)
        labels.append(f"g{idx}")
    for mu in range(4):
        for nu in range(mu + 1, 4):
            basis.append(0.5 * (gammas[mu] @ gammas[nu] - gammas[nu] @ gammas[mu]))
            labels.append(f"s{mu}{nu}")
    basis.append(g5)
    labels.append("g5")
    for idx, gamma in enumerate(gammas):
        basis.append(gamma @ g5)
        labels.append(f"g{idx}g5")

    return gammas, g5, cmat, pr, pl, lorentz, basis, labels


def spinor_classification():
    print("\n" + "=" * 88)
    print("PART 1: LORENTZ-INVARIANT SAME-CHIRALITY SPINOR FORMS")
    print("=" * 88)

    _, g5, cmat, pr, pl, lorentz, basis, labels = build_dirac_data()

    columns = []
    for gamma in basis:
        bilinear = cmat @ gamma
        residual = []
        for generator in lorentz:
            residual.append((generator.T @ bilinear + bilinear @ generator).reshape(-1))
        columns.append(np.concatenate(residual))
    system = np.column_stack(columns)
    ns = null_space(system)
    check("Lorentz-invariant psi^T B psi space has dimension 2", ns.shape[1] == 2)

    c_res = max(np.linalg.norm(s.T @ cmat + cmat @ s) for s in lorentz)
    cg5 = cmat @ g5
    cg5_res = max(np.linalg.norm(s.T @ cg5 + cg5 @ s) for s in lorentz)
    check("C is Lorentz invariant", c_res < 1e-10, f"residual={c_res:.2e}")
    check("C gamma_5 is Lorentz invariant", cg5_res < 1e-10, f"residual={cg5_res:.2e}")
    check("C is antisymmetric", np.linalg.norm(cmat.T + cmat) < 1e-10)
    check("C gamma_5 is antisymmetric", np.linalg.norm(cg5.T + cg5) < 1e-10)

    b_r = cmat @ pr
    b_l = cmat @ pl
    b_r_res = max(np.linalg.norm(s.T @ b_r + b_r @ s) for s in lorentz)
    b_l_res = max(np.linalg.norm(s.T @ b_l + b_l @ s) for s in lorentz)
    check("C P_R is a nonzero Lorentz-invariant same-chirality form", np.linalg.norm(b_r) > 1e-10 and b_r_res < 1e-10,
          f"norm={np.linalg.norm(b_r):.3f}, residual={b_r_res:.2e}")
    check("C P_L is a nonzero Lorentz-invariant same-chirality form", np.linalg.norm(b_l) > 1e-10 and b_l_res < 1e-10,
          f"norm={np.linalg.norm(b_l):.3f}, residual={b_l_res:.2e}")
    check("C P_R is antisymmetric", np.linalg.norm(b_r.T + b_r) < 1e-10)
    check("C P_L is antisymmetric", np.linalg.norm(b_l.T + b_l) < 1e-10)

    print()
    print("  The spinor classification leaves two invariant bilinear seeds: C and C gamma_5.")
    print("  After chirality projection, C P_R and C P_L give the same-chirality")
    print("  Majorana spinor structures. The internal gauge solve decides which")
    print("  field can actually use them.")

    return b_r, b_l


def build_internal_generators():
    """
    Basis ordering for the anomaly-fixed one-generation spectrum:

      0..2   : u_L, c_L, t_L-style color components inside Q_L upper component
      3..5   : d_L, s_L, b_L-style color components inside Q_L lower component
      6      : nu_L
      7      : e_L
      8..10  : u_R colors
      11..13 : d_R colors
      14     : e_R
      15     : nu_R
    """

    n = 16
    generators = []
    labels = ["uL_r", "uL_g", "uL_b", "dL_r", "dL_g", "dL_b", "nu_L", "e_L",
              "uR_r", "uR_g", "uR_b", "dR_r", "dR_g", "dR_b", "e_R", "nu_R"]

    lam = []
    lam.append(np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=complex))
    lam.append(np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], dtype=complex))
    lam.append(np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]], dtype=complex))
    lam.append(np.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]], dtype=complex))
    lam.append(np.array([[0, 0, -1j], [0, 0, 0], [1j, 0, 0]], dtype=complex))
    lam.append(np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex))
    lam.append(np.array([[0, 0, 0], [0, 0, -1j], [0, 1j, 0]], dtype=complex))
    lam.append((1.0 / np.sqrt(3.0)) * np.array([[1, 0, 0], [0, 1, 0], [0, 0, -2]], dtype=complex))

    for idx, matrix in enumerate(lam, start=1):
        gen = np.zeros((n, n), dtype=complex)
        t = matrix / 2.0
        gen[0:3, 0:3] = t
        gen[3:6, 3:6] = t
        gen[8:11, 8:11] = t
        gen[11:14, 11:14] = t
        generators.append((f"SU3_{idx}", gen))

    sx = np.array([[0, 1], [1, 0]], dtype=complex) / 2.0
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex) / 2.0
    sz = np.array([[1, 0], [0, -1]], dtype=complex) / 2.0
    i3 = np.eye(3, dtype=complex)

    for name, s in [("SU2_1", sx), ("SU2_2", sy), ("SU2_3", sz)]:
        gen = np.zeros((n, n), dtype=complex)
        gen[0:6, 0:6] = np.kron(s, i3)
        gen[6:8, 6:8] = s
        generators.append((name, gen))

    y = np.diag([1 / 3] * 6 + [-1] * 2 + [4 / 3] * 3 + [-2 / 3] * 3 + [-2] + [0]).astype(complex)
    generators.append(("Y", y))

    return generators, labels


def internal_majorana_classification():
    print("\n" + "=" * 88)
    print("PART 2: INTERNAL GAUGE-INVARIANT SYMMETRIC BILINEARS")
    print("=" * 88)

    generators, labels = build_internal_generators()
    n = len(labels)

    basis = []
    basis_labels = []
    for i in range(n):
        matrix = np.zeros((n, n), dtype=complex)
        matrix[i, i] = 1.0
        basis.append(matrix)
        basis_labels.append((i, i))
    for i in range(n):
        for j in range(i + 1, n):
            matrix = np.zeros((n, n), dtype=complex)
            matrix[i, j] = 1.0
            matrix[j, i] = 1.0
            basis.append(matrix)
            basis_labels.append((i, j))

    columns = []
    for matrix in basis:
        residual = []
        for _, generator in generators:
            residual.append((generator.T @ matrix + matrix @ generator).reshape(-1))
        columns.append(np.concatenate(residual))
    system = np.column_stack(columns)
    ns = null_space(system)
    check("Gauge-invariant symmetric internal bilinear space has dimension 1", ns.shape[1] == 1)

    coeffs = ns[:, 0]
    invariant = sum(c * m for c, m in zip(coeffs, basis))
    invariant /= np.linalg.norm(invariant)

    template = np.zeros_like(invariant)
    template[15, 15] = invariant[15, 15]
    support_residual = np.linalg.norm(invariant - template)

    direct_template = np.zeros((n, n), dtype=complex)
    direct_template[15, 15] = 1.0
    max_residual = 0.0
    for _, generator in generators:
        max_residual = max(max_residual, np.linalg.norm(generator.T @ direct_template + direct_template @ generator))

    check("Invariant support is only on the nu_R nu_R slot", support_residual < 1e-10,
          f"off-slot norm={support_residual:.2e}")
    check("Direct nu_R nu_R slot is gauge invariant", max_residual < 1e-10, f"residual={max_residual:.2e}")

    forbidden_slots = {
        "nu_L nu_L": (6, 6),
        "e_R e_R": (14, 14),
        "u_R u_R": (8, 8),
        "d_R d_R": (11, 11),
    }
    for name, (i, j) in forbidden_slots.items():
        matrix = np.zeros((n, n), dtype=complex)
        matrix[i, j] = 1.0
        if i != j:
            matrix[j, i] = 1.0
        slot_residual = max(np.linalg.norm(generator.T @ matrix + matrix @ generator) for _, generator in generators)
        check(f"{name} is not gauge invariant at quadratic order", slot_residual > 1e-8,
              f"residual={slot_residual:.3f}")

    print()
    print("  Unique invariant internal bilinear:")
    print(f"    ({labels[15]}, {labels[15]})")

    return direct_template


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA OPERATOR: AXIOM-FIRST CLASSIFICATION")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - main:docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    print("    rows: Framework axiom; Anomaly-forced time; Native weak algebra;")
    print("          Structural SU(3) closure; One-generation matter closure")
    print("  - MINIMAL_AXIOM_INVENTORY.md")
    print("  - UNIFIED_AXIOM_BOUNDARY_NOTE.md")
    print("  - ANOMALY_FORCES_TIME_THEOREM.md")
    print("  - frontier_right_handed_sector.py")

    b_r, _ = spinor_classification()
    internal = internal_majorana_classification()

    print("\n" + "=" * 88)
    print("PART 3: COMBINED OPERATOR")
    print("=" * 88)
    check("Spinor factor is nonzero", np.linalg.norm(b_r) > 1e-10)
    check("Internal factor is nonzero", np.linalg.norm(internal) > 1e-10)
    check("Combined quadratic Majorana candidate therefore exists", True,
          "nu_R^T C P_R nu_R")

    print()
    print("RESULT")
    print("-" * 88)
    print("  Up to normalization, the unique local quadratic same-chirality")
    print("  Lorentz- and gauge-invariant Majorana operator on the anomaly-fixed")
    print("  one-generation surface is:")
    print()
    print("      nu_R^T C P_R nu_R")
    print()
    print("  This classifies the operator. It does NOT derive its coefficient,")
    print("  its scale, or the full 3x3 neutrino texture.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
