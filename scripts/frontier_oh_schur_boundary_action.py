#!/usr/bin/env python3
"""Exact Schur-complement boundary action for the O_h strong-field shell law.

Exact content:
  1. On the exterior domain Omega_R with inner trace Gamma_R, the discrete
     harmonic extension energy is the Schur-complement boundary functional
         E_R(f) = 1/2 f^T Lambda_R f
     where Lambda_R is the exact DtN matrix of the lattice Laplacian.
  2. Its gradient equals the trace flux:
         grad E_R(f) = Lambda_R f = (H_0 u_f)|_{Gamma_R}
     for the harmonic extension u_f.
  3. For the exact local O_h and finite-rank source classes, the exact shell
     field is the unique stationary point of the sourced action
         I_R(f ; j) = 1/2 f^T Lambda_R f - j^T f
     with j given by the microscopic trace flux of the same field.

Bounded consequence:
  4. This derives the shell action from the microscopic lattice dynamics on the
     current strong-field source classes, but it still does not prove a fully
     general Einstein/Regge theorem beyond the current static conformal bridge.
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


same_source = SourceFileLoader(
    "same_source_metric",
    "/private/tmp/physics-review-active/scripts/frontier_same_source_metric_ansatz_scan.py",
).load_module()
coarse = SourceFileLoader(
    "coarse_grained",
    "/private/tmp/physics-review-active/scripts/frontier_coarse_grained_exterior_law.py",
).load_module()
finite_rank = SourceFileLoader(
    "finite_rank_metric",
    "/private/tmp/physics-review-active/scripts/frontier_finite_rank_gravity_residual.py",
).load_module()
dtn = SourceFileLoader(
    "dtn_shell",
    "/private/tmp/physics-review-active/scripts/frontier_discrete_dtn_shell_kernel.py",
).load_module()
sew = SourceFileLoader(
    "sewing_shell",
    "/private/tmp/physics-review-active/scripts/frontier_sewing_shell_source.py",
).load_module()


def schur_dtn_matrix(size: int, cutoff_radius: float):
    trace_idx, bulk_idx = dtn.exterior_sets(size, cutoff_radius)
    H0, interior = finite_rank.build_neg_laplacian_sparse(size)

    H_tt = H0[trace_idx][:, trace_idx].toarray()
    if bulk_idx.size:
        H_tb = H0[trace_idx][:, bulk_idx].toarray()
        H_bt = H0[bulk_idx][:, trace_idx].toarray()
        H_bb = H0[bulk_idx][:, bulk_idx].tocsr()
        X = spsolve(H_bb, H_bt)
        Lambda = H_tt - H_tb @ X
    else:
        Lambda = H_tt
    return Lambda, trace_idx, bulk_idx, interior


def trace_values_from_grid(grid: np.ndarray, trace_idx: np.ndarray, interior: int) -> np.ndarray:
    vals = np.zeros(trace_idx.shape[0], dtype=float)
    for row, idx in enumerate(trace_idx):
        i, j, k = dtn.full_from_flat(int(idx), interior)
        vals[row] = float(grid[i, j, k])
    return vals


def harmonic_extension_from_trace(
    trace_vals: np.ndarray, trace_idx: np.ndarray, bulk_idx: np.ndarray, size: int
) -> np.ndarray:
    return dtn.solve_exterior_dirichlet(trace_vals, trace_idx, bulk_idx, size)


def trace_flux_from_extension(ext_grid: np.ndarray, trace_idx: np.ndarray, interior: int) -> np.ndarray:
    sigma = sew.full_neg_laplacian(ext_grid)
    vals = np.zeros(trace_idx.shape[0], dtype=float)
    for row, idx in enumerate(trace_idx):
        i, j, k = dtn.full_from_flat(int(idx), interior)
        vals[row] = float(sigma[i, j, k])
    return vals


def boundary_action(Lambda: np.ndarray, f: np.ndarray, j: np.ndarray) -> tuple[float, np.ndarray]:
    grad = Lambda @ f - j
    val = 0.5 * float(f @ (Lambda @ f)) - float(j @ f)
    return val, grad


def strict_positive_gains(Lambda: np.ndarray, f: np.ndarray, j: np.ndarray) -> list[float]:
    _, base_grad = boundary_action(Lambda, f, j)
    if float(np.max(np.abs(base_grad))) > 1e-10:
        raise RuntimeError("reference point is not stationary")
    gains = []
    for idx in [0, len(f) // 2, len(f) - 1]:
        trial = f.copy()
        trial[idx] += 1e-4
        base_val, _ = boundary_action(Lambda, f, j)
        trial_val, _ = boundary_action(Lambda, trial, j)
        gains.append(float(trial_val - base_val))
    return gains


def analyze_family(
    phi_grid: np.ndarray, Lambda: np.ndarray, trace_idx: np.ndarray, bulk_idx: np.ndarray, interior: int
):
    ext = sew.exterior_projector(phi_grid, 4.0)
    f = trace_values_from_grid(ext, trace_idx, interior)
    ext_rebuilt = harmonic_extension_from_trace(f, trace_idx, bulk_idx, ext.shape[0])
    j_trace = trace_flux_from_extension(ext_rebuilt, trace_idx, interior)
    grad_expected = Lambda @ f
    return {
        "f": f,
        "ext": ext,
        "ext_rebuilt": ext_rebuilt,
        "j_trace": j_trace,
        "grad_expected": grad_expected,
        "rebuild_err": float(np.max(np.abs(ext_rebuilt - ext))),
        "flux_err": float(np.max(np.abs(grad_expected - j_trace))),
    }


def main() -> None:
    print("Exact Schur-complement boundary action for the O_h shell law")
    print("=" * 72)

    size = 15
    cutoff_radius = 4.0
    Lambda, trace_idx, bulk_idx, interior = schur_dtn_matrix(size, cutoff_radius)
    sym_err = float(np.max(np.abs(Lambda - Lambda.T)))
    eigvals = np.linalg.eigvalsh(0.5 * (Lambda + Lambda.T))
    min_eig = float(np.min(eigvals))

    oh = analyze_family(same_source.build_best_phi_grid(), Lambda, trace_idx, bulk_idx, interior)
    fr = analyze_family(coarse.build_finite_rank_phi_grid(), Lambda, trace_idx, bulk_idx, interior)

    oh_val, oh_grad = boundary_action(Lambda, oh["f"], oh["j_trace"])
    fr_val, fr_grad = boundary_action(Lambda, fr["f"], fr["j_trace"])
    oh_gains = strict_positive_gains(Lambda, oh["f"], oh["j_trace"])
    fr_gains = strict_positive_gains(Lambda, fr["f"], fr["j_trace"])

    print(
        f"trace count={len(trace_idx)}, bulk count={len(bulk_idx)}, "
        f"symmetry error={sym_err:.3e}, min eigenvalue={min_eig:.6e}"
    )
    print(
        f"exact local O_h: rebuild_err={oh['rebuild_err']:.3e}, flux_err={oh['flux_err']:.3e}, "
        f"stationary_grad={np.max(np.abs(oh_grad)):.3e}"
    )
    print(
        f"finite-rank: rebuild_err={fr['rebuild_err']:.3e}, flux_err={fr['flux_err']:.3e}, "
        f"stationary_grad={np.max(np.abs(fr_grad)):.3e}"
    )
    print(
        "sample boundary-action gains: "
        f"O_h {', '.join(f'{g:.3e}' for g in oh_gains)} ; "
        f"finite-rank {', '.join(f'{g:.3e}' for g in fr_gains)}"
    )

    record(
        "the exact exterior shell boundary action is the symmetric Schur complement of the lattice Laplacian",
        sym_err < 1e-12 and min_eig > 0.0,
        f"symmetry error={sym_err:.3e}, min eigenvalue={min_eig:.6e}",
    )
    record(
        "for the exact local O_h class the trace flux equals the gradient of the Schur boundary action exactly",
        oh["flux_err"] < 1e-12 and oh["rebuild_err"] < 1e-12,
        f"rebuild_err={oh['rebuild_err']:.3e}, flux_err={oh['flux_err']:.3e}",
    )
    record(
        "for the exact local O_h class the microscopic sourced boundary action is stationary at the exact shell trace",
        float(np.max(np.abs(oh_grad))) < 1e-12,
        f"max stationary gradient={np.max(np.abs(oh_grad)):.3e}, action={oh_val:.6e}",
    )
    record(
        "the exact local O_h shell trace is the unique local minimum of the microscopic sourced boundary action",
        all(g > 0.0 for g in oh_gains),
        "all sampled perturbation gains are strictly positive",
        status="BOUNDED",
    )
    record(
        "for the broader finite-rank class the same Schur boundary action reproduces the exact shell trace law",
        fr["flux_err"] < 1e-12 and fr["rebuild_err"] < 1e-12 and float(np.max(np.abs(fr_grad))) < 1e-12,
        (
            f"rebuild_err={fr['rebuild_err']:.3e}, flux_err={fr['flux_err']:.3e}, "
            f"max stationary gradient={np.max(np.abs(fr_grad)):.3e}"
        ),
    )
    record(
        "the current strong-field shell action is derived from microscopic lattice dynamics rather than inserted on the reduced surface",
        oh["flux_err"] < 1e-12 and float(np.max(np.abs(oh_grad))) < 1e-12,
        "exact Schur-complement boundary energy generates the shell trace law",
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
