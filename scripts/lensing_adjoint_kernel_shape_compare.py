#!/usr/bin/env python3
"""Compare normalized adjoint-kernel shapes across impact parameter.

This extends the exact adjoint-kernel lane by asking whether the
absolute first-order layer kernel |K_l| keeps roughly the same broad
shape across b in {3,4,5,6}, or whether the kernel itself reshapes
substantially as b changes.

We report:
  - per-b moment summaries (peak, abs-center, abs-width, left/right split)
  - pairwise raw total-variation distance on normalized |K_l|
  - pairwise peak-aligned total-variation distance on normalized |K_l|

If peak-aligned TV is much smaller than raw TV, that supports the
"quasi-fixed broad kernel sampled against 1/r_field(b)" picture.
If peak-aligned TV stays large, the exponent must come from genuine
kernel reshaping with b.
"""

from __future__ import annotations


# Heavy compute / sweep runner — `AUDIT_TIMEOUT_SEC = 1800`
# means the audit-lane precompute and live audit runner allow up to
# 30 min of wall time before recording a timeout. The 120 s default
# ceiling is too tight under concurrency contention; see
# `docs/audit/RUNNER_CACHE_POLICY.md`.
AUDIT_TIMEOUT_SEC = 1800

import argparse
from collections import defaultdict

from lensing_adjoint_kernel_probe import (
    build_free_and_adjoint,
    kernel_stats,
    layer_kernel_for_b,
)
from kubo_continuum_limit import BETA, K_PER_H, PW_PHYS, SRC_LAYER_FRAC, grow


def normalize_abs_layer(abs_layer_contrib: dict[int, float]) -> dict[int, float]:
    total = sum(abs_layer_contrib.values())
    if total <= 0:
        return {}
    return {layer: val / total for layer, val in abs_layer_contrib.items()}


def tv_distance(p: dict[int, float], q: dict[int, float]) -> float:
    keys = set(p) | set(q)
    return 0.5 * sum(abs(p.get(k, 0.0) - q.get(k, 0.0)) for k in keys)


def shift_to_peak(p: dict[int, float], peak_layer: int) -> dict[int, float]:
    return {layer - peak_layer: val for layer, val in p.items()}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--t-phys", type=float, default=15.0)
    parser.add_argument("--h", type=float, default=0.25)
    parser.add_argument("--b-values", type=float, nargs="*", default=[3.0, 4.0, 5.0, 6.0])
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--drift", type=float, default=0.20)
    parser.add_argument("--restore", type=float, default=0.70)
    parser.add_argument("--beta", type=float, default=BETA)
    args = parser.parse_args()

    H = args.h
    NL = max(3, round(args.t_phys / H))
    PW = PW_PHYS
    k_phase = K_PER_H / H
    x_src = round(NL * SRC_LAYER_FRAC) * H

    pos, adj, _ = grow(args.seed, args.drift, args.restore, NL, PW, 3, H)
    A, lam, cz_free, T0, _ = build_free_and_adjoint(pos, adj, NL, PW, H, k_phase, args.beta)

    rows: list[dict] = []
    for b in args.b_values:
        layer_contrib, abs_layer_contrib = layer_kernel_for_b(
            pos, adj, H, k_phase, args.beta, A, lam, b, x_src
        )
        stats = kernel_stats(layer_contrib, abs_layer_contrib, H, x_src)
        peak_layer = max(abs_layer_contrib, key=abs_layer_contrib.get)
        rows.append(
            {
                "b": b,
                "peak_layer": peak_layer,
                "p_abs": normalize_abs_layer(abs_layer_contrib),
                "stats": stats,
            }
        )

    print("=" * 100)
    print("LENSING ADJOINT KERNEL SHAPE COMPARE")
    print("=" * 100)
    print(
        f"T_phys={args.t_phys:g}  H={H:g}  NL={NL}  PW={PW:g}  "
        f"k_phase={k_phase:.3f}  beta={args.beta:.3f}"
    )
    print(f"seed={args.seed}  drift={args.drift:.2f}  restore={args.restore:.2f}")
    print(f"x_src={x_src:.3f}  cz_free={cz_free:+.6f}  T0={T0:.6e}")
    print(f"b_values={args.b_values}")

    print("\nPer-b summary")
    print(
        f"{'b':>4s} {'peak_x':>8s} {'abs_ctr':>8s} {'abs_w':>8s} "
        f"{'|K| in [xsrc±5]':>16s} {'|K| left/right':>16s}"
    )
    for row in rows:
        s = row["stats"]
        peak_x = row["peak_layer"] * H
        lr = f"{s['left_frac']:.2f}/{s['right_frac']:.2f}"
        print(
            f"{row['b']:4.1f} {peak_x:8.3f} {s['abs_center']:8.3f} {s['abs_width']:8.3f} "
            f"{s['centered_frac']:16.3f} {lr:>16s}"
        )

    print("\nPairwise normalized |K_l| distances")
    print(f"{'pair':>12s} {'raw_TV':>10s} {'peak_align_TV':>16s}")
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            ri = rows[i]
            rj = rows[j]
            raw = tv_distance(ri["p_abs"], rj["p_abs"])
            ali = shift_to_peak(ri["p_abs"], ri["peak_layer"])
            alj = shift_to_peak(rj["p_abs"], rj["peak_layer"])
            aligned = tv_distance(ali, alj)
            pair = f"{ri['b']:.1f}-{rj['b']:.1f}"
            print(f"{pair:>12s} {raw:10.3f} {aligned:16.3f}")

    widths = [row["stats"]["abs_width"] for row in rows]
    centers = [row["stats"]["abs_center"] for row in rows]
    center_fracs = [row["stats"]["centered_frac"] for row in rows]
    print("\nRange summary")
    print(f"  abs-center range: {min(centers):.3f} .. {max(centers):.3f}  (span {(max(centers)-min(centers)):.3f})")
    print(f"  abs-width range : {min(widths):.3f} .. {max(widths):.3f}  (span {(max(widths)-min(widths)):.3f})")
    print(
        f"  |K| in [xsrc±5] : {min(center_fracs):.3f} .. {max(center_fracs):.3f}  "
        f"(span {(max(center_fracs)-min(center_fracs)):.3f})"
    )

    print("\nInterpretation guide")
    print("  - small raw TV: kernel barely changes with b even before alignment")
    print("  - raw TV >> peak-aligned TV: mostly one broad kernel translating downstream")
    print("  - peak-aligned TV still large: genuine reshaping with b")


if __name__ == "__main__":
    main()
