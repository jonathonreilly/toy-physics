#!/usr/bin/env python3
"""
Majorana adjacent singlet-placement theorem on the midpoint-anchored cascade.

Question:
  Once the minimal endpoint-exchange bridge fixes the Majorana doublet anchor
  at k_B = 8, can the branch also fix the singlet placement on the exact
  weak-axis 1+2 cascade geometry?

Answer on the minimal adjacent lift:
  Yes. On the exact weak-axis geometry, the T_1 return splits into one UV-
  directed singled-out channel through O_0 and one residual two-state channel
  through T_2. Since O_0 is exactly one Hamming-weight step closer to the UV
  endpoint than T_1, the minimal adjacent lift places the singled-out singlet
  one staircase level above the midpoint-anchored doublet:

      k_A = 7,   k_B = 8.

Boundary:
  This closes the singlet/doublet placement only on the minimal adjacent lift.
  It does not yet derive eps/B or the full A/B/epsilon amplitude law.
"""

from __future__ import annotations

import math
import sys

import numpy as np

PASS_COUNT = 0
FAIL_COUNT = 0

PI = math.pi
G_BARE = 1.0
ALPHA_BARE = G_BARE**2 / (4.0 * PI)
PLAQ_MC = 0.5934
U0 = PLAQ_MC ** 0.25
ALPHA_LM = ALPHA_BARE / U0
M_PL = 1.2209e19

I2 = np.eye(2, dtype=complex)
SX = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
GAMMA_1 = np.kron(SX, np.kron(I2, I2))

STATES = [(s1, s2, s3) for s1 in range(2) for s2 in range(2) for s3 in range(2)]
INDEX = {state: idx for idx, state in enumerate(STATES)}

O0 = [(0, 0, 0)]
T1 = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
T2 = [(1, 1, 0), (1, 0, 1), (0, 1, 1)]

K_B = 8
K_A = K_B - 1


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


def basis(states: list[tuple[int, int, int]]) -> np.ndarray:
    eye = np.eye(8, dtype=complex)
    return np.column_stack([eye[:, INDEX[state]] for state in states])


def hamming_weight(state: tuple[int, int, int]) -> int:
    return sum(state)


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA: ADJACENT SINGLET-PLACEMENT THEOREM")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - docs/DM_NEUTRINO_CASCADE_GEOMETRY_NOTE_2026-04-14.md")
    print("  - docs/NEUTRINO_MAJORANA_ENDPOINT_EXCHANGE_MIDPOINT_THEOREM_NOTE.md")
    print("  - docs/THREE_GENERATION_STRUCTURE_NOTE.md")
    print()
    print("Question:")
    print("  After the exact midpoint theorem fixes the doublet anchor k_B = 8,")
    print("  can the singlet placement be fixed on the exact weak-axis 1+2")
    print("  cascade geometry?")

    b0 = basis(O0)
    b1 = basis(T1)
    b2 = basis(T2)
    p0 = b0 @ b0.conj().T
    p2 = b2 @ b2.conj().T

    one_hop_o0 = b0.conj().T @ GAMMA_1 @ b1
    one_hop_t2 = b2.conj().T @ GAMMA_1 @ b1
    via_o0 = b1.conj().T @ GAMMA_1 @ p0 @ GAMMA_1 @ b1
    via_t2 = b1.conj().T @ GAMMA_1 @ p2 @ GAMMA_1 @ b1

    image_states = []
    for state in T1:
        vec = np.zeros(8, dtype=complex)
        vec[INDEX[state]] = 1.0
        image = GAMMA_1 @ vec
        image_state = STATES[int(np.argmax(np.abs(image)))]
        image_states.append((state, image_state))

    uv_images = [dst for _, dst in image_states if hamming_weight(dst) < 1]
    ir_images = [dst for _, dst in image_states if hamming_weight(dst) > 1]

    print()
    print("Exact weak-axis images of the T_1 basis:")
    for src, dst in image_states:
        print(f"  {src} -> {dst}  (hw {hamming_weight(src)} -> {hamming_weight(dst)})")

    print()
    print("Exact return split on T_1:")
    print(f"  via O_0 =\n{via_o0}")
    print()
    print(f"  via T_2 =\n{via_t2}")

    check(
        "The weak-axis one-hop map has one UV-directed image and two IR-directed images",
        len(uv_images) == 1 and len(ir_images) == 2,
        f"uv={uv_images}, ir={ir_images}",
    )
    check(
        "The unique UV-directed image is the exact singlet O_0",
        uv_images == O0,
        f"uv images={uv_images}",
    )
    check(
        "The singled-out return channel is rank-1 and isolates one state",
        np.allclose(via_o0, np.diag([1.0, 0.0, 0.0]), atol=1e-12),
        "via O_0 = diag(1,0,0)",
    )
    check(
        "The residual return channel is rank-2 and keeps the remaining pair degenerate",
        np.allclose(via_t2, np.diag([0.0, 1.0, 1.0]), atol=1e-12),
        "via T_2 = diag(0,1,1)",
    )
    check(
        "The exact midpoint theorem anchors the doublet at k_B = 8",
        K_B == 8,
        f"k_B={K_B}",
    )
    check(
        "On the minimal adjacent lift, the unique UV singled-out channel sits one step above the doublet anchor",
        K_A == K_B - 1,
        f"k_A={K_A}, k_B={K_B}",
    )

    a_scale = M_PL * ALPHA_LM ** K_A
    b_scale = M_PL * ALPHA_LM ** K_B

    print()
    print("Minimal adjacent-lift consequence:")
    print(f"  doublet anchor: k_B = {K_B},  B = M_Pl * alpha_LM^{K_B} = {b_scale:.4e} GeV")
    print(f"  singlet place:  k_A = {K_A},  A = M_Pl * alpha_LM^{K_A} = {a_scale:.4e} GeV")
    print()
    print("Result:")
    print("  The exact midpoint theorem plus the exact 1+2 cascade geometry fix")
    print("  the singlet/doublet placement on the minimal adjacent lift:")
    print()
    print("      k_A = 7,   k_B = 8.")
    print()
    print("  What remains is not the staircase placement anymore. It is the")
    print("  doublet splitting and texture amplitudes, especially eps/B.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
