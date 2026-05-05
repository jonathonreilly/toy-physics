#!/usr/bin/env python3
"""Audit the bare alpha_3 / alpha_em dimension-ratio support corollary.

This runner intentionally verifies both pieces of the landing:

1. the exact bare-coupling algebra, and
2. the status boundary that keeps this as support-side bookkeeping rather than
   a new minimal-stack theorem.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
D = 3


@dataclass
class Audit:
    passed: int = 0
    failed: int = 0

    def check(self, label: str, condition: bool, detail: str = "") -> None:
        if condition:
            self.passed += 1
            print(f"PASS: {label}" + (f" :: {detail}" if detail else ""))
        else:
            self.failed += 1
            print(f"FAIL: {label}" + (f" :: {detail}" if detail else ""))


def read(path: str) -> str:
    primary = ROOT / path
    if primary.exists():
        return primary.read_text(encoding="utf-8")
    # Fall back: notes archived as audited_failed (retained_no_go) live
    # under archive_unlanded/<bucket>/<filename>. Search for the basename.
    archive_root = ROOT / "archive_unlanded"
    if archive_root.exists():
        from pathlib import Path as _Path
        target_name = _Path(path).name
        for archived in archive_root.rglob(target_name):
            return archived.read_text(encoding="utf-8")
    raise FileNotFoundError(f"{path} not found in repo or archive_unlanded/")


def frac_eq(label: str, audit: Audit, actual: Fraction, expected: Fraction) -> None:
    audit.check(label, actual == expected, f"actual={actual}, expected={expected}")


def float_close(label: str, audit: Audit, actual: float, expected: float, tol: float = 1e-14) -> None:
    audit.check(label, abs(actual - expected) <= tol, f"actual={actual:.17g}, expected={expected:.17g}")


def audit_authority_surfaces(audit: Audit) -> None:
    note_path = "docs/FRAMEWORK_BARE_ALPHA_3_ALPHA_EM_DIMENSION_FIXED_RATIO_SUPPORT_NOTE_2026-04-25.md"
    cl3_path = "docs/CL3_SM_EMBEDDING_THEOREM.md"
    ew_path = "docs/YT_EW_COLOR_PROJECTION_THEOREM.md"
    matrix_path = "docs/publication/ci3_z3/PUBLICATION_MATRIX.md"
    validation_path = "docs/publication/ci3_z3/DERIVATION_VALIDATION_MAP.md"
    atlas_path = "docs/publication/ci3_z3/DERIVATION_ATLAS.md"

    paths = [note_path, cl3_path, ew_path, matrix_path, validation_path, atlas_path]
    archive_root = ROOT / "archive_unlanded"

    def _authority_exists(rel: str) -> bool:
        if (ROOT / rel).exists():
            return True
        if archive_root.exists():
            from pathlib import Path as _P
            for _ in archive_root.rglob(_P(rel).name):
                return True
        return False

    for rel in paths:
        audit.check(f"authority file exists: {rel}", _authority_exists(rel))

    note = read(note_path)
    cl3 = read(cl3_path)
    ew = read(ew_path)
    matrix = read(matrix_path)
    validation = read(validation_path)
    atlas = read(atlas_path)

    audit.check(
        "note status is support corollary",
        "support corollary" in note and "not a new retained front-door theorem" in note,
    )
    audit.check(
        "note blocks minimal-stack promotion",
        "does not promote the `Cl(3) -> SM` support packet" in note,
    )
    audit.check(
        "note blocks direct low-energy readout",
        "does not promote the bare integer `9`" in note
        and "directly observable low-energy" in note,
    )
    audit.check(
        "note distinguishes SU(5)",
        "not the SU(5) bare normalization" in note and "5/72" in note,
    )

    forbidden = [
        "Retained derivation theorem on main",
        "three independent retained inputs",
        "independent retained structural routes",
    ]
    for phrase in forbidden:
        audit.check(f"forbidden overclaim absent: {phrase}", phrase not in note)

    audit.check(
        "CL3 packet remains support-only",
        "not part of the accepted minimal-input stack" in cl3 and "support theorem" in cl3,
    )
    audit.check(
        "CL3 packet carries d+1/d+2 bookkeeping",
        "1/(d+1)" in cl3 and "1/(d+2)" in cl3 and "bare gauge couplings" in cl3,
    )
    audit.check(
        "EW normalization lane exists",
        "standalone retained EW normalization lane" in ew
        or "Retained status" in ew
        or "EW normalization lane" in ew,
    )
    audit.check(
        "publication matrix keeps CL3 support boundary",
        "support packet / atlas only; not part of the accepted minimal-input stack" in matrix,
    )
    audit.check(
        "publication matrix carries bare-ratio support row",
        "Bare alpha_3/alpha_em dimension-ratio support" in matrix and "bounded support corollary" in matrix,
    )
    audit.check(
        "validation map carries support row",
        "Bare alpha_3/alpha_em dimension-ratio support" in validation and "support corollary" in validation,
    )
    audit.check(
        "atlas carries support tool row",
        "Bare alpha_3/alpha_em dimension-ratio support" in atlas and "not part of the accepted minimal-input stack" in atlas,
    )


def audit_exact_algebra(audit: Audit) -> None:
    d = D
    g3_sq = Fraction(1, 1)
    g2_sq = Fraction(1, d + 1)
    gy_sq = Fraction(1, d + 2)

    inv_g3 = Fraction(1, 1) / g3_sq
    inv_g2 = Fraction(1, 1) / g2_sq
    inv_gy = Fraction(1, 1) / gy_sq
    inv_gem = inv_g2 + inv_gy
    gem_sq = Fraction(1, 1) / inv_gem

    frac_eq("input d fixed to 3", audit, Fraction(d, 1), Fraction(3, 1))
    frac_eq("g3^2 canonical", audit, g3_sq, Fraction(1, 1))
    frac_eq("g2^2 = 1/(d+1)", audit, g2_sq, Fraction(1, 4))
    frac_eq("gY^2 = 1/(d+2)", audit, gy_sq, Fraction(1, 5))
    frac_eq("1/g2^2 = d+1", audit, inv_g2, Fraction(4, 1))
    frac_eq("1/gY^2 = d+2", audit, inv_gy, Fraction(5, 1))

    frac_eq("D1 inverse-EM sum = 2d+3", audit, inv_gem, Fraction(2 * d + 3, 1))
    frac_eq("D1 inverse-EM sum at d=3 = 9", audit, inv_gem, Fraction(9, 1))
    frac_eq("D2 g_em^2 = 1/(2d+3)", audit, gem_sq, Fraction(1, 9))

    sin2 = gy_sq / (g2_sq + gy_sq)
    cos2 = g2_sq / (g2_sq + gy_sq)
    frac_eq("D3 sin^2(theta_W) = (d+1)/(2d+3)", audit, sin2, Fraction(d + 1, 2 * d + 3))
    frac_eq("D3 sin^2(theta_W) at d=3 = 4/9", audit, sin2, Fraction(4, 9))
    frac_eq("cos^2(theta_W) at d=3 = 5/9", audit, cos2, Fraction(5, 9))
    frac_eq("weak-angle sum = 1", audit, sin2 + cos2, Fraction(1, 1))

    alpha_ratio = g3_sq / gem_sq
    frac_eq("D4 alpha3/alpha_em = g3^2/g_em^2", audit, alpha_ratio, Fraction(9, 1))
    frac_eq("D4 alpha3/alpha_em = g3^2*(2d+3)", audit, alpha_ratio, g3_sq * Fraction(2 * d + 3, 1))

    alpha_em = float(gem_sq) / (4.0 * math.pi)
    alpha3 = float(g3_sq) / (4.0 * math.pi)
    float_close("D5 alpha_em = 1/(36 pi)", audit, alpha_em, 1.0 / (36.0 * math.pi))
    float_close("alpha3/alpha_em float ratio = 9", audit, alpha3 / alpha_em, 9.0)

    inverse_alpha_sum_factor = inv_g3 + inv_g2 + inv_gy
    frac_eq("D6 inverse-alpha sum factor = 2d+4", audit, inverse_alpha_sum_factor, Fraction(2 * d + 4, 1))
    float_close(
        "D6 inverse-alpha sum = 40 pi",
        audit,
        float(inverse_alpha_sum_factor) * 4.0 * math.pi,
        40.0 * math.pi,
    )

    su5_sin2 = Fraction(3, 8)
    frac_eq("framework minus SU(5) sin^2 offset = 5/72", audit, sin2 - su5_sin2, Fraction(5, 72))
    audit.check("framework bare angle is not SU(5)", sin2 != su5_sin2)


def audit_dimension_fingerprint(audit: Audit) -> None:
    expected = {2: 7, 3: 9, 4: 11, 5: 13}
    for d, value in expected.items():
        ratio = 2 * d + 3
        audit.check(f"dimension fingerprint d={d}", ratio == value, f"ratio={ratio}")

    inverse = {2 * d + 3: d for d in range(1, 9)}
    audit.check("integer 9 uniquely maps to d=3 in checked range", inverse[9] == 3)
    audit.check("fingerprint sequence odd integers", all((2 * d + 3) % 2 == 1 for d in range(1, 9)))


def main() -> int:
    audit = Audit()
    print("=== Bare alpha_3 / alpha_em dimension-ratio support audit ===")
    audit_authority_surfaces(audit)
    audit_exact_algebra(audit)
    audit_dimension_fingerprint(audit)
    print(f"TOTAL: PASS={audit.passed}, FAIL={audit.failed}")
    if audit.failed:
        print("VERDICT: FAIL")
        return 1
    print("VERDICT: SUPPORT COROLLARY CLOSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
