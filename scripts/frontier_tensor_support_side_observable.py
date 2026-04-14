#!/usr/bin/env python3
"""Exact support-side observable on the current axiom-first gravity frontier.

This runner isolates the exact microscopic support datum that survives the
shell/junction blindness theorem:

    delta_A1 = phi_support(center)/Q - phi_support(arm_mean)/Q

The runner verifies:
  1. the exact endpoint support coefficients at e0 and s/sqrt(6)
  2. the exact canonical formula on the projective A1 family

This is exact support-side structure, not yet the tensor boundary observable.
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
    print("Exact support-side A1 observable")
    print("=" * 72)

    basis = same_source.build_adapted_basis()
    e0 = basis[:, 0]
    s = basis[:, 1]
    s_unit = s / np.sqrt(6.0)

    delta_e0 = center_law.support_delta(e0)
    delta_s = center_law.support_delta(s_unit)

    print(f"delta_A1(e0) = {delta_e0:.12e}")
    print(f"delta_A1(s/sqrt(6)) = {delta_s:.12e}")

    record(
        "the exact support-side observable is the A1 center-excess scalar delta_A1",
        abs(delta_e0 - 1.0 / 6.0) < 1e-12 and abs(delta_s) < 1e-12,
        f"endpoint values: e0={delta_e0:.3e}, s/sqrt(6)={delta_s:.3e}",
    )

    max_err = 0.0
    for r in [0.0, 0.25, 0.5, 0.75, 1.25, 1.75]:
        q = (e0 + r * s) / (1.0 + np.sqrt(6.0) * r)
        delta = center_law.support_delta(q)
        formula = 1.0 / (6.0 * (1.0 + np.sqrt(6.0) * r))
        err = abs(delta - formula)
        max_err = max(max_err, err)
        print(f"r={r:.2f}: delta={delta:.12e}, formula={formula:.12e}, err={err:.3e}")

    record(
        "the canonical projective A1 family obeys the exact center-excess law",
        max_err < 1e-12,
        f"max formula error={max_err:.3e}",
    )

    print("\nVerdict:")
    print(
        "The retained stack gives one exact microscopic support observable, "
        "delta_A1, with exact endpoint coefficients at e0 and s/sqrt(6). "
        "This is the right support-side primitive, but it still does not yet "
        "produce the exact tensor observable on A1 x {E_x, T1x}."
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
