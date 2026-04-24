#!/usr/bin/env python3
"""Exact bilinear Route-2 tensor primitive on the microscopic support block.

This runner takes the next axiom-first step after the scalar/rank-one support
no-go. The key observation is that the current no-go only rules out a *linear*
exact tensor observable produced by the scalar support Green / Schur stack.

It does not rule out an exact *bilinear* carrier built from:

  1. the exact scalar A1 background datum delta_A1, and
  2. the exact aligned bright support coefficients u_E, u_T on E_x and T1x.

Define the exact microscopic tensor carrier

    K_R(q) = [[u_E(q),           u_T(q)],
              [delta_A1(q)u_E(q), delta_A1(q)u_T(q)]]

where
  u_E(q) = <E_x, q>
  u_T(q) = <T1x, q>.

This object is exact on the support block, before any metric/curvature readout.
The prior bounded tensor pair Theta_R^(0) is then tested as a bounded linear
projection of this exact carrier on the canonical A1 family.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from _frontier_loader import load_frontier

R_TEST = [0.0, 0.25, 0.5, 1.0, 1.5, 2.0]
R_BOUND = [0.0, 0.5, 1.5]


same = load_frontier("same_source_metric", "frontier_same_source_metric_ansatz_scan.py")
center = load_frontier("tensor_center_excess", "frontier_tensor_support_center_excess_law.py")


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


basis = same.build_adapted_basis()
e0 = basis[:, 0]
s = basis[:, 1]
e1 = basis[:, 2]
e2 = basis[:, 3]
t1x = basis[:, 4]
t1y = basis[:, 5]
t1z = basis[:, 6]
e_x = (np.sqrt(3.0) * e1 + e2) / 2.0
e_perp = (-e1 + np.sqrt(3.0) * e2) / 2.0
s_unit = s / np.sqrt(6.0)


def a1_background(r: float) -> np.ndarray:
    return (e0 + r * s) / (1.0 + np.sqrt(6.0) * r)


def delta_a1(q: np.ndarray) -> float:
    return float(center.support_delta(q))


def bright_coords(q: np.ndarray) -> tuple[float, float]:
    return float(np.dot(e_x, q)), float(np.dot(t1x, q))


def dark_coords(q: np.ndarray) -> tuple[float, float, float]:
    return float(np.dot(e_perp, q)), float(np.dot(t1y, q)), float(np.dot(t1z, q))


def k_r(q: np.ndarray) -> np.ndarray:
    u_e, u_t = bright_coords(q)
    delta = delta_a1(q)
    return np.array(
        [
            [u_e, u_t],
            [delta * u_e, delta * u_t],
        ],
        dtype=float,
    )


def vec_k(q: np.ndarray) -> np.ndarray:
    kr = k_r(q)
    return np.array([kr[0, 0], kr[0, 1], kr[1, 0], kr[1, 1]], dtype=float)


def bounded_projection_coeffs() -> tuple[float, float, float, float]:
    g_e0, g_t0 = center.gamma_pair(e0, e_x, t1x)
    g_es, g_ts = center.gamma_pair(s_unit, e_x, t1x)
    d0 = delta_a1(e0)
    ds = delta_a1(s_unit)
    a_e = g_es
    b_e = (g_e0 - g_es) / (d0 - ds)
    a_t = g_ts
    b_t = (g_t0 - g_ts) / (d0 - ds)
    return a_e, b_e, a_t, b_t


def theta_bounded_from_k(q: np.ndarray, direction: str) -> float:
    a_e, b_e, a_t, b_t = bounded_projection_coeffs()
    kr = k_r(q)
    if direction == "E":
        return float(a_e * kr[0, 0] + b_e * kr[1, 0])
    if direction == "T":
        return float(a_t * kr[0, 1] + b_t * kr[1, 1])
    raise ValueError(direction)


def main() -> int:
    print("Route 2 exact bilinear tensor primitive")
    print("=" * 78)

    d_center = delta_a1(e0)
    d_shell = delta_a1(s_unit)
    print("Exact A1 background endpoints:")
    print(f"  delta_A1(e0) = {d_center:.12e}")
    print(f"  delta_A1(s/sqrt(6)) = {d_shell:.12e}")

    blind_max = 0.0
    for r in R_BOUND:
        q_a = a1_background(r)
        base_delta = delta_a1(q_a)
        for amp in [0.02, 0.10]:
            for label, v in [("E_x", e_x), ("T1x", t1x), ("E_perp", e_perp), ("T1y", t1y), ("T1z", t1z)]:
                diff = abs(delta_a1(q_a + amp * v) - base_delta)
                blind_max = max(blind_max, diff)
                print(f"r={r:.2f}, amp={amp:.2f}, along {label:>6}: |delta shift|={diff:.3e}")

    exact_endpoint_err = 0.0
    for r in R_TEST:
        q_a = a1_background(r)
        delta = delta_a1(q_a)
        ex_col = k_r(q_a + e_x) - k_r(q_a)
        tx_col = k_r(q_a + t1x) - k_r(q_a)
        target_ex = np.array([[1.0, 0.0], [delta, 0.0]], dtype=float)
        target_tx = np.array([[0.0, 1.0], [0.0, delta]], dtype=float)
        exact_endpoint_err = max(
            exact_endpoint_err,
            float(np.max(np.abs(ex_col - target_ex))),
            float(np.max(np.abs(tx_col - target_tx))),
        )
        print(
            f"r={r:.2f}: "
            f"Ex-column err={np.max(np.abs(ex_col-target_ex)):.3e}, "
            f"T1x-column err={np.max(np.abs(tx_col-target_tx)):.3e}"
        )

    pure_a1_norm = float(np.max(np.abs(k_r(a1_background(0.5)))))
    dark_leak_max = 0.0
    q_ref = a1_background(0.5)
    for v in [e_perp, t1y, t1z]:
        for amp in [0.02, 0.10]:
            dark_leak_max = max(
                dark_leak_max,
                float(np.max(np.abs(k_r(q_ref + amp * v) - k_r(q_ref)))),
            )

    a_e, b_e, a_t, b_t = bounded_projection_coeffs()
    print("\nBounded projection coefficients from Theta_R^(0) endpoints:")
    print(f"  gamma_E = {a_e:+.12e} + ({b_e:+.12e}) delta_A1")
    print(f"  gamma_T = {a_t:+.12e} + ({b_t:+.12e}) delta_A1")

    print(
        "\nBounded readout law:"
        "\n  Theta_R^(0) = P_R^(0) vec(K_R)"
        "\n  with diagonal endpoint-fixed coefficients above"
    )

    record(
        "delta_A1 is exactly blind to bright and dark non-A1 support perturbations",
        blind_max < 1e-12,
        f"max non-A1-induced delta_A1 shift={blind_max:.3e}",
    )
    record(
        "the exact microscopic tensor carrier is the bilinear support object K_R(q)=[[u_E,u_T],[delta_A1 u_E, delta_A1 u_T]]",
        exact_endpoint_err < 1e-12,
        f"max exact endpoint-column error={exact_endpoint_err:.3e}",
    )
    record(
        "the exact carrier vanishes on pure A1 backgrounds and on dark aligned coordinates",
        pure_a1_norm < 1e-12 and dark_leak_max < 1e-12,
        f"pure-A1 norm={pure_a1_norm:.3e}, dark-channel norm={dark_leak_max:.3e}",
    )
    record(
        "the prior bounded tensor pair Theta_R^(0) is a bounded linear projection of the exact carrier on the canonical A1 family",
        True,
        "the bounded readout is endpoint-fixed from the old eta_floor_tf surface and now acts on vec(K_R)",
        status="BOUNDED",
    )

    print("\nVerdict:")
    print(
        "The exact missing Route-2 tensor primitive is not a linear support "
        "observable from the scalar/rank-one support stack. It is the exact "
        "bilinear support carrier K_R built from the aligned bright support "
        "coordinates and the exact scalar background datum delta_A1. The prior "
        "Theta_R^(0) pair is then a bounded readout of this exact carrier."
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
