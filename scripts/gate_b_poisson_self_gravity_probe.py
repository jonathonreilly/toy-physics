#!/usr/bin/env python3
"""Gate B Poisson-like self-gravity / backreaction probe.

This is the smallest retained-grown transfer test for the new backreaction
idea.

Question:
  If the propagated amplitude itself sources a weak Poisson-like correction to
  the grown-row field between steps, can we get a bounded self-gravity signal
  without breaking the zero-coupling reduction or the weak-field class?

Scope:
  - retained grown geometry row only: drift=0.2, restore=0.7
  - one static source-resolved baseline field
  - one backreaction update sourced by the propagated amplitude density
  - one exact zero-coupling reduction check
  - one bounded observable: detector centroid shift plus escape ratio

The key design rule is:
  - each propagation step is linear on a fixed field
  - the nonlinearity only enters between steps, when the propagated amplitude
    updates the next field
  - that keeps the reduction check meaningful and avoids the "just change the
    graph while propagating" trap
"""

from __future__ import annotations

import cmath
import math
import random
import statistics
import time
from dataclasses import dataclass

BETA = 0.8
K = 5.0
MAX_D_PHYS = 3
H = 0.5
NL = 25
PW = 8
DRIFT = 0.2
RESTORE = 0.7
SEEDS = [0]
EPS_SWEEP = [0.0, 0.05, 0.1, 0.2, 0.5]
SOURCE_STRENGTHS = [1e-6, 2e-6, 5e-6, 1e-5]
SOURCE_Z = 3.0
FIELD_STRENGTH = 5e-5
FIELD_EPS = 0.1
BACKREACTION_MU = 0.06
BACKREACTION_EPS = 0.25


@dataclass(frozen=True)
class SeedResult:
    seed: int
    p0: float
    delta0: float
    escape: dict[float, float]
    delta: dict[float, float]
    max_zero_diff: float


def _mean(values):
    return sum(values) / len(values) if values else math.nan


def _fit_power(xs: list[float], ys: list[float]) -> float | None:
    pairs = [(x, y) for x, y in zip(xs, ys) if x > 0 and y > 0]
    if len(pairs) < 3:
        return None
    lx = [math.log(x) for x, _ in pairs]
    ly = [math.log(y) for _, y in pairs]
    mx = sum(lx) / len(lx)
    my = sum(ly) / len(ly)
    sxx = sum((x - mx) ** 2 for x in lx)
    if sxx < 1e-12:
        return None
    sxy = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
    return sxy / sxx


def grow(seed: int):
    rng = random.Random(seed)
    hw = int(PW / H)
    md = max(1, round(MAX_D_PHYS / H))
    pos: list[tuple[float, float, float]] = []
    adj: dict[int, list[int]] = {}
    nmap: dict[tuple[int, int, int], int] = {}
    layers: list[list[int]] = []

    pos.append((0.0, 0.0, 0.0))
    nmap[(0, 0, 0)] = 0
    layers.append([0])

    for layer in range(1, NL):
        x = layer * H
        nodes: list[int] = []
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                if layer == 1:
                    y = iy * H
                    z = iz * H
                else:
                    prev = nmap.get((layer - 1, iy, iz))
                    if prev is None:
                        continue
                    _, py, pz = pos[prev]
                    y = py + rng.gauss(0.0, DRIFT * H)
                    z = pz + rng.gauss(0.0, DRIFT * H)
                    y = y * (1.0 - RESTORE) + (iy * H) * RESTORE
                    z = z * (1.0 - RESTORE) + (iz * H) * RESTORE
                idx = len(pos)
                pos.append((x, y, z))
                nmap[(layer, iy, iz)] = idx
                nodes.append(idx)
        layers.append(nodes)

        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                si = nmap.get((layer - 1, iy, iz))
                if si is None:
                    continue
                edges: list[int] = []
                for dy in range(-md, md + 1):
                    for dz in range(-md, md + 1):
                        di = nmap.get((layer, iy + dy, iz + dz))
                        if di is not None:
                            edges.append(di)
                adj[si] = adj.get(si, []) + edges

    return pos, adj, layers, nmap


def source_field(pos, nmap, z_mass: float):
    gl = 2 * NL // 3
    iz_m = round(z_mass / H)
    mi = nmap.get((gl, 0, iz_m))
    if mi is None:
        raise RuntimeError(f"no source node for z={z_mass}")
    field = [0.0] * len(pos)
    mx, my, mz = pos[mi]
    for i in range(len(pos)):
        r = math.sqrt((pos[i][0] - mx) ** 2 + (pos[i][1] - my) ** 2 + (pos[i][2] - mz) ** 2) + FIELD_EPS
        field[i] = FIELD_STRENGTH / r
    return field


def propagate(pos, adj, field):
    n = len(pos)
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    amps[0] = 1.0
    hm = H * H
    for i in order:
        if abs(amps[i]) < 1e-30:
            continue
        for j in adj.get(i, []):
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            dz = pos[j][2] - pos[i][2]
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            act = L * (1.0 - lf)
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * cmath.exp(1j * K * act) * w * hm / (L * L)
    return amps


def detector_prob(amps, det):
    return sum(abs(amps[d]) ** 2 for d in det)


def detector_centroid_z(amps, pos, det):
    probs = [abs(amps[d]) ** 2 for d in det]
    tot = sum(probs)
    if tot <= 1e-30:
        return 0.0
    return sum(p * pos[d][2] for p, d in zip(probs, det)) / tot


def layer_mass_sources(amps, pos, layers):
    sources: list[tuple[float, tuple[float, float, float]]] = []
    for layer_nodes in layers:
        mass = sum(abs(amps[i]) ** 2 for i in layer_nodes)
        if mass <= 1e-30:
            continue
        wx = wy = wz = 0.0
        for i in layer_nodes:
            w = abs(amps[i]) ** 2
            wx += w * pos[i][0]
            wy += w * pos[i][1]
            wz += w * pos[i][2]
        sources.append((mass, (wx / mass, wy / mass, wz / mass)))
    return sources


def backreaction_field(pos, amps, layers, eps: float):
    field = [0.0] * len(pos)
    if eps <= 0.0:
        return field
    sources = layer_mass_sources(amps, pos, layers)
    if not sources:
        return field
    for i, (x, y, z) in enumerate(pos):
        total = 0.0
        for mass, (mx, my, mz) in sources:
            r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + BACKREACTION_EPS
            total += mass * math.exp(-BACKREACTION_MU * r) / r
        field[i] = eps * total
    return field


def one_loop(pos, adj, layers, base_field, eps: float):
    psi0 = propagate(pos, adj, base_field)
    br_field = backreaction_field(pos, psi0, layers, eps)
    psi1 = propagate(pos, adj, [b + br for b, br in zip(base_field, br_field)])
    return psi0, psi1, br_field


def main() -> None:
    t0 = time.time()
    print("=" * 104)
    print("GATE B POISSON SELF-GRAVITY PROBE")
    print("  retained grown row only: drift=0.2, restore=0.7")
    print("  promoted observable: detector centroid shift and escape after one backreaction loop")
    print("  guardrail: eps=0 must exactly recover the frozen grown baseline")
    print("=" * 104)
    print(
        f"h={H}, W={PW}, NL={NL}, seeds={SEEDS}, source_z={SOURCE_Z}, "
        f"source strengths={SOURCE_STRENGTHS}, eps sweep={EPS_SWEEP}"
    )
    print(
        f"backreaction kernel: exp(-mu r)/(r+eps), mu={BACKREACTION_MU:.2f}, "
        f"eps0={BACKREACTION_EPS:.2f}"
    )
    print()

    rows: list[SeedResult] = []
    for seed in SEEDS:
        print(f"  seed {seed}: building grown row and running one-loop backreaction...", flush=True)
        pos, adj, layers, nmap = grow(seed)
        det = layers[-1]
        free = propagate(pos, adj, [0.0] * len(pos))
        free_det = detector_centroid_z(free, pos, det)

        baseline = propagate(pos, adj, source_field(pos, nmap, SOURCE_Z))
        p0 = detector_prob(baseline, det)
        delta0 = detector_centroid_z(baseline, pos, det) - free_det

        escape: dict[float, float] = {}
        delta: dict[float, float] = {}
        max_zero_diff = 0.0
        for eps in EPS_SWEEP:
            psi0, psi1, _ = one_loop(pos, adj, layers, source_field(pos, nmap, SOURCE_Z), eps)
            p1 = detector_prob(psi1, det)
            escape[eps] = p1 / p0 if p0 > 1e-30 else 0.0
            delta[eps] = detector_centroid_z(psi1, pos, det) - free_det
            if eps == 0.0:
                max_zero_diff = max(abs(a - b) for a, b in zip(psi0, psi1))

        rows.append(
            SeedResult(
                seed=seed,
                p0=p0,
                delta0=delta0,
                escape=escape,
                delta=delta,
                max_zero_diff=max_zero_diff,
            )
        )
        print(f"  seed {seed}: done", flush=True)

    print(f"{'seed':>4s} {'P_det(0)':>14s} {'delta(0)':>12s} " + " ".join(f"{eps:>9.2f}" for eps in EPS_SWEEP[1:]))
    print("-" * 104)
    for row in rows:
        vals = [f"{row.seed:4d}", f"{row.p0:14.6e}", f"{row.delta0:+12.6e}"]
        for eps in EPS_SWEEP[1:]:
            vals.append(f"{row.escape[eps]:9.3f}")
        print(" ".join(vals))

    print()
    print("ZERO-COUPLING REDUCTION")
    print(f"  max |psi(eps=0) - baseline| = {max(r.max_zero_diff for r in rows):.3e}")
    print()
    print(f"{'eps':>6s} {'mean escape':>12s} {'mean delta':>12s} {'direction':>10s}")
    print("-" * 48)
    mean_delta_by_eps: dict[float, float] = {}
    for eps in EPS_SWEEP:
        mean_escape = _mean([r.escape[eps] for r in rows])
        mean_delta = _mean([r.delta[eps] for r in rows])
        mean_delta_by_eps[eps] = mean_delta
        direction = "TOWARD" if mean_delta > 0 else "AWAY"
        print(f"{eps:6.2f} {mean_escape:12.3f} {mean_delta:12.6e} {direction:>10s}")

    print()
    print("WEAK-FIELD MASS LAW CHECK")
    for eps in (0.0, 0.1):
        per_s: list[float] = []
        for s in SOURCE_STRENGTHS:
            vals = []
            for seed in SEEDS:
                pos, adj, layers, nmap = grow(seed)
                det = layers[-1]
                free = propagate(pos, adj, [0.0] * len(pos))
                free_det = detector_centroid_z(free, pos, det)
                base_field = source_field(pos, nmap, SOURCE_Z)
                scaled_field = [s * v for v in base_field]
                psi0, psi1, _ = one_loop(pos, adj, layers, scaled_field, eps)
                vals.append(abs(detector_centroid_z(psi1, pos, det) - free_det))
            per_s.append(_mean(vals))
        alpha = _fit_power(SOURCE_STRENGTHS, per_s)
        print(
            f"  eps={eps:4.2f}: F~M exponent = "
            f"{alpha:.2f}" if alpha is not None else f"  eps={eps:4.2f}: F~M exponent = n/a"
        )

    print()
    print("SAFE READ")
    print("  - eps=0 exactly recovers the frozen grown baseline.")
    print("  - The backreaction loop is materially different from the static field,")
    print("    but the only promoted observable here is the detector centroid shift.")
    print("  - If the weak-field exponent stays near 1 and the centroid shift grows")
    print("    monotonically with eps, this is a bounded self-gravity bridge;")
    print("    if the exponent collapses, freeze it as a no-go.")
    print(f"  runtime = {time.time() - t0:.2f}s")


if __name__ == "__main__":
    main()
