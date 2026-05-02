#!/usr/bin/env python3
"""Verify Tr[Y²] = 40/3 over full one-generation content + SU(5) GUT
normalization consistency at exact Fraction precision."""

from fractions import Fraction
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "FULL_Y_SQUARED_TRACE_SU5_GUT_NOTE_2026-05-02.md"

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


# LHCM-derived hypercharges (Convention A: Q = T_3 + Y/2)
Y_QL = Fraction(1, 3)
Y_LL = Fraction(-1)
Y_uR = Fraction(4, 3)
Y_dR = Fraction(-2, 3)
Y_eR = Fraction(-2)
Y_nuR = Fraction(0)


section("Part 1: note structure")
note_text = NOTE_PATH.read_text()
required = [
    "Full One-Generation Tr[Y²] = 40/3",
    "SU(5) GUT Normalization",
    "8/3",
    "32/3",
    "40/3",
    "Convention A",
    "Convention B",
    "proposal_allowed: false",
]
for s in required:
    check(f"contains: {s!r}", s in note_text)


section("Part 2: LH-only Tr[Y²] = 8/3 (sister consistency)")
trY2_LH = Fraction(6) * Y_QL**2 + Fraction(2) * Y_LL**2
check("Tr[Y²]_LH = 6·(1/3)² + 2·(-1)² = 8/3 exactly",
      trY2_LH == Fraction(8, 3),
      detail=f"Tr[Y²]_LH = {trY2_LH}")


section("Part 3: RH-only Tr[Y²] = 32/3")
trY2_RH = (
    Fraction(3) * Y_uR**2
    + Fraction(3) * Y_dR**2
    + Fraction(1) * Y_eR**2
    + Fraction(1) * Y_nuR**2
)
check("Tr[Y²]_RH = 3·(4/3)² + 3·(-2/3)² + (-2)² + 0² = 32/3 exactly",
      trY2_RH == Fraction(32, 3),
      detail=f"Tr[Y²]_RH = {trY2_RH}")


section("Part 4: full one-generation Tr[Y²] = 40/3")
trY2_full = trY2_LH + trY2_RH
check("Tr[Y²]_full = Tr[Y²]_LH + Tr[Y²]_RH = 8/3 + 32/3 = 40/3 exactly",
      trY2_full == Fraction(40, 3),
      detail=f"Tr[Y²]_full = {trY2_full}")


section("Part 5: SU(5) GUT normalization Y_GUT² = (3/5) Y²")
gut_factor = Fraction(3, 5)
trY_GUT2_full = gut_factor * trY2_full
check("Tr[Y_GUT²] = (3/5) · 40/3 = 8 (Convention A full)",
      trY_GUT2_full == Fraction(8),
      detail=f"Tr[Y_GUT²]_full = {trY_GUT2_full}")


section("Part 6: Convention A → Convention B factor of 4")
# Convention B: Y_B = Y_A / 2, so Tr[Y_B²] = Tr[Y_A²] / 4
trY2_full_B = trY2_full / Fraction(4)
check("Tr[Y²]_B = Tr[Y²]_A / 4 = 40/3 / 4 = 10/3",
      trY2_full_B == Fraction(10, 3),
      detail=f"Tr[Y²]_B = {trY2_full_B}")
# In Convention B, SU(5) consistency check
trY_GUT2_full_B = gut_factor * trY2_full_B
check("Tr[Y_GUT²]_B = (3/5) · 10/3 = 2 (per Weyl family in 5̄+10)",
      trY_GUT2_full_B == Fraction(2),
      detail=f"Tr[Y_GUT²]_B = {trY_GUT2_full_B}")


section("Part 7: SU(3) Casimir consistency in SU(5)")
# Per Weyl family, Tr[T_a²]_5̄ + Tr[T_a²]_10 should equal 2 (matches Tr[Y_GUT²])
# T(5̄) = 1/2 for fundamental of SU(5) restricted to SU(3): contribution = 1/2
# T(10) = 3/2 from antisymmetric of fundamental: contribution = 3/2
# Total per Weyl family: 1/2 + 3/2 = 2 — matches Tr[Y_GUT²]_B = 2
T_5bar = Fraction(1, 2)
T_10 = Fraction(3, 2)
TT_total = T_5bar + T_10
check("Tr[T_a²]_5̄+10 = 1/2 + 3/2 = 2 per Weyl family",
      TT_total == Fraction(2),
      detail=f"Tr[T_a²] = {TT_total}")
check("SU(5) consistency: Tr[Y_GUT²] = Tr[T_a²] = 2 per Weyl family (Convention B)",
      trY_GUT2_full_B == TT_total,
      detail=f"Y_GUT² = {trY_GUT2_full_B}, T_a² = {TT_total}")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}\n{'='*88}")
sys.exit(1 if FAIL_COUNT > 0 else 0)
