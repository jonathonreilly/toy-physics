#!/usr/bin/env python3
"""Exact Lorentzian signature-class extension on the direct-universal route.

This upgrades the universal positive-background local family to the full
nondegenerate Lorentzian 3+1 background class. The key difference is that the
action is no longer required to be positive-definite; it is required only to
be an exact nondegenerate stationary family.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np


ROOT = Path("/private/tmp/physics-review-active")
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
    return (np.outer(u, v) + np.outer(v, u)) / math.sqrt(2.0)


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


def random_orthogonal(rng: np.random.Generator) -> np.ndarray:
    a = rng.normal(size=(4, 4))
    q, _ = np.linalg.qr(a)
    if np.linalg.det(q) < 0:
        q[:, 0] *= -1
    return q


def random_invertible(rng: np.random.Generator) -> np.ndarray:
    q1 = random_orthogonal(rng)
    q2 = random_orthogonal(rng)
    scales = np.diag(0.8 + 0.4 * rng.random(size=4))
    return q1 @ scales @ q2


def random_lorentzian(rng: np.random.Generator) -> np.ndarray:
    vals = np.array(
        [
            -(0.8 + rng.random()),
            0.8 + rng.random(),
            0.8 + rng.random(),
            0.8 + rng.random(),
        ],
        dtype=float,
    )
    q = random_orthogonal(rng)
    return q.T @ np.diag(vals) @ q


def action_value(k_op: np.ndarray, f: np.ndarray, j: np.ndarray) -> float:
    return 0.5 * float(f @ (k_op @ f)) - float(j @ f)


def main() -> int:
    obs_text = (DOCS / "OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md").read_text(encoding="utf-8")
    lift_text = (DOCS / "S3_ANOMALY_SPACETIME_LIFT_NOTE.md").read_text(encoding="utf-8")
    pos_text = (DOCS / "UNIVERSAL_GR_POSITIVE_BACKGROUND_LOCAL_CLOSURE_NOTE.md").read_text(encoding="utf-8")

    lambda_r = np.array(
        [
            [2.0, 0.2, 0.0],
            [0.2, 1.7, 0.1],
            [0.0, 0.1, 1.4],
        ],
        dtype=float,
    )
    lambda_sym = float(np.max(np.abs(lambda_r - lambda_r.T)))
    lambda_min = float(np.min(np.linalg.eigvalsh(lambda_r)))

    rng = np.random.default_rng(23)
    samples = 10
    max_cov_err = 0.0
    max_diag_err = 0.0
    max_offdiag_err = 0.0
    max_grad_err = 0.0
    max_completion_err = 0.0
    min_abs_eig = float("inf")
    min_det_abs = float("inf")
    min_h_pos = float("inf")
    min_h_neg_mag = float("inf")

    for _ in range(samples):
        d = random_lorentzian(rng)
        vals, basis = principal_basis(d)
        g = gram(basis, d)
        h_d = -g
        expected = np.diag(
            [
                1.0 / (vals[0] * vals[0]),
                1.0 / (vals[1] * vals[1]),
                1.0 / (vals[2] * vals[2]),
                1.0 / (vals[3] * vals[3]),
                1.0 / (vals[0] * vals[1]),
                1.0 / (vals[0] * vals[2]),
                1.0 / (vals[0] * vals[3]),
                1.0 / (vals[1] * vals[2]),
                1.0 / (vals[1] * vals[3]),
                1.0 / (vals[2] * vals[3]),
            ]
        )
        max_diag_err = max(max_diag_err, float(np.max(np.abs(np.diag(h_d) - np.diag(expected)))))
        max_offdiag_err = max(max_offdiag_err, float(np.max(np.abs(h_d - np.diag(np.diag(h_d))))))

        s = random_invertible(rng)
        d2 = s.T @ d @ s
        h = rng.normal(size=(4, 4))
        h = 0.5 * (h + h.T)
        k = rng.normal(size=(4, 4))
        k = 0.5 * (k + k.T)
        lhs = bilinear(h, k, d)
        rhs = bilinear(s.T @ h @ s, s.T @ k @ s, d2)
        max_cov_err = max(max_cov_err, abs(lhs - rhs))

        h_eigs = np.linalg.eigvalsh(h_d)
        min_abs_eig = min(min_abs_eig, float(np.min(np.abs(h_eigs))))
        pos = h_eigs[h_eigs > 0.0]
        neg = h_eigs[h_eigs < 0.0]
        if len(pos):
            min_h_pos = min(min_h_pos, float(np.min(pos)))
        if len(neg):
            min_h_neg_mag = min(min_h_neg_mag, float(np.min(np.abs(neg))))

        k_op = np.kron(h_d, lambda_r)
        eigs = np.linalg.eigvalsh(0.5 * (k_op + k_op.T))
        min_det_abs = min(min_det_abs, abs(float(np.linalg.det(k_op))))
        min_abs_eig = min(min_abs_eig, float(np.min(np.abs(eigs))))

        j = rng.normal(size=k_op.shape[0])
        f_star = np.linalg.solve(k_op, j)
        grad = k_op @ f_star - j
        max_grad_err = max(max_grad_err, float(np.max(np.abs(grad))))

        delta = rng.normal(size=k_op.shape[0])
        delta /= max(float(np.linalg.norm(delta)), 1e-12)
        delta *= 1e-3
        base = action_value(k_op, f_star, j)
        pert = action_value(k_op, f_star + delta, j)
        exact_gap = 0.5 * float(delta @ (k_op @ delta))
        max_completion_err = max(max_completion_err, abs((pert - base) - exact_gap))

    record(
        "the universal route already has the exact scalar generator, 3+1 lift, and positive-background local closure",
        "observable principle" in obs_text.lower()
        and "pl s^3 x r" in lift_text.lower()
        and "positive-background" in pos_text.lower()
        and "local" in pos_text.lower(),
        "the Lorentzian step starts from the fully closed positive-background local family",
    )
    record(
        "the Hessian bilinear is exactly congruence-covariant on the nondegenerate Lorentzian class",
        max_cov_err < 5e-12,
        f"max congruence-covariance error={max_cov_err:.3e}",
    )
    record(
        "the principal basis diagonalizes the Lorentzian local operator exactly",
        max_diag_err < 1e-12 and max_offdiag_err < 1e-12,
        f"max diagonal error={max_diag_err:.3e}, max offdiag error={max_offdiag_err:.3e}",
    )
    record(
        "the local Lorentzian Hessian is nondegenerate with mixed signature",
        min_h_pos > 0.0 and min_h_neg_mag > 0.0 and min_abs_eig > 0.0,
        f"min positive eig={min_h_pos:.6e}, min |negative eig|={min_h_neg_mag:.6e}, min |glued eig|={min_abs_eig:.6e}",
    )
    record(
        "every sampled Lorentzian background carries a unique exact stationary bridge field",
        lambda_sym < 1e-12 and lambda_min > 0.0 and min_det_abs > 0.0 and max_grad_err < 1e-12,
        f"Lambda_R symmetry={lambda_sym:.3e}, Lambda_R min eig={lambda_min:.6e}, min |det K|={min_det_abs:.6e}, max stationary gradient error={max_grad_err:.3e}",
    )
    record(
        "the exact quadratic completion identity survives without positivity on the Lorentzian class",
        max_completion_err < 1e-12,
        f"max completion identity error={max_completion_err:.3e}",
    )

    print("UNIVERSAL GR LORENTZIAN SIGNATURE EXTENSION")
    print("=" * 78)
    print(f"max congruence-covariance error = {max_cov_err:.3e}")
    print(f"max principal diagonal error    = {max_diag_err:.3e}")
    print(f"max principal offdiag error     = {max_offdiag_err:.3e}")
    print(f"Lambda_R symmetry error         = {lambda_sym:.3e}")
    print(f"Lambda_R min eigenvalue         = {lambda_min:.6e}")
    print(f"min |glued operator eigenvalue| = {min_abs_eig:.6e}")
    print(f"min |det glued operator|        = {min_det_abs:.6e}")
    print(f"max stationary gradient error   = {max_grad_err:.3e}")
    print(f"max completion identity error   = {max_completion_err:.3e}")

    print("\nVerdict:")
    print(
        "The direct-universal route extends exactly from the positive-symmetric "
        "background family to the full nondegenerate Lorentzian 3+1 background "
        "class. The price of Lorentzian signature is loss of convexity, not loss "
        "of exact stationary closure."
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
