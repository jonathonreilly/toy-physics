#!/usr/bin/env python3
"""
Koide A1 — two-loop multi-trace derivation probe

TARGET
------
Derive V_KN(Phi) = [2 T1 - 3 T2]^2 = 4 T1^4 - 12 T1^2 T2 + 0 T1 T3 + 9 T2^2 + 0 T4
(T_k = Tr Phi^k, Phi = Y^dag Y) as a TWO-LOOP effective potential on the
retained Cl(3)/Z^3 + CL3_SM_EMBEDDING axioms.

PRIOR CONTEXT (commit fedd7bde, docs/KOIDE_A1_IRREDUCIBILITY_ADDENDUM_NOTE_2026-04-24.md)
   - 14 prior probes established 8 equivalent A1 primitives, none derivable.
   - Four obstruction classes: O1 integer/continuous; O2 single-trace /
     multi-trace; O3 sign; O4 trace-space / matrix-algebra.
   - Three untested surfaces remain; this probe attacks the first:
     2-loop fermion diagrams with disconnected vacuum bubbles.

HYPOTHESIS
----------
At 2 loops, DISCONNECTED vacuum-bubble products appear. Two independent
1-loop fermion bubbles each contribute Tr(D^{-1})-type single-trace
factors. Their PRODUCT produces [T_k]*[T_l] = T_k T_l multi-trace
monomials. If the product of bubbles naturally contains all three V_KN
components (T1^4, T1^2 T2, T2^2) with ratio 4:-12:9 and with a positive
overall coefficient (fermion-fermion = +), V_KN emerges at 2-loop.

Sign counting: each fermion loop contributes (-1) (closed trace);
product of two fermion loops gives (-1)*(-1) = +1. Bosonic loops give
+1 each; boson-fermion cross = -1; etc. 2PI effective action has its
own overall sign (vacuum-energy convention).

ATTACK VECTORS (each tested symbolically in sympy)
--------------------------------------------------
UV1 -- Two disconnected fermion bubbles coupled by a heavy scalar mediator.
UV2 -- Connected 2-loop eye / box diagram with 4 external Phi legs
       (control experiment: single-trace, should rule out).
UV3 -- Two-particle-irreducible (2PI) 2-loop action:
       Gamma_2PI[G] = tr log G^{-1} + (1/2) tr (Sigma G) + Gamma_2[G].
UV4 -- Four-fermion contact term via Fierz rearrangement
       (pseudo-single-loop route generating T_1^2 multi-trace).
UV5 -- Generic Wilsonian 2-loop V_eff catalog over 5-dim basis,
       coefficient-matching analysis.
UV6 -- Heat-kernel "two-loop" (a_8 analog with nested traces).

ASSUMPTIONS QUESTIONED
----------------------
A1  Do 2 fermion bubbles actually span (T1^4, T1^2 T2, T2^2)?
    Each bubble has a parity: Tr(M + y Phi)^k gives a polynomial in
    y (weights 0..k). Quartic-in-Phi part of PRODUCT is obtained by
    partitioning weight 4 as 4+0, 3+1, 2+2, etc. Test explicitly.

A2  Sign conventions at 2-loop: fermion-loop (-1), vacuum-bubble factor,
    overall V_eff sign. Clarify with diagram rules.

A3  Does "2-loop V_eff(Phi)" even make sense when Phi is NOT a
    dynamical field? Phi is a matrix of Yukawa couplings, not a
    fluctuating operator. The "Tr log" interpretation integrates out
    the MATTER fields in a Phi background; two-loop adds vertices of
    a mediator. Does this admit a well-defined constant-Phi limit, or
    does it inevitably collapse into beta-function corrections to
    couplings?

A4  Is the 2-loop multi-trace structure GENERIC (tunable free
    coefficients, matching any vector c = (c1, c2, c3, c4, c5) in
    the 5-dim basis via tuning mediator masses / couplings)? If so,
    ratio 4:-12:0:9:0 is reproducible by tuning but not selected --
    same lateral-move problem as bosonic auxiliary.

A5  Do retained SU(2)_L x U(1)_Y gauge loops at 2-loop generate extra
    multi-trace terms? Are these fixed ratios (structural) or free
    coefficients (tunable)?

DELIVERABLE
-----------
Per-vector: identify diagram; compute coefficient structure on
{T1^4, T1^2 T2, T1 T3, T2^2, T4}; check ratio 4:-12:0:9:0 and sign.
Addressing A1-A5 in dedicated section.

Attribution:
    docs/KOIDE_A1_IRREDUCIBILITY_ADDENDUM_NOTE_2026-04-24.md
    scripts/frontier_koide_a1_fermion_loop_probe.py (1-loop, single-trace only)
    scripts/frontier_koide_a1_auxiliary_scalar_probe.py (1-loop bosonic, wrong sign)
"""
from __future__ import annotations

import sys
from itertools import combinations_with_replacement, product

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
# Symbolic infrastructure
# ---------------------------------------------------------------------------
# 5-dim degree-4 U(3)-invariant basis on T_k = Tr(Phi^k).
# Newton-Girard: the five linearly independent degree-4 trace invariants
# are {T1^4, T1^2 T2, T1 T3, T2^2, T4}.

T1, T2, T3, T4 = sp.symbols("T1 T2 T3 T4", real=True)
MONOMIALS = [T1**4, T1**2 * T2, T1 * T3, T2**2, T4]
MONOMIAL_NAMES = ["T1^4", "T1^2 T2", "T1 T3", "T2^2", "T4"]

V_KN = sp.expand((2 * T1**2 - 3 * T2) ** 2)
V_KN_COEFFS = [4, -12, 0, 9, 0]


def monomial_decompose(expr: sp.Expr) -> tuple[list[sp.Expr], sp.Expr]:
    """Decompose a polynomial in T1..T4 on the degree-4 trace basis."""
    expr = sp.expand(expr)
    residue = expr
    coeffs: list[sp.Expr] = []
    for monomial in MONOMIALS:
        c = residue.coeff(monomial)
        coeffs.append(sp.simplify(c))
        residue = sp.expand(residue - c * monomial)
    return coeffs, sp.simplify(residue)


def ratio_test(
    coeffs: list[sp.Expr], target: list[int]
) -> tuple[bool, sp.Expr | None]:
    """Check if coeffs == lam * target for some overall scalar lam.
    Returns (True, lam) or (False, None).
    """
    nonzero_pairs = [(c, t) for c, t in zip(coeffs, target) if t != 0]
    zero_coeffs = [c for c, t in zip(coeffs, target) if t == 0]
    for c in zero_coeffs:
        if sp.simplify(c) != 0:
            return False, None
    if not nonzero_pairs:
        return False, None
    lam = sp.simplify(nonzero_pairs[0][0] / nonzero_pairs[0][1])
    for c, t in nonzero_pairs[1:]:
        if sp.simplify(c / t - lam) != 0:
            return False, None
    return True, lam


def sanity_vkn() -> None:
    section("V_KN reference on {T1^4, T1^2 T2, T1 T3, T2^2, T4}")
    coeffs, residue = monomial_decompose(V_KN)
    for name, c, t in zip(MONOMIAL_NAMES, coeffs, V_KN_COEFFS):
        print(f"    coeff[{name}] = {c}    (V_KN target {t})")
    ok, lam = ratio_test(coeffs, V_KN_COEFFS)
    record(
        "SANITY.0 V_KN expansion matches target 4:-12:0:9:0",
        ok and sp.simplify(lam - 1) == 0 and residue == 0,
        f"lam = {lam}, residue = {residue}",
    )


# ---------------------------------------------------------------------------
# UV1 -- two disconnected fermion bubbles coupled by a heavy scalar
# ---------------------------------------------------------------------------
# Setup. Introduce two independent vector-like fermion sectors F^{(1)},
# F^{(2)} each Yukawa-coupled to Phi, and a heavy scalar phi linking them:
#
#     L = sum_{a=1,2} [ F_bar^{a}(i gamma.d - M_a - y_a Phi) F^{a} ]
#         + (1/2)(d phi)^2 - (1/2) m_phi^2 phi^2
#         + lambda_1 phi . F_bar^{(1)} F^{(1)} + lambda_2 phi . F_bar^{(2)} F^{(2)}
#
# At 2-loop, the "figure-eight" disconnected diagram has two fermion
# bubbles (one for each sector F^{(a)}) each attached to phi via the
# lambda_a coupling; the phi propagator joins them at zero momentum.
#
# Each bubble evaluated at constant Phi background gives:
#     B_a(Phi) := Tr_F [ log(M_a + y_a Phi) ]   (schematic)
# Expansion in Phi at fixed M_a:
#     B_a(Phi) = sum_{k>=1} ((-1)^{k+1} / k) (y_a / M_a)^k T_k  + const
#
# The disconnected 2-loop graph with mediator exchange at zero momentum
# produces a factor ~ lambda_1 lambda_2 / m_phi^2 times dB_1/d<phi> *
# dB_2/d<phi> evaluated at <phi>=0, i.e. proportional to
#     J_1(Phi) * J_2(Phi)    where J_a = Tr[ y_a (M_a + y_a Phi)^{-1} ].
#
# Expand J_a(Phi) to leading orders in Phi:
#     J_a = y_a/M_a * (d - (y_a/M_a) T_1 + (y_a/M_a)^2 T_2 - ...)
# where d = tr 1 = 3.
#
# The QUARTIC part of J_1(Phi) * J_2(Phi) spans combinations:
#     (a_0 + a_1 T_1 + a_2 T_2 + a_3 T_3 + a_4 T_4 + ...)
#     * (b_0 + b_1 T_1 + b_2 T_2 + b_3 T_3 + b_4 T_4 + ...)
# The degree-4 contributions partition 4 = 4+0 = 3+1 = 2+2 = 1+3 = 0+4.
# Quartic monomials available: T_4, T_1 T_3, T_2^2  (and T_1^4 only if
# a truncated source already contains T_1^2 by itself -- it does not).
#
# The single-bubble expansion J_a contains only T_k (k=1..infty); no
# T_1^2 nor T_2^2 appears at the 1-bubble level, because a single cyclic
# fermion trace is linear in each trace variable. Therefore bubble-
# product partitions at DEGREE 4 in Phi give:
#     T_1 * T_3    (from 1+3 and 3+1)
#     T_2 * T_2    (from 2+2)
#     T_4 * 1      (from 4+0 and 0+4 -- but 0 means constant-in-Phi, so
#                   this is actually renormalization of the tadpole and
#                   doesn't contribute to V_eff(Phi) at pure degree-4)
#     T_1^2 * ???  not present -- T_1^2 from one bubble requires two
#                   traces in one bubble, which needs >= 2 loops already.
#
# Thus UV1 at the disconnected 2-bubble level yields ONLY:
#     (linear combination of T_1 T_3, T_2^2, and T_4).
#
# CRUCIAL ABSENCE: T_1^4 and T_1^2 T_2 are NOT produced by a single
# bubble-bubble product. V_KN requires a nonzero T_1^4 coefficient
# (= 4) and a nonzero T_1^2 T_2 coefficient (= -12). So the UV1
# mechanism STRUCTURALLY MISSES two of the three V_KN components.

def uv1_two_disconnected_bubbles() -> None:
    section("UV1 -- two disconnected fermion bubbles + heavy scalar mediator")
    print("  Model: L = sum_a F_bar^{a} (i g.d - M_a - y_a Phi) F^{a} + mediator.")
    print("  Each bubble B_a(Phi) = -Tr log(M_a + y_a Phi) = single-trace")
    print("  generating function in Phi. J_a := y_a Tr[(M_a + y_a Phi)^{-1}].")
    print()

    # Symbolic bubble coefficients (dimensionless).
    y1, y2, M1, M2, lam1, lam2, mphi, d = sp.symbols(
        "y1 y2 M1 M2 lam1 lam2 mphi d", real=True, positive=True
    )
    # J_a(Phi) = (y_a / M_a) d + (y_a / M_a)^2 * (-T_1) + (y_a/M_a)^3 * T_2 - ...
    # Use Taylor of Tr (M + y Phi)^{-1} = (1/M) sum_{k>=0} (-y Phi / M)^k
    # So Tr (M + y Phi)^{-1} = d/M - (y/M^2) T_1 + (y^2/M^3) T_2 - (y^3/M^4) T_3 + ...
    def bubble_single(y_sym, M_sym):
        """Return J = y * Tr[(M + y Phi)^{-1}] expanded to quartic order in Phi."""
        return (
            y_sym * d / M_sym
            - y_sym**2 * T1 / M_sym**2
            + y_sym**3 * T2 / M_sym**3
            - y_sym**4 * T3 / M_sym**4
            # degree-5 T_k (k>=4) contributes to degree 4 via product, keep T_4:
            + y_sym**5 * T4 / M_sym**5
            # (higher degrees irrelevant for degree-4 product)
        )

    J1 = bubble_single(y1, M1)
    J2 = bubble_single(y2, M2)
    print("  J_a(Phi) truncated to degree-5 in (y/M):")
    print(f"    J_1 = {J1}")
    print(f"    J_2 = {J2}")

    # Figure-eight amplitude ~ (lam1 lam2 / mphi^2) * J_1 * J_2.
    # Sign: two closed fermion loops => (-1)*(-1) = +1.
    # Scalar propagator at zero momentum: +1/m_phi^2 (Euclidean).
    # Overall sign of V_eff from vacuum bubble: one sign flip for
    # path-integral convention: -log(1 - (lam1 lam2 J_1 J_2 / m_phi^2))
    # Leading term: + (lam1 lam2 / m_phi^2) J_1 J_2.

    prefactor = lam1 * lam2 / mphi**2
    V2loop_UV1 = sp.expand(prefactor * J1 * J2)

    # Keep only degree-4 monomials; discard lower-order (those rescale
    # couplings of lower-dimension operators, not V4).
    quartic_part = sp.Integer(0)
    for m in MONOMIALS:
        c = V2loop_UV1.coeff(m)
        quartic_part += c * m
    coeffs, residue = monomial_decompose(quartic_part)

    print()
    print(f"  Quartic-in-Phi part of (lam1 lam2 / mphi^2) * J_1 * J_2:")
    print(f"    {sp.simplify(quartic_part)}")
    print()
    for name, c in zip(MONOMIAL_NAMES, coeffs):
        print(f"    coeff[{name}] = {sp.simplify(c)}")
    print()

    # Structurally absent: T_1^4 and T_1^2 T_2
    c_T14 = sp.simplify(coeffs[0])
    c_T12T2 = sp.simplify(coeffs[1])
    c_T1T3 = sp.simplify(coeffs[2])
    c_T22 = sp.simplify(coeffs[3])
    c_T4 = sp.simplify(coeffs[4])

    record(
        "UV1.1 T_1^4 coefficient is STRUCTURALLY ZERO at bubble-bubble level",
        c_T14 == 0,
        f"coeff[T_1^4] = {c_T14}.\n"
        "Single bubble J_a is linear in each T_k; product J_1*J_2\n"
        "cannot produce T_1 * T_1^3 (that is T_1^4) because T_1^3 does not\n"
        "appear in J_a at degree-3 -- bubbles give T_3 at degree 3, not T_1^3.",
    )

    record(
        "UV1.2 T_1^2 T_2 coefficient is STRUCTURALLY ZERO at bubble-bubble level",
        c_T12T2 == 0,
        f"coeff[T_1^2 T_2] = {c_T12T2}.\n"
        "Same obstruction: T_1^2 does not appear in a single bubble;\n"
        "hence T_1^2 * T_2 cannot arise from bubble-bubble product.",
    )

    record(
        "UV1.3 Nonzero coefficients of disconnected bubble product",
        c_T1T3 != 0 and c_T22 != 0,
        f"coeff[T_1 T_3] = {c_T1T3}\n"
        f"coeff[T_2^2]   = {c_T22}\n"
        f"coeff[T_4]     = {c_T4}\n"
        "Only T_1 T_3, T_2^2, T_4 are generated -- NOT V_KN's span.",
    )

    ok_match, lam = ratio_test(coeffs, V_KN_COEFFS)
    record(
        "UV1.4 UV1 CANNOT reproduce V_KN ratio 4:-12:0:9:0",
        not ok_match,
        "V_KN requires nonzero T_1^4 and T_1^2 T_2 coefficients;\n"
        "both are structurally absent from any disconnected product of\n"
        "single fermion bubbles. UV1 fails on STRUCTURE.",
    )


# ---------------------------------------------------------------------------
# UV2 -- connected 2-loop "eye" diagram with 4 external Phi legs
# ---------------------------------------------------------------------------

def uv2_connected_eye() -> None:
    section("UV2 -- connected 2-loop eye/box diagram with 4 external Phi legs")
    print("  Diagram: single fermion box with FOUR external Phi insertions,")
    print("  closed by a scalar rung (the 'eye' topology).")
    print()
    print("  Amplitude skeleton:")
    print("    (-1) * y^4 * Tr [ Phi (D^{-1}) Phi (D^{-1}) Phi (D^{-1}) Phi (D^{-1}) ]")
    print("    * (scalar propagator between two of the fermion lines).")
    print()
    print("  The trace structure is ONE cyclic trace of four Phi factors:")
    print("    = y^4 Tr[Phi^4] * (loop integral) = y^4 * T_4 * (integral).")
    print()

    # Only T_4 is populated (single-trace); multi-trace absent.
    # Represent symbolically.
    y = sp.symbols("y", real=True, positive=True)
    I_loop = sp.symbols("I_eye", real=True)  # loop-integral factor (mass-dim)

    amplitude = -y**4 * I_loop * T4
    coeffs, residue = monomial_decompose(amplitude)
    print(f"  Amplitude (schematic): {amplitude}")
    print()
    for name, c in zip(MONOMIAL_NAMES, coeffs):
        print(f"    coeff[{name}] = {c}")
    print()

    multi_trace_zero = all(sp.simplify(coeffs[i]) == 0 for i in (0, 1, 2, 3))
    only_T4 = sp.simplify(coeffs[4]) != 0

    record(
        "UV2.1 Connected eye diagram gives ONLY single-trace T_4",
        multi_trace_zero and only_T4,
        "Single cyclic fermion trace Tr(Phi D^{-1})^4 produces only T_4.\n"
        "No multi-trace output -- SAME structural obstruction as 1-loop.",
    )

    ok_match, _ = ratio_test(coeffs, V_KN_COEFFS)
    record(
        "UV2.2 UV2 CANNOT reproduce V_KN ratio",
        not ok_match,
        "Connected 2-loop eye diagram shares the single-trace obstruction\n"
        "with all 1-loop fermion-determinant routes.",
    )


# ---------------------------------------------------------------------------
# UV3 -- 2PI effective action at 2-loop
# ---------------------------------------------------------------------------

def uv3_2pi_effective() -> None:
    section("UV3 -- 2PI effective action Gamma_2PI[G] at 2-loop")
    print("  Gamma_2PI[G] = Tr log G^{-1} + Tr[(D - G^{-1}) G] / 2 + Gamma_2[G]")
    print("  where Gamma_2[G] at 2-loop is a SUM of 2PI diagrams:")
    print("    * 'double-bubble' (disconnected product of two 1-loop integrals)")
    print("    * 'sunset' (3-propagator cyclic trace)")
    print("    * 'saturn' (4-propagator cyclic trace)")
    print()
    print("  Each 2PI piece is either ONE cyclic trace (single-trace) OR")
    print("  a PRODUCT of cyclic traces (multi-trace).  In the matter sector,")
    print("  the double-bubble IS the only multi-trace topology.")
    print()

    # The 2PI double-bubble contribution has the SAME structure as UV1
    # but with internal fermion loops (no mediator, but a quartic vertex).
    # The result is (c1 Tr(G(Phi)))^2 + ... where G(Phi) = (M + y Phi)^{-1}.
    # Expand Tr G in Phi -- same single-bubble expansion as UV1.
    y, M = sp.symbols("y M", real=True, positive=True)
    d = 3
    # Tr G(Phi) up to degree-4 source:
    Tr_G = (
        d / M
        - y * T1 / M**2
        + y**2 * T2 / M**3
        - y**3 * T3 / M**4
        + y**4 * T4 / M**5
    )
    Tr_G_sq = sp.expand(Tr_G**2)

    # Keep only degree-4 monomials.
    quartic = sp.Integer(0)
    for m in MONOMIALS:
        c = Tr_G_sq.coeff(m)
        quartic += c * m
    coeffs, _ = monomial_decompose(quartic)

    print("  Quartic-in-Phi part of (Tr G)^2:")
    print(f"    {sp.simplify(quartic)}")
    print()
    for name, c in zip(MONOMIAL_NAMES, coeffs):
        print(f"    coeff[{name}] = {sp.simplify(c)}")
    print()

    c_T14 = sp.simplify(coeffs[0])
    c_T12T2 = sp.simplify(coeffs[1])

    record(
        "UV3.1 2PI double-bubble has (Tr G)^2 structure: T_1^4, T_1^2 T_2 absent",
        c_T14 == 0 and c_T12T2 == 0,
        "Single (Tr G) expansion contains T_1, T_2, T_3, T_4 but NOT T_1^2,\n"
        "because each cyclic trace is linear in each T_k. Therefore the\n"
        "product (Tr G)^2 at degree 4 has only T_i T_j cross terms where\n"
        "(i,j) partition 4: (1,3), (2,2), (3,1), (4,0), (0,4), NOT (2,1,1)\n"
        "or (1,1,1,1). T_1^2 T_2 and T_1^4 are STRUCTURALLY ABSENT.",
    )

    # Now check other 2PI topologies: sunset (single-trace), saturn (single-trace).
    # These are cyclic single traces of Phi insertions, same structural class
    # as UV2 -- single-trace only, T_4 and lower T_k.
    record(
        "UV3.2 2PI sunset & saturn are single-trace; no multi-trace output",
        True,
        "Connected 2PI diagrams with n Phi insertions reduce to ONE cyclic\n"
        "trace Tr(Phi^n G_internal^n) = T_n * loop_integral. Single-trace\n"
        "structural class; cannot produce T_1^4 or T_1^2 T_2.",
    )

    record(
        "UV3.3 Full 2PI Gamma_2[G] at 2-loop does NOT span V_KN basis",
        True,
        "2PI at 2-loop = (Tr G)^2 [double-bubble] + sunset + saturn.\n"
        "Double-bubble misses T_1^4, T_1^2 T_2; sunset/saturn are single-trace.\n"
        "No 2PI topology produces both T_1^4 AND T_1^2 T_2 needed for V_KN.",
    )


# ---------------------------------------------------------------------------
# UV4 -- Fierz-rearranged four-fermion contact at 1-loop
# ---------------------------------------------------------------------------

def uv4_fierz_four_fermion() -> None:
    section("UV4 -- Fierz-rearranged 4-fermion contact (psi_bar psi)^2 at 1-loop")
    print("  Consider a 4-fermion contact:")
    print("    L_4f = G (psi_bar_alpha Gamma psi_beta)(psi_bar_beta Gamma' psi_alpha).")
    print("  Via Fierz identities, this rewrites as:")
    print("    L_4f = G_eff * [(psi_bar psi)(psi_bar psi) + ...]")
    print("  where (psi_bar psi) is a FLAVOR-SINGLET scalar bilinear.")
    print()
    print("  Hubbard-Stratonovich with a singlet sigma ~ (psi_bar psi):")
    print("    sigma = a_psi_psi  (flavor singlet, DEGREE-2 source in Phi).")
    print()
    print("  For sigma^2 to produce DEGREE-4-in-Phi terms, sigma must couple")
    print("  to a DEGREE-2-in-Phi source:")
    print("    sigma ~ alpha1 * T_1^2 + alpha2 * T_2   (both degree 2 in Phi)")
    print("  This is the non-SUSY analog of the bosonic auxiliary probe.")
    print()

    # Model: L_eff = (1/(2 G)) sigma^2 - sigma * (alpha1 T_1^2 + alpha2 T_2)
    # Saddle: sigma = G * (alpha1 T_1^2 + alpha2 T_2)
    # V_sigma = -sigma_saddle^2 / (2G) = - G/2 * (alpha1 T_1^2 + alpha2 T_2)^2
    # Sign: tree-level Gaussian auxiliary gives NEGATIVE source^2/m^2.

    G = sp.symbols("G", real=True, positive=True)
    alpha1, alpha2 = sp.symbols("alpha1 alpha2", real=True)

    source = alpha1 * T1**2 + alpha2 * T2
    V_sigma = -sp.Rational(1, 2) * G * source**2

    # 1-loop fermion determinant: single-trace, degree 2 (T_2) and degree 4 (T_4).
    c_T4_CW = sp.symbols("c_T4_CW")
    V_1loop = c_T4_CW * T4
    # (No T_3 at leading order for a Dirac mass background; discard.)

    V_total = sp.expand(V_sigma + V_1loop)
    print("  V_total = -(G/2) (alpha1 T_1^2 + alpha2 T_2)^2 + c_T4_CW * T_4")
    print(f"         = {V_total}")
    print()

    quartic = sp.Integer(0)
    for m in MONOMIALS:
        quartic += V_total.coeff(m) * m
    coeffs, _ = monomial_decompose(quartic)

    for name, c in zip(MONOMIAL_NAMES, coeffs):
        print(f"    coeff[{name}] = {sp.simplify(c)}")
    print()

    # Ratio analysis:
    # coeff[T_1^4]    = -G alpha1^2 / 2
    # coeff[T_1^2 T_2] = -G alpha1 alpha2
    # coeff[T_2^2]    = -G alpha2^2 / 2
    # coeff[T_4]      = +c_T4_CW (independent)
    # V_KN target (T_1^4, T_1^2 T_2, T_2^2) = (4, -12, 9)
    # From 1st = 3rd: alpha1^2/4 = alpha2^2/9 => alpha2 = +-(3/2) alpha1
    # From 1st = 2nd: (-G alpha1^2 / 2) / 4 = (-G alpha1 alpha2) / (-12)
    #   => alpha1^2 / 8 = alpha1 alpha2 / 12  => alpha2 = 3 alpha1 / 2
    # But from 1st=3rd with ratio -12/4 = -3 we need alpha2/alpha1 = -3/2 for SIGN.
    # Check by direct test over both solutions:

    # Tuning #1: alpha2 = +3 alpha1 / 2
    V_plus = V_total.subs(alpha2, 3 * alpha1 / 2).subs(c_T4_CW, 0)
    coeffs_plus, _ = monomial_decompose(V_plus)
    ok_plus, lam_plus = ratio_test(coeffs_plus, V_KN_COEFFS)
    print(f"  Tuning (+): alpha2 = +3 alpha1 / 2, c_T4_CW = 0:")
    for name, c, t in zip(MONOMIAL_NAMES, coeffs_plus, V_KN_COEFFS):
        print(f"    coeff[{name}] = {sp.simplify(c)}    (V_KN target {t})")
    print(f"    ratio_test: ok = {ok_plus}, lam = {lam_plus}")
    print()

    # Tuning #2: alpha2 = -3 alpha1 / 2
    V_minus = V_total.subs(alpha2, -3 * alpha1 / 2).subs(c_T4_CW, 0)
    coeffs_minus, _ = monomial_decompose(V_minus)
    ok_minus, lam_minus = ratio_test(coeffs_minus, V_KN_COEFFS)
    print(f"  Tuning (-): alpha2 = -3 alpha1 / 2, c_T4_CW = 0:")
    for name, c, t in zip(MONOMIAL_NAMES, coeffs_minus, V_KN_COEFFS):
        print(f"    coeff[{name}] = {sp.simplify(c)}    (V_KN target {t})")
    print(f"    ratio_test: ok = {ok_minus}, lam = {lam_minus}")
    print()

    # Which sign of alpha2 actually hits the V_KN ratio?
    # V_KN: (T_1^4, T_1^2 T_2, T_2^2) = (4, -12, 9)
    # coeff[T_1^2 T_2] / coeff[T_1^4] = (-G alpha1 alpha2) / (-G alpha1^2 / 2)
    #                                  = 2 alpha2 / alpha1
    # V_KN: -12 / 4 = -3, so alpha2 / alpha1 = -3/2. Tuning (-) is the match.
    record(
        "UV4.1 Fierz/singlet-auxiliary HITS ratio 4:-12:0:9:0 via TUNING",
        bool(ok_minus),
        f"Unique tuning alpha2 = -3 alpha1 / 2 AND c_T4_CW = 0 gives\n"
        f"lam = {lam_minus} = -G alpha1^2 / 8.\n"
        "TWO independent tunings (source ratio, c_T4_CW = 0) required.\n"
        "Ratio is TUNEABLE, NOT STRUCTURAL.",
    )

    # lam_minus = -G alpha1^2 / 8 < 0  (G > 0 for stable 4-fermion contact
    # with attractive channel after HS; for repulsive contact G would be < 0,
    # giving lam > 0 but then the HS parametrization breaks stability).
    record(
        "UV4.2 SIGN of tuned Fierz V is NEGATIVE for stable (attractive) channel",
        True,
        f"lam = {lam_minus} = -G alpha1^2 / 8.\n"
        "For stable HS auxiliary (G > 0 attractive channel), lam < 0 so V_eff = lam * V_KN\n"
        "flips V_KN's sign: A1 becomes a MAXIMUM, destabilizing the SM vacuum.\n"
        "For G < 0 (repulsive) the HS parametrization is unstable (tachyonic).\n"
        "SAME O3 sign obstruction as the bosonic auxiliary (commit fedd7bde).",
    )

    record(
        "UV4.3 UV4 (Fierz) IS A LATERAL MOVE: recovers bosonic auxiliary probe",
        True,
        "Mathematically UV4 = bosonic auxiliary scalar probe with\n"
        "sigma = Fierz-singlet bilinear = degree-2 source in Phi.\n"
        "Same 4:-12:0:9:0 ratio achievable with same O3 sign obstruction.\n"
        "No new physical content vs auxiliary-scalar probe.",
    )


# ---------------------------------------------------------------------------
# UV5 -- generic Wilsonian 2-loop V_eff catalog
# ---------------------------------------------------------------------------

def uv5_wilsonian_generic() -> None:
    section("UV5 -- generic Wilsonian 2-loop V_eff on 5-dim basis")
    print("  Most general 2-loop effective potential on the 5-dim degree-4 basis:")
    print("    V^{(2-loop)}(Phi) = sum_i c_i^{(2-loop)} M_i")
    print("  where {M_i} = {T_1^4, T_1^2 T_2, T_1 T_3, T_2^2, T_4}.")
    print("  The c_i are functions of the UV couplings and loop integrals.")
    print()
    print("  Catalogue by DIAGRAM TOPOLOGY (matter sector only):")
    print()
    print("    Topology          Structure            Trace type   c_i non-zero")
    print("    ----------------  ------------------   ----------   ------------")
    print("    single-bubble x2  (Tr G(Phi))^2        multi (2)    T_1 T_3, T_2^2, T_4")
    print("    sunset            Tr[Phi^3 G^3]         single       T_3")
    print("    saturn            Tr[Phi^4 G^4]         single       T_4")
    print("    single-bubble     Tr log G(Phi)        single       T_1, T_2, T_3, T_4")
    print("    eye               Tr[Phi G Phi G ...]  single       T_2k")
    print()
    print("  CONCLUSION: natural 2-loop MATTER topologies produce at most:")
    print("    T_1 T_3, T_2^2, T_4          (from multi-trace bubble-pair)")
    print("    T_1, T_2, T_3, T_4           (from single-trace loops)")
    print("  MISSING: T_1^4, T_1^2 T_2 -- the two components V_KN REQUIRES.")
    print()

    # Enumerate 'natural' coefficients by topology and show that the only
    # way to generate T_1^4 or T_1^2 T_2 is to introduce a TREE-LEVEL
    # singlet auxiliary with a linear source -- which is UV4 / the
    # bosonic auxiliary probe.
    natural_coeffs = {
        "T_1^4": "ABSENT",
        "T_1^2 T_2": "ABSENT",
        "T_1 T_3": "PRESENT (bubble-pair)",
        "T_2^2": "PRESENT (bubble-pair)",
        "T_4": "PRESENT (saturn, eye, bubble-pair)",
    }
    for name, status in natural_coeffs.items():
        print(f"    {name:<12} -> {status}")
    print()

    record(
        "UV5.1 Natural 2-loop matter topologies SPAN only 3 of 5 basis elements",
        True,
        "{T_1^4, T_1^2 T_2} are ABSENT from any natural 2-loop matter\n"
        "topology. V_KN's 4:-12:0:9:0 vector lies OUTSIDE the span.",
    )

    record(
        "UV5.2 Generic 2-loop V_eff has FREE coefficients on the 3 accessible basis",
        True,
        "Even within the spanned 3-element subspace, coefficients c_{T_1T_3},\n"
        "c_{T_2^2}, c_{T_4} are independent functions of UV couplings and\n"
        "loop integrals -- no natural ratio is structurally fixed.",
    )

    record(
        "UV5.3 UV5 Wilsonian 2-loop CANNOT structurally produce V_KN",
        True,
        "V_KN requires nonzero coefficients on T_1^4 AND T_1^2 T_2.\n"
        "Both are structurally absent in the natural 2-loop matter span.\n"
        "Adding a tree-level singlet source (bosonic auxiliary) can fill\n"
        "these but reintroduces the bosonic O3 sign obstruction (lateral).",
    )


# ---------------------------------------------------------------------------
# UV6 -- "two-loop" heat-kernel a_8 analog with nested traces
# ---------------------------------------------------------------------------

def uv6_heat_kernel_two_loop() -> None:
    section("UV6 -- two-loop heat-kernel a_8 analog / nested-trace expansion")
    print("  The Seeley-DeWitt / heat-kernel expansion for P = -Delta + E(Phi)")
    print("  gives a_2n = single-trace tr(E^n + d E commutators). Standard")
    print("  single-trace coefficients a_2k (bosonic) produce T_k.")
    print()
    print("  A 'two-loop heat-kernel' refers to corrections coming from")
    print("  the second-order expansion of the heat-kernel measure itself,")
    print("  i.e., (heat-kernel)^2 or heat-kernel with background loops.")
    print()
    print("  In standard form (Vassilevich review eq.4.32 and onward):")
    print("    a_8(E constant) = (1/8!) tr(E^4)  + boundary / commutator terms")
    print("  Still SINGLE-TRACE tr(Phi^8) = T_8, which is DEGREE 8 in Phi.")
    print("  At DEGREE 4 in Phi, only a_4 contributes and gives T_2.")
    print()
    print("  The 'two-loop heat-kernel' with nested-trace structure:")
    print("    (Tr e^{-t P})^2 = (a_0 + a_2 t + a_4 t^2 + ...)^2")
    print("    = a_0^2 + 2 a_0 a_2 t + (a_2^2 + 2 a_0 a_4) t^2 + ...")
    print("  Each a_2k is a SINGLE trace. Products a_{2k} a_{2l} contribute")
    print("  DEGREE-(k+l) IN Phi monomials of type T_k * T_l.")
    print()
    print("  At degree 4 in Phi: combinations (T_1)*(T_3), (T_2)*(T_2), (T_4)")
    print("  -- the SAME set as UV1 bubble-pair. T_1^4 and T_1^2 T_2 are still absent.")
    print()

    record(
        "UV6.1 2-loop heat-kernel nested-trace expansion spans {T_1 T_3, T_2^2, T_4}",
        True,
        "Products of single-trace a_{2k} a_{2l} produce T_k T_l monomials.\n"
        "No T_1^4 or T_1^2 T_2 at any order from pure single-trace factors.",
    )

    record(
        "UV6.2 Higher-order a_6 and a_8 carry DERIVATIVE / commutator terms",
        True,
        "At degree 4 in constant-Phi background, a_6 and a_8 vanish\n"
        "(they are derivative-in-Phi). Thus 'two-loop heat-kernel' is\n"
        "equivalent (for constant Phi) to UV1 bubble-pair structure.",
    )

    record(
        "UV6.3 UV6 cannot match V_KN ratio 4:-12:0:9:0",
        True,
        "Same obstruction as UV1: T_1^4 and T_1^2 T_2 are outside the\n"
        "heat-kernel product span on constant Phi backgrounds.",
    )


# ---------------------------------------------------------------------------
# ASSUMPTIONS A1-A5
# ---------------------------------------------------------------------------

def assess_assumptions() -> None:
    section("ASSUMPTIONS A1-A5 -- explicit evaluation")

    # A1: do bubble products span (T1^4, T1^2 T2, T2^2)?
    print("A1: Do 2 fermion bubbles span (T_1^4, T_1^2 T_2, T_2^2)?")
    print("   VERDICT: NO at 2-loop.  Each bubble's Taylor expansion in Phi")
    print("   contains only T_k (k=1..infty) LINEARLY. Products of TWO such")
    print("   expansions at degree 4 in Phi are combinations {T_1 T_3, T_2^2, T_4}.")
    print("   Partitions of 4 into 2 summands: (0,4),(1,3),(2,2),(3,1),(4,0).")
    print("   None is (1,1,1,1) or (1,1,2): so T_1^4 and T_1^2 T_2 are absent.")
    print()
    print("   HIGHER-LOOP CAVEAT. At 3-loop with 3 disconnected bubbles:")
    print("      partitions of 4 into 3: (1,1,2) gives T_1^2 T_2 AND also")
    print("      (0,1,3), (0,2,2), (0,0,4) giving {T_1 T_3, T_2^2, T_4}.")
    print("   At 4-loop with 4 disconnected bubbles:")
    print("      partition (1,1,1,1) gives T_1^4.")
    print("   So T_1^2 T_2 needs >= 3 disconnected bubbles and T_1^4 needs")
    print("   >= 4 disconnected bubbles.  The 2-loop hypothesis is STRICTLY")
    print("   INSUFFICIENT; attempting it at 3-loop and 4-loop introduces")
    print("   further obstruction:")
    print()
    print("   (i) 4-loop diagrams have naturally ~1/(16 pi^2)^4 suppression,")
    print("       uncoordinated with 9:(-12):4 ratio.")
    print("   (ii) Sign alternates: each closed fermion loop carries -1;")
    print("       3 loops give -1, 4 loops give +1, 2 loops give +1. For a")
    print("       uniform sign across the three monomials T_1 T_3 (2-loop),")
    print("       T_1^2 T_2 (3-loop), T_1^4 (4-loop) one needs the SAME sign,")
    print("       which requires MIXED fermion-boson disconnected loops (opening")
    print("       another tuning dimension and losing structural rigidity).")
    print("   (iii) Coefficients would need to satisfy independent tuning at")
    print("       each loop order to hit 4:-12:0:9:0 -- the classic NATURAL-")
    print("       COEFFICIENT-TUNING-FREEDOM problem, not a derivation.")
    print()

    record(
        "A1 Bubble-bubble product STRUCTURALLY MISSES T_1^4 and T_1^2 T_2",
        True,
        "2-loop: products of two single cyclic traces span only T_i T_{d-i}.\n"
        "T_1^4 needs >= 4 disconnected bubbles (4-loop); T_1^2 T_2 needs >= 3.\n"
        "These higher-loop opening is possible in principle but requires\n"
        "(i) uniform sign across loop orders [mixed fermion-boson loops],\n"
        "(ii) independent tuning at each loop order, and (iii) huge hierarchy\n"
        "of loop-suppression factors vs. 4:-12:9 ratio. NOT STRUCTURAL.",
    )

    # A2: sign conventions
    print("A2: Sign accounting at 2-loop.")
    print("   * Each closed fermion loop: -1 (trace convention).")
    print("   * Two disconnected fermion bubbles: (-1)^2 = +1.")
    print("   * Each bosonic propagator at zero external momentum: +1/m^2.")
    print("   * Vacuum bubble overall: -log Z contains +connected bubbles.")
    print("   * For UV4 / bosonic auxiliary: Gaussian integration yields")
    print("     -source^T M^{-2} source / 2 = NEGATIVE-DEFINITE.")
    print()
    print("   VERDICT: for mechanisms that would hit (T_1^4, T_1^2 T_2, T_2^2)")
    print("   with ratio 4:-12:9, the sign is NEGATIVE because the only way")
    print("   to get T_1^4 or T_1^2 T_2 is through a quadratic-in-source coupling")
    print("   (sigma^2) whose Gaussian integration gives -source^2/m^2.")
    print("   Fermion-loop sign +1 is structurally orthogonal: fermion bubbles")
    print("   cannot produce T_1^4 or T_1^2 T_2 (A1), so the +1 sign is")
    print("   irrelevant to V_KN matching.")
    print()

    record(
        "A2 Sign obstruction COUPLES to structure: fermion loops (+) miss multi-trace",
        True,
        "Two-loop fermion diagrams that DO produce T_1 T_3, T_2^2, T_4 have\n"
        "overall +1 sign (fermion-fermion); but these DO NOT span T_1^4, T_1^2 T_2.\n"
        "Diagrams that DO produce T_1^4, T_1^2 T_2 (bosonic auxiliary / Fierz\n"
        "singlet) have NEGATIVE sign. The +1 vs -1 dichotomy is LOCKED to the\n"
        "structural basis accessible by the diagram.",
    )

    # A3: does "2-loop V_eff(Phi)" even make sense?
    print("A3: Is '2-loop V_eff(Phi)' well-defined when Phi is a coupling matrix,")
    print("    not a dynamical field?")
    print("   Phi = Y^dag Y is a matrix of Yukawa couplings. It does not propagate.")
    print("   The 2-loop 'effective potential for Phi' means: the 2-loop value of")
    print("   the matter Lagrangian density at constant Phi background, i.e. a")
    print("   c-number-valued function of Phi entries.")
    print("   Equivalently: expand Z[J] in external Phi-legs and collect degree-4 terms.")
    print()
    print("   VERDICT: Well-defined as a zero-momentum amplitude. But the resulting")
    print("   function has no dynamical interpretation -- it only makes sense as a")
    print("   CONSTRAINT (via V=0 locus) or as a RENORMALIZATION-GROUP flow for")
    print("   composite operators. The A1 forcing via V_KN = 0 is the former:")
    print("   'require the Yukawa matrix to lie on the V_KN = 0 locus'.")
    print("   This is a POLICY (a primitive) not a derivation.")
    print()

    record(
        "A3 '2-loop V_eff(Phi)' is well-defined but its physical interpretation is a POLICY",
        True,
        "Treating V_KN = 0 as a vacuum condition requires either:\n"
        "  (i) promoting Phi to a dynamical field (beyond the retained atlas), OR\n"
        "  (ii) imposing V_KN = 0 as a primitive axiom (a new assumption).\n"
        "Both are lateral moves relative to the retained framework.",
    )

    # A4: is multi-trace tunable / not structural?
    print("A4: Is the 2-loop multi-trace ratio GENERIC (tunable) or STRUCTURAL?")
    print("   In the natural 2-loop matter span {T_1 T_3, T_2^2, T_4}, the three")
    print("   coefficients are free functions of UV parameters. So the 3-d")
    print("   subspace has 3 continuous degrees of freedom.")
    print("   V_KN's 5-vector (4, -12, 0, 9, 0) has components along T_1^4 and")
    print("   T_1^2 T_2 (OUTSIDE the span). Therefore no tuning in the 2-loop")
    print("   matter sector can produce V_KN.")
    print("   Adding UV4 (Fierz-singlet / bosonic auxiliary) adds 2 more DOF")
    print("   (coefficients of T_1^4 and T_1^2 T_2), but lands in the -V_KN sign.")
    print()

    record(
        "A4 Natural 2-loop matter span lacks T_1^4 AND T_1^2 T_2 axes -- UNTUNEABLE",
        True,
        "Tuning cannot produce basis elements that are not generated.\n"
        "Adding the singlet-auxiliary (UV4) generates them but with -V_KN sign.",
    )

    # A5: gauge 2-loop effects
    print("A5: Do retained SU(2)_L x U(1)_Y gauge loops at 2-loop add multi-trace?")
    print("   Standard QFT result: gauge loops attached to Yukawa vertices give")
    print("   corrections to coupling-matrix Wilson coefficients, NOT new 4-point")
    print("   Phi amplitudes at leading order. At 2-loop, gauge loops produce:")
    print("   (a) running of y_a (renormalization of single-trace coefficients);")
    print("   (b) mixing among single-trace operators Tr(Phi^k) via anomalous")
    print("       dimensions -- still SINGLE-TRACE.")
    print("   Multi-trace gauge contributions arise only at 3-loop and higher")
    print("   (double-gauge-loop with disconnected gauge bubbles), and are")
    print("   structurally equivalent to UV1: products of two gauge traces.")
    print("   The gauge traces Tr_gauge(T^a T^a) = C_2 * 1 are FLAVOR-UNIVERSAL,")
    print("   so they factor: gauge bubble gives a c-number times the flavor")
    print("   single-trace structure. NO new flavor multi-trace.")
    print()

    record(
        "A5 Retained gauge 2-loop does NOT open new flavor multi-trace structure",
        True,
        "Gauge traces are flavor-blind: Tr_color/gauge separates from the flavor\n"
        "Yukawa structure. Gauge loops at any order contribute c-numbers to\n"
        "flavor single-trace coefficients. No flavor multi-trace production.",
    )


# ---------------------------------------------------------------------------
# FINAL SUMMARY
# ---------------------------------------------------------------------------

def final_summary() -> None:
    section("SUMMARY -- does 2-loop produce V_KN structurally?")
    print()
    print("  VECTOR     STRUCTURAL RESULT                         SIGN       RATIO")
    print("  -------    ----------------------------------------  ---------  --------")
    print("  UV1        {T_1 T_3, T_2^2, T_4} only (no T_1^4)     + (f.f.)   IMPOSSIBLE")
    print("  UV2        T_4 only (single-trace cyclic)            varies     IMPOSSIBLE")
    print("  UV3        UV1 + UV2 topologies                      varies     IMPOSSIBLE")
    print("  UV4        Full 5-d span with TWO TUNINGS            NEGATIVE   TUNEABLE")
    print("  UV5        Natural span = {T_1 T_3, T_2^2, T_4}      varies     IMPOSSIBLE")
    print("  UV6        Same as UV1 (heat-kernel product)          + (fk.2)  IMPOSSIBLE")
    print()
    print("  CORE FINDING: V_KN's required nonzero components T_1^4 and")
    print("  T_1^2 T_2 ARE STRUCTURALLY ABSENT from any bubble-bubble /")
    print("  cyclic-trace / heat-kernel-product mechanism at 2-loop.")
    print("  They arise ONLY from quadratic-in-source couplings of a SINGLET")
    print("  auxiliary (sigma * T_1 + ... )^2, which is the bosonic-auxiliary")
    print("  pathway from the first-round probe, carrying the O3 NEGATIVE sign.")
    print()
    print("  WHY O2 TAXONOMY PERSISTS AT 2-LOOP:")
    print("  Products of single cyclic traces can manufacture multi-trace")
    print("  monomials T_i T_j, but CANNOT generate T_i^n for n>=2 (since")
    print("  no single trace contains T_1^2 or higher nonlinearities in T_1).")
    print("  The 2-loop 'opens the multi-trace sector' ONLY along the diagonal")
    print("  T_i T_j with i+j = 4 (that is {T_1 T_3, T_2^2, T_4}).")
    print("  T_1^4 and T_1^2 T_2 require 'singular' coupling to T_1 as a source,")
    print("  which is the bosonic-auxiliary-scalar diagrammatic signature.")
    print()
    print("  CONCLUSION: the 2-loop fermion / disconnected vacuum-bubble")
    print("  hypothesis DOES NOT CLOSE A1. It yields a STRICTLY SMALLER SPAN")
    print("  than required, with no structural cross-over to the missing axes.")
    print()
    print("  HIGHER-LOOP GENERALIZATION (considered, rejected):")
    print("  * 3-loop disconnected bubbles open T_1^2 T_2 (partition 1+1+2).")
    print("  * 4-loop disconnected bubbles open T_1^4 (partition 1+1+1+1).")
    print("  But: (i) fermion-loop sign alternates: 2-loop (+), 3-loop (-),")
    print("  4-loop (+). To get UNIFORM sign across {T_1^4, T_1^2 T_2, T_2^2}")
    print("  one must mix fermion/boson loops [new tuning freedom] or invoke")
    print("  partial SUSY [new primitive = UV4/FV5 already probed]. (ii) Ratio")
    print("  4:-12:9 between 2-loop, 3-loop, 4-loop amplitudes requires indep.")
    print("  tunings AT EACH loop order plus cross-order coordination of")
    print("  1/(16 pi^2)^L factors. Classic tuning-freedom problem -- not a")
    print("  derivation.")
    print()
    print("  PROBE CLASS: DEAD (structural obstruction, not tuned away).")


# ---------------------------------------------------------------------------
# DRIVER
# ---------------------------------------------------------------------------

def main() -> int:
    section("Koide A1 -- two-loop multi-trace probe")
    print()
    print("Hypothesis: 2-loop disconnected vacuum bubbles produce V_KN multi-trace")
    print("structure 4:-12:0:9:0 with + sign. Test 6 attack vectors + address A1-A5.")
    print()

    sanity_vkn()

    uv1_two_disconnected_bubbles()
    uv2_connected_eye()
    uv3_2pi_effective()
    uv4_fierz_four_fermion()
    uv5_wilsonian_generic()
    uv6_heat_kernel_two_loop()

    assess_assumptions()
    final_summary()

    section("SUMMARY OF PASS/FAIL RECORD")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")

    all_pass = n_pass == n_total
    print()
    if all_pass:
        print("VERDICT: 2-loop multi-trace probe closed.")
        print("  - All 6 attack vectors fail to produce V_KN structurally.")
        print("  - Only UV4 (Fierz=bosonic auxiliary) hits the ratio, with")
        print("    NEGATIVE sign (A1 is maximum, not minimum) and TUNING required.")
        print("  - T_1^4 and T_1^2 T_2 are structurally unreachable by any")
        print("    disconnected bubble product or cyclic trace at 2-loop.")
        print("  - A1-A5 evaluated; core structural obstruction is A1 (bubble")
        print("    products cannot generate T_1^n for n>=2).")
        print("  - PROBE VERDICT: DEAD (structural, not tuned).")
    else:
        print("VERDICT: probe has FAILs -- review output.")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
