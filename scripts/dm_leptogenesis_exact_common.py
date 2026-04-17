#!/usr/bin/env python3
"""
Shared exact-source helpers for refreshed DM leptogenesis runners.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable

import numpy as np
from scipy import integrate, special

PI = math.pi
ZETA_3 = 1.2020569031595942

PLAQ_MC = 0.5934
u0 = PLAQ_MC ** 0.25
g_bare = 1.0
alpha_bare = g_bare**2 / (4.0 * PI)
ALPHA_LM = alpha_bare / u0

M_PL = 1.2209e19
C_APBC = (7.0 / 8.0) ** 0.25
V_EW = M_PL * C_APBC * ALPHA_LM**16

G_WEAK = 0.653
Y0 = G_WEAK**2 / 64.0
Y0_SQ = Y0**2

G_STAR_EXACT = 28.0 + (7.0 / 8.0) * 90.0
C_SPH = 28.0 / 79.0
ETA_OBS = 6.12e-10

D_THERMAL_EXACT = 135.0 * ZETA_3 / (4.0 * PI**4 * G_STAR_EXACT)
G_S_TODAY_EXACT = 2.0 + (7.0 / 8.0) * 6.0 * (4.0 / 11.0)
S_OVER_NGAMMA_EXACT = (PI**4 / (45.0 * ZETA_3)) * G_S_TODAY_EXACT
H_RAD_COEFFICIENT_EXACT = math.sqrt(4.0 * PI**3 * G_STAR_EXACT / 45.0) / M_PL

D_THERMAL_BENCH_LEGACY = D_THERMAL_EXACT
S_OVER_NGAMMA_BENCH_LEGACY = 7.04


def g_self_energy(x: float) -> float:
    return math.sqrt(x) / (x - 1.0)


def f_vertex(x: float) -> float:
    if abs(x - 1.0) < 1e-6:
        return 0.5
    return math.sqrt(x) * (1.0 - (1.0 + x) * math.log((1.0 + x) / x))


def f_total(x: float) -> float:
    return g_self_energy(x) + f_vertex(x)


def kappa_fit(k_decay: float) -> float:
    return (0.3 / k_decay) * (math.log(k_decay)) ** 0.6


def n_eq_gamma_over_t3_exact() -> float:
    return 2.0 * ZETA_3 / PI**2


def n_eq_majorana_over_t3_exact() -> float:
    return 3.0 * ZETA_3 / (2.0 * PI**2)


def s_over_t3_relativistic(g_star_s: float) -> float:
    return (2.0 * PI**2 / 45.0) * g_star_s


@dataclass(frozen=True)
class ExactLeptogenesisPackage:
    k_A: int
    k_B: int
    eps_over_B: float
    M1: float
    M2: float
    M3: float
    gamma: float
    E1: float
    E2: float
    cp1: float
    cp2: float
    K00: float
    epsilon_1: float
    epsilon_DI: float
    epsilon_ratio: float
    h_rad_over_t2_exact: float
    m_tilde_exact_eV: float
    m_star_exact_eV: float
    k_decay_exact: float
    m_star_bench_eV: float
    k_decay_bench: float
    kappa_fit_bench: float
    eta_ratio_fit_bench_legacy: float
    eta_ratio_fit_bench_exact_bookkeeping: float


def exact_package() -> ExactLeptogenesisPackage:
    k_A = 7
    k_B = 8
    a_mr = M_PL * ALPHA_LM**k_A
    b_mr = M_PL * ALPHA_LM**k_B
    eps_over_B = ALPHA_LM / 2.0

    m1 = b_mr * (1.0 - eps_over_B)
    m2 = b_mr * (1.0 + eps_over_B)
    m3 = a_mr

    gamma = 0.5
    e1 = math.sqrt(8.0 / 3.0)
    e2 = math.sqrt(8.0) / 3.0
    cp1 = -2.0 * gamma * e1 / 3.0
    cp2 = 2.0 * gamma * e2 / 3.0
    k00 = 2.0

    x23 = (m2 / m1) ** 2
    x3 = (m3 / m1) ** 2
    epsilon_1 = abs((1.0 / (8.0 * PI)) * Y0_SQ * (cp1 * f_total(x23) + cp2 * f_total(x3)) / k00)

    m3_gev = Y0_SQ * V_EW**2 / m1
    epsilon_di = (3.0 / (16.0 * PI)) * m1 * m3_gev / V_EW**2
    epsilon_ratio = epsilon_1 / epsilon_di

    h_rad_over_t2_exact = H_RAD_COEFFICIENT_EXACT
    m_tilde_exact_eV = k00 * Y0_SQ * V_EW**2 / m1 * 1e9
    m_star_exact_eV = 8.0 * PI * V_EW**2 * h_rad_over_t2_exact * 1e9
    k_decay_exact = m_tilde_exact_eV / m_star_exact_eV
    m_star_bench_eV = m_star_exact_eV
    k_decay_bench = k_decay_exact
    kappa_fit_bench = kappa_fit(k_decay_exact)

    eta_ratio_fit_bench_legacy = (
        S_OVER_NGAMMA_BENCH_LEGACY
        * C_SPH
        * D_THERMAL_BENCH_LEGACY
        * epsilon_1
        * kappa_fit_bench
        / ETA_OBS
    )
    eta_ratio_fit_bench_exact_bookkeeping = (
        S_OVER_NGAMMA_EXACT
        * C_SPH
        * D_THERMAL_EXACT
        * epsilon_1
        * kappa_fit_bench
        / ETA_OBS
    )

    return ExactLeptogenesisPackage(
        k_A=k_A,
        k_B=k_B,
        eps_over_B=eps_over_B,
        M1=m1,
        M2=m2,
        M3=m3,
        gamma=gamma,
        E1=e1,
        E2=e2,
        cp1=cp1,
        cp2=cp2,
        K00=k00,
        epsilon_1=epsilon_1,
        epsilon_DI=epsilon_di,
        epsilon_ratio=epsilon_ratio,
        h_rad_over_t2_exact=h_rad_over_t2_exact,
        m_tilde_exact_eV=m_tilde_exact_eV,
        m_star_exact_eV=m_star_exact_eV,
        k_decay_exact=k_decay_exact,
        m_star_bench_eV=m_star_bench_eV,
        k_decay_bench=k_decay_bench,
        kappa_fit_bench=kappa_fit_bench,
        eta_ratio_fit_bench_legacy=eta_ratio_fit_bench_legacy,
        eta_ratio_fit_bench_exact_bookkeeping=eta_ratio_fit_bench_exact_bookkeeping,
    )


def n_eq_normalized_mb(z: float) -> float:
    return 0.5 * z * z * float(special.kv(2, z))


def h_rad_exact(temperature: float) -> float:
    return H_RAD_COEFFICIENT_EXACT * temperature * temperature


def exact_radiation_expansion_profile(z: float) -> float:
    return 1.0


def reference_expansion_profile(z: float) -> float:
    return exact_radiation_expansion_profile(z)


def decay_profile(z: float, k_decay: float, expansion_profile: Callable[[float], float]) -> float:
    return k_decay * z * float(special.kv(1, z) / special.kv(2, z)) / expansion_profile(z)


def washout_profile(z: float, k_decay: float, expansion_profile: Callable[[float], float]) -> float:
    return 0.25 * k_decay * z**3 * float(special.kv(1, z)) / expansion_profile(z)


def solve_normalized_transport(
    k_decay: float,
    expansion_profile: Callable[[float], float] | None = None,
    z_min: float = 1.0e-3,
    z_max: float = 35.0,
    n_eval: int = 20000,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if expansion_profile is None:
        expansion_profile = reference_expansion_profile

    def rhs(z: float, state: np.ndarray) -> list[float]:
        n_n1, n_bm = state
        n_eq = n_eq_normalized_mb(z)
        d_rate = decay_profile(z, k_decay, expansion_profile)
        w_rate = washout_profile(z, k_decay, expansion_profile)
        dn_n1 = -d_rate * (n_n1 - n_eq)
        dn_bm = d_rate * (n_n1 - n_eq) - w_rate * n_bm
        return [dn_n1, dn_bm]

    sol = integrate.solve_ivp(
        rhs,
        (z_min, z_max),
        (n_eq_normalized_mb(z_min), 0.0),
        method="BDF",
        dense_output=True,
        rtol=1.0e-10,
        atol=1.0e-12,
    )
    if not sol.success:
        raise RuntimeError(sol.message)

    z_grid = np.linspace(z_min, z_max, n_eval)
    n_n1, n_bm = sol.sol(z_grid)
    return z_grid, n_n1, n_bm


def formal_transport_integral(
    z_grid: np.ndarray,
    n_n1: np.ndarray,
    k_decay: float,
    expansion_profile: Callable[[float], float] | None = None,
) -> float:
    if expansion_profile is None:
        expansion_profile = reference_expansion_profile
    w_vals = np.array([washout_profile(float(z), k_decay, expansion_profile) for z in z_grid], dtype=float)
    tail = np.zeros_like(z_grid)
    for idx in range(len(z_grid) - 2, -1, -1):
        tail[idx] = tail[idx + 1] + 0.5 * (w_vals[idx] + w_vals[idx + 1]) * (z_grid[idx + 1] - z_grid[idx])
    dn_dz = np.gradient(n_n1, z_grid)
    return float(np.trapezoid(-dn_dz * np.exp(-tail), z_grid))


def kappa_axiom_reference(k_decay: float) -> tuple[float, float]:
    z_grid, n_n1, n_bm = solve_normalized_transport(k_decay, reference_expansion_profile)
    direct = abs(float(n_bm[-1]))
    formal = formal_transport_integral(z_grid, n_n1, k_decay, reference_expansion_profile)
    return direct, formal


def solve_multisource_flavored_transport(
    lambdas: np.ndarray,
    k_decays: np.ndarray,
    source_matrix: np.ndarray,
    washout_matrix: np.ndarray,
    expansion_profile: Callable[[float], float] | None = None,
    z_min: float = 1.0e-3,
    z_max: float = 35.0,
    n_eval: int = 20000,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if expansion_profile is None:
        expansion_profile = reference_expansion_profile

    lambdas = np.asarray(lambdas, dtype=float)
    k_decays = np.asarray(k_decays, dtype=float)
    source_matrix = np.asarray(source_matrix, dtype=float)
    washout_matrix = np.asarray(washout_matrix, dtype=float)

    n_sources = int(lambdas.shape[0])
    n_flavors = int(source_matrix.shape[1])
    if k_decays.shape != (n_sources,):
        raise ValueError("k_decays must have shape (n_sources,)")
    if source_matrix.shape != (n_sources, n_flavors):
        raise ValueError("source_matrix must have shape (n_sources, n_flavors)")
    if washout_matrix.shape != (n_sources, n_flavors):
        raise ValueError("washout_matrix must have shape (n_sources, n_flavors)")

    def rhs(z: float, state: np.ndarray) -> np.ndarray:
        occupancies = state[:n_sources]
        asymmetries = state[n_sources:]

        d_occ = np.zeros(n_sources, dtype=float)
        d_asym = np.zeros(n_flavors, dtype=float)

        for idx in range(n_sources):
            z_i = float(lambdas[idx] * z)
            neq_i = n_eq_normalized_mb(z_i)
            d_rate = float(lambdas[idx]) * decay_profile(z_i, float(k_decays[idx]), expansion_profile)
            w_rate = float(lambdas[idx]) * washout_profile(z_i, float(k_decays[idx]), expansion_profile)
            source_i = d_rate * (occupancies[idx] - neq_i)

            d_occ[idx] = -source_i
            d_asym += source_matrix[idx] * source_i
            d_asym -= washout_matrix[idx] * w_rate * asymmetries

        return np.concatenate((d_occ, d_asym))

    initial_state = np.zeros(n_sources + n_flavors, dtype=float)
    for idx in range(n_sources):
        initial_state[idx] = n_eq_normalized_mb(float(lambdas[idx]) * z_min)

    sol = integrate.solve_ivp(
        rhs,
        (z_min, z_max),
        initial_state,
        method="BDF",
        dense_output=True,
        rtol=1.0e-10,
        atol=1.0e-12,
    )
    if not sol.success:
        raise RuntimeError(sol.message)

    z_grid = np.linspace(z_min, z_max, n_eval)
    state_grid = sol.sol(z_grid)
    occupancies = state_grid[:n_sources]
    asymmetries = state_grid[n_sources:]
    return z_grid, occupancies, asymmetries
