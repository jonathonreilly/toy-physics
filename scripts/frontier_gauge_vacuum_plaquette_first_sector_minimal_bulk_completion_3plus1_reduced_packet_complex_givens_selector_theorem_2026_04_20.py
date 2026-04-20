#!/usr/bin/env python3
"""
Canonical complex-Givens selector theorem for exact reduced projected-source
packet commutation on the selected retained `3d+1` slice.
"""

from __future__ import annotations

import math
import sys

import numpy as np
from scipy.optimize import least_squares

from frontier_dm_leptogenesis_dweh_even_split_transfer_layer import (
    TARGET,
    delta_live_from_projected_even_split,
    mass_from_projected_even_split,
    q_plus_from_projected_even_split,
    sparse_face_projected_data,
)
from frontier_dm_leptogenesis_k00_sparse_face_target_preimage_theorem import (
    solve_sparse_target_preimage,
)
from frontier_dm_leptogenesis_ne_projected_source_law_derivation import (
    hermitian_linear_responses,
)
from frontier_gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_3plus1_line_helper_2026_04_19 import (
    compressed_local_block_from_line,
)
from frontier_gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_3plus1_line_rho1_least_distortion_selector_theorem_2026_04_20 import (
    selected_line,
)

PASS_COUNT = 0
FAIL_COUNT = 0

ANGLE_LOWER = np.array([-1.55, -math.pi, -1.55, -math.pi, -1.55, -math.pi], dtype=float)
ANGLE_UPPER = np.array([1.55, math.pi, 1.55, math.pi, 1.55, math.pi], dtype=float)
RNG = np.random.default_rng(12)
SEEDS = [np.zeros(6, dtype=float)] + [
    RNG.uniform(ANGLE_LOWER, ANGLE_UPPER) for _ in range(40)
]
_SOLVE_CACHE: list[dict[str, np.ndarray | float]] | None = None


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    return condition


def target_packet4() -> np.ndarray:
    x, y, phase = solve_sparse_target_preimage()
    data = sparse_face_projected_data(np.array([x[0], x[1], y[0], phase], dtype=float))
    return np.array([data["E1"], data["E2"], data["S12"], data["S13"]], dtype=float)


def selected_real_slice_h() -> np.ndarray:
    line = selected_line()
    h, _responses, _live, _qmat = compressed_local_block_from_line(line)
    return np.asarray(h, dtype=complex)


def reduced_packet4_from_responses(responses: np.ndarray) -> np.ndarray:
    e1 = 0.5 * (responses[1] - responses[2]) + 0.25 * (responses[3] - responses[5])
    e2 = responses[0] + 0.25 * (responses[3] + responses[5]) - 0.5 * (responses[1] + responses[2]) - 0.5 * responses[7]
    return np.array([e1, e2, responses[3], responses[5]], dtype=float)


def live_from_reduced_packet4(packet4: np.ndarray) -> np.ndarray:
    e1, e2, s12, s13 = [float(x) for x in packet4]
    return np.array(
        [
            mass_from_projected_even_split(e2, s12, s13),
            delta_live_from_projected_even_split(e1, s12, s13),
            q_plus_from_projected_even_split(s12, s13),
        ],
        dtype=float,
    )


def complex_givens(i: int, j: int, theta: float, phi: float) -> np.ndarray:
    u = np.eye(3, dtype=complex)
    c = float(np.cos(theta))
    s = float(np.sin(theta))
    u[i, i] = c
    u[j, j] = c
    u[i, j] = -np.exp(-1j * phi) * s
    u[j, i] = np.exp(1j * phi) * s
    return u


def complex_givens_chain(params: np.ndarray) -> np.ndarray:
    t12, p12, t13, p13, t23, p23 = [float(x) for x in np.asarray(params, dtype=float)]
    return (
        complex_givens(0, 1, t12, p12)
        @ complex_givens(0, 2, t13, p13)
        @ complex_givens(1, 2, t23, p23)
    )


def reduced_packet_residual(params: np.ndarray) -> np.ndarray:
    h0 = selected_real_slice_h()
    u = complex_givens_chain(params)
    h = u.conj().T @ h0 @ u
    responses = np.array(hermitian_linear_responses(h), dtype=float)
    return reduced_packet4_from_responses(responses) - target_packet4()


def exact_givens_solutions() -> list[dict[str, np.ndarray | float]]:
    global _SOLVE_CACHE
    if _SOLVE_CACHE is not None:
        out: list[dict[str, np.ndarray | float]] = []
        for item in _SOLVE_CACHE:
            copied: dict[str, np.ndarray | float] = {}
            for key, value in item.items():
                if isinstance(value, np.ndarray):
                    copied[key] = np.array(value, copy=True)
                else:
                    copied[key] = value
            out.append(copied)
        return out

    h0 = selected_real_slice_h()
    target4 = target_packet4()
    sols: list[dict[str, np.ndarray | float]] = []
    for seed in SEEDS:
        result = least_squares(
            reduced_packet_residual,
            seed,
            bounds=(ANGLE_LOWER, ANGLE_UPPER),
            xtol=1.0e-12,
            ftol=1.0e-12,
            gtol=1.0e-12,
            max_nfev=5000,
        )
        resid = np.array(result.fun, dtype=float)
        norm = float(np.linalg.norm(resid))
        if norm >= 1.0e-9:
            continue
        params = np.array(result.x, dtype=float)
        u = complex_givens_chain(params)
        h = u.conj().T @ h0 @ u
        responses = np.array(hermitian_linear_responses(h), dtype=float)
        packet4 = reduced_packet4_from_responses(responses)
        dist = float(np.linalg.norm(u - np.eye(3, dtype=complex)))
        duplicate = False
        for item in sols:
            same_u = min(
                np.linalg.norm(u - np.asarray(item["u"])),
                np.linalg.norm(u + np.asarray(item["u"])),
            )
            if same_u < 1.0e-7:
                duplicate = True
                break
        if not duplicate:
            sols.append(
                {
                    "params": params,
                    "u": u,
                    "packet4": packet4,
                    "responses": responses,
                    "resid": resid,
                    "norm": norm,
                    "dist": dist,
                }
            )

    sols.sort(key=lambda item: float(item["dist"]))
    _SOLVE_CACHE = [
        {
            "params": np.array(item["params"], dtype=float),
            "u": np.array(item["u"], dtype=complex),
            "packet4": np.array(item["packet4"], dtype=float),
            "responses": np.array(item["responses"], dtype=float),
            "resid": np.array(item["resid"], dtype=float),
            "norm": float(item["norm"]),
            "dist": float(item["dist"]),
        }
        for item in sols
    ]
    return exact_givens_solutions()


def selected_givens_solution() -> dict[str, np.ndarray | float]:
    return exact_givens_solutions()[0]


def main() -> int:
    print("=" * 118)
    print("GAUGE-VACUUM PLAQUETTE FIRST-SECTOR MINIMAL-BULK COMPLETION 3D+1 REDUCED-PACKET COMPLEX-GIVENS SELECTOR")
    print("=" * 118)
    print()
    print("Question:")
    print("  On the canonical retained `3d` slice selected from the minimally-positive")
    print("  Wilson branch, is there a finite-parameter internal unitary law that")
    print("  exactly matches the reduced projected-source packet (E1,E2,S12,S13)?")

    sols = exact_givens_solutions()
    selected = selected_givens_solution()
    packet4 = np.asarray(selected["packet4"], dtype=float)
    target4 = target_packet4()
    live = live_from_reduced_packet4(packet4)
    gap = float(sols[1]["dist"] - sols[0]["dist"]) if len(sols) > 1 else float("inf")

    print()
    print(f"  exact-solution count in audited grammar      = {len(sols)}")
    print(f"  selected params                              = {np.round(np.asarray(selected['params'], dtype=float), 12).tolist()}")
    print(f"  selected reduced packet                      = {np.round(packet4, 12).tolist()}")
    print(f"  selected distortion to identity              = {float(selected['dist']):.12f}")
    if len(sols) > 1:
        print(f"  next exact distortion                        = {float(sols[1]['dist']):.12f}")
        print(f"  distortion gap                               = {gap:.12f}")
    print()

    check(
        "The selected retained real slice admits exact reduced-packet commutation inside the finite complex-Givens grammar G12·G13·G23",
        len(sols) > 0 and float(selected["norm"]) < 1.0e-9,
        f"best_norm={float(selected['norm']):.3e}",
    )
    check(
        "The selected complex-Givens dressing reproduces the exact reduced projected-source packet (E1,E2,S12,S13)",
        np.linalg.norm(packet4 - target4) < 1.0e-9,
        f"packet_err={np.linalg.norm(packet4 - target4):.3e}",
    )
    check(
        "Consequently the exact ordered even law (S12,S13) is now matched on the same selected retained slice",
        np.linalg.norm(packet4[2:] - target4[2:]) < 1.0e-9,
        f"pair_err={np.linalg.norm(packet4[2:] - target4[2:]):.3e}",
    )
    check(
        "Among the audited exact complex-Givens solutions, Frobenius distance to the identity has a strict minimum",
        len(sols) > 1 and gap > 1.0e-3,
        f"gap={gap:.6f}",
    )
    check(
        "The selected exact reduced-packet dressing lands on the observed live DM target as well",
        np.linalg.norm(live - TARGET) < 1.0e-9,
        f"live_err={np.linalg.norm(live - TARGET):.3e}",
    )

    print("\n" + "=" * 118)
    print("RESULT")
    print("=" * 118)
    print("  Stronger retained-slice law:")
    print("    - keep the canonical selected Wilson branch and the canonical selected")
    print("      retained `3d` slice from the complement-line theorem")
    print("    - inside that fixed slice, solve the reduced projected-source packet")
    print("      equation within the ordered complex-Givens grammar G12·G13·G23")
    print("    - choose the exact solution with least Frobenius distortion to the")
    print("      identity basis on that selected slice")
    print("    - this yields exact reduced projected-source commutation and the live")
    print("      DM target on the same selected retained slice")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
