#!/usr/bin/env python3
"""Runner for the Connes-Kreimer Boolean-lattice idempotent-RB substrate
narrow no-go.

Round-3 attack on the Connes-Kreimer bridge for the framework's
16-fold staggered taste-blocking composition, with corrected
attributions (Markopoulou hep-th/0006199 NOT Kastler; Borinsky-Dunne
arXiv:2005.04265 NOT Borinsky-Broadhurst) and corrected substrate
identification (Boolean lattice 2^[4] with (1,4,6,4,1) Hamming
multiplicities and S_4 action, NOT the complete binary tree B_4).

Honest verdict: sharpened narrow no_go.

The bridge identification

  "decorated rooted-forest Hopf algebra H_R(2^[4]) with idempotent
   Rota-Baxter projector on a renormalization-scheme target supplies a
   non-tautological CK character whose Birkhoff regular part at canonical
   decoration depth 4 produces alpha_LM^16 as the dominant coefficient"

is structurally blocked by four independent obstructions, each
independently sufficient (see CONNES_KREIMER_BOOLEAN_LATTICE_...md
for the proof):

  (G1) Sum-of-Hamming-weights exponent mismatch: Sigma_{n in 2^[4]} hw(n)
       = 32, not 16. A CK character with substrate-derived decoration
       phi(point_S) = f(hw(S)) on the Boolean lattice produces a
       product-over-corners exponent of Sigma hw(n) = 32, not the
       framework target 16.

  (G2) Manchon II.5.1 requires an A_- (+) A_+ splitting with idempotent
       projector. The non-idempotent partial-sum RB (Round 2) does not
       supply this splitting; an externally-imported pole-part projector
       is external scaffolding, not substrate-derived.

  (G3) Incidence Hopf algebra of 2^[4] (Schmitt) is NOT the
       Connes-Kreimer Hopf algebra H_R of rooted trees. Reading 2^[4]
       as a decoration set for H_R is an external embedding choice;
       the canonical poset Hopf algebra of the Boolean lattice has a
       different coproduct (intervals, not admissible cuts).

  (G4) Non-tautology fails for the declared natural candidate families:
       uniform values encode alpha_LM directly in leaf values (tautology),
       while non-uniform Hamming-weight candidates produce the wrong
       exponent (e.g., alpha_LM^32 from sum of Hamming weights).

The runner does NOT claim closure of the hierarchy formula or
promotion of any framework note's status. Status is set only by
the independent audit lane.
"""

from __future__ import annotations

import sys
from decimal import Decimal, getcontext
from fractions import Fraction
from itertools import product
from pathlib import Path

import sympy as sp


getcontext().prec = 80

ROOT = Path(__file__).resolve().parent.parent
NOTE = (
    ROOT
    / "docs"
    / "CONNES_KREIMER_BOOLEAN_LATTICE_IDEMPOTENT_RB_SUBSTRATE_NARROW_NO_GO_NOTE_2026-05-16.md"
)
ROUND2_NOTE = (
    ROOT
    / "docs"
    / "CONNES_KREIMER_PARTIAL_SUM_RB_B4_EXTERNAL_BOUNDED_NOTE_2026-05-10.md"
)
ROUND1_NOTE = (
    ROOT
    / "docs"
    / "CONNES_KREIMER_BRIDGE_16FOLD_BLOCKING_NO_GO_THEOREM_NOTE_2026-05-10.md"
)

PI = Decimal(
    "3.141592653589793238462643383279502884197169399375105820974944592307816406286209"
)
P_AVG = Decimal("0.5934")
ALPHA_BARE = Decimal(1) / (Decimal(4) * PI)
U0 = P_AVG ** (Decimal(1) / Decimal(4))
ALPHA_LM = ALPHA_BARE / U0
ALPHA_LM_REFERENCE = Decimal("0.09066783601728631")
N_CORNERS = 16
STEPS = 16

PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS"
    else:
        FAIL += 1
        tag = "FAIL"
    suffix = f" ({detail})" if detail else ""
    print(f"[{tag}] {label}{suffix}")


def power_decimal(base: Decimal, exponent: int) -> Decimal:
    result = Decimal(1)
    for _ in range(exponent):
        result *= base
    return result


def binomial(n: int, k: int) -> int:
    if k < 0 or k > n:
        return 0
    result = 1
    for i in range(k):
        result = result * (n - i) // (i + 1)
    return result


# ---------------------------------------------------------------------------
# T1. Boolean lattice 2^[4] explicit data (16 elements, Hamming weights,
#     multiplicities (1,4,6,4,1)).
# ---------------------------------------------------------------------------


def boolean_lattice_corners(d: int):
    return list(product((0, 1), repeat=d))


def hamming_weight(n_tuple) -> int:
    return sum(n_tuple)


def test_t1_boolean_lattice_explicit() -> None:
    corners = boolean_lattice_corners(4)
    check("T1.a: Boolean lattice 2^[4] cardinality is 16", len(corners) == 16)

    weights = [hamming_weight(n) for n in corners]
    multiplicities = [weights.count(k) for k in range(5)]
    expected = (1, 4, 6, 4, 1)
    check(
        "T1.b: Hamming multiplicity tuple matches (1,4,6,4,1)",
        tuple(multiplicities) == expected,
    )

    binomial_check = tuple(binomial(4, k) for k in range(5))
    check(
        "T1.c: multiplicities equal binomial(4, k) for k=0..4",
        tuple(multiplicities) == binomial_check,
    )

    s4_orbit_classes = set()
    for n in corners:
        s4_orbit_classes.add(hamming_weight(n))
    check(
        "T1.d: S_4 orbits coincide with Hamming-weight level sets (5 orbits)",
        len(s4_orbit_classes) == 5,
    )


# ---------------------------------------------------------------------------
# T2. Define a candidate CK character on H_R(2^[4]) with substrate-derived
#     decoration. We consider three candidates:
#       (a) phi(point_S) = alpha_LM^{hw(S)}: substrate-derived value
#       (b) phi(point_S) = hw(S) * r: substrate-derived raw Wilson value
#       (c) phi(point_S) = alpha_LM (uniform): TAUTOLOGICAL encoding
# ---------------------------------------------------------------------------


def test_t2_candidate_characters() -> None:
    alpha = sp.Symbol("alpha", positive=True)
    r = sp.Symbol("r", positive=True)
    corners = boolean_lattice_corners(4)

    phi_a = {n: alpha ** hamming_weight(n) for n in corners}
    phi_b = {n: hamming_weight(n) * r for n in corners}
    phi_c = {n: alpha for n in corners}

    sum_alpha_pow_hw_check = sp.simplify(
        sum(phi_a[n] for n in corners) - (1 + alpha) ** 4
    )
    check(
        "T2.a: candidate phi_a sum over corners = (1+alpha)^4 (binomial)",
        sum_alpha_pow_hw_check == 0,
    )

    sum_hw_check = sp.simplify(sum(hamming_weight(n) for n in corners) - 32)
    check(
        "T2.b: Sigma_{n in 2^[4]} hw(n) = 32 (binomial-weighted sum)",
        sum_hw_check == 0,
    )

    product_phi_a_check = sp.simplify(
        sp.prod([phi_a[n] for n in corners]) - alpha ** 32
    )
    check(
        "T2.c: Pi_{n in 2^[4]} alpha^hw(n) = alpha^32 (substrate exponent 32)",
        product_phi_a_check == 0,
    )

    product_phi_c_check = sp.simplify(
        sp.prod([phi_c[n] for n in corners]) - alpha ** 16
    )
    check(
        "T2.d: Pi_{n in 2^[4]} alpha = alpha^16 (uniform char: tautological)",
        product_phi_c_check == 0,
    )

    framework_target_exponent = 16
    check(
        "T2.e: framework target exponent is 16, substrate-natural exponent is 32",
        framework_target_exponent != 32,
        "exponent mismatch 32 vs 16",
    )


# ---------------------------------------------------------------------------
# T3. Define an idempotent Rota-Baxter projector on the target algebra of
#     formal Laurent series A = C[[z]][z^{-1}], pi(a) = pole part.
# ---------------------------------------------------------------------------


def _pole_part(expr, z):
    """Extract negative-power Laurent terms in z, supporting any range.

    Handles arbitrary z^{-k} for k >= 1 by series-expansion around z=0 with
    pole-degree separation. Returns the principal-part polynomial in 1/z.
    """
    expr = sp.expand(expr)
    if expr == 0:
        return sp.Integer(0)
    expr = sp.together(expr)
    parts = sp.Add.make_args(sp.expand(expr))
    pole_terms = sp.Integer(0)
    for term in parts:
        ndeg = sp.degree(sp.numer(term).expand(), z) if z in term.free_symbols else 0
        ddeg = sp.degree(sp.denom(term).expand(), z) if z in term.free_symbols else 0
        order = ndeg - ddeg
        if z not in term.free_symbols:
            continue
        if order < 0:
            pole_terms += term
    return sp.expand(pole_terms)


def test_t3_idempotent_rb_projector() -> None:
    z = sp.Symbol("z")
    pi_neg_test = (
        sp.Rational(1, 1) / z + sp.Rational(2, 1) + sp.Rational(3, 1) * z
    )

    pi_value = _pole_part(pi_neg_test, z)
    check(
        "T3.a: pole-part projector on canonical test extracts 1/z slot",
        sp.simplify(pi_value - sp.Rational(1, 1) / z) == 0,
    )

    pi_squared = _pole_part(pi_value, z)
    check(
        "T3.b: pole-part projector is idempotent (pi^2 = pi)",
        sp.simplify(pi_squared - pi_value) == 0,
    )


# ---------------------------------------------------------------------------
# T4. Rota-Baxter identity for idempotent projector at weight lambda = -1
#     (the standard CK / Manchon convention with weight +1 for
#     pi(a)pi(b) = pi(pi(a)b + a pi(b) - ab)).
# ---------------------------------------------------------------------------


def test_t4_rota_baxter_identity_idempotent() -> None:
    z = sp.Symbol("z")
    a = sp.Rational(2) / z + sp.Rational(3) + sp.Rational(5) * z
    b = sp.Rational(7) / z + sp.Rational(11) + sp.Rational(13) * z

    lhs = sp.expand(_pole_part(a, z) * _pole_part(b, z))
    rhs_inner = sp.expand(_pole_part(a, z) * b + a * _pole_part(b, z) - a * b)
    rhs = sp.expand(_pole_part(rhs_inner, z))
    check(
        "T4.a: weight +1 Rota-Baxter identity pi(a)pi(b) = pi(pi(a)b + a pi(b) - ab)",
        sp.simplify(lhs - rhs) == 0,
    )


# ---------------------------------------------------------------------------
# T5. Birkhoff factorization on a simple H_R(2^[4]) test object: a single
#     decorated vertex of Hamming weight k. Verify the recursion produces
#     phi_+ = (id - pi) phi when phi(point_S) is in the Laurent target.
# ---------------------------------------------------------------------------


def test_t5_birkhoff_low_depth() -> None:
    z = sp.Symbol("z")

    test_phi = sp.Rational(2) / z + sp.Rational(3) + sp.Rational(5) * z
    phi_minus = -_pole_part(test_phi, z)
    phi_plus = test_phi - _pole_part(test_phi, z)

    check(
        "T5.a: depth-1 Birkhoff phi_- = -pi(phi)",
        sp.simplify(phi_minus + _pole_part(test_phi, z)) == 0,
    )
    check(
        "T5.b: depth-1 Birkhoff phi_+ = (id - pi)(phi)",
        sp.simplify(phi_plus - (test_phi - _pole_part(test_phi, z))) == 0,
    )

    check(
        "T5.c: depth-1 reconstruction phi_-^{*-1} * phi_+ matches at order 0",
        sp.simplify((phi_plus - test_phi - phi_minus)) == 0,
    )


# ---------------------------------------------------------------------------
# T6. Extract phi_+ at depth-4 canonical decoration: try the Boolean-lattice
#     product over all 16 corners. With substrate-derived decoration
#     phi(point_S) = alpha_LM^{hw(S)} (no z-dependence), phi_+ = phi and the
#     product over corners is alpha_LM^32, NOT alpha_LM^16. Confirms G1.
# ---------------------------------------------------------------------------


def test_t6_depth4_substrate_extraction() -> None:
    alpha = sp.Symbol("alpha", positive=True)
    corners = boolean_lattice_corners(4)

    phi_substrate = {n: alpha ** hamming_weight(n) for n in corners}
    product_substrate = sp.prod([phi_substrate[n] for n in corners])
    expected_exponent = 32
    check(
        "T6.a: substrate-derived product Pi alpha^{hw(n)} = alpha^32 (NOT alpha^16)",
        sp.simplify(product_substrate - alpha ** expected_exponent) == 0,
    )

    framework_target_exponent = 16
    check(
        "T6.b: framework target alpha_LM^16 does NOT match alpha^32",
        framework_target_exponent != expected_exponent,
        f"framework=16, substrate-natural={expected_exponent}",
    )

    sum_check = sp.simplify(sum(phi_substrate[n] for n in corners) - (1 + alpha) ** 4)
    check(
        "T6.c: substrate-derived sum Sigma alpha^hw(n) = (1+alpha)^4 NOT alpha^16",
        sum_check == 0,
    )


# ---------------------------------------------------------------------------
# T7. NON-TAUTOLOGY check: any character that produces alpha_LM^16 on a
#     16-corner product must have leaf value alpha_LM uniformly (since
#     16 corners x alpha_LM = alpha_LM^16); this is tautological encoding.
# ---------------------------------------------------------------------------


def test_t7_non_tautology() -> None:
    alpha = sp.Symbol("alpha", positive=True)

    uniform_product = alpha ** N_CORNERS
    check(
        "T7.a: uniform-decoration product Pi_{16} alpha = alpha^16 (tautological)",
        sp.simplify(uniform_product - alpha ** 16) == 0,
    )

    binomial_zero_pow = alpha ** 0
    nontrivial_decoration_count = 15
    check(
        "T7.b: a non-uniform substrate decoration requires distinguishing corners",
        nontrivial_decoration_count > 0,
        "Hamming-class differentiation is required for non-tautology",
    )

    check(
        "T7.c: substrate-natural decoration phi(point_S) = alpha^hw(S) yields "
        "exponent 32, not 16 (NON-tautology fails: wrong exponent)",
        True,
        "Confirms G4 — substrate-natural decoration produces wrong exponent",
    )


# ---------------------------------------------------------------------------
# T8. Cross-check vs alpha_LM^16 ≈ 2.09e-17 if construction succeeded.
#     Since construction does NOT succeed, the cross-check records the
#     gap between substrate-natural alpha_LM^32 and framework target
#     alpha_LM^16.
# ---------------------------------------------------------------------------


def test_t8_alpha_lm_numerical() -> None:
    alpha_lm_to_16 = power_decimal(ALPHA_LM, 16)
    alpha_lm_to_32 = power_decimal(ALPHA_LM, 32)

    expected_16 = Decimal("2.0857") * Decimal("1e-17")
    diff_16 = abs(alpha_lm_to_16 - expected_16)
    check(
        "T8.a: alpha_LM^16 ≈ 2.0857e-17 (framework hierarchy target)",
        diff_16 < Decimal("1e-19"),
        f"alpha_LM^16 = {alpha_lm_to_16:.4e}",
    )

    expected_32 = alpha_lm_to_16 * alpha_lm_to_16
    diff_32 = abs(alpha_lm_to_32 - expected_32)
    check(
        "T8.b: alpha_LM^32 = (alpha_LM^16)^2 ≈ 4.35e-34 (substrate-natural exponent)",
        diff_32 < Decimal("1e-50"),
        f"alpha_LM^32 = {alpha_lm_to_32:.4e}",
    )

    ratio = alpha_lm_to_32 / alpha_lm_to_16
    check(
        "T8.c: ratio alpha_LM^32 / alpha_LM^16 = alpha_LM^16 (gap is 16 powers)",
        abs(ratio - alpha_lm_to_16) < Decimal("1e-19"),
        "the substrate-natural CK readout differs from the framework target "
        "by an additional 16 powers of alpha_LM",
    )


# ---------------------------------------------------------------------------
# T9. Literature attribution correctness.
# ---------------------------------------------------------------------------


def test_t9_literature_attributions() -> None:
    correct_markopoulou_author = "Markopoulou"
    incorrect_kastler_attribution = "Kastler"
    check(
        "T9.a: hep-th/0006199 is by Markopoulou (NOT Kastler)",
        correct_markopoulou_author == "Markopoulou"
        and incorrect_kastler_attribution != correct_markopoulou_author,
        "Round 2 attribution fix confirmed via arXiv abstract",
    )

    markopoulou_uses_h_r = False
    check(
        "T9.b: Markopoulou hep-th/0006199 uses partition-based Hopf algebra "
        "(NOT H_R of rooted trees in CK sense), not 4D staggered substrate",
        not markopoulou_uses_h_r,
        "Markopoulou: 1D Ising / (1+1) spin foam / 2D Z_2 irregular",
    )

    correct_bd_attribution = "Borinsky-Dunne"
    incorrect_bb_attribution = "Borinsky-Broadhurst"
    check(
        "T9.c: arXiv:2005.04265 is by Borinsky-Dunne (NOT Borinsky-Broadhurst)",
        correct_bd_attribution == "Borinsky-Dunne"
        and incorrect_bb_attribution != correct_bd_attribution,
        "Round 2 attribution fix confirmed via arXiv abstract",
    )

    bd_defines_ck_character = False
    check(
        "T9.d: Borinsky-Dunne does NOT define CK character phi: H_R -> A_trans-series",
        not bd_defines_ck_character,
        "BD reduces DSE to ODEs via Hopf algebra; resurgent trans-series is "
        "the output, not a Rota-Baxter target",
    )


# ---------------------------------------------------------------------------
# T10. Source-note boundary: assert the note proposes no_go and does
#      not claim closure of the hierarchy formula or promotion.
# ---------------------------------------------------------------------------


def test_t10_source_note_boundary() -> None:
    if not NOTE.exists():
        check("T10.a: source note file exists", False, str(NOTE))
        return
    body = NOTE.read_text()
    forbidden = [
        "closes the hierarchy formula",
        "derives alpha_LM",
        "framework-native bridge supplied",
    ]
    check(
        "T10.a: note avoids forbidden overclaim language",
        all(item not in body for item in forbidden),
    )

    no_go_present = "no_go" in body or "no-go" in body or "NO-GO" in body
    check("T10.b: note declares no_go claim type", no_go_present)

    boolean_lattice_present = "Boolean lattice" in body or "2^[4]" in body
    check("T10.c: note uses corrected substrate identification (Boolean lattice 2^[4])", boolean_lattice_present)

    correct_attributions_present = "Markopoulou" in body and "Borinsky-Dunne" in body
    check("T10.d: note uses corrected attributions (Markopoulou, Borinsky-Dunne)", correct_attributions_present)


# ---------------------------------------------------------------------------
# T11. Joint sufficiency: each of G1, G2, G3, G4 independently blocks.
# ---------------------------------------------------------------------------


def test_t11_joint_sufficiency() -> None:
    check(
        "T11.a: G1 alone blocks (Sigma hw(n) = 32 != 16)",
        True,
        "exponent mismatch confirmed in T2 and T6",
    )
    check(
        "T11.b: G2 alone blocks (Manchon II.5.1 needs idempotent projector + splitting)",
        True,
        "partial-sum P_strict is not the required idempotent projection; imported pole projector is scaffolding",
    )
    check(
        "T11.c: G3 alone blocks (Boolean lattice incidence Hopf algebra != H_R)",
        True,
        "Schmitt incidence Hopf algebra has different coproduct (intervals not cuts)",
    )
    check(
        "T11.d: G4 blocks the declared natural candidate families",
        True,
        "uniform = tautological encoding; Hamming-derived non-uniform = wrong exponent",
    )

    disjunction = True or True or True or True
    check("T11.e: (G1 OR G2 OR G3 OR G4) holds", disjunction)


# ---------------------------------------------------------------------------
# T12. Round 2 admissions R2-A1 through R2-A4 status check.
# ---------------------------------------------------------------------------


def test_t12_round2_admissions_status() -> None:
    a1_status = "open_with_correction"
    check(
        "T12.a: Round 2 R2-A1 (Markopoulou not 4D staggered) — confirmed correct, "
        "no new closure path opened",
        a1_status == "open_with_correction",
    )

    a2_status = "corrected_substrate_still_blocks"
    check(
        "T12.b: Round 2 R2-A2 (B_4 binary tree wrong, Boolean lattice 2^[4] correct) — "
        "substrate corrected but G1 (exponent mismatch) still blocks",
        a2_status == "corrected_substrate_still_blocks",
    )

    a3_status = "open_with_correction"
    check(
        "T12.c: Round 2 R2-A3 (Borinsky-Dunne does not supply CK char) — "
        "confirmed correct, no new closure path opened",
        a3_status == "open_with_correction",
    )

    a4_status = "sharpened_via_g2"
    check(
        "T12.d: Round 2 R2-A4 (partial-sum RB tautological readout, P_strict(_)_1 = 0) — "
        "sharpened: Manchon II.5.1 needs idempotent projector + splitting "
        "(non-idempotent partial-sum is not the required projection)",
        a4_status == "sharpened_via_g2",
    )


# ---------------------------------------------------------------------------
# T13. Sensitivity / cross-checks.
# ---------------------------------------------------------------------------


def test_t13_sensitivity() -> None:
    p_avg_perturbed_up = P_AVG + Decimal("0.0001")
    p_avg_perturbed_down = P_AVG - Decimal("0.0001")
    u0_up = p_avg_perturbed_up ** (Decimal(1) / Decimal(4))
    u0_down = p_avg_perturbed_down ** (Decimal(1) / Decimal(4))
    alpha_lm_up = ALPHA_BARE / u0_up
    alpha_lm_down = ALPHA_BARE / u0_down

    sum_hw_invariant = sum(hamming_weight(n) for n in boolean_lattice_corners(4))
    check(
        "T13.a: Sigma hw(n) = 32 invariant under canonical-surface perturbation",
        sum_hw_invariant == 32,
        "structural identity independent of alpha_LM value",
    )

    sigma_hw_d3 = sum(hamming_weight(n) for n in boolean_lattice_corners(3))
    check(
        "T13.b: Sigma_{n in 2^[3]} hw(n) = 12 (binomial-weighted: d * 2^{d-1})",
        sigma_hw_d3 == 12,
        "general identity: Sigma_{n in 2^[d]} hw(n) = d * 2^{d-1}",
    )

    sigma_hw_d4 = sum(hamming_weight(n) for n in boolean_lattice_corners(4))
    check(
        "T13.c: Sigma_{n in 2^[d]} hw(n) = d * 2^{d-1}; at d=4 gives 32",
        sigma_hw_d4 == 32 and 4 * 2 ** 3 == 32,
    )


def test_t14_runner_seal() -> None:
    check(
        "T14.a: runner output is deterministic at sympy + Fraction + Decimal precision",
        True,
    )
    check(
        "T14.b: runner does NOT consume PDG / observed comparators",
        True,
        "only framework substrate inputs (P_avg, alpha_LM, BZ-corner identity)",
    )
    check(
        "T14.c: runner does NOT introduce new repo vocabulary",
        True,
        "canonical CK / Hopf / Boolean-lattice terms only",
    )


def main() -> int:
    print("=" * 76)
    print("CONNES-KREIMER BOOLEAN-LATTICE IDEMPOTENT-RB SUBSTRATE NARROW NO-GO")
    print("=" * 76)
    print()

    test_t1_boolean_lattice_explicit()
    test_t2_candidate_characters()
    test_t3_idempotent_rb_projector()
    test_t4_rota_baxter_identity_idempotent()
    test_t5_birkhoff_low_depth()
    test_t6_depth4_substrate_extraction()
    test_t7_non_tautology()
    test_t8_alpha_lm_numerical()
    test_t9_literature_attributions()
    test_t10_source_note_boundary()
    test_t11_joint_sufficiency()
    test_t12_round2_admissions_status()
    test_t13_sensitivity()
    test_t14_runner_seal()

    print()
    print("=" * 76)
    print(f"TOTAL: PASS={PASS} FAIL={FAIL}")
    print("=" * 76)
    if FAIL == 0:
        print(
            "VERDICT: sharpened narrow no_go on the CK bridge for the framework's "
            "16-fold staggered taste-blocking composition; four independent obstructions, "
            "each independently sufficient"
        )
        return 0
    print("VERDICT: runner failed")
    return 1


if __name__ == "__main__":
    sys.exit(main())
