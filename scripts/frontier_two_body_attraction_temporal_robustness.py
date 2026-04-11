#!/usr/bin/env python3
"""
Bounded temporal-robustness follow-up for the Wilson two-body attraction lane.

This keeps the same audited surface as the side/placement robustness sweep:
  - open 3D Wilson lattice
  - MASS=0.3, WILSON_R=1.0
  - G=5, mu2=0.001, REG=1e-3
  - Gaussian packets with sigma=1.0
  - sides 18, 20, 22
  - placement families centered / face_offset / corner_offset
  - separations d = 4, 6, 8, 10, 12

The only change is temporal:
  - extend the trace from 15 to 35 steps
  - score several fixed windows on the same trajectories

The retained observable remains the shared-vs-self-only separation residual:
  a_mutual = a_sep(shared) - a_sep(self_only)

This runner is intentionally bounded. It does not claim:
  - cross-architecture robustness
  - both-masses closure
  - action-reaction closure
  - a full-trace force law
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
N_STEPS = 35
SIGMA = 1.0
G_VAL = 5.0
MU2 = 0.001

SIDES = (18, 20, 22)
SEPARATIONS = (4, 6, 8, 10, 12)
PLACEMENT_FAMILIES = ("centered", "face_offset", "corner_offset")

WINDOWS: tuple[tuple[str, int, int], ...] = (
    ("w02_10", 2, 11),
    ("w05_13", 5, 14),
    ("w08_16", 8, 17),
    ("w11_19", 11, 20),
    ("w14_22", 14, 23),
    ("w17_25", 17, 26),
)


@dataclass(frozen=True)
class Placement:
    center_a: tuple[int, int, int]
    center_b: tuple[int, int, int]
    family: str


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
        psi_a = self.gaussian_wavepacket(center_a)
        psi_b = self.gaussian_wavepacket(center_b)

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
            else:
                raise ValueError(f"unknown mode {mode}")

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


def projected_window_motion(shared, self_only, initial_vec, start: int, stop: int):
    u = initial_vec / max(np.linalg.norm(initial_vec), 1e-30)
    res_a = shared["com_a"] - self_only["com_a"]
    res_b = shared["com_b"] - self_only["com_b"]
    dxa = np.dot(res_a[stop - 1] - res_a[start], u)
    dxb = np.dot(res_b[stop - 1] - res_b[start], u)
    return float(dxa), float(dxb)


def evaluate_window(shared, self_only, placement, start: int, stop: int):
    a_mut = separation_acceleration(shared["sep"]) - separation_acceleration(self_only["sep"])
    window = a_mut[start:stop]
    a_mean = float(np.mean(window))
    a_std = float(np.std(window))
    snr = abs(a_mean) / (a_std + 1e-12)

    initial_vec = np.asarray(placement.center_b, dtype=float) - np.asarray(placement.center_a, dtype=float)
    dx_a, dx_b = projected_window_motion(shared, self_only, initial_vec, start, stop)
    inward_both = dx_a > 0 and dx_b < 0

    return {
        "a_mutual_mean": a_mean,
        "a_mutual_std": a_std,
        "snr": snr,
        "signal": "ATTRACT" if a_mean < -1e-6 else ("REPEL" if a_mean > 1e-6 else "NULL"),
        "clean": snr > 2.0,
        "inward_both": inward_both,
        "dx_a_mutual": dx_a,
        "dx_b_mutual": dx_b,
    }


def run_config(side: int, d: int, family: str):
    lat = OpenWilsonLattice(side)
    placement = placement_for(side, d, family)
    shared = lat.run_mode("SHARED", placement.center_a, placement.center_b)
    self_only = lat.run_mode("SELF_ONLY", placement.center_a, placement.center_b)

    row = {"side": side, "family": family, "d": d}
    for label, start, stop in WINDOWS:
        metrics = evaluate_window(shared, self_only, placement, start, stop)
        for key, value in metrics.items():
            row[f"{label}_{key}"] = value
    return row


def window_summary(rows, label):
    attract = [r for r in rows if r[f"{label}_signal"] == "ATTRACT"]
    clean = [r for r in rows if r[f"{label}_clean"]]
    inward = [r for r in rows if r[f"{label}_inward_both"]]
    strong = [
        r for r in rows
        if r[f"{label}_signal"] == "ATTRACT"
        and r[f"{label}_clean"]
        and r[f"{label}_inward_both"]
    ]

    summary = {
        "configs": len(rows),
        "attract": len(attract),
        "clean": len(clean),
        "inward": len(inward),
        "strong": len(strong),
    }
    if len(strong) >= 3 and len({r['d'] for r in strong}) >= 3:
        slope, r2 = power_law_fit(
            [r["d"] for r in strong],
            [abs(r[f"{label}_a_mutual_mean"]) for r in strong],
        )
        summary["slope"] = slope
        summary["r2"] = r2
    else:
        summary["slope"] = None
        summary["r2"] = None

    families: dict[str, dict[str, float | int | None]] = {}
    for family in PLACEMENT_FAMILIES:
        sub = [r for r in strong if r["family"] == family]
        entry: dict[str, float | int | None] = {"strong": len(sub)}
        if len(sub) >= 3 and len({r['d'] for r in sub}) >= 3:
            slope, r2 = power_law_fit(
                [r["d"] for r in sub],
                [abs(r[f"{label}_a_mutual_mean"]) for r in sub],
            )
            entry["slope"] = slope
            entry["r2"] = r2
        else:
            entry["slope"] = None
            entry["r2"] = None
        families[family] = entry
    summary["families"] = families
    return summary


def summarize_window(rows, label):
    summary = window_summary(rows, label)
    print(f"\nWindow {label}")
    print("-" * 108)
    print(
        f"configs={summary['configs']} "
        f"attract={summary['attract']}/{summary['configs']} "
        f"clean={summary['clean']}/{summary['configs']} "
        f"inward={summary['inward']}/{summary['configs']} "
        f"strong={summary['strong']}/{summary['configs']}"
    )
    if summary["slope"] is not None:
        print(f"global strong rows: |a_mut| ~ d^{summary['slope']:.3f}  R^2={summary['r2']:.4f}")
    else:
        print("global strong rows: insufficient rows")
    for family in PLACEMENT_FAMILIES:
        entry = summary["families"][family]
        if entry["slope"] is not None:
            print(f"{family:13s}: |a_mut| ~ d^{entry['slope']:.3f}  R^2={entry['r2']:.4f}")
        else:
            print(f"{family:13s}: insufficient strong rows")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary-json", help="Write compact window summary JSON to this path.")
    parser.add_argument("--quiet", action="store_true", help="Suppress per-row progress output.")
    return parser.parse_args()


def main():
    args = parse_args()
    t0 = time.time()
    if not args.quiet:
        print("=" * 108)
        print("WILSON TWO-BODY TEMPORAL ROBUSTNESS")
        print("=" * 108)
        print(f"MASS={MASS}, WILSON_R={WILSON_R}, DT={DT}, N_STEPS={N_STEPS}, SIGMA={SIGMA}")
        print(f"G={G_VAL}, mu2={MU2}, REG={REG}")
        print(f"sides={SIDES}")
        print(f"separations={SEPARATIONS}")
        print(f"placement_families={PLACEMENT_FAMILIES}")
        print(f"windows={WINDOWS}")
        print()

    rows = []
    for side in SIDES:
        for family in PLACEMENT_FAMILIES:
            for d in SEPARATIONS:
                row_start = time.time()
                row = run_config(side, d, family)
                rows.append(row)
                if not args.quiet:
                    baseline = "w02_10"
                    tail = "w17_25"
                    print(
                        f"side={side:2d} family={family:13s} d={d:2d} "
                        f"{baseline}: {row[f'{baseline}_signal']:7s} "
                        f"SNR={row[f'{baseline}_snr']:.2f} "
                        f"inward={'Y' if row[f'{baseline}_inward_both'] else 'N'} "
                        f"a_mut={row[f'{baseline}_a_mutual_mean']:+.6f} ; "
                        f"{tail}: {row[f'{tail}_signal']:7s} "
                        f"SNR={row[f'{tail}_snr']:.2f} "
                        f"inward={'Y' if row[f'{tail}_inward_both'] else 'N'} "
                        f"a_mut={row[f'{tail}_a_mutual_mean']:+.6f} "
                        f"({time.time() - row_start:.1f}s)"
                    )

    summary = {
        "rows": len(rows),
        "elapsed_s": time.time() - t0,
        "windows": {label: window_summary(rows, label) for label, _, _ in WINDOWS},
    }
    if args.summary_json:
        with open(args.summary_json, "w") as f:
            json.dump(summary, f, indent=2)
    if args.quiet:
        print(json.dumps(summary, indent=2))
    else:
        for label, _, _ in WINDOWS:
            summarize_window(rows, label)
        print(f"\nElapsed: {summary['elapsed_s']:.1f}s")


if __name__ == "__main__":
    main()
