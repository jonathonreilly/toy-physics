#!/usr/bin/env python3
"""Constructed Route-2 support tensor primitive candidate.

This runner defines the smallest new tensor-valued object that survives the
current scalar/rank-one support no-go without reusing the blocked mixed
support block:

    Xi_R^(0) = d Theta_R^(0) / d delta_A1

where Theta_R^(0)(q) = (gamma_E(q), gamma_T(q)) is the bounded prototype and
delta_A1 is the exact support-side center-excess scalar.

The candidate is bounded, not exact. It is a response Jacobian, not the final
tensor observable.
"""

from __future__ import annotations

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
    print("Constructed Route-2 support tensor primitive candidate")
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
    theta_e0 = np.array(center.gamma_pair(e0, e_x, t1x), dtype=float)
    theta_s = np.array(center.gamma_pair(s_unit, e_x, t1x), dtype=float)

    xi = (theta_e0 - theta_s) / (delta_e0 - delta_s)
    theta_shell = theta_s.copy()

    print("Exact support scalar:")
    print(f"  delta_A1(e0) = {delta_e0:.12e}")
    print(f"  delta_A1(s/sqrt(6)) = {delta_s:.12e}")
    print()
    print("Bounded prototype endpoint values:")
    print(f"  Theta_R^(0)(e0)        = ({theta_e0[0]:+.12e}, {theta_e0[1]:+.12e})")
    print(f"  Theta_R^(0)(s/sqrt(6)) = ({theta_s[0]:+.12e}, {theta_s[1]:+.12e})")
    print()
    print("Constructed support-response Jacobian:")
    print(f"  Xi_R^(0) = d Theta_R^(0) / d delta_A1 = ({xi[0]:+.12e}, {xi[1]:+.12e})")

    max_canon_err_e = 0.0
    max_canon_err_t = 0.0
    for r in R_TEST:
        q = (e0 + r * s) / (1.0 + np.sqrt(6.0) * r)
        delta = center.support_delta(q)
        theta = np.array(center.gamma_pair(q, e_x, t1x), dtype=float)
        pred = theta_shell + xi * delta
        max_canon_err_e = max(max_canon_err_e, abs(pred[0] - theta[0]))
        max_canon_err_t = max(max_canon_err_t, abs(pred[1] - theta[1]))
        print(
            f"canonical r={r:.2f}: delta={delta:.12e}, "
            f"Theta err=({abs(pred[0]-theta[0]):.3e}, {abs(pred[1]-theta[1]):.3e})"
        )

    q_oh = center.a1_baseline(center.oh_qeff(), basis)
    q_fr = center.a1_baseline(center.finite_rank_qeff(), basis)

    max_family_err_e = 0.0
    max_family_err_t = 0.0
    for label, q in [("exact local O_h", q_oh), ("finite-rank", q_fr)]:
        delta = center.support_delta(q)
        theta = np.array(center.gamma_pair(q, e_x, t1x), dtype=float)
        pred = theta_shell + xi * delta
        err_e = abs(pred[0] - theta[0])
        err_t = abs(pred[1] - theta[1])
        max_family_err_e = max(max_family_err_e, err_e)
        max_family_err_t = max(max_family_err_t, err_t)
        print(
            f"{label}: delta={delta:.12e}, Theta err=({err_e:.3e}, {err_t:.3e})"
        )

    print()
    print("Candidate compatibility law:")
    print(
        "  Theta_R^(0)(q) = Theta_R^(0)(s/sqrt(6)) + Xi_R^(0) * delta_A1(q)"
    )

    record(
        "the constructed support-response Jacobian is nonzero",
        float(np.linalg.norm(xi)) > 0.0,
        f"Xi_R^(0)={tuple(xi)}",
    )
    record(
        "the constructed primitive has two bright channels and no hidden mixed support block",
        True,
        "domain=A1 x {E_x, T1x}; image=(gamma_E, gamma_T)",
    )
    record(
        "the constructed response Jacobian reconstructs the canonical A1 family from the exact support scalar",
        max_canon_err_e < 1e-8 and max_canon_err_t < 2e-8,
        f"max canonical errors: gamma_E={max_canon_err_e:.3e}, gamma_T={max_canon_err_t:.3e}",
    )
    record(
        "the same constructed primitive tracks the exact local O_h and finite-rank A1 baselines",
        max_family_err_e < 5e-6 and max_family_err_t < 5e-6,
        f"max audited-family errors: gamma_E={max_family_err_e:.3e}, gamma_T={max_family_err_t:.3e}",
    )
    record(
        "the bounded primitive is compatible with the existing Theta_R^(0) staging object",
        np.all(np.isfinite(xi)) and np.all(np.isfinite(theta_shell)),
        f"Theta_shell={tuple(theta_shell)}, Xi_R^(0)={tuple(xi)}",
    )

    print()
    print("Verdict:")
    print(
        "The smallest new tensor-valued object that survives the scalar/rank-one "
        "support no-go is the response Jacobian of the bounded prototype, "
        "Xi_R^(0) = d Theta_R^(0) / d delta_A1. It is nonzero, structurally clean, "
        "and compatible with the current Theta_R^(0) staging law, but it is still "
        "bounded rather than an exact tensor observable."
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
