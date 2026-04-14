#!/usr/bin/env python3
"""Exact A1 projective blindness of the current shell/junction tensor toolbox.

This runner tests the sharpest axiom-first question left in the gravity lane:

  can the remaining projective A1 shape law r = s/e0 be derived from the
  current exact shell/junction stack?

On the retained gravity surface, the exact ingredients are:
  - support-space A1 basis vectors e0, s
  - exact exterior projector on the sewing band
  - exact shell source sigma = H0(Pi_ext phi)
  - exact static-conformal shell lift
      rho = sigma / (2 pi psi^5)
      S   = rho * u / (1 - u)
    with u = Pi_ext phi

The key exact question is whether those shell/junction objects retain any
dependence on the projective A1 ratio r at fixed total charge Q.

If not, then the remaining tensor renormalization law cannot be derived from
the current shell/junction stack alone, and the right axiom-first pivot is to
the microscopic support block before exterior projection.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib.machinery import SourceFileLoader

import numpy as np


ROOT = "/private/tmp/physics-review-active"
SIZE = 15
EPS = 0.005
R_VALUES = [0.75, 1.25, 1.75]


same = SourceFileLoader(
    "same_source_metric",
    f"{ROOT}/scripts/frontier_same_source_metric_ansatz_scan.py",
).load_module()
sew = SourceFileLoader(
    "sewing_shell",
    f"{ROOT}/scripts/frontier_sewing_shell_source.py",
).load_module()
two = SourceFileLoader(
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


RADII = sew.radii_grid(SIZE)
BAND_MASK = (RADII > 3.0 + 1e-12) & (RADII <= 5.0 + 1e-12)


def support_green_columns() -> tuple[np.ndarray, int]:
    h0, interior = same.build_neg_laplacian_sparse(SIZE)
    center = interior // 2
    support = [
        same.flat_idx(center + v[0], center + v[1], center + v[2], interior)
        for v in same.SUPPORT_COORDS
    ]
    return same.solve_columns(h0, support), interior


G0P, INTERIOR = support_green_columns()


def phi_from_q(q: np.ndarray) -> np.ndarray:
    phi = np.zeros((SIZE, SIZE, SIZE), dtype=float)
    phi[1:-1, 1:-1, 1:-1] = (G0P @ q).reshape((INTERIOR, INTERIOR, INTERIOR))
    return phi


def bridge_fields(q: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    phi = phi_from_q(q)
    u = sew.exterior_projector(phi, 4.0)
    sigma = sew.full_neg_laplacian(u)
    psi = 1.0 + u
    alpha = (1.0 - u) / (1.0 + u)
    rho = sigma / (2.0 * np.pi * psi**5)
    stress = 0.5 * rho * (1.0 / alpha - 1.0)
    return u, sigma, rho, stress


def exact_linear_response(
    q_bg: np.ndarray, q_dir: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    u, sigma, rho, _ = bridge_fields(q_bg)
    du, dsigma, _, _ = bridge_fields(q_dir)
    psi = 1.0 + u
    drho = dsigma / (2.0 * np.pi * psi**5) - (5.0 * sigma * du) / (2.0 * np.pi * psi**6)
    dstress = drho * u / (1.0 - u) + rho * du / (1.0 - u) ** 2
    return du, dsigma, drho, dstress


def band_max_diff(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.max(np.abs(a[BAND_MASK] - b[BAND_MASK])))


def eta_floor(q: np.ndarray) -> float:
    return float(two.tensor_metrics(phi_from_q(q))[0])


def centered_beta(q_bg: np.ndarray, q_dir: np.ndarray) -> float:
    return float((eta_floor(q_bg + EPS * q_dir) - eta_floor(q_bg - EPS * q_dir)) / (2.0 * EPS))


def main() -> int:
    print("Exact A1 projective blindness of the current shell/junction tensor toolbox")
    print("=" * 78)

    basis = same.build_adapted_basis()
    e0 = basis[:, 0]
    s = basis[:, 1]
    e1 = basis[:, 2]
    e2 = basis[:, 3]
    t1x = basis[:, 4]
    ex = (np.sqrt(3.0) * e1 + e2) / 2.0

    q_s_unit = s / np.sqrt(6.0)

    u_e0, sigma_e0, _, _ = bridge_fields(e0)
    u_s, sigma_s, _, _ = bridge_fields(q_s_unit)
    u_diff = band_max_diff(u_e0, u_s)
    sigma_diff = band_max_diff(sigma_e0, sigma_s)

    print(f"max band difference of u/Q between e0 and s/sqrt(6) = {u_diff:.3e}")
    print(f"max band difference of sigma/Q between e0 and s/sqrt(6) = {sigma_diff:.3e}")

    record(
        "A1(center) and A1(shell) induce the same exterior-projector potential per unit charge on the sewing band",
        u_diff < 1e-12,
        f"max band difference = {u_diff:.3e}",
    )
    record(
        "A1(center) and A1(shell) induce the same shell source per unit charge on the sewing band",
        sigma_diff < 1e-12,
        f"max band difference = {sigma_diff:.3e}",
    )

    response_rows = []
    for r in R_VALUES:
        q = (e0 + r * s) / (1.0 + np.sqrt(6.0) * r)
        du_ex, dsig_ex, drho_ex, dS_ex = exact_linear_response(q, ex)
        du_tx, dsig_tx, drho_tx, dS_tx = exact_linear_response(q, t1x)
        beta_ex = centered_beta(q, ex)
        beta_tx = centered_beta(q, t1x)
        response_rows.append(
            {
                "r": r,
                "du_ex": du_ex,
                "dsig_ex": dsig_ex,
                "drho_ex": drho_ex,
                "dS_ex": dS_ex,
                "du_tx": du_tx,
                "dsig_tx": dsig_tx,
                "drho_tx": drho_tx,
                "dS_tx": dS_tx,
                "beta_ex": beta_ex,
                "beta_tx": beta_tx,
            }
        )
        print(
            f"r={r:.2f}: beta_E_x={beta_ex:+.12e}, beta_T1x={beta_tx:+.12e}"
        )

    first = response_rows[0]
    max_du_ex = max(band_max_diff(first["du_ex"], row["du_ex"]) for row in response_rows[1:])
    max_dsig_ex = max(band_max_diff(first["dsig_ex"], row["dsig_ex"]) for row in response_rows[1:])
    max_drho_ex = max(band_max_diff(first["drho_ex"], row["drho_ex"]) for row in response_rows[1:])
    max_dS_ex = max(band_max_diff(first["dS_ex"], row["dS_ex"]) for row in response_rows[1:])
    max_du_tx = max(band_max_diff(first["du_tx"], row["du_tx"]) for row in response_rows[1:])
    max_dsig_tx = max(band_max_diff(first["dsig_tx"], row["dsig_tx"]) for row in response_rows[1:])
    max_drho_tx = max(band_max_diff(first["drho_tx"], row["drho_tx"]) for row in response_rows[1:])
    max_dS_tx = max(band_max_diff(first["dS_tx"], row["dS_tx"]) for row in response_rows[1:])

    beta_ex_vals = [row["beta_ex"] for row in response_rows]
    beta_tx_vals = [row["beta_tx"] for row in response_rows]
    beta_ex_spread = float(max(beta_ex_vals) - min(beta_ex_vals))
    beta_tx_spread = float(max(beta_tx_vals) - min(beta_tx_vals))

    print(
        "exact shell/junction response spreads at fixed Q=1:\n"
        f"  E_x: du={max_du_ex:.3e}, dsigma={max_dsig_ex:.3e}, "
        f"drho={max_drho_ex:.3e}, dS={max_dS_ex:.3e}\n"
        f"  T1x: du={max_du_tx:.3e}, dsigma={max_dsig_tx:.3e}, "
        f"drho={max_drho_tx:.3e}, dS={max_dS_tx:.3e}"
    )
    print(
        "numerical tensor-drive coefficient spreads on the same Q=1 projective grid:\n"
        f"  beta_E_x spread = {beta_ex_spread:.3e}\n"
        f"  beta_T1x spread = {beta_tx_spread:.3e}"
    )

    record(
        "for fixed total charge, the exact shell/junction response to E_x is projectively blind to the A1 ratio r",
        max_du_ex < 1e-12 and max_dsig_ex < 1e-12 and max_drho_ex < 1e-12 and max_dS_ex < 1e-12,
        (
            f"max band spreads: du={max_du_ex:.3e}, dsigma={max_dsig_ex:.3e}, "
            f"drho={max_drho_ex:.3e}, dS={max_dS_ex:.3e}"
        ),
    )
    record(
        "for fixed total charge, the exact shell/junction response to T1x is projectively blind to the A1 ratio r",
        max_du_tx < 1e-12 and max_dsig_tx < 1e-12 and max_drho_tx < 1e-12 and max_dS_tx < 1e-12,
        (
            f"max band spreads: du={max_du_tx:.3e}, dsigma={max_dsig_tx:.3e}, "
            f"drho={max_drho_tx:.3e}, dS={max_dS_tx:.3e}"
        ),
    )
    record(
        "the current numerical tensor-drive coefficients still vary across the same projective A1 grid",
        beta_ex_spread > 1e-7 and beta_tx_spread > 1e-7,
        f"spreads: beta_E_x={beta_ex_spread:.3e}, beta_T1x={beta_tx_spread:.3e}",
        status="BOUNDED",
    )

    print("\nVerdict:")
    print(
        "The current exact shell/junction tensor toolbox is projectively blind "
        "to the A1 background ratio r at fixed total charge. So the remaining "
        "r-law seen by the numerical tensor boundary drive cannot be derived "
        "from the present shell/junction stack alone. The clean axiom-first "
        "pivot is to the microscopic support block before exterior projection."
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
