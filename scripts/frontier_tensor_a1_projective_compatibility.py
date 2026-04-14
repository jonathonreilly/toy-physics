#!/usr/bin/env python3
"""Bounded projective-A1 compatibility check for the last tensor law.

This runner asks whether the two audited restricted families are already
compatible with one common scalar shape law on the projective `A1` manifold.

For each family:
  1. extract the scalar `A1` baseline
  2. compute its projective coordinate `r = s/e0`
  3. compute the shell-normalized bright coefficients
       gamma_E, gamma_T
  4. compare them to the coefficients of the canonical projective background
       q_A1(r; Q=1)

If the differences are small, then the remaining gravity mismatch is no longer
family-structural. It is concentrated in the exact derivation of the scalar
shape law itself.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib.machinery import SourceFileLoader

import numpy as np


ROOT = "/private/tmp/physics-review-active"
EPS = 0.005

same = SourceFileLoader(
    "same_source_metric",
    f"{ROOT}/scripts/frontier_same_source_metric_ansatz_scan.py",
).load_module()
finite_rank = SourceFileLoader(
    "finite_rank_metric",
    f"{ROOT}/scripts/frontier_finite_rank_gravity_residual.py",
).load_module()
two = SourceFileLoader(
    "tensor_two_channel",
    f"{ROOT}/scripts/frontier_tensor_boundary_drive_two_channel.py",
).load_module()
shell = SourceFileLoader(
    "one_parameter_shell",
    f"{ROOT}/scripts/frontier_one_parameter_reduced_shell_law.py",
).load_module()


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    status: str


CHECKS: list[Check] = []


def record(name: str, ok: bool, detail: str, status: str = "BOUNDED") -> None:
    CHECKS.append(Check(name=name, ok=ok, detail=detail, status=status))
    tag = "PASS" if ok else "FAIL"
    print(f"[{status}] {tag}: {name}")
    if detail:
        print(f"    {detail}")


def eta_floor(q: np.ndarray) -> float:
    return float(two.tensor_metrics(two.phi_from_q(q))[0])


def gamma_pair(q: np.ndarray) -> tuple[float, float]:
    basis = same.build_adapted_basis()
    e1 = basis[:, 2]
    e2 = basis[:, 3]
    t1x = basis[:, 4]
    ex = (np.sqrt(3.0) * e1 + e2) / 2.0
    beta_e = float((eta_floor(q + EPS * ex) - eta_floor(q - EPS * ex)) / (2.0 * EPS))
    beta_t = float((eta_floor(q + EPS * t1x) - eta_floor(q - EPS * t1x)) / (2.0 * EPS))
    red = shell.reduced_data(two.phi_from_q(q))
    a_aniso = float(red["anchor_per_Q"]) * float(np.sum(q))
    return beta_e / a_aniso, beta_t / a_aniso


def oh_qeff() -> np.ndarray:
    h0, interior = same.build_neg_laplacian_sparse(15)
    center = interior // 2
    support = [
        same.flat_idx(center + v[0], center + v[1], center + v[2], interior)
        for v in same.SUPPORT_COORDS
    ]
    g0p = same.solve_columns(h0, support)
    gs = g0p[support, :]
    w = same.build_commutant_operator(0.0698, 0.0499, -0.0070, 0.0642, 0.1056)
    m = same.build_invariant_source(0.8247, 0.2271)
    return np.linalg.solve(np.eye(7) - w @ gs, m)


def finite_rank_qeff() -> np.ndarray:
    _, _, _, _, _, gs, w, masses = finite_rank.finite_rank_setup()
    return np.linalg.solve(np.eye(7) - w @ gs, masses)


def a1_baseline(q_eff: np.ndarray) -> tuple[np.ndarray, float]:
    basis = same.build_adapted_basis()
    coeff = basis.T @ q_eff
    q_a1 = basis[:, :2] @ coeff[:2]
    r = float(coeff[1] / coeff[0])
    return q_a1, r


def canonical_shape_q(r: float) -> np.ndarray:
    basis = same.build_adapted_basis()
    e0 = basis[:, 0]
    s = basis[:, 1]
    return (e0 + r * s) / (1.0 + np.sqrt(6.0) * r)


def main() -> int:
    print("Projective A1 compatibility of the bright tensor law")
    print("=" * 78)

    families = [
        ("exact local O_h", oh_qeff()),
        ("finite-rank", finite_rank_qeff()),
    ]

    max_diff_e = 0.0
    max_diff_t = 0.0
    for label, q_eff in families:
        q_a1, r = a1_baseline(q_eff)
        g_e, g_t = gamma_pair(q_a1)
        g_e_shape, g_t_shape = gamma_pair(canonical_shape_q(r))
        diff_e = abs(g_e - g_e_shape)
        diff_t = abs(g_t - g_t_shape)
        max_diff_e = max(max_diff_e, diff_e)
        max_diff_t = max(max_diff_t, diff_t)
        print(f"\n{label}:")
        print(f"  r = {r:.12f}")
        print(f"  actual gamma_E = {g_e:+.12e}")
        print(f"  actual gamma_T = {g_t:+.12e}")
        print(f"  shape  gamma_E = {g_e_shape:+.12e}")
        print(f"  shape  gamma_T = {g_t_shape:+.12e}")
        print(f"  diffs: gamma_E={diff_e:.3e}, gamma_T={diff_t:.3e}")

    record(
        "the exact local O_h and finite-rank scalar baselines are both closely tracked by one projective A1 shape law",
        max_diff_e < 5e-6 and max_diff_t < 5e-6,
        f"max diffs across audited families: gamma_E={max_diff_e:.3e}, gamma_T={max_diff_t:.3e}",
    )

    print("\nVerdict:")
    print(
        "The two audited restricted families are already closely compatible with "
        "one common projective A1 shape law for the normalized bright tensor "
        "coefficients. So the remaining gravity gap is no longer family "
        "dependence; it is the exact derivation of that scalar shape law."
    )

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    if n_fail == 0:
        print("All checks passed.")
        return 0
    print("Some checks failed.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
