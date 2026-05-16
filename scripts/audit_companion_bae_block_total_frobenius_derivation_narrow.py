#!/usr/bin/env python3
"""Exact-symbolic audit-companion runner for the BAE block-total-Frobenius
derivation narrow theorem note
`BAE_BLOCK_TOTAL_FROBENIUS_DERIVATION_NARROW_THEOREM_NOTE_2026-05-16.md`.

The parent narrow note's load-bearing content is the algebraic
identification, conditional on the F1 canonicality hypothesis, of the
F1-extremum locus on `Herm_circ(3)` with the BAE locus:

  E_+(H)    = 3 a^2,                                                      (E+)
  E_perp(H) = 6 |b|^2,                                                    (Eperp)
  F1(H)     = log E_+ + log E_perp,                                       (F1)

GIVEN H_F1 (F1 is canonical on Herm_circ(3); NOT discharged), the
F1-extremum locus under E_+ + E_perp = const is

  E_+ = E_perp = E_tot/2  <=>  a^2 = 2 |b|^2  <=>  kappa = 2,             (T1)
  kappa = 2               <=>  |b|^2 / a^2 = 1/2  (= BAE).                (T2)

The locus identification is then

  { (a,b) : F1-critical } = BAE.                                          (LOCUS)

Hessian sign at the critical point:

  d^2 F1 / dE_+^2     = -1/E_+^2   = -4/E_tot^2  < 0,                     (T3)
  d^2 F1 / dE_perp^2  = -1/E_perp^2 = -4/E_tot^2 < 0.

This Pattern A audit-companion runner adds a sympy-based exact-symbolic
verification:

  (a) treats (a, b) as free symbols with a real, b complex;
  (b) constructs the circulant H = a I + b C + b_bar C^2 explicitly;
  (c) verifies E_+ = 3 a^2 and E_perp = 6 |b|^2 parametrically;
  (d) verifies the F1 Lagrange extremum at E_+ = E_perp = E_tot/2;
  (e) verifies kappa = 2 <=> |b|^2/a^2 = 1/2 algebraically;
  (f) verifies the F1 Hessian is strictly negative-definite on the
      constraint surface at the critical point;
  (g) verifies the LOCUS set equality on sample points (on-locus and
      off-locus);
  (h) counterfactual: F3 = log E_+ + 2 log E_perp has critical point at
      kappa = 1 (NOT BAE), demonstrating that this narrow theorem does
      NOT discharge F1-vs-F3 selection;
  (i) review-hygiene checks on the note (vocabulary, citations, claim
      type, no-new-axiom, no-new-vocabulary).

Companion role: not a new claim row, not a new source note, no status
promotion. Provides audit-friendly evidence that the parent's
load-bearing one-step algebraic chain holds at exact symbolic precision
and that the F1 canonicality hypothesis remains explicitly undischarged.
"""

from pathlib import Path
import sys

try:
    import sympy
    from sympy import (
        Rational,
        Symbol,
        expand,
        log,
        sqrt,
        simplify,
        symbols,
        conjugate,
        re,
        I,
        Matrix,
    )
except ImportError:
    print("FAIL: sympy required for exact algebra")
    sys.exit(1)


PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS (A)"
    else:
        FAIL += 1
        tag = "FAIL (A)"
    suffix = f"  ({detail})" if detail else ""
    print(f"  [{tag}] {label}{suffix}")


def section(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


def main() -> int:
    print("=" * 88)
    print("Audit companion (exact-symbolic) for")
    print("BAE_BLOCK_TOTAL_FROBENIUS_DERIVATION_NARROW_THEOREM_NOTE_2026-05-16")
    print("Goal: sympy-symbolic verification that F1-extremum locus = BAE locus")
    print("on Herm_circ(3), conditional on F1 canonicality hypothesis.")
    print("=" * 88)

    # ---------------------------------------------------------------------
    section("Part 0: symbolic setup")
    # ---------------------------------------------------------------------

    a = Symbol("a", real=True)
    b_re = Symbol("b_re", real=True)
    b_im = Symbol("b_im", real=True)
    b = b_re + I * b_im
    b_bar = b_re - I * b_im
    abs_b_sq = b_re ** 2 + b_im ** 2  # |b|^2

    # 3x3 cyclic permutation matrix C: C^3 = I
    C = Matrix([
        [0, 1, 0],
        [0, 0, 1],
        [1, 0, 0],
    ])
    C2 = C * C
    I3 = Matrix.eye(3)

    H = a * I3 + b * C + b_bar * C2
    H_simplified = sympy.simplify(H)

    print("  H = a I + b C + bbar C^2 =")
    print(H_simplified)
    check(
        "C^3 = I (cyclic identity)",
        sympy.simplify(C ** 3 - I3) == sympy.zeros(3, 3),
        detail="C generates the cyclic group of order 3",
    )
    check(
        "H is Hermitian (i.e. H^dagger = H)",
        sympy.simplify(H.H - H) == sympy.zeros(3, 3),
        detail="circulant Hermitian on a real + complex pair (b, bbar)",
    )

    # ---------------------------------------------------------------------
    section("Part 1: block-total Frobenius identities (E+) and (Eperp)")
    # ---------------------------------------------------------------------

    # pi_+(H) = (tr H / 3) I.  On H, tr(H) = 3a (since tr(C) = tr(C^2) = 0).
    tr_H = sympy.trace(H)
    check(
        "tr(H) = 3a (cyclic shifts have zero trace)",
        sympy.simplify(tr_H - 3 * a) == 0,
        detail=f"tr(H) = {sympy.simplify(tr_H)}",
    )

    pi_plus_H = (tr_H / 3) * I3
    pi_perp_H = H - pi_plus_H

    # E_+ = ||pi_+(H)||_F^2 = tr(pi_+^H pi_+)
    E_plus_raw = sympy.simplify((pi_plus_H.H * pi_plus_H).trace())
    # Force real reduction
    E_plus = sympy.simplify(sympy.expand(sympy.re(E_plus_raw)) + 0)
    E_plus_target = 3 * a ** 2
    check(
        "(E+): E_+(H) = ||pi_+(H)||_F^2 = 3 a^2",
        sympy.simplify(E_plus - E_plus_target) == 0,
        detail=f"E_+ - 3a^2 = {sympy.simplify(E_plus - E_plus_target)}",
    )

    # E_perp = ||pi_perp(H)||_F^2 = tr(pi_perp^H pi_perp)
    E_perp_raw = sympy.simplify((pi_perp_H.H * pi_perp_H).trace())
    E_perp = sympy.simplify(sympy.expand(sympy.re(E_perp_raw)) + 0)
    E_perp_target = 6 * abs_b_sq
    check(
        "(Eperp): E_perp(H) = ||pi_perp(H)||_F^2 = 6 |b|^2",
        sympy.simplify(E_perp - E_perp_target) == 0,
        detail=f"E_perp - 6|b|^2 = {sympy.simplify(E_perp - E_perp_target)}",
    )

    # Frobenius orthogonality: <pi_+, pi_perp>_F = 0
    fro_inner = sympy.simplify((pi_plus_H.H * pi_perp_H).trace())
    fro_inner_real = sympy.simplify(sympy.expand(sympy.re(fro_inner)) + 0)
    check(
        "<pi_+(H), pi_perp(H)>_F = 0 (orthogonal isotypic decomposition)",
        fro_inner_real == 0,
        detail=f"inner product reduces to {fro_inner_real}",
    )

    # ---------------------------------------------------------------------
    section("Part 2: F1 Lagrange extremum (T1 / CP / KAPPA)")
    # ---------------------------------------------------------------------

    # Abstract positive coordinates for the Lagrange step
    E_p, E_q, mu_lag, E_tot = symbols(
        "E_p E_q mu_lag E_tot",
        positive=True,
        real=True,
    )

    # F1 = log E_p + log E_q under constraint E_p + E_q = E_tot
    # Lagrangian L = log E_p + log E_q - mu_lag * (E_p + E_q - E_tot)
    # Stationary: 1/E_p = mu_lag, 1/E_q = mu_lag
    # Hence E_p = E_q = E_tot/2
    # Lagrange solve:
    L = log(E_p) + log(E_q) - mu_lag * (E_p + E_q - E_tot)
    grad_L = [
        sympy.diff(L, E_p),
        sympy.diff(L, E_q),
        sympy.diff(L, mu_lag),
    ]
    sols = sympy.solve(grad_L, (E_p, E_q, mu_lag), dict=True)
    # Expected: E_p = E_q = E_tot/2
    sols_clean = [
        {k: sympy.simplify(v) for k, v in s.items()} for s in sols
    ]

    expected_E_star = E_tot / 2
    found_critical = False
    for s in sols_clean:
        if (
            sympy.simplify(s[E_p] - expected_E_star) == 0
            and sympy.simplify(s[E_q] - expected_E_star) == 0
        ):
            found_critical = True
            break
    check(
        "(T1/CP): F1 Lagrange extremum is at E_+ = E_perp = E_tot/2",
        found_critical,
        detail=f"sols = {sols_clean}",
    )

    # Translate via (E+) and (Eperp): 3 a^2 = 6 |b|^2 i.e. a^2 = 2 |b|^2
    a_sym, b_sq_sym = symbols("a_sym b_sq_sym", positive=True, real=True)
    eq_locus = 3 * a_sym ** 2 - 6 * b_sq_sym  # = 0 at the locus
    sols_locus = sympy.solve(eq_locus, a_sym ** 2)
    check(
        "(KAPPA): 3 a^2 = 6 |b|^2 reduces to a^2 = 2 |b|^2",
        len(sols_locus) == 1
        and sympy.simplify(sols_locus[0] - 2 * b_sq_sym) == 0,
        detail=f"sols(a^2) = {sols_locus}",
    )

    # kappa = a^2 / |b|^2 at the locus
    kappa_at_locus = sympy.simplify((2 * b_sq_sym) / b_sq_sym)
    check(
        "(KAPPA): kappa = a^2 / |b|^2 = 2 at the F1 extremum",
        sympy.simplify(kappa_at_locus - 2) == 0,
        detail=f"kappa = {kappa_at_locus}",
    )

    # ---------------------------------------------------------------------
    section("Part 3: kappa = 2 <=> |b|^2/a^2 = 1/2 (T2 / KB)")
    # ---------------------------------------------------------------------

    # Forward: kappa = 2 means a^2 / |b|^2 = 2, so |b|^2 / a^2 = 1/2
    kappa = a_sym ** 2 / b_sq_sym
    BAE_form = b_sq_sym / a_sym ** 2

    # Substitute kappa = 2 into BAE_form via a^2 = 2 |b|^2
    BAE_at_kappa_2 = sympy.simplify(BAE_form.subs(a_sym ** 2, 2 * b_sq_sym))
    check(
        "(T2/KB) forward: kappa = 2 implies |b|^2/a^2 = 1/2",
        sympy.simplify(BAE_at_kappa_2 - Rational(1, 2)) == 0,
        detail=f"BAE form at kappa=2: {BAE_at_kappa_2}",
    )

    # Reverse: |b|^2 / a^2 = 1/2 means a^2 = 2 |b|^2, so kappa = 2
    kappa_at_BAE = sympy.simplify(kappa.subs(a_sym ** 2, 2 * b_sq_sym))
    check(
        "(T2/KB) reverse: |b|^2/a^2 = 1/2 implies kappa = 2",
        sympy.simplify(kappa_at_BAE - 2) == 0,
        detail=f"kappa at BAE: {kappa_at_BAE}",
    )

    # ---------------------------------------------------------------------
    section("Part 4: F1 Hessian negative-definite at critical point (T3)")
    # ---------------------------------------------------------------------

    # On the constraint surface E_p + E_q = E_tot, parameterize by t = E_p
    # so E_q = E_tot - t. Then F1(t) = log t + log(E_tot - t).
    t = Symbol("t", positive=True, real=True)
    F1_constrained = log(t) + log(E_tot - t)
    F1_t_double = sympy.diff(F1_constrained, t, 2)
    F1_t_double_at_critical = F1_t_double.subs(t, E_tot / 2)
    F1_t_double_simplified = sympy.simplify(F1_t_double_at_critical)
    expected = -8 / E_tot ** 2
    check(
        "(T3): d^2 F1 / dt^2 |_{t=E_tot/2} = -8/E_tot^2 < 0 (negative definite)",
        sympy.simplify(F1_t_double_simplified - expected) == 0,
        detail=f"d^2 F1 / dt^2 = {F1_t_double_simplified}",
    )

    # Verify the unconstrained Hessian entries match the parent's
    # "Derivable corollary": diagonal -1/E_p^2, -1/E_q^2 at E_p = E_q = E_tot/2
    F1_uncon = log(E_p) + log(E_q)
    Hess_pp = sympy.diff(F1_uncon, E_p, 2)
    Hess_qq = sympy.diff(F1_uncon, E_q, 2)
    Hess_pq = sympy.diff(F1_uncon, E_p, E_q)
    Hess_pp_crit = sympy.simplify(Hess_pp.subs([(E_p, E_tot / 2)]))
    Hess_qq_crit = sympy.simplify(Hess_qq.subs([(E_q, E_tot / 2)]))
    check(
        "(T3): unconstrained F1 Hessian diagonals at critical point: -4/E_tot^2",
        sympy.simplify(Hess_pp_crit + 4 / E_tot ** 2) == 0
        and sympy.simplify(Hess_qq_crit + 4 / E_tot ** 2) == 0
        and Hess_pq == 0,
        detail=f"Hess_pp = {Hess_pp_crit}, Hess_qq = {Hess_qq_crit}, Hess_pq = {Hess_pq}",
    )

    # ---------------------------------------------------------------------
    section("Part 5: LOCUS set equality (T2 chain)")
    # ---------------------------------------------------------------------

    # Sample on-locus point: a = sqrt(2), b = 1 (so a^2 = 2, |b|^2 = 1)
    a_on = sqrt(2)
    b_on_sq = Rational(1)
    kappa_on = a_on ** 2 / b_on_sq
    BAE_on = b_on_sq / a_on ** 2
    check(
        "LOCUS sample on-locus (a^2 = 2, |b|^2 = 1): kappa = 2 and |b|^2/a^2 = 1/2",
        sympy.simplify(kappa_on - 2) == 0
        and sympy.simplify(BAE_on - Rational(1, 2)) == 0,
        detail=f"kappa = {kappa_on}, BAE = {BAE_on}",
    )

    # Sample off-locus point: a = 1, b = 1 (so kappa = 1, NOT BAE)
    a_off = Rational(1)
    b_off_sq = Rational(1)
    kappa_off = a_off ** 2 / b_off_sq
    BAE_off = b_off_sq / a_off ** 2
    check(
        "LOCUS sample off-locus (a^2 = 1, |b|^2 = 1): kappa = 1 != 2 and BAE = 1 != 1/2",
        sympy.simplify(kappa_off - 1) == 0
        and sympy.simplify(BAE_off - 1) == 0
        and kappa_off != 2,
        detail=f"kappa = {kappa_off}, BAE = {BAE_off}",
    )

    # Another off-locus: kappa = 1/2, BAE = 2 (mirror image)
    a_off2_sq = Rational(1)
    b_off2_sq = Rational(2)
    kappa_off2 = a_off2_sq / b_off2_sq
    BAE_off2 = b_off2_sq / a_off2_sq
    check(
        "LOCUS sample off-locus (a^2 = 1, |b|^2 = 2): kappa = 1/2 and BAE = 2 (mirror)",
        sympy.simplify(kappa_off2 - Rational(1, 2)) == 0
        and sympy.simplify(BAE_off2 - 2) == 0,
        detail=f"kappa = {kappa_off2}, BAE = {BAE_off2}",
    )

    # ---------------------------------------------------------------------
    section("Part 6: counterfactual — F3 extremum at kappa = 1 (NOT BAE)")
    # ---------------------------------------------------------------------

    # F3 = log E_p + 2 log E_q under constraint E_p + E_q = E_tot
    # Lagrangian: L = log E_p + 2 log E_q - mu (E_p + E_q - E_tot)
    # Stationary: 1/E_p = mu, 2/E_q = mu
    # Hence E_q = 2 E_p, so E_tot = 3 E_p, E_p = E_tot/3, E_q = 2 E_tot/3
    # Translate via (E+),(Eperp): 3 a^2 = E_tot/3, 6 |b|^2 = 2 E_tot/3
    # So a^2 = E_tot/9, |b|^2 = E_tot/9, hence a^2 = |b|^2, kappa = 1
    F3_uncon = log(E_p) + 2 * log(E_q)
    L_F3 = F3_uncon - mu_lag * (E_p + E_q - E_tot)
    grad_F3 = [
        sympy.diff(L_F3, E_p),
        sympy.diff(L_F3, E_q),
        sympy.diff(L_F3, mu_lag),
    ]
    sols_F3 = sympy.solve(grad_F3, (E_p, E_q, mu_lag), dict=True)
    sols_F3_clean = [
        {k: sympy.simplify(v) for k, v in s.items()} for s in sols_F3
    ]
    # Expected: E_p = E_tot/3, E_q = 2 E_tot/3
    expected_F3 = (E_tot / 3, 2 * E_tot / 3)
    found_F3 = False
    for s in sols_F3_clean:
        if (
            sympy.simplify(s[E_p] - expected_F3[0]) == 0
            and sympy.simplify(s[E_q] - expected_F3[1]) == 0
        ):
            found_F3 = True
            break
    check(
        "counterfactual: F3 extremum at (E_+, E_perp) = (E_tot/3, 2 E_tot/3)",
        found_F3,
        detail=f"sols = {sols_F3_clean}",
    )

    # Translate to (a, b): 3 a^2 = E_tot/3, 6 |b|^2 = 2 E_tot/3
    # so a^2 = E_tot/9, |b|^2 = E_tot/9, kappa = 1
    a_sq_F3 = (E_tot / 3) / 3  # E_tot / 9
    b_sq_F3 = (2 * E_tot / 3) / 6  # E_tot / 9
    kappa_F3 = sympy.simplify(a_sq_F3 / b_sq_F3)
    check(
        "counterfactual: F3 extremum gives kappa = 1 (NOT 2 = BAE)",
        sympy.simplify(kappa_F3 - 1) == 0 and kappa_F3 != 2,
        detail=f"F3 extremum kappa = {kappa_F3}",
    )

    BAE_at_F3 = sympy.simplify(b_sq_F3 / a_sq_F3)
    check(
        "counterfactual: F3 extremum gives |b|^2/a^2 = 1 (NOT 1/2 = BAE)",
        sympy.simplify(BAE_at_F3 - 1) == 0,
        detail=f"BAE at F3 extremum = {BAE_at_F3} (off the BAE locus)",
    )

    # ---------------------------------------------------------------------
    section("Part 7: review-hygiene checks on the source note")
    # ---------------------------------------------------------------------

    note_path = (
        Path(__file__).resolve().parent.parent
        / "docs"
        / "BAE_BLOCK_TOTAL_FROBENIUS_DERIVATION_NARROW_THEOREM_NOTE_2026-05-16.md"
    )
    if note_path.exists():
        text = note_path.read_text(encoding="utf-8")
        check(
            "source note exists at expected path",
            True,
            detail=str(note_path.name),
        )
        check(
            "Status authority line present",
            "Status authority:" in text and "independent audit lane only" in text,
        )
        check(
            "claim_type bounded_theorem present in note",
            "**Type:** bounded_theorem" in text,
        )
        # Verify that the F1-vs-F3 selection question is preserved explicitly
        check(
            "Open derivation gap (F1-vs-F3) preserved",
            "F1-vs-F3" in text or "F1 canonicality" in text,
        )
        check(
            "does NOT claim positive closure of BAE",
            "Does **not** close BAE positively" in text,
        )
        check(
            "does NOT discharge the F1 canonicality hypothesis",
            "Does **not** discharge the hypothesis" in text,
        )
        check(
            "no new axiom admission",
            "Does **not** add a new axiom" in text,
        )
        check(
            "no new repo vocabulary",
            "no new repo vocabulary" in text.lower()
            or "Does **not** add a new axiom, new repo vocabulary" in text,
        )
        check(
            "cites koide_kappa_block_total_frobenius_algebraic upstream",
            "KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_ALGEBRAIC_NARROW_THEOREM_NOTE_2026-05-10"
            in text,
        )
        check(
            "cites primitive_p_bae_m1_m2_duality upstream",
            "PRIMITIVE_P_BAE_M1_M2_DUALITY_NOTE_2026-05-10_pPbae_duality" in text,
        )
        check(
            "cites BAE 30-probe campaign synthesis for the Open gap",
            "KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09"
            in text,
        )
        check(
            "uses markdown-link form for upstream citations",
            "[`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_ALGEBRAIC_NARROW_THEOREM_NOTE_2026-05-10.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_ALGEBRAIC_NARROW_THEOREM_NOTE_2026-05-10.md)"
            in text,
        )
    else:
        check(
            "source note exists at expected path",
            False,
            detail=f"missing: {note_path}",
        )

    # ---------------------------------------------------------------------
    section("Summary")
    # ---------------------------------------------------------------------
    print("  Verified at exact sympy precision:")
    print("    (E+)   E_+(H) = 3 a^2 parametric in (a, b)")
    print("    (Eperp) E_perp(H) = 6 |b|^2 parametric in (a, b)")
    print("    Frobenius orthogonality: <pi_+, pi_perp>_F = 0")
    print("    (T1/CP) F1 Lagrange extremum at E_+ = E_perp = E_tot/2")
    print("    (KAPPA) F1 extremum locus reduces to kappa = 2")
    print("    (T2/KB) kappa = 2 <=> |b|^2/a^2 = 1/2 (BAE)")
    print("    (T3)    F1 Hessian negative-definite at critical point")
    print("    (LOCUS) on-locus + off-locus sample identifications")
    print("    Counterfactual: F3 extremum at kappa = 1 (NOT BAE)")
    print("    Review-hygiene: note structure, claim type, citations,")
    print("                    open-gap preservation, no-new-axiom.")
    print()
    print(
        "  This audit-companion verifies the locus identification F1-extremum = BAE")
    print(
        "  algebraically, conditional on the F1 canonicality hypothesis H_F1, which")
    print("  is explicitly NOT discharged. The retention of")
    print(
        "  koide_kappa_block_total_frobenius_algebraic_narrow_theorem_note_2026-05-10")
    print(
        "  ratifies the F1-extremum algebra; the F1-vs-F3 weighting selection remains")
    print(
        "  the genuinely open atom per the 30-probe BAE campaign terminal synthesis.")

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS}, FAIL={FAIL}")
    print("=" * 88)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
