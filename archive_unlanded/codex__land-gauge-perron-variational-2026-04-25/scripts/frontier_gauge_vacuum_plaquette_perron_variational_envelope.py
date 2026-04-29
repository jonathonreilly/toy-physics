#!/usr/bin/env python3
"""Audit the gauge-vacuum plaquette Perron variational envelope theorem.

This runner validates the reusable finite-dimensional identities behind the
note: Rayleigh-Perron uniqueness, Collatz-Wielandt certificates, and the
symmetrically inserted source derivative. It deliberately does not evaluate
the open beta=6 residual environment coefficients or repin the canonical
plaquette value.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
NOTE = DOCS / "GAUGE_VACUUM_PLAQUETTE_PERRON_VARIATIONAL_ENVELOPE_THEOREM_NOTE_2026-04-25.md"

TOL = 1.0e-10


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    detail: str


def add(checks: list[Check], name: str, passed: bool, detail: str = "") -> None:
    checks.append(Check(name=name, passed=bool(passed), detail=detail))


def top_eigenpair(matrix: np.ndarray) -> tuple[float, np.ndarray, np.ndarray]:
    values, vectors = np.linalg.eigh(matrix)
    idx = int(np.argmax(values))
    vec = vectors[:, idx]
    if np.sum(vec) < 0:
        vec = -vec
    return float(values[idx]), vec, values


def rayleigh(matrix: np.ndarray, vector: np.ndarray) -> float:
    v = vector / np.linalg.norm(vector)
    return float(v @ (matrix @ v))


def cw_bounds(matrix: np.ndarray, vector: np.ndarray) -> tuple[float, float, np.ndarray]:
    ratios = (matrix @ vector) / vector
    return float(np.min(ratios)), float(np.max(ratios)), ratios


def sourced_top_log_lambda(matrix: np.ndarray, source: np.ndarray, s: float) -> float:
    sourced = sourced_matrix(matrix, source, s)
    lam, _, _ = top_eigenpair(sourced)
    return float(np.log(lam))


def sourced_matrix(matrix: np.ndarray, source: np.ndarray, s: float) -> np.ndarray:
    diagonal = np.diag(np.exp(0.5 * s * np.diag(source)))
    return diagonal @ matrix @ diagonal


def part_authorities(checks: list[Check]) -> None:
    authorities = [
        "GAUGE_VACUUM_PLAQUETTE_PERRON_REDUCTION_THEOREM_NOTE.md",
        "GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TENSOR_TRANSFER_THEOREM_NOTE.md",
        "GAUGE_VACUUM_PLAQUETTE_PERRON_JACOBI_UNDERDETERMINATION_NOTE.md",
        "GAUGE_VACUUM_PLAQUETTE_TRANSFER_OPERATOR_CHARACTER_RECURRENCE_NOTE.md",
    ]
    for filename in authorities:
        path = DOCS / filename
        add(checks, f"authority exists: {filename}", path.exists(), str(path))

    text = NOTE.read_text(encoding="utf-8")
    add(
        checks,
        "note states the executable runner",
        "frontier_gauge_vacuum_plaquette_perron_variational_envelope.py" in text,
        "script line is present",
    )
    add(
        checks,
        "note preserves no numeric plaquette closure boundary",
        "No numeric plaquette closure is claimed" in text
        and "does not assert a\n   value for `P(6)`" in text,
        "P(6) remains open",
    )
    add(
        checks,
        "note preserves residual environment boundary",
        "does not evaluate the still-open boundary coefficients" in text
        and "explicit evaluation of `rho_(p,q)(6)`" in text,
        "rho_(p,q)(6) remains open",
    )
    add(
        checks,
        "note preserves cutoff convergence boundary",
        "cutoff-to-full-source-sector convergence theorem" in text,
        "finite cutoff certificates are not full beta=6 convergence",
    )


def part_rayleigh_perron(checks: list[Check]) -> tuple[np.ndarray, float, np.ndarray]:
    transfer = np.array(
        [
            [2.15, 0.62, 0.33, 0.19],
            [0.62, 1.72, 0.58, 0.41],
            [0.33, 0.58, 1.94, 0.67],
            [0.19, 0.41, 0.67, 1.51],
        ],
        dtype=float,
    )

    lam0, psi0, values = top_eigenpair(transfer)
    values_desc = np.sort(values)[::-1]
    gap = values_desc[0] - values_desc[1]

    add(
        checks,
        "transfer proxy is self-adjoint",
        np.max(np.abs(transfer - transfer.T)) < TOL,
        f"max asymmetry={np.max(np.abs(transfer - transfer.T)):.3e}",
    )
    add(
        checks,
        "transfer proxy is strictly positive entrywise",
        float(np.min(transfer)) > 0.0,
        f"min entry={np.min(transfer):.6f}",
    )
    add(
        checks,
        "Perron eigenvector is strictly positive",
        float(np.min(psi0)) > 0.0,
        f"min psi={np.min(psi0):.6f}",
    )
    add(
        checks,
        "Perron eigenvalue is simple",
        gap > 1.0e-8,
        f"lambda0={lam0:.12f}, gap={gap:.6e}",
    )
    add(
        checks,
        "Rayleigh quotient at Perron vector equals lambda0",
        abs(rayleigh(transfer, psi0) - lam0) < TOL,
        f"Rayleigh(psi0)={rayleigh(transfer, psi0):.12f}",
    )

    rng = np.random.default_rng(314159)
    for idx in range(10):
        sample = rng.normal(size=transfer.shape[0])
        rq = rayleigh(transfer, sample)
        add(
            checks,
            f"random Rayleigh sample {idx} lies below lambda0",
            rq <= lam0 + 1.0e-12,
            f"rq={rq:.12f}, lambda0={lam0:.12f}",
        )

    orthogonal = np.array([psi0[1], -psi0[0], 0.0, 0.0])
    if np.linalg.norm(orthogonal) < TOL:
        orthogonal = np.array([0.0, psi0[2], -psi0[1], 0.0])
    orthogonal = orthogonal - float(orthogonal @ psi0) * psi0
    perturbed = psi0 + 0.2 * orthogonal / np.linalg.norm(orthogonal)
    add(
        checks,
        "non-Perron perturbation lowers the Rayleigh quotient",
        rayleigh(transfer, perturbed) < lam0 - 1.0e-6,
        f"perturbed rq={rayleigh(transfer, perturbed):.12f}",
    )

    return transfer, lam0, psi0


def part_collatz_wielandt(checks: list[Check], transfer: np.ndarray, lam0: float, psi0: np.ndarray) -> None:
    m0, m1, ratios = cw_bounds(transfer, psi0)
    add(
        checks,
        "Perron vector collapses Collatz-Wielandt envelope",
        abs(m0 - lam0) < 1.0e-10 and abs(m1 - lam0) < 1.0e-10,
        f"min={m0:.12f}, max={m1:.12f}, spread={np.ptp(ratios):.3e}",
    )

    trial_vectors = [
        np.array([1.0, 1.0, 1.0, 1.0]),
        np.array([2.0, 1.0, 0.7, 1.6]),
        np.array([0.4, 1.3, 2.2, 0.9]),
        np.array([3.0, 0.8, 0.6, 1.1]),
    ]
    for idx, trial in enumerate(trial_vectors):
        lower, upper, _ = cw_bounds(transfer, trial)
        add(
            checks,
            f"trial vector {idx} bounds Perron eigenvalue",
            lower <= lam0 + 1.0e-12 and lam0 <= upper + 1.0e-12,
            f"[{lower:.12f}, {upper:.12f}] contains {lam0:.12f}",
        )
        add(
            checks,
            f"trial vector {idx} has positive finite certificate",
            lower > 0.0 and np.isfinite(upper),
            f"width={upper - lower:.6e}",
        )


def part_source_derivative(checks: list[Check], transfer: np.ndarray, psi0: np.ndarray) -> None:
    source = np.diag([0.30, -0.10, 0.45, 0.05])
    expected = float(psi0 @ (source @ psi0))
    h = 1.0e-5
    finite_difference = (
        sourced_top_log_lambda(transfer, source, h)
        - sourced_top_log_lambda(transfer, source, -h)
    ) / (2.0 * h)

    add(
        checks,
        "symmetric source derivative equals Perron expectation",
        abs(finite_difference - expected) < 1.0e-9,
        f"fd={finite_difference:.12f}, <B>={expected:.12f}",
    )
    add(
        checks,
        "source insertion remains symmetric",
        np.max(np.abs(
            sourced_matrix(transfer, source, 2.0e-4)
            - sourced_matrix(transfer, source, 2.0e-4).T
        ))
        < TOL,
        "T(s)=exp(sB/2)T exp(sB/2) is self-adjoint for diagonal B",
    )


def main() -> int:
    checks: list[Check] = []

    print("=" * 78)
    print("GAUGE-VACUUM PLAQUETTE PERRON VARIATIONAL ENVELOPE AUDIT")
    print("=" * 78)
    print()
    print("Scope: finite-dimensional theorem audit; no beta=6 plaquette repinning.")
    print()

    part_authorities(checks)
    transfer, lam0, psi0 = part_rayleigh_perron(checks)
    part_collatz_wielandt(checks, transfer, lam0, psi0)
    part_source_derivative(checks, transfer, psi0)

    pass_count = 0
    fail_count = 0
    for check in checks:
        status = "PASS" if check.passed else "FAIL"
        if check.passed:
            pass_count += 1
        else:
            fail_count += 1
        print(f"[{status}] {check.name}")
        if check.detail:
            print(f"       {check.detail}")

    print()
    print(f"TOTAL: PASS={pass_count} FAIL={fail_count}")
    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
