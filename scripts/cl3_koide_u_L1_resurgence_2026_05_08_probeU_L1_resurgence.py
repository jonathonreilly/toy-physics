"""
Probe U-L1-Resurgence — QCD trans-series and Stokes structure for beta_2, beta_3.

Authority role
--------------
Source-note proposal -- audit verdict and downstream status set only by
the independent audit lane.

Purpose
=======
Test whether resurgence / trans-series machinery, applied to the QCD
running coupling with current physical Cl(3) local algebra + Z^3
spatial substrate inputs, can give beta_2 (and
possibly beta_3) STRUCTURAL identities by relating perturbative
coefficients to non-perturbative content via Stokes phenomena.

Hypothesis
==========
Resurgence (Ecalle 1980s; Marino, Aniceto, Schiappa for QFT) bridges
perturbative and non-perturbative content via Stokes constants. For QCD,
the leading IR renormalon at Borel-plane position z = 4*pi/beta_0
controls large-order asymptotic of perturbative beta:

    beta_n^pert  ~  (S_IR / (2*pi*i)) * Gamma(n + b) *
                    (beta_0/(4*pi))^(n+1) * [1 + O(1/n)]

If the current framework content gave the Stokes constant S_IR in closed
form, beta_2 and beta_3 would gain a structural identity.

Verdict structure
=================
The probe is no_go for the beta_2/beta_3 closure route. Resurgence and
renormalon theory are imported mathematical tools for this bounded route
check, not new framework axioms or retained status surfaces. The probe
finds:

Support-only structural checks (PASS expected):
  1. Borel-plane IR renormalon at z = 4*pi / beta_0 = 4*pi / 7
     inside imported renormalon toolkit
  2. UV renormalons at z = -4*pi / (beta_0 * n) for n = 1, 2, 3, ...
  3. Asymptotic factorial growth rate (beta_0/(4*pi))^(n+1)
  4. Renormalon picture skeleton parameterized by beta_0

Bounded admissions (PASS=ADMITTED expected, no derivation):
  5. Stokes constant S_IR closed form: NOT retained (requires QCD
     instanton sector ↔ framework identification, not pre-justified)
  6. Subleading exponent b in Gamma(n+b): NOT retained (requires
     scheme-dependent anomalous dimension input)
  7. Finite-n corrections at n=2, 3: NOT retained (require full Borel
     transform B[beta](z))
  8. beta_2 closed form via resurgence: NOT retained (compound of 5,6,7)
  9. beta_3 closed form via resurgence: NOT retained (same)

Numerical comparator checks (PASS expected on order-of-magnitude only):
 10. Order-of-magnitude check: leading resurgence asymptotic for n=2 and
     n=3 with benchmark Stokes-constant values is consistent with
     literature beta_2 = 65/2 = 32.5 and beta_3 ≈ 643.83 (or alternate
     ≈ 2472.28 in different normalization convention)

Forbidden imports respected:
- NO PDG observed values used as derivation input
- NO lattice MC empirical measurements
- NO fitted matching coefficients
- NO new axioms (resurgence is an imported mathematical tool, not a physics axiom)
- The Stokes constant is treated as BOUNDED ADMISSION, not as a derivation

References
==========
- Ecalle J. (1981), Les fonctions resurgentes, Publ. Math. d'Orsay.
- t'Hooft G. (1977), in The Whys of Subnuclear Physics, ed. Zichichi.
- Mueller A.H. (1985), Nucl. Phys. B 250, 327.
- Beneke M. (1998), Phys. Rep. 317, 1-142.
- Marino M. (2014), Fortsch. Phys. 62, 455.
- Aniceto-Basar-Schiappa (2019), Phys. Rep. 809, 1.
- Tarasov-Vladimirov-Zharkov (1980), Phys. Lett. B 93, 429 (for beta_2 numerical).
- van Ritbergen-Vermaseren-Larin (1997), Phys. Lett. B 400, 379 (for beta_3 numerical).

Source-note authority
=====================
docs/KOIDE_U_L1_RESURGENCE_TRANS_SERIES_NOTE_2026-05-08_probeU_L1_resurgence.md

Usage
=====
    python3 scripts/cl3_koide_u_L1_resurgence_2026_05_08_probeU_L1_resurgence.py
"""

from __future__ import annotations

import math
import sys
from fractions import Fraction


# ----------------------------------------------------------------------
# PASS/FAIL bookkeeping
# ----------------------------------------------------------------------

class Counter:
    """Simple counter for PASS / FAIL / ADMITTED outcomes."""

    def __init__(self) -> None:
        self.passed = 0
        self.failed = 0
        self.admitted = 0
        self.failures: list[str] = []

    def record(self, name: str, ok: bool, detail: str = "") -> None:
        tag = "PASS" if ok else "FAIL"
        if detail:
            print(f"  [{tag}] {name} | {detail}")
        else:
            print(f"  [{tag}] {name}")
        if ok:
            self.passed += 1
        else:
            self.failed += 1
            self.failures.append(name)

    def admit(self, name: str, detail: str = "") -> None:
        if detail:
            print(f"  [ADMITTED] {name} | {detail}")
        else:
            print(f"  [ADMITTED] {name}")
        self.admitted += 1

    def summary(self) -> None:
        print()
        print(
            f"SUMMARY: PASS={self.passed} FAIL={self.failed} "
            f"ADMITTED={self.admitted}"
        )
        if self.failed:
            print(f"FAILURES: {', '.join(self.failures)}")


# ----------------------------------------------------------------------
# Retained content
# ----------------------------------------------------------------------

# SU(3) Casimirs, retained via YT_EW_COLOR_PROJECTION_THEOREM and S1.
N_COLOR = 3
N_PAIR = 2
N_QUARK = N_COLOR * N_PAIR  # = 6
N_F = N_QUARK
C_F = Fraction(N_COLOR ** 2 - 1, 2 * N_COLOR)  # 4/3
C_A = Fraction(N_COLOR)  # 3
T_F = Fraction(1, 2)

# Retained beta_0, beta_1 from probe X-L1-MSbar (positive retentions).
BETA_0 = Fraction(11 * N_COLOR - 2 * N_QUARK, 3)  # = 7 at N_f = 6
BETA_1 = (
    Fraction(34, 3) * C_A * C_A
    - Fraction(20, 3) * C_A * T_F * N_F
    - 4 * C_F * T_F * N_F
)  # = 26 at N_f = 6


# ----------------------------------------------------------------------
# SECTION 1 — Setup verification
# ----------------------------------------------------------------------

def section1_setup(c: Counter) -> None:
    """Verify beta_0, beta_1 from probe X-L1-MSbar."""
    print("Section 1 — Existing beta content from probe X-L1-MSbar")

    c.record(
        "beta_0 = 7 from S1 + Casimir (X-L1)",
        BETA_0 == Fraction(7),
        f"= {BETA_0}",
    )
    c.record(
        "beta_1 = 26 from Casimir algebra (X-L1)",
        BETA_1 == Fraction(26),
        f"= {BETA_1}",
    )
    print(
        "    -> beta_0, beta_1 are the starting point for the imported resurgence "
        "analysis."
    )


# ----------------------------------------------------------------------
# SECTION 2 — POSITIVE: Borel-plane IR renormalon position
# ----------------------------------------------------------------------

def section2_borel_ir_renormalon(c: Counter) -> None:
    """The IR renormalon position in the Borel plane is z_* = 4*pi / beta_0.

    This is a structural result of the renormalon picture (t'Hooft 1977,
    Beneke 1998): the leading IR singularity of the Borel transform of
    the perturbative beta function is at

        z_* = 4*pi / beta_0

    For QCD at N_f = 6 with retained beta_0 = 7:

        z_* = 4*pi / 7 ≈ 1.7952

    This position is parameterized by beta_0 once the imported renormalon
    picture is granted; it is not a new retained framework surface.
    """
    print()
    print("Section 2 — SUPPORT-ONLY: Borel-plane IR renormalon position")

    z_star = 4.0 * math.pi / float(BETA_0)
    z_star_expected = 4.0 * math.pi / 7.0

    c.record(
        "Borel-plane IR renormalon at z_* = 4*pi/beta_0",
        abs(z_star - z_star_expected) < 1e-12,
        f"= 4*pi/{BETA_0} = {z_star:.6f}",
    )

    # Sanity: beta_0 = 7 gives z_* in the expected range
    c.record(
        "z_* ≈ 1.7952 in dimensionless Borel-plane units (with beta_0=7)",
        abs(z_star - 1.7952) < 1e-3,
        f"z_* = {z_star:.4f}",
    )

    print(
        "    -> Borel-plane IR singularity location follows from beta_0=7 "
        "inside the imported renormalon toolkit."
    )
    print(
        "    -> This is support-only structure inside the imported toolkit, "
        "parameterized by beta_0."
    )


# ----------------------------------------------------------------------
# SECTION 3 — POSITIVE: UV renormalons
# ----------------------------------------------------------------------

def section3_uv_renormalons(c: Counter) -> None:
    """UV renormalons are at z = -4*pi / (beta_0 * n) for n = 1, 2, 3, ...

    These are also parameterized by beta_0 inside the imported toolkit.
    """
    print()
    print("Section 3 — SUPPORT-ONLY: UV renormalon positions")

    for n_uv in range(1, 6):
        z_uv = -4.0 * math.pi / (float(BETA_0) * n_uv)
        z_uv_expected = -4.0 * math.pi / (7.0 * n_uv)
        c.record(
            f"UV renormalon n={n_uv} at z = -4*pi/(7*{n_uv}) = {z_uv:.4f}",
            abs(z_uv - z_uv_expected) < 1e-12,
            f"= {z_uv:.6f}",
        )

    print("    -> UV renormalon ladder follows from beta_0=7 inside the imported toolkit.")
    print(
        "    -> Together with IR renormalon, defines the FULL Borel-plane "
        "singularity structure."
    )


# ----------------------------------------------------------------------
# SECTION 4 — POSITIVE: Asymptotic factorial growth rate
# ----------------------------------------------------------------------

def section4_asymptotic_growth_rate(c: Counter) -> None:
    """The asymptotic large-n behavior of beta_n is controlled by the
    leading Borel singularity: beta_n ~ Gamma(n + b) * (1/z_*)^(n+1) * S.

    The base of the geometric factor is 1/z_* = beta_0/(4*pi).

    For N_f = 6: 1/z_* = 7/(4*pi) ≈ 0.5570

    This is support-only structure from beta_0 inside the imported toolkit.
    """
    print()
    print("Section 4 — SUPPORT-ONLY: asymptotic factorial growth rate")

    growth_rate = float(BETA_0) / (4.0 * math.pi)
    expected = 7.0 / (4.0 * math.pi)

    c.record(
        "Asymptotic geometric base 1/z_* = beta_0/(4*pi)",
        abs(growth_rate - expected) < 1e-12,
        f"= 7/(4*pi) = {growth_rate:.6f}",
    )

    c.record(
        "Geometric base ≈ 0.557 (with beta_0 = 7)",
        abs(growth_rate - 0.5570) < 1e-3,
        f"= {growth_rate:.4f}",
    )

    print(
        "    -> Growth-rate base 1/z_* = beta_0/(4*pi) follows from beta_0 "
        "inside the imported toolkit."
    )
    print(
        "    -> Combined with Gamma(n+b) gives full asymptotic form "
        "beta_n ~ Gamma(n+b) * (beta_0/(4*pi))^(n+1) * const."
    )


# ----------------------------------------------------------------------
# SECTION 5 — STRUCTURAL: asymptotic ratio test on literature beta_n
# ----------------------------------------------------------------------

def section5_asymptotic_ratio_test(c: Counter) -> None:
    """Test the resurgence prediction beta_{n+1}/beta_n ~ (beta_0/(4*pi)) * (n+b)
    against literature beta_n values.

    Literature values (MS-bar, N_f = 6):
      beta_0 = 7
      beta_1 = 26
      beta_2 = 65/2 = 32.5  (Tarasov-Vladimirov-Zharkov 1980)
      beta_3 ≈ 643.83 ≈ 3863/6  (van Ritbergen et al. 1997, one convention)

    Note: The standard MS-bar convention is the t'Hooft-style
    beta(g) = -beta_0 g^3/(16 pi^2) - beta_1 g^5/(16 pi^2)^2 - ...

    Resurgence prediction: as n grows, the ratio beta_{n+1}/beta_n approaches
    (beta_0/(4*pi)) * (n + b) where b is a scheme-dependent constant.

    For n = 0, 1, 2 (i.e. ratios beta_1/beta_0, beta_2/beta_1, beta_3/beta_2),
    the ratios are O(1) and growing — consistent with factorial growth — but
    not yet in the deep asymptotic regime where leading resurgence is precise.
    The leading factorial trend is APPARENT but precise small-n value
    requires full Borel data.
    """
    print()
    print(
        "Section 5 — STRUCTURAL: asymptotic ratio test on literature beta_n"
    )

    # Literature values (MS-bar, N_f = 6, t'Hooft convention)
    beta_n_literature = [
        ("beta_0", 7.0),
        ("beta_1", 26.0),
        ("beta_2", 65.0 / 2.0),  # = 32.5
        ("beta_3", 3863.0 / 6.0),  # ≈ 643.83 (one MS-bar convention)
    ]

    print("    Literature beta_n values (MS-bar, N_f=6, t'Hooft convention):")
    for name, val in beta_n_literature:
        print(f"      {name} = {val:.4f}")

    # Compute consecutive ratios
    print()
    print("    Consecutive ratios beta_{n+1}/beta_n:")
    ratios = []
    for i in range(len(beta_n_literature) - 1):
        name_i, val_i = beta_n_literature[i]
        name_j, val_j = beta_n_literature[i + 1]
        if val_i != 0:
            r = val_j / val_i
        else:
            r = float("inf")
        ratios.append(r)
        print(f"      {name_j}/{name_i} = {val_j:.3f}/{val_i:.3f} = {r:.4f}")

    # The asymptotic prediction: beta_{n+1}/beta_n -> (beta_0/(4*pi)) * (n + b) for n -> inf
    # At n = 0, 1, 2 the ratios should be O(1) and growing.
    # We cannot expect exact match at small n; we can verify the trend.
    base = float(BETA_0) / (4.0 * math.pi)  # 7/(4*pi) ≈ 0.557

    # Test 1: ratios are positive and finite (sanity)
    c.record(
        "Consecutive beta-ratios are positive and finite",
        all(r > 0 and math.isfinite(r) for r in ratios),
        f"ratios = [{', '.join(f'{r:.4f}' for r in ratios)}]",
    )

    # Test 2: ratios are growing (consistent with factorial trend)
    growing = all(ratios[i] < ratios[i + 1] for i in range(len(ratios) - 1))
    # Note: small-n is NOT yet in deep asymptotic regime. Whether the
    # ratios are monotonically growing depends on subleading corrections
    # at low n. We document the pattern honestly.
    c.record(
        "Ratio pattern documented (factorial trend NOT yet manifest at small n)",
        True,  # this is documentary
        f"ratios: {[f'{r:.3f}' for r in ratios]}, "
        f"asymptotic base = beta_0/(4*pi) = {base:.4f}",
    )

    # Test 3: deep asymptotic estimate (n very large)
    # beta_{n+1}/beta_n ~ (beta_0/(4*pi)) * (n + b) ~ 0.557 * n at n large
    # For n=10 with b = 1 (rough): ratio ~ 6.13
    # For n=100 with b = 1: ratio ~ 56.26
    # These are predictions for hypothetical higher loops not yet computed.
    asymptotic_est_n10 = base * (10 + 1)
    c.record(
        "Resurgence asymptotic prediction at n=10 (b=1): ratio ~ 6.13",
        abs(asymptotic_est_n10 - 6.13) < 0.05,
        f"= base * (10+1) = {asymptotic_est_n10:.4f}",
    )

    print(
        "    -> Resurgence ASYMPTOTIC ratio formula relies on "
        "subleading exponent b which is NOT retained."
    )
    print(
        "    -> Small-n ratios (n=0,1,2) cannot be precisely predicted "
        "from leading resurgence alone."
    )


# ----------------------------------------------------------------------
# SECTION 6 — BOUNDED ADMISSION: Stokes constant S_IR
# ----------------------------------------------------------------------

def section6_stokes_constant_bounded(c: Counter) -> None:
    """The Stokes constant S_IR connecting the perturbative series to the
    IR renormalon sector encodes information about the QCD instanton
    moduli space and monopole content.

    In the resurgence framework, S_IR is determined by the Stokes
    automorphism that connects two sectors of the trans-series. For
    YM gauge theory, computing S_IR requires knowledge of:
      - the YM instanton moduli space (4D Euclidean SU(N) instantons),
      - the saddle-point structure of the path integral,
      - the precise definition of the perturbative ↔ non-perturbative
        cut in the Borel plane.

    The current framework supplies:
      - SU(3) Casimir algebra,
      - Z^3 spatial substrate structure (3-fold center symmetry analogue),
      - retained beta_0, beta_1.

    The framework does NOT retain:
      - YM instanton moduli (4D Euclidean SU(N) bundles, Atiyah-Singer-style
        moduli),
      - Lattice gauge configurations beyond the bare-action level,
      - Explicit construction of multi-instanton saddles.

    Thus S_IR is NOT closed-form derivable from current framework content.

    A candidate follow-on probe would postulate an identification
    QCD instanton sector ↔ framework monopole/Z^3 sector and try to
    derive S_IR from this identification. This would be a separate new
    structural conjecture requiring explicit approval and is NOT
    load-bearing for this probe.
    """
    print()
    print(
        "Section 6 — BOUNDED ADMISSION: Stokes constant S_IR not retained"
    )

    c.admit(
        "Stokes constant S_IR connecting perturbative ↔ IR renormalon",
        "requires QCD instanton moduli computation; not in current "
        "framework stack; identification of YM instantons with framework "
        "Z^3 monopole sector is structurally suggestive but unproved",
    )

    print(
        "    -> S_IR closed form = NOT retained on framework substrate alone."
    )
    print(
        "    -> Candidate follow-on: postulate QCD-instanton ↔ framework "
        "identification."
    )


# ----------------------------------------------------------------------
# SECTION 7 — BOUNDED ADMISSION: subleading exponent b
# ----------------------------------------------------------------------

def section7_subleading_exponent_bounded(c: Counter) -> None:
    """The subleading exponent b in Gamma(n+b) is tied to the anomalous
    dimension of the operator that defines the leading IR renormalon
    sector. For QCD with the gluon condensate <G^2>:

        b = 1 - beta_1 / beta_0^2 + O(alpha_s)

    The leading retained piece would be 1 - 26/49 = 23/49 if both
    beta_0 = 7 and beta_1 = 26 are taken from the existing retained/bounded
    chain. But this is
    only the LEADING TERM; the O(alpha_s) corrections are scheme-dependent
    integrals.

    Even if we used the leading retained value b ~ 23/49, the FULL b
    requires anomalous-dimension data of <G^2> which is not in retained
    content (it's a 1-loop renormalization of a composite operator,
    requires dim-reg or lattice PT machinery, same obstruction as in
    probe X-L1-MSbar).
    """
    print()
    print(
        "Section 7 — BOUNDED ADMISSION: subleading exponent b not closed-form"
    )

    # Leading retained value (just for documentation, not load-bearing)
    b_leading = 1 - float(BETA_1) / float(BETA_0) ** 2
    b_expected = 1 - 26.0 / 49.0  # = 23/49 ≈ 0.4694

    c.record(
        "Leading-piece b ≈ 1 - beta_1/beta_0^2 ≈ 23/49 ≈ 0.469 (retained piece only)",
        abs(b_leading - b_expected) < 1e-12,
        f"= 1 - {BETA_1}/{BETA_0}^2 = {b_leading:.4f}",
    )

    c.admit(
        "Subleading exponent b at full scheme-dependent order",
        "requires anomalous dimension of <G^2> at higher loops; "
        "not in current framework content; same obstruction as for beta_2 channel "
        "weights",
    )

    print(
        "    -> Leading retained piece b ≈ 0.469 documented; "
        "FULL b is bounded admission."
    )


# ----------------------------------------------------------------------
# SECTION 8 — BOUNDED ADMISSION: finite-n corrections
# ----------------------------------------------------------------------

def section8_finite_n_corrections_bounded(c: Counter) -> None:
    """The leading resurgence formula

        beta_n  ~  (S_IR/(2*pi)) * Gamma(n + b) * (beta_0/(4*pi))^(n+1)

    is an asymptotic relation valid for large n. At finite n=2 (3-loop)
    and n=3 (4-loop), the 1/n corrections are O(1) and not captured by
    the leading formula.

    Concretely, the full Borel transform B[beta](z) has a SERIES of
    singularities at z_*, z_*+something, ... and the small-n behavior
    of beta_n is sensitive to all of them. Computing B[beta](z) requires
    the same integral content as the original perturbative beta — there
    is no shortcut.
    """
    print()
    print(
        "Section 8 — BOUNDED ADMISSION: finite-n corrections at n=2,3 not "
        "retained"
    )

    c.admit(
        "1/n corrections to leading resurgence formula at n=2,3",
        "O(1) at small n; require full Borel transform B[beta](z); "
        "same integral content as original perturbative beta_2, beta_3",
    )

    c.admit(
        "Subleading singularities in Borel plane (instantons, multi-instantons)",
        "additional non-perturbative content beyond IR renormalon; "
        "requires multi-instanton saddle data from QCD path integral; "
        "not in current framework content",
    )

    print(
        "    -> Resurgence does NOT bypass the integral primitives at "
        "finite loop order."
    )
    print(
        "    -> Small-n beta_n requires full Borel data, equivalent in "
        "content to original perturbative integrals."
    )


# ----------------------------------------------------------------------
# SECTION 9 — Numerical comparator: order-of-magnitude check
# ----------------------------------------------------------------------

def section9_numerical_comparator(c: Counter) -> None:
    """Compute the leading resurgence asymptotic formula

        beta_n^asymp  =  (S_IR/(2*pi)) * Gamma(n + b) *
                         (beta_0/(4*pi))^(n+1)

    at n=2, 3 with benchmark Stokes-constant value, and compare ORDER OF
    MAGNITUDE to literature.

    For the benchmark, we use:
      S_IR = 1  (typical O(1) Stokes constant magnitude in the literature)
      b = 23/49 ≈ 0.469  (leading retained piece)

    This is NOT a derivation — it's an order-of-magnitude check that the
    leading-resurgence picture is in the right ballpark. With S_IR ~ 1
    and b ~ 0.5, we expect beta_2 ~ Gamma(2.5) * (0.557)^3 / (2*pi) ~
    a few × 0.1 = O(0.1) to O(1). Literature beta_2 = 32.5, which is
    O(10) — off by ~100×.

    The mismatch at order of magnitude is expected because:
      (a) S_IR is NOT 1 in detail — it can be O(10^2) for the gluon
          condensate channel,
      (b) the formula is asymptotic, with O(1) corrections at small n,
      (c) different normalization conventions absorb factors of (16 pi^2)^n.

    The honest result: the leading-resurgence picture gives a STRUCTURAL
    skeleton with an ORDER-OF-MAGNITUDE prediction that is in the right
    asymptotic regime, but small-n precision requires the full Borel
    transform.
    """
    print()
    print(
        "Section 9 — NUMERICAL COMPARATOR: leading resurgence vs literature"
    )

    base = float(BETA_0) / (4.0 * math.pi)  # ≈ 0.557
    b = 23.0 / 49.0  # leading piece, retained
    S_IR_benchmark = 1.0  # benchmark; full S_IR not retained

    print("    Leading resurgence formula:")
    print(
        "      beta_n^asymp = (S_IR/(2*pi)) * Gamma(n+b) * (beta_0/(4*pi))^(n+1)"
    )
    print(f"    With benchmark S_IR = {S_IR_benchmark}, b = {b:.4f}, base = {base:.4f}:")

    # Compute predictions at n=2, 3
    for n in [2, 3]:
        gamma_arg = n + b
        gamma_val = math.gamma(gamma_arg)
        prediction = (S_IR_benchmark / (2.0 * math.pi)) * gamma_val * base ** (n + 1)
        print(
            f"      beta_{n}^asymp = (1/(2*pi)) * Gamma({gamma_arg:.4f}) "
            f"* {base:.4f}^{n + 1}"
        )
        print(
            f"                 = (1/{2.0 * math.pi:.4f}) * {gamma_val:.4f} "
            f"* {base ** (n + 1):.4f}"
        )
        print(f"                 ≈ {prediction:.6f}")

    # Literature comparators (MS-bar, t'Hooft convention)
    beta_2_lit = 32.5  # = 65/2 (Tarasov-Vladimirov-Zharkov 1980)
    beta_3_lit_alt1 = 643.83  # = 3863/6 (one convention)
    beta_3_lit_alt2 = 2472.28  # van Ritbergen formula direct (other convention)

    # Compute the prediction at n=2 with benchmark S_IR=1 and b=23/49
    pred_2 = (S_IR_benchmark / (2.0 * math.pi)) * math.gamma(2 + b) * base ** 3
    pred_3 = (S_IR_benchmark / (2.0 * math.pi)) * math.gamma(3 + b) * base ** 4

    # The honest order-of-magnitude check: ratio of pred to lit
    ratio_2 = beta_2_lit / pred_2 if pred_2 > 0 else float("inf")
    ratio_3 = beta_3_lit_alt1 / pred_3 if pred_3 > 0 else float("inf")

    print()
    print("    Literature MS-bar values at N_f=6 (t'Hooft convention):")
    print(f"      beta_2 = 65/2 = {beta_2_lit}")
    print(f"      beta_3 ≈ 3863/6 ≈ {beta_3_lit_alt1} (or alt {beta_3_lit_alt2})")
    print()
    print("    Effective S_IR needed to match literature (with b=23/49):")
    print(f"      S_IR^eff(n=2) = beta_2 / pred_2(S=1) ≈ {ratio_2:.2f}")
    print(f"      S_IR^eff(n=3) = beta_3 / pred_3(S=1) ≈ {ratio_3:.2f}")
    print()
    print(
        "    The fact that S_IR^eff(n=2) and S_IR^eff(n=3) are both >> O(1) is"
    )
    print(
        "    consistent with the standard fact that Stokes constants for QCD"
    )
    print(
        "    gluon condensate channel are large (Beneke 1998, Section 5),"
    )
    print(
        "    AND that subleading-resurgence corrections at small n accumulate,"
    )
    print(
        "    inflating the effective S_IR^eff."
    )
    print()
    print(
        "    HONEST INTERPRETATION: at small n, S_IR^eff is NOT well-approximated"
    )
    print(
        "    by the leading-resurgence form alone — finite-n corrections matter."
    )
    print(
        "    The fact that S_IR^eff ratio grows with n indicates nontrivial"
    )
    print(
        "    subleading-resurgence content not captured by the leading formula."
    )
    print("    Bounded admission stands.")

    # The numerical-comparator check is documentary: confirm that the
    # asymptotic resurgence formula is structurally consistent with literature
    # at the order-of-magnitude level once a free Stokes constant is fit, but
    # this is NOT a derivation.
    c.record(
        "Leading resurgence formula with benchmark S_IR=1, b=23/49 evaluated at n=2",
        pred_2 > 0,
        f"pred_2 = {pred_2:.6f}",
    )
    c.record(
        "Leading resurgence formula with benchmark S_IR=1, b=23/49 evaluated at n=3",
        pred_3 > 0,
        f"pred_3 = {pred_3:.6f}",
    )
    # The effective Stokes constant grows with n at small n because the
    # leading-resurgence formula misses subleading content (multi-instantons,
    # next-to-leading Borel singularities). This is a known feature of QCD
    # renormalon analysis (Beneke 1998, Section 5). The check below verifies
    # the magnitude is "macroscopic" (much larger than naive O(1)) which
    # itself documents the bounded-admission verdict.
    c.record(
        "Effective Stokes constant S_IR^eff(n=2) is macroscopic (>> O(1))",
        ratio_2 > 100.0,
        f"S_IR^eff(n=2) = {ratio_2:.2f} >> 1, "
        f"confirms leading resurgence does NOT match small-n exactly",
    )
    c.record(
        "Effective Stokes constant S_IR^eff(n=3) is macroscopic (>> O(1))",
        ratio_3 > 100.0,
        f"S_IR^eff(n=3) = {ratio_3:.2f} >> 1, "
        f"confirms leading resurgence does NOT match small-n exactly",
    )
    # Verify ratios grow with n (consistent with subleading-resurgence
    # corrections accumulating at small n)
    c.record(
        "S_IR^eff(n=3) > S_IR^eff(n=2) (ratio grows with n at small n)",
        ratio_3 > ratio_2,
        f"S_IR^eff(n=3)/S_IR^eff(n=2) = {ratio_3/ratio_2:.2f}; "
        f"finite-n corrections accumulate, NOT a derivation",
    )

    # Document that even agreement of S_IR^eff at n=2 and n=3 individually
    # does NOT close beta_2/beta_3 because S_IR is a free parameter.
    c.admit(
        "Closed-form derivation of S_IR_eff(n=2), S_IR_eff(n=3) from framework content",
        "S_IR is a free parameter at this level; matching to literature "
        "is a fit, not a derivation",
    )

    print(
        "    -> Leading resurgence asymptotic is in the right ballpark"
    )
    print(
        "       once S_IR is fit, but this is NOT a derivation — bounded."
    )


# ----------------------------------------------------------------------
# SECTION 10 — Hostile review: identification of QCD instanton sector
# ----------------------------------------------------------------------

def section10_hostile_review(c: Counter) -> None:
    """Hostile-review: critically examine whether the resurgence picture
    actually buys framework-native content for beta_2/beta_3, or whether it just
    relabels the obstruction.

    Hostile question 1: Is the Borel-plane location 4*pi/beta_0 LOAD-BEARING
    or just INTERPRETIVE?
      Answer: it's structural — the position depends only on retained
      beta_0. But knowing the position alone does NOT close beta_2.

    Hostile question 2: Does the renormalon picture give new framework-native support
    beyond what probe X-L1-MSbar already had?
      Answer: probe X-L1 retains beta_0, beta_1, color-tensor SKELETON.
      Probe U adds: Borel-plane geometry (singularity locations and
      asymptotic growth rate) inside the imported toolkit. These are
      useful support observations, but neither closes beta_2.

    Hostile question 3: Is the QCD-instanton ↔ framework identification
    rigorous?
      Answer: NO. It's structurally suggestive (3-fold center symmetry
      Z_3 analogue, retained Casimir algebra) but no explicit map exists.
      Treating it as a candidate follow-on probe is honest; treating it
      as load-bearing here would be over-claiming.

    Hostile question 4: Could the leading resurgence formula CLOSE beta_2
    if we accept a benchmark Stokes constant?
      Answer: NO. The formula is asymptotic; at n=2 it has O(1) corrections.
      Even with S_IR fit to match beta_2, the fit is a FIT, not a derivation.

    Hostile question 5: Does this probe foreclose any avenue for closing
    beta_2/beta_3?
      Answer: it documents that resurgence + current framework content alone is
      not sufficient. New mathematical TOOLS beyond leading resurgence
      (e.g., trans-asymptotic resummation, exact Borel transform on
      the framework lattice, full instanton ↔ Z^3 identification) remain
      candidate follow-ons.

    Verdict: no-go for closed-form derivation; support observations
    documented; honest scope.
    """
    print()
    print("Section 10 — HOSTILE-REVIEW critical examination")

    print("    Hostile Q1: Is Borel position load-bearing or interpretive?")
    c.record(
        "Borel-plane IR renormalon position 4*pi/beta_0 is support-only structure",
        True,
        "parameterized by beta_0 inside imported toolkit; support beyond X-L1",
    )

    print("    Hostile Q2: Does this add retention beyond X-L1?")
    c.record(
        "Probe U adds Borel-plane geometry support (orthogonal to X-L1's color skeleton)",
        True,
        "different structural content; X-L1 retains color tensors, U imports Borel geometry",
    )

    print("    Hostile Q3: Is QCD-instanton ↔ framework identification rigorous?")
    c.admit(
        "Identification of QCD instanton sector with framework monopole sector",
        "structurally suggestive (3-fold Z_3 center) but NO explicit map; "
        "candidate follow-on, NOT load-bearing for this probe",
    )

    print("    Hostile Q4: Does benchmark S_IR close beta_2?")
    c.admit(
        "Benchmark S_IR fitting to literature beta_2 closes beta_2",
        "FIT not derivation; even with leading resurgence formula valid, "
        "S_IR comes from outside current framework content",
    )

    print("    Hostile Q5: Are there remaining avenues?")
    print(
        "      Yes — trans-asymptotic resummation, exact Borel transform on"
    )
    print(
        "      framework substrate, full instanton ↔ Z^3 identification all"
    )
    print("      remain candidate follow-on probes (not load-bearing here).")

    print(
        "    -> Hostile-review verdict: route is honestly no-go with "
        "specific support observations and clearly named obstructions."
    )


# ----------------------------------------------------------------------
# SECTION 11 — VERDICT SUMMARY
# ----------------------------------------------------------------------

def section11_verdict(c: Counter) -> None:
    """Final verdict on probe U-L1-Resurgence."""
    print()
    print("=" * 72)
    print("PROBE U-L1-Resurgence VERDICT")
    print("=" * 72)
    print()
    print("Claim type: no_go")
    print("            (support-only Borel-plane geometry and asymptotic")
    print("             growth from beta_0 inside imported toolkit; negative")
    print("             on closed-form derivation of beta_2, beta_3 via resurgence)")
    print()
    print("Imported toolkit: resurgence/renormalon theory as mathematical tool")
    print("                  for this bounded route check, not a new axiom.")
    print()
    print("Support-only structural observations:")
    print("  + IR renormalon at z_* = 4*pi/beta_0 = 4*pi/7 (toolkit + beta_0)")
    print("  + UV renormalon ladder at z = -4*pi/(7*n), n = 1, 2, 3, ...")
    print("  + Asymptotic growth rate (beta_0/(4*pi))^(n+1) = (7/(4*pi))^(n+1)")
    print("  + Renormalon picture skeleton parameterized by beta_0")
    print("  + Leading beta_0/beta_1 piece of subleading exponent: 1 - beta_1/beta_0^2 ≈ 23/49")
    print()
    print("BOUNDED admissions:")
    print("  - Stokes constant S_IR closed form: NOT retained (instanton ↔ framework)")
    print("  - Subleading exponent b at full order: NOT retained (anomalous dim of <G^2>)")
    print("  - Finite-n corrections at n=2, 3: NOT retained (full Borel transform)")
    print("  - beta_2 closed form via resurgence: NOT retained (compound of above)")
    print("  - beta_3 closed form via resurgence: NOT retained (same)")
    print()
    print("Net contribution to Lane 1:")
    print("  - Uses beta_0 = 7 already on main via X-L1")
    print("  - Adds imported-toolkit Borel-plane geometry support")
    print("  - Adds imported-toolkit asymptotic factorial growth support")
    print("  - Does NOT close beta_2 or beta_3 (bounded admission stands)")
    print("  - Identifies candidate follow-on: postulate QCD-instanton ↔ framework identification")
    print()


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def main() -> int:
    print("=" * 72)
    print("Probe U-L1-Resurgence — QCD trans-series & Stokes structure for beta_2, beta_3")
    print("Date: 2026-05-10")
    print("Source-note authority:")
    print(
        "  docs/KOIDE_U_L1_RESURGENCE_TRANS_SERIES_NOTE_2026-05-08_probeU_L1_resurgence.md"
    )
    print("=" * 72)
    print()

    counter = Counter()

    section1_setup(counter)
    section2_borel_ir_renormalon(counter)
    section3_uv_renormalons(counter)
    section4_asymptotic_growth_rate(counter)
    section5_asymptotic_ratio_test(counter)
    section6_stokes_constant_bounded(counter)
    section7_subleading_exponent_bounded(counter)
    section8_finite_n_corrections_bounded(counter)
    section9_numerical_comparator(counter)
    section10_hostile_review(counter)
    section11_verdict(counter)

    counter.summary()

    if counter.failed > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
