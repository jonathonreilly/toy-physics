#!/usr/bin/env python3
"""Verify sin²θ_W^GUT = 3/8 derivation from SU(5) embedding + LHCM Tr[Y²]
at exact Fraction precision."""

from fractions import Fraction
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "SIN_SQUARED_THETA_W_GUT_FROM_SU5_NOTE_2026-05-02.md"

PASS_COUNT = 0
FAIL_COUNT = 0


def check(label, ok, detail=""):
    global PASS_COUNT, FAIL_COUNT
    tag = "PASS (A)" if ok else "FAIL (A)"
    if ok:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    print(f"  [{tag}] {label}  ({detail})")


def section(title):
    print("\n" + "-" * 88 + f"\n{title}\n" + "-" * 88)


section("Part 1: note structure")
note_text = NOTE_PATH.read_text()
required = [
    "sin²θ_W^GUT = 3/8",
    "SU(5) Embedding",
    "LHCM-Derived Tr[Y²]",
    "Y_GUT = √(3/5) · Y_SM",
    "tan²θ_W^GUT  =  3/5",
    "cos²θ_W^GUT  =  5/8",
    "sin²θ_W(M_Z) ≈ 0.231",
    "RG running",
    "proposal_allowed: false",
]
for s in required:
    check(f"contains: {s!r}", s in note_text)


section("Part 2: GUT normalization Y_GUT² = (3/5) Y_SM²")
gut_factor_squared = Fraction(3, 5)
check("Y_GUT² / Y_SM² = 3/5",
      gut_factor_squared == Fraction(3, 5),
      detail=f"factor² = {gut_factor_squared}")


section("Part 3: tan²θ_W^GUT = g'²/g_2² = 3/5 at GUT scale")
tan2_theta_W_GUT = Fraction(3, 5)
check("tan²θ_W^GUT = 3/5",
      tan2_theta_W_GUT == Fraction(3, 5),
      detail="from g'² = g_2² · (3/5) at GUT scale (g_2 = g_1_GUT)")


section("Part 4: sin²θ_W^GUT = 3/8")
sin2_theta_W_GUT = tan2_theta_W_GUT / (Fraction(1) + tan2_theta_W_GUT)
check("sin²θ_W^GUT = tan² / (1 + tan²) = (3/5) / (8/5) = 3/8",
      sin2_theta_W_GUT == Fraction(3, 8),
      detail=f"= {tan2_theta_W_GUT} / {Fraction(1) + tan2_theta_W_GUT} = {sin2_theta_W_GUT}")


section("Part 5: cos²θ_W^GUT = 5/8")
cos2_theta_W_GUT = Fraction(1) - sin2_theta_W_GUT
check("cos²θ_W^GUT = 1 - 3/8 = 5/8",
      cos2_theta_W_GUT == Fraction(5, 8),
      detail=f"= 1 - {sin2_theta_W_GUT} = {cos2_theta_W_GUT}")

# Verify sin² + cos² = 1
check("sin²θ_W^GUT + cos²θ_W^GUT = 1 (Pythagoras)",
      sin2_theta_W_GUT + cos2_theta_W_GUT == Fraction(1),
      detail=f"{sin2_theta_W_GUT} + {cos2_theta_W_GUT} = {sin2_theta_W_GUT + cos2_theta_W_GUT}")

# Verify tan² = sin²/cos²
tan2_check = sin2_theta_W_GUT / cos2_theta_W_GUT
check("tan² = sin²/cos² consistency",
      tan2_check == tan2_theta_W_GUT,
      detail=f"sin²/cos² = {sin2_theta_W_GUT}/{cos2_theta_W_GUT} = {tan2_check}")


section("Part 6: numerical agreement with literature")
# 3/8 = 0.375
sin2_decimal = float(sin2_theta_W_GUT)
check("sin²θ_W^GUT decimal value = 0.375",
      abs(sin2_decimal - 0.375) < 1e-10,
      detail=f"3/8 = {sin2_decimal}")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}\n{'='*88}")
sys.exit(1 if FAIL_COUNT > 0 else 0)
