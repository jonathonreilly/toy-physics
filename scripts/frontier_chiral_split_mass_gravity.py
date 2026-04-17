#!/usr/bin/env python3
"""
Split-Mass / Split-Gravity Chiral Harness
==========================================

Goal:
  Test whether the chiral bottleneck is caused by overloading theta to do
  two jobs at once:
    1. set the free dispersion gap (inertial mass)
    2. set the gravity response to the local field

Models compared:
  - Overloaded baseline:
      theta_eff = theta_m * (1 - theta_m * f)
    The same theta_m controls both the free gap and the field response.

  - Split parameter model:
      theta_eff = theta_m * (1 - g * f)
    theta_m sets the free gap; g is a separate susceptibility parameter.

The transport itself remains local and unitary: coin then nearest-neighbor shift.
"""

from __future__ import annotations

import math
import time

try:
    import numpy as np
except ModuleNotFoundError as exc:
    raise SystemExit("numpy is required.") from exc


# ----------------------------------------------------------------------
# Shared utilities
# ----------------------------------------------------------------------

def fit_power(x_data, y_data):
    if len(x_data) < 3:
        return float("nan"), 0.0
    x = np.asarray(x_data, dtype=float)
    y = np.asarray(y_data, dtype=float)
    mask = (x > 0) & (y > 0)
    x = x[mask]
    y = y[mask]
    if len(x) < 3:
        return float("nan"), 0.0
    lx = np.log(x)
    ly = np.log(y)
    mx = lx.mean()
    my = ly.mean()
    sxx = np.sum((lx - mx) ** 2)
    if sxx < 1e-12:
        return float("nan"), 0.0
    slope = np.sum((lx - mx) * (ly - my)) / sxx
    pred = my + slope * (lx - mx)
    ss_res = np.sum((ly - pred) ** 2)
    ss_tot = np.sum((ly - my) ** 2)
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 1e-30 else 0.0
    return float(slope), float(r2)


def fit_line(x_data, y_data):
    x = np.asarray(x_data, dtype=float)
    y = np.asarray(y_data, dtype=float)
    if len(x) < 2:
        return float("nan"), float("nan"), 0.0
    mx = x.mean()
    my = y.mean()
    sxx = np.sum((x - mx) ** 2)
    if sxx < 1e-12:
        return float("nan"), float("nan"), 0.0
    slope = np.sum((x - mx) * (y - my)) / sxx
    intercept = my - slope * mx
    pred = slope * x + intercept
    ss_res = np.sum((y - pred) ** 2)
    ss_tot = np.sum((y - my) ** 2)
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 1e-30 else 0.0
    return float(slope), float(intercept), float(r2)


def normalize_state(psi):
    norm = np.linalg.norm(psi)
    if norm < 1e-30:
        return psi.copy()
    return psi / norm


def shift_1d(psi, n_y, boundary="reflecting"):
    plus = psi[0::2]
    minus = psi[1::2]
    new_plus = np.zeros(n_y, dtype=complex)
    new_minus = np.zeros(n_y, dtype=complex)

    if boundary == "periodic":
        new_plus[1:] += plus[:-1]
        new_plus[0] += plus[-1]
        new_minus[:-1] += minus[1:]
        new_minus[-1] += minus[0]
    else:
        new_plus[1:] += plus[:-1]
        new_minus[-1] += plus[-1]
        new_minus[:-1] += minus[1:]
        new_plus[0] += minus[0]

    out = np.empty_like(psi)
    out[0::2] = new_plus
    out[1::2] = new_minus
    return out


def detector_probs_1d(psi, n_y):
    return np.abs(psi[0::2]) ** 2 + np.abs(psi[1::2]) ** 2


def centroid(probs):
    ys = np.arange(len(probs), dtype=float)
    total = np.sum(probs)
    if total < 1e-30:
        return float(len(probs) / 2.0)
    return float(np.sum(ys * probs) / total)


def make_field_1d(n_layers, n_y, strength, mass_y):
    ys = np.arange(n_y, dtype=float)
    field = np.zeros((n_layers, n_y), dtype=float)
    for layer in range(n_layers):
        field[layer, :] = strength / (np.abs(ys - mass_y) + 0.1)
    return field


def bloch_eigenvector(theta, k):
    c = np.cos(theta)
    s = np.sin(theta)
    energy = np.arccos(np.clip(c * np.cos(k), -1.0, 1.0))
    lam = np.exp(-1j * energy)
    denom = np.exp(1j * k) * c - lam
    if abs(s) < 1e-12 or abs(denom) < 1e-12:
        vec = np.array([1.0 + 0.0j, 0.0 + 0.0j], dtype=complex)
    else:
        vec = np.array(
            [-np.exp(1j * k) * 1j * s / denom, 1.0 + 0.0j],
            dtype=complex,
        )
    return vec / np.linalg.norm(vec)


def make_gaussian_packet(n_y, center, sigma, k0, theta):
    ys = np.arange(n_y, dtype=float)
    envelope = np.exp(-0.5 * ((ys - center) / sigma) ** 2)
    phase = np.exp(1j * k0 * (ys - center))
    vec = bloch_eigenvector(theta, k0)
    psi = np.zeros(2 * n_y, dtype=complex)
    psi[0::2] = envelope * phase * vec[0]
    psi[1::2] = envelope * phase * vec[1]
    return normalize_state(psi)


def group_velocity(theta, k):
    energy = np.arccos(np.clip(np.cos(theta) * np.cos(k), -1.0, 1.0))
    return float(np.cos(theta) * np.sin(k) / (np.sin(energy) + 1e-30))


def chiral_walk_1d(
    n_y,
    n_layers,
    theta_m,
    field_2d=None,
    mode="baseline",
    g=0.3,
    boundary="reflecting",
    init_psi=None,
    source_y=None,
):
    """
    1D chiral walk with unitary coin + local nearest-neighbor shift.

    mode:
      - baseline: theta_eff = theta_m * (1 - theta_m * f)
      - split:    theta_eff = theta_m * (1 - g * f)
    """
    if init_psi is not None:
        psi = normalize_state(init_psi.astype(complex))
    else:
        if source_y is None:
            source_y = n_y // 2
        psi = np.zeros(2 * n_y, dtype=complex)
        amp = 1.0 / np.sqrt(2.0)
        psi[2 * source_y] = amp
        psi[2 * source_y + 1] = amp

    for layer in range(n_layers):
        field = None if field_2d is None else field_2d[layer]
        if field is None:
            th = np.full(n_y, theta_m, dtype=float)
        else:
            if mode == "baseline":
                th = theta_m * (1.0 - theta_m * field)
            elif mode == "split":
                th = theta_m * (1.0 - g * field)
            else:
                raise ValueError(f"unknown mode: {mode}")

        ct = np.cos(th)
        st = np.sin(th)
        plus = psi[0::2]
        minus = psi[1::2]
        new_plus = ct * plus + 1j * st * minus
        new_minus = 1j * st * plus + ct * minus
        psi = np.empty_like(psi)
        psi[0::2] = new_plus
        psi[1::2] = new_minus
        psi = shift_1d(psi, n_y, boundary=boundary)

    return psi


def exact_dispersion(theta, k):
    return np.arccos(np.clip(np.cos(theta) * np.cos(k), -1.0, 1.0))


def kg_fit(theta_m):
    k_vals = np.linspace(0.01, 0.35, 80)
    E = exact_dispersion(theta_m, k_vals)
    x = k_vals ** 2
    y = E ** 2
    slope, intercept, r2 = fit_line(x, y)
    m_fit = math.sqrt(max(intercept, 0.0))
    return {
        "theta": theta_m,
        "m_fit": m_fit,
        "slope": slope,
        "r2": r2,
        "max_resid": float(np.max(np.abs(y - (slope * x + intercept)))),
    }


def deflection_for_model(theta_m, strength, k0, mode, g, n_y=161, travel_target=18.0):
    center = n_y // 2
    source = center - 24
    mass_site = center
    sigma = 6.0
    vg = group_velocity(theta_m, k0)
    n_layers = max(12, int(round(travel_target / max(abs(vg), 1e-6))))

    field = make_field_1d(n_layers, n_y, strength, mass_site)
    init_psi = make_gaussian_packet(n_y, source, sigma, k0, theta_m)
    psi_free = chiral_walk_1d(
        n_y,
        n_layers,
        theta_m,
        field_2d=None,
        mode=mode,
        g=g,
        boundary="reflecting",
        init_psi=init_psi,
        source_y=source,
    )
    psi_field = chiral_walk_1d(
        n_y,
        n_layers,
        theta_m,
        field_2d=field,
        mode=mode,
        g=g,
        boundary="reflecting",
        init_psi=init_psi,
        source_y=source,
    )

    c0 = centroid(detector_probs_1d(psi_free, n_y))
    cf = centroid(detector_probs_1d(psi_field, n_y))
    return cf - c0, n_layers


def sweep_k(theta_m, strength, mode, g, k_values):
    deflections = []
    layers_used = []
    for k0 in k_values:
        d, n_layers = deflection_for_model(theta_m, strength, k0, mode, g)
        deflections.append(d)
        layers_used.append(n_layers)
    arr = np.asarray(deflections, dtype=float)
    mean = float(np.mean(arr))
    std = float(np.std(arr))
    cv = float(std / abs(mean)) if abs(mean) > 1e-15 else float("inf")
    return deflections, layers_used, cv, mean, std


def sweep_strength(theta_m, k0, mode, g, strengths):
    deflections = []
    for strength in strengths:
        d, _ = deflection_for_model(theta_m, strength, k0, mode, g)
        deflections.append(abs(d))
    alpha, r2 = fit_power(strengths, deflections)
    return deflections, alpha, r2


def sweep_g(theta_m, strength, k0, g_values):
    deflections = []
    for g in g_values:
        d, _ = deflection_for_model(theta_m, strength, k0, "split", g)
        deflections.append(d)
    slope, intercept, r2 = fit_line(g_values, deflections)
    return deflections, slope, intercept, r2


# ----------------------------------------------------------------------
# Main experiment
# ----------------------------------------------------------------------

def main():
    t0 = time.time()

    theta_grid = [0.15, 0.25, 0.35, 0.45, 0.55]
    theta_ref = 0.30
    g_split = 0.30
    k_ref = 0.60
    k_values = [0.20, 0.40, 0.60, 0.80, 1.00]
    strengths = [2e-4, 5e-4, 1e-3, 2e-3, 5e-3]

    print("=" * 72)
    print("SPLIT-PARAMETER CHIRAL GRAVITY")
    print("=" * 72)
    print("Overloaded baseline: theta_eff = theta_m * (1 - theta_m * f)")
    print("Split model:         theta_eff = theta_m * (1 - g * f)")
    print(f"Reference split g = {g_split:.2f} at theta_ref = {theta_ref:.2f}")
    print()

    # Free KG fit is the same field-free operator for both models.
    print("=" * 72)
    print("1) FREE DISPERSION / KG FIT")
    print("=" * 72)
    print(f"{'theta_m':>8}  {'m_fit':>10}  {'slope':>10}  {'R^2':>8}  {'max_resid':>12}")
    free_rows = []
    for theta_m in theta_grid:
        row = kg_fit(theta_m)
        free_rows.append(row)
        print(
            f"{theta_m:8.2f}  {row['m_fit']:10.6f}  {row['slope']:10.6f}"
            f"  {row['r2']:8.6f}  {row['max_resid']:12.3e}"
        )
    print("  Baseline and split are identical here by construction.")
    print()

    # Field strength scaling at fixed theta_ref.
    print("=" * 72)
    print("2) F ∝ M SCALING AT FIXED theta_m")
    print("=" * 72)
    print(f"Reference theta_m = {theta_ref:.2f}, k0 = {k_ref:.2f}")
    base_strengths, alpha_base_m, r2_base_m = sweep_strength(
        theta_ref, k_ref, "baseline", g_split, strengths
    )
    split_strengths, alpha_split_m, r2_split_m = sweep_strength(
        theta_ref, k_ref, "split", g_split, strengths
    )
    print(f"{'M':>10}  {'baseline |d|':>14}  {'split |d|':>14}")
    for m, db, ds in zip(strengths, base_strengths, split_strengths):
        print(f"{m:10.1e}  {db:14.6e}  {ds:14.6e}")
    print(f"Baseline alpha_M = {alpha_base_m:.3f} (R^2={r2_base_m:.4f})")
    print(f"Split alpha_M    = {alpha_split_m:.3f} (R^2={r2_split_m:.4f})")
    print()

    # Wavelength / carrier sensitivity at fixed theta.
    print("=" * 72)
    print("3) k-ACHROMATICITY AT FIXED theta_m")
    print("=" * 72)
    print(f"theta_m = {theta_ref:.2f}, strength = 5e-4")
    base_k, base_layers, base_cv, base_mean, base_std = sweep_k(
        theta_ref, 5e-4, "baseline", g_split, k_values
    )
    split_k, split_layers, split_cv, split_mean, split_std = sweep_k(
        theta_ref, 5e-4, "split", g_split, k_values
    )
    print(f"{'k0':>6}  {'baseline d':>14}  {'split d':>14}  {'layers':>6}")
    for k0, db, ds, nl in zip(k_values, base_k, split_k, base_layers):
        print(f"{k0:6.2f}  {db:14.6e}  {ds:14.6e}  {nl:6d}")
    print(f"Baseline CV_k = {base_cv:.4f}")
    print(f"Split CV_k    = {split_cv:.4f}")
    print()

    # Theta dependence / equivalence-style behavior.
    print("=" * 72)
    print("4) g CONTROL AT FIXED theta_m")
    print("=" * 72)
    print(f"theta_m = {theta_ref:.2f}, k0 = {k_ref:.2f}, strength = 5e-4")
    g_values = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
    g_deflections, g_slope, g_intercept, g_r2 = sweep_g(
        theta_ref, 5e-4, k_ref, g_values
    )
    print(f"{'g':>6}  {'split d':>14}")
    for g_val, d in zip(g_values, g_deflections):
        print(f"{g_val:6.2f}  {d:14.6e}")
    print(f"Split d(g) fit: slope={g_slope:.6e}, R^2={g_r2:.4f}")
    print()

    # Theta dependence / equivalence-style behavior.
    print("=" * 72)
    print("5) theta_m DEPENDENCE / EQUIVALENCE-STYLE BEHAVIOR")
    print("=" * 72)
    print("Using the mean |deflection| across the k band to suppress resonance noise.")
    theta_env_base = []
    theta_env_split = []
    for theta_m in theta_grid:
        base_k_defl, _, _, _, _ = sweep_k(theta_m, 5e-4, "baseline", g_split, k_values)
        split_k_defl, _, _, _, _ = sweep_k(theta_m, 5e-4, "split", g_split, k_values)
        base_env = float(np.mean(np.abs(base_k_defl)))
        split_env = float(np.mean(np.abs(split_k_defl)))
        theta_env_base.append(base_env)
        theta_env_split.append(split_env)
        print(
            f"  theta_m={theta_m:.2f}  baseline env={base_env:.6e}  "
            f"split env={split_env:.6e}"
        )

    alpha_theta_base, r2_theta_base = fit_power(theta_grid, theta_env_base)
    alpha_theta_split, r2_theta_split = fit_power(theta_grid, theta_env_split)
    cv_theta_base = float(np.std(theta_env_base) / np.mean(theta_env_base))
    cv_theta_split = float(np.std(theta_env_split) / np.mean(theta_env_split))
    print(f"Baseline theta envelope exponent = {alpha_theta_base:.3f} (R^2={r2_theta_base:.4f})")
    print(f"Split theta envelope exponent    = {alpha_theta_split:.3f} (R^2={r2_theta_split:.4f})")
    print(f"Baseline theta envelope CV       = {cv_theta_base:.4f}")
    print(f"Split theta envelope CV          = {cv_theta_split:.4f}")

    # Global verdict.
    print()
    print("=" * 72)
    print("VERDICT")
    print("=" * 72)
    kg_ok = all(row["r2"] > 0.999 for row in free_rows)
    m_ok = alpha_base_m > 0.8 and alpha_split_m > 0.8
    theta_reduction = cv_theta_split < cv_theta_base * 0.85
    if theta_reduction and kg_ok and m_ok:
        verdict = "OVERLOADING IS A REAL BLOCKER FOR THE theta DEPENDENCE"
    elif kg_ok and m_ok:
        verdict = "OVERLOADING MATTERS, BUT IT IS NOT THE ONLY BLOCKER"
    else:
        verdict = "RESULTS ARE INCONCLUSIVE"
    print(f"Free KG fit OK:       {kg_ok}")
    print(f"F∝M scaling OK:       {m_ok}")
    print(f"Theta sensitivity reduced in split: {theta_reduction}")
    print(f"g control is linear-ish: {g_r2 > 0.98}")
    print(f"*** {verdict} ***")
    print()
    print(f"Total runtime: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
