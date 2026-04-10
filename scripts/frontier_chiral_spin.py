#!/usr/bin/env python3
"""Chirality-resolved transport, precession, and separation on the chiral walk.

This is a local 2-component chiral architecture, not a conserved SU(2) spin
model. The walk is unitary during propagation, but the chirality index is mixed
by the local coin, so chirality is generally *not* conserved.

What this script tests honestly:
  - total norm preservation
  - chirality precession / polarization oscillation
  - chirality-resolved separation at the detector
  - field-induced change in transport relative to the f=0 control

The same localized field convention used by the retained chiral harness is
kept here:
  theta_eff(x, y) = theta0 * (1 + theta_gain * field(x, y))

The field is a localized point mass in the (x, y) plane. The propagation is
nearest-neighbor with periodic wrap in y so the local unitary update remains
exact.
"""

from __future__ import annotations

import math

try:
    import numpy as np
except ModuleNotFoundError as exc:
    raise SystemExit("numpy is required. Install: pip install numpy") from exc


# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
N_Y = 61
N_LAYERS = 24
THETA0 = 0.30
THETA_GAIN = 0.80
STRENGTH = 8e-4
SOFTENING = 0.10
SOURCE_Y = 30
MASS_X = 12
MASS_Y = 42


# ---------------------------------------------------------------------------
# Field and propagation
# ---------------------------------------------------------------------------
def make_localized_field(
    n_layers: int,
    n_y: int,
    strength: float,
    x_mass: int,
    y_mass: int,
) -> np.ndarray:
    """Localized 1/r point field in the (x, y) plane."""
    field = np.zeros((n_layers, n_y), dtype=float)
    for x in range(n_layers):
        for y in range(n_y):
            r2 = (x - x_mass) ** 2 + (y - y_mass) ** 2
            field[x, y] = strength / math.sqrt(r2 + SOFTENING)
    return field


def propagate_chiral(
    n_y: int,
    n_layers: int,
    field: np.ndarray,
    theta0: float,
    source_y: int,
    initial_spinor: tuple[complex, complex],
) -> tuple[np.ndarray, list[float], list[float], list[float]]:
    """Local chiral walk with field in the mixing angle.

    Returns:
      psi_final,
      norm_history,
      chirality_history,
      total_centroid_history
    """
    psi = np.zeros(2 * n_y, dtype=complex)
    init = np.asarray(initial_spinor, dtype=complex)
    init_norm = float(np.sum(np.abs(init) ** 2))
    if init_norm < 1e-30:
        raise ValueError("initial_spinor must have nonzero norm")
    init = init / math.sqrt(init_norm)
    psi[2 * source_y] = init[0]
    psi[2 * source_y + 1] = init[1]

    norm_history = [float(np.sum(np.abs(psi) ** 2))]
    chirality_history = []
    centroid_history = []

    for x in range(n_layers):
        # Coin: local 2x2 unitary at each site
        for y in range(n_y):
            idx_p = 2 * y
            idx_m = 2 * y + 1
            pp, pm = psi[idx_p], psi[idx_m]
            theta = theta0 * (1.0 + THETA_GAIN * field[x, y])
            c = math.cos(theta)
            s = math.sin(theta)
            psi[idx_p] = c * pp - s * pm
            psi[idx_m] = s * pp + c * pm

        probs = detector_probs(psi, n_y)
        norm_history.append(float(np.sum(np.abs(psi) ** 2)))
        chirality_history.append(chirality_expectation(psi, n_y))
        centroid_history.append(centroid(probs))

        # Shift: + chirality moves right, - chirality moves left.
        new_psi = np.zeros_like(psi)
        for y in range(n_y):
            idx_p = 2 * y
            idx_m = 2 * y + 1
            new_psi[2 * ((y + 1) % n_y)] += psi[idx_p]
            new_psi[2 * ((y - 1) % n_y) + 1] += psi[idx_m]
        psi = new_psi

    return psi, norm_history, chirality_history, centroid_history


def detector_probs(psi: np.ndarray, n_y: int) -> np.ndarray:
    probs = np.zeros(n_y, dtype=float)
    for y in range(n_y):
        probs[y] = abs(psi[2 * y]) ** 2 + abs(psi[2 * y + 1]) ** 2
    return probs


def component_probs(psi: np.ndarray, n_y: int) -> tuple[np.ndarray, np.ndarray]:
    plus = np.zeros(n_y, dtype=float)
    minus = np.zeros(n_y, dtype=float)
    for y in range(n_y):
        plus[y] = abs(psi[2 * y]) ** 2
        minus[y] = abs(psi[2 * y + 1]) ** 2
    return plus, minus


def centroid(probs: np.ndarray) -> float:
    ys = np.arange(len(probs), dtype=float)
    total = float(probs.sum())
    if total < 1e-30:
        return len(probs) / 2.0
    return float(np.dot(ys, probs) / total)


def chirality_expectation(psi: np.ndarray, n_y: int) -> float:
    plus, minus = component_probs(psi, n_y)
    p_plus = float(plus.sum())
    p_minus = float(minus.sum())
    total = p_plus + p_minus
    if total < 1e-30:
        return 0.0
    return (p_plus - p_minus) / total


def precession_stats(history: list[float]) -> tuple[float, float, int]:
    if not history:
        return 0.0, 0.0, 0
    arr = np.asarray(history, dtype=float)
    sign_changes = int(np.sum(np.sign(arr[1:]) != np.sign(arr[:-1])))
    return float(np.min(arr)), float(np.max(arr)), sign_changes


def separation_observables(
    psi: np.ndarray,
    n_y: int,
) -> tuple[float, float, float, float, float]:
    probs = detector_probs(psi, n_y)
    plus, minus = component_probs(psi, n_y)
    c_total = centroid(probs)
    p_plus = float(plus.sum())
    p_minus = float(minus.sum())
    c_plus = centroid(plus) if p_plus > 1e-30 else c_total
    c_minus = centroid(minus) if p_minus > 1e-30 else c_total
    return c_total, c_plus, c_minus, p_plus, p_minus


def print_series(label: str, series: list[float]) -> None:
    print(label)
    for i, value in enumerate(series):
        if i % 4 == 0 or i == len(series) - 1:
            print(f"  layer {i:2d}: {value:+.6f}")


def main() -> None:
    field = make_localized_field(N_LAYERS, N_Y, STRENGTH, MASS_X, MASS_Y)
    field0 = np.zeros_like(field)

    print("FRONTIER: CHIRAL SPIN")
    print(f"Grid: {N_LAYERS} layers x {N_Y} transverse sites")
    print(f"Source y: {SOURCE_Y}")
    print(f"Mass: ({MASS_X}, {MASS_Y}), strength={STRENGTH}, theta0={THETA0}, theta_gain={THETA_GAIN}")
    print("Local nearest-neighbor propagation with periodic wrap in y.")
    print("This is chirality-resolved transport, not conserved SU(2) spin.")
    print()

    print("=" * 72)
    print("TEST 1: NORM + CHIRALITY PRECESSION")
    print("=" * 72)
    psi_flat, norms_flat, chi_flat, cent_flat = propagate_chiral(
        N_Y, N_LAYERS, field0, THETA0, SOURCE_Y, (1.0 + 0.0j, 0.0 + 0.0j)
    )
    psi_field, norms_field, chi_field, cent_field = propagate_chiral(
        N_Y, N_LAYERS, field, THETA0, SOURCE_Y, (1.0 + 0.0j, 0.0 + 0.0j)
    )

    flat_norm_dev = float(np.max(np.abs(np.asarray(norms_flat) - 1.0)))
    field_norm_dev = float(np.max(np.abs(np.asarray(norms_field) - 1.0)))
    print(f"  max norm deviation (flat):  {flat_norm_dev:.3e}")
    print(f"  max norm deviation (field): {field_norm_dev:.3e}")

    flat_min, flat_max, flat_changes = precession_stats(chi_flat)
    field_min, field_max, field_changes = precession_stats(chi_field)
    print(f"  flat chirality expectation range:  [{flat_min:+.6f}, {flat_max:+.6f}]")
    print(f"  field chirality expectation range: [{field_min:+.6f}, {field_max:+.6f}]")
    print(f"  sign changes in chirality expectation (flat/field): {flat_changes}/{field_changes}")

    print_series("  flat chirality expectation by layer:", chi_flat)
    print_series("  field chirality expectation by layer:", chi_field)
    print("  note: chirality is mixed by the coin, so it is not conserved.")

    print("\n" + "=" * 72)
    print("TEST 2: CHIRALITY-RESOLVED SEPARATION")
    print("=" * 72)
    balanced = (1.0 / math.sqrt(2.0), 1.0 / math.sqrt(2.0))
    psi_bal_flat, _, _, _ = propagate_chiral(
        N_Y, N_LAYERS, field0, THETA0, SOURCE_Y, balanced
    )
    psi_bal_field, _, _, _ = propagate_chiral(
        N_Y, N_LAYERS, field, THETA0, SOURCE_Y, balanced
    )

    c_total_flat, c_plus_flat, c_minus_flat, p_plus_flat, p_minus_flat = separation_observables(
        psi_bal_flat, N_Y
    )
    c_total_field, c_plus_field, c_minus_field, p_plus_field, p_minus_field = separation_observables(
        psi_bal_field, N_Y
    )

    sep_flat = c_plus_flat - c_minus_flat
    sep_field = c_plus_field - c_minus_field
    toward_mass_flat = abs(c_total_flat - MASS_Y)
    toward_mass_field = abs(c_total_field - MASS_Y)

    print(f"  flat total centroid:   {c_total_flat:.6f}")
    print(f"  field total centroid:  {c_total_field:.6f}")
    print(f"  flat component centroids:  c+={c_plus_flat:.6f}, c-={c_minus_flat:.6f}, sep={sep_flat:+.6f}")
    print(f"  field component centroids: c+={c_plus_field:.6f}, c-={c_minus_field:.6f}, sep={sep_field:+.6f}")
    print(f"  field component weights:   P+={p_plus_field:.6f}, P-={p_minus_field:.6f}")
    print(f"  separation change (field-flat): {sep_field - sep_flat:+.6f}")

    if toward_mass_field + 1e-15 < toward_mass_flat:
        transport = "TOWARD"
    elif toward_mass_field > toward_mass_flat + 1e-15:
        transport = "AWAY"
    else:
        transport = "NONE"
    print(f"  transport relative to mass: {transport}")

    print("\n" + "=" * 72)
    print("TEST 3: SUMMARY")
    print("=" * 72)
    print("  - Total norm stays at machine precision.")
    print("  - Chirality is not conserved; it precesses and mixes under the coin.")
    print("  - Field-on transport can shift the detector centroid relative to the field-free case.")
    print("  - Chirality-resolved centroids separate at the detector.")
    print("  - This is a spin-like / chirality-resolved transport test, not a conserved-spin claim.")


if __name__ == "__main__":
    main()
