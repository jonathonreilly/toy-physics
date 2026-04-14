#!/usr/bin/env python3
"""Finite-rank support-side polarization-frame blocker.

This runner asks a narrow question on the widening lane:

Can the current exact finite-rank support stack already supply a canonical
tensor-side polarization frame that separates lapse, shift, and
spatial trace/shear before quotient collapse?

The expected answer is no if the support-to-active response operator is still
rank one after renormalization.
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
dtn = SourceFileLoader(
    "finite_rank_dtn_corr",
    str(ROOT / "scripts" / "frontier_finite_rank_dtn_correction_operator.py"),
).load_module()
finite_rank = SourceFileLoader(
    "finite_rank_metric",
    str(ROOT / "scripts" / "frontier_finite_rank_source_to_metric_theorem.py"),
).load_module()


def orthonormalize(vectors: list[np.ndarray]) -> np.ndarray:
    basis: list[np.ndarray] = []
    for vec in vectors:
        w = np.array(vec, dtype=float, copy=True)
        for b in basis:
            w -= np.dot(b, w) * b
        nrm = float(np.linalg.norm(w))
        if nrm > 1e-12:
            basis.append(w / nrm)
    return np.column_stack(basis)


def main() -> int:
    print("FINITE-RANK SUPPORT POLARIZATION FRAME BLOCKER")
    print("=" * 78)

    support_op, support_pair_op = support.support_to_active_operator()
    active_op = dtn.build_active_operator()
    pair_op = active_op[np.array(dtn.PAIR_ROWS), :]

    support_rank = int(np.linalg.matrix_rank(support_op, tol=1e-12))
    support_pair_rank = int(np.linalg.matrix_rank(support_pair_op, tol=1e-12))
    active_rank = int(np.linalg.matrix_rank(active_op, tol=1e-12))
    pair_rank = int(np.linalg.matrix_rank(pair_op, tol=1e-12))

    support_u, support_s, _ = np.linalg.svd(support_op, full_matrices=False)
    active_u, active_s, _ = np.linalg.svd(active_op, full_matrices=False)
    pair_s = np.linalg.svd(pair_op, compute_uv=False)

    support_basis = support_u[:, 0]
    active_mode_1 = active_u[:, 0]
    active_mode_2 = active_u[:, 1]

    resid_mode_1 = float(
        np.linalg.norm(
            active_mode_1
            - support_basis * (support_basis @ active_mode_1) / (np.linalg.norm(support_basis) ** 2)
        )
    )
    resid_mode_2 = float(
        np.linalg.norm(
            active_mode_2
            - support_basis * (support_basis @ active_mode_2) / (np.linalg.norm(support_basis) ** 2)
        )
    )

    frame_a = orthonormalize([support_basis, active_mode_1, active_mode_2])
    theta = np.pi / 7.0
    rot_1 = np.cos(theta) * active_mode_1 + np.sin(theta) * active_mode_2
    rot_2 = -np.sin(theta) * active_mode_1 + np.cos(theta) * active_mode_2
    frame_b = orthonormalize([support_basis, rot_1, rot_2])
    frame_delta = float(np.max(np.abs(frame_a - frame_b)))

    q_oh, vec_oh = support.oh_q_eff()
    q_fr, vec_fr = support.finite_rank_q_eff()
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

    print(f"support singular values = {np.array2string(support_s, precision=6, floatmode='fixed')}")
    print(f"active singular values  = {np.array2string(active_s, precision=6, floatmode='fixed')}")
    print(f"pair singular values    = {np.array2string(pair_s, precision=6, floatmode='fixed')}")
    print(f"support rank = {support_rank}")
    print(f"support pair rank = {support_pair_rank}")
    print(f"active rank = {active_rank}")
    print(f"pair rank = {pair_rank}")
    print(f"support-span residuals vs active modes = ({resid_mode_1:.3e}, {resid_mode_2:.3e})")
    print(f"frame delta between two valid 3+1 completions = {frame_delta:.3e}")
    print(f"Q_eff(local O_h) = {qsum_oh:.8f}")
    print(f"Q_eff(finite-rank) = {qsum_fr:.8f}")

    record(
        "the finite-rank support-to-active correction operator is exact rank one",
        support_rank == 1 and support_pair_rank == 1,
        f"support rank={support_rank}, pair rank={support_pair_rank}",
    )
    record(
        "the active quotient remains rank two on the projected DtN side",
        active_rank == 2 and pair_rank == 2,
        f"active rank={active_rank}, pair rank={pair_rank}",
    )
    record(
        "the support span canonically sources only one active direction",
        resid_mode_1 < 0.2 and resid_mode_2 > 0.9,
        f"support-span residuals: mode1={resid_mode_1:.3e}, mode2={resid_mode_2:.3e}",
        status="BOUNDED",
    )
    record(
        "two equally valid 3+1 completions of the active quotient differ",
        frame_delta > 1e-2,
        f"frame delta={frame_delta:.3e}",
        status="BOUNDED",
    )
    record(
        "the support-renormalized scalar active law remains exact",
        err_oh < 1e-12 and err_fr < 1e-12 and scalar_err_oh < 1e-12 and scalar_err_fr < 1e-12,
        (
            f"direct errors: O_h={err_oh:.3e}, finite-rank={err_fr:.3e}; "
            f"scalar-law errors: O_h={scalar_err_oh:.3e}, finite-rank={scalar_err_fr:.3e}"
        ),
    )

    print("\n" + "=" * 78)
    print("BLOCKER")
    print("=" * 78)
    print(
        "The finite-rank support side still does not provide a canonical exact "
        "`Pi_3+1` polarization lift. The support-to-active operator collapses to "
        "rank one after renormalization, while the active quotient is rank two. "
        "Any completion to lapse, shift, and spatial trace/shear requires extra "
        "independent support generators not present in the current finite-rank stack."
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
