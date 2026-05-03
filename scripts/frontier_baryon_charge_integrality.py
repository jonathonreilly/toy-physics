#!/usr/bin/env python3
"""Verify baryon charge integrality Q_baryon = N_u - 1."""

from fractions import Fraction
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "BARYON_CHARGE_INTEGRALITY_NOTE_2026-05-02.md"

PASS = 0
FAIL = 0


def check(label, ok, detail=""):
    global PASS, FAIL
    if ok:
        PASS += 1
    else:
        FAIL += 1
    tag = "PASS (A)" if ok else "FAIL (A)"
    print(f"  [{tag}] {label}  ({detail})")


Q_u = Fraction(2, 3)
Q_d = Fraction(-1, 3)


print("\n" + "-" * 88 + "\nPart 1: note structure\n" + "-" * 88)
note_text = NOTE_PATH.read_text()
required = ["Baryon Charge Integrality", "Q_baryon = N_u − 1", "Δ⁺⁺", "Δ⁻"]
for s in required:
    check(f"contains: {s!r}", s in note_text)


print("\n" + "-" * 88 + "\nPart 2: integrality theorem\n" + "-" * 88)
for N_u in range(4):
    N_d = 3 - N_u
    Q_baryon = N_u * Q_u + N_d * Q_d
    expected = Fraction(N_u - 1)
    check(f"Q_baryon for N_u={N_u} = N_u - 1 = {expected}",
          Q_baryon == expected,
          detail=f"computed = {Q_baryon}")
    check(f"Q_baryon for N_u={N_u} is integer",
          Q_baryon.denominator == 1)


print("\n" + "-" * 88 + "\nPart 3: specific baryons\n" + "-" * 88)
baryons = [
    ("Δ⁻ (ddd)", 0, Fraction(-1)),
    ("n (udd)", 1, Fraction(0)),
    ("p (uud)", 2, Fraction(1)),
    ("Δ⁺⁺ (uuu)", 3, Fraction(2)),
]
for name, N_u, expected in baryons:
    Q = N_u * Q_u + (3 - N_u) * Q_d
    check(f"{name}: Q = {expected}",
          Q == expected, detail=f"computed = {Q}")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
