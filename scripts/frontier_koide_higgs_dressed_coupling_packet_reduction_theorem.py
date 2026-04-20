#!/usr/bin/env python3
"""
Frontier runner — Koide Higgs-dressed coupling-packet reduction theorem.

Companion to
`docs/KOIDE_HIGGS_DRESSED_COUPLING_PACKET_REDUCTION_THEOREM_NOTE_2026-04-20.md`.
"""

from __future__ import annotations

import numpy as np

from frontier_higgs_dressed_propagator_v1 import E1, GAMMA, H3, M_STAR, DELTA_STAR, Q_PLUS_STAR


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


def main() -> None:
    print("=" * 88)
    print("Koide Higgs-dressed coupling-packet reduction theorem")
    print("=" * 88)

    H_STAR = H3(M_STAR, DELTA_STAR, Q_PLUS_STAR)
    g = np.array([H_STAR[2, 0], H_STAR[1, 0]], dtype=complex)
    lambda_plus = Q_PLUS_STAR + DELTA_STAR - E1
    lambda_minus = Q_PLUS_STAR - DELTA_STAR + E1
    g_reduced = np.array([lambda_plus + 1j * GAMMA, lambda_minus], dtype=complex)

    check(
        "The omitted-channel coupling vector is exactly reconstructed from the two visible chamber links and the fixed half-gamma phase",
        np.max(np.abs(g - g_reduced)) < 1.0e-15,
        detail=f"g={np.round(g, 12).tolist()}",
    )
    check(
        "The first coupling arm is the chamber-slack link plus the fixed imaginary half-gamma",
        abs(g[0].real - lambda_plus) < 1.0e-15 and abs(g[0].imag - GAMMA) < 1.0e-15,
        detail=f"lambda_plus={lambda_plus:.12f}",
    )
    check(
        "The second coupling arm is a second visible chamber link rather than an independent complex datum",
        abs(g[1].real - lambda_minus) < 1.0e-15 and abs(g[1].imag) < 1.0e-15,
        detail=f"lambda_minus={lambda_minus:.12f}",
    )

    packet = np.outer(g, g.conj())
    packet_reduced = np.outer(g_reduced, g_reduced.conj())
    check(
        "The full rank-1 omitted-channel self-energy packet is exactly determined by that two-real chamber packet",
        np.max(np.abs(packet - packet_reduced)) < 1.0e-15,
    )
    check(
        "So the coherent self-energy carries only two real visible chamber degrees of freedom",
        np.linalg.matrix_rank(packet, tol=1.0e-10) == 1,
        detail=f"trace={np.trace(packet).real:.12f}",
    )

    print()
    print("Interpretation:")
    print("  The coherent omitted-channel vector g is not an arbitrary complex 2-vector.")
    print("  Once the retained fixed constants E1 and Gamma=1/2 are peeled off, it is")
    print("  exactly one visible two-link chamber packet (lambda_plus, lambda_minus).")
    print("  So the live transport object is sharper again:")
    print("      derive the visible two-link chamber packet from retained physics.")
    print()
    print(f"  lambda_plus  = {lambda_plus:.12f}")
    print(f"  lambda_minus = {lambda_minus:.12f}")
    print()
    print(f"PASS={PASS} FAIL={FAIL}")
    if FAIL:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
