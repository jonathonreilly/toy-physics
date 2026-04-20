#!/usr/bin/env python3
"""
Frontier runner — Koide Higgs-dressed basin-transfer no-go theorem.

Companion to
`docs/KOIDE_HIGGS_DRESSED_BASIN_TRANSFER_NO_GO_THEOREM_NOTE_2026-04-20.md`.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import brentq

from frontier_higgs_dressed_propagator_v1 import (
    E1,
    H3,
    direction_cos,
    embed_4x4_to_16,
    koide_Q,
    sigma_with_weight_operator,
)


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


CANDIDATES = [
    ("Basin 1", (0.657061342210, 0.933806343759, 0.715042329587)),
    ("Basin 2", (28.006, 20.722, 5.012)),
    ("Basin X", (21.128264, 12.680028, 2.089235)),
    ("CP-conjugate", (0.4074, 0.8771, 0.4463)),
    ("C_neg q<0", (0.9985, 1.4299, -1.291)),
]


def missing_axis_lift(H: np.ndarray, h0: float = 0.0) -> np.ndarray:
    W4 = np.zeros((4, 4), dtype=complex)
    W4[0, 0] = h0
    W4[1:, 1:] = H
    return W4


def sigma_data(H: np.ndarray, lambda_value: float, h0: float = 0.0) -> tuple[float, float]:
    W4 = missing_axis_lift(H, h0)
    evals, evecs = np.linalg.eigh(W4)
    diffs = lambda_value - evals
    if np.min(np.abs(diffs)) < 1.0e-9:
        raise ValueError("lambda too close to a pole")
    W4_res = evecs @ np.diag(1.0 / diffs) @ evecs.conj().T
    sigma = sigma_with_weight_operator(embed_4x4_to_16(W4_res))
    sigma_eigs = np.linalg.eigvalsh((sigma + sigma.conj().T) / 2.0)
    masses = np.abs(sigma_eigs)
    return koide_Q(masses), direction_cos(masses)


def q_residual(H: np.ndarray, lambda_value: float) -> float:
    return sigma_data(H, lambda_value)[0] - 2.0 / 3.0


def interval_roots(H: np.ndarray, left: float, right: float, samples: int = 600) -> list[float]:
    xs = np.linspace(left, right, samples)
    roots: list[float] = []
    prev_x = None
    prev_v = None
    for x in xs:
        try:
            value = q_residual(H, x)
        except ValueError:
            prev_x = None
            prev_v = None
            continue
        if not np.isfinite(value):
            prev_x = None
            prev_v = None
            continue
        if prev_v is not None and prev_v * value < 0.0:
            root = brentq(lambda y: q_residual(H, y), prev_x, x)
            if not roots or min(abs(root - old) for old in roots) > 1.0e-8:
                roots.append(root)
        prev_x = x
        prev_v = value
    return roots


def all_roots(H: np.ndarray) -> tuple[np.ndarray, list[float]]:
    poles = np.sort(np.linalg.eigvalsh(missing_axis_lift(H, 0.0)))
    epsilon = 1.0e-4
    intervals = [(float(poles[0]) - 5.0, float(poles[0]) - epsilon)]
    intervals.extend((float(poles[i]) + epsilon, float(poles[i + 1]) - epsilon) for i in range(3))
    intervals.append((float(poles[-1]) + epsilon, float(poles[-1]) + 5.0))
    roots: list[float] = []
    for left, right in intervals:
        if right <= left:
            continue
        roots.extend(interval_roots(H, left, right))
    return poles, sorted(roots)


def main() -> None:
    print("=" * 88)
    print("Koide Higgs-dressed basin-transfer no-go theorem")
    print("=" * 88)

    dets = []
    chamber_margins = []
    results = {}
    for label, triple in CANDIDATES:
        H = H3(*triple)
        dets.append(float(np.linalg.det(H).real))
        chamber_margins.append(float(triple[1] + triple[2] - E1))
        check(
            f"{label}: H(m, delta, q_+) is Hermitian",
            np.allclose(H, H.conj().T, atol=1.0e-14),
        )

    check(
        "The tested transport packet spans both C_base and C_neg chamber competitors",
        min(dets) < 0.0 < max(dets),
        detail=f"det-range=[{min(dets):.6f}, {max(dets):.6f}]",
    )
    check(
        "The tested packet also spans both chamber-satisfying and chamber-violating competitors",
        min(chamber_margins) < 0.0 < max(chamber_margins),
        detail=f"margin-range=[{min(chamber_margins):.6f}, {max(chamber_margins):.6f}]",
    )

    for label, triple in CANDIDATES:
        H = H3(*triple)
        poles, roots = all_roots(H)
        positive_small_roots = [root for root in roots if 0.0 < root < 1.0]
        small_root = min(positive_small_roots)
        q_value, cos_value = sigma_data(H, small_root)
        results[label] = {
            "small_root": small_root,
            "cos": cos_value,
            "roots": roots,
        }

        check(
            f"{label}: the missing-axis lift has four real poles",
            len(poles) == 4 and np.all(np.isreal(poles)),
            detail=f"poles={[round(float(p), 6) for p in poles]}",
        )
        check(
            f"{label}: the h_0 = 0 resolvent family has exactly eight Q=2/3 roots",
            len(roots) == 8,
            detail=f"roots={[round(root, 12) for root in roots]}",
        )
        check(
            f"{label}: there is a unique small positive Q=2/3 root below 1",
            len(positive_small_roots) == 1,
            detail=f"lambda_small={small_root:.12f}",
        )
        check(
            f"{label}: the small positive root lands exactly on Koide Q=2/3",
            abs(q_value - 2.0 / 3.0) < 1.0e-12,
            detail=f"Q={q_value:.12f}",
        )
        check(
            f"{label}: the same root still gives a strong charged-lepton direction match",
            cos_value > 0.97,
            detail=f"cos={cos_value:.12f}",
        )

    excluded_labels = ["Basin 2", "Basin X", "CP-conjugate", "C_neg q<0"]
    excluded_good = min(results[label]["cos"] for label in excluded_labels)
    check(
        "Excluded G1 competitors also carry the same high-cos small-root transport mechanism",
        excluded_good > 0.97,
        detail=f"min excluded cos={excluded_good:.12f}",
    )
    check(
        "The excluded CP-conjugate competitor actually matches the PDG sqrt(m) direction better than Basin 1 on this transport route",
        results["CP-conjugate"]["cos"] > results["Basin 1"]["cos"],
        detail=(
            f"cos_CP={results['CP-conjugate']['cos']:.12f}, "
            f"cos_B1={results['Basin 1']['cos']:.12f}"
        ),
    )
    check(
        "So the missing-axis Higgs-dressed resolvent route is basin-indiscriminate over the current G1 competitor set",
        len(CANDIDATES) == sum(1 for label in CANDIDATES if results[label[0]]["cos"] > 0.97),
        detail="all tested competitors support the same small positive root mechanism",
    )

    print()
    print("Interpretation:")
    print("  The missing-axis Higgs-dressed resolvent route is not the physical basin")
    print("  selector. Basin 1, Basin 2, Basin X, the chamber-violating CP-conjugate")
    print("  point, and the C_neg q<0 point all carry the same eight-root pattern,")
    print("  including a unique small positive Koide root with strong charged-lepton")
    print("  direction cosine. The excluded CP-conjugate point even beats Basin 1 on")
    print("  the direction-cos metric. So this transport avenue cannot bypass the")
    print("  open G1 chamber/basin selection program; it inherits it.")
    print()
    for label, _ in CANDIDATES:
        print(
            f"  {label:14s} small_root={results[label]['small_root']:.12f} "
            f"cos={results[label]['cos']:.12f}"
        )
    print()
    print(f"PASS={PASS} FAIL={FAIL}")
    if FAIL:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
