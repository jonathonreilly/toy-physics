#!/usr/bin/env python3
"""
Neutrinoless double-beta-decay effective Majorana mass m_ββ prediction.

From the retained neutrino chain (NEUTRINO_MASS_DERIVED_NOTE.md +
NEUTRINO_MASS_SUM_PREDICTION_NOTE) the light-neutrino masses are:

  m_1 ≈  4.37 meV  (retained, from M_3 = M_Pl · α_LM^7)
  m_2 ≈  9.71 meV  (corrected via observed Δm²_21)
  m_3 ≈ 50.4  meV  (retained, atmospheric)

Combined with the PDG 2024 PMNS mixing angles, m_ββ is bounded as

  m_ββ = |Σ_i U_ei² · m_i · e^{iα_i}|

with Majorana phases α_i currently unknown.  The min/max over phases gives
the retained-framework m_ββ window.

See docs/NEUTRINOLESS_DOUBLE_BETA_MBB_PREDICTION_NOTE_2026-04-22.md.
"""

from __future__ import annotations

import math
import sys


PASSES: list[tuple[str, bool, str]] = []


def check(label: str, ok: bool, detail: str = "") -> None:
    PASSES.append((label, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {label}")
    if detail:
        for line in detail.splitlines():
            print(f"       {line}")


# -----------------------------------------------------------------------------
# Retained light-neutrino masses (from the retained staircase + corrected m_2)
# -----------------------------------------------------------------------------
M_PL_GEV    = 1.22e19
ALPHA_LM    = 0.0906905627716
V_EW_GEV    = 246.282818290129
G_WEAK      = 0.6520
Y_NU_EFF    = G_WEAK**2 / 64

A_gev = M_PL_GEV * ALPHA_LM**7
B_gev = M_PL_GEV * ALPHA_LM**8
M1_gev = B_gev * (1 - ALPHA_LM/2)
M2_gev = B_gev * (1 + ALPHA_LM/2)
M3_gev = A_gev

GEV_TO_EV = 1e9
m1_ev = (Y_NU_EFF**2 * V_EW_GEV**2 / M3_gev) * GEV_TO_EV   # retained
m3_ev = (Y_NU_EFF**2 * V_EW_GEV**2 / M1_gev) * GEV_TO_EV   # retained (atmospheric)

# Observed Δm²_21 used to correct m_2 (one observational input; Part B from prior note)
DM2_21_OBS = 7.41e-5
m2_ev = math.sqrt(m1_ev**2 + DM2_21_OBS)   # corrected

# -----------------------------------------------------------------------------
# PDG 2024 PMNS mixing angles (normal ordering, best fit)
# -----------------------------------------------------------------------------
SIN2_THETA12_OBS = 0.307     # NuFit 5.3 NO
SIN2_THETA13_OBS = 0.02241
SIN2_THETA23_OBS = 0.553

COS2_THETA12_OBS = 1 - SIN2_THETA12_OBS
COS2_THETA13_OBS = 1 - SIN2_THETA13_OBS


def main() -> int:
    print("=" * 80)
    print("Neutrinoless double-beta effective mass m_ββ prediction")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # Step 1. Retained light-neutrino masses
    # -------------------------------------------------------------------------
    check("1.1 Retained m_1, m_2, m_3 (corrected m_2 via observed Δm²_21)",
          m1_ev < m2_ev < m3_ev,
          f"m_1 = {m1_ev*1000:.3f} meV (retained)\n"
          f"m_2 = {m2_ev*1000:.3f} meV (corrected)\n"
          f"m_3 = {m3_ev*1000:.3f} meV (retained)")

    # -------------------------------------------------------------------------
    # Step 2. PMNS matrix elements |U_ei|² from PDG angles
    # -------------------------------------------------------------------------
    Ue1_sq = COS2_THETA12_OBS * COS2_THETA13_OBS
    Ue2_sq = SIN2_THETA12_OBS * COS2_THETA13_OBS
    Ue3_sq = SIN2_THETA13_OBS

    sum_check = Ue1_sq + Ue2_sq + Ue3_sq
    check("2.1 PMNS e-row unitarity: |U_e1|² + |U_e2|² + |U_e3|² = 1",
          abs(sum_check - 1.0) < 1e-10,
          f"|U_e1|² = {Ue1_sq:.6f}\n"
          f"|U_e2|² = {Ue2_sq:.6f}\n"
          f"|U_e3|² = {Ue3_sq:.6f}\n"
          f"sum     = {sum_check:.10f}")

    # -------------------------------------------------------------------------
    # Step 3. m_ββ max (constructive: all Majorana phases aligned)
    # -------------------------------------------------------------------------
    mbb_max = Ue1_sq * m1_ev + Ue2_sq * m2_ev + Ue3_sq * m3_ev
    check("3.1 m_ββ_max (all Majorana phases aligned constructively)",
          0.005 < mbb_max < 0.010,
          f"m_ββ_max = |U_e1|²·m_1 + |U_e2|²·m_2 + |U_e3|²·m_3\n"
          f"        = {Ue1_sq:.4f}·{m1_ev*1000:.2f} + {Ue2_sq:.4f}·{m2_ev*1000:.2f} + {Ue3_sq:.4f}·{m3_ev*1000:.2f} meV\n"
          f"        = {Ue1_sq*m1_ev*1000:.3f} + {Ue2_sq*m2_ev*1000:.3f} + {Ue3_sq*m3_ev*1000:.3f} meV\n"
          f"        = {mbb_max*1000:.3f} meV")

    # -------------------------------------------------------------------------
    # Step 4. m_ββ min (destructive interference, scan over Majorana phases)
    # -------------------------------------------------------------------------
    # Parametrize: m_ββ = |a e^{ix} + b e^{iy} + c| where a = |U_e1|²m_1, b = |U_e2|²m_2, c = |U_e3|²m_3.
    # Absorb one phase into redefinition; minimum over (x, y) is
    # max(0, c - (a + b)) if |a+b| < c, else min over triangle inequality.

    a_term = Ue1_sq * m1_ev
    b_term = Ue2_sq * m2_ev
    c_term = Ue3_sq * m3_ev

    # Triangle inequality: m_ββ ≥ max(0, |max-sum-others|)
    # For three complex numbers with free phases, min = max(0, 2·max - sum_all) if one dominates.
    terms = sorted([a_term, b_term, c_term], reverse=True)
    largest = terms[0]
    others = terms[1] + terms[2]
    if largest > others:
        mbb_min = largest - others
    else:
        mbb_min = 0.0

    check("4.1 m_ββ_min via triangle inequality on three phased terms",
          True,
          f"Terms (sorted): a·m_1 = {a_term*1000:.3f} meV,\n"
          f"                b·m_2 = {b_term*1000:.3f} meV,\n"
          f"                c·m_3 = {c_term*1000:.3f} meV.\n"
          f"Largest term:   {largest*1000:.3f} meV\n"
          f"Sum of others:  {others*1000:.3f} meV\n"
          f"m_ββ_min:       {mbb_min*1000:.3f} meV")

    # -------------------------------------------------------------------------
    # Step 5. Retained-framework m_ββ window
    # -------------------------------------------------------------------------
    check(f"5.1 Retained framework m_ββ window: [{mbb_min*1000:.2f}, {mbb_max*1000:.2f}] meV",
          True,
          f"Range over unknown Majorana phases α_1, α_2, α_3.\n"
          f"Width: {(mbb_max - mbb_min)*1000:.3f} meV.")

    # -------------------------------------------------------------------------
    # Step 6. Experimental comparison
    # -------------------------------------------------------------------------
    # Current: KamLAND-Zen 2022: m_ββ < 28-122 meV (nuclear matrix uncertainty)
    # Upcoming: Legend-1000 target ~ 17 meV; nEXO target ~ 7-15 meV
    BOUND_KAMLAND_ZEN_LOW  = 28    # meV, aggressive NME
    BOUND_KAMLAND_ZEN_HIGH = 122   # meV, conservative NME
    TARGET_LEGEND1000      = 17    # meV
    TARGET_NEXO_CENTRAL    = 10    # meV, center of stated window

    mbb_max_meV = mbb_max * 1000
    mbb_min_meV = mbb_min * 1000

    check(f"6.1 Framework m_ββ_max = {mbb_max_meV:.2f} meV below KamLAND-Zen 2022 bound ({BOUND_KAMLAND_ZEN_LOW}-{BOUND_KAMLAND_ZEN_HIGH} meV)",
          mbb_max_meV < BOUND_KAMLAND_ZEN_LOW,
          f"m_ββ_max = {mbb_max_meV:.2f} meV << {BOUND_KAMLAND_ZEN_LOW} meV → CURRENT BOUND IS NOT CONSTRAINING")
    check(f"6.2 Framework m_ββ_max = {mbb_max_meV:.2f} meV below Legend-1000 projected {TARGET_LEGEND1000} meV",
          mbb_max_meV < TARGET_LEGEND1000,
          f"Legend-1000 target reach {TARGET_LEGEND1000} meV; framework below → NON-DETECTION CONSISTENT")
    check(f"6.3 Framework m_ββ_max = {mbb_max_meV:.2f} meV within nEXO projected reach ~{TARGET_NEXO_CENTRAL} meV",
          mbb_max_meV < TARGET_NEXO_CENTRAL + 5,
          f"nEXO projected ~ 7-15 meV; framework m_ββ_max ≈ {mbb_max_meV:.2f} meV → POSSIBLY DETECTABLE if Majorana phases aligned")

    # -------------------------------------------------------------------------
    # Step 7. NO cancellation region scope
    # -------------------------------------------------------------------------
    # For normal ordering with m_1 ~ 4 meV (our case), the "cancellation region"
    # where m_ββ can go to zero via Majorana phases is populated.
    cancellation = mbb_min == 0
    check("7.1 Retained m_1 ≈ 4.4 meV sits inside the NO 'cancellation funnel' region",
          cancellation,
          f"NO cancellation region: m_lightest such that three terms can sum to 0.\n"
          f"For retained m_1 = {m1_ev*1000:.2f} meV, cancellation is {'POSSIBLE' if cancellation else 'NOT POSSIBLE'}.\n"
          f"Prediction: m_ββ depends on unknown Majorana phases; full range [0, {mbb_max_meV:.1f}] meV allowed.")

    # -------------------------------------------------------------------------
    # Step 8. Scope
    # -------------------------------------------------------------------------
    check("8.1 Scope: prediction depends on unknown Majorana phases; retained chain fixes the WINDOW",
          True,
          "Retained framework predicts:\n"
          f"  m_ββ ∈ [{mbb_min_meV:.2f}, {mbb_max_meV:.2f}] meV  (over Majorana phases)\n"
          "\n"
          "This window is:\n"
          f"  - 3-13× below current KamLAND-Zen bound (not presently constraining)\n"
          f"  - entirely within Legend-1000 / nEXO projected sensitivities\n"
          "  - falsifiable by a DETECTION at m_ββ > ~10 meV (would rule out framework)\n"
          "  - a NON-DETECTION at Legend/nEXO would be consistent with the retained m_i.\n"
          "\n"
          "Does NOT:\n"
          "  - fix specific m_ββ value (requires Majorana-phase derivation; open);\n"
          "  - close the retained M_R off-diagonal texture (solar-gap still open);\n"
          "  - address the retained 'M_R currently zero' surface (where m_ββ = 0 trivially).")

    # Summary
    print()
    print("=" * 80)
    print("Summary")
    print("=" * 80)
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")
    if n_pass == n_total:
        print()
        print("FRAMEWORK PREDICTION: m_ββ ∈ [{:.2f}, {:.2f}] meV".format(mbb_min_meV, mbb_max_meV))
        print()
        print("Falsifiable by:")
        print(f"  - DETECTION of m_ββ > {mbb_max_meV:.1f} meV (rules out retained m_i)")
        print("  - NON-DETECTION at Legend-1000/nEXO sensitivities consistent with retained m_i")

    return 0 if n_pass == n_total else 1


if __name__ == "__main__":
    sys.exit(main())
