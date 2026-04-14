#!/usr/bin/env python3
"""Route 2 tensor endpoint theorem: exact support endpoints, blocked tensor lift.

This runner makes the route-2 split explicit:
  1. the support-side endpoint coefficients of delta_A1 are exact
  2. the first tensor primitive endpoint coefficients are still bounded
  3. the exact tensor endpoint theorem is blocked because the current stack
     lacks an exact tensor-valued observable on A1 x {E_x, T1x}

The goal is to localize the blocker cleanly, not to inflate the current
bounded tensor prototype into an exact theorem.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib.machinery import SourceFileLoader

import numpy as np


ROOT = "/private/tmp/physics-review-active"

center_law = SourceFileLoader(
    "tensor_support_center_excess_law",
    f"{ROOT}/scripts/frontier_tensor_support_center_excess_law.py",
).load_module()
proto = SourceFileLoader(
    "tensor_primitive_prototype",
    f"{ROOT}/scripts/frontier_s3_time_tensor_primitive_prototype.py",
).load_module()
blind = SourceFileLoader(
    "tensor_a1_shell_projective_blindness",
    f"{ROOT}/scripts/frontier_tensor_a1_shell_projective_blindness.py",
).load_module()
same_source = SourceFileLoader(
    "same_source_metric",
    f"{ROOT}/scripts/frontier_same_source_metric_ansatz_scan.py",
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


def main() -> int:
    print("Route 2 tensor endpoint coefficients")
    print("=" * 78)

    basis = same_source.build_adapted_basis()
    e0 = basis[:, 0]
    s = basis[:, 1]
    s_unit = s / np.sqrt(6.0)
    e_x = (np.sqrt(3.0) * basis[:, 2] + basis[:, 3]) / 2.0
    t1x = basis[:, 4]

    delta_e0 = center_law.support_delta(e0)
    delta_s = center_law.support_delta(s_unit)
    delta_formula = lambda r: 1.0 / (6.0 * (1.0 + np.sqrt(6.0) * r))

    print("Exact support endpoints:")
    print(f"  delta_A1(e0)        = {delta_e0:.12e}")
    print(f"  delta_A1(s/sqrt(6)) = {delta_s:.12e}")

    record(
        "the exact support-side endpoint coefficients are e0=1/6 and s/sqrt(6)=0",
        abs(delta_e0 - 1.0 / 6.0) < 1e-12 and abs(delta_s) < 1e-12,
        f"delta_A1(e0)={delta_e0:.12e}, delta_A1(s/sqrt(6))={delta_s:.12e}",
    )

    max_formula_err = 0.0
    for r in [0.25, 0.5, 0.75, 1.0, 1.5, 2.0]:
        q = (e0 + r * s) / (1.0 + np.sqrt(6.0) * r)
        delta = center_law.support_delta(q)
        err = abs(delta - delta_formula(r))
        max_formula_err = max(max_formula_err, err)
        print(f"  r={r:.2f}: delta_A1={delta:.12e}, formula={delta_formula(r):.12e}, err={err:.3e}")

    record(
        "the exact projective A1 support law is delta_A1(r)=1/(6(1+sqrt(6)r))",
        max_formula_err < 1e-12,
        f"max formula error = {max_formula_err:.3e}",
    )

    theta_e0 = center_law.gamma_pair(e0, e_x, t1x)
    theta_s = center_law.gamma_pair(s_unit, e_x, t1x)
    print("\nBounded tensor primitive endpoint data:")
    print(f"  Theta_R^(0)(e0)        = ({theta_e0[0]:+.12e}, {theta_e0[1]:+.12e})")
    print(f"  Theta_R^(0)(s/sqrt(6)) = ({theta_s[0]:+.12e}, {theta_s[1]:+.12e})")

    # The current shell/junction stack is exact but projectively blind to r.
    # Verify the blindness statement on the support-side observables.
    u_diff, sigma_diff = blind.band_max_diff(
        blind.bridge_fields(e0)[0], blind.bridge_fields(s_unit)[0]
    ), blind.band_max_diff(
        blind.bridge_fields(e0)[1], blind.bridge_fields(s_unit)[1]
    )
    record(
        "the exact shell/junction stack is projectively blind to the A1 ratio r on the sewing band",
        u_diff < 1e-12 and sigma_diff < 1e-12,
        f"u/Q diff={u_diff:.3e}, sigma/Q diff={sigma_diff:.3e}",
    )

    record(
        "the current tensor endpoint coefficients remain bounded prototype data",
        np.isfinite(theta_e0[0]) and np.isfinite(theta_e0[1]) and np.isfinite(theta_s[0]) and np.isfinite(theta_s[1]),
        f"Theta_R^(0)(e0)=({theta_e0[0]:+.3e}, {theta_e0[1]:+.3e}), "
        f"Theta_R^(0)(s/sqrt(6))=({theta_s[0]:+.3e}, {theta_s[1]:+.3e})",
        status="BOUNDED",
    )

    record(
        "the exact tensor endpoint theorem is still blocked",
        True,
        "the current stack still lacks an exact tensor-valued observable on A1 x {E_x, T1x}",
        status="BLOCKED",
    )

    print("\nVerdict:")
    print(
        "The support-side endpoint theorem is exact: delta_A1(e0)=1/6 and "
        "delta_A1(s/sqrt(6))=0. The first Route-2 tensor primitive only has a "
        "bounded endpoint prototype, because the exact shell/junction stack is "
        "projectively blind to r and the tensor lift is still numerical."
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
