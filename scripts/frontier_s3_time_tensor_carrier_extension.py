#!/usr/bin/env python3
"""Exact blocker for a tensor-carrier extension of the Route 2 Schur/static stack.

This runner tests the narrow question:

    can the exact Schur boundary action plus static-constraint lift be minimally
    extended into a genuine tensor carrier on the current support block
    A1 x {E_x, T1x}?

The answer on the current retained machinery is no:
  - the exact support Hessian has no mixed A1-bright block,
  - the exact support-to-active operator is rank one / charge-only,
  - the exact support scalar delta_A1 is blind to E_x and T1x.

The runner also prints the bounded staging object Theta_R^(0) so the exact
blocker is separated from the best available prototype.
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
support_amp = SourceFileLoader(
    "support_renorm_active_amp",
    f"{ROOT}/scripts/frontier_support_renormalized_active_amplitude.py",
).load_module()
center_law = SourceFileLoader(
    "tensor_support_center_excess_law",
    f"{ROOT}/scripts/frontier_tensor_support_center_excess_law.py",
).load_module()
two_channel = SourceFileLoader(
    "tensor_two_channel",
    f"{ROOT}/scripts/frontier_tensor_boundary_drive_two_channel.py",
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


def support_green_matrix() -> np.ndarray:
    h0, interior = same.build_neg_laplacian_sparse(15)
    center = interior // 2
    support = [
        same.flat_idx(center + v[0], center + v[1], center + v[2], interior)
        for v in same.SUPPORT_COORDS
    ]
    g0p = same.solve_columns(h0, support)
    return g0p[support, :]


def main() -> int:
    print("Route 2 tensor-carrier extension blocker")
    print("=" * 78)

    basis = same.build_adapted_basis()
    e0 = basis[:, 0]
    s = basis[:, 1]
    e1 = basis[:, 2]
    e2 = basis[:, 3]
    t1x = basis[:, 4]
    t1y = basis[:, 5]
    t1z = basis[:, 6]
    e_x = (np.sqrt(3.0) * e1 + e2) / 2.0
    e_perp = (-e1 + np.sqrt(3.0) * e2) / 2.0

    gs = support_green_matrix()
    a1 = np.column_stack([e0, s])
    bright = np.column_stack([e_x, t1x])
    mixed = a1.T @ gs @ bright
    mixed_norm = float(np.max(np.abs(mixed)))

    print("Mixed A1-bright support block:")
    print(np.array2string(mixed, precision=12, floatmode="fixed"))
    print(f"max |P_A1^T G_S P_bright| = {mixed_norm:.3e}")

    active_op, pair_op = support_amp.support_to_active_operator()
    active_rank = int(np.linalg.matrix_rank(active_op, tol=1e-12))
    pair_rank = int(np.linalg.matrix_rank(pair_op, tol=1e-12))
    active_bright_norm = max(
        float(np.max(np.abs(active_op @ e_x))),
        float(np.max(np.abs(active_op @ t1x))),
    )

    print("\nSupport-to-active operator:")
    print(np.array2string(active_op, precision=6, floatmode="fixed"))
    print(f"active rank = {active_rank}")
    print(f"pair rank = {pair_rank}")
    print(f"max |active_op @ E_x| = {float(np.max(np.abs(active_op @ e_x))):.3e}")
    print(f"max |active_op @ T1x| = {float(np.max(np.abs(active_op @ t1x))):.3e}")

    delta_e0 = center_law.support_delta(e0)
    delta_s = center_law.support_delta(s / np.sqrt(6.0))
    bright_dir_max = 0.0
    for label, q in [("e0", e0), ("s/sqrt(6)", s / np.sqrt(6.0))]:
        for chan_name, v in [("E_x", e_x), ("T1x", t1x)]:
            eps = 1e-6
            d = (
                center_law.support_delta(q + eps * v)
                - center_law.support_delta(q - eps * v)
            ) / (2.0 * eps)
            bright_dir_max = max(bright_dir_max, abs(float(d)))
            print(f"{label:>8} along {chan_name}: d delta_A1 = {float(d):+.3e}")

    theta_e0 = center_law.gamma_pair(e0, e_x, t1x)
    theta_s = center_law.gamma_pair(s / np.sqrt(6.0), e_x, t1x)
    print("\nBounded staging object Theta_R^(0):")
    print(f"  Theta_R^(0)(e0) = ({theta_e0[0]:+.12e}, {theta_e0[1]:+.12e})")
    print(
        f"  Theta_R^(0)(s/sqrt(6)) = ({theta_s[0]:+.12e}, {theta_s[1]:+.12e})"
    )

    record(
        "the exact support Hessian has no mixed A1-bright block",
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
        active_bright_norm < 1e-12,
        f"max bright-channel image norm = {active_bright_norm:.3e}",
    )
    record(
        "the exact support scalar delta_A1 is blind to bright-channel perturbations",
        bright_dir_max < 1e-10,
        f"max bright directional derivative = {bright_dir_max:.3e}",
    )
    record(
        "the bounded Theta_R^(0) staging object remains distinct from an exact tensor carrier",
        abs(theta_e0[0]) > 0.0 and abs(theta_s[0]) > 0.0,
        (
            f"Theta_R^(0)(e0)=({theta_e0[0]:+.3e},{theta_e0[1]:+.3e}), "
            f"Theta_R^(0)(s/sqrt(6))=({theta_s[0]:+.3e},{theta_s[1]:+.3e})"
        ),
        status="BOUNDED",
    )

    print("\nVerdict:")
    print(
        "The exact Schur boundary action plus static-constraint lift do not "
        "tensorize on the current support-side stack. The support Hessian is "
        "scalar/rank-one on A1, the support-to-active map is charge-only, and "
        "the surviving scalar delta_A1 does not see the bright tensor channels. "
        "So the branch still lacks an exact tensor carrier on A1 x {E_x, T1x}; "
        "Theta_R^(0) remains only a bounded staging object."
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
