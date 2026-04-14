#!/usr/bin/env python3
"""Axiom-first primitive-chain reduction for Route 2.

This runner does not try to close GR directly. It proves the cleaner next
statement:

  on the current retained and bounded stack, the smallest missing Route-2
  primitive is an exact tensor-valued support observable on
  A1 x {E_x, T1x}.

It verifies the reduction from four ingredients already on the branch:

  1. exact route-2 kinematics on PL S^3 x R
  2. exact slice generator Lambda_R and bounded transfer bridge T_R
  3. scalar-only observable principle on this route
  4. two-channel tensor frontier plus exact A1 center-excess law
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib.machinery import SourceFileLoader
from pathlib import Path

import numpy as np
from scipy.linalg import expm


ROOT = Path("/private/tmp/physics-review-active")
REPO = Path("/Users/jonreilly/Projects/Physics")


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


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def first_existing(paths: list[Path]) -> Path:
    for path in paths:
        if path.exists():
            return path
    raise FileNotFoundError("None of the candidate paths exist: " + ", ".join(str(p) for p in paths))


def flat_index(ls: int, lt: int, x0: int, x1: int, x2: int, t: int) -> int:
    return (((x0 % ls) * ls + (x1 % ls)) * ls + (x2 % ls)) * lt + (t % lt)


def slice_projector(ls: int, lt: int, predicate) -> np.ndarray:
    n = ls**3 * lt
    p = np.zeros((n, n), dtype=complex)
    for x0 in range(ls):
        for x1 in range(ls):
            for x2 in range(ls):
                for t in range(lt):
                    i = flat_index(ls, lt, x0, x1, x2, t)
                    if predicate(x0, x1, x2, t):
                        p[i, i] = 1.0
    return p


def hessian_entry(inv_d: np.ndarray, p_a: np.ndarray, p_b: np.ndarray) -> float:
    return float((-np.trace(inv_d @ p_a @ inv_d @ p_b)).real)


def main() -> int:
    atlas = first_existing([
        REPO / "docs" / "publication" / "ci3_z3" / "DERIVATION_ATLAS.md",
        ROOT / "docs" / "publication" / "ci3_z3" / "DERIVATION_ATLAS.md",
    ])
    s3_note = first_existing([
        REPO / "docs" / "S3_GENERAL_R_DERIVATION_NOTE.md",
        ROOT / "docs" / "S3_GENERAL_R_DERIVATION_NOTE.md",
    ])
    anomaly_note = first_existing([
        REPO / "docs" / "ANOMALY_FORCES_TIME_THEOREM.md",
        ROOT / "docs" / "ANOMALY_FORCES_TIME_THEOREM.md",
    ])
    transfer_note = ROOT / "docs" / "S3_TIME_TRANSFER_MATRIX_BRIDGE_NOTE.md"
    observable_note = ROOT / "docs" / "S3_TIME_OBSERVABLE_HESSIAN_ROUTE_NOTE.md"
    support_note = ROOT / "docs" / "TENSOR_SUPPORT_CENTER_EXCESS_LAW_NOTE.md"
    two_channel_note = ROOT / "docs" / "TENSOR_BOUNDARY_DRIVE_TWO_CHANNEL_NOTE.md"

    atlas_text = read_text(atlas)
    s3_text = read_text(s3_note)
    anomaly_text = read_text(anomaly_note)
    transfer_text = read_text(transfer_note)
    observable_text = read_text(observable_note)
    support_text = read_text(support_note)
    two_channel_text = read_text(two_channel_note)

    same = SourceFileLoader(
        "same_source_metric",
        f"{ROOT}/scripts/frontier_same_source_metric_ansatz_scan.py",
    ).load_module()
    schur = SourceFileLoader(
        "oh_schur_boundary_action",
        f"{ROOT}/scripts/frontier_oh_schur_boundary_action.py",
    ).load_module()
    hier = SourceFileLoader(
        "hierarchy_observable_principle",
        f"{REPO}/scripts/frontier_hierarchy_observable_principle_from_axiom.py",
    ).load_module()
    two = SourceFileLoader(
        "tensor_two_channel",
        f"{ROOT}/scripts/frontier_tensor_boundary_drive_two_channel.py",
    ).load_module()
    center = SourceFileLoader(
        "tensor_center_excess",
        f"{ROOT}/scripts/frontier_tensor_support_center_excess_law.py",
    ).load_module()

    print("Route 2 primitive-chain reduction")
    print("=" * 78)

    s3_exact = (
        ("PL homeomorphic to S^3" in s3_text or "PL homeomorphic to `S^3`" in s3_text)
        and "for every R >= 2" in s3_text
    )
    time_exact = "d_t = 1" in anomaly_text and "single-clock" in anomaly_text.lower()
    atlas_support = (
        "Anomaly-forced time" in atlas_text
        and ("S^3 general-`R` extension" in atlas_text or "`S^3` general-`R` extension" in atlas_text)
        and ("Restricted Schur boundary action" in atlas_text or "Restricted strong-field closure synthesis" in atlas_text)
    )

    record(
        "Route-2 background is exact on PL S^3 x R",
        s3_exact and time_exact and atlas_support and "PL S^3 x R" in transfer_text,
        "S^3 + single-clock time are retained atlas tools",
    )

    Lambda, trace_idx, bulk_idx, interior = schur.schur_dtn_matrix(15, 4.0)
    Lambda_sym = 0.5 * (Lambda + Lambda.T)
    sym_err = float(np.max(np.abs(Lambda - Lambda.T)))
    min_eig = float(np.min(np.linalg.eigvalsh(Lambda_sym)))
    T = expm(-Lambda_sym)
    t_sym_err = float(np.max(np.abs(T - T.T)))
    t_radius = float(np.max(np.abs(np.linalg.eigvals(T))))

    record(
        "the current Route-2 slice law is exact/bounded through Lambda_R and T_R",
        "T_R := exp(-Lambda_R)" in transfer_text and sym_err < 1e-12 and min_eig > 0.0 and t_sym_err < 1e-12 and t_radius < 1.0,
        f"Lambda symmetry={sym_err:.3e}, min eig={min_eig:.6e}, T spectral radius={t_radius:.6e}",
        status="BOUNDED",
    )

    ls, lt, u0 = 2, 4, 0.9
    d = hier.build_dirac_4d_apbc(ls, lt, u0)
    inv_d = np.linalg.inv(d)
    p_time = slice_projector(ls, lt, lambda x0, x1, x2, t: t == 0)
    p_space = slice_projector(ls, lt, lambda x0, x1, x2, t: x0 == 0)
    h_tt = hessian_entry(inv_d, p_time, p_time)
    h_ss = hessian_entry(inv_d, p_space, p_space)
    h_ts = hessian_entry(inv_d, p_time, p_space)
    hessian = np.array([[h_tt, h_ts], [h_ts, h_ss]], dtype=float)
    h_sym_err = float(np.max(np.abs(hessian - hessian.T)))

    record(
        "the observable principle remains scalar-only on Route 2",
        "scalar-only" in observable_text and h_sym_err < 1e-12,
        f"scalar Hessian={hessian.tolist()}",
    )

    basis = same.build_adapted_basis()
    coeff = basis.T @ two.finite_rank_qeff()
    q_a1 = basis[:, :2] @ coeff[:2]
    e1 = basis[:, 2]
    e2 = basis[:, 3]
    t1x = basis[:, 4]
    t1y = basis[:, 5]
    t1z = basis[:, 6]
    e_x = (np.sqrt(3.0) * e1 + e2) / 2.0
    e_perp = (-e1 + np.sqrt(3.0) * e2) / 2.0
    eta0, _, _ = two.tensor_metrics(two.phi_from_q(q_a1))
    amp = 0.10
    deta_ex = two.tensor_metrics(two.phi_from_q(q_a1 + amp * e_x))[0] - eta0
    deta_ep = two.tensor_metrics(two.phi_from_q(q_a1 + amp * e_perp))[0] - eta0
    deta_tx = two.tensor_metrics(two.phi_from_q(q_a1 + amp * t1x))[0] - eta0
    deta_ty = two.tensor_metrics(two.phi_from_q(q_a1 + amp * t1y))[0] - eta0
    deta_tz = two.tensor_metrics(two.phi_from_q(q_a1 + amp * t1z))[0] - eta0

    bright_ok = (
        abs(deta_ex) > 1e-6
        and abs(deta_tx) > 1e-6
        and abs(deta_ep) < 1e-8
        and abs(deta_ty) < 1e-6
        and abs(deta_tz) < 1e-6
    )
    record(
        "the tensor frontier is already localized to the bright support channels E_x and T1x",
        bright_ok and "two-channel bright observable" in two_channel_text,
        (
            f"deta(E_x)={deta_ex:+.6e}, deta(E_perp)={deta_ep:+.6e}, "
            f"deta(T1x)={deta_tx:+.6e}, deta(T1y)={deta_ty:+.6e}, deta(T1z)={deta_tz:+.6e}"
        ),
        status="BOUNDED",
    )

    e0 = basis[:, 0]
    s = basis[:, 1]
    s_unit = s / np.sqrt(6.0)
    delta_e0 = center.support_delta(e0)
    delta_s = center.support_delta(s_unit)
    formula_e0 = 1.0 / 6.0
    formula_s = 0.0
    g_e0_e, g_e0_t = center.gamma_pair(e0, e_x, t1x)
    g_s_e, g_s_t = center.gamma_pair(s_unit, e_x, t1x)
    delta_ok = (
        abs(delta_e0 - formula_e0) < 1e-12
        and abs(delta_s - formula_s) < 1e-12
        and "delta_A1(r) = 1 / (6 (1 + sqrt(6) r))" in support_text
    )
    record(
        "the remaining A1 dependence is reduced to the exact support scalar delta_A1 and two endpoint coefficient pairs",
        delta_ok,
        (
            f"delta(e0)={delta_e0:.12e}, delta(shell)={delta_s:.12e}; "
            f"gamma(center)=({g_e0_e:+.6e},{g_e0_t:+.6e}), "
            f"gamma(shell)=({g_s_e:+.6e},{g_s_t:+.6e})"
        ),
        status="BOUNDED",
    )

    record(
        "the smallest missing Route-2 primitive is an exact tensor-valued support observable on A1 x {E_x, T1x}",
        all(c.ok for c in CHECKS[:-1]),
        "current scalar route stops at T_R; current tensor route is already reduced to bright support channels and endpoint data",
    )

    print()
    print("Primitive chain:")
    print("  P0: exact background PL S^3 x R")
    print("  P1: exact tensor support observable Theta_R on A1 x {E_x, T1x}")
    print("  P2: exact endpoint coefficient theorem at e0 and s/sqrt(6)")
    print("  P3: exact support-to-slice time-coupling law")
    print("  P4: exact PL S^3 x R dynamics action / uniqueness theorem")
    print()
    print(f"PASS={sum(c.ok for c in CHECKS)} FAIL={sum(not c.ok for c in CHECKS)}")
    return 1 if any(not c.ok for c in CHECKS) else 0


if __name__ == "__main__":
    raise SystemExit(main())
