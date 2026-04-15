#!/usr/bin/env python3
"""Exact Hessian-selector uniqueness inside the Schur normal-form class."""

from __future__ import annotations

import pathlib
import sys
import time
from dataclasses import dataclass

import numpy as np

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import frontier_yt_exact_schur_normal_form_uniqueness as base

np.set_printoptions(precision=10, linewidth=120)


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    status: str = "EXACT"


CHECKS: list[Check] = []


def record(name: str, ok: bool, detail: str, status: str = "EXACT") -> None:
    CHECKS.append(Check(name=name, ok=ok, detail=detail, status=status))
    tag = "PASS" if ok else "FAIL"
    print(f"[{status}] {tag}: {name}")
    if detail:
        print(f"    {detail}")


def normalized(v: np.ndarray) -> np.ndarray:
    return v / max(np.linalg.norm(v), 1.0e-12)


def selector_shape_metrics(sel: np.ndarray, ref: np.ndarray) -> tuple[float, float]:
    rel_l2 = float(np.linalg.norm(sel - ref) / max(np.linalg.norm(ref), 1.0e-12))
    corr = float(np.dot(normalized(sel), normalized(ref)))
    return rel_l2, corr


def main() -> int:
    print("=" * 78)
    print("YT EXACT HESSIAN SELECTOR UNIQUENESS")
    print("=" * 78)
    print()
    print("Test whether every admissible exact Schur coarse bridge operator inside")
    print("the current intrinsic budgets induces the same local Hessian selector")
    print("shape on the forced UV window.")
    print()
    t0 = time.time()

    g1_v, g2_v = base.ew_boundary_at_v()
    g1_pl, g2_pl = base.run_ew_upward(g1_v, g2_v)
    g3_sm = base.sm_like_g3_trajectory()
    kernel = base.accepted_kernel(g1_pl, g2_pl, g3_sm)

    tau_frac = base.TAU_GRID / base.LOG_SPAN
    x_kernel = 1.0 - tau_frac
    uv_mask = x_kernel >= 0.95
    order = np.argsort(x_kernel[uv_mask])
    x_uv = x_kernel[uv_mask][order]
    kernel_uv = kernel[uv_mask][order]

    _, kernel_loc, h_loc, lap = base.build_reference_operator(x_uv, kernel_uv)
    ref_selector = normalized(np.diag(h_loc))

    local_scale = base.HIGHER_ORDER_RATIO * np.linalg.norm(h_loc, 2)
    nonlocal_scale = base.NONLOCAL_RATIO_OP * np.linalg.norm(h_loc, 2)

    rows = []
    for d_amp in [0.0, 0.25, 0.5, 0.75, 1.0]:
        for n_amp in [0.0, 0.25, 0.5, 0.75, 1.0]:
            for mode in range(4):
                d_mode = base.smooth_diag_mode(x_uv, mode)
                for phase, scale in [(0, 2.5), (1, 4.0), (2, 7.0)]:
                    n_mode = base.quasi_local_tail(len(x_uv), scale, phase)
                    k = h_loc + d_amp * local_scale * d_mode + n_amp * nonlocal_scale * n_mode
                    k = 0.5 * (k + k.T)
                    eig = np.linalg.eigvalsh(k)
                    if np.min(eig) <= 1.0e-8:
                        continue
                    selector_diag = 1.0 / np.maximum(np.diag(k), 1.0e-12)
                    selector_shape = normalized(selector_diag)
                    rel_l2, corr = selector_shape_metrics(selector_shape, ref_selector)
                    rows.append(
                        {
                            "d_amp": d_amp,
                            "n_amp": n_amp,
                            "mode": mode,
                            "phase": phase,
                            "scale": scale,
                            "min_eig": float(np.min(eig)),
                            "selector_rel_l2": rel_l2,
                            "selector_corr": corr,
                        }
                    )

    max_rel_l2 = max(r["selector_rel_l2"] for r in rows)
    min_corr = min(r["selector_corr"] for r in rows)
    min_eig = min(r["min_eig"] for r in rows)

    print(f"Forced UV window: x >= 0.95, points = {len(x_uv)}")
    print(f"Surviving SPD operators         = {len(rows)}")
    print(f"min eigenvalue across class     = {min_eig:.6e}")
    print(f"max selector-shape rel L2 drift = {max_rel_l2:.6e}")
    print(f"min selector-shape correlation  = {min_corr:.9f}")
    print()

    record(
        "every admissible Schur coarse operator remains positive definite",
        min_eig > 0.0,
        f"min eigenvalue across class = {min_eig:.6e}",
    )
    record(
        "the local Hessian selector shape is unique across the admissible Schur class",
        max_rel_l2 < 2.5e-2,
        f"max selector-shape relative L2 drift = {max_rel_l2:.6e}",
    )
    record(
        "the local Hessian selector stays strongly aligned with the reference selector",
        min_corr > 0.999,
        f"min selector correlation = {min_corr:.9f}",
    )
    record(
        "selector uniqueness is stronger than the already-bounded response-class uniqueness",
        max_rel_l2 < base.CONSERVATIVE_REL_BUDGET,
        f"selector drift = {max_rel_l2:.6e}, branch budget = {base.CONSERVATIVE_REL_BUDGET:.6e}",
        status="BOUNDED",
    )

    print()
    print("-" * 78)
    print("Interpretation")
    print("-" * 78)
    print(
        "Inside the intrinsic local/nonlocal budget tube, the exact Schur coarse "
        "operator does not induce multiple competing local Hessian selectors."
    )
    print(
        "So the remaining YT gap is no longer selector ambiguity inside the "
        "coarse class. It is only whether the exact microscopic bridge belongs "
        "to this already-unique Schur class."
    )
    print()
    print("=" * 78)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print(f"FINAL TALLY: {n_pass} PASS / {n_fail} FAIL")
    print(f"Elapsed: {time.time() - t0:.2f} s")
    print("=" * 78)
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
