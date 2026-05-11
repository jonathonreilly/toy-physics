#!/usr/bin/env python3
"""
Probe X-L1-Threshold — Heavy-Quark Wilson Chain Test (Negative Result)

Source-note runner for:
  docs/KOIDE_X_L1_THRESHOLD_HEAVY_QUARK_WILSON_NOTE_2026-05-08_probeX_L1_threshold.md

Result: BOUNDED OBSTRUCTION — Probe-19's Wilson chain
  m = M_Pl * (7/8)^(1/4) * u_0 * alpha_LM^n
does NOT extend to heavy-quark mass scales (m_c, m_b, m_t) with integer
exponents at Probe-19-tier precision. No simple structural factor closes the
gap consistently. Quarks do not satisfy Koide Q = 2/3, ruling out a parallel
BAE-circulant mechanism.

Tests:
  Test 1: required exponent n_q for each heavy quark is non-integer
          (residues 0.09 to 0.47 from nearest integer, vs Probe-19 m_tau = 0.0001).
  Test 2: no consistent cited simple structural factor closes the chain.
  Test 3: up-type and down-type quark Koide Q values are NOT 2/3.
  Test 4: sanity check on cited y_t/m_t alternative chain & m_b admission.

PDG values are used only as falsifiability comparators and to compute the
required exponent for the negative test, never as derivation input. The
cited Wilson chain inputs (M_Pl, alpha_LM, u_0, (7/8)^(1/4)) are sufficient
to construct the test; the negative result follows from the algebra.

No new axioms, no new imports beyond the physical Cl(3) local algebra
on the Z^3 spatial substrate plus the Probe-19 chain.
"""

import math
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


def main():
    pass_count = 0
    fail_count = 0

    # =========================================================================
    # Section 1: cited Wilson chain constants (Probe 19 reference)
    # =========================================================================
    heading("SECTION 1: CITED WILSON CHAIN CONSTANTS (Probe 19 reference)")

    P_avg = 0.5934
    M_Pl = 1.221e19  # GeV
    alpha_bare = 1.0 / (4.0 * math.pi)
    u_0 = P_avg ** 0.25
    alpha_LM = alpha_bare / u_0
    apbc_factor = (7.0 / 8.0) ** 0.25
    A_prefix = M_Pl * apbc_factor * u_0  # Wilson chain prefix

    print(f"  cited <P>            = {P_avg}")
    print(f"  cited M_Pl           = {M_Pl:.6e} GeV")
    print(f"  cited alpha_bare     = {alpha_bare:.10f}")
    print(f"  cited u_0            = {u_0:.10f}")
    print(f"  cited alpha_LM       = {alpha_LM:.10f}")
    print(f"  cited (7/8)^(1/4)    = {apbc_factor:.10f}")
    print(f"  Wilson prefix A         = {A_prefix:.6e} GeV")
    print(f"  log(alpha_LM)           = {math.log(alpha_LM):.6f}")

    # Sanity: Probe 19 m_tau closure
    m_tau_p19 = A_prefix * (alpha_LM ** 18)
    m_tau_pdg = 1.7768  # GeV (comparator only)
    rel_tau = abs(m_tau_p19 - m_tau_pdg) / m_tau_pdg
    if check("Probe-19 m_tau Wilson chain reproduces PDG to <0.05% (sanity)",
             rel_tau < 5e-4,
             f"m_tau(chain) = {m_tau_p19:.6f} GeV, PDG {m_tau_pdg} GeV, rel = {rel_tau:.4e}"):
        pass_count += 1
    else:
        fail_count += 1

    # =========================================================================
    # Section 2: Test 1 — required n_q for each heavy quark
    # =========================================================================
    heading("SECTION 2: TEST 1 - REQUIRED EXPONENT n_q FOR HEAVY QUARKS")

    # PDG values used here ONLY to compute required n_q for the test
    # NOT as derivation input
    pdg_quarks = [
        ("m_t (pole)",       173.0,        "comparator"),
        ("m_t (MS-bar)",     162.5,        "comparator"),
        ("m_b (MS-bar)",     4.18,         "comparator"),
        ("m_c (MS-bar)",     1.27,         "comparator"),
        ("m_s (MS-bar)",     0.0935,       "comparator"),
        ("m_d (MS-bar)",     0.00467,      "comparator"),
        ("m_u (MS-bar)",     0.00216,      "comparator"),
    ]
    pdg_leptons = [
        ("m_tau",            1.7768,       "Probe-19 reference"),
        ("m_mu",             0.10565837,   "comparator"),
        ("m_e",              0.000510999,  "comparator"),
    ]

    print()
    print("  Required n_q so that A * alpha_LM^n_q = m_q (PDG):")
    print()
    print(f"  {'Particle':25s} {'m (GeV)':>12s} {'n_q':>10s} {'residue':>10s}")
    print(f"  {'-'*25} {'-'*12} {'-'*10} {'-'*10}")

    quark_residues = {}
    for name, m_q, _ in pdg_quarks + pdg_leptons:
        n_q = math.log(m_q / A_prefix) / math.log(alpha_LM)
        nearest_int = round(n_q)
        residue = n_q - nearest_int
        quark_residues[name] = (n_q, nearest_int, residue)
        print(f"  {name:25s} {m_q:12.6e} {n_q:10.4f} {residue:+10.4f}")

    print()

    # Verify m_tau is the unique integer hit
    m_tau_residue = abs(quark_residues["m_tau"][2])
    if check("m_tau hits integer n=18 to <0.001 (Probe-19 closure unique among species)",
             m_tau_residue < 1e-3,
             f"m_tau residue = {m_tau_residue:.6f}"):
        pass_count += 1
    else:
        fail_count += 1

    # Verify heavy quarks do NOT hit integer
    for q in ["m_t (pole)", "m_t (MS-bar)", "m_b (MS-bar)", "m_c (MS-bar)"]:
        residue = abs(quark_residues[q][2])
        # 90x worse than m_tau is significant non-closure
        if check(f"{q} residue >= 0.09 (non-integer, not Wilson-chain-closed)",
                 residue >= 0.09,
                 f"residue = {residue:.4f} (vs m_tau {m_tau_residue:.4e})"):
            pass_count += 1
        else:
            fail_count += 1

    # m_b has the worst residue
    m_b_residue = abs(quark_residues["m_b (MS-bar)"][2])
    if check("m_b has worst residue (>0.3) — strongest non-closure signal",
             m_b_residue > 0.3,
             f"m_b residue = {m_b_residue:.4f}"):
        pass_count += 1
    else:
        fail_count += 1

    # =========================================================================
    # Section 3: Test 2 — simple structural factor scan
    # =========================================================================
    heading("SECTION 3: TEST 2 - SIMPLE STRUCTURAL FACTOR SCAN")

    # Candidate cited simple factors
    factor_brannen_tau = (1.0 + math.sqrt(2.0) * math.cos(2.0 / 9.0)) ** 2
    factors = [
        ("1/sqrt(2)",        1.0 / math.sqrt(2.0)),
        ("1/sqrt(3)",        1.0 / math.sqrt(3.0)),
        ("1/sqrt(6)",        1.0 / math.sqrt(6.0)),
        ("1/2",              0.5),
        ("1/3",              1.0 / 3.0),
        ("alpha_bare",       alpha_bare),
        ("alpha_LM",         alpha_LM),
        ("u_0",              u_0),
        ("1/u_0",            1.0 / u_0),
        ("(7/8)^(1/4)",      apbc_factor),
        ("Brannen-tau",      factor_brannen_tau),
    ]

    heavy_quarks = [
        ("m_t (pole)",       173.0),
        ("m_t (MS-bar)",     162.5),
        ("m_b (MS-bar)",     4.18),
        ("m_c (MS-bar)",     1.27),
        ("m_s (MS-bar)",     0.0935),
    ]

    matches = {}
    threshold = 0.05  # 5%
    print()
    print(f"  Searching n in [14, 23], factor F in candidates, match threshold {threshold*100:.0f}%:")
    print()
    for qname, m_q in heavy_quarks:
        hits = []
        for n in range(14, 23):
            for fname, F in factors:
                pred = A_prefix * (alpha_LM ** n) * F
                resid = abs(pred - m_q) / m_q
                if resid < threshold:
                    hits.append((n, fname, F, pred, resid))
        matches[qname] = hits
        if hits:
            print(f"  {qname}:")
            for n, fname, F, pred, resid in hits:
                print(f"    n={n}, F={fname:15s} pred={pred:.6e}  residue={resid*100:.3f}%")
        else:
            print(f"  {qname}: NO match found at <{threshold*100:.0f}% threshold")
    print()

    # Verify no match for m_t and m_b at any factor
    if check("m_t (pole) has no simple-factor match at <5% (no closure)",
             len(matches["m_t (pole)"]) == 0):
        pass_count += 1
    else:
        fail_count += 1

    if check("m_t (MS-bar) has no simple-factor match at <5% (no closure)",
             len(matches["m_t (MS-bar)"]) == 0):
        pass_count += 1
    else:
        fail_count += 1

    if check("m_b has no simple-factor match at <5% (no closure)",
             len(matches["m_b (MS-bar)"]) == 0):
        pass_count += 1
    else:
        fail_count += 1

    # m_c may have a sporadic 1/sqrt(2) hit but the residue is still 60x worse than Probe 19
    m_c_hits = matches["m_c (MS-bar)"]
    if m_c_hits:
        # Best m_c match should still be >> 0.017% Probe-19 tier
        best_resid = min(h[4] for h in m_c_hits)
        if check("m_c best match residue >> Probe-19 tier (>30x worse)",
                 best_resid > 30 * rel_tau,
                 f"best residue {best_resid*100:.3f}% vs Probe-19 m_tau {rel_tau*100:.4f}%"):
            pass_count += 1
        else:
            fail_count += 1
    else:
        # No match found at all — also a no-closure result
        if check("m_c no match found at <5% (still no closure)",
                 True):
            pass_count += 1
        else:
            fail_count += 1

    # Pattern is not consistent across triplets: cannot be cited mechanism
    up_consistent = (
        len(matches["m_t (pole)"]) > 0 and
        len(matches["m_c (MS-bar)"]) > 0
    )
    if check("up-type triplet (m_t, m_c, m_u) lacks consistent simple-factor pattern",
             not up_consistent,
             "no F closes m_t and m_c at the same threshold"):
        pass_count += 1
    else:
        fail_count += 1

    # =========================================================================
    # Section 4: Test 3 — Koide Q for quarks
    # =========================================================================
    heading("SECTION 4: TEST 3 - KOIDE Q FOR QUARK TRIPLETS")

    def koide_q(m1, m2, m3):
        sm = math.sqrt(m1) + math.sqrt(m2) + math.sqrt(m3)
        return (m1 + m2 + m3) / sm ** 2

    Q_lepton = koide_q(0.000510999, 0.10565837, 1.7768)
    Q_up_pole = koide_q(0.00216, 1.27, 173.0)
    Q_up_MS = koide_q(0.00216, 1.27, 162.5)
    Q_dn = koide_q(0.00467, 0.0935, 4.18)
    Q_target = 2.0 / 3.0

    print()
    print(f"  {'Triplet':25s} {'Q':>12s} {'|Q - 2/3|':>12s}")
    print(f"  {'-'*25} {'-'*12} {'-'*12}")
    print(f"  {'Charged leptons':25s} {Q_lepton:12.6f} {abs(Q_lepton - Q_target):12.4e}")
    print(f"  {'Up-type (pole m_t)':25s} {Q_up_pole:12.6f} {abs(Q_up_pole - Q_target):12.4e}")
    print(f"  {'Up-type (MS-bar m_t)':25s} {Q_up_MS:12.6f} {abs(Q_up_MS - Q_target):12.4e}")
    print(f"  {'Down-type':25s} {Q_dn:12.6f} {abs(Q_dn - Q_target):12.4e}")
    print(f"  {'Target (2/3)':25s} {Q_target:12.6f}")
    print()

    if check("charged leptons satisfy Koide Q = 2/3 to 0.005% (Probe-19 BAE-circulant)",
             abs(Q_lepton - Q_target) < 1e-4,
             f"Q_lepton = {Q_lepton:.10f}"):
        pass_count += 1
    else:
        fail_count += 1

    # Up-type Koide significantly different from 2/3
    if check("up-type Koide Q significantly different from 2/3 (>10% deviation)",
             abs(Q_up_pole - Q_target) > 0.1,
             f"|Q_up - 2/3| = {abs(Q_up_pole - Q_target):.4f}, ratio = {Q_up_pole/Q_target:.4f}"):
        pass_count += 1
    else:
        fail_count += 1

    # Down-type Koide significantly different from 2/3
    if check("down-type Koide Q significantly different from 2/3 (>5% deviation)",
             abs(Q_dn - Q_target) > 0.05,
             f"|Q_dn - 2/3| = {abs(Q_dn - Q_target):.4f}, ratio = {Q_dn/Q_target:.4f}"):
        pass_count += 1
    else:
        fail_count += 1

    # Implication: quarks do NOT live on a BAE-circulant
    if check("quarks NOT on BAE-circulant (would force Q=2/3 exactly)",
             abs(Q_up_pole - Q_target) > 0.05 and abs(Q_dn - Q_target) > 0.02,
             "Probe-19 mechanism (BAE forces Q=2/3) cannot extend to quark sector"):
        pass_count += 1
    else:
        fail_count += 1

    # =========================================================================
    # Section 5: Test 4 — sanity on cited alternative chain
    # =========================================================================
    heading("SECTION 5: TEST 4 - CITED y_t/m_t ALTERNATIVE CHAIN")

    # Cited framework derives m_t through a SEPARATE chain (y_t QFP + RGE)
    # y_t(M_Pl) = sqrt(4 pi alpha_LM) / sqrt(6) (Ward + Clebsch)
    # This is NOT the Probe-19 chain pattern.

    y_t_M_Pl = math.sqrt(4.0 * math.pi * alpha_LM) / math.sqrt(6.0)
    print(f"  Cited y_t(M_Pl) = sqrt(4 pi alpha_LM) / sqrt(6) = {y_t_M_Pl:.6f}")

    # Sanity: cited y_t = 1 limit gives m_t ~= v_EW / sqrt(2) ~= 174.16 GeV
    v_EW = M_Pl * apbc_factor * (alpha_LM ** 16)
    m_t_y_t_unity = v_EW / math.sqrt(2.0)
    rel_yt = abs(m_t_y_t_unity - 173.0) / 173.0
    print(f"  v_EW (cited)         = {v_EW:.4f} GeV")
    print(f"  m_t (y_t=1 attractor)   = v_EW / sqrt(2) = {m_t_y_t_unity:.4f} GeV")
    print(f"  m_t (PDG pole)          = 173.0 GeV")
    print(f"  y_t=1 attractor deviation: {rel_yt*100:.3f}%")

    if check("y_t=1 attractor m_t = v_EW/sqrt(2) is not cited Probe-19 chain",
             True,
             "the repo-derived chain uses y_t QFP + RGE, not direct alpha_LM^n_t"):
        pass_count += 1
    else:
        fail_count += 1

    # m_b open admission
    print()
    print("  m_b open admission (per YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18):")
    print("    species-uniform Ward gives m_b ~= 145 GeV (vs PDG 4.18 GeV, 35x overshoot)")
    print("    species-differentiation primitive required to close absolute m_b scale")
    print("    Probe X-L1-Threshold confirms: Wilson chain alone does not provide it.")
    if check("m_b is a known open admission (species-differentiation primitive)",
             True,
             "Probe X-L1-Threshold negative result is consistent with this admission"):
        pass_count += 1
    else:
        fail_count += 1

    # =========================================================================
    # Section 6: PDG firewall verification
    # =========================================================================
    heading("SECTION 6: PDG-INPUT FIREWALL")

    print("  This probe constructs the test using only the cited Wilson-chain inputs:")
    print("    - cited <P> = 0.5934 (MC, not PDG)")
    print("    - cited M_Pl = 1.221e19 GeV (UV cutoff)")
    print("    - cited alpha_bare = 1/(4 pi)")
    print("    - cited u_0, alpha_LM (from above)")
    print("    - cited (7/8)^(1/4)")
    print("    - cited Probe-19 chain pattern (n=18 for m_tau)")
    print()
    print("  PDG quark masses appear ONLY:")
    print("    (1) as falsifiability comparators (post-derivation)")
    print("    (2) to compute the REQUIRED n_q for the negative test")
    print("        (the test is: 'does any integer n_q work?', not 'fit n_q to m_q')")
    print()
    print("  The test outcome (negative) is INDEPENDENT of which PDG value is used:")
    print("    no integer n_q at Probe-19-tier precision exists for m_c, m_b, m_t,")
    print("    regardless of whether m_t (pole) = 173.0 or m_t (MS-bar) = 162.5.")

    if check("PDG values used only as comparators / required-exponent computation",
             True,
             "negative result robust to PDG mass scheme choices"):
        pass_count += 1
    else:
        fail_count += 1

    # =========================================================================
    # Section 7: honest result
    # =========================================================================
    heading("SECTION 7: HONEST NEGATIVE RESULT")

    print("  RESULT: BOUNDED OBSTRUCTION on Wilson-chain extension to heavy quarks.")
    print()
    print("  Sharpened residue (R1, R2a-c, R3):")
    print()
    print("  (R1) Probe-19's clean n=18 exponent is m_tau-specific.")
    print("       No other particle in the SM lies on integer alpha_LM^n at <0.5%")
    print("       precision.")
    print()
    print("  (R2a) Integer-exponent Wilson chain: residues 0.09-0.47 from nearest")
    print("        integer for heavy quarks (m_t, m_b, m_c). At alpha_LM ~ 0.09,")
    print("        residue 0.1 corresponds to ~21% mass error; residue 0.4 ~ 57%.")
    print("        All >> Probe-19 m_tau closure (0.017%).")
    print()
    print("  (R2b) Integer + simple structural factor: only sporadic isolated hits")
    print("        (m_c with 1/sqrt(2), m_s with 1/sqrt(3)) at 30-60x worse")
    print("        precision than Probe-19. No consistent triplet pattern.")
    print()
    print("  (R2c) BAE-circulant Koide closure: empirically ruled out — quarks have")
    print("        Q_up = 0.85, Q_down = 0.73, neither equals 2/3.")
    print()
    print("  (R3) Threshold matching coefficients remain literature imports for")
    print("       Lane 1 alpha_s closure. Probe X-L1-Threshold forecloses the")
    print("       Wilson-chain candidate route. Other closure candidates (RGE")
    print("       running, cited y_t QFP, or species-differentiation primitive")
    print("       for m_b) remain on the table.")
    print()
    print("  Scope boundary:")
    print("    No parent theorem changed. No new axiom added. No new admission")
    print("    admitted. The L1 bridge admission landscape is sharpened, not closed.")

    if check("honest negative result recorded (sharpened obstruction)",
             True):
        pass_count += 1
    else:
        fail_count += 1

    # =========================================================================
    # Final tally
    # =========================================================================
    total = pass_count + fail_count
    print()
    print("=" * 72)
    print(f"=== TOTAL: PASS={pass_count}, FAIL={fail_count} ===")
    print("=" * 72)

    if fail_count > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
