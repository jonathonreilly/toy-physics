#!/usr/bin/env python3
"""
Current-stack nonderivation theorem for a finite Tau_(>1) upper bound on the
first symmetric three-sample beta=6 plaquette PF seam.
"""

from __future__ import annotations

from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]

THEOREM_PASS = 0
SUPPORT_PASS = 0
FAIL = 0


def check(name: str, condition: bool, detail: str = "", bucket: str = "THEOREM") -> None:
    global THEOREM_PASS, SUPPORT_PASS, FAIL
    status = "PASS" if condition else "FAIL"
    if condition:
        if bucket == "SUPPORT":
            SUPPORT_PASS += 1
        else:
            THEOREM_PASS += 1
    else:
        FAIL += 1
    print(f"  [{status}] [{bucket}] {name}")
    if detail:
        print(f"         {detail}")


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text()


def radical_entries() -> dict[str, sp.Expr]:
    rt2 = sp.sqrt(2)
    return {
        "a": -3 * sp.sqrt(2 - rt2),
        "b": -3 * rt2 + 3 * sp.sqrt(2 - sp.sqrt(2 + rt2)) + 3 * sp.sqrt(2 - sp.sqrt(2 - rt2)),
        "c": 16
        + 8 * sp.sqrt(2 + rt2)
        - 8 * sp.sqrt(2 + sp.sqrt(2 + rt2))
        - 8 * sp.sqrt(2 + sp.sqrt(2 - rt2)),
        "d": 3 * rt2 + 3 * sp.sqrt(2 - sp.sqrt(2 + rt2)) - 3 * sp.sqrt(2 - sp.sqrt(2 - rt2)),
        "e": 16
        - 8 * sp.sqrt(2 + rt2)
        - 8 * sp.sqrt(2 + sp.sqrt(2 + rt2))
        + 8 * sp.sqrt(2 + sp.sqrt(2 - rt2)),
    }


def sample_matrix() -> sp.Matrix:
    entries = radical_entries()
    return sp.Matrix(
        [
            [1, entries["a"], 0],
            [1, entries["b"], entries["c"]],
            [1, entries["d"], entries["e"]],
        ]
    )


def main() -> int:
    char_note = read("docs/GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_CHARACTER_MEASURE_THEOREM_NOTE.md")
    envelope_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_CHARACTER_TRUNCATION_ENVELOPE_NOTE_2026-04-17.md"
    )
    cone_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_POSITIVE_CONE_ORDER_WITNESS_NOTE_2026-04-17.md"
    )
    wedge_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_TAU_CONTROLLED_RETAINED_COEFFICIENT_WEDGE_NOTE_2026-04-17.md"
    )
    scalar_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_BETA6_SCALAR_VALUE_INSUFFICIENCY_NOTE_2026-04-17.md"
    )

    entries = radical_entries()
    a = sp.simplify(entries["a"])
    b = sp.simplify(entries["b"])
    c = sp.simplify(entries["c"])
    d = sp.simplify(entries["d"])
    e = sp.simplify(entries["e"])
    alpha = sp.simplify(-a)
    beta = sp.simplify(-e)

    tau = sp.symbols("tau", nonnegative=True)
    rho10 = sp.Integer(0)
    rho11 = sp.Integer(0)
    zhat_a = sp.Integer(1)
    zhat_b = sp.Integer(1)
    zhat_c = sp.Integer(1)
    r_a = sp.Integer(0)
    r_b = sp.Integer(0)
    r_c = sp.Integer(0)
    zhat_e = sp.simplify(1 + tau)

    # Exact current-stack witness family
    gap_a = sp.simplify(zhat_a - (1 + a * rho10 + r_a))
    gap_b = sp.simplify(zhat_b - (1 + b * rho10 + c * rho11 + r_b))
    gap_c = sp.simplify(zhat_c - (1 + d * rho10 + e * rho11 + r_c))
    identity_gap = sp.simplify(zhat_e - 1 - 18 * rho10 - 64 * rho11 - tau)

    fmat = sample_matrix()
    coeffs = sp.Matrix([1, 0, 0])
    cone_gap = sp.simplify(fmat * coeffs - sp.Matrix([zhat_a, zhat_b, zhat_c]))

    wedge_rho10_gap = sp.simplify((1 + tau) / alpha - rho10)
    wedge_rho11_gap = sp.simplify((1 + d * rho10 + tau) / beta - rho11)

    tau_examples = [sp.Integer(0), sp.Rational(1, 2), sp.Integer(1), sp.Integer(10), sp.Integer(1000)]
    example_rows: list[str] = []
    example_ok = True
    for tval in tau_examples:
        subs = {tau: tval}
        gap_vals = [
            sp.simplify(gap_a.subs(subs)),
            sp.simplify(gap_b.subs(subs)),
            sp.simplify(gap_c.subs(subs)),
            sp.simplify(identity_gap.subs(subs)),
        ]
        wedge_vals = [
            float(sp.N(wedge_rho10_gap.subs(subs), 50)),
            float(sp.N(wedge_rho11_gap.subs(subs), 50)),
        ]
        example_ok &= all(val == 0 for val in gap_vals) and min(wedge_vals) >= -1.0e-12
        example_rows.append(
            f"tau={sp.N(tval, 20)} -> gaps={gap_vals}, wedge_gaps=({wedge_vals[0]:.12f}, {wedge_vals[1]:.12f})"
        )

    print("=" * 110)
    print("GAUGE-VACUUM PLAQUETTE FIRST SYMMETRIC THREE-SAMPLE TAU UPPER-BOUND NONDERIVATION")
    print("=" * 110)
    print()
    print("Exact current-stack witness family")
    print("  rho_(1,0)(6) = 0")
    print("  rho_(1,1)(6) = 0")
    print("  R_A^(>1) = R_B^(>1) = R_C^(>1) = 0")
    print("  Z_hat_A = Z_hat_B = Z_hat_C = 1")
    print("  Z_hat_6(e) = 1 + tau")
    print("  Tau_(>1) = tau  (free nonnegative parameter)")
    print()
    print("Exact retained reconstruction of the sample triple (1,1,1)")
    print(f"  coefficient vector                          = {coeffs}")
    print(f"  F [1,0,0]^T - [1,1,1]^T                    = {cone_gap}")
    print()
    print("Representative tau values")
    for row in example_rows:
        print(f"  {row}")
    print()

    check(
        "Character-measure theorem already fixes a real nonnegative class function with nonnegative conjugation-symmetric normalized coefficients",
        "real nonnegative class function" in char_note
        and "`rho_(p,q)(beta) >= 0`" in char_note
        and "`rho_(p,q)(beta) = rho_(q,p)(beta)`" in char_note
        and "`rho_(0,0)(beta) = 1`" in char_note,
        bucket="SUPPORT",
    )
    check(
        "The truncation-envelope theorem already fixes the three sample equations, the tail box, and the identity-mass relation",
        "`Z_hat_A = 1 + a rho_(1,0) + R_A^(>1)`" in envelope_note
        and "`|R_i^(>1)| <= Tau_(>1)`" in envelope_note
        and "`Tau_(>1) = Z_hat_6(e) - 1 - 18 rho_(1,0)(6) - 64 rho_(1,1)(6)`" in envelope_note,
        bucket="SUPPORT",
    )
    check(
        "The positive-cone theorem already fixes the retained cone and the order witness used on the first seam",
        "`C = Cone(r_0, r_1, r_2)`" in cone_note
        and "`Z_B >= Z_A`" in cone_note,
        bucket="SUPPORT",
    )
    check(
        "The Tau-controlled wedge note already proves the current stack still does not upper-bound tau itself",
        "an upper bound on `Tau_(>1)` itself" in wedge_note
        and "does **not** solve `rho10`, `rho11`, or `tau`" in wedge_note,
        bucket="SUPPORT",
    )
    check(
        "The scalar-value insufficiency theorem already blocks any shortcut from one fixed same-surface scalar observable to the full class-sector vector",
        "one scalar framework-point observable leaves nontrivial class-sector freedom" in scalar_note,
        bucket="SUPPORT",
    )

    check(
        "The witness family satisfies the exact three-sample truncation-envelope equations identically for arbitrary nonnegative tau",
        gap_a == 0 and gap_b == 0 and gap_c == 0,
        detail=f"gaps=({gap_a}, {gap_b}, {gap_c})",
    )
    check(
        "The same family satisfies the exact tail envelope and identity-mass relation with Tau_(>1)=tau and Z_hat_6(e)=1+tau",
        identity_gap == 0 and r_a == 0 and r_b == 0 and r_c == 0,
        detail=f"identity gap={identity_gap}",
    )
    check(
        "The retained sample triple (1,1,1) lies exactly on the trivial ray of the first retained positive cone",
        coeffs == sp.Matrix([1, 0, 0]) and cone_gap == sp.Matrix([0, 0, 0]),
        detail=f"coefficient vector={coeffs}, cone gap={cone_gap}",
    )
    check(
        "The exact Tau-controlled wedge inequalities hold for the witness family for arbitrary nonnegative tau",
        float(sp.N(alpha, 50)) > 0.0
        and float(sp.N(beta, 50)) > 0.0
        and sp.simplify(wedge_rho10_gap - (1 + tau) / alpha) == 0
        and sp.simplify(wedge_rho11_gap - (1 + tau) / beta) == 0,
        detail=f"rho10 gap={sp.simplify(wedge_rho10_gap)}, rho11 gap={sp.simplify(wedge_rho11_gap)}",
    )
    check(
        "Therefore the current exact seam constraints admit arbitrarily large Tau_(>1), so no finite theorem-grade upper bound follows from them alone",
        example_ok and tau in wedge_rho10_gap.free_symbols and tau in wedge_rho11_gap.free_symbols,
        detail="the current witness family is exact for symbolic tau and remains valid on explicit large tau examples",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
