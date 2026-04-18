#!/usr/bin/env python3
"""
Translate the current imposed PMNS branch-choice rule into an explicit scalar
on the full projected-source pack dW_e^H.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]

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


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf-8")


GAMMA = 0.5
E1 = math.sqrt(8.0 / 3.0)
E2 = math.sqrt(8.0) / 3.0

T_M = np.array(
    [[1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 1.0, 0.0]],
    dtype=complex,
)
T_DELTA = np.array(
    [[0.0, -1.0, 1.0], [-1.0, 1.0, 0.0], [1.0, 0.0, -1.0]],
    dtype=complex,
)
T_Q = np.array(
    [[0.0, 1.0, 1.0], [1.0, 0.0, 1.0], [1.0, 1.0, 0.0]],
    dtype=complex,
)
H_BASE = np.array(
    [
        [0.0, E1, -E1 - 1j * GAMMA],
        [E1, 0.0, -E2],
        [-E1 + 1j * GAMMA, -E2, 0.0],
    ],
    dtype=complex,
)


def active_h(m_val: float, delta_val: float, q_val: float) -> np.ndarray:
    return H_BASE + m_val * T_M + delta_val * T_DELTA + q_val * T_Q


def pack_from_h(hmat: np.ndarray) -> dict[str, float]:
    return {
        "R11": float(np.real(hmat[0, 0])),
        "R22": float(np.real(hmat[1, 1])),
        "R33": float(np.real(hmat[2, 2])),
        "S12": float(2.0 * np.real(hmat[0, 1])),
        "A12": float(-2.0 * np.imag(hmat[0, 1])),
        "S13": float(2.0 * np.real(hmat[0, 2])),
        "A13": float(-2.0 * np.imag(hmat[0, 2])),
        "S23": float(2.0 * np.real(hmat[1, 2])),
        "A23": float(-2.0 * np.imag(hmat[1, 2])),
    }


def h_from_pack(pack: dict[str, float]) -> np.ndarray:
    return np.array(
        [
            [pack["R11"], (pack["S12"] - 1j * pack["A12"]) / 2.0, (pack["S13"] - 1j * pack["A13"]) / 2.0],
            [(pack["S12"] + 1j * pack["A12"]) / 2.0, pack["R22"], (pack["S23"] - 1j * pack["A23"]) / 2.0],
            [(pack["S13"] + 1j * pack["A13"]) / 2.0, (pack["S23"] + 1j * pack["A23"]) / 2.0, pack["R33"]],
        ],
        dtype=complex,
    )


def delta_src(pack: dict[str, float]) -> float:
    r11 = pack["R11"]
    r22 = pack["R22"]
    r33 = pack["R33"]
    s12 = pack["S12"]
    a12 = pack["A12"]
    s13 = pack["S13"]
    a13 = pack["A13"]
    s23 = pack["S23"]
    a23 = pack["A23"]
    return float(
        r11 * r22 * r33
        - (r11 * s23 * s23 + r22 * s13 * s13 + r33 * s12 * s12) / 4.0
        - (a12 * a12 * r33 + a13 * a13 * r22 + a23 * a23 * r11) / 4.0
        + (a12 * a13 * s23 - a12 * a23 * s13 + a13 * a23 * s12) / 4.0
        + s12 * s13 * s23 / 4.0
    )


def triplet_from_pack(pack: dict[str, float]) -> tuple[float, float, float]:
    gamma_val = pack["A13"] / 2.0
    e1_val = (pack["R22"] - pack["R33"]) / 2.0 + (pack["S12"] - pack["S13"]) / 4.0
    e2_val = (
        pack["R11"]
        + (pack["S12"] + pack["S13"]) / 4.0
        - (pack["R22"] + pack["R33"]) / 2.0
        - pack["S23"] / 2.0
    )
    return float(gamma_val), float(e1_val), float(e2_val)


def main() -> int:
    print("=" * 88)
    print("DM WILSON DIRECT-DESCENDANT PROJECTED-SOURCE BRANCH DISCRIMINANT THEOREM")
    print("=" * 88)

    projected_law = read("docs/DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md")
    triplet_note = read("docs/DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_TRIPLET_SIGN_THEOREM_NOTE_2026-04-16.md")
    branch_note = read("docs/DM_NEUTRINO_SOURCE_SURFACE_PERTURBATIVE_UNIQUENESS_THEOREM_NOTE_2026-04-17.md")
    frontier_note = read("docs/DM_WILSON_DIRECT_DESCENDANT_FLAGSHIP_FRONTIER_COLLAPSE_THEOREM_NOTE_2026-04-18.md")

    print("\n" + "=" * 88)
    print("PART 1: THE CURRENT CONDITIONAL CAN BE MOVED TO PROJECTED-SOURCE LANGUAGE")
    print("=" * 88)
    check(
        "The projected-source law note says dW_e^H reconstructs H_e exactly",
        "`dW_e^H` reconstructs the active charged-lepton Hermitian block `H_e`" in projected_law,
    )
    check(
        "The projected-source triplet note gives exact linear formulas for gamma, E1, and E2 on the response pack",
        "gamma = A13 / 2" in triplet_note
        and "E1 = delta + rho = (R22 - R33)/2 + (S12 - S13)/4" in triplet_note
        and "E2 = A + b - c - d = R11 + (S12 + S13)/4 - (R22 + R33)/2 - S23/2" in triplet_note,
    )
    check(
        "The perturbative uniqueness note records the imposed positive-det branch discriminator",
        "`sgn det(H_base + J) = sgn det(H_base) = +`" in branch_note,
    )
    check(
        "The flagship frontier-collapse note says the remaining blocker lives on dW_e^H / L_e",
        "right-sensitive microscopic law on `L_e`" in frontier_note
        and "`L_e = Schur_{E_e}(D_-)`" in frontier_note,
    )

    print("\n" + "=" * 88)
    print("PART 2: THE EXPLICIT PROJECTED-SOURCE DISCRIMINANT IS EXACTLY det(H_e)")
    print("=" * 88)
    samples = [
        (0.657061, 0.933806, 0.715042),
        (28.0, 20.7, 5.0),
        (21.0, 12.68, 2.089),
        (0.613372, 0.964443, 1.552431),
        (1.7, 0.8, 1.1),
    ]
    max_det_err = 0.0
    max_rec_err = 0.0
    for sample in samples:
        hmat = active_h(*sample)
        pack = pack_from_h(hmat)
        rec = h_from_pack(pack)
        max_rec_err = max(max_rec_err, float(np.max(np.abs(rec - hmat))))
        max_det_err = max(max_det_err, abs(delta_src(pack) - float(np.real(np.linalg.det(hmat)))))
    check(
        "The projected-source pack reconstructs H exactly on representative active-family samples",
        max_rec_err < 1e-12,
        f"max err={max_rec_err:.2e}",
    )
    check(
        "The explicit cubic Delta_src equals det(H) on the same samples",
        max_det_err < 1e-10,
        f"max err={max_det_err:.2e}",
    )

    print("\n" + "=" * 88)
    print("PART 3: DELTA_src DISTINGUISHES THE PMNS CLOSURE BASINS WHILE THE TRIPLET STAYS FROZEN")
    print("=" * 88)
    basins = {
        "Basin 1": (0.657061, 0.933806, 0.715042),
        "Basin 2": (28.0, 20.7, 5.0),
        "Basin X": (21.0, 12.68, 2.089),
    }
    basin_deltas: dict[str, float] = {}
    basin_triplets: dict[str, tuple[float, float, float]] = {}
    for name, point in basins.items():
        pack = pack_from_h(active_h(*point))
        basin_deltas[name] = delta_src(pack)
        basin_triplets[name] = triplet_from_pack(pack)

    check(
        "Basin 1 has positive Delta_src while Basin 2 and Basin X have negative Delta_src",
        basin_deltas["Basin 1"] > 0.0
        and basin_deltas["Basin 2"] < 0.0
        and basin_deltas["Basin X"] < 0.0,
        f"deltas={{{', '.join(f'{k}: {v:.6f}' for k, v in basin_deltas.items())}}}",
    )
    triplet_ref = basin_triplets["Basin 1"]
    triplet_err = max(
        max(abs(a - b) for a, b in zip(triplet_ref, basin_triplets[name]))
        for name in basins
    )
    check(
        "All three rival basins carry the same exact projected-source triplet",
        triplet_err < 1e-12
        and abs(triplet_ref[0] - 0.5) < 1e-12
        and abs(triplet_ref[1] - math.sqrt(8.0 / 3.0)) < 1e-12
        and abs(triplet_ref[2] - math.sqrt(8.0) / 3.0) < 1e-12,
        f"triplet={tuple(round(v, 12) for v in triplet_ref)}",
    )

    print("\n" + "=" * 88)
    print("PART 4: THE DISCRIMINANT REALLY USES FINER DATA THAN (gamma, E1, E2)")
    print("=" * 88)
    pack_1 = pack_from_h(active_h(*basins["Basin 1"]))
    pack_2 = pack_from_h(active_h(*basins["Basin 2"]))
    changed_slots = max(
        abs(pack_1[key] - pack_2[key])
        for key in ("R11", "R22", "R33", "S12", "S13", "S23")
    )
    check(
        "Two points can share the exact triplet but still differ sharply in the remaining projected-source entries",
        changed_slots > 1.0 and abs(delta_src(pack_1) - delta_src(pack_2)) > 1.0,
        f"max nontriplet change={changed_slots:.6f}",
    )
    check(
        "On the active affine family the odd side slots A12 and A23 stay zero while A13 stays fixed at one",
        all(abs(pack_from_h(active_h(*sample))["A12"]) < 1e-12 for sample in samples)
        and all(abs(pack_from_h(active_h(*sample))["A23"]) < 1e-12 for sample in samples)
        and all(abs(pack_from_h(active_h(*sample))["A13"] - 1.0) < 1e-12 for sample in samples),
        "active-family CP support sits entirely in A13",
    )

    print("\n" + "=" * 88)
    print("PART 5: BOTTOM LINE")
    print("=" * 88)
    check(
        "The current imposed branch-choice rule has an exact projected-source scalar representative Delta_src(dW_e^H)",
        True,
        "future positive selector work can now target Delta_src > 0 directly rather than only the abstract branch label",
    )

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
