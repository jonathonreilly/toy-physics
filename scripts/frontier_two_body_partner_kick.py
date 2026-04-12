#!/usr/bin/env python3
"""
Frontier two-body partner-kick observable on a periodic 3D staggered lattice.

This is a cleaner follow-up to the raw separation-acceleration harness. It
compares two separately evolved orbitals under:

  1. SHARED self-consistent field from rho_A + rho_B
  2. SELF_ONLY field from rho_A and rho_B individually

The mutual channel is then the partner-induced centroid kick:

  kick_A(t) = x_A^shared(t) - x_A^self_only(t)
  kick_B(t) = x_B^shared(t) - x_B^self_only(t)

For a packet A to the left of packet B:
  - attraction means kick_A > 0 and kick_B < 0

To reduce parity artifacts and common-translation contamination, the script
averages over both:

  - two parity placements with the same separation
  - both left/right orientations of the pair
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.sparse import csc_matrix
from scipy.sparse import eye as speye
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve


N_SIDE = 9
N = N_SIDE**3
MASS = 0.30
DT = 0.08
N_STEPS = 8
SIGMA = 1.0
CENTER_Y = 4
CENTER_Z = 4


coords = np.zeros((N, 3), dtype=int)
for x in range(N_SIDE):
    for y in range(N_SIDE):
        for z in range(N_SIDE):
            idx = x * N_SIDE**2 + y * N_SIDE + z
            coords[idx] = (x, y, z)

x_coord = coords[:, 0].astype(float)


def index_of(x: int, y: int, z: int):
    return (x % N_SIDE) * N_SIDE**2 + (y % N_SIDE) * N_SIDE + (z % N_SIDE)


adj = [[] for _ in range(N)]
for x in range(N_SIDE):
    for y in range(N_SIDE):
        for z in range(N_SIDE):
            i = index_of(x, y, z)
            for dx, dy, dz in (
                (1, 0, 0),
                (-1, 0, 0),
                (0, 1, 0),
                (0, -1, 0),
                (0, 0, 1),
                (0, 0, -1),
            ):
                j = index_of(x + dx, y + dy, z + dz)
                if j not in adj[i]:
                    adj[i].append(j)


def build_laplacian():
    L = lil_matrix((N, N), dtype=float)
    for i in range(N):
        for j in adj[i]:
            if j <= i:
                continue
            L[i, j] -= 1.0
            L[j, i] -= 1.0
            L[i, i] += 1.0
            L[j, j] += 1.0
    return csc_matrix(L)


LAP = build_laplacian()


def build_hamiltonian(phi: np.ndarray):
    H = lil_matrix((N, N), dtype=complex)
    for x in range(N_SIDE):
        for y in range(N_SIDE):
            for z in range(N_SIDE):
                i = index_of(x, y, z)
                eps = (-1) ** (x + y + z)
                H[i, i] = (MASS + phi[i]) * eps

                j = index_of(x + 1, y, z)
                H[i, j] += -0.5j
                H[j, i] += 0.5j

                j = index_of(x, y + 1, z)
                eta2 = (-1) ** x
                H[i, j] += eta2 * (-0.5j)
                H[j, i] += eta2 * (0.5j)

                j = index_of(x, y, z + 1)
                eta3 = (-1) ** (x + y)
                H[i, j] += eta3 * (-0.5j)
                H[j, i] += eta3 * (0.5j)

    return csc_matrix(H)


def cn_step(H: csc_matrix, psi: np.ndarray):
    I = speye(N, format="csc")
    A = I + 0.5j * DT * H
    B = I - 0.5j * DT * H
    return spsolve(A, B @ psi)


def gaussian_packet(cx: float, cy: float, cz: float, sigma: float, mass_weight: float = 1.0):
    psi = np.zeros(N, dtype=complex)
    for i in range(N):
        dx = coords[i, 0] - cx
        dy = coords[i, 1] - cy
        dz = coords[i, 2] - cz
        dx = dx - N_SIDE * round(dx / N_SIDE)
        dy = dy - N_SIDE * round(dy / N_SIDE)
        dz = dz - N_SIDE * round(dz / N_SIDE)
        r2 = dx * dx + dy * dy + dz * dz
        psi[i] = np.exp(-r2 / (2 * sigma**2))
    norm = np.sqrt(np.sum(np.abs(psi) ** 2))
    if norm > 0:
        psi *= np.sqrt(mass_weight) / norm
    return psi


def centroid_x(psi: np.ndarray):
    prob = np.abs(psi) ** 2
    prob /= prob.sum()
    theta = 2 * np.pi * x_coord / N_SIDE
    cx_cos = np.sum(prob * np.cos(theta))
    cx_sin = np.sum(prob * np.sin(theta))
    angle = np.arctan2(cx_sin, cx_cos)
    if angle < 0:
        angle += 2 * np.pi
    return angle * N_SIDE / (2 * np.pi)


def solve_poisson(rho: np.ndarray, G_val: float, mu2: float, reg: float = 1e-3):
    M = LAP + (mu2 + reg) * speye(N, format="csc")
    return spsolve(M, G_val * rho)


def gradient_x(phi: np.ndarray):
    grad = np.zeros(N)
    for x in range(N_SIDE):
        for y in range(N_SIDE):
            for z in range(N_SIDE):
                i = index_of(x, y, z)
                phi_plus = phi[index_of(x + 1, y, z)]
                phi_minus = phi[index_of(x - 1, y, z)]
                grad[i] = 0.5 * (phi_plus - phi_minus)
    return grad


@dataclass
class KickSummary:
    force_a: float
    force_b: float
    kick_a: np.ndarray
    kick_b: np.ndarray


def run_pair(cx_a: int, cx_b: int, G_val: float, mu2: float, mass_b: float = 1.0):
    psi_a0 = gaussian_packet(cx_a, CENTER_Y, CENTER_Z, SIGMA, 1.0)
    psi_b0 = gaussian_packet(cx_b, CENTER_Y, CENTER_Z, SIGMA, mass_b)

    rho_a0 = np.abs(psi_a0) ** 2
    rho_b0 = np.abs(psi_b0) ** 2
    phi_a0 = solve_poisson(rho_a0, G_val, mu2)
    phi_b0 = solve_poisson(rho_b0, G_val, mu2)
    force_a = -float(np.sum(rho_a0 * gradient_x(phi_b0)))
    force_b = -float(np.sum(rho_b0 * gradient_x(phi_a0)))

    psi_a_shared = psi_a0.copy()
    psi_b_shared = psi_b0.copy()
    psi_a_self = psi_a0.copy()
    psi_b_self = psi_b0.copy()

    kick_a = np.zeros(N_STEPS + 1)
    kick_b = np.zeros(N_STEPS + 1)

    for step in range(1, N_STEPS + 1):
        rho_shared = np.abs(psi_a_shared) ** 2 + np.abs(psi_b_shared) ** 2
        phi_shared = solve_poisson(rho_shared, G_val, mu2)
        H_shared = build_hamiltonian(phi_shared)
        psi_a_shared = cn_step(H_shared, psi_a_shared)
        psi_b_shared = cn_step(H_shared, psi_b_shared)

        phi_a = solve_poisson(np.abs(psi_a_self) ** 2, G_val, mu2)
        phi_b = solve_poisson(np.abs(psi_b_self) ** 2, G_val, mu2)
        H_a = build_hamiltonian(phi_a)
        H_b = build_hamiltonian(phi_b)
        psi_a_self = cn_step(H_a, psi_a_self)
        psi_b_self = cn_step(H_b, psi_b_self)

        kick_a[step] = centroid_x(psi_a_shared) - centroid_x(psi_a_self)
        kick_b[step] = centroid_x(psi_b_shared) - centroid_x(psi_b_self)

    return KickSummary(force_a=force_a, force_b=force_b, kick_a=kick_a, kick_b=kick_b)


def symmetry_averaged_stats(separation: int, G_val: float, mu2: float, mass_b: float = 1.0):
    configs: list[tuple[KickSummary, int]] = []
    for shift in (0, 1):
        left = 2 + shift
        right = left + separation
        configs.append((run_pair(left, right, G_val, mu2, mass_b), +1))
        configs.append((run_pair(right, left, G_val, mu2, mass_b), -1))

    mutual_signed = []
    common_shift = []
    grad_diag = []
    for cfg, direction in configs:
        mutual_signed.append(direction * 0.5 * (cfg.kick_a - cfg.kick_b))
        common_shift.append(0.5 * (cfg.kick_a + cfg.kick_b))
        grad_diag.append(direction * 0.5 * (cfg.force_a - cfg.force_b))

    mutual_signed = np.mean(mutual_signed, axis=0)
    common_shift = np.mean(common_shift, axis=0)
    grad_diag = float(np.mean(grad_diag))
    toward = mutual_signed[1:] > 0
    return {
        "grad_diag": grad_diag,
        "toward_steps": int(np.sum(toward)),
        "early_toward": int(np.sum(toward[:5])),
        "mean_mutual_kick_1_5": float(np.mean(mutual_signed[1:6])),
        "final_mutual_kick": float(mutual_signed[-1]),
        "common_shift_1_5": float(np.mean(common_shift[1:6])),
    }


def print_row(label: str, stats: dict[str, float]):
    print(
        f"{label:<14s} "
        f"gradDiag={stats['grad_diag']:+.6f} "
        f"toward={stats['toward_steps']}/8 "
        f"early={stats['early_toward']}/5 "
        f"meanKick={stats['mean_mutual_kick_1_5']:+.6e} "
        f"finalKick={stats['final_mutual_kick']:+.6e} "
        f"commonShift={stats['common_shift_1_5']:+.6e}"
    )


def main():
    print("=" * 88)
    print("FRONTIER TWO-BODY PARTNER-KICK TEST")
    print("3D periodic staggered lattice, symmetry-averaged two-orbital shared vs self-only")
    print("=" * 88)

    print("\nG sweep  (sep=4, mu2=0.01)")
    for G_val in (5, 10, 20, 50, 100):
        stats = symmetry_averaged_stats(4, G_val, 0.01)
        print_row(f"G={G_val}", stats)

    print("\nSeparation sweep  (G=20, mu2=0.01)")
    for separation in (2, 3, 4):
        stats = symmetry_averaged_stats(separation, 20, 0.01)
        print_row(f"sep={separation}", stats)

    print("\nScreening sweep  (G=20, sep=4)")
    for mu2 in (0.0, 0.01, 0.05, 0.22):
        stats = symmetry_averaged_stats(4, 20, mu2)
        print_row(f"mu2={mu2:.2f}", stats)

    print("\nMass-ratio sweep  (G=20, sep=4, mass_B variable)")
    for mass_b in (1.0, 1.5, 2.0, 3.0):
        stats = symmetry_averaged_stats(4, 20, 0.01, mass_b=mass_b)
        print_row(f"mB={mass_b:.1f}", stats)

    print("\nInterpretation:")
    print("  early=5/5 with positive meanKick would be the clearest early-time mutual-attraction signal.")
    print("  Shared-vs-self-only isolates the mutual channel from self-focusing.")
    print("  commonShift near 0 means the orientation average has removed most common translation.")
    print("  gradDiag is only a partner-field gradient diagnostic, not an exact force claim.")


if __name__ == "__main__":
    main()
