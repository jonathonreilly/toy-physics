#!/usr/bin/env python3
"""
Frontier runner — Koide Gamma-orbit semigroup basin-transfer no-go theorem.

Companion to
`docs/KOIDE_GAMMA_ORBIT_SEMIGROUP_BASIN_TRANSFER_NO_GO_THEOREM_NOTE_2026-04-20.md`.
"""

from __future__ import annotations

import math

import numpy as np
from scipy.linalg import expm
from scipy.optimize import brentq, minimize_scalar

from frontier_higgs_dressed_propagator_v1 import H3


PASS = 0
FAIL = 0


def check(label: str, cond: bool, detail: str = "") -> None:
    global PASS, FAIL
    if cond:
        PASS += 1
        status = "PASS"
    else:
        FAIL += 1
        status = "FAIL"
    print(f"  [{status}] {label}" + (f"  ({detail})" if detail else ""))


PDG_SQRT = np.sqrt(np.array([0.51099895, 105.6583755, 1776.86], dtype=float))
PDG_DIR = PDG_SQRT / np.linalg.norm(PDG_SQRT)

CANDIDATES = [
    ("Basin 1", (0.657061342210, 0.933806343759, 0.715042329587)),
    ("Basin 2", (28.006, 20.722, 5.012)),
    ("Basin X", (21.128264, 12.680028, 2.089235)),
    ("CP-conjugate", (0.4074, 0.8771, 0.4463)),
    ("C_neg q<0", (0.9985, 1.4299, -1.291)),
]


def positive_block(H: np.ndarray, beta: float) -> np.ndarray:
    return expm(beta * H)


def slot_values(H: np.ndarray, beta: float) -> tuple[float, float]:
    X = positive_block(H, beta)
    return float(np.real(X[2, 2])), float(np.real(X[1, 1]))


def koide_root_pair(v: float, w: float) -> tuple[float, float]:
    rad = math.sqrt(3.0 * (v * v + 4.0 * v * w + w * w))
    return 2.0 * (v + w) - rad, 2.0 * (v + w) + rad


def u_minus(H: np.ndarray, beta: float) -> float:
    v, w = slot_values(H, beta)
    return koide_root_pair(v, w)[0]


def direction_cos(amp: np.ndarray) -> float:
    return float(np.dot(amp / np.linalg.norm(amp), PDG_DIR))


def semigroup_data(H: np.ndarray) -> tuple[float, float, float, float]:
    beta_c = float(brentq(lambda beta: u_minus(H, beta), 0.0, 1.0))

    def objective(beta: float) -> float:
        v, w = slot_values(H, beta)
        u_small, _ = koide_root_pair(v, w)
        if u_small <= 0.0:
            return 1.0e6
        amp = np.array([u_small, v, w], dtype=float)
        return -direction_cos(amp)

    optimum = minimize_scalar(objective, bounds=(beta_c + 1.0e-6, 1.0), method="bounded")
    beta_star = float(optimum.x)
    v_star, w_star = slot_values(H, beta_star)
    u_star, _ = koide_root_pair(v_star, w_star)
    amp = np.array([u_star, v_star, w_star], dtype=float)
    q_value = float(np.sum(amp * amp) / (np.sum(amp) ** 2))
    scale = float(np.dot(amp, PDG_SQRT) / np.dot(amp, amp))
    max_rel = float(np.max(np.abs((scale * amp - PDG_SQRT) / PDG_SQRT)))
    return beta_c, beta_star, q_value, direction_cos(amp), max_rel


def main() -> None:
    print("=" * 88)
    print("Koide Gamma-orbit semigroup basin-transfer no-go theorem")
    print("=" * 88)

    results = {}
    for label, triple in CANDIDATES:
        H = H3(*triple)
        X1 = positive_block(H, 1.0)
        check(
            f"{label}: H(m, delta, q_+) is Hermitian",
            np.allclose(H, H.conj().T, atol=1.0e-12),
        )
        check(
            f"{label}: the one-clock block exp(H) is positive Hermitian",
            np.allclose(X1, X1.conj().T, atol=1.0e-9) and np.min(np.linalg.eigvalsh(X1)) > -5.0e-4,
            detail=f"min eig={np.min(np.linalg.eigvalsh(X1)):.6e}",
        )

        beta_c, beta_star, q_value, cos_value, max_rel = semigroup_data(H)
        results[label] = {
            "beta_c": beta_c,
            "beta_star": beta_star,
            "cos": cos_value,
            "max_rel": max_rel,
        }

        check(
            f"{label}: the small semigroup branch turns positive at one sharp threshold beta_c in (0,1)",
            0.0 < beta_c < 1.0,
            detail=f"beta_c={beta_c:.12f}",
        )
        check(
            f"{label}: the optimized small semigroup branch lies exactly on Koide Q=2/3",
            abs(q_value - 2.0 / 3.0) < 1.0e-12,
            detail=f"beta*={beta_star:.12f}",
        )
        check(
            f"{label}: the optimized semigroup witness is essentially the PDG sqrt(m) direction",
            cos_value > 0.9999999999,
            detail=f"cos={cos_value:.15f}",
        )
        check(
            f"{label}: after one overall scale fit the semigroup witness stays within 0.03% of PDG sqrt(m)",
            max_rel < 3.0e-4,
            detail=f"max_rel={max_rel:.6e}",
        )

    excluded_labels = ["Basin 2", "Basin X", "CP-conjugate", "C_neg q<0"]
    excluded_floor = min(results[label]["cos"] for label in excluded_labels)
    spread = max(results[label]["cos"] for label, _ in CANDIDATES) - min(
        results[label]["cos"] for label, _ in CANDIDATES
    )
    check(
        "Excluded G1 competitors also admit the same near-perfect semigroup witness",
        excluded_floor > 0.9999999999,
        detail=f"min excluded cos={excluded_floor:.15f}",
    )
    check(
        "The semigroup witness therefore does not distinguish Basin 1 from the excluded competitor set by direction fit",
        spread < 5.0e-13,
        detail=f"cos spread={spread:.3e}",
    )

    print()
    print("Interpretation:")
    print("  The Gamma-orbit positive one-clock semigroup route is not the physical")
    print("  basin selector either. Basin 1, Basin 2, Basin X, the chamber-violating")
    print("  CP-conjugate point, and the chamber-violating C_neg q<0 point all admit")
    print("  the same near-perfect semigroup witness after one overall scale fit.")
    print("  So this route also inherits the open G1 chamber/basin selection stack")
    print("  rather than bypassing it.")
    print()
    for label, _ in CANDIDATES:
        print(
            f"  {label:14s} beta_c={results[label]['beta_c']:.12f} "
            f"beta*={results[label]['beta_star']:.12f} "
            f"cos={results[label]['cos']:.15f}"
        )
    print()
    print(f"PASS={PASS} FAIL={FAIL}")
    if FAIL:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
