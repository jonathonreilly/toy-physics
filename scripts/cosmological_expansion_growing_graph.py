#!/usr/bin/env python3
"""Cosmological expansion via actual graph growth.

Instead of scaling distances (which doesn't clearly affect beam dynamics),
GROW the graph: each new layer has more nodes than the previous.

Method: at layer n, the transverse width is W(n) = W_0 + alpha * n * h.
New nodes are added at the edges. The beam can spread into the new space.

If the beam width grows proportionally to W(n): de Sitter-like expansion.
If the beam width saturates: the beam doesn't "feel" the new space.
"""

from __future__ import annotations

import math
import numpy as np

BETA = 0.8
K = 5.0
MAX_D_PHYS = 3.0
H = 0.5
PHYS_L = 30
BASE_W = 4


def _run_growing(alpha_w):
    """Build and propagate on a graph where W grows with layer."""
    nl = int(PHYS_L / H) + 1
    max_d = max(1, round(MAX_D_PHYS / H))

    # Build all layers with their individual widths
    layers_hw = []
    layers_nw = []
    layers_npl = []
    layers_start = [0]  # cumulative node index

    total_nodes = 0
    for layer in range(nl):
        phys_w = BASE_W + alpha_w * layer * H
        hw = max(int(BASE_W / H), int(phys_w / H))
        nw = 2 * hw + 1
        npl = nw * nw
        layers_hw.append(hw)
        layers_nw.append(nw)
        layers_npl.append(npl)
        if layer < nl - 1:
            layers_start.append(layers_start[-1] + npl)
        total_nodes += npl

    # Precompute offsets (max connectivity)
    offsets = []
    for dy in range(-max_d, max_d + 1):
        for dz in range(-max_d, max_d + 1):
            dyp, dzp = dy * H, dz * H
            L = math.sqrt(H * H + dyp * dyp + dzp * dzp)
            theta = math.atan2(math.sqrt(dyp * dyp + dzp * dzp), H)
            w = math.exp(-BETA * theta * theta)
            offsets.append((dy, dz, L, w * H * H / (L * L)))
    T = sum(wr for _, _, _, wr in offsets)

    # Propagate layer by layer
    # Each layer has different nw, so we can't use a fixed array
    prev_amps = np.zeros(layers_npl[0], dtype=np.complex128)
    hw0 = layers_hw[0]
    prev_amps[hw0 * layers_nw[0] + hw0] = 1.0  # source at center

    beam_widths = []

    for layer in range(nl):
        hw_curr = layers_hw[layer]
        nw_curr = layers_nw[layer]
        npl_curr = layers_npl[layer]

        if layer == 0:
            curr_amps = prev_amps
        else:
            curr_amps = np.zeros(npl_curr, dtype=np.complex128)

        # Measure beam width at this layer
        p = np.abs(curr_amps if layer > 0 else prev_amps) ** 2
        t = p.sum()
        if t > 0:
            hw_l = layers_hw[layer if layer > 0 else 0]
            nw_l = layers_nw[layer if layer > 0 else 0]
            zc = np.array([iz * H for _ in range(-hw_l, hw_l + 1) for iz in range(-hw_l, hw_l + 1)])
            if len(zc) == len(p):
                mean_z = np.dot(p, zc) / t
                var_z = np.dot(p, (zc - mean_z) ** 2) / t
                beam_widths.append((layer, math.sqrt(var_z), layers_hw[layer] * H))

        if layer >= nl - 1:
            break

        # Propagate to next layer
        hw_next = layers_hw[layer + 1]
        nw_next = layers_nw[layer + 1]
        npl_next = layers_npl[layer + 1]
        hw_curr = layers_hw[layer]
        nw_curr = layers_nw[layer]

        sa = curr_amps if layer > 0 else prev_amps
        next_amps = np.zeros(npl_next, dtype=np.complex128)

        for dy, dz, L, w_raw in offsets:
            # Source nodes in current layer
            for yi_s in range(nw_curr):
                iy_s = yi_s - hw_curr
                for zi_s in range(nw_curr):
                    iz_s = zi_s - hw_curr
                    si = yi_s * nw_curr + zi_s
                    ai = sa[si]
                    if abs(ai) < 1e-300:
                        continue
                    # Destination in next layer
                    iy_d = iy_s + dy - hw_curr + hw_next
                    iz_d = zi_s + dz - hw_curr + hw_next
                    if 0 <= iy_d < nw_next and 0 <= iz_d < nw_next:
                        di = iy_d * nw_next + iz_d
                        phase = K * L
                        next_amps[di] += ai * complex(math.cos(phase), math.sin(phase)) * w_raw / T

        prev_amps = sa
        if layer > 0:
            curr_amps = next_amps
        else:
            prev_amps = next_amps
        # Actually we need to carry forward properly
        prev_amps = next_amps

    return beam_widths, layers_hw


def main():
    print("=" * 70)
    print("COSMOLOGICAL EXPANSION VIA GROWING GRAPH")
    print(f"W(layer) = {BASE_W} + alpha * layer * {H}")
    print(f"h={H}, L={PHYS_L}")
    print("=" * 70)
    print()

    for alpha_w in [0.0, 0.1, 0.2, 0.5]:
        label = "flat" if alpha_w == 0 else f"expanding (alpha={alpha_w})"
        bw, hw_list = _run_growing(alpha_w)
        print(f"alpha_w={alpha_w:.1f} ({label})")
        print(f"  {'layer':>6s} {'W_phys':>8s} {'sigma':>8s} {'sigma/W':>8s}")
        for layer, sigma, w_phys in bw:
            if layer % 10 == 0 or layer == len(bw) - 1:
                ratio = sigma / w_phys if w_phys > 0 else 0
                print(f"  {layer:6d} {w_phys:8.1f} {sigma:8.3f} {ratio:8.4f}")
        # sigma at detector
        if bw:
            final = bw[-1]
            print(f"  detector: sigma={final[1]:.3f}, W={final[2]:.1f}")
        print()


if __name__ == "__main__":
    main()
