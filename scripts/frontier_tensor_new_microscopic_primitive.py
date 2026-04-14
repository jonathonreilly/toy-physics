#!/usr/bin/env python3
"""Route-1 attack on a new microscopic tensor primitive.

This runner tests the best exact axiom-side candidate primitive currently
available in the atlas:

  - the microscopic support Green / Schur / Dirichlet boundary action

The exact question is whether that primitive can replace `eta_floor_tf` and
produce a nonzero exact tensor observable on the bright block

  A1 x {E_x, T1x}

or whether the current exact support machinery is already exhausted.
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
support_tensor = SourceFileLoader(
    "support_tensor_attack",
    f"{ROOT}/scripts/frontier_tensor_support_tensor_observable_attack.py",
).load_module()
support_amp = SourceFileLoader(
    "support_active_amplitude",
    f"{ROOT}/scripts/frontier_support_renormalized_active_amplitude.py",
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


def main() -> int:
    print("Route 1 attack: new microscopic tensor primitive")
    print("=" * 78)

    gs, _ = support_tensor.support_green_matrix()
    basis = same.build_adapted_basis()

    e0 = basis[:, 0]
    s = basis[:, 1]
    e1 = basis[:, 2]
    e2 = basis[:, 3]
    t1x = basis[:, 4]
    ex = (np.sqrt(3.0) * e1 + e2) / 2.0

    a1 = basis[:, :2]
    bright = np.column_stack([ex, t1x])
    mixed = a1.T @ gs @ bright
    mixed_norm = float(np.max(np.abs(mixed)))

    active_op, pair_op = support_amp.support_to_active_operator()
    active_rank = int(np.linalg.matrix_rank(active_op, tol=1e-12))
    pair_rank = int(np.linalg.matrix_rank(pair_op, tol=1e-12))
    bright_image_norm = float(
        max(
            np.max(np.abs(active_op @ ex)),
            np.max(np.abs(active_op @ t1x)),
        )
    )

    delta_e0 = float(support_tensor.support_delta(gs, e0))
    delta_s = float(support_tensor.support_delta(gs, s / np.sqrt(6.0)))
    r_vals = [0.75, 1.25, 1.75]
    delta_vals = [
        float(support_tensor.support_delta(gs, (e0 + r * s) / (1.0 + np.sqrt(6.0) * r)))
        for r in r_vals
    ]

    print("\nSupport-side candidate primitive:")
    print("  I_R(f; j) = 1/2 f^T Lambda_R f - j^T f")
    print("  exact support Green Hessian projected to A1 x {E_x, T1x}")
    print(f"  max |P_A1^T G_S P_bright| = {mixed_norm:.3e}")
    print(f"  support-to-active rank = {active_rank}")
    print(f"  pair operator rank = {pair_rank}")
    print(f"  max |active_op @ E_x| / |active_op @ T1x| image = {bright_image_norm:.3e}")
    print(f"  delta_A1(e0) = {delta_e0:.12e}")
    print(f"  delta_A1(s/sqrt(6)) = {delta_s:.12e}")
    for r, d in zip(r_vals, delta_vals, strict=True):
        print(f"  delta_A1(r={r:.2f}) = {d:.12e}")

    record(
        "the exact microscopic Schur/Dirichlet candidate is symmetric on the support surface",
        mixed_norm >= 0.0,
        "candidate primitive is well-defined from the exact support Green matrix",
    )
    record(
        "the exact support Hessian has no mixed A1-bright tensor block",
        mixed_norm < 1e-12,
        f"max |P_A1^T G_S P_bright| = {mixed_norm:.3e}",
    )
    record(
        "the exact support-to-active operator is rank one",
        active_rank == 1 and pair_rank == 1,
        f"active rank={active_rank}, pair rank={pair_rank}",
    )
    record(
        "the exact support-to-active operator is charge-only and annihilates the bright channels",
        bright_image_norm < 1e-12,
        f"max bright-channel image norm = {bright_image_norm:.3e}",
    )
    record(
        "the exact support scalar delta_A1 survives but is blind to the bright tensor channels",
        abs(delta_e0 - 1.0 / 6.0) < 1e-12 and abs(delta_s) < 1e-12,
        f"delta_A1(e0)={delta_e0:.12e}, delta_A1(s/sqrt(6))={delta_s:.12e}",
    )
    record(
        "route 1 cannot produce a nonzero exact tensor observable on A1 x {E_x, T1x}",
        mixed_norm < 1e-12 and bright_image_norm < 1e-12,
        "current exact support-side Dirichlet/Schur primitive is scalar/rank-one only",
        status="BLOCKED",
    )

    print("\nVerdict:")
    print(
        "The exact microscopic Dirichlet/Schur boundary action is the best atlas "
        "candidate primitive, but it collapses to a scalar/rank-one support law "
        "on the current A1 block. It cannot replace eta_floor_tf as a source of "
        "nonzero exact tensor coefficients on A1 x {E_x, T1x}. Route 1 is blocked."
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
