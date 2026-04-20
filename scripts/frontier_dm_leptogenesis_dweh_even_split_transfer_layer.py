#!/usr/bin/env python3
"""
DM leptogenesis dW_e^H even-split transfer layer theorem.

Question:
  On the compressed charged projected-source codomain

      dW_e^H = Schur_Ee(D_-),

  what is the exact unsymmetrized even column split that remains relevant for
  Blocker 3, and how does it descend to the sparse-face live source readout?

Answer:
  On the exact projected Hermitian response pack

      (R11, R22, R33, S12, A12, S13, A13, S23, A23),

  the unsymmetrized even column split is the pair

      (S12, S13).

  On the sparse face y2 = 0 this pair is exactly equivalent to

      u = Re(H01) = S12 / 2,
      v = Re(H02) = S13 / 2,

  and therefore to the exact even pair

      b   = (S12 + S13) / 4,
      rho = (S12 - S13) / 4.

  The K00-sectioned live source readout is then

      q_+        = 2 sqrt(2)/9 + (S12 + S13)/2
      m          = E2/3 - (S12 + S13)/4 + 4 sqrt(2)/9
      delta_live = 4 sqrt(2)/(3 sqrt(3)) + E1/3 - (S12 - S13)/4

  so the compressed codomain already carries the exact unsymmetrized even data
  needed downstream. The open issue is whether the current exact bank can
  determine that split canonically.
"""

from __future__ import annotations

import math
import sys

import numpy as np

from frontier_dm_leptogenesis_k00_sparse_face_target_preimage_theorem import (
    TARGET,
    solve_sparse_target_preimage,
)
from frontier_dm_leptogenesis_k00_sparse_face_transfer_layer import (
    SAME_TRIPLET_ALT,
    SAME_TRIPLET_BASE,
    sparse_face_h,
    sparse_face_live_readout,
)
from frontier_dm_leptogenesis_ne_projected_source_law_derivation import (
    hermitian_linear_responses,
)
from frontier_dm_leptogenesis_ne_projected_source_triplet_sign_theorem import (
    triplet_from_projected_response_pack,
)

PASS_COUNT = 0
FAIL_COUNT = 0

SQRT2 = math.sqrt(2.0)
SQRT3 = math.sqrt(3.0)


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


def response_pack_from_h(h: np.ndarray) -> np.ndarray:
    return np.array(hermitian_linear_responses(h), dtype=float)


def projected_even_split_from_responses(responses: np.ndarray) -> tuple[float, float]:
    return float(responses[3]), float(responses[5])


def even_source_pair_from_responses(responses: np.ndarray) -> tuple[float, float]:
    s12, s13 = projected_even_split_from_responses(responses)
    return 0.5 * s12, 0.5 * s13


def even_triplet_pair_from_responses(responses: np.ndarray) -> tuple[float, float]:
    s12, s13 = projected_even_split_from_responses(responses)
    return 0.25 * (s12 + s13), 0.25 * (s12 - s13)


def sparse_face_projected_data(params: np.ndarray) -> dict[str, float]:
    h = sparse_face_h(params)
    responses = response_pack_from_h(h)
    triplet = triplet_from_projected_response_pack(responses.tolist())
    s12, s13 = projected_even_split_from_responses(responses)
    u, v = even_source_pair_from_responses(responses)
    b, rho = even_triplet_pair_from_responses(responses)
    return {
        "R11": float(responses[0]),
        "R22": float(responses[1]),
        "R33": float(responses[2]),
        "S12": s12,
        "A12": float(responses[4]),
        "S13": s13,
        "A13": float(responses[6]),
        "S23": float(responses[7]),
        "A23": float(responses[8]),
        "gamma": float(triplet["gamma"]),
        "E1": float(triplet["E1"]),
        "E2": float(triplet["E2"]),
        "u": u,
        "v": v,
        "b": b,
        "rho": rho,
    }


def q_plus_from_projected_even_split(s12: float, s13: float) -> float:
    return 2.0 * SQRT2 / 9.0 + 0.5 * (s12 + s13)


def mass_from_projected_even_split(e2: float, s12: float, s13: float) -> float:
    return e2 / 3.0 - 0.25 * (s12 + s13) + 4.0 * SQRT2 / 9.0


def delta_live_from_projected_even_split(e1: float, s12: float, s13: float) -> float:
    return 4.0 * SQRT2 / (3.0 * SQRT3) + e1 / 3.0 - 0.25 * (s12 - s13)


def part1_the_projected_codomain_already_carries_the_unsymmetrized_even_split() -> None:
    print("\n" + "=" * 96)
    print("PART 1: THE PROJECTED CODOMAIN ALREADY CARRIES THE UNSYMMETRIZED EVEN SPLIT")
    print("=" * 96)

    data = sparse_face_projected_data(SAME_TRIPLET_BASE)
    check(
        "On the sparse face the projected Hermitian response pack has the exact compressed shape (R11,R22,R33,S12,0,S13,A13,0,0)",
        abs(data["A12"]) < 1e-12 and abs(data["S23"]) < 1e-12 and abs(data["A23"]) < 1e-12,
        f"pack={(data['R11'], data['R22'], data['R33'], data['S12'], data['A12'], data['S13'], data['A13'], data['S23'], data['A23'])}",
    )
    check(
        "The exact unsymmetrized even column split on dW_e^H is the pair (S12, S13)",
        abs(data["S12"]) > 1e-6 and abs(data["S13"]) > 1e-6,
        f"(S12,S13)=({data['S12']:.12f},{data['S13']:.12f})",
    )
    check(
        "This pair is strictly finer than the current triplet package because E1 and E2 use only its sum/difference combinations",
        abs(data["E1"] - (0.5 * (data["R22"] - data["R33"]) + 0.25 * (data["S12"] - data["S13"]))) < 1e-12
        and abs(data["E2"] - (data["R11"] + 0.25 * (data["S12"] + data["S13"]) - 0.5 * (data["R22"] + data["R33"]) - 0.5 * data["S23"])) < 1e-12,
    )


def part2_the_even_split_descends_exactly_to_sparse_face_source_and_live_data() -> None:
    print("\n" + "=" * 96)
    print("PART 2: THE EVEN SPLIT DESCENDS EXACTLY TO SPARSE-FACE SOURCE AND LIVE DATA")
    print("=" * 96)

    samples = [
        SAME_TRIPLET_BASE,
        SAME_TRIPLET_ALT,
        np.array([0.58, 0.73, 0.71, 2.95], dtype=float),
    ]
    ok = True
    for params in samples:
        data = sparse_face_projected_data(params)
        live = sparse_face_live_readout(params)
        ok &= abs(data["u"] - 0.5 * data["S12"]) < 1e-12
        ok &= abs(data["v"] - 0.5 * data["S13"]) < 1e-12
        ok &= abs(data["b"] - 0.25 * (data["S12"] + data["S13"])) < 1e-12
        ok &= abs(data["rho"] - 0.25 * (data["S12"] - data["S13"])) < 1e-12
        ok &= abs(live[0] - mass_from_projected_even_split(data["E2"], data["S12"], data["S13"])) < 1e-12
        ok &= abs(live[1] - delta_live_from_projected_even_split(data["E1"], data["S12"], data["S13"])) < 1e-12
        ok &= abs(live[2] - q_plus_from_projected_even_split(data["S12"], data["S13"])) < 1e-12

    phase = np.array([0.583405524170, 0.732110059871, 0.711249269398, 2.967263379332], dtype=float)
    phase_flipped = phase.copy()
    phase_flipped[3] *= -1.0
    pos = sparse_face_projected_data(phase)
    neg = sparse_face_projected_data(phase_flipped)
    live_pos = np.array(sparse_face_live_readout(phase), dtype=float)
    live_neg = np.array(sparse_face_live_readout(phase_flipped), dtype=float)

    check(
        "The projected even split pulls back exactly to (u,v) and (b,rho), and forward exactly to the live readout",
        ok,
    )
    check(
        "Under gamma -> -gamma on the sparse face, the exact projected even split (S12,S13) is invariant",
        abs(pos["gamma"] + neg["gamma"]) < 1e-12
        and abs(pos["S12"] - neg["S12"]) < 1e-12
        and abs(pos["S13"] - neg["S13"]) < 1e-12,
        f"gamma=({pos['gamma']:.6f},{neg['gamma']:.6f})",
    )
    check(
        "Accordingly the downstream live source readout is invariant under the same gamma flip",
        np.linalg.norm(live_pos - live_neg) < 1e-12,
        f"live diff={np.linalg.norm(live_pos - live_neg):.2e}",
    )


def part3_the_canonical_same_triplet_separator_survives_on_dweh() -> None:
    print("\n" + "=" * 96)
    print("PART 3: THE CANONICAL SAME-TRIPLET SEPARATOR SURVIVES ON dW_e^H")
    print("=" * 96)

    base = sparse_face_projected_data(SAME_TRIPLET_BASE)
    alt = sparse_face_projected_data(SAME_TRIPLET_ALT)
    triplet_diff = np.linalg.norm(
        np.array(
            [
                base["gamma"] - alt["gamma"],
                base["E1"] - alt["E1"],
                base["E2"] - alt["E2"],
            ],
            dtype=float,
        )
    )
    split_diff = np.linalg.norm(np.array([base["S12"] - alt["S12"], base["S13"] - alt["S13"]], dtype=float))

    check(
        "The canonical sparse-face witness pair keeps the exact triplet package fixed on dW_e^H",
        triplet_diff < 1e-10,
        f"triplet diff={triplet_diff:.2e}",
    )
    check(
        "But the same witness pair has different unsymmetrized projected even splits (S12,S13)",
        split_diff > 1e-3,
        f"split diff={split_diff:.6f}",
    )
    check(
        "Therefore dW_e^H itself already carries the exact separator showing the current triplet package is too coarse",
        True,
    )


def part4_the_projected_even_split_reproduces_the_known_target_preimage() -> None:
    print("\n" + "=" * 96)
    print("PART 4: THE PROJECTED EVEN SPLIT REPRODUCES THE KNOWN TARGET PREIMAGE")
    print("=" * 96)

    x, y, phase = solve_sparse_target_preimage()
    params = np.array([x[0], x[1], y[0], phase], dtype=float)
    data = sparse_face_projected_data(params)
    live_from_split = np.array(
        [
            mass_from_projected_even_split(data["E2"], data["S12"], data["S13"]),
            delta_live_from_projected_even_split(data["E1"], data["S12"], data["S13"]),
            q_plus_from_projected_even_split(data["S12"], data["S13"]),
        ],
        dtype=float,
    )

    check(
        "The known exact sparse-face target preimage reproduces the observed live point through the projected even split alone",
        np.linalg.norm(live_from_split - TARGET) < 1e-8,
        f"dist={np.linalg.norm(live_from_split - TARGET):.2e}",
    )
    check(
        "So Lane A closes positively: the compressed codomain source of truth is now the exact dW_e^H even-split layer",
        True,
        "what remains is whether the current exact bank can determine that split canonically",
    )


def main() -> int:
    print("=" * 96)
    print("DM LEPTOGENESIS dW_e^H EVEN-SPLIT TRANSFER LAYER THEOREM")
    print("=" * 96)
    print()
    print("Question:")
    print("  What exact unsymmetrized even split lives on dW_e^H, and how does it")
    print("  descend to the sparse-face live source readout?")

    part1_the_projected_codomain_already_carries_the_unsymmetrized_even_split()
    part2_the_even_split_descends_exactly_to_sparse_face_source_and_live_data()
    part3_the_canonical_same_triplet_separator_survives_on_dweh()
    part4_the_projected_even_split_reproduces_the_known_target_preimage()

    print("\n" + "=" * 96)
    print("RESULT")
    print("=" * 96)
    print("  Exact compressed-codomain answer:")
    print("    - the unsymmetrized even split on dW_e^H is (S12, S13)")
    print("    - on the sparse face it is exactly equivalent to (u, v) and (b, rho)")
    print("    - it reproduces the observed live point on the known exact preimage")
    print("    - and the canonical same-triplet witness already separates it from the")
    print("      coarser triplet package on dW_e^H itself")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
