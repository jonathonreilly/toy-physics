#!/usr/bin/env python3
"""Audit the conditional cross-sector A^2-Q_l-|V_cb| bridge.

This runner verifies the algebra in
  docs/CROSS_SECTOR_A_SQUARED_KOIDE_VCB_BRIDGE_SUPPORT_NOTE_2026-04-25.md

Scope:
  - retained inputs: CKM atlas A^2, lambda^2, |V_cb|, canonical alpha_s(v)
  - conditional/open input: Koide support target Q_l = 2/3

It intentionally checks that package control surfaces still mark Koide
as open/support rather than retained closure.
"""

from __future__ import annotations

import math
import sys
from fractions import Fraction
from pathlib import Path

from canonical_plaquette_surface import CANONICAL_ALPHA_S_V


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


def close(a: float, b: float, tol: float = 1e-12) -> bool:
    return abs(a - b) <= tol


REPO_ROOT = Path(__file__).resolve().parents[1]

# Retained CKM / gauge-vacuum inputs.
ALPHA_S_V = CANONICAL_ALPHA_S_V
LAMBDA_SQ = ALPHA_S_V / 2.0
A_SQ_CKM = Fraction(2, 3)
N_PAIR = 2
N_COLOR = 3

# Open charged-lepton Koide support target, not retained closure.
Q_L_KOIDE_TARGET = Fraction(2, 3)

# PDG-style |V_cb| comparator used only for the support test.
V_CB_PDG = 0.0410
V_CB_PDG_ERR = 0.0014


def read_rel(rel: str) -> str:
    return (REPO_ROOT / rel).read_text(encoding="utf-8")


def audit_authorities() -> None:
    banner("Authority and status checks")

    retained_authorities = (
        "docs/ALPHA_S_DERIVED_NOTE.md",
        "docs/WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md",
        "docs/CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md",
    )
    for rel in retained_authorities:
        check(f"retained input authority present: {rel}", (REPO_ROOT / rel).exists())

    koide_authorities = (
        "docs/KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md",
        "docs/KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md",
        "docs/KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE_2026-04-25.md",
        "docs/publication/ci3_z3/PUBLICATION_MATRIX.md",
        "docs/publication/ci3_z3/EXTERNAL_REVIEWER_GUIDE.md",
        "docs/publication/ci3_z3/CLAIMS_TABLE.md",
    )
    for rel in koide_authorities:
        check(f"Koide support/open authority present: {rel}", (REPO_ROOT / rel).exists())

    matrix = read_rel("docs/publication/ci3_z3/PUBLICATION_MATRIX.md")
    guide = read_rel("docs/publication/ci3_z3/EXTERNAL_REVIEWER_GUIDE.md")
    claims = read_rel("docs/publication/ci3_z3/CLAIMS_TABLE.md")
    harness = read_rel("docs/CANONICAL_HARNESS_INDEX.md")

    status_text = "\n".join((matrix, guide, claims, harness))
    check("Koide remains marked as open/support in package surfaces",
          "open flagship lane" in status_text and "support package" in status_text)
    check("Koide retained closure is not promoted",
          "not retained closure" in status_text or "explicitly not promoted" in status_text)
    check("Q=2/3 physical source-domain blocker is still visible",
          "Q = 2/3" in status_text and "remains open" in status_text)


def audit_inputs() -> None:
    banner("Inputs")

    print("  retained CKM / gauge-vacuum inputs:")
    print(f"    A^2 = N_pair/N_color = {A_SQ_CKM}")
    print(f"    lambda^2 = alpha_s(v)/2 = {LAMBDA_SQ:.15f}")
    print(f"    alpha_s(v) = {ALPHA_S_V:.15f}")
    print()
    print("  conditional Koide support target:")
    print(f"    Q_l = {Q_L_KOIDE_TARGET}  (open/support, not retained closure)")

    check("A^2 = 2/3", A_SQ_CKM == Fraction(2, 3))
    check("Q_l target = 2/3", Q_L_KOIDE_TARGET == Fraction(2, 3))
    check("N_pair = 2", N_PAIR == 2)
    check("N_color = 3", N_COLOR == 3)
    check("A^2 = N_pair/N_color", A_SQ_CKM == Fraction(N_PAIR, N_COLOR))
    check("alpha_s(v) > 0", ALPHA_S_V > 0)
    check("lambda^2 = alpha_s(v)/2", close(LAMBDA_SQ, ALPHA_S_V / 2.0))


def audit_conditional_identity() -> None:
    banner("Conditional bridge: Q_l alpha_s(v)^2 = 4 |V_cb|^2")

    vcb_sq_from_a = float(A_SQ_CKM) * LAMBDA_SQ ** 2
    vcb_sq_from_alpha = ALPHA_S_V ** 2 / 6.0
    vcb_sq_from_q = float(Q_L_KOIDE_TARGET) * LAMBDA_SQ ** 2

    lhs = float(Q_L_KOIDE_TARGET) * ALPHA_S_V ** 2
    rhs = 4.0 * vcb_sq_from_a

    print(f"  |V_cb|^2 from A^2 lambda^4       = {vcb_sq_from_a:.12f}")
    print(f"  |V_cb|^2 from alpha_s(v)^2 / 6  = {vcb_sq_from_alpha:.12f}")
    print(f"  |V_cb|^2 from Q_l lambda^4       = {vcb_sq_from_q:.12f}")
    print(f"  Q_l alpha_s(v)^2                = {lhs:.12f}")
    print(f"  4 |V_cb|^2                      = {rhs:.12f}")

    check("|V_cb|^2 = alpha_s(v)^2/6", close(vcb_sq_from_a, vcb_sq_from_alpha))
    check("conditional |V_cb|^2 = Q_l lambda^4", close(vcb_sq_from_a, vcb_sq_from_q))
    check("conditional Q_l alpha_s(v)^2 = 4 |V_cb|^2", close(lhs, rhs))
    check("bridge ratio is 1", close(lhs / rhs, 1.0))


def audit_extractions() -> None:
    banner("Extraction forms")

    vcb_atlas = math.sqrt(float(A_SQ_CKM)) * (ALPHA_S_V / 2.0)
    vcb_sq_atlas = vcb_atlas ** 2
    q_from_atlas = 4.0 * vcb_sq_atlas / ALPHA_S_V ** 2
    alpha_from_atlas = 2.0 * vcb_atlas / math.sqrt(float(Q_L_KOIDE_TARGET))

    print(f"  atlas |V_cb| = {vcb_atlas:.12f}")
    print(f"  extracted Q_l = {q_from_atlas:.12f}")
    print(f"  extracted alpha_s(v) = {alpha_from_atlas:.12f}")

    check("atlas extraction gives Q_l target", close(q_from_atlas, float(Q_L_KOIDE_TARGET)))
    check("atlas extraction gives canonical alpha_s(v)", close(alpha_from_atlas, ALPHA_S_V))

    q_pdg = 4.0 * V_CB_PDG ** 2 / ALPHA_S_V ** 2
    q_pdg_err = 8.0 * V_CB_PDG * V_CB_PDG_ERR / ALPHA_S_V ** 2
    q_dev = (q_pdg - float(Q_L_KOIDE_TARGET)) / q_pdg_err

    alpha_pdg = 2.0 * V_CB_PDG / math.sqrt(float(Q_L_KOIDE_TARGET))
    alpha_pdg_err = 2.0 * V_CB_PDG_ERR / math.sqrt(float(Q_L_KOIDE_TARGET))
    alpha_dev = (alpha_pdg - ALPHA_S_V) / alpha_pdg_err

    print()
    print("  PDG-style comparator:")
    print(f"    |V_cb| = {V_CB_PDG:.4f} +/- {V_CB_PDG_ERR:.4f}")
    print(f"    Q_l extracted = {q_pdg:.4f} +/- {q_pdg_err:.4f} ({q_dev:+.3f} sigma)")
    print(f"    alpha_s extracted = {alpha_pdg:.6f} +/- {alpha_pdg_err:.6f} ({alpha_dev:+.3f} sigma)")

    check("PDG-style Q_l extraction is within 1 sigma of target", abs(q_dev) < 1.0)
    check("PDG-style alpha_s extraction is within 1 sigma of canonical", abs(alpha_dev) < 1.0)


def audit_status_boundaries() -> None:
    banner("Status boundaries")

    note_text = read_rel("docs/CROSS_SECTOR_A_SQUARED_KOIDE_VCB_BRIDGE_SUPPORT_NOTE_2026-04-25.md")
    forbidden = (
        "Retained derivation theorem",
        "three independently-retained",
        "Koide three-gap closure",
        "Q_l = 2/3` is retained",
    )
    for phrase in forbidden:
        check(f"note avoids overclaim: {phrase}", phrase not in note_text)

    required = (
        "conditional cross-sector support corollary",
        "does **not** promote charged-lepton Koide",
        "open/support target, not retained closure",
        "does not close the charged-lepton Koide lane",
    )
    for phrase in required:
        check(f"note states boundary: {phrase}", phrase in note_text)


def audit_falsification_projection() -> None:
    banner("Falsification projection")

    eras = [
        ("PDG-style comparator", 0.0014),
        ("Belle II / LHCb upgrade target", 0.0007),
        ("HL-LHC scale target", 0.0003),
    ]

    previous = None
    for era, sigma_vcb in eras:
        sigma_q = 8.0 * V_CB_PDG * sigma_vcb / ALPHA_S_V ** 2
        print(f"  {era:32s} sigma(|V_cb|)={sigma_vcb:.4f}  sigma(Q_l)={sigma_q:.4f}")
        if previous is not None:
            check(f"{era}: projected Q_l uncertainty tightens", sigma_q < previous)
        previous = sigma_q


def audit_summary() -> None:
    banner("Summary")

    print("  Verdict: support-corollary audit passes if FAIL=0.")
    print("  Retained part: CKM atlas plus canonical alpha_s(v).")
    print("  Conditional part: Koide Q_l = 2/3 support target.")
    print("  Bridge: Q_l alpha_s(v)^2 = 4 |V_cb|^2.")


def main() -> int:
    print("=" * 88)
    print("Conditional cross-sector A^2-Q_l-|V_cb| bridge audit")
    print("See docs/CROSS_SECTOR_A_SQUARED_KOIDE_VCB_BRIDGE_SUPPORT_NOTE_2026-04-25.md")
    print("=" * 88)

    audit_authorities()
    audit_inputs()
    audit_conditional_identity()
    audit_extractions()
    audit_status_boundaries()
    audit_falsification_projection()
    audit_summary()

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
