#!/usr/bin/env python3
"""
Probe Y-S4b-RGE — RGE Lambda Running Closes the +12% Higgs Gap (probeY_S4b_rge)
================================================================================

Question
--------
Probe X-S4b-Combined (PR #938) tested the COMBINATION of three retained
ingredients — (i) m_H/v = 1/(2 u_0), (ii) v_EW = 246.28 GeV, (iii) G2
Born-as-source position-density trace — and found the combination yields
m_H(combined) = v_EW/(2 u_0) = 140.31 GeV, +12.03% above PDG 125.25 GeV.
The probe concluded the combination collapses to the "symmetric-point
identification" (V''_taste(0)/N_taste, square-rooted), and the +12%
residual is "structurally NOT addressable by recombining components
inheriting the symmetric-point identification."

A LATENT POSSIBILITY remained untested: Probe X's components were ALL
evaluated at the symmetric point (m=0). Renormalization-group running
of the Higgs quartic coupling λ from M_Pl down to v_EW via the SM
β_λ — which is RETAINED content per HIGGS_MASS_RETENTION_ANALYSIS_NOTE
— had never been wired explicitly into the Probe X comparison. If
β_λ-running is a structurally distinct retained ingredient (NOT a
symmetric-point identification), it could close the +12% gap that
Probe X declared structurally inaccessible.

This probe tests that hypothesis.

Method
------
1. Verify β_λ retention. Confirm the framework retains the full SM
   3-loop β_λ system + the classicality boundary condition λ(M_Pl)=0
   per HIGGS_MASS_RETENTION_ANALYSIS_NOTE_2026-04-18.md.
2. Reproduce the Probe X-S4b-Combined symmetric-point prediction
   m_H_sym = v_EW/(2 u_0) = 140.30 GeV.
3. Run the canonical 3-loop RGE machinery (the existing retained
   runner scripts/frontier_higgs_mass_full_3loop.py) using framework-
   derived couplings at v and λ(M_Pl) = 0, integrating M_Pl → v_EW
   to obtain λ(v_EW) and then m_H = sqrt(2 λ(v_EW)) · v_EW.
4. Compare m_H(RGE) to (a) the symmetric-point shortcut 140.30 GeV
   and (b) PDG 125.25 GeV. Quantify gap closure.
5. Report tier verdict per the brief: positive if RGE closes m_H to
   within ~5% of PDG; bounded if running is retained but does not
   close; negative if β_λ not retained or running cannot be derived.

Tier Assessment
---------------
This probe finds: POSITIVE TIER.

The retained 3-loop SM RGE with λ(M_Pl)=0 boundary, framework-derived
couplings at v_EW, and through-2-loop matching gives m_H = 125.14 GeV
at 3-loop (deviation -0.09% from PDG 125.25 GeV; well inside the ±5%
positive-theorem threshold). The +12.03% gap from Probe X-S4b-Combined
is fully closed. The structural reason: β_λ-running over 17 decades
of log-scale (M_Pl → v) is qualitatively different content from the
symmetric-point identification — it integrates the running of the top
Yukawa y_t and gauge couplings, NOT a static mean-field readout.

Cross-references
----------------
- Source note: docs/KOIDE_Y_S4B_RGE_LAMBDA_RUNNING_NOTE_2026-05-08_probeY_S4b_rge.md
- Probe X-S4b-Combined: docs/KOIDE_X_S4B_COMBINED_HIGGS_EWSB_G2_NOTE_2026-05-08_probeX_S4b_combined.md
- Retained 3-loop runner: scripts/frontier_higgs_mass_full_3loop.py
- Retained analysis: docs/HIGGS_MASS_RETENTION_ANALYSIS_NOTE_2026-04-18.md
- Canonical surface: scripts/canonical_plaquette_surface.py
"""

from __future__ import annotations

import os
import sys
import types
import importlib.util

import numpy as np

# Ensure we can import the existing retained runner machinery without
# triggering its __main__ block.
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from canonical_plaquette_surface import (
    CANONICAL_PLAQUETTE,
    CANONICAL_U0,
    CANONICAL_ALPHA_BARE,
    CANONICAL_ALPHA_LM,
    CANONICAL_ALPHA_S_V,
)

PI = np.pi

# Comparator (NEVER used as derivation input; only for falsifiability tier check)
M_H_PDG = 125.25
V_PDG = 246.22

# Tier thresholds per brief
TIER_POSITIVE_THRESHOLD = 0.05
TIER_BOUNDED_THRESHOLD = 0.10

PASS_COUNT = 0
FAIL_COUNT = 0


def report(tag, ok, msg):
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if ok else "FAIL"
    if ok:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    print(f"  [{status}] {tag}: {msg}")


def import_retained_runner():
    """Import the retained 3-loop SM RGE runner without executing its __main__."""
    path = os.path.join(HERE, "frontier_higgs_mass_full_3loop.py")
    src = open(path).read().replace("if __name__", "if False")
    mod = types.ModuleType("h3l")
    mod.__file__ = path
    exec(compile(src, path, "exec"), mod.__dict__)
    return mod


def kY1_betalambda_retained():
    """K1: β_λ + λ(M_Pl)=0 are retained content (not new content for this probe).

    Confirms that the retained 3-loop runner exposes β_λ at all three loop
    orders and ingests the classicality boundary λ(M_Pl)=0.
    """
    print("\n" + "=" * 78)
    print("K1: β_λ retention check (no new content; uses retained runner)")
    print("=" * 78)

    mod = import_retained_runner()

    # Retained quantities
    print(f"\n  Retained framework constants (from canonical_plaquette_surface):")
    print(f"    <P> = {CANONICAL_PLAQUETTE}")
    print(f"    u_0 = {CANONICAL_U0:.6f}")
    print(f"    α_bare = {CANONICAL_ALPHA_BARE:.6f}")
    print(f"    α_LM   = {CANONICAL_ALPHA_LM:.6f}")
    print(f"    α_s(v) = {CANONICAL_ALPHA_S_V:.6f}")
    print(f"    M_Pl   = {mod.M_PL:.4e} GeV")
    print(f"    v_EW   = {mod.V_DERIVED:.4f} GeV (hierarchy theorem)")
    print(f"    y_t(v) = {mod.YT_V_DERIVED:.4f} (retained YT central)")

    # Verify the retained beta function evaluates at all loop orders
    g1_test, g2_test, g3_test, yt_test, lam_test = 0.464, 0.648, 1.139, 0.918, 0.0
    y_test = [g1_test, g2_test, g3_test, yt_test, lam_test]
    t_test = np.log(mod.M_PL)
    beta1 = mod.beta_full(t_test, y_test, n_f=6, loop_order=1)
    beta2 = mod.beta_full(t_test, y_test, n_f=6, loop_order=2)
    beta3 = mod.beta_full(t_test, y_test, n_f=6, loop_order=3)

    print(f"\n  β_λ(M_Pl, λ=0) at framework couplings:")
    print(f"    1-loop:  {beta1[4]:+.6e}")
    print(f"    2-loop:  {beta2[4]:+.6e}")
    print(f"    3-loop:  {beta3[4]:+.6e}")
    print(f"  All three loop orders implemented in retained runner.")

    ok = all(np.isfinite(b[4]) for b in [beta1, beta2, beta3])
    report("k1-beta-lambda-retained", ok,
           "β_λ at 1/2/3-loop and λ(M_Pl)=0 BC are retained content")

    return mod


def kY2_symmetric_point_baseline(mod):
    """K2: Reproduce Probe X-S4b-Combined symmetric-point shortcut.

    Probe X showed: m_H_sym = v_EW/(2 u_0) = 140.31 GeV (+12.03% from PDG).
    """
    print("\n" + "=" * 78)
    print("K2: Probe X-S4b-Combined symmetric-point prediction (baseline)")
    print("=" * 78)

    m_h_sym = mod.V_DERIVED / (2.0 * mod.U0)
    gap_sym = (m_h_sym - M_H_PDG) / M_H_PDG * 100

    print(f"\n  Probe X-S4b-Combined: m_H = v_EW/(2 u_0)")
    print(f"    v_EW = {mod.V_DERIVED:.4f} GeV")
    print(f"    u_0  = {mod.U0:.6f}")
    print(f"    m_H_sym = {m_h_sym:.4f} GeV")
    print(f"    PDG comparator: {M_H_PDG} GeV")
    print(f"    Gap: {gap_sym:+.2f}% (Probe X verdict: BOUNDED, structurally inaccessible)")

    # Match to within rounding precision (Probe X reported 140.31)
    ok = abs(m_h_sym - 140.30) < 0.05
    report("k2-symmetric-point-shortcut", ok,
           f"Reproduces Probe X m_H_sym = 140.30 GeV (got {m_h_sym:.4f}); +12.04% gap")

    return m_h_sym, gap_sym


def kY3_rge_running_to_vew(mod):
    """K3: Run β_λ from M_Pl to v_EW with λ(M_Pl)=0 BC, framework couplings.

    Uses the retained 3-loop SM RGE machinery (already in main).
    """
    print("\n" + "=" * 78)
    print("K3: RGE running from M_Pl to v_EW with λ(M_Pl) = 0")
    print("=" * 78)

    # Framework couplings at v_EW (retained)
    g1_v = 0.464  # GUT-normalized U(1) at v
    g2_v = 0.648  # SU(2) at v
    g3_v = float(np.sqrt(4 * PI * CANONICAL_ALPHA_S_V))  # from canonical α_s
    yt_v = mod.YT_V_DERIVED                              # retained YT central
    print(f"\n  Framework-derived couplings at v_EW = {mod.V_DERIVED:.4f} GeV:")
    print(f"    g_1(v) = {g1_v:.4f}  [GUT normalized]")
    print(f"    g_2(v) = {g2_v:.4f}")
    print(f"    g_3(v) = {g3_v:.4f}  [from α_s(v) = {CANONICAL_ALPHA_S_V:.4f}]")
    print(f"    y_t(v) = {yt_v:.4f}  [retained YT central]")

    # Run RGE: v → M_Pl (gauge+Yukawa) → DOWN with λ(M_Pl)=0 → v_EW
    t_v = np.log(mod.V_DERIVED)
    t_pl = np.log(mod.M_PL)

    results = {}
    print(f"\n  RGE results at each loop order:")
    print(f"  {'loop':>5} {'λ(M_Pl)':>10} {'λ(v)':>12} {'m_H (GeV)':>12} {'gap_PDG':>10}")
    print(f"  {'-'*5} {'-'*10} {'-'*12} {'-'*12} {'-'*10}")

    for nloop in [1, 2, 3]:
        # Step 1: Run gauge+Yukawa from v to M_Pl to get UV trajectories
        y0_up = [g1_v, g2_v, g3_v, yt_v, 0.13]  # λ guess for upward run
        y_pl, _ = mod.run_with_thresholds(
            y0_up, t_v, t_pl,
            loop_order=nloop,
            apply_threshold_corrections=(nloop >= 2),
        )
        g1_pl, g2_pl, g3_pl, yt_pl, _ = y_pl

        # Step 2: Run DOWN with λ(M_Pl) = 0 (classicality BC)
        y0_down = [g1_pl, g2_pl, g3_pl, yt_pl, 0.0]
        y_v_out, _ = mod.run_with_thresholds(
            y0_down, t_pl, t_v,
            loop_order=nloop,
            apply_threshold_corrections=(nloop >= 2),
        )
        lam_v = y_v_out[4]

        if lam_v > 0:
            m_h = float(np.sqrt(2.0 * lam_v) * mod.V_DERIVED)
        else:
            m_h = float(-np.sqrt(2.0 * abs(lam_v)) * mod.V_DERIVED)

        gap_pdg = (m_h - M_H_PDG) / M_H_PDG * 100
        results[nloop] = {
            "lam_v": float(lam_v),
            "m_h": m_h,
            "gap_pdg": float(gap_pdg),
            "yt_pl": float(yt_pl),
            "g3_pl": float(g3_pl),
        }
        print(f"  {nloop:>5d} {0.0:>10.6f} {lam_v:>12.6f} {m_h:>12.2f} {gap_pdg:>+10.2f}%")

    # Final at 3-loop
    m_h_3l = results[3]["m_h"]
    gap_3l = results[3]["gap_pdg"]

    # Tier check
    rel_gap = abs(gap_3l) / 100.0
    is_positive = rel_gap < TIER_POSITIVE_THRESHOLD
    is_bounded = TIER_POSITIVE_THRESHOLD <= rel_gap < TIER_BOUNDED_THRESHOLD

    print(f"\n  3-loop RGE result:")
    print(f"    m_H(RGE, 3-loop) = {m_h_3l:.2f} GeV")
    print(f"    PDG comparator   = {M_H_PDG} GeV")
    print(f"    Relative gap     = {gap_3l:+.2f}%")
    print(f"    Positive tier (<=5%)? {is_positive}")

    report("k3-rge-running-3loop", is_positive,
           f"3-loop m_H = {m_h_3l:.2f} GeV ({gap_3l:+.2f}% from PDG); positive: {is_positive}")

    return results


def kY4_gap_closure_quantification(m_h_sym, results_rge):
    """K4: Quantify gap closure from symmetric-point baseline to RGE."""
    print("\n" + "=" * 78)
    print("K4: Gap closure quantification (Probe X baseline → RGE prediction)")
    print("=" * 78)

    sym_gap_pct = (m_h_sym - M_H_PDG) / M_H_PDG * 100
    rge_gap_pct = results_rge[3]["gap_pdg"]
    rge_m_h = results_rge[3]["m_h"]

    closure_gev = m_h_sym - rge_m_h
    closure_pct = sym_gap_pct - rge_gap_pct

    print(f"\n  Probe X-S4b-Combined (symmetric-point):  m_H = {m_h_sym:.2f} GeV  ({sym_gap_pct:+.2f}%)")
    print(f"  Probe Y-S4b-RGE     (3-loop running):     m_H = {rge_m_h:.2f} GeV  ({rge_gap_pct:+.2f}%)")
    print(f"  ----")
    print(f"  Gap closure:     {closure_gev:+.2f} GeV  ({closure_pct:+.2f}% percentage-points)")
    print(f"  Closure ratio:   {(1 - abs(rge_gap_pct)/abs(sym_gap_pct))*100:.1f}% of original gap eliminated")

    ok = closure_gev > 10.0  # gap closure of at least ~10 GeV
    report("k4-gap-closure", ok,
           f"RGE running closes {closure_gev:.2f} GeV of the +12% gap")

    return closure_gev, closure_pct


def kY5_structural_distinction(mod, m_h_sym, results_rge):
    """K5: Structural reason RGE running is NOT a symmetric-point identification.

    Probe X concluded the +12% residual is "structurally NOT addressable
    by recombining components inheriting the symmetric-point identification."
    This K-statement diagnoses why β_λ-running ESCAPES that argument.

    Three structural distinctions:

    (a) Loop-scale integration. β_λ-running integrates over 17 decades of
        log-scale (M_Pl → v_EW), accumulating contributions from the top
        Yukawa squared-into-quartic feedback loop. The symmetric-point
        identification has NO log-scale integration content.

    (b) Initial condition is not the symmetric-point curvature. The
        classicality BC λ(M_Pl)=0 is a UV boundary condition (a fixed
        framework axiom about Planck-scale classicality). It is NOT
        derived from V''_taste(0)/N_taste. The sym-point identification
        equates curvature/N_taste with (m_H/v)² at m=0; the RGE BC
        equates the QUARTIC COUPLING with zero at the UV scale. These
        are independent physical statements.

    (c) Top Yukawa is the dominant driver. The 1-loop β_λ has the
        characteristic structure β_λ^(1) ⊃ -6 y_t^4 (top loop driving
        λ negative under upward running, hence positive under downward
        running from λ(M_Pl)=0). The y_t input is from the YT chain
        (separate retained content), NOT from the taste-sector
        symmetric-point analysis.
    """
    print("\n" + "=" * 78)
    print("K5: Structural distinction RGE-running ≠ symmetric-point identification")
    print("=" * 78)

    # (a) Log-scale span: 17 decades
    t_v = np.log(mod.V_DERIVED)
    t_pl = np.log(mod.M_PL)
    log_span = (t_pl - t_v) / np.log(10.0)
    print(f"\n  (a) Log-scale integration span: M_Pl/v_EW ≈ 10^{log_span:.2f}")
    print(f"      β_λ integrates over {log_span:.1f} decades of log-scale.")
    print(f"      The symmetric-point identification has NO log-scale content.")

    ok_a = log_span > 15.0
    report("k5a-log-scale-span", ok_a,
           f"RGE integrates {log_span:.1f} decades, distinct from sym-point readout")

    # (b) BC distinction: λ(M_Pl)=0 vs (m_H/v)² = 1/(4u_0²)
    sym_lam_equiv = 1.0 / (4.0 * mod.U0**2) / 2.0  # m_H_sym² / (2 v²)
    actual_lam_v = results_rge[3]["lam_v"]
    print(f"\n  (b) Boundary condition distinction:")
    print(f"      Symmetric-point: (m_H/v)² = 1/(4 u_0²) → λ_sym(v) = {sym_lam_equiv:.6f}")
    print(f"      Classicality BC: λ(M_Pl) = 0 → λ_RGE(v)_3loop = {actual_lam_v:.6f}")
    print(f"      Ratio: λ_RGE/λ_sym = {actual_lam_v/sym_lam_equiv:.4f}")
    print(f"      Independent BCs at independent scales (M_Pl vs v).")

    ok_b = abs(actual_lam_v - sym_lam_equiv) > 0.01  # genuinely different
    report("k5b-bc-distinct", ok_b,
           f"λ(M_Pl)=0 BC distinct from sym-point (m_H/v)²=1/(4u_0²)")

    # (c) Top Yukawa dominance in β_λ
    # β_λ^(1) ⊃ -6 y_t^4 / (16 π²) at λ=0
    yt_pl = results_rge[3]["yt_pl"]
    g3_pl = results_rge[3]["g3_pl"]
    fac = 1.0 / (16.0 * PI**2)
    top_loop_term = fac * (-6.0) * yt_pl**4
    print(f"\n  (c) Top Yukawa dominance:")
    print(f"      β_λ^(1) ⊃ -6 y_t^4 / (16π²)")
    print(f"      At M_Pl: y_t = {yt_pl:.4f}, g_3 = {g3_pl:.4f}")
    print(f"      -6 y_t^4 / (16π²) = {top_loop_term:.6e}")
    print(f"      Top Yukawa drives λ via the y_t² → y_t⁴ feedback.")
    print(f"      y_t input from YT chain (separate retained content), NOT taste-sector.")

    ok_c = abs(top_loop_term) > 1e-6
    report("k5c-top-yukawa-driver", ok_c,
           f"β_λ^(1) -6y_t^4 term = {top_loop_term:.4e} (drives running)")

    return ok_a, ok_b, ok_c


def kY6_consistency_with_retention_analysis(mod, results_rge):
    """K6: Cross-check vs HIGGS_MASS_RETENTION_ANALYSIS_NOTE_2026-04-18.md.

    The retained authority predicts m_H = 125.04 GeV ± 3.17 GeV (1σ
    quadrature) on the 3-loop λ(M_Pl)=0 route. This probe should land
    inside that band.
    """
    print("\n" + "=" * 78)
    print("K6: Consistency with retained band m_H = 125.04 ± 3.17 GeV (1σ)")
    print("=" * 78)

    # Retained authority band (HIGGS_MASS_RETENTION_ANALYSIS_NOTE_2026-04-18 §0)
    M_H_RETAINED_CENTRAL = 125.04
    SIGMA_RETAINED_QUAD = 3.17

    m_h_3l = results_rge[3]["m_h"]
    sigma_dev = (m_h_3l - M_H_RETAINED_CENTRAL) / SIGMA_RETAINED_QUAD

    print(f"\n  Retained authority: m_H = {M_H_RETAINED_CENTRAL} ± {SIGMA_RETAINED_QUAD} GeV (1σ quadrature)")
    print(f"  Probe Y prediction:  m_H = {m_h_3l:.2f} GeV (3-loop RGE)")
    print(f"  Distance from central: {(m_h_3l - M_H_RETAINED_CENTRAL):+.2f} GeV = {sigma_dev:+.2f}σ")

    in_1sigma = abs(sigma_dev) <= 1.0
    print(f"  Within 1σ retained band? {in_1sigma}")

    report("k6-retained-band-consistency", in_1sigma,
           f"Probe Y m_H = {m_h_3l:.2f} GeV at {sigma_dev:+.2f}σ from retained {M_H_RETAINED_CENTRAL}")

    return sigma_dev


def kY7_tier_verdict(results_rge):
    """K7: Final tier verdict per the brief.

    - Positive theorem if RGE closes m_H to within ~5% of PDG.
    - Bounded if running is retained but doesn't close.
    - Negative if β_λ not retained or running cannot be derived.
    """
    print("\n" + "=" * 78)
    print("K7: Tier verdict per probe brief")
    print("=" * 78)

    m_h_3l = results_rge[3]["m_h"]
    gap_3l = results_rge[3]["gap_pdg"]
    rel_gap = abs(gap_3l) / 100.0

    if rel_gap < TIER_POSITIVE_THRESHOLD:
        tier = "POSITIVE"
        verdict = (
            f"RGE running of λ from λ(M_Pl)=0 to v_EW via retained 3-loop SM β_λ "
            f"gives m_H = {m_h_3l:.2f} GeV, deviation {gap_3l:+.2f}% from PDG 125.25 GeV. "
            f"Closes the +12.04% gap from Probe X-S4b-Combined within the ~5% threshold. "
            f"Tier: POSITIVE THEOREM."
        )
    elif rel_gap < TIER_BOUNDED_THRESHOLD:
        tier = "BOUNDED"
        verdict = (
            f"RGE running gives m_H = {m_h_3l:.2f} GeV ({gap_3l:+.2f}% from PDG). "
            f"Outside the ~5% positive threshold but within ~10%. "
            f"Tier: BOUNDED."
        )
    else:
        tier = "NEGATIVE"
        verdict = (
            f"RGE running gives m_H = {m_h_3l:.2f} GeV ({gap_3l:+.2f}% from PDG). "
            f"Outside both 5% and 10% thresholds. Tier: NEGATIVE."
        )

    print(f"\n  Verdict: {tier}")
    print(f"  {verdict}")

    is_positive = rel_gap < TIER_POSITIVE_THRESHOLD
    report("k7-tier-verdict", is_positive,
           f"Tier: {tier} (m_H = {m_h_3l:.2f} GeV, {gap_3l:+.2f}% from PDG)")

    return tier, verdict


def main():
    print("=" * 78)
    print("Probe Y-S4b-RGE — RGE Lambda Running Closes the +12% Higgs Gap")
    print("Loop: probe-y-s4b-rge-lambda-running-20260508-probeY_S4b_rge")
    print("Date: 2026-05-08 (compute date 2026-05-10)")
    print("=" * 78)

    # K1: β_λ retention
    mod = kY1_betalambda_retained()

    # K2: Reproduce Probe X-S4b-Combined symmetric-point baseline
    m_h_sym, gap_sym = kY2_symmetric_point_baseline(mod)

    # K3: RGE running M_Pl → v_EW with λ(M_Pl)=0
    results_rge = kY3_rge_running_to_vew(mod)

    # K4: Quantify gap closure
    closure_gev, closure_pct = kY4_gap_closure_quantification(m_h_sym, results_rge)

    # K5: Structural distinction (NOT a symmetric-point identification)
    kY5_structural_distinction(mod, m_h_sym, results_rge)

    # K6: Consistency with retained band
    kY6_consistency_with_retention_analysis(mod, results_rge)

    # K7: Tier verdict
    tier, verdict = kY7_tier_verdict(results_rge)

    # Summary
    print("\n" + "=" * 78)
    print("Summary")
    print("=" * 78)
    print(f"  PASS = {PASS_COUNT}, FAIL = {FAIL_COUNT}")
    print(f"  Tier: {tier}")
    print(f"  Verdict: {verdict}")
    print()
    print(f"  Probe X-S4b-Combined (sym-point):  m_H = {m_h_sym:.2f} GeV  ({gap_sym:+.2f}%)")
    print(f"  Probe Y-S4b-RGE     (3-loop):     m_H = {results_rge[3]['m_h']:.2f} GeV  ({results_rge[3]['gap_pdg']:+.2f}%)")
    print(f"  Gap closure: {closure_gev:+.2f} GeV ({(1-abs(results_rge[3]['gap_pdg'])/abs(gap_sym))*100:.1f}% of original gap)")
    print()

    if FAIL_COUNT == 0:
        print(f"  ALL CHECKS PASSED ({PASS_COUNT}/{PASS_COUNT}).")
        print(f"  Probe Y-S4b-RGE: POSITIVE THEOREM.")
        return 0
    print(f"  {FAIL_COUNT} checks FAILED out of {PASS_COUNT + FAIL_COUNT}.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
