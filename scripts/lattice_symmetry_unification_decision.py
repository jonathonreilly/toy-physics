#!/usr/bin/env python3
"""Ordered lattice + explicit Z2 symmetry unification decision.

This script answers one narrow question:

Can the dense ordered-lattice symmetry line move from a same-family
two-harness bridge to a review-safe one-family retained setup?

Scope rules:
  - standard linear propagator only
  - no layer norm, collapse, or noncanonical harnesses
  - Born is reported as a same-family companion Sorkin audit, not the exact
    same two-slit aperture card used for MI / d_TV / gravity
"""

from __future__ import annotations

from dataclasses import dataclass
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.lattice_mirror_hybrid import K, LAM, N_YBINS, generate_lattice_mirror_hybrid, propagate

N_LAYERS = 40
HALF_WIDTH = 20
MAX_DY_VALUES = [3, 4, 5, 6]
B_VALUES = [2, 3, 4, 5, 6, 7, 8, 10, 13, 16, 19]
GEOMETRIES = {
    "narrow_center": [4],
    "wide_center": [3, 4, 5],
    "wide_outer": [4, 5, 6],
}
TRADEOFF_OFFSETS = [-1, 0, 1]
CANONICAL_GEOMETRY = "wide_center"
CANONICAL_OFFSET = 1

RETAIN_BORN_MAX = 1e-12
RETAIN_K0_MAX = 1e-9
RETAIN_MI_MIN = 0.10
RETAIN_DECOH_MIN = 0.03
RETAIN_DISTANCE_R2_MIN = 0.80


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
class DistanceFit:
    peak_b: int
    alpha: float
    r2: float


def build_setup(max_dy: int) -> Setup:
    positions, adj, barrier_layer, node_map = generate_lattice_mirror_hybrid(
        N_LAYERS,
        HALF_WIDTH,
        max_dy,
    )
    gravity_layer = 2 * N_LAYERS // 3
    source = [node_map[(0, 0)]]
    detector = [node_map[(N_LAYERS - 1, y)] for y in range(-HALF_WIDTH, HALF_WIDTH + 1)]
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


def detector_power(amps: list[complex], detector: list[int]) -> float:
    return sum(abs(amps[d]) ** 2 for d in detector)


def field_for_mass(
    positions: list[tuple[float, float]],
    node_map: dict[tuple[int, int], int],
    gravity_layer: int,
    mass_y: int,
    strength: float = 0.1,
) -> list[float]:
    mx, my = positions[node_map[(gravity_layer, mass_y)]]
    field = [0.0] * len(positions)
    for idx, (ix, iy) in enumerate(positions):
        field[idx] = strength / (math.sqrt((ix - mx) ** 2 + (iy - my) ** 2) + 0.1)
    return field


def lower_rows(upper_rows: list[int]) -> list[int]:
    return [-y for y in reversed(upper_rows)]


def aperture_for_rows(setup: Setup, upper_rows: list[int]) -> dict[str, object]:
    upper_nodes = [setup.node_map[(setup.barrier_layer, y)] for y in upper_rows]
    lower_nodes = [setup.node_map[(setup.barrier_layer, y)] for y in lower_rows(upper_rows)]
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


def cl_purity(
    setup: Setup,
    amps_a: list[complex],
    amps_b: list[complex],
) -> tuple[float, float]:
    width = 2 * (HALF_WIDTH + 1) / N_YBINS
    env_depth = max(1, round(N_LAYERS / 6))
    mid_nodes = []
    for layer in range(setup.barrier_layer + 1, min(N_LAYERS - 1, setup.barrier_layer + 1 + env_depth)):
        mid_nodes.extend(setup.node_map[(layer, y)] for y in range(-HALF_WIDTH, HALF_WIDTH + 1))

    bins_a = [0j] * N_YBINS
    bins_b = [0j] * N_YBINS
    for node in mid_nodes:
        bi = max(0, min(N_YBINS - 1, int((setup.positions[node][1] + HALF_WIDTH + 1) / width)))
        bins_a[bi] += amps_a[node]
        bins_b[bi] += amps_b[node]

    s_norm_num = sum(abs(a - b) ** 2 for a, b in zip(bins_a, bins_b))
    norm_a = sum(abs(a) ** 2 for a in bins_a)
    norm_b = sum(abs(b) ** 2 for b in bins_b)
    s_norm = s_norm_num / (norm_a + norm_b) if (norm_a + norm_b) > 0 else 0.0
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


def barrier_metrics(setup: Setup, upper_rows: list[int], mass_offset: int) -> dict[str, float]:
    aperture = aperture_for_rows(setup, upper_rows)
    mass_y = aperture["top_row"] + mass_offset
    field_mass = field_for_mass(setup.positions, setup.node_map, setup.gravity_layer, mass_y)
    field_zero = [0.0] * len(setup.positions)

    amps_mass = propagate(setup.positions, setup.adj, field_mass, setup.source, K, aperture["blocked"])
    amps_flat = propagate(setup.positions, setup.adj, field_zero, setup.source, K, aperture["blocked"])
    gravity = centroid_y(amps_mass, setup.positions, setup.detector) - centroid_y(
        amps_flat,
        setup.positions,
        setup.detector,
    )

    amps_mass_k0 = propagate(setup.positions, setup.adj, field_mass, setup.source, 0.0, aperture["blocked"])
    amps_flat_k0 = propagate(setup.positions, setup.adj, field_zero, setup.source, 0.0, aperture["blocked"])
    gravity_k0 = centroid_y(amps_mass_k0, setup.positions, setup.detector) - centroid_y(
        amps_flat_k0,
        setup.positions,
        setup.detector,
    )

    amps_upper = propagate(
        setup.positions,
        setup.adj,
        field_mass,
        setup.source,
        K,
        aperture["blocked"] | set(aperture["lower_nodes"]),
    )
    amps_lower = propagate(
        setup.positions,
        setup.adj,
        field_mass,
        setup.source,
        K,
        aperture["blocked"] | set(aperture["upper_nodes"]),
    )

    purity, s_norm = cl_purity(setup, amps_upper, amps_lower)
    result = {
        "mass_y": float(mass_y),
        "gravity": gravity,
        "gravity_abs": abs(gravity),
        "gravity_k0": gravity_k0,
        "mi": mutual_info(amps_upper, amps_lower, setup.positions, setup.detector),
        "dtv": d_tv(amps_upper, amps_lower, setup.detector),
        "pur_cl": purity,
        "decoh": 1.0 - purity if not math.isnan(purity) else math.nan,
        "born": born_companion_audit(setup, upper_rows),
        "s_norm": s_norm,
    }

    upper_flat = propagate(
        setup.positions,
        setup.adj,
        field_zero,
        setup.source,
        K,
        aperture["blocked"] | set(aperture["lower_nodes"]),
    )
    lower_flat = propagate(
        setup.positions,
        setup.adj,
        field_zero,
        setup.source,
        K,
        aperture["blocked"] | set(aperture["upper_nodes"]),
    )
    result["upper_flat_power"] = detector_power(upper_flat, setup.detector)
    result["upper_mass_power"] = detector_power(amps_upper, setup.detector)
    result["lower_flat_power"] = detector_power(lower_flat, setup.detector)
    result["lower_mass_power"] = detector_power(amps_lower, setup.detector)
    return result


def distance_curve(setup: Setup, blocked: set[int]) -> list[tuple[int, float]]:
    field_zero = [0.0] * len(setup.positions)
    amps_flat = propagate(setup.positions, setup.adj, field_zero, setup.source, K, blocked)
    flat_centroid = centroid_y(amps_flat, setup.positions, setup.detector)
    rows = []
    for b in B_VALUES:
        field_mass = field_for_mass(setup.positions, setup.node_map, setup.gravity_layer, b)
        amps_mass = propagate(setup.positions, setup.adj, field_mass, setup.source, K, blocked)
        delta = centroid_y(amps_mass, setup.positions, setup.detector) - flat_centroid
        rows.append((b, delta))
    return rows


def fit_tail(rows: list[tuple[int, float]]) -> DistanceFit | None:
    usable = [(b, abs(delta)) for b, delta in rows if not math.isnan(delta) and abs(delta) > 1e-9]
    if len(usable) < 3:
        return None
    peak_b, _ = max(usable, key=lambda item: item[1])
    tail = [(b, value) for b, value in usable if b >= peak_b]
    if len(tail) < 3:
        return None
    xs = [math.log(b) for b, _ in tail]
    ys = [math.log(value) for _, value in tail]
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    syy = sum((y - my) ** 2 for y in ys)
    if sxx <= 1e-12 or syy <= 1e-12:
        return None
    return DistanceFit(
        peak_b=peak_b,
        alpha=sxy / sxx,
        r2=(sxy * sxy) / (sxx * syy),
    )


def fit_label(fit: DistanceFit | None) -> str:
    if fit is None:
        return "none"
    return f"peak@{fit.peak_b},a={fit.alpha:.2f},R2={fit.r2:.2f}"


def curve_label(rows: list[tuple[int, float]], absolute: bool) -> str:
    parts = []
    for b, delta in rows:
        value = abs(delta) if absolute else delta
        parts.append(f"b={b}:{value:+.4f}" if not absolute else f"b={b}:{value:.4f}")
    return "  ".join(parts)


def retained(metrics: dict[str, float], distance_fit: DistanceFit | None) -> bool:
    return (
        not math.isnan(metrics["born"])
        and metrics["born"] <= RETAIN_BORN_MAX
        and not math.isnan(metrics["gravity_k0"])
        and abs(metrics["gravity_k0"]) <= RETAIN_K0_MAX
        and not math.isnan(metrics["mi"])
        and metrics["mi"] >= RETAIN_MI_MIN
        and not math.isnan(metrics["decoh"])
        and metrics["decoh"] >= RETAIN_DECOH_MIN
        and not math.isnan(metrics["gravity"])
        and metrics["gravity"] > 0.0
        and distance_fit is not None
        and distance_fit.alpha < 0.0
        and distance_fit.r2 >= RETAIN_DISTANCE_R2_MIN
    )


def main() -> None:
    print("=" * 112)
    print("LATTICE-SYMMETRY UNIFICATION DECISION")
    print("  ordered 2D lattice + explicit Z2 symmetry, standard linear propagator only")
    print("  Born is a same-family companion Sorkin audit, not the exact same 2-slit aperture card")
    print("=" * 112)
    print()

    setups = {max_dy: build_setup(max_dy) for max_dy in MAX_DY_VALUES}
    canonical_rows = []
    no_barrier_fits = {}
    barrier_curves = {}
    no_barrier_curves = {}

    print("CANONICAL DECISION SWEEP")
    print(
        f"  slit family={CANONICAL_GEOMETRY} rows={GEOMETRIES[CANONICAL_GEOMETRY]} "
        f"mass convention=top_slit+{CANONICAL_OFFSET} detector=final-layer centroid"
    )
    print(
        f"  {'max_dy':>6s}  {'mass_y':>6s}  {'MI':>7s}  {'d_TV':>7s}  {'pur_cl':>7s}  "
        f"{'1-pur':>7s}  {'grav':>9s}  {'sign':>4s}  {'k=0':>11s}  {'Born':>10s}  {'retain':>6s}"
    )
    print(f"  {'-' * 102}")
    for max_dy in MAX_DY_VALUES:
        setup = setups[max_dy]
        metrics = barrier_metrics(setup, GEOMETRIES[CANONICAL_GEOMETRY], CANONICAL_OFFSET)
        barrier_curves[max_dy] = distance_curve(setup, aperture_for_rows(setup, GEOMETRIES[CANONICAL_GEOMETRY])["blocked"])
        no_barrier_curves[max_dy] = distance_curve(setup, set())
        no_barrier_fits[max_dy] = fit_tail(no_barrier_curves[max_dy])
        row_retained = retained(metrics, no_barrier_fits[max_dy])
        canonical_rows.append((max_dy, metrics, row_retained))
        sign = "towd" if metrics["gravity"] > 0 else "away"
        print(
            f"  {max_dy:6d}  {metrics['mass_y']:6.0f}  {metrics['mi']:7.3f}  {metrics['dtv']:7.3f}  "
            f"{metrics['pur_cl']:7.3f}  {metrics['decoh']:7.3f}  {metrics['gravity']:+9.4f}  "
            f"{sign:>4s}  {metrics['gravity_k0']:+11.3e}  {metrics['born']:10.2e}  "
            f"{'yes' if row_retained else 'no':>6s}"
        )
    print()

    print("DISTANCE-LAW COMPATIBILITY: BARRIER HARNESS (canonical slit family)")
    for max_dy in MAX_DY_VALUES:
        rows = barrier_curves[max_dy]
        fit = fit_tail(rows)
        positive_count = sum(1 for _, delta in rows if delta > 0)
        print(f"  max_dy={max_dy}")
        print(f"    signed : {curve_label(rows, absolute=False)}")
        print(f"    |delta|: {curve_label(rows, absolute=True)}")
        print(f"    positive points={positive_count}  tail fit={fit_label(fit)}")
    print()

    print("DISTANCE-LAW COMPATIBILITY: NO-BARRIER COMPANION HARNESS")
    for max_dy in MAX_DY_VALUES:
        rows = no_barrier_curves[max_dy]
        fit = no_barrier_fits[max_dy]
        positive_count = sum(1 for _, delta in rows if delta > 0)
        print(f"  max_dy={max_dy}")
        print(f"    signed : {curve_label(rows, absolute=False)}")
        print(f"    |delta|: {curve_label(rows, absolute=True)}")
        print(f"    positive points={positive_count}  tail fit={fit_label(fit)}")
    print()

    print("TRADEOFF MAP")
    print(
        f"  {'max_dy':>6s}  {'slit':>13s}  {'off':>4s}  {'Born':>10s}  {'MI':>7s}  "
        f"{'1-pur':>7s}  {'grav_s':>6s}  {'|grav|':>8s}  {'distance_fit':>22s}  {'retain':>6s}"
    )
    print(f"  {'-' * 104}")
    tradeoff_rows = []
    for max_dy in MAX_DY_VALUES:
        setup = setups[max_dy]
        distance_fit = no_barrier_fits[max_dy]
        for geometry_name, upper_rows in GEOMETRIES.items():
            for offset in TRADEOFF_OFFSETS:
                metrics = barrier_metrics(setup, upper_rows, offset)
                row_retained = retained(metrics, distance_fit)
                tradeoff_rows.append((max_dy, geometry_name, offset, metrics, row_retained))
                sign = "towd" if metrics["gravity"] > 0 else "away"
                print(
                    f"  {max_dy:6d}  {geometry_name:>13s}  {offset:+4d}  {metrics['born']:10.2e}  "
                    f"{metrics['mi']:7.3f}  {metrics['decoh']:7.3f}  {sign:>6s}  "
                    f"{metrics['gravity_abs']:8.3f}  {fit_label(distance_fit):>22s}  "
                    f"{'yes' if row_retained else 'no':>6s}"
                )
    print()

    print("BEAM-DEPLETION DIAGNOSTIC (canonical slit family, mass=top_slit+1)")
    print(f"  {'max_dy':>6s}  {'upper mass/flat':>15s}  {'lower mass/flat':>15s}  {'skew':>9s}")
    print(f"  {'-' * 56}")
    for max_dy, metrics, _ in canonical_rows:
        upper_ratio = metrics["upper_mass_power"] / metrics["upper_flat_power"]
        lower_ratio = metrics["lower_mass_power"] / metrics["lower_flat_power"]
        print(
            f"  {max_dy:6d}  {upper_ratio:15.4f}  {lower_ratio:15.4f}  {upper_ratio - lower_ratio:+9.4f}"
        )
    print()

    born_clean_count = sum(1 for _, _, _, metrics, _ in tradeoff_rows if metrics["born"] <= RETAIN_BORN_MAX)
    coexistence_count = sum(
        1
        for _, _, _, metrics, _ in tradeoff_rows
        if metrics["mi"] >= RETAIN_MI_MIN and metrics["decoh"] >= RETAIN_DECOH_MIN
    )
    positive_gravity_count = sum(1 for _, _, _, metrics, _ in tradeoff_rows if metrics["gravity"] > 0)
    retained_count = sum(1 for *_, row_retained in tradeoff_rows if row_retained)

    if retained_count > 0:
        decision = "PROMOTED"
        blocker = "none"
    elif positive_gravity_count == 0 and coexistence_count > 0:
        decision = "NEGATIVE"
        blocker = "beam depletion from the symmetric two-slit geometry; aperture retuning did not fix the sign"
    else:
        decision = "BOUNDED"
        blocker = "same-slit attractive pocket not review-safe on this dense ordered-lattice window"

    print("DECISION")
    print(f"  Born-clean companion rows: {born_clean_count}/{len(tradeoff_rows)}")
    print(f"  Nontrivial MI + decoherence rows: {coexistence_count}/{len(tradeoff_rows)}")
    print(f"  Positive-gravity rows: {positive_gravity_count}/{len(tradeoff_rows)}")
    print(f"  Retained one-family rows: {retained_count}/{len(tradeoff_rows)}")
    print(f"  conclusion={decision}")
    print(f"  blocker={blocker}")


if __name__ == "__main__":
    main()
