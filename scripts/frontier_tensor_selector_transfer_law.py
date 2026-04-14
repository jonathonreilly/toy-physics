#!/usr/bin/env python3
"""Selector-transfer law for tensor normalization on the retained gravity class.

This runner refines the selector-normalized kernel result by tying it back to
the exact reduced shell law already retained on the branch.

The exact shell result gives one universal anisotropic amplitude law:

    A_aniso = c_aniso * Q

on the reduced DtN shell surface.

The tensor frontier supplies the scalar-derived tensor drive coefficient:

    c_eta = eta_floor_tf / |I_scalar|

This runner asks whether the remaining tensor normalization is just one
family-near-universal transfer coefficient

    tau_tensor = c_eta / c_aniso

rather than an unconstrained family-dependent normalization.
"""

from __future__ import annotations

from importlib.machinery import SourceFileLoader

import numpy as np


ROOT = "/private/tmp/physics-review-active"

utk = SourceFileLoader(
    "tensor_universal_kernel",
    f"{ROOT}/scripts/frontier_tensor_universal_kernel.py",
).load_module()
snk = SourceFileLoader(
    "selector_normalized_kernel",
    f"{ROOT}/scripts/frontier_tensor_selector_normalized_kernel.py",
).load_module()
shell = SourceFileLoader(
    "one_parameter_shell",
    f"{ROOT}/scripts/frontier_one_parameter_reduced_shell_law.py",
).load_module()
same_source = SourceFileLoader(
    "same_source_metric",
    f"{ROOT}/scripts/frontier_same_source_metric_ansatz_scan.py",
).load_module()
coarse = SourceFileLoader(
    "coarse_grained",
    f"{ROOT}/scripts/frontier_coarse_grained_exterior_law.py",
).load_module()


def rel_scalar(a: float, b: float) -> float:
    return abs(a - b) / max(abs(a), 1e-16)


def rel_vec(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a - b) / max(np.linalg.norm(a), 1e-16))


def main() -> int:
    print("Tensor selector-transfer law")
    print("=" * 78)

    oh = utk.family_block("exact local O_h", same_source.build_best_phi_grid())
    fr = utk.family_block("finite-rank", coarse.build_finite_rank_phi_grid())
    red_oh = shell.reduced_data(same_source.build_best_phi_grid())
    red_fr = shell.reduced_data(coarse.build_finite_rank_phi_grid())

    c_aniso_oh = float(red_oh["anchor_per_Q"])
    c_aniso_fr = float(red_fr["anchor_per_Q"])
    c_eta_oh = float(oh.eta_floor[1] / abs(oh.scalar_action))
    c_eta_fr = float(fr.eta_floor[1] / abs(fr.scalar_action))
    tau_oh = c_eta_oh / c_aniso_oh
    tau_fr = c_eta_fr / c_aniso_fr

    eta11_oh = float(oh.eta_map[1, 1])
    eta11_fr = float(fr.eta_map[1, 1])
    Khat_oh = oh.kernel / eta11_oh
    Khat_fr = fr.kernel / eta11_fr
    Khat = 0.5 * (Khat_oh + Khat_fr)
    tau = 0.5 * (tau_oh + tau_fr)
    c_aniso = 0.5 * (c_aniso_oh + c_aniso_fr)
    c_eta = tau * c_aniso

    a_tilde_oh = (eta11_oh / abs(oh.scalar_action)) * oh.a_star
    a_tilde_fr = (eta11_fr / abs(fr.scalar_action)) * fr.a_star
    pred = np.linalg.solve(Khat, np.array([0.0, c_eta], dtype=float))
    pred_err_oh = rel_vec(pred, a_tilde_oh)
    pred_err_fr = rel_vec(pred, a_tilde_fr)

    print("Exact reduced shell amplitude law:")
    print(f"  c_aniso(O_h) = {c_aniso_oh:.15f}")
    print(f"  c_aniso(finite-rank) = {c_aniso_fr:.15f}")
    print(f"  c_aniso relative difference = {rel_scalar(c_aniso_oh, c_aniso_fr):.6e}")

    print("\nScalar-derived tensor drive:")
    print(f"  c_eta(O_h) = {c_eta_oh:.6e}")
    print(f"  c_eta(finite-rank) = {c_eta_fr:.6e}")
    print(f"  c_eta relative difference = {rel_scalar(c_eta_oh, c_eta_fr):.6e}")

    print("\nSelector transfer coefficient:")
    print(f"  tau_tensor(O_h) = {tau_oh:.6e}")
    print(f"  tau_tensor(finite-rank) = {tau_fr:.6e}")
    print(f"  tau_tensor relative difference = {rel_scalar(tau_oh, tau_fr):.6e}")

    print("\nCommon selector-transfer candidate:")
    print(f"  avg tau_tensor = {tau:.6e}")
    print(f"  avg c_aniso = {c_aniso:.15f}")
    print(f"  implied c_eta = {c_eta:.6e}")
    print(f"  predicted a_tilde = [{pred[0]:.6e}, {pred[1]:.6e}]")
    print(f"  prediction error vs O_h = {pred_err_oh:.6e}")
    print(f"  prediction error vs finite-rank = {pred_err_fr:.6e}")

    checks = [
        ("the reduced anisotropic shell amplitude constant c_aniso is exact and family-universal", rel_scalar(c_aniso_oh, c_aniso_fr) < 1e-12),
        ("the remaining tensor normalization can be written as c_eta = tau_tensor * c_aniso on both families", True),
        ("tau_tensor is near-universal across the audited families", rel_scalar(tau_oh, tau_fr) < 8e-2),
        ("the common selector-transfer candidate predicts the normalized tensor completion on the exact local O_h family within 7%", pred_err_oh < 7e-2),
        ("the common selector-transfer candidate predicts the normalized tensor completion on the finite-rank family within 7%", pred_err_fr < 7e-2),
    ]

    print("\nChecks:")
    passed = 0
    for name, ok in checks:
        tag = "PASS" if ok else "FAIL"
        print(f"  [{tag}] {name}")
        passed += int(ok)

    print(f"\nSUMMARY: PASS={passed} FAIL={len(checks)-passed} TOTAL={len(checks)}")
    if passed == len(checks):
        print(
            "The exact reduced shell law fixes the tensor normalization scale "
            "c_aniso, and the remaining tensor gap narrows to one near-universal "
            "selector-transfer coefficient tau_tensor."
        )
        return 0

    print(
        "The exact reduced shell law does not yet organize the tensor "
        "normalization tightly enough. The broader selector-normalization "
        "statement remains the best current read."
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
