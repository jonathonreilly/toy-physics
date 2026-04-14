#!/usr/bin/env python3
"""Finite-rank `3+1` promotion blocker.

This runner checks whether the exact projected DtN correction operator plus the
exact scalar active-quotient amplitude law already force a full lapse-shift-
spatial `3+1` matching map on the finite-rank widening lane.

The answer should be no if the exact stack is still scalar after quotienting;
the remaining missing primitive is then the tensor polarization lift.
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


dtn = SourceFileLoader(
    "finite_rank_dtn_corr",
    str(ROOT / "scripts" / "frontier_finite_rank_dtn_correction_operator.py"),
).load_module()
support_mod = SourceFileLoader(
    "support_renormalized_active_amplitude",
    str(ROOT / "scripts" / "frontier_support_renormalized_active_amplitude.py"),
).load_module()
src = SourceFileLoader(
    "finite_rank_source_metric",
    str(ROOT / "scripts" / "frontier_finite_rank_source_to_metric_theorem.py"),
).load_module()


def main() -> int:
    print("FINITE-RANK 3+1 PROMOTION BLOCKER")
    print("=" * 78)

    active_op = dtn.build_active_operator()
    pair_op = active_op[np.array(dtn.PAIR_ROWS), :]
    active_rank = int(np.linalg.matrix_rank(active_op, tol=1e-12))
    pair_rank = int(np.linalg.matrix_rank(pair_op, tol=1e-12))
    singular_values = np.linalg.svd(pair_op, compute_uv=False)

    support_op, support_pair_op = support_mod.support_to_active_operator()
    support_rank = int(np.linalg.matrix_rank(support_op, tol=1e-12))
    support_pair_rank = int(np.linalg.matrix_rank(support_pair_op, tol=1e-12))

    q_oh, vec_oh = support_mod.oh_q_eff()
    q_fr, vec_fr = support_mod.finite_rank_q_eff()
    qsum_oh = float(np.sum(q_oh))
    qsum_fr = float(np.sum(q_fr))
    pred_oh = support_op @ q_oh
    pred_fr = support_op @ q_fr
    scalar_oh = support_op[:, 0] * qsum_oh
    scalar_fr = support_op[:, 0] * qsum_fr
    err_oh = float(np.max(np.abs(pred_oh - vec_oh)))
    err_fr = float(np.max(np.abs(pred_fr - vec_fr)))
    scalar_err_oh = float(np.max(np.abs(vec_oh - scalar_oh)))
    scalar_err_fr = float(np.max(np.abs(vec_fr - scalar_fr)))

    phi_full, support_sites, interior, q_eff = src.finite_rank.exact_finite_rank_field()
    boundary = src.boundary_stationarity_report(phi_full)
    coarse_report = src.coarse_metric_report(phi_full)
    best = coarse_report["best"]

    print(f"active-op rank = {active_rank}")
    print(f"pair quotient rank = {pair_rank}")
    print(f"pair-quotient singular values = {np.array2string(singular_values, precision=6, floatmode='fixed')}")
    print(f"support-to-active rank = {support_rank}")
    print(f"support-to-active pair rank = {support_pair_rank}")
    print(f"Q_eff(local O_h) = {qsum_oh:.8f}")
    print(f"Q_eff(finite-rank) = {qsum_fr:.8f}")
    print(
        "best coarse 3+1 residuals: "
        f"direct={best[4]:.3e}, coarse={best[5]:.3e}, improvement={coarse_report['improvement']:.1f}x"
    )

    record(
        "the projected active correction operator is still exact on the finite-rank quotient",
        active_rank == 2 and pair_rank == 2,
        f"active rank={active_rank}, pair rank={pair_rank}",
    )
    record(
        "the support-renormalized active correction is still exact rank one",
        support_rank == 1 and support_pair_rank == 1,
        f"support rank={support_rank}, pair rank={support_pair_rank}",
    )
    record(
        "the scalar active-quotient amplitude law holds at machine precision",
        err_oh < 1e-12 and err_fr < 1e-12 and scalar_err_oh < 1e-12 and scalar_err_fr < 1e-12,
        (
            f"direct errors: O_h={err_oh:.3e}, finite-rank={err_fr:.3e}; "
            f"scalar-law errors: O_h={scalar_err_oh:.3e}, finite-rank={scalar_err_fr:.3e}"
        ),
    )
    record(
        "the direct finite-rank 3+1 residual remains nonzero",
        best[4] > 0,
        f"direct residual={best[4]:.3e}",
        status="BOUNDED",
    )

    print("\n" + "=" * 78)
    print("BLOCKER")
    print("=" * 78)
    print(
        "The exact projected DtN correction operator and the exact scalar active-quotient "
        "law still collapse to a scalar quotient after renormalization. They do not, by "
        "themselves, supply a full lapse-shift-spatial `3+1` matching map. The missing "
        "primitive is an exact `3+1` polarization lift `Pi_3+1` that separates the active "
        "scalar quotient into lapse, shift, and spatial-trace/shear channels."
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
