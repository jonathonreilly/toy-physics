#!/usr/bin/env python3
"""Local two-channel Jacobian and background-normalization gap.

This runner sharpens the remaining gravity frontier on the current restricted
class by working directly at the scalar `A1` baselines of the two audited
families:

  - exact local O_h
  - finite-rank

It asks two questions:

1. What is the exact local support-side response law of the tensor boundary
   drive `eta_floor_tf` around those scalar baselines?
2. Does the retained reduced-shell amplitude law already fix the two bright
   coefficients, or is one last background-normalization law still missing?

Exact/bounded split:
  - Exact structure:
      the local Jacobian is two-channel in the aligned directions `E_x` and
      `T1x`; dark directions `E_perp`, `T1y`, `T1z` vanish to numerical
      precision under centered differentiation.
  - Bounded structure:
      the bright coefficients are stable across a small epsilon window and
      become materially closer after normalization by the retained anisotropic
      shell amplitude `A_aniso = c_aniso * Q`, but do not become exact.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib.machinery import SourceFileLoader

import numpy as np


ROOT = "/private/tmp/physics-review-active"
EPS_LIST = [0.0025, 0.005, 0.01]

same = SourceFileLoader(
    "same_source_metric",
    f"{ROOT}/scripts/frontier_same_source_metric_ansatz_scan.py",
).load_module()
finite_rank = SourceFileLoader(
    "finite_rank_metric",
    f"{ROOT}/scripts/frontier_finite_rank_gravity_residual.py",
).load_module()
two = SourceFileLoader(
    "tensor_two_channel",
    f"{ROOT}/scripts/frontier_tensor_boundary_drive_two_channel.py",
).load_module()
shell = SourceFileLoader(
    "one_parameter_shell",
    f"{ROOT}/scripts/frontier_one_parameter_reduced_shell_law.py",
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


def eta_floor(q: np.ndarray) -> float:
    return float(two.tensor_metrics(two.phi_from_q(q))[0])


def oh_qeff() -> np.ndarray:
    h0, interior = same.build_neg_laplacian_sparse(15)
    center = interior // 2
    support = [
        same.flat_idx(center + v[0], center + v[1], center + v[2], interior)
        for v in same.SUPPORT_COORDS
    ]
    g0p = same.solve_columns(h0, support)
    gs = g0p[support, :]
    w = same.build_commutant_operator(0.0698, 0.0499, -0.0070, 0.0642, 0.1056)
    m = same.build_invariant_source(0.8247, 0.2271)
    return np.linalg.solve(np.eye(7) - w @ gs, m)


def finite_rank_qeff() -> np.ndarray:
    _, _, _, _, _, gs, w, masses = finite_rank.finite_rank_setup()
    return np.linalg.solve(np.eye(7) - w @ gs, masses)


def a1_baseline(q_eff: np.ndarray) -> np.ndarray:
    basis = same.build_adapted_basis()
    coeff = basis.T @ q_eff
    return basis[:, :2] @ coeff[:2]


def bright_dark_directions() -> dict[str, np.ndarray]:
    basis = same.build_adapted_basis()
    e1 = basis[:, 2]
    e2 = basis[:, 3]
    return {
        "E_x": (np.sqrt(3.0) * e1 + e2) / 2.0,
        "E_perp": (-e1 + np.sqrt(3.0) * e2) / 2.0,
        "T1x": basis[:, 4],
        "T1y": basis[:, 5],
        "T1z": basis[:, 6],
    }


def centered_derivative(q0: np.ndarray, direction: np.ndarray, eps: float) -> float:
    return float((eta_floor(q0 + eps * direction) - eta_floor(q0 - eps * direction)) / (2.0 * eps))


def family_report(label: str, q0: np.ndarray) -> dict[str, object]:
    directions = bright_dark_directions()
    derivs: dict[str, list[float]] = {name: [] for name in directions}
    for eps in EPS_LIST:
        for name, vec in directions.items():
            derivs[name].append(centered_derivative(q0, vec, eps))

    phi_grid = two.phi_from_q(q0)
    red = shell.reduced_data(phi_grid)
    q_total = float(np.sum(q0))
    c_aniso = float(red["anchor_per_Q"])
    a_aniso = q_total * c_aniso

    out = {
        "label": label,
        "Q": q_total,
        "c_aniso": c_aniso,
        "A_aniso": a_aniso,
        "derivs": derivs,
        "beta_E_x": float(np.mean(derivs["E_x"])),
        "beta_T1x": float(np.mean(derivs["T1x"])),
        "dark_max": float(
            max(
                max(abs(x) for x in derivs["E_perp"]),
                max(abs(x) for x in derivs["T1y"]),
                max(abs(x) for x in derivs["T1z"]),
            )
        ),
        "Ex_stability": float(max(abs(x - np.mean(derivs["E_x"])) for x in derivs["E_x"])),
        "T1x_stability": float(max(abs(x - np.mean(derivs["T1x"])) for x in derivs["T1x"])),
    }
    return out


def rel(a: float, b: float) -> float:
    return abs(a - b) / max(abs(a), 1e-16)


def main() -> int:
    print("Local two-channel Jacobian and background-normalization gap")
    print("=" * 78)

    oh = family_report("exact local O_h A1 baseline", a1_baseline(oh_qeff()))
    fr = family_report("finite-rank A1 baseline", a1_baseline(finite_rank_qeff()))

    for fam in [oh, fr]:
        print(f"\n{fam['label']}:")
        print(f"  Q = {fam['Q']:.12e}")
        print(f"  c_aniso = {fam['c_aniso']:.15f}")
        print(f"  A_aniso = {fam['A_aniso']:.12e}")
        for eps, bex, bep, btx, bty, btz in zip(
            EPS_LIST,
            fam["derivs"]["E_x"],
            fam["derivs"]["E_perp"],
            fam["derivs"]["T1x"],
            fam["derivs"]["T1y"],
            fam["derivs"]["T1z"],
        ):
            print(
                f"  eps={eps:.4f}: "
                f"beta(E_x)={bex:+.12e}, beta(E_perp)={bep:+.12e}, "
                f"beta(T1x)={btx:+.12e}, beta(T1y)={bty:+.12e}, beta(T1z)={btz:+.12e}"
            )
        print(
            f"  mean bright coefficients: beta_E_x={fam['beta_E_x']:+.12e}, "
            f"beta_T1x={fam['beta_T1x']:+.12e}"
        )
        print(
            f"  coefficient stability: "
            f"E_x={fam['Ex_stability']:.3e}, T1x={fam['T1x_stability']:.3e}"
        )

    raw_ex_rel = rel(oh["beta_E_x"], fr["beta_E_x"])
    raw_t_rel = rel(oh["beta_T1x"], fr["beta_T1x"])

    gamma_ex_oh = oh["beta_E_x"] / oh["A_aniso"]
    gamma_ex_fr = fr["beta_E_x"] / fr["A_aniso"]
    gamma_t_oh = oh["beta_T1x"] / oh["A_aniso"]
    gamma_t_fr = fr["beta_T1x"] / fr["A_aniso"]
    gamma_ex_rel = rel(gamma_ex_oh, gamma_ex_fr)
    gamma_t_rel = rel(gamma_t_oh, gamma_t_fr)

    print("\nCross-family comparison:")
    print(f"  raw beta_E_x relative difference = {raw_ex_rel:.6e}")
    print(f"  raw beta_T1x relative difference = {raw_t_rel:.6e}")
    print(f"  A_aniso-normalized gamma_E relative difference = {gamma_ex_rel:.6e}")
    print(f"  A_aniso-normalized gamma_T relative difference = {gamma_t_rel:.6e}")
    print(f"  gamma_E(O_h) = {gamma_ex_oh:+.12e}")
    print(f"  gamma_E(finite-rank) = {gamma_ex_fr:+.12e}")
    print(f"  gamma_T(O_h) = {gamma_t_oh:+.12e}")
    print(f"  gamma_T(finite-rank) = {gamma_t_fr:+.12e}")

    record(
        "the local tensor-boundary-drive Jacobian is two-channel on the exact local O_h A1 baseline",
        oh["dark_max"] < 1e-10,
        f"max dark coefficient magnitude = {oh['dark_max']:.3e}",
    )
    record(
        "the local tensor-boundary-drive Jacobian is two-channel on the finite-rank A1 baseline",
        fr["dark_max"] < 1e-10,
        f"max dark coefficient magnitude = {fr['dark_max']:.3e}",
    )
    record(
        "the bright Jacobian coefficients are stable across the audited epsilon window on the exact local O_h baseline",
        oh["Ex_stability"] < 1e-10 and oh["T1x_stability"] < 1e-10,
        f"E_x stability={oh['Ex_stability']:.3e}, T1x stability={oh['T1x_stability']:.3e}",
        status="BOUNDED",
    )
    record(
        "the bright Jacobian coefficients are stable across the audited epsilon window on the finite-rank baseline",
        fr["Ex_stability"] < 1e-10 and fr["T1x_stability"] < 1e-10,
        f"E_x stability={fr['Ex_stability']:.3e}, T1x stability={fr['T1x_stability']:.3e}",
        status="BOUNDED",
    )
    record(
        "the retained reduced-shell amplitude A_aniso materially narrows the cross-family mismatch of the bright coefficients",
        gamma_ex_rel < raw_ex_rel and gamma_t_rel < raw_t_rel,
        (
            f"raw (E_x,T1x)=({raw_ex_rel:.3e}, {raw_t_rel:.3e}), "
            f"normalized=({gamma_ex_rel:.3e}, {gamma_t_rel:.3e})"
        ),
        status="BOUNDED",
    )
    record(
        "the retained shell toolbox still does not determine the bright coefficients exactly across the two audited A1 baselines",
        gamma_ex_rel > 5e-2 or gamma_t_rel > 5e-2,
        (
            f"A_aniso-normalized mismatch: gamma_E={gamma_ex_rel:.3e}, "
            f"gamma_T={gamma_t_rel:.3e}"
        ),
    )

    print("\nVerdict:")
    print(
        "The remaining full-GR gap is not channel selection anymore. The local "
        "tensor-boundary-drive law is exactly two-channel around both audited "
        "scalar A1 baselines, but the retained shell toolbox does not yet fix "
        "the two bright coefficients exactly. After the exact shell amplitude "
        "normalization is factored out, one last A1-background renormalization "
        "law is still missing."
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
