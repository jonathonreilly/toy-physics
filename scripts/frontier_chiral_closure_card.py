#!/usr/bin/env python3
"""Integrated chiral closure card on one localized harness.

This script keeps one architecture end-to-end:
  - local 2-component chiral walk
  - nearest-neighbor shift, hence finite signal speed
  - localized point-mass field f(x,y)
  - localized barrier/slit absorber for the Born test

What is localized:
  - the mass: a single point at (x_mass, y_mass) with 1/r falloff
  - the barrier: one layer with three open slits, all other nodes absorbed
  - the propagation rule: nearest-neighbor coin + shift

What is not localized:
  - there is no dense global operator
  - no global x-invariant medium
  - no spectral averaging claim

The retained gravity channel is the theta-coupled chiral walk:
  theta_eff(x,y) = theta0 * (1 + field(x,y))

This is the channel that previously gave:
  - Born barrier/slit I3 ~ 0 when absorption is used
  - TOWARD gravity
  - F∝M ~ 1
  - exact light-cone style transport from the shift

The field does not depend on k in this closure card; k is only used as
a probe label for reporting the reference phase scale.
"""

from __future__ import annotations

import math
import time

try:
    import numpy as np
except ModuleNotFoundError as exc:
    raise SystemExit("numpy is required. Install: pip install numpy") from exc


# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
N_Y = 25
N_LAYERS = 20
THETA0 = 0.30
K_REF = 5.0
STRENGTH = 5e-4
MASS_X = 10
MASS_Y = 22
SOURCE_Y = 10
BARRIER_LAYER = 8
SLITS = [8, 10, 12]
SOFTENING = 0.1


# ---------------------------------------------------------------------------
# Field and propagation
# ---------------------------------------------------------------------------
def make_localized_field(n_layers: int, n_y: int, strength: float,
                         x_mass: int, y_mass: int) -> np.ndarray:
    """Localized 1/r point field in the (x, y) plane."""
    field = np.zeros((n_layers, n_y), dtype=float)
    for x in range(n_layers):
        for y in range(n_y):
            r2 = (x - x_mass) ** 2 + (y - y_mass) ** 2
            field[x, y] = strength / math.sqrt(r2 + SOFTENING)
    return field


def propagate_chiral_theta(
    n_y: int,
    n_layers: int,
    field: np.ndarray,
    theta0: float,
    source_y: int,
    blocked_by_layer: dict[int, set[int]] | None = None,
) -> tuple[np.ndarray, list[float]]:
    """Local chiral walk with field in the mixing angle."""
    if blocked_by_layer is None:
        blocked_by_layer = {}

    psi = np.zeros(2 * n_y, dtype=complex)
    psi[2 * source_y] = 1.0  # right-mover at source

    norms = [float(np.sum(np.abs(psi) ** 2))]
    for x in range(n_layers):
        blocked = blocked_by_layer.get(x, set())

        # Coin: local 2x2 unitary at each site
        for y in range(n_y):
            idx_p = 2 * y
            idx_m = 2 * y + 1
            pp, pm = psi[idx_p], psi[idx_m]
            if y in blocked:
                # absorption barrier: remove amplitude at blocked nodes
                psi[idx_p] = 0.0
                psi[idx_m] = 0.0
                continue

            f = field[x, y]
            theta = theta0 * (1.0 + f)
            c = math.cos(theta)
            s = math.sin(theta)
            psi[idx_p] = c * pp - s * pm
            psi[idx_m] = s * pp + c * pm

        # Shift: + chirality moves right, - chirality moves left
        new_psi = np.zeros_like(psi)
        for y in range(n_y):
            idx_p = 2 * y
            idx_m = 2 * y + 1

            # right-mover
            if y + 1 < n_y:
                new_psi[2 * (y + 1)] += psi[idx_p]
            else:
                new_psi[idx_m] += psi[idx_p]

            # left-mover
            if y - 1 >= 0:
                new_psi[2 * (y - 1) + 1] += psi[idx_m]
            else:
                new_psi[idx_p] += psi[idx_m]

        psi = new_psi
        norms.append(float(np.sum(np.abs(psi) ** 2)))

    return psi, norms


def detector_probs(psi: np.ndarray, n_y: int) -> np.ndarray:
    probs = np.zeros(n_y, dtype=float)
    for y in range(n_y):
        probs[y] = abs(psi[2 * y]) ** 2 + abs(psi[2 * y + 1]) ** 2
    return probs


def centroid(probs: np.ndarray) -> float:
    ys = np.arange(len(probs), dtype=float)
    total = float(probs.sum())
    if total < 1e-30:
        return len(probs) / 2.0
    return float(np.dot(ys, probs) / total)


def fit_power_law(strengths: list[float], deltas: list[float]) -> tuple[float, float]:
    arr = np.array(deltas, dtype=float)
    signs = np.sign(arr)
    if not (np.all(signs == signs[0]) and signs[0] != 0):
        return float("nan"), 0.0
    log_s = np.log10(np.array(strengths, dtype=float))
    log_d = np.log10(np.abs(arr))
    coeffs = np.polyfit(log_s, log_d, 1)
    alpha = float(coeffs[0])
    pred = np.polyval(coeffs, log_s)
    ss_res = float(np.sum((log_d - pred) ** 2))
    ss_tot = float(np.sum((log_d - np.mean(log_d)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return alpha, r2


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
def test_norm(field: np.ndarray) -> bool:
    print("=" * 72)
    print("TEST 1: NORM PRESERVATION")
    print("=" * 72)
    psi, norms = propagate_chiral_theta(N_Y, N_LAYERS, field, THETA0, SOURCE_Y)
    norms = np.array(norms, dtype=float)
    max_dev = float(np.max(np.abs(norms - 1.0)))
    print(f"  norms: {np.array2string(norms, precision=12, suppress_small=True)}")
    print(f"  max deviation from 1.0: {max_dev:.2e}")
    ok = max_dev < 1e-12
    print(f"  {'PASS' if ok else 'FAIL'}")
    return ok


def test_born() -> bool:
    print("\n" + "=" * 72)
    print("TEST 2: BORN / SLIT (3-slit absorption barrier)")
    print("=" * 72)
    field = np.zeros((N_LAYERS, N_Y), dtype=float)
    slit_set = set(SLITS)

    def run(open_slits: list[int]) -> np.ndarray:
        blocked_layer = {BARRIER_LAYER: set(range(N_Y)) - set(open_slits)}
        psi, _ = propagate_chiral_theta(N_Y, N_LAYERS, field, THETA0, SOURCE_Y,
                                        blocked_by_layer=blocked_layer)
        return detector_probs(psi, N_Y)

    A, B, C = SLITS
    P_abc = run([A, B, C])
    P_ab = run([A, B])
    P_ac = run([A, C])
    P_bc = run([B, C])
    P_a = run([A])
    P_b = run([B])
    P_c = run([C])

    I3 = P_abc - P_ab - P_ac - P_bc + P_a + P_b + P_c
    i3_max = float(np.max(np.abs(I3)))
    p_total = float(np.sum(P_abc))
    i3_norm = i3_max / p_total if p_total > 1e-30 else float("inf")

    two_slit = run([A, C])
    one_slit = run([A])
    visibility = 0.0
    if np.max(two_slit) > 1e-30:
        region = two_slit[8:25]
        visibility = float((np.max(region) - np.min(region)) /
                           (np.max(region) + np.min(region) + 1e-30))

    print(f"  localized barrier: layer {BARRIER_LAYER}, open slits {SLITS}")
    print(f"  P(ABC) total: {p_total:.6f}")
    print(f"  |I3| max: {i3_max:.2e}")
    print(f"  |I3|/P:   {i3_norm:.2e}")
    print(f"  fringe visibility (A+C open): {visibility:.4f}")
    ok = i3_norm < 1e-6
    print(f"  {'PASS' if ok else 'FAIL'}")
    return ok


def test_gravity(field: np.ndarray) -> bool:
    print("\n" + "=" * 72)
    print("TEST 3: GRAVITY DIRECTION")
    print("=" * 72)
    field0 = np.zeros_like(field)
    psi_0, _ = propagate_chiral_theta(N_Y, N_LAYERS, field0, THETA0, SOURCE_Y)
    psi_f, _ = propagate_chiral_theta(N_Y, N_LAYERS, field, THETA0, SOURCE_Y)
    c0 = centroid(detector_probs(psi_0, N_Y))
    cf = centroid(detector_probs(psi_f, N_Y))
    delta = cf - c0
    direction = "TOWARD" if delta > 0 else ("AWAY" if delta < 0 else "NONE")
    print(f"  source y = {SOURCE_Y}, mass y = {MASS_Y}")
    print(f"  centroid flat  = {c0:.6f}")
    print(f"  centroid field = {cf:.6f}")
    print(f"  delta          = {delta:+.6e} ({direction})")
    ok = direction == "TOWARD"
    print(f"  {'PASS' if ok else 'FAIL'}")
    return ok


def test_f_prop_m() -> tuple[bool, float, float]:
    print("\n" + "=" * 72)
    print("TEST 4: F ∝ M SCALING")
    print("=" * 72)
    strengths = [1e-6, 2e-6, 5e-6, 1e-5, 2e-5, 5e-5]
    field0 = np.zeros((N_LAYERS, N_Y), dtype=float)
    c0 = centroid(detector_probs(propagate_chiral_theta(N_Y, N_LAYERS, field0,
                                                        THETA0, SOURCE_Y)[0], N_Y))
    deltas = []
    for s in strengths:
        f = make_localized_field(N_LAYERS, N_Y, s, MASS_X, MASS_Y)
        psi, _ = propagate_chiral_theta(N_Y, N_LAYERS, f, THETA0, SOURCE_Y)
        cf = centroid(detector_probs(psi, N_Y))
        delta = cf - c0
        deltas.append(delta)
        print(f"  strength={s:.1e}: delta={delta:+.6e}")

    alpha, r2 = fit_power_law(strengths, deltas)
    ok = np.isfinite(alpha) and abs(alpha - 1.0) < 0.20 and r2 > 0.95
    print(f"  fit alpha = {alpha:.4f}, R^2 = {r2:.6f}")
    print(f"  {'PASS' if ok else 'FAIL'}")
    return ok, alpha, r2


def test_signal_speed() -> bool:
    print("\n" + "=" * 72)
    print("TEST 5: SIGNAL SPEED STYLE CHECK")
    print("=" * 72)
    n_y = 61
    n_layers = 20
    source = n_y // 2
    field = np.zeros((n_layers, n_y), dtype=float)
    psi = np.zeros(2 * n_y, dtype=complex)
    psi[2 * source] = 1.0
    edges = []

    for _ in range(n_layers):
        # coin
        for y in range(n_y):
            idx_p = 2 * y
            idx_m = 2 * y + 1
            pp, pm = psi[idx_p], psi[idx_m]
            c = math.cos(THETA0)
            s = math.sin(THETA0)
            psi[idx_p] = c * pp - s * pm
            psi[idx_m] = s * pp + c * pm

        # shift
        new_psi = np.zeros_like(psi)
        for y in range(n_y):
            idx_p = 2 * y
            idx_m = 2 * y + 1
            if y + 1 < n_y:
                new_psi[2 * (y + 1)] += psi[idx_p]
            else:
                new_psi[idx_m] += psi[idx_p]
            if y - 1 >= 0:
                new_psi[2 * (y - 1) + 1] += psi[idx_m]
            else:
                new_psi[idx_p] += psi[idx_m]
        psi = new_psi

        probs = np.array([abs(psi[2 * y]) ** 2 + abs(psi[2 * y + 1]) ** 2
                          for y in range(n_y)], dtype=float)
        nz = np.where(probs > 1e-30)[0]
        if len(nz) > 0:
            edge = max(nz[-1] - source, source - nz[0])
        else:
            edge = 0
        edges.append(edge)

    layers = np.arange(1, n_layers + 1, dtype=float)
    edges_arr = np.array(edges, dtype=float)
    slope = float(np.polyfit(layers, edges_arr, 1)[0]) if np.any(edges_arr > 0) else 0.0
    print(f"  edges: {[int(e) for e in edges[:10]]} ...")
    print(f"  fitted front speed = {slope:.4f} sites/layer")
    ok = 0.5 < slope <= 1.05
    print(f"  {'PASS' if ok else 'FAIL'}")
    return ok


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    print("FRONTIER: CHIRAL CLOSURE CARD")
    print("Architecture: local 2-component chiral walk")
    print("Coupling: theta-coupled localized mass field")
    print(f"Localized mass: point at (x={MASS_X}, y={MASS_Y})")
    print(f"Localized barrier: layer {BARRIER_LAYER}, slits {SLITS}")
    print(f"Source: y={SOURCE_Y}")
    print(f"Reference k label: {K_REF} (spectral averaging not applicable here)")
    print()

    field = make_localized_field(N_LAYERS, N_Y, STRENGTH, MASS_X, MASS_Y)

    print("What is localized:")
    print("  - mass field is point-localized in (x, y)")
    print("  - barrier is localized to one layer with three slits")
    print("  - propagation is nearest-neighbor only")
    print("What is not localized:")
    print("  - no dense global operator")
    print("  - no x-invariant medium")
    print("  - no source-defined spectral average")
    print()

    t0 = time.time()
    results = {}
    results["norm"] = test_norm(field)
    results["born"] = test_born()
    results["gravity"] = test_gravity(field)
    fm_pass, alpha, r2 = test_f_prop_m()
    results["f_prop_m"] = fm_pass
    results["signal_speed"] = test_signal_speed()
    elapsed = time.time() - t0

    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)
    for name, passed in results.items():
        print(f"  {name:14s}: {'PASS' if passed else 'FAIL'}")

    core = results["norm"] and results["born"]
    grav = results["gravity"] and results["f_prop_m"]
    all_pass = all(results.values())
    print(f"\n  Core (norm + Born): {'PASS' if core else 'FAIL'}")
    print(f"  Gravity (dir + F∝M): {'PASS' if grav else 'FAIL'}")
    print(f"  ALL TESTS:          {'PASS' if all_pass else 'FAIL'}")
    print(f"  Elapsed:             {elapsed:.2f}s")
    print("\n  Notes:")
    print("    - This closure card is theta-coupled only; k is a reference label.")
    print("    - Gravity and F∝M are reported on the same localized harness.")
    print("    - Signal speed is a finite-support style check from the shift rule.")


if __name__ == "__main__":
    main()
