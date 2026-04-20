#!/usr/bin/env python3
"""
Shared nilpotent-chain helper layer for the reopened Wilson step-2 lane.

This file is the new source of truth for the sharpest local Wilson constructive
object. It packages the exact algebraic recovery formulas from one local
nilpotent chain generator N_chain to:

  - the local projections P1, P2, P3,
  - the full matrix-unit system on the physical two-edge chain,
  - the local Hermitian packet,
  - the restricted chain-plane embedding data,
  - the local path-algebra embedding data,
  - and the full 9-real Hermitian source basis relevant for dW_e^H / H_e.
"""

from __future__ import annotations

import sys

import numpy as np

from frontier_dm_leptogenesis_ne_projected_source_law_derivation import (
    hermitian_basis,
    hermitian_linear_responses,
    reconstruct_h_from_responses,
)

PASS_COUNT = 0
FAIL_COUNT = 0


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


def e(i: int, j: int, n: int = 3) -> np.ndarray:
    m = np.zeros((n, n), dtype=complex)
    m[i, j] = 1.0
    return m


def canonical_n_chain() -> np.ndarray:
    return e(0, 1) + e(1, 2)


def recover_chain_projections(n_chain: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    eye = np.eye(n_chain.shape[0], dtype=complex)
    p1 = eye - n_chain.conj().T @ n_chain
    p3 = eye - n_chain @ n_chain.conj().T
    p2 = n_chain.conj().T @ n_chain + n_chain @ n_chain.conj().T - eye
    return p1, p2, p3


def recover_chain_matrix_units(n_chain: np.ndarray) -> dict[str, np.ndarray]:
    p1, p2, p3 = recover_chain_projections(n_chain)
    e12 = p1 @ n_chain @ p2
    e23 = p2 @ n_chain @ p3
    e13 = n_chain @ n_chain
    e21 = e12.conj().T
    e32 = e23.conj().T
    e31 = e13.conj().T
    return {
        "E11": p1,
        "E22": p2,
        "E33": p3,
        "E12": e12,
        "E21": e21,
        "E23": e23,
        "E32": e32,
        "E13": e13,
        "E31": e31,
    }


def chain_plane_packet_from_n(n_chain: np.ndarray) -> dict[str, np.ndarray]:
    units = recover_chain_matrix_units(n_chain)
    return {
        "X12": units["E12"] + units["E21"],
        "Y12": -1j * units["E12"] + 1j * units["E21"],
        "X23": units["E23"] + units["E32"],
        "Y23": -1j * units["E23"] + 1j * units["E32"],
    }


def long_corner_packet_from_n(n_chain: np.ndarray) -> dict[str, np.ndarray]:
    units = recover_chain_matrix_units(n_chain)
    return {
        "X13": units["E13"] + units["E31"],
        "Y13": -1j * units["E13"] + 1j * units["E31"],
    }


def full_hermitian_basis_from_n(n_chain: np.ndarray) -> list[np.ndarray]:
    units = recover_chain_matrix_units(n_chain)
    chain = chain_plane_packet_from_n(n_chain)
    long = long_corner_packet_from_n(n_chain)
    return [
        units["E11"],
        units["E22"],
        units["E33"],
        chain["X12"],
        chain["Y12"],
        long["X13"],
        long["Y13"],
        chain["X23"],
        chain["Y23"],
    ]


def path_algebra_embedding_from_n(n_chain: np.ndarray) -> dict[str, np.ndarray]:
    return recover_chain_matrix_units(n_chain)


def build_synthetic_wilson_parent(
    h_target: np.ndarray,
    parent_dim: int = 5,
    spectator_eigs: tuple[float, ...] = (2.0, 3.0),
) -> dict[str, np.ndarray]:
    if parent_dim < 3:
        raise ValueError("parent_dim must be at least 3")
    i_e = np.zeros((parent_dim, 3), dtype=complex)
    i_e[:3, :3] = np.eye(3, dtype=complex)
    s_w = np.zeros((parent_dim, parent_dim), dtype=complex)
    s_w[:3, :3] = np.asarray(h_target, dtype=complex)
    for k, val in enumerate(spectator_eigs, start=3):
        if k < parent_dim:
            s_w[k, k] = val
    p_e = i_e @ i_e.conj().T
    return {"I_e": i_e, "P_e": p_e, "S_W": s_w}


def embedded_source(i_e: np.ndarray, x: np.ndarray) -> np.ndarray:
    return i_e @ np.asarray(x, dtype=complex) @ i_e.conj().T


def first_variation_from_resolvent(s_w: np.ndarray, source: np.ndarray) -> float:
    return float(np.real(np.trace(np.asarray(s_w, dtype=complex) @ np.asarray(source, dtype=complex))))


def response_pack_from_n_chain_sources(s_w: np.ndarray, i_e: np.ndarray, n_chain: np.ndarray) -> list[float]:
    return [
        first_variation_from_resolvent(s_w, embedded_source(i_e, x))
        for x in full_hermitian_basis_from_n(n_chain)
    ]


def generic_hermitian_target() -> np.ndarray:
    return np.array(
        [
            [0.84, 0.31 - 0.27j, -0.42 + 0.19j],
            [0.31 + 0.27j, -0.18, 0.57 + 0.11j],
            [-0.42 - 0.19j, 0.57 - 0.11j, 1.06],
        ],
        dtype=complex,
    )


def main() -> int:
    print("=" * 104)
    print("PERRON-FROBENIUS STEP-2 NILPOTENT-CHAIN HELPER LAYER")
    print("=" * 104)
    print()
    print("Question:")
    print("  Does one local nilpotent chain generator N_chain already recover the")
    print("  full local Wilson algebra/source data needed downstream?")

    n = canonical_n_chain()
    units = recover_chain_matrix_units(n)
    p1, p2, p3 = recover_chain_projections(n)
    packet = chain_plane_packet_from_n(n)
    long = long_corner_packet_from_n(n)

    proj_err = max(
        float(np.linalg.norm(p1 - e(0, 0))),
        float(np.linalg.norm(p2 - e(1, 1))),
        float(np.linalg.norm(p3 - e(2, 2))),
    )
    unit_err = max(
        float(np.linalg.norm(units["E12"] - e(0, 1))),
        float(np.linalg.norm(units["E23"] - e(1, 2))),
        float(np.linalg.norm(units["E13"] - e(0, 2))),
        float(np.linalg.norm(np.linalg.matrix_power(n, 3))),
    )
    check(
        "N_chain recovers the exact chain projections P1,P2,P3 and the downstream long corner E13 = N^2",
        proj_err < 1e-12 and unit_err < 1e-12,
        f"proj_err={proj_err:.2e}, unit_err={unit_err:.2e}",
    )

    basis_from_n = full_hermitian_basis_from_n(n)
    canonical_basis = hermitian_basis()
    basis_err = max(float(np.linalg.norm(a - b)) for a, b in zip(basis_from_n, canonical_basis))
    check(
        "The full Hermitian source basis recovered from N_chain matches the repo's canonical 9-real Hermitian basis exactly",
        basis_err < 1e-12,
        f"basis_err={basis_err:.2e}",
    )

    packet_err = max(
        float(np.linalg.norm(packet["X12"] - (e(0, 1) + e(1, 0)))),
        float(np.linalg.norm(packet["Y12"] - (-1j * e(0, 1) + 1j * e(1, 0)))),
        float(np.linalg.norm(packet["X23"] - (e(1, 2) + e(2, 1)))),
        float(np.linalg.norm(packet["Y23"] - (-1j * e(1, 2) + 1j * e(2, 1)))),
        float(np.linalg.norm(long["X13"] - (e(0, 2) + e(2, 0)))),
        float(np.linalg.norm(long["Y13"] - (-1j * e(0, 2) + 1j * e(2, 0)))),
    )
    check(
        "N_chain recovers both the nearest-neighbor Hermitian 4-packet and the downstream long-corner Hermitian pair",
        packet_err < 1e-12,
        f"packet_err={packet_err:.2e}",
    )

    h_target = generic_hermitian_target()
    responses = [float(np.real(np.trace(b @ h_target))) for b in basis_from_n]
    h_rec = reconstruct_h_from_responses(responses)
    response_err = float(np.linalg.norm(np.array(responses, dtype=float) - np.array(hermitian_linear_responses(h_target), dtype=float)))
    rec_err = float(np.linalg.norm(h_rec - h_target))
    check(
        "Responses on the N_chain-generated Hermitian basis reconstruct an arbitrary 3x3 Hermitian target exactly",
        response_err < 1e-12 and rec_err < 1e-12,
        f"(response_err,reconstruction_err)=({response_err:.2e},{rec_err:.2e})",
    )

    model = build_synthetic_wilson_parent(h_target)
    embedded_responses = response_pack_from_n_chain_sources(model["S_W"], model["I_e"], n)
    embed_err = float(
        np.linalg.norm(np.array(embedded_responses, dtype=float) - np.array(hermitian_linear_responses(h_target), dtype=float))
    )
    check(
        "On a synthetic embedded Wilson parent, the N_chain-generated Hermitian sources already produce the full projected response pack",
        embed_err < 1e-12,
        f"embed_err={embed_err:.2e}",
    )

    print("\n" + "=" * 104)
    print("RESULT")
    print("=" * 104)
    print("  Exact helper-layer answer:")
    print("    - one local nilpotent chain generator N_chain already recovers the")
    print("      full local path algebra, the Hermitian 4-packet, the long-corner pair,")
    print("      and the full 9-real Hermitian source basis")
    print("    - on an embedded Wilson parent, those N_chain-generated sources already")
    print("      reproduce the exact projected Hermitian response pack")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
