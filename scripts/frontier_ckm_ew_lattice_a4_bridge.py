#!/usr/bin/env python3
"""Audit the retained CKM-EW lattice A^4 bridge identity.

This runner deliberately salvages only the theorem-grade content:

    sin^2(theta_W)|_lattice = A^4 = 4/9

and the retained consistency equality

    A^2 = dim_fund(SU(2)) / dim_fund(SU(3)) = 2/3.

It explicitly does not certify an independent below-W2 derivation of the
Wolfenstein A^2 law.
"""

from __future__ import annotations

import re
import sys
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs" / "CKM_EW_LATTICE_A4_BRIDGE_RETAINED_IDENTITY_NOTE_2026-04-25.md"

AUTHORITY_FILES = {
    "minimal_axioms": ROOT / "docs" / "MINIMAL_AXIOMS_2026-04-11.md",
    "yt_ew": ROOT / "docs" / "YT_EW_COLOR_PROJECTION_THEOREM.md",
    "wolfenstein": ROOT / "docs" / "WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md",
    "ckm_counts": ROOT / "docs" / "CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md",
    "cl3_taste": ROOT / "docs" / "CL3_TASTE_GENERATION_THEOREM.md",
}

passes = 0
fails = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global passes, fails
    status = "PASS" if condition else "FAIL"
    suffix = f"  ({detail})" if detail else ""
    print(f"  [{status}] {name}{suffix}")
    if condition:
        passes += 1
    else:
        fails += 1


def section(title: str) -> None:
    print("\n" + "-" * 88)
    print(title)
    print("-" * 88)


def text(path: Path) -> str:
    return path.read_text() if path.exists() else ""


def status_line(content: str) -> str:
    for line in content.splitlines()[:40]:
        stripped = line.strip()
        if stripped.lower().startswith("**status:**") or stripped.lower().startswith("status:"):
            return re.sub(r"^\*?\*?status:\*?\*?\s*", "", stripped, flags=re.IGNORECASE)
    return ""


def contains_normalized(haystack: str, needle: str) -> bool:
    return " ".join(needle.split()).lower() in " ".join(haystack.split()).lower()


def extract_first_fraction(pattern: str, source: str) -> Fraction | None:
    match = re.search(pattern, source, re.IGNORECASE)
    if not match:
        return None
    return Fraction(int(match.group(1)), int(match.group(2)))


def main() -> int:
    print("=" * 88)
    print("CKM-EW lattice A^4 retained bridge audit")
    print(f"See {NOTE.relative_to(ROOT)}")
    print("=" * 88)

    note = text(NOTE)
    authorities = {name: text(path) for name, path in AUTHORITY_FILES.items()}

    section("Authority and status boundary")
    for name, path in AUTHORITY_FILES.items():
        check(f"authority exists: {path.relative_to(ROOT)}", path.exists())
        print(f"    extracted Status: {status_line(authorities[name])!r}")

    check("YT_EW authority is retained/derived",
          "retained" in status_line(authorities["yt_ew"]).lower()
          and "derived" in status_line(authorities["yt_ew"]).lower())
    check("Wolfenstein authority is retained",
          "retained" in status_line(authorities["wolfenstein"]).lower())
    check("CKM counts authority is retained",
          "retained" in status_line(authorities["ckm_counts"]).lower())
    check("CL3 taste remains support-tier",
          "support" in status_line(authorities["cl3_taste"]).lower())

    required_boundaries = [
        "not an `A^2`-below-`W2` derivation",
        "A2_BELOW_W2_DERIVATION_CLOSED=FALSE",
        "SUPPORT_TIER_PROMOTION=FALSE",
        "KOIDE_CLOSURE=FALSE",
        "Support-tier CL3 taste-generation readings are not used.",
    ]
    for phrase in required_boundaries:
        check(f"note states boundary: {phrase}", contains_normalized(note, phrase))

    forbidden_promotions = [
        "A2_BELOW_W2_DERIVATION_CLOSED=TRUE",
        "SUPPORT_TIER_PROMOTION=TRUE",
        "KOIDE_CLOSURE=TRUE",
        "therefore closes Koide",
    ]
    for phrase in forbidden_promotions:
        check(f"note avoids promotion: {phrase}", not contains_normalized(note, phrase))

    section("Retained EW lattice angle")
    yt = authorities["yt_ew"]
    has_g2 = "g_2^2" in yt and "1/(d+1)" in yt
    has_gY = "g_Y^2" in yt and "1/(d+2)" in yt
    has_quarters = "1/4" in yt
    has_fifths = "1/5" in yt
    check("YT_EW contains g_2^2 = 1/(d+1)", has_g2)
    check("YT_EW contains g_Y^2 = 1/(d+2)", has_gY)
    check("YT_EW contains retained 1/4 value", has_quarters)
    check("YT_EW contains retained 1/5 value", has_fifths)

    d = 3
    g2_sq = Fraction(1, d + 1)
    gY_sq = Fraction(1, d + 2)
    sin2_lattice = gY_sq / (gY_sq + g2_sq)
    check("g_2^2 = 1/4 at d=3", g2_sq == Fraction(1, 4))
    check("g_Y^2 = 1/5 at d=3", gY_sq == Fraction(1, 5))
    check("sin^2(theta_W)|_lattice = 4/9", sin2_lattice == Fraction(4, 9))

    section("Retained CKM A^4 side")
    wolf = authorities["wolfenstein"]
    counts = authorities["ckm_counts"]
    a_sq_from_w2 = extract_first_fraction(r"A\^2\s*=\s*(\d+)\s*/\s*(\d+)", wolf)
    n_pair_match = re.search(r"n[_\s]pair\s*=\s*(\d+)", counts, re.IGNORECASE)
    n_color_match = re.search(r"n[_\s]color\s*=\s*(\d+)", counts, re.IGNORECASE)
    n_pair = int(n_pair_match.group(1)) if n_pair_match else None
    n_color = int(n_color_match.group(1)) if n_color_match else None
    check("W2 authority contains A^2 = 2/3", a_sq_from_w2 == Fraction(2, 3))
    check("CKM counts authority contains n_pair = 2", n_pair == 2)
    check("CKM counts authority contains n_color = 3", n_color == 3)

    a_sq = Fraction(n_pair, n_color) if n_pair and n_color else Fraction(0)
    a_four = a_sq * a_sq
    check("A^2 = n_pair/n_color = 2/3", a_sq == Fraction(2, 3))
    check("A^4 = 4/9", a_four == Fraction(4, 9))
    check("retained EW-CKM identity sin^2(theta_W)|_lattice = A^4",
          sin2_lattice == a_four == Fraction(4, 9))

    section("Gauge-dimension consistency, not below-W2 derivation")
    minimal = authorities["minimal_axioms"]
    has_su2 = "SU(2)" in minimal and "exact native" in minimal
    has_su3 = "SU(3)" in minimal and "structural" in minimal
    dim_su2_fund = 2
    dim_su3_fund = 3
    gauge_ratio = Fraction(dim_su2_fund, dim_su3_fund)
    check("minimal axioms retain exact native SU(2)", has_su2)
    check("minimal axioms retain structural SU(3)", has_su3)
    check("dim_fund(SU(2)) / dim_fund(SU(3)) = 2/3",
          gauge_ratio == Fraction(2, 3))
    check("gauge-dimension ratio equals retained A^2 at values",
          gauge_ratio == a_sq == Fraction(2, 3))
    check("runner does not certify below-W2 A^2 derivation",
          contains_normalized(note, "not, by itself, a derivation of the Wolfenstein `A^2` law below `W2`"))

    section("Summary")
    print("  Certified:")
    print("    sin^2(theta_W)|_lattice = A^4 = 4/9")
    print("    A^2 = dim_fund(SU(2))/dim_fund(SU(3)) = 2/3 as retained consistency")
    print()
    print("  Not certified:")
    print("    independent below-W2 derivation of A^2, support-tier promotion,")
    print("    physical M_Z weak-angle prediction, or Koide closure.")

    print("\n" + "=" * 88)
    print(f"TOTAL: PASS={passes}, FAIL={fails}")
    print(f"PASSED: {passes}/{passes + fails}")
    print("=" * 88)
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
