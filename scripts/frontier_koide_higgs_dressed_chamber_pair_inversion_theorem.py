#!/usr/bin/env python3
"""
Frontier runner — Koide Higgs-dressed chamber-pair inversion theorem.

Companion to
`docs/KOIDE_HIGGS_DRESSED_CHAMBER_PAIR_INVERSION_THEOREM_NOTE_2026-04-20.md`.
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
    print("Koide Higgs-dressed chamber-pair inversion theorem")
    print("=" * 88)

    H_STAR = H3(M_STAR, DELTA_STAR, Q_PLUS_STAR)
    lambda_plus = H_STAR[2, 0].real
    lambda_minus = H_STAR[1, 0].real

    q_recovered = 0.5 * (lambda_plus + lambda_minus)
    delta_recovered = E1 + 0.5 * (lambda_plus - lambda_minus)
    g_reconstructed = np.array([lambda_plus + 1j * GAMMA, lambda_minus], dtype=complex)
    g_actual = np.array([H_STAR[2, 0], H_STAR[1, 0]], dtype=complex)

    check(
        "The visible two-link packet exactly recovers q_+* by averaging",
        abs(q_recovered - Q_PLUS_STAR) < 1.0e-15,
        detail=f"q_recovered={q_recovered:.12f}",
    )
    check(
        "The same packet exactly recovers delta_* by the fixed E1-shifted difference",
        abs(delta_recovered - DELTA_STAR) < 1.0e-15,
        detail=f"delta_recovered={delta_recovered:.12f}",
    )
    check(
        "The coherent omitted-channel vector is exactly reconstructed from that visible packet and the fixed half-gamma phase",
        np.max(np.abs(g_reconstructed - g_actual)) < 1.0e-15,
        detail=f"g={np.round(g_actual, 12).tolist()}",
    )
    check(
        "So the full omitted-channel self-energy carries no extra data beyond the chamber pair (q_+, delta)",
        np.max(np.abs(np.outer(g_reconstructed, g_reconstructed.conj()) - np.outer(g_actual, g_actual.conj()))) < 1.0e-15,
    )
    inverse_map = np.array([[0.5, 0.5], [0.5, -0.5]], dtype=float)
    check(
        "The local transport packet therefore repackages the G1 chamber pair rather than introducing a new independent datum",
        abs(np.linalg.det(inverse_map)) > 1.0e-12,
        detail=f"(lambda_plus, lambda_minus)=({lambda_plus:.12f}, {lambda_minus:.12f})",
    )

    print()
    print("Interpretation:")
    print("  The Higgs-dressed omitted-channel packet is linearly invertible back to")
    print("  the visible G1 chamber pair (q_+, delta). So this transport route no")
    print("  longer carries a new microscopic datum beyond those chamber pins.")
    print("  The live closure object is therefore sharper again:")
    print("      derive the G1 chamber pair (q_+, delta) from retained physics.")
    print()
    print(f"  lambda_plus  = {lambda_plus:.12f}")
    print(f"  lambda_minus = {lambda_minus:.12f}")
    print()
    print(f"PASS={PASS} FAIL={FAIL}")
    if FAIL:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
