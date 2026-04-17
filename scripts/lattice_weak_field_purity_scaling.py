#!/usr/bin/env python3
"""Purity scaling on the retained weak-field ordered-lattice pocket.

This script freezes one narrow question:

  Does the retained weak-field lattice pocket keep a real scaling law in the
  CL-bath purity as N changes, or is the apparent exponent only a small-window
  descriptive fit?

Scope rules:
  - standard linear propagator only
  - same ordered 2D lattice + explicit Z2 symmetry family
  - same weak-field family retained in the field-strength reopening note
  - Born is a same-family companion Sorkin audit, not the exact same 2-slit
    aperture card used for MI / d_TV / gravity
"""

from __future__ import annotations

from dataclasses import dataclass
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.lattice_mirror_hybrid import K, LAM, N_YBINS, generate_lattice_mirror_hybrid, propagate
HALF_WIDTH = 20
MAX_DY = 5
STRENGTH = 0.0005
SLIT_ROWS = [3, 4, 5]
MASS_OFFSET = 1
B_VALUES = [2, 3, 4, 5, 6, 7, 8, 10, 13, 16, 19]
N_VALUES = [20, 30, 40, 50, 60, 80, 100]


@dataclass(frozen=True)
class Setup:
    positions: list[tuple[float, float]]
    adj: dict[int, list[int]]
    barrier_layer: int
    gravity_layer: int
    node_map: dict[tuple[int, int], int]
    source: list[int]
    detector: list[int]
    barrier_nodes: list[int]


@dataclass(frozen=True)
class Fit:
    coeff: float
    alpha: float
    r2: float


def build_setup(n_layers: int) -> Setup:
    positions, adj, barrier_layer, node_map = generate_lattice_mirror_hybrid(
        n_layers,
        HALF_WIDTH,
        MAX_DY,
    )
    gravity_layer = 2 * n_layers // 3
    source = [node_map[(0, 0)]]
    detector = [node_map[(n_layers - 1, y)] for y in range(-HALF_WIDTH, HALF_WIDTH + 1)]
    barrier_nodes = [node_map[(barrier_layer, y)] for y in range(-HALF_WIDTH, HALF_WIDTH + 1)]
    return Setup(
        positions=positions,
        adj=adj,
        barrier_layer=barrier_layer,
        gravity_layer=gravity_layer,
        node_map=node_map,
        source=source,
        detector=detector,
        barrier_nodes=barrier_nodes,
    )


def centroid_y(amps: list[complex], positions: list[tuple[float, float]], detector: list[int]) -> float:
    total = sum(abs(amps[d]) ** 2 for d in detector)
    if total <= 1e-30:
        return math.nan
    return sum(abs(amps[d]) ** 2 * positions[d][1] for d in detector) / total


def field_for_mass(
    positions: list[tuple[float, float]],
    node_map: dict[tuple[int, int], int],
    gravity_layer: int,
    mass_y: int,
    strength: float = STRENGTH,
) -> list[float]:
    mx, my = positions[node_map[(gravity_layer, mass_y)]]
    field = [0.0] * len(positions)
    for idx, (ix, iy) in enumerate(positions):
        field[idx] = strength / (math.sqrt((ix - mx) ** 2 + (iy - my) ** 2) + 0.1)
    return field


def aperture_for_rows(setup: Setup, upper_rows: list[int]) -> dict[str, object]:
    upper_nodes = [setup.node_map[(setup.barrier_layer, y)] for y in upper_rows]
    lower_rows = [-y for y in reversed(upper_rows)]
    lower_nodes = [setup.node_map[(setup.barrier_layer, y)] for y in lower_rows]
    blocked = set(setup.barrier_nodes) - set(upper_nodes + lower_nodes)
    return {
        "upper_nodes": upper_nodes,
        "lower_nodes": lower_nodes,
        "blocked": blocked,
        "top_row": max(upper_rows),
    }


def born_companion_audit(setup: Setup, upper_rows: list[int]) -> float:
    representative = upper_rows[len(upper_rows) // 2]
    upper = [setup.node_map[(setup.barrier_layer, representative)]]
    lower = [setup.node_map[(setup.barrier_layer, -representative)]]
    center = [setup.node_map[(setup.barrier_layer, 0)]]
    all_slits = set(upper + lower + center)
    other = set(setup.barrier_nodes) - all_slits
    field_zero = [0.0] * len(setup.positions)
    probs = {}
    for key, open_set in [
        ("abc", all_slits),
        ("ab", set(upper + lower)),
        ("ac", set(upper + center)),
        ("bc", set(lower + center)),
        ("a", set(upper)),
        ("b", set(lower)),
        ("c", set(center)),
    ]:
        blocked = other | (all_slits - open_set)
        amps = propagate(setup.positions, setup.adj, field_zero, setup.source, K, blocked)
        probs[key] = [abs(amps[d]) ** 2 for d in setup.detector]

    i3_sum = 0.0
    p_abc = 0.0
    for idx in range(len(setup.detector)):
        term = (
            probs["abc"][idx]
            - probs["ab"][idx]
            - probs["ac"][idx]
            - probs["bc"][idx]
            + probs["a"][idx]
            + probs["b"][idx]
            + probs["c"][idx]
        )
        i3_sum += abs(term)
        p_abc += probs["abc"][idx]
    return i3_sum / p_abc if p_abc > 1e-30 else math.nan


def mutual_info(amps_a: list[complex], amps_b: list[complex], positions: list[tuple[float, float]], detector: list[int]) -> float:
    width = 2 * (HALF_WIDTH + 1) / N_YBINS
    prob_a = [0.0] * N_YBINS
    prob_b = [0.0] * N_YBINS
    for d in detector:
        bi = max(0, min(N_YBINS - 1, int((positions[d][1] + HALF_WIDTH + 1) / width)))
        prob_a[bi] += abs(amps_a[d]) ** 2
        prob_b[bi] += abs(amps_b[d]) ** 2
    norm_a = sum(prob_a)
    norm_b = sum(prob_b)
    if norm_a <= 1e-30 or norm_b <= 1e-30:
        return math.nan
    prob_a = [p / norm_a for p in prob_a]
    prob_b = [p / norm_b for p in prob_b]

    entropy_mix = 0.0
    entropy_cond = 0.0
    for idx in range(N_YBINS):
        mix = 0.5 * prob_a[idx] + 0.5 * prob_b[idx]
        if mix > 1e-30:
            entropy_mix -= mix * math.log2(mix)
        if prob_a[idx] > 1e-30:
            entropy_cond -= 0.5 * prob_a[idx] * math.log2(prob_a[idx])
        if prob_b[idx] > 1e-30:
            entropy_cond -= 0.5 * prob_b[idx] * math.log2(prob_b[idx])
    return entropy_mix - entropy_cond


def d_tv(amps_a: list[complex], amps_b: list[complex], detector: list[int]) -> float:
    prob_a = {d: abs(amps_a[d]) ** 2 for d in detector}
    prob_b = {d: abs(amps_b[d]) ** 2 for d in detector}
    norm_a = sum(prob_a.values())
    norm_b = sum(prob_b.values())
    if norm_a <= 1e-30 or norm_b <= 1e-30:
        return math.nan
    return 0.5 * sum(abs(prob_a[d] / norm_a - prob_b[d] / norm_b) for d in detector)


def cl_purity(setup: Setup, amps_a: list[complex], amps_b: list[complex]) -> tuple[float, float]:
    width = 2 * (HALF_WIDTH + 1) / N_YBINS
    n_layers = len({round(p[0]) for p in setup.positions})
    env_depth = max(1, round(n_layers / 6))
    mid_nodes = []
    for layer in range(setup.barrier_layer + 1, min(n_layers - 1, setup.barrier_layer + 1 + env_depth)):
        mid_nodes.extend(setup.node_map[(layer, y)] for y in range(-HALF_WIDTH, HALF_WIDTH + 1))

    bins_a = [0j] * N_YBINS
    bins_b = [0j] * N_YBINS
    for node in mid_nodes:
        bi = max(0, min(N_YBINS - 1, int((setup.positions[node][1] + HALF_WIDTH + 1) / width)))
        bins_a[bi] += amps_a[node]
        bins_b[bi] += amps_b[node]

    s_num = sum(abs(a - b) ** 2 for a, b in zip(bins_a, bins_b))
    norm_a = sum(abs(a) ** 2 for a in bins_a)
    norm_b = sum(abs(b) ** 2 for b in bins_b)
    s_norm = s_num / (norm_a + norm_b) if (norm_a + norm_b) > 0 else 0.0
    d_cl = math.exp(-(LAM ** 2) * s_norm)

    rho = {}
    for d1 in setup.detector:
        for d2 in setup.detector:
            rho[(d1, d2)] = (
                amps_a[d1].conjugate() * amps_a[d2]
                + amps_b[d1].conjugate() * amps_b[d2]
                + d_cl * amps_a[d1].conjugate() * amps_b[d2]
                + d_cl * amps_b[d1].conjugate() * amps_a[d2]
            )

    trace = sum(rho[(d, d)] for d in setup.detector).real
    if trace <= 1e-30:
        return math.nan, s_norm
    for key in rho:
        rho[key] /= trace
    purity = sum(abs(value) ** 2 for value in rho.values()).real
    return purity, s_norm


def fit_power_law(points: list[tuple[int, float]]) -> Fit | None:
    usable = [(n, v) for n, v in points if n > 0 and v > 0 and not math.isnan(v)]
    if len(usable) < 3:
        return None
    xs = [math.log(n) for n, _ in usable]
    ys = [math.log(v) for _, v in usable]
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    syy = sum((y - my) ** 2 for y in ys)
    if sxx <= 1e-12 or syy <= 1e-12:
        return None
    alpha = sxy / sxx
    coeff = math.exp(my - alpha * mx)
    r2 = (sxy * sxy) / (sxx * syy)
    return Fit(coeff=coeff, alpha=alpha, r2=r2)


def main() -> None:
    print("=" * 96)
    print("LATTICE WEAK-FIELD PURITY SCALING")
    print("  ordered 2D lattice + explicit Z2 symmetry, standard linear propagator only")
    print("  canonical family: max_dy=5, wide_center, strength=0.0005")
    print("=" * 96)
    print()

    rows = []
    print("PURITY SWEEP")
    print(
        f"  {'N':>4s}  {'MI':>7s}  {'d_TV':>7s}  {'1-pur':>7s}  {'grav@b6':>9s}  {'+b':>3s}  "
        f"{'Born':>10s}  {'k=0':>11s}  {'fit':>20s}  {'retain':>6s}"
    )
    print(f"  {'-' * 92}")

    for n_layers in N_VALUES:
        setup = build_setup(n_layers)
        aperture = aperture_for_rows(setup, SLIT_ROWS)
        mass_y = aperture["top_row"] + MASS_OFFSET
        field_m = field_for_mass(setup.positions, setup.node_map, setup.gravity_layer, mass_y, strength=STRENGTH)
        field_zero = [0.0] * len(setup.positions)

        amps_mass = propagate(setup.positions, setup.adj, field_m, setup.source, K, aperture["blocked"])
        amps_flat = propagate(setup.positions, setup.adj, field_zero, setup.source, K, aperture["blocked"])
        gravity = centroid_y(amps_mass, setup.positions, setup.detector) - centroid_y(
            amps_flat,
            setup.positions,
            setup.detector,
        )

        amps_mass_k0 = propagate(setup.positions, setup.adj, field_m, setup.source, 0.0, aperture["blocked"])
        amps_flat_k0 = propagate(setup.positions, setup.adj, field_zero, setup.source, 0.0, aperture["blocked"])
        gravity_k0 = centroid_y(amps_mass_k0, setup.positions, setup.detector) - centroid_y(
            amps_flat_k0,
            setup.positions,
            setup.detector,
        )

        amps_upper = propagate(
            setup.positions,
            setup.adj,
            field_m,
            setup.source,
            K,
            aperture["blocked"] | set(aperture["lower_nodes"]),
        )
        amps_lower = propagate(
            setup.positions,
            setup.adj,
            field_m,
            setup.source,
            K,
            aperture["blocked"] | set(aperture["upper_nodes"]),
        )
        mi = mutual_info(amps_upper, amps_lower, setup.positions, setup.detector)
        dtv = d_tv(amps_upper, amps_lower, setup.detector)
        purity, s_norm = cl_purity(setup, amps_upper, amps_lower)
        born = born_companion_audit(setup, SLIT_ROWS)
        decoh = 1.0 - purity if not math.isnan(purity) else math.nan

        barrier_rows = []
        amps_flat = propagate(setup.positions, setup.adj, field_zero, setup.source, K, aperture["blocked"])
        flat_centroid = centroid_y(amps_flat, setup.positions, setup.detector)
        for b in B_VALUES:
            field_b = field_for_mass(setup.positions, setup.node_map, setup.gravity_layer, b, strength=STRENGTH)
            amps_b = propagate(setup.positions, setup.adj, field_b, setup.source, K, aperture["blocked"])
            delta = centroid_y(amps_b, setup.positions, setup.detector) - flat_centroid
            barrier_rows.append((b, delta))

        fit = fit_power_law([(b, abs(delta)) for b, delta in barrier_rows if b >= 7 and abs(delta) > 1e-9])
        positive_b = sum(1 for _, delta in barrier_rows if delta > 0)
        retained = (
            not math.isnan(born)
            and born <= 1e-12
            and not math.isnan(gravity_k0)
            and abs(gravity_k0) <= 1e-9
            and not math.isnan(mi)
            and mi >= 0.10
            and not math.isnan(decoh)
            and decoh >= 0.03
            and not math.isnan(gravity)
            and gravity > 0.0
            and positive_b == len(B_VALUES)
            and fit is not None
            and fit.alpha < 0.0
            and fit.r2 >= 0.80
        )
        rows.append(
            {
                "N": n_layers,
                "mi": mi,
                "dtv": dtv,
                "purity": purity,
                "decoh": decoh,
                "gravity": gravity,
                "gravity_k0": gravity_k0,
                "born": born,
                "positive_b": positive_b,
                "fit": fit,
                "s_norm": s_norm,
                "barrier_rows": barrier_rows,
                "retained": retained,
            }
        )
        print(
            f"  {n_layers:4d}  {mi:7.3f}  {dtv:7.3f}  {decoh:7.3f}  {gravity:+9.4f}  "
            f"{positive_b:3d}  {born:10.2e}  {gravity_k0:+11.3e}  "
            f"{(f'a={fit.alpha:.2f},R2={fit.r2:.2f}' if fit else 'none'):>20s}  "
            f"{'yes' if retained else 'no':>6s}"
        )

    print()
    print("CANONICAL ROW")
    canonical = next(row for row in rows if row["N"] == 40)
    print(
        f"  N=40 max_dy={MAX_DY} slit=wide_center strength={STRENGTH:.4f} "
        f"Born={canonical['born']:.2e} k=0={canonical['gravity_k0']:+.2e}"
    )
    print(
        f"  MI={canonical['mi']:.3f} d_TV={canonical['dtv']:.3f} "
        f"1-pur={canonical['decoh']:.3f} grav@b6={canonical['gravity']:+.4f}"
    )
    if canonical["fit"] is None:
        canonical_fit = "none"
    else:
        canonical_fit = f"a={canonical['fit'].alpha:.2f},R2={canonical['fit'].r2:.2f}"
    print(f"  positive_b={canonical['positive_b']}/{len(B_VALUES)} fit={canonical_fit}")
    print()

    fit_all = fit_power_law([(row["N"], row["decoh"]) for row in rows if row["decoh"] > 0])
    fit_retained = fit_power_law([(row["N"], row["decoh"]) for row in rows if row["retained"] and row["decoh"] > 0])
    print("PURITY FIT")
    if fit_all is None:
        print("  all rows: fit=none")
    else:
        n_half = (0.5 / fit_all.coeff) ** (1.0 / fit_all.alpha) if fit_all.alpha != 0 else math.inf
        print(f"  all rows: 1-pur_cl ~= {fit_all.coeff:.4f} * N^({fit_all.alpha:+.3f})")
        print(f"  all rows: R^2 = {fit_all.r2:.4f}")
        print(f"  all rows: N_half ~= {n_half:.3e}")
    if fit_retained is None:
        print("  retained rows: fit=none")
    else:
        n_half_r = (0.5 / fit_retained.coeff) ** (1.0 / fit_retained.alpha) if fit_retained.alpha != 0 else math.inf
        print(f"  retained rows: 1-pur_cl ~= {fit_retained.coeff:.4f} * N^({fit_retained.alpha:+.3f})")
        print(f"  retained rows: R^2 = {fit_retained.r2:.4f}")
        print(f"  retained rows: N_half ~= {n_half_r:.3e}")
    print()

    retained_rows = [row for row in rows if row["retained"]]
    print("DECISION")
    print(f"  retained rows: {len(retained_rows)}/{len(rows)}")
    print(f"  Born-clean rows: {sum(1 for row in rows if row['born'] <= 1e-12)}/{len(rows)}")
    print(f"  positive-gravity rows: {sum(1 for row in rows if row['gravity'] > 0)}/{len(rows)}")
    print(f"  conclusion={'PROMOTED' if len(retained_rows) > 0 else 'BOUNDED'}")


if __name__ == "__main__":
    main()
