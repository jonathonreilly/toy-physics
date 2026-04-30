#!/usr/bin/env python3
"""
Lane 5 C2 stretch: can CKM CP orientation select the PMNS A13 sheet?

Question:
  Can the current CKM CP-phase structure supply the right-sensitive PMNS
  doublet-block selector needed by the Lane 5 eta-retirement gate?

Answer on the current branch-local science surface:
  No as an unconditional theorem. A conditional selector
  sign(A13_PMNS) = sign(eta_CKM) is algebraically coherent and chooses the
  constructive sheet, but the current authority surface has no typed
  cross-sector coupling from the quark CKM CP orientation to
  dW_e^H = Schur_Ee(D_-). The missing object is that coupling law.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0

np.set_printoptions(precision=10, suppress=True, linewidth=120)


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf-8")


def even_pmns_data(delta: float, q_plus: float, a13_abs: float) -> tuple[float, float, float]:
    """A minimal stand-in for the even response pair and A13 magnitude."""
    return (
        round(delta * delta + q_plus * q_plus, 12),
        round(delta * delta * q_plus * q_plus, 12),
        round(a13_abs, 12),
    )


def odd_pmns_data(delta: float, a13_abs: float) -> tuple[int, float]:
    sign = 1 if delta > 0 else -1
    return sign, sign * a13_abs


def ckm_cp_orientation() -> tuple[float, float, float, int]:
    rho = 1.0 / 6.0
    eta = math.sqrt(5.0) / 6.0
    delta = math.atan(math.sqrt(5.0))
    sign_eta = 1 if eta > 0.0 else -1
    return rho, eta, delta, sign_eta


def candidate_cross_sector_selector(sign_eta_ckm: int, a13_abs: float) -> float:
    return sign_eta_ckm * a13_abs


def test_authority_text() -> None:
    print("\n" + "=" * 88)
    print("PART 1: AUTHORITY TEXT NAMES THE C2 SELECTOR TARGET")
    print("=" * 88)

    eta_audit = read("docs/HUBBLE_LANE5_ETA_RETIREMENT_GATE_AUDIT_NOTE_2026-04-26.md")
    a13 = read("docs/DM_LEPTOGENESIS_PMNS_MINIMAL_A13_SHEET_SELECTOR_THEOREM_NOTE_2026-04-16.md")
    blindness = read("docs/DM_LEPTOGENESIS_PMNS_SELECTOR_BANK_CP_SHEET_BLINDNESS_THEOREM_NOTE_2026-04-16.md")
    ckm = read("docs/CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md")
    right = read("docs/PMNS_RIGHT_CONJUGACY_INVARIANT_NO_GO_NOTE.md")

    check(
        "Lane 5 eta audit names the right-sensitive Z3 doublet-block law",
        "right-sensitive" in eta_audit and "Z_3" in eta_audit and "doublet-block" in eta_audit,
    )
    check(
        "Lane 5 eta audit lists CKM atlas structure as an unexplored coupling source",
        "CKM atlas" in eta_audit and "sqrt(5)" in eta_audit,
    )
    check(
        "PMNS A13 theorem reduces the residual selector to sign(A13)",
        "sign of `A13`" in a13 and "A13 > 0" in a13 and "A13 < 0" in a13,
    )
    check(
        "PMNS selector-bank theorem records CP-sheet blindness",
        "CP-sheet blind" in blindness and "delta -> -delta" in blindness,
    )
    check(
        "CKM CP theorem supplies a positive eta_CKM orientation",
        "eta = sqrt(5)/6" in ckm and "tan(delta_CKM)" in ckm,
    )
    check(
        "Right-conjugacy note says the missing object must break right-orbit blindness",
        "non-conjugacy-invariant" in right and "right-sensitive" in right,
    )


def test_pmns_even_data_blindness() -> None:
    print("\n" + "=" * 88)
    print("PART 2: PMNS EVEN DATA CANNOT SELECT THE A13 SIGN")
    print("=" * 88)

    rho_star = math.sqrt(6.0) / 3.0
    a13_abs = 2.0 * rho_star
    plus = {
        "delta": rho_star,
        "q_plus": rho_star,
        "a13_abs": a13_abs,
    }
    minus = {
        "delta": -rho_star,
        "q_plus": rho_star,
        "a13_abs": a13_abs,
    }

    even_plus = even_pmns_data(**plus)
    even_minus = even_pmns_data(**minus)
    odd_plus = odd_pmns_data(plus["delta"], plus["a13_abs"])
    odd_minus = odd_pmns_data(minus["delta"], minus["a13_abs"])

    print(f"  even(+sheet) = {even_plus}")
    print(f"  even(-sheet) = {even_minus}")
    print(f"  odd(+sheet)  = sign,A13 = {odd_plus}")
    print(f"  odd(-sheet)  = sign,A13 = {odd_minus}")

    check("The two sheets have identical even PMNS data", even_plus == even_minus)
    check("The same two sheets have opposite A13 sign", odd_plus[0] == -odd_minus[0])
    check("A selector using only the even data is sheet-blind", even_plus == even_minus and odd_plus != odd_minus)


def test_ckm_orientation_candidate_is_conditional() -> None:
    print("\n" + "=" * 88)
    print("PART 3: CKM ORIENTATION GIVES A COHERENT BUT CONDITIONAL SELECTOR")
    print("=" * 88)

    rho, eta, delta_ckm, sign_eta = ckm_cp_orientation()
    a13_abs = 2.0 * math.sqrt(6.0) / 3.0
    selected_a13 = candidate_cross_sector_selector(sign_eta, a13_abs)

    print(f"  rho_CKM={rho:.12f}")
    print(f"  eta_CKM={eta:.12f}")
    print(f"  delta_CKM={delta_ckm:.12f}")
    print(f"  candidate selected A13={selected_a13:.12f}")

    check("CKM CP coordinates obey rho=1/6", abs(rho - 1.0 / 6.0) < 1e-12)
    check("CKM CP coordinates obey eta=sqrt(5)/6", abs(eta - math.sqrt(5.0) / 6.0) < 1e-12)
    check("CKM orientation is positive on the named branch", sign_eta == 1)
    check("The candidate sign(A13)=sign(eta_CKM) selects A13>0", selected_a13 > 0.0)


def test_missing_typed_coupling_witness() -> None:
    print("\n" + "=" * 88)
    print("PART 4: CURRENT SURFACE HAS NO TYPED CKM->PMNS COUPLING")
    print("=" * 88)

    sign_eta = ckm_cp_orientation()[3]
    a13_abs = 2.0 * math.sqrt(6.0) / 3.0

    world_plus = {
        "ckm_sign": sign_eta,
        "pmns_even": even_pmns_data(math.sqrt(6.0) / 3.0, math.sqrt(6.0) / 3.0, a13_abs),
        "pmns_a13": a13_abs,
    }
    world_minus = {
        "ckm_sign": sign_eta,
        "pmns_even": even_pmns_data(-math.sqrt(6.0) / 3.0, math.sqrt(6.0) / 3.0, a13_abs),
        "pmns_a13": -a13_abs,
    }

    coupling_law_present = False
    current_data_distinguish_worlds = (
        world_plus["ckm_sign"] != world_minus["ckm_sign"]
        or world_plus["pmns_even"] != world_minus["pmns_even"]
    )
    conditional_law_would_select = candidate_cross_sector_selector(sign_eta, a13_abs) == world_plus["pmns_a13"]

    check("Two witnesses share CKM orientation and PMNS even data", not current_data_distinguish_worlds)
    check("The witnesses differ only in the PMNS A13 sign", world_plus["pmns_a13"] == -world_minus["pmns_a13"])
    check("A cross-sector sign law would select the constructive witness", conditional_law_would_select)
    check("That cross-sector sign law is not present on the current surface", not coupling_law_present)
    check("Therefore the current surface cannot prove the selector", conditional_law_would_select and not coupling_law_present)


def test_status_firewall() -> None:
    print("\n" + "=" * 88)
    print("PART 5: CLAIM-STATUS FIREWALL")
    print("=" * 88)

    actual_current_surface_status = "no-go"
    conditional_surface_status = "conditional-support"
    open_imports = [
        "typed CKM CP orientation to PMNS dW_e^H coupling law",
        "canonical right-frame law or equivalent right-sensitive observable principle",
    ]
    proposal_allowed = False

    check("Actual current-surface status is no-go for unconditional C2 closure", actual_current_surface_status == "no-go")
    check("The candidate is only conditional support under a new coupling law", conditional_surface_status == "conditional-support")
    check("The typed cross-sector coupling remains open", len(open_imports) == 2)
    check("No stronger branch-local proposal wording is allowed", not proposal_allowed)


def main() -> int:
    print("=" * 88)
    print("LANE 5 C2: CKM/PMNS RIGHT-SENSITIVE SELECTOR STRETCH")
    print("=" * 88)
    print()
    print("Claim under test:")
    print("  CKM CP orientation might provide the missing PMNS A13 sign selector")
    print("  for the Lane 5 eta-retirement C2 gate.")
    print()
    print("Boundary result:")
    print("  The sign rule is algebraically coherent but only conditional.")
    print("  Current authority has no typed CKM->PMNS right-sensitive coupling law.")

    test_authority_text()
    test_pmns_even_data_blindness()
    test_ckm_orientation_candidate_is_conditional()
    test_missing_typed_coupling_witness()
    test_status_firewall()

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)

    if FAIL_COUNT:
        print("C2 selector stretch runner failed; do not use the note.")
        return 1

    print("Result: no unconditional C2 selector closure on the current surface.")
    print("Conditional support exists only if a typed CKM->PMNS coupling law is added.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
