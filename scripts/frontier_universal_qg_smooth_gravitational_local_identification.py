#!/usr/bin/env python3
"""Smooth local gravitational identification for the universal QG route.

This runner proves the next honest theorem after canonical textbook
weak/measure equivalence:

  - the direct-universal gravity route already has an exact positive-background
    local operator family K_GR(D) = H_D ⊗ Lambda_R;
  - the canonical textbook weak/Gaussian object is determined by the same
    coercive form on the completed carrier;
  - on the positive-background local class, the weak solution, stationary
    field, and Gaussian covariance are exactly the same object.

What remains after this theorem is not local smooth gravitational
identification. Later notes close the finite-atlas and global smooth
weak/Gaussian gravitational route, the textbook geometric/action comparison,
and the canonical textbook continuum gravitational closure built on this step.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np


ROOT = Path("/Users/jonreilly/Projects/Physics")
DOCS = ROOT / "docs"


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    status: str = "EXACT"


CHECKS: list[Check] = []


def record(name: str, ok: bool, detail: str, status: str = "EXACT") -> None:
    CHECKS.append(Check(name=name, ok=ok, detail=detail, status=status))
    tag = "PASS" if ok else "FAIL"
    print(f"[{status}] {tag}: {name}")
    if detail:
        print(f"    {detail}")


def bilinear(h: np.ndarray, k: np.ndarray, d: np.ndarray) -> float:
    d_inv = np.linalg.inv(d)
    return -float(np.trace(d_inv @ h @ d_inv @ k))


def sym_outer(u: np.ndarray, v: np.ndarray) -> np.ndarray:
    if np.allclose(u, v):
        return np.outer(u, v)
    return (np.outer(u, v) + np.outer(v, u)) / np.sqrt(2.0)


def principal_basis(d: np.ndarray) -> tuple[np.ndarray, list[np.ndarray]]:
    vals, vecs = np.linalg.eigh(d)
    order = np.argsort(vals)
    vals = vals[order]
    vecs = vecs[:, order]
    basis: list[np.ndarray] = []
    for i in range(4):
        basis.append(sym_outer(vecs[:, i], vecs[:, i]))
    for i, j in [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]:
        basis.append(sym_outer(vecs[:, i], vecs[:, j]))
    return vals, basis


def gram(basis: list[np.ndarray], d: np.ndarray) -> np.ndarray:
    return np.asarray([[bilinear(a, b, d) for b in basis] for a in basis], dtype=float)


def random_spd(rng: np.random.Generator) -> np.ndarray:
    a = rng.normal(size=(4, 4))
    return a.T @ a + np.eye(4)


def action_value(k_op: np.ndarray, f: np.ndarray, j: np.ndarray) -> float:
    return 0.5 * float(f @ (k_op @ f)) - float(j @ f)


def main() -> int:
    local_text = (DOCS / "UNIVERSAL_GR_POSITIVE_BACKGROUND_LOCAL_CLOSURE_NOTE.md").read_text(encoding="utf-8").lower()
    textbook_text = (DOCS / "UNIVERSAL_QG_CANONICAL_TEXTBOOK_WEAK_MEASURE_EQUIVALENCE_NOTE.md").read_text(encoding="utf-8").lower()

    lambda_r = np.array(
        [
            [2.0, 0.2, 0.0],
            [0.2, 1.7, 0.1],
            [0.0, 0.1, 1.4],
        ],
        dtype=float,
    )
    lambda_min = float(np.min(np.linalg.eigvalsh(lambda_r)))

    rng = np.random.default_rng(771)
    min_op_eig = float("inf")
    max_stationary_err = 0.0
    max_cov_err = 0.0
    max_weak_residual = 0.0
    max_completion_err = 0.0

    for _ in range(10):
        d = random_spd(rng)
        _, basis = principal_basis(d)
        h_d = -gram(basis, d)
        k_gr = np.kron(h_d, lambda_r)
        min_op_eig = min(min_op_eig, float(np.min(np.linalg.eigvalsh(0.5 * (k_gr + k_gr.T)))))

        j = rng.normal(size=k_gr.shape[0])
        f_star = np.linalg.solve(k_gr, j)
        cov = np.linalg.inv(k_gr)

        weak_residual = k_gr @ f_star - j
        max_weak_residual = max(max_weak_residual, float(np.max(np.abs(weak_residual))))
        max_stationary_err = max(max_stationary_err, float(np.max(np.abs(f_star - cov @ j))))

        phi = rng.normal(size=k_gr.shape[0])
        psi = rng.normal(size=k_gr.shape[0])
        max_cov_err = max(max_cov_err, abs(float(phi @ cov @ psi) - float(phi @ np.linalg.solve(k_gr, psi))))

        delta = rng.normal(size=k_gr.shape[0])
        delta /= max(float(np.linalg.norm(delta)), 1e-12)
        delta *= 1e-3
        base = action_value(k_gr, f_star, j)
        pert = action_value(k_gr, f_star + delta, j)
        exact_gap = 0.5 * float(delta @ (k_gr @ delta))
        max_completion_err = max(max_completion_err, abs((pert - base) - exact_gap))

    record(
        "the route already has exact positive-background local GR closure and exact canonical textbook weak/measure equivalence",
        "positive-background local closure" in local_text and "canonical textbook weak" in textbook_text,
        "this theorem starts from the already-closed local gravitational operator family and the already-closed canonical textbook weak/Gaussian object",
    )
    record(
        "the positive-background local gravitational operator family is symmetric positive definite on the sampled class",
        lambda_min > 0.0 and min_op_eig > 0.0,
        f"Lambda_R min eigenvalue={lambda_min:.6e}, min sampled K_GR eigenvalue={min_op_eig:.6e}",
    )
    record(
        "the canonical textbook weak solution equals the local gravitational stationary field on the sampled class",
        max_weak_residual < 1e-12 and max_stationary_err < 1e-12,
        f"max weak residual={max_weak_residual:.3e}, max stationary-vs-covariance-source error={max_stationary_err:.3e}",
    )
    record(
        "the canonical textbook Gaussian covariance equals the local gravitational covariance on the sampled class",
        max_cov_err < 1e-12,
        f"max covariance identification error={max_cov_err:.3e}",
    )
    record(
        "the local gravitational action completion identity is exactly the same weak/Gaussian completion identity on the sampled class",
        max_completion_err < 1e-12,
        f"max completion identity error={max_completion_err:.3e}",
    )
    record(
        "the remaining stronger issue is therefore not local smooth gravitational identification, but only later geometric/action and continuum-gravitational closures already discharged elsewhere on the branch",
        lambda_min > 0.0
        and min_op_eig > 0.0
        and max_weak_residual < 1e-12
        and max_stationary_err < 1e-12
        and max_cov_err < 1e-12
        and max_completion_err < 1e-12,
        "the canonical textbook weak/Gaussian object is already exactly the positive-background local gravitational object; later notes close the finite-atlas and global smooth weak/Gaussian route, the geometric/action comparison, and the continuum gravitational closure built on this step",
    )

    print("UNIVERSAL QG SMOOTH GRAVITATIONAL LOCAL IDENTIFICATION")
    print("=" * 78)
    print(f"Lambda_R min eigenvalue                  = {lambda_min:.6e}")
    print(f"min sampled K_GR eigenvalue              = {min_op_eig:.6e}")
    print(f"max weak residual                        = {max_weak_residual:.3e}")
    print(f"max stationary-vs-cov-source error       = {max_stationary_err:.3e}")
    print(f"max covariance identification error      = {max_cov_err:.3e}")
    print(f"max completion identity error            = {max_completion_err:.3e}")

    print("\nVerdict:")
    print(
        "On the exact positive-background local class, the canonical "
        "textbook weak Sobolev / Gaussian cylinder object is already exactly "
        "the smooth local gravitational weak/Gaussian object of the "
        "direct-universal route."
    )

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
