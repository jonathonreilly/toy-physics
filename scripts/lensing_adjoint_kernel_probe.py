#!/usr/bin/env python3
"""Exact adjoint-weighted layer kernel for the lensing Kubo response.

This script computes the literal first-order layer kernel

    K_l = 2 Re sum_{edges i->j, layer(j)=l} lambda_j * A_i * U_ij

for the detector-centroid response, where:

    A_j      free propagator amplitude
    lambda_j reverse detector sensitivity
    U_ij     first-order edge perturbation = W_ij * (-i k L_ij / r_field)

Unlike the earlier finite-path notes, this is the exact observable
implemented by `true_kubo_at_H` up to the same floating-point arithmetic.

The main diagnostic is whether K_l is compact and centered around the
mass plane, or whether the response is distributed over a much broader
portion of the path.
"""

from __future__ import annotations


# Heavy compute / sweep runner — `AUDIT_TIMEOUT_SEC = 1800`
# means the audit-lane precompute and live audit runner allow up to
# 30 min of wall time before recording a timeout. The 120 s default
# ceiling is too tight under concurrency contention; see
# `docs/audit/RUNNER_CACHE_POLICY.md`.
AUDIT_TIMEOUT_SEC = 1800

import argparse
import math
from collections import defaultdict

from kubo_continuum_limit import BETA, K_PER_H, PW_PHYS, SRC_LAYER_FRAC, grow, true_kubo_at_H


def build_free_and_adjoint(pos, adj, NL, PW, H, k_phase, beta):
    """Return free amplitudes A, detector sensitivity lambda, and free stats."""
    n = len(pos)
    order = sorted(range(n), key=lambda i: pos[i][0])
    h2 = H * H

    A = [0j] * n
    A[0] = 1.0 + 0j
    for i in order:
        ai = A[i]
        if abs(ai) < 1e-30:
            continue
        for j in adj.get(i, []):
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
            A[j] += ai * phi * w * h2 / (L * L)

    hw = int(PW / H)
    npl = (2 * hw + 1) ** 2
    ds_idx = n - npl
    detector = list(range(ds_idx, n))
    weights = [abs(A[k]) ** 2 for k in detector]
    zs = [pos[k][2] for k in detector]
    T0 = sum(weights)
    if T0 <= 0:
        raise RuntimeError("free detector probability is zero")
    cz_free = sum(w * z for w, z in zip(weights, zs)) / T0

    # Linear functional L(B) = sum_k c_k B_k with kubo = 2 Re L(B)
    c = [0j] * n
    for k in detector:
        c[k] = ((pos[k][2] - cz_free) / T0) * A[k].conjugate()

    lam = c[:]
    for i in reversed(order):
        acc = lam[i]
        for j in adj.get(i, []):
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
            acc += lam[j] * W
        lam[i] = acc

    return A, lam, cz_free, T0, order


def layer_kernel_for_b(pos, adj, H, k_phase, beta, A, lam, z_src, x_src):
    """Exact signed layer contributions K_l for one impact parameter."""
    h2 = H * H
    layer_contrib = defaultdict(float)
    abs_layer_contrib = defaultdict(float)

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
            mx = 0.5 * (pos[i][0] + pos[j][0])
            mz = 0.5 * (pos[i][2] + pos[j][2])
            r_field = math.sqrt((mx - x_src) ** 2 + (mz - z_src) ** 2) + 0.1
            phase = k_phase * L
            phi = complex(math.cos(phase), math.sin(phase))
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-beta * theta * theta)
            W = phi * w * h2 / (L * L)
            U = complex(0.0, -k_phase * L / r_field) * W
            contrib = 2.0 * (lam[j] * ai * U).real
            layer = round(pos[j][0] / H)
            layer_contrib[layer] += contrib
            abs_layer_contrib[layer] += abs(contrib)

    return dict(layer_contrib), dict(abs_layer_contrib)


def kernel_stats(layer_contrib, abs_layer_contrib, H, x_src):
    layers = sorted(layer_contrib)
    signed_total = sum(layer_contrib.values())
    abs_total = sum(abs_layer_contrib.values())
    xs = [layer * H for layer in layers]
    signed_center = (
        sum(x * layer_contrib[layer] for x, layer in zip(xs, layers)) / signed_total
        if abs(signed_total) > 1e-15
        else float("nan")
    )
    abs_center = (
        sum(x * abs_layer_contrib[layer] for x, layer in zip(xs, layers)) / abs_total
        if abs_total > 1e-15
        else float("nan")
    )
    abs_width = (
        math.sqrt(
            sum(abs_layer_contrib[layer] * (x - abs_center) ** 2 for x, layer in zip(xs, layers))
            / abs_total
        )
        if abs_total > 1e-15
        else float("nan")
    )

    def frac_in_window(lo, hi):
        if abs_total <= 1e-15:
            return float("nan")
        s = 0.0
        for layer, val in abs_layer_contrib.items():
            x = layer * H
            if lo <= x <= hi:
                s += val
        return s / abs_total

    peak_layer = max(layers, key=lambda l: abs_layer_contrib.get(l, 0.0))
    peak_x = peak_layer * H
    centered_frac = frac_in_window(x_src - 5.0, x_src + 5.0)
    left_frac = frac_in_window(0.0, x_src)
    right_frac = frac_in_window(x_src, max(xs) if xs else x_src)
    return {
        "signed_total": signed_total,
        "abs_total": abs_total,
        "signed_center": signed_center,
        "abs_center": abs_center,
        "abs_width": abs_width,
        "peak_x": peak_x,
        "centered_frac": centered_frac,
        "left_frac": left_frac,
        "right_frac": right_frac,
    }


def main():
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
    beta = args.beta

    pos, adj, _ = grow(args.seed, args.drift, args.restore, NL, PW, 3, H)
    A, lam, cz_free, T0, _ = build_free_and_adjoint(pos, adj, NL, PW, H, k_phase, beta)

    print("=" * 100)
    print("LENSING ADJOINT KERNEL PROBE")
    print("=" * 100)
    print(f"T_phys={args.t_phys:g}  H={H:g}  NL={NL}  PW={PW:g}  k_phase={k_phase:.3f}  beta={beta:.3f}")
    print(f"seed={args.seed}  drift={args.drift:.2f}  restore={args.restore:.2f}")
    print(f"x_src={x_src:.3f}  detector_x={(NL-1)*H:.3f}  cz_free={cz_free:+.6f}  T0={T0:.6e}")
    print(f"b_values={args.b_values}")
    print()
    print("Exact kernel identity:")
    print("  kubo = Σ_l K_l")
    print("  K_l = 2 Re Σ_{edges into layer l} lambda_j * A_i * U_ij")
    print()

    print(
        f"{'b':>4s} {'kubo(sum K_l)':>14s} {'kubo(ref)':>12s} {'|Δ|':>10s}"
        f" {'peak_x':>8s} {'abs_ctr':>8s} {'abs_w':>8s}"
        f" {'|K| in [xsrc±5]':>16s} {'|K| left/right':>16s}"
    )
    for b in args.b_values:
        layer_contrib, abs_layer_contrib = layer_kernel_for_b(pos, adj, H, k_phase, beta, A, lam, b, x_src)
        stats = kernel_stats(layer_contrib, abs_layer_contrib, H, x_src)
        kubo_exact = stats["signed_total"]
        if abs(beta - BETA) < 1e-12:
            kubo_ref, _, _ = true_kubo_at_H(pos, adj, NL, PW, H, k_phase, x_src, b)
            delta = abs(kubo_exact - kubo_ref)
            kubo_ref_txt = f"{kubo_ref:+12.6f}"
            delta_txt = f"{delta:10.3e}"
        else:
            kubo_ref_txt = f"{'n/a':>12s}"
            delta_txt = f"{'n/a':>10s}"
        lr = (
            f"{stats['left_frac']:.2f}/{stats['right_frac']:.2f}"
            if stats["left_frac"] == stats["left_frac"] and stats["right_frac"] == stats["right_frac"]
            else "nan"
        )
        print(
            f"{b:4.1f} {kubo_exact:+14.6f} {kubo_ref_txt} {delta_txt}"
            f" {stats['peak_x']:8.3f} {stats['abs_center']:8.3f} {stats['abs_width']:8.3f}"
            f" {stats['centered_frac']:16.3f} {lr:>16s}"
        )

        # Show the strongest signed and absolute layers to make the shape visible in logs.
        top_signed = sorted(layer_contrib.items(), key=lambda kv: abs(kv[1]), reverse=True)[:6]
        print("     top signed layers:", "  ".join(f"x={layer*H:.2f}:{val:+.3e}" for layer, val in top_signed))

    print()
    print("Interpretation:")
    print("  - If |K| is compact around x_src with a narrow width, a centered finite-path surrogate is plausible.")
    print("  - If |K| is broad or strongly skewed, the slope is coming from the full adjoint-weighted wave response.")


if __name__ == "__main__":
    main()
