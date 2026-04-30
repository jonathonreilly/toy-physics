#!/usr/bin/env python3
"""
Numba-compiled SU(3) Wilson-loop Monte Carlo for the alpha_s direct route.

This module is intentionally separate from the strict audit gate.  It supplies
compiled gauge-update and Wilson-loop kernels that can produce the certificate
consumed by scripts/frontier_alpha_s_direct_wilson_loop.py once production
statistics exist.

The update is a Cabibbo-Marinari SU(2)-subgroup pseudo-heat-bath with
Kennedy-Pendleton-style SU(2) sampling, followed by deterministic SU(2)
subgroup overrelaxation sweeps.  It never uses the alpha_LM/u0 chain and never
uses the plaquette as a running-coupling input.
"""

from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path
from typing import Any

import numpy as np

try:
    from numba import njit, prange
except ImportError as exc:  # pragma: no cover - exercised only without numba.
    raise SystemExit("numba is required for this production MC backend") from exc


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPO_ROOT / "outputs" / "alpha_s_wilson_loop_production"
DEFAULT_BENCHMARK = OUTPUT_DIR / "numba_heatbath_overrelax_benchmark_2026-04-30.json"
DEFAULT_CERTIFICATE = REPO_ROOT / "outputs" / "alpha_s_direct_wilson_loop_certificate_2026-04-30.json"

NC = 3
NDIM = 4
BETA = 6.0
CF_SU3 = 4.0 / 3.0
HB_PYTHON_US_PER_LINK = 182.5
METROPOLIS_PYTHON_US_PER_LINK = 85.49


def parse_dims(text: str) -> tuple[int, int, int, int]:
    vals = tuple(int(part.strip()) for part in text.split(",") if part.strip())
    if len(vals) != 4 or any(v <= 1 for v in vals):
        raise argparse.ArgumentTypeError("dims must be four comma-separated integers, e.g. 8,8,8,16")
    return vals  # type: ignore[return-value]


def build_neighbors(dims: tuple[int, int, int, int]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    vol = math.prod(dims)
    fwd = np.empty((vol, NDIM), dtype=np.int64)
    bwd = np.empty((vol, NDIM), dtype=np.int64)
    parity = np.empty(vol, dtype=np.int64)
    lx, ly, lz, lt = dims
    for s in range(vol):
        x = s % lx
        y = (s // lx) % ly
        z = (s // (lx * ly)) % lz
        t = (s // (lx * ly * lz)) % lt
        coords = [x, y, z, t]
        parity[s] = (x + y + z + t) & 1
        for mu, length in enumerate(dims):
            cp = coords.copy()
            cm = coords.copy()
            cp[mu] = (cp[mu] + 1) % length
            cm[mu] = (cm[mu] - 1) % length
            fwd[s, mu] = ((cp[3] * lz + cp[2]) * ly + cp[1]) * lx + cp[0]
            bwd[s, mu] = ((cm[3] * lz + cm[2]) * ly + cm[1]) * lx + cm[0]
    return fwd, bwd, parity


def cold_links(dims: tuple[int, int, int, int]) -> np.ndarray:
    vol = math.prod(dims)
    u = np.zeros((vol, NDIM, NC, NC), dtype=np.complex128)
    eye = np.eye(NC, dtype=np.complex128)
    for s in range(vol):
        for mu in range(NDIM):
            u[s, mu] = eye
    return u


@njit(cache=True)
def seed_numba_rng(seed: int) -> None:
    np.random.seed(seed)


@njit(cache=True)
def matmul3(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    c = np.empty((3, 3), dtype=np.complex128)
    for i in range(3):
        for j in range(3):
            z = 0.0 + 0.0j
            for k in range(3):
                z += a[i, k] * b[k, j]
            c[i, j] = z
    return c


@njit(cache=True)
def matmul3_out(a: np.ndarray, b: np.ndarray, out: np.ndarray) -> None:
    for i in range(3):
        for j in range(3):
            z = 0.0 + 0.0j
            for k in range(3):
                z += a[i, k] * b[k, j]
            out[i, j] = z


@njit(cache=True)
def dagger3(a: np.ndarray) -> np.ndarray:
    b = np.empty((3, 3), dtype=np.complex128)
    for i in range(3):
        for j in range(3):
            b[i, j] = np.conj(a[j, i])
    return b


@njit(cache=True)
def dagger3_out(a: np.ndarray, out: np.ndarray) -> None:
    for i in range(3):
        for j in range(3):
            out[i, j] = np.conj(a[j, i])


@njit(cache=True)
def eye3() -> np.ndarray:
    a = np.zeros((3, 3), dtype=np.complex128)
    a[0, 0] = 1.0
    a[1, 1] = 1.0
    a[2, 2] = 1.0
    return a


@njit(cache=True)
def project_su3_rows(m: np.ndarray) -> np.ndarray:
    out = np.empty((3, 3), dtype=np.complex128)

    n0 = 0.0
    for j in range(3):
        n0 += (m[0, j] * np.conj(m[0, j])).real
    n0 = math.sqrt(max(n0, 1.0e-300))
    for j in range(3):
        out[0, j] = m[0, j] / n0

    dot01 = 0.0 + 0.0j
    for j in range(3):
        dot01 += np.conj(out[0, j]) * m[1, j]

    n1 = 0.0
    for j in range(3):
        out[1, j] = m[1, j] - dot01 * out[0, j]
        n1 += (out[1, j] * np.conj(out[1, j])).real
    n1 = math.sqrt(max(n1, 1.0e-300))
    for j in range(3):
        out[1, j] = out[1, j] / n1

    out[2, 0] = np.conj(out[0, 1] * out[1, 2] - out[0, 2] * out[1, 1])
    out[2, 1] = np.conj(out[0, 2] * out[1, 0] - out[0, 0] * out[1, 2])
    out[2, 2] = np.conj(out[0, 0] * out[1, 1] - out[0, 1] * out[1, 0])
    return out


@njit(cache=True)
def project_su2(m: np.ndarray) -> np.ndarray:
    a = 0.5 * (m[0, 0] + np.conj(m[1, 1]))
    b = 0.5 * (m[1, 0] - np.conj(m[0, 1]))
    norm = math.sqrt(max((a * np.conj(a)).real + (b * np.conj(b)).real, 0.0))
    if norm < 1.0e-30:
        out = np.zeros((2, 2), dtype=np.complex128)
        out[0, 0] = 1.0
        out[1, 1] = 1.0
        return out

    a = a / norm
    b = b / norm

    out = np.empty((2, 2), dtype=np.complex128)
    out[0, 0] = a
    out[0, 1] = -np.conj(b)
    out[1, 0] = b
    out[1, 1] = np.conj(a)
    return out


@njit(cache=True)
def su2_quaternion_norm(m: np.ndarray) -> float:
    a = 0.5 * (m[0, 0] + np.conj(m[1, 1]))
    b = 0.5 * (m[1, 0] - np.conj(m[0, 1]))
    return math.sqrt(max((a * np.conj(a)).real + (b * np.conj(b)).real, 0.0))


@njit(cache=True)
def dagger2(a: np.ndarray) -> np.ndarray:
    b = np.empty((2, 2), dtype=np.complex128)
    b[0, 0] = np.conj(a[0, 0])
    b[0, 1] = np.conj(a[1, 0])
    b[1, 0] = np.conj(a[0, 1])
    b[1, 1] = np.conj(a[1, 1])
    return b


@njit(cache=True)
def matmul2(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    c = np.empty((2, 2), dtype=np.complex128)
    c[0, 0] = a[0, 0] * b[0, 0] + a[0, 1] * b[1, 0]
    c[0, 1] = a[0, 0] * b[0, 1] + a[0, 1] * b[1, 1]
    c[1, 0] = a[1, 0] * b[0, 0] + a[1, 1] * b[1, 0]
    c[1, 1] = a[1, 0] * b[0, 1] + a[1, 1] * b[1, 1]
    return c


@njit(cache=True)
def subgroup_indices(subgroup: int) -> tuple[int, int]:
    if subgroup == 0:
        return 0, 1
    if subgroup == 1:
        return 0, 2
    return 1, 2


@njit(cache=True)
def extract_su2_submatrix(m: np.ndarray, subgroup: int) -> np.ndarray:
    i0, i1 = subgroup_indices(subgroup)
    out = np.empty((2, 2), dtype=np.complex128)
    out[0, 0] = m[i0, i0]
    out[0, 1] = m[i0, i1]
    out[1, 0] = m[i1, i0]
    out[1, 1] = m[i1, i1]
    return out


@njit(cache=True)
def left_multiply_subgroup(link: np.ndarray, r: np.ndarray, subgroup: int) -> np.ndarray:
    i0, i1 = subgroup_indices(subgroup)
    out = link.copy()
    for j in range(3):
        a0 = link[i0, j]
        a1 = link[i1, j]
        out[i0, j] = r[0, 0] * a0 + r[0, 1] * a1
        out[i1, j] = r[1, 0] * a0 + r[1, 1] * a1
    return out


@njit(cache=True)
def quaternion_to_su2(a0: float, a1: float, a2: float, a3: float) -> np.ndarray:
    out = np.empty((2, 2), dtype=np.complex128)
    out[0, 0] = a0 + 1j * a3
    out[0, 1] = a2 + 1j * a1
    out[1, 0] = -a2 + 1j * a1
    out[1, 1] = a0 - 1j * a3
    return out


@njit(cache=True)
def random_su2_quaternion_matrix() -> np.ndarray:
    x0 = np.random.normal()
    x1 = np.random.normal()
    x2 = np.random.normal()
    x3 = np.random.normal()
    norm = math.sqrt(max(x0 * x0 + x1 * x1 + x2 * x2 + x3 * x3, 1.0e-300))
    return quaternion_to_su2(x0 / norm, x1 / norm, x2 / norm, x3 / norm)


@njit(cache=True)
def su2_heatbath_matrix(k: float) -> np.ndarray:
    if k < 1.0e-10:
        return random_su2_quaternion_matrix()

    two_k = 2.0 * k
    a0 = 0.99
    for _ in range(10000):
        rr = np.random.random()
        if two_k > 100.0:
            a0_candidate = 1.0 + math.log(max(rr + (1.0 - rr) * math.exp(-2.0 * two_k), 1.0e-300)) / two_k
        else:
            a0_candidate = math.log(rr * math.exp(two_k) + (1.0 - rr) * math.exp(-two_k)) / two_k
        if -1.0 <= a0_candidate <= 1.0:
            if np.random.random() < math.sqrt(max(1.0 - a0_candidate * a0_candidate, 0.0)):
                a0 = a0_candidate
                break

    radius = math.sqrt(max(1.0 - a0 * a0, 0.0))
    phi = 2.0 * math.pi * np.random.random()
    cos_theta = 2.0 * np.random.random() - 1.0
    sin_theta = math.sqrt(max(1.0 - cos_theta * cos_theta, 0.0))
    a1 = radius * sin_theta * math.cos(phi)
    a2 = radius * sin_theta * math.sin(phi)
    a3 = radius * cos_theta
    return quaternion_to_su2(a0, a1, a2, a3)


@njit(cache=True)
def staple_sum(u: np.ndarray, fwd: np.ndarray, bwd: np.ndarray, site: int, mu: int) -> np.ndarray:
    a = np.zeros((3, 3), dtype=np.complex128)
    tmp1 = np.empty((3, 3), dtype=np.complex128)
    tmp2 = np.empty((3, 3), dtype=np.complex128)
    d1 = np.empty((3, 3), dtype=np.complex128)
    d2 = np.empty((3, 3), dtype=np.complex128)
    xp_mu = fwd[site, mu]
    for nu in range(NDIM):
        if nu == mu:
            continue
        xp_nu = fwd[site, nu]
        xm_nu = bwd[site, nu]
        xp_mu_m_nu = bwd[xp_mu, nu]

        dagger3_out(u[xp_nu, mu], d1)
        matmul3_out(u[xp_mu, nu], d1, tmp1)
        dagger3_out(u[site, nu], d2)
        matmul3_out(tmp1, d2, tmp2)
        a += tmp2

        dagger3_out(u[xp_mu_m_nu, nu], d1)
        dagger3_out(u[xm_nu, mu], d2)
        matmul3_out(d1, d2, tmp1)
        matmul3_out(tmp1, u[xm_nu, nu], tmp2)
        a += tmp2
    return a


@njit(cache=True)
def spatial_staple_sum(u: np.ndarray, fwd: np.ndarray, bwd: np.ndarray, site: int, mu: int) -> np.ndarray:
    a = np.zeros((3, 3), dtype=np.complex128)
    tmp1 = np.empty((3, 3), dtype=np.complex128)
    tmp2 = np.empty((3, 3), dtype=np.complex128)
    d1 = np.empty((3, 3), dtype=np.complex128)
    d2 = np.empty((3, 3), dtype=np.complex128)
    xp_mu = fwd[site, mu]
    for nu in range(3):
        if nu == mu:
            continue
        xp_nu = fwd[site, nu]
        xm_nu = bwd[site, nu]
        xp_mu_m_nu = bwd[xp_mu, nu]

        dagger3_out(u[xp_nu, mu], d1)
        matmul3_out(u[xp_mu, nu], d1, tmp1)
        dagger3_out(u[site, nu], d2)
        matmul3_out(tmp1, d2, tmp2)
        a += tmp2

        dagger3_out(u[xp_mu_m_nu, nu], d1)
        dagger3_out(u[xm_nu, mu], d2)
        matmul3_out(d1, d2, tmp1)
        matmul3_out(tmp1, u[xm_nu, nu], tmp2)
        a += tmp2
    return a


@njit(cache=True)
def heatbath_link(u: np.ndarray, fwd: np.ndarray, bwd: np.ndarray, site: int, mu: int, beta: float) -> None:
    a = staple_sum(u, fwd, bwd, site, mu)
    link = u[site, mu].copy()

    for subgroup in range(3):
        w = matmul3(link, a)
        w2 = extract_su2_submatrix(w, subgroup)
        scale = su2_quaternion_norm(w2)
        r_new = su2_heatbath_matrix((beta / 3.0) * scale)

        if scale > 1.0e-15:
            v = project_su2(w2)
            r = matmul2(r_new, dagger2(v))
        else:
            r = r_new
        link = left_multiply_subgroup(link, r, subgroup)

    u[site, mu] = project_su3_rows(link)


@njit(cache=True)
def overrelax_link(u: np.ndarray, fwd: np.ndarray, bwd: np.ndarray, site: int, mu: int) -> None:
    a = staple_sum(u, fwd, bwd, site, mu)
    link = u[site, mu].copy()

    for subgroup in range(3):
        w = matmul3(link, a)
        w2 = extract_su2_submatrix(w, subgroup)
        v = project_su2(w2)
        vdag = dagger2(v)
        r = matmul2(vdag, vdag)
        link = left_multiply_subgroup(link, r, subgroup)

    u[site, mu] = project_su3_rows(link)


@njit(cache=True)
def sweep_heatbath_overrelax(
    u: np.ndarray,
    fwd: np.ndarray,
    bwd: np.ndarray,
    parity: np.ndarray,
    beta: float,
    n_overrelax: int,
) -> None:
    vol = u.shape[0]
    for p in range(2):
        for site in range(vol):
            if parity[site] == p:
                for mu in range(NDIM):
                    heatbath_link(u, fwd, bwd, site, mu, beta)

    for _ in range(n_overrelax):
        for p in range(2):
            for site in range(vol):
                if parity[site] == p:
                    for mu in range(NDIM):
                        overrelax_link(u, fwd, bwd, site, mu)


@njit(cache=True, parallel=True)
def sweep_heatbath_overrelax_parallel(
    u: np.ndarray,
    fwd: np.ndarray,
    bwd: np.ndarray,
    parity: np.ndarray,
    beta: float,
    n_overrelax: int,
) -> None:
    vol = u.shape[0]
    for p in range(2):
        for mu in range(NDIM):
            for site in prange(vol):
                if parity[site] == p:
                    heatbath_link(u, fwd, bwd, site, mu, beta)

    for _ in range(n_overrelax):
        for p in range(2):
            for mu in range(NDIM):
                for site in prange(vol):
                    if parity[site] == p:
                        overrelax_link(u, fwd, bwd, site, mu)


@njit(cache=True)
def plaquette(u: np.ndarray, fwd: np.ndarray) -> float:
    total = 0.0
    count = 0
    vol = u.shape[0]
    for site in range(vol):
        for mu in range(NDIM):
            for nu in range(mu + 1, NDIM):
                xp_mu = fwd[site, mu]
                xp_nu = fwd[site, nu]
                p = matmul3(u[site, mu], u[xp_mu, nu])
                p = matmul3(p, dagger3(u[xp_nu, mu]))
                p = matmul3(p, dagger3(u[site, nu]))
                total += (p[0, 0] + p[1, 1] + p[2, 2]).real / 3.0
                count += 1
    return total / count


@njit(cache=True)
def ape_smear_spatial(u: np.ndarray, fwd: np.ndarray, bwd: np.ndarray, alpha: float, steps: int) -> np.ndarray:
    smeared = u.copy()
    vol = u.shape[0]
    for _ in range(steps):
        nxt = smeared.copy()
        for site in range(vol):
            for mu in range(3):
                staple = spatial_staple_sum(smeared, fwd, bwd, site, mu)
                candidate = (1.0 - alpha) * smeared[site, mu] + (alpha / 4.0) * staple
                nxt[site, mu] = project_su3_rows(candidate)
        smeared = nxt
    return smeared


@njit(cache=True)
def wilson_loop_at(
    u: np.ndarray,
    fwd: np.ndarray,
    bwd: np.ndarray,
    start: int,
    r: int,
    t_extent: int,
    spatial_dir: int,
    time_dir: int,
) -> float:
    w = eye3()
    site = start
    for _ in range(r):
        w = matmul3(w, u[site, spatial_dir])
        site = fwd[site, spatial_dir]
    for _ in range(t_extent):
        w = matmul3(w, u[site, time_dir])
        site = fwd[site, time_dir]
    for _ in range(r):
        site = bwd[site, spatial_dir]
        w = matmul3(w, dagger3(u[site, spatial_dir]))
    for _ in range(t_extent):
        site = bwd[site, time_dir]
        w = matmul3(w, dagger3(u[site, time_dir]))
    return (w[0, 0] + w[1, 1] + w[2, 2]).real / 3.0


@njit(cache=True)
def copy3(src: np.ndarray, dst: np.ndarray) -> None:
    for i in range(3):
        for j in range(3):
            dst[i, j] = src[i, j]


@njit(cache=True)
def set_eye3(out: np.ndarray) -> None:
    for i in range(3):
        for j in range(3):
            out[i, j] = 0.0
    out[0, 0] = 1.0
    out[1, 1] = 1.0
    out[2, 2] = 1.0


@njit(cache=True)
def wilson_loop_at_fast(
    u: np.ndarray,
    fwd: np.ndarray,
    bwd: np.ndarray,
    start: int,
    r: int,
    t_extent: int,
    spatial_dir: int,
    time_dir: int,
) -> float:
    w = np.empty((3, 3), dtype=np.complex128)
    tmp = np.empty((3, 3), dtype=np.complex128)
    d = np.empty((3, 3), dtype=np.complex128)
    set_eye3(w)
    site = start
    for _ in range(r):
        matmul3_out(w, u[site, spatial_dir], tmp)
        copy3(tmp, w)
        site = fwd[site, spatial_dir]
    for _ in range(t_extent):
        matmul3_out(w, u[site, time_dir], tmp)
        copy3(tmp, w)
        site = fwd[site, time_dir]
    for _ in range(r):
        site = bwd[site, spatial_dir]
        dagger3_out(u[site, spatial_dir], d)
        matmul3_out(w, d, tmp)
        copy3(tmp, w)
    for _ in range(t_extent):
        site = bwd[site, time_dir]
        dagger3_out(u[site, time_dir], d)
        matmul3_out(w, d, tmp)
        copy3(tmp, w)
    return (w[0, 0] + w[1, 1] + w[2, 2]).real / 3.0


@njit(cache=True)
def measure_wilson_loops(u: np.ndarray, fwd: np.ndarray, bwd: np.ndarray, max_r: int, max_t: int) -> np.ndarray:
    out = np.zeros((max_r, max_t), dtype=np.float64)
    vol = u.shape[0]
    time_dir = 3
    for r in range(1, max_r + 1):
        for t_extent in range(1, max_t + 1):
            total = 0.0
            count = 0
            for site in range(vol):
                for spatial_dir in range(3):
                    total += wilson_loop_at(u, fwd, bwd, site, r, t_extent, spatial_dir, time_dir)
                    count += 1
            out[r - 1, t_extent - 1] = total / count
    return out


@njit(cache=True, parallel=True)
def measure_wilson_loops_parallel(
    u: np.ndarray,
    fwd: np.ndarray,
    bwd: np.ndarray,
    max_r: int,
    max_t: int,
) -> np.ndarray:
    out = np.zeros((max_r, max_t), dtype=np.float64)
    vol = u.shape[0]
    time_dir = 3
    n_paths = vol * 3
    for r in range(1, max_r + 1):
        for t_extent in range(1, max_t + 1):
            total = 0.0
            for path in prange(n_paths):
                site = path // 3
                spatial_dir = path - 3 * site
                total += wilson_loop_at_fast(u, fwd, bwd, site, r, t_extent, spatial_dir, time_dir)
            out[r - 1, t_extent - 1] = total / n_paths
    return out


def warm_up_numba() -> None:
    dims = (2, 2, 2, 4)
    fwd, bwd, parity = build_neighbors(dims)
    u = cold_links(dims)
    seed_numba_rng(123)
    sweep_heatbath_overrelax(u, fwd, bwd, parity, BETA, 1)
    sweep_heatbath_overrelax_parallel(u, fwd, bwd, parity, BETA, 1)
    _ = plaquette(u, fwd)
    us = ape_smear_spatial(u, fwd, bwd, 0.5, 1)
    _ = measure_wilson_loops(us, fwd, bwd, 1, 1)
    _ = measure_wilson_loops_parallel(us, fwd, bwd, 1, 1)


def run_benchmark(args: argparse.Namespace) -> dict[str, Any]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    dims = args.dims
    fwd, bwd, parity = build_neighbors(dims)
    u = cold_links(dims)
    seed_numba_rng(args.seed)

    print("Compiling numba kernels...")
    warm_up_numba()

    for _ in range(args.warmup_sweeps):
        if args.serial:
            sweep_heatbath_overrelax(u, fwd, bwd, parity, BETA, args.overrelax)
        else:
            sweep_heatbath_overrelax_parallel(u, fwd, bwd, parity, BETA, args.overrelax)

    links_per_sweep = math.prod(dims) * NDIM
    t0 = time.perf_counter()
    plaq_samples = []
    for i in range(args.sweeps):
        if args.serial:
            sweep_heatbath_overrelax(u, fwd, bwd, parity, BETA, args.overrelax)
        else:
            sweep_heatbath_overrelax_parallel(u, fwd, bwd, parity, BETA, args.overrelax)
        if (i + 1) % max(1, args.plaquette_interval) == 0:
            plaq_samples.append(float(plaquette(u, fwd)))
    elapsed = time.perf_counter() - t0
    us_per_link = elapsed / (args.sweeps * links_per_sweep) * 1.0e6
    speedup_vs_heatbath = HB_PYTHON_US_PER_LINK / us_per_link if us_per_link > 0 else float("inf")
    speedup_vs_metropolis = METROPOLIS_PYTHON_US_PER_LINK / us_per_link if us_per_link > 0 else float("inf")

    result = {
        "kind": "numba_compiled_su3_heatbath_overrelax_benchmark",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "dims": list(dims),
        "beta": BETA,
        "sweeps": args.sweeps,
        "warmup_sweeps": args.warmup_sweeps,
        "overrelax_sweeps_per_heatbath": args.overrelax,
        "sweep_kernel": "serial" if args.serial else "checkerboard_parallel",
        "links_per_sweep": links_per_sweep,
        "elapsed_seconds": elapsed,
        "compiled_us_per_link": us_per_link,
        "pure_python_heatbath_reference_us_per_link": HB_PYTHON_US_PER_LINK,
        "pure_python_metropolis_reference_us_per_link": METROPOLIS_PYTHON_US_PER_LINK,
        "speedup_vs_pure_python_heatbath": speedup_vs_heatbath,
        "speedup_vs_pure_python_metropolis": speedup_vs_metropolis,
        "speedup_target": 50.0,
        "speedup_target_pass": speedup_vs_heatbath >= 50.0,
        "plaquette_samples": plaq_samples,
        "production_ready": speedup_vs_heatbath >= 50.0,
        "notes": [
            "Compiled numba @njit kernels update links; orchestration and IO remain Python.",
            "Benchmark compares per-link time against prior pure-Python Cabibbo-Marinari heat-bath reference.",
            "Plaquette samples are diagnostics only, not alpha_s inputs.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps(result, indent=2, sort_keys=True))
    return result


def jackknife_mean_stderr(values: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    n = values.shape[0]
    mean = values.mean(axis=0)
    if n <= 1:
        return mean, np.full_like(mean, np.nan)
    jk = np.empty_like(values)
    total = values.sum(axis=0)
    for i in range(n):
        jk[i] = (total - values[i]) / (n - 1)
    err = np.sqrt((n - 1) * ((jk - jk.mean(axis=0)) ** 2).mean(axis=0))
    return mean, err


def analyze_ensemble(
    dims: tuple[int, int, int, int],
    loops: np.ndarray,
    r0_anchor_fm: float,
) -> dict[str, Any]:
    mean, err = jackknife_mean_stderr(loops)
    wilson_entries = []
    for r in range(mean.shape[0]):
        for t_extent in range(mean.shape[1]):
            wilson_entries.append(
                {
                    "R_over_a": r + 1,
                    "T_over_a": t_extent + 1,
                    "mean": float(mean[r, t_extent]),
                    "stderr": float(err[r, t_extent]) if math.isfinite(float(err[r, t_extent])) else None,
                    "n_cfg": int(loops.shape[0]),
                }
            )

    static_potential = []
    for r in range(mean.shape[0]):
        veffs = []
        for t_extent in range(mean.shape[1] - 1):
            w0 = mean[r, t_extent]
            w1 = mean[r, t_extent + 1]
            if w0 > 0 and w1 > 0:
                veffs.append(math.log(w0 / w1))
        if veffs:
            tail = veffs[-min(3, len(veffs)) :]
            v_mean = float(np.mean(tail))
            v_spread = float(np.std(tail)) if len(tail) > 1 else 0.0
            static_potential.append(
                {
                    "R_over_a": r + 1,
                    "V_lattice": v_mean,
                    "plateau_chi2_dof": min(99.0, (v_spread / max(abs(v_mean), 1.0e-12)) ** 2),
                    "plateau_pass": len(tail) >= 2 and v_spread / max(abs(v_mean), 1.0e-12) <= 0.35,
                    "source": "effective_mass_tail",
                }
            )

    running = []
    r_vals = np.array([p["R_over_a"] for p in static_potential], dtype=float)
    v_vals = np.array([p["V_lattice"] for p in static_potential], dtype=float)
    if len(r_vals) >= 3:
        deriv = np.gradient(v_vals, r_vals)
        force = deriv
        target = 1.65
        rr = r_vals * r_vals * force
        r0_over_a = None
        for i in range(len(rr) - 1):
            if (rr[i] - target) * (rr[i + 1] - target) <= 0:
                frac = (target - rr[i]) / max(rr[i + 1] - rr[i], 1.0e-300)
                r0_over_a = float(r_vals[i] + frac * (r_vals[i + 1] - r_vals[i]))
                break
        if r0_over_a is None:
            r0_over_a = float("nan")
        a_fm = r0_anchor_fm / r0_over_a if math.isfinite(r0_over_a) and r0_over_a > 0 else float("nan")

        for r, force_r in zip(r_vals[: min(4, len(r_vals))], force[: min(4, len(force))]):
            alpha = (r * r / CF_SU3) * force_r
            if alpha > 0 and math.isfinite(alpha) and math.isfinite(a_fm):
                mu_gev = 0.1973269804 / (r * a_fm)
                running.append({"R_over_a": float(r), "mu_GeV": float(mu_gev), "alpha_qq": float(alpha)})
    else:
        r0_over_a = float("nan")
        a_fm = float("nan")

    return {
        "dims": list(dims),
        "wilson_loops": wilson_entries,
        "static_potential": static_potential,
        "running_coupling": running,
        "r0_over_a": r0_over_a,
        "a_fm": a_fm,
    }


def run_ensemble(args: argparse.Namespace) -> dict[str, Any]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    dims = args.dims
    fwd, bwd, parity = build_neighbors(dims)
    loops = []
    therm_done = False
    completed_measurements = 0
    if args.resume_checkpoint and args.checkpoint_npz.exists():
        chk = np.load(args.checkpoint_npz, allow_pickle=False)
        saved_dims = tuple(int(x) for x in chk["dims"].tolist())
        if saved_dims != dims:
            raise ValueError(f"checkpoint dims {saved_dims} do not match requested dims {dims}")
        u = chk["u"]
        therm_done = bool(chk["therm_done"])
        if "loops" in chk:
            loop_array = chk["loops"]
            loops = [loop_array[i].copy() for i in range(loop_array.shape[0])]
            completed_measurements = len(loops)
        print(f"Resumed checkpoint {args.checkpoint_npz}: therm_done={therm_done}, completed={completed_measurements}")
    else:
        u = cold_links(dims)
    seed_numba_rng(args.seed)
    warm_up_numba()

    links_per_sweep = math.prod(dims) * NDIM
    print(f"Running ensemble dims={dims}, beta={BETA}, links/sweep={links_per_sweep}")
    print(f"Thermalization sweeps={args.therm}, measurements={args.measurements}, separation={args.separation}")
    t0 = time.perf_counter()
    if not therm_done:
        for sweep in range(args.therm):
            if args.serial:
                sweep_heatbath_overrelax(u, fwd, bwd, parity, BETA, args.overrelax)
            else:
                sweep_heatbath_overrelax_parallel(u, fwd, bwd, parity, BETA, args.overrelax)
            if (sweep + 1) % max(1, args.progress_interval) == 0:
                print(f"  therm {sweep + 1}/{args.therm}: plaquette={plaquette(u, fwd):.6f}")
        therm_done = True
        write_checkpoint(args.checkpoint_npz, dims, u, np.asarray(loops, dtype=np.float64), therm_done)

    for cfg in range(completed_measurements, args.measurements):
        for _ in range(args.separation):
            if args.serial:
                sweep_heatbath_overrelax(u, fwd, bwd, parity, BETA, args.overrelax)
            else:
                sweep_heatbath_overrelax_parallel(u, fwd, bwd, parity, BETA, args.overrelax)
        measured_u = ape_smear_spatial(u, fwd, bwd, args.ape_alpha, args.ape_steps)
        if args.serial:
            wl = measure_wilson_loops(measured_u, fwd, bwd, args.max_r, args.max_t)
        else:
            wl = measure_wilson_loops_parallel(measured_u, fwd, bwd, args.max_r, args.max_t)
        loops.append(wl)
        if (cfg + 1) % max(1, args.progress_interval) == 0:
            print(f"  cfg {cfg + 1}/{args.measurements}: W11={wl[0, 0]:.6f}, plaquette={plaquette(u, fwd):.6f}")
        if (cfg + 1) % max(1, args.checkpoint_every) == 0:
            write_checkpoint(args.checkpoint_npz, dims, u, np.asarray(loops, dtype=np.float64), therm_done)

    elapsed = time.perf_counter() - t0
    loop_array = np.asarray(loops, dtype=np.float64)
    data = {
        "metadata": {
            "authority": "wilson_loop_static_potential",
            "action": "Cl3Z3_SU3_Wilson",
            "g_bare": 1.0,
            "uses_alpha_lm_chain": False,
            "uses_alpha_bare_over_u0_squared": False,
            "uses_plaquette_as_running_coupling_input": False,
            "update_algorithm": "numba_compiled_cabibbo_marinari_heatbath_plus_su2_subgroup_overrelaxation",
            "ape_smearing": {"steps": args.ape_steps, "alpha": args.ape_alpha},
        },
        "dims": list(dims),
        "beta": BETA,
        "therm_sweeps": args.therm,
        "measurements": args.measurements,
        "separation_sweeps": args.separation,
        "overrelax_sweeps_per_heatbath": args.overrelax,
        "sweep_kernel": "serial" if args.serial else "checkerboard_parallel",
        "elapsed_seconds": elapsed,
        "raw_wilson_loops": loop_array.tolist(),
        "analysis": analyze_ensemble(dims, loop_array, args.r0_anchor_fm),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_checkpoint(args.checkpoint_npz, dims, u, loop_array, therm_done)
    print(f"Wrote ensemble data: {args.output}")
    return data


def write_checkpoint(
    path: Path,
    dims: tuple[int, int, int, int],
    u: np.ndarray,
    loops: np.ndarray,
    therm_done: bool,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp.npz")
    np.savez(
        tmp,
        dims=np.asarray(dims, dtype=np.int64),
        u=u,
        loops=loops,
        therm_done=np.asarray(therm_done),
        saved_at_utc=np.asarray(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())),
    )
    tmp.replace(path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    bench = sub.add_parser("benchmark", help="Benchmark compiled update kernels.")
    bench.add_argument("--dims", type=parse_dims, default=(4, 4, 4, 4))
    bench.add_argument("--sweeps", type=int, default=20)
    bench.add_argument("--warmup-sweeps", type=int, default=2)
    bench.add_argument("--overrelax", type=int, default=4)
    bench.add_argument("--serial", action="store_true", help="Use the serial sweep kernel instead of checkerboard parallel.")
    bench.add_argument("--plaquette-interval", type=int, default=10)
    bench.add_argument("--seed", type=int, default=20260430)
    bench.add_argument("--output", type=Path, default=DEFAULT_BENCHMARK)

    ens = sub.add_parser("ensemble", help="Run one Wilson-loop production/pilot ensemble.")
    ens.add_argument("--dims", type=parse_dims, required=True)
    ens.add_argument("--therm", type=int, default=1000)
    ens.add_argument("--measurements", type=int, default=1000)
    ens.add_argument("--separation", type=int, default=20)
    ens.add_argument("--overrelax", type=int, default=4)
    ens.add_argument("--serial", action="store_true", help="Use the serial sweep kernel instead of checkerboard parallel.")
    ens.add_argument("--ape-steps", type=int, default=5)
    ens.add_argument("--ape-alpha", type=float, default=0.5)
    ens.add_argument("--max-r", type=int, default=8)
    ens.add_argument("--max-t", type=int, default=8)
    ens.add_argument("--r0-anchor-fm", type=float, default=0.5)
    ens.add_argument("--progress-interval", type=int, default=10)
    ens.add_argument("--seed", type=int, default=20260430)
    ens.add_argument("--output", type=Path, default=OUTPUT_DIR / "ensemble.json")
    ens.add_argument("--checkpoint-npz", type=Path, default=OUTPUT_DIR / "ensemble_checkpoint.npz")
    ens.add_argument("--checkpoint-every", type=int, default=10)
    ens.add_argument("--resume-checkpoint", action="store_true")

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.cmd == "benchmark":
        result = run_benchmark(args)
        return 0 if result["speedup_target_pass"] else 2
    if args.cmd == "ensemble":
        run_ensemble(args)
        return 0
    raise AssertionError(args.cmd)


if __name__ == "__main__":
    raise SystemExit(main())
