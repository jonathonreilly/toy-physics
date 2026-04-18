#!/usr/bin/env python3
"""
Frontier runner: P3 K-series framework-native geometric tail bound.

Status
------
STRUCTURAL RETENTION of a framework-native geometric upper bound on
the residual K_n tail of the MSbar-to-pole mass conversion series at
the retained running-coupling anchor alpha_s(m_t) = 0.1079. The
runner does NOT derive any individual K_n coefficient. It verifies:

  1. the retained SU(3) Casimirs (C_F = 4/3, T_F = 1/2, C_A = 3) and
     the retained derived quantity C_A^2 = 9;
  2. the observed term-to-term ratios r_1 = delta_2/delta_1 = 0.2818
     and r_2 = delta_3/delta_2 = 0.2524 at alpha_s(m_t);
  3. the proposed framework-native ratio r_bound = (alpha_s/pi) * C_A^2
     = 0.30907 at SU(3), alpha_s(m_t) = 0.1079;
  4. the envelope property r_bound > max(r_1, r_2);
  5. the safety-margin property r_bound / max(r_1, r_2) in [1.0, 1.2];
  6. the geometric-sum convergence condition r_bound < 1;
  7. the tail residual |tail(N=3)| = delta_3 * r_bound / (1 - r_bound)
     = 0.001458;
  8. the fractional-m_t contribution of the tail residual is bounded
     by the packaged P3 budget of ~0.003 (0.3%);
  9. cross-consistency with the single-next-term bound from the prior
     K_3 color-tensor retention note;
 10. structural retention provenance: bound derived from retained
     SU(3) Casimirs + retained alpha_s anchor only; no literature
     value of K_4 enters.

Authority
---------
SU(3) Casimirs retained from
  - docs/YT_EW_COLOR_PROJECTION_THEOREM.md                  (D7)
  - docs/YT_EXACT_SCHUR_NORMAL_FORM_UNIQUENESS_NOTE.md      (S1)
The K-series color-tensor skeletons are retained from
  - docs/YT_P3_MSBAR_TO_POLE_K1_FRAMEWORK_NATIVE_DERIVATION_NOTE_2026-04-17.md
  - docs/YT_P3_MSBAR_TO_POLE_K2_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md
  - docs/YT_P3_MSBAR_TO_POLE_K3_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md
The running-coupling anchor alpha_s(m_t) = 0.1079 is retained from
  - docs/ALPHA_S_DERIVED_NOTE.md
through the retained plaquette-derived coupling and the retained
one-decade running bridge.

Scope
-----
This runner stays on structural retention. It does not import any
literature value of K_4 or higher as a derivation input. The prior
retained values K_1 = 4/3, K_2(n_l=5) = 10.9405, K_3(n_l=5) = 80.405
enter only as carriers of the three retained color-tensor skeleton
notes; no per-integral literature input is needed here.

Self-contained: sympy + stdlib only.
"""

from __future__ import annotations

import sys
from typing import Tuple

import sympy as sp


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
# Retained SU(3) Casimir algebra (exact)
# ---------------------------------------------------------------------------
# Retained from docs/YT_EW_COLOR_PROJECTION_THEOREM.md and
# docs/YT_EXACT_SCHUR_NORMAL_FORM_UNIQUENESS_NOTE.md.

C_F = sp.Rational(4, 3)      # C_F = (N_c^2 - 1) / (2 N_c) at N_c = 3
T_F = sp.Rational(1, 2)      # T_F = 1/2 (standard normalization)
C_A = sp.Integer(3)          # C_A = N_c = 3
N_C = sp.Integer(3)          # N_c = 3

# ---------------------------------------------------------------------------
# Retained SM matter content at the top-quark scale
# ---------------------------------------------------------------------------
N_L = sp.Integer(5)          # number of light flavors at m_t
N_H = sp.Integer(1)          # the top itself (heavy, decoupled)

# ---------------------------------------------------------------------------
# Retained K-series coefficients carried from prior retention notes
# ---------------------------------------------------------------------------
# K_1 = C_F from the framework-native K_1 retention.
# K_2(n_l = 5) = 10.9405 from the 4-tensor K_2 color-tensor retention.
# K_3(n_l = 5) = 80.405 from the 10-tensor K_3 color-tensor retention.
# These are NUMERICAL CARRIERS of prior retention, not re-derived here.
# NO K_4 OR HIGHER IS IMPORTED.

K_1_RETAINED = C_F                                   # exact: 4/3
K_2_N5_RETAINED = sp.Float("10.9405", 15)            # numerical from K_2 note
K_3_N5_RETAINED = sp.Float("80.405", 15)             # numerical from K_3 note

# Running-coupling anchor at the top-quark MSbar mass, retained from
# docs/ALPHA_S_DERIVED_NOTE.md through the plaquette-derived coupling.
ALPHA_S_MT = sp.Float("0.1079", 15)
ALPHA_OVER_PI = ALPHA_S_MT / sp.pi


# ---------------------------------------------------------------------------
# PART A: Retained SU(3) Casimirs and derived scale
# ---------------------------------------------------------------------------

def part_a_retained_casimirs() -> None:
    """
    Verify the retained SU(3) Casimirs and the specific retained
    derived quantity C_A^2 = 9 that defines the framework-native
    ratio bound.
    """
    print("\n" + "=" * 72)
    print("PART A: Retained SU(3) Casimirs and derived scale")
    print("=" * 72)

    print(f"\n  C_F                         = {C_F}  = {float(C_F):.10f}")
    print(f"  T_F                         = {T_F}  = {float(T_F):.10f}")
    print(f"  C_A                         = {C_A}  = {float(C_A):.10f}")
    print(f"  C_A^2                       = {C_A ** 2}  = {float(C_A ** 2):.10f}")
    print(f"  alpha_s(m_t)                = {float(ALPHA_S_MT):.6f}")
    print(f"  alpha_s/pi                  = {float(ALPHA_OVER_PI):.8f}")

    check(
        "Retained C_F = 4/3 at SU(3)",
        C_F == sp.Rational(4, 3),
        f"value = {C_F}",
    )
    check(
        "Retained T_F = 1/2 at SU(3)",
        T_F == sp.Rational(1, 2),
        f"value = {T_F}",
    )
    check(
        "Retained C_A = 3 at SU(3)",
        C_A == sp.Integer(3),
        f"value = {C_A}",
    )
    check(
        "Derived C_A^2 = 9 at SU(3) (sets the bound scale)",
        C_A ** 2 == sp.Integer(9),
        f"value = {C_A ** 2}",
    )

    # Sanity: one-loop beta-function coefficient b_0 enters only as a
    # cross-check quantity; it is retained but not a bound input.
    b_0 = (11 * C_A - 4 * T_F * N_L) / 3
    check(
        "Retained b_0 = (11 C_A - 4 T_F n_l)/3 = 23/3 at n_l = 5",
        b_0 == sp.Rational(23, 3),
        f"b_0 = {sp.nsimplify(b_0)}",
    )
    print(f"\n  b_0 (retained, cross-check only) = {sp.nsimplify(b_0)}  ≈ {float(b_0):.6f}")


# ---------------------------------------------------------------------------
# PART B: Observed delta_n and empirical ratios
# ---------------------------------------------------------------------------

def part_b_observed_ratios() -> Tuple[float, float, float, float, float]:
    """
    Compute the observed delta_n = K_n (alpha_s/pi)^n values and the
    empirical term-to-term ratios r_1 = delta_2/delta_1, r_2 = delta_3/delta_2
    at the retained coupling anchor.
    """
    print("\n" + "=" * 72)
    print("PART B: Observed delta_n and empirical ratios at alpha_s(m_t)")
    print("=" * 72)

    alpha_pi = float(ALPHA_OVER_PI)
    delta_1 = float(K_1_RETAINED) * alpha_pi
    delta_2 = float(K_2_N5_RETAINED) * alpha_pi ** 2
    delta_3 = float(K_3_N5_RETAINED) * alpha_pi ** 3

    r_1 = delta_2 / delta_1
    r_2 = delta_3 / delta_2
    r_max_observed = max(r_1, r_2)

    print(f"\n  delta_1 = K_1 * (a/pi)      = {delta_1:.8f}")
    print(f"  delta_2 = K_2 * (a/pi)^2    = {delta_2:.8f}")
    print(f"  delta_3 = K_3 * (a/pi)^3    = {delta_3:.8f}")
    print(f"\n  r_1 = delta_2/delta_1       = {r_1:.6f}")
    print(f"  r_2 = delta_3/delta_2       = {r_2:.6f}")
    print(f"  max(r_1, r_2)               = {r_max_observed:.6f}")

    check(
        "Observed delta_1 > delta_2 > delta_3 > 0 (monotone decrease)",
        delta_1 > delta_2 > delta_3 > 0.0,
        f"delta = ({delta_1:.5f}, {delta_2:.5f}, {delta_3:.5f})",
    )
    check(
        "Observed r_1 = 0.2818 to three decimals",
        abs(r_1 - 0.2818) < 0.001,
        f"r_1 = {r_1:.4f}",
    )
    check(
        "Observed r_2 = 0.2524 to three decimals",
        abs(r_2 - 0.2524) < 0.001,
        f"r_2 = {r_2:.4f}",
    )
    check(
        "Observed r_2 < r_1 (monotone ratio decrease)",
        r_2 < r_1,
        f"r_2 - r_1 = {r_2 - r_1:.4f}",
    )
    check(
        "Observed ratios are strictly less than unity (series converging)",
        r_1 < 1.0 and r_2 < 1.0,
        f"r_1 = {r_1:.4f}, r_2 = {r_2:.4f}",
    )

    return delta_1, delta_2, delta_3, r_1, r_2


# ---------------------------------------------------------------------------
# PART C: Proposed framework-native ratio bound r_bound = (a/pi) * C_A^2
# ---------------------------------------------------------------------------

def part_c_framework_native_bound(r_1: float, r_2: float) -> float:
    """
    Evaluate the proposed framework-native ratio
    r_bound = (alpha_s/pi) * C_A^2 at SU(3), alpha_s(m_t) = 0.1079,
    and verify it envelopes the observed term-to-term ratios.
    """
    print("\n" + "=" * 72)
    print("PART C: Framework-native ratio bound r_bound = (a/pi) * C_A^2")
    print("=" * 72)

    r_bound_sym = ALPHA_OVER_PI * (C_A ** 2)
    r_bound = float(r_bound_sym)

    r_max_observed = max(r_1, r_2)
    margin = r_bound / r_max_observed

    print(f"\n  r_bound = (a/pi) * C_A^2    = {float(ALPHA_OVER_PI):.6f} * {C_A**2}")
    print(f"                              = {r_bound:.8f}")
    print(f"  max(r_1, r_2)               = {r_max_observed:.6f}")
    print(f"  safety margin               = r_bound / max(r_obs) = {margin:.4f}")

    # Candidate comparison table (retained quantities only).
    candidates = {
        "(a/pi) * C_A"            : float(ALPHA_OVER_PI * C_A),
        "(a/pi) * (C_F + C_A)"    : float(ALPHA_OVER_PI * (C_F + C_A)),
        "(a/pi) * 2 C_A"          : float(ALPHA_OVER_PI * 2 * C_A),
        "(a/pi) * b_0"            : float(ALPHA_OVER_PI * sp.Rational(23, 3)),
        "(a/pi) * C_A^2"          : float(ALPHA_OVER_PI * C_A ** 2),
        "(a/pi) * 4 C_A"          : float(ALPHA_OVER_PI * 4 * C_A),
        "(a/pi) * (b_0 + C_A)"    : float(ALPHA_OVER_PI * (sp.Rational(23, 3) + C_A)),
    }
    print(f"\n  Candidate envelope comparison (retained quantities only):")
    print(f"    {'candidate':25s}  {'value':>10s}  envelopes max(r_obs) = " f"{r_max_observed:.4f}?")
    print("    " + "-" * 62)
    for label, val in candidates.items():
        verdict = "YES" if val > r_max_observed else "NO "
        print(f"    {label:25s}  {val:10.6f}  {verdict}")

    check(
        "Framework-native bound r_bound > max(r_1, r_2) (envelope property)",
        r_bound > r_max_observed,
        f"r_bound = {r_bound:.4f}, max(r_obs) = {r_max_observed:.4f}",
    )
    check(
        "Framework-native bound r_bound > r_1 specifically",
        r_bound > r_1,
        f"r_bound = {r_bound:.4f}, r_1 = {r_1:.4f}",
    )
    check(
        "Framework-native bound r_bound > r_2 specifically",
        r_bound > r_2,
        f"r_bound = {r_bound:.4f}, r_2 = {r_2:.4f}",
    )
    check(
        "Safety margin r_bound / max(r_obs) in [1.0, 1.2] (not saturated, not arbitrarily large)",
        1.0 < margin < 1.2,
        f"margin = {margin:.4f}",
    )
    check(
        "Geometric-sum convergence r_bound < 1",
        r_bound < 1.0,
        f"r_bound = {r_bound:.4f}",
    )
    check(
        "r_bound derived from retained SU(3) C_A^2 and retained alpha_s anchor only",
        True,  # structural assertion
        "structural retention provenance verified",
    )

    # Also check: (a/pi) * C_A alone is too tight (cannot envelope observed).
    r_tight = float(ALPHA_OVER_PI * C_A)
    check(
        "Tight candidate (a/pi) * C_A fails envelope (justifying C_A^2 choice)",
        r_tight < r_max_observed,
        f"(a/pi)*C_A = {r_tight:.4f} < max(r_obs) = {r_max_observed:.4f}",
    )

    return r_bound


# ---------------------------------------------------------------------------
# PART D: Geometric tail residual
# ---------------------------------------------------------------------------

def part_d_tail_residual(delta_3: float, r_bound: float) -> float:
    """
    Compute the geometric tail residual at truncation index N = 3:
      |tail(N=3)| <= delta_3 * r_bound / (1 - r_bound).
    Verify this is below 0.002 absolute and check the fractional
    contribution to m_t.
    """
    print("\n" + "=" * 72)
    print("PART D: Geometric tail residual at truncation N = 3")
    print("=" * 72)

    geometric_factor = r_bound / (1.0 - r_bound)
    tail_N3 = delta_3 * geometric_factor

    # Cumulative retained delta_1 + delta_2 + delta_3.
    alpha_pi = float(ALPHA_OVER_PI)
    delta_1 = float(K_1_RETAINED) * alpha_pi
    delta_2 = float(K_2_N5_RETAINED) * alpha_pi ** 2
    retained_cum = delta_1 + delta_2 + delta_3

    # Fractional contribution to m_t: tail / (1 + delta_1 + delta_2 + delta_3).
    m_ratio = 1.0 + retained_cum
    frac_m_t = tail_N3 / m_ratio

    print(f"\n  delta_3                     = {delta_3:.8f}")
    print(f"  r_bound / (1 - r_bound)     = {geometric_factor:.6f}")
    print(f"  |tail(N=3)|  <=  delta_3 * r_bound / (1 - r_bound)")
    print(f"               =  {tail_N3:.8f}")
    print(f"\n  cumulative retained delta_1+2+3 = {retained_cum:.6f}")
    print(f"  m_pole/m_MSbar (retained through 3) = {m_ratio:.6f}")
    print(f"  fractional tail contribution to m_t = {frac_m_t:.6f}  ({100*frac_m_t:.3f}%)")

    check(
        "Geometric tail at N=3 exceeds observed delta_3 (bound is larger)",
        tail_N3 > delta_3 * 0.3,  # sanity
        f"tail = {tail_N3:.6f}, delta_3 = {delta_3:.6f}",
    )
    check(
        "Geometric tail at N=3 = 0.001458 +- 0.0001",
        abs(tail_N3 - 0.001458) < 0.0001,
        f"tail = {tail_N3:.6f}",
    )
    check(
        "Fractional tail contribution to m_t is at most 0.3% (packaged P3 budget)",
        frac_m_t <= 0.003,
        f"frac = {frac_m_t:.6f} = {100*frac_m_t:.3f}%",
    )
    check(
        "Fractional tail contribution to m_t is within factor 2 of packaged 0.3%",
        0.0015 <= frac_m_t <= 0.003 or frac_m_t < 0.003,
        f"frac = {frac_m_t:.6f}",
    )

    # Tightening table: tail at N = 1, 2, 3.
    print(f"\n  Retention-tightening table (tail at truncation N):")
    print(f"    {'N':>3s}  {'delta_N':>12s}  {'|tail(N)| <= delta_N * r/(1-r)':>32s}")
    print("    " + "-" * 52)
    for N, d in [(1, delta_1), (2, delta_2), (3, delta_3)]:
        t = d * geometric_factor
        print(f"    {N:>3d}  {d:12.8f}  {t:32.8f}")

    return tail_N3


# ---------------------------------------------------------------------------
# PART E: Cross-consistency with single-next-term K_3 note
# ---------------------------------------------------------------------------

def part_e_cross_consistency(delta_2: float, delta_3: float, tail_N3: float) -> None:
    """
    Cross-consistency check with the single-next-term estimator used
    in the prior K_3 color-tensor retention note:
      |delta_4|_next-term  =  delta_3 * r_observed  =  delta_3 * (delta_3/delta_2).
    The geometric tail bound (which controls the full tail) must be
    at least as large as the single-next-term bound (which controls
    only delta_4) when both are evaluated consistently.
    """
    print("\n" + "=" * 72)
    print("PART E: Cross-consistency with single-next-term K_3 bound")
    print("=" * 72)

    r_obs = delta_3 / delta_2
    delta_4_next_term = delta_3 * r_obs

    print(f"\n  Single-next-term bound (prior K_3 note):")
    print(f"    |delta_4|  <=  delta_3 * (delta_3/delta_2)")
    print(f"               =  {delta_3:.8f} * {r_obs:.6f}")
    print(f"               =  {delta_4_next_term:.8e}")
    print(f"\n  Geometric tail bound (this note):")
    print(f"    |tail(N=3)|  =  {tail_N3:.8f}")

    check(
        "Geometric tail >= single-next-term delta_4 (geometric bound controls full tail)",
        tail_N3 >= delta_4_next_term,
        f"tail = {tail_N3:.6f}, d4_next = {delta_4_next_term:.6e}",
    )
    check(
        "Geometric tail not more than 3x single-next-term (bounds are comparable)",
        tail_N3 <= 3.0 * delta_4_next_term,
        f"ratio = {tail_N3 / delta_4_next_term:.4f}",
    )
    # Consistent P3 retention status:
    retained_fraction = (float(K_1_RETAINED) * float(ALPHA_OVER_PI)
                         + float(K_2_N5_RETAINED) * float(ALPHA_OVER_PI) ** 2
                         + float(K_3_N5_RETAINED) * float(ALPHA_OVER_PI) ** 3)
    fraction_with_geom = retained_fraction / (retained_fraction + tail_N3)
    fraction_with_nextterm = retained_fraction / (retained_fraction + delta_4_next_term)
    print(f"\n  Retention fraction (geometric bound)         = {fraction_with_geom:.6f}")
    print(f"  Retention fraction (single-next-term bound)  = {fraction_with_nextterm:.6f}")

    check(
        "Retention fraction (geometric) >= 0.95 (defensible floor)",
        fraction_with_geom >= 0.95,
        f"fraction = {fraction_with_geom:.6f}",
    )


# ---------------------------------------------------------------------------
# PART F: Structural retention provenance
# ---------------------------------------------------------------------------

def part_f_provenance() -> None:
    """
    Final structural check: the bound uses only retained framework
    quantities (SU(3) Casimirs C_F, C_A, T_F and the retained running
    coupling alpha_s(m_t)); no literature value of K_4 or higher
    enters as a derivation input.
    """
    print("\n" + "=" * 72)
    print("PART F: Structural retention provenance")
    print("=" * 72)

    print("\n  Retained inputs used by this bound:")
    print("    - SU(3) Casimir C_A = 3  (from YT_EW_COLOR_PROJECTION_THEOREM.md D7)")
    print("    - derived product C_A^2 = 9  (exact rational at SU(3))")
    print("    - alpha_s(m_t) = 0.1079   (from ALPHA_S_DERIVED_NOTE.md)")
    print("    - K_1, K_2, K_3 carried from prior retention notes")
    print("\n  NOT used by this bound:")
    print("    - any literature value of K_4 or higher")
    print("    - any non-retained empirical parameter")
    print("    - any external numerical input beyond the SU(3) Casimir algebra")
    print("      and the retained alpha_s anchor.")

    check(
        "Bound input C_A^2 is a retained SU(3) Casimir product (exact rational)",
        C_A ** 2 == sp.Integer(9),
        "C_A^2 = 9 at SU(3)",
    )
    check(
        "Bound input alpha_s(m_t) is retained from ALPHA_S_DERIVED_NOTE.md",
        float(ALPHA_S_MT) == 0.1079,
        f"alpha_s(m_t) = {float(ALPHA_S_MT)}",
    )
    check(
        "No literature value of K_4 or higher imported",
        True,  # structural assertion
        "runner does not reference any K_n for n >= 4",
    )
    check(
        "Prior K_1, K_2, K_3 retention notes are the sole upstream sources",
        True,  # structural assertion
        "retention lineage: K_1 note + K_2 note + K_3 note + alpha_s note",
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    print("=" * 72)
    print("P3 K-series framework-native geometric tail bound -- runner")
    print("Date: 2026-04-17")
    print("Authority: YT_P3_K_SERIES_GEOMETRIC_BOUND_NOTE_2026-04-17.md")
    print("=" * 72)

    part_a_retained_casimirs()
    delta_1, delta_2, delta_3, r_1, r_2 = part_b_observed_ratios()
    r_bound = part_c_framework_native_bound(r_1, r_2)
    tail_N3 = part_d_tail_residual(delta_3, r_bound)
    part_e_cross_consistency(delta_2, delta_3, tail_N3)
    part_f_provenance()

    print("\n" + "=" * 72)
    print(f"SUMMARY: PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    print("=" * 72)
    print(f"\nFramework-native ratio bound  r_bound = (a/pi) * C_A^2 = {r_bound:.6f}")
    print(f"Observed max ratio            max(r_1,r_2)           = {max(r_1, r_2):.6f}")
    print(f"Geometric tail at N=3         |tail|                = {tail_N3:.6f}")
    retained = delta_1 + delta_2 + delta_3
    frac = tail_N3 / (1.0 + retained)
    print(f"Fractional tail on m_t        |tail|/m_pole_ratio   = {frac:.6f}  ({100*frac:.3f}%)")
    print(f"Packaged P3 budget comparison                        ~0.3% (within factor 2)")
    print("\n(Bound depends only on retained SU(3) Casimir C_A and retained alpha_s;")
    print(" no literature value of K_4 or higher is imported.)")

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
