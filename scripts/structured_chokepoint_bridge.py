#!/usr/bin/env python3
"""Structured chokepoint bridge: grid placement + strict layer-1 mirror DAGs.

This is the narrow bridge probe between the structured-placement lane and the
canonical mirror chokepoint readout. The graph family is deliberately strict:

  - structured mirror-symmetric placement inspired by structured_mirror_growth
  - layer-1-only chokepoint connectivity
  - standard linear propagator and joint readout from mirror_chokepoint_joint

The intent is not to introduce a new scorer. It is to test whether a bounded
structured placement can survive the unchanged canonical Born + gravity +
decoherence harness.
"""

from __future__ import annotations

import argparse
import math
import os
import random
import sys
import time
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts import mirror_chokepoint_joint as canonical


def generate_structured_chokepoint_dag(
    n_layers: int,
    npl_half: int,
    grid_spacing: float,
    connect_radius: float,
    layer_jitter: float,
    rng_seed: int,
):
    """Generate a strict mirror-symmetric DAG with structured placement.

    Each non-source layer has 2 * npl_half nodes:
    - npl_half upper-half nodes
    - npl_half exact y-mirrors in the lower half

    Placement follows the structured-mirror idea from the growth script:
    local grid-like placement with a small random walk offset across layers.
    Connectivity remains strict layer-1 only.
    """
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
    mirror_map = {}

    n_extra = 1  # one transverse coordinate besides y: z
    grid_per_dim = npl_half
    grid_offset = [0.0, 0.0]

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []

        if layer == 0:
            idx = len(positions)
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(idx)
            mirror_map[idx] = idx
        else:
            grid_offset[0] += rng.gauss(0.0, layer_jitter)
            grid_offset[1] += rng.gauss(0.0, layer_jitter)

            z_positions = [
                i * grid_spacing + grid_offset[1]
                for i in range(grid_per_dim)
            ]

            count = 0
            for z in z_positions:
                if count >= npl_half:
                    break

                # Structured upper/lower placement around the midline.
                y_upper = abs(grid_offset[0]) + (count + 1) * grid_spacing * 0.5
                pos_upper = (x, y_upper, z)
                idx_upper = len(positions)
                positions.append(pos_upper)
                layer_nodes.append(idx_upper)

                pos_lower = (x, -y_upper, z)
                idx_lower = len(positions)
                positions.append(pos_lower)
                layer_nodes.append(idx_lower)

                mirror_map[idx_upper] = idx_lower
                mirror_map[idx_lower] = idx_upper
                count += 1

            prev_nodes = layer_indices[-1] if layer_indices else []
            for idx in layer_nodes:
                pos_i = positions[idx]
                if pos_i[1] < 0:
                    continue
                for prev_idx in prev_nodes:
                    pos_p = positions[prev_idx]
                    dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(pos_i, pos_p)))
                    if dist <= connect_radius:
                        adj[prev_idx].append(idx)

            # Enforce exact mirror edges for the lower half.
            for prev_idx in prev_nodes:
                for curr_idx in adj.get(prev_idx, []):
                    mprev = mirror_map.get(prev_idx)
                    mcurr = mirror_map.get(curr_idx)
                    if mprev is not None and mcurr is not None:
                        if mcurr not in adj.get(mprev, []):
                            adj[mprev].append(mcurr)

        layer_indices.append(layer_nodes)

    return positions, dict(adj)


def _mean_se(vals):
    vals = [v for v in vals if v is not None and not math.isnan(v)]
    if not vals:
        return float("nan"), float("nan")
    mean = sum(vals) / len(vals)
    if len(vals) < 2:
        return mean, 0.0
    var = sum((v - mean) ** 2 for v in vals) / (len(vals) - 1)
    return mean, math.sqrt(var / len(vals))


def run_narrow_probe(
    n_layers: int,
    npl_half: int,
    grid_spacing: float,
    connect_radius: float,
    layer_jitter: float,
    n_seeds: int,
):
    seeds = [s * 7 + 3 for s in range(n_seeds)]
    dtv_all, pur_all, sn_all, grav_all, born_all, k0_all = [], [], [], [], [], []

    for seed in seeds:
        pos, adj = generate_structured_chokepoint_dag(
            n_layers=n_layers,
            npl_half=npl_half,
            grid_spacing=grid_spacing,
            connect_radius=connect_radius,
            layer_jitter=layer_jitter,
            rng_seed=seed,
        )
        r = canonical.measure_joint(pos, adj, n_layers, canonical.K)
        if not r:
            continue
        dtv_all.append(r["dtv"])
        pur_all.append(r["pur_cl"])
        sn_all.append(r["s_norm"])
        grav_all.append(r["gravity"])
        if not math.isnan(r["born"]):
            born_all.append(r["born"])
        k0_all.append(r["grav_k0"])

    return {
        "dtv": _mean_se(dtv_all),
        "pur": _mean_se(pur_all),
        "sn": _mean_se(sn_all),
        "grav": _mean_se(grav_all),
        "born": _mean_se(born_all),
        "k0": _mean_se(k0_all),
        "n_ok": len(dtv_all),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-layers", nargs="+", type=int, default=[25, 40, 60])
    parser.add_argument("--npl-half", type=int, default=canonical.NPL_HALF)
    parser.add_argument("--grid-spacing", type=float, default=1.0)
    parser.add_argument("--connect-radius", type=float, default=3.5)
    parser.add_argument("--layer-jitter", type=float, default=0.25)
    parser.add_argument("--n-seeds", type=int, default=canonical.N_SEEDS)
    args = parser.parse_args()

    print("=" * 110)
    print("STRUCTURED CHOKEPOINT BRIDGE: Born + Gravity + Decoherence")
    print(
        f"  structured placement, layer-1 chokepoint, canonical readout, "
        f"NPL_HALF={args.npl_half}, seeds={args.n_seeds}"
    )
    print(
        f"  grid_spacing={args.grid_spacing}, connect_radius={args.connect_radius}, "
        f"layer_jitter={args.layer_jitter}"
    )
    print("=" * 110)
    print()

    print(
        f"  {'N':>4s}  {'d_TV':>8s}  {'pur_cl':>8s}  {'S_norm':>8s}  "
        f"{'gravity':>10s}  {'Born':>10s}  {'k=0':>10s}  {'ok':>3s}  {'time':>5s}"
    )
    print(f"  {'-' * 96}")

    any_retained = False
    for nl in args.n_layers:
        t0 = time.time()
        r = run_narrow_probe(
            n_layers=nl,
            npl_half=args.npl_half,
            grid_spacing=args.grid_spacing,
            connect_radius=args.connect_radius,
            layer_jitter=args.layer_jitter,
            n_seeds=args.n_seeds,
        )
        dt = time.time() - t0
        if r["n_ok"] > 0:
            any_retained = True
            mdtv, _ = r["dtv"]
            mpur, sepur = r["pur"]
            msn, _ = r["sn"]
            mg, seg = r["grav"]
            mborn, _ = r["born"]
            mk0, _ = r["k0"]
            born_str = f"{mborn:10.2e}" if not math.isnan(mborn) else "       nan"
            print(
                f"  {nl:4d}  {mdtv:8.4f}  {mpur:7.4f}±{sepur:.02f}  {msn:8.4f}  "
                f"{mg:+7.4f}±{seg:.3f}  {born_str}  {mk0:+10.2e}  "
                f"{r['n_ok']:3d}  {dt:4.0f}s"
            )
        else:
            print(f"  {nl:4d}  FAIL  {dt:4.0f}s")

    print()
    print("VALIDATION CRITERIA:")
    print("  Born: |I3|/P < 1e-10 = machine precision (PASS)")
    print("  k=0: must be 0 (phase-mediated gravity)")
    print("  pur_cl < 0.95 at retained N: decoherence ceiling broken")
    print("  gravity > 0 with grav_t > 2: significant attraction")
    print()
    if any_retained:
        print("DECISION: retained structured bridge pocket, narrow canonical readout only")
    else:
        print("DECISION: no retained structured bridge row on this narrow probe")


if __name__ == "__main__":
    main()
