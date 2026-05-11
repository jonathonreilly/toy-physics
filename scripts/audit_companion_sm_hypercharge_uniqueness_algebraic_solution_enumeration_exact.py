#!/usr/bin/env python3
"""Exact-symbolic audit-companion runner for
`sm_hypercharge_uniqueness_algebraic_solution_enumeration_narrow_theorem_note_2026-05-10`.

Pattern A narrow rescope of the load-bearing solution-enumeration step
inside the parent
`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`.

Given the three retained right-handed singlet anomaly-cancellation
equations

    (A1)  3 (y_1 + y_2) + y_3 + y_4   =   0,
    (A2)  y_1 + y_2                    =   2/3,
    (A3)  3 (y_1^3 + y_2^3) + y_3^3 + y_4^3   =  -16/9,

plus the neutral-singlet identification y_4 = 0 (N) and the
electric-charge labelling Q(u_R) > 0 (Q), this script verifies, at
exact rational precision via sympy, that the rational solution set is
exactly two ordered 4-tuples related by the y_1 <-> y_2 swap, and that
(Q) selects the unique tuple (+4/3, -2/3, -2, 0).

Verification covers:
  (1) Step 1: y_4 = 0 and (A1)+(A2) force y_3 = -2;
  (2) Step 2: substitution into (A3) gives y_1^3 + y_2^3 = 56/27;
  (3) Step 3: the rational quadratic 9 t^2 - 6 t - 8 = 0 has
      discriminant 324 = 18^2 and rational roots {4/3, -2/3};
  (4) Direct sympy `solve` enumeration over (y_1, y_2, y_3, y_4) in Q^4
      of the system (A1)+(A2)+(A3)+(N) returns exactly the two-element
      set S_2 = { (4/3, -2/3, -2, 0), (-2/3, 4/3, -2, 0) };
  (5) Imposing y_1 > 0 (Q) reduces S_2 to the singleton S_1 = { (4/3,
      -2/3, -2, 0) };
  (6) The one-generation electric-charge spectrum under Q = T_3 + Y/2
      is exactly { 0, +/-1/3, +/-2/3, +/-1 } with denominators {1, 3};
  (7) Counterfactual: dropping (N) gives a 1-parameter rational family.
"""

from pathlib import Path
import sys

try:
    import sympy
    from sympy import Rational, Symbol, symbols, simplify, solve, sqrt
except ImportError:
    print("FAIL: sympy required for exact algebra")
    sys.exit(1)


ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "SM_HYPERCHARGE_UNIQUENESS_ALGEBRAIC_SOLUTION_ENUMERATION_NARROW_THEOREM_NOTE_2026-05-10.md"
CLAIM_ID = "sm_hypercharge_uniqueness_algebraic_solution_enumeration_narrow_theorem_note_2026-05-10"


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
    print(CLAIM_ID)
    print("Goal: sympy-symbolic rational-solution enumeration of (A1)-(A3)+(N)+(Q)")
    print("=" * 88)

    # ---------------------------------------------------------------------
    section("Part 0: symbolic setup of the anomaly system")
    # ---------------------------------------------------------------------
    y1, y2, y3, y4 = symbols("y1 y2 y3 y4", rational=True)
    # (A1), (A2), (A3) at exact rationals; right-hand sides imported from
    # the parent note's retained left-handed content tabulation.
    A1 = 3 * (y1 + y2) + y3 + y4
    A2 = y1 + y2 - Rational(2, 3)
    A3 = 3 * (y1**3 + y2**3) + y3**3 + y4**3 - (-Rational(16, 9))
    print(f"  (A1) 3(y1 + y2) + y3 + y4 = 0")
    print(f"  (A2) y1 + y2 = 2/3")
    print(f"  (A3) 3(y1^3 + y2^3) + y3^3 + y4^3 = -16/9")
    print(f"  (N)  y4 = 0")

    # ---------------------------------------------------------------------
    section("Part 1: Step 1 reduction — y_4 = 0 and (A1)+(A2) imply y_3 = -2")
    # ---------------------------------------------------------------------
    # Substitute y4 = 0 into A1, and use A2 in the resulting expression.
    # A2 says y1 + y2 = 2/3; substitute y2 = 2/3 - y1 into A1|_{y4=0}.
    A1_N = A1.subs(y4, 0)
    A1_after_A2 = A1_N.subs(y2, Rational(2, 3) - y1)
    # Now A1_after_A2 should simplify to 2 + y3 (independent of y1).
    y3_value = solve(A1_after_A2, y3)
    check(
        "Step 1: y4 = 0 and (A1)+(A2) reduce to y3 = -2",
        len(y3_value) == 1 and simplify(y3_value[0] - Rational(-2)) == 0,
        detail=f"y3 = {y3_value}",
    )

    # ---------------------------------------------------------------------
    section("Part 2: Step 2 — (A3) reduces to y_1^3 + y_2^3 = 56/27")
    # ---------------------------------------------------------------------
    # Substitute y4 = 0 and y3 = -2 into A3 and rearrange.
    # A3 = 3(y1^3+y2^3) + y3^3 + y4^3 - (-16/9) = 3(y1^3+y2^3) + y3^3 + y4^3 + 16/9
    # Setting A3 = 0 gives 3(y1^3+y2^3) = -y3^3 - y4^3 - 16/9.
    # At y3 = -2, y4 = 0: 3(y1^3+y2^3) = -(-8) - 0 - 16/9 = 8 - 16/9 = 56/9.
    # So y1^3 + y2^3 = 56/27.
    A3_N = A3.subs({y4: 0, y3: -2})
    # A3_N = 0 gives the closed form. Solve for y1^3 by isolating:
    # 3*y1^3 + 3*y2^3 = -A3_N + 3*(y1^3 + y2^3) i.e. we test A3_N = 3*(y1^3+y2^3) - 56/9.
    A3_N_target = 3 * (y1**3 + y2**3) - Rational(56, 9)
    check(
        "Step 2: A3 at (y4=0, y3=-2) is 3*(y1^3+y2^3) - 56/9",
        simplify(A3_N - A3_N_target) == 0,
        detail=f"A3_N - target = {simplify(A3_N - A3_N_target)}",
    )
    # Equivalently, setting A3_N = 0 means y1^3 + y2^3 = 56/27.
    check(
        "Step 2: setting A3_N = 0 forces y1^3 + y2^3 = 56/27",
        simplify(A3_N.subs(y1**3 + y2**3, Rational(56, 27))) == 0
        or simplify(A3_N + Rational(56, 9) - 3 * (y1**3 + y2**3)) == 0,
        detail="3*(y1^3 + y2^3) = 56/9, so y1^3+y2^3 = 56/27",
    )

    # ---------------------------------------------------------------------
    section("Part 3: Step 3 — closed-form quadratic 9 t^2 - 6 t - 8 = 0 with rational roots")
    # ---------------------------------------------------------------------
    # From (S2) and (A2): use identity (y1+y2)^3 = y1^3+y2^3 + 3 y1 y2 (y1+y2)
    # (2/3)^3 = 56/27 + 3 y1 y2 (2/3)
    # 8/27 = 56/27 + 2 y1 y2
    # 2 y1 y2 = -48/27 = -16/9
    # y1 y2 = -8/9.
    # So y1, y2 are roots of t^2 - (2/3) t - 8/9 = 0, or 9 t^2 - 6 t - 8 = 0.
    t = Symbol("t", rational=True)
    quad = 9 * t**2 - 6 * t - 8
    disc = (-6) ** 2 - 4 * 9 * (-8)
    check(
        "discriminant of 9 t^2 - 6 t - 8 is 324 = 18^2 (perfect square)",
        disc == 324 and sympy.sqrt(disc) == 18,
        detail=f"disc = {disc}, sqrt(disc) = {sympy.sqrt(disc)}",
    )
    roots = solve(quad, t)
    check(
        "rational roots of 9 t^2 - 6 t - 8 are exactly {4/3, -2/3}",
        set(roots) == {Rational(4, 3), Rational(-2, 3)},
        detail=f"roots = {roots}",
    )

    # ---------------------------------------------------------------------
    section("Part 4: rational solution enumeration over Q^4 of (A1)+(A2)+(A3)+(N)")
    # ---------------------------------------------------------------------
    sols = solve([A1, A2, A3, y4], [y1, y2, y3, y4], dict=True)
    # Convert to ordered 4-tuples
    S2_set = {(s[y1], s[y2], s[y3], s[y4]) for s in sols}
    expected_S2 = {
        (Rational(4, 3), Rational(-2, 3), Rational(-2), Rational(0)),
        (Rational(-2, 3), Rational(4, 3), Rational(-2), Rational(0)),
    }
    check(
        "rational solution set S_2 has exactly two elements",
        len(S2_set) == 2,
        detail=f"|S_2| = {len(S2_set)}",
    )
    check(
        "S_2 = { (+4/3, -2/3, -2, 0), (-2/3, +4/3, -2, 0) }",
        S2_set == expected_S2,
        detail=f"S_2 = {S2_set}",
    )

    # ---------------------------------------------------------------------
    section("Part 5: Q-labelling (Q): y_1 > 0 selects the unique tuple S_1")
    # ---------------------------------------------------------------------
    S1_set = {tup for tup in S2_set if tup[0] > 0}
    expected_S1 = {(Rational(4, 3), Rational(-2, 3), Rational(-2), Rational(0))}
    check(
        "imposing Q(u_R) > 0 (y_1 > 0) reduces S_2 to a singleton",
        len(S1_set) == 1,
        detail=f"|S_1| = {len(S1_set)}",
    )
    check(
        "S_1 = { (+4/3, -2/3, -2, 0) }",
        S1_set == expected_S1,
        detail=f"S_1 = {S1_set}",
    )

    # ---------------------------------------------------------------------
    section("Part 6: one-generation electric-charge spectrum under Q = T_3 + Y/2")
    # ---------------------------------------------------------------------
    y1_v, y2_v, y3_v, y4_v = Rational(4, 3), Rational(-2, 3), Rational(-2), Rational(0)
    # SU(2) singlets: Q = Y/2
    Q_uR = y1_v / 2
    Q_dR = y2_v / 2
    Q_eR = y3_v / 2
    Q_nuR = y4_v / 2
    check("Q(u_R) = +2/3", Q_uR == Rational(2, 3))
    check("Q(d_R) = -1/3", Q_dR == Rational(-1, 3))
    check("Q(e_R) = -1", Q_eR == -1)
    check("Q(ν_R) = 0", Q_nuR == 0)

    # SU(2) doublets: Q = T_3 + Y/2 for Y_QL = +1/3, Y_LL = -1
    Y_QL = Rational(1, 3)
    Y_LL = Rational(-1)
    Q_uL = Rational(1, 2) + Y_QL / 2
    Q_dL = Rational(-1, 2) + Y_QL / 2
    Q_nuL = Rational(1, 2) + Y_LL / 2
    Q_eL = Rational(-1, 2) + Y_LL / 2
    check("Q(u_L) = +2/3", Q_uL == Rational(2, 3))
    check("Q(d_L) = -1/3", Q_dL == Rational(-1, 3))
    check("Q(ν_L) = 0", Q_nuL == 0)
    check("Q(e_L) = -1", Q_eL == -1)

    # The "one-generation spectrum" the parent note refers to means the set
    # of distinct values of Q across the eight chiral states {Q,L doublets +
    # u_R, d_R, e_R, nu_R singlets} together with their charge conjugates
    # (antiparticles, which carry the opposite electric charge in the same
    # generation). The parent claim is {0, +/-1/3, +/-2/3, +/-1}.
    particles = {Q_uR, Q_dR, Q_eR, Q_nuR, Q_uL, Q_dL, Q_nuL, Q_eL}
    antiparticles = {-q for q in particles}
    spectrum = particles | antiparticles
    expected_spectrum = {
        Rational(0),
        Rational(1, 3),
        Rational(-1, 3),
        Rational(2, 3),
        Rational(-2, 3),
        Rational(1),
        Rational(-1),
    }
    check(
        "electric-charge spectrum = { 0, +/-1/3, +/-2/3, +/-1 } (particles + antiparticles)",
        spectrum == expected_spectrum,
        detail=f"spectrum = {sorted(spectrum)}",
    )
    # Denominators
    dens = {q.q for q in spectrum}
    check(
        "denominators of the charge spectrum are exactly {1, 3}",
        dens == {1, 3},
        detail=f"denominators = {dens}",
    )

    # ---------------------------------------------------------------------
    section("Part 7: counterfactual — drop (N) gives a 1-parameter family")
    # ---------------------------------------------------------------------
    # Solve without N: 3 equations (A1, A2, A3) in 4 unknowns => 1-parameter family.
    # Concretely: pick three distinct y4 values and verify each yields a solution.
    counter_witnesses = []
    for y4_choice in [Rational(1, 3), Rational(2, 3), Rational(-1)]:
        sols_yk = solve(
            [A1.subs(y4, y4_choice), A2, A3.subs(y4, y4_choice)],
            [y1, y2, y3],
            dict=True,
        )
        if sols_yk:
            counter_witnesses.append((y4_choice, len(sols_yk)))
    check(
        "counterfactual: dropping (N) admits multiple rational solutions parameterized by y_4",
        len(counter_witnesses) >= 3,
        detail=f"witnesses: {counter_witnesses}",
    )

    # Specifically verify that y4 = 1/3 gives a different y3 than y4 = 0:
    sols_y4_third = solve(
        [A1.subs(y4, Rational(1, 3)), A2, A3.subs(y4, Rational(1, 3))],
        [y1, y2, y3],
        dict=True,
    )
    if sols_y4_third:
        y3_at_y4_third = sols_y4_third[0][y3]
    else:
        y3_at_y4_third = None
    check(
        "counterfactual: y_4 = 1/3 yields y_3 != -2",
        y3_at_y4_third is not None and y3_at_y4_third != -2,
        detail=f"at y4 = 1/3, y3 = {y3_at_y4_third}",
    )

    # ---------------------------------------------------------------------
    section("Part 8: note structure and scope discipline")
    # ---------------------------------------------------------------------
    note_text = NOTE_PATH.read_text()
    required = [
        "SM Hypercharge Uniqueness Algebraic Solution-Enumeration Narrow Theorem",
        "Status authority:** independent audit lane only",
        "3 (y_1 + y_2) + y_3 + y_4",
        "y_1 + y_2",
        "y_1^3 + y_2^3",
        "y_4 = 0",
        "Pattern A narrow rescope",
        "STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md",
        "Forbidden imports check",
        "S_2",
        "S_1",
    ]
    for s in required:
        check(f"note contains: {s!r}", s in note_text)

    # Scope discipline: must NOT claim derivation of the upstream inputs
    forbidden_declined = [
        "derive the coefficients of (A1)-(A3)",
        "derive the requirement that an anomaly-cancelling",
        "derive the neutral-singlet identification",
    ]
    for f in forbidden_declined:
        check(
            f"narrow scope explicitly declines: {f!r}",
            f in note_text,  # the note says "Does NOT derive ..."
            detail="appears under 'What this does NOT claim'",
        )

    # ---------------------------------------------------------------------
    section("Summary")
    # ---------------------------------------------------------------------
    print("  Verified at exact sympy precision:")
    print("    Step 1: y4 = 0 and (A1)+(A2) imply y3 = -2")
    print("    Step 2: (A3) reduces to y1^3 + y2^3 = 56/27")
    print("    Step 3: quadratic 9 t^2 - 6 t - 8 has discriminant 18^2, roots {4/3, -2/3}")
    print("    Direct enumeration: S_2 = {(+4/3, -2/3, -2, 0), (-2/3, +4/3, -2, 0)}")
    print("    Q-labelling: S_1 = {(+4/3, -2/3, -2, 0)}")
    print("    Electric-charge spectrum: {0, +/-1/3, +/-2/3, +/-1}, denominators {1, 3}")
    print("    Counterfactual: dropping y4 = 0 reopens a 1-parameter family")

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS}, FAIL={FAIL}")
    print("=" * 88)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
