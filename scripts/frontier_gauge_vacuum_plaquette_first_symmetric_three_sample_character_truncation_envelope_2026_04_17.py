#!/usr/bin/env python3
"""
Exact first-retained character-truncation envelope for the first symmetric
three-sample plaquette PF target.
"""

from __future__ import annotations

import cmath
import math
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.special import iv


ROOT = Path(__file__).resolve().parents[1]

THEOREM_PASS = 0
SUPPORT_PASS = 0
FAIL = 0

BETA = 6.0
ARG = BETA / 3.0
MODE_MAX = 80


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


def highest_weight_triple(p: int, q: int) -> list[int]:
    return [p + q, q, 0]


def coefficient_matrix(mode: int, lam: list[int]) -> np.ndarray:
    return np.array(
        [[iv(mode + lam[j] + i - j, ARG) for j in range(3)] for i in range(3)],
        dtype=float,
    )


def wilson_character_coefficient(p: int, q: int) -> float:
    lam = highest_weight_triple(p, q)
    total = 0.0
    for mode in range(-MODE_MAX, MODE_MAX + 1):
        total += float(np.linalg.det(coefficient_matrix(mode, lam)))
    return total


def normalized_link_eigenvalue(p: int, q: int, c00: float) -> float:
    return wilson_character_coefficient(p, q) / (dim_su3(p, q) * c00)


def radical_entries() -> dict[str, sp.Expr]:
    rt2 = sp.sqrt(2)
    return {
        "a": -3 * sp.sqrt(2 - rt2),
        "b": -3 * rt2 + 3 * sp.sqrt(2 - sp.sqrt(2 + rt2)) + 3 * sp.sqrt(2 - sp.sqrt(2 - rt2)),
        "c": 16
        + 8 * sp.sqrt(2 + rt2)
        - 8 * sp.sqrt(2 + sp.sqrt(2 + rt2))
        - 8 * sp.sqrt(2 + sp.sqrt(2 - rt2)),
        "d": 3 * rt2 + 3 * sp.sqrt(2 - sp.sqrt(2 + rt2)) - 3 * sp.sqrt(2 - sp.sqrt(2 - rt2)),
        "e": 16
        - 8 * sp.sqrt(2 + rt2)
        - 8 * sp.sqrt(2 + sp.sqrt(2 + rt2))
        + 8 * sp.sqrt(2 + sp.sqrt(2 - rt2)),
    }


def sample_angles() -> dict[str, tuple[float, float]]:
    return {
        "A": (-13.0 * math.pi / 16.0, 5.0 * math.pi / 8.0),
        "B": (-5.0 * math.pi / 16.0, -7.0 * math.pi / 16.0),
        "C": (7.0 * math.pi / 16.0, -11.0 * math.pi / 16.0),
    }


def torus_point(theta1: float, theta2: float) -> tuple[complex, complex, complex]:
    return (
        cmath.exp(1j * theta1),
        cmath.exp(1j * theta2),
        cmath.exp(-1j * (theta1 + theta2)),
    )


def character_value(p: int, q: int, point: tuple[complex, complex, complex]) -> complex:
    lam = highest_weight_triple(p, q)
    exponents_num = [lam[j] + 2 - j for j in range(3)]
    exponents_den = [2 - j for j in range(3)]
    num = np.array([[point[i] ** exponents_num[j] for j in range(3)] for i in range(3)], dtype=complex)
    den = np.array([[point[i] ** exponents_den[j] for j in range(3)] for i in range(3)], dtype=complex)
    return complex(np.linalg.det(num) / np.linalg.det(den))


def orbit_coefficient(rho: dict[tuple[int, int], float], p: int, q: int) -> float:
    if p == q:
        return float(dim_su3(p, q) * rho[(p, q)])
    return float(dim_su3(p, q) * rho[(p, q)] + dim_su3(q, p) * rho[(q, p)])


def retained_formula(entries: dict[str, sp.Expr], rho10: float, rho11: float) -> dict[str, float]:
    a = float(sp.N(entries["a"], 50))
    b = float(sp.N(entries["b"], 50))
    c = float(sp.N(entries["c"], 50))
    d = float(sp.N(entries["d"], 50))
    e = float(sp.N(entries["e"], 50))
    return {
        "A": 1.0 + a * rho10,
        "B": 1.0 + b * rho10 + c * rho11,
        "C": 1.0 + d * rho10 + e * rho11,
    }


def main() -> int:
    char_note = read("docs/GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_CHARACTER_MEASURE_THEOREM_NOTE.md")
    radical_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_EXACT_RADICAL_RECONSTRUCTION_MAP_NOTE_2026-04-17.md"
    )
    local_note = read("docs/GAUGE_VACUUM_PLAQUETTE_LOCAL_ENVIRONMENT_FACTORIZATION_THEOREM_NOTE.md")

    entries = radical_entries()
    a = float(sp.N(entries["a"], 50))
    b = float(sp.N(entries["b"], 50))
    c = float(sp.N(entries["c"], 50))
    d = float(sp.N(entries["d"], 50))
    e = float(sp.N(entries["e"], 50))

    angles = sample_angles()
    points = {name: torus_point(*pair) for name, pair in angles.items()}

    # Exact first retained formulas from the explicit sample matrix.
    retained_rows = {
        "A": np.array([1.0, a, 0.0], dtype=float),
        "B": np.array([1.0, b, c], dtype=float),
        "C": np.array([1.0, d, e], dtype=float),
    }

    # Character-bound support on a small exact box.
    box = [(p, q) for p in range(4) for q in range(4)]
    char_bound_gap = 0.0
    for name, point in points.items():
        for p, q in box:
            char_bound_gap = max(char_bound_gap, abs(character_value(p, q, point)) - dim_su3(p, q))

    # Verify the retained rows against direct character evaluation.
    retained_eval_gap = 0.0
    for name, point in points.items():
        phi0 = character_value(0, 0, point)
        phi1 = 3.0 * (character_value(1, 0, point) + character_value(0, 1, point))
        phi2 = 8.0 * character_value(1, 1, point)
        direct = np.array([phi0.real, phi1.real, phi2.real], dtype=float)
        retained_eval_gap = max(retained_eval_gap, float(np.max(np.abs(direct - retained_rows[name]))))

    # Finite positive symmetric witness for the tail envelope.
    rho = {
        (0, 0): 1.0,
        (1, 0): 0.12,
        (0, 1): 0.12,
        (1, 1): 0.03,
        (2, 0): 0.02,
        (0, 2): 0.02,
        (2, 1): 0.01,
        (1, 2): 0.01,
        (2, 2): 0.008,
        (3, 0): 0.006,
        (0, 3): 0.006,
        (3, 1): 0.004,
        (1, 3): 0.004,
        (3, 2): 0.002,
        (2, 3): 0.002,
        (3, 3): 0.001,
    }

    rho10 = rho[(1, 0)]
    rho11 = rho[(1, 1)]
    retained_witness = retained_formula(entries, rho10, rho11)
    tau_box = 0.0
    for (p, q), coeff in rho.items():
        if (p, q) not in {(0, 0), (1, 0), (0, 1), (1, 1)}:
            tau_box += (dim_su3(p, q) ** 2) * coeff

    full_witness: dict[str, float] = {}
    tails: dict[str, float] = {}
    tail_envelope_gap = 0.0
    for name, point in points.items():
        total = 0.0 + 0.0j
        for (p, q), coeff in rho.items():
            total += dim_su3(p, q) * coeff * character_value(p, q, point)
        full_witness[name] = float(total.real)
        tails[name] = full_witness[name] - retained_witness[name]
        tail_envelope_gap = max(tail_envelope_gap, abs(tails[name]) - tau_box)

    # Local retained witness from the explicit four-link Wilson factor.
    c00 = wilson_character_coefficient(0, 0)
    a10 = normalized_link_eigenvalue(1, 0, c00)
    a11 = normalized_link_eigenvalue(1, 1, c00)
    local_rho10 = a10**4
    local_rho11 = a11**4
    local_witness = retained_formula(entries, local_rho10, local_rho11)

    # Identity retained coefficients.
    identity_retained = np.array([1.0, 18.0, 64.0], dtype=float)

    print("=" * 110)
    print("GAUGE-VACUUM PLAQUETTE FIRST SYMMETRIC THREE-SAMPLE CHARACTER-TRUNCATION ENVELOPE")
    print("=" * 110)
    print()
    print("Exact first-retained radical rows")
    print(f"  W_A row = [1, {a:.12f}, 0]")
    print(f"  W_B row = [1, {b:.12f}, {c:.12f}]")
    print(f"  W_C row = [1, {d:.12f}, {e:.12f}]")
    print(f"  identity retained row = {identity_retained.tolist()}")
    print()
    print("Finite positive symmetric witness for the universal tail envelope")
    print(f"  rho_(1,0), rho_(1,1)                    = {rho10:.6f}, {rho11:.6f}")
    print(f"  Tau_box                                 = {tau_box:.12f}")
    for name in ("A", "B", "C"):
        print(
            f"  {name}: retained={retained_witness[name]:.12f}  "
            f"tail={tails[name]: .12f}  full={full_witness[name]:.12f}"
        )
    print()
    print("Exact beta=6 local retained witness")
    print(f"  a_(1,0)(6)^4                            = {local_rho10:.15f}")
    print(f"  a_(1,1)(6)^4                            = {local_rho11:.15f}")
    for name in ("A", "B", "C"):
        print(f"  Z_hat_{name}^(loc,1)                     = {local_witness[name]:.15f}")
    print()
    print(f"  max retained-evaluation gap             = {retained_eval_gap:.3e}")
    print(f"  max character-bound excess on box       = {char_bound_gap:.3e}")
    print(f"  max tail-envelope excess                = {tail_envelope_gap:.3e}")
    print()

    check(
        "The character-measure note already fixes rho_(p,q)(6) >= 0, rho_(p,q)(6)=rho_(q,p)(6), and rho_(0,0)(6)=1",
        "`rho_(p,q)(beta) >= 0`" in char_note
        and "`rho_(p,q)(beta) = rho_(q,p)(beta)`" in char_note
        and "`rho_(0,0)(beta) = 1`" in char_note,
        bucket="SUPPORT",
    )
    check(
        "The exact radical reconstruction note already fixes the first symmetric three-sample map and the exact W_A decoupling",
        "exact radical-form three-sample matrix" in radical_note and "F_(A,2) = 0" in radical_note,
        bucket="SUPPORT",
    )
    check(
        "The local/environment factorization note already fixes the explicit four-link Wilson factor a_(p,q)(6)^4",
        "`D_beta^mix,norm chi_(p,q) = a_(p,q)(beta)^4 chi_(p,q)`" in local_note,
        bucket="SUPPORT",
    )
    check(
        "The first symmetric retained sample formulas agree with direct character evaluation on W_A, W_B, W_C",
        retained_eval_gap < 1.0e-12,
        detail=f"max retained gap = {retained_eval_gap:.3e}",
    )
    check(
        "The exact W_A retained formula depends only on rho_(1,0)(6) because the chi_(1,1) orbit vanishes there",
        abs(retained_rows["A"][2]) < 1.0e-15,
        detail=f"W_A third entry = {retained_rows['A'][2]:.3e}",
    )
    check(
        "Low-box SU(3) character evaluations at W_A, W_B, W_C satisfy the universal bound |chi_(p,q)(W)| <= d_(p,q)",
        char_bound_gap < 1.0e-12,
        detail=f"max excess = {char_bound_gap:.3e}",
    )
    check(
        "For a positive symmetric finite-box witness, the retained truncation error at each named sample is bounded by the omitted identity tail mass",
        tail_envelope_gap < 1.0e-12,
        detail=f"max tail-envelope excess = {tail_envelope_gap:.3e}",
    )
    check(
        "The explicit beta=6 local four-link Wilson coefficients produce a concrete same-surface retained witness triple without claiming the residual environment solve",
        0.0 < local_rho11 < local_rho10 < 1.0
        and local_witness["A"] < local_witness["B"] < local_witness["C"],
        detail=(
            f"a10^4={local_rho10:.12f}, a11^4={local_rho11:.12f}, "
            f"local witness={[round(local_witness[k], 12) for k in ('A', 'B', 'C')]}"
        ),
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
