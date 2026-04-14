#!/usr/bin/env python3
"""Exact blocker for the Route 2 tensor support primitive attempt.

Starting from the exact support-side scalar delta_A1 and the bounded Route-2
comparison objects Theta_R^(0) and Xi_R^(0), verify the sharp exact obstruction:
the current exact support-side machinery is scalar/rank-one on A1 and cannot
produce a nonzero exact tensor observable on A1 x {E_x, T1x}.

The bounded Jacobian Xi_R^(0) is printed only as comparison surface.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib.machinery import SourceFileLoader

import numpy as np


ROOT = "/private/tmp/physics-review-active"
EPS = 1e-6
R_TEST = [0.25, 0.5, 0.75, 1.0, 1.5, 2.0]


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    status: str


CHECKS: list[Check] = []


def record(name: str, ok: bool, detail: str, status: str = "EXACT") -> None:
    CHECKS.append(Check(name=name, ok=ok, detail=detail, status=status))
    tag = "PASS" if ok else "FAIL"
    print(f"[{status}] {tag}: {name}")
    if detail:
        print(f"    {detail}")


def exact_support_green_block() -> np.ndarray:
    h0, interior = same.build_neg_laplacian_sparse(15)
    center = interior // 2
    support = [
        same.flat_idx(center + v[0], center + v[1], center + v[2], interior)
        for v in same.SUPPORT_COORDS
    ]
    g0p = same.solve_columns(h0, support)
    return g0p[support, :]


same = SourceFileLoader(
    "same_source_metric",
    f"{ROOT}/scripts/frontier_same_source_metric_ansatz_scan.py",
).load_module()
support_amp = SourceFileLoader(
    "support_renorm_active_amp",
    f"{ROOT}/scripts/frontier_support_renormalized_active_amplitude.py",
).load_module()
center = SourceFileLoader(
    "tensor_support_center_excess",
    f"{ROOT}/scripts/frontier_tensor_support_center_excess_law.py",
).load_module()


def main() -> int:
    print("Route 2 exact tensor support primitive attempt")
    print("=" * 78)

    gs = exact_support_green_block()
    basis = same.build_adapted_basis()
    e0 = basis[:, 0]
    s = basis[:, 1]
    s_unit = s / np.sqrt(6.0)
    e1 = basis[:, 2]
    e2 = basis[:, 3]
    t1x = basis[:, 4]
    e_x = (np.sqrt(3.0) * e1 + e2) / 2.0
    bright = np.column_stack([e_x, t1x])
    a1 = basis[:, :2]

    mixed = a1.T @ gs @ bright
    mixed_norm = float(np.max(np.abs(mixed)))

    print("Exact support Green mixed block:")
    print(np.array2string(mixed, precision=12, floatmode="fixed"))
    print(f"max |mixed block| = {mixed_norm:.3e}")

    active_op, pair_op = support_amp.support_to_active_operator()
    active_rank = int(np.linalg.matrix_rank(active_op, tol=1e-12))
    pair_rank = int(np.linalg.matrix_rank(pair_op, tol=1e-12))
    bright_images = np.column_stack([active_op @ e_x, active_op @ t1x])
    bright_image_norm = float(np.max(np.abs(bright_images)))

    print("\nExact support-to-active operator:")
    print(np.array2string(active_op, precision=6, floatmode="fixed"))
    print(f"active rank = {active_rank}")
    print(f"pair rank = {pair_rank}")
    print(f"max bright-channel image norm = {bright_image_norm:.3e}")

    delta_e0 = center.support_delta(e0)
    delta_s = center.support_delta(s_unit)
    print("\nExact support scalar:")
    print(f"  delta_A1(e0) = {delta_e0:.12e}")
    print(f"  delta_A1(s/sqrt(6)) = {delta_s:.12e}")

    bright_dir_max = 0.0
    for label, q in [
        ("e0", e0),
        ("s/sqrt(6)", s_unit),
        ("r=1", (e0 + s) / (1.0 + np.sqrt(6.0))),
        ("r=1.5", (e0 + 1.5 * s) / (1.0 + 1.5 * np.sqrt(6.0))),
    ]:
        for chan_name, v in [("E_x", e_x), ("T1x", t1x)]:
            d = (
                center.support_delta(q + EPS * v)
                - center.support_delta(q - EPS * v)
            ) / (2.0 * EPS)
            bright_dir_max = max(bright_dir_max, abs(float(d)))
            print(f"{label:>8} along {chan_name}: d delta_A1 = {float(d):+.3e}")

    theta_e0 = np.array(center.gamma_pair(e0, e_x, t1x), dtype=float)
    theta_s = np.array(center.gamma_pair(s_unit, e_x, t1x), dtype=float)
    xi = (theta_e0 - theta_s) / (delta_e0 - delta_s)
    theta_shell = theta_s.copy()

    print("\nBounded comparison surface:")
    print(f"  Theta_R^(0)(e0)        = ({theta_e0[0]:+.12e}, {theta_e0[1]:+.12e})")
    print(f"  Theta_R^(0)(s/sqrt(6)) = ({theta_s[0]:+.12e}, {theta_s[1]:+.12e})")
    print(f"  Xi_R^(0) = d Theta_R^(0) / d delta_A1 = ({xi[0]:+.12e}, {xi[1]:+.12e})")

    max_canon_err_e = 0.0
    max_canon_err_t = 0.0
    for r in R_TEST:
        q = (e0 + r * s) / (1.0 + np.sqrt(6.0) * r)
        delta = center.support_delta(q)
        theta = np.array(center.gamma_pair(q, e_x, t1x), dtype=float)
        pred = theta_shell + xi * delta
        max_canon_err_e = max(max_canon_err_e, abs(pred[0] - theta[0]))
        max_canon_err_t = max(max_canon_err_t, abs(pred[1] - theta[1]))

    record(
        "the exact support Green Hessian has no mixed A1-bright block",
        mixed_norm < 1e-12,
        f"max |P_A1^T G_S P_bright| = {mixed_norm:.3e}",
    )
    record(
        "the exact support-to-active operator is rank one and charge-only",
        active_rank == 1 and pair_rank == 1,
        f"active rank={active_rank}, pair rank={pair_rank}",
    )
    record(
        "the exact support-to-active operator annihilates the bright E_x and T1x channels",
        bright_image_norm < 1e-12,
        f"max bright-channel image norm = {bright_image_norm:.3e}",
    )
    record(
        "the exact support scalar delta_A1 is blind to bright-channel perturbations on the projective A1 family",
        bright_dir_max < 1e-10,
        f"max bright directional derivative = {bright_dir_max:.3e}",
    )
    record(
        "the bounded response Jacobian Xi_R^(0) remains a useful comparison surface",
        np.all(np.isfinite(xi)) and np.linalg.norm(xi) > 0.0,
        f"Xi_R^(0)=({xi[0]:+.3e}, {xi[1]:+.3e})",
        status="BOUNDED",
    )
    record(
        "the bounded prototype reconstructs the canonical A1 family from delta_A1 at the observed accuracy",
        max_canon_err_e < 1e-8 and max_canon_err_t < 2e-8,
        f"max canonical residuals: gamma_E={max_canon_err_e:.3e}, gamma_T={max_canon_err_t:.3e}",
        status="BOUNDED",
    )

    print("\nVerdict:")
    print(
        "The current exact support-side machinery is scalar/rank-one on A1. "
        "Its exact Hessian has no mixed A1-bright block, its support-to-active "
        "response is charge-only, and the surviving exact support scalar "
        "delta_A1 is blind to E_x and T1x. Therefore the retained stack cannot "
        "produce a nonzero exact tensor observable on A1 x {E_x, T1x}. The "
        "bounded response Jacobian Xi_R^(0) is the best comparison surface, but "
        "it is not an exact tensor primitive."
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
