#!/usr/bin/env python3
"""Exact same-charge common-harmonic bridge closure on current source classes.

Exact content:
  1. For an exact exterior lattice field phi_ext with shell source sigma_R and
     total shell charge Q, any common-harmonic bridge family
         psi_c = 1 + c phi_ext
         chi_c = 1 - c phi_ext
     carries shell charges +cQ and -cQ respectively.
  2. Therefore exact same-source / same-charge inheritance fixes c = 1.
  3. With c = 1, both bridge functions are exact exterior harmonic functions
     outside the sewing shell.

Bounded content:
  4. In the natural two-parameter common-harmonic metric family
         psi = 1 + b phi,   alpha psi = 1 - a phi,
     off-diagonal coefficient mismatch a != b degrades the exterior 4D vacuum
     residual by more than an order of magnitude on both current exact source
     families.
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
sew = SourceFileLoader(
    "sewing_shell",
    "/private/tmp/physics-review-active/scripts/frontier_sewing_shell_source.py",
).load_module()


def bridge_data(phi_grid: np.ndarray, cutoff_radius: float = 4.0):
    ext = sew.exterior_projector(phi_grid, cutoff_radius)
    sigma = sew.full_neg_laplacian(ext)
    total_charge = float(np.sum(sigma))
    radii = sew.radii_grid(phi_grid.shape[0])
    outside = radii > 5.0 + 1e-12
    return ext, sigma, total_charge, outside


def scaled_bridge_charge(
    ext: np.ndarray, cutoff_radius: float, coeff: float
) -> tuple[float, float]:
    psi_c = 1.0 + coeff * ext
    chi_c = 1.0 - coeff * ext
    sigma_psi = sew.full_neg_laplacian(psi_c - 1.0)
    sigma_chi = -sew.full_neg_laplacian(chi_c - 1.0)
    return float(np.sum(sigma_psi)), float(np.sum(sigma_chi))


def harmonicity_errors(ext: np.ndarray, outside_mask: np.ndarray, coeff: float) -> tuple[float, float]:
    psi_c = 1.0 + coeff * ext
    chi_c = 1.0 - coeff * ext
    lap_psi = sew.full_neg_laplacian(psi_c)
    lap_chi = sew.full_neg_laplacian(chi_c)
    return (
        float(np.max(np.abs(lap_psi[outside_mask]))),
        float(np.max(np.abs(lap_chi[outside_mask]))),
    )


def common_harmonic_metric_residual(phi_amp: float, a_coef: float, b_coef: float) -> float:
    def metric(point: np.ndarray) -> np.ndarray:
        r = max(np.linalg.norm(point), 1e-12)
        phi = phi_amp / r
        psi = 1.0 + b_coef * phi
        alpha_psi = 1.0 - a_coef * phi
        alpha = alpha_psi / psi
        return np.diag(np.array([-(alpha**2), psi**4, psi**4, psi**4], dtype=float))

    return max(
        float(np.max(np.abs(coarse.einstein_tensor(metric, p))))
        for p in coarse.probe_points(4.5)
    )


def main() -> None:
    print("Exact same-charge common-harmonic bridge closure")
    print("=" * 72)

    families = [
        ("exact local O_h", same_source.build_best_phi_grid()),
        ("exact finite-rank", coarse.build_finite_rank_phi_grid()),
    ]

    coeff_samples = [0.8, 1.0, 1.2]
    for label, phi_grid in families:
        ext, sigma, total_charge, outside = bridge_data(phi_grid)
        print(f"\n{label}: Q = {total_charge:.8f}")

        for coeff in coeff_samples:
            q_psi, q_chi = scaled_bridge_charge(ext, 4.0, coeff)
            print(
                f"  c={coeff:.1f}: Q_psi={q_psi:.8f}, Q_chi={q_chi:.8f}, "
                f"expected=+/- {coeff*total_charge:.8f}"
            )

        err_psi, err_chi = harmonicity_errors(ext, outside, 1.0)
        print(
            f"  exterior harmonicity at c=1: "
            f"max |H0 psi|={err_psi:.3e}, max |H0 chi|={err_chi:.3e}"
        )

        record(
            f"{label} common-harmonic bridge preserves exact shell charge only at c=1",
            all(
                abs(scaled_bridge_charge(ext, 4.0, c)[0] - c * total_charge) < 1e-12
                and abs(scaled_bridge_charge(ext, 4.0, c)[1] - c * total_charge) < 1e-12
                for c in coeff_samples
            ),
            (
                f"sample charges: "
                + ", ".join(
                    f"c={c:.1f}->({scaled_bridge_charge(ext, 4.0, c)[0]:.6f},"
                    f"{scaled_bridge_charge(ext, 4.0, c)[1]:.6f})"
                    for c in coeff_samples
                )
            ),
        )
        record(
            f"{label} exact same-source bridge fixes the common harmonic coefficient to c=1",
            abs(scaled_bridge_charge(ext, 4.0, 1.0)[0] - total_charge) < 1e-12
            and abs(scaled_bridge_charge(ext, 4.0, 1.0)[1] - total_charge) < 1e-12,
            f"Q={total_charge:.8f}, c=1 gives Q_psi=Q_chi={total_charge:.8f}",
        )
        record(
            f"{label} bridge functions psi=1+phi and chi=1-phi are exact exterior harmonic functions",
            err_psi < 1e-12 and err_chi < 1e-12,
            f"max (|H0 psi|, |H0 chi|)=({err_psi:.3e}, {err_chi:.3e})",
        )

    phi_oh = same_source.build_best_phi_grid()
    phi_fr = coarse.build_finite_rank_phi_grid()
    a_oh, _, _ = coarse.fit_radial_harmonic_projection(phi_oh, 4.5)
    a_fr, _, _ = coarse.fit_radial_harmonic_projection(phi_fr, 4.5)

    oh_diag = common_harmonic_metric_residual(a_oh, 1.0, 1.0)
    oh_off = min(
        common_harmonic_metric_residual(a_oh, 1.0, 0.9),
        common_harmonic_metric_residual(a_oh, 0.9, 1.0),
        common_harmonic_metric_residual(a_oh, 1.0, 1.1),
        common_harmonic_metric_residual(a_oh, 1.1, 1.0),
    )
    fr_diag = common_harmonic_metric_residual(a_fr, 1.0, 1.0)
    fr_off = min(
        common_harmonic_metric_residual(a_fr, 1.0, 0.9),
        common_harmonic_metric_residual(a_fr, 0.9, 1.0),
        common_harmonic_metric_residual(a_fr, 1.0, 1.1),
        common_harmonic_metric_residual(a_fr, 1.1, 1.0),
    )

    print("\nCommon-harmonic 4D residual support:")
    print(
        f"  exact local O_h: diag={oh_diag:.3e}, best off-diagonal={oh_off:.3e}, "
        f"penalty={oh_off/oh_diag:.1f}x"
    )
    print(
        f"  exact finite-rank: diag={fr_diag:.3e}, best off-diagonal={fr_off:.3e}, "
        f"penalty={fr_off/fr_diag:.1f}x"
    )

    record(
        "the exact local O_h common-harmonic metric strongly prefers equal spatial and temporal coefficients",
        oh_off > 20.0 * oh_diag,
        f"diag={oh_diag:.3e}, best off-diagonal={oh_off:.3e}, penalty={oh_off/oh_diag:.1f}x",
        status="BOUNDED",
    )
    record(
        "the exact finite-rank common-harmonic metric strongly prefers equal spatial and temporal coefficients",
        fr_off > 20.0 * fr_diag,
        f"diag={fr_diag:.3e}, best off-diagonal={fr_off:.3e}, penalty={fr_off/fr_diag:.1f}x",
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
