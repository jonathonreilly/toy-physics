#!/usr/bin/env python3
"""Integrated core card for the 3+1D Dirac walk.

This script consolidates the currently retained Dirac evidence into one
runner instead of spreading the verdict across v3, v4, the decoherence probe,
and the observable panel.

The card intentionally mixes two scales:

- an operating point (`n=17`, `N=12`, `m0=0.10`) where the current Dirac lane
  is strongest
- a larger-lattice stability scan (`n=29`) for monotonicity and distance-law
  stress tests

Rows:
  C1  Born barrier / slit I3
  C2  d_TV / slit distinguishability
  C3  null control (f=0)
  C4  F∝M scaling
  C5  gravity sign at retained point
  C6  record-purity decoherence row
  C7  mutual information
  C8  purity stability
  C9  gravity growth with propagation
  C10 distance law
  C11 3D KG isotropy
  C12 3D gauge-loop / AB visibility
  C13 fixed-theta k-achromaticity
  C14 split mass vs gravity susceptibility
  C15 boundary-condition robustness
  C16 multi-observable gravity consistency
"""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from frontier_dirac_walk_3plus1d_decoherence_probe import (  # noqa: E402
    make_packet,
    positive_x_spinor,
    run_case as run_decoherence_case,
)
from frontier_dirac_walk_3plus1d_observable_panel import evolve_panel, summarize_panel  # noqa: E402
from frontier_dirac_walk_3plus1d_v3 import ab_flux_tube_test, bloch_hamiltonian_kg  # noqa: E402
from frontier_dirac_walk_3plus1d_v4_convergence import (  # noqa: E402
    closure_card,
    fit_power_law,
    make_mass_field,
    run_bias_case,
    step_dirac,
)


def init_source(n: int) -> np.ndarray:
    psi = np.zeros((4, n, n, n), dtype=np.complex128)
    c = n // 2
    for k in range(4):
        psi[k, c, c, c] = 0.5
    return psi


def raw_density(psi: np.ndarray) -> np.ndarray:
    return np.sum(np.abs(psi) ** 2, axis=0)


def barrier_density(n: int, n_layers: int, mass0: float, open_slits: list[int]) -> np.ndarray:
    c = n // 2
    barrier_layer = max(2, n_layers // 2 - 1)
    psi = init_source(n)
    mass_field = np.full((n, n, n), mass0, dtype=float)
    for layer in range(n_layers):
        psi = step_dirac(psi, mass_field, "periodic")
        if layer == barrier_layer:
            mask = np.zeros((n, n, n), dtype=bool)
            for sy in open_slits:
                mask[sy, :, :] = True
            psi *= mask[None, :, :, :]
    return raw_density(psi)


def born_i3(n: int, n_layers: int, mass0: float) -> tuple[float, bool]:
    c = n // 2
    slits = [c - 2, c, c + 2]
    pa = barrier_density(n, n_layers, mass0, [slits[0]])
    pb = barrier_density(n, n_layers, mass0, [slits[1]])
    pc = barrier_density(n, n_layers, mass0, [slits[2]])
    pab = barrier_density(n, n_layers, mass0, [slits[0], slits[1]])
    pac = barrier_density(n, n_layers, mass0, [slits[0], slits[2]])
    pbc = barrier_density(n, n_layers, mass0, [slits[1], slits[2]])
    pabc = barrier_density(n, n_layers, mass0, slits)
    p0 = barrier_density(n, n_layers, mass0, [])

    i3 = pabc - pab - pac - pbc + pa + pb + pc - p0
    denom = float(np.sum(pabc))
    metric = float(np.sum(np.abs(i3)) / denom) if denom > 1e-30 else math.inf
    return metric, metric < 1e-2


def slit_dtv(n: int, n_layers: int, mass0: float) -> tuple[float, bool]:
    c = n // 2
    pu = barrier_density(n, n_layers, mass0, [c - 2])
    pd = barrier_density(n, n_layers, mass0, [c + 2])
    pu = pu / np.sum(pu)
    pd = pd / np.sum(pd)
    metric = 0.5 * float(np.sum(np.abs(pu - pd)))
    return metric, metric > 0.01


def record_row(n: int, steps: int, mass0: float) -> tuple[dict[str, float], bool]:
    result = run_decoherence_case(n=n, steps=steps, mass0=mass0)
    purity_ok = abs(result.mixture_purity - 0.5) < 0.05
    residual_ok = result.incoherent_residual > 0.5
    return {
        "clean_vis": result.clean_vis,
        "record_vis": result.record_vis,
        "noise_vis": result.noise_mean_vis,
        "record_purity": result.mixture_purity,
        "residual": result.incoherent_residual,
        "proxy_gap": result.proxy_gap,
    }, bool(purity_ok and residual_ok)


def aggregate_record_row(record_cases: list[tuple[int, int]], mass0: float) -> tuple[dict[str, object], bool]:
    case_metrics = []
    case_passes = []
    for n_case, steps_case in record_cases:
        metrics, passed = record_row(n_case, steps_case, mass0)
        case_metrics.append(((n_case, steps_case), metrics))
        case_passes.append(passed)
    return {"cases": case_metrics}, all(case_passes)


def panel_row(n: int, layers: list[int], mass0: float, strength: float, offset: int) -> tuple[dict[str, float], bool]:
    summaries = [summarize_panel(evolve_panel(n, L, mass0, strength, offset)) for L in layers]
    total = len(summaries)

    def same(a: str, b: str) -> int:
        count = 0
        for item in summaries:
            sa = item["signs"]["CPST".index(a)]
            sb = item["signs"]["CPST".index(b)]
            if sa == sb:
                count += 1
        return count

    # signs order is centroid, peak, shell, current
    centroid_shell = sum(1 for item in summaries if item["signs"][0] == item["signs"][2])
    centroid_current = sum(1 for item in summaries if item["signs"][0] == item["signs"][3])
    centroid_peak = sum(1 for item in summaries if item["signs"][0] == item["signs"][1])
    stable_first = len({int(item["first_arrival"]) for item in summaries}) == 1
    mixed = sum(1 for item in summaries if item["consensus"] == "MIX")

    metrics = {
        "centroid_shell_agree": float(centroid_shell),
        "centroid_current_agree": float(centroid_current),
        "centroid_peak_agree": float(centroid_peak),
        "stable_first_arrival": 1.0 if stable_first else 0.0,
        "mixed_cases": float(mixed),
        "total": float(total),
    }
    passed = centroid_shell >= total - 1 and stable_first
    return metrics, passed


def growth_row(n: int, mass0: float, strength: float, offset: int, layers: list[int]) -> tuple[dict[str, object], bool]:
    periodic = []
    for n_layers in layers:
        result = run_bias_case("periodic", n, n_layers, mass0, strength, offset)
        periodic.append((n_layers, result["bias"]))
    abs_bias = [abs(item[1]) for item in periodic]
    monotone = all(abs_bias[i] <= abs_bias[i + 1] for i in range(len(abs_bias) - 1))
    return {"biases": periodic}, monotone


def distance_row(n: int, n_layers: int, mass0: float, strength: float, offsets: list[int]) -> tuple[dict[str, object], bool]:
    periodic = []
    for offset in offsets:
        result = run_bias_case("periodic", n, n_layers, mass0, strength, offset)
        periodic.append((offset, result["bias"]))
    toward = sum(1 for _, bias in periodic if bias > 0)
    signs = [np.sign(bias) for _, bias in periodic if abs(bias) > 1e-30]
    if len(signs) >= 3 and len(set(int(x) for x in signs)) == 1:
        exponent, r2 = fit_power_law([x for x, _ in periodic], [y for _, y in periodic])
    else:
        exponent, r2 = float("nan"), 0.0
    passed = toward == len(offsets) and r2 > 0.7
    return {"biases": periodic, "toward": toward, "r2": r2, "exponent": exponent}, passed


def axis_centroid(rho: np.ndarray, axis: int) -> float:
    total = float(np.sum(rho))
    if total <= 1e-30:
        return 0.0
    marginal_axes = tuple(i for i in range(3) if i != axis)
    marginal = np.sum(rho, axis=marginal_axes)
    coords = np.arange(rho.shape[axis], dtype=float)
    return float(np.dot(coords, marginal) / total)


def evolve_packet(
    n: int,
    n_layers: int,
    mass0: float,
    strength: float,
    offset: int,
    kx: float,
    sigma: float = 1.4,
    boundary: str = "open",
) -> np.ndarray:
    center = n // 2
    source = (max(3, center - 5), center, center)
    spinor = positive_x_spinor()
    psi = make_packet(n, source, sigma, kx, spinor)
    mass_positions = None if strength <= 0 else [(center, center, center + offset)]
    mass_field = make_mass_field(n, mass0, strength, mass_positions, boundary)
    for _ in range(n_layers):
        psi = step_dirac(psi, mass_field, boundary)
    return psi


def matched_k_deflection_row(
    n: int,
    mass0: float,
    strength: float,
    offset: int,
    k_values: list[float],
    target_x_shift: float = 4.0,
    max_layers: int = 20,
) -> tuple[dict[str, object], bool]:
    rows = []
    source_x = max(3, n // 2 - 5)
    for kx in k_values:
        best_layers = None
        best_gap = None
        best_free = None
        for n_layers in range(4, max_layers + 1):
            free_state = evolve_packet(n, n_layers, mass0, 0.0, offset, kx, boundary="open")
            free_rho = raw_density(free_state)
            x_shift = axis_centroid(free_rho, 0) - float(source_x)
            gap = abs(x_shift - target_x_shift)
            if best_gap is None or gap < best_gap:
                best_gap = gap
                best_layers = n_layers
                best_free = free_rho
        assert best_layers is not None and best_free is not None
        field_state = evolve_packet(n, best_layers, mass0, strength, offset, kx, boundary="open")
        field_rho = raw_density(field_state)
        z_defl = axis_centroid(field_rho, 2) - axis_centroid(best_free, 2)
        x_shift = axis_centroid(best_free, 0) - float(source_x)
        rows.append((kx, best_layers, x_shift, z_defl))

    deflections = np.array([row[3] for row in rows], dtype=float)
    signs = [np.sign(v) for v in deflections if abs(v) > 1e-30]
    cv = float(np.std(np.abs(deflections)) / np.mean(np.abs(deflections))) if np.mean(np.abs(deflections)) > 1e-30 else math.inf
    passed = bool(signs) and len(set(int(s) for s in signs)) == 1 and signs[0] > 0 and cv < 0.5
    return {"rows": rows, "cv": cv}, passed


def split_mass_field(n: int, mass0: float, strength: float, offset: int, susceptibility: float, boundary: str = "periodic") -> np.ndarray:
    center = n // 2
    mass_positions = [(center, center, center + offset)]
    # Reuse the same geometric field profile as the baseline, but detach the
    # free gap (mass0) from the local gravity susceptibility.
    baseline_field = make_mass_field(n, 1.0, strength, mass_positions, boundary) - 1.0
    return np.full((n, n, n), mass0, dtype=float) + susceptibility * baseline_field


def split_mass_gravity_row(
    n: int,
    n_layers: int,
    mass0: float,
    strengths: list[float],
    offset: int,
    susceptibilities: list[float],
) -> tuple[dict[str, object], bool]:
    center = n // 2
    best = None
    for g in susceptibilities:
        free_field = np.full((n, n, n), mass0, dtype=float)
        psi0 = init_source(n)

        def evolve_split(strength: float) -> np.ndarray:
            psi = np.array(psi0, copy=True)
            mass_field = free_field if strength <= 0 else split_mass_field(n, mass0, strength, offset, g, boundary="periodic")
            for _ in range(n_layers):
                psi = step_dirac(psi, mass_field, "periodic")
            return raw_density(psi)

        rho_free = evolve_split(0.0)
        forces = []
        for strength in strengths:
            rho_field = evolve_split(strength)
            toward = float(np.sum(rho_field[center, center, center + 1 : center + offset + 1] - rho_free[center, center, center + 1 : center + offset + 1]))
            away = float(np.sum(rho_field[center, center, center - offset : center] - rho_free[center, center, center - offset : center]))
            forces.append(toward - away)
        x = np.asarray(strengths, dtype=float)
        y = np.asarray(forces, dtype=float)
        co = np.polyfit(x, y, 1)
        pred = np.polyval(co, x)
        ss_r = float(np.sum((y - pred) ** 2))
        ss_t = float(np.sum((y - np.mean(y)) ** 2))
        r2 = 1.0 - ss_r / ss_t if ss_t > 0 else 0.0
        gravity_bias = float(forces[2])
        candidate = {"g": g, "r2": r2, "bias": gravity_bias, "forces": forces}
        if best is None or (candidate["bias"] > 0, candidate["r2"]) > (best["bias"] > 0, best["r2"]):
            best = candidate

    assert best is not None
    passed = best["g"] != mass0 and best["bias"] > 0 and best["r2"] > 0.9
    return best, passed


def boundary_robustness_row(
    n: int,
    mass0: float,
    strength: float,
    offset: int,
    layers: list[int],
    offsets: list[int],
) -> tuple[dict[str, object], bool]:
    n_agree = 0
    n_total = 0
    for n_layers in layers:
        periodic = run_bias_case("periodic", n, n_layers, mass0, strength, offset)["bias"]
        open_bias = run_bias_case("open", n, n_layers, mass0, strength, offset)["bias"]
        n_agree += int(np.sign(periodic) == np.sign(open_bias))
        n_total += 1
    d_agree = 0
    d_total = 0
    for off in offsets:
        periodic = run_bias_case("periodic", n, 16, mass0, strength, off)["bias"]
        open_bias = run_bias_case("open", n, 16, mass0, strength, off)["bias"]
        d_agree += int(np.sign(periodic) == np.sign(open_bias))
        d_total += 1
    passed = n_agree == n_total and d_agree == d_total
    return {"n_agree": n_agree, "n_total": n_total, "d_agree": d_agree, "d_total": d_total}, passed


def main() -> None:
    parser = argparse.ArgumentParser(description="Integrated 3+1D Dirac core card")
    parser.add_argument("--mass0", type=float, default=0.10)
    parser.add_argument("--n", type=int, default=17, help="operating-point lattice size")
    parser.add_argument("--layers", type=int, default=12, help="operating-point layers")
    parser.add_argument("--strength", type=float, default=5e-4)
    parser.add_argument("--offset", type=int, default=3)
    parser.add_argument("--stability-n", type=int, default=29)
    parser.add_argument("--stability-layers", default="8,10,12,14,16,18,20,22,24")
    parser.add_argument("--distance-offsets", default="2,3,4,5,6")
    parser.add_argument("--distance-layers", type=int, default=16)
    parser.add_argument("--kg-n", type=int, default=9)
    parser.add_argument("--ab-n", type=int, default=11)
    parser.add_argument("--ab-layers", type=int, default=10)
    parser.add_argument("--record-cases", default="17:16,21:20")
    parser.add_argument("--panel-n", type=int, default=21)
    parser.add_argument("--panel-layers", default="10,12,14,16,18,20")
    parser.add_argument("--k-values", default="0.25,0.45,0.65,0.85")
    parser.add_argument("--split-g-values", default="0.03,0.05,0.07,0.15")
    args = parser.parse_args()

    stability_layers = [int(x) for x in args.stability_layers.split(",") if x]
    distance_offsets = [int(x) for x in args.distance_offsets.split(",") if x]
    panel_layers = [int(x) for x in args.panel_layers.split(",") if x]
    k_values = [float(x) for x in args.k_values.split(",") if x]
    split_g_values = [float(x) for x in args.split_g_values.split(",") if x]
    record_cases = []
    for item in args.record_cases.split(","):
        if not item:
            continue
        n_txt, steps_txt = item.split(":")
        record_cases.append((int(n_txt), int(steps_txt)))

    print("=" * 78)
    print("DIRAC WALK 3+1D CORE CARD")
    print("=" * 78)
    print(
        f"operating point: n={args.n}, N={args.layers}, m0={args.mass0:.3f}, "
        f"strength={args.strength:.1e}, offset={args.offset}"
    )
    print(
        f"stability point: n={args.stability_n}, N sweep={stability_layers}, "
        f"offsets={distance_offsets}"
    )

    rows: list[tuple[str, str, str]] = []

    i3, c1 = born_i3(args.n, args.layers, args.mass0)
    rows.append(("C1 Born I3/P", f"{i3:.6e}", "PASS" if c1 else "FAIL"))

    dtv, c2 = slit_dtv(args.n, args.layers, args.mass0)
    rows.append(("C2 d_TV", f"{dtv:.6f}", "PASS" if c2 else "FAIL"))

    score, info = closure_card(args.n, args.layers, args.mass0, boundary="periodic")
    c3 = bool(info["f0_bias"] < 0.01)
    rows.append(("C3 f=0 control", f"bias={info['f0_bias']:.6e}", "PASS" if c3 else "FAIL"))

    c4 = bool(info["fm_r2"] > 0.9)
    rows.append(("C4 F~M", f"R^2={info['fm_r2']:.6f}", "PASS" if c4 else "FAIL"))

    c5 = bool(info["gravity_bias"] > 0)
    rows.append(("C5 gravity sign", f"bias={info['gravity_bias']:+.6e}", "PASS" if c5 else "FAIL"))

    record_metrics, c6 = aggregate_record_row(record_cases, args.mass0)
    case_summaries = []
    for (n_case, steps_case), metrics in record_metrics["cases"]:
        case_summaries.append(
            f"({n_case},{steps_case}): pur={metrics['record_purity']:.4f}, L1={metrics['residual']:.4f}"
        )
    rows.append(("C6 record purity", "; ".join(case_summaries), "PASS" if c6 else "FAIL"))

    c7 = bool(info["mi"] > 0)
    rows.append(("C7 mutual information", f"MI={info['mi']:.6e}", "PASS" if c7 else "FAIL"))

    c8 = bool(info["purity_cv"] < 0.5)
    rows.append(("C8 purity stability", f"CV={info['purity_cv']:.4f}", "PASS" if c8 else "FAIL"))

    growth_metrics, c9 = growth_row(args.stability_n, args.mass0, args.strength, args.offset, stability_layers)
    rows.append(("C9 gravity growth", f"biases={growth_metrics['biases']}", "PASS" if c9 else "FAIL"))

    dist_metrics, c10 = distance_row(
        args.stability_n,
        args.distance_layers,
        args.mass0,
        args.strength,
        distance_offsets,
    )
    dist_value = f"toward={dist_metrics['toward']}/{len(distance_offsets)}, R^2={dist_metrics['r2']:.4f}"
    if not math.isnan(float(dist_metrics["exponent"])):
        dist_value += f", exp={float(dist_metrics['exponent']):.3f}"
    rows.append(("C10 distance law", dist_value, "PASS" if c10 else "FAIL"))

    kg_r2, m_fit, c2_fit, axis_slopes = bloch_hamiltonian_kg(args.mass0, n=args.kg_n)
    slopes = list(axis_slopes.values())
    iso_ratio = max(slopes) / min(slopes) if slopes and min(slopes) > 0 else math.inf
    c11 = kg_r2 > 0.99 and iso_ratio < 1.05
    rows.append(
        ("C11 KG isotropy", f"R^2={kg_r2:.6f}, iso={iso_ratio:.4f}, m={m_fit:.4f}, c^2={c2_fit:.4f}", "PASS" if c11 else "FAIL")
    )

    ab_v = ab_flux_tube_test(args.mass0, n=args.ab_n, N=args.ab_layers)
    c12 = ab_v > 0.3
    rows.append(("C12 AB visibility", f"V={ab_v:.4f}", "PASS" if c12 else "FAIL"))

    k_metrics, c13 = matched_k_deflection_row(args.stability_n, args.mass0, args.strength, args.offset, k_values)
    k_desc = ", ".join(f"k={k:.2f}:L={L},dx={dx:.2f},dz={dz:+.2e}" for k, L, dx, dz in k_metrics["rows"])
    rows.append(("C13 fixed-theta k-achrom", f"CV={k_metrics['cv']:.4f}; {k_desc}", "PASS" if c13 else "FAIL"))

    split_metrics, c14 = split_mass_gravity_row(args.n, args.layers, args.mass0, [1e-4, 2e-4, 5e-4, 1e-3, 2e-3], args.offset, split_g_values)
    rows.append(
        (
            "C14 split mass/gravity",
            f"best_g={split_metrics['g']:.3f}, R^2={split_metrics['r2']:.4f}, bias={split_metrics['bias']:+.3e}",
            "PASS" if c14 else "FAIL",
        )
    )

    boundary_metrics, c15 = boundary_robustness_row(args.stability_n, args.mass0, args.strength, args.offset, stability_layers, distance_offsets)
    rows.append(
        (
            "C15 boundary robustness",
            f"N agree={boundary_metrics['n_agree']}/{boundary_metrics['n_total']}, offset agree={boundary_metrics['d_agree']}/{boundary_metrics['d_total']}",
            "PASS" if c15 else "FAIL",
        )
    )

    panel_metrics, c16 = panel_row(args.panel_n, panel_layers, args.mass0, args.strength, args.offset)
    rows.append(
        (
            "C16 multi-observable gravity",
            (
                f"centroid/shell={int(panel_metrics['centroid_shell_agree'])}/{int(panel_metrics['total'])}, "
                f"centroid/current={int(panel_metrics['centroid_current_agree'])}/{int(panel_metrics['total'])}, "
                f"centroid/peak={int(panel_metrics['centroid_peak_agree'])}/{int(panel_metrics['total'])}, "
                f"stable_first={bool(panel_metrics['stable_first_arrival'])}"
            ),
            "PASS" if c16 else "FAIL",
        )
    )

    print()
    print(f"{'Row':<28} {'Value':<88} Status")
    print("-" * 128)
    pass_count = 0
    for label, value, status in rows:
        classified_status = f"[C] {status}" if status in {"PASS", "FAIL"} else status
        print(f"{label:<28} {value:<88} {classified_status}")
        pass_count += int(status == "PASS")

    print("-" * 128)
    print(f"Retained periodic closure score (legacy v4 rows): {score}/10")
    print(f"Integrated core-card score shown here: {pass_count}/{len(rows)}")
    print()
    print("Interpretation:")
    print("  - KG and AB are now first-class retained 3+1D positives on the Dirac lane.")
    print("  - Record purity is judged with an explicit which-path mixture, not the old detector proxy.")
    print("  - Split mass vs gravity susceptibility is viable, but fixed-theta carrier-k achromaticity still fails.")
    print("  - Gravity stability is still the main blocker: non-monotone N-growth and mixed-sign distance law remain.")
    print("  - Centroid and shell are the primary gravity readouts; peak is not a promotion gate.")


if __name__ == "__main__":
    main()
