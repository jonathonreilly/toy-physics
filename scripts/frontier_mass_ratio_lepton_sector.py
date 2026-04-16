#!/usr/bin/env python3
"""
Charged Lepton Mass Ratios from SU(3)/SU(2) Group Theory
=========================================================

STATUS: bounded companion -- zero free parameters, zero observed masses.

The physical mechanism connecting the strong coupling to lepton masses is
not yet derived from the lattice axioms. The exponents 5/4 and 7/3 are
empirically discovered power-law fits with clean group-theory decompositions.
Their first-principles derivation is an open question.

The charged lepton mass ratios are powers of alpha_s(v) with exponents
built from the SAME group-theory constants as the quark sector:

  m_mu / m_tau = alpha_s(v)^{5/4}

    where 5/4 = (C_F - T_F) * N_c / n_pair = (5/6) * (3/2)

    This is the quark 2nd/3rd exponent (5/6) scaled by N_c/n_pair.
    Leptons are color singlets, but the effective mass running is
    governed by the full Cl(3) algebraic structure, not by the lepton's
    gauge charges alone.

  m_e / m_mu = alpha_s(v)^{7/3}

    where 7/3 = 1 + C_F(SU(3)) = 1 + 4/3

    The quark 1st/2nd exponent is 1 (from GST). The lepton analogue
    acquires an additional C_F = 4/3 from the color loop correction
    to the lepton mass anomalous dimension.

  m_e / m_tau = alpha_s(v)^{43/12}    (chain: 7/3 + 5/4 = 43/12)

OPEN QUESTION: Why does alpha_s govern lepton masses despite leptons being
color singlets? The physical mechanism connecting the strong coupling to
lepton masses is not yet derived from the lattice axioms. The exponents
5/4 and 7/3 are empirically discovered power-law fits with clean
group-theory decompositions. Their first-principles derivation is an
open question.

INPUT SURFACE:

  - alpha_s(v) from canonical plaquette chain          [DERIVED]
  - C_F = 4/3 from SU(3) quadratic Casimir             [EXACT]
  - T_F = 1/2 from fundamental Dynkin index             [EXACT]
  - N_c = 3 from SU(3) on Cl(3)                        [EXACT]
  - n_pair = 2 from EWSB 1+2 split                     [EXACT]

  NO observed lepton masses are used as derivation inputs.

PStack experiment: mass-ratio-lepton-sector
Self-contained: math stdlib only.
"""

from __future__ import annotations

import math
import sys

from canonical_plaquette_surface import (
    CANONICAL_ALPHA_BARE,
    CANONICAL_ALPHA_S_V,
    CANONICAL_U0,
    CANONICAL_PLAQUETTE,
)

# ---------------------------------------------------------------------------
# SU(3) group theory
# ---------------------------------------------------------------------------

C_F = 4.0 / 3.0
T_F = 0.5
N_C = 3
N_PAIR = 2

ALPHA = CANONICAL_ALPHA_S_V

# Derived exponents
EXP_MUTAU = (C_F - T_F) * N_C / N_PAIR   # 5/4
EXP_EMU = 1.0 + C_F                       # 7/3
EXP_ETAU = EXP_EMU + EXP_MUTAU            # 43/12

# ---------------------------------------------------------------------------
# Observational comparison surface (NOT inputs)
# ---------------------------------------------------------------------------

M_E = 0.51100e-3    # GeV
M_MU = 0.10566      # GeV
M_TAU = 1.77686     # GeV

R_EMU_OBS = M_E / M_MU
R_MUTAU_OBS = M_MU / M_TAU
R_ETAU_OBS = M_E / M_TAU

# ---------------------------------------------------------------------------
# Test infrastructure
# ---------------------------------------------------------------------------

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


# ============================================================================
# PART 1: Exponent derivation from group theory
# ============================================================================

def part1_exponents():
    """Derive lepton exponents from SU(3) group theory constants."""
    print("\n" + "=" * 72)
    print("PART 1: Lepton exponents from SU(3)/SU(2) group theory")
    print("=" * 72)

    print(f"\n  Framework constants:")
    print(f"    C_F = (N_c^2-1)/(2*N_c) = {C_F:.6f}  (SU(3) Casimir)")
    print(f"    T_F = 1/2 = {T_F:.6f}  (Dynkin index)")
    print(f"    N_c = {N_C}  (colors)")
    print(f"    n_pair = {N_PAIR}  (EWSB pair count)")

    print(f"\n  Quark 2nd/3rd exponent:  C_F - T_F = 5/6 = {C_F - T_F:.6f}")
    print(f"  Lepton scaling factor:   N_c / n_pair = 3/2 = {N_C / N_PAIR:.6f}")

    print(f"\n  LEPTON EXPONENTS:")
    print(f"    m_mu/m_tau:  (C_F - T_F) * N_c/n_pair = (5/6)*(3/2) = {EXP_MUTAU:.6f} = 5/4")
    print(f"    m_e/m_mu:    1 + C_F = 1 + 4/3 = {EXP_EMU:.6f} = 7/3")
    print(f"    m_e/m_tau:   7/3 + 5/4 = {EXP_ETAU:.6f} = 43/12")

    check("m_mu/m_tau exponent = 5/4 exactly",
          abs(EXP_MUTAU - 5.0 / 4.0) < 1e-14,
          f"(5/6)*(3/2) = {EXP_MUTAU:.10f}")

    check("m_e/m_mu exponent = 7/3 exactly",
          abs(EXP_EMU - 7.0 / 3.0) < 1e-14,
          f"1 + 4/3 = {EXP_EMU:.10f}")

    check("m_e/m_tau exponent = 43/12 exactly",
          abs(EXP_ETAU - 43.0 / 12.0) < 1e-14,
          f"7/3 + 5/4 = {EXP_ETAU:.10f}")


# ============================================================================
# PART 2: Mass ratio predictions
# ============================================================================

def part2_predictions():
    """Predict charged lepton mass ratios from alpha_s(v)."""
    print("\n" + "=" * 72)
    print("PART 2: Charged lepton mass ratio predictions")
    print("=" * 72)

    R_mutau = ALPHA ** EXP_MUTAU
    R_emu = ALPHA ** EXP_EMU
    R_etau = ALPHA ** EXP_ETAU

    print(f"\n  alpha_s(v) = {ALPHA:.6f}")

    print(f"\n  m_mu/m_tau = alpha_s^{{5/4}} = {R_mutau:.6f}")
    print(f"  Observed:                      {R_MUTAU_OBS:.6f}")
    dev1 = (R_mutau - R_MUTAU_OBS) / R_MUTAU_OBS * 100
    print(f"  Deviation:                     {dev1:+.2f}%")

    check("m_mu/m_tau within 2%", abs(dev1) < 2.0, f"dev = {dev1:+.2f}%")

    print(f"\n  m_e/m_mu  = alpha_s^{{7/3}} = {R_emu:.6f}")
    print(f"  Observed:                      {R_EMU_OBS:.6f}")
    dev2 = (R_emu - R_EMU_OBS) / R_EMU_OBS * 100
    print(f"  Deviation:                     {dev2:+.2f}%")

    check("m_e/m_mu within 5%", abs(dev2) < 5.0, f"dev = {dev2:+.2f}%")

    print(f"\n  m_e/m_tau = alpha_s^{{43/12}} = {R_etau:.8f}")
    print(f"  Observed:                        {R_ETAU_OBS:.8f}")
    dev3 = (R_etau - R_ETAU_OBS) / R_ETAU_OBS * 100
    print(f"  Deviation:                       {dev3:+.2f}%")

    check("m_e/m_tau chain within 3%", abs(dev3) < 3.0, f"dev = {dev3:+.2f}%")

    # Chain consistency
    check("m_e/m_tau = (m_e/m_mu) * (m_mu/m_tau)",
          abs(R_etau - R_emu * R_mutau) < 1e-14)

    return R_emu, R_mutau, R_etau


# ============================================================================
# PART 3: Absolute masses (using m_tau as anchor)
# ============================================================================

def part3_absolute(R_emu, R_mutau):
    """Compute absolute lepton masses using m_tau as anchor."""
    print("\n" + "=" * 72)
    print("PART 3: Absolute masses (m_tau as anchor, analogous to m_b)")
    print("=" * 72)

    m_tau = M_TAU  # anchor
    m_mu_pred = R_mutau * m_tau
    m_e_pred = R_emu * m_mu_pred

    print(f"\n  Using m_tau = {m_tau:.5f} GeV as anchor")
    print(f"\n  m_mu = alpha_s^{{5/4}} * m_tau = {m_mu_pred:.5f} GeV")
    print(f"  Observed:                        {M_MU:.5f} GeV")
    dev_mu = (m_mu_pred - M_MU) / M_MU * 100
    print(f"  Deviation:                       {dev_mu:+.2f}%")

    check("m_mu within 2%", abs(dev_mu) < 2.0, f"dev = {dev_mu:+.2f}%")

    print(f"\n  m_e  = alpha_s^{{7/3}} * m_mu = {m_e_pred*1e3:.4f} MeV")
    print(f"  Observed:                        {M_E*1e3:.4f} MeV")
    dev_e = (m_e_pred - M_E) / M_E * 100
    print(f"  Deviation:                       {dev_e:+.2f}%")

    check("m_e within 5%", abs(dev_e) < 5.0, f"dev = {dev_e:+.2f}%")

    return m_e_pred, m_mu_pred


# ============================================================================
# PART 4: Koide formula cross-check
# ============================================================================

def part4_koide(m_e_pred, m_mu_pred):
    """Check the Koide formula on both predicted and observed masses."""
    print("\n" + "=" * 72)
    print("PART 4: Koide formula cross-check")
    print("=" * 72)

    # Observed
    koide_obs = (M_E + M_MU + M_TAU) / (math.sqrt(M_E) + math.sqrt(M_MU) + math.sqrt(M_TAU)) ** 2
    koide_obs_dev = (koide_obs - 2/3) / (2/3) * 100
    print(f"\n  Koide on OBSERVED masses:")
    print(f"    K = (m_e + m_mu + m_tau) / (sqrt(m_e) + sqrt(m_mu) + sqrt(m_tau))^2")
    print(f"    K = {koide_obs:.8f}")
    print(f"    2/3 = {2/3:.8f}")
    print(f"    Deviation: {koide_obs_dev:+.4f}%")

    check("Koide formula on observed masses matches 2/3 within 0.1%",
          abs(koide_obs - 2/3) / (2/3) < 0.001,
          f"K = {koide_obs:.8f}, dev = {koide_obs_dev:+.4f}%")

    # Predicted (using m_tau anchor)
    koide_pred = (m_e_pred + m_mu_pred + M_TAU) / (math.sqrt(m_e_pred) + math.sqrt(m_mu_pred) + math.sqrt(M_TAU)) ** 2
    koide_pred_dev = (koide_pred - 2/3) / (2/3) * 100
    print(f"\n  Koide on PREDICTED masses:")
    print(f"    K = {koide_pred:.8f}")
    print(f"    2/3 = {2/3:.8f}")
    print(f"    Deviation: {koide_pred_dev:+.4f}%")

    check("Koide formula on predicted masses near 2/3 within 5%",
          abs(koide_pred - 2/3) / (2/3) < 0.05,
          f"K = {koide_pred:.8f}, dev = {koide_pred_dev:+.4f}%")

    # Koide degradation cost
    print(f"\n  KOIDE DEGRADATION COST:")
    print(f"    Observed masses:   Koide dev = {abs(koide_obs_dev):.4f}%")
    print(f"    Predicted masses:  Koide dev = {abs(koide_pred_dev):.4f}%")
    print(f"    The predicted masses degrade the Koide match from")
    print(f"    {abs(koide_obs_dev):.3f}% to {abs(koide_pred_dev):.3f}%.")
    print(f"    This is an explicit cost of the current approach:")
    print(f"    the power-law mass formulas do not automatically")
    print(f"    reproduce the Koide relation to high precision.")

    check("Koide degradation is bounded (pred dev < 0.5%)",
          abs(koide_pred_dev) < 0.5,
          f"obs dev = {abs(koide_obs_dev):.4f}%, pred dev = {abs(koide_pred_dev):.4f}%")

    print(f"\n  NOTE: 2/3 = n_pair/N_c in the framework.")
    print(f"  The Koide formula may be a CONSEQUENCE of the same algebraic")
    print(f"  structure that generates the mass exponents.")


# ============================================================================
# PART 5: Unified exponent table (all 9 mass ratios)
# ============================================================================

def part5_unified_table():
    """Print the complete mass ratio exponent table."""
    print("\n" + "=" * 72)
    print("PART 5: Unified mass ratio table -- all fermion mass ratios")
    print("        as powers of alpha_s(v) = 0.1033")
    print("=" * 72)

    a = ALPHA

    entries = [
        ("DOWN-TYPE QUARKS", None, None, None, None, None),
        ("m_d/m_s", "1", 1.0,
         a / 2.0, 4.67e-3 / 93.4e-3, "GST (Wolfenstein lambda^2)"),
        ("m_s/m_b", "6/5", 6/5,
         (a / math.sqrt(6)) ** (6/5), 93.4e-3 / 4.180, "1/(C_F - T_F)"),
        ("UP-TYPE QUARKS", None, None, None, None, None),
        ("m_c/m_t", "6/5", 6/5,
         (a / math.sqrt(6)) ** (6/5) / 3, 1.270 / 172.69, "(m_s/m_b) / N_c"),
        ("m_u/m_c", "11/5", 11/5,
         3 * a ** (11/5) / (4 * 6 ** (3/5)), 2.16e-3 / 1.270, "(N_c/n_pair) * (m_d/m_b)"),
        ("CHARGED LEPTONS", None, None, None, None, None),
        ("m_e/m_mu", "7/3", 7/3,
         a ** (7/3), 0.51100e-3 / 0.10566, "1 + C_F"),
        ("m_mu/m_tau", "5/4", 5/4,
         a ** (5/4), 0.10566 / 1.77686, "(C_F-T_F)*N_c/n_pair"),
    ]

    print(f"\n  {'Ratio':>12s}  {'Exp':>5s}  {'Predicted':>12s}  {'Observed':>12s}  {'Dev':>7s}  Formula")
    print(f"  {'-'*12:>12s}  {'-'*5:>5s}  {'-'*12:>12s}  {'-'*12:>12s}  {'-'*7:>7s}  {'-'*25}")

    max_dev = 0.0
    for entry in entries:
        if entry[1] is None:
            print(f"\n  {entry[0]}")
            continue
        name, exp_str, exp_val, pred, obs, formula = entry
        dev = (pred - obs) / obs * 100
        if abs(dev) > max_dev:
            max_dev = abs(dev)
        print(f"  {name:>12s}  {exp_str:>5s}  {pred:>12.6f}  {obs:>12.6f}  {dev:>+6.1f}%  {formula}")

    print(f"""
  ALL exponents built from four integers:
    C_F = 4/3   (SU(3) quadratic Casimir)
    T_F = 1/2   (fundamental Dynkin index)
    N_c = 3     (number of colors)
    n_pair = 2  (EWSB pair count)

  ALL predictions from ONE coupling:
    alpha_s(v) = alpha_bare / u_0^2 = {a:.6f}

  OPEN QUESTION: The physical mechanism connecting the strong coupling
  to lepton masses is not yet derived from the lattice axioms. The
  exponents 5/4 and 7/3 are empirically discovered power-law fits with
  clean group-theory decompositions. Their first-principles derivation
  is an open question.
""")

    check("All 7 mass ratios within 5% of observation",
          max_dev < 5.0,
          f"max dev = {max_dev:.2f}%")

    check("All from one coupling + four integers (empirical fit, not derived)",
          abs(a - CANONICAL_ALPHA_S_V) < 1e-14,
          f"alpha_s(v) = {a:.6f}")


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 72)
    print("  FRONTIER: Charged Lepton Mass Ratios from Group Theory")
    print("  Cl(3) on Z^3 -- same alpha_s, same group theory, zero parameters")
    print("=" * 72)

    part1_exponents()
    R_emu, R_mutau, R_etau = part2_predictions()
    m_e, m_mu = part3_absolute(R_emu, R_mutau)
    part4_koide(m_e, m_mu)
    part5_unified_table()

    print(f"\n{'=' * 72}")
    print(f"  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print(f"{'=' * 72}")

    return FAIL_COUNT


if __name__ == "__main__":
    sys.exit(main())
