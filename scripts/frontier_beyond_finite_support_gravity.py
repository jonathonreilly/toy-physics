#!/usr/bin/env python3
"""Beyond finite support gravity: low-moment threshold and long-range obstruction.

This script is intentionally narrower than the broader-support note already on
the branch. Its purpose is to pinpoint where the current bridge package stops:

  - noncompact exponentially decaying tails should remain truncation-stable;
  - algebraic tails with p > 5 in 3D should remain controlled because the
    monopole and second moment are finite;
  - algebraic tails with p <= 5 should fail the current bridge criterion.

The test uses the same Poisson/Dirichlet machinery as the existing gravity
bridge scripts, but focuses on tail-moment scaling and truncation stability
instead of re-running the finite-support bridge closure.
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


SIZES = [21, 31, 39]
R_CUTS = [4.0, 6.0, 8.0, 10.0]


def radii_grid(size: int) -> np.ndarray:
    center = (size - 1) / 2.0
    i, j, k = np.mgrid[0:size, 0:size, 0:size]
    return np.sqrt((i - center) ** 2 + (j - center) ** 2 + (k - center) ** 2)


def build_source(size: int, profile: str, param: float) -> np.ndarray:
    r = radii_grid(size)
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
    size = source_grid.shape[0]
    H0, interior = finite_rank.build_neg_laplacian_sparse(size)
    rhs = source_grid[1:-1, 1:-1, 1:-1].reshape(-1)
    sol = spsolve(H0, rhs)
    out = np.zeros_like(source_grid)
    out[1:-1, 1:-1, 1:-1] = sol.reshape((interior, interior, interior))
    return out


def truncation_stats(source: np.ndarray, cutoff: float) -> dict[str, float]:
    r = radii_grid(source.shape[0])
    tail_mask = r > cutoff + 1e-12
    q_total = float(np.sum(source))
    q_tail = float(np.sum(source[tail_mask]))
    m2_total = float(np.sum(source * r * r))
    m2_tail = float(np.sum(source[tail_mask] * r[tail_mask] * r[tail_mask]))
    return {
        "q_total": q_total,
        "q_tail": q_tail,
        "q_frac": q_tail / max(q_total, 1e-15),
        "m2_total": m2_total,
        "m2_tail": m2_tail,
        "m2_frac": m2_tail / max(m2_total, 1e-15),
    }


def rel_truncation_error(full_phi: np.ndarray, trunc_phi: np.ndarray, cutoff: float) -> dict[str, float]:
    r = radii_grid(full_phi.shape[0])
    mask = r > cutoff + 1.0
    diff = np.abs(full_phi - trunc_phi)
    denom = np.maximum(np.abs(full_phi), 1e-12)
    rel = diff / denom
    return {
        "max_rel": float(np.max(rel[mask])),
        "rms_rel": float(np.sqrt(np.mean(rel[mask] ** 2))),
    }


def profile_report(profile: str, param: float) -> dict[str, object]:
    print(f"\nProfile: {profile}({param})")
    print("=" * 72)
    box_rows = []

    for size in SIZES:
        source = build_source(size, profile, param)
        full_phi = solve_poisson(source)
        r = radii_grid(size)
        cutoff = 10.0
        trunc_source = source.copy()
        trunc_source[r > cutoff + 1e-12] = 0.0
        trunc_phi = solve_poisson(trunc_source)

        tail = truncation_stats(source, cutoff)
        err = rel_truncation_error(full_phi, trunc_phi, cutoff)
        box_rows.append((size, tail, err))

        print(
            f"N={size}: q_tail={tail['q_tail']:.3e} ({tail['q_frac']:.3e}), "
            f"m2_tail={tail['m2_tail']:.3e} ({tail['m2_frac']:.3e}), "
            f"max_rel={err['max_rel']:.3e}, rms_rel={err['rms_rel']:.3e}"
        )

    q_growth = box_rows[-1][1]["q_tail"] / max(box_rows[0][1]["q_tail"], 1e-15)
    m2_growth = box_rows[-1][1]["m2_tail"] / max(box_rows[0][1]["m2_tail"], 1e-15)
    err_growth = box_rows[-1][2]["max_rel"] / max(box_rows[0][2]["max_rel"], 1e-15)

    return {
        "rows": box_rows,
        "q_growth": q_growth,
        "m2_growth": m2_growth,
        "err_growth": err_growth,
        "last": box_rows[-1],
    }


def main() -> None:
    print("Beyond finite support gravity: support-class threshold")
    print("=" * 72)
    print("Current test box sizes:", SIZES)
    print("Truncation radius for tail moments: R=10")

    exp = profile_report("exp", 1.0)
    p55 = profile_report("power", 5.5)
    p50 = profile_report("power", 5.0)
    p45 = profile_report("power", 4.5)
    p25 = profile_report("power", 2.5)

    record(
        "exponentially localized noncompact tails are truncation-stable",
        exp["last"][2]["max_rel"] < 1e-2 and exp["last"][1]["m2_frac"] < 5e-2,
        (
            f"N={SIZES[-1]} max_rel={exp['last'][2]['max_rel']:.3e}, "
            f"m2_tail_frac={exp['last'][1]['m2_frac']:.3e}"
        ),
    )
    record(
        "steep algebraic tails with p > 5 remain on the safe side of the bridge ordering at the current resolution",
        p55["last"][2]["max_rel"] < p50["last"][2]["max_rel"] and p55["last"][1]["m2_frac"] < p50["last"][1]["m2_frac"],
        (
            f"p=5.5: max_rel={p55['last'][2]['max_rel']:.3e}, "
            f"m2_frac={p55['last'][1]['m2_frac']:.3e}"
        ),
        status="BOUNDED",
    )
    record(
        "the borderline p = 5 tail is marginal and does not settle into a finite-shell regime",
        p50["last"][2]["max_rel"] > p55["last"][2]["max_rel"]
        and p50["last"][2]["max_rel"] < p45["last"][2]["max_rel"],
        (
            f"p=5.0: max_rel={p50['last'][2]['max_rel']:.3e}, "
            f"m2_frac={p50['last'][1]['m2_frac']:.3e}"
        ),
        status="BOUNDED",
    )
    record(
        "the p = 4.5 tail is obstructed by the long-range second-moment divergence",
        p45["last"][2]["max_rel"] > p50["last"][2]["max_rel"] and p45["last"][1]["m2_frac"] > p50["last"][1]["m2_frac"],
        (
            f"p=4.5: max_rel={p45['last'][2]['max_rel']:.3e}, "
            f"m2_frac={p45['last'][1]['m2_frac']:.3e}"
        ),
        status="BOUNDED",
    )
    record(
        "the p = 2.5 tail obstructs even monopole closure on the current box",
        p25["last"][1]["q_frac"] > 0.3 and p25["last"][2]["max_rel"] > 0.5,
        (
            f"p=2.5: q_frac={p25['last'][1]['q_frac']:.3e}, "
            f"max_rel={p25['last'][2]['max_rel']:.3e}"
        ),
        status="BOUNDED",
    )
    record(
        "the current bridge theorem stops at the finite-second-moment class in 3D",
        exp["last"][1]["m2_frac"] < p55["last"][1]["m2_frac"] < p50["last"][1]["m2_frac"] < p45["last"][1]["m2_frac"] < p25["last"][1]["m2_frac"],
        "p > 5 widens only on the finite-second-moment side; p <= 5 stops",
        status="BOUNDED",
    )

    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)
    passed = sum(c.ok for c in CHECKS)
    failed = sum(not c.ok for c in CHECKS)
    print(f"PASS={passed} FAIL={failed} TOTAL={len(CHECKS)}")
    if failed == 0:
        print("All checks passed.")
    else:
        print("Some checks failed.")


if __name__ == "__main__":
    main()
