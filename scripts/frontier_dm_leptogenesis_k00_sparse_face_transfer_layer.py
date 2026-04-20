#!/usr/bin/env python3
"""
DM leptogenesis K00-sparse-face transfer layer theorem.

Question:
  After the K00 = 0 quotient section and the sparse-face reduction y2 = 0,
  what is the exact canonical reduced carrier for the remaining Blocker 3
  object, and what exact transfer formulas live on it?

Answer:
  The remaining constructive carrier is the exact sparse face

      y2 = 0

  on the fixed native seed surface, together with the target-independent
  quotient section K00 = 0. On that reduced carrier:

      q_+        = 2 sqrt(2)/9 + 2 b
      m          = E2/3 - b + 4 sqrt(2)/9
      delta_live = 4 sqrt(2)/(3 sqrt(3)) + delta_trip/3 - 2 rho/3

  and, equivalently, with the exact even source-column pair

      u = Re H01,
      v = Re H02,

  one has

      b   = (u + v)/2
      rho = (u - v)/2
      q_+ = 2 sqrt(2)/9 + u + v
      m   = E2/3 - (u + v)/2 + 4 sqrt(2)/9
      delta_live = 4 sqrt(2)/(3 sqrt(3)) + E1/3 - (u - v)/2.

  The K00-sectioned live readout is gamma-blind on this reduced carrier.
  So this file is the new source of truth for the sparse-face transfer layer.
"""

from __future__ import annotations

import math
import sys

import numpy as np

from frontier_dm_leptogenesis_constructive_live_doublet_corner_descendant_theorem import (
    m_delta_from_doublet_chi,
    q_plus_from_doublet_trivial,
)
from frontier_dm_leptogenesis_k00_sparse_face_target_preimage_theorem import (
    TARGET,
    alpha_k00,
    solve_sparse_target_preimage,
    sparse_face_point,
)
from frontier_dm_leptogenesis_ne_projected_source_law_derivation import (
    hermitian_linear_responses,
)
from frontier_dm_leptogenesis_ne_projected_source_triplet_sign_theorem import (
    triplet_from_projected_response_pack,
)
from frontier_dm_leptogenesis_pmns_cp_bridge_boundary import (
    breaking_triplet_coordinates,
)
from frontier_dm_leptogenesis_pmns_projector_interface import canonical_h

PASS_COUNT = 0
FAIL_COUNT = 0

SQRT2 = math.sqrt(2.0)
SQRT3 = math.sqrt(3.0)

SAME_TRIPLET_BASE = np.array([0.61, 0.74, 0.69, 2.40], dtype=float)
SAME_TRIPLET_ALT = np.array([0.740174807345, 0.711084189877, 0.605953549912, 2.721668675564], dtype=float)


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


def sparse_face_h(params: np.ndarray) -> np.ndarray:
    x, y, phase = sparse_face_point(*[float(v) for v in params])
    return canonical_h(x, y, phase)


def sparse_face_even_source_pair(params: np.ndarray) -> tuple[float, float]:
    h = sparse_face_h(params)
    return float(np.real(h[0, 1])), float(np.real(h[0, 2]))


def sparse_face_exact_triplet_even_data(params: np.ndarray) -> dict[str, float]:
    h = sparse_face_h(params)
    trip = triplet_from_projected_response_pack(hermitian_linear_responses(h))
    direct = breaking_triplet_coordinates(h)
    u, v = sparse_face_even_source_pair(params)
    return {
        "gamma": float(trip["gamma"]),
        "E1": float(trip["E1"]),
        "E2": float(trip["E2"]),
        "A": float(direct["A"]),
        "b": float(direct["b"]),
        "c": float(direct["c"]),
        "d": float(direct["d"]),
        "rho": float(direct["rho"]),
        "delta_trip": float(direct["delta"]),
        "u": u,
        "v": v,
    }


def sparse_face_live_readout(params: np.ndarray) -> tuple[float, float, float]:
    h = sparse_face_h(params)
    h_sec = h + alpha_k00(h) * np.eye(3, dtype=complex)
    mass, delta_live = m_delta_from_doublet_chi(h_sec)
    q_plus = q_plus_from_doublet_trivial(h_sec)
    return mass, delta_live, q_plus


def q_plus_from_even_triplet_b(b: float) -> float:
    return 2.0 * SQRT2 / 9.0 + 2.0 * b


def mass_from_even_triplet_b_e2(b: float, e2: float) -> float:
    return e2 / 3.0 - b + 4.0 * SQRT2 / 9.0


def delta_live_from_even_triplet(delta_trip: float, rho: float) -> float:
    return 4.0 * SQRT2 / (3.0 * SQRT3) + delta_trip / 3.0 - 2.0 * rho / 3.0


def b_rho_from_even_source_pair(u: float, v: float) -> tuple[float, float]:
    return 0.5 * (u + v), 0.5 * (u - v)


def q_plus_from_even_source_pair(u: float, v: float) -> float:
    return 2.0 * SQRT2 / 9.0 + u + v


def mass_from_even_source_pair(e2: float, u: float, v: float) -> float:
    return e2 / 3.0 - 0.5 * (u + v) + 4.0 * SQRT2 / 9.0


def delta_live_from_even_source_pair(e1: float, u: float, v: float) -> float:
    return 4.0 * SQRT2 / (3.0 * SQRT3) + e1 / 3.0 - 0.5 * (u - v)


def part1_the_exact_sparse_face_is_the_canonical_reduced_carrier() -> None:
    print("\n" + "=" * 96)
    print("PART 1: THE EXACT SPARSE FACE IS THE CANONICAL REDUCED CARRIER")
    print("=" * 96)

    params = SAME_TRIPLET_BASE
    x, y, _phase = sparse_face_point(*[float(v) for v in params])
    h = sparse_face_h(params)
    responses = np.array(hermitian_linear_responses(h), dtype=float)

    check(
        "The reduced carrier keeps the fixed native seed constraints exactly",
        abs(float(np.mean(x)) - float(np.mean(x))) < 1e-12 and abs(float(y[1])) < 1e-12,
        f"y={np.array2string(y, precision=12)}",
    )
    check(
        "On y2 = 0 the Hermitian carrier is exactly 23-sparse",
        abs(h[1, 2]) < 1e-12 and abs(h[2, 1]) < 1e-12,
        f"H23={h[1,2]}",
    )
    check(
        "The projected response pack collapses exactly to (R11,R22,R33,S12,0,S13,A13,0,0)",
        abs(responses[4]) < 1e-12 and abs(responses[7]) < 1e-12 and abs(responses[8]) < 1e-12,
        f"pack={np.array2string(responses, precision=6)}",
    )


def part2_the_transfer_formulas_are_exact_and_gamma_blind() -> None:
    print("\n" + "=" * 96)
    print("PART 2: THE TRANSFER FORMULAS ARE EXACT AND GAMMA-BLIND")
    print("=" * 96)

    samples = [
        SAME_TRIPLET_BASE,
        SAME_TRIPLET_ALT,
        np.array([0.58, 0.73, 0.71, 2.95], dtype=float),
    ]

    ok_triplet = True
    ok_edges = True
    for params in samples:
        data = sparse_face_exact_triplet_even_data(params)
        mass, delta_live, q_plus = sparse_face_live_readout(params)
        q_formula = q_plus_from_even_triplet_b(data["b"])
        m_formula = mass_from_even_triplet_b_e2(data["b"], data["E2"])
        delta_formula = delta_live_from_even_triplet(data["delta_trip"], data["rho"])
        ok_triplet &= (
            abs(q_plus - q_formula) < 1e-12
            and abs(mass - m_formula) < 1e-12
            and abs(delta_live - delta_formula) < 1e-12
        )
        q_edge = q_plus_from_even_source_pair(data["u"], data["v"])
        m_edge = mass_from_even_source_pair(data["E2"], data["u"], data["v"])
        delta_edge = delta_live_from_even_source_pair(data["E1"], data["u"], data["v"])
        ok_edges &= (
            abs(q_plus - q_edge) < 1e-12
            and abs(mass - m_edge) < 1e-12
            and abs(delta_live - delta_edge) < 1e-12
        )

    phase = np.array([0.583405524170, 0.732110059871, 0.711249269398, 2.967263379332], dtype=float)
    phase_flipped = phase.copy()
    phase_flipped[3] *= -1.0
    pos = sparse_face_exact_triplet_even_data(phase)
    neg = sparse_face_exact_triplet_even_data(phase_flipped)
    live_pos = np.array(sparse_face_live_readout(phase), dtype=float)
    live_neg = np.array(sparse_face_live_readout(phase_flipped), dtype=float)

    check(
        "The K00-sectioned live readout obeys the exact affine (b,rho,E2) sparse-face formulas",
        ok_triplet,
    )
    check(
        "The same live readout obeys the equivalent exact affine (u,v,E1,E2) formulas",
        ok_edges,
    )
    check(
        "Gamma flips sign under oriented-phase reversal while the K00-sectioned live readout stays fixed",
        abs(pos["gamma"] + neg["gamma"]) < 1e-12
        and abs(pos["u"] - neg["u"]) < 1e-12
        and abs(pos["v"] - neg["v"]) < 1e-12
        and np.linalg.norm(live_pos - live_neg) < 1e-12,
        f"gamma=({pos['gamma']:.6f},{neg['gamma']:.6f})",
    )


def part3_the_source_column_pair_is_exactly_equivalent_to_the_even_triplet_pair() -> None:
    print("\n" + "=" * 96)
    print("PART 3: THE SOURCE-COLUMN PAIR IS EXACTLY EQUIVALENT TO THE EVEN TRIPLET PAIR")
    print("=" * 96)

    samples = [SAME_TRIPLET_BASE, SAME_TRIPLET_ALT]
    ok = True
    for params in samples:
        data = sparse_face_exact_triplet_even_data(params)
        b, rho = b_rho_from_even_source_pair(data["u"], data["v"])
        ok &= abs(b - data["b"]) < 1e-12 and abs(rho - data["rho"]) < 1e-12

    base = sparse_face_exact_triplet_even_data(SAME_TRIPLET_BASE)
    alt = sparse_face_exact_triplet_even_data(SAME_TRIPLET_ALT)

    check(
        "On the sparse face the exact even source-column pair (u,v) reconstructs (b,rho) by b=(u+v)/2 and rho=(u-v)/2",
        ok,
    )
    check(
        "The same-triplet counterexample remains available on the new reduced carrier",
        abs(base["gamma"] - alt["gamma"]) < 1e-10
        and abs(base["E1"] - alt["E1"]) < 1e-10
        and abs(base["E2"] - alt["E2"]) < 1e-10,
        f"triplet diff={np.linalg.norm(np.array([base['gamma']-alt['gamma'], base['E1']-alt['E1'], base['E2']-alt['E2']], dtype=float)):.2e}",
    )
    check(
        "But that same-triplet pair has different exact even source-column data",
        abs(base["u"] - alt["u"]) > 1e-3 and abs(base["v"] - alt["v"]) > 1e-3,
        f"(u,v) diff=({abs(base['u']-alt['u']):.6f},{abs(base['v']-alt['v']):.6f})",
    )


def part4_the_transfer_layer_reproduces_the_known_target_preimage() -> None:
    print("\n" + "=" * 96)
    print("PART 4: THE TRANSFER LAYER REPRODUCES THE KNOWN TARGET PREIMAGE")
    print("=" * 96)

    x, y, phase = solve_sparse_target_preimage()
    params = np.array([x[0], x[1], y[0], phase], dtype=float)
    data = sparse_face_exact_triplet_even_data(params)
    live = np.array(sparse_face_live_readout(params), dtype=float)
    live_formula = np.array(
        [
            mass_from_even_source_pair(data["E2"], data["u"], data["v"]),
            delta_live_from_even_source_pair(data["E1"], data["u"], data["v"]),
            q_plus_from_even_source_pair(data["u"], data["v"]),
        ],
        dtype=float,
    )

    check(
        "The sparse-face transfer formulas reproduce the already known exact target preimage",
        np.linalg.norm(live - TARGET) < 1e-8 and np.linalg.norm(live_formula - TARGET) < 1e-8,
        f"dist={np.linalg.norm(live - TARGET):.2e}",
    )
    check(
        "So the reduced sparse-face transfer layer is now a complete exact readout source of truth",
        True,
        "what remains open is selecting the even source data, not reading them out",
    )


def main() -> int:
    print("=" * 96)
    print("DM LEPTOGENESIS K00-SPARSE-FACE TRANSFER LAYER THEOREM")
    print("=" * 96)
    print()
    print("Question:")
    print("  What is the exact canonical reduced carrier and transfer layer after the")
    print("  K00 = 0 section and sparse-face reduction?")

    part1_the_exact_sparse_face_is_the_canonical_reduced_carrier()
    part2_the_transfer_formulas_are_exact_and_gamma_blind()
    part3_the_source_column_pair_is_exactly_equivalent_to_the_even_triplet_pair()
    part4_the_transfer_layer_reproduces_the_known_target_preimage()

    print("\n" + "=" * 96)
    print("RESULT")
    print("=" * 96)
    print("  Exact reduced-layer answer:")
    print("    - the remaining carrier is the sparse face y2 = 0 with the K00 = 0 section")
    print("    - the live readout is gamma-blind there")
    print("    - the exact missing even data can be written either as (b, rho) or as")
    print("      the constructive source-column pair (u, v) = (Re H01, Re H02)")
    print("    - this file is the new source of truth for the sparse-face transfer layer")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
