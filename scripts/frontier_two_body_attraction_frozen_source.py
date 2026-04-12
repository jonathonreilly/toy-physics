#!/usr/bin/env python3
"""
Frozen-source follow-up for the bounded Wilson two-body attraction lane.

This stays on the same low-screening open-Wilson convention as the current
bounded side-lane result and asks a narrower question:

Does the early-time near-inverse-square mutual-attraction law survive when the
field is frozen from the initial density instead of being recomputed from the
evolving packets?

This script intentionally does not widen the geometry class. It keeps:
  - open 3D cubic Wilson lattice
  - centered x-axis packet placements
  - MASS=0.3, WILSON_R=1.0
  - G=5, mu2=0.001
  - sigma=1.0, DT=0.08

It varies:
  - trace length
  - analysis window
  - field mode: SHARED, SELF_ONLY, FROZEN_SOURCE

The retained observable remains:
  a_mutual(t) = a_sep(shared) - a_sep(self_only)

and the fit is always taken on early-time absolute means |a_mutual| for the
named window on rows that stay attractive for that same window.
"""

from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import expm_multiply, spsolve


MASS = 0.30
WILSON_R = 1.0
DT = 0.08
REG = 1e-3
SIGMA = 1.0
G_VAL = 5.0
MU2 = 0.001

SIDE = 20
DEFAULT_SEPARATIONS = (4, 6, 8, 10, 12)
DEFAULT_TRACE_STEPS = (15, 25, 35)
WINDOWS = {
    15: (("w2_10", 2, 11), ("w3_11", 3, 12), ("w6_14", 6, 15)),
    25: (("w2_10", 2, 11), ("w6_14", 6, 15), ("w10_18", 10, 19), ("w14_22", 14, 23)),
    35: (("w2_10", 2, 11), ("w10_18", 10, 19), ("w18_26", 18, 27), ("w26_34", 26, 35)),
}


@dataclass(frozen=True)
class Placement:
    center_a: tuple[int, int, int]
    center_b: tuple[int, int, int]


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

    def run_mode(self, mode: str, placement: Placement, n_steps: int):
        psi_a = self.gaussian_wavepacket(placement.center_a)
        psi_b = self.gaussian_wavepacket(placement.center_b)
        rho_frozen = np.abs(psi_a) ** 2 + np.abs(psi_b) ** 2
        phi_frozen = self.solve_poisson(rho_frozen, G_VAL, MU2)

        com_a = np.zeros((n_steps + 1, 3), dtype=float)
        com_b = np.zeros((n_steps + 1, 3), dtype=float)
        com_a[0] = self.center_of_mass_vec(psi_a)
        com_b[0] = self.center_of_mass_vec(psi_b)

        for t in range(n_steps):
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
                raise ValueError(f"unsupported mode: {mode}")

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


def centered_placement(side: int, d: int) -> Placement:
    center = side // 2
    x_a = center - d // 2
    x_b = center + (d - d // 2)
    return Placement((x_a, center, center), (x_b, center, center))


def separation_acceleration(sep):
    a = np.zeros(len(sep), dtype=float)
    a[1:-1] = (sep[2:] - 2 * sep[1:-1] + sep[:-2]) / DT**2
    a[0] = a[1]
    a[-1] = a[-2]
    return a


def power_law_fit(xs, ys):
    lx = np.log(np.asarray(xs, dtype=float))
    ly = np.log(np.asarray(ys, dtype=float))
    slope, intercept = np.polyfit(lx, ly, 1)
    fit = slope * lx + intercept
    ss_res = float(np.sum((ly - fit) ** 2))
    ss_tot = float(np.sum((ly - np.mean(ly)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
    return slope, r2


def projected_pair_motion(mode_a, mode_b, initial_vec):
    u = initial_vec / max(np.linalg.norm(initial_vec), 1e-30)
    dx_a = np.dot(mode_a["com_a"][-1] - mode_b["com_a"][-1], u)
    dx_b = np.dot(mode_a["com_b"][-1] - mode_b["com_b"][-1], u)
    return float(dx_a), float(dx_b)


def measure_window(a_mut, start: int, stop: int):
    window = a_mut[start:stop]
    mean = float(np.mean(window))
    std = float(np.std(window))
    snr = abs(mean) / (std + 1e-12)
    return mean, std, snr


def run_trace(lat: OpenWilsonLattice, d: int, n_steps: int):
    placement = centered_placement(lat.side, d)
    shared = lat.run_mode("SHARED", placement, n_steps)
    self_only = lat.run_mode("SELF_ONLY", placement, n_steps)
    frozen_source = lat.run_mode("FROZEN_SOURCE", placement, n_steps)
    a_shared_self = separation_acceleration(shared["sep"]) - separation_acceleration(self_only["sep"])
    a_shared_frozen = separation_acceleration(shared["sep"]) - separation_acceleration(frozen_source["sep"])
    a_self_frozen = separation_acceleration(self_only["sep"]) - separation_acceleration(frozen_source["sep"])
    initial_vec = np.asarray(placement.center_b, dtype=float) - np.asarray(placement.center_a, dtype=float)
    dx_shared_self_a, dx_shared_self_b = projected_pair_motion(shared, self_only, initial_vec)
    dx_shared_frozen_a, dx_shared_frozen_b = projected_pair_motion(shared, frozen_source, initial_vec)

    result = {
        "d": d,
        "n_steps": n_steps,
        "shared_dsep": float(shared["sep"][-1] - shared["sep"][0]),
        "self_dsep": float(self_only["sep"][-1] - self_only["sep"][0]),
        "frozen_dsep": float(frozen_source["sep"][-1] - frozen_source["sep"][0]),
        "dx_shared_self_a": dx_shared_self_a,
        "dx_shared_self_b": dx_shared_self_b,
        "dx_shared_frozen_a": dx_shared_frozen_a,
        "dx_shared_frozen_b": dx_shared_frozen_b,
        "inward_shared_self": dx_shared_self_a > 0 and dx_shared_self_b < 0,
        "inward_shared_frozen": dx_shared_frozen_a > 0 and dx_shared_frozen_b < 0,
        "windows": {
            "shared_self": {},
            "shared_frozen": {},
            "self_frozen": {},
        },
    }
    for label, start, stop in WINDOWS[n_steps]:
        for pair_key, series in (
            ("shared_self", a_shared_self),
            ("shared_frozen", a_shared_frozen),
            ("self_frozen", a_self_frozen),
        ):
            mean, std, snr = measure_window(series, start, stop)
            result["windows"][pair_key][label] = {
                "start": start,
                "stop": stop,
                "mean": mean,
                "std": std,
                "snr": snr,
                "signal": "ATTRACT" if mean < -1e-6 else ("REPEL" if mean > 1e-6 else "NULL"),
                "clean": snr > 2.0,
            }
    return result


def summarize(results, trace_steps):
    print("\nFrozen-source summaries")
    print("-" * 108)
    for n_steps in trace_steps:
        sub = [r for r in results if r["n_steps"] == n_steps]
        print(f"\ntrace={n_steps} side={SIDE} centered configs={len(sub)}")
        for label, start, stop in WINDOWS[n_steps]:
            for pair_key, pair_label, inward_key in (
                ("shared_self", "SHARED-SELF_ONLY", "inward_shared_self"),
                ("shared_frozen", "SHARED-FROZEN", "inward_shared_frozen"),
                ("self_frozen", "SELF_ONLY-FROZEN", None),
            ):
                rows = [r for r in sub if r["windows"][pair_key][label]["signal"] == "ATTRACT"]
                clean_rows = [r for r in rows if r["windows"][pair_key][label]["clean"]]
                if len(rows) >= 3:
                    slope, r2 = power_law_fit(
                        [r["d"] for r in rows],
                        [abs(r["windows"][pair_key][label]["mean"]) for r in rows],
                    )
                    fit_msg = f"|a_mut| ~ d^{slope:.3f}  R^2={r2:.4f}"
                else:
                    fit_msg = "fit=insufficient"
                inward_text = f"{sum(r[inward_key] for r in sub)}/{len(sub)}" if inward_key else "-"
                print(
                    f"  {label:7s} [{start}:{stop}] {pair_label:15s}: "
                    f"attract={len(rows)}/{len(sub)} clean={len(clean_rows)}/{len(sub)} "
                    f"inward={inward_text} {fit_msg}"
                )


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, nargs="+", default=list(DEFAULT_TRACE_STEPS))
    parser.add_argument("--separations", type=int, nargs="+", default=list(DEFAULT_SEPARATIONS))
    parser.add_argument("--json-out", type=str, default="")
    return parser.parse_args()


def main():
    args = parse_args()
    trace_steps = tuple(args.steps)
    separations = tuple(args.separations)
    t0 = time.time()
    lat = OpenWilsonLattice(SIDE)

    print("=" * 108)
    print("WILSON TWO-BODY FROZEN-SOURCE CONTROL")
    print("=" * 108)
    print(f"side={SIDE}, separations={separations}")
    print(f"MASS={MASS}, WILSON_R={WILSON_R}, DT={DT}, SIGMA={SIGMA}")
    print(f"G={G_VAL}, mu2={MU2}, REG={REG}")
    print("placement_family=centered")
    print()

    results = []
    for n_steps in trace_steps:
        print(f"Trace length {n_steps}")
        print("-" * 108)
        for d in separations:
            row_start = time.time()
            res = run_trace(lat, d, n_steps)
            results.append(res)
            base_label = WINDOWS[n_steps][0][0]
            print(
                f"d={d:2d} "
                f"base({base_label}) SH/SELF={res['windows']['shared_self'][base_label]['mean']:+.6f} "
                f"+/- {res['windows']['shared_self'][base_label]['std']:.6f} "
                f"SNR={res['windows']['shared_self'][base_label]['snr']:.2f} "
                f"SH/FROZEN={res['windows']['shared_frozen'][base_label]['mean']:+.6f} "
                f"+/- {res['windows']['shared_frozen'][base_label]['std']:.6f} "
                f"inward_SH/SELF={'Y' if res['inward_shared_self'] else 'N'} "
                f"inward_SH/FROZEN={'Y' if res['inward_shared_frozen'] else 'N'} "
                f"dsep SH={res['shared_dsep']:+.4f} SELF={res['self_dsep']:+.4f} FROZEN={res['frozen_dsep']:+.4f} "
                f"({time.time() - row_start:.1f}s)"
            )
        print()

    summarize(results, trace_steps)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
    print(f"\nElapsed: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
