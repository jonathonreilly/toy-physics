#!/usr/bin/env python3
"""Small lensing sign/phase diagram for the signed-gravity lane.

This is a deliberately light companion to lensing_k_sweep.py. It separates two
effects that should not be conflated:

  1. chi-product sign: source_sign * response_sign in a locked candidate sector
  2. wave phase: k*h interference windows that can flip centroid deflection

The output is a first diagnostic map, not a geometric-optics theorem and not a
claim of antigravity.
"""

from __future__ import annotations

import math


BETA = 0.8
H = 0.5
PHYS_L = 14.0
PHYS_W = 5.0
MAX_D_PHYS = 2.5
SOURCE_LAYER_FRAC = 1.0 / 3.0
SOURCE_B = 2.0
SOURCE_STRENGTH = 0.080
KH_VALUES = (0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0)


class Layered2D:
    def __init__(self, h: float = H) -> None:
        self.h = h
        self.nl = int(PHYS_L / h) + 1
        self.hw = int(PHYS_W / h)
        self.nw = 2 * self.hw + 1
        self.n = self.nl * self.nw
        self.max_d = max(1, round(MAX_D_PHYS / h))
        self.pos = []
        self.nmap = {}
        idx = 0
        for layer in range(self.nl):
            x = layer * h
            for iy in range(-self.hw, self.hw + 1):
                self.pos.append((x, iy * h))
                self.nmap[(layer, iy)] = idx
                idx += 1
        self.offsets = []
        for dy in range(-self.max_d, self.max_d + 1):
            dyp = dy * h
            length = math.sqrt(h * h + dyp * dyp)
            theta = math.atan2(abs(dyp), h)
            weight = math.exp(-BETA * theta * theta) * h / length
            self.offsets.append((dy, length, weight))

    def layer_start(self, layer: int) -> int:
        return layer * self.nw


def field_layers(lat: Layered2D, chi_product: int) -> list[list[float]]:
    source_layer = int(lat.nl * SOURCE_LAYER_FRAC)
    sx = source_layer * lat.h
    sy = SOURCE_B
    out = []
    for layer in range(lat.nl):
        row = []
        for iy in range(-lat.hw, lat.hw + 1):
            x = layer * lat.h
            y = iy * lat.h
            r = math.sqrt((x - sx) ** 2 + (y - sy) ** 2) + 0.15
            raw_well = -SOURCE_STRENGTH / r
            row.append(chi_product * raw_well)
        out.append(row)
    return out


def propagate(lat: Layered2D, k_phase: float, chi_product: int) -> list[complex]:
    fields = field_layers(lat, chi_product)
    amps = [0j] * lat.n
    amps[lat.nmap[(0, 0)]] = 1.0 + 0j

    for layer in range(lat.nl - 1):
        ls = lat.layer_start(layer)
        ld = lat.layer_start(layer + 1)
        src = amps[ls : ls + lat.nw]
        if max(abs(v) for v in src) < 1e-30:
            continue
        for iy in range(lat.nw):
            ai = src[iy]
            if abs(ai) < 1e-30:
                continue
            for dy, length, weight in lat.offsets:
                jy = iy + dy
                if jy < 0 or jy >= lat.nw:
                    continue
                local_field = 0.5 * (fields[layer][iy] + fields[layer + 1][jy])
                action = length * (1.0 + local_field)
                phase = k_phase * action
                amps[ld + jy] += ai * complex(math.cos(phase), math.sin(phase)) * weight
    return amps


def detector_centroid(lat: Layered2D, amps: list[complex]) -> float:
    start = lat.layer_start(lat.nl - 1)
    total = 0.0
    weighted = 0.0
    for iy in range(lat.nw):
        idx = start + iy
        prob = abs(amps[idx]) ** 2
        total += prob
        weighted += prob * lat.pos[idx][1]
    return weighted / total if total > 1e-30 else 0.0


def classify(delta: float) -> str:
    if abs(delta) < 1e-9:
        return "ZERO"
    return "TOWARD" if delta > 0.0 else "AWAY"


def main() -> None:
    lat = Layered2D()
    free = propagate(lat, KH_VALUES[0] / H, 0)
    # The free centroid is recomputed per k below, but this guards construction.
    _ = detector_centroid(lat, free)

    print("=" * 88)
    print("LENSING SIGN/PHASE DIAGRAM")
    print("  bounded diagnostic: chi-product sign vs k*h wave phase")
    print("=" * 88)
    print(f"h={H}, L={PHYS_L}, W={PHYS_W}, source_b={SOURCE_B}, strength={SOURCE_STRENGTH}")
    print("positive delta means detector centroid shifts toward the source at +b")
    print()
    print(f"  {'k*h':>5s}  {'delta chi+':>12s} {'read+':>8s}  {'delta chi-':>12s} {'read-':>8s}  phase_read")
    print("  " + "-" * 72)

    product_plus_toward = 0
    product_minus_away = 0
    rows = 0
    for kh in KH_VALUES:
        k_phase = kh / H
        free = propagate(lat, k_phase, 0)
        free_centroid = detector_centroid(lat, free)
        plus = detector_centroid(lat, propagate(lat, k_phase, +1)) - free_centroid
        minus = detector_centroid(lat, propagate(lat, k_phase, -1)) - free_centroid
        read_plus = classify(plus)
        read_minus = classify(minus)
        product_plus_toward += int(read_plus == "TOWARD")
        product_minus_away += int(read_minus == "AWAY")
        rows += 1
        if read_plus == "TOWARD" and read_minus == "AWAY":
            phase_read = "sign-clean"
        elif read_plus == read_minus:
            phase_read = "wave-dominated"
        else:
            phase_read = "phase-flipped"
        print(f"  {kh:5.1f}  {plus:+12.4e} {read_plus:>8s}  {minus:+12.4e} {read_minus:>8s}  {phase_read}")

    print()
    print("SUMMARY")
    print(f"  chi_product=+1 TOWARD rows: {product_plus_toward}/{rows}")
    print(f"  chi_product=-1 AWAY rows:   {product_minus_away}/{rows}")
    print("  Any k-window sign flip here is a wave-interference diagnostic, not a")
    print("  native chi_g derivation and not a physical propulsion claim.")


if __name__ == "__main__":
    main()
