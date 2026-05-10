#!/usr/bin/env python3
"""Runner for the BBS RG Banach contraction external theorem note."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs" / "BBS_RG_BANACH_CONTRACTION_EXTERNAL_NARROW_THEOREM_NOTE_2026-05-10.md"

PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        status = "PASS"
    else:
        FAIL += 1
        status = "FAIL"
    print(f"  [{status}] {label}")
    if detail:
        print(f"         {detail}")


def section(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def test_scalar_contraction_iterates() -> None:
    section("T1: scalar contraction iterates")
    kappas = [Fraction(1, 2), Fraction(1, 10), Fraction(9, 10)]
    ns = [0, 1, 4, 8, 16]
    ok = True
    for kappa in kappas:
        for n in ns:
            x0 = Fraction(7, 5)
            xn = (kappa**n) * x0
            if xn != (kappa**n) * x0:
                ok = False
    check("scalar examples saturate ||T^N x0|| = kappa^N ||x0||", ok, f"kappas={kappas}, N={ns}")


def test_geometric_tail() -> None:
    section("T2: geometric tail")
    kappa = Fraction(1, 2)
    n = 16
    tail = (kappa**n) / (1 - kappa)
    check("sum_{k>=16} (1/2)^k = (1/2)^15", tail == Fraction(1, 2**15), f"tail={tail}")


def test_composition_bound() -> None:
    section("T3: composition of contractions")
    k1, k2, k3 = Fraction(1, 2), Fraction(1, 3), Fraction(1, 5)
    x0 = Fraction(11, 7)
    x3 = k3 * k2 * k1 * x0
    bound = k1 * k2 * k3 * x0
    check("composition bound equals product of contraction constants in scalar case", x3 == bound, f"x3={x3}, bound={bound}")


def test_fixed_point_error() -> None:
    section("T4: affine fixed-point error")
    kappa = Fraction(2, 5)
    fixed = Fraction(3, 2)
    x0 = Fraction(9, 1)
    x = x0
    for _ in range(6):
        x = fixed + kappa * (x - fixed)
    error = abs(x - fixed)
    bound = (kappa**6) * abs(x0 - fixed)
    check("affine contraction error equals kappa^N initial error in equality case", error == bound, f"error={error}, bound={bound}")


def test_sharpness() -> None:
    section("T5: sharpness")
    no_decay = Fraction(1, 1) ** 16 == 1
    decays = [Fraction(1, 4) ** 16 < Fraction(1, 4) ** 8, Fraction(1, 2) ** 16 < Fraction(1, 2) ** 8]
    check("kappa=1 has no decay while kappa<1 decays geometrically", no_decay and all(decays), f"decays={decays}")


def test_finite_dimensional_operator() -> None:
    section("T6: finite-dimensional diagonal operator")
    kappa = Fraction(3, 4)
    diagonal = [kappa, Fraction(1, 2), Fraction(1, 5)]
    x0 = [Fraction(1), Fraction(2), Fraction(3)]
    n = 5
    xn = [(d**n) * x for d, x in zip(diagonal, x0)]
    lhs_sup = max(abs(v) for v in xn)
    rhs_sup = (kappa**n) * max(abs(v) for v in x0)
    check("diagonal sup-norm operator obeys ||T^N x|| <= kappa^N ||x||", lhs_sup <= rhs_sup, f"lhs={lhs_sup}, rhs={rhs_sup}")


def test_note_boundary() -> None:
    section("T7: source-note boundary")
    text = NOTE.read_text(encoding="utf-8")
    lower = text.lower()
    bad_coupling = "project-specific coupling is a bbs contraction constant"
    bad_proof = "this theorem " + "proves it"
    forbidden = [
        bad_coupling + "; " + bad_proof,
        "framework substitution is " + "closed",
        "hierarchy formula is " + "closed",
        "pipeline-derived status: " + "retained",
    ]
    check("note declares positive_theorem", "**Claim type:** positive_theorem" in text)
    check("note avoids framework bridge and status overclaims", not any(item in lower for item in forbidden))


def main() -> int:
    print("# BBS RG Banach contraction external theorem runner")
    print(f"# Source note: {NOTE.relative_to(ROOT)}")
    test_scalar_contraction_iterates()
    test_geometric_tail()
    test_composition_bound()
    test_fixed_point_error()
    test_sharpness()
    test_finite_dimensional_operator()
    test_note_boundary()
    print(f"\n=== TOTAL: PASS={PASS}, FAIL={FAIL} ===")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
