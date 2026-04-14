#!/usr/bin/env python3
"""Universal tensor-kernel obstruction check for the retained gravity class.

This runner asks the exact remaining question on the current branch:

    can a single positive-definite 2x2 tensor boundary kernel K_tensor, paired
    with one microscopic source law, close both audited restricted families?

It compares the exact local O_h and finite-rank classes using the minimal
rank-two tensor block already identified on the branch and reports the sharpest
universal-kernel obstruction visible from those data.
"""

from __future__ import annotations

from dataclasses import dataclass
from _frontier_loader import load_frontier

import numpy as np


AMPLITUDE = 0.02

tcomp = load_frontier("tensor_completion", "frontier_tensorial_einstein_regge_completion.py")
same_source = load_frontier("same_source_metric", "frontier_same_source_metric_ansatz_scan.py")
coarse = load_frontier("coarse_grained", "frontier_coarse_grained_exterior_law.py")


@dataclass
class FamilyBlock:
    label: str
    kernel: np.ndarray
    eta_map: np.ndarray
    eta_floor: np.ndarray
    a_star: np.ndarray
    scalar_action: float
    mix_err_ti: float
    mix_err_tf: float


def fmt_matrix(mat: np.ndarray) -> str:
    return (
        "[["
        f"{mat[0,0]:.6e}, {mat[0,1]:.6e}"
        "],\n ["
        f"{mat[1,0]:.6e}, {mat[1,1]:.6e}"
        "]]"
    )


def rel_diff(a: np.ndarray, b: np.ndarray) -> float:
    denom = max(float(np.linalg.norm(b)), 1e-16)
    return float(np.linalg.norm(a - b) / denom)


def family_block(label: str, phi_grid) -> FamilyBlock:
    base = tcomp.probe_family("base", phi_grid, eps_vec=0.0, eps_ten=0.0, omega=0.0)
    vec = tcomp.probe_family("vec", phi_grid, eps_vec=AMPLITUDE, eps_ten=0.0, omega=1.0)
    ten = tcomp.probe_family("ten", phi_grid, eps_vec=0.0, eps_ten=AMPLITUDE, omega=1.0)
    mix = tcomp.probe_family("mix", phi_grid, eps_vec=AMPLITUDE, eps_ten=AMPLITUDE, omega=1.0)

    kernel = np.array(
        [
            [
                (vec.e_ti - base.e_ti) / AMPLITUDE,
                0.5
                * (
                    (vec.e_spatial_tf - base.e_spatial_tf) / AMPLITUDE
                    + (ten.e_ti - base.e_ti) / AMPLITUDE
                ),
            ],
            [
                0.5
                * (
                    (vec.e_spatial_tf - base.e_spatial_tf) / AMPLITUDE
                    + (ten.e_ti - base.e_ti) / AMPLITUDE
                ),
                (ten.e_spatial_tf - base.e_spatial_tf) / AMPLITUDE,
            ],
        ],
        dtype=float,
    )
    eta_map = np.array(
        [
            [
                (vec.e_ti - base.e_ti) / AMPLITUDE,
                (ten.e_ti - base.e_ti) / AMPLITUDE,
            ],
            [
                (vec.e_spatial_tf - base.e_spatial_tf) / AMPLITUDE,
                (ten.e_spatial_tf - base.e_spatial_tf) / AMPLITUDE,
            ],
        ],
        dtype=float,
    )
    eta_floor = np.array([0.0, base.e_spatial_tf], dtype=float)
    a_star = np.linalg.solve(kernel, eta_floor)

    mix_err_ti = abs(
        (mix.e_ti - base.e_ti)
        - ((vec.e_ti - base.e_ti) + (ten.e_ti - base.e_ti))
    )
    mix_err_tf = abs(
        (mix.e_spatial_tf - base.e_spatial_tf)
        - ((vec.e_spatial_tf - base.e_spatial_tf) + (ten.e_spatial_tf - base.e_spatial_tf))
    )

    print(f"{label}:")
    print(f"  scalar_action={base.scalar_action:.6e}")
    print(f"  K_tensor=\n{fmt_matrix(kernel)}")
    print(f"  eta_map=\n{fmt_matrix(eta_map)}")
    print(f"  eta_floor=[{eta_floor[0]:.6e}, {eta_floor[1]:.6e}]")
    print(f"  a_star=[{a_star[0]:.6e}, {a_star[1]:.6e}]")
    print(
        f"  mixed additivity error=[dG_0i={mix_err_ti:.3e}, dG_TF={mix_err_tf:.3e}]"
    )

    return FamilyBlock(
        label=label,
        kernel=kernel,
        eta_map=eta_map,
        eta_floor=eta_floor,
        a_star=a_star,
        scalar_action=base.scalar_action,
        mix_err_ti=mix_err_ti,
        mix_err_tf=mix_err_tf,
    )


def main() -> int:
    print("Tensor universal kernel obstruction check")
    print("=" * 78)

    oh = family_block("exact local O_h", same_source.build_best_phi_grid())
    fr = family_block("finite-rank", coarse.build_finite_rank_phi_grid())

    kernel_rel = rel_diff(oh.kernel, fr.kernel)
    eta_map_rel = rel_diff(oh.eta_map, fr.eta_map)
    eta_floor_rel = abs(
        (oh.eta_floor[1] / max(abs(oh.scalar_action), 1e-16))
        - (fr.eta_floor[1] / max(abs(fr.scalar_action), 1e-16))
    ) / max(abs(oh.eta_floor[1] / max(abs(oh.scalar_action), 1e-16)), 1e-16)
    a_rel = rel_diff(oh.a_star, fr.a_star)

    K_univ = 0.5 * (oh.kernel + fr.kernel)
    eigs = np.linalg.eigvalsh(K_univ)
    a_univ_oh = np.linalg.solve(K_univ, oh.eta_floor)
    a_univ_fr = np.linalg.solve(K_univ, fr.eta_floor)
    a_univ_rel = rel_diff(a_univ_oh, a_univ_fr)

    print("\nCross-family comparison:")
    print(f"  kernel relative difference = {kernel_rel:.6e}")
    print(f"  eta_map relative difference = {eta_map_rel:.6e}")
    print(f"  eta_floor relative difference = {eta_floor_rel:.6e}")
    print(f"  a_star relative difference = {a_rel:.6e}")
    print("\nBest common positive candidate:")
    print(f"  K_univ eigenvalues = ({eigs[0]:.6e}, {eigs[1]:.6e})")
    print(f"  a_univ(O_h) = [{a_univ_oh[0]:.6e}, {a_univ_oh[1]:.6e}]")
    print(f"  a_univ(finite-rank) = [{a_univ_fr[0]:.6e}, {a_univ_fr[1]:.6e}]")
    print(f"  a_univ relative difference = {a_univ_rel:.6e}")

    print("\nVerdict:")
    if kernel_rel < 0.05 and eta_map_rel < 0.05 and a_rel < 0.05 and a_univ_rel < 0.05:
        print(
            "A single positive 2x2 tensor kernel and source law close both audited "
            "families with the current retained tensor block."
        )
        return 0

    print(
        "No family-universal positive K_tensor is visible on the current audited "
        "restricted class. The minimal rank-two block is locally sufficient on "
        "each family, but the kernel, source map, and required completion amplitudes "
        "remain family-sensitive. An additional selector / coarse-graining / "
        "microscopic source law would be needed to make the tensor completion "
        "universal."
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

