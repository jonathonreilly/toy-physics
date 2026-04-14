#!/usr/bin/env python3
"""Route 2 exact endpoint-coefficient audit.

This runner isolates the strongest exact theorem currently available on
Route 2:

    delta_A1(e0) = 1/6
    delta_A1(s / sqrt(6)) = 0
    delta_A1(r) = 1 / (6 (1 + sqrt(6) r))

It then checks the bounded prototype ladder

    Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))

to show that the tensor endpoint coefficients are still bounded prototype
data, not exact theorem data. The exact blocker is the missing tensor-valued
support observable on A1 x {E_x, T1x}.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib.machinery import SourceFileLoader

import numpy as np


ROOT = "/private/tmp/physics-review-active"
R_TEST = [0.25, 0.5, 0.75, 1.0, 1.5, 2.0]


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
    f"{ROOT}/scripts/frontier_same_source_metric_ansatz_scan.py",
).load_module()
center = SourceFileLoader(
    "tensor_center_excess",
    f"{ROOT}/scripts/frontier_tensor_support_center_excess_law.py",
).load_module()
def main() -> int:
    print("Route 2 exact endpoint coefficients")
    print("=" * 78)

    basis = same.build_adapted_basis()
    e0 = basis[:, 0]
    s = basis[:, 1]
    s_unit = s / np.sqrt(6.0)
    e1 = basis[:, 2]
    e2 = basis[:, 3]
    t1x = basis[:, 4]
    e_x = (np.sqrt(3.0) * e1 + e2) / 2.0

    delta_e0 = center.support_delta(e0)
    delta_s = center.support_delta(s_unit)
    delta_formula = lambda r: 1.0 / (6.0 * (1.0 + np.sqrt(6.0) * r))

    print("Exact support-side endpoint coefficients:")
    print(f"  delta_A1(e0)        = {delta_e0:.12e}")
    print(f"  delta_A1(s/sqrt(6)) = {delta_s:.12e}")

    exact_scalar = abs(delta_e0 - 1.0 / 6.0) < 1e-12 and abs(delta_s) < 1e-12
    record(
        "the exact support-side endpoint coefficients are e0=1/6 and s/sqrt(6)=0",
        exact_scalar,
        f"delta_A1(e0)={delta_e0:.12e}, delta_A1(s/sqrt(6))={delta_s:.12e}",
    )

    max_formula_err = 0.0
    for r in R_TEST:
        q = (e0 + r * s) / (1.0 + np.sqrt(6.0) * r)
        delta = center.support_delta(q)
        err = abs(delta - delta_formula(r))
        max_formula_err = max(max_formula_err, err)
        print(
            f"  r={r:.2f}: delta_A1={delta:.12e}, "
            f"formula={delta_formula(r):.12e}, err={err:.3e}"
        )

    record(
        "the exact projective A1 support law is delta_A1(r)=1/(6(1+sqrt(6)r))",
        max_formula_err < 1e-12,
        f"max formula error = {max_formula_err:.3e}",
    )

    theta_e0 = np.array(center.gamma_pair(e0, e_x, t1x), dtype=float)
    theta_s = np.array(center.gamma_pair(s_unit, e_x, t1x), dtype=float)
    xi = (theta_e0 - theta_s) / (delta_e0 - delta_s)
    theta_shell = theta_s.copy()

    print("\nBounded tensor prototype endpoint data:")
    print(f"  Theta_R^(0)(e0)        = ({theta_e0[0]:+.12e}, {theta_e0[1]:+.12e})")
    print(f"  Theta_R^(0)(s/sqrt(6)) = ({theta_s[0]:+.12e}, {theta_s[1]:+.12e})")
    print(f"  Xi_R^(0)               = ({xi[0]:+.12e}, {xi[1]:+.12e})")

    max_canon_e = 0.0
    max_canon_t = 0.0
    for r in R_TEST:
        q = (e0 + r * s) / (1.0 + np.sqrt(6.0) * r)
        delta = center.support_delta(q)
        theta = np.array(center.gamma_pair(q, e_x, t1x), dtype=float)
        pred = theta_shell + xi * delta
        max_canon_e = max(max_canon_e, abs(pred[0] - theta[0]))
        max_canon_t = max(max_canon_t, abs(pred[1] - theta[1]))
        print(
            f"  canonical r={r:.2f}: delta={delta:.12e}, "
            f"Theta err=({abs(pred[0]-theta[0]):.3e}, {abs(pred[1]-theta[1]):.3e})"
        )

    q_oh = center.a1_baseline(center.oh_qeff(), basis)
    q_fr = center.a1_baseline(center.finite_rank_qeff(), basis)
    max_family_e = 0.0
    max_family_t = 0.0
    for label, q in [("exact local O_h", q_oh), ("finite-rank", q_fr)]:
        delta = center.support_delta(q)
        theta = np.array(center.gamma_pair(q, e_x, t1x), dtype=float)
        pred = theta_shell + xi * delta
        err_e = abs(pred[0] - theta[0])
        err_t = abs(pred[1] - theta[1])
        max_family_e = max(max_family_e, err_e)
        max_family_t = max(max_family_t, err_t)
        print(
            f"  {label}: delta={delta:.12e}, "
            f"Theta err=({err_e:.3e}, {err_t:.3e})"
        )

    exact_support_blocked = abs(delta_e0 - 1.0 / 6.0) < 1e-12 and abs(delta_s) < 1e-12
    record(
        "the exact support-side endpoint theorem is complete",
        exact_support_blocked,
        "exact scalar endpoint coefficients and projective law are closed",
    )
    record(
        "the exact tensor endpoint theorem is still blocked",
        False,
        "the current exact support machinery is scalar/rank-one and does not produce an exact tensor-valued observable on A1 x {E_x, T1x}",
        status="BLOCKED",
    )

    record(
        "the bounded prototype ladder reconstructs the canonical A1 family",
        max_canon_e < 1e-8 and max_canon_t < 2e-8,
        f"max canonical errors: gamma_E={max_canon_e:.3e}, gamma_T={max_canon_t:.3e}",
        status="BOUNDED",
    )
    record(
        "the bounded prototype ladder tracks the audited exact-local and finite-rank A1 baselines",
        max_family_e < 5e-6 and max_family_t < 5e-6,
        f"max audited-family errors: gamma_E={max_family_e:.3e}, gamma_T={max_family_t:.3e}",
        status="BOUNDED",
    )

    print("\nVerdict:")
    print(
        "The strongest exact endpoint theorem on Route 2 is the scalar support "
        "law delta_A1(e0)=1/6, delta_A1(s/sqrt(6))=0, "
        "delta_A1(r)=1/(6(1+sqrt(6)r)). The tensor endpoint coefficients of "
        "Theta_R^(0) remain bounded prototype data because the current exact "
        "support stack is scalar/rank-one and cannot yet produce an exact "
        "tensor-valued observable on A1 x {E_x, T1x}."
    )

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    return 1 if any(c.status == "BLOCKED" for c in CHECKS) else 0


if __name__ == "__main__":
    raise SystemExit(main())
