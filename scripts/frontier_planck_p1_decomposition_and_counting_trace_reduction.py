#!/usr/bin/env python3
"""Audit runner for P1 decomposition and counting-trace reduction."""

from __future__ import annotations

from pathlib import Path
import math

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_P1_DECOMPOSITION_AND_COUNTING_TRACE_REDUCTION_2026-04-23.md"


def hamming_weight(idx: int) -> int:
    return sum((idx >> bit) & 1 for bit in range(4))


def packet_projector() -> np.ndarray:
    p = np.zeros((16, 16), dtype=float)
    for idx in range(16):
        if hamming_weight(idx) == 1:
            p[idx, idx] = 1.0
    return p


def entropy(weights: np.ndarray) -> float:
    positive = weights[weights > 0]
    return float(-np.sum(positive * np.log(positive)))


def expect(name: str, cond: bool, detail: str = "") -> int:
    if cond:
        print(f"PASS: {name}: {detail}")
        return 1
    print(f"FAIL: {name}: {detail}")
    return 0


def main() -> int:
    note = NOTE.read_text()
    p_a = packet_projector()
    rho_count = np.eye(16) / 16.0
    uniform_weights = np.full(16, 1.0 / 16.0)
    nonuniform_weights = np.array([0.10, 0.02] + [0.88 / 14.0] * 14)

    checks = [
        (
            "note-identifies-only-load-bearing-p1-clause",
            "P1.4" in note and "real load-bearing state law" in note,
            "P1 should reduce to no-preferred primitive event",
        ),
        (
            "note-recasts-rho-as-counting-trace-not-vacuum",
            "normalized counting trace" in note
            and "not as a claim about every local reduced physical vacuum" in note,
            "I_16/16 should be object-class clarified",
        ),
        (
            "packet-rank-is-four",
            int(np.trace(p_a)) == 4,
            f"rank(P_A)={int(np.trace(p_a))}",
        ),
        (
            "counting-trace-gives-quarter",
            math.isclose(float(np.trace(rho_count @ p_a)), 0.25, abs_tol=1e-12),
            f"tau(P_A)={float(np.trace(rho_count @ p_a)):.6f}",
        ),
        (
            "uniform-counting-has-maximal-event-entropy",
            math.isclose(entropy(uniform_weights), math.log(16.0), abs_tol=1e-12)
            and entropy(nonuniform_weights) < math.log(16.0),
            f"H_uniform={entropy(uniform_weights):.6f}, H_nonuniform={entropy(nonuniform_weights):.6f}",
        ),
        (
            "nonuniform-weighting-is-extra-local-datum",
            "15-parameter local datum" in note and "hidden state data" in note,
            "nonuniform p_eta requires source/preparation/boundary/dynamics",
        ),
        (
            "note-preserves-reviewer-fork",
            "counting-trace reading accepted" in note
            and "state-expectation reading imposed" in note,
            "note should not overclaim if reviewer rejects counting object class",
        ),
    ]

    passed = 0
    for name, cond, detail in checks:
        passed += expect(name, cond, detail)

    print(f"SUMMARY: PASS={passed} FAIL={len(checks) - passed}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
