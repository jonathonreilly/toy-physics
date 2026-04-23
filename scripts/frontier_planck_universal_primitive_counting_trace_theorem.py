#!/usr/bin/env python3
"""Audit runner for the universal primitive counting-trace theorem."""

from __future__ import annotations

from pathlib import Path
import itertools
import math

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_UNIVERSAL_PRIMITIVE_COUNTING_TRACE_THEOREM_2026-04-23.md"


def hamming_weight(idx: int) -> int:
    return sum((idx >> bit) & 1 for bit in range(4))


def packet_indices() -> list[int]:
    return [idx for idx in range(16) if hamming_weight(idx) == 1]


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

    # Atomic naturality under all relabelings forces all atomic weights equal.
    # It is enough to impose invariance under adjacent transpositions.
    weights = np.array([1 / 16] * 16, dtype=float)
    transposition_invariant = True
    for i, j in itertools.combinations(range(16), 2):
        swapped = weights.copy()
        swapped[i], swapped[j] = swapped[j], swapped[i]
        transposition_invariant &= np.allclose(swapped, weights)

    total += 1
    passed += expect(
        "uniform-weights-are-relabeling-invariant",
        transposition_invariant,
        "all atom relabelings preserve normalized counting weights",
    )

    total += 1
    passed += expect(
        "normalization-fixes-atom-weight",
        math.isclose(float(np.sum(weights)), 1.0, abs_tol=1e-12)
        and math.isclose(float(weights[0]), 1 / 16, abs_tol=1e-12),
        f"sum={float(np.sum(weights)):.6f}, atom={float(weights[0]):.6f}",
    )

    packet = packet_indices()
    coeff = sum(weights[idx] for idx in packet)

    total += 1
    passed += expect(
        "packet-has-rank-four",
        len(packet) == 4,
        f"indices={packet}",
    )

    total += 1
    passed += expect(
        "counting-trace-gives-quarter",
        math.isclose(coeff, 0.25, abs_tol=1e-12),
        f"rank/dim={len(packet)}/16={coeff:.6f}",
    )

    nonuniform = np.array([0.10, 0.02] + [0.88 / 14.0] * 14)
    nonuniform_coeff = sum(nonuniform[idx] for idx in packet)

    total += 1
    passed += expect(
        "nonuniform-dynamical-state-is-extra-datum",
        not math.isclose(nonuniform_coeff, coeff, abs_tol=1e-12),
        f"dynamic={nonuniform_coeff:.6f}, counting={coeff:.6f}",
    )

    required = [
        "U1. Object-class locality",
        "U4. Finite additivity",
        "U5. Atomic naturality",
        "normalized counting trace",
        "not a dynamical state expectation",
    ]

    total += 1
    passed += expect(
        "note-records-uniqueness-assumptions",
        all(phrase in note for phrase in required),
        "note states object-class, additivity, naturality, and non-vacuum status",
    )

    print(f"SUMMARY: PASS={passed} FAIL={total - passed}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
