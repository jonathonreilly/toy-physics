#!/usr/bin/env python3
"""Exact support-side A1 center-excess law plus bounded tensor consequence.

This runner advances the post-blindness gravity route on the microscopic
support block rather than the shell side.

Exact content:
  1. On the seven-site star support, the exact A1 support block at fixed total
     charge retains one scalar datum after charge normalization:
         delta_A1 = (phi_support(center) - phi_support(arm_mean)) / Q.
  2. For the canonical Q=1 projective A1 family
         q_A1(r) = (e0 + r s) / (1 + sqrt(6) r),
     that exact datum is
         delta_A1(r) = 1 / (6 (1 + sqrt(6) r)).

Bounded content:
  3. The current bright tensor coefficients gamma_E, gamma_T are almost
     perfectly affine in that exact support-side scalar on the canonical A1
     family.
  4. The same affine law predicts the audited exact local O_h and finite-rank
     A1 baselines to the same few-e-6 level already seen in the projective-A1
     compatibility note.
"""

from __future__ import annotations

from dataclasses import dataclass
from _frontier_loader import load_frontier

import numpy as np


EPS = 0.005
R_TEST = [0.25, 0.5, 0.75, 1.0, 1.5, 2.0]


same = load_frontier("same_source_metric", "frontier_same_source_metric_ansatz_scan.py")
finite_rank = load_frontier("finite_rank_metric", "frontier_finite_rank_gravity_residual.py")
two = load_frontier("tensor_two_channel", "frontier_tensor_boundary_drive_two_channel.py")
shell = load_frontier("one_parameter_shell", "frontier_one_parameter_reduced_shell_law.py")


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


H0, INTERIOR = same.build_neg_laplacian_sparse(15)
CENTER = INTERIOR // 2
SUPPORT = [
    same.flat_idx(CENTER + v[0], CENTER + v[1], CENTER + v[2], INTERIOR)
    for v in same.SUPPORT_COORDS
]
G0P = same.solve_columns(H0, SUPPORT)
GS = G0P[SUPPORT, :]


def phi_from_q(q: np.ndarray) -> np.ndarray:
    phi = np.zeros((15, 15, 15), dtype=float)
    phi[1:-1, 1:-1, 1:-1] = (G0P @ q).reshape((INTERIOR, INTERIOR, INTERIOR))
    return phi


def support_potential(q: np.ndarray) -> np.ndarray:
    return GS @ q


def support_delta(q: np.ndarray) -> float:
    vals = support_potential(q)
    q_total = float(np.sum(q))
    return float(vals[0] / q_total - np.mean(vals[1:]) / q_total)


def eta_floor(q: np.ndarray) -> float:
    return float(two.tensor_metrics(phi_from_q(q))[0])


def gamma_pair(q: np.ndarray, ex: np.ndarray, t1x: np.ndarray) -> tuple[float, float]:
    beta_e = float((eta_floor(q + EPS * ex) - eta_floor(q - EPS * ex)) / (2.0 * EPS))
    beta_t = float((eta_floor(q + EPS * t1x) - eta_floor(q - EPS * t1x)) / (2.0 * EPS))
    red = shell.reduced_data(phi_from_q(q))
    a_aniso = float(red["anchor_per_Q"]) * float(np.sum(q))
    return beta_e / a_aniso, beta_t / a_aniso


def oh_qeff() -> np.ndarray:
    w = same.build_commutant_operator(0.0698, 0.0499, -0.0070, 0.0642, 0.1056)
    m = same.build_invariant_source(0.8247, 0.2271)
    return np.linalg.solve(np.eye(7) - w @ GS, m)


def finite_rank_qeff() -> np.ndarray:
    _, _, _, _, _, gs, w, masses = finite_rank.finite_rank_setup()
    return np.linalg.solve(np.eye(7) - w @ gs, masses)


def a1_baseline(q_eff: np.ndarray, basis: np.ndarray) -> np.ndarray:
    coeff = basis.T @ q_eff
    return basis[:, :2] @ coeff[:2]


def main() -> int:
    print("Support-side A1 center-excess law for the tensor frontier")
    print("=" * 78)

    basis = same.build_adapted_basis()
    e0 = basis[:, 0]
    s = basis[:, 1]
    s_unit = s / np.sqrt(6.0)
    e1 = basis[:, 2]
    e2 = basis[:, 3]
    t1x = basis[:, 4]
    ex = (np.sqrt(3.0) * e1 + e2) / 2.0

    vals_e0 = support_potential(e0)
    vals_s = support_potential(s_unit)
    arm_diff = float(np.max(np.abs(vals_e0[1:] - vals_s[1:])))
    center_excess_diff = float(abs((vals_e0[0] - vals_s[0]) - (1.0 / 6.0)))

    print("Unit-charge A1 endpoint support potentials:")
    print(f"  e0      = {np.array2string(vals_e0, precision=12, floatmode='fixed')}")
    print(f"  s/sqrt6 = {np.array2string(vals_s, precision=12, floatmode='fixed')}")
    print(f"  max arm-site difference = {arm_diff:.3e}")
    print(f"  center-excess residual from 1/6 = {center_excess_diff:.3e}")

    record(
        "the two unit-charge A1 basis backgrounds induce the same arm-site support potential",
        arm_diff < 1e-12,
        f"max arm-site difference = {arm_diff:.3e}",
    )
    record(
        "the exact surviving A1 support datum is the center-excess scalar, with endpoint size 1/6",
        center_excess_diff < 1e-12,
        f"center-excess residual from 1/6 = {center_excess_diff:.3e}",
    )

    max_delta_formula_err = 0.0
    for r in R_TEST:
        q = (e0 + r * s) / (1.0 + np.sqrt(6.0) * r)
        delta = support_delta(q)
        delta_formula = 1.0 / (6.0 * (1.0 + np.sqrt(6.0) * r))
        max_delta_formula_err = max(max_delta_formula_err, abs(delta - delta_formula))
        print(
            f"r={r:.2f}: delta_A1={delta:.12e}, "
            f"formula={delta_formula:.12e}, err={abs(delta-delta_formula):.3e}"
        )

    record(
        "on the canonical Q=1 projective A1 family, the exact support-side scalar is delta_A1(r)=1/(6(1+sqrt(6)r))",
        max_delta_formula_err < 1e-12,
        f"max formula error = {max_delta_formula_err:.3e}",
    )

    gamma_e0 = gamma_pair(e0, ex, t1x)
    gamma_s = gamma_pair(s_unit, ex, t1x)
    delta_e0 = support_delta(e0)
    delta_s = support_delta(s_unit)
    slope_e = (gamma_e0[0] - gamma_s[0]) / (delta_e0 - delta_s)
    intercept_e = gamma_s[0] - slope_e * delta_s
    slope_t = (gamma_e0[1] - gamma_s[1]) / (delta_e0 - delta_s)
    intercept_t = gamma_s[1] - slope_t * delta_s

    print("\nEndpoint tensor coefficients:")
    print(f"  gamma_E(center) = {gamma_e0[0]:+.12e}")
    print(f"  gamma_E(shell)  = {gamma_s[0]:+.12e}")
    print(f"  gamma_T(center) = {gamma_e0[1]:+.12e}")
    print(f"  gamma_T(shell)  = {gamma_s[1]:+.12e}")
    print("\nAffine support law from exact A1 endpoints:")
    print(f"  gamma_E(delta) = {intercept_e:+.12e} + ({slope_e:+.12e}) delta")
    print(f"  gamma_T(delta) = {intercept_t:+.12e} + ({slope_t:+.12e}) delta")

    max_canonical_err_e = 0.0
    max_canonical_err_t = 0.0
    for r in R_TEST:
        q = (e0 + r * s) / (1.0 + np.sqrt(6.0) * r)
        delta = support_delta(q)
        g_e, g_t = gamma_pair(q, ex, t1x)
        pred_e = intercept_e + slope_e * delta
        pred_t = intercept_t + slope_t * delta
        max_canonical_err_e = max(max_canonical_err_e, abs(pred_e - g_e))
        max_canonical_err_t = max(max_canonical_err_t, abs(pred_t - g_t))
        print(
            f"canonical r={r:.2f}: "
            f"gamma_E err={abs(pred_e-g_e):.3e}, gamma_T err={abs(pred_t-g_t):.3e}"
        )

    q_oh = a1_baseline(oh_qeff(), basis)
    q_fr = a1_baseline(finite_rank_qeff(), basis)
    max_family_err_e = 0.0
    max_family_err_t = 0.0
    for label, q in [("exact local O_h", q_oh), ("finite-rank", q_fr)]:
        delta = support_delta(q)
        g_e, g_t = gamma_pair(q, ex, t1x)
        pred_e = intercept_e + slope_e * delta
        pred_t = intercept_t + slope_t * delta
        err_e = abs(pred_e - g_e)
        err_t = abs(pred_t - g_t)
        max_family_err_e = max(max_family_err_e, err_e)
        max_family_err_t = max(max_family_err_t, err_t)
        print(
            f"{label}: delta_A1={delta:.12e}, "
            f"gamma_E err={err_e:.3e}, gamma_T err={err_t:.3e}"
        )

    record(
        "the current bright tensor coefficients are nearly affine in the exact support-side center-excess scalar on the canonical A1 family",
        max_canonical_err_e < 1e-8 and max_canonical_err_t < 2e-8,
        (
            f"max canonical affine-law errors: "
            f"gamma_E={max_canonical_err_e:.3e}, gamma_T={max_canonical_err_t:.3e}"
        ),
        status="BOUNDED",
    )
    record(
        "the same support-side affine law tracks the exact local O_h and finite-rank A1 baselines",
        max_family_err_e < 5e-6 and max_family_err_t < 5e-6,
        (
            f"max audited-family affine-law errors: "
            f"gamma_E={max_family_err_e:.3e}, gamma_T={max_family_err_t:.3e}"
        ),
        status="BOUNDED",
    )

    print("\nVerdict:")
    print(
        "The shell-blindness pivot can now be sharpened again. After fixing total "
        "charge, the exact A1 support block retains one microscopic scalar datum, "
        "the support center-excess delta_A1. The current bright tensor coefficients "
        "are then almost exactly an affine law in that exact support scalar. So the "
        "remaining exact gravity theorem is no longer an arbitrary function of r; it "
        "is the derivation of the exact tensor endpoint coefficients at the two A1 "
        "support endpoints and the exact tensor observable they belong to."
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
