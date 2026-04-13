#!/usr/bin/env python3
"""
Static isotropic vacuum bridge for gravity.

This is not a framework derivation of full GR. It is a bounded bridge check:
for the standard static isotropic vacuum system, the spatial conformal factor
psi and the combined lapse-density alpha*psi are both harmonic outside the
source, which fixes the isotropic Schwarzschild pair.
"""

from __future__ import annotations

import math

import numpy as np

PASS = 0
FAIL = 0


def record(name: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS"
    else:
        FAIL += 1
        tag = "FAIL"
    print(f"[{tag}] {name}")
    if detail:
        print(f"       {detail}")


def radial_laplacian(f: np.ndarray, r: np.ndarray) -> np.ndarray:
    """Spherical radial Laplacian for a radial function on a uniform grid."""
    dr = r[1] - r[0]
    df = np.gradient(f, dr, edge_order=2)
    return np.gradient(r * r * df, dr, edge_order=2) / (r * r)


def main() -> int:
    print("=" * 78)
    print("STATIC ISOTROPIC VACUUM BRIDGE")
    print("=" * 78)

    mu_values = [0.1, 0.5, 1.0]
    r = np.linspace(5.0, 300.0, 5000)

    max_lap_psi = 0.0
    max_lap_alphapsi = 0.0

    for mu in mu_values:
        psi = 1.0 + mu / r
        alpha = (1.0 - mu / r) / (1.0 + mu / r)
        alpha_psi = alpha * psi

        lap_psi = radial_laplacian(psi, r)
        lap_alpha_psi = radial_laplacian(alpha_psi, r)

        max_lap_psi = max(max_lap_psi, float(np.max(np.abs(lap_psi))))
        max_lap_alphapsi = max(max_lap_alphapsi, float(np.max(np.abs(lap_alpha_psi))))

        record(
            f"harmonic_psi_mu_{mu}",
            float(np.max(np.abs(lap_psi))) < 5e-3,
            f"max |Delta psi| = {np.max(np.abs(lap_psi)):.3e}",
        )
        record(
            f"harmonic_alpha_psi_mu_{mu}",
            float(np.max(np.abs(lap_alpha_psi))) < 5e-3,
            f"max |Delta(alpha psi)| = {np.max(np.abs(lap_alpha_psi)):.3e}",
        )

        # Weak-field checks at large r.
        r_far = 200.0
        alpha_far = (1.0 - mu / r_far) / (1.0 + mu / r_far)
        psi_far = 1.0 + mu / r_far
        lhs_alpha = alpha_far
        rhs_alpha = 1.0 - 2.0 * mu / r_far
        lhs_spatial = psi_far ** 4
        rhs_spatial = 1.0 + 4.0 * mu / r_far

        record(
            f"weak_field_alpha_mu_{mu}",
            abs(lhs_alpha - rhs_alpha) < 5e-4,
            f"alpha={lhs_alpha:.8f}, 1-2mu/r={rhs_alpha:.8f}",
        )
        record(
            f"weak_field_spatial_mu_{mu}",
            abs(lhs_spatial - rhs_spatial) < 5e-4,
            f"psi^4={lhs_spatial:.8f}, 1+4mu/r={rhs_spatial:.8f}",
        )

    # Asymptotic flatness.
    mu = 1.0
    r_inf = 1e6
    psi_inf = 1.0 + mu / r_inf
    alpha_inf = (1.0 - mu / r_inf) / (1.0 + mu / r_inf)
    record("asymptotic_psi", abs(psi_inf - 1.0) < 2e-6, f"psi(infty)={psi_inf:.12f}")
    record("asymptotic_alpha", abs(alpha_inf - 1.0) < 2e-6, f"alpha(infty)={alpha_inf:.12f}")

    # Exterior relation alpha*psi = 1 - mu/r.
    for mu in mu_values:
        sample_r = np.array([10.0, 30.0, 100.0, 250.0])
        psi = 1.0 + mu / sample_r
        alpha = (1.0 - mu / sample_r) / (1.0 + mu / sample_r)
        expected = 1.0 - mu / sample_r
        err = float(np.max(np.abs(alpha * psi - expected)))
        record(
            f"product_relation_mu_{mu}",
            err < 1e-12,
            f"max |alpha psi - (1-mu/r)| = {err:.3e}",
        )

    print()
    print("Summary")
    print(f"  max |Delta psi|       = {max_lap_psi:.3e}")
    print(f"  max |Delta(alpha psi)| = {max_lap_alphapsi:.3e}")
    print(f"  PASS={PASS}  FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
