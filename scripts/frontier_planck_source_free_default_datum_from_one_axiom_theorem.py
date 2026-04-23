#!/usr/bin/env python3
"""Audit runner for the one-axiom source-free default-datum theorem."""

from __future__ import annotations

import itertools
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


def p0_projector() -> np.ndarray:
    p = np.zeros((16, 16), dtype=complex)
    p[0, 0] = 1.0
    return p


def entropy(rho: np.ndarray) -> float:
    vals = np.linalg.eigvalsh(rho)
    vals = vals[vals > 1e-15]
    return float(-np.sum(vals * np.log(vals)))


def local_rotation(theta: float) -> np.ndarray:
    return np.array(
        [[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]],
        dtype=complex,
    )


def local_unitary() -> np.ndarray:
    return np.kron(
        np.kron(np.kron(local_rotation(0.37), local_rotation(0.21)), local_rotation(0.41)),
        local_rotation(0.19),
    )


def paulis() -> list[np.ndarray]:
    i = np.eye(2, dtype=complex)
    x = np.array([[0, 1], [1, 0]], dtype=complex)
    y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    z = np.array([[1, 0], [0, -1]], dtype=complex)
    return [i, x, y, z]


def local_pauli_twirl(rho: np.ndarray) -> np.ndarray:
    acc = np.zeros_like(rho, dtype=complex)
    ps = paulis()
    for ops in itertools.product(ps, repeat=4):
        u = ops[0]
        for op in ops[1:]:
            u = np.kron(u, op)
        acc += u @ rho @ u.conj().T
    return acc / (4 ** 4)


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
    p0 = p0_projector()
    U = local_unitary()

    checks.append(
        Check(
            "note-scopes-theorem-to-one-axiom-surface",
            "accepted one-axiom information / Hilbert / locality surface" in note,
            "note should be explicit about surface of the claim",
        )
    )
    checks.append(
        Check(
            "note-records-dynamical-vacuum-escape-hatch",
            "reduced vacuum state observable" in note,
            "hostile-review escape hatch should be explicit",
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

    rho_twirl = local_pauli_twirl(rho_hidden)
    checks.append(
        Check(
            "local-object-only-twirl-forces-tracial-state",
            np.allclose(rho_twirl, rho_default, atol=1e-12),
            "local Pauli twirl removes hidden one-cell datum and lands on I_16/16",
        )
    )

    checks.append(
        Check(
            "default-datum-presentation-independent",
            np.allclose(U @ rho_default @ U.conj().T, rho_default, atol=1e-12),
            "I_16/16 is invariant under factor-preserving presentation changes",
        )
    )

    prob_before = float(np.real(np.trace(rho_hidden @ p0)))
    prob_after = float(np.real(np.trace((U @ rho_hidden @ U.conj().T) @ p0)))
    checks.append(
        Check(
            "hidden-preparation-visible-under-frame-change",
            not math.isclose(prob_before, prob_after, rel_tol=0.0, abs_tol=1e-9),
            f"prob_before={prob_before:.6f}, prob_after={prob_after:.6f}",
        )
    )

    rho_prep = p0.copy()
    prep_after = U @ p0 @ U.conj().T
    pair_before = float(np.real(np.trace(rho_prep @ p0)))
    pair_after = float(np.real(np.trace((U @ rho_prep @ U.conj().T) @ prep_after)))
    checks.append(
        Check(
            "prepared-state-transforms-with-preparation-datum",
            math.isclose(pair_before, pair_after, rel_tol=0.0, abs_tol=1e-12),
            f"before={pair_before:.6f}, after={pair_after:.6f}",
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
