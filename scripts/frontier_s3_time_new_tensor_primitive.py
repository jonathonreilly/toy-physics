#!/usr/bin/env python3
"""Sharp blocker for the smallest missing Route-2 tensor primitive.

This runner answers the current worker question directly:

    does the exact support-side stack already contain the smallest exact
    microscopic tensor primitive needed before exterior projection?

The branch evidence says no. The exact support stack is scalar/rank-one on
the current A1 block, the support scalar delta_A1 is blind to the bright
tensor channels, and the only usable tensor-side object is still the bounded
staging prototype Theta_R^(0).
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib.machinery import SourceFileLoader

import numpy as np


ROOT = "/private/tmp/physics-review-active"

support_center = SourceFileLoader(
    "tensor_support_center_excess_law",
    f"{ROOT}/scripts/frontier_tensor_support_center_excess_law.py",
).load_module()
support_obs = SourceFileLoader(
    "tensor_support_side_observable",
    f"{ROOT}/scripts/frontier_tensor_support_side_observable.py",
).load_module()
a1_blind = SourceFileLoader(
    "tensor_a1_shell_projective_blindness",
    f"{ROOT}/scripts/frontier_tensor_a1_shell_projective_blindness.py",
).load_module()
boundary = SourceFileLoader(
    "tensor_boundary_drive_two_channel",
    f"{ROOT}/scripts/frontier_tensor_boundary_drive_two_channel.py",
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
    print("Route 2 new tensor primitive: sharp blocker")
    print("=" * 78)

    basis = support_obs.same_source.build_adapted_basis()
    e0 = basis[:, 0]
    s = basis[:, 1]
    s_unit = s / np.sqrt(6.0)
    e1 = basis[:, 2]
    e2 = basis[:, 3]
    t1x = basis[:, 4]
    e_x = (np.sqrt(3.0) * e1 + e2) / 2.0
    e_perp = (-e1 + np.sqrt(3.0) * e2) / 2.0

    delta_e0 = support_center.support_delta(e0)
    delta_s = support_center.support_delta(s_unit)
    delta_formula_err = 0.0
    for r in [0.0, 0.25, 0.5, 0.75, 1.25, 1.75]:
        q = (e0 + r * s) / (1.0 + np.sqrt(6.0) * r)
        delta = support_center.support_delta(q)
        formula = 1.0 / (6.0 * (1.0 + np.sqrt(6.0) * r))
        delta_formula_err = max(delta_formula_err, abs(delta - formula))
        print(
            f"r={r:.2f}: delta_A1={delta:.12e}, formula={formula:.12e}, "
            f"err={abs(delta-formula):.3e}"
        )

    record(
        "the exact surviving support primitive is the scalar center-excess delta_A1",
        abs(delta_e0 - 1.0 / 6.0) < 1e-12 and abs(delta_s) < 1e-12,
        f"delta_A1(e0)={delta_e0:.12e}, delta_A1(s/sqrt(6))={delta_s:.12e}",
    )
    record(
        "the canonical projective A1 family obeys the exact center-excess law",
        delta_formula_err < 1e-12,
        f"max formula error={delta_formula_err:.3e}",
    )

    eta0, scalar0, _ = boundary.tensor_metrics(boundary.phi_from_q(boundary.finite_rank_qeff()))
    amp = 0.10
    q_bg = boundary.finite_rank_qeff()
    d_ex = boundary.tensor_metrics(boundary.phi_from_q(q_bg + amp * e_x))[0] - eta0
    d_ep = boundary.tensor_metrics(boundary.phi_from_q(q_bg + amp * e_perp))[0] - eta0
    d_tx = boundary.tensor_metrics(boundary.phi_from_q(q_bg + amp * t1x))[0] - eta0
    print("\nTensor boundary-drive probe at amp=0.10:")
    print(f"  deta(E_x)    = {d_ex:+.12e}")
    print(f"  deta(E_perp) = {d_ep:+.12e}")
    print(f"  deta(T1x)    = {d_tx:+.12e}")

    record(
        "the current tensor boundary drive is bright only on aligned channels, not on an exact support primitive",
        abs(d_ex) > 1e-6 and abs(d_tx) > 1e-6 and abs(d_ep) < 1e-8,
        f"E_x={d_ex:+.3e}, E_perp={d_ep:+.3e}, T1x={d_tx:+.3e}",
        status="BOUNDED",
    )

    print("\nBounded staging object:")
    print("  Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))")
    print("  This is useful staging data, but not an exact tensor observable.")

    print("\nVerdict:")
    print(
        "The exact support-side stack is scalar/rank-one on A1 and therefore "
        "cannot produce a nonzero exact tensor observable on A1 x {E_x, T1x}. "
        "The smallest missing Route-2 primitive is a new microscopic tensor "
        "operator before exterior projection."
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
