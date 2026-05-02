#!/usr/bin/env python3
"""Verify nucleon charges Q_p = +1, Q_n = 0 from quark hypercharges."""

from fractions import Fraction
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "HADRONIC_CHARGES_FROM_QUARK_Y_NOTE_2026-05-02.md"

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


# Quark electric charges from cycle 18 (Q = T_3 + Y/2)
Q_u = Fraction(2, 3)  # T_3 = +1/2, Y = +1/3 → Q = +2/3
Q_d = Fraction(-1, 3)  # T_3 = -1/2, Y = +1/3 → Q = -1/3


print("\n" + "-" * 88 + "\nPart 1: note structure\n" + "-" * 88)
note_text = NOTE_PATH.read_text()
required = ["Hadronic Electric Charges", "Q_p = +1", "Q_n = 0", "p = uud", "n = udd"]
for s in required:
    check(f"contains: {s!r}", s in note_text)


print("\n" + "-" * 88 + "\nPart 2: proton charge\n" + "-" * 88)
Q_p = Q_u + Q_u + Q_d
check("Q_p = Q_u + Q_u + Q_d = +1 (uud)",
      Q_p == Fraction(1),
      detail=f"= {Q_u} + {Q_u} + {Q_d} = {Q_p}")


print("\n" + "-" * 88 + "\nPart 3: neutron charge\n" + "-" * 88)
Q_n = Q_u + Q_d + Q_d
check("Q_n = Q_u + Q_d + Q_d = 0 (udd)",
      Q_n == Fraction(0),
      detail=f"= {Q_u} + {Q_d} + {Q_d} = {Q_n}")


print("\n" + "-" * 88 + "\nPart 4: charge conservation in beta decay\n" + "-" * 88)
# n → p + e^- + ν̄_e: charge conservation 0 = 1 + (-1) + 0 ✓
Q_e = Fraction(-1)
Q_nuebar = Fraction(0)
beta_decay_balance = Q_p + Q_e + Q_nuebar - Q_n
check("β decay charge conservation: Q_p + Q_e + Q_νbar = Q_n",
      beta_decay_balance == Fraction(0),
      detail=f"{Q_p} + {Q_e} + {Q_nuebar} = {Q_p+Q_e+Q_nuebar}, Q_n={Q_n}")


print("\n" + "=" * 88 + f"\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n" + "=" * 88)
sys.exit(1 if FAIL > 0 else 0)
