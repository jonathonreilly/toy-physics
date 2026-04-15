#!/usr/bin/env python3
"""Microscopic admissibility of the exact Schur YT bridge class.

This runner addresses the remaining structural objection after:

- exact coarse-grained bridge operator;
- exact Schur normal-form uniqueness;
- Schur stability gap.

Question:
    Can axiom-native *microscopic* local positive bridge operators reduce,
    under exact Schur/Feshbach marginalization, into coarse operators that
    still belong to the already-closed Schur normal-form class?

This runner answers that on the current branch by constructing local
microscopic bridge operators around the exact coarse UV bridge and checking
that every surviving exact reduction remains inside the unique stable Schur
class and its explicit conservative endpoint budget.
"""

from __future__ import annotations

import pathlib
import sys
import time
from dataclasses import dataclass

import numpy as np

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import frontier_yt_exact_coarse_grained_bridge_operator as coarse
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


def normalized_fine_laplacian(n: int) -> np.ndarray:
    lap = np.zeros((n, n))
    for i in range(n):
        lap[i, i] = 2.0
        if i > 0:
            lap[i, i - 1] = -1.0
        if i + 1 < n:
            lap[i, i + 1] = -1.0
    return lap / max(np.linalg.norm(lap, 2), 1.0e-12)


def local_coupling_template(x_uv: np.ndarray, fine_dim: int, profile: int) -> np.ndarray:
    x_f = np.linspace(np.min(x_uv), np.max(x_uv), fine_dim)
    widths = [0.010, 0.015, 0.022]
    phases = [0.0, 0.7, 1.3]
    width = widths[profile % len(widths)]
    phase = phases[profile % len(phases)]
    mat = np.zeros((len(x_uv), fine_dim))
    for i, xu in enumerate(x_uv):
        for j, xf in enumerate(x_f):
            local = np.exp(-abs(xu - xf) / width)
            mod = 1.0 + 0.08 * np.cos((i + j + 1) * phase)
            mat[i, j] = local * mod
    return mat / max(np.linalg.norm(mat, 2), 1.0e-12)


def local_coupling_mode(x_uv: np.ndarray, fine_dim: int, mode: int) -> np.ndarray:
    x_f = np.linspace(np.min(x_uv), np.max(x_uv), fine_dim)
    mat = np.zeros((len(x_uv), fine_dim))
    for i, xu in enumerate(x_uv):
        for j, xf in enumerate(x_f):
            d = abs(xu - xf)
            if mode == 0:
                val = np.exp(-d / 0.012)
            elif mode == 1:
                val = (xu - np.mean(x_uv)) * np.exp(-d / 0.016)
            else:
                val = np.sin((i + 1) * (j + 1) / 11.0) * np.exp(-d / 0.020)
            mat[i, j] = val
    return mat / max(np.linalg.norm(mat, 2), 1.0e-12)


def build_local_reference_microscopic_operator(
    k_target: np.ndarray,
    x_uv: np.ndarray,
    fine_dim: int = 24,
    profile: int = 0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    fine_lap = normalized_fine_laplacian(fine_dim)
    c0 = np.diag(np.linspace(1.35, 2.45, fine_dim)) + 0.09 * fine_lap
    b0 = 0.042 * local_coupling_template(x_uv, fine_dim, profile)
    a0 = k_target + b0 @ np.linalg.solve(c0, b0.T)
    j_eff = np.ones(len(x_uv))
    k_full = np.block([[a0, b0], [b0.T, c0]])
    j_full = np.concatenate([j_eff, np.zeros(fine_dim)])
    keep = np.arange(len(x_uv))
    return k_full, j_full, keep, c0, b0


def classify_reduction(
    x_uv: np.ndarray,
    kernel_uv: np.ndarray,
    h_loc: np.ndarray,
    k_eff: np.ndarray,
) -> tuple[float, float, float]:
    response = np.linalg.solve(k_eff, np.ones(len(x_uv)))
    _, aff_rel = base.affine_stats(x_uv, response)
    resp_rel = float(
        np.linalg.norm(response - kernel_uv) / max(np.linalg.norm(kernel_uv), 1.0e-12)
    )
    tail_ratio = float(np.linalg.norm(k_eff - h_loc, 2) / max(np.linalg.norm(h_loc, 2), 1.0e-12))
    return aff_rel, resp_rel, tail_ratio


def main() -> int:
    print("=" * 78)
    print("YT MICROSCOPIC SCHUR CLASS ADMISSIBILITY")
    print("=" * 78)
    print()
    print("Start from local positive microscopic bridge operators on the accepted")
    print("UV window, reduce them exactly by Schur complement, and test whether")
    print("every surviving reduction remains inside the unique stable Schur class.")
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

    affine_ref, kernel_loc, h_loc, lap = base.build_reference_operator(x_uv, kernel_uv)
    tail_scale = base.NONLOCAL_RATIO_OP * float(np.mean(np.diag(h_loc)))
    k_target = h_loc + tail_scale * lap

    local_scale = base.HIGHER_ORDER_RATIO * np.linalg.norm(h_loc, 2)
    nonlocal_scale = base.NONLOCAL_RATIO_OP * np.linalg.norm(h_loc, 2)

    rows = []
    coarse_ok = 0
    for profile in range(3):
        k_full0, j_full0, keep, c0, b0 = build_local_reference_microscopic_operator(
            k_target,
            x_uv,
            fine_dim=24,
            profile=profile,
        )
        n_coarse = len(x_uv)
        n_fine = c0.shape[0]
        fine_lap = normalized_fine_laplacian(n_fine)

        a0 = k_full0[:n_coarse, :n_coarse]
        c_base = k_full0[n_coarse:, n_coarse:]
        b_base = k_full0[:n_coarse, n_coarse:]

        for a_amp in [0.0, 0.35, 0.7, 1.0]:
            for b_amp in [0.0, 0.35, 0.7, 1.0]:
                for c_amp in [0.0, 0.35, 0.7, 1.0]:
                    for mode in range(3):
                        d_mode = base.smooth_diag_mode(x_uv, mode)
                        b_mode = local_coupling_mode(x_uv, n_fine, mode)
                        c_mode = fine_lap if mode < 2 else np.diag(np.linspace(-1.0, 1.0, n_fine))
                        c_mode = c_mode / max(np.linalg.norm(c_mode, 2), 1.0e-12)

                        a = a0 + a_amp * local_scale * d_mode
                        b = b_base + b_amp * 0.12 * np.linalg.norm(b_base, 2) * b_mode
                        c = c_base + c_amp * 0.12 * np.linalg.norm(c_base, 2) * c_mode
                        c = 0.5 * (c + c.T)
                        if np.min(np.linalg.eigvalsh(c)) <= 1.0e-5:
                            continue

                        k_full = np.block([[a, b], [b.T, c]])
                        k_full = 0.5 * (k_full + k_full.T)
                        eig = np.linalg.eigvalsh(k_full)
                        if np.min(eig) <= 1.0e-6:
                            continue

                        k_eff, _ = coarse.schur_reduce(k_full, j_full0, keep)
                        aff_rel, resp_rel, tail_ratio = classify_reduction(x_uv, kernel_uv, h_loc, k_eff)
                        coarse_ok_flag = aff_rel < 1.5e-2 and resp_rel < base.CONSERVATIVE_REL_BUDGET
                        if coarse_ok_flag:
                            coarse_ok += 1

                        rows.append(
                            {
                                "profile": profile,
                                "a_amp": a_amp,
                                "b_amp": b_amp,
                                "c_amp": c_amp,
                                "mode": mode,
                                "eig_min": float(np.min(eig)),
                                "aff_rel": aff_rel,
                                "resp_rel": resp_rel,
                                "tail_ratio": tail_ratio,
                            }
                        )

    if not rows:
        raise RuntimeError("no admissible microscopic operators survived")

    max_aff = max(r["aff_rel"] for r in rows)
    max_resp = max(r["resp_rel"] for r in rows)
    max_tail = max(r["tail_ratio"] for r in rows)
    worst = max(rows, key=lambda r: r["resp_rel"])
    all_in_class = all(
        r["aff_rel"] < 1.5e-2 and r["resp_rel"] < base.CONSERVATIVE_REL_BUDGET
        for r in rows
    )

    print(f"Microscopic operators tested      = {len(rows)}")
    print(f"Coarse reductions in Schur class  = {coarse_ok}")
    print(f"Max affine residual              = {max_aff:.6e}")
    print(f"Max response-vs-kernel gap       = {max_resp:.6e}")
    print(f"Max reduced tail ratio           = {max_tail:.6e}")
    print(f"Conservative branch budget       = {base.CONSERVATIVE_REL_BUDGET:.6e}")
    print()
    print("Worst retained microscopic reduction:")
    print(
        "  "
        f"profile={worst['profile']}, "
        f"(a,b,c)=({worst['a_amp']:.2f},{worst['b_amp']:.2f},{worst['c_amp']:.2f}), "
        f"mode={worst['mode']}, "
        f"resp={worst['resp_rel']:.6e}, aff={worst['aff_rel']:.6e}, "
        f"tail={worst['tail_ratio']:.6e}"
    )
    print()

    record(
        "local positive microscopic bridge operators reduce exactly by Schur complement to coarse UV operators",
        True,
        f"{len(rows)} microscopic local operators survived positivity and exact reduction",
    )
    record(
        "every surviving microscopic reduction remains inside the unique Schur normal-form class",
        all_in_class,
        f"max affine residual={max_aff:.6e}, max response gap={max_resp:.6e}",
    )
    record(
        "the microscopic reductions stay inside the conservative endpoint budget",
        max_resp < base.CONSERVATIVE_REL_BUDGET,
        f"max response gap={max_resp:.6e}, budget={base.CONSERVATIVE_REL_BUDGET:.6e}",
    )
    record(
        "the reduced nonlocal tail remains on the same intrinsic branch nonlocal scale across the microscopic locality tube",
        max_tail < 1.20 * base.NONLOCAL_RATIO_OP,
        f"max reduced tail ratio={max_tail:.6e}, branch ratio={base.NONLOCAL_RATIO_OP:.6e}",
        status="BOUNDED",
    )
    record(
        "the remaining y_t ambiguity is no longer microscopic admissibility at branch scale",
        all_in_class and max_resp < base.CONSERVATIVE_REL_BUDGET,
        f"all microscopic reductions stayed in class across {len(rows)} exact Schur tests",
        status="BOUNDED",
    )

    print()
    print("-" * 78)
    print("Interpretation")
    print("-" * 78)
    print(
        "Within the axiom-native microscopic locality tube tested here, exact "
        "local positive bridge operators do not reduce to multiple coarse "
        "classes. They all land in the same unique stable Schur class."
    )
    print(
        "So the branch no longer needs a separate microscopic-admissibility "
        "escape hatch at this scale. What remains is only the explicit "
        "package-native endpoint budget carried by the exact bridge."
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
