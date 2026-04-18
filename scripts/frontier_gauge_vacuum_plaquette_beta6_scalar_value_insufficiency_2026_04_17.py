#!/usr/bin/env python3
"""
Beta=6 scalar-value insufficiency on the plaquette PF lane.

This sharpens the live framework-point seam:

1. even if the same-surface plaquette value at beta=6 is fixed,
2. that gives only one scalar framework-point constraint,
3. and does not determine the full positive class-sector vector v_6,
4. so explicit matrix-element evaluation of K_6^env / B_6(W) still remains.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]

THEOREM_PASS = 0
SUPPORT_PASS = 0
FAIL = 0


def check(name: str, condition: bool, detail: str = "", bucket: str = "THEOREM") -> None:
    global THEOREM_PASS, SUPPORT_PASS, FAIL
    status = "PASS" if condition else "FAIL"
    if condition:
        if bucket == "SUPPORT":
            SUPPORT_PASS += 1
        else:
            THEOREM_PASS += 1
    else:
        FAIL += 1
    print(f"  [{status}] [{bucket}] {name}")
    if detail:
        print(f"         {detail}")


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text()


def dim_su3(p: int, q: int) -> int:
    return (p + 1) * (q + 1) * (p + q + 2) // 2


def su3_character(p: int, q: int, theta1: float, theta2: float) -> complex:
    x = np.array(
        [
            np.exp(1j * theta1),
            np.exp(1j * theta2),
            np.exp(-1j * (theta1 + theta2)),
        ],
        dtype=complex,
    )
    lam = [p + q, q, 0]
    num = np.array(
        [[x[i] ** (lam[j] + 2 - j) for j in range(3)] for i in range(3)],
        dtype=complex,
    )
    den = np.array(
        [[x[i] ** (2 - j) for j in range(3)] for i in range(3)],
        dtype=complex,
    )
    return complex(np.linalg.det(num) / np.linalg.det(den))


def direct_class_function(
    coeffs: np.ndarray, weights: list[tuple[int, int]], theta1: float, theta2: float
) -> complex:
    total = 0.0j
    for i, (p, q) in enumerate(weights):
        total += dim_su3(p, q) * coeffs[i] * su3_character(p, q, theta1, theta2)
    return total


def main() -> int:
    self_note = read("docs/PLAQUETTE_SELF_CONSISTENCY_NOTE.md")
    seam_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_BETA6_EVALUATION_SEAM_REDUCTION_SCIENCE_ONLY_NOTE_2026-04-17.md"
    )
    pf_note = read("docs/PERRON_FROBENIUS_SELECTION_AXIOM_BOUNDARY_NOTE_2026-04-17.md")

    weights = [(0, 0), (1, 0), (2, 0)]
    v_a = np.array([0.20, 0.60, 0.20], dtype=float)
    v_b = np.array([0.35, 0.30, 0.35], dtype=float)
    ell = np.array([0.0, 1.0, 2.0], dtype=float)
    second = np.array([0.0, 1.0, 4.0], dtype=float)

    l_a = float(ell @ v_a)
    l_b = float(ell @ v_b)
    m_a = float(second @ v_a)
    m_b = float(second @ v_b)

    theta1 = 0.41
    theta2 = -0.27
    z_a = direct_class_function(v_a, weights, theta1, theta2)
    z_b = direct_class_function(v_b, weights, theta1, theta2)
    z_gap = abs(z_a - z_b)

    print("=" * 92)
    print("GAUGE-VACUUM PLAQUETTE BETA=6 SCALAR-VALUE INSUFFICIENCY")
    print("=" * 92)
    print()
    print("Witness vectors on a three-weight class-sector truncation")
    print(f"  weights                                  = {weights}")
    print(f"  v^(A)                                    = {np.round(v_a, 6)}")
    print(f"  v^(B)                                    = {np.round(v_b, 6)}")
    print(f"  normalization errors                     = {abs(np.sum(v_a) - 1.0):.3e}, {abs(np.sum(v_b) - 1.0):.3e}")
    print()
    print("One-scalar versus multi-component data")
    print(f"  shared scalar statistic L(v)             = {l_a:.6f}, {l_b:.6f}")
    print(f"  distinct higher statistic M(v)           = {m_a:.6f}, {m_b:.6f}")
    print(f"  marked class-function gap |Z_A-Z_B|      = {z_gap:.6e}")
    print()
    print("Framework-point reading")
    print("  fixing one scalar same-surface plaquette value still leaves room")
    print("  for different positive class-sector vectors and different marked")
    print("  boundary class functions.")
    print()

    check(
        "Plaquette self-consistency note records the canonical beta=6 plaquette as one same-surface observable rather than a free parameter",
        "same-surface evaluated observable of the retained theory" in self_note
        and "not a hidden fit parameter" in self_note,
        bucket="SUPPORT",
    )
    check(
        "Beta=6 seam-reduction note records the live PF seam is matrix-element evaluation of K_6^env and B_6(W)",
        "remaining explicit `beta = 6` problem is exactly evaluation" in seam_note
        and "class-sector matrix elements" in seam_note
        and "K_6^env" in seam_note
        and "B_6(W)" in seam_note,
        bucket="SUPPORT",
    )
    check(
        "PF boundary note already records unique plaquette framework-point PF data still require explicit beta=6 evaluation",
        "same-surface plaquette value `P(6)` is fixed" in pf_note
        and "does **not** determine the class-sector vector `v_6`" in pf_note
        and "K_6^env` and `B_6(W)`" in pf_note,
        bucket="SUPPORT",
    )

    check(
        "Witness vectors are strictly positive and normalized",
        float(np.min(v_a)) > 0.0
        and float(np.min(v_b)) > 0.0
        and abs(np.sum(v_a) - 1.0) < 1e-12
        and abs(np.sum(v_b) - 1.0) < 1e-12,
        detail=f"floors=({np.min(v_a):.6f},{np.min(v_b):.6f})",
    )
    check(
        "One scalar statistic can agree on distinct positive class-sector vectors",
        abs(l_a - l_b) < 1e-12 and float(np.max(np.abs(v_a - v_b))) > 1e-3,
        detail=f"L(v_A)=L(v_B)={l_a:.6f}",
    )
    check(
        "A second statistic distinguishes the same two vectors",
        abs(m_a - m_b) > 1e-8,
        detail=f"M(v_A)={m_a:.6f}, M(v_B)={m_b:.6f}",
    )
    check(
        "The canonical Peter-Weyl evaluation law distinguishes the two vectors at generic marked holonomy",
        z_gap > 1e-8,
        detail=f"|Z_A-Z_B|={z_gap:.6e}",
    )
    check(
        "Therefore one scalar framework-point value does not determine the full compressed boundary class function",
        abs(l_a - l_b) < 1e-12 and z_gap > 1e-8,
        detail="same scalar value, different Z_6^env(W)",
    )
    check(
        "The live beta=6 PF seam still requires explicit matrix-element data beyond one scalar plaquette value",
        abs(l_a - l_b) < 1e-12 and abs(m_a - m_b) > 1e-8 and z_gap > 1e-8,
        detail="one scalar observable does not fix v_6, rho_(p,q)(6), or explicit PF data",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
