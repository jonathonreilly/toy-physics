#!/usr/bin/env python3
"""Cosmological expansion via growing graph — fixed propagation.

Each layer has width W(n) = W_0 + alpha * n * h.
New transverse nodes appear at edges. The beam propagates from
one variable-width layer to the next.

The key: node indexing uses (iy, iz) coordinates, NOT absolute indices.
Each layer maps iy,iz → amplitude. The propagation kernel connects
(iy,iz) in layer n to (iy+dy, iz+dz) in layer n+1, but only if
both source and destination exist in their respective layers.
"""

from __future__ import annotations

import math
import numpy as np

BETA = 0.8
K = 5.0
MAX_D_PHYS = 3.0
H = 0.5
PHYS_L = 40
BASE_W = 4


def _run(alpha_w):
    nl = int(PHYS_L / H) + 1
    max_d = max(1, round(MAX_D_PHYS / H))

    # Precompute offsets
    offsets = []
    for dy in range(-max_d, max_d + 1):
        for dz in range(-max_d, max_d + 1):
            dyp, dzp = dy * H, dz * H
            L = math.sqrt(H * H + dyp * dyp + dzp * dzp)
            theta = math.atan2(math.sqrt(dyp * dyp + dzp * dzp), H)
            w = math.exp(-BETA * theta * theta)
            offsets.append((dy, dz, L, w * H * H / (L * L)))
    T_base = sum(wr for _, _, _, wr in offsets)

    # Per-layer: hw(layer), stored as dict[iy,iz] → amplitude
    def hw_at(layer):
        phys_w = BASE_W + alpha_w * layer * H
        return int(phys_w / H)

    # Propagate using dict-based amplitudes
    hw0 = hw_at(0)
    current = {}
    current[(0, 0)] = 1.0 + 0j  # source at center

    beam_data = []

    for layer in range(nl):
        hw_curr = hw_at(layer)

        # Measure beam width
        total_p = sum(abs(a) ** 2 for a in current.values())
        if total_p > 0:
            mean_z = sum(abs(a) ** 2 * iz * H for (iy, iz), a in current.items()) / total_p
            var_z = sum(abs(a) ** 2 * (iz * H - mean_z) ** 2 for (iy, iz), a in current.items()) / total_p
            sigma = math.sqrt(var_z)
            beam_data.append((layer, sigma, hw_curr * H, total_p))

        if layer >= nl - 1:
            break

        # Propagate to next layer
        hw_next = hw_at(layer + 1)
        next_amps = {}

        for (iy_s, iz_s), ai in current.items():
            if abs(ai) < 1e-30:
                continue
            for dy, dz, L, w_raw in offsets:
                iy_d = iy_s + dy
                iz_d = iz_s + dz
                # Check destination is within next layer
                if abs(iy_d) > hw_next or abs(iz_d) > hw_next:
                    continue
                # Compute T for this source node (how many valid destinations)
                # For simplicity, use T_base (interior node approximation)
                phase = K * L
                kernel = ai * complex(math.cos(phase), math.sin(phase)) * w_raw / T_base
                key = (iy_d, iz_d)
                if key in next_amps:
                    next_amps[key] += kernel
                else:
                    next_amps[key] = kernel

        current = next_amps

    return beam_data


def main():
    print("=" * 70)
    print("COSMOLOGICAL EXPANSION VIA GROWING GRAPH (FIXED)")
    print(f"W(n) = {BASE_W} + alpha * n * {H}")
    print(f"h={H}, L={PHYS_L}")
    print("=" * 70)
    print()

    for alpha_w in [0.0, 0.1, 0.3, 0.5]:
        label = "flat" if alpha_w == 0 else f"expanding"
        bd = _run(alpha_w)
        print(f"alpha_w={alpha_w:.1f} ({label})")
        print(f"  {'layer':>6s} {'x':>6s} {'W':>6s} {'sigma':>8s} {'P_total':>10s}")
        for layer, sigma, w, p in bd:
            if layer % 10 == 0 or layer == len(bd) - 1:
                print(f"  {layer:6d} {layer * H:6.1f} {w:6.1f} {sigma:8.3f} {p:10.2e}")

        # sigma at start vs end
        if len(bd) >= 2:
            s0 = bd[0][1]
            sf = bd[-1][1]
            w0 = bd[0][2]
            wf = bd[-1][2]
            print(f"  sigma: {s0:.3f} → {sf:.3f}, W: {w0:.1f} → {wf:.1f}")
            if wf > w0:
                print(f"  sigma/W ratio: {s0 / w0:.4f} → {sf / wf:.4f}")
        print()


if __name__ == "__main__":
    main()
