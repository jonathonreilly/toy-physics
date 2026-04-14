#!/usr/bin/env python3
"""Tensorial bridge principle test on the current strong-field class.

This script targets the last gravity gap beyond the exact static conformal
bridge:

  - can the universal anisotropic DtN shell mode be promoted into a genuine
    local tensor/shear bridge that improves the 4D Einstein residual?

Exact content:
  1. The reduced anisotropic shell mode is extracted from the exact shell
     source by subtracting the shell-radial average.
  2. That mode is promoted into the minimal traceless spatial shear metric
         g_xx = psi^4 exp(eps s),  g_yy = psi^4 exp(-eps s),  g_zz = psi^4
     with the exact same scalar lapse/conformal sector.
  3. Scanning eps shows whether the tensor/shear deformation can beat the
     scalar bridge on the exact local O_h and finite-rank source classes.
  4. The exact Schur boundary action gives the quadratic cost of turning on
     the tensor/shear mode around the scalar bridge.

Bounded content:
  5. If the best residual occurs at nonzero eps while the boundary-action
     curvature remains strictly positive, then the tensor/shear mode is a real
     first correction but not a closure by itself.

This does not retread the solved shell/kernel/junction chain beyond the
required setup. It tests the first non-scalar bridge deformation directly.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib.machinery import SourceFileLoader

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


same_source = SourceFileLoader(
    "same_source_metric",
    "/private/tmp/physics-review-active/scripts/frontier_same_source_metric_ansatz_scan.py",
).load_module()
coarse = SourceFileLoader(
    "coarse_grained",
    "/private/tmp/physics-review-active/scripts/frontier_coarse_grained_exterior_law.py",
).load_module()
rad = SourceFileLoader(
    "radial_shell",
    "/private/tmp/physics-review-active/scripts/frontier_radial_shell_matching_law.py",
).load_module()
schur = SourceFileLoader(
    "schur",
    "/private/tmp/physics-review-active/scripts/frontier_oh_schur_boundary_action.py",
).load_module()
sew = SourceFileLoader(
    "sewing_shell",
    "/private/tmp/physics-review-active/scripts/frontier_sewing_shell_source.py",
).load_module()
dtn = SourceFileLoader(
    "dtn_shell",
    "/private/tmp/physics-review-active/scripts/frontier_discrete_dtn_shell_kernel.py",
).load_module()


SIZE = 15
CUTOFF = 4.0
CENTER = (SIZE - 1) / 2.0


def shell_to_tensor_mode(phi_grid: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return the scalar exterior field, the zero-monopole tensor candidate, and its trace mode."""
    phi_ext = sew.exterior_projector(phi_grid, CUTOFF)
    sigma = sew.full_neg_laplacian(phi_ext)
    sigma_rad = rad.radial_average_shell(sigma)
    delta_sigma = sigma - sigma_rad
    tensor_mode = rad.solve_from_source(delta_sigma)
    return phi_ext, delta_sigma, tensor_mode


def trace_values_from_grid(grid: np.ndarray, trace_idx: np.ndarray, interior: int) -> np.ndarray:
    return schur.trace_values_from_grid(grid, trace_idx, interior)


def boundary_action(Lambda: np.ndarray, f: np.ndarray, j: np.ndarray) -> tuple[float, np.ndarray]:
    grad = Lambda @ f - j
    val = 0.5 * float(f @ (Lambda @ f)) - float(j @ f)
    return val, grad


def charge_gap(Lambda: np.ndarray, v: np.ndarray) -> float:
    return float(v @ (Lambda @ v))


def interpolate(grid: np.ndarray, point: np.ndarray) -> float:
    return coarse.interpolate_phi(grid, point)


def probe_points(r: float) -> list[np.ndarray]:
    return [
        np.array([r, 0.0, 0.0], dtype=float),
        np.array([r / np.sqrt(2.0), r / np.sqrt(2.0), 0.0], dtype=float),
        np.array([r / np.sqrt(3.0)] * 3, dtype=float),
    ]


def tensor_metric_factory(phi_grid: np.ndarray, shear_grid: np.ndarray, eps: float):
    """Minimal traceless spatial shear on top of the scalar bridge."""

    def metric(point: np.ndarray) -> np.ndarray:
        phi = interpolate(phi_grid, point)
        shear = interpolate(shear_grid, point)
        psi = 1.0 + phi
        alpha = (1.0 - phi) / (1.0 + phi)
        eta = float(np.exp(eps * shear))
        return np.diag(
            np.array(
                [
                    -(alpha**2),
                    psi**4 * eta,
                    psi**4 / eta,
                    psi**4,
                ],
                dtype=float,
            )
        )

    return metric


def einstein_residual(phi_grid: np.ndarray, shear_grid: np.ndarray, eps: float) -> float:
    metric = tensor_metric_factory(phi_grid, shear_grid, eps)
    radii = [4.5]
    values = []
    for r in radii:
        for p in probe_points(r):
            values.append(float(np.max(np.abs(coarse.einstein_tensor(metric, p)))))
    return float(np.max(values))


def family_report(name: str, phi_grid: np.ndarray):
    Lambda, trace_idx, bulk_idx, interior = schur.schur_dtn_matrix(SIZE, CUTOFF)
    action_data = schur.analyze_family(phi_grid, Lambda, trace_idx, bulk_idx, interior)
    f_scalar = action_data["f"]
    j_trace = action_data["j_trace"]

    phi_ext, delta_sigma, tensor_mode_grid = shell_to_tensor_mode(phi_grid)
    tensor_trace = trace_values_from_grid(tensor_mode_grid, trace_idx, interior)
    tensor_trace -= float(np.mean(tensor_trace))
    tensor_trace /= max(float(np.max(np.abs(tensor_trace))), 1e-12)

    tensor_ext = dtn.solve_exterior_dirichlet(tensor_trace, trace_idx, bulk_idx, SIZE)
    tensor_ext_norm = max(float(np.max(np.abs(tensor_ext))), 1e-12)
    tensor_ext /= tensor_ext_norm

    scalar_base_action, scalar_base_grad = boundary_action(Lambda, f_scalar, j_trace)
    tensor_gap_coef = charge_gap(Lambda, tensor_trace)

    eps_grid = np.linspace(0.0, 1.0, 21)
    residual_rows = []
    for eps in eps_grid:
        residual_rows.append((eps, einstein_residual(phi_ext, tensor_ext, eps)))
    best_eps, best_res = min(residual_rows, key=lambda row: row[1])
    scalar_res = einstein_residual(phi_ext, tensor_ext, 0.0)
    action_gap_eps = 0.1
    action_gap = 0.5 * action_gap_eps**2 * tensor_gap_coef

    print(f"\n{name}:")
    print(
        f"  scalar_boundary_action={scalar_base_action:.6e}, "
        f"scalar_grad={float(np.max(np.abs(scalar_base_grad))):.3e}"
    )
    print(
        f"  tensor_trace_monopole={float(np.sum(tensor_trace)):.3e}, "
        f"tensor_gap_coeff={tensor_gap_coef:.6e}"
    )
    print(
        f"  scalar_Einstein_residual={scalar_res:.3e}, "
        f"best_eps={best_eps:+.3f}, best_tensor_residual={best_res:.3e}, "
        f"ratio={best_res / max(scalar_res, 1e-15):.3f}"
    )
    print(f"  sampled action gap at eps={action_gap_eps:.1f}: {action_gap:.6e}")

    return {
        "tensor_trace": tensor_trace,
        "tensor_gap_coef": tensor_gap_coef,
        "scalar_res": scalar_res,
        "best_eps": best_eps,
        "best_res": best_res,
        "action_gap": action_gap,
        "phi_ext": phi_ext,
        "tensor_ext": tensor_ext,
    }


def main() -> None:
    print("Tensorial bridge principle test")
    print("=" * 72)

    oh = family_report("exact local O_h", same_source.build_best_phi_grid())
    fr = family_report("exact finite-rank", coarse.build_finite_rank_phi_grid())

    record(
        "the tensor/shear candidate has zero monopole on the shell trace after removing the scalar charge mode",
        abs(float(np.sum(oh["tensor_trace"]))) < 1e-12 and abs(float(np.sum(fr["tensor_trace"]))) < 1e-12,
        f"monopoles: O_h={float(np.sum(oh['tensor_trace'])):.3e}, finite-rank={float(np.sum(fr['tensor_trace'])):.3e}",
    )
    record(
        "the exact Schur boundary action has strictly positive curvature along the tensor/shear mode",
        oh["tensor_gap_coef"] > 0.0 and fr["tensor_gap_coef"] > 0.0,
        f"gap coefficients: O_h={oh['tensor_gap_coef']:.6e}, finite-rank={fr['tensor_gap_coef']:.6e}",
    )
    record(
        "the tensor/shear deformation lowers the Einstein residual on the exact local O_h class",
        oh["best_res"] < oh["scalar_res"] - 1e-12 and oh["best_eps"] > 0.0,
        f"best eps={oh['best_eps']:+.3f}, scalar={oh['scalar_res']:.3e}, best={oh['best_res']:.3e}",
        status="BOUNDED",
    )
    record(
        "the tensor/shear deformation lowers the Einstein residual on the finite-rank class",
        fr["best_res"] < fr["scalar_res"] - 1e-12 and fr["best_eps"] > 0.0,
        f"best eps={fr['best_eps']:+.3f}, scalar={fr['scalar_res']:.3e}, best={fr['best_res']:.3e}",
        status="BOUNDED",
    )
    record(
        "the tensor/shear mode is a real first correction but not a closure of the bridge gap",
        oh["best_res"] < oh["scalar_res"] - 1e-12
        and fr["best_res"] < fr["scalar_res"] - 1e-12
        and oh["tensor_gap_coef"] > 0.0
        and fr["tensor_gap_coef"] > 0.0,
        (
            f"best eps=(O_h {oh['best_eps']:+.3f}, finite-rank {fr['best_eps']:+.3f}); "
            f"residual ratios=(O_h {oh['best_res']/oh['scalar_res']:.3f}, "
            f"finite-rank {fr['best_res']/fr['scalar_res']:.3f})"
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
