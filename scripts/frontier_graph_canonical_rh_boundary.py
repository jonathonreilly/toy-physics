#!/usr/bin/env python3
"""Verify the paper-safe right-handed boundary theorem.

This is a synthesis helper, not a new derivation attempt.  It checks the
strongest statement currently supported by the graph/taste surface:

  1. The 3D KS surface gives the left-handed gauge algebra and quantum numbers.
  2. CPT / Dirac-sea structure are graph-canonical on that 3D surface.
  3. The 3D surface has no SU(2) singlets, so right-handed singlets require
     4D chirality input.
  4. In 4D, gamma_5 provides the chirality split and anomaly cancellation
     uniquely fixes the right-handed hypercharges once the singlet template
     and neutral-neutrino condition are supplied.

The goal is to state the exact theorem that survives, and the exact blocker
that remains open, without assuming a graph-canonical singlet template.
"""

from __future__ import annotations

from fractions import Fraction
import numpy as np

PASS = 0
FAIL = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS, FAIL
    if condition:
        PASS += 1
        status = "PASS"
    else:
        FAIL += 1
        status = "FAIL"
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def kron3(a, b, c):
    return np.kron(a, np.kron(b, c))


def kron4(a, b, c, d):
    return np.kron(a, np.kron(b, np.kron(c, d)))


I2 = np.eye(2, dtype=complex)
I8 = np.eye(8, dtype=complex)
I16 = np.eye(16, dtype=complex)
sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)


def comm(a, b):
    return a @ b - b @ a


def acomm(a, b):
    return a @ b + b @ a


def build_3d():
    g1 = kron3(sx, I2, I2)
    g2 = kron3(sz, sx, I2)
    g3 = kron3(sz, sz, sx)
    t1 = 0.5 * kron3(sx, I2, I2)
    t2 = 0.5 * kron3(sy, I2, I2)
    t3 = 0.5 * kron3(sz, I2, I2)
    swap23 = np.zeros((8, 8), dtype=complex)
    for a in range(2):
        for b in range(2):
            for c in range(2):
                src = 4 * a + 2 * b + c
                dst = 4 * a + 2 * c + b
                swap23[dst, src] = 1.0
    p_sym = (I8 + swap23) / 2.0
    p_anti = (I8 - swap23) / 2.0
    y8 = (Fraction(1, 3)) * p_sym + (Fraction(-1, 1)) * p_anti
    chi = kron3(sz, sz, sz)
    return g1, g2, g3, t1, t2, t3, swap23, p_sym, p_anti, y8, chi


def build_4d():
    g0 = kron4(sz, sz, sz, sx)
    g1 = kron4(sx, I2, I2, I2)
    g2 = kron4(sz, sx, I2, I2)
    g3 = kron4(sz, sz, sx, I2)
    g5 = g0 @ g1 @ g2 @ g3
    return g0, g1, g2, g3, g5


def verify_3d_surface():
    print("=" * 78)
    print("3D GRAPH/ TASTE SURFACE")
    print("=" * 78)
    g1, g2, g3, t1, t2, t3, swap23, p_sym, p_anti, y8, chi = build_3d()
    generators = [g1, g2, g3]

    # No SU(2) singlets on the one-particle surface.
    casimir = t1 @ t1 + t2 @ t2 + t3 @ t3
    evals = np.linalg.eigvalsh(casimir)
    check("C^8 SU(2) Casimir is uniform 3/4", np.allclose(evals, 0.75))
    t3_diag = np.real(np.diag(t3))
    check("No T3 = 0 states on C^8", not np.any(np.isclose(t3_diag, 0.0)))

    # Left-handed gauge content.
    y_evals = np.linalg.eigvalsh(np.asarray(y8, dtype=complex))
    num_quark = int(np.sum(np.isclose(y_evals, 1.0 / 3.0)))
    num_lepton = int(np.sum(np.isclose(y_evals, -1.0)))
    check("3D gauge content = 6 quark states + 2 lepton states", num_quark == 6 and num_lepton == 2)

    # The graph-canonical grading.
    check("chi^2 = I", np.allclose(chi @ chi, I8))
    check("{chi, G1} = {chi, G2} = {chi, G3} = 0",
          all(np.allclose(acomm(chi, g), 0) for g in generators))
    check("chi commutes with SWAP23", np.allclose(comm(chi, swap23), 0))

    # CPT / particle-hole structure.
    h = 0.31 * g1 - 0.27 * g2 + 0.49 * g3
    check("Particle-hole symmetry {chi, H} = 0", np.allclose(acomm(chi, h), 0))
    check("Clifford generators are real", all(np.allclose(g.imag, 0) for g in generators))
    check("Complex conjugation is a symmetry of the 3D Clifford surface",
          all(np.allclose(np.conj(g), g) for g in generators))

    return {
        "g1": g1,
        "g2": g2,
        "g3": g3,
        "t1": t1,
        "t2": t2,
        "t3": t3,
        "swap23": swap23,
        "p_sym": p_sym,
        "p_anti": p_anti,
        "y8": y8,
        "chi": chi,
    }


def verify_4d_chirality():
    print("\n" + "=" * 78)
    print("4D CHIRALITY")
    print("=" * 78)
    g0, g1, g2, g3, g5 = build_4d()
    generators = [g0, g1, g2, g3]
    check("gamma_5^2 = I", np.allclose(g5 @ g5, I16))
    check("gamma_5 is Hermitian", np.allclose(g5, g5.conj().T))
    check("gamma_5 has 8 +1 and 8 -1 eigenvalues",
          np.sum(np.linalg.eigvalsh(g5) > 0.5) == 8 and np.sum(np.linalg.eigvalsh(g5) < -0.5) == 8)
    check("{gamma_5, Gamma_mu} = 0 for all mu",
          all(np.allclose(acomm(g5, g), 0) for g in generators))
    return g5


def verify_conditional_anomaly_completion():
    print("\n" + "=" * 78)
    print("CONDITIONAL ANOMALY COMPLETION")
    print("=" * 78)
    # Singlet template is an input here; the point is to verify the completion,
    # not to derive the template graph-canonically.
    y1 = Fraction(4, 3)
    y2 = Fraction(-2, 3)
    y3 = Fraction(-2, 1)
    y4 = Fraction(0, 1)

    tr_y = 3 * y1 + 3 * y2 + y3 + y4
    tr_y3 = (
        6 * Fraction(1, 3) ** 3
        + 2 * Fraction(-1, 1) ** 3
        + 3 * (-y1) ** 3
        + 3 * (-y2) ** 3
        + (-y3) ** 3
        + (-y4) ** 3
    )
    su3_sq_y = Fraction(1, 3) - y1 / 2 - y2 / 2
    su2_sq_y = 3 * Fraction(1, 2) * Fraction(1, 3) + 1 * Fraction(1, 2) * Fraction(-1)

    check("Tr[Y] = 0 on the singlet template", tr_y == 0)
    check("Tr[Y^3] = 0 on the singlet template", tr_y3 == 0)
    check("Tr[SU(3)^2 Y] = 0", su3_sq_y == 0)
    check("Tr[SU(2)^2 Y] = 0", su2_sq_y == 0)
    doublets = 3 + 1  # 3 colour copies of Q_L plus one L_L
    check("Witten anomaly even-doublet count", doublets % 2 == 0, f"doublets = {doublets}")
    return {"y1": y1, "y2": y2, "y3": y3, "y4": y4}


def main() -> int:
    print("=" * 78)
    print("GRAPH-CANONICAL RIGHT-HANDED BOUNDARY THEOREM")
    print("=" * 78)
    print("Goal: test the paper-safe boundary statement directly.")

    surface = verify_3d_surface()
    verify_4d_chirality()
    charges = verify_conditional_anomaly_completion()

    print("\n" + "=" * 78)
    print("THEOREM THAT SURVIVES")
    print("=" * 78)
    print("3D graph/taste structure canonically gives:")
    print("  - the left-handed gauge algebra on C^8")
    print("  - left-handed matter quantum numbers")
    print("  - CPT / particle-hole doubling and antiparticle structure")
    print("4D physical spacetime gives:")
    print("  - chirality via gamma_5")
    print("  - SU(2)-singlet right-handed fermions")
    print("Given the 4D singlet template and nu_R = 0, anomaly cancellation")
    print("uniquely fixes the right-handed hypercharges.")
    print()
    print("OPEN BLOCKER:")
    print("  The 3D graph/taste surface does NOT canonically derive the")
    print("  right-handed singlet template.  That is the missing theorem.")
    print()
    print("PAPER-SAFE VERSION:")
    print("  '3D derives the gauge algebra and left-handed matter quantum")
    print("   numbers; 4D supplies chirality and therefore the SU(2)-singlet")
    print("   right-handed sector.'")

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    total = PASS + FAIL
    print(f"PASS={PASS} FAIL={FAIL} TOTAL={total}")
    if FAIL == 0:
        print("ALL CHECKS PASSED")
        return 0
    print("SOME CHECKS FAILED")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
