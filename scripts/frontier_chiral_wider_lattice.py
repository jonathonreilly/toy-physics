#!/usr/bin/env python3
"""
Lorentzian Chiral Walk -- Wider Lattice & Parity Oscillation Diagnosis
======================================================================

Two issues to fix from the closure card:

Issue 1: Distance law on wider lattice (n_y=41, height=20).
  Mass at d=2..10 from center; fit TOWARD points to power law.

Issue 2: Multi-L parity oscillation.
  Gravity sign alternates with L. Diagnose: is it parity of L?
  Does |delta| grow? Does it depend on theta_0?

Issue 3: Fix attempt -- symmetric chirality source.
  Initialize both chiralities to kill parity oscillation.

Issue 4: F proportional to M on wider lattice.

HYPOTHESIS: "Wider lattice gives 7+ TOWARD out of 9 distance points.
  Multi-L oscillation is a source-parity artifact fixed by symmetric init."
FALSIFICATION: "If distance law still fails at d>4, or symmetric source
  doesn't fix the oscillation."
"""

from __future__ import annotations
import math
import time

try:
    import numpy as np
except ModuleNotFoundError as exc:
    raise SystemExit("numpy is required.") from exc


# ── Parameters ────────────────────────────────────────────────────────
N_Y = 41              # height=20 (sites 0..40)
N_LAYERS = 30
THETA_0 = 0.3
K = 5.0
STRENGTH = 5e-4
SOURCE_Y = N_Y // 2   # = 20


# ── 1D Chiral Propagator (copied from closure card) ─────────────────

def make_field_1d(n_layers, n_y, strength, mass_y):
    """1/r field from mass at mass_y."""
    field = np.zeros((n_layers, n_y))
    for x in range(n_layers):
        for y in range(n_y):
            field[x, y] = strength / (abs(y - mass_y) + 0.1)
    return field


def propagate_chiral(n_y, n_layers, theta_0, k, field, source_y,
                     barrier_layer=None, open_slits=None,
                     source_init=None):
    """
    Lorentzian chiral walk with absorption blocking.

    theta(y) = theta_0 * (1 - f(x,y))   [Lorentzian coupling]
    phi = 0  (no phase coupling)

    source_init: if provided, a tuple (psi_plus, psi_minus) for the source site.
                 Default: (1.0, 0.0) = pure right-mover.
    """
    psi = np.zeros(2 * n_y, dtype=complex)
    if source_init is not None:
        psi[2 * source_y] = source_init[0]
        psi[2 * source_y + 1] = source_init[1]
    else:
        psi[2 * source_y] = 1.0  # right-mover at source

    for x in range(n_layers):
        # Step 1: Coin at each site
        for y in range(n_y):
            f = field[x, y] if field is not None else 0.0
            th = theta_0 * (1.0 - f)
            idx_p = 2 * y
            idx_m = 2 * y + 1
            pp, pm = psi[idx_p], psi[idx_m]
            psi[idx_p] = np.cos(th) * pp - np.sin(th) * pm
            psi[idx_m] = np.sin(th) * pp + np.cos(th) * pm

        # Step 1b: Absorption blocking at barrier
        if barrier_layer is not None and x == barrier_layer and open_slits is not None:
            for y in range(n_y):
                if y not in open_slits:
                    psi[2 * y] = 0.0
                    psi[2 * y + 1] = 0.0

        # Step 2: Shift with reflecting boundaries
        new_psi = np.zeros_like(psi)
        for y in range(n_y):
            # psi_+ moves to y+1
            if y + 1 < n_y:
                new_psi[2 * (y + 1)] += psi[2 * y]
            else:
                new_psi[2 * y + 1] += psi[2 * y]  # reflect: + -> -
            # psi_- moves to y-1
            if y - 1 >= 0:
                new_psi[2 * (y - 1) + 1] += psi[2 * y + 1]
            else:
                new_psi[2 * y] += psi[2 * y + 1]  # reflect: - -> +
        psi = new_psi

    return psi


def detector_probs(psi, n_y):
    """Total probability at each y site."""
    probs = np.zeros(n_y)
    for y in range(n_y):
        probs[y] = abs(psi[2 * y]) ** 2 + abs(psi[2 * y + 1]) ** 2
    return probs


def centroid(probs):
    """Probability-weighted centroid."""
    ys = np.arange(len(probs))
    total = probs.sum()
    if total < 1e-30:
        return len(probs) / 2.0
    return float(np.sum(ys * probs) / total)


def fit_power(x_data, y_data):
    """Fit log-log power law. Returns (slope, R^2)."""
    if len(x_data) < 3:
        return float('nan'), 0.0
    lx = np.log(np.array(x_data, dtype=float))
    ly = np.log(np.array(y_data, dtype=float))
    mx = lx.mean(); my = ly.mean()
    sxx = np.sum((lx - mx) ** 2)
    sxy = np.sum((lx - mx) * (ly - my))
    if sxx < 1e-10:
        return float('nan'), 0.0
    slope = sxy / sxx
    ss_res = np.sum((ly - (my + slope * (lx - mx))) ** 2)
    ss_tot = np.sum((ly - my) ** 2)
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return float(slope), float(r2)


# ======================================================================
# MAIN
# ======================================================================

def main():
    t_total = time.time()
    print("=" * 72)
    print("LORENTZIAN CHIRAL WALK -- WIDER LATTICE & PARITY DIAGNOSIS")
    print("=" * 72)
    print(f"  n_y={N_Y} (height={N_Y//2}), n_layers={N_LAYERS}")
    print(f"  theta_0={THETA_0}, strength={STRENGTH}")
    print(f"  source_y={SOURCE_Y}")
    print("=" * 72)
    print()

    # ==================================================================
    # PART 1: Distance law on wider lattice
    # ==================================================================
    print("=" * 72)
    print("PART 1: DISTANCE LAW ON WIDER LATTICE (n_y=41)")
    print("=" * 72)

    offsets = list(range(2, 11))  # d=2 through d=10
    field_0 = np.zeros((N_LAYERS, N_Y))

    # Free propagation (no mass)
    psi_free = propagate_chiral(N_Y, N_LAYERS, THETA_0, K, field_0, SOURCE_Y)
    c_free = centroid(detector_probs(psi_free, N_Y))
    print(f"  Free centroid: {c_free:.6f} (center={SOURCE_Y})")
    print()

    toward_count = 0
    away_count = 0
    toward_ds = []
    toward_deltas = []

    print(f"  {'d':>3s}  {'y_mass':>6s}  {'centroid':>10s}  {'delta':>12s}  {'dir':>6s}")
    print(f"  {'---':>3s}  {'------':>6s}  {'--------':>10s}  {'--------':>12s}  {'---':>6s}")

    for d in offsets:
        y_mass = SOURCE_Y + d
        field_m = make_field_1d(N_LAYERS, N_Y, STRENGTH, y_mass)
        psi_m = propagate_chiral(N_Y, N_LAYERS, THETA_0, K, field_m, SOURCE_Y)
        c_m = centroid(detector_probs(psi_m, N_Y))
        delta = c_m - c_free
        direction = "TOWARD" if delta > 0 else "AWAY"
        if delta > 0:
            toward_count += 1
            toward_ds.append(d)
            toward_deltas.append(abs(delta))
        else:
            away_count += 1
        print(f"  {d:3d}  {y_mass:6d}  {c_m:10.6f}  {delta:12.8f}  {direction:>6s}")

    print()
    print(f"  TOWARD: {toward_count}/9, AWAY: {away_count}/9")

    if len(toward_ds) >= 3:
        slope, r2 = fit_power(toward_ds, toward_deltas)
        print(f"  Power-law fit (TOWARD points): slope={slope:.3f}, R^2={r2:.4f}")
    else:
        print(f"  Not enough TOWARD points for power-law fit")

    dist_pass = toward_count >= 7
    print(f"  Distance law: {'PASS' if dist_pass else 'FAIL'} (need 7+ TOWARD)")
    print()

    # ==================================================================
    # PART 2: Multi-L parity oscillation diagnosis
    # ==================================================================
    print("=" * 72)
    print("PART 2: MULTI-L PARITY OSCILLATION DIAGNOSIS")
    print("=" * 72)

    y_mass_diag = SOURCE_Y + 4  # d=4 from center
    L_values = list(range(10, 42, 2))  # L=10,12,...,40

    print(f"  y_mass={y_mass_diag} (d=4), source={SOURCE_Y}")
    print()
    print(f"  {'L':>3s}  {'delta':>14s}  {'dir':>6s}  {'L%2':>3s}  {'L%4':>3s}")
    print(f"  {'---':>3s}  {'--------':>14s}  {'---':>6s}  {'---':>3s}  {'---':>3s}")

    l_results = []
    for L in L_values:
        field_0_L = np.zeros((L, N_Y))
        field_m_L = make_field_1d(L, N_Y, STRENGTH, y_mass_diag)
        psi_free_L = propagate_chiral(N_Y, L, THETA_0, K, field_0_L, SOURCE_Y)
        psi_mass_L = propagate_chiral(N_Y, L, THETA_0, K, field_m_L, SOURCE_Y)
        c_f = centroid(detector_probs(psi_free_L, N_Y))
        c_m = centroid(detector_probs(psi_mass_L, N_Y))
        delta = c_m - c_f
        direction = "TOWARD" if delta > 0 else "AWAY"
        l_results.append((L, delta, direction))
        print(f"  {L:3d}  {delta:14.10f}  {direction:>6s}  {L%2:3d}  {L%4:3d}")

    # Analyze the pattern
    print()
    toward_Ls = [r[0] for r in l_results if r[2] == "TOWARD"]
    away_Ls = [r[0] for r in l_results if r[2] == "AWAY"]
    print(f"  TOWARD L values: {toward_Ls}")
    print(f"  AWAY L values:   {away_Ls}")

    # Check if it's every-other-L
    signs = [1 if r[1] > 0 else -1 for r in l_results]
    alternating = all(signs[i] != signs[i+1] for i in range(len(signs)-1))
    print(f"  Strictly alternating? {alternating}")

    # Check L%4 pattern
    t_mod4 = set(L % 4 for L in toward_Ls) if toward_Ls else set()
    a_mod4 = set(L % 4 for L in away_Ls) if away_Ls else set()
    print(f"  TOWARD L mod 4: {t_mod4}")
    print(f"  AWAY L mod 4:   {a_mod4}")

    # Check |delta| monotonicity
    abs_deltas = [abs(r[1]) for r in l_results]
    monotonic_growing = all(abs_deltas[i] <= abs_deltas[i+1] for i in range(len(abs_deltas)-1))
    print(f"  |delta| monotonically growing? {monotonic_growing}")
    print()

    # Theta_0 dependence
    print("  --- Theta_0 dependence of oscillation ---")
    print(f"  {'theta_0':>7s}  {'L=20 delta':>14s}  {'L=24 delta':>14s}  {'same_sign?':>10s}")
    for th0 in [0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0]:
        deltas_th = []
        for L in [20, 24]:
            f0 = np.zeros((L, N_Y))
            fm = make_field_1d(L, N_Y, STRENGTH, y_mass_diag)
            pf = propagate_chiral(N_Y, L, th0, K, f0, SOURCE_Y)
            pm = propagate_chiral(N_Y, L, th0, K, fm, SOURCE_Y)
            d = centroid(detector_probs(pm, N_Y)) - centroid(detector_probs(pf, N_Y))
            deltas_th.append(d)
        same = "YES" if (deltas_th[0] > 0) == (deltas_th[1] > 0) else "NO"
        print(f"  {th0:7.2f}  {deltas_th[0]:14.10f}  {deltas_th[1]:14.10f}  {same:>10s}")
    print()

    # ==================================================================
    # PART 3: Symmetric source fix
    # ==================================================================
    print("=" * 72)
    print("PART 3: SYMMETRIC SOURCE FIX")
    print("=" * 72)

    source_types = {
        "default (psi+ only)":    (1.0 + 0j, 0.0 + 0j),
        "symmetric (1/sqrt2, 1/sqrt2)": (1.0/np.sqrt(2), 1.0/np.sqrt(2)),
        "90-phase (1/sqrt2, i/sqrt2)":  (1.0/np.sqrt(2), 1j/np.sqrt(2)),
        "psi- only":              (0.0 + 0j, 1.0 + 0j),
    }

    for src_name, src_init in source_types.items():
        print(f"\n  Source: {src_name}")
        print(f"    {'L':>3s}  {'delta':>14s}  {'dir':>6s}")
        print(f"    {'---':>3s}  {'--------':>14s}  {'---':>6s}")

        toward_n = 0
        for L in L_values:
            f0 = np.zeros((L, N_Y))
            fm = make_field_1d(L, N_Y, STRENGTH, y_mass_diag)
            pf = propagate_chiral(N_Y, L, THETA_0, K, f0, SOURCE_Y,
                                  source_init=src_init)
            pm = propagate_chiral(N_Y, L, THETA_0, K, fm, SOURCE_Y,
                                  source_init=src_init)
            c_f = centroid(detector_probs(pf, N_Y))
            c_m = centroid(detector_probs(pm, N_Y))
            delta = c_m - c_f
            direction = "TOWARD" if delta > 0 else "AWAY"
            if delta > 0:
                toward_n += 1
            print(f"    {L:3d}  {delta:14.10f}  {direction:>6s}")

        print(f"    TOWARD: {toward_n}/{len(L_values)}")

    print()

    # Also test symmetric source on the distance law
    print("  --- Distance law with symmetric source ---")
    src_sym = (1.0/np.sqrt(2), 1.0/np.sqrt(2))
    psi_free_sym = propagate_chiral(N_Y, N_LAYERS, THETA_0, K, field_0,
                                    SOURCE_Y, source_init=src_sym)
    c_free_sym = centroid(detector_probs(psi_free_sym, N_Y))

    toward_sym = 0
    sym_ds = []
    sym_deltas = []

    print(f"  {'d':>3s}  {'delta':>14s}  {'dir':>6s}")
    print(f"  {'---':>3s}  {'--------':>14s}  {'---':>6s}")
    for d in offsets:
        y_mass = SOURCE_Y + d
        fm = make_field_1d(N_LAYERS, N_Y, STRENGTH, y_mass)
        pm = propagate_chiral(N_Y, N_LAYERS, THETA_0, K, fm, SOURCE_Y,
                              source_init=src_sym)
        c_m = centroid(detector_probs(pm, N_Y))
        delta = c_m - c_free_sym
        direction = "TOWARD" if delta > 0 else "AWAY"
        if delta > 0:
            toward_sym += 1
            sym_ds.append(d)
            sym_deltas.append(abs(delta))
        print(f"  {d:3d}  {delta:14.10f}  {direction:>6s}")

    print(f"  TOWARD (symmetric): {toward_sym}/9")
    if len(sym_ds) >= 3:
        slope, r2 = fit_power(sym_ds, sym_deltas)
        print(f"  Power-law fit: slope={slope:.3f}, R^2={r2:.4f}")
    print()

    # ==================================================================
    # PART 4: F proportional to M on wider lattice
    # ==================================================================
    print("=" * 72)
    print("PART 4: F PROPORTIONAL TO M ON WIDER LATTICE")
    print("=" * 72)

    y_mass_fm = SOURCE_Y + 4  # d=4
    strengths = [1e-4, 2e-4, 5e-4, 1e-3, 2e-3, 5e-3]

    psi_free_fm = propagate_chiral(N_Y, N_LAYERS, THETA_0, K, field_0, SOURCE_Y)
    c_free_fm = centroid(detector_probs(psi_free_fm, N_Y))

    print(f"  y_mass={y_mass_fm} (d=4), L={N_LAYERS}")
    print(f"  {'strength':>10s}  {'delta':>14s}  {'delta/strength':>16s}  {'dir':>6s}")
    print(f"  {'--------':>10s}  {'--------':>14s}  {'--------------':>16s}  {'---':>6s}")

    fm_deltas = []
    fm_strengths_used = []
    for s in strengths:
        fm = make_field_1d(N_LAYERS, N_Y, s, y_mass_fm)
        pm = propagate_chiral(N_Y, N_LAYERS, THETA_0, K, fm, SOURCE_Y)
        c_m = centroid(detector_probs(pm, N_Y))
        delta = c_m - c_free_fm
        ratio = delta / s if s > 0 else 0.0
        direction = "TOWARD" if delta > 0 else "AWAY"
        fm_deltas.append(abs(delta))
        fm_strengths_used.append(s)
        print(f"  {s:10.1e}  {delta:14.10f}  {ratio:16.6f}  {direction:>6s}")

    # Fit power law delta vs strength
    if len(fm_deltas) >= 3:
        slope_fm, r2_fm = fit_power(fm_strengths_used, fm_deltas)
        print(f"\n  Power-law fit (delta vs M): slope={slope_fm:.3f}, R^2={r2_fm:.4f}")
        fm_pass = abs(slope_fm - 1.0) < 0.15
        print(f"  F prop M: {'PASS' if fm_pass else 'FAIL'} (slope={slope_fm:.3f}, want ~1.0)")
    else:
        print(f"  Not enough points for fit")
    print()

    # Also test F~M with symmetric source
    print("  --- F proportional to M with symmetric source ---")
    psi_free_sym2 = propagate_chiral(N_Y, N_LAYERS, THETA_0, K, field_0,
                                     SOURCE_Y, source_init=src_sym)
    c_free_sym2 = centroid(detector_probs(psi_free_sym2, N_Y))

    fm_deltas_sym = []
    fm_str_sym = []
    print(f"  {'strength':>10s}  {'delta':>14s}  {'delta/strength':>16s}  {'dir':>6s}")
    print(f"  {'--------':>10s}  {'--------':>14s}  {'--------------':>16s}  {'---':>6s}")
    for s in strengths:
        fm = make_field_1d(N_LAYERS, N_Y, s, y_mass_fm)
        pm = propagate_chiral(N_Y, N_LAYERS, THETA_0, K, fm, SOURCE_Y,
                              source_init=src_sym)
        c_m = centroid(detector_probs(pm, N_Y))
        delta = c_m - c_free_sym2
        ratio = delta / s if s > 0 else 0.0
        direction = "TOWARD" if delta > 0 else "AWAY"
        fm_deltas_sym.append(abs(delta))
        fm_str_sym.append(s)
        print(f"  {s:10.1e}  {delta:14.10f}  {ratio:16.6f}  {direction:>6s}")

    if len(fm_deltas_sym) >= 3:
        slope_s, r2_s = fit_power(fm_str_sym, fm_deltas_sym)
        print(f"\n  Power-law fit (symmetric): slope={slope_s:.3f}, R^2={r2_s:.4f}")
        fm_pass_s = abs(slope_s - 1.0) < 0.15
        print(f"  F prop M (symmetric): {'PASS' if fm_pass_s else 'FAIL'}")
    print()

    # ==================================================================
    # SUMMARY
    # ==================================================================
    print("=" * 72)
    print("SUMMARY")
    print("=" * 72)

    print(f"  Part 1 -- Distance law (wider, default source):")
    print(f"    TOWARD: {toward_count}/9  {'PASS' if dist_pass else 'FAIL'}")

    print(f"  Part 2 -- Multi-L oscillation:")
    print(f"    Alternating: {alternating}")
    print(f"    TOWARD L mod 4: {t_mod4}, AWAY L mod 4: {a_mod4}")

    print(f"  Part 3 -- Symmetric source fix:")
    print(f"    (see detailed results above)")

    print(f"  Part 4 -- F prop M (wider lattice):")
    if len(fm_deltas) >= 3:
        print(f"    slope={slope_fm:.3f}  {'PASS' if fm_pass else 'FAIL'}")

    elapsed = time.time() - t_total
    print(f"\n  Total time: {elapsed:.1f}s")
    print("=" * 72)


if __name__ == "__main__":
    main()
