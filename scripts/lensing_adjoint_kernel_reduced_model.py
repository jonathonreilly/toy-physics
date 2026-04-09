#!/usr/bin/env python3
"""Reduced adjoint-kernel model for the retained lensing fingerprint.

This script starts from the exact first-order factorization

    kubo_true(b) = sum_e c_e / r_e(b)

where the signed edge coefficients c_e are fixed by the free propagator and
detector adjoint, and all b-dependence enters only through the field distance
factor r_e(b).

It then compresses those edge coefficients to a signed layer model:

    kubo_red(b) = sum_l C_l / r_l(b)

using fixed effective geometry per layer. This is a reduced surrogate of the
exact edge formula, not a derivation.

The expensive full `true_kubo_at_H` harness is optional here. The retained
reference series is the exact edge replay, with an optional bounded spot-check
against the full harness at one or more `b` values.
"""

from __future__ import annotations

import argparse
import math
from collections import defaultdict

from kubo_continuum_limit import BETA, K_PER_H, PW_PHYS, SRC_LAYER_FRAC, grow, true_kubo_at_H
from lensing_adjoint_kernel_probe import build_free_and_adjoint
from lensing_deflection_sweep import log_slope


def signed_edge_coefficients(pos, adj, H, k_phase, beta, A, lam):
    """Return signed b-independent edge coefficients and midpoint geometry."""
    h2 = H * H
    edges = []
    for i, outs in adj.items():
        ai = A[i]
        if abs(ai) < 1e-30:
            continue
        for j in outs:
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            dz = pos[j][2] - pos[i][2]
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            phase = k_phase * L
            phi = complex(math.cos(phase), math.sin(phase))
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-beta * theta * theta)
            W = phi * w * h2 / (L * L)
            coeff = 2.0 * (lam[j] * ai * W * complex(0.0, -k_phase * L)).real
            mx = 0.5 * (pos[i][0] + pos[j][0])
            mz = 0.5 * (pos[i][2] + pos[j][2])
            layer = round(pos[j][0] / H)
            edges.append((layer, coeff, mx, mz))
    return edges


def exact_edge_sum(edges, x_src, b):
    total = 0.0
    for _layer, coeff, mx, mz in edges:
        r = math.sqrt((mx - x_src) ** 2 + (mz - b) ** 2) + 0.1
        total += coeff / r
    return total


def compress_layers(edges):
    """Layer-compress signed edge coefficients with two geometry choices."""
    by_layer = defaultdict(list)
    for layer, coeff, mx, mz in edges:
        by_layer[layer].append((coeff, mx, mz))

    rows = []
    for layer in sorted(by_layer):
        items = by_layer[layer]
        c_sum = sum(c for c, _, _ in items)
        if abs(c_sum) < 1e-15:
            continue
        abs_sum = sum(abs(c) for c, _, _ in items)
        x_signed = sum(c * mx for c, mx, _ in items) / c_sum
        z_signed = sum(c * mz for c, _, mz in items) / c_sum
        x_abs = sum(abs(c) * mx for c, mx, _ in items) / abs_sum
        z_abs = sum(abs(c) * mz for c, _, mz in items) / abs_sum
        rows.append(
            {
                "layer": layer,
                "C": c_sum,
                "x_signed": x_signed,
                "z_signed": z_signed,
                "x_abs": x_abs,
                "z_abs": z_abs,
            }
        )
    return rows


def reduced_sum(rows, x_src, b, geom_key):
    total = 0.0
    for row in rows:
        x = row[f"x_{geom_key}"]
        z = row[f"z_{geom_key}"]
        r = math.sqrt((x - x_src) ** 2 + (z - b) ** 2) + 0.1
        total += row["C"] / r
    return total


def summarize_model(label, bs, ys, ref):
    slope, _, r2 = log_slope(bs, ys)
    rel_errors = []
    for y, yref in zip(ys, ref):
        if abs(yref) > 1e-15:
            rel_errors.append(abs(y - yref) / abs(yref))
    mean_rel = sum(rel_errors) / len(rel_errors) if rel_errors else float("nan")
    max_rel = max(rel_errors) if rel_errors else float("nan")
    return {
        "label": label,
        "slope": slope,
        "r2": r2,
        "mean_rel": mean_rel,
        "max_rel": max_rel,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--t-phys", type=float, default=15.0)
    parser.add_argument("--h", type=float, default=0.25)
    parser.add_argument("--b-values", type=float, nargs="*", default=[3.0, 4.0, 5.0, 6.0])
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--drift", type=float, default=0.20)
    parser.add_argument("--restore", type=float, default=0.70)
    parser.add_argument("--beta", type=float, default=BETA)
    parser.add_argument(
        "--truth-mode",
        choices=["none", "spotcheck", "full"],
        default="spotcheck",
        help="how much of the expensive true_kubo harness to replay",
    )
    parser.add_argument(
        "--spotcheck-b",
        type=float,
        nargs="*",
        default=[3.0],
        help="b values to cross-check with true_kubo_at_H when --truth-mode=spotcheck",
    )
    args = parser.parse_args()

    H = args.h
    NL = max(3, round(args.t_phys / H))
    PW = PW_PHYS
    k_phase = K_PER_H / H
    x_src = round(NL * SRC_LAYER_FRAC) * H
    beta = args.beta

    pos, adj, _ = grow(args.seed, args.drift, args.restore, NL, PW, 3, H)
    A, lam, cz_free, T0, _ = build_free_and_adjoint(pos, adj, NL, PW, H, k_phase, beta)
    edges = signed_edge_coefficients(pos, adj, H, k_phase, beta, A, lam)
    layers = compress_layers(edges)

    exact_vals = []
    red_signed = []
    red_abs = []
    for b in args.b_values:
        exact_vals.append(exact_edge_sum(edges, x_src, b))
        red_signed.append(reduced_sum(layers, x_src, b, "signed"))
        red_abs.append(reduced_sum(layers, x_src, b, "abs"))

    truth_targets = []
    if args.truth_mode == "full":
        truth_targets = list(args.b_values)
    elif args.truth_mode == "spotcheck":
        truth_targets = [b for b in args.spotcheck_b if b in args.b_values]

    truth_checks = {}
    for b in truth_targets:
        true_kubo, _, _ = true_kubo_at_H(pos, adj, NL, PW, H, k_phase, x_src, b, beta=beta)
        truth_checks[b] = true_kubo

    print("=" * 100)
    print("LENSING ADJOINT KERNEL REDUCED MODEL")
    print("=" * 100)
    print(
        f"T_phys={args.t_phys:g}  H={H:g}  NL={NL}  PW={PW:g}  "
        f"k_phase={k_phase:.3f}  beta={beta:.3f}"
    )
    print(f"seed={args.seed}  drift={args.drift:.2f}  restore={args.restore:.2f}")
    print(f"x_src={x_src:.3f}  cz_free={cz_free:+.6f}  T0={T0:.6e}")
    print(f"b_values={args.b_values}")
    print(f"n_edges={len(edges)}  n_layer_terms={len(layers)}")
    print()
    print("Exact factorization:")
    print("  kubo_true(b) = sum_e c_e / r_e(b)")
    print("  c_e is fixed by the free propagator and detector adjoint")
    print("  all b-dependence enters through r_e(b)")
    print()

    print(
        f"{'b':>4s} {'exact_edge':>12s} {'truth chk':>12s} {'|Δ|':>10s}"
        f" {'layer_signed':>14s} {'rel err':>10s} {'layer_abs':>12s} {'rel err':>10s}"
    )
    for b, exact_k, rs, ra in zip(args.b_values, exact_vals, red_signed, red_abs):
        truth = truth_checks.get(b, float("nan"))
        d_exact = abs(truth - exact_k) if b in truth_checks else float("nan")
        err_signed = abs(rs - exact_k) / abs(exact_k) if abs(exact_k) > 1e-15 else float("nan")
        err_abs = abs(ra - exact_k) / abs(exact_k) if abs(exact_k) > 1e-15 else float("nan")
        print(
            f"{b:4.1f} {exact_k:+12.6f} {truth:+12.6f} {d_exact:10.3e}"
            f" {rs:+14.6f} {err_signed:10.2%} {ra:+12.6f} {err_abs:10.2%}"
        )

    print()
    if truth_checks:
        print("Harness spot-checks")
        for b in truth_targets:
            exact_k = exact_vals[list(args.b_values).index(b)]
            truth = truth_checks[b]
            diff = abs(truth - exact_k)
            rel = diff / abs(truth) if abs(truth) > 1e-15 else float("nan")
            print(
                f"  b={b:g}: true_kubo={truth:+.6f}  exact_edge={exact_k:+.6f}"
                f"  |Δ|={diff:.3e}  rel={rel:.2%}"
            )
        print()

    print("Model summary")
    for summary in [
        summarize_model("exact_edge", args.b_values, exact_vals, exact_vals),
        summarize_model("layer_signed", args.b_values, red_signed, exact_vals),
        summarize_model("layer_abs", args.b_values, red_abs, exact_vals),
    ]:
        print(
            f"  {summary['label']:<12s} slope={summary['slope']:+.4f}  R²={summary['r2']:.4f}"
            f"  mean rel err={summary['mean_rel']:.2%}  max rel err={summary['max_rel']:.2%}"
        )

    print()
    print("Interpretation guide")
    print("  - exact_edge is the exact edge-level replay of the first-order observable")
    print("  - optional truth checks confirm the replay against true_kubo_at_H")
    print("  - layer_signed is the main reduced surrogate")
    print("  - layer_abs is a control showing what happens if signed cancellation is discarded")


if __name__ == "__main__":
    main()
