#!/usr/bin/env python3
"""Minimal two-field graph prototype: scalar gravity background + spinor matter.

This is intentionally lightweight. The goal is not to close a full card; it is
to answer one question:

    Is a two-field architecture more plausible than forcing gravity, spin, and
    transport into one scalar or coin-based field?

Design:
  - Scalar sector: a fixed cubic-graph gravity background Phi(x), kept simple
    and clean. It is a normalized source bump on the same lattice.
  - Spinor sector: a 4-component Dirac matter field psi(x) evolved on the same
    cubic lattice with an FFT split-step kinetic operator plus the scalar
    background as a local potential.

Diagnostics reported:
  - norm behavior
  - whether matter feels the scalar gravity signal
  - whether a spinor-specific quantity survives
  - biggest immediate blocker

The script does not modify or depend on the existing scalar/Dirac harnesses.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass

import numpy as np


# ---------------------------------------------------------------------------
# Dirac algebra
# ---------------------------------------------------------------------------

gamma0 = np.array(
    [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, -1, 0],
        [0, 0, 0, -1],
    ],
    dtype=np.complex128,
)
gamma1 = np.array(
    [
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [0, -1, 0, 0],
        [-1, 0, 0, 0],
    ],
    dtype=np.complex128,
)
gamma2 = np.array(
    [
        [0, 0, 0, -1j],
        [0, 0, 1j, 0],
        [0, 1j, 0, 0],
        [-1j, 0, 0, 0],
    ],
    dtype=np.complex128,
)
gamma3 = np.array(
    [
        [0, 0, 1, 0],
        [0, 0, 0, -1],
        [-1, 0, 0, 0],
        [0, 1, 0, 0],
    ],
    dtype=np.complex128,
)
gamma5 = 1j * gamma0 @ gamma1 @ gamma2 @ gamma3
g0g = [gamma0 @ gamma1, gamma0 @ gamma2, gamma0 @ gamma3]


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


def idx_grid(n: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    coords = np.arange(n, dtype=float)
    return np.meshgrid(coords, coords, coords, indexing="ij")


def periodic_distance(a: np.ndarray, b: float, n: int) -> np.ndarray:
    d = np.abs(a - b)
    return np.minimum(d, n - d)


def normalized_scalar_source(n: int, center: tuple[int, int, int], sigma: float = 1.6) -> np.ndarray:
    x, y, z = idx_grid(n)
    cx, cy, cz = center
    r2 = (
        periodic_distance(x, cx, n) ** 2
        + periodic_distance(y, cy, n) ** 2
        + periodic_distance(z, cz, n) ** 2
    )
    src = np.exp(-r2 / (2.0 * sigma**2))
    src = src / np.linalg.norm(src.ravel())
    return src


def scalar_potential_from_source(source: np.ndarray, strength: float) -> np.ndarray:
    # Simple attractive background: the scalar sector stays clean and local.
    return -strength * source


def positive_x_spinor() -> np.ndarray:
    # A simple upper-block spinor; enough to test survival of spinor-specific structure.
    spinor = np.array([1.0, 0.0, 0.0, 0.0], dtype=np.complex128)
    return spinor / np.linalg.norm(spinor)


def initial_spinor_packet(
    n: int,
    center: tuple[int, int, int],
    sigma: float,
    k_z: float = 0.0,
) -> np.ndarray:
    x, y, z = idx_grid(n)
    cx, cy, cz = center
    r2 = (
        periodic_distance(x, cx, n) ** 2
        + periodic_distance(y, cy, n) ** 2
        + periodic_distance(z, cz, n) ** 2
    )
    env = np.exp(-r2 / (2.0 * sigma**2))
    phase = np.exp(1j * k_z * (z - cz))
    psi = np.zeros((4, n, n, n), dtype=np.complex128)
    spin = positive_x_spinor()
    for c in range(4):
        psi[c] = spin[c] * env * phase
    psi /= np.sqrt(np.sum(np.abs(psi) ** 2))
    return psi


def dirac_kinetic_phases(n: int, mass: float, dt: float) -> np.ndarray:
    freqs = np.fft.fftfreq(n) * 2.0 * np.pi
    phases = np.zeros((n, n, n, 4, 4), dtype=np.complex128)
    for ix, kx in enumerate(freqs):
        for iy, ky in enumerate(freqs):
            for iz, kz in enumerate(freqs):
                h = mass * gamma0 + np.sin(kx) * g0g[0] + np.sin(ky) * g0g[1] + np.sin(kz) * g0g[2]
                eigvals, eigvecs = np.linalg.eigh(h)
                u = eigvecs @ np.diag(np.exp(-0.5j * dt * eigvals)) @ eigvecs.conj().T
                phases[ix, iy, iz] = u
    return phases


def apply_kinetic(psi: np.ndarray, kin_phases: np.ndarray) -> np.ndarray:
    psi_k = np.fft.fftn(psi, axes=(1, 2, 3))
    out_k = np.zeros_like(psi_k)
    for a in range(4):
        for b in range(4):
            out_k[a] += kin_phases[:, :, :, a, b] * psi_k[b]
    return np.fft.ifftn(out_k, axes=(1, 2, 3))


def apply_potential(psi: np.ndarray, potential: np.ndarray, dt: float, matter_mass: float) -> np.ndarray:
    phase = np.exp(-1j * matter_mass * potential * dt)
    out = np.zeros_like(psi)
    for c in range(4):
        out[c] = psi[c] * phase
    return out


def evolve_spinor(
    psi0: np.ndarray,
    potential: np.ndarray,
    mass: float,
    dt: float,
    steps: int,
) -> tuple[np.ndarray, list[float]]:
    n = psi0.shape[1]
    kin = dirac_kinetic_phases(n, mass, dt)
    psi = psi0.copy()
    norms = [float(np.sum(np.abs(psi) ** 2))]
    for _ in range(steps):
        psi = apply_kinetic(psi, kin)
        psi = apply_potential(psi, potential, dt, mass)
        psi = apply_kinetic(psi, kin)
        norms.append(float(np.sum(np.abs(psi) ** 2)))
    return psi, norms


def centroid_z(psi: np.ndarray) -> float:
    rho = np.sum(np.abs(psi) ** 2, axis=0)
    n = rho.shape[0]
    coords = np.arange(n, dtype=float) - n // 2
    marginal = np.sum(rho, axis=(0, 1))
    total = float(np.sum(marginal))
    return float(np.dot(coords, marginal) / total) if total > 0 else 0.0


def gamma5_expectation(psi: np.ndarray) -> float:
    total = float(np.sum(np.abs(psi) ** 2))
    if total <= 1e-30:
        return 0.0
    g5 = np.zeros_like(psi)
    for a in range(4):
        for b in range(4):
            g5[a] += gamma5[a, b] * psi[b]
    inner = np.sum(np.conjugate(psi) * g5)
    return float(np.real(inner) / total)


def upper_lower_imbalance(psi: np.ndarray) -> float:
    upper = float(np.sum(np.abs(psi[0]) ** 2) + np.sum(np.abs(psi[1]) ** 2))
    lower = float(np.sum(np.abs(psi[2]) ** 2) + np.sum(np.abs(psi[3]) ** 2))
    total = upper + lower
    return (upper - lower) / total if total > 1e-30 else 0.0


@dataclass
class CaseResult:
    strength: float
    free_cz: float
    grav_cz: float
    delta_cz: float
    norm_drift: float
    g5_initial: float
    g5_final: float
    block_initial: float
    block_final: float


def run_case(
    n: int,
    steps: int,
    dt: float,
    matter_mass: float,
    source_strength: float,
    source_offset: int,
    sigma: float,
    carrier_k: float,
) -> CaseResult:
    center = n // 2
    source_pos = (center, center, center + source_offset)
    source = normalized_scalar_source(n, source_pos, sigma=sigma)
    potential = scalar_potential_from_source(source, source_strength)

    psi0 = initial_spinor_packet(n, (center, center, center), sigma=sigma, k_z=carrier_k)
    free_final, free_norms = evolve_spinor(psi0, np.zeros_like(potential), matter_mass, dt, steps)
    grav_final, grav_norms = evolve_spinor(psi0, potential, matter_mass, dt, steps)

    return CaseResult(
        strength=source_strength,
        free_cz=centroid_z(free_final),
        grav_cz=centroid_z(grav_final),
        delta_cz=centroid_z(grav_final) - centroid_z(free_final),
        norm_drift=max(
            max(abs(v - free_norms[0]) for v in free_norms),
            max(abs(v - grav_norms[0]) for v in grav_norms),
        ),
        g5_initial=gamma5_expectation(psi0),
        g5_final=gamma5_expectation(grav_final),
        block_initial=upper_lower_imbalance(psi0),
        block_final=upper_lower_imbalance(grav_final),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Scalar gravity background + spinor matter on a cubic graph.")
    parser.add_argument("--n", type=int, default=17)
    parser.add_argument("--steps", type=int, default=14)
    parser.add_argument("--dt", type=float, default=0.25)
    parser.add_argument("--matter-mass", type=float, default=0.22)
    parser.add_argument("--sigma", type=float, default=1.7)
    parser.add_argument("--carrier-k", type=float, default=0.0)
    parser.add_argument("--source-offset", type=int, default=3)
    parser.add_argument("--strengths", type=float, nargs="+", default=[2e-4, 5e-4, 1e-3])
    args = parser.parse_args()

    center = args.n // 2
    source = normalized_scalar_source(args.n, (center, center, center + args.source_offset), sigma=args.sigma)
    source_norm = float(np.linalg.norm(source.ravel()))

    print("=" * 72)
    print("GRAPH SCALAR + SPINOR")
    print("=" * 72)
    print(f"  n={args.n}, steps={args.steps}, dt={args.dt}, matter_mass={args.matter_mass}")
    print(f"  source_offset={args.source_offset}, sigma={args.sigma}, carrier_k={args.carrier_k}")
    print(f"  scalar background norm = {source_norm:.6f}")
    print()

    results: list[CaseResult] = []
    for strength in args.strengths:
        result = run_case(
            n=args.n,
            steps=args.steps,
            dt=args.dt,
            matter_mass=args.matter_mass,
            source_strength=strength,
            source_offset=args.source_offset,
            sigma=args.sigma,
            carrier_k=args.carrier_k,
        )
        results.append(result)
        print(f"[strength={strength:.1e}] norm_drift={result.norm_drift:.3e} "
              f"delta_cz={result.delta_cz:+.4e} "
              f"g5:{result.g5_initial:+.3f}->{result.g5_final:+.3f} "
              f"block:{result.block_initial:+.3f}->{result.block_final:+.3f}")

    norm_ok = max(r.norm_drift for r in results) < 1e-10
    signal_ok = all(r.delta_cz > 0 for r in results)
    spinor_ok = any(abs(r.g5_final) > 0.05 for r in results) or any(abs(r.block_final) > 0.05 for r in results)
    blocker = "one-way scalar background only; no spinor backreaction" if signal_ok else "matter response is still too weak or sign-unstable"

    print("\nSummary")
    print(f"  norm behavior: {'PASS' if norm_ok else 'FAIL'} (matter norm drift <= machine epsilon)")
    print(f"  scalar gravity signal: {'PASS' if signal_ok else 'FAIL'} (matter centroid shifts toward source)")
    print(f"  spinor-specific quantity: {'PASS' if spinor_ok else 'FAIL'} (gamma5 / block imbalance survives)")
    print(f"  immediate blocker: {blocker}")


if __name__ == "__main__":
    main()
