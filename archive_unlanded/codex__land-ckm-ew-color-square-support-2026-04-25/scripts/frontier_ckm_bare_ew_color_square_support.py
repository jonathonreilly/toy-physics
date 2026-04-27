#!/usr/bin/env python3
"""Audit the bare EW / CKM color-square support identity.

This verifies exact algebra on already-retained package inputs. It does not
promote the identity into a new minimal-stack derivation of d=3.
"""

from __future__ import annotations

import re
import sys
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    suffix = f"  ({detail})" if detail else ""
    print(f"  [{status}] {name}{suffix}")
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1


def banner(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


def read_text(rel_path: str) -> str:
    path = ROOT / rel_path
    return path.read_text(encoding="utf-8") if path.exists() else ""


def extract_status(content: str) -> str:
    for line in content.splitlines()[:40]:
        stripped = line.strip()
        if stripped.lower().startswith("**status:**"):
            return stripped.split("**", 2)[-1].strip()
        if stripped.lower().startswith("status:"):
            return stripped.split(":", 1)[1].strip()
    return ""


def retained_or_framework_status(content: str) -> bool:
    status = extract_status(content).lower()
    return (
        "retained" in status
        or "derived -- standalone retained" in status
        or "current public framework memo" in status
    )


def audit_authorities() -> None:
    banner("Authority status extraction")
    authorities = [
        (
            "docs/YT_EW_COLOR_PROJECTION_THEOREM.md",
            ("derived", "retained"),
        ),
        (
            "docs/CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md",
            ("retained",),
        ),
        (
            "docs/MINIMAL_AXIOMS_2026-04-11.md",
            ("framework",),
        ),
        (
            "docs/WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md",
            ("retained",),
        ),
        (
            "docs/FRAMEWORK_BARE_ALPHA_3_ALPHA_EM_DIMENSION_FIXED_RATIO_SUPPORT_NOTE_2026-04-25.md",
            ("support",),
        ),
    ]
    for rel_path, required_words in authorities:
        text = read_text(rel_path)
        status = extract_status(text)
        print(f"  {rel_path}")
        print(f"    extracted status: {status!r}")
        check(f"authority exists: {Path(rel_path).name}", bool(text))
        check(
            f"status contains expected words: {Path(rel_path).name}",
            all(word in status.lower() for word in required_words),
        )
        if "SUPPORT_NOTE" not in rel_path:
            check(
                f"load-bearing authority is retained/framework: {Path(rel_path).name}",
                retained_or_framework_status(text),
            )


def audit_source_values() -> tuple[Fraction, Fraction, Fraction, int, int, int, int]:
    banner("Source value extraction")
    yt = read_text("docs/YT_EW_COLOR_PROJECTION_THEOREM.md")
    ckm = read_text("docs/CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md")

    has_g3 = bool(re.search(r"g_3\^2\s*=\s*1\b", yt))
    has_g2 = bool(re.search(r"g_2\^2\s*=\s*1/\(d\+1\)\s*=\s*1/4", yt))
    has_gy = bool(re.search(r"g_Y\^2\s*=\s*1/\(d\+2\)\s*=\s*1/5", yt))
    check("YT_EW contains g_3^2 = 1", has_g3)
    check("YT_EW contains g_2^2 = 1/(d+1) = 1/4", has_g2)
    check("YT_EW contains g_Y^2 = 1/(d+2) = 1/5", has_gy)

    n_pair = re.search(r"n[_\s]pair\s*=\s*(\d+)", ckm, re.IGNORECASE)
    n_color = re.search(r"n[_\s]color\s*=\s*(\d+)", ckm, re.IGNORECASE)
    n_quark = re.search(r"n[_\s]quark\s*=\s*[^=]*=\s*(\d+)|n[_\s]quark\s*=\s*(\d+)", ckm, re.IGNORECASE)
    n_pair_value = int(n_pair.group(1)) if n_pair else -1
    n_color_value = int(n_color.group(1)) if n_color else -1
    n_quark_value = int(n_quark.group(1) or n_quark.group(2)) if n_quark else -1
    check("CKM structural counts contain N_pair = 2", n_pair_value == 2)
    check("CKM structural counts contain N_color = 3", n_color_value == 3)
    check("CKM structural counts contain N_quark = 6", n_quark_value == 6)

    d = 3
    return (
        Fraction(1, 1),
        Fraction(1, d + 1),
        Fraction(1, d + 2),
        d,
        n_pair_value,
        n_color_value,
        n_quark_value,
    )


def audit_identities(
    g3_sq: Fraction,
    g2_sq: Fraction,
    gy_sq: Fraction,
    d: int,
    n_pair: int,
    n_color: int,
    n_quark: int,
) -> None:
    banner("Exact color-square support identities")
    inv_g3 = 1 / g3_sq
    inv_g2 = 1 / g2_sq
    inv_gy = 1 / gy_sq

    inv_sum = inv_g2 + inv_gy
    product = inv_g2 * inv_gy
    color_square = n_color**2
    structural_product = n_pair**2 * (n_quark - 1)
    discriminant = color_square**2 - 4 * structural_product
    adjoint_dim = n_color**2 - 1
    pythagorean = n_pair**2 + (n_quark - 1)

    print(f"  1/g_2^2 + 1/g_Y^2 = {inv_g2} + {inv_gy} = {inv_sum}")
    print(f"  N_color^2 = {n_color}^2 = {color_square}")
    check("S1 color-square identity", inv_sum == color_square)
    check("S1 equals 2d+3", inv_sum == 2 * d + 3)

    print(f"  (1/g_2^2)(1/g_Y^2) = {product}")
    print(f"  N_pair^2(N_quark-1) = {structural_product}")
    check("S2 product identity", product == structural_product)

    check("S3 inverse couplings are roots of x^2 - 9x + 20", inv_g2**2 - color_square * inv_g2 + structural_product == 0)
    check("S3 inverse hypercharge is root of x^2 - 9x + 20", inv_gy**2 - color_square * inv_gy + structural_product == 0)
    check("S4 unit discriminant", discriminant == 1)

    check("S5 adjoint-dimension identity", inv_sum - inv_g3 == adjoint_dim)
    check("S6 structural Pythagorean identity", pythagorean == color_square)

    sin2 = gy_sq / (g2_sq + gy_sq)
    cos2 = g2_sq / (g2_sq + gy_sq)
    check("weak-angle bare sin^2 = 4/9", sin2 == Fraction(4, 9))
    check("weak-angle bare cos^2 = 5/9", cos2 == Fraction(5, 9))
    check("weak-angle normalized structural sum", sin2 + cos2 == 1)


def audit_conditional_selector() -> None:
    banner("Conditional selector lemma, not retained derivation")
    solutions = [candidate for candidate in range(0, 20) if 2 * candidate + 3 == candidate**2]
    print("  If the color-square relation is promoted with N_color=d:")
    print("    2d+3=d^2 -> (d-3)(d+1)=0")
    print(f"  Non-negative integer solutions in 0..19: {solutions}")
    check("conditional selector has unique non-negative solution d=3", solutions == [3])


def audit_summary() -> None:
    banner("Scope summary")
    print("  Verified: exact EW/CKM support identities at retained package values.")
    print("  Verified: conditional color-square selector would pick d=3.")
    print("  Not claimed: a new minimal-stack derivation of d=3 or N_color=3.")
    print("  Not claimed: a direct low-energy weak-angle or alpha ratio observable.")
    print()
    print("See docs/CKM_BARE_EW_COLOR_SQUARE_IDENTITY_SUPPORT_NOTE_2026-04-25.md")


def main() -> int:
    print("=" * 88)
    print("Bare EW / CKM color-square support audit")
    print("=" * 88)

    audit_authorities()
    values = audit_source_values()
    audit_identities(*values)
    audit_conditional_selector()
    audit_summary()

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
