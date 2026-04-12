#!/usr/bin/env python3
"""
Three-way SHARED / SELF_ONLY / FROZEN_SOURCE discriminator on the open 3D
Wilson lattice.

Purpose: determine whether the mutual-channel attraction signal is genuinely
dynamic (recomputed at every time-step) or merely a static-field artefact
(frozen potential computed once from the initial densities).

Three modes:
  SHARED       -- both packets source a shared gravitational field, updated
                  every step  (the full mutual channel)
  SELF_ONLY    -- each packet sees only its own field, updated every step
                  (baseline: no mutual coupling)
  FROZEN_SOURCE -- compute phi once from rho_A(0) + rho_B(0), then evolve
                   both packets in that fixed field forever

Observables per (side, distance, placement) row:
  a_mutual_shared  = a_sep(SHARED)  - a_sep(SELF_ONLY)
  a_mutual_frozen  = a_sep(FROZEN)  - a_sep(SELF_ONLY)
  discriminator    = a_mutual_shared - a_mutual_frozen

If discriminator is reliably positive (i.e. SHARED attraction is stronger
than FROZEN attraction) across the grid, the mutual channel is genuinely
dynamic.  If the discriminator is near zero or mixed-sign, the signal is
explained by the static initial field.

Uses the SAME conventions, parameters, lattice class, and early-time window
as frontier_two_body_attraction_robustness.py.
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import expm_multiply, spsolve


# ---------- parameters (identical to robustness sweep) ----------
MASS = 0.30
WILSON_R = 1.0
DT = 0.08
REG = 1e-3
N_STEPS = 15
SIGMA = 1.0
G_VAL = 5.0
MU2 = 0.001

SIDES = (18, 20, 22)
SEPARATIONS = (4, 6, 8, 10, 12)
PLACEMENT_FAMILIES = ("centered", "face_offset", "corner_offset")

EARLY = slice(2, 11)  # steps 2-10 inclusive


# ---------- data ----------
@dataclass(frozen=True)
class Placement:
    center_a: tuple[int, int, int]
    center_b: tuple[int, int, int]
    family: str


# ---------- lattice ----------
class OpenWilsonLattice:
    def __init__(self, side: int):
        self.side = side
        self.n = side**3
        self.pos = np.zeros((self.n, 3), dtype=float)
        self.adj: dict[int, list[int]] = {}
        for x in range(side):
            for y in range(side):
                for z in range(side):
                    i = self.site_index(x, y, z)
                    self.pos[i] = [x, y, z]
                    nbrs: list[int] = []
                    for dx, dy, dz in (
                        (1, 0, 0),
                        (-1, 0, 0),
                        (0, 1, 0),
                        (0, -1, 0),
                        (0, 0, 1),
                        (0, 0, -1),
                    ):
                        nx, ny, nz = x + dx, y + dy, z + dz
                        if 0 <= nx < side and 0 <= ny < side and 0 <= nz < side:
                            nbrs.append(self.site_index(nx, ny, nz))
                    self.adj[i] = nbrs
        self.lap = self.build_laplacian()

    def site_index(self, x: int, y: int, z: int) -> int:
        return x * self.side**2 + y * self.side + z

    def build_laplacian(self):
        rows, cols, vals = [], [], []
        for i in range(self.n):
            rows.append(i)
            cols.append(i)
            vals.append(-len(self.adj[i]))
            for j in self.adj[i]:
                rows.append(i)
                cols.append(j)
                vals.append(1.0)
        return sparse.csr_matrix((vals, (rows, cols)), shape=(self.n, self.n))

    def gaussian_wavepacket(self, center, sigma=SIGMA):
        psi = np.zeros(self.n, dtype=complex)
        cx, cy, cz = center
        for i in range(self.n):
            x, y, z = self.pos[i]
            r2 = (x - cx) ** 2 + (y - cy) ** 2 + (z - cz) ** 2
            psi[i] = np.exp(-r2 / (2 * sigma**2))
        psi /= np.linalg.norm(psi)
        return psi

    def solve_poisson(self, rho, G, mu2):
        A = self.lap - mu2 * sparse.eye(self.n) - REG * sparse.eye(self.n)
        rhs = -4.0 * np.pi * G * rho
        return spsolve(A.tocsc(), rhs).real

    def build_wilson_hamiltonian(self, phi):
        rows, cols, vals = [], [], []
        for i in range(self.n):
            for j in self.adj[i]:
                if j <= i:
                    continue
                rows.append(i)
                cols.append(j)
                vals.append(-0.5j + 0.5 * WILSON_R)
                rows.append(j)
                cols.append(i)
                vals.append(+0.5j + 0.5 * WILSON_R)
            diag = MASS + phi[i] + 0.5 * WILSON_R * len(self.adj[i])
            rows.append(i)
            cols.append(i)
            vals.append(diag)
        return sparse.csr_matrix((vals, (rows, cols)), shape=(self.n, self.n))

    def center_of_mass_vec(self, psi):
        rho = np.abs(psi) ** 2
        norm = max(np.sum(rho), 1e-30)
        return np.sum(rho[:, None] * self.pos, axis=0) / norm

    def evolve_step(self, psi, H):
        return expm_multiply(-1j * DT * H, psi)

    def run_mode(self, mode: str, center_a, center_b):
        """
        Evolve two packets in one of three modes.

        SHARED:        phi = Poisson(rho_A + rho_B), recomputed every step
        SELF_ONLY:     phi_A = Poisson(rho_A), phi_B = Poisson(rho_B), each step
        FROZEN_SOURCE: phi = Poisson(rho_A(0) + rho_B(0)), computed ONCE at t=0
        """
        psi_a = self.gaussian_wavepacket(center_a)
        psi_b = self.gaussian_wavepacket(center_b)

        # For FROZEN_SOURCE, compute the potential once from initial densities
        phi_frozen = None
        if mode == "FROZEN_SOURCE":
            rho_init = np.abs(psi_a) ** 2 + np.abs(psi_b) ** 2
            phi_frozen = self.solve_poisson(rho_init, G_VAL, MU2)

        com_a = np.zeros((N_STEPS + 1, 3), dtype=float)
        com_b = np.zeros((N_STEPS + 1, 3), dtype=float)
        com_a[0] = self.center_of_mass_vec(psi_a)
        com_b[0] = self.center_of_mass_vec(psi_b)

        for t in range(N_STEPS):
            if mode == "SHARED":
                rho_total = np.abs(psi_a) ** 2 + np.abs(psi_b) ** 2
                phi_shared = self.solve_poisson(rho_total, G_VAL, MU2)
                phi_a = phi_shared
                phi_b = phi_shared
            elif mode == "SELF_ONLY":
                phi_a = self.solve_poisson(np.abs(psi_a) ** 2, G_VAL, MU2)
                phi_b = self.solve_poisson(np.abs(psi_b) ** 2, G_VAL, MU2)
            elif mode == "FROZEN_SOURCE":
                phi_a = phi_frozen
                phi_b = phi_frozen
            else:
                raise ValueError(f"unknown mode: {mode}")

            H_a = self.build_wilson_hamiltonian(phi_a)
            H_b = self.build_wilson_hamiltonian(phi_b)
            psi_a = self.evolve_step(psi_a, H_a)
            psi_b = self.evolve_step(psi_b, H_b)
            psi_a /= np.linalg.norm(psi_a)
            psi_b /= np.linalg.norm(psi_b)
            com_a[t + 1] = self.center_of_mass_vec(psi_a)
            com_b[t + 1] = self.center_of_mass_vec(psi_b)

        return {
            "com_a": com_a,
            "com_b": com_b,
            "sep": np.linalg.norm(com_b - com_a, axis=1),
        }


# ---------- analysis helpers ----------
def separation_acceleration(sep):
    a = np.zeros(len(sep), dtype=float)
    a[1:-1] = (sep[2:] - 2 * sep[1:-1] + sep[:-2]) / DT**2
    a[0] = a[1]
    a[-1] = a[-2]
    return a


def placement_for(side: int, d: int, family: str) -> Placement:
    center = side // 2
    offset = max(2, side // 6)
    y = center
    z = center
    if family == "face_offset":
        y = center - offset
    elif family == "corner_offset":
        y = center - offset
        z = center - offset
    x_a = center - d // 2
    x_b = center + (d - d // 2)
    return Placement((x_a, y, z), (x_b, y, z), family)


# ---------- per-row runner ----------
def run_config(side: int, d: int, family: str):
    lat = OpenWilsonLattice(side)
    placement = placement_for(side, d, family)

    shared = lat.run_mode("SHARED", placement.center_a, placement.center_b)
    self_only = lat.run_mode("SELF_ONLY", placement.center_a, placement.center_b)
    frozen = lat.run_mode("FROZEN_SOURCE", placement.center_a, placement.center_b)

    a_shared = separation_acceleration(shared["sep"])
    a_self = separation_acceleration(self_only["sep"])
    a_frozen = separation_acceleration(frozen["sep"])

    # mutual-channel signals
    a_mutual_shared = a_shared - a_self   # existing mutual signal
    a_mutual_frozen = a_frozen - a_self   # frozen-field control
    a_discrim = a_mutual_shared - a_mutual_frozen  # what dynamic update adds

    # early-time means
    ms_mean = float(np.mean(a_mutual_shared[EARLY]))
    mf_mean = float(np.mean(a_mutual_frozen[EARLY]))
    disc_mean = float(np.mean(a_discrim[EARLY]))

    ms_std = float(np.std(a_mutual_shared[EARLY]))
    mf_std = float(np.std(a_mutual_frozen[EARLY]))
    disc_std = float(np.std(a_discrim[EARLY]))

    return {
        "side": side,
        "family": family,
        "d": d,
        "a_mutual_shared": ms_mean,
        "a_mutual_shared_std": ms_std,
        "a_mutual_frozen": mf_mean,
        "a_mutual_frozen_std": mf_std,
        "discriminator": disc_mean,
        "discriminator_std": disc_std,
        "shared_sign": "NEG" if ms_mean < -1e-8 else ("POS" if ms_mean > 1e-8 else "ZERO"),
        "frozen_sign": "NEG" if mf_mean < -1e-8 else ("POS" if mf_mean > 1e-8 else "ZERO"),
        "disc_sign": "NEG" if disc_mean < -1e-8 else ("POS" if disc_mean > 1e-8 else "ZERO"),
        "disc_positive": disc_mean > 1e-8,
        "dsep_shared": float(shared["sep"][-1] - shared["sep"][0]),
        "dsep_self": float(self_only["sep"][-1] - self_only["sep"][0]),
        "dsep_frozen": float(frozen["sep"][-1] - frozen["sep"][0]),
    }


# ---------- summary ----------
def summarize(rows):
    n = len(rows)
    disc_pos = sum(1 for r in rows if r["disc_positive"])
    disc_neg = sum(1 for r in rows if r["discriminator"] < -1e-8)
    disc_zero = n - disc_pos - disc_neg

    disc_vals = [r["discriminator"] for r in rows]
    mean_disc = float(np.mean(disc_vals))
    std_disc = float(np.std(disc_vals))

    ms_vals = [r["a_mutual_shared"] for r in rows]
    mf_vals = [r["a_mutual_frozen"] for r in rows]

    print()
    print("=" * 120)
    print("SUMMARY")
    print("=" * 120)
    print(f"Total configs: {n}")
    print(f"discriminator > 0 (SHARED stronger than FROZEN): {disc_pos}/{n}  ({100*disc_pos/n:.1f}%)")
    print(f"discriminator < 0 (FROZEN stronger than SHARED): {disc_neg}/{n}  ({100*disc_neg/n:.1f}%)")
    print(f"discriminator ~ 0 (indistinguishable):           {disc_zero}/{n}  ({100*disc_zero/n:.1f}%)")
    print()
    print(f"mean(discriminator) = {mean_disc:+.8f}")
    print(f"std(discriminator)  = {std_disc:.8f}")
    print(f"mean(a_mutual_shared)  = {float(np.mean(ms_vals)):+.8f}")
    print(f"mean(a_mutual_frozen)  = {float(np.mean(mf_vals)):+.8f}")

    # By side
    print()
    print("By side:")
    for side in SIDES:
        sub = [r for r in rows if r["side"] == side]
        dp = sum(1 for r in sub if r["disc_positive"])
        md = float(np.mean([r["discriminator"] for r in sub]))
        print(f"  side={side}: disc>0 = {dp}/{len(sub)}, mean(disc) = {md:+.8f}")

    # By family
    print()
    print("By placement family:")
    for family in PLACEMENT_FAMILIES:
        sub = [r for r in rows if r["family"] == family]
        dp = sum(1 for r in sub if r["disc_positive"])
        md = float(np.mean([r["discriminator"] for r in sub]))
        print(f"  {family:13s}: disc>0 = {dp}/{len(sub)}, mean(disc) = {md:+.8f}")

    # By separation
    print()
    print("By separation:")
    for d in SEPARATIONS:
        sub = [r for r in rows if r["d"] == d]
        dp = sum(1 for r in sub if r["disc_positive"])
        md = float(np.mean([r["discriminator"] for r in sub]))
        print(f"  d={d:2d}: disc>0 = {dp}/{len(sub)}, mean(disc) = {md:+.8f}")

    # Verdict
    print()
    print("=" * 120)
    print("VERDICT")
    print("=" * 120)
    if disc_pos >= 0.8 * n and mean_disc > 0:
        print("PASS: The mutual channel is genuinely dynamic.")
        print(f"  {disc_pos}/{n} rows show discriminator > 0.")
        print(f"  SHARED attraction is consistently stronger than FROZEN_SOURCE.")
        print("  The dynamic field update adds real signal beyond the static initial potential.")
    elif disc_pos <= 0.2 * n or mean_disc <= 0:
        print("FAIL: The mutual channel is explained by the static initial field.")
        print(f"  Only {disc_pos}/{n} rows show discriminator > 0.")
        print("  SHARED and FROZEN_SOURCE produce equivalent attraction.")
        print("  The dynamic update does not add meaningful signal.")
    else:
        print("MIXED: The discriminator shows mixed results.")
        print(f"  {disc_pos}/{n} rows show discriminator > 0.")
        print(f"  mean(discriminator) = {mean_disc:+.8f}")
        print("  The dynamic channel may contribute, but the evidence is not clean.")
    print()


# ---------- main ----------
def main():
    t0 = time.time()
    print("=" * 120)
    print("WILSON THREE-WAY DISCRIMINATOR: SHARED vs SELF_ONLY vs FROZEN_SOURCE")
    print("=" * 120)
    print(f"MASS={MASS}, WILSON_R={WILSON_R}, DT={DT}, N_STEPS={N_STEPS}, SIGMA={SIGMA}")
    print(f"G={G_VAL}, mu2={MU2}, REG={REG}")
    print(f"sides={SIDES}, separations={SEPARATIONS}")
    print(f"placement_families={PLACEMENT_FAMILIES}")
    print(f"early-time window: steps {EARLY.start}-{EARLY.stop - 1}")
    print()

    hdr = (
        f"{'side':>4s} {'family':>13s} {'d':>3s} | "
        f"{'a_mut_SH':>12s} {'a_mut_FR':>12s} {'discrim':>12s} | "
        f"{'SH_sign':>7s} {'FR_sign':>7s} {'D_sign':>7s} {'D>0':>4s} | "
        f"{'dsep_SH':>9s} {'dsep_SELF':>9s} {'dsep_FR':>9s} | "
        f"{'time':>5s}"
    )
    print(hdr)
    print("-" * len(hdr))

    rows = []
    for side in SIDES:
        for family in PLACEMENT_FAMILIES:
            for d in SEPARATIONS:
                row_start = time.time()
                row = run_config(side, d, family)
                rows.append(row)
                elapsed = time.time() - row_start
                print(
                    f"{side:4d} {family:>13s} {d:3d} | "
                    f"{row['a_mutual_shared']:+12.8f} {row['a_mutual_frozen']:+12.8f} {row['discriminator']:+12.8f} | "
                    f"{row['shared_sign']:>7s} {row['frozen_sign']:>7s} {row['disc_sign']:>7s} {'Y' if row['disc_positive'] else 'N':>4s} | "
                    f"{row['dsep_shared']:+9.5f} {row['dsep_self']:+9.5f} {row['dsep_frozen']:+9.5f} | "
                    f"{elapsed:5.1f}s"
                )

    summarize(rows)
    print(f"Total elapsed: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
