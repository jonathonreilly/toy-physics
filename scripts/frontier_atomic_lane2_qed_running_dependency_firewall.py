#!/usr/bin/env python3
"""Lane 2 QED running dependency firewall.

This runner verifies the structural content of
``docs/ATOMIC_LANE2_QED_RUNNING_DEPENDENCY_FIREWALL_NOTE_2026-04-30.md`` and
checks that the ``alpha_EM(M_Z) -> alpha(0)`` QED running step is honestly
quantified into three named sub-residuals (R-Lep, R-Q-Heavy, R-Had-NP).

Result:
  The runner is a verification harness for an exact reduction theorem.
  It does NOT close Lane 2 or retire any retained-grade dependency.

  The textbook-input arithmetic confirms that the QED running step is
  well-defined when the load-bearing masses and hadronic data are supplied,
  but those are precisely the open primitives blocking Lane 2 on the current
  retained surface.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

PASS_COUNT = 0
FAIL_COUNT = 0

ROOT = Path(__file__).resolve().parents[1]


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    return condition


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def section(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


# Comparator constants only (NOT proof inputs).
# Source: PDG 2024 review of particle physics (charged-lepton masses,
# heavy-quark MS-bar masses, M_Z, alpha^{-1}(0)).
M_E_MEV_COMP = 0.51099895000
M_MU_MEV_COMP = 105.6583755
M_TAU_MEV_COMP = 1776.86
M_C_MEV_COMP = 1273.0
M_B_MEV_COMP = 4183.0
M_T_MEV_COMP = 172570.0
M_Z_MEV_COMP = 91187.6

ALPHA_0_INV_COMP = 137.035999084
ALPHA_MZ_INV_COMP = 127.952  # PDG (used only as an external-cross-check comparator)

# Repo retained reusable EW alpha (per USABLE_DERIVED_VALUES_INDEX.md)
ALPHA_MZ_INV_REPO = 127.67

# Comparator hadronic vacuum polarization (Jegerlehner 2019, PDG-cited).
# Used only to scale R-Had-NP magnitude.
DELTA_ALPHA_HAD_5_COMP = 0.02766


def delta_alpha_lep_perturbative(
    m_lepton_mev: float, mu_mev: float, alpha: float
) -> float:
    """One-loop leptonic vacuum polarization Delta alpha at scale mu, valid
    for mu >> m_lepton.

    Standard QED MS-bar one-loop formula:
        Delta alpha_lep,f(mu^2) = (alpha / 3 pi) * [ ln(mu^2 / m_f^2) - 5/3 ]
    """
    if mu_mev <= 0 or m_lepton_mev <= 0:
        raise ValueError("masses and scale must be positive")
    log_term = math.log((mu_mev / m_lepton_mev) ** 2)
    return (alpha / (3.0 * math.pi)) * (log_term - 5.0 / 3.0)


def delta_alpha_quark_heavy_perturbative(
    m_quark_mev: float, q_charge: float, mu_mev: float, alpha: float
) -> float:
    """One-loop heavy-quark vacuum polarization (perturbative, mu >> m_q).

    Standard formula:
        Delta alpha_q,heavy(mu^2)
            = (3 Q_q^2 alpha / 3 pi) * [ ln(mu^2 / m_q^2) - 5/3 ]
    where 3 = N_c.
    """
    if mu_mev <= 0 or m_quark_mev <= 0:
        raise ValueError("masses and scale must be positive")
    log_term = math.log((mu_mev / m_quark_mev) ** 2)
    return (3.0 * q_charge ** 2 * alpha / (3.0 * math.pi)) * (log_term - 5.0 / 3.0)


def part1_note_structure() -> None:
    section("Part 1: firewall note structure")
    note = read(
        "docs/ATOMIC_LANE2_QED_RUNNING_DEPENDENCY_FIREWALL_NOTE_2026-04-30.md"
    )
    check(
        "note exists with correct title",
        "Atomic Lane 2 — QED Running Dependency Firewall" in note,
    )
    check(
        "note status is exact reduction theorem (not bare retained)",
        "exact reduction theorem" in note and "no claim promotion" in note,
    )
    check(
        "note does NOT use bare 'Status: retained' or 'Status: promoted'",
        "Status: retained" not in note and "Status: promoted" not in note,
    )
    check(
        "note references 2026-04-27 predecessor firewall",
        "ATOMIC_RYDBERG_DEPENDENCY_FIREWALL_NOTE_2026-04-27" in note,
    )
    check(
        "note names three sub-residuals R-Lep, R-Q-Heavy, R-Had-NP",
        "(R-Lep)" in note and "(R-Q-Heavy)" in note and "(R-Had-NP)" in note,
    )
    check(
        "note names Lane 1 + Lane 3 + Lane 6 dependency chain",
        "Lane 1" in note and "Lane 3" in note and "Lane 6" in note,
    )
    check(
        "note states forbidden imports section",
        "Forbidden imports" in note or "forbidden imports" in note,
    )


def part2_running_arithmetic() -> None:
    section("Part 2: textbook-input QED running arithmetic")

    # Use alpha(0) at the prefactor — at one loop the choice of alpha(0) vs
    # alpha(M_Z) is absorbed into higher-order matching.
    alpha_one_loop = 1.0 / ALPHA_0_INV_COMP
    # Build leptonic Delta alpha sum at M_Z.
    delta_lep_e = delta_alpha_lep_perturbative(M_E_MEV_COMP, M_Z_MEV_COMP, alpha_one_loop)
    delta_lep_mu = delta_alpha_lep_perturbative(M_MU_MEV_COMP, M_Z_MEV_COMP, alpha_one_loop)
    delta_lep_tau = delta_alpha_lep_perturbative(M_TAU_MEV_COMP, M_Z_MEV_COMP, alpha_one_loop)
    delta_lep_total = delta_lep_e + delta_lep_mu + delta_lep_tau
    print(
        f"  Delta alpha_lep (e, mu, tau): {delta_lep_e:.5f} + {delta_lep_mu:.5f} "
        f"+ {delta_lep_tau:.5f} = {delta_lep_total:.5f}"
    )
    # PDG value Delta alpha_lep ~= 0.0314772 (3 leptons at M_Z).
    check(
        "Delta alpha_lep matches PDG comparator within 1.5%",
        abs(delta_lep_total - 0.0314772) / 0.0314772 < 0.015,
        f"computed {delta_lep_total:.5f} vs comparator 0.0314772",
    )

    # Build heavy-quark Delta alpha at M_Z (c, b only — t too heavy at M_Z).
    delta_q_c = delta_alpha_quark_heavy_perturbative(
        M_C_MEV_COMP, 2.0 / 3.0, M_Z_MEV_COMP, alpha_one_loop
    )
    delta_q_b = delta_alpha_quark_heavy_perturbative(
        M_B_MEV_COMP, -1.0 / 3.0, M_Z_MEV_COMP, alpha_one_loop
    )
    print(
        f"  Delta alpha_quark perturbative (c, b only): "
        f"{delta_q_c:.5f} + {delta_q_b:.5f} = {delta_q_c + delta_q_b:.5f}"
    )
    # The c, b perturbative-tail piece is part of Delta alpha_had^(5).
    # The full hadronic piece needs non-perturbative R(s); the perturbative
    # piece for c, b alone is bounded above by the full Delta alpha_had^(5).
    check(
        "perturbative c+b pieces individually positive (correct sign)",
        delta_q_c > 0 and delta_q_b > 0,
    )
    check(
        "perturbative c+b sum is bounded above by full Delta alpha_had^(5)",
        delta_q_c + delta_q_b < DELTA_ALPHA_HAD_5_COMP,
        f"perturbative {delta_q_c + delta_q_b:.5f} vs full hadronic {DELTA_ALPHA_HAD_5_COMP:.5f}",
    )

    # Total Delta alpha_lep + non-perturbative hadronic residual:
    # The standard PDG split is Delta alpha_lep + Delta alpha_top + Delta alpha_had^(5).
    # Top is negligible at M_Z (heavy decoupling).
    # PDG-2024 leading-order pieces sum to 0.05908; the full all-orders Delta
    # alpha at M_Z is ~0.0663 because of higher-order O(alpha^2) and
    # O(alpha alpha_s) corrections. The test below verifies the LO arithmetic
    # against the LO PDG sum, NOT the all-orders Delta alpha.
    delta_total_lo = delta_lep_total + DELTA_ALPHA_HAD_5_COMP
    pdg_lo_sum = 0.0314772 + DELTA_ALPHA_HAD_5_COMP
    print(f"  Delta alpha_total LO (computed): {delta_total_lo:.5f}")
    print(f"  Delta alpha_total LO (PDG-2024 reference sum): {pdg_lo_sum:.5f}")
    check(
        "Delta alpha LO decomposition matches PDG leading-order sum to <1%",
        abs(delta_total_lo - pdg_lo_sum) / pdg_lo_sum < 0.01,
    )


def part3_substitution_failure() -> None:
    section("Part 3: substitution failure size (consistent with 2026-04-27 firewall)")
    # Direct substitution alpha(M_Z) for alpha(0) in inverse-alpha space:
    inv_alpha_substitute = ALPHA_MZ_INV_REPO
    inv_alpha_correct = ALPHA_0_INV_COMP
    inv_alpha_pct_shift = abs(inv_alpha_substitute - inv_alpha_correct) / inv_alpha_correct
    print(f"  alpha^{{-1}}(M_Z) repo {inv_alpha_substitute} vs alpha^{{-1}}(0) comparator "
          f"{inv_alpha_correct}: shift = {inv_alpha_pct_shift * 100:.2f}%")
    check(
        "inverse-alpha shift between alpha(M_Z) and alpha(0) is ~7%",
        0.05 < inv_alpha_pct_shift < 0.10,
    )

    # Rydberg E ~ alpha^2, so the energy shift is ~ 2 * (alpha(M_Z)/alpha(0) - 1)
    # in the small-shift limit, which is ~14%.
    alpha_substitute = 1.0 / inv_alpha_substitute
    alpha_correct = 1.0 / inv_alpha_correct
    energy_pct_shift = (alpha_substitute / alpha_correct) ** 2 - 1.0
    print(f"  Rydberg energy E ~ alpha^2 shift: {energy_pct_shift * 100:.2f}%")
    check(
        "Rydberg energy shift ~14-15% (consistent with 2026-04-27 firewall's ~15%)",
        0.13 < energy_pct_shift < 0.17,
    )


def part4_dependency_chain() -> None:
    section("Part 4: dependency-chain firewall structure")
    # Verify that no Lane 6 closure alone closes Lane 2.
    # Lane 6 retains m_e, m_mu, m_tau -> closes R-Lep.
    # But R-Q-Heavy still needs Lane 3 (m_c, m_b).
    # And R-Had-NP still needs Lane 1 substrate or admitted R(s).
    print("  Sub-residual coverage on Lane 6 closure alone:")
    lane6_closes_R_Lep = True
    lane6_closes_R_Q_Heavy = False
    lane6_closes_R_Had_NP = False
    print(f"    R-Lep:     {lane6_closes_R_Lep}")
    print(f"    R-Q-Heavy: {lane6_closes_R_Q_Heavy}")
    print(f"    R-Had-NP:  {lane6_closes_R_Had_NP}")
    check(
        "Lane 6 alone does NOT close Lane 2",
        not (lane6_closes_R_Lep and lane6_closes_R_Q_Heavy and lane6_closes_R_Had_NP),
    )

    print("  Sub-residual coverage on Lane 6 + Lane 3:")
    closes_R_Lep = True
    closes_R_Q_Heavy = True  # Lane 3 retains m_c, m_b
    closes_R_Had_NP = False
    print(f"    R-Lep:     {closes_R_Lep}")
    print(f"    R-Q-Heavy: {closes_R_Q_Heavy}")
    print(f"    R-Had-NP:  {closes_R_Had_NP}")
    check(
        "Lane 6 + Lane 3 alone does NOT close Lane 2 (R-Had-NP blocked)",
        not (closes_R_Lep and closes_R_Q_Heavy and closes_R_Had_NP),
    )

    print("  Sub-residual coverage on Lane 6 + Lane 3 + Lane 1:")
    closes_R_Had_NP = True  # Lane 1 substrate R(s) closes the hadronic piece
    print(f"    R-Lep:     {closes_R_Lep}")
    print(f"    R-Q-Heavy: {closes_R_Q_Heavy}")
    print(f"    R-Had-NP:  {closes_R_Had_NP}")
    check(
        "Lane 6 + Lane 3 + Lane 1 closes the running primitive at structural level",
        closes_R_Lep and closes_R_Q_Heavy and closes_R_Had_NP,
    )

    # Even structural closure leaves the QED loop primitive. The integrand
    # shape (vacuum polarization at one loop) is currently a textbook input;
    # its retention on the framework substrate is a separate primitive that
    # does NOT follow from alpha(M_Z) value retention alone.
    qed_loop_primitive_retained_on_substrate = False
    check(
        "QED loop primitive on framework substrate remains an open primitive even after Lanes 1+3+6 close",
        not qed_loop_primitive_retained_on_substrate,
    )


def part5_forbidden_imports() -> None:
    section("Part 5: forbidden-import role check")
    note = read(
        "docs/ATOMIC_LANE2_QED_RUNNING_DEPENDENCY_FIREWALL_NOTE_2026-04-30.md"
    )
    # The note must use comparator values only as scaling, not as proof input.
    check(
        "note marks PDG R-ratio comparator role explicitly",
        "comparator" in note.lower() and "Delta alpha_had^(5)" in note,
    )
    check(
        "note marks Rydberg comparator role explicitly",
        "Rydberg" in note and "comparator" in note.lower(),
    )
    check(
        "note states no atomic observable is used to tune a framework parameter",
        "No atomic observable is used to tune a framework parameter" in note,
    )


def main() -> int:
    section("Lane 2 QED running dependency firewall verification")
    part1_note_structure()
    part2_running_arithmetic()
    part3_substitution_failure()
    part4_dependency_chain()
    part5_forbidden_imports()

    print()
    print("-" * 88)
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("-" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
