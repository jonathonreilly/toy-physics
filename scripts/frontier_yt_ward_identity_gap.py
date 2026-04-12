#!/usr/bin/env python3
"""
Ward-identity blocker probe for the top-Yukawa normalization lane.

This runner verifies the rigorous algebraic pieces already in hand and then
states the exact missing identity needed to upgrade the conditional theorem to
a closed normalization result.
"""

from __future__ import annotations

import numpy as np

PASS_COUNT = 0
FAIL_COUNT = 0


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if ok else "FAIL"
    if ok:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    print(f"  [{status}] {tag}: {msg}")


I2 = np.eye(2, dtype=complex)
sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)

G1 = np.kron(np.kron(sx, I2), I2)
G2 = np.kron(np.kron(sy, sx), I2)
G3 = np.kron(np.kron(sy, sy), sx)
G5 = 1j * G1 @ G2 @ G3
P_PLUS = (np.eye(8, dtype=complex) + G5) / 2.0


def main() -> None:
    print("=" * 78)
    print("TOP YUKAWA WARD-IDENTITY BLOCKER")
    print("=" * 78)
    print()

    g5_sq_err = np.linalg.norm(G5 @ G5 - np.eye(8))
    report("gamma5_squared", g5_sq_err < 1e-12, f"Gamma_5^2 = I (err={g5_sq_err:.2e})")

    proj_err = np.linalg.norm(P_PLUS @ P_PLUS - P_PLUS)
    report("projector_idempotent", proj_err < 1e-12, f"P_+^2 = P_+ (err={proj_err:.2e})")

    tr_ratio = np.trace(P_PLUS).real / 8.0
    report("projector_trace_half", abs(tr_ratio - 0.5) < 1e-12, f"Tr(P_+)/dim = {tr_ratio:.4f}")

    print()
    print("BLOCKER:")
    print("  The remaining missing theorem is the lattice Ward identity")
    print("  that matches the Yukawa normalization to the gauge-link normalization.")
    print()
    print("  Missing identity:")
    print("    Z_Y = Z_g")
    print("  Equivalent normalized-trace form:")
    print("    N_c * y_t^2 = g_s^2 * Tr(P_+)/dim(taste)")
    print()
    print("  Imported assumptions still in use:")
    print("    - gauge and Yukawa vertices share the same lattice link normalization")
    print("    - g_s is the correct renormalized input for that shared normalization")
    print("    - no extra independent vertex factor appears between lattice and continuum")
    print()
    print("  Conditional consequence if the identity is supplied:")
    print("    y_t = g_s / sqrt(6)")
    print()
    print(f"FINAL SCORE: {PASS_COUNT} PASS, {FAIL_COUNT} FAIL")


if __name__ == "__main__":
    main()
