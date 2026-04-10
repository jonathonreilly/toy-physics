#!/usr/bin/env python3
"""4-Component Dirac Walk v4 - larger-lattice convergence attack.

This probe keeps the reversed gravity coupling that gave TOWARD in v2/v3:

    m(r) = m0 * (1 + f(r))

and attacks the remaining failures on larger lattices:

1. Gravity monotonicity over N
2. Distance law over offset
3. Closure improvement as n grows
4. Periodic vs one non-periodic boundary comparison where feasible

The non-periodic boundary here is open/absorbing. That makes it a diagnostic
boundary for the sign windows, not a closure test, because norm is not
conserved there.
"""

from __future__ import annotations

import argparse
import math
import time

import numpy as np
from scipy import stats


gamma0 = np.array(
    [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, -1, 0],
        [0, 0, 0, -1],
    ],
    dtype=complex,
)

gamma1 = np.array(
    [
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [0, -1, 0, 0],
        [-1, 0, 0, 0],
    ],
    dtype=complex,
)

gamma2 = np.array(
    [
        [0, 0, 0, -1j],
        [0, 0, 1j, 0],
        [0, 1j, 0, 0],
        [-1j, 0, 0, 0],
    ],
    dtype=complex,
)

gamma3 = np.array(
    [
        [0, 0, 1, 0],
        [0, 0, 0, -1],
        [-1, 0, 0, 0],
        [0, 1, 0, 0],
    ],
    dtype=complex,
)

GAMMAS = [gamma0, gamma1, gamma2, gamma3]


def projectors(gp: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    evals, evecs = np.linalg.eigh(gp)
    p_plus = sum(
        np.outer(evecs[:, i], evecs[:, i].conj())
        for i in range(4)
        if evals[i] > 0
    )
    p_minus = sum(
        np.outer(evecs[:, i], evecs[:, i].conj())
        for i in range(4)
        if evals[i] < 0
    )
    return p_plus, p_minus


PX_P, PX_M = projectors(gamma0 @ gamma1)
PY_P, PY_M = projectors(gamma0 @ gamma2)
PZ_P, PZ_M = projectors(gamma0 @ gamma3)


def dirac_coin_step(psi: np.ndarray, mass_field: np.ndarray) -> np.ndarray:
    cm = np.cos(mass_field)
    sm = np.sin(mass_field)
    out = np.zeros_like(psi)
    out[0] = (cm + 1j * sm) * psi[0]
    out[1] = (cm + 1j * sm) * psi[1]
    out[2] = (cm - 1j * sm) * psi[2]
    out[3] = (cm - 1j * sm) * psi[3]
    return out


def _shift_piece(piece: np.ndarray, axis: int, direction: int, boundary: str) -> np.ndarray:
    if boundary == "periodic":
        return np.roll(piece, -1 if direction > 0 else 1, axis=axis)

    out = np.zeros_like(piece)
    src = [slice(None)] * 3
    dst = [slice(None)] * 3
    if direction > 0:
        src[axis] = slice(0, -1)
        dst[axis] = slice(1, None)
    else:
        src[axis] = slice(1, None)
        dst[axis] = slice(0, -1)
    out[tuple(dst)] = piece[tuple(src)]
    return out


def shift_dir(psi: np.ndarray, axis: int, boundary: str) -> np.ndarray:
    out = np.zeros_like(psi)
    if axis == 0:
        p_plus, p_minus = PX_P, PX_M
    elif axis == 1:
        p_plus, p_minus = PY_P, PY_M
    elif axis == 2:
        p_plus, p_minus = PZ_P, PZ_M
    else:
        raise ValueError(f"invalid axis: {axis}")

    for c in range(4):
        pp = sum(p_plus[c, d] * psi[d] for d in range(4))
        pm = sum(p_minus[c, d] * psi[d] for d in range(4))
        out[c] += _shift_piece(pp, axis, +1, boundary)
        out[c] += _shift_piece(pm, axis, -1, boundary)
    return out


def step_dirac(psi: np.ndarray, mass_field: np.ndarray, boundary: str) -> np.ndarray:
    psi = dirac_coin_step(psi, mass_field)
    psi = shift_dir(psi, 0, boundary)
    psi = shift_dir(psi, 1, boundary)
    psi = shift_dir(psi, 2, boundary)
    return psi


def min_image_dist(n: int, mass_pos: tuple[int, int, int]) -> np.ndarray:
    c = np.arange(n)
    dx = np.abs(c[:, None, None] - mass_pos[0])
    dx = np.minimum(dx, n - dx)
    dy = np.abs(c[None, :, None] - mass_pos[1])
    dy = np.minimum(dy, n - dy)
    dz = np.abs(c[None, None, :] - mass_pos[2])
    dz = np.minimum(dz, n - dz)
    return np.sqrt(dx**2 + dy**2 + dz**2)


def direct_dist(n: int, mass_pos: tuple[int, int, int]) -> np.ndarray:
    c = np.arange(n)
    dx = np.abs(c[:, None, None] - mass_pos[0])
    dy = np.abs(c[None, :, None] - mass_pos[1])
    dz = np.abs(c[None, None, :] - mass_pos[2])
    return np.sqrt(dx**2 + dy**2 + dz**2)


def make_mass_field(
    n: int,
    mass0: float,
    strength: float,
    mass_positions: list[tuple[int, int, int]] | None,
    boundary: str,
) -> np.ndarray:
    mf = np.full((n, n, n), mass0, dtype=float)
    if not mass_positions or strength <= 0:
        return mf

    total_f = np.zeros((n, n, n), dtype=float)
    for mp in mass_positions:
        r = min_image_dist(n, mp) if boundary == "periodic" else direct_dist(n, mp)
        total_f += strength / (r + 0.1)
    return mass0 * (1.0 + total_f)


def evolve(
    n: int,
    n_layers: int,
    mass0: float,
    strength: float = 0.0,
    mass_positions: list[tuple[int, int, int]] | None = None,
    boundary: str = "periodic",
) -> np.ndarray:
    psi = np.zeros((4, n, n, n), dtype=np.complex128)
    c = n // 2
    for k in range(4):
        psi[k, c, c, c] = 0.5
    mf = make_mass_field(n, mass0, strength, mass_positions, boundary)
    for _ in range(n_layers):
        psi = step_dirac(psi, mf, boundary)
    return psi


def density(psi: np.ndarray) -> tuple[np.ndarray, float]:
    rho = np.sum(np.abs(psi) ** 2, axis=0)
    total = float(np.sum(rho))
    if total > 1e-30:
        rho = rho / total
    return rho, total


def readout_bias(rho_field: np.ndarray, rho_free: np.ndarray, n: int, offset: int) -> tuple[float, float, float]:
    c = n // 2
    toward = float(np.sum(rho_field[c, c, c + 1 : c + offset + 1] - rho_free[c, c, c + 1 : c + offset + 1]))
    away = float(np.sum(rho_field[c, c, c - offset : c] - rho_free[c, c, c - offset : c]))
    return toward, away, toward - away


def run_bias_case(
    boundary: str,
    n: int,
    n_layers: int,
    mass0: float,
    strength: float,
    offset: int,
) -> dict[str, float]:
    c = n // 2
    rho_free, norm_free = density(evolve(n, n_layers, mass0, 0.0, None, boundary))
    rho_field, norm_field = density(
        evolve(n, n_layers, mass0, strength, [(c, c, c + offset)], boundary)
    )
    toward, away, bias = readout_bias(rho_field, rho_free, n, offset)
    return {
        "toward": toward,
        "away": away,
        "bias": bias,
        "norm_free": norm_free,
        "norm_field": norm_field,
    }


def fit_power_law(offsets: list[int], biases: list[float]) -> tuple[float, float]:
    arr = np.array(biases, dtype=float)
    signs = np.sign(arr)
    if not (np.all(signs == signs[0]) and signs[0] != 0):
        return float("nan"), 0.0
    x = np.log10(np.array(offsets, dtype=float))
    y = np.log10(np.abs(arr))
    coeffs = np.polyfit(x, y, 1)
    pred = np.polyval(coeffs, x)
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return float(coeffs[0]), r2


def closure_card(n: int, n_layers: int, mass0: float, boundary: str = "periodic") -> tuple[int, dict[str, object]]:
    if boundary != "periodic":
        raise ValueError("closure_card is only meaningful on the periodic unitary walk")

    c = n // 2
    strength = 5e-4
    score = 0
    slits = [c - 2, c, c + 2]
    barrier_layer = max(2, n_layers // 2 - 1)

    def ev_barrier(open_slits: list[int], noise: float = 0.0) -> np.ndarray:
        psi = np.zeros((4, n, n, n), dtype=np.complex128)
        for k in range(4):
            psi[k, c, c, c] = 0.5
        mf = np.full((n, n, n), mass0, dtype=float)
        rng = np.random.default_rng(42) if noise > 0 else None
        for layer in range(n_layers):
            if noise > 0:
                ph = rng.uniform(-noise, noise, (n, n, n))
                psi = psi * np.exp(1j * ph)[None, :, :, :]
            psi = step_dirac(psi, mf, boundary)
            if layer == barrier_layer:
                mask = np.zeros((n, n, n), dtype=bool)
                for sy in open_slits:
                    mask[sy, :, :] = True
                psi *= mask[None, :, :, :]
        return density(psi)[0]

    rf = ev_barrier(slits)
    rs = [ev_barrier([s]) for s in slits]
    pt = float(np.sum(rf))
    born = float(np.sum(np.abs(rf - sum(rs))) / pt) if pt > 1e-30 else float("inf")
    p1 = born > 0.01
    score += int(p1)

    ru = ev_barrier([c - 2])
    rd = ev_barrier([c + 2])
    pu = ru / np.sum(ru)
    pd = rd / np.sum(rd)
    dtv = 0.5 * float(np.sum(np.abs(pu - pd)))
    p2 = dtv > 0.01
    score += int(p2)

    r0 = density(evolve(n, n_layers, mass0, 0.0, None, boundary))[0]
    pz = float(np.sum(r0[c, c, c + 1 : c + 4]))
    mz = float(np.sum(r0[c, c, c - 3 : c]))
    bias = abs(pz - mz) / (pz + mz) if (pz + mz) > 0 else 0.0
    p3 = bias < 0.01
    score += int(p3)

    strengths = [1e-4, 2e-4, 5e-4, 1e-3, 2e-3]
    forces = []
    r0 = density(evolve(n, n_layers, mass0, 0.0, None, boundary))[0]
    for s in strengths:
        r1 = density(evolve(n, n_layers, mass0, s, [(c, c, c + 3)], boundary))[0]
        d = r1 - r0
        forces.append(float(np.sum(d[c, c, c + 1 : c + 4]) - np.sum(d[c, c, c - 3 : c])))
    fa = np.array(forces, dtype=float)
    sa = np.array(strengths, dtype=float)
    co = np.polyfit(sa, fa, 1)
    pred = np.polyval(co, sa)
    ss_r = float(np.sum((fa - pred) ** 2))
    ss_t = float(np.sum((fa - np.mean(fa)) ** 2))
    r2fm = 1.0 - ss_r / ss_t if ss_t > 0 else 0.0
    p4 = r2fm > 0.9
    score += int(p4)

    r0 = density(evolve(n, n_layers, mass0, 0.0, None, boundary))[0]
    r1 = density(evolve(n, n_layers, mass0, strength, [(c, c, c + 3)], boundary))[0]
    d = r1 - r0
    tw = float(np.sum(d[c, c, c + 1 : c + 4]))
    aw = float(np.sum(d[c, c, c - 3 : c]))
    p5 = tw > aw
    score += int(p5)

    rn = ev_barrier(slits, noise=0.5)
    pn = float(np.sum(rn))
    bn = float(np.sum(np.abs(rn - sum(rs))) / pn) if pn > 1e-30 else float("inf")
    p6 = bn < born
    score += int(p6)

    pg = density(evolve(n, n_layers, mass0, strength, [(c, c, c)], boundary))[0]
    pn = pg / np.sum(pg)
    px = np.sum(pn, axis=(1, 2))
    py = np.sum(pn, axis=(0, 2))
    pxy = np.sum(pn, axis=2)
    mi = 0.0
    for ix in range(n):
        for iy in range(n):
            if pxy[ix, iy] > 1e-30 and px[ix] > 1e-30 and py[iy] > 1e-30:
                mi += pxy[ix, iy] * np.log(pxy[ix, iy] / (px[ix] * py[iy]))
    p7 = mi > 0
    score += int(p7)

    purs = {}
    for L in [max(6, n_layers - 4), n_layers - 2, n_layers]:
        if L < 4:
            continue
        rr = density(evolve(n, L, mass0, strength, [(c, c, c)], boundary))[0]
        purs[L] = float(np.sum(rr**2) / np.sum(rr) ** 2)
    vals = list(purs.values())
    cv = float(np.std(vals) / np.mean(vals)) if np.mean(vals) > 0 else 0.0
    p8 = cv < 0.5
    score += int(p8)

    gf = {}
    for L in [max(6, n_layers - 4), n_layers - 2, n_layers]:
        r0 = density(evolve(n, L, mass0, 0.0, None, boundary))[0]
        r1 = density(evolve(n, L, mass0, strength, [(c, c, c + 3)], boundary))[0]
        d = r1 - r0
        gf[L] = float(np.sum(d[c, c, c + 1 : c + 4]) - np.sum(d[c, c, c - 3 : c]))
    vg = list(gf.values())
    abs_vg = [abs(v) for v in vg]
    mono = all(abs_vg[i] <= abs_vg[i + 1] for i in range(len(abs_vg) - 1))
    p9 = mono
    score += int(p9)

    offsets = list(range(2, min(5, n // 4) + 1))
    fdl = []
    r0 = density(evolve(n, n_layers, mass0, 0.0, None, boundary))[0]
    for dz in offsets:
        r1 = density(evolve(n, n_layers, mass0, strength, [(c, c, c + dz)], boundary))[0]
        d = r1 - r0
        fdl.append(float(np.sum(d[c, c, c + 1 : c + dz + 1]) - np.sum(d[c, c, c - dz : c])))
    fa = np.array(fdl, dtype=float)
    oa = np.array(offsets, dtype=float)
    valid = np.abs(fa) > 1e-30
    if np.sum(valid) >= 3:
        lr = np.log(oa[valid])
        lf = np.log(np.abs(fa[valid]))
        cf = np.polyfit(lr, lf, 1)
        pf = np.polyval(cf, lr)
        sr = float(np.sum((lf - pf) ** 2))
        st = float(np.sum((lf - np.mean(lf)) ** 2))
        r2dl = 1.0 - sr / st if st > 0 else 0.0
    else:
        r2dl = 0.0
    p10 = r2dl > 0.7
    score += int(p10)

    return score, {
        "born": born,
        "dtv": dtv,
        "f0_bias": bias,
        "fm_r2": r2fm,
        "gravity_bias": tw - aw,
        "decoh": bn,
        "mi": mi,
        "purity_cv": cv,
        "grav_growth": mono,
        "dist_r2": r2dl,
        "results": [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10],
    }


def sweep_monotonicity(boundary: str, n: int, n_layers_values: list[int], mass0: float, offset: int) -> list[tuple[int, float, float, float]]:
    rows = []
    for L in n_layers_values:
        if L >= n - 3:
            continue
        res = run_bias_case(boundary, n, L, mass0, 5e-4, offset)
        rows.append((L, res["toward"], res["away"], res["bias"]))
    return rows


def sweep_distance(boundary: str, n: int, n_layers: int, mass0: float, offsets: list[int]) -> list[tuple[int, float, float, float]]:
    rows = []
    for off in offsets:
        res = run_bias_case(boundary, n, n_layers, mass0, 5e-4, off)
        rows.append((off, res["toward"], res["away"], res["bias"]))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mass0", type=float, default=0.30)
    parser.add_argument("--strength", type=float, default=5e-4)
    args = parser.parse_args()

    mass0 = args.mass0
    strength = args.strength
    start = time.time()

    print("=" * 78)
    print("FRONTIER: 4-COMPONENT DIRAC WALK v4 - LARGE-LATTICE CONVERGENCE")
    print("=" * 78)
    print(f"reversed coupling: m(r) = m0 * (1 + f(r))")
    print(f"mass0={mass0:.3f}, strength={strength:.1e}")
    print()

    # Baseline periodic closure mass stays fixed for the larger-lattice attack.
    baseline_n = 17
    baseline_layers = 12
    print("BASELINE PERIODIC CLOSURE MASS CHECK")
    baseline_score, baseline_info = closure_card(baseline_n, baseline_layers, mass0, boundary="periodic")
    print(f"  n={baseline_n}, N={baseline_layers}: score={baseline_score}/10, gravity_bias={baseline_info['gravity_bias']:+.4e}")
    print(f"  rows: {''.join('P' if x else 'F' for x in baseline_info['results'])}")
    print()

    print("LARGER-LATTICE PERIODIC CLOSURE SWEEP")
    closure_rows = []
    for n in (17, 21, 25, 29):
        layers = 12
        score, info = closure_card(n, layers, mass0, boundary="periodic")
        closure_rows.append((n, layers, score, info["gravity_bias"], info["dist_r2"]))
        print(
            f"  n={n:2d}, N={layers:2d}: score={score}/10, "
            f"gravity_bias={info['gravity_bias']:+.4e}, dist_R2={info['dist_r2']:.4f}"
        )
    print()

    print("MONOTONICITY OVER N (offset=3)")
    mono_ns = 29
    N_values = [8, 10, 12, 14, 16, 18, 20, 22, 24]
    for boundary in ("periodic", "open"):
        rows = sweep_monotonicity(boundary, mono_ns, N_values, mass0, offset=3)
        biases = [row[3] for row in rows]
        mono = all(biases[i] <= biases[i + 1] for i in range(len(biases) - 1)) and all(b > 0 for b in biases)
        print(f"\n  [{boundary}] n={mono_ns}")
        for L, toward, away, bias in rows:
            tag = "TOWARD" if bias > 0 else "AWAY"
            print(f"    N={L:2d}: toward={toward:+.4e}, away={away:+.4e}, bias={bias:+.4e} -> {tag}")
        print(f"    monotone increasing TOWARD bias: {'YES' if mono else 'NO'}")

    print("\nDISTANCE LAW OVER OFFSET")
    dist_ns = 29
    dist_layers = 16
    offsets = [2, 3, 4, 5, 6]
    for boundary in ("periodic", "open"):
        rows = sweep_distance(boundary, dist_ns, dist_layers, mass0, offsets)
        biases = [row[3] for row in rows]
        toward_count = sum(1 for b in biases if b > 0)
        alpha, r2 = fit_power_law(offsets, biases)
        print(f"\n  [{boundary}] n={dist_ns}, N={dist_layers}")
        for off, toward, away, bias in rows:
            tag = "TOWARD" if bias > 0 else "AWAY"
            print(f"    off={off}: toward={toward:+.4e}, away={away:+.4e}, bias={bias:+.4e} -> {tag}")
        print(f"    TOWARD count: {toward_count}/{len(offsets)}")
        if np.isnan(alpha):
            print("    power-law fit: not available (sign mix or zero values)")
        else:
            print(f"    power-law fit: alpha={alpha:.3f}, R^2={r2:.4f}")

    print("\nSUMMARY")
    best_closure = max(closure_rows, key=lambda row: row[2])
    print(
        f"  best periodic closure: n={best_closure[0]}, N={best_closure[1]}, "
        f"score={best_closure[2]}/10, gravity_bias={best_closure[3]:+.4e}"
    )
    print(f"  runtime: {time.time() - start:.1f}s")


if __name__ == "__main__":
    main()
