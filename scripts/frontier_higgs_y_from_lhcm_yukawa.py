#!/usr/bin/env python3
"""Verify Higgs Y_H = +1 derivation from LHCM-derived hypercharges and
Yukawa structure at exact Fraction precision."""

from fractions import Fraction
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "HIGGS_Y_FROM_LHCM_AND_YUKAWA_STRUCTURE_NOTE_2026-05-02.md"

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


# LHCM-derived hypercharges (exact rational, cycles 1-3)
Y_QL = Fraction(1, 3)
Y_LL = Fraction(-1)
Y_uR = Fraction(4, 3)
Y_dR = Fraction(-2, 3)
Y_eR = Fraction(-2)
Y_nuR = Fraction(0)


section("Part 1: note structure")
note_text = NOTE_PATH.read_text()
required = [
    "Higgs Y_H from LHCM-Derived Hypercharges and Yukawa Structure",
    "Y_H  =  +1",
    "Y(H)  =  Y(u_R) − Y(Q_L)",
    "Y(H) = Y(Q_L) − Y(d_R)",  # in inline backticks, single space
    "Y(H)  =  Y(L_L) − Y(e_R)",
    "Q̄_L · H̃ · u_R",
    "Q̄_L · H · d_R",
    "L̄_L · H · e_R",
    "proposal_allowed: false",
]
for s in required:
    check(f"contains: {s!r}", s in note_text)


section("Part 2: Y_H derivation from up-quark Yukawa")
# Q̄_L · H̃ · u_R: -Y(Q_L) + Y(H̃) + Y(u_R) = 0
# Y(H̃) = -Y(H), so -Y(Q_L) - Y(H) + Y(u_R) = 0
# Y(H) = Y(u_R) - Y(Q_L)
Y_H_from_up = Y_uR - Y_QL
check("up-quark Yukawa: Y(H) = Y(u_R) − Y(Q_L) = +1",
      Y_H_from_up == Fraction(1),
      detail=f"Y(H) = {Y_uR} − {Y_QL} = {Y_H_from_up}")


section("Part 3: Y_H derivation from down-quark Yukawa")
# Q̄_L · H · d_R: -Y(Q_L) + Y(H) + Y(d_R) = 0
# Y(H) = Y(Q_L) - Y(d_R)
Y_H_from_down = Y_QL - Y_dR
check("down-quark Yukawa: Y(H) = Y(Q_L) − Y(d_R) = +1",
      Y_H_from_down == Fraction(1),
      detail=f"Y(H) = {Y_QL} − ({Y_dR}) = {Y_H_from_down}")


section("Part 4: Y_H derivation from charged-lepton Yukawa")
# L̄_L · H · e_R: -Y(L_L) + Y(H) + Y(e_R) = 0
# Y(H) = Y(L_L) - Y(e_R)
Y_H_from_lepton = Y_LL - Y_eR
check("charged-lepton Yukawa: Y(H) = Y(L_L) − Y(e_R) = +1",
      Y_H_from_lepton == Fraction(1),
      detail=f"Y(H) = {Y_LL} − ({Y_eR}) = {Y_H_from_lepton}")


section("Part 5: Y_H derivation from neutral-lepton Yukawa (ν_R)")
# L̄_L · H̃ · ν_R: -Y(L_L) + Y(H̃) + Y(ν_R) = 0
# Y(H̃) = -Y(H), so Y(H) = Y(ν_R) - Y(L_L)
Y_H_from_neutral_lepton = Y_nuR - Y_LL
check("neutral-lepton Yukawa: Y(H) = Y(ν_R) − Y(L_L) = +1",
      Y_H_from_neutral_lepton == Fraction(1),
      detail=f"Y(H) = {Y_nuR} − ({Y_LL}) = {Y_H_from_neutral_lepton}")


section("Part 6: cross-check consistency across all four Yukawa couplings")
all_Y_H = [Y_H_from_up, Y_H_from_down, Y_H_from_lepton, Y_H_from_neutral_lepton]
all_consistent = all(y == Fraction(1) for y in all_Y_H)
check("all four Yukawa couplings give Y_H = +1 consistently",
      all_consistent,
      detail=f"values = {all_Y_H}")


section("Part 7: electric charge of Higgs")
# Q(H_+) = T_3(H_+) + Y(H)/2 = +1/2 + 1/2 = +1
# Q(H_0) = T_3(H_0) + Y(H)/2 = -1/2 + 1/2 = 0
T_3_Hplus = Fraction(1, 2)
T_3_H0 = Fraction(-1, 2)
Q_Hplus = T_3_Hplus + Y_H_from_up / Fraction(2)
Q_H0 = T_3_H0 + Y_H_from_up / Fraction(2)
check("Q(H+) = T_3(H+) + Y(H)/2 = +1 (charged Higgs)",
      Q_Hplus == Fraction(1),
      detail=f"+1/2 + 1/2 = {Q_Hplus}")
check("Q(H0) = T_3(H0) + Y(H)/2 = 0 (neutral Higgs)",
      Q_H0 == Fraction(0),
      detail=f"-1/2 + 1/2 = {Q_H0}")


section("Part 8: explicit non-closure")
non_closures = [
    "SM Yukawa coupling form itself",
    "LHCM",
    "STANDARD_MODEL_HYPERCHARGE_UNIQUENESS",
    "Higgs VEV",
]
for nc in non_closures:
    check(f"non-closure: {nc}",
          nc in note_text)

print(f"\n{'='*88}\n  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}\n{'='*88}")
sys.exit(1 if FAIL_COUNT > 0 else 0)
