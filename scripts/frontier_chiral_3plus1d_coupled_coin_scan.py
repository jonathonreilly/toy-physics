#!/usr/bin/env python3
"""
Frontier: 3+1D chiral coupled-coin scan
=======================================

Goal:
  Interpolate between the current factorized 6x6 coin
  (2x2 ⊕ 2x2 ⊕ 2x2) and a cross-axis coupled family that remains unitary.

Questions:
  1. Does cross-axis coupling improve low-k 3D Klein-Gordon/isotropic
     dispersion quality?
  2. Does cross-axis coupling improve a 3D gauge/loop response?

This is intentionally review-safe and self-contained:
  - no edits to the existing retained harnesses
  - unitary coin family by construction
  - periodic 3D lattice with a torus-aware gauge sheet
  - scan reports best/worst coupling points for both metrics

The scan parameter `mix` runs from 0.0 (direct-sum baseline) to 1.0
(strongest coupled pair-space unitary in this family).
"""

from __future__ import annotations

import time
from dataclasses import dataclass

import numpy as np


# ── Parameters ──────────────────────────────────────────────────────────────
N_DEFAULT = 17
L_DEFAULT = 16
THETA0 = 0.30
STRENGTH = 5e-4
MIX_VALUES = np.linspace(0.0, 1.0, 9)


# ── Basic state helpers ─────────────────────────────────────────────────────
def make_state(n: int, source=None, balanced: bool = True) -> np.ndarray:
    """Balanced 6-component source at one lattice site."""
    psi = np.zeros((6, n, n, n), dtype=np.complex128)
    if source is None:
        source = (n // 2, n // 2, n // 2)
    sy, sz, sw = source
    amp = 1.0 / np.sqrt(6.0) if balanced else 1.0
    for k in range(6):
        psi[k, sy, sz, sw] = amp
    return psi


def probability_density(psi: np.ndarray) -> np.ndarray:
    return np.sum(np.abs(psi) ** 2, axis=0)


def min_image_dist(n: int, mass_pos: tuple[int, int, int]) -> np.ndarray:
    """Minimum-image distance on a 3D periodic lattice."""
    coords = np.arange(n)
    dy = np.abs(coords[:, None, None] - mass_pos[0])
    dy = np.minimum(dy, n - dy)
    dz = np.abs(coords[None, :, None] - mass_pos[1])
    dz = np.minimum(dz, n - dz)
    dw = np.abs(coords[None, None, :] - mass_pos[2])
    dw = np.minimum(dw, n - dw)
    return np.sqrt(dy**2 + dz**2 + dw**2)


def theta_grid(n: int, mass_positions=None, strength: float = STRENGTH) -> np.ndarray:
    """Local theta field: theta0 * (1 - sum_m strength/(r_m + 0.1))."""
    if mass_positions is None:
        mass_positions = []
    total_f = np.zeros((n, n, n), dtype=float)
    for mp in mass_positions:
        r = min_image_dist(n, mp)
        total_f += strength / (r + 0.1)
    return THETA0 * (1.0 - total_f)


# ── Coupled-coin family ──────────────────────────────────────────────────────
COUPLER6_H = np.ones((6, 6), dtype=float) - np.eye(6, dtype=float)
COUPLER6_EIGVALS, COUPLER6_EIGVECS = np.linalg.eigh(COUPLER6_H / 5.0)


def coupler6_unitary(mix: float) -> np.ndarray:
    """6x6 unitary that couples all chirality components.

    mix=0.0 -> identity
    mix=1.0 -> strongest coupling in this family

    The generator is fully dense (all off-diagonal entries equal), so this is
    intentionally more coupled than the factorized 2x2⊕2x2⊕2x2 baseline.
    """
    phases = np.exp(1j * (np.pi / 2.0) * mix * COUPLER6_EIGVALS)
    return COUPLER6_EIGVECS @ np.diag(phases) @ COUPLER6_EIGVECS.conj().T


def apply_coin(psi: np.ndarray, theta: np.ndarray, mix: float) -> np.ndarray:
    """Apply factorized pair coins followed by a unitary pair-space mixer."""
    ct = np.cos(theta)
    st = np.sin(theta)

    # Direct-sum 2x2 coins on each of the three axis pairs.
    mixed = np.empty_like(psi)
    for a, b in ((0, 1), (2, 3), (4, 5)):
        pa = psi[a]
        pb = psi[b]
        mixed[a] = ct * pa + 1j * st * pb
        mixed[b] = 1j * st * pa + ct * pb

    if mix <= 1e-15:
        return mixed

    # Fully coupled 6x6 unitary across all chirality components.
    flat = mixed.reshape(6, -1)
    coupled = coupler6_unitary(mix) @ flat
    return coupled.reshape(6, *mixed.shape[1:])


def apply_shift(psi: np.ndarray, gauge=None) -> np.ndarray:
    """Nearest-neighbor shift with optional U(1) gauge phases.

    Gauge fields are arrays A_y, A_z, A_w defined on sites as the phase on the
    positive link leaving that site.
    """
    if gauge is None:
        gauge = {}
    ay = gauge.get("ay")
    az = gauge.get("az")
    aw = gauge.get("aw")

    out = np.zeros_like(psi)

    if ay is None:
        out[0] = np.roll(psi[0], -1, axis=0)
        out[1] = np.roll(psi[1], +1, axis=0)
    else:
        out[0] = np.roll(psi[0] * np.exp(1j * ay), -1, axis=0)
        out[1] = np.roll(psi[1], +1, axis=0) * np.exp(-1j * ay)

    if az is None:
        out[2] = np.roll(psi[2], -1, axis=1)
        out[3] = np.roll(psi[3], +1, axis=1)
    else:
        out[2] = np.roll(psi[2] * np.exp(1j * az), -1, axis=1)
        out[3] = np.roll(psi[3], +1, axis=1) * np.exp(-1j * az)

    if aw is None:
        out[4] = np.roll(psi[4], -1, axis=2)
        out[5] = np.roll(psi[5], +1, axis=2)
    else:
        out[4] = np.roll(psi[4] * np.exp(1j * aw), -1, axis=2)
        out[5] = np.roll(psi[5], +1, axis=2) * np.exp(-1j * aw)

    return out


def evolve(n: int, n_layers: int, mix: float, strength: float, mass_positions=None, gauge=None,
           source=None) -> np.ndarray:
    psi = make_state(n, source=source)
    theta = theta_grid(n, mass_positions=mass_positions, strength=strength)
    for _ in range(n_layers):
        psi = apply_coin(psi, theta, mix)
        psi = apply_shift(psi, gauge=gauge)
    return psi


# ── Dispersion scan ─────────────────────────────────────────────────────────
@dataclass
class DispersionResult:
    mix: float
    r2: float
    mass2: float
    speed2: float
    direction_cv: float
    mean_abs_resid: float


def step_operator_k(kvec: tuple[float, float, float], theta: float, mix: float) -> np.ndarray:
    """6x6 step operator in momentum space."""
    ky, kz, kw = kvec
    c = np.cos(theta)
    s = np.sin(theta)
    coin6 = np.zeros((6, 6), dtype=np.complex128)
    blocks = ((0, 1), (2, 3), (4, 5))
    for a, b in blocks:
        coin6[a, a] = c
        coin6[a, b] = 1j * s
        coin6[b, a] = 1j * s
        coin6[b, b] = c

    coin6 = coupler6_unitary(mix) @ coin6
    shift = np.diag(
        np.array(
            [
                np.exp(1j * ky),
                np.exp(-1j * ky),
                np.exp(1j * kz),
                np.exp(-1j * kz),
                np.exp(1j * kw),
                np.exp(-1j * kw),
            ],
            dtype=np.complex128,
        )
    )
    return shift @ coin6


def low_band_energy(kvec: tuple[float, float, float], theta: float, mix: float) -> float:
    eigvals = np.linalg.eigvals(step_operator_k(kvec, theta, mix))
    phases = np.angle(eigvals)
    positive = phases[phases >= 0.0]
    if positive.size:
        return float(np.min(positive))
    return float(np.min(np.abs(phases)))


def dispersion_scan(mix: float) -> DispersionResult:
    """Fit the lowest positive band to E^2 = m^2 + v^2 |k|^2."""
    directions = {
        "y": (1.0, 0.0, 0.0),
        "z": (0.0, 1.0, 0.0),
        "w": (0.0, 0.0, 1.0),
        "yz": (1.0, 1.0, 0.0),
        "yw": (1.0, 0.0, 1.0),
        "zw": (0.0, 1.0, 1.0),
        "diag": (1.0, 1.0, 1.0),
    }
    k_mags = np.linspace(0.05, 0.35, 7)
    records = []
    by_mag = {float(k): [] for k in k_mags}

    for k_mag in k_mags:
        for label, vec in directions.items():
            norm = np.linalg.norm(vec)
            kvec = tuple(k_mag * np.array(vec) / norm)
            e = low_band_energy(kvec, THETA0, mix)
            records.append((k_mag**2, e**2))
            by_mag[float(k_mag)].append(e**2)

    x = np.array([r[0] for r in records], dtype=float)
    y = np.array([r[1] for r in records], dtype=float)
    coeffs = np.polyfit(x, y, 1)
    fit = np.polyval(coeffs, x)
    ss_res = float(np.sum((y - fit) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 1e-30 else 0.0

    direction_cvs = []
    for k_mag, vals in by_mag.items():
        vals = np.array(vals, dtype=float)
        mean = float(np.mean(vals))
        if mean > 1e-30:
            direction_cvs.append(float(np.std(vals) / mean))
    direction_cv = float(np.mean(direction_cvs)) if direction_cvs else 0.0

    mean_abs_resid = float(np.mean(np.abs(y - fit)))
    return DispersionResult(
        mix=mix,
        r2=r2,
        mass2=float(coeffs[1]),
        speed2=float(coeffs[0]),
        direction_cv=direction_cv,
        mean_abs_resid=mean_abs_resid,
    )


# ── Gauge / loop scan ───────────────────────────────────────────────────────
@dataclass
class GaugeResult:
    mix: float
    visibility: float
    r2: float
    mean_return: float
    min_return: float
    max_return: float


def flux_sheet(n: int, phi: float) -> dict:
    """A plaquette flux sheet in the y-links of a square y-z loop."""
    c = n // 2
    ay = np.zeros((n, n, n), dtype=float)
    ay[:, c + 2, c] = phi / 4.0
    return {"ay": ay}


def gauge_scan(mix: float) -> GaugeResult:
    n = 13
    n_layers = 10
    c = n // 2
    radius = 2
    source = (c - radius, c - radius, c)
    target = (c + radius, c + radius, c)
    phi_values = np.linspace(0.0, 2.0 * np.pi, 24, endpoint=False)
    returns = []

    mask = np.zeros((n, n, n), dtype=bool)
    y0, y1 = c - radius, c + radius
    z0, z1 = c - radius, c + radius
    w = c
    for y in range(y0, y1 + 1):
        mask[y, z0, w] = True
        mask[y, z1, w] = True
    for z in range(z0, z1 + 1):
        mask[y0, z, w] = True
        mask[y1, z, w] = True

    for phi in phi_values:
        gauge = flux_sheet(n, phi)
        psi = evolve(
            n,
            n_layers,
            mix,
            STRENGTH,
            gauge=gauge,
            source=source,
        )
        for _ in range(2):
            psi = apply_shift(apply_coin(psi, theta_grid(n), mix), gauge=gauge)
            psi *= mask[None, :, :, :]
        rho = probability_density(psi)
        returns.append(float(rho[target]))

    returns_arr = np.array(returns, dtype=float)
    pmax = float(np.max(returns_arr))
    pmin = float(np.min(returns_arr))
    mean = float(np.mean(returns_arr))
    vis = (pmax - pmin) / (pmax + pmin) if (pmax + pmin) > 1e-30 else 0.0

    cos_p = np.cos(phi_values)
    sin_p = np.sin(phi_values)
    x = np.column_stack([np.ones_like(cos_p), cos_p, sin_p])
    coeffs, _, _, _ = np.linalg.lstsq(x, returns_arr, rcond=None)
    fit = x @ coeffs
    ss_res = float(np.sum((returns_arr - fit) ** 2))
    ss_tot = float(np.sum((returns_arr - mean) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 1e-30 else 0.0

    return GaugeResult(
        mix=mix,
        visibility=vis,
        r2=r2,
        mean_return=mean,
        min_return=pmin,
        max_return=pmax,
    )


def scan_family():
    disp_results = []
    gauge_results = []
    for mix in MIX_VALUES:
        print(f"  mix={mix:.2f}: running dispersion scan...")
        disp_results.append(dispersion_scan(float(mix)))
        print(f"  mix={mix:.2f}: running gauge scan...")
        gauge_results.append(gauge_scan(float(mix)))
    return disp_results, gauge_results


def print_scan_table(disp_results, gauge_results):
    print()
    print("=" * 78)
    print("3+1D COUPLED-COIN SCAN")
    print("=" * 78)
    print(f"  theta0={THETA0}, strength={STRENGTH}, n={N_DEFAULT}, L={L_DEFAULT}")
    print("  mix=0 is the current factorized direct-sum coin; mix=1 is the most")
    print("  strongly cross-coupled unitary in this family.")
    print()
    print(
        f"{'mix':>6} {'KG R^2':>10} {'dir_CV':>10} {'m^2':>10} "
        f"{'gauge V':>10} {'gauge R^2':>10}"
    )
    print("-" * 78)
    for d, g in zip(disp_results, gauge_results):
        print(
            f"{d.mix:6.2f} {d.r2:10.4f} {d.direction_cv:10.4f} {d.mass2:10.4f} "
            f"{g.visibility:10.4f} {g.r2:10.4f}"
        )

    best_kg = max(disp_results, key=lambda r: (r.r2, -r.direction_cv))
    worst_kg = min(disp_results, key=lambda r: (r.r2, -r.direction_cv))
    best_gauge = max(gauge_results, key=lambda r: (r.visibility, r.r2))
    worst_gauge = min(gauge_results, key=lambda r: (r.visibility, r.r2))

    print()
    print("Best/Worst")
    print(
        f"  Best KG fit:    mix={best_kg.mix:.2f}, R^2={best_kg.r2:.4f}, "
        f"dir_CV={best_kg.direction_cv:.4f}, m^2={best_kg.mass2:.4f}"
    )
    print(
        f"  Worst KG fit:   mix={worst_kg.mix:.2f}, R^2={worst_kg.r2:.4f}, "
        f"dir_CV={worst_kg.direction_cv:.4f}, m^2={worst_kg.mass2:.4f}"
    )
    print(
        f"  Best gauge:     mix={best_gauge.mix:.2f}, V={best_gauge.visibility:.4f}, "
        f"R^2={best_gauge.r2:.4f}, target=[{best_gauge.min_return:.6e}, {best_gauge.max_return:.6e}]"
    )
    print(
        f"  Worst gauge:    mix={worst_gauge.mix:.2f}, V={worst_gauge.visibility:.4f}, "
        f"R^2={worst_gauge.r2:.4f}, target=[{worst_gauge.min_return:.6e}, {worst_gauge.max_return:.6e}]"
    )

    kg_gain = best_kg.r2 - worst_kg.r2
    gauge_gain = best_gauge.visibility - worst_gauge.visibility
    print()
    print(f"  KG gain across scan:    {kg_gain:+.4f}")
    print(f"  Gauge gain across scan: {gauge_gain:+.4f}")
    separability_blocker = (best_kg.mix > 0.0 and best_gauge.mix > 0.0)
    print(
        f"  Separability looks like the blocker: "
        f"{'YES' if separability_blocker else 'NOT CLEAR'}"
    )
    return best_kg, worst_kg, best_gauge, worst_gauge


def main():
    t0 = time.time()
    print("FRONTIER: 3+1D COUPLED-COIN SCAN")
    print("=" * 78)
    print("  Interpolate from factorized 2x2⊕2x2⊕2x2 coin to a coupled family.")
    print("  Measure low-k KG/isotropy and a 3D AB/Wilson return signal.")
    print()
    disp_results, gauge_results = scan_family()
    best_kg, worst_kg, best_gauge, worst_gauge = print_scan_table(
        disp_results, gauge_results
    )
    elapsed = time.time() - t0
    print()
    print("=" * 78)
    print("SUMMARY")
    print("=" * 78)
    print(f"  Runtime: {elapsed:.1f}s")
    print(
        f"  Best KG point:    mix={best_kg.mix:.2f} (R^2={best_kg.r2:.4f}, "
        f"dir_CV={best_kg.direction_cv:.4f})"
    )
    print(
        f"  Best gauge point: mix={best_gauge.mix:.2f} (V={best_gauge.visibility:.4f}, "
        f"R^2={best_gauge.r2:.4f})"
    )
    print(
        f"  Worst KG point:   mix={worst_kg.mix:.2f} (R^2={worst_kg.r2:.4f}, "
        f"dir_CV={worst_kg.direction_cv:.4f})"
    )
    print(
        f"  Worst gauge point:mix={worst_gauge.mix:.2f} (V={worst_gauge.visibility:.4f}, "
        f"R^2={worst_gauge.r2:.4f})"
    )


if __name__ == "__main__":
    main()
