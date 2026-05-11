#!/usr/bin/env python3
"""3+1D chiral decoherence sweep on the periodic architecture.

This script keeps the 3+1D periodic walk fixed and compares three propagation
modes on the same lattice:

- coherent amplitudes
- fully decohered classical probabilities
- phase-kill after each layer

The point is to test whether the 3+1D gravity-sign windows disappear under
decoherence, or whether they persist in the classicalized walk too.

Dependencies: numpy only.
"""

from __future__ import annotations

import math

import numpy as np


THETA0 = 0.3
STRENGTH = 5e-4
OFFSET = 3
SIZES = (15, 21, 23, 25, 31)
LAYERS = (12, 14, 16, 18, 20, 28)


def make_field(n: int, center: int, mass: tuple[int, int, int]) -> np.ndarray:
    y, z, w = np.meshgrid(
        np.arange(n, dtype=float),
        np.arange(n, dtype=float),
        np.arange(n, dtype=float),
        indexing="ij",
    )
    my, mz, mw = mass
    dy = np.minimum(np.abs(y - my), n - np.abs(y - my))
    dz = np.minimum(np.abs(z - mz), n - np.abs(z - mz))
    dw = np.minimum(np.abs(w - mw), n - np.abs(w - mw))
    r = np.sqrt(dy**2 + dz**2 + dw**2)
    return STRENGTH / (r + 0.1)


def init_amp_state(n: int) -> np.ndarray:
    state = np.zeros((n, n, n, 6), dtype=np.complex128)
    center = n // 2
    state[center, center, center, :] = 1.0 / math.sqrt(6.0)
    return state


def init_prob_state(n: int) -> np.ndarray:
    prob = np.zeros((n, n, n, 6), dtype=float)
    center = n // 2
    prob[center, center, center, :] = 1.0 / 6.0
    return prob


def amp_coin(state: np.ndarray, field: np.ndarray) -> np.ndarray:
    flat = state.reshape(-1, 6)
    theta = THETA0 * (1.0 - field.reshape(-1))
    ct = np.cos(theta)
    st = 1j * np.sin(theta)

    plus, minus = flat[:, 0].copy(), flat[:, 1].copy()
    flat[:, 0] = ct * plus + st * minus
    flat[:, 1] = st * plus + ct * minus

    plus, minus = flat[:, 2].copy(), flat[:, 3].copy()
    flat[:, 2] = ct * plus + st * minus
    flat[:, 3] = st * plus + ct * minus

    plus, minus = flat[:, 4].copy(), flat[:, 5].copy()
    flat[:, 4] = ct * plus + st * minus
    flat[:, 5] = st * plus + ct * minus

    return flat.reshape(state.shape)


def prob_coin(prob: np.ndarray, field: np.ndarray) -> np.ndarray:
    flat = prob.reshape(-1, 6)
    theta = THETA0 * (1.0 - field.reshape(-1))
    c2 = np.cos(theta) ** 2
    s2 = np.sin(theta) ** 2

    plus, minus = flat[:, 0].copy(), flat[:, 1].copy()
    flat[:, 0] = c2 * plus + s2 * minus
    flat[:, 1] = s2 * plus + c2 * minus

    plus, minus = flat[:, 2].copy(), flat[:, 3].copy()
    flat[:, 2] = c2 * plus + s2 * minus
    flat[:, 3] = s2 * plus + c2 * minus

    plus, minus = flat[:, 4].copy(), flat[:, 5].copy()
    flat[:, 4] = c2 * plus + s2 * minus
    flat[:, 5] = s2 * plus + c2 * minus

    return flat.reshape(prob.shape)


def shift(arr: np.ndarray) -> np.ndarray:
    out = np.zeros_like(arr)
    out[:, :, :, 0] = np.roll(arr[:, :, :, 0], 1, axis=0)
    out[:, :, :, 1] = np.roll(arr[:, :, :, 1], -1, axis=0)
    out[:, :, :, 2] = np.roll(arr[:, :, :, 2], 1, axis=1)
    out[:, :, :, 3] = np.roll(arr[:, :, :, 3], -1, axis=1)
    out[:, :, :, 4] = np.roll(arr[:, :, :, 4], 1, axis=2)
    out[:, :, :, 5] = np.roll(arr[:, :, :, 5], -1, axis=2)
    return out


def evolve_amp(n: int, field: np.ndarray, n_layers: int, phase_kill: bool) -> np.ndarray:
    state = init_amp_state(n)
    for _ in range(n_layers):
        state = amp_coin(state, field)
        state = shift(state)
        if phase_kill:
            state = np.abs(state).astype(np.complex128)
    return np.sum(np.abs(state) ** 2, axis=-1)


def evolve_prob(n: int, field: np.ndarray, n_layers: int) -> np.ndarray:
    prob = init_prob_state(n)
    for _ in range(n_layers):
        prob = prob_coin(prob, field)
        prob = shift(prob)
    return np.sum(prob, axis=-1)


def signed_min_image_coords(n: int, center: int) -> np.ndarray:
    coords = np.arange(n, dtype=float) - float(center)
    half = n // 2
    coords[coords > half] -= n
    coords[coords < -half] += n
    return coords


def toward_mass_expectation(prob: np.ndarray, center: int) -> float:
    z_marginal = np.sum(prob, axis=(0, 2))
    total = float(np.sum(z_marginal))
    if total <= 1e-30:
        return 0.0
    signed_z = signed_min_image_coords(prob.shape[1], center)
    return float(np.dot(signed_z, z_marginal) / total)


def run_case(n: int, n_layers: int) -> tuple[float, float, float]:
    center = n // 2
    mass = (center, center + OFFSET, center)
    field0 = np.zeros((n, n, n), dtype=float)
    fieldm = make_field(n, center, mass)

    p0_coh = evolve_amp(n, field0, n_layers, phase_kill=False)
    pm_coh = evolve_amp(n, fieldm, n_layers, phase_kill=False)
    coherent = toward_mass_expectation(pm_coh, center) - toward_mass_expectation(p0_coh, center)

    p0_cl = evolve_prob(n, field0, n_layers)
    pm_cl = evolve_prob(n, fieldm, n_layers)
    classical = toward_mass_expectation(pm_cl, center) - toward_mass_expectation(p0_cl, center)

    p0_pk = evolve_amp(n, field0, n_layers, phase_kill=True)
    pm_pk = evolve_amp(n, fieldm, n_layers, phase_kill=True)
    phase_kill = toward_mass_expectation(pm_pk, center) - toward_mass_expectation(p0_pk, center)

    return coherent, classical, phase_kill


def verdict(delta: float) -> str:
    return "TOWARD" if delta > 0.0 else "AWAY"


def main() -> None:
    print("=" * 78)
    print("FRONTIER: 3+1D CHIRAL DECOHERENCE SWEEP")
    print("=" * 78)
    print(
        "Same periodic 3+1D architecture for coherent, classical, and phase-kill modes."
    )
    print(f"theta0={THETA0}, strength={STRENGTH}, mass offset={OFFSET}")
    print()

    print(
        f"{'n':>4s} {'L':>4s} {'coherent':>12s} {'dir':>7s} "
        f"{'classical':>12s} {'dir':>7s} {'phase_kill':>12s} {'dir':>7s}"
    )
    print(
        f"{'-' * 4:>4s} {'-' * 4:>4s} {'-' * 12:>12s} {'-' * 7:>7s} "
        f"{'-' * 12:>12s} {'-' * 7:>7s} {'-' * 12:>12s} {'-' * 7:>7s}"
    )

    all_rows: list[tuple[int, int, float, float, float]] = []
    for n in SIZES:
        for n_layers in LAYERS:
            coherent, classical, phase_kill = run_case(n, n_layers)
            all_rows.append((n, n_layers, coherent, classical, phase_kill))
            print(
                f"{n:4d} {n_layers:4d} "
                f"{coherent:+12.6e} {verdict(coherent):>7s} "
                f"{classical:+12.6e} {verdict(classical):>7s} "
                f"{phase_kill:+12.6e} {verdict(phase_kill):>7s}"
            )
        print()

    coherent_away = [(n, l) for n, l, c, _, _ in all_rows if c <= 0.0]
    classical_away = [(n, l) for n, l, _, c, _ in all_rows if c <= 0.0]
    phase_kill_away = [(n, l) for n, l, _, _, p in all_rows if p <= 0.0]

    print("=" * 78)
    print("SUMMARY")
    print("=" * 78)
    print(f"coherent AWAY windows: {coherent_away or 'none'}")
    print(f"classical AWAY windows: {classical_away or 'none'}")
    print(f"phase-kill AWAY windows: {phase_kill_away or 'none'}")
    print()
    print(
        "Interpretation: if AWAY windows remain in the classical and phase-kill "
        "columns, decoherence does not remove the 3+1D sign problem on this "
        "periodic architecture."
    )

    # Explicit AWAY-window assertions tied to docs/CHIRAL_3PLUS1D_RECURRENCE_NOTE.md.
    # These are the bounded-table values for theta0=0.3, strength=5e-4, offset=3,
    # n in {15,21,23,25,31}, L in {12,14,16,18,20,28}. Any change in the sweep
    # that perturbs these sets will trip an assert and force the note table to
    # be re-synced.
    expected_coherent_away = {
        (15, 16), (15, 18), (15, 20),
        (21, 12), (21, 28),
        (23, 12), (23, 28),
        (25, 14), (25, 28),
        (31, 16), (31, 20),
    }
    expected_classical_away = {
        (15, 14), (15, 16), (15, 18),
        (21, 12), (21, 18), (21, 20),
        (23, 12), (23, 18), (23, 20), (23, 28),
        (25, 20), (25, 28),
        (31, 28),
    }
    coherent_set = set(coherent_away)
    classical_set = set(classical_away)
    phase_kill_set = set(phase_kill_away)

    assert coherent_set == expected_coherent_away, (
        "coherent AWAY windows drifted from the bounded note table:\n"
        f"  unexpected: {sorted(coherent_set - expected_coherent_away)}\n"
        f"  missing:    {sorted(expected_coherent_away - coherent_set)}"
    )
    assert classical_set == expected_classical_away, (
        "classical AWAY windows drifted from the bounded note table:\n"
        f"  unexpected: {sorted(classical_set - expected_classical_away)}\n"
        f"  missing:    {sorted(expected_classical_away - classical_set)}"
    )
    assert phase_kill_set == expected_classical_away, (
        "phase-kill AWAY windows drifted from the bounded note table "
        "(expected to match classical column):\n"
        f"  unexpected: {sorted(phase_kill_set - expected_classical_away)}\n"
        f"  missing:    {sorted(expected_classical_away - phase_kill_set)}"
    )
    print(
        "PASS: coherent, classical, and phase-kill AWAY-window sets match the "
        "bounded note table."
    )


if __name__ == "__main__":
    main()
