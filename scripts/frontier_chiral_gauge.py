#!/usr/bin/env python3
"""Chiral U(1) gauge test.

This harness stays inside the chiral architecture and checks three things:

1. U(1) pure-gauge invariance on a local chiral ring walk.
2. AB-style modulation on a ring geometry when a nontrivial holonomy is
   threaded through the loop.
3. An explicit caveat that SU(2) is *not* claimed here. The model carries a
   single complex U(1) phase per link; it does not have the extra color space
   needed for a non-abelian gauge test.

Dependencies: numpy only.
"""

from __future__ import annotations

import math
import numpy as np


N_SITES = 64
THETA_GAUGE = 0.31
THETA_AB = 0.0
PURE_GAUGE_STEPS = 19
AB_STEPS = N_SITES // 2
SOURCE_SITE = 0
DETECTOR_SITE = N_SITES // 2


def circular_distance(indices: np.ndarray, center: int, size: int) -> np.ndarray:
    raw = np.abs(indices - center)
    return np.minimum(raw, size - raw)


def make_packet(size: int, center: int, width: float) -> np.ndarray:
    sites = np.arange(size, dtype=float)
    dist = circular_distance(sites, center, size)
    envelope = np.exp(-0.5 * (dist / width) ** 2)
    state = np.zeros((size, 2), dtype=np.complex128)
    state[:, 0] = envelope / math.sqrt(2.0)
    state[:, 1] = envelope / math.sqrt(2.0)
    norm = math.sqrt(float(np.sum(np.abs(state) ** 2)))
    if norm > 0.0:
        state /= norm
    return state


def gauge_transform(state: np.ndarray, lam: np.ndarray) -> np.ndarray:
    phase = np.exp(1j * lam)[:, None]
    return phase * state


def coin_step(state: np.ndarray, theta: float) -> np.ndarray:
    c = math.cos(theta)
    s = math.sin(theta)
    out = np.empty_like(state)
    out[:, 0] = c * state[:, 0] - s * state[:, 1]
    out[:, 1] = s * state[:, 0] + c * state[:, 1]
    return out


def shift_step(state: np.ndarray, link_phase: np.ndarray) -> np.ndarray:
    size = state.shape[0]
    out = np.zeros_like(state)
    phase = np.exp(1j * link_phase)
    idx = np.arange(size)
    out[(idx + 1) % size, 0] += phase * state[:, 0]
    out[(idx - 1) % size, 1] += np.conj(np.roll(phase, 1)) * state[:, 1]
    return out


def step(state: np.ndarray, theta: float, link_phase: np.ndarray) -> np.ndarray:
    return shift_step(coin_step(state, theta), link_phase)


def propagate(
    state0: np.ndarray,
    theta: float,
    link_phase: np.ndarray,
    steps: int,
) -> np.ndarray:
    state = np.array(state0, dtype=np.complex128, copy=True)
    for _ in range(steps):
        state = step(state, theta, link_phase)
    return state


def site_probabilities(state: np.ndarray) -> np.ndarray:
    return np.sum(np.abs(state) ** 2, axis=1)


def pure_gauge_test() -> dict[str, float]:
    sites = np.arange(N_SITES, dtype=float)
    lam = (
        0.61 * np.sin(2.0 * np.pi * sites / N_SITES)
        + 0.23 * np.cos(4.0 * np.pi * sites / N_SITES)
        + 0.11 * np.sin(6.0 * np.pi * sites / N_SITES)
    )
    pure_link = np.roll(lam, -1) - lam
    zero_link = np.zeros_like(pure_link)
    psi0 = make_packet(N_SITES, SOURCE_SITE, width=3.2)

    psi_pure = propagate(psi0, THETA_GAUGE, pure_link, PURE_GAUGE_STEPS)
    psi_free = propagate(
        gauge_transform(psi0, lam),
        THETA_GAUGE,
        zero_link,
        PURE_GAUGE_STEPS,
    )
    psi_free_back = gauge_transform(psi_free, -lam)

    p_pure = site_probabilities(psi_pure)
    p_free_back = site_probabilities(psi_free_back)
    return {
        "max_prob_diff": float(np.max(np.abs(p_pure - p_free_back))),
        "rms_prob_diff": float(
            np.sqrt(np.mean((p_pure - p_free_back) ** 2))
        ),
        "pure_wilson_loop": float(np.angle(np.exp(1j * np.sum(pure_link)))),
        "pure_wilson_modulus": float(abs(np.exp(1j * np.sum(pure_link)))),
    }


def ab_sweep() -> dict[str, object]:
    psi0 = np.zeros((N_SITES, 2), dtype=np.complex128)
    psi0[SOURCE_SITE, 0] = 1.0 / math.sqrt(2.0)
    psi0[SOURCE_SITE, 1] = 1.0 / math.sqrt(2.0)

    flux_values = np.linspace(0.0, 2.0 * np.pi, 13)
    detector_probs = []
    for flux in flux_values:
        link = np.full(N_SITES, flux / N_SITES, dtype=float)
        psi = propagate(psi0, THETA_AB, link, AB_STEPS)
        a = psi[DETECTOR_SITE, 0]
        b = psi[DETECTOR_SITE, 1]
        detector_port = (a + b) / math.sqrt(2.0)
        detector_probs.append(float(abs(detector_port) ** 2))

    detector_probs = np.array(detector_probs, dtype=float)
    v = (
        float((np.max(detector_probs) - np.min(detector_probs))
              / (np.max(detector_probs) + np.min(detector_probs)))
        if np.max(detector_probs) + np.min(detector_probs) > 0.0
        else 0.0
    )
    best_idx = int(np.argmax(detector_probs))
    worst_idx = int(np.argmin(detector_probs))
    return {
        "flux_values": flux_values,
        "detector_probs": detector_probs,
        "visibility": v,
        "best_flux": float(flux_values[best_idx]),
        "best_prob": float(detector_probs[best_idx]),
        "worst_flux": float(flux_values[worst_idx]),
        "worst_prob": float(detector_probs[worst_idx]),
        "wilson_loops": np.exp(1j * flux_values),
    }


def report() -> int:
    pure = pure_gauge_test()
    ab = ab_sweep()

    pure_ok = pure["max_prob_diff"] < 1e-12 and abs(pure["pure_wilson_modulus"] - 1.0) < 1e-12
    ab_ok = ab["visibility"] > 0.5

    print("=" * 72)
    print("CHIRAL U(1) GAUGE TEST")
    print("=" * 72)
    print(f"Ring sites: {N_SITES}")
    print(f"Pure-gauge coin angle: {THETA_GAUGE}")
    print(f"AB coin angle: {THETA_AB} (phase-only holonomy limit)")
    print(f"Pure-gauge steps: {PURE_GAUGE_STEPS}")
    print(f"AB steps: {AB_STEPS}")
    print(f"Source site: {SOURCE_SITE}")
    print(f"Detector site: {DETECTOR_SITE}")

    print("\nPure gauge invariance:")
    print(f"  Wilson loop phase:     {pure['pure_wilson_loop']:+.6e} rad")
    print(f"  Wilson loop modulus:   {pure['pure_wilson_modulus']:.6e}")
    print(f"  Max prob difference:   {pure['max_prob_diff']:.3e}")
    print(f"  RMS prob difference:   {pure['rms_prob_diff']:.3e}")
    print(f"  Verdict:               {'PASS' if pure_ok else 'FAIL'}")

    print("\nAB-style ring modulation:")
    for flux, prob in zip(ab["flux_values"], ab["detector_probs"]):
        print(f"  flux={flux:6.3f} -> detector P={prob:.6f}")
    print(f"  visibility:            {ab['visibility']:.6f}")
    print(f"  best flux/prob:        {ab['best_flux']:.3f} / {ab['best_prob']:.6f}")
    print(f"  worst flux/prob:       {ab['worst_flux']:.3f} / {ab['worst_prob']:.6f}")
    print(f"  Verdict:               {'PASS' if ab_ok else 'FAIL'}")

    print("\nSU(2) caveat:")
    print(
        "  Unsupported here. The walk only carries a single U(1) phase per link "
        "and a 2-state chirality degree of freedom; there is no non-abelian color "
        "space, so no SU(2) gauge claim is made."
    )

    overall = pure_ok and ab_ok
    print("\nOverall:", "PASS" if overall else "FAIL")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(report())
