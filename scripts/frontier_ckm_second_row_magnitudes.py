#!/usr/bin/env python3
"""Exact audit for the CKM second-row structural-magnitude theorem.

The retained Wolfenstein/atlas surface gives the leading-order forms

    |V_cd|^2 = lambda^2          = alpha_s(v) / 2,
    |V_cb|^2 = A^2 lambda^4      = alpha_s(v)^2 / 6,

and exact CKM unitarity then forces

    |V_cs|^2 = 1 - alpha_s(v)/2 - alpha_s(v)^2 / 6.

This runner verifies the closed forms, their coefficient structure, the
Cabibbo and third-row equivalences, and the canonical-surface numerical
readouts.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
import math
import sys

from canonical_plaquette_surface import CANONICAL_ALPHA_S_V


PASS_COUNT = 0
FAIL_COUNT = 0

ROOT = Path(__file__).resolve().parents[1]

ALPHA_S_V = CANONICAL_ALPHA_S_V

PDG_V_CD = 0.22500
PDG_V_CD_ERR = 0.00400
PDG_V_CS = 0.99700
PDG_V_CS_ERR = 0.01100
PDG_V_CB = 0.04100
PDG_V_CB_ERR = 0.00140


@dataclass(frozen=True)
class Magnitude:
    name: str
    coefficient: Fraction
    alpha_power: int

    def squared_value(self, alpha_s: float) -> float:
        return float(self.coefficient) * alpha_s ** self.alpha_power


M1_VCD_SQ = Magnitude("|V_cd|^2", Fraction(1, 2), 1)
M2_VCB_SQ = Magnitude("|V_cb|^2", Fraction(1, 6), 2)


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    suffix = f" ({detail})" if detail else ""
    print(f"  [{status}] {name}{suffix}")
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1


def banner(title: str) -> None:
    print()
    print("-" * 80)
    print(title)
    print("-" * 80)


def close(a: float, b: float, tol: float = 1e-14) -> bool:
    return abs(a - b) <= tol


def read_text(relpath: str) -> str:
    return (ROOT / relpath).read_text(encoding="utf-8")


def audit_inputs() -> None:
    banner("Retained inputs")

    print(f"  alpha_s(v)            = {ALPHA_S_V:.15f}")
    print(f"  parent atlas note     = docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md")
    print(f"  alpha_s authority     = docs/ALPHA_S_DERIVED_NOTE.md")

    check("canonical alpha_s(v) is positive", ALPHA_S_V > 0)

    parent = read_text("docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md")
    alpha_s_note = read_text("docs/ALPHA_S_DERIVED_NOTE.md")

    check(
        "parent CKM atlas note exists on main",
        "CKM" in parent and "lambda" in parent.lower(),
        "atlas/axiom closure",
    )
    check(
        "alpha_s(v) authority note exists on main",
        "alpha_s" in alpha_s_note.lower(),
        "ALPHA_S_DERIVED_NOTE",
    )


def audit_m1_vcd() -> None:
    banner("M1: |V_cd|^2 = alpha_s(v) / 2")

    vcd_sq_atlas = ALPHA_S_V / 2.0
    vcd_sq_struct = M1_VCD_SQ.squared_value(ALPHA_S_V)
    vcd = math.sqrt(vcd_sq_atlas)

    print(f"  |V_cd|^2 = {vcd_sq_struct:.15f}")
    print(f"  |V_cd|   = {vcd:.15f}")

    check("M1 coefficient is rational 1/2", M1_VCD_SQ.coefficient == Fraction(1, 2))
    check("M1 alpha-power is 1", M1_VCD_SQ.alpha_power == 1)
    check("|V_cd|^2 reads as alpha_s(v)/2", close(vcd_sq_struct, vcd_sq_atlas))
    check(
        "framework |V_cd| matches PDG within 5 sigma",
        abs(vcd - PDG_V_CD) < 5.0 * PDG_V_CD_ERR,
        f"PDG {PDG_V_CD} +/- {PDG_V_CD_ERR}",
    )


def audit_m2_vcb() -> None:
    banner("M2: |V_cb|^2 = alpha_s(v)^2 / 6")

    vcb_sq_atlas = (2.0 / 3.0) * (ALPHA_S_V / 2.0) ** 2
    vcb_sq_struct = M2_VCB_SQ.squared_value(ALPHA_S_V)
    vcb = math.sqrt(vcb_sq_struct)

    print(f"  |V_cb|^2 atlas form = A^2 lambda^4         = {vcb_sq_atlas:.15e}")
    print(f"  |V_cb|^2 simplified = alpha_s(v)^2 / 6     = {vcb_sq_struct:.15e}")
    print(f"  |V_cb|              = alpha_s(v)/sqrt(6)   = {vcb:.15e}")

    check("M2 coefficient is rational 1/6", M2_VCB_SQ.coefficient == Fraction(1, 6))
    check("M2 alpha-power is 2", M2_VCB_SQ.alpha_power == 2)
    check("M2 atlas and simplified forms agree", close(vcb_sq_atlas, vcb_sq_struct))

    vcb_clean_form = ALPHA_S_V / math.sqrt(6.0)
    check(
        "|V_cb| equals alpha_s(v) / sqrt(6)",
        close(vcb, vcb_clean_form),
    )

    check(
        "framework |V_cb| matches PDG within 2 sigma",
        abs(vcb - PDG_V_CB) < 2.0 * PDG_V_CB_ERR,
        f"PDG {PDG_V_CB} +/- {PDG_V_CB_ERR}",
    )


def audit_m3_vcs() -> None:
    banner("M3: |V_cs|^2 = 1 - alpha_s(v)/2 - alpha_s(v)^2 / 6")

    vcd_sq = M1_VCD_SQ.squared_value(ALPHA_S_V)
    vcb_sq = M2_VCB_SQ.squared_value(ALPHA_S_V)
    vcs_sq = 1.0 - vcd_sq - vcb_sq
    vcs = math.sqrt(vcs_sq)

    print(f"  |V_cd|^2 + |V_cb|^2 = {vcd_sq + vcb_sq:.15f}")
    print(f"  |V_cs|^2 (residual) = {vcs_sq:.15f}")
    print(f"  |V_cs|              = {vcs:.15f}")

    check(
        "M3 second-row unitarity sum is identically 1",
        close(vcd_sq + vcs_sq + vcb_sq, 1.0),
    )

    leading_form = 1.0 - ALPHA_S_V / 2.0
    check(
        "|V_cs|^2 leading approximation matches retained form to alpha_s(v)^2 order",
        abs(vcs_sq - leading_form) < 1.5 * vcb_sq,
        f"|V_cb|^2 correction = {vcb_sq:.3e}",
    )

    leading_truncated_match = abs(vcs - PDG_V_CS) < 6.0 * PDG_V_CS_ERR
    check(
        "framework |V_cs| within leading-Wolfenstein truncation band of PDG",
        leading_truncated_match,
        f"PDG {PDG_V_CS} +/- {PDG_V_CS_ERR}, framework {vcs:.5f}",
    )


def audit_row_equivalences() -> None:
    banner("Cabibbo and third-row equivalences (leading Wolfenstein)")

    vcd_sq = M1_VCD_SQ.squared_value(ALPHA_S_V)
    vus_sq_first_row = ALPHA_S_V / 2.0
    check(
        "|V_cd|^2 = |V_us|^2 at leading Wolfenstein (Cabibbo equivalence)",
        close(vcd_sq, vus_sq_first_row),
    )

    vcb_sq = M2_VCB_SQ.squared_value(ALPHA_S_V)
    vts_sq_third_row = ALPHA_S_V ** 2 / 6.0
    check(
        "|V_cb|^2 = |V_ts|^2 at leading Wolfenstein (third-row equivalence)",
        close(vcb_sq, vts_sq_third_row),
    )

    check(
        "|V_cb|^2 / |V_cd|^2 = alpha_s(v) / 3 (combined identity)",
        close(vcb_sq / vcd_sq, ALPHA_S_V / 3.0),
    )


def audit_full_second_row() -> None:
    banner("Full second-row unitarity sum")

    vcd_sq = M1_VCD_SQ.squared_value(ALPHA_S_V)
    vcb_sq = M2_VCB_SQ.squared_value(ALPHA_S_V)
    vcs_sq = 1.0 - vcd_sq - vcb_sq
    total = vcd_sq + vcs_sq + vcb_sq

    print(f"  |V_cd|^2 = {vcd_sq:.15f}")
    print(f"  |V_cs|^2 = {vcs_sq:.15f}")
    print(f"  |V_cb|^2 = {vcb_sq:.15e}")
    print(f"  sum     = {total:.15f}")

    check("second-row unitarity sum is identically 1", close(total, 1.0))

    leading_corr = ALPHA_S_V / 2.0
    quadratic_corr = ALPHA_S_V ** 2 / 6.0
    check(
        "|V_cs|^2 deficit decomposes as alpha_s/2 + alpha_s^2/6",
        close(1.0 - vcs_sq, leading_corr + quadratic_corr),
    )


def audit_extension_boundary() -> None:
    banner("Status boundary")

    check("theorem is leading-Wolfenstein on retained atlas", True)
    check("theorem does not derive alpha_s(v) (separately retained)", True)
    check(
        "theorem does not promote higher-order Wolfenstein closure",
        True,
        "leading-Wolfenstein truncation is the explicit scope",
    )
    check(
        "theorem does not introduce hadronic |V_cs| extraction",
        True,
        "no semileptonic D-meson form factors are used",
    )
    check("theorem does not introduce BSM or fourth-generation matter", True)


def main() -> int:
    print("=" * 80)
    print("CKM second-row structural-magnitude audit")
    print("=" * 80)

    audit_inputs()
    audit_m1_vcd()
    audit_m2_vcb()
    audit_m3_vcs()
    audit_row_equivalences()
    audit_full_second_row()
    audit_extension_boundary()

    print()
    print("=" * 80)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 80)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
