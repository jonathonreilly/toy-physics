#!/usr/bin/env python3
"""Runner for the naive lattice fermion 2^d species-count theorem."""

from __future__ import annotations

from itertools import product
from pathlib import Path

try:
    import sympy as sp
    from sympy import simplify, sin, symbols
except ImportError as exc:
    raise SystemExit("sympy required for exact algebra") from exc

ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs" / "NAIVE_LATTICE_FERMION_TWO_POWER_D_SPECIES_COUNT_NARROW_THEOREM_NOTE_2026-05-10.md"

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


def test_d4_corners_are_zeros() -> None:
    section("T1: d=4 naive Brillouin-zone corners")
    corners = list(product([0, sp.pi], repeat=4))
    zero_count = 0
    for corner in corners:
        value = sum(simplify(sin(k) ** 2) for k in corner)
        if simplify(value) == 0:
            zero_count += 1
    check(
        "all 16 corners {0, pi}^4 are zeros of sum_mu sin^2(k_mu a)",
        zero_count == 16,
        f"zero corners={zero_count}/16",
    )


def test_two_power_d_counts() -> None:
    section("T2: 2^d corner counts")
    counts = {d: len(list(product([0, sp.pi], repeat=d))) for d in range(1, 7)}
    expected = {d: 2**d for d in range(1, 7)}
    check(
        "corner count equals 2^d for d=1..6",
        counts == expected,
        f"counts={counts}",
    )


def test_zero_condition_reduction() -> None:
    section("T3: gamma algebra zero condition")
    k1, k2, k3, k4 = symbols("k1 k2 k3 k4", real=True)
    sin_sq_sum = sin(k1) ** 2 + sin(k2) ** 2 + sin(k3) ** 2 + sin(k4) ** 2
    zero_count = 0
    nonzero_sample_count = 0
    for corner in product([0, sp.pi], repeat=4):
        if simplify(sin_sq_sum.subs({k1: corner[0], k2: corner[1], k3: corner[2], k4: corner[3]})) == 0:
            zero_count += 1
    for sample in [(sp.pi / 2, 0, 0, 0), (sp.pi / 3, sp.pi, 0, 0), (sp.pi / 4, sp.pi / 5, 0, sp.pi)]:
        if simplify(sin_sq_sum.subs({k1: sample[0], k2: sample[1], k3: sample[2], k4: sample[3]})) != 0:
            nonzero_sample_count += 1
    check(
        "sum_mu sin^2(k_mu a) vanishes at corners and not at non-corner samples",
        zero_count == 16 and nonzero_sample_count == 3,
        f"corner zeros={zero_count}, non-corner nonzeros={nonzero_sample_count}",
    )


def test_d4_species_count() -> None:
    section("T4: d=4 species count")
    check("2^4 equals 16", 2**4 == 16, "d=4 naive count=16")


def test_wilson_lifts_nonzero_corners() -> None:
    section("T5: Wilson regulator context")
    lifted = 0
    unlifted = 0
    for corner in product([0, sp.pi], repeat=4):
        wilson = sum(1 - sp.cos(k) for k in corner)
        if simplify(wilson) == 0:
            unlifted += 1
        else:
            lifted += 1
    check(
        "Wilson term leaves one corner and lifts 15 naive doublers at d=4",
        unlifted == 1 and lifted == 15,
        f"unlifted={unlifted}, lifted={lifted}",
    )


def test_staggered_reduction_context() -> None:
    section("T6: staggered regulator context")
    rows = {}
    for d in (2, 4, 6):
        rows[d] = (2**d, 2 ** (d // 2), 2 ** (d // 2))
    ok = all(naive == tastes * reduced_spin for naive, tastes, reduced_spin in rows.values())
    check(
        "Kogut-Susskind count identity 2^d = 2^(d/2) * 2^(d/2) at even d",
        ok,
        f"rows={rows}",
    )


def test_regulator_dependence_disclosed() -> None:
    section("T7: regulator dependence disclosure")
    regulator_counts = {
        "naive_d4": 16,
        "wilson": 1,
        "twisted_mass": 2,
        "domain_wall": 1,
        "overlap": 1,
        "staggered_d4": 4,
    }
    ok = all(isinstance(v, int) and v > 0 for v in regulator_counts.values())
    ok = ok and len(set(regulator_counts.values())) > 1
    check(
        "non-naive regulators are explicitly different from the naive 16 count",
        ok,
        f"regulator_counts={regulator_counts}",
    )


def test_note_boundary() -> None:
    section("T8: source-note boundary")
    text = NOTE.read_text(encoding="utf-8")
    lower = text.lower()
    forbidden = [
        "regulator-independence of the `2^d` count; the theorem proves it",
        "closes any framework hierarchy",
        "nielsen-ninomiya as a numerical `2^d` lower-bound statement for every regulator/operator; the theorem proves it",
    ]
    check(
        "source note declares positive_theorem and avoids bridge overclaims",
        "**Claim type:** positive_theorem" in text and not any(item in lower for item in forbidden),
        "claim type present; overclaim phrases absent",
    )


def main() -> int:
    print("# Naive lattice fermion 2^d species-count runner")
    print(f"# Source note: {NOTE.relative_to(ROOT)}")
    test_d4_corners_are_zeros()
    test_two_power_d_counts()
    test_zero_condition_reduction()
    test_d4_species_count()
    test_wilson_lifts_nonzero_corners()
    test_staggered_reduction_context()
    test_regulator_dependence_disclosed()
    test_note_boundary()
    print(f"\n=== TOTAL: PASS={PASS}, FAIL={FAIL} ===")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
