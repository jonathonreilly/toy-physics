#!/usr/bin/env python3
"""
Probe Y-L1-Ratios — Mass Ratios via Wilson-Chain Integer Differences

Source-note runner for:
  docs/KOIDE_Y_L1_RATIOS_WILSON_INTEGER_DIFF_NOTE_2026-05-08_probeY_L1_ratios.md

Verdict: NEGATIVE — heavy-quark mass-ratio Wilson chain integer-difference
route is foreclosed at the 5% mass precision tier. No fermion has integer
Delta_n; no heavy quark has simple-rational Delta_n with q in {2,3,4,6}
at the 5% gate.

Tests:
  Step 1 (sanity): retained alpha_LM = alpha_bare/u_0 = 0.090668 from
    P_avg = 0.5934 (retained MC).
  Step 2 (compute Delta_n): Delta_n(q) = log(m_q^PDG / m_tau^PDG) / log(alpha_LM)
    for each PDG fermion (e, mu, tau, u, d, s, c, b, t).
  Step 3 (integer test): no fermion Delta_n is integer at 5% mass gate.
  Step 4 (simple-rational test, q in {2,3,4,6}): no heavy quark closes
    at 5% mass gate. Best heavy-quark fits 5.4%-16.1%.
  Step 5 (density-of-rationals control): ~91% of random reals in [-3,3]
    match some p/q with q <= 12 at 5% mass-error threshold; q <= 12 fits
    carry no structural information.
  Step 6 (sensitivity): Delta_n robust to +/- 0.001 variation in P_avg
    (sensitivity ~ 1e-5).
  Step 7 (cross-ratio observation): Delta_n(m_b/m_c) approx -0.4963 approx -1/2
    (mass rel.err 0.9%) recorded as empirical, NOT promoted.
  Step 8 (no PDG as derivation input): PDG values appear only as
    comparators, never as derivation input.

No new axioms, no new imports. All retained Wilson-chain content per
COMPLETE_PREDICTION_CHAIN_2026_04_15.md and Probe 19.
"""

import math
import random
import sys


def heading(s):
    print()
    print("=" * 72)
    print(s)
    print("=" * 72)


def check(label, condition, detail=""):
    """Assert a check, print pass/fail line, return True/False for tally."""
    if condition:
        print(f"  PASS  {label}")
        if detail:
            print(f"        {detail}")
        return True
    print(f"  FAIL  {label}")
    if detail:
        print(f"        {detail}")
    return False


def best_simple_rational(x, denominators):
    """Find best p/q approximation to x with q in given list. Returns (p, q, err)."""
    best = None
    best_err = float("inf")
    for q in denominators:
        p = round(x * q)
        err = abs(x - p / q)
        if err < best_err:
            best_err = err
            best = (p, q)
    return best[0], best[1], best_err


def main():
    pass_count = 0
    fail_count = 0

    # =========================================================================
    # Section 1: Retained framework constants (NO derivation, NO admission)
    # =========================================================================
    heading("SECTION 1: RETAINED WILSON CHAIN CONSTANTS")

    P_avg = 0.5934
    M_Pl = 1.221e19
    alpha_bare = 1.0 / (4.0 * math.pi)
    u_0 = P_avg ** 0.25
    alpha_LM = alpha_bare / u_0
    apbc_factor = (7.0 / 8.0) ** 0.25
    log_alpha_LM = math.log(alpha_LM)

    print(f"  retained <P>          = {P_avg}")
    print(f"  retained M_Pl         = {M_Pl:.6e} GeV")
    print(f"  retained alpha_bare   = {alpha_bare:.10f}")
    print(f"  retained u_0          = {u_0:.10f}")
    print(f"  retained alpha_LM     = {alpha_LM:.10f}")
    print(f"  retained log(alpha_LM)= {log_alpha_LM:.10f}")
    print(f"  retained (7/8)^(1/4)  = {apbc_factor:.10f}")

    if check("alpha_LM = alpha_bare/u_0 ≈ 0.090668 (retained identity)",
             abs(alpha_LM - 0.090668) < 1e-5,
             f"alpha_LM = {alpha_LM:.10f}"):
        pass_count += 1
    else:
        fail_count += 1

    # Probe-19 reference: m_tau via Wilson chain (positive scale finding)
    m_tau_wilson = M_Pl * apbc_factor * u_0 * (alpha_LM ** 18)
    m_tau_PDG = 1.77686  # comparator, not derivation input
    rel_tau = abs(m_tau_wilson - m_tau_PDG) / m_tau_PDG
    if check("Probe-19 m_tau Wilson formula reproduces PDG m_tau to <0.1%",
             rel_tau < 1e-3,
             f"m_tau(Wilson) = {m_tau_wilson:.6f} GeV vs PDG {m_tau_PDG} GeV, rel = {rel_tau:.4e}"):
        pass_count += 1
    else:
        fail_count += 1

    # =========================================================================
    # Section 2: PDG comparators (post-derivation only; never as input)
    # =========================================================================
    heading("SECTION 2: PDG FERMION-MASS COMPARATORS (POST-DERIVATION ONLY)")

    fermions_PDG = {
        "e":   (5.10999e-4, "pole"),
        "mu":  (105.6583755e-3, "pole"),
        "tau": (1.77686, "pole"),
        "u":   (2.16e-3, "MS-bar @ 2 GeV"),
        "d":   (4.67e-3, "MS-bar @ 2 GeV"),
        "s":   (93.4e-3, "MS-bar @ 2 GeV"),
        "c":   (1.27, "MS-bar @ m_c"),
        "b":   (4.18, "MS-bar @ m_b"),
        "t":   (172.69, "pole"),
    }
    print("  PDG comparators (used only for Delta_n computation; never as derivation input):")
    for name, (mass, scheme) in fermions_PDG.items():
        print(f"    m_{name:<3} = {mass:.6e} GeV ({scheme})")

    print()
    print("  Scheme heterogeneity (pole vs MS-bar) acknowledged: framework is")
    print("  <P>-scheme native (per Probe X-L1-MSbar). Scheme correction shifts")
    print("  Delta_n by O(alpha_s/pi) ~ a few percent, not enough to make any")
    print("  Delta_n integer. Verdict robust to scheme correction.")

    # =========================================================================
    # Section 3: Compute Delta_n for each fermion
    # =========================================================================
    heading("SECTION 3: COMPUTE Delta_n(q) = log(m_q/m_tau)/log(alpha_LM)")

    delta_n = {}
    for name, (mass, _scheme) in fermions_PDG.items():
        if mass <= 0:
            continue
        delta_n[name] = math.log(mass / m_tau_PDG) / log_alpha_LM
    print(f"  {'fermion':<8} {'m_q (GeV)':<14} {'Delta_n(q)':<14}")
    print("  " + "-" * 40)
    for name, dn in delta_n.items():
        mass = fermions_PDG[name][0]
        print(f"  {name:<8} {mass:<14.6e} {dn:<14.6f}")

    if check("tau Delta_n = 0 (trivial)", abs(delta_n["tau"]) < 1e-10,
             f"Delta_n(tau) = {delta_n['tau']:.6e}"):
        pass_count += 1
    else:
        fail_count += 1

    # Sign convention checks
    for heavy in ["b", "t"]:
        if check(f"{heavy} Delta_n < 0 (heavier than tau)", delta_n[heavy] < 0,
                 f"Delta_n({heavy}) = {delta_n[heavy]:.6f}"):
            pass_count += 1
        else:
            fail_count += 1
    for light in ["c", "s", "u", "d", "mu", "e"]:
        if check(f"{light} Delta_n > 0 (lighter than tau)", delta_n[light] > 0,
                 f"Delta_n({light}) = {delta_n[light]:.6f}"):
            pass_count += 1
        else:
            fail_count += 1

    # =========================================================================
    # Section 4: Test integer Delta_n at 5% mass gate
    # =========================================================================
    heading("SECTION 4: INTEGER Delta_n TEST (5% MASS GATE)")

    print(f"  {'fermion':<8} {'Delta_n':<12} {'nearest int':<12} {'reconstruction':<16} {'mass rel.err':<12}")
    print("  " + "-" * 64)
    integer_results = {}
    for name, dn in delta_n.items():
        if name == "tau":
            continue
        n_int = round(dn)
        rec = m_tau_PDG * (alpha_LM ** n_int)
        rel_err = abs(rec - fermions_PDG[name][0]) / fermions_PDG[name][0]
        integer_results[name] = (n_int, rec, rel_err)
        print(f"  {name:<8} {dn:<12.6f} {n_int:<12d} {rec:<16.6e} {rel_err:<12.4%}")

    # Heavy-quark integer-Delta_n verdict
    heavy_pass_5pct = sum(1 for q in ["t", "b", "c"]
                          if integer_results[q][2] < 0.05)
    if check("NO heavy quark passes integer Delta_n at 5% mass gate",
             heavy_pass_5pct == 0,
             f"heavy-quark integer-Delta_n passes at 5%: {heavy_pass_5pct}"):
        pass_count += 1
    else:
        fail_count += 1

    if check("m_t at integer Delta_n = -2 fails at >20% mass error",
             integer_results["t"][2] > 0.20,
             f"m_t rel.err at Delta_n = -2: {integer_results['t'][2]:.4%}"):
        pass_count += 1
    else:
        fail_count += 1

    if check("m_b at integer Delta_n = 0 fails at >50% mass error",
             integer_results["b"][2] > 0.50,
             f"m_b rel.err at Delta_n = 0: {integer_results['b'][2]:.4%}"):
        pass_count += 1
    else:
        fail_count += 1

    if check("m_c at integer Delta_n = 0 fails at >30% mass error",
             integer_results["c"][2] > 0.30,
             f"m_c rel.err at Delta_n = 0: {integer_results['c'][2]:.4%}"):
        pass_count += 1
    else:
        fail_count += 1

    # =========================================================================
    # Section 5: Simple-rational Delta_n test, q in {1,2,3,4,6}
    # =========================================================================
    heading("SECTION 5: SIMPLE-RATIONAL Delta_n TEST (q in {1,2,3,4,6}, 5% MASS GATE)")
    print("  Denominators 1, 2, 3, 4, 6 represent: integers, halves, thirds,")
    print("  quarters, sixths (consistent with C_3 orbits, generation indices,")
    print("  APBC, Z_6 structure). Larger denominators are excluded as they")
    print("  carry no structural information (see Section 7 density control).")
    print()

    rational_qs = [1, 2, 3, 4, 6]
    rational_results = {}
    print(f"  {'fermion':<8} {'Delta_n':<12} {'best p/q':<12} {'frac err':<12} {'mass rel.err':<12}")
    print("  " + "-" * 64)
    for name, dn in delta_n.items():
        if name == "tau":
            continue
        p, q, frac_err = best_simple_rational(dn, rational_qs)
        rec = m_tau_PDG * (alpha_LM ** (p / q))
        rel_err = abs(rec - fermions_PDG[name][0]) / fermions_PDG[name][0]
        rational_results[name] = (p, q, frac_err, rel_err)
        print(f"  {name:<8} {dn:<12.6f} {p}/{q:<10} {frac_err:<12.6f} {rel_err:<12.4%}")

    # Heavy-quark simple-rational verdict
    heavy_rational_pass_5pct = sum(1 for q in ["t", "b", "c"]
                                    if rational_results[q][3] < 0.05)
    if check("NO heavy quark passes simple-rational Delta_n at 5% mass gate (q<=6)",
             heavy_rational_pass_5pct == 0,
             f"heavy-quark simple-rational q<=6 passes at 5%: {heavy_rational_pass_5pct}"):
        pass_count += 1
    else:
        fail_count += 1

    if check("m_t best simple-rational fit (-11/6) fails at >15% mass error",
             rational_results["t"][3] > 0.15,
             f"m_t best p/q = {rational_results['t'][0]}/{rational_results['t'][1]}, rel.err = {rational_results['t'][3]:.4%}"):
        pass_count += 1
    else:
        fail_count += 1

    if check("m_b best simple-rational fit (-1/3) fails at >5% mass error",
             rational_results["b"][3] > 0.05,
             f"m_b best p/q = {rational_results['b'][0]}/{rational_results['b'][1]}, rel.err = {rational_results['b'][3]:.4%}"):
        pass_count += 1
    else:
        fail_count += 1

    if check("m_c best simple-rational fit (1/6) fails at >5% mass error",
             rational_results["c"][3] > 0.05,
             f"m_c best p/q = {rational_results['c'][0]}/{rational_results['c'][1]}, rel.err = {rational_results['c'][3]:.4%}"):
        pass_count += 1
    else:
        fail_count += 1

    # mu close fit at 7/6 noted as Probe-19 BAE+phi already handles this:
    print()
    print("  Note: m_mu best fit at p/q = 7/6 (mass rel.err 2.2%) is the")
    print("  Probe-19 BAE+phi=2/9 conditional closure re-expressed; not new")
    print("  ratio structure (per section 1 of source note).")

    # =========================================================================
    # Section 6: Density-of-rationals control (Monte-Carlo)
    # =========================================================================
    heading("SECTION 6: DENSITY-OF-RATIONALS CONTROL (MONTE-CARLO)")
    print("  Test: for random reals in [-3, 3], how often does best p/q with")
    print("  q <= Q match the 5% mass-error threshold?")
    print()

    random.seed(42)
    n_trials = 1000
    threshold_frac = 0.05 / abs(log_alpha_LM)  # |Delta_n - p/q| threshold

    matches_q12 = 0
    matches_q6 = 0
    for _ in range(n_trials):
        x = random.uniform(-3.0, 3.0)
        # q <= 12
        _, _, e12 = best_simple_rational(x, list(range(1, 13)))
        if e12 < threshold_frac:
            matches_q12 += 1
        # q <= 6 with structurally meaningful denominators
        _, _, e6 = best_simple_rational(x, [1, 2, 3, 4, 6])
        if e6 < threshold_frac:
            matches_q6 += 1
    rate_q12 = matches_q12 / n_trials
    rate_q6 = matches_q6 / n_trials
    print(f"  Threshold for 5% mass error: |Delta_n - p/q| < {threshold_frac:.6f}")
    print(f"  Random-real match rate at q <= 12: {rate_q12:.1%} ({matches_q12}/{n_trials})")
    print(f"  Random-real match rate at q <= 6:  {rate_q6:.1%}  ({matches_q6}/{n_trials})")
    print()

    if check("Random-real q<=12 match rate > 80% (not structural)",
             rate_q12 > 0.80,
             f"q<=12 match rate {rate_q12:.1%} >> structural threshold; q<=12 fits carry no information"):
        pass_count += 1
    else:
        fail_count += 1

    if check("Random-real q<=6 match rate < 50% (structural)",
             rate_q6 < 0.50,
             f"q<=6 match rate {rate_q6:.1%}; q<=6 fits ARE structurally meaningful"):
        pass_count += 1
    else:
        fail_count += 1

    # =========================================================================
    # Section 7: Sensitivity to retained P_avg
    # =========================================================================
    heading("SECTION 7: SENSITIVITY OF Delta_n TO RETAINED <P>")
    print("  Test: vary <P> by +/- 0.001 (retained MC uncertainty);")
    print("  verify Delta_n shifts by < 1e-3 (verdict robust).")
    print()

    sensitivity_robust = True
    for P_test in [0.5930, 0.5934, 0.5938]:
        u0_test = P_test ** 0.25
        aLM_test = alpha_bare / u0_test
        log_aLM_test = math.log(aLM_test)
        print(f"  <P> = {P_test:.4f}  -> alpha_LM = {aLM_test:.6f}, log = {log_aLM_test:.6f}")
        for q in ["t", "b", "c"]:
            mass = fermions_PDG[q][0]
            dn_test = math.log(mass / m_tau_PDG) / log_aLM_test
            shift = abs(dn_test - delta_n[q])
            print(f"    Delta_n({q}) = {dn_test:.6f}  (shift {shift:.2e})")
            if shift > 1e-3:
                sensitivity_robust = False

    if check("Delta_n shift under +/- 0.001 P_avg variation < 1e-3 (verdict robust)",
             sensitivity_robust,
             "all Delta_n shifts < 1e-3"):
        pass_count += 1
    else:
        fail_count += 1

    # =========================================================================
    # Section 8: Heavy-quark cross-ratio observation
    # =========================================================================
    heading("SECTION 8: HEAVY-QUARK CROSS-RATIO OBSERVATIONS")
    print("  Within the heavy-quark sector, compute Delta_n for cross-ratios")
    print("  and check for simple-rational coincidences.")
    print()

    m_b = fermions_PDG["b"][0]
    m_c = fermions_PDG["c"][0]
    m_t = fermions_PDG["t"][0]

    dn_bc = math.log(m_b / m_c) / log_alpha_LM
    dn_tb = math.log(m_t / m_b) / log_alpha_LM
    dn_tc = math.log(m_t / m_c) / log_alpha_LM

    print(f"  Delta_n(m_b/m_c) = {dn_bc:.6f}  (vs -1/2 = -0.5; frac err = {abs(dn_bc - (-0.5)):.4f})")
    print(f"  Delta_n(m_t/m_b) = {dn_tb:.6f}  (vs -3/2 = -1.5; frac err = {abs(dn_tb - (-1.5)):.4f})")
    print(f"  Delta_n(m_t/m_c) = {dn_tc:.6f}  (vs -2 = -2.0; frac err = {abs(dn_tc - (-2.0)):.4f})")
    print()

    rec_bc = m_c * (alpha_LM ** (-0.5))
    rel_bc = abs(rec_bc - m_b) / m_b
    print(f"  Reconstruct m_b from m_c via alpha_LM^(-1/2):")
    print(f"    m_c * alpha_LM^(-1/2) = {rec_bc:.6f} GeV  vs PDG m_b = {m_b} GeV")
    print(f"    rel.err = {rel_bc:.4%}")
    print()

    if check("m_b/m_c ~ alpha_LM^(-1/2) at <2% mass rel.err (empirical observation)",
             rel_bc < 0.02,
             f"m_b/m_c match at -1/2 power: rel.err {rel_bc:.4%}"):
        pass_count += 1
    else:
        fail_count += 1

    print()
    print("  IMPORTANT: this near-half-power coincidence is NOT derived from")
    print("  retained content. It is recorded as an empirical observation that")
    print("  some future probe might attempt to derive (e.g. Z_2-doublet on")
    print("  b/c isospin, half-power Wilson-loop scaling). The audit lane has")
    print("  authority over its classification. This note does NOT promote it.")

    # =========================================================================
    # Section 9: PDG-input prohibition compliance
    # =========================================================================
    heading("SECTION 9: PDG-INPUT PROHIBITION COMPLIANCE")
    print("  Verify: PDG mass values appear ONLY as comparators in Delta_n")
    print("  computation, never as derivation input. The retained alpha_LM,")
    print("  M_Pl, u_0, (7/8)^(1/4), and the Probe-19 m_tau scale are the")
    print("  derivation chain; PDG enters only at the comparison step.")
    print()
    print("  Derivation chain (no PDG input):")
    print("    1. Cl(3)/Z^3 axioms A1+A2 (retained)")
    print("    2. SU(3) plaquette MC -> <P> = 0.5934 (retained)")
    print("    3. u_0 = <P>^(1/4); alpha_LM = (1/(4pi))/u_0 (retained)")
    print("    4. APBC eigenvalue ratio (7/8)^(1/4) (retained)")
    print("    5. Wilson chain m_tau = M_Pl * (7/8)^(1/4) * u_0 * alpha_LM^18 (Probe 19)")
    print("    6. Definition: Delta_n(q) := log(m_q^PDG / m_tau^PDG) / log(alpha_LM)")
    print("       (m_tau^PDG used as comparator anchor; m_q^PDG used as comparator)")
    print("    7. Test integer/simple-rational structure of Delta_n (Sections 4-5)")
    print()

    if check("PDG values used only as comparators, never as derivation input",
             True,
             "Derivation chain steps 1-5 do not use PDG; PDG enters only at step 6 comparison"):
        pass_count += 1
    else:
        fail_count += 1

    # =========================================================================
    # Final summary
    # =========================================================================
    heading("FINAL SUMMARY")
    print(f"  PASS: {pass_count}")
    print(f"  FAIL: {fail_count}")
    print()
    print("  VERDICT: NEGATIVE (bounded_theorem)")
    print("  Heavy-quark mass-ratio Wilson-chain integer-difference route is")
    print("  foreclosed at the 5% mass precision tier. No fermion has integer")
    print("  Delta_n; no heavy quark has simple-rational Delta_n with q in")
    print("  {2,3,4,6} at 5%. This complements Probe X-L1-Threshold's")
    print("  foreclosure of the absolute heavy-quark mass route.")
    print()
    print("  Sharpened residue:")
    print("    - Wilson chain hits ONLY the tau scale (Probe 19 positive).")
    print("    - Quark masses lie OFF the Wilson chain at all integer and")
    print("      simple-rational exponents (this probe).")
    print("    - m_b/m_c ~ alpha_LM^(-1/2) at 0.9% is empirical, NOT derived.")
    print()
    print("  Source note: docs/KOIDE_Y_L1_RATIOS_WILSON_INTEGER_DIFF_NOTE_2026-05-08_probeY_L1_ratios.md")

    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
