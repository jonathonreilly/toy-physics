#!/usr/bin/env python3
"""Audit the EW alpha lattice adjoint-dimension support corollary.

This runner verifies the algebra after the retained EW-normalization
bookkeeping and leading R_conn support factor are accepted. It also verifies
that the note is framed as support, not as a new retained theorem or a direct
low-energy observable.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTE = "docs/EW_ALPHA_LATTICE_ADJOINT_DIM_SUPPORT_NOTE_2026-04-25.md"


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


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def frac_eq(audit: Audit, label: str, actual: Fraction, expected: Fraction) -> None:
    audit.check(label, actual == expected, f"actual={actual}, expected={expected}")


def float_close(
    audit: Audit,
    label: str,
    actual: float,
    expected: float,
    tol: float = 1e-14,
) -> None:
    audit.check(label, abs(actual - expected) <= tol, f"actual={actual:.17g}, expected={expected:.17g}")


def audit_authority_boundary(audit: Audit) -> None:
    paths = [
        NOTE,
        "docs/YT_EW_COLOR_PROJECTION_THEOREM.md",
        "docs/MINIMAL_AXIOMS_2026-04-11.md",
        "docs/CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md",
        "docs/FRAMEWORK_BARE_ALPHA_3_ALPHA_EM_DIMENSION_FIXED_RATIO_SUPPORT_NOTE_2026-04-25.md",
        "docs/CANONICAL_HARNESS_INDEX.md",
        "docs/publication/ci3_z3/RESULTS_INDEX.md",
        "docs/publication/ci3_z3/CLAIMS_TABLE.md",
        "docs/publication/ci3_z3/PUBLICATION_MATRIX.md",
        "docs/publication/ci3_z3/DERIVATION_VALIDATION_MAP.md",
        "docs/publication/ci3_z3/DERIVATION_ATLAS.md",
    ]
    for rel in paths:
        audit.check(f"file exists: {rel}", (ROOT / rel).exists())

    note = read(NOTE)
    note_flat = " ".join(note.split())
    yt = read("docs/YT_EW_COLOR_PROJECTION_THEOREM.md")
    axioms = read("docs/MINIMAL_AXIOMS_2026-04-11.md")
    ckm_counts = read("docs/CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md")
    sibling = read("docs/FRAMEWORK_BARE_ALPHA_3_ALPHA_EM_DIMENSION_FIXED_RATIO_SUPPORT_NOTE_2026-04-25.md")

    audit.check(
        "note is support-only",
        "support corollary" in note
        and "does not promote a new retained theorem" in note_flat
        and "does not claim a direct low-energy observable" in note_flat,
    )
    audit.check(
        "note preserves R_conn caveat",
        "O(1/N_color^4)" in note and "does not remove" in note,
    )
    audit.check(
        "note excludes flawed Pythagorean route",
        "(1/4)(5/9) = 5/36" in note and "is not equal" in note,
    )
    for phrase in ["NEW retained", "retained EW lattice closure theorem", "direct prediction of alpha_EM(M_Z)"]:
        audit.check(f"forbidden overclaim absent: {phrase}", phrase not in note)

    audit.check(
        "YT_EW retained lane provides bare couplings",
        "standalone retained EW normalization lane" in yt
        and "g_2^2 = 1/4" in yt
        and "g_Y^2 = 1/5" in yt,
    )
    audit.check(
        "YT_EW carries R_conn correction",
        "R_conn = (N_c^2 - 1)/N_c^2" in yt
        and "(9/8) alpha_EW(lattice)" in yt,
    )
    audit.check("minimal axioms carry Z^3", "`Z^3`" in axioms and "Spatial substrate" in axioms)
    audit.check("CKM counts carry N_color", "n_color = 3" in ckm_counts)
    audit.check(
        "sibling support note carries bare alpha identities",
        "alpha_em(bare)" in sibling and "g_em^2(bare) = 1/9" in sibling,
    )


def audit_exact_algebra(audit: Audit) -> None:
    d = 3
    n_color = 3
    g2_sq = Fraction(1, d + 1)
    gy_sq = Fraction(1, d + 2)

    frac_eq(audit, "d = 3", Fraction(d, 1), Fraction(3, 1))
    frac_eq(audit, "N_color = 3", Fraction(n_color, 1), Fraction(3, 1))
    frac_eq(audit, "g2^2 = 1/(d+1)", g2_sq, Fraction(1, 4))
    frac_eq(audit, "gY^2 = 1/(d+2)", gy_sq, Fraction(1, 5))

    e_sq_direct = (g2_sq * gy_sq) / (g2_sq + gy_sq)
    e_sq_inverse = Fraction(1, 1) / (Fraction(1, 1) / g2_sq + Fraction(1, 1) / gy_sq)
    e_sq_color = Fraction(1, n_color * n_color)
    frac_eq(audit, "S1 direct EW mixing gives e_lattice^2", e_sq_direct, Fraction(1, 9))
    frac_eq(audit, "S1 inverse-coupling form gives same e_lattice^2", e_sq_inverse, Fraction(1, 9))
    frac_eq(audit, "S1 e_lattice^2 = 1/N_color^2", e_sq_direct, e_sq_color)

    alpha_bare_factor = e_sq_direct
    frac_eq(audit, "S2 alpha_em,bare factor before 4pi", alpha_bare_factor, Fraction(1, 9))
    float_close(audit, "S2 alpha_em,bare = 1/(36 pi)", float(alpha_bare_factor) / (4 * math.pi), 1 / (36 * math.pi))

    r_conn = Fraction(n_color * n_color - 1, n_color * n_color)
    inv_r_conn = Fraction(1, 1) / r_conn
    adj_dim = n_color * n_color - 1
    alpha_rconn_factor = alpha_bare_factor * inv_r_conn
    frac_eq(audit, "R_conn = 8/9", r_conn, Fraction(8, 9))
    frac_eq(audit, "1/R_conn = 9/8", inv_r_conn, Fraction(9, 8))
    frac_eq(audit, "dim(adj SU(3)) = 8", Fraction(adj_dim, 1), Fraction(8, 1))
    frac_eq(audit, "S3 R_conn-corrected alpha factor = 1/8", alpha_rconn_factor, Fraction(1, 8))
    float_close(
        audit,
        "S3 alpha_EW,Rconn(lattice) = 1/(32 pi)",
        float(alpha_rconn_factor) / (4 * math.pi),
        1 / (32 * math.pi),
    )

    identity = 4 * math.pi * (1 / (32 * math.pi)) * adj_dim
    float_close(audit, "adjoint-dimension support identity equals 1", identity, 1.0)

    flawed_route = g2_sq * Fraction(5, 9)
    frac_eq(audit, "flawed route is 5/36, not 1/9", flawed_route, Fraction(5, 36))
    audit.check("flawed route is excluded by algebra", flawed_route != e_sq_direct)


def audit_public_wiring(audit: Audit) -> None:
    files = [
        "docs/CANONICAL_HARNESS_INDEX.md",
        "docs/publication/ci3_z3/RESULTS_INDEX.md",
        "docs/publication/ci3_z3/CLAIMS_TABLE.md",
        "docs/publication/ci3_z3/PUBLICATION_MATRIX.md",
        "docs/publication/ci3_z3/DERIVATION_VALIDATION_MAP.md",
        "docs/publication/ci3_z3/DERIVATION_ATLAS.md",
    ]
    for rel in files:
        text = read(rel)
        audit.check(
            f"{rel} preserves bare-ratio row key",
            "Bare alpha_3/alpha_em dimension-ratio support" in text
            or "bare `alpha_3/alpha_em` dimension-ratio support" in text
            or "Bare `alpha_3/alpha_em" in text,
        )
        audit.check(f"{rel} links adjoint-dim support note", "EW_ALPHA_LATTICE_ADJOINT_DIM_SUPPORT_NOTE_2026-04-25.md" in text)
        if rel != "docs/publication/ci3_z3/PUBLICATION_MATRIX.md":
            audit.check(f"{rel} links adjoint-dim runner", "frontier_ew_alpha_lattice_adjoint_dim_support.py" in text)


def main() -> int:
    audit = Audit()
    print("EW alpha lattice adjoint-dimension support audit")
    audit_authority_boundary(audit)
    audit_exact_algebra(audit)
    audit_public_wiring(audit)
    print(f"TOTAL: PASS={audit.passed} FAIL={audit.failed}")
    return 0 if audit.failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
