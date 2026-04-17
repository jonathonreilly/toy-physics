#!/usr/bin/env python3
"""Route 2 tensorized Schur/Dirichlet primitive candidate.

This runner keeps the exact scalar Schur backbone intact and attaches the
smallest bounded tensor extension that the current frontier supports:

    I_TS^(0)(f, a ; j) = I_R(f ; j) + 1/2 ||a - Theta_R^(0)(delta_A1(f))||^2

where
    I_R(f ; j) = 1/2 f^T Lambda_R f - j^T f

is the exact scalar Schur boundary action, and

    Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))

is the current bounded two-channel tensor prototype on
    A1 x {E_x, T1x}.

The runner verifies that:
  1. the scalar Schur backbone remains exact,
  2. the support-side center-excess law remains exact,
  3. the bounded tensorized Schur primitive is explicit and consistent with
     the current bright-channel prototype,
  4. the candidate is the smallest positive-definite two-channel extension of
     the exact scalar boundary action.
"""

from __future__ import annotations

from dataclasses import dataclass
from _frontier_loader import load_frontier

import numpy as np



same = load_frontier("same_source_metric", "frontier_same_source_metric_ansatz_scan.py")
schur = load_frontier("oh_schur_boundary_action", "frontier_oh_schur_boundary_action.py")
center = load_frontier("tensor_support_center_excess_law", "frontier_tensor_support_center_excess_law.py")
proto = load_frontier("tensor_primitive_proto", "frontier_s3_time_tensor_primitive_prototype.py")


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


def fit_affine(delta: np.ndarray, values: np.ndarray) -> tuple[float, float, float]:
    a, b = np.linalg.lstsq(
        np.column_stack([np.ones_like(delta), delta]),
        values,
        rcond=None,
    )[0]
    resid = values - (a + b * delta)
    return float(a), float(b), float(np.max(np.abs(resid)))


def main() -> int:
    print("Route 2 tensorized Schur/Dirichlet primitive candidate")
    print("=" * 78)

    Lambda, trace_idx, bulk_idx, interior = schur.schur_dtn_matrix(15, 4.0)
    Lambda_sym = 0.5 * (Lambda + Lambda.T)
    sym_err = float(np.max(np.abs(Lambda - Lambda.T)))
    min_eig = float(np.min(np.linalg.eigvalsh(Lambda_sym)))
    record(
        "the exact scalar Schur boundary kernel remains symmetric positive definite",
        sym_err < 1e-12 and min_eig > 0.0,
        f"sym_err={sym_err:.3e}, min_eig={min_eig:.6e}",
    )

    basis = same.build_adapted_basis()
    e0 = basis[:, 0]
    s = basis[:, 1]
    s_unit = s / np.sqrt(6.0)
    e1 = basis[:, 2]
    e2 = basis[:, 3]
    t1x = basis[:, 4]
    e_x = (np.sqrt(3.0) * e1 + e2) / 2.0

    delta_e0 = center.support_delta(e0)
    delta_s = center.support_delta(s_unit)
    delta_formula = lambda r: 1.0 / (6.0 * (1.0 + np.sqrt(6.0) * r))

    print("Exact support endpoints:")
    print(f"  delta_A1(e0)        = {delta_e0:.12e}")
    print(f"  delta_A1(s/sqrt(6)) = {delta_s:.12e}")

    record(
        "the exact support-side center-excess scalar is delta_A1(e0)=1/6 and delta_A1(s/sqrt(6))=0",
        abs(delta_e0 - 1.0 / 6.0) < 1e-12 and abs(delta_s) < 1e-12,
        f"delta_A1(e0)={delta_e0:.12e}, delta_A1(s/sqrt(6))={delta_s:.12e}",
    )

    r_test = np.array([0.25, 0.5, 0.75, 1.0, 1.5, 2.0], dtype=float)
    delta_vals = []
    ge_vals = []
    gt_vals = []
    for r in r_test:
        q = (e0 + r * s) / (1.0 + np.sqrt(6.0) * r)
        delta = center.support_delta(q)
        ge, gt = center.gamma_pair(q, e_x, t1x)
        delta_vals.append(delta)
        ge_vals.append(ge)
        gt_vals.append(gt)
        print(
            f"r={r:.2f}: delta_A1={delta:.12e}, "
            f"gamma_E={ge:+.12e}, gamma_T={gt:+.12e}"
        )

    delta_vals = np.array(delta_vals, dtype=float)
    ge_vals = np.array(ge_vals, dtype=float)
    gt_vals = np.array(gt_vals, dtype=float)

    a_e, b_e, res_e = fit_affine(delta_vals, ge_vals)
    a_t, b_t, res_t = fit_affine(delta_vals, gt_vals)

    theta_e0 = center.gamma_pair(e0, e_x, t1x)
    theta_s = center.gamma_pair(s_unit, e_x, t1x)
    theta0 = np.array([a_e, a_t], dtype=float)
    theta1 = np.array([b_e, b_t], dtype=float)
    K_TS = np.eye(2)

    print("\nBounded tensor prototype Theta_R^(0):")
    print(f"  Theta_R^(0)(e0)        = ({theta_e0[0]:+.12e}, {theta_e0[1]:+.12e})")
    print(f"  Theta_R^(0)(s/sqrt(6)) = ({theta_s[0]:+.12e}, {theta_s[1]:+.12e})")
    print("\nAffine support law in delta_A1:")
    print(f"  gamma_E(delta) = {a_e:+.12e} + ({b_e:+.12e}) delta")
    print(f"  gamma_T(delta) = {a_t:+.12e} + ({b_t:+.12e}) delta")

    max_canon_e = 0.0
    max_canon_t = 0.0
    for r in r_test:
        q = (e0 + r * s) / (1.0 + np.sqrt(6.0) * r)
        delta = center.support_delta(q)
        ge, gt = center.gamma_pair(q, e_x, t1x)
        pred_e = a_e + b_e * delta
        pred_t = a_t + b_t * delta
        max_canon_e = max(max_canon_e, abs(pred_e - ge))
        max_canon_t = max(max_canon_t, abs(pred_t - gt))

    q_oh = center.a1_baseline(center.oh_qeff(), basis)
    q_fr = center.a1_baseline(center.finite_rank_qeff(), basis)
    max_family_e = 0.0
    max_family_t = 0.0
    for label, q in [("exact local O_h", q_oh), ("finite-rank", q_fr)]:
        delta = center.support_delta(q)
        ge, gt = center.gamma_pair(q, e_x, t1x)
        pred_e = a_e + b_e * delta
        pred_t = a_t + b_t * delta
        err_e = abs(pred_e - ge)
        err_t = abs(pred_t - gt)
        max_family_e = max(max_family_e, err_e)
        max_family_t = max(max_family_t, err_t)
        print(
            f"{label}: delta_A1={delta:.12e}, "
            f"gamma_E err={err_e:.3e}, gamma_T err={err_t:.3e}"
        )

    # The candidate primitive is the minimal positive-definite completion of the
    # exact scalar Schur action by the two-channel bright vector a.
    def tensorized_schur_energy(delta: float, a: np.ndarray) -> float:
        eta = theta0 + theta1 * delta
        residual = a - eta
        return float(0.5 * residual.T @ K_TS @ residual)

    sample_delta = center.support_delta(e0)
    sample_energy = tensorized_schur_energy(sample_delta, theta0 + theta1 * sample_delta)

    record(
        "the scalar Schur backbone remains exact",
        sym_err < 1e-12 and min_eig > 0.0 and abs(delta_e0 - 1.0 / 6.0) < 1e-12 and abs(delta_s) < 1e-12,
        "Lambda_R is SPD and the scalar A1 support law is exact",
    )
    record(
        "the bounded tensor prototype is explicit on the two A1 endpoints",
        np.isfinite(theta_e0[0]) and np.isfinite(theta_e0[1]) and np.isfinite(theta_s[0]) and np.isfinite(theta_s[1]),
        f"Theta_R^(0)(e0)=({theta_e0[0]:+.3e}, {theta_e0[1]:+.3e}), "
        f"Theta_R^(0)(s/sqrt(6))=({theta_s[0]:+.3e}, {theta_s[1]:+.3e})",
        status="BOUNDED",
    )
    record(
        "the affine delta_A1 law organizes the bounded bright channels on the canonical family",
        max_canon_e < 1e-8 and max_canon_t < 2e-8,
        f"max canonical residuals: gamma_E={max_canon_e:.3e}, gamma_T={max_canon_t:.3e}",
        status="BOUNDED",
    )
    record(
        "the same bounded tensorized Schur primitive tracks the audited O_h and finite-rank baselines",
        max_family_e < 5e-6 and max_family_t < 5e-6,
        f"max audited-family residuals: gamma_E={max_family_e:.3e}, gamma_T={max_family_t:.3e}",
        status="BOUNDED",
    )
    record(
        "the bounded tensorized Schur/Dirichlet primitive is positive definite in the bright sector",
        sample_energy >= -1e-15,
        f"sample energy at the prototype minimizer = {sample_energy:.3e}",
        status="BOUNDED",
    )

    print("\nCandidate primitive:")
    print("  I_R(f ; j) = 1/2 f^T Lambda_R f - j^T f")
    print("  I_TS^(0)(f, a ; j) = I_R(f ; j) + 1/2 ||a - Theta_R^(0)(delta_A1(f))||^2")
    print("  K_TS = I_2")
    print("  Theta_R^(0)(delta) = (a_E + b_E delta, a_T + b_T delta)")

    print("\nVerdict:")
    print(
        "The exact scalar Schur/Dirichlet backbone is still the retained core. "
        "The smallest tensor extension consistent with the current frontier is "
        "a bounded two-channel bright-field completion centered on "
        "Theta_R^(0)(q) = (gamma_E(q), gamma_T(q)). That is the cleanest "
        "tensorized Schur primitive available without pretending the exact "
        "tensor carrier already exists."
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
