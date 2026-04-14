#!/usr/bin/env python3
"""Localize the remaining tensor-transfer gap to intra-orbit shell structure.

This runner uses the exact retained shell/source toolbox already on the branch:

  - projector-shell source law
  - exact reduced shell law
  - exact DtN anisotropic orbit mode

It asks a sharper question than the previous transfer obstruction:

    if tau_tensor is not fixed by the current retained shell data, what
    microscopic shell datum is still missing?

The answer on the audited restricted class is:

  - orbit-summed shell source data are identical across the exact local O_h
    and finite-rank families
  - but the finite-rank family has nonzero intra-orbit shell-source fine
    structure while the exact local O_h family does not

So the remaining tensor-transfer law must use intra-orbit shell structure, not
just orbit sums or other reduced shell observables.
"""

from __future__ import annotations

from collections import defaultdict
from contextlib import redirect_stdout
from dataclasses import dataclass
from importlib.machinery import SourceFileLoader
from io import StringIO

import numpy as np


ROOT = "/private/tmp/physics-review-active"

sew = SourceFileLoader(
    "sewing_shell",
    f"{ROOT}/scripts/frontier_sewing_shell_source.py",
).load_module()
utk = SourceFileLoader(
    "tensor_universal_kernel",
    f"{ROOT}/scripts/frontier_tensor_universal_kernel.py",
).load_module()
same_source = SourceFileLoader(
    "same_source_metric",
    f"{ROOT}/scripts/frontier_same_source_metric_ansatz_scan.py",
).load_module()
coarse = SourceFileLoader(
    "coarse_grained",
    f"{ROOT}/scripts/frontier_coarse_grained_exterior_law.py",
).load_module()


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    status: str


CHECKS: list[Check] = []

SIZE = 15
CENTER = (SIZE - 1) // 2
RADII = sew.radii_grid(SIZE)
BAND_MASK = (RADII > 3.0 + 1e-12) & (RADII <= 5.0 + 1e-12)


def record(name: str, ok: bool, detail: str, status: str = "EXACT") -> None:
    CHECKS.append(Check(name=name, ok=ok, detail=detail, status=status))
    tag = "PASS" if ok else "FAIL"
    print(f"[{status}] {tag}: {name}")
    if detail:
        print(f"    {detail}")


def orbit_key(i: int, j: int, k: int) -> tuple[int, int, int]:
    return tuple(sorted([abs(i - CENTER), abs(j - CENTER), abs(k - CENTER)], reverse=True))


def normalized_shell_source(phi_grid: np.ndarray) -> np.ndarray:
    sigma = sew.full_neg_laplacian(sew.exterior_projector(phi_grid, 4.0))
    q = float(np.sum(sigma))
    return sigma / q


def orbit_stats(source_grid: np.ndarray) -> dict[tuple[int, int, int], dict[str, float]]:
    values: dict[tuple[int, int, int], list[float]] = defaultdict(list)
    for i in range(SIZE):
        for j in range(SIZE):
            for k in range(SIZE):
                if not BAND_MASK[i, j, k]:
                    continue
                val = float(source_grid[i, j, k])
                if abs(val) < 1e-14:
                    continue
                values[orbit_key(i, j, k)].append(val)

    out: dict[tuple[int, int, int], dict[str, float]] = {}
    for key, vals in values.items():
        arr = np.array(vals, dtype=float)
        out[key] = {
            "mean": float(np.mean(arr)),
            "std": float(np.std(arr)),
            "count": float(arr.size),
        }
    return out


def max_mean_diff(
    a: dict[tuple[int, int, int], dict[str, float]],
    b: dict[tuple[int, int, int], dict[str, float]],
) -> float:
    keys = sorted(set(a) | set(b))
    return max(abs(a[k]["mean"] - b[k]["mean"]) for k in keys)


def max_std(values: dict[tuple[int, int, int], dict[str, float]]) -> float:
    return max(v["std"] for v in values.values())


def weighted_rms_std(values: dict[tuple[int, int, int], dict[str, float]]) -> float:
    num = sum(v["count"] * (v["std"] ** 2) for v in values.values())
    den = sum(v["count"] for v in values.values())
    return float(np.sqrt(num / max(den, 1.0)))


def main() -> int:
    print("Tensor transfer localization to intra-orbit shell structure")
    print("=" * 78)

    phi_oh = same_source.build_best_phi_grid()
    phi_fr = coarse.build_finite_rank_phi_grid()
    src_oh = normalized_shell_source(phi_oh)
    src_fr = normalized_shell_source(phi_fr)

    stats_oh = orbit_stats(src_oh)
    stats_fr = orbit_stats(src_fr)

    mean_diff = max_mean_diff(stats_oh, stats_fr)
    max_std_oh = max_std(stats_oh)
    max_std_fr = max_std(stats_fr)
    rms_std_oh = weighted_rms_std(stats_oh)
    rms_std_fr = weighted_rms_std(stats_fr)

    with redirect_stdout(StringIO()):
        blk_oh = utk.family_block("exact local O_h", phi_oh)
        blk_fr = utk.family_block("finite-rank", phi_fr)
    c_eta_oh = float(blk_oh.eta_floor[1] / abs(blk_oh.scalar_action))
    c_eta_fr = float(blk_fr.eta_floor[1] / abs(blk_fr.scalar_action))
    # Use the retained selector-transfer normalization c_eta / c_aniso from the
    # exact reduced shell law.
    shell = SourceFileLoader(
        "one_parameter_shell",
        f"{ROOT}/scripts/frontier_one_parameter_reduced_shell_law.py",
    ).load_module()
    c_aniso_oh = float(shell.reduced_data(phi_oh)["anchor_per_Q"])
    c_aniso_fr = float(shell.reduced_data(phi_fr)["anchor_per_Q"])
    tau_oh = c_eta_oh / c_aniso_oh
    tau_fr = c_eta_fr / c_aniso_fr
    tau_rel = abs(tau_oh - tau_fr) / max(abs(tau_oh), 1e-16)

    print("Orbit-summed shell-source comparison:")
    print(f"  max orbit-mean difference = {mean_diff:.3e}")
    print("\nIntra-orbit shell-source fine structure:")
    print(f"  exact local O_h max orbit std = {max_std_oh:.3e}")
    print(f"  exact local O_h weighted rms std = {rms_std_oh:.3e}")
    print(f"  finite-rank max orbit std = {max_std_fr:.3e}")
    print(f"  finite-rank weighted rms std = {rms_std_fr:.3e}")
    print("\nSelector-transfer mismatch:")
    print(f"  tau_tensor(O_h) = {tau_oh:.6e}")
    print(f"  tau_tensor(finite-rank) = {tau_fr:.6e}")
    print(f"  tau_tensor relative difference = {tau_rel:.6e}")

    record(
        "the exact local O_h and finite-rank families have identical orbit-summed shell-source data on the sewing band",
        mean_diff < 1e-12,
        f"max orbit-mean difference={mean_diff:.3e}",
    )
    record(
        "the exact local O_h shell source is orbit-constant on each active shell orbit",
        max_std_oh < 1e-12 and rms_std_oh < 1e-12,
        f"max orbit std={max_std_oh:.3e}, weighted rms std={rms_std_oh:.3e}",
    )
    record(
        "the finite-rank shell source carries nonzero intra-orbit shell fine structure",
        max_std_fr > 1e-5 and rms_std_fr > 1e-5,
        f"max orbit std={max_std_fr:.6e}, weighted rms std={rms_std_fr:.6e}",
        status="BOUNDED",
    )
    record(
        "the remaining tau_tensor mismatch therefore cannot be determined by orbit-summed shell-source data alone",
        mean_diff < 1e-12 and max_std_oh < 1e-12 and max_std_fr > 1e-5 and tau_rel > 5e-2,
        (
            f"identical orbit means with tau mismatch={tau_rel:.6e}; "
            "the distinguishing datum is intra-orbit shell fine structure"
        ),
    )

    print("\nVerdict:")
    print(
        "The missing tensor-transfer theorem is now localized to microscopic "
        "intra-orbit shell structure on the sewing band. Orbit sums, shell "
        "means, and the reduced DtN mode are already exhausted on the audited "
        "restricted class."
    )

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    if n_fail == 0:
        print("All checks passed.")
        return 0
    print("Some checks failed.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
