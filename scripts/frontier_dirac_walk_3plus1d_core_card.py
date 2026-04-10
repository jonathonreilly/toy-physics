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

from frontier_dirac_walk_3plus1d_decoherence_probe import run_case as run_decoherence_case  # noqa: E402
from frontier_dirac_walk_3plus1d_observable_panel import evolve_panel, summarize_panel  # noqa: E402
from frontier_dirac_walk_3plus1d_v3 import ab_flux_tube_test, bloch_hamiltonian_kg  # noqa: E402
from frontier_dirac_walk_3plus1d_v4_convergence import (  # noqa: E402
    closure_card,
    fit_power_law,
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
    args = parser.parse_args()

    stability_layers = [int(x) for x in args.stability_layers.split(",") if x]
    distance_offsets = [int(x) for x in args.distance_offsets.split(",") if x]
    panel_layers = [int(x) for x in args.panel_layers.split(",") if x]
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

    record_passes = []
    for n_case, steps_case in record_cases:
        rec_metrics, rec_pass = record_row(n_case, steps_case, args.mass0)
        record_passes.append(rec_pass)
        rows.append(
            (
                f"C6 record purity ({n_case},{steps_case})",
                (
                    f"pur={rec_metrics['record_purity']:.4f}, "
                    f"L1={rec_metrics['residual']:.4f}, "
                    f"proxy_gap={rec_metrics['proxy_gap']:.4f}"
                ),
                "PASS" if rec_pass else "FAIL",
            )
        )

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
        print(f"{label:<28} {value:<88} {status}")
        pass_count += int(status == "PASS")

    print("-" * 128)
    print(f"Retained periodic closure score (legacy v4 rows): {score}/10")
    print(f"Integrated core-card score shown here: {pass_count}/{len(rows)}")
    print()
    print("Interpretation:")
    print("  - KG and AB are now first-class retained 3+1D positives on the Dirac lane.")
    print("  - Record purity is judged with an explicit which-path mixture, not the old detector proxy.")
    print("  - Gravity stability is still the main blocker: non-monotone N-growth and mixed-sign distance law remain.")
    print("  - Centroid and shell are the primary gravity readouts; peak is not a promotion gate.")


if __name__ == "__main__":
    main()
