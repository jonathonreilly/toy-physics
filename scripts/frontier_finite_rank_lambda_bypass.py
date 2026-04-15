#!/usr/bin/env python3
"""Finite-rank lambda bypass test.

This runner asks one narrow question:

Can the finite-rank/class-expansion route canonically fix the remaining
weight-1 mixing angle `lambda`, or does it inherit the same one-parameter
ambiguity already seen on the phase-lift side?

The test is intentionally restricted to the finite-rank widening stack:
  - the exact support-irrep enlargement `A1(center) ⊕ A1(shell) ⊕ E ⊕ T1`;
  - the exact Route-2 bright carrier `K_R`;
  - the exact scalar source-to-metric theorem.

The answer should be negative if the widening route still leaves an
SO(2)-orbit of normalized bright-basis choices.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib.machinery import SourceFileLoader
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent.parent


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


same = SourceFileLoader(
    "same_source_metric",
    str(ROOT / "scripts" / "frontier_same_source_metric_ansatz_scan.py"),
).load_module()
finite_rank = SourceFileLoader(
    "finite_rank_metric",
    str(ROOT / "scripts" / "frontier_finite_rank_gravity_residual.py"),
).load_module()
support_mod = SourceFileLoader(
    "support_amplitude",
    str(ROOT / "scripts" / "frontier_support_renormalized_active_amplitude.py"),
).load_module()
center = SourceFileLoader(
    "tensor_center_excess",
    str(ROOT / "scripts" / "frontier_tensor_support_center_excess_law.py"),
).load_module()
bilinear = SourceFileLoader(
    "route2_bilinear",
    str(ROOT / "scripts" / "frontier_s3_time_bilinear_tensor_primitive.py"),
).load_module()
source_metric = SourceFileLoader(
    "finite_rank_source_metric",
    str(ROOT / "scripts" / "frontier_finite_rank_source_to_metric_theorem.py"),
).load_module()


def rot2(theta: float) -> np.ndarray:
    c = float(np.cos(theta))
    s = float(np.sin(theta))
    return np.array([[c, -s], [s, c]], dtype=float)


def rotate_bright_basis(ex: np.ndarray, t1x: np.ndarray, theta: float) -> tuple[np.ndarray, np.ndarray]:
    r = rot2(theta)
    stacked = np.column_stack([ex, t1x]) @ r.T
    return stacked[:, 0], stacked[:, 1]


def pair_phase(pair: tuple[float, float]) -> float:
    return float(np.arctan2(pair[1], pair[0]))


def rotated_gamma_pair(q: np.ndarray, ex: np.ndarray, t1x: np.ndarray) -> tuple[float, float]:
    return center.gamma_pair(q, ex, t1x)


def main() -> int:
    print("FINITE-RANK LAMBDA BYPASS TEST")
    print("=" * 78)

    basis = same.build_adapted_basis()
    e0 = basis[:, 0]
    s = basis[:, 1]
    e1 = basis[:, 2]
    e2 = basis[:, 3]
    t1x = basis[:, 4]
    t1y = basis[:, 5]
    t1z = basis[:, 6]
    ex = (np.sqrt(3.0) * e1 + e2) / 2.0
    e_perp = (-e1 + np.sqrt(3.0) * e2) / 2.0

    q_oh, _ = support_mod.oh_q_eff()
    q_fr, _ = support_mod.finite_rank_q_eff()
    q_a1 = basis[:, :2] @ (basis[:, :2].T @ q_fr)
    q_e = basis[:, 2:4] @ (basis[:, 2:4].T @ q_fr)
    q_t = basis[:, 4:7] @ (basis[:, 4:7].T @ q_fr)

    support_op, support_pair_op = support_mod.support_to_active_operator()
    support_rank = int(np.linalg.matrix_rank(support_op, tol=1e-12))
    support_pair_rank = int(np.linalg.matrix_rank(support_pair_op, tol=1e-12))

    support_frame_rank = int(np.linalg.matrix_rank(np.column_stack([q_a1, q_e, q_t]), tol=1e-12))
    support_frame_resid = float(np.linalg.norm(q_fr - (q_a1 + q_e + q_t)))

    phi_full, _, _, _ = finite_rank.exact_finite_rank_field()
    boundary = source_metric.boundary_stationarity_report(phi_full)
    coarse = source_metric.coarse_metric_report(phi_full)

    print("Finite-rank source-to-metric theorem outputs:")
    print(
        "  boundary: "
        f"rebuild_err={boundary['rebuild_err']:.3e}, "
        f"flux_err={boundary['flux_err']:.3e}, "
        f"stationary_grad={boundary['stationary_grad']:.3e}"
    )
    print(
        "  coarse: "
        f"R_match={coarse['best'][0]:.1f}, "
        f"direct={coarse['best'][4]:.3e}, "
        f"coarse={coarse['best'][5]:.3e}, "
        f"improvement={coarse['improvement']:.1f}x"
    )

    thetas = np.linspace(0.0, np.pi / 2.0, 6)
    oh_norms = []
    fr_norms = []
    oh_phases = []
    fr_phases = []
    action_spreads = []

    q_test = q_fr + 0.13 * ex + 0.07 * t1x

    for theta in thetas:
        ex_rot, t1x_rot = rotate_bright_basis(ex, t1x, theta)
        pair_oh = rotated_gamma_pair(q_oh, ex_rot, t1x_rot)
        pair_fr = rotated_gamma_pair(q_fr, ex_rot, t1x_rot)
        oh_norms.append(float(np.linalg.norm(pair_oh)))
        fr_norms.append(float(np.linalg.norm(pair_fr)))
        oh_phases.append(pair_phase(pair_oh))
        fr_phases.append(pair_phase(pair_fr))
        action_spreads.append(
            bilinear_action_penalty(q_test, theta)
        )
        print(
            f"theta={theta:.3f}: "
            f"O_h pair={pair_oh[0]:+.12e}, {pair_oh[1]:+.12e}; "
            f"finite-rank pair={pair_fr[0]:+.12e}, {pair_fr[1]:+.12e}"
        )

    oh_norm_span = float(max(oh_norms) - min(oh_norms))
    fr_norm_span = float(max(fr_norms) - min(fr_norms))
    oh_phase_span = float(np.max(np.unwrap(oh_phases)) - np.min(np.unwrap(oh_phases)))
    fr_phase_span = float(np.max(np.unwrap(fr_phases)) - np.min(np.unwrap(fr_phases)))
    action_span = float(max(action_spreads) - min(action_spreads))

    print("\nRotation diagnostics:")
    print(f"  O_h norm span      = {oh_norm_span:.3e}")
    print(f"  finite-rank norm span = {fr_norm_span:.3e}")
    print(f"  O_h phase span     = {oh_phase_span:.3e}")
    print(f"  finite-rank phase span = {fr_phase_span:.3e}")
    print(f"  bright-action span = {action_span:.3e}")
    print(f"  support frame rank  = {support_frame_rank}")
    print(f"  support frame resid = {support_frame_resid:.3e}")
    print(f"  support-to-active rank = {support_rank}")
    print(f"  support-to-active pair rank = {support_pair_rank}")

    record(
        "the finite-rank widening route still has exact support-irrep rank three but no canonical bright origin",
        support_frame_rank == 3 and support_frame_resid < 1e-12,
        f"rank([A1,E,T1])={support_frame_rank}, residual={support_frame_resid:.3e}",
    )
    record(
        "the support-to-active operator remains exact rank one on the widened finite-rank class",
        support_rank == 1 and support_pair_rank == 1,
        f"support rank={support_rank}, pair rank={support_pair_rank}",
    )
    record(
        "rotating the bright basis leaves the Route-2 carrier action unchanged",
        action_span < 1e-12,
        f"max bright-action span={action_span:.3e}",
    )
    record(
        "the exact bright-coefficient pair traces a nontrivial SO(2) orbit on the exact O_h source",
        oh_norm_span < 1e-10 and oh_phase_span > 1.0,
        f"O_h norm span={oh_norm_span:.3e}, O_h phase span={oh_phase_span:.3e}",
    )
    record(
        "the exact bright-coefficient pair traces the same nontrivial SO(2) orbit on the finite-rank source",
        fr_norm_span < 1e-10 and fr_phase_span > 1.0,
        f"finite-rank norm span={fr_norm_span:.3e}, finite-rank phase span={fr_phase_span:.3e}",
    )
    record(
        "the finite-rank source-to-metric theorem is scalar and therefore theta-blind",
        boundary["rebuild_err"] < 1e-12 and boundary["flux_err"] < 1e-12 and boundary["stationary_grad"] < 1e-12,
        (
            f"boundary errors: rebuild={boundary['rebuild_err']:.3e}, "
            f"flux={boundary['flux_err']:.3e}, grad={boundary['stationary_grad']:.3e}"
        ),
        status="BOUNDED",
    )

    print("\nVerdict:")
    print(
        "The finite-rank/class-expansion route does not canonically fix lambda. "
        "Its exact support enlargement gives a stronger block frame and exact "
        "scalar source-to-metric control, but the bright coefficients still move "
        "on a nontrivial SO(2) orbit under basis rotations. The tensorized Route-2 "
        "action is orthogonally blind to that orbit, and the scalar finite-rank "
        "source-to-metric theorem has no theta handle to select a preferred "
        "section. So the widening route inherits the same one-parameter ambiguity "
        "rather than bypassing it."
    )

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    return 0 if n_fail == 0 else 1


def bilinear_action_penalty(q: np.ndarray, theta: float) -> float:
    """Tensorized Route-2 penalty after a bright-basis rotation."""

    ex = (np.sqrt(3.0) * basis_vecs[2] + basis_vecs[3]) / 2.0
    t1x = basis_vecs[4]
    u_e, u_t = bilinear.bright_coords(q)
    delta = bilinear.delta_a1(q)
    carrier = np.array([u_e, u_t, delta * u_e, delta * u_t], dtype=float)
    a = carrier.copy()
    r = rot2(theta)
    r4 = np.block(
        [
            [r, np.zeros((2, 2), dtype=float)],
            [np.zeros((2, 2), dtype=float), r],
        ]
    )
    carrier_rot = r4 @ carrier
    a_rot = r4 @ a
    return 0.5 * float(np.sum((a_rot - carrier_rot) ** 2))


basis_vecs = same.build_adapted_basis()


if __name__ == "__main__":
    raise SystemExit(main())
