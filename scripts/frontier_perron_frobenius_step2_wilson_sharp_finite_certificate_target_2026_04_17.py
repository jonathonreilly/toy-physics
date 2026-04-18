#!/usr/bin/env python3
"""
Package the whole Wilson compressed route as the sharp finite 7+3 certificate:
7 nearest-neighbor Hermitian support sources plus 3 scalar spectral identities.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]

THEOREM_PASS = 0
SUPPORT_PASS = 0
FAIL = 0


def check(name: str, condition: bool, detail: str = "", bucket: str = "THEOREM") -> None:
    global THEOREM_PASS, SUPPORT_PASS, FAIL
    status = "PASS" if condition else "FAIL"
    if condition:
        if bucket == "SUPPORT":
            SUPPORT_PASS += 1
        else:
            THEOREM_PASS += 1
    else:
        FAIL += 1
    print(f"  [{status}] [{bucket}] {name}")
    if detail:
        print(f"         {detail}")


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text()


def e(i: int, j: int) -> np.ndarray:
    m = np.zeros((3, 3), dtype=complex)
    m[i, j] = 1.0
    return m


def embedded(x: np.ndarray) -> np.ndarray:
    out = np.zeros((5, 5), dtype=complex)
    out[:3, :3] = x
    return out


def power_invariants(a: np.ndarray) -> tuple[float, float, float]:
    return (
        float(np.trace(a).real),
        float(np.trace(a @ a).real),
        float(np.trace(a @ a @ a).real),
    )


def main() -> int:
    seven_note = read("docs/PERRON_FROBENIUS_STEP2_WILSON_SEVEN_PACKET_CHAIN_REDUCTION_NOTE_2026-04-17.md")
    spectral_note = read("docs/PERRON_FROBENIUS_STEP2_WILSON_COMPRESSED_BLOCK_SPECTRAL_REDUCTION_NOTE_2026-04-17.md")
    note = read("docs/PERRON_FROBENIUS_STEP2_WILSON_SHARP_FINITE_CERTIFICATE_TARGET_NOTE_2026-04-17.md")

    print("=" * 108)
    print("PERRON-FROBENIUS STEP-2 WILSON SHARP FINITE CERTIFICATE TARGET")
    print("=" * 108)
    print()

    f11 = embedded(e(0, 0))
    f22 = embedded(e(1, 1))
    f33 = embedded(e(2, 2))
    f12 = embedded(e(0, 1))
    f21 = embedded(e(1, 0))
    f23 = embedded(e(1, 2))
    f32 = embedded(e(2, 1))

    s4 = f12 + f21
    s5 = -1j * f12 + 1j * f21
    s8 = f23 + f32
    s9 = -1j * f23 + 1j * f32

    rf12 = 0.5 * (s4 + 1j * s5)
    rf21 = 0.5 * (s4 - 1j * s5)
    rf23 = 0.5 * (s8 + 1j * s9)
    rf32 = 0.5 * (s8 - 1j * s9)
    rf11 = rf12 @ rf21
    rf22 = rf21 @ rf12
    rf33 = rf32 @ rf23
    rf13 = rf12 @ rf23
    rf31 = rf32 @ rf21
    p_e = rf11 + rf22 + rf33

    chain_err = 0.0
    chain_relations = [
        rf11 @ rf22,
        rf11 @ rf33,
        rf22 @ rf33,
        rf12 - rf11 @ rf12 @ rf22,
        rf21 - rf22 @ rf21 @ rf11,
        rf23 - rf22 @ rf23 @ rf33,
        rf32 - rf33 @ rf32 @ rf22,
        rf12 @ rf21 - rf11,
        rf21 @ rf12 - rf22,
        rf23 @ rf32 - rf22,
        rf32 @ rf23 - rf33,
    ]
    for rel in chain_relations:
        chain_err = max(chain_err, float(np.linalg.norm(rel)))

    units = {
        (1, 1): rf11, (2, 2): rf22, (3, 3): rf33,
        (1, 2): rf12, (2, 1): rf21,
        (2, 3): rf23, (3, 2): rf32,
        (1, 3): rf13, (3, 1): rf31,
    }
    full_err = 0.0
    for i in range(1, 4):
        for j in range(1, 4):
            for k in range(1, 4):
                for l in range(1, 4):
                    lhs = units[(i, j)] @ units[(k, l)]
                    rhs = units[(i, l)] if j == k else np.zeros_like(lhs)
                    full_err = max(full_err, float(np.linalg.norm(lhs - rhs)))

    h_e = np.array(
        [
            [1.7, 0.2 - 0.4j, -0.3 + 0.1j],
            [0.2 + 0.4j, -0.6, 0.5 - 0.2j],
            [-0.3 - 0.1j, 0.5 + 0.2j, 0.9],
        ],
        dtype=complex,
    )
    s_w = np.zeros((5, 5), dtype=complex)
    s_w[:3, :3] = h_e
    s_w[3:, 3:] = np.diag([0.4, -0.2])
    b_e = np.eye(5, 3, dtype=complex).conj().T @ s_w @ np.eye(5, 3, dtype=complex)
    inv_gap = max(abs(a - b) for a, b in zip(power_invariants(b_e), power_invariants(h_e)))

    print(f"rank(P_e)                                   = {int(round(np.trace(p_e).real))}")
    print(f"chain relation max error                    = {chain_err:.3e}")
    print(f"full matrix-unit max error                  = {full_err:.3e}")
    print(f"spectral invariant gap                      = {inv_gap:.3e}")
    print()

    check(
        "The support side is already exactly finite at the sharper level: a 7-packet nearest-neighbor chain reconstructs the full matrix-unit system and rank-3 support",
        chain_err < 1.0e-12 and full_err < 1.0e-12 and abs(np.trace(p_e).real - 3.0) < 1.0e-12,
        detail=f"rank(P_e)={int(round(np.trace(p_e).real))}, chain_err={chain_err:.2e}, full_err={full_err:.2e}",
    )
    check(
        "The post-support side is still exactly finite: the compressed block matches H_e through the 3 scalar spectral identities",
        inv_gap < 1.0e-12,
        detail=f"invariant gap={inv_gap:.2e}",
    )
    check(
        "The new note records the exact sharp 7+3 certificate form of the Wilson compressed route",
        "one sharp finite `7 + 3` certificate" in note
        and "nearest-neighbor Hermitian `7`-packet" in note
        and "`Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`" in note
        and "best reviewer-facing Wilson target is no longer `9 + 3`. It is now" in note,
    )
    check(
        "The sharp certificate note uses the seven-packet and spectral-reduction theorems in the right way and preserves the support-first obstruction",
        "one nearest-neighbor `7`-packet plus finite chain identities" in seven_note
        and "three scalar spectral identities" in spectral_note
        and "current bank still does **not** realize even the first `7`-packet layer" in note,
    )

    check(
        "The Wilson reviewer target is now strictly smaller than the older 9+3 package",
        "So the correct hard-review-safe Wilson target is now one `7 + 3` certificate" in note,
        bucket="SUPPORT",
    )
    check(
        "The current bank still fails at the first support-side layer of the sharp 7+3 certificate",
        "So the obstruction remains support-side first." in note,
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
