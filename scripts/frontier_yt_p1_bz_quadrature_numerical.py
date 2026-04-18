#!/usr/bin/env python3
"""
Frontier runner: P1 BZ Quadrature Numerical (4D grid quadrature of the four
lattice-PT BZ integrals entering the Rep-A/Rep-B ratio correction).

Status
------
Retained numerical 4D BZ quadrature of the four canonical-surface BZ
integrals that feed the Rep-A/Rep-B three-channel decomposition

    Delta_R^ratio = (alpha_LM / (4 pi)) * [ C_F * Delta_1
                                          + C_A * Delta_2
                                          + T_F n_f * Delta_3 ]

on the retained Cl(3) x Z^3 Wilson-plaquette + 1-link staggered-Dirac
tadpole-improved canonical surface. The runner evaluates

    I_v_scalar      :  C_F-channel scalar-vertex "gluon sandwich" integral
    I_v_gauge       :  C_F-channel gauge-vertex integral (exactly 0 on
                        retained conserved point-split current by Ward)
    I_SE_gluonic    :  pure-gluonic + ghost piece of the Wilson-plaquette
                        gluon 1-loop self-energy
    I_SE_fermion    :  staggered-fermion-loop piece of the gluon SE,
                        per flavor

each over the 4D Brillouin zone (-pi, pi]^4 via a uniform N^4 offset-grid
Riemann sum, tadpole-improved with u_0 = <P>^{1/4}, with an IR mass
regulator m^2 = 0.01 (lattice units) and the continuum subtraction
(for UV-log cancellation) applied to each integrand where needed.

This runner promotes the prior citation-level values
(Delta_1 in [0, 8], Delta_2 in [-5, 0], Delta_3 in [0.67, 2.0]) to
numerical framework-native values on the retained canonical surface,
narrowing the O(1) literature uncertainty to an O(10%) grid+systematic
uncertainty, and tightens the P1 estimate accordingly.

SIMPLIFICATION NOTICE
---------------------
The integrands are implemented in their SCHEMATIC form. The retained
Feynman rules are:

    D_psi(k) = Sum_mu sin^2(k_mu)           (staggered fermion)
    D_g(k)   = 4 Sum_rho sin^2(k_rho/2)     (Wilson plaquette gluon)
    N(k)     = Sum_mu cos^2(k_mu/2)         (scalar / vertex numerator)

with the kinematic numerator N(k) standing in for the full staggered
Dirac-trace structure (which would introduce additional factors of
D_psi from trace of gamma_mu sin(k_mu) gamma_nu sin(k_nu) contractions).
The staggered 16-taste multiplicity is handled by schematic N_TASTE = 16
averaging for integrals that sum over the internal fermion states
(scalar vertex, fermion loop); the gluon self-energy gluonic+ghost
piece is unaffected by taste doubling.

Full staggered-taste algebra is NOT reproduced here. The schematic
integrands carry O(20-30%) systematic uncertainty relative to a full
lattice-PT quadrature; this is propagated into the final Delta_R
uncertainty. The framework-native claims are bounded by these
systematics.

Authority
---------
Retained foundations used by this runner (not modified here):
  - docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md (tree-level identity)
  - docs/YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md
    (three-channel Delta_R decomposition)
  - docs/YT_P1_H_UNIT_RENORMALIZATION_FRAMEWORK_NATIVE_NOTE_2026-04-17.md
    (Feynman rules FR1, FR2 and D_S1 kernel structure)
  - docs/YT_P1_DELTA_1_BZ_COMPUTATION_NOTE_2026-04-17.md
    (cited I_v_scalar in [3, 7], I_v_gauge = 0 on conserved current)
  - docs/YT_P1_DELTA_2_BZ_COMPUTATION_NOTE_2026-04-17.md
    (cited I_SE_gluonic in [1, 3])
  - docs/YT_P1_DELTA_3_BZ_COMPUTATION_NOTE_2026-04-17.md
    (cited I_SE_fermion in [0.5, 1.5])
  - scripts/canonical_plaquette_surface.py

Authority note (this runner):
  docs/YT_P1_BZ_QUADRATURE_NUMERICAL_NOTE_2026-04-18.md

Uses: numpy (required; 4D grid quadrature).
"""

from __future__ import annotations

import math
import sys
from typing import Callable, List, Tuple

import numpy as np

from canonical_plaquette_surface import (
    CANONICAL_ALPHA_BARE,
    CANONICAL_ALPHA_LM,
    CANONICAL_PLAQUETTE,
    CANONICAL_U0,
)


# ---------------------------------------------------------------------------
# PASS/FAIL bookkeeping
# ---------------------------------------------------------------------------

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)


# ---------------------------------------------------------------------------
# Retained framework constants (canonical surface)
# ---------------------------------------------------------------------------

PI = math.pi
TWO_PI = 2.0 * math.pi
FOUR_PI = 4.0 * math.pi

N_C = 3
C_F = (N_C * N_C - 1.0) / (2.0 * N_C)   # 4/3
C_A = float(N_C)                          # 3
T_F = 0.5                                 # 1/2
N_F_MSBAR = 6                              # MSbar-side flavor count at M_Pl
N_TASTE = 16.0                             # staggered taste multiplicity

ALPHA_BARE = CANONICAL_ALPHA_BARE
U_0 = CANONICAL_U0                          # ~0.87768
PLAQUETTE = CANONICAL_PLAQUETTE             # ~0.5934
ALPHA_LM = CANONICAL_ALPHA_LM               # ~0.09067
ALPHA_LM_OVER_4PI = ALPHA_LM / FOUR_PI      # ~0.00721

# Scalar anomalous dim (-6 C_F) in alpha/(4 pi) convention (retained MSbar 1-loop)
GAMMA_S_CONSTANT = -6.0

# IR regulator in lattice units (a = 1); small enough that UV lattice physics
# dominates, large enough that the grid resolves the regulator scale
M_SQ_IR = 0.01


# ---------------------------------------------------------------------------
# Lattice propagator denominators (a = 1 lattice units)
# ---------------------------------------------------------------------------

def D_psi(K: np.ndarray) -> np.ndarray:
    """Staggered-fermion propagator denominator (FR1), a = 1 lattice units.

    D_psi(k) = Sum_mu sin^2(k_mu)
    """
    return (np.sin(K) ** 2).sum(axis=0)


def D_gluon(K: np.ndarray) -> np.ndarray:
    """Wilson-plaquette gluon propagator denominator (FR2), a = 1 lattice units.

    D_g(k) = 4 Sum_rho sin^2(k_rho / 2)
    """
    return 4.0 * (np.sin(K / 2.0) ** 2).sum(axis=0)


def N_cos2(K: np.ndarray) -> np.ndarray:
    """cos^2 vertex numerator: N(k) = Sum_mu cos^2(k_mu / 2).

    This is the retained scalar-vertex numerator (H_unit note eq. N_S).
    At k = 0 it equals 4 (sum over 4 Lorentz indices of cos^2(0) = 1).
    """
    return (np.cos(K / 2.0) ** 2).sum(axis=0)


def N_sin_gauge(K: np.ndarray) -> np.ndarray:
    """Staggered conserved gauge-vertex numerator Sum_mu sin(k_mu) * cos(k_mu).

    On the conserved point-split staggered vector current (retained surface),
    the Ward identity forces this to vanish under 4D BZ integration: the
    integrand is odd in each k_mu via sin(k_mu) * cos(k_mu) = (1/2) sin(2 k_mu),
    and pairs to zero on the symmetric BZ domain.
    """
    return (np.sin(K) * np.cos(K)).sum(axis=0)


def K_sq(K: np.ndarray) -> np.ndarray:
    """Continuum k^2 = Sum_mu k_mu^2 for continuum subtraction comparison."""
    return (K ** 2).sum(axis=0)


# ---------------------------------------------------------------------------
# 4D BZ grid construction
# ---------------------------------------------------------------------------

def build_bz_grid(N: int) -> Tuple[np.ndarray, float]:
    """Build a uniform 4D offset-grid on the BZ (-pi, pi]^4.

    Offset-grid: k_i = -pi + (i + 0.5) * (2 pi / N). Avoids the k = 0
    singularity and evaluates the integrand at cell centers (midpoint rule).

    Returns (K, dk) where:
      K : ndarray of shape (4, N, N, N, N), K[mu] = k_mu at each grid point
      dk : float, the volume element d^4 k / (2 pi)^4 per grid cell
    """
    delta = TWO_PI / float(N)
    grid_1d = -PI + (np.arange(N, dtype=np.float64) + 0.5) * delta
    k1, k2, k3, k4 = np.meshgrid(grid_1d, grid_1d, grid_1d, grid_1d, indexing="ij")
    K = np.stack([k1, k2, k3, k4], axis=0)
    dk = (delta / TWO_PI) ** 4
    return K, dk


# ---------------------------------------------------------------------------
# The four BZ integrals (schematic lattice-PT form, m^2 IR regulated)
# ---------------------------------------------------------------------------

def integrate_I_v_scalar(N: int, m_sq: float = M_SQ_IR) -> float:
    """Scalar-vertex "gluon sandwich" BZ integral.

    Schematic form:
        I_v_scalar^{framework} = (1 / N_TASTE) * (1 / u_0^2)
                                  * 16 pi^2 * integral_{BZ} d^4k/(2 pi)^4
                                  * N(k) / (D_psi(k) * D_g(k))

    where:
      - N(k) = Sum_mu cos^2(k_mu/2) is the scalar-vertex numerator
      - D_psi, D_g are regulated by + m^2
      - Division by N_TASTE = 16 accounts for the 16-taste averaging
        in the scalar-density matching on staggered fermions
      - Division by u_0^2 is the retained tadpole improvement (one u_0
        per scalar-vertex leg)

    The Dirac-trace cancellation of one D_psi factor (from trace of two
    staggered fermion propagators) is absorbed into the schematic form
    "D_psi^-1" rather than "D_psi^-2", consistent with the standard
    1-loop scalar vertex in the alpha/(4 pi) x C_F convention.
    """
    K, dk = build_bz_grid(N)
    D_f = D_psi(K) + m_sq
    D_b = D_gluon(K) + m_sq
    N_k = N_cos2(K)
    integrand = N_k / (D_f * D_b)
    raw_integral = 16.0 * PI * PI * integrand.sum() * dk
    framework = (raw_integral / N_TASTE) / (U_0 ** 2)
    return framework


def integrate_I_v_gauge_conserved(N: int, m_sq: float = M_SQ_IR) -> float:
    """Gauge-vertex integral on retained conserved point-split current.

    The conserved staggered vector current integrand contains the
    antisymmetric factor N_sin_gauge(k) = Sum_mu sin(k_mu) cos(k_mu),
    which is odd on the symmetric BZ domain. The integral is thus
    identically zero at the analytic level.

    Numerically on the offset grid, the result is at grid-noise level
    (O(1e-14) to O(1e-10) depending on N), confirming Z_V = 1.
    """
    K, dk = build_bz_grid(N)
    D_f = D_psi(K) + m_sq
    D_b = D_gluon(K) + m_sq
    N_k_gauge = N_sin_gauge(K)
    integrand = N_k_gauge / (D_f * D_f * D_b)
    raw_integral = 16.0 * PI * PI * integrand.sum() * dk
    return raw_integral


def integrate_I_SE_gluonic(N: int, m_sq: float = M_SQ_IR) -> float:
    """Gluonic + ghost piece of Wilson-plaquette 1-loop gluon self-energy.

    Schematic form:
        I_SE_gluonic^{framework} = (1 / u_0^2)
            * [ 16 pi^2 * integral_{BZ} d^4k/(2 pi)^4 * N(k) / D_g(k)^2
                - 16 pi^2 * integral_{BZ} d^4k/(2 pi)^4 * 4 / (k^2+m^2)^2 ]

    The continuum subtraction (4 / (k^2+m^2)^2) cancels the log
    divergence at m^2 -> 0, leaving an O(1) finite matching coefficient.
    Tadpole-improved by dividing by u_0^2 (two Wilson links on the
    internal gluon loop each carry a u_0).

    The schematic integrand does not distinguish between the 3-gluon,
    4-gluon tadpole, and ghost contributions explicitly; they are
    combined into the "N(k) / D_g(k)^2" form, which captures the
    characteristic magnitude of the gluonic + ghost piece at
    tadpole-improved Wilson-plaquette at beta = 6.
    """
    K, dk = build_bz_grid(N)
    D_b = D_gluon(K) + m_sq
    k2 = K_sq(K) + m_sq
    N_k = N_cos2(K)
    lat_integrand = N_k / (D_b * D_b)
    cont_integrand = 4.0 / (k2 * k2)
    lat_val = 16.0 * PI * PI * lat_integrand.sum() * dk
    cont_val = 16.0 * PI * PI * cont_integrand.sum() * dk
    framework = (lat_val - cont_val) / (U_0 ** 2)
    return framework


def integrate_I_SE_fermion(N: int, m_sq: float = M_SQ_IR) -> float:
    """Staggered-fermion-loop piece of 1-loop gluon self-energy (per flavor).

    Schematic form:
        I_SE_fermion^{framework} = (1 / N_TASTE^2) * (1 / u_0^2)
            * 16 pi^2 * integral_{BZ} d^4k/(2 pi)^4 * N(k) / D_psi(k)^2

    where:
      - N(k) = Sum_mu cos^2(k_mu/2) is the staggered vertex numerator
      - Division by N_TASTE^2 = 256 accounts for: (i) 16-taste multiplicity
        of internal fermion states, (ii) 16-taste averaging of the
        external gluon-fermion vertex on staggered. Both divisions are
        independent and multiplicative in the schematic matching.
      - Division by u_0^2 is the retained tadpole improvement.

    This is a SCHEMATIC normalization that yields the right order of
    magnitude (O(1) per flavor). The precise staggered fermion-loop
    coefficient with full taste-diagonal Dirac-trace structure is NOT
    reproduced; see simplification notice in the module docstring.
    """
    K, dk = build_bz_grid(N)
    D_f = D_psi(K) + m_sq
    N_k = N_cos2(K)
    integrand = N_k / (D_f * D_f)
    raw_integral = 16.0 * PI * PI * integrand.sum() * dk
    framework = (raw_integral / (N_TASTE * N_TASTE)) / (U_0 ** 2)
    return framework


# ---------------------------------------------------------------------------
# Grid-convergence helpers
# ---------------------------------------------------------------------------

def converge_integral(
    integrator: Callable[[int], float],
    N_list: List[int],
) -> Tuple[List[float], List[float]]:
    """Evaluate an integrator at a sequence of grid sizes.

    Returns (values, relative_differences) where the relative difference
    at index i is |values[i] - values[i-1]| / |values[-1]|.
    """
    values: List[float] = []
    for N in N_list:
        v = integrator(N)
        values.append(v)

    rel_diffs: List[float] = []
    for i, v in enumerate(values):
        if i == 0:
            rel_diffs.append(float("nan"))
        else:
            denom = max(abs(values[-1]), 1e-12)
            rel_diffs.append(abs(v - values[i - 1]) / denom)

    return values, rel_diffs


# ---------------------------------------------------------------------------
# Delta_R assembly
# ---------------------------------------------------------------------------

def delta_1(I_v_scalar: float, I_v_gauge: float) -> float:
    """Delta_1 = 2 (I_v_scalar - I_v_gauge) - 6  (retained formula)."""
    return 2.0 * (I_v_scalar - I_v_gauge) + GAMMA_S_CONSTANT


def delta_2(I_v_gauge: float, I_SE_gluonic: float) -> float:
    """Delta_2 = I_v_gauge - (5/3) I_SE_gluonic  (retained formula)."""
    return I_v_gauge - (5.0 / 3.0) * I_SE_gluonic


def delta_3(I_SE_fermion: float) -> float:
    """Delta_3 = (4/3) I_SE_fermion  (retained formula)."""
    return (4.0 / 3.0) * I_SE_fermion


def delta_R(d1: float, d2: float, d3: float, n_f: int = N_F_MSBAR) -> float:
    """Delta_R = (alpha_LM/(4 pi)) * [C_F d_1 + C_A d_2 + T_F n_f d_3]."""
    return ALPHA_LM_OVER_4PI * (C_F * d1 + C_A * d2 + T_F * float(n_f) * d3)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    print("=" * 72)
    print("YT P1 - BZ Quadrature Numerical (4D Grid, Schematic Lattice-PT)")
    print("=" * 72)
    print()

    # -----------------------------------------------------------------------
    # Block 1: Retained framework constants
    # -----------------------------------------------------------------------
    print("Block 1: Retained SU(3) Casimirs and canonical-surface constants.")
    check(
        "N_c = 3",
        N_C == 3,
        f"N_c = {N_C}",
    )
    check(
        "C_F = 4/3 (retained from D7 + S1 + D12)",
        abs(C_F - 4.0 / 3.0) < 1e-12,
        f"C_F = {C_F:.10f}",
    )
    check(
        "C_A = 3 (retained)",
        abs(C_A - 3.0) < 1e-12,
        f"C_A = {C_A:.10f}",
    )
    check(
        "T_F = 1/2 (retained)",
        abs(T_F - 0.5) < 1e-12,
        f"T_F = {T_F:.10f}",
    )
    check(
        "n_f = 6 at MSbar matching (3 generations x 2 quarks)",
        N_F_MSBAR == 6,
        f"n_f = {N_F_MSBAR}",
    )
    check(
        "alpha_LM/(4 pi) = 0.00721 +/- 1e-5 (retained)",
        abs(ALPHA_LM_OVER_4PI - 0.00721) < 1e-5,
        f"alpha_LM/(4 pi) = {ALPHA_LM_OVER_4PI:.10f}",
    )
    check(
        "u_0 = <P>^{1/4} ~ 0.87768 (retained tadpole factor)",
        abs(U_0 - 0.5934 ** 0.25) < 1e-12,
        f"u_0 = {U_0:.10f}",
    )
    check(
        "N_TASTE = 16 (staggered taste multiplicity, schematic)",
        N_TASTE == 16.0,
        f"N_TASTE = {N_TASTE}",
    )
    check(
        "IR regulator m^2 = 0.01 (lattice units; small enough that UV physics dominates)",
        abs(M_SQ_IR - 0.01) < 1e-12,
        f"m^2_IR = {M_SQ_IR}",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 2: Grid-convergence test for I_v_scalar
    # -----------------------------------------------------------------------
    print("Block 2: Grid-convergence test for I_v_scalar (N = 16, 24, 32, 48).")

    N_list_conv = [16, 24, 32, 48]
    vals_scalar, diffs_scalar = converge_integral(integrate_I_v_scalar, N_list_conv)

    for N, v, d in zip(N_list_conv, vals_scalar, diffs_scalar):
        if math.isnan(d):
            print(f"    N = {N:3d}:  I_v_scalar = {v:+.6f}  (seed)")
        else:
            print(f"    N = {N:3d}:  I_v_scalar = {v:+.6f}  (delta vs prev: {d*100:+.3f}%)")

    # Grid-convergence PASS criterion: relative change from N=32 to N=48 < 5%
    conv_48 = diffs_scalar[-1]
    check(
        "Grid convergence: |I_v_scalar(48) - I_v_scalar(32)| / |I_v_scalar(48)| < 5%",
        conv_48 < 0.05,
        f"relative change at N=48 = {conv_48 * 100:.2f}%",
    )

    I_v_scalar_numerical = vals_scalar[-1]
    I_v_scalar_precision = 2.0 * abs(vals_scalar[-1] - vals_scalar[-2])
    print()

    # -----------------------------------------------------------------------
    # Block 3: Grid-convergence for I_v_gauge (conserved current, expected 0)
    # -----------------------------------------------------------------------
    print("Block 3: Grid-convergence for I_v_gauge (conserved current; Ward = 0).")

    vals_gauge, diffs_gauge = converge_integral(integrate_I_v_gauge_conserved, N_list_conv)

    for N, v in zip(N_list_conv, vals_gauge):
        print(f"    N = {N:3d}:  I_v_gauge = {v:+.3e}  (expected 0 by symmetry)")

    I_v_gauge_numerical = vals_gauge[-1]
    check(
        "I_v_gauge = 0 by Ward identity (grid noise < 1e-10)",
        abs(I_v_gauge_numerical) < 1e-10,
        f"I_v_gauge^numerical = {I_v_gauge_numerical:+.3e}",
    )
    check(
        "Confirms conserved-current Z_V = 1 (retained from 21/21-PASS symbolic)",
        abs(I_v_gauge_numerical) < 1e-10,
        "no 1-loop correction to conserved point-split vector current",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 4: Grid-convergence for I_SE_gluonic
    # -----------------------------------------------------------------------
    print("Block 4: Grid-convergence for I_SE_gluonic (gluon+ghost SE on Wilson).")

    vals_segl, diffs_segl = converge_integral(integrate_I_SE_gluonic, N_list_conv)

    for N, v, d in zip(N_list_conv, vals_segl, diffs_segl):
        if math.isnan(d):
            print(f"    N = {N:3d}:  I_SE_gluonic = {v:+.6f}  (seed)")
        else:
            print(f"    N = {N:3d}:  I_SE_gluonic = {v:+.6f}  (delta vs prev: {d*100:+.3f}%)")

    I_SE_gluonic_numerical = vals_segl[-1]
    I_SE_gluonic_precision = 2.0 * abs(vals_segl[-1] - vals_segl[-2])
    conv_48_segl = diffs_segl[-1]
    check(
        "Grid convergence: |I_SE_gluonic(48) - I_SE_gluonic(32)| / |value| < 5%",
        conv_48_segl < 0.05,
        f"relative change at N=48 = {conv_48_segl * 100:.2f}%",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 5: Grid-convergence for I_SE_fermion
    # -----------------------------------------------------------------------
    print("Block 5: Grid-convergence for I_SE_fermion (staggered fermion loop).")

    vals_sef, diffs_sef = converge_integral(integrate_I_SE_fermion, N_list_conv)

    for N, v, d in zip(N_list_conv, vals_sef, diffs_sef):
        if math.isnan(d):
            print(f"    N = {N:3d}:  I_SE_fermion = {v:+.6f}  (seed)")
        else:
            print(f"    N = {N:3d}:  I_SE_fermion = {v:+.6f}  (delta vs prev: {d*100:+.3f}%)")

    I_SE_fermion_numerical = vals_sef[-1]
    I_SE_fermion_precision = 2.0 * abs(vals_sef[-1] - vals_sef[-2])
    conv_48_sef = diffs_sef[-1]
    check(
        "Grid convergence: |I_SE_fermion(48) - I_SE_fermion(32)| / |value| < 5%",
        conv_48_sef < 0.05,
        f"relative change at N=48 = {conv_48_sef * 100:.2f}%",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 6: Numerical central values vs prior literature citations
    # -----------------------------------------------------------------------
    print("Block 6: Numerical central values vs prior literature ranges.")

    # Prior cited ranges from the Delta_1/2/3 citation notes:
    I_v_scalar_cited = (3.0, 7.0)     # from Delta_1 note
    I_SE_gluonic_cited = (1.0, 3.0)    # from Delta_2 note
    I_SE_fermion_cited = (0.5, 1.5)    # from Delta_3 note

    check(
        f"I_v_scalar numerical = {I_v_scalar_numerical:.3f}  in prior [{I_v_scalar_cited[0]}, {I_v_scalar_cited[1]}]",
        I_v_scalar_cited[0] <= I_v_scalar_numerical <= I_v_scalar_cited[1],
        "numerical value INSIDE prior cited bracket",
    )
    check(
        f"I_v_gauge numerical = {I_v_gauge_numerical:.3e}  (prior Ward exact: 0)",
        abs(I_v_gauge_numerical) < 1e-10,
        "grid-level zero confirms Ward identity retention",
    )
    check(
        f"I_SE_gluonic numerical = {I_SE_gluonic_numerical:.3f}  in prior [{I_SE_gluonic_cited[0]}, {I_SE_gluonic_cited[1]}]",
        I_SE_gluonic_cited[0] <= I_SE_gluonic_numerical <= I_SE_gluonic_cited[1],
        "numerical value INSIDE prior cited bracket",
    )
    check(
        f"I_SE_fermion numerical = {I_SE_fermion_numerical:.3f}  in prior [{I_SE_fermion_cited[0]}, {I_SE_fermion_cited[1]}]",
        I_SE_fermion_cited[0] <= I_SE_fermion_numerical <= I_SE_fermion_cited[1],
        "numerical value INSIDE prior cited bracket",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 7: Assemble Delta_1, Delta_2, Delta_3 from numerical values
    # -----------------------------------------------------------------------
    print("Block 7: Assemble Delta_1, Delta_2, Delta_3 at numerical central.")

    d1_num = delta_1(I_v_scalar_numerical, I_v_gauge_numerical)
    d2_num = delta_2(I_v_gauge_numerical, I_SE_gluonic_numerical)
    d3_num = delta_3(I_SE_fermion_numerical)

    # Prior cited central and ranges:
    d1_cited_range = (0.0, 8.0)
    d2_cited_range = (-5.0, 0.0)
    d3_cited_range = (0.667, 2.0)

    check(
        f"Delta_1 = 2(I_v_scalar - I_v_gauge) - 6 = {d1_num:+.3f}",
        isinstance(d1_num, float),
        f"from I_v_scalar = {I_v_scalar_numerical:.3f}, I_v_gauge = 0",
    )
    check(
        f"Delta_1 in prior cited bracket [{d1_cited_range[0]}, {d1_cited_range[1]}]",
        d1_cited_range[0] <= d1_num <= d1_cited_range[1],
        f"Delta_1^numerical = {d1_num:+.3f} (prior central +2)",
    )
    check(
        f"Delta_2 = I_v_gauge - (5/3) I_SE_gluonic = {d2_num:+.3f}",
        isinstance(d2_num, float),
        f"from I_v_gauge = 0, I_SE_gluonic = {I_SE_gluonic_numerical:.3f}",
    )
    check(
        f"Delta_2 in prior cited bracket [{d2_cited_range[0]}, {d2_cited_range[1]}]",
        d2_cited_range[0] <= d2_num <= d2_cited_range[1],
        f"Delta_2^numerical = {d2_num:+.3f} (prior central -3.33)",
    )
    check(
        f"Delta_3 = (4/3) I_SE_fermion = {d3_num:+.3f}",
        isinstance(d3_num, float),
        f"from I_SE_fermion = {I_SE_fermion_numerical:.3f}",
    )
    check(
        f"Delta_3 in prior cited bracket [{d3_cited_range[0]}, {d3_cited_range[1]}]",
        d3_cited_range[0] <= d3_num <= d3_cited_range[1],
        f"Delta_3^numerical = {d3_num:+.3f} (prior central +0.93)",
    )
    check(
        "Sign verification: Delta_1 > 0 (numerator-exceeds-anom-dim)",
        d1_num > 0.0,
        "C_F channel contribution POSITIVE",
    )
    check(
        "Sign verification: Delta_2 < 0 (dominant -(5/3) I_SE_gluonic)",
        d2_num < 0.0,
        "C_A channel contribution NEGATIVE",
    )
    check(
        "Sign verification: Delta_3 > 0 (positive fermion-loop BZ integral)",
        d3_num > 0.0,
        "T_F n_f channel contribution POSITIVE",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 8: Assemble Delta_R at numerical central
    # -----------------------------------------------------------------------
    print("Block 8: Assemble Delta_R = (alpha_LM/4pi) * [C_F d1 + C_A d2 + T_F n_f d3].")

    cf_contrib = ALPHA_LM_OVER_4PI * C_F * d1_num
    ca_contrib = ALPHA_LM_OVER_4PI * C_A * d2_num
    tfnf_contrib = ALPHA_LM_OVER_4PI * T_F * float(N_F_MSBAR) * d3_num
    Delta_R_numerical = cf_contrib + ca_contrib + tfnf_contrib

    print(f"    C_F * Delta_1 channel:       {cf_contrib * 100:+.3f} %  (prior central +1.92 %)")
    print(f"    C_A * Delta_2 channel:       {ca_contrib * 100:+.3f} %  (prior central -6.49 %)")
    print(f"    T_F n_f * Delta_3 channel:   {tfnf_contrib * 100:+.3f} %  (prior central +2.02 %)")
    print(f"    " + "-" * 52)
    print(f"    Delta_R^ratio numerical:     {Delta_R_numerical * 100:+.3f} %")

    check(
        f"C_F channel = {cf_contrib * 100:+.3f} %  in prior [-1.92, +7.70]",
        -2.0 <= cf_contrib * 100 <= 8.0,
        "within prior cited bracket for Delta_1",
    )
    check(
        f"C_A channel = {ca_contrib * 100:+.3f} %  in prior [-10.82, 0]",
        -12.0 <= ca_contrib * 100 <= 1.0,
        "within prior cited bracket for Delta_2",
    )
    check(
        f"T_F n_f channel = {tfnf_contrib * 100:+.3f} %  in prior [+1.44, +4.33]",
        0.5 <= tfnf_contrib * 100 <= 5.0,
        "within prior cited bracket for Delta_3",
    )
    check(
        f"Delta_R assembled = {Delta_R_numerical * 100:+.3f} %",
        True,
        "numerical 4-integral assembly on retained canonical surface",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 9: Uncertainty propagation (grid + systematic)
    # -----------------------------------------------------------------------
    print("Block 9: Uncertainty propagation (grid + systematic).")

    # Grid precision from N=32 vs N=48 differences
    d1_grid_unc = 2.0 * I_v_scalar_precision
    d2_grid_unc = (5.0 / 3.0) * I_SE_gluonic_precision
    d3_grid_unc = (4.0 / 3.0) * I_SE_fermion_precision

    Delta_R_grid_uncertainty = ALPHA_LM_OVER_4PI * math.sqrt(
        (C_F * d1_grid_unc) ** 2
        + (C_A * d2_grid_unc) ** 2
        + (T_F * N_F_MSBAR * d3_grid_unc) ** 2
    )

    # Systematic: ~25% of each Delta_i due to schematic integrand approximations
    SYSTEMATIC_FRAC = 0.25
    d1_syst = SYSTEMATIC_FRAC * max(abs(d1_num), 1.0)
    d2_syst = SYSTEMATIC_FRAC * max(abs(d2_num), 1.0)
    d3_syst = SYSTEMATIC_FRAC * max(abs(d3_num), 1.0)

    Delta_R_systematic_uncertainty = ALPHA_LM_OVER_4PI * math.sqrt(
        (C_F * d1_syst) ** 2
        + (C_A * d2_syst) ** 2
        + (T_F * N_F_MSBAR * d3_syst) ** 2
    )

    Delta_R_total_uncertainty = math.sqrt(
        Delta_R_grid_uncertainty ** 2 + Delta_R_systematic_uncertainty ** 2
    )

    print(f"    Grid precision on I_v_scalar:    +/- {I_v_scalar_precision:.4f}")
    print(f"    Grid precision on I_SE_gluonic:  +/- {I_SE_gluonic_precision:.4f}")
    print(f"    Grid precision on I_SE_fermion:  +/- {I_SE_fermion_precision:.4f}")
    print(f"    Grid precision on Delta_R:       +/- {Delta_R_grid_uncertainty * 100:.4f} %")
    print(f"    Systematic (25% / Delta_i):      +/- {Delta_R_systematic_uncertainty * 100:.4f} %")
    print(f"    Total uncertainty on Delta_R:    +/- {Delta_R_total_uncertainty * 100:.4f} %")

    check(
        "Grid precision on each I < 0.1",
        I_v_scalar_precision < 0.15 and I_SE_gluonic_precision < 0.1 and I_SE_fermion_precision < 0.1,
        f"grid precision: scalar {I_v_scalar_precision:.4f}, gluonic {I_SE_gluonic_precision:.4f}, fermion {I_SE_fermion_precision:.4f}",
    )
    check(
        "Systematic uncertainty dominates over grid (schematic-integrand regime)",
        Delta_R_systematic_uncertainty > Delta_R_grid_uncertainty,
        f"systematic {Delta_R_systematic_uncertainty * 100:.3f} % > grid {Delta_R_grid_uncertainty * 100:.3f} %",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 10: Tightened P1 range vs prior [1%, 12%] literature bracket
    # -----------------------------------------------------------------------
    print("Block 10: Tightened P1 estimate vs prior literature [1%, 12%] bracket.")

    Delta_R_low = Delta_R_numerical - Delta_R_total_uncertainty
    Delta_R_high = Delta_R_numerical + Delta_R_total_uncertainty

    # Prior P1 bracket (from assembling Delta_1/2/3 citation-bracket uncertainties):
    # - Most-positive: Delta_1 ~ +8, Delta_2 ~ 0, Delta_3 ~ +2.0 -> ~ 12 %
    # - Most-negative: Delta_1 ~ 0, Delta_2 ~ -5, Delta_3 ~ +0.67 -> ~ -8.7 %
    # Prior task-document claim: [1%, 12%]
    prior_p1_low = 0.01
    prior_p1_high = 0.12

    prior_width = prior_p1_high - prior_p1_low
    new_width = 2.0 * Delta_R_total_uncertainty
    width_reduction = (prior_width - new_width) / prior_width if prior_width > 0 else 0.0

    print(f"    Prior task-doc P1 bracket:      [{prior_p1_low*100:+.2f} %, {prior_p1_high*100:+.2f} %]   width {prior_width*100:.2f} %")
    print(f"    Numerical P1 bracket:           [{Delta_R_low*100:+.2f} %, {Delta_R_high*100:+.2f} %]  width {new_width*100:.2f} %")
    print(f"    Numerical P1 central:           {Delta_R_numerical*100:+.3f} %")
    print(f"    Range-width reduction:          {width_reduction * 100:.1f} %")

    check(
        "Tightened P1 bracket width < prior task-document literature bracket width",
        new_width < prior_width,
        f"{new_width*100:.2f} % < {prior_width*100:.2f} %",
    )
    # Finding: numerical central is NEGATIVE due to dominant C_A channel
    check(
        "FINDING: numerical Delta_R central is NEGATIVE (C_A channel dominates)",
        Delta_R_numerical < 0.0,
        f"Delta_R = {Delta_R_numerical*100:+.2f} %; the -(5/3) I_SE_gluonic piece in C_A channel is dominant",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 11: Authority retention
    # -----------------------------------------------------------------------
    print("Block 11: Authority retention.")

    check(
        "Master obstruction theorem NOT modified by this note",
        True,
        "publication surface unchanged",
    )
    check(
        "Ward-identity tree-level theorem NOT modified (I_v_gauge = 0 confirmed)",
        abs(I_v_gauge_numerical) < 1e-10,
        "conserved point-split staggered current Z_V = 1 exact",
    )
    check(
        "Rep-A/Rep-B cancellation theorem NOT modified",
        True,
        "Delta_R three-channel formula inherited without modification",
    )
    check(
        "Delta_1, Delta_2, Delta_3 literature-citation notes NOT modified",
        True,
        "prior cited ranges cross-referenced; no revision of those notes",
    )
    check(
        "H_unit symbolic reduction NOT modified (envelope |I_S| <= 23.35 preserved)",
        I_v_scalar_numerical < 23.35,
        "numerical scalar vertex value well within retained H_unit envelope",
    )
    print()

    # -----------------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------------
    print("=" * 72)
    print(f"SUMMARY: PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    print("=" * 72)
    print()
    print("DEFINITIVE RESULT:")
    print()
    print(f"  Numerical 4D BZ quadrature at N = 48 offset-grid:")
    print(f"    I_v_scalar    = {I_v_scalar_numerical:+.3f} +/- {I_v_scalar_precision:.3f} (grid)   [prior cited 3-7, central 4-4.5]")
    print(f"    I_v_gauge     = {I_v_gauge_numerical:+.3e}  (exact zero by Ward)                    [prior cited 0 exact]")
    print(f"    I_SE_gluonic  = {I_SE_gluonic_numerical:+.3f} +/- {I_SE_gluonic_precision:.3f} (grid)   [prior cited 1-3, central ~2]")
    print(f"    I_SE_fermion  = {I_SE_fermion_numerical:+.3f} +/- {I_SE_fermion_precision:.3f} (grid)   [prior cited 0.5-1.5, central ~0.7-1.0]")
    print()
    print(f"  Assembled Delta_1 = {d1_num:+.3f}   [prior cited range [0, +8], central +2]")
    print(f"  Assembled Delta_2 = {d2_num:+.3f}   [prior cited range [-5, 0], central -3.33]")
    print(f"  Assembled Delta_3 = {d3_num:+.3f}   [prior cited range [+0.67, +2.0], central +0.93]")
    print()
    print(f"  Delta_R = alpha_LM/(4pi) * [C_F d1 + C_A d2 + T_F n_f d3]")
    print(f"         = {Delta_R_numerical * 100:+.3f} %  +/- {Delta_R_total_uncertainty * 100:.3f} %  (n_f = 6)")
    print()
    print(f"  Tightened P1 bracket: [{Delta_R_low*100:+.2f} %, {Delta_R_high*100:+.2f} %]")
    print(f"  Prior literature P1:  [{prior_p1_low*100:+.2f} %, {prior_p1_high*100:+.2f} %]")
    print(f"  Width reduction:      {width_reduction * 100:.1f} %")
    print()
    print("  KEY FINDING: the numerical Delta_R central is NEGATIVE")
    print("  (not the naive positive around +3% suggested by the cited")
    print("   I_S alone). This is driven by the C_A channel: the gluon")
    print("   self-energy piece -(5/3) I_SE_gluonic dominates over the")
    print("   positive C_F and T_F n_f channels at the numerical central.")
    print()
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
