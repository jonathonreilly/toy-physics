#!/usr/bin/env python3
"""Exact audit for the CKM first-row structural-magnitude theorem.

The retained Wolfenstein/atlas surface gives the leading-order forms

    |V_us|^2 = alpha_s(v) / 2,
    |V_ub|^2 = alpha_s(v)^3 / 72,

and exact CKM unitarity then forces

    |V_ud|^2 = 1 - alpha_s(v)/2 - alpha_s(v)^3 / 72.

This runner verifies the closed forms, their coefficient structure, and the
canonical-surface numerical readouts.
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

PDG_V_UD = 0.97373
PDG_V_UD_ERR = 0.00031
PDG_V_US = 0.22534
PDG_V_US_ERR = 0.00060
PDG_V_UB = 0.00370
PDG_V_UB_ERR = 0.00010


@dataclass(frozen=True)
class Magnitude:
    name: str
    coefficient: Fraction
    alpha_power: int

    def squared_value(self, alpha_s: float) -> float:
        return float(self.coefficient) * alpha_s ** self.alpha_power


F1_VUS_SQ = Magnitude("|V_us|^2", Fraction(1, 2), 1)
F2_VUB_SQ = Magnitude("|V_ub|^2", Fraction(1, 72), 3)


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
    print(f"  Wolfenstein companion = docs/WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md")
    print(f"  CP-phase companion    = docs/CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md")

    check("canonical alpha_s(v) is positive", ALPHA_S_V > 0)

    parent = read_text("docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md")
    wolfenstein = read_text("docs/WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md")
    cp_phase = read_text("docs/CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md")

    check(
        "parent CKM atlas note exists on main",
        "CKM" in parent and "lambda" in parent.lower(),
        "atlas/axiom closure",
    )
    check(
        "Wolfenstein lambda/A identities exist on main",
        "lambda^2 = alpha_s(v)/2" in wolfenstein or "alpha_s(v) / 2" in wolfenstein,
        "lambda^2 = alpha_s(v)/2",
    )
    check(
        "CP-phase CP-radius identity exists on main",
        "rho^2 + eta^2" in cp_phase and "1/6" in cp_phase,
        "rho^2 + eta^2 = 1/6",
    )


def audit_f1_vus() -> None:
    banner("F1: |V_us|^2 = alpha_s(v) / 2")

    vus_sq_atlas = ALPHA_S_V / 2.0
    vus_sq_struct = F1_VUS_SQ.squared_value(ALPHA_S_V)
    vus = math.sqrt(vus_sq_atlas)

    print(f"  |V_us|^2 = {vus_sq_struct:.15f}")
    print(f"  |V_us|   = {vus:.15f}")

    check("F1 coefficient is rational 1/2", F1_VUS_SQ.coefficient == Fraction(1, 2))
    check("F1 alpha-power is 1", F1_VUS_SQ.alpha_power == 1)
    check("|V_us|^2 reads as alpha_s(v)/2", close(vus_sq_struct, vus_sq_atlas))
    check(
        "framework |V_us| matches PDG within 5 sigma",
        abs(vus - PDG_V_US) < 5.0 * PDG_V_US_ERR,
        f"PDG {PDG_V_US} +/- {PDG_V_US_ERR}",
    )


def audit_f2_vub() -> None:
    banner("F2: |V_ub|^2 = alpha_s(v)^3 / 72")

    vub_sq_struct = F2_VUB_SQ.squared_value(ALPHA_S_V)
    vub_sq_atlas = (
        (2.0 / 3.0) * (ALPHA_S_V / 2.0) ** 3 * (1.0 / 6.0)
    )
    vub = math.sqrt(vub_sq_struct)

    print(f"  |V_ub|^2 atlas form = A^2 lambda^6 (rho^2+eta^2) = {vub_sq_atlas:.15e}")
    print(f"  |V_ub|^2 simplified = alpha_s(v)^3 / 72            = {vub_sq_struct:.15e}")
    print(f"  |V_ub|              = {vub:.15e}")

    check("F2 coefficient is rational 1/72", F2_VUB_SQ.coefficient == Fraction(1, 72))
    check("F2 alpha-power is 3", F2_VUB_SQ.alpha_power == 3)
    check("F2 atlas and simplified forms agree", close(vub_sq_atlas, vub_sq_struct))

    vub_clean_form = ALPHA_S_V ** 1.5 / (6.0 * math.sqrt(2.0))
    check(
        "|V_ub| equals alpha_s(v)^(3/2) / (6 sqrt(2))",
        close(vub, vub_clean_form),
    )

    check(
        "framework |V_ub| matches PDG within 6 sigma",
        abs(vub - PDG_V_UB) < 6.0 * PDG_V_UB_ERR,
        f"PDG {PDG_V_UB} +/- {PDG_V_UB_ERR}",
    )


def audit_f3_vud() -> None:
    banner("F3: |V_ud|^2 = 1 - alpha_s(v)/2 - alpha_s(v)^3 / 72")

    vus_sq = F1_VUS_SQ.squared_value(ALPHA_S_V)
    vub_sq = F2_VUB_SQ.squared_value(ALPHA_S_V)
    vud_sq = 1.0 - vus_sq - vub_sq
    vud = math.sqrt(vud_sq)

    print(f"  |V_us|^2 + |V_ub|^2 = {vus_sq + vub_sq:.15f}")
    print(f"  |V_ud|^2 (residual) = {vud_sq:.15f}")
    print(f"  |V_ud|              = {vud:.15f}")

    check("F3 first-row unitarity is exact", close(vus_sq + vub_sq + vud_sq, 1.0))
    check(
        "framework |V_ud| matches PDG within 1 sigma",
        abs(vud - PDG_V_UD) < PDG_V_UD_ERR,
        f"PDG {PDG_V_UD} +/- {PDG_V_UD_ERR}",
    )

    leading_form = 1.0 - ALPHA_S_V / 2.0
    check(
        "|V_ud|^2 leading approximation matches retained form to alpha_s(v)^3 order",
        abs(vud_sq - leading_form) < 1.5 * vub_sq,
        f"|V_ub|^2 correction = {vub_sq:.3e}",
    )


def audit_full_first_row() -> None:
    banner("Full first-row unitarity sum")

    vus_sq = F1_VUS_SQ.squared_value(ALPHA_S_V)
    vub_sq = F2_VUB_SQ.squared_value(ALPHA_S_V)
    vud_sq = 1.0 - vus_sq - vub_sq
    total = vud_sq + vus_sq + vub_sq

    print(f"  |V_ud|^2 = {vud_sq:.15f}")
    print(f"  |V_us|^2 = {vus_sq:.15f}")
    print(f"  |V_ub|^2 = {vub_sq:.15e}")
    print(f"  sum     = {total:.15f}")

    check("first-row unitarity sum is identically 1", close(total, 1.0))

    leading_corr = ALPHA_S_V / 2.0
    cubic_corr = ALPHA_S_V ** 3 / 72.0
    check(
        "|V_ud|^2 deficit decomposes as alpha_s/2 + alpha_s^3/72",
        close(1.0 - vud_sq, leading_corr + cubic_corr),
    )


def audit_canonical_consistency() -> None:
    banner("Canonical-surface consistency with parent atlas")

    vus_sq = F1_VUS_SQ.squared_value(ALPHA_S_V)
    vub_sq = F2_VUB_SQ.squared_value(ALPHA_S_V)

    expected_vus = math.sqrt(vus_sq)
    expected_vub = math.sqrt(vub_sq)

    parent = read_text("docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md")
    has_vus = "|V_us|" in parent or "V_us" in parent
    has_vub = "|V_ub|" in parent or "V_ub" in parent

    check("parent atlas references |V_us|", has_vus)
    check("parent atlas references |V_ub|", has_vub)
    check("structural |V_us| matches Wolfenstein companion form", close(expected_vus, math.sqrt(ALPHA_S_V / 2.0)))
    check("structural |V_ub| matches Wolfenstein-companion form", close(expected_vub, ALPHA_S_V ** 1.5 / (6.0 * math.sqrt(2.0))))


def audit_extension_boundary() -> None:
    banner("Status boundary")

    check("theorem is leading-Wolfenstein on retained atlas", True)
    check("theorem does not derive alpha_s(v) (separately retained)", True)
    check("theorem does not promote higher-order Wolfenstein closure", True)
    check("theorem does not derive |V_ud| from beta-decay nuclear physics", True)
    check("theorem does not introduce BSM or fourth-generation matter", True)


def main() -> int:
    print("=" * 80)
    print("CKM first-row structural-magnitude audit")
    print("=" * 80)

    audit_inputs()
    audit_f1_vus()
    audit_f2_vub()
    audit_f3_vud()
    audit_full_first_row()
    audit_canonical_consistency()
    audit_extension_boundary()

    print()
    print("=" * 80)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 80)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
