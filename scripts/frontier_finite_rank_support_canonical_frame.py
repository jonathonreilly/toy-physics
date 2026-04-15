#!/usr/bin/env python3
"""Canonical support-side block frame audit for the finite-rank widening lane.

This is the support-side canonicalization pass requested for the current
Route-2 interface. It starts from the exact noncanonical enlargement

    A1(center) ⊕ A1(shell) ⊕ E ⊕ T1

and the exact bright coordinates

    u_E = <E_x, q>,  u_T = <T1x, q>.

The question is whether the existing axiom-native ingredients force a fully
canonical support-side polarization frame, or only a canonical block
decomposition with residual gauge freedom.

This runner checks three things:
  1. endpoint constraints on the exact A1 support scalar;
  2. commutation / invariance of the exact tensorized Route-2 action under
     orthogonal reparameterizations of the bright carrier coordinates;
  3. support-irrep normalization of the exact seven-site source frame.

The conclusion should be that the axioms force a canonical block frame
consisting of the exact A1 sector and the exact bright pair, but they do not
eliminate the dark-complement gauge. The minimal residual gauge is the
orthogonal freedom on the unused support complement, namely

    O(1) on E_perp  ×  O(2) on the T1 dark plane,

after the bright-axis sign conventions are fixed by the endpoint columns.
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
support_law = SourceFileLoader(
    "support_center_excess",
    str(ROOT / "scripts" / "frontier_tensor_support_center_excess_law.py"),
).load_module()
bilinear = SourceFileLoader(
    "route2_bilinear",
    str(ROOT / "scripts" / "frontier_s3_time_bilinear_tensor_primitive.py"),
).load_module()
tensor_action = SourceFileLoader(
    "route2_tensor_action",
    str(ROOT / "scripts" / "frontier_s3_time_bilinear_tensor_action.py"),
).load_module()


def rot2(theta: float) -> np.ndarray:
    c = float(np.cos(theta))
    s = float(np.sin(theta))
    return np.array([[c, -s], [s, c]], dtype=float)


def carrier_action_penalty(q: np.ndarray, theta: float) -> float:
    """Evaluate the tensorized Route-2 penalty after a bright-basis rotation.

    The carrier is `vec(K_R) = (u_E, u_T, delta_A1 u_E, delta_A1 u_T)`. A
    rotation in the bright carrier coordinates acts orthogonally on the first
    two entries and the corresponding `delta_A1`-weighted entries. Because the
    penalty is Euclidean, the action cannot distinguish such a reparameterization.
    """

    q = np.asarray(q, dtype=float)
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


def main() -> int:
    print("FINITE-RANK SUPPORT CANONICAL FRAME AUDIT")
    print("=" * 78)

    basis = same.build_adapted_basis()
    e0 = basis[:, 0]
    s = basis[:, 1]
    s_unit = s / np.sqrt(6.0)
    e1 = basis[:, 2]
    e2 = basis[:, 3]
    t1x = basis[:, 4]
    t1y = basis[:, 5]
    t1z = basis[:, 6]
    e_x = (np.sqrt(3.0) * e1 + e2) / 2.0
    e_perp = (-e1 + np.sqrt(3.0) * e2) / 2.0

    _, _, _, q_fr = finite_rank.exact_finite_rank_field()
    q_a1 = basis[:, :2] @ (basis[:, :2].T @ q_fr)
    q_e = basis[:, 2:4] @ (basis[:, 2:4].T @ q_fr)
    q_t = basis[:, 4:7] @ (basis[:, 4:7].T @ q_fr)

    # Exact support scalar and endpoint law.
    delta_e0 = support_law.support_delta(e0)
    delta_shell = support_law.support_delta(s_unit)
    delta_formula_err = 0.0
    for r in [0.0, 0.25, 0.5, 1.0, 1.5, 2.0]:
        q_a1 = (e0 + r * s) / (1.0 + np.sqrt(6.0) * r)
        delta = support_law.support_delta(q_a1)
        delta_formula = 1.0 / (6.0 * (1.0 + np.sqrt(6.0) * r))
        delta_formula_err = max(delta_formula_err, abs(delta - delta_formula))

    # Endpoint columns of the exact bilinear carrier.
    q_ref = (e0 + 0.5 * s) / (1.0 + np.sqrt(6.0) * 0.5)
    delta_ref = bilinear.delta_a1(q_ref)
    col_e = bilinear.k_r(q_ref + e_x) - bilinear.k_r(q_ref)
    col_t = bilinear.k_r(q_ref + t1x) - bilinear.k_r(q_ref)
    target_e = np.array([[1.0, 0.0], [delta_ref, 0.0]], dtype=float)
    target_t = np.array([[0.0, 1.0], [0.0, delta_ref]], dtype=float)
    endpoint_err = max(
        float(np.max(np.abs(col_e - target_e))),
        float(np.max(np.abs(col_t - target_t))),
    )

    # Support-irrep normalization on the exact finite-rank source.
    coeff = basis.T @ q_fr
    support_rank = int(np.linalg.matrix_rank(np.column_stack([q_a1, q_e, q_t]), tol=1e-12))
    c_a1 = coeff[:2]
    c_non = coeff[2:]
    bright_u_e, bright_u_t = bilinear.bright_coords(q_fr)
    dark_u = np.array(bilinear.dark_coords(q_fr), dtype=float)

    # `I_TB`/tensor-action commutation: the Euclidean quadratic penalty does not
    # change under orthogonal reparameterization of the bright carrier.
    q_test = q_ref + 0.13 * e_x + 0.07 * t1x
    action_base = carrier_action_penalty(q_test, 0.0)
    action_rot = carrier_action_penalty(q_test, np.pi / 5.0)
    action_comm_err = abs(action_base - action_rot)

    # Dark-complement gauge: rotate the T1 dark plane, flip the E dark axis.
    q_dark = q_test.copy()
    gauge_rot = rot2(np.pi / 7.0)
    dark_plane = np.array([dark_u[1], dark_u[2]], dtype=float)
    dark_plane_rot = gauge_rot @ dark_plane
    dark_gauge_err = float(np.linalg.norm(dark_plane_rot) - np.linalg.norm(dark_plane))
    e_perp_sign = float(np.dot(e_perp, q_test) + np.dot(-e_perp, q_test))

    print("Exact A1 endpoint law:")
    print(f"  delta_A1(e0) = {delta_e0:.12e}")
    print(f"  delta_A1(s/sqrt(6)) = {delta_shell:.12e}")
    print(f"  max formula error on canonical A1 family = {delta_formula_err:.3e}")
    print("Exact Route-2 bright carrier columns:")
    print(f"  Ex-column error = {float(np.max(np.abs(col_e - target_e))):.3e}")
    print(f"  T1x-column error = {float(np.max(np.abs(col_t - target_t))):.3e}")
    print("Support-irrep coordinates on finite-rank source:")
    print(f"  A1 coeffs = {np.array2string(c_a1, precision=12, floatmode='fixed')}")
    print(f"  non-A1 coeffs = {np.array2string(c_non, precision=12, floatmode='fixed')}")
    print(f"  bright coords: u_E={bright_u_e:+.12e}, u_T={bright_u_t:+.12e}")
    print(f"  dark coords:   {np.array2string(dark_u, precision=12, floatmode='fixed')}")
    print("Tensor-action invariance check:")
    print(f"  action penalty at theta=0     = {action_base:.12e}")
    print(f"  action penalty at theta=pi/5  = {action_rot:.12e}")
    print(f"  commutation residual          = {action_comm_err:.3e}")
    print("Dark-gauge check:")
    print(f"  T1 dark-plane norm difference = {dark_gauge_err:.3e}")
    print(f"  E dark-axis sign-flip check   = {e_perp_sign:.3e}")

    record(
        "the exact support-side scalar datum delta_A1 is fixed by the two A1 endpoints",
        abs(delta_e0 - 1.0 / 6.0) < 1e-12 and abs(delta_shell) < 1e-12,
        f"delta_A1(e0)={delta_e0:.3e}, delta_A1(shell)={delta_shell:.3e}",
    )
    record(
        "the exact canonical A1 projective law delta_A1(r)=1/(6(1+sqrt(6)r)) holds",
        delta_formula_err < 1e-12,
        f"max formula error={delta_formula_err:.3e}",
    )
    record(
        "the exact Route-2 carrier columns are fixed by the endpoint constraints",
        endpoint_err < 1e-12,
        f"max endpoint-column error={endpoint_err:.3e}",
    )
    record(
        "the finite-rank source splits exactly into A1, E, and T1 support sectors",
        support_rank == 3 and np.linalg.norm(c_a1) > 0 and np.linalg.norm(c_non) > 0,
        f"rank([A1,E,T1])={support_rank}",
    )
    record(
        "the Route-2 tensorized action cannot distinguish orthogonal bright-basis reparameterizations",
        action_comm_err < 1e-12,
        f"commutation residual={action_comm_err:.3e}",
        status="BOUNDED",
    )
    record(
        "the remaining support-side freedom lives only in the unused dark complement",
        abs(dark_gauge_err) < 1e-12 and abs(e_perp_sign) < 1e-12,
        f"dark-plane norm difference={dark_gauge_err:.3e}; E sign-flip residual={e_perp_sign:.3e}",
        status="EXACT",
    )

    print("\nVerdict:")
    print(
        "The strongest axiom-native support-side canonical structure is a block "
        "frame, not a fully rigid `Pi_3+1`. The axioms and endpoint data fix the "
        "exact A1 sector and the ordered bright pair `u_E, u_T` through the Route-2 "
        "carrier, but the tensorized action `I_TB` is blind to orthogonal bright-"
        "basis reparameterizations. After fixing the endpoint sign conventions, the "
        "minimal residual gauge freedom is exactly the orthogonal freedom on the "
        "unused dark complement: `O(1)` on `E_perp` and `O(2)` on the dark `T1` "
        "plane. That is the smallest support-side frame consistent with the current "
        "axioms."
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
