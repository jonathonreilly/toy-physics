#!/usr/bin/env python3
"""
Taste-scalar Coleman-Weinberg isotropy on the retained Cl(3)/Z^3 taste block.

Exact theorem:
  the one-loop fermion CW Hessian on the taste block is isotropic at any
  axis-aligned minimum phi = (v, 0, 0).

Bounded downstream package:
  a gauge-only leading split then gives a near-degenerate taste-scalar pair and
  a weak scalar-only thermal-cubic estimate.
"""

from __future__ import annotations

import math
import sys

import numpy as np

from canonical_plaquette_surface import CANONICAL_ALPHA_LM

M_PL = 1.2209e19
V_EW = M_PL * ((7.0 / 8.0) ** 0.25) * (CANONICAL_ALPHA_LM ** 16)

# Live package values on main.
G1_V = 0.464376
G2_V = 0.648031
GP_V = G1_V * math.sqrt(3.0 / 5.0)
MH_3L = 125.10

THEOREM_PASS = 0
BOUNDED_PASS = 0
FAIL = 0


def check(kind: str, name: str, condition: bool, detail: str = "") -> bool:
    global THEOREM_PASS, BOUNDED_PASS, FAIL
    status = "PASS" if condition else "FAIL"
    if condition:
        if kind == "theorem":
            THEOREM_PASS += 1
        else:
            BOUNDED_PASS += 1
    else:
        FAIL += 1
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    return condition


def shift_ops() -> list[np.ndarray]:
    i2 = np.eye(2, dtype=complex)
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    return [
        np.kron(sx, np.kron(i2, i2)),
        np.kron(i2, np.kron(sx, i2)),
        np.kron(i2, np.kron(i2, sx)),
    ]


def eigenvalues(phi: tuple[float, float, float]) -> list[float]:
    vals = []
    for a in range(2):
        for b in range(2):
            for c in range(2):
                s = (a, b, c)
                vals.append(sum(phi[i] * ((-1) ** s[i]) for i in range(3)))
    return vals


def potential_from_lambda_sq(phi: np.ndarray, func) -> float:
    return float(sum(func(lam * lam) for lam in eigenvalues(tuple(phi.tolist()))))


def numeric_hessian(phi0: np.ndarray, func, eps: float = 1.0e-3) -> np.ndarray:
    hess = np.zeros((3, 3), dtype=float)
    for i in range(3):
        for j in range(3):
            pp = phi0.copy(); pp[i] += eps; pp[j] += eps
            pm = phi0.copy(); pm[i] += eps; pm[j] -= eps
            mp = phi0.copy(); mp[i] -= eps; mp[j] += eps
            mm = phi0.copy(); mm[i] -= eps; mm[j] -= eps
            hess[i, j] = (
                potential_from_lambda_sq(pp, func)
                - potential_from_lambda_sq(pm, func)
                - potential_from_lambda_sq(mp, func)
                + potential_from_lambda_sq(mm, func)
            ) / (4.0 * eps * eps)
    return hess


def theorem_shift_algebra() -> list[np.ndarray]:
    print("\n" + "=" * 72)
    print("THEOREM SECTION 1: Commuting involution taste block")
    print("=" * 72)
    ops = shift_ops()
    i8 = np.eye(8, dtype=complex)
    for idx, op in enumerate(ops, start=1):
        diff = np.max(np.abs(op @ op - i8))
        check("theorem", f"S_{idx}^2 = I", diff < 1e-14, f"max diff = {diff:.1e}")
        herm = np.max(np.abs(op - op.conj().T))
        check("theorem", f"S_{idx} Hermitian", herm < 1e-14, f"max diff = {herm:.1e}")
    for i in range(3):
        for j in range(i + 1, 3):
            comm = np.max(np.abs(ops[i] @ ops[j] - ops[j] @ ops[i]))
            check("theorem", f"[S_{i+1}, S_{j+1}] = 0", comm < 1e-14, f"max diff = {comm:.1e}")
    return ops


def theorem_eigenstructure(ops: list[np.ndarray]) -> None:
    print("\n" + "=" * 72)
    print("THEOREM SECTION 2: Exact taste-block eigenstructure")
    print("=" * 72)

    def h(phi: tuple[float, float, float]) -> np.ndarray:
        return phi[0] * ops[0] + phi[1] * ops[1] + phi[2] * ops[2]

    test_points = [
        (1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (0.0, 0.0, 1.0),
        (1.0, 0.5, 0.3),
        (V_EW, 0.0, 0.0),
    ]
    for phi in test_points:
        num = sorted(np.linalg.eigvalsh(h(phi)))
        ana = sorted(eigenvalues(phi))
        diff = max(abs(a - b) for a, b in zip(num, ana))
        check("theorem", f"H{phi} eigenvalues match exact sign sum", diff < 1e-10, f"max diff = {diff:.1e}")

    at_vev = eigenvalues((V_EW, 0.0, 0.0))
    spread = max(abs(abs(val) - V_EW) for val in at_vev)
    check("theorem", "At phi=(v,0,0) all |lambda_s| = v", spread < 1e-10, f"spread = {spread:.1e}")


def theorem_binary_orthogonality() -> None:
    print("\n" + "=" * 72)
    print("THEOREM SECTION 3: Binary orthogonality identity")
    print("=" * 72)
    states = [(a, b, c) for a in range(2) for b in range(2) for c in range(2)]
    for i in range(3):
        for j in range(3):
            total = sum(((-1) ** s[i]) * ((-1) ** s[j]) for s in states)
            target = 8 if i == j else 0
            check("theorem", f"sum_s (-1)^s_{i+1} (-1)^s_{j+1} = {target}", total == target, f"computed = {total}")


def theorem_isotropy() -> None:
    print("\n" + "=" * 72)
    print("THEOREM SECTION 4: CW isotropy at axis-aligned minimum")
    print("=" * 72)
    phi0 = np.array([V_EW, 0.0, 0.0], dtype=float)

    funcs = [
        ("quartic-log", lambda x: (x + 1.0) ** 2 * (math.log(x + 1.0) - 1.5)),
        ("quadratic-polynomial", lambda x: (x + 9.0) ** 2),
        ("smooth-log1p", lambda x: math.log1p((x + 25.0) / 25.0)),
    ]

    for name, func in funcs:
        hess = numeric_hessian(phi0, func)
        diag = [hess[k, k] for k in range(3)]
        spread = (max(diag) - min(diag)) / max(1.0, abs(diag[0]))
        off = max(abs(hess[i, j]) for i in range(3) for j in range(3) if i != j)
        off_rel = off / max(1.0, abs(diag[0]))
        check("theorem", f"{name}: diagonal isotropy", spread < 1e-6, f"spread = {spread:.1e}")
        check("theorem", f"{name}: off-diagonals vanish", off_rel < 1e-6, f"off/diag = {off_rel:.1e}")


def bounded_gauge_split() -> tuple[float, float]:
    print("\n" + "=" * 72)
    print("BOUNDED SECTION 1: Gauge-only leading split")
    print("=" * 72)

    delta_gauge = (3.0 / (16.0 * math.pi ** 2)) * (
        2.0 * (G2_V / 2.0) ** 4 + ((G2_V ** 2 + GP_V ** 2) / 4.0) ** 2
    ) * V_EW ** 2
    m_taste_sq = MH_3L ** 2 - delta_gauge
    m_taste = math.sqrt(m_taste_sq)
    fractional = 100.0 * delta_gauge / (MH_3L ** 2)

    print(f"  v            = {V_EW:.12f} GeV")
    print(f"  g_2(v)       = {G2_V:.6f}")
    print(f"  g'(v)        = {GP_V:.6f}")
    print(f"  m_H          = {MH_3L:.2f} GeV")
    print(f"  delta_gauge  = {delta_gauge:.2f} GeV^2")
    print(f"  m_taste      = {m_taste:.2f} GeV")
    print(f"  split        = {MH_3L - m_taste:.2f} GeV ({fractional:.3f}%)")

    check("bounded", "delta_gauge > 0 on the gauge-only split model", delta_gauge > 0.0, f"delta = {delta_gauge:.2f} GeV^2")
    check("bounded", "m_taste^2 remains positive", m_taste_sq > 0.0, f"m_taste^2 = {m_taste_sq:.2f} GeV^2")
    check("bounded", "taste scalar is within 1 GeV of Higgs", abs(MH_3L - m_taste) < 1.0, f"|Δm| = {abs(MH_3L - m_taste):.2f} GeV")
    check("bounded", "leading split is sub-percent", fractional < 1.0, f"fractional split = {fractional:.3f}%")
    return m_taste, delta_gauge


def bounded_ewpt(m_taste: float) -> None:
    print("\n" + "=" * 72)
    print("BOUNDED SECTION 2: Scalar-only thermal-cubic estimate")
    print("=" * 72)

    lambda_h = MH_3L ** 2 / (2.0 * V_EW ** 2)
    m_w = G2_V * V_EW / 2.0
    m_z = math.sqrt(G2_V ** 2 + GP_V ** 2) * V_EW / 2.0
    e_gauge = (2.0 * m_w ** 3 + m_z ** 3) / (4.0 * math.pi * V_EW ** 3)
    kappa_taste = 2.0 * m_taste ** 2 / V_EW ** 2
    e_taste = 2.0 / (12.0 * math.pi) * (kappa_taste / 2.0) ** 1.5
    kappa_h = 2.0 * MH_3L ** 2 / V_EW ** 2
    e_higgs = 1.0 / (12.0 * math.pi) * (kappa_h / 2.0) ** 1.5
    vc_tc = 2.0 * (e_gauge + e_taste + e_higgs) / lambda_h

    print(f"  E_gauge   = {e_gauge:.6f}")
    print(f"  E_higgs   = {e_higgs:.6f}")
    print(f"  E_taste   = {e_taste:.6f}")
    print(f"  v_c/T_c   = {vc_tc:.6f}")

    check("bounded", "scalar-only estimate gives a nonzero first-order signal", vc_tc > 0.0, f"v_c/T_c = {vc_tc:.6f}")
    check("bounded", "scalar-only estimate stays below sphaleron-protection threshold", vc_tc < 1.0, f"v_c/T_c = {vc_tc:.6f}")


def main() -> int:
    print("=" * 72)
    print("FRONTIER: Taste-scalar Coleman-Weinberg isotropy")
    print("=" * 72)
    theorem_eigenstructure(theorem_shift_algebra())
    theorem_binary_orthogonality()
    theorem_isotropy()
    m_taste, _ = bounded_gauge_split()
    bounded_ewpt(m_taste)
    print("\n" + "=" * 72)
    print(f"SUMMARY: THEOREM PASS={THEOREM_PASS} BOUNDED PASS={BOUNDED_PASS} FAIL={FAIL}")
    print("=" * 72)
    return FAIL


if __name__ == "__main__":
    sys.exit(main())
