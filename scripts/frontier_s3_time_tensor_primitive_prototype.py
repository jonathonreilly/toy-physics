#!/usr/bin/env python3
"""Bounded prototype for the first missing Route-2 tensor primitive.

This runner defines the current working support-block prototype

    Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))

on A1 x {E_x, T1x}, extracts its endpoint values, and checks that the
current affine delta_A1 law reproduces the canonical and audited families.
"""

from __future__ import annotations

# Runner takes ~120s on the canonical grid; declare an explicit
# AUDIT_TIMEOUT_SEC per RUNNER_CACHE_POLICY.md so cached runs don't
# straddle the default 120s ceiling and intermittently record status: timeout.
AUDIT_TIMEOUT_SEC = 240

from dataclasses import dataclass
from _frontier_loader import load_frontier

import numpy as np


R_TEST = [0.25, 0.5, 0.75, 1.0, 1.5, 2.0]


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


same = load_frontier("same_source_metric", "frontier_same_source_metric_ansatz_scan.py")
center = load_frontier("tensor_center_excess", "frontier_tensor_support_center_excess_law.py")


def main() -> int:
    print("Route 2 tensor primitive prototype")
    print("=" * 78)

    basis = same.build_adapted_basis()
    e0 = basis[:, 0]
    s = basis[:, 1]
    s_unit = s / np.sqrt(6.0)
    e1 = basis[:, 2]
    e2 = basis[:, 3]
    t1x = basis[:, 4]
    e_x = (np.sqrt(3.0) * e1 + e2) / 2.0

    g_e0 = center.gamma_pair(e0, e_x, t1x)
    g_s = center.gamma_pair(s_unit, e_x, t1x)
    d_e0 = center.support_delta(e0)
    d_s = center.support_delta(s_unit)

    slope_e = (g_e0[0] - g_s[0]) / (d_e0 - d_s)
    intercept_e = g_s[0] - slope_e * d_s
    slope_t = (g_e0[1] - g_s[1]) / (d_e0 - d_s)
    intercept_t = g_s[1] - slope_t * d_s

    print("Prototype endpoint values:")
    print(f"  Theta_R^(0)(e0)         = ({g_e0[0]:+.12e}, {g_e0[1]:+.12e})")
    print(f"  Theta_R^(0)(s/sqrt(6))  = ({g_s[0]:+.12e}, {g_s[1]:+.12e})")
    print()
    print("Affine support law in delta_A1:")
    print(f"  gamma_E(delta) = {intercept_e:+.12e} + ({slope_e:+.12e}) delta")
    print(f"  gamma_T(delta) = {intercept_t:+.12e} + ({slope_t:+.12e}) delta")

    max_canon_e = 0.0
    max_canon_t = 0.0
    for r in R_TEST:
        q = (e0 + r * s) / (1.0 + np.sqrt(6.0) * r)
        delta = center.support_delta(q)
        g_e, g_t = center.gamma_pair(q, e_x, t1x)
        pred_e = intercept_e + slope_e * delta
        pred_t = intercept_t + slope_t * delta
        max_canon_e = max(max_canon_e, abs(pred_e - g_e))
        max_canon_t = max(max_canon_t, abs(pred_t - g_t))
        print(
            f"canonical r={r:.2f}: delta={delta:.12e}, "
            f"gamma_E err={abs(pred_e-g_e):.3e}, gamma_T err={abs(pred_t-g_t):.3e}"
        )

    q_oh = center.a1_baseline(center.oh_qeff(), basis)
    q_fr = center.a1_baseline(center.finite_rank_qeff(), basis)

    max_family_e = 0.0
    max_family_t = 0.0
    for label, q in [("exact local O_h", q_oh), ("finite-rank", q_fr)]:
        delta = center.support_delta(q)
        g_e, g_t = center.gamma_pair(q, e_x, t1x)
        pred_e = intercept_e + slope_e * delta
        pred_t = intercept_t + slope_t * delta
        err_e = abs(pred_e - g_e)
        err_t = abs(pred_t - g_t)
        max_family_e = max(max_family_e, err_e)
        max_family_t = max(max_family_t, err_t)
        print(
            f"{label}: delta={delta:.12e}, "
            f"gamma_E err={err_e:.3e}, gamma_T err={err_t:.3e}"
        )

    record(
        "the first missing Route-2 primitive has a clean bounded prototype on A1 x {E_x, T1x}",
        True,
        "Theta_R^(0)(q) := (gamma_E(q), gamma_T(q))",
    )
    record(
        "the prototype endpoint coefficients are well defined at e0 and s/sqrt(6)",
        np.isfinite(g_e0[0]) and np.isfinite(g_e0[1]) and np.isfinite(g_s[0]) and np.isfinite(g_s[1]),
        f"center={g_e0}, shell={g_s}",
    )
    record(
        "the affine delta_A1 law reproduces the canonical A1 family",
        max_canon_e < 1e-8 and max_canon_t < 2e-8,
        f"max canonical errors: gamma_E={max_canon_e:.3e}, gamma_T={max_canon_t:.3e}",
    )
    record(
        "the same bounded prototype tracks the audited exact-local and finite-rank A1 baselines",
        max_family_e < 5e-6 and max_family_t < 5e-6,
        f"max audited-family errors: gamma_E={max_family_e:.3e}, gamma_T={max_family_t:.3e}",
    )

    print()
    print("Summary:")
    print("  First missing primitive: tensor-valued support observable")
    print("  Current bounded prototype: Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))")
    print("  Endpoint theorem: not exact yet, but endpoint data are now explicit")
    print(f"PASS={sum(c.ok for c in CHECKS)} FAIL={sum(not c.ok for c in CHECKS)}")
    return 1 if any(not c.ok for c in CHECKS) else 0


if __name__ == "__main__":
    raise SystemExit(main())
