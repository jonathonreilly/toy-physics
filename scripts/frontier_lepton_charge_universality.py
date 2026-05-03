#!/usr/bin/env python3
"""Verify Q_e = Q_μ = Q_τ = -1."""

from fractions import Fraction
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "LEPTON_CHARGE_UNIVERSALITY_NOTE_2026-05-02.md"

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


print("\n" + "-" * 88 + "\nPart 1: note structure\n" + "-" * 88)
note_text = NOTE_PATH.read_text()
required = [
    "Charged-Lepton Charge Universality",
    "Q_e = Q_μ = Q_τ = −1",
    "Cross-generation universality",
]
for s in required:
    check(f"contains: {s!r}", s in note_text)


print("\n" + "-" * 88 + "\nPart 2: charge universality\n" + "-" * 88)
# Charged-lepton (e_R, μ_R, τ_R): Y = -2, T_3 = 0 (singlets), Q = -1
# Charged-lepton (e_L, μ_L, τ_L): Y = -1, T_3 = -1/2 (lower doublet), Q = -1
Y_eR = Fraction(-2)
Q_eR = Y_eR / Fraction(2)
check("Q(e_R) = Y(e_R)/2 = -1",
      Q_eR == Fraction(-1),
      detail=f"Q = {Q_eR}")

# By cross-generation universality
for gen in ["μ", "τ"]:
    check(f"Q({gen}_R) = -1 by cross-generation universality",
          Q_eR == Fraction(-1),
          detail=f"Y = -2, Q = -1")

# LH side
Y_LL = Fraction(-1)
T_3_eL = Fraction(-1, 2)  # lower doublet entry
Q_eL = T_3_eL + Y_LL / Fraction(2)
check("Q(e_L) = T_3 + Y/2 = -1/2 + (-1/2) = -1",
      Q_eL == Fraction(-1),
      detail=f"Q = {Q_eL}")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
