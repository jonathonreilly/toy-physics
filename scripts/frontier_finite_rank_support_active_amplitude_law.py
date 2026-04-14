#!/usr/bin/env python3
"""Finite-rank support-renormalized active-shell amplitude law.

Exact content:
  1. The microscopic support-to-active response operator is rank one.
  2. The active correction factors exactly through the total renormalized
     support charge Q_eff.
  3. The same scalar-amplitude law holds on the active pair quotient.

Bounded content:
  4. The scalar amplitude law does not by itself produce the full tensorial
     `3+1` matching map.
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


support = SourceFileLoader(
    "support_renormalized_active_amplitude",
    str(ROOT / "scripts" / "frontier_support_renormalized_active_amplitude.py"),
).load_module()


def main() -> int:
    print("FINITE-RANK SUPPORT-RENORMALIZED ACTIVE-SHELL AMPLITUDE LAW")
    print("=" * 78)

    active_op, pair_op = support.support_to_active_operator()
    active_mode = active_op[:, 0]
    pair_mode = pair_op[:, 0]
    ones = np.ones((1, active_op.shape[1]), dtype=float)
    active_fact = active_mode[:, None] @ ones
    pair_fact = pair_mode[:, None] @ ones

    active_rank = int(np.linalg.matrix_rank(active_op, tol=1e-12))
    pair_rank = int(np.linalg.matrix_rank(pair_op, tol=1e-12))
    active_factor_resid = float(np.max(np.abs(active_op - active_fact)))
    pair_factor_resid = float(np.max(np.abs(pair_op - pair_fact)))

    q_oh, vec_oh = support.oh_q_eff()
    q_fr, vec_fr = support.finite_rank_q_eff()
    qsum_oh = float(np.sum(q_oh))
    qsum_fr = float(np.sum(q_fr))

    pred_oh = active_op @ q_oh
    pred_fr = active_op @ q_fr
    scalar_oh = active_mode * qsum_oh
    scalar_fr = active_mode * qsum_fr
    pair_scalar_oh = pair_mode * qsum_oh
    pair_scalar_fr = pair_mode * qsum_fr

    err_oh = float(np.max(np.abs(pred_oh - vec_oh)))
    err_fr = float(np.max(np.abs(pred_fr - vec_fr)))
    scalar_err_oh = float(np.max(np.abs(vec_oh - scalar_oh)))
    scalar_err_fr = float(np.max(np.abs(vec_fr - scalar_fr)))
    pair_err_oh = float(np.max(np.abs(vec_oh[:2] - pair_scalar_oh)))
    pair_err_fr = float(np.max(np.abs(vec_fr[:2] - pair_scalar_fr)))

    print("Support -> active-orbit response operator:")
    print(np.array2string(active_op, precision=8, floatmode="fixed"))
    print(f"active rank = {active_rank}")
    print(f"pair rank = {pair_rank}")
    print(f"active factorization residual = {active_factor_resid:.3e}")
    print(f"pair factorization residual = {pair_factor_resid:.3e}")
    print(f"unit-charge active mode = {np.array2string(active_mode, precision=8, floatmode='fixed')}")
    print(f"Q_eff(local O_h) = {qsum_oh:.8f}")
    print(f"Q_eff(finite-rank) = {qsum_fr:.8f}")

    record(
        "the microscopic support-to-active correction operator is exact rank one",
        active_rank == 1 and pair_rank == 1,
        f"active rank={active_rank}, pair rank={pair_rank}",
    )
    record(
        "the support-to-active operator factors exactly through total renormalized support charge",
        active_factor_resid < 1e-12 and pair_factor_resid < 1e-12,
        (
            f"active residual={active_factor_resid:.3e}, "
            f"pair residual={pair_factor_resid:.3e}"
        ),
    )
    record(
        "the exact local O_h and finite-rank source families satisfy the full active support-response law",
        err_oh < 1e-12 and err_fr < 1e-12 and scalar_err_oh < 1e-12 and scalar_err_fr < 1e-12,
        (
            f"direct errors: O_h={err_oh:.3e}, finite-rank={err_fr:.3e}; "
            f"scalar-law errors: O_h={scalar_err_oh:.3e}, finite-rank={scalar_err_fr:.3e}"
        ),
    )
    record(
        "the same scalar-amplitude law holds exactly on the active pair quotient",
        pair_err_oh < 1e-12 and pair_err_fr < 1e-12,
        f"pair errors: O_h={pair_err_oh:.3e}, finite-rank={pair_err_fr:.3e}",
    )

    print("\n" + "=" * 78)
    print("BLOCKER")
    print("=" * 78)
    print(
        "The support-renormalized active-shell amplitude law is exact, but it still "
        "does not supply the full tensorial `3+1` matching map. The next missing "
        "primitive is the tensorial promotion of this scalar quotient law."
    )

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    if n_fail == 0:
        print("All checks passed.")
    else:
        print("Some checks failed.")

    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
