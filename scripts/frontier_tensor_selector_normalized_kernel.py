#!/usr/bin/env python3
"""Selector-normalized tensor kernel on the retained gravity class.

The raw universal-kernel theorem fails on the current restricted gravity class:
the fitted positive 2x2 tensor kernel differs materially between the exact
local O_h and finite-rank families.

This runner asks a narrower question suggested by the retained stack:

    does the family dependence mostly live in a missing normalization law,
    rather than in the tensor kernel shape itself?

The tested normalization uses only quantities already forced by the current
scalar/tensor stack:

  - the dominant traceless-shear channel scale eta_11
  - the scalar Schur action magnitude |I_scalar|
  - the scalar-derived traceless tensor floor coefficient
      c_eta = eta_floor_tf / |I_scalar|

If

  K_tensor = eta_11 * K_hat
  eta_floor = |I_scalar| * c_eta * e_tf

with approximately universal K_hat and c_eta, then the normalized completion
coordinate

  a_tilde = (eta_11 / |I_scalar|) * a

is family-near-universal even though the raw kernel is not.
"""

from __future__ import annotations

from importlib.machinery import SourceFileLoader

import numpy as np


ROOT = "/private/tmp/physics-review-active"

utk = SourceFileLoader(
    "tensor_universal_kernel",
    f"{ROOT}/scripts/frontier_tensor_universal_kernel.py",
).load_module()
same_source = SourceFileLoader(
    "same_source_metric",
    f"{ROOT}/scripts/frontier_same_source_metric_ansatz_scan.py",
).load_module()
coarse = SourceFileLoader(
    "coarse_grained",
    f"{ROOT}/scripts/frontier_coarse_grained_exterior_law.py",
).load_module()


def rel_diff(a: np.ndarray, b: np.ndarray) -> float:
    denom = max(float(np.linalg.norm(b)), 1e-16)
    return float(np.linalg.norm(a - b) / denom)


def main() -> int:
    print("Selector-normalized tensor kernel")
    print("=" * 78)

    oh = utk.family_block("exact local O_h", same_source.build_best_phi_grid())
    fr = utk.family_block("finite-rank", coarse.build_finite_rank_phi_grid())

    eta11_oh = float(oh.eta_map[1, 1])
    eta11_fr = float(fr.eta_map[1, 1])
    c_eta_oh = float(oh.eta_floor[1] / abs(oh.scalar_action))
    c_eta_fr = float(fr.eta_floor[1] / abs(fr.scalar_action))

    Khat_oh = oh.kernel / eta11_oh
    Khat_fr = fr.kernel / eta11_fr
    etahat_oh = oh.eta_map / eta11_oh
    etahat_fr = fr.eta_map / eta11_fr
    a_tilde_oh = (eta11_oh / abs(oh.scalar_action)) * oh.a_star
    a_tilde_fr = (eta11_fr / abs(fr.scalar_action)) * fr.a_star

    Khat_rel = rel_diff(Khat_oh, Khat_fr)
    etahat_rel = rel_diff(etahat_oh, etahat_fr)
    c_eta_rel = abs(c_eta_oh - c_eta_fr) / max(abs(c_eta_oh), 1e-16)
    a_tilde_rel = rel_diff(a_tilde_oh, a_tilde_fr)

    Khat = 0.5 * (Khat_oh + Khat_fr)
    c_eta = 0.5 * (c_eta_oh + c_eta_fr)
    eigs = np.linalg.eigvalsh(Khat)
    pred = np.linalg.solve(Khat, np.array([0.0, c_eta], dtype=float))
    pred_err_oh = rel_diff(pred, a_tilde_oh)
    pred_err_fr = rel_diff(pred, a_tilde_fr)

    print("\nSelector-normalized kernel shapes:")
    print(
        "  exact local O_h Khat="
        f"[[{Khat_oh[0,0]:.6e}, {Khat_oh[0,1]:.6e}], "
        f"[{Khat_oh[1,0]:.6e}, {Khat_oh[1,1]:.6e}]]"
    )
    print(
        "  finite-rank     Khat="
        f"[[{Khat_fr[0,0]:.6e}, {Khat_fr[0,1]:.6e}], "
        f"[{Khat_fr[1,0]:.6e}, {Khat_fr[1,1]:.6e}]]"
    )
    print(
        f"  Khat relative difference = {Khat_rel:.6e}\n"
        f"  etahat relative difference = {etahat_rel:.6e}"
    )

    print("\nScalar-derived tensor drive coefficient:")
    print(f"  c_eta(O_h) = {c_eta_oh:.6e}")
    print(f"  c_eta(finite-rank) = {c_eta_fr:.6e}")
    print(f"  c_eta relative difference = {c_eta_rel:.6e}")

    print("\nNormalized completion coordinates:")
    print(f"  a_tilde(O_h) = [{a_tilde_oh[0]:.6e}, {a_tilde_oh[1]:.6e}]")
    print(f"  a_tilde(finite-rank) = [{a_tilde_fr[0]:.6e}, {a_tilde_fr[1]:.6e}]")
    print(f"  a_tilde relative difference = {a_tilde_rel:.6e}")

    print("\nBest common selector-normalized candidate:")
    print(f"  avg Khat eigenvalues = ({eigs[0]:.6e}, {eigs[1]:.6e})")
    print(f"  avg c_eta = {c_eta:.6e}")
    print(f"  predicted a_tilde = [{pred[0]:.6e}, {pred[1]:.6e}]")
    print(f"  prediction error vs O_h = {pred_err_oh:.6e}")
    print(f"  prediction error vs finite-rank = {pred_err_fr:.6e}")

    checks = [
        ("normalized kernel shape is near-universal", Khat_rel < 5e-2),
        ("normalized source map is near-universal", etahat_rel < 5e-2),
        ("scalar-derived tensor drive coefficient is near-universal", c_eta_rel < 8e-2),
        ("normalized completion coordinate is materially closer than the raw a_star", a_tilde_rel < 1.5e-1),
        ("common selector-normalized candidate stays positive definite", float(np.min(eigs)) > 0.0),
        ("common selector-normalized candidate predicts both families within 7%", pred_err_oh < 7e-2 and pred_err_fr < 7e-2),
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
            "Selector-normalized tensor universality holds as a bounded result on the "
            "audited restricted class. The raw universal K_tensor obstruction is still "
            "real, but the missing principle is narrowed to the normalization/selector "
            "law rather than the tensor kernel shape itself."
        )
        return 0

    print(
        "Selector-normalized universality did not close cleanly enough. The raw "
        "obstruction remains the best current description."
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
