#!/usr/bin/env python3
"""3+1D Dirac observable panel.

Run one consistent Dirac harness and compare several gravity readouts side by
side:
  - centroid shift
  - peak shift
  - first-arrival layer for mass-side accumulation
  - early mass-side accumulation
  - directionally projected current
  - mass-side shell imbalance

The goal is to separate geometry-driven transport from readout-specific
behavior on the same lattice, mass, and coupling convention.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from frontier_dirac_walk_3plus1d_v3 import (  # noqa: E402
    gamma0,
    gamma3,
    min_image_dist,
    prob,
    step_zyx,
)


ALPHA_Z = gamma0 @ gamma3


def parse_int_list(text: str) -> list[int]:
    return [int(item.strip()) for item in text.split(",") if item.strip()]


def init_state(n: int) -> np.ndarray:
    psi = np.zeros((4, n, n, n), dtype=np.complex128)
    c = n // 2
    psi[:, c, c, c] = 0.5
    return psi


def build_mass_field(n: int, mass0: float, strength: float, offset: int) -> np.ndarray:
    field = np.full((n, n, n), mass0, dtype=float)
    if strength <= 0:
        return field
    c = n // 2
    mass_pos = (c, c, c + offset)
    tf = strength / (min_image_dist(n, mass_pos) + 0.1)
    return mass0 * (1.0 + tf)


def signed_min_image(idx: int, center: int, n: int) -> float:
    d = idx - center
    half = n // 2
    if d > half:
        d -= n
    if d < -half:
        d += n
    return float(d)


def torus_centroid_z(rho: np.ndarray, center: int) -> float:
    total = float(np.sum(rho))
    if total <= 1e-30:
        return 0.0
    n = rho.shape[2]
    zs = np.array([signed_min_image(i, center, n) for i in range(n)], dtype=float)
    z_marginal = np.sum(rho, axis=(0, 1))
    return float(np.dot(zs, z_marginal) / total)


def peak_signed_z(rho: np.ndarray, center: int) -> tuple[float, int]:
    z_marginal = np.sum(rho, axis=(0, 1))
    idx = int(np.argmax(z_marginal))
    return signed_min_image(idx, center, rho.shape[2]), idx


def directional_shell_sum(arr: np.ndarray, center: int, radius: int) -> float:
    """Mass-side minus opposite-side sum on symmetric shells."""
    n = arr.shape[2]
    r = min(radius, center, n - center - 1)
    if r <= 0:
        return 0.0
    plus_idx = [(center + dz) % n for dz in range(1, r + 1)]
    minus_idx = [(center - dz) % n for dz in range(1, r + 1)]
    plus = float(np.sum(arr[:, :, plus_idx]))
    minus = float(np.sum(arr[:, :, minus_idx]))
    return plus - minus


def current_density_z(psi: np.ndarray) -> np.ndarray:
    return np.einsum("aijk,ab,bijk->ijk", psi.conj(), ALPHA_Z, psi).real


def sign_char(value: float, eps: float = 1e-12) -> str:
    if value > eps:
        return "T"
    if value < -eps:
        return "A"
    return "0"


def evolve_panel(
    n: int,
    layers: int,
    mass0: float,
    strength: float,
    offset: int,
) -> list[dict[str, float]]:
    center = n // 2
    free_field = np.full((n, n, n), mass0, dtype=float)
    grav_field = build_mass_field(n, mass0, strength, offset)

    psi_free = init_state(n)
    psi_grav = init_state(n)
    rows: list[dict[str, float]] = []

    for layer in range(1, layers + 1):
        psi_free = step_zyx(psi_free, free_field, n)
        psi_grav = step_zyx(psi_grav, grav_field, n)

        rho_free = prob(psi_free)
        rho_grav = prob(psi_grav)
        jz_free = current_density_z(psi_free)
        jz_grav = current_density_z(psi_grav)

        c_free = torus_centroid_z(rho_free, center)
        c_grav = torus_centroid_z(rho_grav, center)
        p_free, p_free_idx = peak_signed_z(rho_free, center)
        p_grav, p_grav_idx = peak_signed_z(rho_grav, center)

        shell_free = directional_shell_sum(rho_free, center, offset)
        shell_grav = directional_shell_sum(rho_grav, center, offset)
        curr_free = directional_shell_sum(jz_free, center, offset)
        curr_grav = directional_shell_sum(jz_grav, center, offset)

        peak_delta = signed_min_image(int(p_grav_idx - p_free_idx), 0, n)

        rows.append(
            {
                "layer": float(layer),
                "centroid_delta": c_grav - c_free,
                "peak_delta": peak_delta,
                "peak_free_idx": float(p_free_idx),
                "peak_grav_idx": float(p_grav_idx),
                "shell_delta": shell_grav - shell_free,
                "current_delta": curr_grav - curr_free,
                "shell_free": shell_free,
                "shell_grav": shell_grav,
                "current_free": curr_free,
                "current_grav": curr_grav,
            }
        )

    return rows


def summarize_panel(rows: list[dict[str, float]]) -> dict[str, float | int | str]:
    final = rows[-1]
    early_rows = rows[: max(1, len(rows) // 2)]
    early_accum = float(sum(row["shell_delta"] for row in early_rows))
    first_arrival = next((int(row["layer"]) for row in rows if row["shell_delta"] > 0), -1)

    centroid_delta = float(final["centroid_delta"])
    peak_delta = float(final["peak_delta"])
    shell_delta = float(final["shell_delta"])
    current_delta = float(final["current_delta"])

    signs = {
        "centroid": sign_char(centroid_delta),
        "peak": sign_char(peak_delta),
        "shell": sign_char(shell_delta),
        "current": sign_char(current_delta),
    }
    nonzero = [v for v in signs.values() if v != "0"]
    consensus = "ALL" if nonzero and len(set(nonzero)) == 1 else "MIX"

    return {
        "first_arrival": first_arrival,
        "early_accum": early_accum,
        "centroid_delta": centroid_delta,
        "peak_delta": peak_delta,
        "shell_delta": shell_delta,
        "current_delta": current_delta,
        "signs": "".join(signs[key] for key in ("centroid", "peak", "shell", "current")),
        "consensus": consensus,
    }


def print_summary_row(n_layers: int, summary: dict[str, float | int | str]) -> None:
    print(
        f"{n_layers:4d}  "
        f"{float(summary['centroid_delta']):+12.4e}  "
        f"{float(summary['peak_delta']):+12.4e}  "
        f"{int(summary['first_arrival']):6d}  "
        f"{float(summary['early_accum']):+12.4e}  "
        f"{float(summary['current_delta']):+12.4e}  "
        f"{float(summary['shell_delta']):+12.4e}  "
        f"{str(summary['signs']):>4}  "
        f"{str(summary['consensus']):>4}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="3+1D Dirac observable panel")
    parser.add_argument("--n", type=int, default=21, help="lattice size")
    parser.add_argument(
        "--layers",
        default="10,12,14,16,18,20",
        help="comma-separated layer counts to sweep",
    )
    parser.add_argument("--mass", type=float, default=0.3, help="base mass / mixing")
    parser.add_argument("--strength", type=float, default=5e-4, help="gravity strength")
    parser.add_argument("--offset", type=int, default=3, help="mass offset along z")
    args = parser.parse_args()

    layers_list = parse_int_list(args.layers)
    center = args.n // 2

    print("=" * 78)
    print("DIRAC WALK 3+1D OBSERVABLE PANEL")
    print("=" * 78)
    print(f"n={args.n}, center={center}, mass={args.mass}, strength={args.strength}, offset={args.offset}")
    print("Observables: centroid, peak, first-arrival, early shell accumulation, current, shell")
    print()
    print(
        f"{'N':>4}  {'centroid':>12}  {'peak':>12}  {'first+':>6}  "
        f"{'early_shell':>12}  {'current':>12}  {'shell':>12}  {'sig':>4}  {'cons':>4}"
    )
    print("-" * 92)

    all_summaries = []
    for layers in layers_list:
        rows = evolve_panel(args.n, layers, args.mass, args.strength, args.offset)
        summary = summarize_panel(rows)
        all_summaries.append((layers, summary))

        print_summary_row(layers, summary)

    centroid_vs_peak = 0
    centroid_vs_shell = 0
    centroid_vs_current = 0
    peak_vs_shell = 0
    total = len(all_summaries)

    for _, summary in all_summaries:
        c = summary["signs"][0]
        p = summary["signs"][1]
        s = summary["signs"][2]
        j = summary["signs"][3]
        if c == p and c != "0":
            centroid_vs_peak += 1
        if c == s and c != "0":
            centroid_vs_shell += 1
        if c == j and c != "0":
            centroid_vs_current += 1
        if p == s and p != "0":
            peak_vs_shell += 1

    print("=" * 78)
    print("AGREEMENT SUMMARY")
    print("=" * 78)
    print(f"centroid vs peak:   {centroid_vs_peak}/{total}")
    print(f"centroid vs shell:   {centroid_vs_shell}/{total}")
    print(f"centroid vs current: {centroid_vs_current}/{total}")
    print(f"peak vs shell:       {peak_vs_shell}/{total}")

    same_all = sum(1 for _, summary in all_summaries if summary["consensus"] == "ALL")
    mixed = total - same_all
    print(f"all-four agree:      {same_all}/{total}")
    print(f"mixed-sign cases:    {mixed}/{total}")

    print()
    print("Interpretation:")
    print("  - If centroid, peak, current, and shell all agree, the sign is likely geometric.")
    print("  - If peak disagrees but centroid/current/shell agree, the issue is readout-specific.")
    print("  - If the panel flips only near large N, recurrence / boundary effects are still active.")


if __name__ == "__main__":
    main()
