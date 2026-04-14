#!/usr/bin/env python3
"""Microscopic tensor source-to-channel map `eta` on the retained gravity class.

This runner does not redo the scalar-shell closure. It starts from the already
retained scalar bridge and measures the smallest tensor-valued source response
needed to populate the non-scalar Einstein channels.

The object of interest is the restricted Jacobian

    eta = d( G_0i, G_ij^TF ) / d( eps_vec, eps_tf )

evaluated on the scalar bridge for the exact local O_h and exact finite-rank
classes already on the branch.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib.machinery import SourceFileLoader

import numpy as np


ROOT = "/private/tmp/physics-review-active"
AMPLITUDE = 0.02

tm = SourceFileLoader(
    "tensor_matching",
    f"{ROOT}/scripts/frontier_tensor_matching_completion_theorem.py",
).load_module()


@dataclass
class FamilyEta:
    label: str
    eta: np.ndarray
    scalar_action: float
    scalar_blind: bool
    mixed_add_ti: float
    mixed_add_tf: float


def response_matrix(phi_grid) -> FamilyEta:
    base = tm.tcomp.probe_family("base", phi_grid, eps_vec=0.0, eps_ten=0.0, omega=0.0)
    vec = tm.tcomp.probe_family("vec", phi_grid, eps_vec=AMPLITUDE, eps_ten=0.0, omega=1.0)
    ten = tm.tcomp.probe_family("ten", phi_grid, eps_vec=0.0, eps_ten=AMPLITUDE, omega=1.0)
    mix = tm.tcomp.probe_family("mix", phi_grid, eps_vec=AMPLITUDE, eps_ten=AMPLITUDE, omega=1.0)

    eta = np.array(
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
    scalar_blind = (
        abs(vec.scalar_action - base.scalar_action) < 1e-14
        and abs(ten.scalar_action - base.scalar_action) < 1e-14
        and abs(mix.scalar_action - base.scalar_action) < 1e-14
    )

    mix_add_ti = abs(
        (mix.e_ti - base.e_ti)
        - ((vec.e_ti - base.e_ti) + (ten.e_ti - base.e_ti))
    )
    mix_add_tf = abs(
        (mix.e_spatial_tf - base.e_spatial_tf)
        - ((vec.e_spatial_tf - base.e_spatial_tf) + (ten.e_spatial_tf - base.e_spatial_tf))
    )

    return FamilyEta(
        label="",
        eta=eta,
        scalar_action=base.scalar_action,
        scalar_blind=scalar_blind,
        mixed_add_ti=mix_add_ti,
        mixed_add_tf=mix_add_tf,
    )


def fmt_matrix(mat: np.ndarray) -> str:
    return (
        "[["
        f"{mat[0,0]:.6e}, {mat[0,1]:.6e}"
        "],\n ["
        f"{mat[1,0]:.6e}, {mat[1,1]:.6e}"
        "]]"
    )


def main() -> int:
    print("Tensor source-to-channel map eta")
    print("=" * 76)
    print(f"source amplitude = {AMPLITUDE:.3f}")

    oh = response_matrix(tm.same_source.build_best_phi_grid())
    fr = response_matrix(tm.coarse.build_finite_rank_phi_grid())

    eta_mean = 0.5 * (oh.eta + fr.eta)
    dom_mask = np.array([[True, True], [False, True]], dtype=bool)
    dom_spread = np.max(
        np.abs(oh.eta[dom_mask] - fr.eta[dom_mask]) / np.maximum(np.abs(eta_mean[dom_mask]), 1e-12)
    )

    print("\nRestricted source-to-channel matrices:")
    print(f"  exact local O_h:\n{fmt_matrix(oh.eta)}")
    print(f"  finite-rank:\n{fmt_matrix(fr.eta)}")
    print(f"  mean:\n{fmt_matrix(eta_mean)}")
    print(f"  dominant-entry relative family spread: {dom_spread:.3e}")

    print("\nDerived diagnostics:")
    for label, fam in [("O_h", oh), ("finite-rank", fr)]:
        det = float(np.linalg.det(fam.eta))
        sv = np.linalg.svd(fam.eta, compute_uv=False)
        print(
            f"  {label}: det={det:.6e}, singular_values=({sv[0]:.6e}, {sv[1]:.6e}), "
            f"scalar_blind={fam.scalar_blind}, "
            f"additivity=(dG_0i={fam.mixed_add_ti:.3e}, dG_TF={fam.mixed_add_tf:.3e})"
        )
        print(
            f"    channel entries: vec->G_0i={fam.eta[0,0]:.6e}, "
            f"tensor->G_0i={fam.eta[0,1]:.6e}, "
            f"vec->G_TF={fam.eta[1,0]:.6e}, tensor->G_TF={fam.eta[1,1]:.6e}"
        )

    checks = [
        (
            "scalar Schur boundary action is unchanged under vector, tensor, and mixed probes",
            oh.scalar_blind and fr.scalar_blind,
        ),
        (
            "the restricted tensor source map has rank two on the exact local O_h class",
            float(np.linalg.det(oh.eta)) > 0.0,
        ),
        (
            "the restricted tensor source map has rank two on the finite-rank class",
            float(np.linalg.det(fr.eta)) > 0.0,
        ),
        (
            "mixed tensor probes are locally additive on the exact local O_h class",
            oh.mixed_add_ti < 5e-7 and oh.mixed_add_tf < 5e-7,
        ),
        (
            "mixed tensor probes are locally additive on the finite-rank class",
            fr.mixed_add_ti < 5e-7 and fr.mixed_add_tf < 5e-7,
        ),
        (
            "the tensor source map is sharply constrained rather than scalar-degenerate",
            oh.eta[0,0] > 1e-3
            and oh.eta[1,1] > 1e-2
            and fr.eta[0,0] > 1e-3
            and fr.eta[1,1] > 1e-2,
        ),
    ]

    print("\nChecks:")
    passed = 0
    for name, ok in checks:
        tag = "PASS" if ok else "FAIL"
        print(f"  [{tag}] {name}")
        passed += int(ok)
    print(f"\nSUMMARY: PASS={passed} FAIL={len(checks)-passed} TOTAL={len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
