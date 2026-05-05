#!/usr/bin/env python3
"""Quasi-normal mode scaling: does mode spacing depend on G and s?

In GR: QNM frequencies ~ 1/M (inverse mass).
If delta_k ~ 1/(G*s) or 1/G: the mode spectrum encodes the mass.

Test: sweep G at fixed s, and s at fixed G.
Find absorption peaks and measure their spacing.
"""

from __future__ import annotations


# Heavy compute / sweep runner — `AUDIT_TIMEOUT_SEC = 1800`
# means the audit-lane precompute and live audit runner allow up to
# 30 min of wall time before recording a timeout. The 120 s default
# ceiling is too tight under concurrency contention; see
# `docs/audit/RUNNER_CACHE_POLICY.md`.
AUDIT_TIMEOUT_SEC = 1800

import math
import numpy as np

BETA = 0.8
MAX_D_PHYS = 3.0
H = 0.5
PHYS_W = 6
PHYS_L = 30
MASS_Z = 3.0


def _setup():
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
            offsets.append((dy, dz, L, math.exp(-BETA * theta * theta) * H * H / (L * L)))
    T = sum(wr for _, _, _, wr in offsets)
    pos = np.array([(layer * H, iy * H, iz * H)
                    for layer in range(nl)
                    for iy in range(-hw, hw + 1)
                    for iz in range(-hw, hw + 1)])
    return nl, hw, nw, npl, offsets, T, pos


def _ext_field(nl, npl, pos, s):
    gl = int(PHYS_L / H) + 1
    gl = gl // 3
    sx = np.array([gl * H, 0.0, round(MASS_Z / H) * H])
    f = np.zeros((nl, npl))
    for layer in range(nl):
        ls = layer * npl
        dx = pos[ls:ls + npl] - sx
        f[layer] = s / (np.sqrt(np.sum(dx ** 2, axis=1)) + 0.1)
    return f


def _self_field(amps, nl, npl, pos, G):
    f = np.zeros((nl, npl))
    for layer in range(nl):
        p = np.abs(amps[layer]) ** 2
        if p.sum() < 1e-300:
            continue
        pn = p / p.sum()
        top_k = min(30, npl)
        ti = np.argpartition(pn, -top_k)[-top_k:]
        ls = layer * npl
        for idx in ti:
            if pn[idx] < 1e-8:
                continue
            dx = pos[ls:ls + npl] - pos[ls + idx]
            f[layer] += G * pn[idx] / (np.sqrt(np.sum(dx ** 2, axis=1)) + 0.1)
    return f


def _prop(nl, nw, npl, hw, offsets, T, field, k):
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
            phase = k * L * (1.0 - lf)
            np.add.at(amps[layer + 1], di_m,
                      ai_m * (np.cos(phase) + 1j * np.sin(phase)) * w_raw / T)
    return amps


def _converge_field(nl, nw, npl, hw, offsets, T, pos, s, G, k_ref=5.0, n_iter=60):
    ef = _ext_field(nl, npl, pos, s)
    total = ef.copy()
    f_self = np.zeros((nl, npl))
    for _ in range(n_iter):
        amps = _prop(nl, nw, npl, hw, offsets, T, total, k_ref)
        f_new = _self_field(amps, nl, npl, pos, G)
        f_self = 0.1 * f_new + 0.9 * f_self
        total = ef + f_self
    return total


def _absorption_spectrum(nl, nw, npl, hw, offsets, T, field, k_values):
    zero = np.zeros((nl, npl))
    escapes = []
    for k in k_values:
        free_k = _prop(nl, nw, npl, hw, offsets, T, zero, k)
        sc_k = _prop(nl, nw, npl, hw, offsets, T, field, k)
        pf = np.sum(np.abs(free_k[-1]) ** 2)
        ps = np.sum(np.abs(sc_k[-1]) ** 2)
        escapes.append(ps / pf if pf > 0 else 0.0)
    return np.array(escapes)


def _find_absorption_peaks(k_values, escapes, threshold=0.5):
    """Find local minima in escape (= absorption peaks)."""
    peaks = []
    for i in range(1, len(escapes) - 1):
        if escapes[i] < escapes[i - 1] and escapes[i] < escapes[i + 1]:
            if escapes[i] < threshold:
                peaks.append(k_values[i])
    return peaks


def main():
    nl, hw, nw, npl, offsets, T, pos = _setup()
    k_scan = np.arange(2.0, 20.0, 0.5)

    print("=" * 75)
    print("QUASI-NORMAL MODE SCALING")
    print(f"h={H}, W={PHYS_W}, L={PHYS_L}")
    print("=" * 75)
    print()

    # Sweep 1: vary G at fixed s=0.004
    s_fixed = 0.004
    G_values = [0.02, 0.05, 0.10, 0.20]

    print(f"SWEEP 1: G varies, s={s_fixed} fixed")
    print(f"{'G':>6s}  {'peaks':>30s}  {'spacings':>20s}  {'mean_dk':>8s}")
    print("-" * 72)

    for G in G_values:
        cf = _converge_field(nl, nw, npl, hw, offsets, T, pos, s_fixed, G)
        esc = _absorption_spectrum(nl, nw, npl, hw, offsets, T, cf, k_scan)
        peaks = _find_absorption_peaks(k_scan, esc, threshold=0.5)
        if len(peaks) >= 2:
            spacings = [peaks[i + 1] - peaks[i] for i in range(len(peaks) - 1)]
            mean_dk = sum(spacings) / len(spacings)
            peaks_s = ", ".join(f"{p:.1f}" for p in peaks)
            sp_s = ", ".join(f"{s:.1f}" for s in spacings)
            print(f"{G:6.2f}  {peaks_s:>30s}  {sp_s:>20s}  {mean_dk:8.2f}")
        else:
            peaks_s = ", ".join(f"{p:.1f}" for p in peaks) if peaks else "none"
            print(f"{G:6.2f}  {peaks_s:>30s}  {'—':>20s}  {'—':>8s}")

    # Sweep 2: vary s at fixed G=0.05
    G_fixed = 0.05
    s_values = [0.002, 0.004, 0.008, 0.016]

    print()
    print(f"SWEEP 2: s varies, G={G_fixed} fixed")
    print(f"{'s':>6s}  {'peaks':>30s}  {'spacings':>20s}  {'mean_dk':>8s}")
    print("-" * 72)

    for s in s_values:
        cf = _converge_field(nl, nw, npl, hw, offsets, T, pos, s, G_fixed)
        esc = _absorption_spectrum(nl, nw, npl, hw, offsets, T, cf, k_scan)
        peaks = _find_absorption_peaks(k_scan, esc, threshold=0.5)
        if len(peaks) >= 2:
            spacings = [peaks[i + 1] - peaks[i] for i in range(len(peaks) - 1)]
            mean_dk = sum(spacings) / len(spacings)
            peaks_s = ", ".join(f"{p:.1f}" for p in peaks)
            sp_s = ", ".join(f"{s_v:.1f}" for s_v in spacings)
            print(f"{s:6.3f}  {peaks_s:>30s}  {sp_s:>20s}  {mean_dk:8.2f}")
        else:
            peaks_s = ", ".join(f"{p:.1f}" for p in peaks) if peaks else "none"
            print(f"{s:6.3f}  {peaks_s:>30s}  {'—':>20s}  {'—':>8s}")

    # Sweep 3: vary G*s product (keep G*s = constant)
    print()
    print("SWEEP 3: G*s = 0.0002 constant (different partitions)")
    gs_fixed = 0.0002
    partitions = [(0.01, 0.02), (0.02, 0.01), (0.05, 0.004), (0.1, 0.002)]
    print(f"{'G':>6s} {'s':>6s}  {'peaks':>30s}  {'mean_dk':>8s}")
    print("-" * 56)
    for G, s in partitions:
        cf = _converge_field(nl, nw, npl, hw, offsets, T, pos, s, G)
        esc = _absorption_spectrum(nl, nw, npl, hw, offsets, T, cf, k_scan)
        peaks = _find_absorption_peaks(k_scan, esc, threshold=0.5)
        if len(peaks) >= 2:
            spacings = [peaks[i + 1] - peaks[i] for i in range(len(peaks) - 1)]
            mean_dk = sum(spacings) / len(spacings)
            peaks_s = ", ".join(f"{p:.1f}" for p in peaks)
        else:
            peaks_s = ", ".join(f"{p:.1f}" for p in peaks) if peaks else "none"
            mean_dk = float('nan')
        mk = f"{mean_dk:.2f}" if not math.isnan(mean_dk) else "—"
        print(f"{G:6.2f} {s:6.3f}  {peaks_s:>30s}  {mk:>8s}")

    print()
    print("SAFE READ")
    print("  if mean_dk ~ 1/G: modes scale with self-gravity (GR-like)")
    print("  if mean_dk ~ 1/s: modes scale with mass")
    print("  if mean_dk ~ 1/(G*s): modes scale with the product (Schwarzschild)")
    print("  if mean_dk constant at fixed G*s: product is the relevant variable")


if __name__ == "__main__":
    main()
