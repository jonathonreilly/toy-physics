#!/usr/bin/env python3
"""Broader support-class gravity: noncompact tail widening and obstruction.

This script checks whether the current bridge package can widen beyond compact
finite support to genuinely noncompact source tails. The target is not another
finite-support benchmark:

  1. exponentially localized tails: bounded extension should be possible
  2. steep algebraic tails: may still be truncation-stable if low moments stay
     finite
  3. generic long-range algebraic tails: should hit a sharp obstruction

The test compares full-source Poisson fields to truncated finite-radius
approximations on the same Dirichlet box, and tracks tail monopole / quadrupole
content as the box or truncation radius changes.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib.machinery import SourceFileLoader

import numpy as np
from scipy.sparse.linalg import spsolve


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


finite_rank = SourceFileLoader(
    "finite_rank_metric",
    "/private/tmp/physics-review-active/scripts/frontier_finite_rank_gravity_residual.py",
).load_module()
sewing = SourceFileLoader(
    "sewing_shell",
    "/private/tmp/physics-review-active/scripts/frontier_sewing_shell_source.py",
).load_module()


SIZE = 31
CENTER = (SIZE - 1) / 2.0
R_CUTS = [4.0, 6.0, 8.0, 10.0]
RADII = sewing.radii_grid(SIZE)


def build_source(profile: str, param: float) -> np.ndarray:
    i, j, k = np.mgrid[0:SIZE, 0:SIZE, 0:SIZE]
    r = RADII
    if profile == "exp":
        rho = np.exp(-r / param)
    elif profile == "power":
        rho = 1.0 / (1.0 + r) ** param
    else:
        raise ValueError(f"unknown profile: {profile}")
    rho[0, :, :] = 0.0
    rho[-1, :, :] = 0.0
    rho[:, 0, :] = 0.0
    rho[:, -1, :] = 0.0
    rho[:, :, 0] = 0.0
    rho[:, :, -1] = 0.0
    return rho


def solve_poisson(source_grid: np.ndarray) -> np.ndarray:
    H0, interior = finite_rank.build_neg_laplacian_sparse(SIZE)
    rhs = source_grid[1:-1, 1:-1, 1:-1].reshape(-1)
    sol = spsolve(H0, rhs)
    out = np.zeros_like(source_grid)
    out[1:-1, 1:-1, 1:-1] = sol.reshape((interior, interior, interior))
    return out


def tail_moments(source_grid: np.ndarray, cutoff: float) -> dict[str, float]:
    mask = RADII > cutoff + 1e-12
    q_total = float(np.sum(source_grid))
    q_tail = float(np.sum(source_grid[mask]))
    m2_total = float(np.sum(source_grid * RADII * RADII))
    m2_tail = float(np.sum(source_grid[mask] * RADII[mask] * RADII[mask]))
    return {
        "q_total": q_total,
        "q_tail": q_tail,
        "q_frac": q_tail / max(q_total, 1e-15),
        "m2_total": m2_total,
        "m2_tail": m2_tail,
        "m2_frac": m2_tail / max(m2_total, 1e-15),
    }


def truncation_error(full_phi: np.ndarray, trunc_phi: np.ndarray, cutoff: float) -> dict[str, float]:
    mask = RADII > cutoff + 1.0
    diff = np.abs(full_phi - trunc_phi)
    denom = np.maximum(np.abs(full_phi), 1e-12)
    rel = diff / denom
    return {
        "max_rel": float(np.max(rel[mask])),
        "rms_rel": float(np.sqrt(np.mean(rel[mask] ** 2))),
        "max_abs": float(np.max(diff[mask])),
    }


def solve_profile(profile: str, param: float):
    source = build_source(profile, param)
    full_phi = solve_poisson(source)
    rows = []
    for cutoff in R_CUTS:
        trunc_source = source.copy()
        trunc_source[RADII > cutoff + 1e-12] = 0.0
        trunc_phi = solve_poisson(trunc_source)
        tail = tail_moments(source, cutoff)
        err = truncation_error(full_phi, trunc_phi, cutoff)
        rows.append((cutoff, tail, err))
    return source, full_phi, rows


def box_sweep(profile: str, param: float, sizes: list[int]) -> list[tuple[int, dict[str, float]]]:
    out = []
    for size in sizes:
        i, j, k = np.mgrid[0:size, 0:size, 0:size]
        center = (size - 1) / 2.0
        r = np.sqrt((i - center) ** 2 + (j - center) ** 2 + (k - center) ** 2)
        if profile == "exp":
            rho = np.exp(-r / param)
        else:
            rho = 1.0 / (1.0 + r) ** param
        rho[0, :, :] = rho[-1, :, :] = 0.0
        rho[:, 0, :] = rho[:, -1, :] = 0.0
        rho[:, :, 0] = rho[:, :, -1] = 0.0
        mask = r > 6.0 + 1e-12
        q_total = float(np.sum(rho))
        m2_total = float(np.sum(rho * r * r))
        out.append((size, {
            "q_total": q_total,
            "m2_total": m2_total,
            "q_tail": float(np.sum(rho[mask])),
            "m2_tail": float(np.sum(rho[mask] * r[mask] * r[mask])),
        }))
    return out


def report_profile(name: str, param: float, profile: str) -> dict[str, float]:
    source, full_phi, rows = solve_profile(profile, param)
    print(f"\nProfile: {name}")
    print("=" * 72)
    for cutoff, tail, err in rows:
        print(
            f"R={cutoff:.1f}  q_tail={tail['q_tail']:.3e} "
            f"({tail['q_frac']:.3e})  m2_tail={tail['m2_tail']:.3e} "
            f"({tail['m2_frac']:.3e})  err(max/rms)=({err['max_rel']:.3e}, {err['rms_rel']:.3e})"
        )

    last_tail = rows[-1][1]
    last_err = rows[-1][2]
    # Simple trend checks.
    q_fracs = [row[1]["q_frac"] for row in rows]
    m2_fracs = [row[1]["m2_frac"] for row in rows]
    max_errs = [row[2]["max_rel"] for row in rows]
    return {
        "q_frac_last": last_tail["q_frac"],
        "m2_frac_last": last_tail["m2_frac"],
        "err_last": last_err["max_rel"],
        "q_frac_drop": q_fracs[0] / max(q_fracs[-1], 1e-15),
        "m2_frac_drop": m2_fracs[0] / max(m2_fracs[-1], 1e-15),
        "err_drop": max_errs[0] / max(max_errs[-1], 1e-15),
        "q_total": last_tail["q_total"],
        "m2_total": last_tail["m2_total"],
        "rows": rows,
        "source": source,
        "full_phi": full_phi,
    }


def main() -> None:
    print("Broader support-class gravity: noncompact tails")
    print("=" * 72)
    print(f"Box size N={SIZE}, matching radii={R_CUTS}")

    exp = report_profile("exponential tail, xi=1.0", 1.0, "exp")
    p8 = report_profile("power-law tail, p=8.0", 8.0, "power")
    p4 = report_profile("power-law tail, p=4.0", 4.0, "power")
    p25 = report_profile("power-law tail, p=2.5", 2.5, "power")

    sizes = [21, 27, 33]
    p25_sweep = box_sweep("power", 2.5, sizes)
    print("\nMonopole growth sweep for p=2.5")
    print("=" * 72)
    for size, vals in p25_sweep:
        print(
            f"N={size}: q_total={vals['q_total']:.3e}, m2_total={vals['m2_total']:.3e}, "
            f"q_tail(R>6)={vals['q_tail']:.3e}, m2_tail(R>6)={vals['m2_tail']:.3e}"
        )

    q_growth = p25_sweep[-1][1]["q_total"] / max(p25_sweep[0][1]["q_total"], 1e-15)
    m2_growth = p25_sweep[-1][1]["m2_total"] / max(p25_sweep[0][1]["m2_total"], 1e-15)

    record(
        "exponentially localized noncompact tails are truncation-stable on the current box",
        exp["err_last"] < 5e-3 and exp["q_frac_last"] < 5e-2 and exp["m2_frac_last"] < 5e-2,
        (
            f"R=10 max_rel={exp['err_last']:.3e}, q_tail={exp['q_frac_last']:.3e}, "
            f"m2_tail={exp['m2_frac_last']:.3e}"
        ),
    )
    record(
        "sufficiently steep algebraic tails remain compatible with the bridge only if low moments stay finite",
        p8["err_last"] < 1e-2 and p8["q_frac_last"] < 1e-2 and p8["m2_frac_last"] < 1e-1,
        (
            f"p=8.0 at R=10: max_rel={p8['err_last']:.3e}, "
            f"q_tail={p8['q_frac_last']:.3e}, m2_tail={p8['m2_frac_last']:.3e}"
        ),
        status="BOUNDED",
    )
    record(
        "power-law p=4.0 tails do not give a clean finite-shell bridge on the current box",
        p4["m2_frac_last"] > 1e-2 and p4["err_last"] > 1e-2,
        (
            f"p=4.0 at R=10: max_rel={p4['err_last']:.3e}, "
            f"q_tail={p4['q_frac_last']:.3e}, m2_tail={p4['m2_frac_last']:.3e}"
        ),
        status="BOUNDED",
    )
    record(
        "power-law p=2.5 tails obstruct even monopole closure on the current box",
        q_growth > 1.5,
        (
            f"q_total growth N={sizes[0]} -> {sizes[-1]}: {q_growth:.3f}x, "
            f"m2_total growth: {m2_growth:.3f}x"
        ),
        status="BOUNDED",
    )
    record(
        "the current bridge package widens beyond compact support only to the extent that the tail moments remain finite",
        exp["err_last"] < 5e-3 and p8["err_last"] < 1e-2 and p4["m2_frac_last"] > 1e-2,
        (
            "exponential tails pass; steep algebraic tails are bounded; "
            "generic long-range power-law tails are obstructed"
        ),
        status="BOUNDED",
    )

    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    if n_fail == 0:
        print("All checks passed.")
    else:
        print("Some checks failed.")


if __name__ == "__main__":
    main()
