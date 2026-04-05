#!/usr/bin/env python3
"""Poisson-like self-gravity: |psi|^2 generates 1/r field.

THE PHYSICS:
  The probability density |psi(x)|^2 acts as a mass distribution.
  It generates a gravitational field via:

    f_self(y) = G * sum_x |psi(x)|^2 / |y - x|

  This is the Newtonian potential from a distributed source.
  Combined with external field: f_total = f_ext + f_self

  Self-consistent: iterate propagate → field → propagate until
  the field converges.

  If G > 0: |psi|^2 attracts more |psi|^2 → gravitational collapse
  This is the Schrodinger-Newton equation on a lattice.

  The question: does self-gravity produce horizon-like behavior?
"""

from __future__ import annotations

import math
import time
import numpy as np

BETA = 0.8
K = 5.0
MAX_D_PHYS = 3.0
H = 0.5
PHYS_W = 6
PHYS_L = 30
MASS_Z = 3.0
EXT_STRENGTH = 0.004  # Weak external field


def _build():
    nl = int(PHYS_L / H) + 1
    hw = int(PHYS_W / H)
    max_d = max(1, round(MAX_D_PHYS / H))
    nw = 2 * hw + 1
    npl = nw * nw
    offsets = []
    for dy in range(-max_d, max_d + 1):
        for dz in range(-max_d, max_d + 1):
            dyp, dzp = dy * H, dz * H
            L = math.sqrt(H * H + dyp * dyp + dzp * dzp)
            theta = math.atan2(math.sqrt(dyp * dyp + dzp * dzp), H)
            w = math.exp(-BETA * theta * theta)
            offsets.append((dy, dz, L, w * H * H / (L * L)))
    T = sum(wr for _, _, _, wr in offsets)

    # Precompute positions for field generation
    pos = []
    for layer in range(nl):
        x = layer * H
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                pos.append((x, iy * H, iz * H))
    pos = np.array(pos)

    return nl, hw, nw, npl, offsets, T, pos


def _ext_field(nl, nw, hw, npl, pos, s, z_src):
    gl = nl // 3
    iz_s = round(z_src / H)
    sx = np.array([gl * H, 0.0, iz_s * H])
    f = np.zeros((nl, npl))
    for layer in range(nl):
        ls = layer * npl
        dx = pos[ls:ls + npl] - sx
        r = np.sqrt(np.sum(dx ** 2, axis=1)) + 0.1
        f[layer] = s / r
    return f


def _self_field_from_amplitude(amps, nl, npl, pos, G):
    """Generate 1/r field from |psi|^2 distribution at each layer.

    Only include contributions from the SOURCE layer (where the beam
    passes) to avoid O(N^2) all-pairs computation.
    """
    f_self = np.zeros((nl, npl))

    # Compute total |psi|^2 per layer to find where the beam is
    layer_power = np.array([np.sum(np.abs(amps[l]) ** 2) for l in range(nl)])
    total_power = layer_power.sum()
    if total_power < 1e-300:
        return f_self

    # For each layer, the self-field comes from the probability at THAT layer
    # (local approximation — the beam at layer L generates field at layer L)
    for layer in range(nl):
        p = np.abs(amps[layer]) ** 2
        if p.sum() < 1e-300:
            continue

        # Normalize probability
        p_norm = p / p.sum()

        # Compute field at each node from the probability distribution
        # Only use top N nodes to keep computation tractable
        top_k = min(50, npl)
        top_idx = np.argpartition(p_norm, -top_k)[-top_k:]
        top_p = p_norm[top_idx]

        ls = layer * npl
        for idx, prob in zip(top_idx, top_p):
            if prob < 1e-8:
                continue
            src_pos = pos[ls + idx]
            dx = pos[ls:ls + npl] - src_pos
            r = np.sqrt(np.sum(dx ** 2, axis=1)) + 0.1
            f_self[layer] += G * prob / r

    return f_self


def _propagate(nl, nw, npl, hw, offsets, T, field, k):
    amps = np.zeros((nl, npl), dtype=np.complex128)
    amps[0, hw * nw + hw] = 1.0
    for layer in range(nl - 1):
        sa = amps[layer]
        if np.max(np.abs(sa)) < 1e-300:
            continue
        sf = field[layer]
        df = field[min(layer + 1, nl - 1)]
        for dy, dz, L, w_raw in offsets:
            ym, yM = max(0, -dy), min(nw, nw - dy)
            zm, zM = max(0, -dz), min(nw, nw - dz)
            if ym >= yM or zm >= zM:
                continue
            yi, zi = np.meshgrid(np.arange(ym, yM), np.arange(zm, zM), indexing='ij')
            si = yi.ravel() * nw + zi.ravel()
            di = (yi.ravel() + dy) * nw + (zi.ravel() + dz)
            ai = sa[si]
            mask = np.abs(ai) > 1e-300
            if not np.any(mask):
                continue
            si_m, di_m, ai_m = si[mask], di[mask], ai[mask]
            lf = 0.5 * (sf[si_m] + df[di_m])
            act = L * (1.0 - lf)
            phase = k * act
            np.add.at(amps[layer + 1], di_m,
                      ai_m * (np.cos(phase) + 1j * np.sin(phase)) * w_raw / T)
    return amps


def _cz(a, nw, hw):
    p = np.abs(a) ** 2
    t = p.sum()
    if t <= 0:
        return 0.0
    zc = np.array([iz * H for _ in range(-hw, hw + 1) for iz in range(-hw, hw + 1)])
    return float(np.dot(p, zc) / t)


def _dp(a):
    return float(np.sum(np.abs(a) ** 2))


def main():
    t0 = time.time()
    nl, hw, nw, npl, offsets, T, pos = _build()

    zero_field = np.zeros((nl, npl))
    ef = _ext_field(nl, nw, hw, npl, pos, EXT_STRENGTH, MASS_Z)

    free = _propagate(nl, nw, npl, hw, offsets, T, zero_field, K)
    z_free = _cz(free[-1], nw, hw)
    p_free = _dp(free[-1])

    grav = _propagate(nl, nw, npl, hw, offsets, T, ef, K)
    z_grav = _cz(grav[-1], nw, hw)

    print("=" * 80)
    print("POISSON SELF-GRAVITY: |psi|^2 generates 1/r field")
    print(f"  h={H}, W={PHYS_W}, L={PHYS_L}, s_ext={EXT_STRENGTH}, z_src={MASS_Z}")
    print(f"  Baseline gravity: {z_grav - z_free:+.6e} TOWARD")
    print("=" * 80)
    print()

    G_values = [0.0, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0]
    n_iters = 15

    print(f"{'G':>6s} {'iters':>6s} {'delta':>12s} {'dir':>6s} {'escape':>8s} "
          f"{'f_self_max':>10s} {'converged':>10s}")
    print("-" * 70)

    for G in G_values:
        total_field = ef.copy()
        prev_delta = None
        converged = False

        for iteration in range(n_iters):
            amps = _propagate(nl, nw, npl, hw, offsets, T, total_field, K)
            delta = _cz(amps[-1], nw, hw) - z_free
            escape = _dp(amps[-1]) / p_free if p_free > 0 else 0

            if prev_delta is not None and abs(delta - prev_delta) < 1e-8:
                converged = True
                break
            prev_delta = delta

            if G > 0:
                f_self = _self_field_from_amplitude(amps, nl, npl, pos, G)
                total_field_new = ef + f_self
                total_field = total_field_new

        direction = "TOWARD" if delta > 0 else "AWAY"
        f_self_max = (total_field - ef).max() if G > 0 else 0.0
        conv_s = f"iter {iteration + 1}" if converged else f"NOT ({iteration + 1})"
        print(f"{G:6.3f} {iteration + 1:6d} {delta:+12.6e} {direction:>6s} "
              f"{escape:8.4f} {f_self_max:10.6f} {conv_s:>10s}")

    dt = time.time() - t0
    print(f"\n({dt:.0f}s total)")

    print()
    print("SAFE READ")
    print("  G > 0: self-gravity should ENHANCE deflection (positive feedback)")
    print("  if escape drops < 1 at some G: self-gravitational collapse")
    print("  if the system converges: stable self-consistent solution exists")
    print("  if NOT: chaotic/unstable → critical G threshold")
    print("  comparison to Schrodinger-Newton: same physics, discrete setting")


if __name__ == "__main__":
    main()
