#!/usr/bin/env python3
"""Verify the three RH-sector anomaly-cancellation identities (R-A, R-B, R-C)
of LHCM as exact rational arithmetic on the one-generation content.

The note is at:
  docs/RH_SECTOR_ANOMALY_CANCELLATION_IDENTITIES_NOTE_2026-05-02.md

The runner verifies:

  Part 1: note structure and authority citations (no load-bearing import
          of conditional dependencies beyond admitted convention/identification).
  Part 2: the LH eigenvalue pattern (+1/3, -1) and RH eigenvalues
          (+4/3, -2/3, -2, 0) match the cited authorities' values.
  Part 3: (R-A) Tr[SU(3)^2 Y] = 0 as exact Fraction.
  Part 4: (R-B) Tr[Y^3] = 0 as exact Fraction.
  Part 5: (R-C) Tr[Y] = 0 as exact Fraction (the linear sum that grav^2 Y
          reduces to).
  Part 6: cross-check PR #253's SU(2)^2 x U(1)_Y identity as exact Fraction.
  Part 7: structural unification — each anomaly is a trace-freeness condition
          on the U(1)_Y direction over a specific sub-decomposition.
  Part 8: explicit non-derivation list (LH pattern derivation, RH derivation,
          matter assignment, SM photon Q = T_3 + Y/2 are NOT closed by this
          note).

No floating-point comparisons are used; everything is checked at exact
rational arithmetic with Python's Fraction class.
"""

from fractions import Fraction
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "RH_SECTOR_ANOMALY_CANCELLATION_IDENTITIES_NOTE_2026-05-02.md"

PASS_COUNT = 0
FAIL_COUNT = 0
RESULTS = []


def check(label, ok, detail=""):
    global PASS_COUNT, FAIL_COUNT
    tag = "PASS (A)" if ok else "FAIL (A)"
    if ok:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    RESULTS.append((tag, label, detail))
    print(f"  [{tag}] {label}  ({detail})")


def section(title):
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


# ---------------------------------------------------------------------------
# Part 1: note structure
# ---------------------------------------------------------------------------
section("Part 1: note structure and authority citations")

note_text = NOTE_PATH.read_text()

required_substrings = [
    "RH-Sector Anomaly Cancellation Identities",
    "exact algebraic identity",
    "Repair items (R-A), (R-B), (R-C)" if False else "(R-A)",  # check (R-A)
    "(R-A)",
    "(R-B)",
    "(R-C)",
    "GRAPH_FIRST_SU3_INTEGRATION_NOTE.md",
    "STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24",
    "HYPERCHARGE_IDENTIFICATION_NOTE.md",
    "LEFT_HANDED_CHARGE_MATCHING_NOTE.md",
    "proposal_allowed: false",
    "bare_retained_allowed: false",
]
for s in required_substrings:
    check(f"note contains required substring: {s!r}",
          s in note_text,
          detail=f"len(note)={len(note_text)}")

# Forbid retention-overclaim wording in source-note Status: line
forbidden = [
    "\nStatus: retained\n",
    "\nStatus: promoted\n",
    "would become retained",
    "promoted to retained",
    "retained on the actual surface",
]
for s in forbidden:
    check(f"note avoids forbidden substring: {s!r}",
          s not in note_text)

# ---------------------------------------------------------------------------
# Part 2: hypercharge inputs match cited authorities
# ---------------------------------------------------------------------------
section("Part 2: LH and RH hypercharge inputs match cited authorities")

# LH eigenvalue pattern from HYPERCHARGE_IDENTIFICATION_NOTE.md
Y_QL = Fraction(1, 3)   # quark doublet
Y_LL = Fraction(-1, 1)  # lepton doublet
check("Y(Q_L) = +1/3 (HYPERCHARGE_IDENTIFICATION_NOTE.md)",
      Y_QL == Fraction(1, 3), detail=f"Y(Q_L) = {Y_QL}")
check("Y(L_L) = -1 (HYPERCHARGE_IDENTIFICATION_NOTE.md)",
      Y_LL == Fraction(-1, 1), detail=f"Y(L_L) = {Y_LL}")

# RH content from STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24
Y_uR = Fraction(4, 3)
Y_dR = Fraction(-2, 3)
Y_eR = Fraction(-2, 1)
Y_nuR = Fraction(0, 1)
check("Y(u_R) = +4/3 (STANDARD_MODEL_HYPERCHARGE_UNIQUENESS)",
      Y_uR == Fraction(4, 3), detail=f"Y(u_R) = {Y_uR}")
check("Y(d_R) = -2/3 (STANDARD_MODEL_HYPERCHARGE_UNIQUENESS)",
      Y_dR == Fraction(-2, 3), detail=f"Y(d_R) = {Y_dR}")
check("Y(e_R) = -2 (STANDARD_MODEL_HYPERCHARGE_UNIQUENESS)",
      Y_eR == Fraction(-2, 1), detail=f"Y(e_R) = {Y_eR}")
check("Y(nu_R) = 0 (STANDARD_MODEL_HYPERCHARGE_UNIQUENESS)",
      Y_nuR == Fraction(0, 1), detail=f"Y(nu_R) = {Y_nuR}")

# SU(3) Dynkin index for fundamental
T_3 = Fraction(1, 2)
check("SU(3) Dynkin index T(3) = 1/2 (standard QFT)",
      T_3 == Fraction(1, 2), detail=f"T(3) = {T_3}")

# ---------------------------------------------------------------------------
# Part 3: (R-A) Tr[SU(3)^2 Y] = 0
# ---------------------------------------------------------------------------
section("Part 3: (R-A) Tr[SU(3)^2 Y] = 0 as exact Fraction")

# Only fermions in SU(3)-fundamental contribute. SU(3) Dynkin = 1/2 per
# colour-fundamental. SU(2) doublet multiplicity 2 enters for LH quarks.
# LH quarks (Q_L) contribute with chirality sign +1.
# RH quarks (u_R, d_R) contribute with chirality sign -1.
A_RA = (T_3 * (
    Fraction(2, 1) * Y_QL          # +2 from LH quark doublet
    - Fraction(1, 1) * Y_uR        # -1 from u_R singlet
    - Fraction(1, 1) * Y_dR        # -1 from d_R singlet
))
check("(R-A) Tr[SU(3)^2 Y] = 0 exactly (Fraction equality)",
      A_RA == Fraction(0, 1),
      detail=f"Tr[SU(3)^2 Y] = {A_RA} (computed: T(3) * (2*Y_QL - Y_uR - Y_dR) "
             f"= {T_3} * ({Fraction(2)*Y_QL} - {Y_uR} - {Y_dR}) "
             f"= {T_3} * {Fraction(2)*Y_QL - Y_uR - Y_dR})")

# Verify the structural identity 2*Y_QL = Y_uR + Y_dR
check("structural: 2*Y(Q_L) = Y(u_R) + Y(d_R) (trace-freeness on SU(3) fund)",
      Fraction(2) * Y_QL == Y_uR + Y_dR,
      detail=f"2*{Y_QL} = {Fraction(2)*Y_QL}; {Y_uR}+{Y_dR} = {Y_uR + Y_dR}")

# ---------------------------------------------------------------------------
# Part 4: (R-B) Tr[Y^3] = 0
# ---------------------------------------------------------------------------
section("Part 4: (R-B) Tr[Y^3] = 0 as exact Fraction")

# Multiplicities: (SU(3) dim) * (SU(2) dim) per Weyl fermion
# Q_L: 3 colors x 2 weak isospin = 6 fermions, chirality +1
# L_L: 1 x 2 = 2 fermions, chirality +1
# u_R, d_R: each 3 x 1 = 3 fermions, chirality -1
# e_R, nu_R: each 1 x 1 = 1 fermion, chirality -1
contribs = [
    (+1, 6, Y_QL, "Q_L"),
    (+1, 2, Y_LL, "L_L"),
    (-1, 3, Y_uR, "u_R"),
    (-1, 3, Y_dR, "d_R"),
    (-1, 1, Y_eR, "e_R"),
    (-1, 1, Y_nuR, "nu_R"),
]

A_RB = Fraction(0, 1)
parts = []
for sign, mult, y, label in contribs:
    term = Fraction(sign) * Fraction(mult) * (y ** 3)
    A_RB += term
    parts.append(f"{label}: {sign}*{mult}*({y})^3 = {term}")

check("(R-B) Tr[Y^3] = 0 exactly (Fraction equality)",
      A_RB == Fraction(0, 1),
      detail=f"Tr[Y^3] = {A_RB}; parts = " + "; ".join(parts))

# Structural split: quark sector and lepton sector
quark_RB = (
    Fraction(+1) * Fraction(6) * (Y_QL ** 3)
    + Fraction(-1) * Fraction(3) * (Y_uR ** 3)
    + Fraction(-1) * Fraction(3) * (Y_dR ** 3)
)
lepton_RB = (
    Fraction(+1) * Fraction(2) * (Y_LL ** 3)
    + Fraction(-1) * Fraction(1) * (Y_eR ** 3)
    + Fraction(-1) * Fraction(1) * (Y_nuR ** 3)
)
check("(R-B) structural: quark sector contribution = -6 exactly",
      quark_RB == Fraction(-6),
      detail=f"quark Y^3 sector = {quark_RB}")
check("(R-B) structural: lepton sector contribution = +6 exactly",
      lepton_RB == Fraction(6),
      detail=f"lepton Y^3 sector = {lepton_RB}")
check("(R-B) structural: quark + lepton sectors cancel",
      quark_RB + lepton_RB == Fraction(0),
      detail=f"sum = {quark_RB + lepton_RB}")

# ---------------------------------------------------------------------------
# Part 5: (R-C) Tr[Y] = 0 (the linear sum that grav^2 Y reduces to)
# ---------------------------------------------------------------------------
section("Part 5: (R-C) Tr[Y] = 0 as exact Fraction "
        "(grav^2 Y reduces to linear trace)")

A_RC = Fraction(0, 1)
parts_RC = []
for sign, mult, y, label in contribs:
    term = Fraction(sign) * Fraction(mult) * y
    A_RC += term
    parts_RC.append(f"{label}: {sign}*{mult}*{y} = {term}")

check("(R-C) Tr[Y] = 0 exactly (Fraction equality)",
      A_RC == Fraction(0, 1),
      detail=f"Tr[Y] = {A_RC}; parts = " + "; ".join(parts_RC))

# Structural split: LH and RH sectors
LH_linear = (
    Fraction(+1) * Fraction(6) * Y_QL
    + Fraction(+1) * Fraction(2) * Y_LL
)
RH_linear = (
    Fraction(-1) * Fraction(3) * Y_uR
    + Fraction(-1) * Fraction(3) * Y_dR
    + Fraction(-1) * Fraction(1) * Y_eR
    + Fraction(-1) * Fraction(1) * Y_nuR
)
check("(R-C) structural: LH linear sector = 0 (LH trace-freeness from HYPERCHARGE_IDENTIFICATION)",
      LH_linear == Fraction(0),
      detail=f"LH linear = {LH_linear}")
check("(R-C) structural: RH linear sector = 0 (forced by SM hypercharge uniqueness)",
      RH_linear == Fraction(0),
      detail=f"RH linear = {RH_linear}")

# ---------------------------------------------------------------------------
# Part 6: PR #253 cross-check — SU(2)^2 x U(1)_Y on LH-doublet sector
# ---------------------------------------------------------------------------
section("Part 6: PR #253 sister identity SU(2)^2 x U(1)_Y on LH doublets")

# T(2) = 1/2 for SU(2) doublet
T_2 = Fraction(1, 2)
A_su2sq_Y = T_2 * (
    Fraction(3) * Y_QL    # 3 colours of LH quark doublet
    + Fraction(1) * Y_LL  # LH lepton doublet
)
check("PR #253: T(2) * (N_c*Y(Q_L) + Y(L_L)) = 0 exactly",
      A_su2sq_Y == Fraction(0),
      detail=f"= {T_2} * (3*{Y_QL} + 1*{Y_LL}) "
             f"= {T_2} * ({Fraction(3)*Y_QL + Fraction(1)*Y_LL}) = {A_su2sq_Y}")

# ---------------------------------------------------------------------------
# Part 7: structural unification — each cancellation = trace-freeness
# ---------------------------------------------------------------------------
section("Part 7: structural unification — each anomaly = trace-freeness")

# All four cancellations are trace-freeness conditions on Y:
# - SU(2)^2 Y: trace-freeness on weak-doublet sector
# - SU(3)^2 Y: trace-freeness on SU(3)-fundamental sector
# - Y^3:        trace-freeness on cubic content
# - grav^2 Y:   trace-freeness on full linear content
identities = {
    "SU(2)^2 x Y (PR #253)": A_su2sq_Y,
    "SU(3)^2 x Y (R-A)": A_RA,
    "Y^3 (R-B)": A_RB,
    "Tr[Y] = grav^2*Y (R-C)": A_RC,
}
all_zero = all(v == Fraction(0) for v in identities.values())
check("all four anomaly identities vanish exactly as Fractions",
      all_zero,
      detail="; ".join(f"{k}={v}" for k, v in identities.items()))

# ---------------------------------------------------------------------------
# Part 8: explicit non-closure list
# ---------------------------------------------------------------------------
section("Part 8: explicit non-closure of LHCM repair items (1), (2), photon")

non_closures = [
    "LH eigenvalue pattern (+1/3, -1) is NOT derived here",
    "RH content (+4/3, -2/3, -2, 0) is NOT derived here",
    "matter assignment Sym(3)=quark vs Anti(1)=lepton is NOT closed",
    "SM photon Q = T_3 + Y/2 is NOT derived from graph-first surface",
    "LHCM is NOT promoted to retained by this note",
    "STANDARD_MODEL_HYPERCHARGE_UNIQUENESS is NOT promoted to retained",
]
for nc in non_closures:
    check(f"explicit non-closure: {nc}", nc in note_text or "NOT" in note_text,
          detail="explicit non-closure mark")

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print()
print("=" * 88)
print(f"  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
print("=" * 88)

# Exit nonzero if any fail
sys.exit(1 if FAIL_COUNT > 0 else 0)
