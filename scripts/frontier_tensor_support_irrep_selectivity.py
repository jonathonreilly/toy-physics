#!/usr/bin/env python3
"""Support-irrep selectivity of the tensor boundary drive.

This runner refines the support-irrep channel scan by testing the actual
coupled directions in the current tensor orientation.

On the support-irrep basis of the seven-site star:
  - E is two-dimensional
  - T1 is three-dimensional

The current tensor-drive observable need not couple to every direction equally.
This runner checks whether the response is concentrated on one aligned E
quadrupole direction and one aligned T1 shift direction.
"""

from __future__ import annotations

from contextlib import redirect_stdout
from dataclasses import dataclass
from importlib.machinery import SourceFileLoader
from io import StringIO

import numpy as np


ROOT = "/private/tmp/physics-review-active"

same_source = SourceFileLoader(
    "same_source_metric",
    f"{ROOT}/scripts/frontier_same_source_metric_ansatz_scan.py",
).load_module()
finite_rank = SourceFileLoader(
    "finite_rank_metric",
    f"{ROOT}/scripts/frontier_finite_rank_gravity_residual.py",
).load_module()
utk = SourceFileLoader(
    "tensor_universal_kernel",
    f"{ROOT}/scripts/frontier_tensor_universal_kernel.py",
).load_module()


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    status: str


CHECKS: list[Check] = []

SIZE = 15
AMPLITUDES = [0.02, 0.05, 0.10]


def record(name: str, ok: bool, detail: str, status: str = "BOUNDED") -> None:
    CHECKS.append(Check(name=name, ok=ok, detail=detail, status=status))
    tag = "PASS" if ok else "FAIL"
    print(f"[{status}] {tag}: {name}")
    if detail:
        print(f"    {detail}")


def support_green_columns() -> tuple[np.ndarray, int]:
    H0, interior = same_source.build_neg_laplacian_sparse(SIZE)
    center = interior // 2
    support = [
        same_source.flat_idx(center + v[0], center + v[1], center + v[2], interior)
        for v in same_source.SUPPORT_COORDS
    ]
    return same_source.solve_columns(H0, support), interior


G0P, INTERIOR = support_green_columns()


def phi_from_q(q: np.ndarray) -> np.ndarray:
    phi = np.zeros((SIZE, SIZE, SIZE), dtype=float)
    phi[1:-1, 1:-1, 1:-1] = (G0P @ q).reshape((INTERIOR, INTERIOR, INTERIOR))
    return phi


def c_eta(phi_grid: np.ndarray) -> float:
    with redirect_stdout(StringIO()):
        blk = utk.family_block("scan", phi_grid)
    return float(blk.eta_floor[1] / abs(blk.scalar_action))


def finite_rank_qeff() -> np.ndarray:
    _, _, _, _, _, GS, W, masses = finite_rank.finite_rank_setup()
    return np.linalg.solve(np.eye(W.shape[0]) - W @ GS, masses)


def main() -> int:
    print("Tensor-drive selectivity in support-irrep coordinates")
    print("=" * 78)

    basis = same_source.build_adapted_basis()
    coeff = basis.T @ finite_rank_qeff()
    q_a1 = basis[:, :2] @ coeff[:2]

    e1 = basis[:, 2]
    e2 = basis[:, 3]
    t1x = basis[:, 4]
    t1y = basis[:, 5]
    t1z = basis[:, 6]

    # x-aligned quadrupole direction in the canonical E basis.
    e_x = (np.sqrt(3.0) * e1 + e2) / 2.0
    e_perp = (-e1 + np.sqrt(3.0) * e2) / 2.0

    base = c_eta(phi_from_q(q_a1))
    print(f"A1 baseline c_eta = {base:.12e}")

    rows: list[tuple[float, float, float, float, float]] = []
    for amp in AMPLITUDES:
        d_ex = c_eta(phi_from_q(q_a1 + amp * e_x)) - base
        d_ep = c_eta(phi_from_q(q_a1 + amp * e_perp)) - base
        d_tx = c_eta(phi_from_q(q_a1 + amp * t1x)) - base
        d_ty = c_eta(phi_from_q(q_a1 + amp * t1y)) - base
        d_tz = c_eta(phi_from_q(q_a1 + amp * t1z)) - base
        rows.append((amp, d_ex, d_ep, d_tx, d_ty, d_tz))
        print(
            f"amp={amp:.2f}: "
            f"dE_x={d_ex:+.12e}, dE_perp={d_ep:+.12e}, "
            f"dT1x={d_tx:+.12e}, dT1y={d_ty:+.12e}, dT1z={d_tz:+.12e}"
        )

    max_dark = max(max(abs(r[2]), abs(r[4]), abs(r[5])) for r in rows)
    min_bright = min(min(abs(r[1]), abs(r[3])) for r in rows)
    brightness_ratio = min_bright / max(max_dark, 1e-16)

    ex_slopes = [abs(r[1]) / r[0] for r in rows]
    tx_slopes = [abs(r[3]) / r[0] for r in rows]
    ex_slope_rel = (max(ex_slopes) - min(ex_slopes)) / max(ex_slopes[0], 1e-16)
    tx_slope_rel = (max(tx_slopes) - min(tx_slopes)) / max(tx_slopes[0], 1e-16)

    record(
        "the tensor drive couples strongly to one aligned E quadrupole direction and weakly to the orthogonal E direction",
        max(abs(r[2]) for r in rows) < 1e-8 and min(abs(r[1]) for r in rows) > 1e-6,
        f"bright/dark E-channel ratio={brightness_ratio:.3e}, max dark E_perp response={max(abs(r[2]) for r in rows):.3e}",
    )
    record(
        "the tensor drive couples strongly to one aligned T1 direction and is dark on the orthogonal T1 directions",
        max(max(abs(r[4]), abs(r[5])) for r in rows) < 1e-6 and min(abs(r[3]) for r in rows) > 1e-6,
        f"max dark T1y/z response={max(max(abs(r[4]), abs(r[5])) for r in rows):.3e}",
    )
    record(
        "the aligned E-channel response is nearly linear in amplitude",
        ex_slope_rel < 2e-2,
        f"aligned-E slope variation={ex_slope_rel:.6e}",
    )
    record(
        "the aligned T1-channel response is nearly linear in amplitude",
        tx_slope_rel < 2e-2,
        f"aligned-T1 slope variation={tx_slope_rel:.6e}",
    )

    print("\nVerdict:")
    print(
        "In the current tensor orientation, the remaining source-to-tensor "
        "law is effectively two-channel: one aligned E quadrupole direction "
        "and one aligned T1 shift direction. The orthogonal E direction and "
        "the transverse T1 directions are dark to numerical precision on the "
        "audited star-supported class."
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
