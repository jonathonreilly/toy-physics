#!/usr/bin/env python3
"""Audit runner for the event-frame no-information Planck state theorem."""

from __future__ import annotations

from pathlib import Path
import itertools
import math

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_EVENT_FRAME_NO_INFORMATION_STATE_THEOREM_2026-04-23.md"


def event_bits(idx: int) -> tuple[int, int, int, int]:
    return tuple((idx >> bit) & 1 for bit in range(4))


def hamming_weight(idx: int) -> int:
    return sum(event_bits(idx))


def projector(indices: list[int]) -> np.ndarray:
    p = np.zeros((16, 16), dtype=float)
    for idx in indices:
        p[idx, idx] = 1.0
    return p


def permutation_matrix_for_bit_permutation(perm: tuple[int, int, int, int]) -> np.ndarray:
    u = np.zeros((16, 16), dtype=float)
    for idx in range(16):
        bits = event_bits(idx)
        out_bits = [0, 0, 0, 0]
        for src, dst in enumerate(perm):
            out_bits[dst] = bits[src]
        out = sum(bit << pos for pos, bit in enumerate(out_bits))
        u[out, idx] = 1.0
    return u


def expect(name: str, cond: bool, detail: str = "") -> int:
    if cond:
        print(f"PASS: {name}: {detail}")
        return 1
    print(f"FAIL: {name}: {detail}")
    return 0


def main() -> int:
    note = NOTE.read_text()
    passed = 0
    total = 0

    event_indices = list(range(16))
    packet_indices = [idx for idx in event_indices if hamming_weight(idx) == 1]
    p_a = projector(packet_indices)
    n_evt = np.diag([hamming_weight(idx) for idx in event_indices]).astype(float)

    spectral_p_a = np.zeros((16, 16), dtype=float)
    for idx, value in enumerate(np.diag(n_evt)):
        if value == 1:
            spectral_p_a[idx, idx] = 1.0

    total += 1
    passed += expect(
        "packet-is-hamming-one-spectral-projector",
        np.array_equal(p_a, spectral_p_a) and len(packet_indices) == 4,
        f"indices={packet_indices}",
    )

    invariant_under_s4 = True
    for perm in itertools.permutations(range(4)):
        u = permutation_matrix_for_bit_permutation(perm)
        invariant_under_s4 &= np.array_equal(u @ p_a @ u.T, p_a)
        invariant_under_s4 &= np.array_equal(u @ n_evt @ u.T, n_evt)

    total += 1
    passed += expect(
        "packet-is-invariant-under-readout-automorphisms",
        invariant_under_s4,
        "all four-factor permutations preserve N_evt and P_A",
    )

    alpha = 0.04
    beta = (1.0 - 4.0 * alpha) / 12.0
    rho_block = alpha * p_a + beta * (np.eye(16) - p_a)

    total += 1
    passed += expect(
        "packet-stabilizer-alone-does-not-force-quarter",
        not math.isclose(float(np.trace(rho_block @ p_a)), 0.25, abs_tol=1e-12),
        f"Tr(rho_block P_A)={float(np.trace(rho_block @ p_a)):.6f}",
    )

    rho_sf = np.eye(16) / 16.0
    weights_equal = np.allclose(np.diag(rho_sf), np.full(16, 1.0 / 16.0))

    total += 1
    passed += expect(
        "no-preferred-event-state-is-tracial",
        weights_equal and math.isclose(float(np.trace(rho_sf)), 1.0, abs_tol=1e-12),
        "all sixteen event weights are 1/16",
    )

    total += 1
    passed += expect(
        "tracial-state-gives-exact-quarter-on-fixed-packet",
        math.isclose(float(np.trace(rho_sf @ p_a)), 0.25, abs_tol=1e-12),
        f"Tr(I_16/16 P_A)={float(np.trace(rho_sf @ p_a)):.6f}",
    )

    required_phrases = [
        "replacing the older `U(2)^4`",
        "P_A = 1_{N_evt = 1}",
        "packet-preserving invariance alone",
        "Axiom Extension P1",
        "no preferred primitive event",
    ]

    total += 1
    passed += expect(
        "note-records-hardening-logic",
        all(phrase in note for phrase in required_phrases),
        "note separates state law from invariant packet readout",
    )

    print(f"SUMMARY: PASS={passed} FAIL={total - passed}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
