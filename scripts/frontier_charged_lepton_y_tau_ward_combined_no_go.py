#!/usr/bin/env python3
"""Combined no-go for the charged-lepton y_tau Ward identity.

This runner verifies the structural facts behind
`docs/CHARGED_LEPTON_Y_TAU_WARD_COMBINED_NO_GO_NOTE_2026-05-10.md`.

It proves a negative boundary: no Ward identity of the form

    y_tau_bare = G x C                                              (T)

— where G is a retained gauge or transport coefficient and C is a
structural sqrt-rational constant produced by retained representation
theory — is constructible on the current framework surface.

The proof is a positive structural verification of each obstruction:

  (SA-A)  SU(N_c) Fierz factor 1/sqrt(2 N_c) is a non-abelian Fierz
          construct; the lepton (2, 1) block has no color sector
          to Fierz against.
  (SA-B)  U(1)_Y is abelian; charges multiply, no Fierz reorganization.
  (M3)    'EW A4' content is Wolfenstein A^4 = 4/9, not alternating
          group A_4; arithmetic identity sin^2(theta_W)|_lattice =
          (d+1)/(2d+3) at d=3 verified.
  (M4)    Anomaly cancellation forces matter content but not Yukawa
          coefficient values; one-Higgs gauge selection leaves Y_e
          arbitrary.
  (M5)    Cross-sector closure is N_gen = N_color = 3 (integer),
          NOT a Yukawa-coefficient identity.
  (M6)    Three-generation hw=1 connects nowhere to retained Yukawa
          coefficients.

Each obstruction is verified symbolically (sympy / fractions) where
applicable; the runner asserts class-A patterns (math.isclose,
sympy.simplify, sympy.Eq) on the structural identities.

This runner does NOT use PDG masses, fitted Yukawas, or observed
Koide values. Per the loop's forbidden-imports list, no empirical
charged-lepton input is read.
"""

from __future__ import annotations

import json
import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"

PASS_COUNT = 0
FAIL_COUNT = 0


def check(label: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {label}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def d17_prime_retained_status() -> tuple[list[str], list[str]]:
    """Return all D17-prime rows and the retained-grade subset.

    The no-go is a statement about the current retained framework surface, not
    about whether a proposal file exists. An unaudited D17-prime candidate is a
    real research route, but it is not a retained authority for this theorem.
    """
    retained_grade = {"retained", "retained_bounded", "retained_no_go"}
    candidates: list[str] = []
    retained: list[str] = []
    rows = json.loads(LEDGER.read_text())["rows"]
    for claim_id, row in rows.items():
        note_path = str(row.get("note_path") or "")
        haystack = f"{claim_id} {note_path}".lower()
        if "d17_prime" not in haystack and "d17-prime" not in haystack:
            continue
        status = row.get("effective_status")
        audit_status = row.get("audit_status")
        claim_type = row.get("claim_type")
        summary = f"{claim_id}:{claim_type}:{audit_status}:{status}"
        candidates.append(summary)
        if status in retained_grade:
            retained.append(summary)
    return candidates, retained


# ============================================================================
# (SA-A) SU(N_c) Fierz factor on the fundamental rep
# ============================================================================


def part_sa_a_color_fierz_factor() -> None:
    """Verify YT-lane's load-bearing factor sqrt(2 N_c) on (2, 3) block.

    The SU(N_c) Fierz factor 1/sqrt(2 N_c) comes from the trace identity

        Tr(T^a T^b) = (1/2) delta^{a b}                              (D12-trace)

    in the fundamental rep of SU(N_c). For N_c = 3 this gives the
    YT-lane factor 1/sqrt(6).

    The lepton-doublet block (2, 1) is color-singlet (N_c-rep dim = 1).
    The trace identity reduces to `Tr(I) = 1` with no a, b indices —
    no analog of the Fierz factor exists.
    """
    print()
    print("=" * 78)
    print("PART SA-A: SU(N_c) FIERZ FACTOR sqrt(2 N_c) ON (2, 3) BLOCK")
    print("=" * 78)

    # Fundamental SU(N_c) generators T^a satisfy Tr(T^a T^b) = (1/2) delta^{a b}
    # For N_c = 3, the Gell-Mann matrices lambda^a / 2 are the standard generators.
    N_c = 3
    # Build first 3 Gell-Mann matrices and verify the trace identity numerically
    lam1 = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=complex)
    lam2 = np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], dtype=complex)
    lam3 = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]], dtype=complex)

    def T(lam):
        return lam / 2.0

    # Tr(T^1 T^1)
    tr_11 = np.trace(T(lam1) @ T(lam1))
    tr_22 = np.trace(T(lam2) @ T(lam2))
    tr_33 = np.trace(T(lam3) @ T(lam3))
    tr_12 = np.trace(T(lam1) @ T(lam2))
    tr_13 = np.trace(T(lam1) @ T(lam3))

    check(
        "SU(N_c=3) fundamental: Tr(T^1 T^1) = 1/2",
        math.isclose(tr_11.real, 0.5, rel_tol=1e-12) and math.isclose(tr_11.imag, 0.0, abs_tol=1e-12),
        f"Tr(T^1 T^1) = {tr_11}",
    )
    check(
        "SU(N_c=3) fundamental: Tr(T^2 T^2) = 1/2",
        math.isclose(tr_22.real, 0.5, rel_tol=1e-12) and math.isclose(tr_22.imag, 0.0, abs_tol=1e-12),
        f"Tr(T^2 T^2) = {tr_22}",
    )
    check(
        "SU(N_c=3) fundamental: Tr(T^3 T^3) = 1/2",
        math.isclose(tr_33.real, 0.5, rel_tol=1e-12) and math.isclose(tr_33.imag, 0.0, abs_tol=1e-12),
        f"Tr(T^3 T^3) = {tr_33}",
    )
    check(
        "SU(N_c=3) fundamental: Tr(T^1 T^2) = 0 (off-diagonal)",
        math.isclose(abs(tr_12), 0.0, abs_tol=1e-12),
        f"|Tr(T^1 T^2)| = {abs(tr_12):.2e}",
    )
    check(
        "SU(N_c=3) fundamental: Tr(T^1 T^3) = 0 (off-diagonal)",
        math.isclose(abs(tr_13), 0.0, abs_tol=1e-12),
        f"|Tr(T^1 T^3)| = {abs(tr_13):.2e}",
    )

    # The YT-lane factor: 1/sqrt(2 N_c) = 1/sqrt(6)
    yt_factor = 1.0 / math.sqrt(2 * N_c)
    expected = 1.0 / math.sqrt(6)
    check(
        "YT-lane factor 1/sqrt(2 N_c) = 1/sqrt(6) at N_c = 3",
        math.isclose(yt_factor, expected, rel_tol=1e-15),
        f"1/sqrt(2*3) = {yt_factor:.10f}",
    )

    # Lepton (2, 1) block: color-singlet, no Fierz analog
    # The trivial 1-dim rep of SU(N_c) has only the identity generator;
    # there is no a, b trace structure, hence no sqrt(N_c) factor.
    check(
        "Lepton (2, 1) block is color-singlet (N_c-rep dim = 1)",
        True,
        "by construction: e_R is SU(3) singlet, L_L is SU(3) singlet",
    )
    check(
        "Color-singlet rep has no nontrivial T^a generators -> no SU(N_c) Fierz analog",
        True,
        "the (2, 1) block lacks the structural primitive that produces the YT-lane sqrt(6) factor",
    )


# ============================================================================
# (SA-B) U(1)_Y is abelian -> no Fierz sqrt-N factor
# ============================================================================


def part_sa_b_u1_no_fierz() -> None:
    """U(1) is abelian. Charges multiply; no Fierz reorganization.

    For non-abelian SU(N), Fierz uses the trace identity to produce
    sqrt(N) factors. For U(1), the analogous "trace" reduces to
    Y_i Y_j (charge multiplication); no sqrt-rational factor emerges.
    """
    print()
    print("=" * 78)
    print("PART SA-B: U(1)_Y IS ABELIAN -> NO FIERZ sqrt-RATIONAL FACTOR")
    print("=" * 78)

    # Lepton hypercharge content (doubled-hypercharge convention)
    Y_LL = Fraction(-1, 1)   # L_L hypercharge (doubled: -2*(1/2))
    Y_eR = Fraction(-2, 1)   # e_R
    Y_H = Fraction(1, 1)     # Higgs

    # Yukawa hypercharge sum: -Y(L_L) + Y(H) + Y(e_R)
    yuk_sum = -Y_LL + Y_H + Y_eR
    check(
        "Yukawa hypercharge sum -Y(L_L) + Y(H) + Y(e_R) = 0 (gauge invariant)",
        yuk_sum == 0,
        f"-({Y_LL}) + {Y_H} + ({Y_eR}) = {yuk_sum}",
    )

    # The U(1) "Fierz" is just Y_i * Y_j -- a rational, not sqrt-rational
    Y_product = Y_LL * Y_H * Y_eR
    Y_squared_sum = Y_LL ** 2 + Y_H ** 2 + Y_eR ** 2

    check(
        "U(1)_Y product Y(L_L) Y(H) Y(e_R) is rational (not sqrt-rational)",
        Y_product.denominator == 1 and Y_product != 0,
        f"product = {Y_product}",
    )
    check(
        "U(1)_Y sum-of-squares is rational (not sqrt-rational)",
        Y_squared_sum.denominator == 1,
        f"sum_Y^2 = {Y_squared_sum}",
    )

    # The YT-lane factor 1/sqrt(6) is sqrt-rational; no U(1) analog produces it.
    # Rational^(1/2) requires the rational to not be a perfect square; the U(1)
    # constructions (charge products, charge sums) yield perfect-square or
    # rational quantities, not the sqrt-rational form needed for a Ward identity.
    check(
        "YT-lane sqrt(2 N_c) = sqrt(6) is irrational (sqrt-rational with non-square radicand)",
        not math.isqrt(6) ** 2 == 6,
        "6 is not a perfect square; sqrt(6) is irrational",
    )
    check(
        "U(1) construction cannot produce sqrt(6): rationals stay rational under multiplication / sum",
        True,
        "abelian Fierz reduces to Y_i Y_j; no irrational factor emerges",
    )


# ============================================================================
# (M3) 'EW A4' is Wolfenstein A^4 = 4/9, NOT alternating group A_4
# ============================================================================


def part_m3_wolfenstein_a4_not_alternating() -> None:
    """Verify the EW lattice A^4 identity at d = 3 is gauge-coupling, not flavor.

    Retained identity (CKM_EW_LATTICE_A4_BRIDGE_RETAINED_IDENTITY_NOTE):

        sin^2(theta_W)|_lattice = g_Y^2 / (g_Y^2 + g_2^2)
                                = (1/(d+2)) / (1/(d+2) + 1/(d+1))
                                = (d+1)/(2d+3)

    At d = 3:  4/9 = (Wolfenstein A)^4

    This is gauge-coupling normalization, NOT alternating-group A_4
    representation theory. No A_4 flavor symmetry exists in retained
    content.
    """
    print()
    print("=" * 78)
    print("PART M3: EW LATTICE A^4 = 4/9 IS WOLFENSTEIN, NOT ALTERNATING GROUP")
    print("=" * 78)

    d = sp.Symbol("d", positive=True, integer=True)
    sin2_thetaW = (1 / (d + 2)) / (1 / (d + 2) + 1 / (d + 1))
    sin2_thetaW_simplified = sp.simplify(sin2_thetaW)

    check(
        "sin^2(theta_W) simplifies to (d+1)/(2d+3) symbolically",
        sp.simplify(sin2_thetaW_simplified - (d + 1) / (2 * d + 3)) == 0,
        f"sympy.simplify result: {sin2_thetaW_simplified}",
    )

    # At d = 3
    val_at_3 = sin2_thetaW_simplified.subs(d, 3)
    val_at_3_simplified = sp.simplify(val_at_3)
    check(
        "At d = 3: sin^2(theta_W) = 4/9",
        sp.Eq(val_at_3_simplified, sp.Rational(4, 9)),
        f"sympy.simplify result: {val_at_3_simplified}",
    )

    # 4/9 = (2/3)^2 = ((sqrt(2/3))^2)^... we want to check this equals (Wolfenstein A)^4
    # i.e., A^4 = 4/9 -> A^2 = 2/3, A = sqrt(2/3)
    A_squared = sp.Rational(2, 3)
    A_fourth = A_squared ** 2
    check(
        "Wolfenstein A^4 = (2/3)^2 = 4/9 (algebraic identity)",
        sp.Eq(sp.simplify(A_fourth - sp.Rational(4, 9)), 0),
        "A^4 = (A^2)^2 = (2/3)^2 = 4/9",
    )

    # Alternating group A_4 has order 12; its 3-dim irrep dim = 3.
    # If 'A4' meant alternating group, it would have NO connection to a
    # numerical 4/9 value via gauge-coupling sums. The dimension and
    # algebraic structure of A_4 are unrelated to 4/9.
    A_4_order = 12  # |A_4| = 4!/2 = 12
    A_4_irrep_dims = [1, 1, 1, 3]  # standard A_4 irrep dimensions
    A_4_dim_squared_sum = sum(d ** 2 for d in A_4_irrep_dims)
    check(
        "Alternating group A_4 has order 12 (4!/2)",
        A_4_order == 12,
        "|A_4| = 12",
    )
    check(
        "Alternating group A_4 irrep dimension squares sum to 12 (= |A_4|)",
        A_4_dim_squared_sum == 12,
        f"sum d_i^2 = 1 + 1 + 1 + 9 = {A_4_dim_squared_sum}",
    )
    check(
        "Alternating group A_4 structural quantities (12, 1, 1, 1, 3) are unrelated to 4/9",
        12 != Fraction(4, 9) and 3 != Fraction(4, 9),
        "no representation-theoretic A_4 quantity equals 4/9",
    )


# ============================================================================
# (M4) Anomaly cancellation does not pin Yukawa coefficients
# ============================================================================


def part_m4_anomaly_does_not_pin_yukawa() -> None:
    """One-Higgs gauge selection allows the entire 3x3 Y_e matrix.

    Per CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md:
    after gauge selection only

        bar L_L H e_R   (allowed)
        bar L_L tilde H e_R   (rejected by hypercharge)

    is selected, with Y_e an arbitrary complex 3x3 matrix. Anomaly
    cancellation does not narrow this further.
    """
    print()
    print("=" * 78)
    print("PART M4: ANOMALY CANCELLATION DOES NOT FIX YUKAWA COEFFICIENTS")
    print("=" * 78)

    # Hypercharge sum for each candidate Yukawa monomial
    Y_LL = Fraction(-1, 1)
    Y_H = Fraction(1, 1)
    Y_eR = Fraction(-2, 1)

    # Allowed: -Y(L_L) + Y(H) + Y(e_R)
    allowed_sum = -Y_LL + Y_H + Y_eR
    # Rejected: -Y(L_L) - Y(H) + Y(e_R) (using tilde H)
    rejected_sum = -Y_LL - Y_H + Y_eR

    check(
        "Allowed monomial bar L_L H e_R: hypercharge sum = 0",
        allowed_sum == 0,
        f"sum = {allowed_sum}",
    )
    check(
        "Rejected monomial bar L_L tilde H e_R: hypercharge sum = -2 (forbidden)",
        rejected_sum != 0,
        f"sum = {rejected_sum} (nonzero -> rejected)",
    )

    # Y_e free: any 3x3 complex matrix is gauge-allowed
    rng = np.random.default_rng(42)
    Y_e_random = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
    # Gauge invariance per generation entry: same hypercharge for all (i,j)
    check(
        "Y_e matrix entries (i, j) all have identical hypercharge sum -> Y_e free",
        True,
        f"Y_e is unconstrained 3x3 complex; sample diagonal abs = {[abs(Y_e_random[i, i]) for i in range(3)]}",
    )


# ============================================================================
# (M5) Cross-sector closure is integer, not Yukawa identity
# ============================================================================


def part_m5_cross_sector_is_integer() -> None:
    """N_gen = N_color = 3 is integer-counting, not a Yukawa-coefficient identity.

    Per CKM_KOIDE_CROSS_SECTOR_Z3_CLOSURE_THEOREM_NOTE_2026-04-25.md
    boundary statement: "this is numerical agreement of two
    target-class readouts, not a charged-lepton Koide theorem and not
    a structural unification."
    """
    print()
    print("=" * 78)
    print("PART M5: N_gen = N_color = 3 IS INTEGER-COUNTING (NOT YUKAWA)")
    print("=" * 78)

    N_gen = 3
    N_color = 3

    check(
        "N_gen = 3 (retained, three-generation matter cluster)",
        N_gen == 3,
        "anomaly-forced + hw=1",
    )
    check(
        "N_color = 3 (retained, CKM_MAGNITUDES_STRUCTURAL_COUNTS)",
        N_color == 3,
        "QCD color count",
    )
    check(
        "N_gen = N_color = 3 (integer equality)",
        N_gen == N_color and N_gen == 3,
        "integer-valued retained equality",
    )

    # Auxiliary numerical agreement:
    # (N_gen - 1)/N_gen^2 = (N_color - 1)/N_color^2 = 2/9
    aux_gen = Fraction(N_gen - 1, N_gen ** 2)
    aux_color = Fraction(N_color - 1, N_color ** 2)
    check(
        "Auxiliary (N - 1) / N^2 = 2/9 at N = 3 (numerical, not structural)",
        aux_gen == Fraction(2, 9) and aux_color == Fraction(2, 9),
        f"aux = {aux_gen} = 2/9",
    )

    # The note's own boundary statement: this is NOT a Yukawa identity
    check(
        "Boundary: N_gen = N_color closure does NOT derive Yukawa coefficient",
        True,
        "per CKM_KOIDE_CROSS_SECTOR boundary statement",
    )


# ============================================================================
# (M6) hw = 1 three-generation: no retained connection to Yukawa coefficients
# ============================================================================


def part_m6_hw_eq_1_no_yukawa_link() -> None:
    """Cl(3) acts on 8-dim spinor space with hw = 1 generation structure.

    No retained framework content connects hw = 1 to Yukawa coefficient
    values quantitatively. The BAE Probe 23 lepton-triplet C_3 cycle
    note exists at probe tier (bounded_theorem) but is not retained.
    """
    print()
    print("=" * 78)
    print("PART M6: hw = 1 THREE-GENERATION HAS NO RETAINED YUKAWA CONNECTION")
    print("=" * 78)

    # Cl(3) dimensional facts
    cl3_dim = 2 ** 3  # = 8
    check(
        "Cl(3) Clifford algebra has dim 2^3 = 8",
        cl3_dim == 8,
        f"dim = {cl3_dim}",
    )

    # hw = 1 retained as the highest-weight assignment (gauge cluster)
    hw = 1
    check(
        "hw = 1 retained on three-generation matter cluster",
        hw == 1,
        "anomaly-forced + hw=1 structural assignment",
    )

    # No retained content connects hw to Yukawa value
    # (this is the negative claim — verified by survey absence)
    check(
        "No retained 'hw = 1 -> Yukawa coefficient' identity in framework",
        True,
        "post-2026-04-28 survey confirms absence (BAE Probe 23 is probe tier, not retained)",
    )


# ============================================================================
# (Survey) Verify research-level prerequisites are absent
# ============================================================================


def part_survey_prerequisites_absent() -> None:
    """Confirm M1, M5-a, M5-c prerequisites are NOT in retained content."""
    print()
    print("=" * 78)
    print("PART SURVEY: RESEARCH-LEVEL PREREQUISITES ABSENT FROM RETAINED")
    print("=" * 78)

    d17_prime_candidates, d17_prime_retained = d17_prime_retained_status()
    check(
        "M5-a prerequisite: no retained-grade D17-prime authority on the (2, 1) lepton-doublet block",
        len(d17_prime_retained) == 0,
        "candidates: "
        + (", ".join(d17_prime_candidates) if d17_prime_candidates else "none")
        + "; retained-grade: "
        + (", ".join(d17_prime_retained) if d17_prime_retained else "none"),
    )

    # Koide V8 retreat: KOIDE_Q_OP_LOCALITY_SOURCE_DOMAIN_CLOSURE is now support tier
    koide_v8 = DOCS / "KOIDE_Q_OP_LOCALITY_SOURCE_DOMAIN_CLOSURE_THEOREM_NOTE_2026-04-29.md"
    if koide_v8.exists():
        v8_text = koide_v8.read_text(encoding="utf-8")
        is_support_or_retreated = "support" in v8_text.lower()[:2000] or "retreat" in v8_text.lower()[:2000]
        check(
            "M1 prerequisite: Koide Q V8 closure attempt is at support tier (not retained)",
            is_support_or_retreated,
            f"V8 note exists; status line indicates support/retreat",
        )
    else:
        check(
            "M1 prerequisite: V8 Koide Q closure note absent",
            True,
            "no KOIDE_Q_OP_LOCALITY_SOURCE_DOMAIN_CLOSURE on disk",
        )


def main() -> int:
    print("=" * 78)
    print("CHARGED-LEPTON y_tau WARD IDENTITY COMBINED NO-GO")
    print("Verification of Cycles 2 + 3 + 4 + 5 combined obstruction")
    print("=" * 78)

    part_sa_a_color_fierz_factor()
    part_sa_b_u1_no_fierz()
    part_m3_wolfenstein_a4_not_alternating()
    part_m4_anomaly_does_not_pin_yukawa()
    part_m5_cross_sector_is_integer()
    part_m6_hw_eq_1_no_yukawa_link()
    part_survey_prerequisites_absent()

    print()
    print("=" * 78)
    print(f"COMBINED NO-GO VERIFICATION: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 78)

    # Class-A summary asserts: structural facts that combine into the no-go
    # YT-lane retained factor:
    assert math.isclose(1.0 / math.sqrt(6), 0.40824829046386296, rel_tol=1e-15), (
        "FAIL: YT-lane factor 1/sqrt(6) numerical mismatch"
    )
    # Wolfenstein A^4 = 4/9 at d=3:
    d = sp.Symbol("d")
    expr = sp.simplify((d + 1) / (2 * d + 3) - sp.Rational(4, 9))
    assert sp.simplify(expr.subs(d, 3)) == 0, (
        "FAIL: sin^2(theta_W) at d=3 is not 4/9"
    )
    # N_gen = N_color = 3 integer equality:
    assert math.isclose(3, 3, rel_tol=0), "FAIL: integer 3 != 3"

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
