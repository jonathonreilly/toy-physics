#!/usr/bin/env python3
"""Fine-H lensing replay.

Usage:
  python3 lensing_fine_h_batch.py
  python3 lensing_fine_h_batch.py <family> <seed>

No-arg mode replays the full 3-family x 5-seed audit artifact. Argument
mode preserves the original one-family/seed batch output.
"""

from __future__ import annotations
from concurrent.futures import ProcessPoolExecutor, as_completed
import math
import os
import random
import sys
import time

AUDIT_TIMEOUT_SEC = 3600
BETA = 0.8
K_PER_H = 2.5
T_PHYS = 15.0
PW_PHYS = 6.0
MAX_D_PHYS = 3.0
SRC_LAYER_FRAC = 1.0 / 3.0
B_VALUES = [3.0, 4.0, 5.0, 6.0]
SEEDS = [0, 1, 2, 3, 4]
DEFAULT_WORKERS = 4

FAMILIES = {
    "Fam1": (0.20, 0.70),
    "Fam2": (0.05, 0.30),
    "Fam3": (0.50, 0.90),
}


def sample_std(values):
    if len(values) < 2:
        return float("nan")
    mean = sum(values) / len(values)
    return math.sqrt(sum((x - mean) ** 2 for x in values) / (len(values) - 1))


def population_std(values):
    if not values:
        return float("nan")
    mean = sum(values) / len(values)
    return math.sqrt(sum((x - mean) ** 2 for x in values) / len(values))


def power_law_fit(bs, ks):
    valid = [(b, k) for b, k in zip(bs, ks) if not math.isnan(k) and k > 0]
    if len(valid) < 3:
        return None
    bs_v, ks_v = zip(*valid)
    n = len(bs_v)
    log_b = [math.log(b) for b in bs_v]
    log_k = [math.log(k) for k in ks_v]
    sx, sy = sum(log_b), sum(log_k)
    sxx = sum(x * x for x in log_b)
    sxy = sum(x * y for x, y in zip(log_b, log_k))
    den = n * sxx - sx * sx
    if abs(den) < 1e-30:
        return None
    slope = (n * sxy - sx * sy) / den
    intercept = (sy - slope * sx) / n
    pred = [slope * x + intercept for x in log_b]
    ss_res = sum((y - p) ** 2 for y, p in zip(log_k, pred))
    ss_tot = sum((y - sy / n) ** 2 for y in log_k)
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 1e-30 else 0.0
    return slope, math.exp(intercept), r2


def grow(seed, drift, restore, NL, PW, H):
    rng = random.Random(seed)
    hw = int(PW / H)
    md = max(1, round(MAX_D_PHYS / H))
    pos = []
    adj = {}
    nmap = {}
    pos.append((0.0, 0.0, 0.0))
    nmap[(0, 0, 0)] = 0
    for layer in range(1, NL):
        x = layer * H
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                if layer == 1:
                    y, z = iy * H, iz * H
                else:
                    prev = nmap.get((layer - 1, iy, iz))
                    if prev is None:
                        continue
                    _, py, pz = pos[prev]
                    y = py + rng.gauss(0, drift * H)
                    z = pz + rng.gauss(0, drift * H)
                    y = y * (1 - restore) + (iy * H) * restore
                    z = z * (1 - restore) + (iz * H) * restore
                idx = len(pos)
                pos.append((x, y, z))
                nmap[(layer, iy, iz)] = idx
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                si = nmap.get((layer - 1, iy, iz))
                if si is None:
                    continue
                for dy in range(-md, md + 1):
                    for dz in range(-md, md + 1):
                        di = nmap.get((layer, iy + dy, iz + dz))
                        if di is not None:
                            adj.setdefault(si, []).append(di)
    return pos, adj, nmap, NL, hw


def true_kubo(pos, adj, NL, PW, H, k_phase, x_src, z_src):
    n = len(pos)
    A = [0j] * n
    B = [0j] * n
    A[0] = 1.0 + 0j
    order = sorted(range(n), key=lambda i: pos[i][0])
    h2 = H * H
    for i in order:
        ai = A[i]
        bi = B[i]
        if abs(ai) < 1e-30 and abs(bi) < 1e-30:
            continue
        for j in adj.get(i, []):
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            dz = pos[j][2] - pos[i][2]
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            mx = 0.5 * (pos[i][0] + pos[j][0])
            mz = 0.5 * (pos[i][2] + pos[j][2])
            r_field = math.sqrt((mx - x_src) ** 2 + (mz - z_src) ** 2) + 0.1
            phase = k_phase * L
            phi = complex(math.cos(phase), math.sin(phase))
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            w_eff = w * h2 / (L * L)
            dphi_ds = complex(0.0, -k_phase * L / r_field) * phi
            A[j] += ai * phi * w_eff
            B[j] += (bi * phi + ai * dphi_ds) * w_eff

    hw = int(PW / H)
    npl = (2 * hw + 1) ** 2
    ds_idx = n - npl
    weights = [abs(A[k]) ** 2 for k in range(ds_idx, n)]
    zs = [pos[k][2] for k in range(ds_idx, n)]
    T0 = sum(weights)
    if T0 <= 0:
        return float('nan')
    cz_free = sum(w * z for w, z in zip(weights, zs)) / T0
    dT_ds = sum(2.0 * (A[k].conjugate() * B[k]).real for k in range(ds_idx, n))
    dN_ds = sum(2.0 * (A[k].conjugate() * B[k]).real * pos[k][2]
                for k in range(ds_idx, n))
    N0 = T0 * cz_free
    kubo = dN_ds / T0 - N0 * dT_ds / (T0 * T0)
    return kubo


def run_family_seed(fam_name, seed):
    drift, restore = FAMILIES[fam_name]
    H = 0.25
    NL = int(T_PHYS / H) + 1
    k_phase = K_PER_H / H
    x_src = int(NL * SRC_LAYER_FRAC) * H

    t0 = time.time()
    pos, adj, nmap, _, hw = grow(seed, drift, restore, NL, PW_PHYS, H)
    dt_grow = time.time() - t0
    kubos = {}
    timings = {}

    for b in B_VALUES:
        t1 = time.time()
        k = true_kubo(pos, adj, NL, PW_PHYS, H, k_phase, x_src, b)
        dt = time.time() - t1
        kubos[b] = k
        timings[b] = dt

    return {
        "family": fam_name,
        "seed": seed,
        "kubos": kubos,
        "timings": timings,
        "grow_sec": dt_grow,
        "nodes": len(pos),
        "hw": hw,
    }


def run_single(fam_name, seed):
    if fam_name not in FAMILIES:
        raise SystemExit(f"unknown family {fam_name!r}; expected one of {sorted(FAMILIES)}")
    result = run_family_seed(fam_name, seed)
    for b in B_VALUES:
        print(
            f"RESULT {fam_name} seed={seed} b={b:.1f} "
            f"kubo={result['kubos'][b]:+.6f} t={result['timings'][b]:.1f}s",
            flush=True,
        )

    print(
        f"DONE {fam_name} seed={seed} "
        f"grow={result['grow_sec']:.1f}s nodes={result['nodes']}",
        flush=True,
    )


def run_all():
    tasks = [(fam, seed) for fam in FAMILIES for seed in SEEDS]
    workers = min(
        len(tasks),
        max(1, int(os.environ.get("LENSING_FINE_H_WORKERS", DEFAULT_WORKERS))),
    )
    results = {}

    print("FINE_H_FAMILY_UNIVERSALITY_REPLAY")
    print(f"H=0.25 T_phys={T_PHYS:.1f} K_PER_H={K_PER_H:.1f} beta={BETA:.1f}")
    print(f"families={list(FAMILIES)} seeds={SEEDS} b_values={B_VALUES} workers={workers}")

    with ProcessPoolExecutor(max_workers=workers) as pool:
        future_map = {pool.submit(run_family_seed, fam, seed): (fam, seed) for fam, seed in tasks}
        for future in as_completed(future_map):
            fam, seed = future_map[future]
            results[(fam, seed)] = future.result()
            print(f"COMPLETED {fam} seed={seed}", flush=True)

    all_slopes = []
    family_slopes = {}

    for fam in FAMILIES:
        print("")
        print(f"FAMILY {fam}")
        for seed in SEEDS:
            result = results[(fam, seed)]
            kubo_text = " ".join(f"b={b:.1f}:{result['kubos'][b]:+.6f}" for b in B_VALUES)
            print(
                f"SEED {seed} nodes={result['nodes']} hw={result['hw']} "
                f"grow_sec={result['grow_sec']:.1f} {kubo_text}"
            )

        print("B_MEANS")
        mean_kubos = {}
        for b in B_VALUES:
            vals = [results[(fam, seed)]["kubos"][b] for seed in SEEDS]
            mean = sum(vals) / len(vals)
            sigma = sample_std(vals)
            mean_kubos[b] = mean
            print(f"b={b:.1f} mean={mean:+.6f} sample_sigma={sigma:.6f}")

        fit = power_law_fit(B_VALUES, [mean_kubos[b] for b in B_VALUES])
        if fit is not None:
            slope, prefactor, r2 = fit
            print(f"SEED_MEAN_FIT slope={slope:+.6f} prefactor={prefactor:.6f} r2={r2:.6f}")

        seed_slopes = []
        for seed in SEEDS:
            vals = [results[(fam, seed)]["kubos"][b] for b in B_VALUES]
            seed_fit = power_law_fit(B_VALUES, vals)
            if seed_fit is None:
                print(f"SEED_FIT seed={seed} status=failed")
                continue
            slope, prefactor, r2 = seed_fit
            seed_slopes.append(slope)
            all_slopes.append(slope)
            print(f"SEED_FIT seed={seed} slope={slope:+.6f} prefactor={prefactor:.6f} r2={r2:.6f}")

        family_slopes[fam] = seed_slopes
        if seed_slopes:
            print(
                f"FAMILY_SLOPE_SUMMARY mean={sum(seed_slopes)/len(seed_slopes):+.6f} "
                f"sample_sigma={sample_std(seed_slopes):.6f} n={len(seed_slopes)}"
            )

    print("")
    print("CROSS_FAMILY_SUMMARY")
    if all_slopes:
        print(
            f"grand_mean={sum(all_slopes)/len(all_slopes):+.6f} "
            f"population_sigma={population_std(all_slopes):.6f} "
            f"sample_sigma={sample_std(all_slopes):.6f} n={len(all_slopes)}"
        )
    for fam, slopes in family_slopes.items():
        if slopes:
            print(
                f"family={fam} mean_slope={sum(slopes)/len(slopes):+.6f} "
                f"sample_sigma={sample_std(slopes):.6f}"
            )
    for i, fam_a in enumerate(FAMILIES):
        for fam_b in list(FAMILIES)[i + 1:]:
            a = family_slopes.get(fam_a, [])
            b = family_slopes.get(fam_b, [])
            if len(a) < 2 or len(b) < 2:
                continue
            mean_a = sum(a) / len(a)
            mean_b = sum(b) / len(b)
            var_a = sample_std(a) ** 2
            var_b = sample_std(b) ** 2
            se = math.sqrt(var_a / len(a) + var_b / len(b))
            t_val = abs(mean_a - mean_b) / se if se > 1e-30 else 0.0
            print(
                f"PAIRWISE {fam_a}_vs_{fam_b} "
                f"delta={abs(mean_a - mean_b):.6f} se={se:.6f} t={t_val:.3f}"
            )


def main():
    if len(sys.argv) == 1:
        run_all()
        return
    if len(sys.argv) == 3:
        run_single(sys.argv[1], int(sys.argv[2]))
        return
    print("Usage: python3 lensing_fine_h_batch.py [<family> <seed>]")
    sys.exit(1)


if __name__ == "__main__":
    main()
