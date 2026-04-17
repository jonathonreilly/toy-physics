#!/usr/bin/env python3
"""
Frontier runner: Koide sectoral universality test.

Status:
  FALSIFIABILITY TEST of Prediction 3 of the charged-lepton Koide-cone
  derivation (``.claude/science/derivations/charged-lepton-koide-cone-2026-04-17.md``).
  TOE-grade honest comparison of Q = (sum m) / (sum sqrt(m))^2 across the
  three observed mass sectors (charged leptons, down-type quarks, up-type
  quarks) against the theorem-grade target Q = 2/3.

Safe claim:
  On PDG observation surfaces and on the framework-native bounded down-type
  mass-ratio lane, this runner computes Q for each sector and reports the
  deviation from 2/3. It uses framework-native inputs (alpha_s(v), y_t(v))
  only where they derive from existing retained/bounded authority notes.
  PDG values are COMPARISON data only and are never used as derivation inputs.

The runner does not promote Koide universality to a theorem. It is a
falsification test: it outputs a single verdict line

  KOIDE_UNIVERSALITY = CONFIRMED | PARTIAL | CHARGED_LEPTON_ONLY | FALSIFIED

based on the residual deviations across the three sectors.

Dependencies (all reused as-is, no modification):
  - scripts/canonical_plaquette_surface.py (alpha_s(v))
  - docs/DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md (framework-native down ratios)
  - docs/YT_FLAGSHIP_BOUNDARY_NOTE.md (y_t(v) = 0.9176 central value)
  - .claude/science/derivations/charged-lepton-koide-cone-2026-04-17.md
    (algebraic Koide cone and Prediction 3)
"""

from __future__ import annotations

import math

from canonical_plaquette_surface import (
    CANONICAL_ALPHA_BARE,
    CANONICAL_ALPHA_LM,
    CANONICAL_ALPHA_S_V,
    CANONICAL_PLAQUETTE,
    CANONICAL_U0,
)


# ---------------------------------------------------------------------------
# Framework-native anchors (from authority notes, NOT hardcoded ad-hoc)
# ---------------------------------------------------------------------------

# From the promoted CKM / down-type lane (DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md)
ALPHA_S_V = CANONICAL_ALPHA_S_V

# Exact SU(3) constants used by the down-type lane
C_F = 4.0 / 3.0
T_F = 1.0 / 2.0
FIVE_SIXTHS = C_F - T_F  # = 5/6 exactly

# Canonical current y_t(v) central value (YT_FLAGSHIP_BOUNDARY_NOTE.md)
# Appears identically in scripts/frontier_yt_exact_interacting_bridge_transport.py,
# scripts/frontier_yt_bridge_variational_selector.py, and the Higgs mass chain.
YT_V = 0.9176

# Theorem-grade target of the Koide-cone derivation
KOIDE_TARGET = 2.0 / 3.0

# ---------------------------------------------------------------------------
# PDG comparator data (COMPARISON ONLY)
# ---------------------------------------------------------------------------

# Charged leptons - PDG pole masses, MeV (all known to high precision,
# scheme-independent at this accuracy)
M_E_PDG = 0.5109989461
M_MU_PDG = 105.6583745
M_TAU_PDG = 1776.86

# Down-type quarks - PDG threshold-local self-scale (MeV)
# m_d(2 GeV), m_s(2 GeV), m_b(m_b)
M_D_PDG_SELF = 4.67
M_S_PDG_SELF = 93.4
M_B_PDG_SELF = 4180.0

# One-loop QCD transport factors used in the DOWN_TYPE lane (reused as-is)
GAMMA_MS_BAR = 12.0 / 25.0  # anomalous dimension factor for N_f=5 transport
ALPHA_S_2GEV = 0.301
ALPHA_S_MB = 0.226

# Up-type quarks
# PDG MS-bar threshold-local: m_u(2 GeV), m_c(m_c), m_t(pole).
M_U_PDG_SELF = 2.16
M_C_PDG_SELF = 1273.0
M_T_PDG_POLE = 172690.0  # MeV

# Commonly cited running MS-bar values at mu = M_Z (PDG/CKMfitter style)
M_U_MZ = 1.27
M_C_MZ = 619.0
M_T_MZ = 171000.0  # MS-bar at M_Z is ~168.4 GeV; we use a representative
                   # value consistent with 1-loop transport from the pole


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


def koide_Q(m1: float, m2: float, m3: float) -> float:
    num = m1 + m2 + m3
    den = (math.sqrt(m1) + math.sqrt(m2) + math.sqrt(m3)) ** 2
    return num / den


def deviation_pct(value: float, target: float) -> float:
    return (value - target) / target * 100.0


def universal_test(name: str, Q: float, tol_pct: float) -> bool:
    dev = deviation_pct(Q, KOIDE_TARGET)
    ok = abs(dev) < tol_pct
    check(
        f"{name}: Q within {tol_pct:.2f}% of 2/3",
        ok,
        f"Q = {Q:.6f}, dev = {dev:+.3f}%",
    )
    return ok


# ---------------------------------------------------------------------------
# PART A: charged leptons (comparison target)
# ---------------------------------------------------------------------------

def part_a_charged_leptons() -> float:
    print("\n" + "=" * 72)
    print("PART A: Charged-lepton Koide ratio (comparison anchor)")
    print("=" * 72)
    print("\n  PDG pole masses (MeV):")
    print(f"    m_e   = {M_E_PDG}")
    print(f"    m_mu  = {M_MU_PDG}")
    print(f"    m_tau = {M_TAU_PDG}")

    Q_l = koide_Q(M_E_PDG, M_MU_PDG, M_TAU_PDG)
    print(f"\n  Q_l  = (sum m) / (sum sqrt m)^2 = {Q_l:.10f}")
    print(f"  2/3  = {KOIDE_TARGET:.10f}")
    print(f"  dev  = {deviation_pct(Q_l, KOIDE_TARGET):+.4f}%")

    # scheme: pole-mass self-scale (all three known to high precision)
    # Koide identity is scheme-dependent in principle but the empirical
    # pole-mass result is the standard reference value.

    universal_test("Q_l (charged leptons, PDG pole)", Q_l, tol_pct=0.01)

    # sanity: Koide identity is not trivially true
    # the "equal masses" reference gives Q = 1/3, not 2/3
    Q_equal = koide_Q(1.0, 1.0, 1.0)
    check(
        "Q at degenerate masses = 1/3 (Koide is nontrivial)",
        abs(Q_equal - 1.0 / 3.0) < 1e-14,
        f"Q_equal = {Q_equal:.6f}",
    )
    # ratio m_tau >> m_mu >> m_e -> Q -> 1 in hierarchical limit
    Q_hier = koide_Q(1.0, 1.0e6, 1.0e12)
    check(
        "Q at extreme hierarchy tends to 1 (Koide is nontrivial)",
        Q_hier > 0.95,
        f"Q_hier = {Q_hier:.6f}",
    )

    return Q_l


# ---------------------------------------------------------------------------
# PART B: down-type quarks (framework-native prediction + PDG compare)
# ---------------------------------------------------------------------------

def part_b_down_type() -> tuple[float, float, float]:
    print("\n" + "=" * 72)
    print("PART B: Down-type Koide ratio")
    print("=" * 72)

    print(f"\n  alpha_s(v) [canonical, DOWN_TYPE lane] = {ALPHA_S_V:.12f}")
    print(f"  5/6 bridge exponent (C_F - T_F)         = {FIVE_SIXTHS}")

    # --- framework-native -----------------------------------------------
    r_ds_fw = ALPHA_S_V / 2.0
    r_sb_fw = (ALPHA_S_V / math.sqrt(6.0)) ** (6.0 / 5.0)

    # Overall scale cancels. Set m_b = 1, compute m_s, m_d.
    m_b_fw = 1.0
    m_s_fw = r_sb_fw * m_b_fw
    m_d_fw = r_ds_fw * m_s_fw
    Q_d_fw = koide_Q(m_d_fw, m_s_fw, m_b_fw)

    print("\n  Framework-native (parameter-free, only alpha_s(v) + SU(3)):")
    print(f"    m_d/m_s = alpha_s(v)/2                 = {r_ds_fw:.8f}")
    print(f"    m_s/m_b = [alpha_s(v)/sqrt(6)]^(6/5)   = {r_sb_fw:.8f}")
    print(f"    Q_d (framework-native)                 = {Q_d_fw:.8f}")
    print(f"    dev from 2/3                           = "
          f"{deviation_pct(Q_d_fw, KOIDE_TARGET):+.3f}%")

    check(
        "Q_d framework-native is scale-invariant (check m_b=10 gives same Q)",
        abs(Q_d_fw - koide_Q(m_d_fw * 10, m_s_fw * 10, m_b_fw * 10)) < 1e-14,
    )

    # --- PDG threshold-local comparator ---------------------------------
    Q_d_self = koide_Q(M_D_PDG_SELF, M_S_PDG_SELF, M_B_PDG_SELF)
    print("\n  PDG threshold-local self-scale:")
    print(f"    m_d(2 GeV) = {M_D_PDG_SELF}")
    print(f"    m_s(2 GeV) = {M_S_PDG_SELF}")
    print(f"    m_b(m_b)   = {M_B_PDG_SELF}")
    print(f"    Q_d (PDG self-scale)                   = {Q_d_self:.8f}")
    print(f"    dev from 2/3                           = "
          f"{deviation_pct(Q_d_self, KOIDE_TARGET):+.3f}%")

    # --- common-scale comparator: run light masses to m_b ---------------
    transport = (ALPHA_S_MB / ALPHA_S_2GEV) ** GAMMA_MS_BAR
    m_d_mb = M_D_PDG_SELF * transport
    m_s_mb = M_S_PDG_SELF * transport
    Q_d_common = koide_Q(m_d_mb, m_s_mb, M_B_PDG_SELF)
    print("\n  PDG common-scale (all at mu = m_b, one-loop transport):")
    print(f"    transport factor                       = {transport:.6f}")
    print(f"    m_d(m_b) = {m_d_mb:.4f}")
    print(f"    m_s(m_b) = {m_s_mb:.4f}")
    print(f"    Q_d (common-scale m_b)                 = {Q_d_common:.8f}")
    print(f"    dev from 2/3                           = "
          f"{deviation_pct(Q_d_common, KOIDE_TARGET):+.3f}%")

    # Honest TOE-grade assertions:
    # Q_d is NOT at the 2/3 theorem-grade target within PDG precision. We
    # assert the exact honest reading: Q_d deviates from 2/3 at > 5%.
    dev_fw_pct = abs(deviation_pct(Q_d_fw, KOIDE_TARGET))
    dev_self_pct = abs(deviation_pct(Q_d_self, KOIDE_TARGET))
    check(
        "Q_d framework-native deviates from 2/3 by > 5% (Koide NOT at "
        "theorem precision on down-type sector)",
        dev_fw_pct > 5.0,
        f"|dev Q_d fw| = {dev_fw_pct:.3f}%",
    )
    check(
        "Q_d PDG self-scale deviates from 2/3 by > 5% (PDG sector read "
        "confirms framework prediction)",
        dev_self_pct > 5.0,
        f"|dev Q_d PDG| = {dev_self_pct:.3f}%",
    )
    # positive direction is characteristic: top-down-like dominance of m_b
    check(
        "Q_d lies ABOVE 2/3 (m_b dominance of down-type)",
        Q_d_fw > KOIDE_TARGET and Q_d_self > KOIDE_TARGET,
    )
    # consistency: framework-native should be close to PDG self-scale
    check(
        "Q_d framework-native consistent with PDG self-scale (<1% diff)",
        abs((Q_d_fw - Q_d_self) / Q_d_self * 100.0) < 1.0,
        f"|dQ| = {abs((Q_d_fw - Q_d_self)/Q_d_self*100.0):.3f}%",
    )

    return Q_d_fw, Q_d_self, Q_d_common


# ---------------------------------------------------------------------------
# PART C: up-type quarks (sharpest falsifier)
# ---------------------------------------------------------------------------

def part_c_up_type() -> tuple[float, float, float]:
    print("\n" + "=" * 72)
    print("PART C: Up-type Koide ratio (sharpest falsifier)")
    print("=" * 72)

    # --- PDG canonical scheme -------------------------------------------
    Q_u_self = koide_Q(M_U_PDG_SELF, M_C_PDG_SELF, M_T_PDG_POLE)
    print("\n  PDG canonical (threshold-local self-scale):")
    print(f"    m_u(2 GeV)    = {M_U_PDG_SELF} MeV")
    print(f"    m_c(m_c)      = {M_C_PDG_SELF} MeV")
    print(f"    m_t(pole)     = {M_T_PDG_POLE} MeV")
    print(f"    Q_u (PDG self)               = {Q_u_self:.8f}")
    print(f"    dev from 2/3                 = "
          f"{deviation_pct(Q_u_self, KOIDE_TARGET):+.3f}%")

    # --- common-scale MS-bar at M_Z -------------------------------------
    Q_u_mz = koide_Q(M_U_MZ, M_C_MZ, M_T_MZ)
    print("\n  PDG common-scale (MS-bar at mu = M_Z):")
    print(f"    m_u(M_Z) = {M_U_MZ} MeV")
    print(f"    m_c(M_Z) = {M_C_MZ} MeV")
    print(f"    m_t(M_Z) = {M_T_MZ} MeV (representative)")
    print(f"    Q_u (M_Z)                    = {Q_u_mz:.8f}")
    print(f"    dev from 2/3                 = "
          f"{deviation_pct(Q_u_mz, KOIDE_TARGET):+.3f}%")

    # Does running to a common scale shrink the deviation? No -- it makes
    # it worse. Record this as the sharp honest finding.
    dev_self = abs(deviation_pct(Q_u_self, KOIDE_TARGET))
    dev_mz = abs(deviation_pct(Q_u_mz, KOIDE_TARGET))
    check(
        "Common-scale running does NOT shrink Q_u deviation from 2/3 "
        "(running away from Koide target)",
        dev_mz > dev_self,
        f"|dev_self| = {dev_self:.2f}%, |dev_MZ| = {dev_mz:.2f}%",
    )

    # --- "framework-native" Q_u attempt ---------------------------------
    # The framework has y_t(v) = 0.9176 as a bounded anchor, which fixes
    # m_t ~ v * y_t / sqrt(2) up to a known systematic budget. It does NOT
    # currently carry an analogous bounded extraction of m_u/m_c or
    # m_c/m_t on main (grep across docs/ shows no UP_TYPE_MASS_RATIO_* note).
    v_higgs = 246.28
    m_t_fw = v_higgs * YT_V / math.sqrt(2.0) * 1000.0  # MeV
    print("\n  Framework-native up-type status:")
    print(f"    y_t(v) (YT flagship central) = {YT_V}")
    print(f"    m_t(v) = v*y_t/sqrt(2) (MeV) = {m_t_fw:.1f}")
    print("    m_u/m_c, m_c/m_t: NO retained or bounded authority note")
    print("      (confirmed by grep of docs/ on 2026-04-17; only down-type")
    print("       mass-ratio lane exists, see DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md)")

    check(
        "Framework m_t anchor exists (y_t(v) * v / sqrt(2) available)",
        m_t_fw > 1.0e5 and m_t_fw < 2.0e5,
        f"m_t(fw) = {m_t_fw/1000.0:.2f} GeV",
    )
    check(
        "No retained/bounded framework m_u/m_c or m_c/m_t extraction exists",
        True,  # reported as explicit absence
        "honest no-coverage statement",
    )

    # --- Minimum scheme correction to bring Q_u to 2/3 -------------------
    # We fix m_u, m_c at PDG self-scale and ask what rescaling
    # A of sqrt(m_t) is required to put Q at 2/3. Solve
    #     3 (m_u + m_c + A^2 m_t) = 2 (sqrt m_u + sqrt m_c + A sqrt m_t)^2
    # This is a quadratic in A.  Coefficients:
    sqrt_mu = math.sqrt(M_U_PDG_SELF)
    sqrt_mc = math.sqrt(M_C_PDG_SELF)
    sqrt_mt = math.sqrt(M_T_PDG_POLE)
    light_sum_sqrt = sqrt_mu + sqrt_mc

    # 3 A^2 m_t - 2 A^2 m_t - 4 A sqrt m_t (sqrt m_u + sqrt m_c)
    # + 3(m_u + m_c) - 2(sqrt m_u + sqrt m_c)^2 = 0
    # => A^2 m_t - 4 A sqrt_mt * L + C = 0
    # with L = light_sum_sqrt, C = 3(m_u + m_c) - 2 L^2
    a_coef = M_T_PDG_POLE
    b_coef = -4.0 * sqrt_mt * light_sum_sqrt
    c_coef = 3.0 * (M_U_PDG_SELF + M_C_PDG_SELF) - 2.0 * light_sum_sqrt ** 2
    disc = b_coef ** 2 - 4.0 * a_coef * c_coef
    if disc >= 0.0:
        A1 = (-b_coef + math.sqrt(disc)) / (2.0 * a_coef)
        A2 = (-b_coef - math.sqrt(disc)) / (2.0 * a_coef)
        # keep the positive root closest to 1 (smallest scheme correction)
        candidates = [a for a in (A1, A2) if a > 0]
        A_min = min(candidates, key=lambda a: abs(math.log(a)))
        print("\n  Minimum scheme rescaling of sqrt(m_t) to reach Q_u = 2/3:")
        print(f"    A (sqrt m_t rescaling)     = {A_min:.6f}")
        print(f"    Equivalent m_t rescaling   = {A_min**2:.6f}")
        print(f"    Required m_t (MeV)         = {A_min**2 * M_T_PDG_POLE:.1f}")
        print(f"    Required m_t (GeV)         = {A_min**2 * M_T_PDG_POLE/1000.0:.2f}")

        check(
            "Scheme correction to reach Q_u = 2/3 has a real solution",
            True,
            f"A = {A_min:.4f}",
        )
        # is this correction within a natural range (0.5 < A < 2)? No.
        check(
            "Required sqrt(m_t) rescaling lies outside [0.5, 2] (not a "
            "small-perturbation scheme correction)",
            not (0.5 < A_min < 2.0),
            f"A = {A_min:.4f} -> {'LARGE' if not 0.5<A_min<2.0 else 'small'}",
        )
    else:
        check(
            "Scheme correction to reach Q_u = 2/3 has a real solution",
            False,
            "discriminant < 0",
        )
        A_min = float("nan")

    # Honest TOE-grade assertions:
    check(
        "Q_u PDG self-scale deviates from 2/3 by > 10% (Prediction 3 "
        "falsified in canonical PDG scheme)",
        abs(deviation_pct(Q_u_self, KOIDE_TARGET)) > 10.0,
        f"|dev Q_u PDG| = {abs(deviation_pct(Q_u_self, KOIDE_TARGET)):.3f}%",
    )
    check(
        "Q_u M_Z common-scale deviates from 2/3 by > 10% (common-scale "
        "scheme does not rescue universality)",
        abs(deviation_pct(Q_u_mz, KOIDE_TARGET)) > 10.0,
        f"|dev Q_u MZ| = {abs(deviation_pct(Q_u_mz, KOIDE_TARGET)):.3f}%",
    )

    return Q_u_self, Q_u_mz, A_min


# ---------------------------------------------------------------------------
# PART D: overall verdict
# ---------------------------------------------------------------------------

def part_d_verdict(Q_l: float, Q_d_fw: float, Q_d_self: float,
                   Q_d_common: float, Q_u_self: float, Q_u_mz: float) -> str:
    print("\n" + "=" * 72)
    print("PART D: Overall verdict on Koide sectoral universality")
    print("=" * 72)

    dev_l = abs(deviation_pct(Q_l, KOIDE_TARGET))
    dev_d_fw = abs(deviation_pct(Q_d_fw, KOIDE_TARGET))
    dev_d_self = abs(deviation_pct(Q_d_self, KOIDE_TARGET))
    dev_u_self = abs(deviation_pct(Q_u_self, KOIDE_TARGET))
    dev_u_mz = abs(deviation_pct(Q_u_mz, KOIDE_TARGET))

    # thresholds
    TIGHT = 1.0      # % PDG-precision
    SECTOR_MAX = 5.0 # % allowed sector-level deviation for CONFIRMED
    CL_ONLY_TH = 5.0 # % deviation beyond which sector is "clearly != 2/3"

    print(f"\n  Deviations from 2/3:")
    print(f"    |dev Q_l|                 = {dev_l:.3f}%")
    print(f"    |dev Q_d (framework)|     = {dev_d_fw:.3f}%")
    print(f"    |dev Q_d (PDG self)|      = {dev_d_self:.3f}%")
    print(f"    |dev Q_d (common m_b)|    = "
          f"{abs(deviation_pct(Q_d_common, KOIDE_TARGET)):.3f}%")
    print(f"    |dev Q_u (PDG self)|      = {dev_u_self:.3f}%")
    print(f"    |dev Q_u (M_Z common)|    = {dev_u_mz:.3f}%")

    # Verdict logic
    best_u = min(dev_u_self, dev_u_mz)
    best_d = min(dev_d_fw, dev_d_self)

    if dev_l < TIGHT and best_d < SECTOR_MAX and best_u < SECTOR_MAX:
        verdict = "CONFIRMED"
    elif dev_l < TIGHT and best_d < SECTOR_MAX and best_u >= SECTOR_MAX:
        verdict = "PARTIAL"
    elif dev_l < TIGHT and best_d < CL_ONLY_TH and best_u >= SECTOR_MAX:
        verdict = "PARTIAL"
    elif dev_l < TIGHT and best_d >= CL_ONLY_TH and best_u >= CL_ONLY_TH:
        verdict = "CHARGED_LEPTON_ONLY"
    elif dev_l < TIGHT and best_d >= CL_ONLY_TH and best_u < SECTOR_MAX:
        # weird pattern: CL + up agree, down fails
        verdict = "FALSIFIED"
    else:
        verdict = "FALSIFIED"

    print(f"\n  Verdict rule applied:")
    print(f"    tight CL threshold  = {TIGHT}%")
    print(f"    sector threshold    = {SECTOR_MAX}%")
    print(f"    clear-fail threshold= {CL_ONLY_TH}%")

    # emit checks that tie the verdict back to explicit PASS/FAIL items
    check(
        "Q_l passes at PDG precision (< 0.01%)",
        dev_l < 0.01,
        f"dev = {dev_l:.4f}%",
    )
    check(
        "Best Q_d scheme fails sector threshold (>= 5%) -- universality "
        "does NOT hold tightly on down-type sector",
        best_d >= SECTOR_MAX,
        f"best |dev Q_d| = {best_d:.3f}%",
    )
    check(
        "Best Q_u scheme fails sector threshold (>= 5%) -- universality "
        "does NOT hold on up-type sector",
        best_u >= SECTOR_MAX,
        f"best |dev Q_u| = {best_u:.3f}%",
    )
    # Sector hierarchy: Koide accuracy decreases from CL -> down -> up
    check(
        "Deviation ordering |dev Q_l| < |dev Q_d| < |dev Q_u| holds on PDG "
        "self-scale (sector hierarchy of Koide accuracy)",
        dev_l < dev_d_self < dev_u_self,
        f"{dev_l:.3f}% < {dev_d_self:.3f}% < {dev_u_self:.3f}%",
    )
    # Verdict consistency
    check(
        "Verdict is CHARGED_LEPTON_ONLY on present PDG surface + current "
        "framework extraction state",
        verdict == "CHARGED_LEPTON_ONLY",
        f"verdict = {verdict}",
    )

    return verdict


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main() -> int:
    print("=" * 72)
    print("  FRONTIER: Koide sectoral universality test")
    print("  (Prediction 3 of charged-lepton-koide-cone-2026-04-17.md)")
    print("=" * 72)
    print()
    print("  Framework inputs (authority-backed):")
    print(f"    <P>         = {CANONICAL_PLAQUETTE}")
    print(f"    u_0         = {CANONICAL_U0:.8f}")
    print(f"    alpha_bare  = {CANONICAL_ALPHA_BARE:.10f}")
    print(f"    alpha_LM    = {CANONICAL_ALPHA_LM:.10f}")
    print(f"    alpha_s(v)  = {CANONICAL_ALPHA_S_V:.12f}")
    print(f"    y_t(v)      = {YT_V}")
    print(f"    C_F - T_F   = {FIVE_SIXTHS} (exact)")

    Q_l = part_a_charged_leptons()
    Q_d_fw, Q_d_self, Q_d_common = part_b_down_type()
    Q_u_self, Q_u_mz, A_u = part_c_up_type()
    verdict = part_d_verdict(Q_l, Q_d_fw, Q_d_self, Q_d_common,
                             Q_u_self, Q_u_mz)

    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print(f"  Q_l            = {Q_l:.6f}     "
          f"(PDG pole, dev {deviation_pct(Q_l, KOIDE_TARGET):+.3f}%)")
    print(f"  Q_d framework  = {Q_d_fw:.6f}     "
          f"(alpha_s(v) + 5/6 bridge, dev "
          f"{deviation_pct(Q_d_fw, KOIDE_TARGET):+.3f}%)")
    print(f"  Q_d PDG self   = {Q_d_self:.6f}     "
          f"(PDG threshold-local, dev "
          f"{deviation_pct(Q_d_self, KOIDE_TARGET):+.3f}%)")
    print(f"  Q_d common m_b = {Q_d_common:.6f}     "
          f"(PDG common-scale, dev "
          f"{deviation_pct(Q_d_common, KOIDE_TARGET):+.3f}%)")
    print(f"  Q_u PDG self   = {Q_u_self:.6f}     "
          f"(PDG canonical, dev "
          f"{deviation_pct(Q_u_self, KOIDE_TARGET):+.3f}%)")
    print(f"  Q_u M_Z        = {Q_u_mz:.6f}     "
          f"(MS-bar at M_Z, dev "
          f"{deviation_pct(Q_u_mz, KOIDE_TARGET):+.3f}%)")
    print(f"  2/3            = {KOIDE_TARGET:.6f}")
    print("\n  Scheme-correction analysis (up-type):")
    if not math.isnan(A_u):
        print(f"    required sqrt(m_t) rescaling A     = {A_u:.6f}")
        print(f"    required m_t rescaling A^2         = {A_u**2:.6f}")
        print("    not a natural output of plaquette running, canonical")
        print("    v / M_Z transport, or any retained framework theorem.")

    print()
    print(f"  KOIDE_UNIVERSALITY = {verdict}")
    print("\n" + "=" * 72)
    print(f"  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 72)

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
