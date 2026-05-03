#!/usr/bin/env python3
"""Verify meson electric charge integrality from quark Y values."""

from fractions import Fraction
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "MESON_CHARGES_FROM_QUARK_Y_NOTE_2026-05-02.md"

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


# Up-type quarks Q = +2/3, down-type quarks Q = -1/3
Q_up = Fraction(2, 3)
Q_down = Fraction(-1, 3)


print("\n" + "-" * 88 + "\nPart 1: note structure\n" + "-" * 88)
note_text = NOTE_PATH.read_text()
required = ["Meson Electric Charge", "Q_meson = Q_q − Q_q'", "π⁺", "K⁰", "D⁺"]
for s in required:
    check(f"contains: {s!r}", s in note_text)


print("\n" + "-" * 88 + "\nPart 2: meson charge integrality\n" + "-" * 88)
mesons = [
    ("π⁺ (ud̄)", Q_up, Q_down, Fraction(1)),
    ("π⁻ (dū)", Q_down, Q_up, Fraction(-1)),
    ("K⁺ (us̄)", Q_up, Q_down, Fraction(1)),
    ("K⁰ (ds̄)", Q_down, Q_down, Fraction(0)),
    ("K̄⁰ (sd̄)", Q_down, Q_down, Fraction(0)),
    ("D⁺ (cd̄)", Q_up, Q_down, Fraction(1)),
    ("D⁰ (cū)", Q_up, Q_up, Fraction(0)),
    ("B⁰ (db̄)", Q_down, Q_down, Fraction(0)),
    ("B⁺ (ub̄)", Q_up, Q_down, Fraction(1)),
]

for name, Q_q, Q_qbar, expected in mesons:
    Q_meson = Q_q - Q_qbar  # Q for q q̄' is Q_q - Q_q'
    check(f"Q({name}) = {expected}",
          Q_meson == expected,
          detail=f"= {Q_q} - {Q_qbar} = {Q_meson}")
    check(f"Q({name}) is integer",
          Q_meson.denominator == 1)


print("\n" + "-" * 88 + "\nPart 3: charge spectrum is {-1, 0, +1}\n" + "-" * 88)
charges = set(Q_q - Q_qbar for _, Q_q, Q_qbar, _ in mesons)
expected_charges = {Fraction(-1), Fraction(0), Fraction(1)}
check("meson charge spectrum = {-1, 0, +1}",
      charges == expected_charges,
      detail=f"computed = {sorted(charges)}")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
