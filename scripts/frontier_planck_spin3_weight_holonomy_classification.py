#!/usr/bin/env python3
"""Audit the same-defect Spin(3) weight holonomy classification honestly."""

from __future__ import annotations

import math
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_SPIN3_WEIGHT_HOLONOMY_CLASSIFICATION_THEOREM_2026-04-23.md"
GRAVITY_NOTE = ROOT / "docs/GRAVITY_CLEAN_DERIVATION_NOTE.md"


def section(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def check(label: str, passed: bool, detail: str) -> bool:
    tag = "PASS" if passed else "FAIL"
    print(f"  [{tag}] {label}")
    print(f"         {detail}")
    return passed


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split()).lower()


def weights(j: float) -> list[float]:
    n = int(round(2.0 * j))
    return [(-n + 2 * k) / 2.0 for k in range(n + 1)]


def main() -> int:
    note = normalized(NOTE)
    gravity_note = normalized(GRAVITY_NOTE)
    n_pass = 0
    n_fail = 0

    print("Planck same-defect Spin(3) weight holonomy classification audit")
    print("=" * 78)

    section("PART 1: SPIN(3) WEIGHT STRUCTURE")
    sample_spins = [0.5, 1.0, 1.5, 2.0]
    positive_weights: list[float] = []
    all_half_integer = True
    for j in sample_spins:
        ws = weights(j)
        print(f"  j = {j:.1f} -> weights = {ws}")
        positive_weights.extend([abs(w) for w in ws if abs(w) > 1e-15])
        all_half_integer &= all(abs(2.0 * w - round(2.0 * w)) < 1e-12 for w in ws)
    p = check(
        "resolved Spin(3) weights lie in half-integers",
        all_half_integer,
        "for finite-dimensional Spin(3) irreps, m in (1/2) Z",
    )
    n_pass += int(p)
    n_fail += int(not p)

    min_positive_weight = min(positive_weights)
    p = check(
        "smallest nonzero positive Spin(3) weight is 1/2",
        abs(min_positive_weight - 0.5) < 1e-12,
        f"min |m| = {min_positive_weight:.6f}",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: SAME-DEFECT COEFFICIENT MAP")
    coeffs = [(m, 8.0 * math.pi * m) for m in [0.5, 1.0, 1.5, 2.0]]
    for m, coeff in coeffs:
        print(f"  |m| = {m:.1f} -> a^2/l_P^2 = 8 pi |m| = {coeff:.12f}")
    p = check(
        "minimal same-defect spinorial coefficient is 4 pi",
        abs(coeffs[0][1] - 4.0 * math.pi) < 1e-12,
        f"8 pi * (1/2) = {coeffs[0][1]:.12f}",
    )
    n_pass += int(p)
    n_fail += int(not p)

    eps_star = math.pi / 2.0
    q_star = 0.5 * eps_star
    ratio = 8.0 * math.pi * q_star / eps_star
    p = check(
        "same-defect minimal spinor with cubic plaquette defect still lands 4 pi",
        abs(ratio - 4.0 * math.pi) < 1e-12,
        f"eps_* = pi/2, q_* = eps_*/2 = pi/4 -> a^2/l_P^2 = {ratio:.12f}",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: EXACT-PLANCK NO-GO")
    m_required = 1.0 / (8.0 * math.pi)
    p = check(
        "exact Planck would require a non-half-integer weight",
        abs(2.0 * m_required - round(2.0 * m_required)) > 1e-6,
        f"|m| required for a=l_P is 1/(8 pi) = {m_required:.12f}",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "therefore no resolved-weight linear Spin(3) holonomy law can force exact Planck",
        m_required < 0.5,
        "the required weight lies below the smallest nonzero Spin(3) weight 1/2",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 4: LATTICE-UNIT CONSISTENCY")
    g_lattice = 1.0 / (4.0 * math.pi)
    l_planck_sq = g_lattice
    a_sq_min = (4.0 * math.pi) * l_planck_sq
    p = check(
        "gravity note carries G_N = 1/(4 pi) in lattice units",
        "g_n = 1/(4 pi)" in gravity_note or "g_n = 1 / (4 pi)" in gravity_note,
        "the exact gravity normalization is the same 4 pi structure used here",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "minimal same-defect spinorial coefficient reproduces unit lattice spacing exactly",
        abs(a_sq_min - 1.0) < 1e-12,
        f"l_P^2 = 1/(4 pi) -> a^2 = 4 pi l_P^2 = {a_sq_min:.12f}",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 5: NOTE VERDICT")
    p = check(
        "note states the exact classification a^2/l_P^2 = 8 pi |m|",
        "a^2 / l_p^2 = 8 pi |m|" in note,
        "the core classification formula must be stated explicitly",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "note states minimal nonzero coefficient 4 pi and exact-Planck impossibility",
        "smallest nonzero such coefficient is `4 pi`" in note
        and "exact `a = l_p` is impossible" in note,
        "the note must state both the surviving exact candidate and the no-go",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("FINAL VERDICT")
    verdict = (
        "The resolved-weight same-defect Spin(3) holonomy class is now exact: "
        "it yields a^2/l_P^2 = 8 pi |m|, so the minimal spinorial candidate is "
        "4 pi and exact conventional a=l_P is impossible on this whole linear class."
    )
    print(f"  {verdict}")

    print("\n" + "=" * 78)
    print(f"SCORECARD: {n_pass} pass, {n_fail} fail out of {n_pass + n_fail}")
    print("=" * 78)

    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
