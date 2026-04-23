#!/usr/bin/env python3
"""Audit runner for the one-axiom source-free default-datum theorem."""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np


NOTE = (
    Path(__file__).resolve().parents[1]
    / "docs/PLANCK_SCALE_SOURCE_FREE_DEFAULT_DATUM_FROM_ONE_AXIOM_THEOREM_2026-04-23.md"
)


def pa_projector() -> np.ndarray:
    p = np.zeros((16, 16), dtype=complex)
    for idx in (1, 2, 4, 8):
        p[idx, idx] = 1.0
    return p


def hamming_count_operator() -> np.ndarray:
    n = np.zeros((16, 16), dtype=complex)
    for idx in range(16):
        n[idx, idx] = sum((idx >> bit) & 1 for bit in range(4))
    return n


def entropy(rho: np.ndarray) -> float:
    vals = np.linalg.eigvalsh(rho)
    vals = vals[vals > 1e-15]
    return float(-np.sum(vals * np.log(vals)))


@dataclass
class Check:
    name: str
    ok: bool
    detail: str


def main() -> None:
    note = NOTE.read_text()
    checks: list[Check] = []

    rho_default = np.eye(16, dtype=complex) / 16.0
    rho_hidden = np.diag([0.10, 0.02] + [0.88 / 14.0] * 14).astype(complex)
    p_a = pa_projector()
    n_evt = hamming_count_operator()

    checks.append(
        Check(
            "note-promotes-explicit-axiom-extension",
            "Axiom Extension P1" in note and "explicitly promoted" in note,
            "note should be explicit about the Planck-package extension",
        )
    )
    checks.append(
        Check(
            "note-replaces-u2-presentation-argument",
            "older argument appealed to arbitrary factor-local `U(2)^4`" in note
            and "This hardened version does not" in note,
            "state law should no longer rely on arbitrary factor-local rotations",
        )
    )

    i_hidden = math.log(16.0) - entropy(rho_hidden)
    checks.append(
        Check(
            "nontrivial-hidden-state-carries-positive-local-information",
            i_hidden > 0.0,
            f"I_loc(hidden)={i_hidden:.12f}",
        )
    )

    spectral_p_a = np.zeros_like(p_a)
    for idx, val in enumerate(np.diag(n_evt)):
        if val == 1:
            spectral_p_a[idx, idx] = 1.0
    checks.append(
        Check(
            "packet-is-invariantly-defined-by-hamming-count",
            np.allclose(spectral_p_a, p_a, atol=1e-12),
            "P_A is the N_evt=1 spectral projector",
        )
    )

    checks.append(
        Check(
            "no-preferred-event-default-is-tracial",
            np.allclose(np.diag(rho_default), np.full(16, 1.0 / 16.0), atol=1e-12),
            "all primitive event weights are equal",
        )
    )

    alpha = 0.04
    beta = (1.0 - 4.0 * alpha) / 12.0
    rho_block = alpha * p_a + beta * (np.eye(16) - p_a)
    checks.append(
        Check(
            "packet-stabilizer-alone-does-not-force-quarter",
            not math.isclose(float(np.real(np.trace(rho_block @ p_a))), 0.25, abs_tol=1e-12),
            f"Tr(rho_block P_A)={float(np.real(np.trace(rho_block @ p_a))):.6f}",
        )
    )

    coeff_default = float(np.real(np.trace(rho_default @ p_a)))
    coeff_hidden = float(np.real(np.trace(rho_hidden @ p_a)))
    checks.append(
        Check(
            "tracial-default-gives-exact-quarter",
            math.isclose(coeff_default, 0.25, rel_tol=0.0, abs_tol=1e-12),
            f"coeff_default={coeff_default:.6f}",
        )
    )
    checks.append(
        Check(
            "arbitrary-hidden-state-does-not-give-universal-quarter",
            not math.isclose(coeff_hidden, 0.25, rel_tol=0.0, abs_tol=1e-12),
            f"coeff_hidden={coeff_hidden:.6f}",
        )
    )

    passed = 0
    for idx, check in enumerate(checks, start=1):
        status = "PASS" if check.ok else "FAIL"
        print(f"[{idx}] {status} {check.name}: {check.detail}")
        passed += int(check.ok)

    print(f"\n{passed}/{len(checks)} PASS")
    if passed != len(checks):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
