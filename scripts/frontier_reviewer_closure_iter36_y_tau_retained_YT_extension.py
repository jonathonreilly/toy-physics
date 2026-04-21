#!/usr/bin/env python3
"""
Reviewer-Closure Loop Iter 36: attack R2 via retained YT 1-loop α_LM/(4π) machinery

Background: the retained Atlas uses α_LM/(4π) as the canonical 1-loop
lattice PT expansion parameter (YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18,
retained Δ_R ratio formula).

Numerically: α_LM/(4π) = 0.007215, matching y_τ^fw = m_τ/v_EW = 0.007215
at 0.006%.

Question: can this be derived from retained framework by extending the YT
Δ_R 1-loop machinery to the charged-lepton Yukawa?

Test: assume y_τ^fw = (α_LM/(4π)) · C_τ where C_τ is a charged-lepton
Casimir coefficient analogous to {C_F, C_A, T_F n_f} in the YT formula.
If C_τ = 1 from the retained charged-lepton group structure (colorless,
SU(2)_L × U(1) only), then R2 derives.

This iter tests whether C_τ = 1 can be justified from retained structure.
"""

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from dm_leptogenesis_exact_common import ALPHA_LM, V_EW  # noqa: E402

PASSES: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = ""):
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.split("\n"):
            print(f"       {line}")


def section(title: str):
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


M_TAU_PDG = 1776.86


def part_A():
    section("Part A — retained YT 1-loop lattice PT machinery")

    alpha_LM_over_4pi = ALPHA_LM / (4 * math.pi)
    print(f"  Retained Δ_R^ratio = (α_LM/(4π)) · [C_F·Δ_1 + C_A·Δ_2 + T_F n_f·Δ_3]")
    print(f"  (YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18)")
    print()
    print(f"  Retained α_LM/(4π) = 0.00721 (exact lattice PT 1-loop factor)")
    print(f"  Computed α_LM/(4π) = {alpha_LM_over_4pi:.8f}")
    print()

    # This is retained as the 1-loop lattice PT expansion parameter
    record(
        "A.1 α_LM/(4π) is retained as the canonical 1-loop lattice PT factor",
        abs(alpha_LM_over_4pi - 0.00721) < 1e-4,
        f"Matches retained YT_P1 1-loop factor at framework precision",
    )

    # y_τ^fw observed
    y_tau_obs = M_TAU_PDG / (V_EW * 1000.0)
    dev = abs(y_tau_obs - alpha_LM_over_4pi) / alpha_LM_over_4pi * 100
    record(
        "A.2 y_τ^fw = m_τ/v_EW matches α_LM/(4π) at 0.006%",
        dev < 0.01,
        f"y_τ^fw (obs) = {y_tau_obs:.8f}\n"
        f"α_LM/(4π) = {alpha_LM_over_4pi:.8f}\n"
        f"deviation = {dev:.4f}%",
    )


def part_B():
    section("Part B — what would make this framework-derived rather than coincidental?")

    print("  The retained YT 1-loop formula for top Yukawa-like corrections is:")
    print("    Δ_R = (α_LM/(4π)) · [C_F · Δ_1 + C_A · Δ_2 + T_F n_f · Δ_3]")
    print()
    print("  where {C_F, C_A, T_F·n_f} are SU(3)_color Casimirs for the top quark")
    print("  which carries color charge.")
    print()
    print("  For the charged-lepton Yukawa (tau), the tau carries NO color.")
    print("  At 1-loop, tau Yukawa corrections come from EW sector only:")
    print("    - SU(2)_L × U(1)_Y gauge bosons")
    print("    - NOT from QCD (color-blind sector)")
    print()
    print("  Question: is there a charged-lepton-specific Casimir C_τ = 1 at 1-loop?")
    print()

    # Standard SU(2)_L Casimir for tau (charge -1 lepton in fundamental):
    # C_F(SU(2)) = 3/4 (fundamental)
    # C_A(SU(2)) = 2 (adjoint)
    # For the doublet (τ_L, ν_τ): Casimir of 2 = C_F(SU(2)) = 3/4

    print("  Standard SU(2)_L Casimirs:")
    print("    C_F(SU(2)_L, fundamental) = 3/4")
    print("    C_A(SU(2)_L, adjoint) = 2")
    print("  Standard U(1)_Y hypercharge: Y_L = -1/2 (lepton doublet)")
    print()

    # If the 1-loop charged-lepton Yukawa depends on these, y_τ ≠ α_LM/(4π) simply
    # UNLESS there's a specific combination giving coefficient 1

    record(
        "B.1 Direct 1-loop lepton Yukawa has Casimirs {3/4, 2, 1/4} from SU(2)_L + U(1)_Y",
        True,
        "Not obviously combined to give coefficient 1 at 1-loop.",
    )

    print()
    print("  For y_τ^fw = α_LM/(4π) · 1 exactly, we would need the retained")
    print("  charged-lepton sector to give Casimir combination = 1 at 1-loop.")
    print("  This requires a SPECIFIC retained charged-lepton 1-loop computation,")
    print("  which is NOT currently in the Atlas.")

    record(
        "B.2 Charged-lepton 1-loop Yukawa Casimir C_τ = 1 not retained in Atlas",
        True,
        "Without a retained derivation of C_τ = 1, the y_τ = α_LM/(4π) relation\n"
        "remains an observational identification, not a framework derivation.",
    )


def part_C():
    section("Part C — honest verdict on R2 derivability")

    record(
        "C.1 R2 (y_τ = α_LM/(4π)) REMAINS observational identification",
        True,
        "The retained YT 1-loop machinery uses α_LM/(4π) as its canonical PT\n"
        "expansion parameter. This is consistent with y_τ^fw = α_LM/(4π) being\n"
        "a 1-loop lattice PT value, but the specific Casimir coefficient = 1\n"
        "requires a retained charged-lepton-sector 1-loop calculation that is\n"
        "NOT currently in the Atlas.",
    )

    record(
        "C.2 Partial strengthening: α_LM/(4π) is retained as framework-native 1-loop factor",
        True,
        "So y_τ = α_LM/(4π) is 'observational' in the narrow sense that the\n"
        "charged-lepton C_τ = 1 coefficient is observational, but the α_LM/(4π)\n"
        "factor itself is framework-retained via YT_P1_BZ_QUADRATURE machinery.",
    )

    record(
        "C.3 Axiom-only R2 closure requires new retention",
        True,
        "For R2 to derive axiom-only, Atlas needs to add:\n"
        "  'Charged-lepton tau-Yukawa 1-loop lattice theorem: the tau Yukawa\n"
        "   coupling at 1-loop lattice PT equals α_LM/(4π) exactly (C_τ = 1)\n"
        "   from the retained charged-lepton group structure.'\n"
        "Without this retention, R2 stands as a proposed framework axiom.",
    )


def main() -> int:
    section("Iter 36 — attack R2 via retained YT 1-loop machinery")
    print("Question: does y_τ^fw = α_LM/(4π) derive from the retained YT")
    print("1-loop lattice PT structure?")

    part_A()
    part_B()
    part_C()

    section("SUMMARY")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")

    print()
    print("VERDICT:")
    print("  Partial progress: α_LM/(4π) IS retained as the canonical 1-loop")
    print("  lattice PT expansion parameter (YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT).")
    print()
    print("  But R2 (y_τ^fw = α_LM/(4π) exactly) requires an additional retention:")
    print("  a charged-lepton-specific 1-loop Yukawa theorem giving C_τ = 1.")
    print()
    print("  This retention is NOT in the current Atlas. R2 remains a proposed")
    print("  framework axiom, not a derivation from retained structure.")
    print()
    print("  The observational match at 0.006% strongly supports this as a")
    print("  candidate retention, but axiom-only closure still requires adding")
    print("  the charged-lepton-sector 1-loop theorem to the Atlas.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
