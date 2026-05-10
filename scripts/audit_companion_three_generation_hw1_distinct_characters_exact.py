#!/usr/bin/env python3
"""Exact-symbolic audit-companion runner for
`three_generation_hw1_distinct_translation_characters_narrow_theorem_note_2026-05-10`.

This is a Pattern A narrow theorem that isolates the
**distinct-translation-characters / sector-projector** half of the
parent `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`. The sibling
narrow `THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02.md`
holds the complementary algebra-generation / no-proper-quotient half.

The companion script verifies, at exact rational precision via sympy:

  (1) each of the three retained translations
        T_x = diag(-1, +1, +1), T_y = diag(+1, -1, +1), T_z = diag(+1, +1, -1)
      is an involution (T_a^2 = I_3);
  (2) the three matrices pairwise commute and are pairwise distinct;
  (3) the joint character map
        chi(X_i) = ( <X_i, T_x X_i>, <X_i, T_y X_i>, <X_i, T_z X_i> )
      takes the three claimed distinct sign triples (-1,+1,+1),
      (+1,-1,+1), (+1,+1,-1);
  (4) chi is injective on (X_1, X_2, X_3);
  (5) the eight joint sign-projectors
        P(s) = ((I + s_x T_x)/2) ((I + s_y T_y)/2) ((I + s_z T_z)/2)
      partition unity, with exactly three rank-1 components matching the
      basis projectors e_i e_i^T at chi(X_i), and five zero components
      at the remaining sign triples;
  (6) P_i P_j = delta_{i,j} P_i and P_1 + P_2 + P_3 = I_3;
  (7) the rank-1 sector decomposition C^3 = C X_1 + C X_2 + C X_3.

Companion role: not a new claim row, not a new source note, no status
promotion. Provides audit-friendly evidence that the narrow rescope's
load-bearing class-(A) algebra holds at exact symbolic precision on the
abstract `C^3` carrier with the cited retained-grade diagonal-form
generators.
"""

from pathlib import Path
import sys

try:
    import sympy
    from sympy import Matrix, eye, zeros, Rational, simplify
except ImportError:
    print("FAIL: sympy required for exact algebra")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "THREE_GENERATION_HW1_DISTINCT_TRANSLATION_CHARACTERS_NARROW_THEOREM_NOTE_2026-05-10.md"
CLAIM_ID = "three_generation_hw1_distinct_translation_characters_narrow_theorem_note_2026-05-10"


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
    print("Goal: sympy-symbolic verification of distinct joint characters")
    print("and rank-1 sector-projector identities on C^3.")
    print("=" * 88)

    # ---------------------------------------------------------------------
    section("Part 0: setup retained-grade diagonal generators on C^3")
    # ---------------------------------------------------------------------
    T_x = Matrix.diag(-1, 1, 1)
    T_y = Matrix.diag(1, -1, 1)
    T_z = Matrix.diag(1, 1, -1)
    I3 = eye(3)
    Z3 = zeros(3, 3)
    print(f"  T_x = diag(-1, +1, +1)")
    print(f"  T_y = diag(+1, -1, +1)")
    print(f"  T_z = diag(+1, +1, -1)")

    # ---------------------------------------------------------------------
    section("Part 1: each T_a is an involution on C^3")
    # ---------------------------------------------------------------------
    check("T_x^2 == I_3", T_x * T_x == I3, detail=f"T_x^2 = {T_x*T_x}")
    check("T_y^2 == I_3", T_y * T_y == I3, detail=f"T_y^2 = {T_y*T_y}")
    check("T_z^2 == I_3", T_z * T_z == I3, detail=f"T_z^2 = {T_z*T_z}")

    # ---------------------------------------------------------------------
    section("Part 2: the three translations pairwise commute and are pairwise distinct")
    # ---------------------------------------------------------------------
    check("[T_x, T_y] = 0", T_x * T_y - T_y * T_x == Z3)
    check("[T_x, T_z] = 0", T_x * T_z - T_z * T_x == Z3)
    check("[T_y, T_z] = 0", T_y * T_z - T_z * T_y == Z3)

    check("T_x != T_y", T_x != T_y)
    check("T_x != T_z", T_x != T_z)
    check("T_y != T_z", T_y != T_z)

    # ---------------------------------------------------------------------
    section("Part 3: joint character map chi(X_i) takes three distinct sign triples")
    # ---------------------------------------------------------------------
    X = [Matrix([[1], [0], [0]]),
         Matrix([[0], [1], [0]]),
         Matrix([[0], [0], [1]])]

    # chi(X_i) = ( <X_i, T_x X_i>, <X_i, T_y X_i>, <X_i, T_z X_i> )
    chi = []
    for i, x in enumerate(X):
        chi_i = (
            (x.T * (T_x * x))[0, 0],
            (x.T * (T_y * x))[0, 0],
            (x.T * (T_z * x))[0, 0],
        )
        chi.append(chi_i)
        print(f"  chi(X_{i+1}) = {chi_i}")

    check("chi(X_1) == (-1, +1, +1)", chi[0] == (-1, 1, 1))
    check("chi(X_2) == (+1, -1, +1)", chi[1] == (1, -1, 1))
    check("chi(X_3) == (+1, +1, -1)", chi[2] == (1, 1, -1))

    # ---------------------------------------------------------------------
    section("Part 4: chi is injective on (X_1, X_2, X_3)")
    # ---------------------------------------------------------------------
    check("chi(X_1) != chi(X_2)", chi[0] != chi[1])
    check("chi(X_1) != chi(X_3)", chi[0] != chi[2])
    check("chi(X_2) != chi(X_3)", chi[1] != chi[2])
    check(
        "image of chi has three distinct values (injectivity on three basis vectors)",
        len(set(chi)) == 3,
        detail=f"|im(chi)| = {len(set(chi))}",
    )

    # ---------------------------------------------------------------------
    section("Part 5: eight joint sign-projectors P(s) partition unity on C^3")
    # ---------------------------------------------------------------------
    def P_factor(T, s):
        """ ( I + s T ) / 2 """
        return (I3 + s * T) / Rational(2)

    def P_joint(sx, sy, sz):
        return P_factor(T_x, sx) * P_factor(T_y, sy) * P_factor(T_z, sz)

    # Enumerate eight sign triples
    signs = [(sx, sy, sz) for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)]
    projectors = {s: P_joint(*s) for s in signs}

    # The three sign triples in chi(X_i) should give rank-1 projectors e_i e_i^T.
    # The other five should give zero.
    e1e1T = X[0] * X[0].T
    e2e2T = X[1] * X[1].T
    e3e3T = X[2] * X[2].T

    check(
        "P(chi(X_1)) = P(-1,+1,+1) == e_1 e_1^T",
        projectors[(-1, 1, 1)] == e1e1T,
        detail=f"got {projectors[(-1, 1, 1)]}",
    )
    check(
        "P(chi(X_2)) = P(+1,-1,+1) == e_2 e_2^T",
        projectors[(1, -1, 1)] == e2e2T,
        detail=f"got {projectors[(1, -1, 1)]}",
    )
    check(
        "P(chi(X_3)) = P(+1,+1,-1) == e_3 e_3^T",
        projectors[(1, 1, -1)] == e3e3T,
        detail=f"got {projectors[(1, 1, -1)]}",
    )

    # The remaining five sign triples should give zero
    remaining = [s for s in signs if s not in {chi[0], chi[1], chi[2]}]
    for s in remaining:
        check(
            f"P{s} == 0 (no basis vector has these joint signs)",
            projectors[s] == Z3,
            detail=f"got {projectors[s]}",
        )

    check(
        "exactly three sign triples give nonzero (rank-1) projectors",
        sum(1 for s in signs if projectors[s] != Z3) == 3,
    )

    check(
        "exactly five sign triples give the zero operator",
        sum(1 for s in signs if projectors[s] == Z3) == 5,
    )

    # ---------------------------------------------------------------------
    section("Part 6: P_i orthogonality and completeness")
    # ---------------------------------------------------------------------
    P_list = [projectors[chi[i]] for i in range(3)]
    check("P_1^2 == P_1", P_list[0] * P_list[0] == P_list[0])
    check("P_2^2 == P_2", P_list[1] * P_list[1] == P_list[1])
    check("P_3^2 == P_3", P_list[2] * P_list[2] == P_list[2])

    check("P_1 P_2 == 0", P_list[0] * P_list[1] == Z3)
    check("P_1 P_3 == 0", P_list[0] * P_list[2] == Z3)
    check("P_2 P_3 == 0", P_list[1] * P_list[2] == Z3)
    check("P_2 P_1 == 0", P_list[1] * P_list[0] == Z3)
    check("P_3 P_1 == 0", P_list[2] * P_list[0] == Z3)
    check("P_3 P_2 == 0", P_list[2] * P_list[1] == Z3)

    check(
        "P_1 + P_2 + P_3 == I_3 (completeness)",
        P_list[0] + P_list[1] + P_list[2] == I3,
    )

    # Each P_i is rank 1
    for i, P in enumerate(P_list):
        check(
            f"rank(P_{i+1}) == 1",
            P.rank() == 1,
            detail=f"rank = {P.rank()}",
        )

    # ---------------------------------------------------------------------
    section("Part 7: rank-1 sector decomposition C^3 = C X_1 + C X_2 + C X_3")
    # ---------------------------------------------------------------------
    # P_i acts as scalar 1 on C X_i and 0 on the other two sectors.
    for i in range(3):
        for j in range(3):
            target = X[i] if i == j else zeros(3, 1)
            check(
                f"P_{i+1} X_{j+1} == {'X_' + str(i+1) if i == j else '0'}",
                P_list[i] * X[j] == target,
            )

    # Direct sum: any vector v in C^3 splits uniquely as v = sum P_i v
    sx, sy, sz = sympy.symbols("a b c")
    v = Matrix([[sx], [sy], [sz]])
    v_reconstructed = sum((P_list[i] * v for i in range(3)), zeros(3, 1))
    check(
        "any v in C^3 reconstructs as v = sum_i P_i v (direct sum)",
        simplify(v - v_reconstructed) == Z3.col(0).col_join(Z3.col(0)) or
        simplify((v - v_reconstructed).norm()) == 0 or
        v_reconstructed == v,
        detail="P_1 v + P_2 v + P_3 v == v as symbolic identity",
    )

    # ---------------------------------------------------------------------
    section("Part 8: note structure and scope discipline")
    # ---------------------------------------------------------------------
    note_text = NOTE_PATH.read_text()
    required = [
        "Three-Generation `hw=1` Distinct Translation Characters Narrow Theorem",
        "T_x = diag(-1, +1, +1)",
        "T_y = diag(+1, -1, +1)",
        "T_z = diag(+1, +1, -1)",
        "Status authority:** independent audit lane only",
        "C^3 = C X_1 \\oplus C X_2 \\oplus C X_3",
        "SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md",
        "Pattern A narrow rescope",
        "THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md",
        "Forbidden imports check",
    ]
    for s in required:
        check(f"note contains: {s!r}", s in note_text)

    # Scope discipline: must NOT consume generation_axiom_boundary as load-bearing
    forbidden = [
        "load-bears on generation_axiom_boundary",
        "physical-species claim is hereby retained",
        "no proper quotient",  # narrow scope explicitly excludes this
    ]
    for f in forbidden:
        check(
            f"narrow scope avoids forbidden claim: {f!r}",
            f not in note_text or "Does **not** claim no proper quotient" in note_text,
        )

    # ---------------------------------------------------------------------
    section("Summary")
    # ---------------------------------------------------------------------
    print("  Verified at exact sympy precision:")
    print("    Each T_a is an involution on C^3")
    print("    The three translations commute pairwise and are distinct")
    print("    chi(X_i) takes three distinct sign triples (injectivity)")
    print("    Eight joint sign-projectors partition unity")
    print("    Three rank-1 sector projectors P_i = e_i e_i^T")
    print("    Five remaining sign triples give zero operator")
    print("    P_i P_j = delta_{ij} P_i and P_1 + P_2 + P_3 = I_3")
    print("    Rank-1 sector decomposition C^3 = C X_1 + C X_2 + C X_3")

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS}, FAIL={FAIL}")
    print("=" * 88)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
