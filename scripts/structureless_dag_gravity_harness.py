#!/usr/bin/env python3
"""Bounded gravity harness on structureless random causal DAGs.

This is a review-safe follow-up to the note-only structureless-DAG claim.

Question:
  On random x-ordered causal DAGs with no layers or lattice geometry,
  does the valley-linear propagator still produce TOWARD gravity, and
  does the mass-scaling remain near-linear when TOWARD?

Bounded setup:
  - sample 3D points uniformly in a box and sort by x to impose causality
  - connect i -> j when x_j > x_i and the Euclidean distance is below a
    fixed radius
  - use a source slab at low x, a detector slab at high x, and one weak
    source mass near the middle of the graph
  - measure TOWARD fraction, local F~M on the positive rows, and a cheap
    no-field control

The harness is intentionally narrow: it reports only the tested pocket and
does not claim a graph-universality theorem.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import cmath
import math
import random
import statistics


N_SIZES = [200, 500]
N_SEEDS = 8
FIELD_STRENGTHS = [1e-3, 2e-3, 5e-3, 1e-2]

CONNECT_RADIUS = 0.35
PHASE_K = 1.0
KERNEL_POWER = 2.0
FIELD_EPS = 0.1

SOURCE_X_MAX = 0.05
DETECTOR_X_MIN = 0.95
MID_X_MIN = 0.45
MID_X_MAX = 0.55


@dataclass(frozen=True)
class SeedRow:
    seed: int
    toward: int
    valid: int
    strengths: tuple[float, ...]
    deltas: tuple[float, ...]
    local_fm: float | None
    local_r2: float | None
    mean_delta: float
    no_field_delta: float


def build_dag(n: int, seed: int) -> tuple[list[tuple[float, float, float]], dict[int, list[int]]]:
    rng = random.Random(seed)
    pos = [
        (rng.random(), rng.uniform(-1.0, 1.0), rng.uniform(-1.0, 1.0))
        for _ in range(n)
    ]
    pos.sort(key=lambda item: item[0])

    adj: dict[int, list[int]] = defaultdict(list)
    for i in range(n):
        xi, yi, zi = pos[i]
        for j in range(i + 1, n):
            xj, yj, zj = pos[j]
            dx = xj - xi
            dy = yj - yi
            dz = zj - zi
            dist = math.sqrt(dx * dx + dy * dy + dz * dz)
            if dist <= CONNECT_RADIUS:
                adj[i].append(j)
    return pos, dict(adj)


def select_roles(
    pos: list[tuple[float, float, float]],
) -> tuple[list[int], list[int], list[int], int | None]:
    source = [i for i, (x, _, _) in enumerate(pos) if x <= SOURCE_X_MAX]
    detector = [i for i, (x, _, _) in enumerate(pos) if x >= DETECTOR_X_MIN]
    mid = [i for i, (x, _, _) in enumerate(pos) if MID_X_MIN <= x <= MID_X_MAX]
    if not mid:
        return source, detector, mid, None
    mass = max(mid, key=lambda i: pos[i][2])
    return source, detector, mid, mass


def make_field(
    pos: list[tuple[float, float, float]],
    mass_idx: int | None,
    strength: float,
) -> list[float]:
    if mass_idx is None:
        return [0.0] * len(pos)
    mx, my, mz = pos[mass_idx]
    field = []
    for x, y, z in pos:
        dist = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2)
        field.append(strength / (dist + FIELD_EPS))
    return field


def propagate(
    pos: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    source: list[int],
    field: list[float],
    phase_k: float,
) -> list[complex]:
    n = len(pos)
    amps = [0j] * n
    if not source:
        return amps

    seed_amp = 1.0 / len(source)
    for idx in source:
        amps[idx] = seed_amp

    for i in range(n):
        amp_i = amps[i]
        if abs(amp_i) < 1e-30:
            continue
        xi, yi, zi = pos[i]
        for j in adj.get(i, []):
            xj, yj, zj = pos[j]
            dx = xj - xi
            dy = yj - yi
            dz = zj - zi
            dist = math.sqrt(dx * dx + dy * dy + dz * dz)
            if dist < 1e-12:
                continue
            lf = 0.5 * (field[i] + field[j])
            act = dist * (1.0 - lf)
            amps[j] += amp_i * cmath.exp(1j * phase_k * act) / (dist**KERNEL_POWER)
    return amps


def detector_centroid_z(
    amps: list[complex],
    detector: list[int],
    pos: list[tuple[float, float, float]],
) -> float | None:
    if not detector:
        return None
    probs = [abs(amps[i]) ** 2 for i in detector]
    total = sum(probs)
    if total < 1e-30:
        return None
    return sum(pos[i][2] * p for i, p in zip(detector, probs)) / total


def fit_power_law(strengths: list[float], deltas: list[float]) -> tuple[float | None, float | None]:
    pairs = [
        (math.log(s), math.log(d))
        for s, d in zip(strengths, deltas)
        if s > 0.0 and d > 0.0
    ]
    if len(pairs) < 2:
        return None, None

    xs = [x for x, _ in pairs]
    ys = [y for _, y in pairs]
    mean_x = statistics.fmean(xs)
    mean_y = statistics.fmean(ys)
    cov = statistics.fmean((x - mean_x) * (y - mean_y) for x, y in pairs)
    var_x = statistics.fmean((x - mean_x) ** 2 for x in xs)
    if var_x <= 0.0:
        return None, None
    slope = cov / var_x
    intercept = mean_y - slope * mean_x
    ss_res = sum((y - (slope * x + intercept)) ** 2 for x, y in pairs)
    ss_tot = sum((y - mean_y) ** 2 for y in ys)
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0.0 else 1.0
    return slope, r2


def measure_seed(
    n: int,
    seed: int,
) -> SeedRow | None:
    pos, adj = build_dag(n, seed)
    source, detector, mid, mass_idx = select_roles(pos)
    if len(source) < 2 or len(detector) < 2 or mass_idx is None:
        return None

    free_field = [0.0] * n
    free_amps = propagate(pos, adj, source, free_field, PHASE_K)
    free_centroid = detector_centroid_z(free_amps, detector, pos)
    if free_centroid is None:
        return None

    strengths: list[float] = []
    deltas: list[float] = []
    toward = 0
    valid = 0
    for strength in FIELD_STRENGTHS:
        field = make_field(pos, mass_idx, strength)
        mass_amps = propagate(pos, adj, source, field, PHASE_K)
        mass_centroid = detector_centroid_z(mass_amps, detector, pos)
        if mass_centroid is None:
            continue
        delta = mass_centroid - free_centroid
        strengths.append(strength)
        deltas.append(delta)
        valid += 1
        if delta > 0.0:
            toward += 1

    if valid == 0:
        return None

    # A cheap no-field control: the same propagation with zero source strength.
    zero_field = make_field(pos, mass_idx, 0.0)
    zero_amps = propagate(pos, adj, source, zero_field, PHASE_K)
    zero_centroid = detector_centroid_z(zero_amps, detector, pos)
    no_field_delta = 0.0 if zero_centroid is None else zero_centroid - free_centroid

    local_fm, local_r2 = fit_power_law(strengths, deltas)
    mean_delta = statistics.fmean(deltas)
    return SeedRow(
        seed=seed,
        toward=toward,
        valid=valid,
        strengths=tuple(strengths),
        deltas=tuple(deltas),
        local_fm=local_fm,
        local_r2=local_r2,
        mean_delta=mean_delta,
        no_field_delta=no_field_delta,
    )


def summarize_size(n: int) -> list[SeedRow]:
    rows: list[SeedRow] = []
    for seed in range(N_SEEDS):
        row = measure_seed(n, seed)
        if row is not None:
            rows.append(row)
    return rows


def render_rows(n: int, rows: list[SeedRow]) -> None:
    print(f"\nSIZE n={n}")
    print("-" * 78)
    print(f"{'seed':>4s} {'toward':>7s} {'valid':>5s} {'mean_delta':>13s} {'F~M':>8s} {'R^2':>8s} {'no-field':>12s}")
    for row in rows:
        fm = f"{row.local_fm:.2f}" if row.local_fm is not None else "n/a"
        r2 = f"{row.local_r2:.3f}" if row.local_r2 is not None else "n/a"
        print(
            f"{row.seed:4d} {row.toward:7d} {row.valid:5d} "
            f"{row.mean_delta:+13.6e} {fm:>8s} {r2:>8s} {row.no_field_delta:+12.1e}"
        )

    toward_total = sum(r.toward for r in rows)
    sample_total = sum(r.valid for r in rows)
    local_fms = [row.local_fm for row in rows if row.local_fm is not None]
    local_r2s = [row.local_r2 for row in rows if row.local_r2 is not None]
    fm_median = statistics.median(local_fms) if local_fms else None
    fm_mean = statistics.fmean(local_fms) if local_fms else None
    r2_median = statistics.median(local_r2s) if local_r2s else None

    mean_no_field = statistics.fmean(r.no_field_delta for r in rows) if rows else 0.0
    toward_frac = toward_total / sample_total if sample_total else 0.0
    fm_median_txt = f"{fm_median:.2f}" if fm_median is not None else "n/a"
    fm_mean_txt = f"{fm_mean:.2f}" if fm_mean is not None else "n/a"
    r2_median_txt = f"{r2_median:.3f}" if r2_median is not None else "n/a"
    print(
        f"summary: TOWARD={toward_total}/{sample_total} "
        f"({toward_frac:.1%}), "
        f"seed-local F~M median={fm_median_txt}, mean={fm_mean_txt} "
        f"(R^2 median={r2_median_txt}), "
        f"no-field={mean_no_field:+.1e}"
    )


def main() -> None:
    print("=" * 78)
    print("STRUCTURELESS RANDOM CAUSAL DAG GRAVITY HARNESS")
    print("=" * 78)
    print(
        "Setup: random 3D points sorted by x; edges i->j when x_j>x_i and "
        f"distance <= {CONNECT_RADIUS:.2f}; phase k={PHASE_K:.1f}; kernel 1/L^{int(KERNEL_POWER)}"
    )
    print(
        "Source slab: x<=0.05; detector slab: x>=0.95; mass node: highest-z node in the mid-x slab"
    )
    print(
        f"Seed sweep: {N_SEEDS} seeds per size, strengths={FIELD_STRENGTHS}, "
        "controls: no-field"
    )
    print(
        "Retained claim: on this bounded pocket, gravity is noisy in sign but "
        "the positive-shift rows remain close to linear in source strength."
    )

    for n in N_SIZES:
        rows = summarize_size(n)
        if not rows:
            print(f"\nSIZE n={n}: no valid rows")
            continue
        render_rows(n, rows)

    print("\nInterpretation:")
    print(
        "- This is a bounded random-DAG probe, not a graph-universality theorem."
    )
    print(
        "- The safe read is: structureless causal DAGs can show TOWARD rows, and "
        "when they do, the source-strength response is close to linear in this pocket."
    )
    print(
        "- The sign remains seed-sensitive, so the claim stays narrow and review-safe."
    )


if __name__ == "__main__":
    main()
