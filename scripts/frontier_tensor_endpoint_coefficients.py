#!/usr/bin/env python3
"""Tensor endpoint coefficients: exact support law plus blocked tensor lift.

This runner makes the split explicit:
  1. the support-side endpoint coefficients of delta_A1 are exact
  2. the tensor-channel endpoint coefficients are still numerical because the
     exact tensor observable on A1 x {E_x, T1x} is missing

The goal is to localize the blocker cleanly, not to inflate the current
support-side result into a full tensor theorem.
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
    print("Tensor endpoint coefficients")
    print("=" * 72)

    basis = same_source.build_adapted_basis()
    e0 = basis[:, 0]
    s = basis[:, 1]
    s_unit = s / np.sqrt(6.0)

    delta_e0 = center_law.support_delta(e0)
    delta_s = center_law.support_delta(s_unit)
    print(f"Exact support endpoints: delta_A1(e0)={delta_e0:.12e}, delta_A1(s/sqrt(6))={delta_s:.12e}")

    record(
        "the support-side endpoint coefficients are exact",
        abs(delta_e0 - 1.0 / 6.0) < 1e-12 and abs(delta_s) < 1e-12,
        f"delta_A1(e0)={delta_e0:.3e}, delta_A1(s/sqrt(6))={delta_s:.3e}",
    )

    gamma_e0 = center_law.gamma_pair(e0, (np.sqrt(3.0) * basis[:, 2] + basis[:, 3]) / 2.0, basis[:, 4])
    gamma_s = center_law.gamma_pair(s_unit, (np.sqrt(3.0) * basis[:, 2] + basis[:, 3]) / 2.0, basis[:, 4])
    print("\nCurrent tensor coefficients from the numerical frontier:")
    print(f"  gamma_E(e0) = {gamma_e0[0]:+.12e}")
    print(f"  gamma_T(e0) = {gamma_e0[1]:+.12e}")
    print(f"  gamma_E(s/sqrt(6)) = {gamma_s[0]:+.12e}")
    print(f"  gamma_T(s/sqrt(6)) = {gamma_s[1]:+.12e}")

    record(
        "the tensor endpoint coefficients are not yet exact on the retained stack",
        False,
        "tensor endpoints still come from eta_floor_tf; no exact support-side tensor observable exists yet",
        status="BLOCKED",
    )

    print("\nVerdict:")
    print(
        "The support-side endpoint theorem is exact, but the tensor endpoint "
        "coefficients remain blocked because the retained stack still lacks an "
        "exact tensor observable on A1 x {E_x, T1x}. The current tensor "
        "coefficients are still obtained through the numerical eta_floor_tf "
        "pipeline."
    )

    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
