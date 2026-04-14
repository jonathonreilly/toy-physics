#!/usr/bin/env python3
"""Two-channel law for the tensor boundary drive on the current source class.

This runner reformulates the current gravity frontier in terms of the tensor
boundary drive itself:

    eta_floor_tf

rather than the derived ratio c_eta = eta_floor_tf / |I_scalar|.

Using the exact star-supported support-irrep basis, it checks:
  1. scalar-action response is irrep-isotropic inside E and inside T1
  2. eta_floor_tf is bright only on the aligned E_x and T1x channels
  3. eta_floor_tf is nearly affine in those two bright channel amplitudes on
     the audited exact source class
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


def tensor_metrics(phi_grid: np.ndarray) -> tuple[float, float, float]:
    with redirect_stdout(StringIO()):
        blk = utk.family_block("scan", phi_grid)
    return (
        float(blk.eta_floor[1]),
        float(blk.scalar_action),
        float(blk.eta_floor[1] / abs(blk.scalar_action)),
    )


def finite_rank_qeff() -> np.ndarray:
    _, _, _, _, _, GS, W, masses = finite_rank.finite_rank_setup()
    return np.linalg.solve(np.eye(W.shape[0]) - W @ GS, masses)


def fit_linear(amplitudes: np.ndarray, values: np.ndarray) -> tuple[float, float, float]:
    beta = float(np.linalg.lstsq(amplitudes.reshape(-1, 1), values, rcond=None)[0][0])
    resid = values - beta * amplitudes
    slope_var = (max(abs(values / amplitudes)) - min(abs(values / amplitudes))) / max(abs(values[0] / amplitudes[0]), 1e-16)
    return beta, float(np.max(np.abs(resid))), float(slope_var)


def main() -> int:
    print("Two-channel law for the tensor boundary drive")
    print("=" * 78)

    basis = same_source.build_adapted_basis()
    coeff = basis.T @ finite_rank_qeff()
    q_a1 = basis[:, :2] @ coeff[:2]

    e1 = basis[:, 2]
    e2 = basis[:, 3]
    t1x = basis[:, 4]
    t1y = basis[:, 5]
    t1z = basis[:, 6]

    e_x = (np.sqrt(3.0) * e1 + e2) / 2.0
    e_perp = (-e1 + np.sqrt(3.0) * e2) / 2.0

    eta0, scalar0, c0 = tensor_metrics(phi_from_q(q_a1))
    print(f"A1 baseline: eta_floor_tf={eta0:.12e}, scalar_action={scalar0:.12e}, c_eta={c0:.12e}")

    rows = []
    for amp in AMPLITUDES:
        m_ex = tensor_metrics(phi_from_q(q_a1 + amp * e_x))
        m_ep = tensor_metrics(phi_from_q(q_a1 + amp * e_perp))
        m_tx = tensor_metrics(phi_from_q(q_a1 + amp * t1x))
        m_ty = tensor_metrics(phi_from_q(q_a1 + amp * t1y))
        m_tz = tensor_metrics(phi_from_q(q_a1 + amp * t1z))
        rows.append(
            (
                amp,
                m_ex[0] - eta0,
                m_ep[0] - eta0,
                m_tx[0] - eta0,
                m_ty[0] - eta0,
                m_tz[0] - eta0,
                m_ex[1] - scalar0,
                m_ep[1] - scalar0,
                m_tx[1] - scalar0,
                m_ty[1] - scalar0,
                m_tz[1] - scalar0,
            )
        )
        print(
            f"amp={amp:.2f}: "
            f"deta(E_x)={m_ex[0]-eta0:+.12e}, deta(E_perp)={m_ep[0]-eta0:+.12e}, "
            f"deta(T1x)={m_tx[0]-eta0:+.12e}, deta(T1y)={m_ty[0]-eta0:+.12e}, deta(T1z)={m_tz[0]-eta0:+.12e}"
        )
        print(
            f"         "
            f"dI(E_x)={m_ex[1]-scalar0:+.12e}, dI(E_perp)={m_ep[1]-scalar0:+.12e}, "
            f"dI(T1x)={m_tx[1]-scalar0:+.12e}, dI(T1y)={m_ty[1]-scalar0:+.12e}, dI(T1z)={m_tz[1]-scalar0:+.12e}"
        )

    amplitudes = np.array([r[0] for r in rows], dtype=float)
    deta_ex = np.array([r[1] for r in rows], dtype=float)
    deta_ep = np.array([r[2] for r in rows], dtype=float)
    deta_tx = np.array([r[3] for r in rows], dtype=float)
    deta_ty = np.array([r[4] for r in rows], dtype=float)
    deta_tz = np.array([r[5] for r in rows], dtype=float)

    dI_ex = np.array([r[6] for r in rows], dtype=float)
    dI_ep = np.array([r[7] for r in rows], dtype=float)
    dI_tx = np.array([r[8] for r in rows], dtype=float)
    dI_ty = np.array([r[9] for r in rows], dtype=float)
    dI_tz = np.array([r[10] for r in rows], dtype=float)

    beta_ex, resid_ex, slope_ex = fit_linear(amplitudes, deta_ex)
    beta_tx, resid_tx, slope_tx = fit_linear(amplitudes, deta_tx)

    print("\nFitted bright-channel coefficients for eta_floor_tf:")
    print(f"  beta_E_x  = {beta_ex:+.12e}  (max residual {resid_ex:.3e}, slope variation {slope_ex:.3e})")
    print(f"  beta_T1x  = {beta_tx:+.12e}  (max residual {resid_tx:.3e}, slope variation {slope_tx:.3e})")

    record(
        "scalar-action response is isotropic inside the E irrep",
        float(np.max(np.abs(dI_ex - dI_ep))) < 1e-12,
        f"max |dI(E_x)-dI(E_perp)|={float(np.max(np.abs(dI_ex-dI_ep))):.3e}",
        status="EXACT",
    )
    record(
        "scalar-action response is isotropic inside the T1 irrep",
        float(np.max(np.abs(dI_tx - dI_ty))) < 1e-12 and float(np.max(np.abs(dI_tx - dI_tz))) < 1e-12,
        (
            f"max |dI(T1x)-dI(T1y)|={float(np.max(np.abs(dI_tx-dI_ty))):.3e}, "
            f"max |dI(T1x)-dI(T1z)|={float(np.max(np.abs(dI_tx-dI_tz))):.3e}"
        ),
        status="EXACT",
    )
    record(
        "eta_floor_tf is bright only on the aligned E_x and T1x source channels",
        float(np.max(np.abs(deta_ep))) < 1e-8 and float(np.max(np.abs(deta_ty))) < 1e-6 and float(np.max(np.abs(deta_tz))) < 1e-6,
        (
            f"max dark responses: E_perp={float(np.max(np.abs(deta_ep))):.3e}, "
            f"T1y={float(np.max(np.abs(deta_ty))):.3e}, T1z={float(np.max(np.abs(deta_tz))):.3e}"
        ),
    )
    record(
        "eta_floor_tf is nearly affine in the bright E_x and T1x amplitudes on the audited source class",
        resid_ex < 5e-8 and resid_tx < 5e-8 and slope_ex < 1e-2 and slope_tx < 1e-2,
        (
            f"E_x: beta={beta_ex:+.6e}, resid={resid_ex:.3e}, slope_var={slope_ex:.3e}; "
            f"T1x: beta={beta_tx:+.6e}, resid={resid_tx:.3e}, slope_var={slope_tx:.3e}"
        ),
    )

    print("\nVerdict:")
    print(
        "The current gravity frontier is most cleanly phrased at the level of "
        "the tensor boundary drive eta_floor_tf: the scalar action is exactly "
        "irrep-isotropic, while eta_floor_tf is a two-channel bright observable "
        "of the aligned E_x and T1x source directions, with bounded affine "
        "response on the audited exact source class."
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
