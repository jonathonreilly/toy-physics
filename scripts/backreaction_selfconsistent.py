#!/usr/bin/env python3
"""Self-consistent back-reaction: propagator and geometry co-evolve.

THE IDEA:
  In GR, matter tells spacetime how to curve, spacetime tells matter how
  to move. Here:
    1. Propagate on FIXED graph → amplitude distribution |psi|^2
    2. Update field from amplitude: f(x) += epsilon * |psi(x)|^2
       (amplitude generates additional gravitational field)
    3. Re-propagate on same graph with updated field
    4. Iterate until field converges

  Born rule holds at EACH step (fixed graph, linear propagator).
  The field evolves between steps (non-linear dynamics on the field,
  not on the amplitude).

  If epsilon > 0: high-amplitude regions attract more amplitude →
  positive feedback → amplitude concentration → effective horizon.

  The key question: does this self-consistent loop produce:
    (a) Enhanced gravity (stronger deflection than imposed field alone)?
    (b) Absorption (escape < 1)?
    (c) Both?

  If (c): the complex action is an effective description of the
  self-consistent back-reaction.
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
STRENGTH = 0.1


def _build(h):
    nl = int(PHYS_L / h) + 1
    hw = int(PHYS_W / h)
    max_d = max(1, round(MAX_D_PHYS / h))
    nw = 2 * hw + 1
    npl = nw * nw
    offsets = []
    for dy in range(-max_d, max_d + 1):
        for dz in range(-max_d, max_d + 1):
            dyp, dzp = dy * h, dz * h
            L = math.sqrt(h * h + dyp * dyp + dzp * dzp)
            theta = math.atan2(math.sqrt(dyp * dyp + dzp * dzp), h)
            w = math.exp(-BETA * theta * theta)
            offsets.append((dy, dz, L, w * h * h / (L * L)))
    T = sum(wr for _, _, _, wr in offsets)
    return nl, hw, nw, npl, offsets, T


def _ext_field(nl, nw, hw, h, s, z_src):
    gl = nl // 3
    iz_s = round(z_src / h)
    sx, sz = gl * h, iz_s * h
    f = np.zeros((nl, nw * nw))
    for layer in range(nl):
        x = layer * h
        idx = 0
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                r = math.sqrt((x - sx) ** 2 + (iy * h) ** 2 + (iz * h - sz) ** 2) + 0.1
                f[layer, idx] = s / r
                idx += 1
    return f


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


def _cz(a, nw, hw, h):
    p = np.abs(a) ** 2
    t = p.sum()
    if t <= 0:
        return 0.0
    zc = np.array([iz * h for _ in range(-hw, hw + 1) for iz in range(-hw, hw + 1)])
    return float(np.dot(p, zc) / t)


def _dp(a):
    return float(np.sum(np.abs(a) ** 2))


def _amplitude_field(amps, nl, npl, epsilon):
    """Generate additional field from amplitude distribution.

    f_back(x) = epsilon * |psi(x)|^2 / max(|psi|^2)

    This represents: where the quantum amplitude is concentrated,
    the effective gravitational field is stronger.
    """
    f_back = np.zeros((nl, npl))
    for layer in range(nl):
        p = np.abs(amps[layer]) ** 2
        mx = p.max()
        if mx > 0:
            f_back[layer] = epsilon * p / mx
    return f_back


def main():
    nl, hw, nw, npl, offsets, T = _build(H)

    zero_field = np.zeros((nl, npl))
    ext_field = _ext_field(nl, nw, hw, H, STRENGTH, MASS_Z)

    print("=" * 80)
    print("SELF-CONSISTENT BACK-REACTION")
    print(f"  h={H}, W={PHYS_W}, L={PHYS_L}, s={STRENGTH}, z_src={MASS_Z}")
    print("  Iterate: propagate → amplitude field → re-propagate")
    print("=" * 80)
    print()

    # Baseline: no back-reaction
    free = _propagate(nl, nw, npl, hw, offsets, T, zero_field, K)
    z_free = _cz(free[-1], nw, hw, H)
    p_free = _dp(free[-1])

    grav = _propagate(nl, nw, npl, hw, offsets, T, ext_field, K)
    z_grav = _cz(grav[-1], nw, hw, H)
    p_grav = _dp(grav[-1])

    print(f"Baseline (no back-reaction):")
    print(f"  gravity: {z_grav - z_free:+.6e} TOWARD")
    print(f"  escape: {p_grav / p_free:.4f}")
    print()

    # Self-consistent loop for different epsilon values
    epsilons = [0.0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5]
    n_iterations = 10

    print(f"{'eps':>6s} {'iters':>6s} {'delta':>12s} {'dir':>6s} {'escape':>8s} {'field_max':>10s} {'converged':>10s}")
    print("-" * 68)

    for epsilon in epsilons:
        # Start with external field only
        total_field = ext_field.copy()

        prev_delta = None
        converged = False

        for iteration in range(n_iterations):
            # Propagate on current field
            amps = _propagate(nl, nw, npl, hw, offsets, T, total_field, K)
            delta = _cz(amps[-1], nw, hw, H) - z_free
            escape = _dp(amps[-1]) / p_free if p_free > 0 else 0

            # Check convergence
            if prev_delta is not None and abs(delta - prev_delta) < 1e-8:
                converged = True
                break
            prev_delta = delta

            if epsilon > 0:
                # Generate back-reaction field from amplitude
                f_back = _amplitude_field(amps, nl, npl, epsilon)
                # Total field = external + back-reaction
                total_field = ext_field + f_back

        direction = "TOWARD" if delta > 0 else "AWAY"
        f_max = total_field.max()
        conv_s = f"iter {iteration + 1}" if converged else f"NOT ({iteration + 1})"
        print(f"{epsilon:6.2f} {iteration + 1:6d} {delta:+12.6e} {direction:>6s} "
              f"{escape:8.4f} {f_max:10.4f} {conv_s:>10s}")

    # Symmetry check: back-reaction without external field
    print()
    print("SYMMETRY CHECK (back-reaction, no external field)")
    for epsilon in [0.1, 0.5]:
        total_field = np.zeros((nl, npl))
        for iteration in range(n_iterations):
            amps = _propagate(nl, nw, npl, hw, offsets, T, total_field, K)
            f_back = _amplitude_field(amps, nl, npl, epsilon)
            total_field = f_back
        delta = _cz(amps[-1], nw, hw, H) - z_free
        escape = _dp(amps[-1]) / p_free if p_free > 0 else 0
        print(f"  eps={epsilon:.1f}: delta = {delta:+.6e}, escape = {escape:.4f}")

    # Born test: does Born still hold after self-consistent loop?
    print()
    print("BORN TEST after self-consistency (eps=0.1)")
    # Converge the field first
    total_field = ext_field.copy()
    for _ in range(n_iterations):
        amps = _propagate(nl, nw, npl, hw, offsets, T, total_field, K)
        f_back = _amplitude_field(amps, nl, npl, 0.1)
        total_field = ext_field + f_back

    # Now test Born on the CONVERGED field (linear propagator on fixed field)
    slits = [-1, 0, 1]

    def _p_born(open_slits):
        srcs = [((s + hw) * nw + hw, 1.0 + 0j) for s in open_slits]
        a = np.zeros((nl, npl), dtype=np.complex128)
        for idx, amp in srcs:
            a[0, idx] = amp
        for layer in range(nl - 1):
            sa = a[layer]
            if np.max(np.abs(sa)) < 1e-300:
                continue
            sf = total_field[layer]
            df = total_field[min(layer + 1, nl - 1)]
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
                phase = K * act
                np.add.at(a[layer + 1], di_m,
                          ai_m * (np.cos(phase) + 1j * np.sin(phase)) * w_raw / T)
        return _dp(a[-1])

    p123 = _p_born(slits)
    p12 = _p_born([-1, 0])
    p13 = _p_born([-1, 1])
    p23 = _p_born([0, 1])
    p1 = _p_born([-1])
    p2 = _p_born([0])
    p3 = _p_born([1])
    i3 = p123 - p12 - p13 - p23 + p1 + p2 + p3
    born = abs(i3) / max(p123, 1e-300)
    print(f"  Born |I3|/P = {born:.2e}")

    print()
    print("SAFE READ")
    print("  epsilon > 0 should INCREASE gravity (amplitude reinforces field)")
    print("  if escape DROPS below 1: absorption emerges from self-consistency")
    print("  Born MUST hold (propagator is linear on converged field)")
    print("  symmetry check: no external field → delta = 0 (no preferred direction)")
    print("  if gravity enhanced AND escape < 1 AND Born holds:")
    print("    → complex action is the effective theory of self-consistent back-reaction")


if __name__ == "__main__":
    main()
