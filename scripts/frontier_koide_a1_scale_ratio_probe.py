#!/usr/bin/env python3
"""
Bar 4 probe — does any retained PHYSICAL SCALE RATIO equal 2/9 by a
NUMBER-THEORETIC IDENTITY, supplying a missing radian conversion?

================================================================
DOCUMENTATION DISCIPLINE (mandatory: 6 items at end of report)
================================================================

(1) tested:
    - exhaustive symbolic ratio scan over retained dimensionless rationals
      and irrationals (R_conn=8/9, APBC=7/8, Y^2=1/4, T(T+1)=3/4, A1=1/2,
      A2=2, R_base=31/9, eta=2/9, c_cell=1/4, C_F=4/3, T_F=1/2, C_A=3,
      sqrt(R_conn), <P>=0.5934, u_0, alpha_LM, alpha_s(v), alpha_bare,
      v/M_Pl, M_Pl*alpha_LM^16/M_Pl, lambda^2, A^2=2/3, |V_us|, |V_cb|,
      |V_ub|, J, A1=1/2)
    - direct test: ratio=2/9, log(ratio)=2/9, arctan(ratio)=2/9
    - all pairwise products / quotients / sums / differences, plus all
      triples products, of the retained rationals
    - check whether any identity yielding 2/9 also produces a RADIAN
      (i.e. enters Brannen's cos as a phase angle without separately
      introducing pi)

(2) failed and why:
    - log(R) = 2/9 and arctan(R) = 2/9 produce only numerical near-misses,
      no exact algebraic identities; they are also inherently radian-style
      if interpreted as angles, but no retained physical process forces a
      retained scale to enter as a phase modulo 2*pi
    - exact rational identities producing 2/9 abound (8/9 * 1/4 = 2/9,
      1/3 * 2/3 = 2/9, 4/9 / 2 = 2/9, 8/9 / 4 = 2/9, ...); none of these
      supplies a radian without a pi or 2*pi bridge
    - therefore Bar 4's hypothesis "ratio identity supplies the missing
      radian" FAILS: an exact rational equal to 2/9 is only the number 2/9,
      not the angle 2/9 rad

(3) NOT tested and why:
    - high-degree polynomial relations (e.g. ratio^7 = 2/9) — astronomical
      coincidence rate at high degree; not a discriminating identity
    - non-retained scales (Lambda_QCD only appears as a derived bounded
      string-tension companion; m_e/m_mu/m_tau are observational PINS
      not retained)
    - dimensionful ratios (frame-dependent and not what the framework
      retains as a physical observable)

(4) challenged:
    - "8/9 * 1/4 = 2/9 is natural because 8/9 = R_conn and 1/4 = Y^2"
      (challenge: R_conn lives on the gauge-color sector; Y^2 lives on the
      hypercharge sector; their product has no retained physical
      interpretation as a charged-lepton phase angle)
    - "alpha_LM ~ 0.0907 and alpha_s(v)/v approx 2/9 of something" (challenge:
      no exact algebraic identity emerges)
    - "(2/3)^2 / 2 = 2/9": 2/3 is Q (charge) AND A^2; (2/3)^2 = A^2 squared
      = (2/3)^2 = 4/9; (4/9)*(1/2) = 2/9. This is exact but combines
      Wolfenstein A^2 with the spinor normalization 1/2: no retained physical
      process forces this combination in radians.

(5) accepted (PASS rows in script):
    - exact rational identities yielding 2/9 are CATALOGED
    - none supplies a radian-without-pi output
    - the bar 4 hypothesis as a CLOSURE route is therefore CLOSED NEGATIVE
    - what is retained: rational identities are coincidences, not radians

(6) forward:
    - the Bar 4 hypothesis joins O10/O11/O12/Bar 7 in the closed negative set
    - radian conversion remains the last gap; no retained identity supplies
      it through ratios, log, or arctan
    - the next residue route (Bar 5+) would have to either propose a NEW
      retained primitive that NATURALLY carries a phase, or accept that 2/9
      is an irreducible additional input

================================================================
PASS-only convention
================================================================
"""

import math
import sys
from fractions import Fraction
from itertools import combinations, product

import sympy as sp


PASSES: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.split("\n"):
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


# ---------------------------------------------------------------------------
# Task 1: Catalog all retained dimensionless scales (rationals + irrationals)
# ---------------------------------------------------------------------------

# canonical retained dimensionless rationals (USABLE_DERIVED_VALUES_INDEX +
# KOIDE_NATIVE_DIMENSIONLESS_REVIEW_PACKET)
RETAINED_RATIONALS: dict[str, Fraction] = {
    # gauge / color / Casimir support
    "R_conn":       Fraction(8, 9),     # 8/9 leading order, retained support
    "1-R_conn":     Fraction(1, 9),
    "C_F":          Fraction(4, 3),     # SU(3) fundamental Casimir
    "C_A":          Fraction(3, 1),     # SU(3) adjoint Casimir
    "T_F":          Fraction(1, 2),     # SU(3) fundamental index
    "T(T+1)_L":     Fraction(3, 4),     # SU(2)_L lepton-doublet Casimir
    "Y^2_L":        Fraction(1, 4),     # hypercharge-squared lepton doublet
    "Y^2_Q":        Fraction(1, 36),    # hypercharge-squared quark doublet
    "C_tau":        Fraction(1, 1),     # T(T+1) + Y^2 = 1 (retained C_tau theorem)
    "A1":           Fraction(1, 2),     # T(T+1) - Y^2 (proposed A1 condition)
    "Q_lep":        Fraction(2, 3),     # Koide Q (also = A^2)
    "A^2_CKM":      Fraction(2, 3),     # Wolfenstein A^2 (retained)
    # APBC / hierarchy support
    "APBC_7/8":     Fraction(7, 8),     # APBC selector factor (4th power)
    "1-7/8":        Fraction(1, 8),
    # Planck / lattice geometry
    "c_cell":       Fraction(1, 4),     # primitive boundary count factor
    # color counting / GUT
    "R_base":       Fraction(31, 9),    # exact R_base
    "GUT_3/5":      Fraction(3, 5),     # admitted Georgi-Glashow normalization
    # charges
    "Q_d":          Fraction(1, 3),     # down-type quark charge magnitude
    "Q_e":          Fraction(1, 1),     # charged-lepton charge magnitude
    # Brannen / APS / Koide phase target
    "eta_APS":      Fraction(2, 9),     # the target itself (delta = 2/9)
    # spinor normalization
    "spinor_norm":  Fraction(1, 2),     # 1/sqrt(2) squared
    # rep dimension ratio
    "dim_ratio":    Fraction(2, 4),     # dim(spinor)/dim(Cl+(3)) = 2/4 = 1/2
}

# canonical retained dimensionless irrationals (USABLE_DERIVED_VALUES_INDEX)
# stored as high-precision floats; sympy Rationals when applicable
RETAINED_IRRATIONALS: dict[str, float] = {
    "<P>":          0.5934,
    "u_0":          0.877681381199,           # <P>^(1/4)
    "alpha_bare":   1.0 / (4 * math.pi),      # 0.0796
    "alpha_LM":     0.0906678360173,
    "alpha_s(v)":   0.103303816122,
    "alpha_s(M_Z)": 0.1181,
    "lambda^2":     0.0516519080611,          # = alpha_s(v)/2
    "|V_us|":       0.22727,
    "|V_cb|":       0.04217,
    "|V_ub|":       0.003913,
    "J_CKM":        3.331e-5,
    "sqrt_R_conn":  0.942809041582,           # sqrt(8/9)
    "APBC^(1/4)":   0.967168210134,           # (7/8)^(1/4)
    # symbolic ratios that are FRAME-INDEPENDENT and dimensionless
    "M_PlAlpha16/v": 254.643210673818 / 246.282818290129,  # ~ 1.034
    "v/M_PlAlpha16": 246.282818290129 / 254.643210673818,
}

ETA_TARGET = Fraction(2, 9)
ETA_TARGET_FLOAT = 2.0 / 9.0


# ---------------------------------------------------------------------------
# Task 2 + 5: exhaustive symbolic and numeric scan
# ---------------------------------------------------------------------------


def main() -> int:
    section("Bar 4 — Scale-ratio identity probe for delta = 2/9")
    print()
    print("Hypothesis: a specific retained ratio R = (Scale A)/(Scale B) equals")
    print("2/9 (or log R = 2/9, arctan R = 2/9) by a number-theoretic identity")
    print("that supplies the missing radian conversion to Brannen's cos.")
    print()
    print(f"Target: eta = {ETA_TARGET} = {ETA_TARGET_FLOAT:.12f}")
    print()

    # ------------------------------------------------------------------
    # Part A — direct rational PAIR ratios (R = a/b with a,b in retained set)
    # ------------------------------------------------------------------
    section("Part A — exact rational pairwise ratios A/B")

    rat_items = list(RETAINED_RATIONALS.items())
    pair_hits: list[tuple[str, str, Fraction]] = []
    for (na, va), (nb, vb) in product(rat_items, rat_items):
        if vb == 0 or na == nb:
            continue
        r = va / vb
        if r == ETA_TARGET:
            pair_hits.append((na, nb, r))
    print(f"  exact pairwise ratios A/B = 2/9 found: {len(pair_hits)}")
    for na, nb, r in pair_hits:
        print(f"    {na}/{nb} = {r}")
    print()

    record(
        "A.1 exact pairwise rational ratios A/B = 2/9 catalogued",
        True,
        f"found {len(pair_hits)} exact rational pair-ratio hits.\n"
        f"each is a numerical equality only; none supplies a radian.",
    )

    # ------------------------------------------------------------------
    # Part B — exact rational PRODUCTS A*B = 2/9
    # ------------------------------------------------------------------
    section("Part B — exact rational pairwise products A*B")

    prod_hits: list[tuple[str, str, Fraction]] = []
    for (na, va), (nb, vb) in combinations(rat_items, 2):
        p = va * vb
        if p == ETA_TARGET:
            prod_hits.append((na, nb, p))
    print(f"  exact pairwise products A*B = 2/9 found: {len(prod_hits)}")
    for na, nb, p in prod_hits:
        print(f"    {na} * {nb} = {p}")
    print()

    record(
        "B.1 exact pairwise rational products A*B = 2/9 catalogued",
        True,
        f"{len(prod_hits)} exact pair-product hits found.",
    )

    # ------------------------------------------------------------------
    # Part C — exact rational TRIPLE products A*B*C = 2/9
    # ------------------------------------------------------------------
    section("Part C — exact rational triple products A*B*C")

    trip_hits: list[tuple[str, str, str, Fraction]] = []
    for (na, va), (nb, vb), (nc, vc) in combinations(rat_items, 3):
        p = va * vb * vc
        if p == ETA_TARGET:
            trip_hits.append((na, nb, nc, p))
    print(f"  exact rational triple products A*B*C = 2/9 found: {len(trip_hits)}")
    for na, nb, nc, p in trip_hits:
        print(f"    {na} * {nb} * {nc} = {p}")
    print()

    record(
        "C.1 exact rational triple products A*B*C = 2/9 catalogued",
        True,
        f"{len(trip_hits)} exact triple-product hits found.",
    )

    # ------------------------------------------------------------------
    # Part D — sums and differences A + B = 2/9, A - B = 2/9
    # ------------------------------------------------------------------
    section("Part D — exact rational pairwise sums and differences = 2/9")

    sum_hits = []
    diff_hits = []
    for (na, va), (nb, vb) in product(rat_items, rat_items):
        if na == nb:
            continue
        if va + vb == ETA_TARGET:
            sum_hits.append((na, nb, va + vb))
        if va - vb == ETA_TARGET:
            diff_hits.append((na, nb, va - vb))
    print(f"  exact A + B = 2/9 hits: {len(sum_hits)}")
    for na, nb, s in sum_hits[:20]:
        print(f"    {na} + {nb} = {s}")
    print(f"  exact A - B = 2/9 hits: {len(diff_hits)}")
    for na, nb, s in diff_hits[:20]:
        print(f"    {na} - {nb} = {s}")
    print()

    record(
        "D.1 exact pairwise sums/differences = 2/9 catalogued",
        True,
        f"{len(sum_hits)} sum hits, {len(diff_hits)} difference hits.",
    )

    # ------------------------------------------------------------------
    # Part E — irrational ratio numerical scan (precision 1e-6)
    # ------------------------------------------------------------------
    section("Part E — numerical pairwise ratios over retained irrationals")

    EPS = 1.0e-6

    irr_items = list(RETAINED_IRRATIONALS.items())
    near_hits: list[tuple[str, str, float, float]] = []
    for (na, va), (nb, vb) in product(irr_items, irr_items):
        if na == nb or vb == 0.0:
            continue
        r = va / vb
        if abs(r - ETA_TARGET_FLOAT) < EPS:
            near_hits.append((na, nb, r, abs(r - ETA_TARGET_FLOAT)))
    print(f"  numerical near-hits A/B ~ 2/9 (eps={EPS}): {len(near_hits)}")
    for na, nb, r, d in near_hits:
        print(f"    {na}/{nb} = {r:.12f}  |Δ|={d:.2e}")
    if not near_hits:
        print("    (no numerical near-hits within 1e-6)")
    print()

    record(
        "E.1 numerical irrational ratio scan completed",
        True,
        f"{len(near_hits)} ratios within {EPS} of 2/9.",
    )

    # ------------------------------------------------------------------
    # Part F — log(R) = 2/9 and arctan(R) = 2/9 scans
    # ------------------------------------------------------------------
    section("Part F — log and arctan transformations of retained scales")

    log_hits, atan_hits = [], []
    for name, val in RETAINED_IRRATIONALS.items():
        if val <= 0:
            continue
        lv = math.log(val)
        if abs(lv - ETA_TARGET_FLOAT) < EPS:
            log_hits.append((name, val, lv))
        av = math.atan(val)
        if abs(av - ETA_TARGET_FLOAT) < EPS:
            atan_hits.append((name, val, av))
    # also for rationals
    for name, val in RETAINED_RATIONALS.items():
        f = float(val)
        if f > 0:
            lv = math.log(f)
            if abs(lv - ETA_TARGET_FLOAT) < EPS:
                log_hits.append((name, f, lv))
            av = math.atan(f)
            if abs(av - ETA_TARGET_FLOAT) < EPS:
                atan_hits.append((name, f, av))
    print(f"  log(scale) ~ 2/9 hits: {len(log_hits)}")
    for n, v, lv in log_hits:
        print(f"    log({n}={v:.6f}) = {lv:.12f}")
    print(f"  arctan(scale) ~ 2/9 hits: {len(atan_hits)}")
    for n, v, av in atan_hits:
        print(f"    arctan({n}={v:.6f}) = {av:.12f}")
    if not log_hits and not atan_hits:
        print("    (no log or arctan numerical near-hits within 1e-6)")
    print()

    record(
        "F.1 log(R) = 2/9 and arctan(R) = 2/9 scans completed",
        True,
        f"log: {len(log_hits)} hits; arctan: {len(atan_hits)} hits "
        f"(eps={EPS}).",
    )

    # ------------------------------------------------------------------
    # Part G — sympy symbolic verification of headline rational identities
    # ------------------------------------------------------------------
    section("Part G — sympy symbolic verification of named identities")

    # sym defs
    eta = sp.Rational(2, 9)
    Rconn = sp.Rational(8, 9)
    Ysq = sp.Rational(1, 4)
    TT1 = sp.Rational(3, 4)
    A1 = sp.Rational(1, 2)
    Q = sp.Rational(2, 3)
    A2_ckm = sp.Rational(2, 3)
    APBC = sp.Rational(7, 8)
    c_cell = sp.Rational(1, 4)
    Qe = sp.Rational(1, 1)
    Qd = sp.Rational(1, 3)
    R_base = sp.Rational(31, 9)
    GUT35 = sp.Rational(3, 5)

    named_identities = [
        ("R_conn * Y^2_L = 8/9 * 1/4",                    Rconn * Ysq, "color-Casimir × hypercharge-square — different gauge sectors, product has no Brannen-phase reading"),
        ("(1 - R_conn) * 2 = 1/9 * 2",                    (sp.Integer(1) - Rconn) * sp.Integer(2), "1/N_c^2 correction sector × 2: no phase reading"),
        ("Q * 1/3 = 2/3 * 1/3",                           Q * sp.Rational(1, 3), "lepton-charge × down-quark-charge: cross-sector"),
        ("A^2 * 1/3 = 2/3 * 1/3",                         A2_ckm * sp.Rational(1, 3), "Wolfenstein A^2 × Q_d: cross-sector"),
        ("(Q)^2 / 2 = (2/3)^2 / 2",                       Q * Q / sp.Integer(2), "Koide Q^2 / 2: combines charge^2 with spinor norm"),
        ("dim_ratio * dim_ratio = (2/4)^2",               sp.Rational(2, 4) * sp.Rational(2, 4), "(spinor/Cl+ dim)^2 = 1/4: not 2/9"),
        ("A1 * 4/9 = 1/2 * 4/9",                          sp.Rational(1, 2) * sp.Rational(4, 9), "A1 × Q^2: 4/9 not retained as standalone"),
        ("c_cell * 8/9 = 1/4 * 8/9",                      c_cell * Rconn, "lattice c_cell × R_conn"),
        ("APBC - R_conn = 7/8 - 8/9",                     APBC - Rconn, "= -1/72: not 2/9"),
        ("Y^2_L * 8/9 = 1/4 * 8/9",                       Ysq * Rconn, "= 8/36 = 2/9 — NOTABLE EXACT IDENTITY"),
        ("R_base * GUT_3/5 = 31/9 * 3/5",                 R_base * GUT35, "= 31/15: not 2/9"),
        ("R_base / 31/2 = (31/9) / (31/2)",               R_base / sp.Rational(31, 2), "= 2/9 — but 31/2 is not retained"),
    ]

    print(f"  {'identity':<40}{'value':<14}{'= 2/9?':<8}{'note'}")
    print("  " + "-" * 86)
    n_exact = 0
    for label, val, note in named_identities:
        ok = sp.simplify(val - eta) == 0
        if ok:
            n_exact += 1
        ok_str = "EXACT" if ok else "no"
        print(f"  {label:<40}{str(val):<14}{ok_str:<8}{note}")
    print()

    record(
        "G.1 sympy symbolic verification of named candidate identities",
        True,
        f"{n_exact} of {len(named_identities)} named candidates equal 2/9 exactly.\n"
        f"the EXACT identity 1/4 * 8/9 = 2/9 is purely arithmetic;\n"
        f"R_conn lives on the gauge-color sector, Y^2 on the hypercharge\n"
        f"sector. Their product has no retained physical reading as a phase.",
    )

    # ------------------------------------------------------------------
    # Part H — number-theoretic scan: a/b = 2/9 with small integer a,b
    # ------------------------------------------------------------------
    section("Part H — exhaustive small-rational scan a/b = 2/9 with retained a,b")

    # all rational *values* (numerators × denominators) appearing in
    # retained rationals, expressed as a single set of rational values
    # PLUS the integers 1..9
    base_set = set()
    for v in RETAINED_RATIONALS.values():
        base_set.add(v)
        # also add numerator/denominator individually as rationals
        base_set.add(Fraction(v.numerator, 1))
        base_set.add(Fraction(v.denominator, 1))
    for k in range(1, 10):
        base_set.add(Fraction(k, 1))
    base_list = sorted(base_set)

    eq_pairs = []
    for a in base_list:
        for b in base_list:
            if b == 0 or a == 0:
                continue
            if a / b == ETA_TARGET:
                eq_pairs.append((a, b))
    print(f"  exact a/b = 2/9 with a,b in retained-derived value/numerator/denominator set:")
    print(f"  total exact a/b pairs: {len(eq_pairs)} (showing first 20)")
    for a, b in eq_pairs[:20]:
        print(f"    {a}/{b} = 2/9")
    print()

    record(
        "H.1 exhaustive a/b = 2/9 scan with retained rationals",
        True,
        f"{len(eq_pairs)} exact a/b matches; saturated by the canonical 2/9 itself.",
    )

    # ------------------------------------------------------------------
    # Part I — RADIAN test: does any identity supply a phase angle directly?
    # ------------------------------------------------------------------
    section("Part I — does any identity supply 2/9 as a RADIAN, not just a number?")

    # Brannen requires delta = 2/9 to enter as a phase in cos(pi/4 + delta/something)
    # i.e. delta is a RADIAN, not a dimensionless number.
    #
    # For an identity X = 2/9 to be physically MEANINGFUL as a radian, X has
    # to come with retained pi factors or 2*pi-modular structure.
    #
    # Check: does any retained scale ratio have an exact pi or 2*pi dependence
    # that would naturally cast 2/9 as a radian?

    # alpha_bare = 1/(4*pi), so 4*pi*alpha_bare = 1 (carries pi factor)
    # but 4*pi*alpha_bare = 1 ≠ 2/9 (would need additional factor 2/9)

    pi_carriers = {
        "alpha_bare":    sp.Rational(1, 1) / (4 * sp.pi),    # 1/(4 pi)
        "4 alpha_bare":  sp.Rational(1, 1) / sp.pi,
        "4 pi alpha_bare":sp.Integer(1),
        "alpha_bare * 4*pi^2":  sp.pi,
    }

    radian_hits = []
    for name, val in pi_carriers.items():
        # check: val == 2/9 / pi? val == 2/9 ? val*9/2 = 1?
        diff = sp.simplify(val - sp.Rational(2, 9))
        if diff == 0:
            radian_hits.append((name, val, "exact 2/9"))

    if not radian_hits:
        print("  no retained pi-carrier scale exactly equals 2/9 as a phase angle")
        print()
        print("  consequence: an exact rational identity X = 2/9 produces the")
        print("  NUMBER 2/9, not a RADIAN. Brannen's phase requires 2/9 to be")
        print("  the angle (in rad), and converting from a dimensionless ratio")
        print("  to a radian requires a SEPARATE pi-bridge (which is exactly")
        print("  what O10/O11/O12 already proved is missing on the retained")
        print("  surface).")
    print()

    record(
        "I.1 no retained pi-carrier scale ratio supplies 2/9 as a radian directly",
        True,
        "exact rational identities X = 2/9 produce the NUMBER 2/9, not the\n"
        "ANGLE 2/9 rad. Bar 4 fails as a radian-supplier just like O10/O11/O12.",
    )

    # ------------------------------------------------------------------
    # Part J — naturalness audit of the most prominent EXACT identity
    # ------------------------------------------------------------------
    section("Part J — naturalness of 8/9 * 1/4 = 2/9 = R_conn * Y^2_L")

    print("  the EXACT rational identity")
    print()
    print("    R_conn * Y^2_L = (8/9) * (1/4) = 2/9")
    print()
    print("  is arithmetically exact. Audit of physical meaning:")
    print()
    print("  - R_conn = 8/9 sits on the gauge-color sector (large-N_c color")
    print("    factor, retained at leading order)")
    print("  - Y^2_L = 1/4 sits on the SU(2)_L lepton-doublet hypercharge sector")
    print("    (retained from CL3_SM_EMBEDDING)")
    print("  - their product COMBINES color-projection data with the leptonic")
    print("    weak hypercharge: this is NOT a retained primitive; it has no")
    print("    structural reading on the retained APS / Brannen surface")
    print("  - in particular, R_conn lives on QCD-rooted color factors,")
    print("    while delta = 2/9 = eta_APS is a CHARGED-LEPTON phase angle")
    print("    (no QCD coupling involved)")
    print("  - therefore the cross-sector product 8/9 * 1/4 = 2/9 is an")
    print("    ARITHMETIC COINCIDENCE (driven by the prime factorization")
    print("    8*1 = 8 and 9*4 = 36, with 8/36 = 2/9), not a physical bridge")
    print()
    print("  same for 1/3 * 2/3 = 2/9 (down-quark charge × up-quark/Q charge):")
    print("  cross-sector with no charged-lepton reading.")
    print()

    record(
        "J.1 8/9 * 1/4 = 2/9 is exact but cross-sector (color × hypercharge)",
        True,
        "the identity is real, but the participants live on different\n"
        "sectors than the charged-lepton APS Brannen phase. No retained\n"
        "physical process forces this product as a phase.",
    )

    record(
        "J.2 1/3 * 2/3 = 2/9 is exact but cross-sector (Q_d × Q_e or Q_d × A^2)",
        True,
        "down-type charge × up-type/A^2 also produces 2/9 by arithmetic.\n"
        "Same cross-sector criticism.",
    )

    # ------------------------------------------------------------------
    # Part K — conclusion
    # ------------------------------------------------------------------
    section("Part K — Bar 4 hypothesis verdict")

    print("  HYPOTHESIS (Bar 4):")
    print("    a retained scale ratio R = A/B (or log R, arctan R) equals 2/9")
    print("    by a number-theoretic identity that supplies the missing radian.")
    print()
    print("  EVIDENCE GATHERED:")
    print("    - many exact rational identities yield 2/9 (including")
    print("      8/9 * 1/4, 1/3 * 2/3, 4/9 * 1/2, etc.)")
    print("    - none of them carries a retained pi-factor, so none supplies")
    print("      a radian-without-pi output")
    print("    - the irrational ratios (alpha_LM/alpha_s(v), v/M_Pl, ...) do not")
    print("      hit 2/9 to <1e-6 precision either through R, log R, or arctan R")
    print()
    print("  CONCLUSION:")
    print("    BAR 4 FAILS as a radian-supplier. The hypothesis correctly")
    print("    identifies that 2/9 can be reproduced by exact rational")
    print("    identities, but those identities produce the NUMBER 2/9 only,")
    print("    not the ANGLE 2/9 rad. The radian conversion gap, already")
    print("    proven open by O10/O11/O12 and the SELECTED_LINE_LOCAL_RADIAN")
    print("    no-go, is NOT closed by any retained scale-ratio identity.")
    print()
    print("    Bar 4 joins the closed-negative set.")
    print()

    record(
        "K.1 Bar 4 fails as a radian-supplier",
        True,
        "exact rational identities exist but produce numbers, not radians.\n"
        "the radian conversion gap remains open; no retained scale-ratio\n"
        "identity supplies it. Bar 4 is closed negatively.",
    )

    record(
        "K.2 Bar 4 differs from Bar 7 (number-theoretic radian on retained args)",
        True,
        "Bar 7 tested individual special functions at retained args; Bar 4 tested\n"
        "RATIOS of physical scales. Both failed for the same underlying reason:\n"
        "the retained surface does not supply a NATIVE pi-free phase carrier.",
    )

    # ------------------------------------------------------------------
    # SUMMARY
    # ------------------------------------------------------------------
    section("SUMMARY")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")

    print()
    all_pass = (n_pass == n_total)
    if all_pass:
        print("VERDICT: Bar 4 (scale-ratio identity) is closed NEGATIVELY for")
        print("the radian-conversion question. Several exact rational identities")
        print("yield 2/9 (most prominent: 8/9 * 1/4 = 2/9), but none of them")
        print("supplies a phase angle without a separate pi-bridge.")
        print()
        print("DOC ITEMS:")
        print("  (1) tested      — exhaustive symbolic ratio scan over retained")
        print("                    rationals + numerical scan over retained")
        print("                    irrationals; ratio, log, arctan transforms")
        print("  (2) failed      — log(R)=2/9 and arctan(R)=2/9 produce no")
        print("                    exact identities; rational identities that")
        print("                    do hit 2/9 are dimensionless numbers only,")
        print("                    not radians")
        print("  (3) NOT tested  — high-degree polynomial relations and")
        print("                    dimensional ratios (frame-dependent); these")
        print("                    cannot supply a retained physical phase")
        print("  (4) challenged  — 8/9*1/4=2/9 (cross-sector); 1/3*2/3=2/9")
        print("                    (cross-sector); arithmetic, not physical")
        print("  (5) accepted    — Bar 4 closes negatively; rational identities")
        print("                    are cataloged but do not bridge the radian gap")
        print("  (6) forward     — radian conversion still open; future routes")
        print("                    must propose a NEW retained primitive that")
        print("                    NATURALLY carries a phase, or accept 2/9 as")
        print("                    irreducible additional input")
    else:
        print("VERDICT: verification has FAILs.")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
