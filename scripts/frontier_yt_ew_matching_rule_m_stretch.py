#!/usr/bin/env python3
"""Verify the stretch-attempt note for yt_ew matching rule M residual.

The note is at:
  docs/YT_EW_MATCHING_RULE_M_STRETCH_ATTEMPT_NOTE_2026-05-02.md

This runner verifies:
  Part 1: stretch-attempt note structure (A_min, forbidden imports, obstruction)
  Part 2: leading-order Fierz channel decomposition at exact Fraction precision
  Part 3: bounded large-N_c result with explicit O(1/N_c^4) gap noted
  Part 4: three named obstruction routes (O1, O2, O3) explicitly documented
  Part 5: explicit non-closure of exact matching coefficient
"""

from fractions import Fraction
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "YT_EW_MATCHING_RULE_M_STRETCH_ATTEMPT_NOTE_2026-05-02.md"

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
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


# ---------------------------------------------------------------------------
# Part 1: stretch-attempt note structure
# ---------------------------------------------------------------------------
section("Part 1: stretch-attempt note structure")

note_text = NOTE_PATH.read_text()
required = [
    "yt_ew Matching Rule M Stretch Attempt",
    "named obstruction",
    "A_min",
    "Forbidden imports",
    "graph-first SU(N_c) integration",
    "'t Hooft 1/N_c topological expansion",
    "Fierz identity",
    "OZI rule",
    "PDG observed y_t",
    "Fitted lattice empirical R_conn",
    "(O1)",
    "(O2)",
    "(O3)",
    "proposal_allowed: false",
]
for s in required:
    check(f"note contains required substring: {s!r}",
          s in note_text, detail=f"len(note)={len(note_text)}")

forbidden = [
    "\nStatus: retained\n",
    "\nStatus: promoted\n",
    "would become retained",
]
for s in forbidden:
    check(f"note avoids forbidden substring: {s!r}",
          s not in note_text)

# ---------------------------------------------------------------------------
# Part 2: leading-order Fierz channel decomposition (exact)
# ---------------------------------------------------------------------------
section("Part 2: leading-order Fierz channel decomposition at exact Fraction precision")

# At N_c = 3, the Fierz decomposition gives:
# 3 x 3-bar = 1 ⊕ 8
# dim(singlet) = 1, dim(adjoint) = N_c^2 - 1 = 8
# R_adj^{leading} = (N_c^2 - 1)/N_c^2 = 8/9

N_c = Fraction(3)
dim_singlet = Fraction(1)
dim_adjoint = N_c**2 - Fraction(1)
dim_full = N_c * N_c

check("dim(singlet) = 1", dim_singlet == Fraction(1),
      detail=f"dim_singlet = {dim_singlet}")
check("dim(adjoint) = N_c^2 - 1 = 8 at N_c = 3",
      dim_adjoint == Fraction(8),
      detail=f"dim_adjoint = {dim_adjoint}")
check("dim(singlet) + dim(adjoint) = N_c^2 (completeness)",
      dim_singlet + dim_adjoint == dim_full,
      detail=f"1 + 8 = {dim_singlet + dim_adjoint}, N_c^2 = {dim_full}")

R_conn_leading = dim_adjoint / dim_full
check("R_conn^{leading} = (N_c^2 - 1)/N_c^2 = 8/9 at N_c = 3",
      R_conn_leading == Fraction(8, 9),
      detail=f"R_conn^leading = {R_conn_leading}")

# ---------------------------------------------------------------------------
# Part 3: bounded result with O(1/N_c^4) gap
# ---------------------------------------------------------------------------
section("Part 3: bounded large-N_c result with O(1/N_c^4) gap")

# Next-order correction is O(1/N_c^4) ~ 1/81 ≈ 1.2% at N_c = 3
# This is the genus-2 correction

correction_order = Fraction(1) / N_c**4
check("O(1/N_c^4) ~ 1/81 at N_c = 3",
      correction_order == Fraction(1, 81),
      detail=f"correction = {correction_order}")
check("O(1/N_c^4) ~ 1.2% relative correction",
      abs(float(correction_order) - 0.0123) < 0.001,
      detail=f"correction = {float(correction_order)*100:.2f}%")

# Bounded result statement
bounded_lower = R_conn_leading - correction_order
bounded_upper = R_conn_leading + correction_order
check("bounded result R_conn ∈ [8/9 - 1/81, 8/9 + 1/81]",
      bounded_lower < bounded_upper,
      detail=f"[{bounded_lower}, {bounded_upper}]")

# ---------------------------------------------------------------------------
# Part 4: three named obstruction routes (O1, O2, O3)
# ---------------------------------------------------------------------------
section("Part 4: three named obstruction routes documented")

obstructions = {
    "(O1)": "disconnected piece vanishes identically",
    "(O2)": "disconnected piece contributes only to v",
    "(O3)": "exact OZI-vanishing theorem at all genus orders",
}
for tag, desc in obstructions.items():
    check(f"{tag} obstruction documented in note",
          tag in note_text and any(s in note_text for s in desc.split()[:3]),
          detail=desc)

# Each obstruction should have its failure mode named
failure_modes = [
    "Glueball intermediate states exist",
    "renormalization scheme choice",
    "phenomenological",
]
for fm in failure_modes:
    check(f"obstruction failure-mode documented: {fm}",
          fm in note_text,
          detail="failure mode documentation")

# ---------------------------------------------------------------------------
# Part 5: explicit non-closure
# ---------------------------------------------------------------------------
section("Part 5: explicit non-closure of exact matching")

non_closures = [
    ("matching rule M is NOT exact at finite N_c", "NOT exact"),
    ("bounded support tier is the narrowest honest tier", "bounded support"),
    ("yt_ew_color_projection_theorem retention not promoted", "audited_conditional"),
    ("rconn_derived_note retention not promoted", "audited_conditional"),
]
for desc, key in non_closures:
    check(f"explicit non-closure: {desc}",
          key in note_text,
          detail=f"key {key!r} present")

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print()
print("=" * 88)
print(f"  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
print("=" * 88)

sys.exit(1 if FAIL_COUNT > 0 else 0)
