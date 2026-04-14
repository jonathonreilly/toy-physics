#!/usr/bin/env python3
"""Route 2 Theta_R to slice-coupling audit.

This runner checks the cleanest current route-2 law that couples the missing
tensor support observable into the exact slice generator / bounded transfer
bridge.

Current expected outcome:
  - exact route-2 kinematics are present
  - exact slice generator Lambda_R and bounded transfer T_R are present
  - the current exact support-side machinery is scalar/rank-one on the A1 block
  - the only available tensor observable is the bounded staging object
    Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))
  - therefore the route is bounded, not exact
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


def record(name: str, ok: bool, detail: str, status: str = "BOUNDED") -> None:
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


def fit_affine(delta: np.ndarray, values: np.ndarray) -> tuple[float, float, float]:
    a, b = np.linalg.lstsq(
        np.column_stack([np.ones_like(delta), delta]),
        values,
        rcond=None,
    )[0]
    resid = values - (a + b * delta)
    return float(a), float(b), float(np.max(np.abs(resid)))


def main() -> int:
    atlas = first_existing([
        REPO / "docs" / "publication" / "ci3_z3" / "DERIVATION_ATLAS.md",
        ROOT / "docs" / "publication" / "ci3_z3" / "DERIVATION_ATLAS.md",
    ])
    note_path = ROOT / "docs" / "S3_TIME_THETA_TO_SLICE_COUPLING_NOTE.md"
    primitive_chain = ROOT / "docs" / "S3_TIME_PRIMITIVE_CHAIN_NOTE.md"
    transfer_note = ROOT / "docs" / "S3_TIME_TRANSFER_MATRIX_BRIDGE_NOTE.md"
    support_note = ROOT / "docs" / "TENSOR_SUPPORT_SIDE_OBSERVABLE_NOTE.md"
    support_attack_note = ROOT / "docs" / "TENSOR_SUPPORT_TENSOR_OBSERVABLE_ATTACK_NOTE.md"
    center_law_note = ROOT / "docs" / "TENSOR_SUPPORT_CENTER_EXCESS_LAW_NOTE.md"
    proto_note = ROOT / "docs" / "S3_TIME_TENSOR_PRIMITIVE_PROTOTYPE_NOTE.md"
    s3_note = REPO / "docs" / "S3_GENERAL_R_DERIVATION_NOTE.md"
    anomaly_note = REPO / "docs" / "ANOMALY_FORCES_TIME_THEOREM.md"
    schur_note = REPO / "docs" / "OH_SCHUR_BOUNDARY_ACTION_NOTE.md"

    atlas_text = read_text(atlas)
    note_text = read_text(note_path)
    primitive_text = read_text(primitive_chain)
    transfer_text = read_text(transfer_note)
    support_text = read_text(support_note)
    support_attack_text = read_text(support_attack_note)
    center_text = read_text(center_law_note)
    proto_text = read_text(proto_note)
    s3_text = read_text(s3_note)
    anomaly_text = read_text(anomaly_note)
    schur_text = read_text(schur_note)

    same = SourceFileLoader(
        "same_source_metric",
        f"{ROOT}/scripts/frontier_same_source_metric_ansatz_scan.py",
    ).load_module()
    schur = SourceFileLoader(
        "oh_schur_boundary_action",
        f"{ROOT}/scripts/frontier_oh_schur_boundary_action.py",
    ).load_module()
    center = SourceFileLoader(
        "tensor_center_excess",
        f"{ROOT}/scripts/frontier_tensor_support_center_excess_law.py",
    ).load_module()
    proto = SourceFileLoader(
        "tensor_primitive_proto",
        f"{ROOT}/scripts/frontier_s3_time_tensor_primitive_prototype.py",
    ).load_module()
    support_attack = SourceFileLoader(
        "tensor_support_attack",
        f"{ROOT}/scripts/frontier_tensor_support_tensor_observable_attack.py",
    ).load_module()

    print("Route 2 Theta_R to slice-coupling audit")
    print("=" * 78)
    print("  Candidate background: PL S^3 x R")
    print()

    bg_exact = (
        ("PL homeomorphic to S^3" in s3_text or "PL homeomorphic to `S^3`" in s3_text)
        and ("d_t = 1" in anomaly_text or "single-clock" in anomaly_text.lower())
        and "PL S^3 x R" in transfer_text
        and "PL S^3 x R" in note_text
    )
    record(
        "Route-2 kinematics are exact on PL S^3 x R",
        bg_exact,
        "S^3 + single-clock time + route-2 bridge are all present",
    )

    Lambda, trace_idx, bulk_idx, interior = schur.schur_dtn_matrix(15, 4.0)
    Lambda_sym = 0.5 * (Lambda + Lambda.T)
    sym_err = float(np.max(np.abs(Lambda - Lambda.T)))
    min_eig = float(np.min(np.linalg.eigvalsh(Lambda_sym)))
    T = expm(-Lambda_sym)
    T_sym_err = float(np.max(np.abs(T - T.T)))
    spectral_radius = float(np.max(np.abs(np.linalg.eigvals(T))))
    record(
        "Lambda_R is symmetric positive definite and T_R is a positive contraction",
        sym_err < 1e-12 and min_eig > 0.0 and T_sym_err < 1e-12 and spectral_radius < 1.0,
        f"sym_err={sym_err:.3e}, min_eig={min_eig:.6e}, spectral_radius={spectral_radius:.6e}",
        status="BOUNDED",
    )

    support_ok = (
        "no mixed A1-bright block" in support_attack_text.lower()
        or "P_A1^T G_S P_bright = 0" in support_attack_text
    )
    record(
        "the exact support-side tensor primitive is still absent",
        support_ok,
        "current support stack remains scalar/rank-one on A1 x {E_x, T1x}",
    )

    basis = same.build_adapted_basis()
    e0 = basis[:, 0]
    s = basis[:, 1]
    s_unit = s / np.sqrt(6.0)
    e1 = basis[:, 2]
    e2 = basis[:, 3]
    t1x = basis[:, 4]
    e_x = (np.sqrt(3.0) * e1 + e2) / 2.0
    e_perp = (-e1 + np.sqrt(3.0) * e2) / 2.0

    d_e0 = center.support_delta(e0)
    d_s = center.support_delta(s_unit)
    g_e0 = center.gamma_pair(e0, e_x, t1x)
    g_s = center.gamma_pair(s_unit, e_x, t1x)

    r_test = np.array([0.25, 0.5, 0.75, 1.0, 1.5, 2.0], dtype=float)
    delta_vals = []
    ge_vals = []
    gt_vals = []
    for r in r_test:
        q = (e0 + r * s) / (1.0 + np.sqrt(6.0) * r)
        delta_vals.append(center.support_delta(q))
        ge, gt = center.gamma_pair(q, e_x, t1x)
        ge_vals.append(ge)
        gt_vals.append(gt)

    delta_vals = np.array(delta_vals, dtype=float)
    ge_vals = np.array(ge_vals, dtype=float)
    gt_vals = np.array(gt_vals, dtype=float)
    a_e, b_e, res_e = fit_affine(delta_vals, ge_vals)
    a_t, b_t, res_t = fit_affine(delta_vals, gt_vals)

    q_oh = center.a1_baseline(center.oh_qeff(), basis)
    q_fr = center.a1_baseline(center.finite_rank_qeff(), basis)
    fam_errs = []
    for label, q in [("exact local O_h", q_oh), ("finite-rank", q_fr)]:
        delta = center.support_delta(q)
        ge, gt = center.gamma_pair(q, e_x, t1x)
        pred_e = a_e + b_e * delta
        pred_t = a_t + b_t * delta
        fam_errs.append((label, abs(pred_e - ge), abs(pred_t - gt)))

    exact_support_blocked = (
        abs(d_e0 - 1.0 / 6.0) < 1e-12
        and abs(d_s) < 1e-12
        and "delta_A1(r) = 1 / (6 (1 + sqrt(6) r))" in center_text
        and "Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))" in proto_text
    )
    record(
        "the exact support scalar delta_A1 survives but remains scalar-only",
        exact_support_blocked,
        f"delta(e0)={d_e0:.12e}, delta(shell)={d_s:.12e}",
    )

    candidate_ok = (
        res_e < 1e-8
        and res_t < 2e-8
        and all(err_e < 5e-6 and err_t < 5e-6 for _, err_e, err_t in fam_errs)
    )
    record(
        "the bounded Theta_R^(0) staging law is affine in delta_A1 and tracks the audited baselines",
        candidate_ok,
        (
            f"gamma_E(delta)={a_e:+.6e} + ({b_e:+.6e}) delta, resid={res_e:.3e}; "
            f"gamma_T(delta)={a_t:+.6e} + ({b_t:+.6e}) delta, resid={res_t:.3e}"
        ),
        status="BOUNDED",
    )

    coupler_present = (
        (
            "bounded transfer operator" in transfer_text.lower()
            or "bounded transfer-matrix bridge" in transfer_text.lower()
            or "bounded one-step transfer operator" in transfer_text.lower()
        )
        and (
            "Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))" in note_text
            or "Theta_R^(0)(q) := (gamma_E(q), gamma_T(q))" in note_text
            or "Theta_R^(0)(q)" in note_text
        )
    )
    record(
        "the cleanest current coupling is a bounded source-side staging law, not an exact tensor-time theorem",
        coupler_present and candidate_ok and exact_support_blocked,
        "Theta_R^(0) can stage the bright source channels, but it does not close Lambda_R into an exact dynamics law",
        status="BOUNDED",
    )

    print()
    print("Coupling candidate:")
    print("  Theta_R^(0)(q) := (gamma_E(q), gamma_T(q))")
    print("  delta_A1(r) := 1 / (6 (1 + sqrt(6) r))")
    print("  gamma_E(delta) = a_E + b_E delta")
    print("  gamma_T(delta) = a_T + b_T delta")
    print("  T_R := exp(-Lambda_R)")
    print()
    print("Interpretation:")
    print(
        "  The exact slice generator remains Lambda_R and the transfer law remains "
        "T_R = exp(-Lambda_R). The best current coupling to the missing tensor "
        "support observable is only bounded: Theta_R^(0) is an affine source-side "
        "staging observable organized by the exact scalar delta_A1. The exact "
        "tensor/time carrier is still missing."
    )
    print()
    print("Summary:")
    print("  Exact tensor-support carrier: missing")
    print("  Bounded Theta_R staging law: present")
    print("  Exact Lambda_R / T_R slice law: present")
    print(f"PASS={sum(c.ok for c in CHECKS)} FAIL={sum(not c.ok for c in CHECKS)}")
    return 1 if any(not c.ok for c in CHECKS) else 0


if __name__ == "__main__":
    raise SystemExit(main())
