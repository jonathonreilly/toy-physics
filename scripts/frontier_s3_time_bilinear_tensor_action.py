#!/usr/bin/env python3
r"""Route-2 tensorized action/coupling definition from a bilinear carrier.

With the bilinear carrier definition

    K_R(q) = [[u_E(q),           u_T(q)],
              [delta_A1(q)u_E(q), delta_A1(q)u_T(q)]],

the minimal Route-2 tensor extension of the scalar Schur backbone is the
definition

    I_TB(f, a ; j) = I_R(f ; j) + 1/2 ||a - K_R(q)||^2

and the corresponding spacetime carrier on PL S^3 x R is

    Xi_TB(t ; q) = vec(K_R(q)) \otimes exp(-t Lambda_R) u_*.

This still does not identify the carrier with full Einstein dynamics. It does
not derive the upstream inputs; it only verifies that the definition is
algebraically coherent under those named inputs.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.linalg import expm

from _frontier_loader import load_frontier

TIMES = [0.0, 0.5, 1.0, 2.0]


same = load_frontier("same_source_metric", "frontier_same_source_metric_ansatz_scan.py")
schur = load_frontier("oh_schur_boundary_action", "frontier_oh_schur_boundary_action.py")
bilinear = load_frontier(
    "s3_time_bilinear_tensor_primitive",
    "frontier_s3_time_bilinear_tensor_primitive.py",
)


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


def vec_k(q: np.ndarray) -> np.ndarray:
    return bilinear.vec_k(q)


def xi_tb(theta: np.ndarray, seed_t: np.ndarray) -> np.ndarray:
    return np.outer(theta, seed_t)


def main() -> int:
    print("Route 2 tensorized action definition from bilinear carrier")
    print("=" * 78)

    basis = same.build_adapted_basis()
    e0 = basis[:, 0]
    s = basis[:, 1]
    e1 = basis[:, 2]
    e2 = basis[:, 3]
    t1x = basis[:, 4]
    e_x = (np.sqrt(3.0) * e1 + e2) / 2.0

    q_center = e0 + e_x
    q_shell = (s / np.sqrt(6.0)) + t1x
    theta_center = vec_k(q_center)
    theta_shell = vec_k(q_shell)

    Lambda, _, _, _ = schur.schur_dtn_matrix(15, 4.0)
    Lambda_sym = 0.5 * (Lambda + Lambda.T)
    sym_err = float(np.max(np.abs(Lambda - Lambda.T)))
    eigvals = np.linalg.eigvalsh(Lambda_sym)
    min_eig = float(np.min(eigvals))

    u_star = np.ones(Lambda_sym.shape[0], dtype=float)
    u_star /= np.linalg.norm(u_star)

    def seed_t(t: float) -> np.ndarray:
        return expm(-t * Lambda_sym) @ u_star

    xi_center = [xi_tb(theta_center, seed_t(t)) for t in TIMES]
    xi_shell = [xi_tb(theta_shell, seed_t(t)) for t in TIMES]
    semigroup_err = float(
        np.max(
            np.abs(
                seed_t(1.0)
                - expm(-0.5 * Lambda_sym) @ (expm(-0.5 * Lambda_sym) @ u_star)
            )
        )
    )

    print("Bilinear support carrier endpoints:")
    print(f"  vec K_R(e0 + E_x)        = {np.array2string(theta_center, precision=12, floatmode='fixed')}")
    print(f"  vec K_R(s/sqrt(6) + T1x) = {np.array2string(theta_shell, precision=12, floatmode='fixed')}")
    print()
    print(f"Lambda_R symmetry error = {sym_err:.3e}")
    print(f"Lambda_R minimum eigenvalue = {min_eig:.12e}")
    for t, xi in zip(TIMES, xi_center):
        print(f"  ||Xi_TB({t:.1f}; e0+E_x)|| = {float(np.linalg.norm(xi)):.12e}")
    for t, xi in zip(TIMES, xi_shell):
        print(f"  ||Xi_TB({t:.1f}; s/sqrt(6)+T1x)|| = {float(np.linalg.norm(xi)):.12e}")

    record(
        "the Route-2 tensor extension has a finite bilinear carrier definition",
        np.all(np.isfinite(theta_center)) and np.all(np.isfinite(theta_shell)),
        f"endpoint carrier norms={np.linalg.norm(theta_center):.3e}, {np.linalg.norm(theta_shell):.3e}",
    )
    record(
        "the named scalar Schur input supplies a symmetric positive slice generator",
        sym_err < 1e-12 and min_eig > 0.0,
        f"symmetry error={sym_err:.3e}, min eigenvalue={min_eig:.6e}",
    )
    record(
        "the spacetime carrier Xi_TB contracts under the named Route-2 semigroup",
        np.linalg.norm(xi_center[1]) < np.linalg.norm(xi_center[0])
        and np.linalg.norm(xi_center[2]) < np.linalg.norm(xi_center[1])
        and np.linalg.norm(xi_shell[1]) < np.linalg.norm(xi_shell[0])
        and np.linalg.norm(xi_shell[2]) < np.linalg.norm(xi_shell[1])
        and semigroup_err < 1e-12,
        f"semigroup composition error={semigroup_err:.3e}",
    )
    record(
        "the remaining Route-2 GR blocker is the upstream-input and Einstein-dynamics bridge",
        True,
        "K_R, I_TB, and Xi_TB are definitions under named inputs; matching them to the Einstein/Regge tensor law is still open",
        status="BLOCKED",
    )

    print("\nVerdict:")
    print(
        "Route 2 has a definition-only bilinear carrier K_R, tensorized Schur "
        "construction, and spacetime carrier Xi_TB on PL S^3 x R. The remaining "
        "blocker is the upstream-input closure and final identification of this "
        "carrier/action with the Einstein/Regge tensor dynamics law on the "
        "current restricted class."
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
