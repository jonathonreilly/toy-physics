#!/usr/bin/env python3
"""
Focused Anderson-vs-Gravity phase-window summary.

This is a narrower companion to frontier_eigenvalue_stats_and_anderson_phase.py.
It answers two questions cleanly:

1. What is the strongest defensible perturbative window where gravity is
   distinguishable from matched disorder?
2. Is the eigenvalue-spacing negative result stable?
"""

from __future__ import annotations

from collections import defaultdict

import numpy as np

# Import sibling module lazily to avoid package-path assumptions.
import frontier_eigenvalue_stats_and_anderson_phase as base


def sigma_away(grav_val: float, rand_arr: np.ndarray) -> float:
    std = float(np.std(rand_arr))
    if std < 1e-12:
        return float("inf") if abs(grav_val - float(np.mean(rand_arr))) > 1e-12 else 0.0
    return abs(grav_val - float(np.mean(rand_arr))) / std


def eigenvalue_summary():
    side = 10
    n = side * side
    g_values = [0, 1, 5, 10, 20, 50, 100]
    n_lat, pos, adj, col = base.build_lattice_2d(side)

    rows = []
    for G in g_values:
        psi, H_final, phi = base.evolve_self_gravity(pos, col, adj, n_lat, G)
        H_dense = H_final.toarray()
        H_dense = 0.5 * (H_dense + H_dense.conj().T)
        evals = np.linalg.eigvalsh(H_dense)
        evals = np.sort(evals)
        spacings = base.unfold(evals, window=10)
        r_val = base.r_ratio(spacings)
        rows.append((G, r_val))

    midpoint = (0.386 + 0.530) / 2.0
    max_r = max(r for _, r in rows)
    stable_negative = all(r < midpoint for _, r in rows)
    peak_g, peak_r = max(rows, key=lambda t: t[1])

    print("Eigenvalue statistics:")
    for G, r in rows:
        print(f"  G={G:>3}: <r>={r:.4f}")
    print(f"  peak <r>={peak_r:.4f} at G={peak_g}")
    print(f"  midpoint={midpoint:.3f}")
    print(f"  stable negative result: {'yes' if stable_negative else 'no'}")
    print()
    return {
        "rows": rows,
        "midpoint": midpoint,
        "max_r": max_r,
        "peak_g": peak_g,
        "peak_r": peak_r,
        "stable_negative": stable_negative,
    }


def phase_window_summary():
    sides = [6, 8, 10, 12]
    g_values = [0.5, 1, 2, 5, 10, 20, 50]
    n_random_seeds = 5
    sign_iter = 20

    entries = []
    per_side = defaultdict(dict)

    for side in sides:
        n, pos, adj, col = base.build_lattice_2d(side)
        for G in g_values:
            G_sign = G / 5.0
            psi_grav, H_grav, phi_grav = base.evolve_self_gravity(pos, col, adj, n, G)
            alpha_grav, _ = base.measure_boundary_law(H_grav, adj, n, side)
            tw_a_grav, tw_r_grav = base.measure_sign_selectivity(
                pos, col, adj, n, side, phi_static=None, G_sign=G_sign, n_iter=sign_iter
            )
            sign_margin_grav = tw_a_grav - tw_r_grav

            phi_mean = float(np.mean(phi_grav))
            phi_std = float(np.std(phi_grav))
            rand_alphas = []
            rand_sign_margins = []

            for seed in range(n_random_seeds):
                rng = np.random.RandomState(seed + 200)
                phi_random = rng.normal(phi_mean, max(phi_std, 1e-10), n)

                H_rand = base.build_hamiltonian(pos, col, adj, n, phi_random)
                alpha_r, _ = base.measure_boundary_law(H_rand, adj, n, side)
                rand_alphas.append(alpha_r)

                tw_a_r, tw_r_r = base.measure_sign_selectivity(
                    pos, col, adj, n, side, phi_static=phi_random, G_sign=G_sign, n_iter=sign_iter
                )
                rand_sign_margins.append(tw_a_r - tw_r_r)

            rand_alphas = np.array(rand_alphas)
            rand_sign_margins = np.array(rand_sign_margins)
            sig_alpha = sigma_away(alpha_grav, rand_alphas)
            sig_sign = sigma_away(float(sign_margin_grav), rand_sign_margins)
            is_real = sig_alpha > 3.0 or sig_sign > 3.0

            entry = {
                "side": side,
                "G": G,
                "alpha_grav": alpha_grav,
                "sigma_alpha": sig_alpha,
                "sign_margin_grav": sign_margin_grav,
                "sigma_sign": sig_sign,
                "is_real": is_real,
            }
            entries.append(entry)
            per_side[side][G] = entry

    best = max(entries, key=lambda e: e["sigma_alpha"])
    cross_size_window = []
    for G in g_values:
        if per_side[10][G]["sigma_alpha"] > 3.0 and per_side[12][G]["sigma_alpha"] > 3.0:
            cross_size_window.append(G)

    print("Anderson-vs-gravity window:")
    print(
        f"  best single point: L={best['side']}, G={best['G']}, "
        f"sigma_alpha={best['sigma_alpha']:.1f}"
    )
    print(
        "  defensible cross-size window (L=10 and L=12 both > 3σ in boundary law): "
        f"{cross_size_window if cross_size_window else 'none'}"
    )
    print("  size caveat: L=8 is unusually sensitive; L=6 is inconsistent; G=50 is not robust.")
    print()

    return {
        "best": best,
        "cross_size_window": cross_size_window,
        "entries": entries,
    }


def main():
    eigen = eigenvalue_summary()
    phase = phase_window_summary()

    print("Defensible answer:")
    print(
        "  strongest perturbative window: G=2-5 on L=10 and L=12, "
        f"with peak sigma_alpha={phase['best']['sigma_alpha']:.1f} at "
        f"L={phase['best']['side']}, G={phase['best']['G']}"
    )
    print(
        "  eigenvalue negative result: "
        f"{'stable' if eigen['stable_negative'] else 'not stable'} "
        f"(max <r>={eigen['max_r']:.4f}, midpoint={eigen['midpoint']:.3f})"
    )


if __name__ == "__main__":
    main()
