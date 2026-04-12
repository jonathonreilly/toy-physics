#!/usr/bin/env python3
"""
Size scan for the symmetry-averaged two-body partner-kick observable.

This tests whether the narrow positive window seen on the massless periodic 3D
surface is a side-9 resonance or persists at larger odd periodic lattices.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.sparse import csc_matrix
from scipy.sparse import eye as speye
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve


MASS = 0.30
DT = 0.08
N_STEPS = 8
SIGMA = 1.0
MU2 = 0.0


@dataclass
class Lattice3D:
    side: int

    def __post_init__(self):
        self.n = self.side**3
        self.coords = np.zeros((self.n, 3), dtype=int)
        for x in range(self.side):
            for y in range(self.side):
                for z in range(self.side):
                    idx = x * self.side**2 + y * self.side + z
                    self.coords[idx] = (x, y, z)
        self.x_coord = self.coords[:, 0].astype(float)
        self.center_y = self.side // 2
        self.center_z = self.side // 2
        self.adj = [[] for _ in range(self.n)]
        for x in range(self.side):
            for y in range(self.side):
                for z in range(self.side):
                    i = self.index_of(x, y, z)
                    for dx, dy, dz in (
                        (1, 0, 0),
                        (-1, 0, 0),
                        (0, 1, 0),
                        (0, -1, 0),
                        (0, 0, 1),
                        (0, 0, -1),
                    ):
                        j = self.index_of(x + dx, y + dy, z + dz)
                        if j not in self.adj[i]:
                            self.adj[i].append(j)
        self.lap = self.build_laplacian()

    def index_of(self, x: int, y: int, z: int):
        return (x % self.side) * self.side**2 + (y % self.side) * self.side + (z % self.side)

    def build_laplacian(self):
        L = lil_matrix((self.n, self.n), dtype=float)
        for i in range(self.n):
            for j in self.adj[i]:
                if j <= i:
                    continue
                L[i, j] -= 1.0
                L[j, i] -= 1.0
                L[i, i] += 1.0
                L[j, j] += 1.0
        return csc_matrix(L)

    def build_hamiltonian(self, phi: np.ndarray):
        H = lil_matrix((self.n, self.n), dtype=complex)
        for x in range(self.side):
            for y in range(self.side):
                for z in range(self.side):
                    i = self.index_of(x, y, z)
                    eps = (-1) ** (x + y + z)
                    H[i, i] = (MASS + phi[i]) * eps

                    j = self.index_of(x + 1, y, z)
                    H[i, j] += -0.5j
                    H[j, i] += 0.5j

                    j = self.index_of(x, y + 1, z)
                    eta2 = (-1) ** x
                    H[i, j] += eta2 * (-0.5j)
                    H[j, i] += eta2 * (0.5j)

                    j = self.index_of(x, y, z + 1)
                    eta3 = (-1) ** (x + y)
                    H[i, j] += eta3 * (-0.5j)
                    H[j, i] += eta3 * (0.5j)
        return csc_matrix(H)

    def cn_step(self, H: csc_matrix, psi: np.ndarray):
        I = speye(self.n, format="csc")
        A = I + 0.5j * DT * H
        B = I - 0.5j * DT * H
        return spsolve(A, B @ psi)

    def gaussian_packet(self, cx: float, mass_weight: float = 1.0):
        psi = np.zeros(self.n, dtype=complex)
        for i in range(self.n):
            dx = self.coords[i, 0] - cx
            dy = self.coords[i, 1] - self.center_y
            dz = self.coords[i, 2] - self.center_z
            dx = dx - self.side * round(dx / self.side)
            dy = dy - self.side * round(dy / self.side)
            dz = dz - self.side * round(dz / self.side)
            r2 = dx * dx + dy * dy + dz * dz
            psi[i] = np.exp(-r2 / (2 * SIGMA**2))
        norm = np.sqrt(np.sum(np.abs(psi) ** 2))
        psi *= np.sqrt(mass_weight) / norm
        return psi

    def centroid_x(self, psi: np.ndarray):
        prob = np.abs(psi) ** 2
        prob /= prob.sum()
        theta = 2 * np.pi * self.x_coord / self.side
        cx_cos = np.sum(prob * np.cos(theta))
        cx_sin = np.sum(prob * np.sin(theta))
        angle = np.arctan2(cx_sin, cx_cos)
        if angle < 0:
            angle += 2 * np.pi
        return angle * self.side / (2 * np.pi)

    def solve_phi(self, rho: np.ndarray, G_val: float):
        M = self.lap + 1e-3 * speye(self.n, format="csc")
        return spsolve(M, G_val * rho)

    def run_pair(self, cx_a: int, cx_b: int, G_val: float):
        psi_a_shared = self.gaussian_packet(cx_a, 1.0)
        psi_b_shared = self.gaussian_packet(cx_b, 1.0)
        psi_a_self = psi_a_shared.copy()
        psi_b_self = psi_b_shared.copy()

        kick_a = np.zeros(N_STEPS + 1)
        kick_b = np.zeros(N_STEPS + 1)
        for step in range(1, N_STEPS + 1):
            phi_shared = self.solve_phi(np.abs(psi_a_shared) ** 2 + np.abs(psi_b_shared) ** 2, G_val)
            H_shared = self.build_hamiltonian(phi_shared)
            psi_a_shared = self.cn_step(H_shared, psi_a_shared)
            psi_b_shared = self.cn_step(H_shared, psi_b_shared)

            phi_a = self.solve_phi(np.abs(psi_a_self) ** 2, G_val)
            phi_b = self.solve_phi(np.abs(psi_b_self) ** 2, G_val)
            H_a = self.build_hamiltonian(phi_a)
            H_b = self.build_hamiltonian(phi_b)
            psi_a_self = self.cn_step(H_a, psi_a_self)
            psi_b_self = self.cn_step(H_b, psi_b_self)

            kick_a[step] = self.centroid_x(psi_a_shared) - self.centroid_x(psi_a_self)
            kick_b[step] = self.centroid_x(psi_b_shared) - self.centroid_x(psi_b_self)
        return kick_a, kick_b

    def symmetry_stats(self, G_val: float):
        separation = self.side // 2
        start = 2
        configs = []
        for shift in (0, 1):
            left = start + shift
            right = left + separation
            configs.append((self.run_pair(left, right, G_val), +1))
            configs.append((self.run_pair(right, left, G_val), -1))

        mutual = []
        common = []
        for (kick_a, kick_b), direction in configs:
            mutual.append(direction * 0.5 * (kick_a - kick_b))
            common.append(0.5 * (kick_a + kick_b))
        mutual = np.mean(mutual, axis=0)
        common = np.mean(common, axis=0)
        return {
            "separation": separation,
            "toward_steps": int(np.sum(mutual[1:] > 0)),
            "early_toward": int(np.sum(mutual[1:6] > 0)),
            "mean_kick": float(np.mean(mutual[1:6])),
            "final_kick": float(mutual[-1]),
            "common_shift": float(np.mean(common[1:6])),
        }


def main():
    print("=" * 88)
    print("FRONTIER TWO-BODY PARTNER-KICK SIZE SCAN")
    print("massless field (mu2=0), symmetry-averaged periodic 3D surface")
    print("=" * 88)
    for side in (7, 9, 11):
        lat = Lattice3D(side)
        print(f"\nside={side}  sep={side//2}")
        for G in (10, 20, 50):
            stats = lat.symmetry_stats(G)
            print(
                f"  G={G:<3d} toward={stats['toward_steps']}/8 "
                f"early={stats['early_toward']}/5 "
                f"meanKick={stats['mean_kick']:+.6e} "
                f"finalKick={stats['final_kick']:+.6e} "
                f"commonShift={stats['common_shift']:+.6e}"
            )


if __name__ == "__main__":
    main()
