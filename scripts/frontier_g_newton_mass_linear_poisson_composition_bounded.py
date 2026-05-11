#!/usr/bin/env python3
"""Bounded runner for G-Newton mass-linear Poisson composition.

The theorem checked here is conditional and algebraic:

    rho_mass(x; M) = M * rho_grav(x)
    (-Delta_lat) V(.; M) = rho_mass(.; M)

with -Delta_lat the nearest-neighbor graph Laplacian on a finite periodic
Z^3 lattice, solved on the zero-mean subspace. Under those hypotheses,
V(.; M) = M * V_unit follows by composition of two linear maps.

The runner does not derive the canonical mass coupling, the Poisson equation,
Newton's constant, or the parent gravity chain.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS"
    else:
        FAIL += 1
        tag = "FAIL"
    suffix = f" ({detail})" if detail else ""
    print(f"[{tag}] {label}{suffix}")


def section(title: str) -> None:
    print("\n" + "=" * 88)
    print(title)
    print("=" * 88)


def neg_lap_apply(f: np.ndarray) -> np.ndarray:
    """Apply -Delta_lat with periodic boundary conditions."""
    out = 6.0 * f
    for axis in range(3):
        out -= np.roll(f, 1, axis=axis)
        out -= np.roll(f, -1, axis=axis)
    return out


def solve_poisson_periodic(rho: np.ndarray) -> np.ndarray:
    """Solve -Delta_lat V = rho on the periodic zero-mean subspace."""
    if rho.ndim != 3 or rho.shape[0] != rho.shape[1] or rho.shape[1] != rho.shape[2]:
        raise ValueError("rho must be cubic")
    L = rho.shape[0]
    rho_zero_mean = rho - rho.mean()
    rho_k = np.fft.fftn(rho_zero_mean)
    k = 2.0 * np.pi * np.arange(L) / L
    k1, k2, k3 = np.meshgrid(k, k, k, indexing="ij")
    eig = 2.0 * (3.0 - np.cos(k1) - np.cos(k2) - np.cos(k3))
    eig_safe = eig.copy()
    eig_safe[0, 0, 0] = 1.0
    v_k = rho_k / eig_safe
    v_k[0, 0, 0] = 0.0
    return np.fft.ifftn(v_k).real


def gaussian_density(L: int, sigma: float = 1.5) -> np.ndarray:
    c = L // 2
    grid = np.arange(L)
    x, y, z = np.meshgrid(grid, grid, grid, indexing="ij")
    r2 = (x - c) ** 2 + (y - c) ** 2 + (z - c) ** 2
    rho = np.exp(-r2 / (2.0 * sigma**2))
    return rho / rho.sum()


def point_density(L: int, offset: tuple[int, int, int] | None = None) -> np.ndarray:
    c = L // 2
    if offset is None:
        offset = (0, 0, 0)
    rho = np.zeros((L, L, L), dtype=float)
    rho[(c + offset[0]) % L, (c + offset[1]) % L, (c + offset[2]) % L] = 1.0
    return rho


def rel_max(a: np.ndarray, b: np.ndarray) -> float:
    diff = float(np.max(np.abs(a - b)))
    scale = max(float(np.max(np.abs(b))), 1e-30)
    return diff / scale


def check_dependencies() -> None:
    section("Dependency packet exists")
    deps = [
        "docs/G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md",
        "docs/G_NEWTON_WEAK_FIELD_RESPONSE_BOUNDED_CLOSURE_NOTE_2026-05-10_gnewtonG3.md",
        "docs/G_NEWTON_SELF_CONSISTENCY_BOUNDED_SHARPENING_NOTE_2026-05-10_planckP4.md",
        "docs/GRAVITY_CLEAN_DERIVATION_NOTE.md",
        "docs/GRAVITY_FULL_SELF_CONSISTENCY_NOTE.md",
    ]
    for dep in deps:
        check(f"dependency source present: {dep}", (ROOT / dep).exists())


def check_laplacian_linearity() -> None:
    section("Finite-stencil Laplacian linearity")
    rng = np.random.default_rng(20260510)
    for L in (8, 16):
        f = rng.standard_normal((L, L, L))
        g = rng.standard_normal((L, L, L))
        alpha = 2.75
        beta = -1.125
        lhs = neg_lap_apply(alpha * f + beta * g)
        rhs = alpha * neg_lap_apply(f) + beta * neg_lap_apply(g)
        err = float(np.max(np.abs(lhs - rhs)))
        check(
            f"-Delta_lat(alpha f + beta g) linear on L={L}",
            err < 1e-12,
            f"max_abs_err={err:.3e}",
        )

    L = 8
    rho = point_density(L)
    lap = neg_lap_apply(rho)
    c = L // 2
    origin = lap[c, c, c]
    neighbor = lap[c + 1, c, c]
    far = lap[c + 2, c, c]
    check(
        "nearest-neighbor stencil has coefficients 6, -1, 0",
        math.isclose(origin, 6.0) and math.isclose(neighbor, -1.0) and math.isclose(far, 0.0),
        f"origin={origin}, nn={neighbor}, far={far}",
    )


def check_inverse_linearity() -> None:
    section("Periodic Poisson inverse linearity")
    rng = np.random.default_rng(37)
    L = 16
    rho1 = rng.standard_normal((L, L, L))
    rho2 = rng.standard_normal((L, L, L))
    rho1 -= rho1.mean()
    rho2 -= rho2.mean()
    alpha = 3.0
    beta = -0.4
    v1 = solve_poisson_periodic(rho1)
    v2 = solve_poisson_periodic(rho2)
    v_combo = solve_poisson_periodic(alpha * rho1 + beta * rho2)
    err = rel_max(v_combo, alpha * v1 + beta * v2)
    check(
        "(-Delta_lat)^(-1)(alpha rho1 + beta rho2) = alpha V1 + beta V2",
        err < 1e-12,
        f"rel_err={err:.3e}",
    )

    residual = neg_lap_apply(v_combo) - (alpha * rho1 + beta * rho2 - (alpha * rho1 + beta * rho2).mean())
    res_err = float(np.max(np.abs(residual)))
    check("Poisson residual closes on zero-mean source", res_err < 1e-10, f"max_abs_residual={res_err:.3e}")


def check_mass_coupling_linearity() -> None:
    section("Mass-source map linearity")
    rho = gaussian_density(10)
    masses = [0.5, 1.0, 2.0, 5.0, 10.0]
    totals = np.array([(M * rho).sum() for M in masses])
    err = float(np.max(np.abs(totals - np.array(masses))))
    check("sum_x rho_mass(x; M) = M for normalized rho_grav", err < 1e-12, f"max_abs_err={err:.3e}")

    M = 2.0
    alpha = 4.0
    scale_err = float(np.max(np.abs((alpha * M) * rho - alpha * (M * rho))))
    check("rho_mass(alpha M) = alpha rho_mass(M)", scale_err < 1e-15, f"max_abs_err={scale_err:.3e}")

    M1 = 3.0
    M2 = 7.0
    add_err = float(np.max(np.abs((M1 + M2) * rho - (M1 * rho + M2 * rho))))
    check("rho_mass(M1 + M2) = rho_mass(M1) + rho_mass(M2)", add_err < 1e-15, f"max_abs_err={add_err:.3e}")


def check_composition_linearity() -> None:
    section("End-to-end V(.; M) = M V_unit")
    for label, rho in (
        ("Gaussian", gaussian_density(16, sigma=1.7)),
        ("Point", point_density(16)),
    ):
        rho_zm = rho - rho.mean()
        v_unit = solve_poisson_periodic(rho_zm)
        max_err = 0.0
        for M in (0.5, 1.0, 2.0, 5.0, 10.0):
            v_m = solve_poisson_periodic(M * rho_zm)
            max_err = max(max_err, rel_max(v_m, M * v_unit))
        check(f"{label} source: V(M)=M V_unit for M grid", max_err < 1e-12, f"max_rel_err={max_err:.3e}")

    rho = gaussian_density(16, sigma=2.0)
    rho_zm = rho - rho.mean()
    M1 = 1.25
    M2 = 6.5
    v_sum = solve_poisson_periodic((M1 + M2) * rho_zm)
    v_parts = solve_poisson_periodic(M1 * rho_zm) + solve_poisson_periodic(M2 * rho_zm)
    err = rel_max(v_sum, v_parts)
    check("V(M1 + M2) = V(M1) + V(M2)", err < 1e-12, f"rel_err={err:.3e}")

    rho_a = point_density(16, offset=(-4, 0, 0))
    rho_b = point_density(16, offset=(4, 0, 0))
    rho_a -= rho_a.mean()
    rho_b -= rho_b.mean()
    M_a = 3.0
    M_b = 7.0
    v_combo = solve_poisson_periodic(M_a * rho_a + M_b * rho_b)
    v_parts = M_a * solve_poisson_periodic(rho_a) + M_b * solve_poisson_periodic(rho_b)
    err = rel_max(v_combo, v_parts)
    check("multi-source mass superposition is linear", err < 1e-12, f"rel_err={err:.3e}")


def main() -> int:
    print("G-Newton mass-linear Poisson composition bounded theorem")
    check_dependencies()
    check_laplacian_linearity()
    check_inverse_linearity()
    check_mass_coupling_linearity()
    check_composition_linearity()
    print("\n" + "=" * 88)
    print(f"TOTAL: PASS={PASS}, FAIL={FAIL}")
    print("=" * 88)
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
