#!/usr/bin/env python3
"""Generic finite-support Schur bridge closure on the current static bridge.

Exact content:
  1. Any finite-support positive-semidefinite source operator
         H_W = H_0 - P W P^T
     has the exact compressed-source field
         phi = G_0 P (I - W G_S)^-1 m.
  2. For the exterior projector phi_ext, the native same-charge bridge
         psi = 1 + phi_ext
         chi = 1 - phi_ext = alpha * psi
     and the local fields
         rho = sigma_R / (2 pi psi^5)
         S   = 0.5 rho (1/alpha - 1)
     satisfy the static conformal constraint pair exactly.
  3. The same microscopic Schur-complement boundary action remains stationary
     at the exact shell trace.

Bounded content:
  4. The theorem is verified on several genuinely non-star finite-support
     source geometries sampled on the same Dirichlet box.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib.machinery import SourceFileLoader
from itertools import product

import numpy as np


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
static_lift = SourceFileLoader(
    "static_lift",
    "/private/tmp/physics-review-active/scripts/frontier_oh_static_constraint_lift.py",
).load_module()
schur = SourceFileLoader(
    "schur",
    "/private/tmp/physics-review-active/scripts/frontier_oh_schur_boundary_action.py",
).load_module()


SIZE = 15
INTERIOR = SIZE - 2
CENTER = INTERIOR // 2


def nonstar_offsets(seed: int, n_sites: int) -> list[tuple[int, int, int]]:
    rng = np.random.default_rng(seed)
    pool: list[tuple[int, int, int]] = []
    for dx, dy, dz in product(range(-2, 3), repeat=3):
        if dx == dy == dz == 0:
            continue
        nnz = sum(v != 0 for v in (dx, dy, dz))
        if nnz < 2:
            continue
        if dx * dx + dy * dy + dz * dz > 8:
            continue
        pool.append((dx, dy, dz))

    rng.shuffle(pool)
    corner_pool = [
        (1, 1, 1),
        (1, 1, -1),
        (1, -1, 1),
        (-1, 1, 1),
        (-1, -1, 1),
    ]
    chosen = [(0, 0, 0), corner_pool[seed % len(corner_pool)]]
    used = set(chosen)
    for off in pool:
        if off in used:
            continue
        chosen.append(off)
        used.add(off)
        if len(chosen) == n_sites:
            break
    if len(chosen) != n_sites:
        raise RuntimeError("failed to build non-star finite support")
    return chosen


def support_is_nonstar(offsets: list[tuple[int, int, int]]) -> bool:
    return any(sum(v != 0 for v in off) >= 2 for off in offsets if off != (0, 0, 0))


def build_generic_finite_support_phi_grid(seed: int, n_sites: int):
    size = SIZE
    H0, interior = finite_rank.build_neg_laplacian_sparse(size)
    support_offsets = nonstar_offsets(seed, n_sites)
    support = [
        finite_rank.flat_idx(CENTER + dx, CENTER + dy, CENTER + dz, interior)
        for dx, dy, dz in support_offsets
    ]
    G0P = finite_rank.solve_columns(H0, support)
    GS = G0P[support, :]

    rng = np.random.default_rng(seed + 991)
    A = rng.normal(size=(n_sites, n_sites))
    W_raw = A @ A.T
    rho = max(abs(ev) for ev in np.linalg.eigvals(W_raw @ GS))
    scale = 0.42 / rho
    W = scale * W_raw

    masses = rng.uniform(0.55, 1.10, size=n_sites)
    q_eff = np.linalg.solve(np.eye(n_sites) - W @ GS, masses)
    phi_flat = G0P @ q_eff

    phi_grid = np.zeros((size, size, size), dtype=float)
    phi_grid[1:-1, 1:-1, 1:-1] = phi_flat.reshape((interior, interior, interior))

    return phi_grid, support_offsets


def main() -> None:
    print("Generic finite-support Schur bridge closure")
    print("=" * 72)

    Lambda, trace_idx, bulk_idx, interior = schur.schur_dtn_matrix(SIZE, 4.0)

    seeds = [4, 9, 14]
    sizes = [6, 8, 10]
    shell_band = []
    res_psi = []
    res_chi = []
    grad_err = []
    rebuild_err = []
    nonstar_flags = []

    for seed, n_sites in zip(seeds, sizes):
        phi_grid, offsets = build_generic_finite_support_phi_grid(seed, n_sites)
        nonstar_flags.append(support_is_nonstar(offsets))

        family = static_lift.analyze_family(phi_grid)
        shell_band.append((family["shell_support_min"], family["shell_support_max"]))
        res_psi.append(float(np.max(np.abs(family["res_psi"]))))
        res_chi.append(float(np.max(np.abs(family["res_chi"]))))

        action = schur.analyze_family(phi_grid, Lambda, trace_idx, bulk_idx, interior)
        grad_err.append(float(np.max(np.abs(action["grad_expected"] - action["j_trace"]))))
        rebuild_err.append(action["rebuild_err"])

        print(
            f"seed={seed}, n_sites={n_sites}, support={offsets}: "
            f"band=[{family['shell_support_min']:.6f}, {family['shell_support_max']:.6f}], "
            f"max residuals=(psi={res_psi[-1]:.3e}, chi={res_chi[-1]:.3e}), "
            f"action errs=(rebuild={rebuild_err[-1]:.3e}, grad={grad_err[-1]:.3e})"
        )

    shell_min = min(b[0] for b in shell_band)
    shell_max = max(b[1] for b in shell_band)

    record(
        "the sampled finite supports are genuinely non-star support geometries",
        all(nonstar_flags),
        "all sampled supports contain diagonal off-axis support points",
    )
    record(
        "every sampled finite-support field keeps the exact shell source on the sewing band 3 < r <= 5",
        shell_min > 3.0 and shell_max <= 5.0 + 1e-12,
        f"shell band envelope=[{shell_min:.6f}, {shell_max:.6f}] across {len(seeds)} samples",
    )
    record(
        "every sampled finite-support field satisfies the first local static conformal constraint exactly",
        max(res_psi) < 1e-12,
        f"max sampled psi residual={max(res_psi):.3e}",
    )
    record(
        "every sampled finite-support field satisfies the second local static conformal constraint exactly",
        max(res_chi) < 1e-12,
        f"max sampled chi residual={max(res_chi):.3e}",
    )
    record(
        "every sampled finite-support field is stationary for the same microscopic Schur boundary action",
        max(grad_err) < 1e-12 and max(rebuild_err) < 1e-12,
        f"max sampled (rebuild,grad)=({max(rebuild_err):.3e}, {max(grad_err):.3e})",
    )
    record(
        "the bridge-side exact closure package extends beyond the star-supported finite-rank benchmark class to generic finite support",
        all(nonstar_flags)
        and max(res_psi) < 1e-12
        and max(res_chi) < 1e-12
        and max(grad_err) < 1e-12,
        "exact shell source + exact static constraints + exact microscopic boundary action",
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
