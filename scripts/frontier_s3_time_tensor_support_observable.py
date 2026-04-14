#!/usr/bin/env python3
"""Route 2 tensor support observable blocker plus bounded prototype.

This runner asks the exact question left after the Route-2 support-side
reductions:

    can the current exact support machinery produce a nonzero exact tensor
    observable on A1 x {E_x, T1x}?

It also prints the bounded staging object

    Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))

so the next exact primitive has a concrete comparison surface.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib.machinery import SourceFileLoader

import numpy as np


ROOT = "/private/tmp/physics-review-active"

same = SourceFileLoader(
    "same_source_metric",
    f"{ROOT}/scripts/frontier_same_source_metric_ansatz_scan.py",
).load_module()
support_attack = SourceFileLoader(
    "tensor_support_attack",
    f"{ROOT}/scripts/frontier_tensor_support_tensor_observable_attack.py",
).load_module()
support_amp = SourceFileLoader(
    "support_renorm_active_amp",
    f"{ROOT}/scripts/frontier_support_renormalized_active_amplitude.py",
).load_module()
center_law = SourceFileLoader(
    "tensor_support_center_excess",
    f"{ROOT}/scripts/frontier_tensor_support_center_excess_law.py",
).load_module()


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


def exact_support_green_block() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    h0, interior = same.build_neg_laplacian_sparse(15)
    center = interior // 2
    support = [
        same.flat_idx(center + v[0], center + v[1], center + v[2], interior)
        for v in same.SUPPORT_COORDS
    ]
    g0p = same.solve_columns(h0, support)
    gs = g0p[support, :]
    basis = same.build_adapted_basis()
    e0 = basis[:, 0]
    s = basis[:, 1]
    e1 = basis[:, 2]
    e2 = basis[:, 3]
    t1x = basis[:, 4]
    ex = (np.sqrt(3.0) * e1 + e2) / 2.0
    bright = np.column_stack([ex, t1x])
    mixed = basis[:, :2].T @ gs @ bright
    return gs, mixed, np.column_stack([e0, s])


def main() -> int:
    print("Route 2 tensor support observable blocker plus bounded prototype")
    print("=" * 78)

    gs, mixed, _ = exact_support_green_block()
    mixed_norm = float(np.max(np.abs(mixed)))

    print("Exact support Green matrix mixed A1-bright block:")
    print(np.array2string(mixed, precision=12, floatmode="fixed"))
    print(f"max |mixed block| = {mixed_norm:.3e}")

    active_op, pair_op = support_amp.support_to_active_operator()
    active_rank = int(np.linalg.matrix_rank(active_op, tol=1e-12))
    pair_rank = int(np.linalg.matrix_rank(pair_op, tol=1e-12))
    active_bright_norm = float(
        max(
            np.max(np.abs(active_op @ same.build_adapted_basis()[:, 2])),
            np.max(np.abs(active_op @ same.build_adapted_basis()[:, 4])),
        )
    )

    print("\nExact support-to-active operator:")
    print(np.array2string(active_op, precision=6, floatmode="fixed"))
    print(f"active rank = {active_rank}")
    print(f"pair rank = {pair_rank}")
    print(f"max bright-channel image norm = {active_bright_norm:.3e}")

    basis = same.build_adapted_basis()
    e0 = basis[:, 0]
    s = basis[:, 1]
    s_unit = s / np.sqrt(6.0)
    e1 = basis[:, 2]
    e2 = basis[:, 3]
    t1x = basis[:, 4]
    ex = (np.sqrt(3.0) * e1 + e2) / 2.0

    delta_e0 = center_law.support_delta(e0)
    delta_s = center_law.support_delta(s_unit)
    print("\nExact support scalar:")
    print(f"  delta_A1(e0) = {delta_e0:.12e}")
    print(f"  delta_A1(s/sqrt(6)) = {delta_s:.12e}")

    q_center = e0
    q_shell = s_unit
    theta_center = center_law.gamma_pair(q_center, ex, t1x)
    theta_shell = center_law.gamma_pair(q_shell, ex, t1x)
    print("\nBounded prototype Theta_R^(0):")
    print(f"  Theta_R^(0)(e0)        = ({theta_center[0]:+.12e}, {theta_center[1]:+.12e})")
    print(f"  Theta_R^(0)(s/sqrt(6)) = ({theta_shell[0]:+.12e}, {theta_shell[1]:+.12e})")

    record(
        "the exact support Hessian has no mixed A1-bright block",
        mixed_norm < 1e-12,
        f"max |P_A1^T G_S P_bright| = {mixed_norm:.3e}",
    )
    record(
        "the exact support-to-active operator is rank one",
        active_rank == 1 and pair_rank == 1,
        f"active rank={active_rank}, pair rank={pair_rank}",
    )
    record(
        "the exact support-to-active operator annihilates the bright channels",
        active_bright_norm < 1e-12,
        f"max bright-channel image norm = {active_bright_norm:.3e}",
    )
    record(
        "the exact support scalar delta_A1 survives but is scalar-only",
        abs(delta_e0 - 1.0 / 6.0) < 1e-12 and abs(delta_s) < 1e-12,
        f"endpoint values: e0={delta_e0:.3e}, s/sqrt(6)={delta_s:.3e}",
    )
    record(
        "the bounded prototype Theta_R^(0) is explicit on the two A1 endpoints",
        np.isfinite(theta_center[0]) and np.isfinite(theta_center[1]) and np.isfinite(theta_shell[0]) and np.isfinite(theta_shell[1]),
        f"Theta_R^(0)(e0)={theta_center}, Theta_R^(0)(s/sqrt(6))={theta_shell}",
        status="BOUNDED",
    )

    print("\nVerdict:")
    print(
        "The exact support-side machinery is scalar/rank-one on the current A1 "
        "block, so it cannot produce a nonzero exact tensor observable on "
        "A1 x {E_x, T1x}. The only available comparison surface is the bounded "
        "prototype Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))."
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
