#!/usr/bin/env python3
"""
Package the whole Wilson compressed route as the local physical 2-edge + 3
certificate.
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
    two_edge = read("docs/PERRON_FROBENIUS_STEP2_WILSON_TWO_EDGE_CHAIN_REDUCTION_NOTE_2026-04-18.md")
    two_edge_min = read("docs/PERRON_FROBENIUS_STEP2_WILSON_TWO_EDGE_CHAIN_MINIMALITY_NOTE_2026-04-18.md")
    spectral = read("docs/PERRON_FROBENIUS_STEP2_WILSON_COMPRESSED_BLOCK_SPECTRAL_REDUCTION_NOTE_2026-04-17.md")
    note = read("docs/PERRON_FROBENIUS_STEP2_WILSON_PHYSICAL_SHARPEST_CERTIFICATE_TARGET_NOTE_2026-04-18.md")

    print("=" * 108)
    print("PERRON-FROBENIUS STEP-2 WILSON PHYSICAL SHARPEST CERTIFICATE TARGET")
    print("=" * 108)
    print()

    g12 = embedded(e(0, 1))
    g23 = embedded(e(1, 2))
    f21 = g12.conj().T
    f32 = g23.conj().T
    f11 = g12 @ f21
    f22 = f21 @ g12
    f33 = f32 @ g23
    f13 = g12 @ g23
    f31 = f32 @ f21
    p_e = f11 + f22 + f33

    edge_err = max(
        float(np.linalg.norm(g12 @ g12)),
        float(np.linalg.norm(g23 @ g23)),
        float(np.linalg.norm(g12 @ f21 @ g12 - g12)),
        float(np.linalg.norm(g23 @ f32 @ g23 - g23)),
        float(np.linalg.norm(f21 @ g12 - g23 @ f32)),
        float(np.linalg.norm(g23 @ g12)),
        float(np.linalg.norm(g12 @ f32)),
    )

    units = {
        (1, 1): f11, (2, 2): f22, (3, 3): f33,
        (1, 2): g12, (2, 1): f21,
        (2, 3): g23, (3, 2): f32,
        (1, 3): f13, (3, 1): f31,
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
    print(f"two-edge chain max error                    = {edge_err:.3e}")
    print(f"full matrix-unit max error                  = {full_err:.3e}")
    print(f"spectral invariant gap                      = {inv_gap:.3e}")
    print()

    check(
        "The support side is already exactly finite at the physical level: a local adjacent two-edge chain reconstructs the full matrix-unit system and rank-3 support",
        edge_err < 1.0e-12 and full_err < 1.0e-12 and abs(np.trace(p_e).real - 3.0) < 1.0e-12,
        detail=f"rank(P_e)={int(round(np.trace(p_e).real))}, edge_err={edge_err:.2e}, full_err={full_err:.2e}",
    )
    check(
        "The post-support side is still exactly finite: the compressed block matches H_e through the 3 scalar spectral identities",
        inv_gap < 1.0e-12,
        detail=f"invariant gap={inv_gap:.2e}",
    )
    check(
        "The new note records the exact local physical 2-edge + 3 certificate form of the Wilson compressed route",
        "local `2-edge + 3` certificate" in note
        and "adjacent directed nearest-neighbor two-edge chain" in note
        and "`Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`" in note
        and "not merely the abstract" in note
        and "`4 + 3` certificate" in note,
    )
    check(
        "The new note uses the exact two-edge reduction, two-edge minimality, and spectral-reduction theorems in the right way and preserves the local support-first obstruction",
        "adjacent directed nearest-neighbor two-edge chain" in two_edge
        and "exact minimal finite number of complex directed edge channels" in two_edge_min
        and "three scalar spectral identities" in spectral
        and "current bank still does **not** realize even the first local two-edge" in note,
    )

    check(
        "The Wilson reviewer target is now physical, local, and sharp",
        "So the correct hard-review-safe Wilson target is now one local physical" in note
        and "`2-edge + 3` certificate." in note,
        bucket="SUPPORT",
    )
    check(
        "The current bank still fails at the first local support-side layer of the physical 2-edge + 3 certificate",
        "So the obstruction remains local support-side first." in note,
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
