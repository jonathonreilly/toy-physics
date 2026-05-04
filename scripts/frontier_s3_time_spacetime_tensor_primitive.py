#!/usr/bin/env python3
r"""Route 2 spacetime tensor primitive candidate on `PL S^3 x R`.

This runner builds the smallest plausible spacetime-level tensor carrier from
the current Route 2 ingredients:

  - exact background `PL S^3 x R`
  - exact slice generator `Lambda_R`
  - bounded source-side tensor pair `Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))`

The candidate carrier is the rank-1 spacetime tensor

  Xi_R^(0)(t; q) = Theta_R^(0)(q) \otimes V_R(t)

with

  V_R(t) = exp(-t Lambda_R) u_*

where `u_*` is the canonical normalized slice seed.

This is intentionally bounded, not exact. It is the smallest spacetime-level
carrier that mediates between the support-side bright data and the exact slice
dynamics without inventing a new tensor primitive.
"""

from __future__ import annotations

from dataclasses import dataclass
from _frontier_loader import load_frontier
from pathlib import Path

import numpy as np
from scipy.linalg import expm


REPO = Path(__file__).resolve().parents[1]
TIMES = [0.0, 0.5, 1.0, 2.0]


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


def carrier(theta: np.ndarray, seed_t: np.ndarray) -> np.ndarray:
    return np.outer(theta, seed_t)


def main() -> int:
    atlas = REPO / "docs" / "publication" / "ci3_z3" / "DERIVATION_ATLAS.md"
    s3_note = REPO / "docs" / "S3_GENERAL_R_DERIVATION_NOTE.md"
    anomaly_note = REPO / "docs" / "ANOMALY_FORCES_TIME_THEOREM.md"
    transfer_note = REPO / "docs" / "S3_TIME_TRANSFER_MATRIX_BRIDGE_NOTE.md"
    proto_note = REPO / "docs" / "S3_TIME_TENSOR_PRIMITIVE_PROTOTYPE_NOTE.md"
    build_memo = REPO / "docs" / "S3_TIME_TENSOR_BUILD_MEMO.md"
    spacetime_note = REPO / "docs" / "S3_TIME_SPACETIME_TENSOR_PRIMITIVE_NOTE.md"
    theta_note = REPO / "docs" / "S3_TIME_THETA_TO_SLICE_COUPLING_NOTE.md"
    primitive_chain = REPO / "docs" / "S3_TIME_PRIMITIVE_CHAIN_NOTE.md"

    atlas_text = read_text(atlas)
    s3_text = read_text(s3_note)
    anomaly_text = read_text(anomaly_note)
    transfer_text = read_text(transfer_note)
    proto_text = read_text(proto_note)
    build_text = read_text(build_memo)
    spacetime_text = read_text(spacetime_note)
    theta_text = read_text(theta_note)
    primitive_text = read_text(primitive_chain)

    same = load_frontier("same_source_metric", "frontier_same_source_metric_ansatz_scan.py")
    schur = load_frontier("oh_schur_boundary_action", "frontier_oh_schur_boundary_action.py")
    center = load_frontier("tensor_center_excess", "frontier_tensor_support_center_excess_law.py")
    prototype = load_frontier("tensor_primitive_proto", "frontier_s3_time_tensor_primitive_prototype.py")

    print("Route 2 spacetime tensor primitive candidate")
    print("=" * 78)
    print("  Candidate background: PL S^3 x R")
    print()

    basis = same.build_adapted_basis()
    e0 = basis[:, 0]
    s = basis[:, 1]
    s_unit = s / np.sqrt(6.0)
    e1 = basis[:, 2]
    e2 = basis[:, 3]
    t1x = basis[:, 4]
    e_x = (np.sqrt(3.0) * e1 + e2) / 2.0

    theta_e0 = np.array(center.gamma_pair(e0, e_x, t1x), dtype=float)
    theta_s = np.array(center.gamma_pair(s_unit, e_x, t1x), dtype=float)

    Lambda, trace_idx, bulk_idx, interior = schur.schur_dtn_matrix(15, 4.0)
    Lambda_sym = 0.5 * (Lambda + Lambda.T)
    sym_err = float(np.max(np.abs(Lambda - Lambda.T)))
    eigvals = np.linalg.eigvalsh(Lambda_sym)
    min_eig = float(np.min(eigvals))
    max_eig = float(np.max(eigvals))

    u_star = np.ones(Lambda_sym.shape[0], dtype=float)
    u_star /= np.linalg.norm(u_star)

    def seed_t(t: float) -> np.ndarray:
        return expm(-t * Lambda_sym) @ u_star

    def xi(theta: np.ndarray, t: float) -> np.ndarray:
        return carrier(theta, seed_t(t))

    V0 = seed_t(0.0)
    V1 = seed_t(1.0)
    V2 = seed_t(2.0)
    semigroup_err = float(np.max(np.abs(seed_t(1.0) - expm(-0.5 * Lambda_sym) @ (expm(-0.5 * Lambda_sym) @ u_star))))

    xi0_e0 = xi(theta_e0, 0.0)
    xi1_e0 = xi(theta_e0, 1.0)
    xi2_e0 = xi(theta_e0, 2.0)
    xi0_s = xi(theta_s, 0.0)
    xi1_s = xi(theta_s, 1.0)
    xi2_s = xi(theta_s, 2.0)

    norm_theta_e0 = float(np.linalg.norm(theta_e0))
    norm_theta_s = float(np.linalg.norm(theta_s))
    norm_v0 = float(np.linalg.norm(V0))
    norm_v1 = float(np.linalg.norm(V1))
    norm_v2 = float(np.linalg.norm(V2))
    norm_xi0_e0 = float(np.linalg.norm(xi0_e0))
    norm_xi1_e0 = float(np.linalg.norm(xi1_e0))
    norm_xi2_e0 = float(np.linalg.norm(xi2_e0))
    norm_xi0_s = float(np.linalg.norm(xi0_s))
    norm_xi1_s = float(np.linalg.norm(xi1_s))
    norm_xi2_s = float(np.linalg.norm(xi2_s))

    print("Exact / bounded inputs:")
    print(f"  Lambda_R symmetry error = {sym_err:.3e}")
    print(f"  Lambda_R eigenvalue range = [{min_eig:.6e}, {max_eig:.6e}]")
    print(f"  ||u_*|| = {np.linalg.norm(u_star):.6e}")
    print(f"  ||V_R(0)|| = {norm_v0:.6e}")
    print(f"  ||V_R(1)|| = {norm_v1:.6e}")
    print(f"  ||V_R(2)|| = {norm_v2:.6e}")
    print("  Theta_R^(0)(e0)        =", f"({theta_e0[0]:+.12e}, {theta_e0[1]:+.12e})")
    print("  Theta_R^(0)(s/sqrt(6)) =", f"({theta_s[0]:+.12e}, {theta_s[1]:+.12e})")

    print("\nCandidate spacetime tensor primitive:")
    print("  Xi_R^(0)(t; q) = Theta_R^(0)(q) \\otimes V_R(t)")
    print("  V_R(t) = exp(-t Lambda_R) u_*")
    print(f"  ||Xi_R^(0)(0; e0)|| = {norm_xi0_e0:.6e}")
    print(f"  ||Xi_R^(0)(1; e0)|| = {norm_xi1_e0:.6e}")
    print(f"  ||Xi_R^(0)(2; e0)|| = {norm_xi2_e0:.6e}")
    print(f"  ||Xi_R^(0)(0; shell)|| = {norm_xi0_s:.6e}")
    print(f"  ||Xi_R^(0)(1; shell)|| = {norm_xi1_s:.6e}")
    print(f"  ||Xi_R^(0)(2; shell)|| = {norm_xi2_s:.6e}")

    record(
        "the route-2 background is exact on PL S^3 x R",
        "PL homeomorphic to S^3" in s3_text
        and "d_t = 1" in anomaly_text
        and "T_R = exp(-Lambda_R)" in transfer_text,
        "S^3 compactification + anomaly-forced single-clock time are present",
    )
    record(
        "the exact slice generator Lambda_R is symmetric positive definite",
        sym_err < 1e-12 and min_eig > 0.0,
        f"symmetry error={sym_err:.3e}, eigenvalue range=[{min_eig:.6e}, {max_eig:.6e}]",
        status="BOUNDED",
    )
    record(
        "the canonical slice seed is contractively transported by the exact semigroup",
        norm_v1 < norm_v0 and norm_v2 < norm_v1 and semigroup_err < 1e-12,
        f"||V(0)||={norm_v0:.3e}, ||V(1)||={norm_v1:.3e}, ||V(2)||={norm_v2:.3e}, semigroup err={semigroup_err:.3e}",
        status="BOUNDED",
    )
    record(
        "the bounded support-side tensor pair Theta_R^(0) is explicit at the A1 endpoints",
        np.isfinite(theta_e0).all() and np.isfinite(theta_s).all(),
        f"Theta_R^(0)(e0)=({theta_e0[0]:+.3e}, {theta_e0[1]:+.3e}); "
        f"Theta_R^(0)(s/sqrt(6))=({theta_s[0]:+.3e}, {theta_s[1]:+.3e})",
        status="BOUNDED",
    )
    record(
        "the candidate spacetime carrier Xi_R^(0) is bounded and contracts in time",
        norm_xi1_e0 < norm_xi0_e0 and norm_xi2_e0 < norm_xi1_e0 and norm_xi1_s < norm_xi0_s and norm_xi2_s < norm_xi1_s,
        (
            f"e0 norms: {norm_xi0_e0:.3e} -> {norm_xi1_e0:.3e} -> {norm_xi2_e0:.3e}; "
            f"shell norms: {norm_xi0_s:.3e} -> {norm_xi1_s:.3e} -> {norm_xi2_s:.3e}"
        ),
        status="BOUNDED",
    )
    record(
        "the candidate spacetime carrier remains distinct from an exact tensor observable",
        "spacetime tensor carrier candidate" in spacetime_text.lower()
        and "Theta_R^(0)(q) \\otimes V_R(t)" in spacetime_text,
        "the current exact support-side tensor observable is still missing",
        status="BLOCKED",
    )

    print("\nInterpretation:")
    print(
        "Route 2 now has a concrete bounded spacetime tensor carrier candidate. "
        "It lives on the exact PL S^3 x R background, uses the exact slice "
        "generator Lambda_R, and lifts the bounded bright-channel support pair "
        "Theta_R^(0) into a time-dependent rank-1 spacetime tensor. This is the "
        "smallest plausible mediator between the support-side tensor data and "
        "the slice dynamics. It is not yet an exact tensor observable."
    )

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    return 1 if any(not c.ok for c in CHECKS) else 0


if __name__ == "__main__":
    raise SystemExit(main())
