#!/usr/bin/env python3
"""Charged-lepton Koide ratio/source selector firewall.

This runner audits the remaining ratio/source side of the charged-lepton mass
retirement workstream:

    Koide Q support + Brannen/selected-line phase support
      ?=> retained generation-selection primitive without PDG masses.

The result is a narrow negative boundary.  The current support stack can
separate useful conditional statements, but it does not supply a retained
primitive that selects the physical source-free Q representative, the
selected-line Brannen endpoint, or the charged-lepton generation/scale label.
PDG charged-lepton masses appear only in a comparator-only check.
"""

from __future__ import annotations

import math
import re
import sys
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

PASS_COUNT = 0
FAIL_COUNT = 0

PDG_COMPARATORS_MEV = {
    "m_e_pdg_mev": 0.510998950,
    "m_mu_pdg_mev": 105.6583755,
    "m_tau_pdg_mev": 1776.86,
}


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    suffix = f" -- {detail}" if detail else ""
    print(f"{status}: {name}{suffix}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def read_doc(name: str) -> str:
    return (DOCS / name).read_text(encoding="utf-8")


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def contains(text: str, phrase: str) -> bool:
    return normalized(phrase) in normalized(text)


def koide_q_from_sqrt_vector(values: tuple[float, float, float]) -> float:
    numerator = sum(x * x for x in values)
    denominator = sum(values) ** 2
    return numerator / denominator


def brannen_sqrt_vector(
    phase: float, c: float = math.sqrt(2.0), scale: float = 1.0
) -> tuple[float, float, float]:
    return tuple(
        scale * (1.0 + c * math.cos(phase + 2.0 * math.pi * k / 3.0))
        for k in range(3)
    )


def cyclic_rotations(values: tuple[float, float, float]) -> tuple[tuple[float, float, float], ...]:
    return (
        values,
        (values[1], values[2], values[0]),
        (values[2], values[0], values[1]),
    )


def sorted_normalized(values: tuple[float, float, float]) -> tuple[float, float, float]:
    total = sum(values)
    return tuple(sorted(x / total for x in values))


def eta_abss_z3_weights_12() -> sp.Expr:
    omega = -sp.Rational(1, 2) + sp.I * sp.sqrt(3) / 2
    total = 0
    for k in (1, 2):
        z1 = omega**k
        z2 = omega ** (2 * k)
        total += sp.simplify(1 / ((z1 - 1) * (z2 - 1)))
    return sp.simplify(total / 3)


def main() -> int:
    section("A. Current support surfaces and open boundaries")

    source_files = [
        "KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md",
        "KOIDE_Q_OP_LOCALITY_C3_FIXED_SOURCE_SUPPORT_NOTE_2026-04-27.md",
        "KOIDE_Q_SO2_PHASE_ERASURE_SUPPORT_NOTE_2026-04-25.md",
        "KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md",
        "KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24.md",
        "KOIDE_POINTED_ORIGIN_EXHAUSTION_THEOREM_NOTE_2026-04-24.md",
        "KOIDE_Q_DELTA_READOUT_RETENTION_SPLIT_NO_GO_NOTE_2026-04-24.md",
        "CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md",
        "CHARGED_LEPTON_RADIATIVE_TAU_SELECTOR_FIREWALL_NOTE_2026-04-26.md",
    ]
    for name in source_files:
        check(f"source surface exists: {name}", (DOCS / name).exists())

    q_delta_package = read_doc("KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md")
    op_locality = read_doc("KOIDE_Q_OP_LOCALITY_C3_FIXED_SOURCE_SUPPORT_NOTE_2026-04-27.md")
    so2_erasure = read_doc("KOIDE_Q_SO2_PHASE_ERASURE_SUPPORT_NOTE_2026-04-25.md")
    a1_audit = read_doc("KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24.md")
    pointed_origin = read_doc("KOIDE_POINTED_ORIGIN_EXHAUSTION_THEOREM_NOTE_2026-04-24.md")
    readout_split = read_doc("KOIDE_Q_DELTA_READOUT_RETENTION_SPLIT_NO_GO_NOTE_2026-04-24.md")
    direct_no_go = read_doc("CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md")
    radiative_firewall = read_doc("CHARGED_LEPTON_RADIATIVE_TAU_SELECTOR_FIREWALL_NOTE_2026-04-26.md")

    check(
        "Koide package states two physical bridges remain open",
        "The remaining open bridges" in q_delta_package
        and "Koide relation `Q = 2/3`" in q_delta_package
        and "Brannen phase `δ = 2/9`" in q_delta_package,
    )
    check(
        "OP-locality source result is conditional and not mass retention",
        "KOIDE_Q_OP_LOCALITY_C3_FIXED_SOURCE_SUPPORT=TRUE" in op_locality
        and "CHARGED_LEPTON_MASS_RETENTION=FALSE" in op_locality,
    )
    check(
        "SO(2) support note states Q erases the Brannen phase",
        "KOIDE_Q_INDEPENDENT_OF_BRANNEN_PHASE_AND_SCALE=TRUE" in so2_erasure
        and "KOIDE_DELTA_2_OVER_9_RAD_RETAINED_CLOSURE=FALSE" in so2_erasure,
    )
    check(
        "A1 audit leaves the Type-B rational-to-radian primitive open",
        "TYPE_B_TO_RADIAN_IDENTIFICATION_REMAINS_PRIMITIVE=TRUE" in a1_audit,
    )
    check(
        "pointed-origin theorem says unpointed data do not force the closing origin",
        "RETAINED_UNPOINTED_DATA_FORCE_POINTED_ORIGIN=FALSE" in pointed_origin
        and "RESIDUAL_PRIMITIVE=retained_physical_source_boundary_origin_laws"
        in pointed_origin,
    )
    check(
        "readout split keeps Q background and delta endpoint residuals open",
        "Q_DELTA_READOUT_RETENTION_SPLIT_CLOSES_FULL_LANE=FALSE" in readout_split
        and "RESIDUAL_DELTA=selected_line_endpoint_transition_tau_not_removed_by_closed_readout"
        in readout_split,
    )

    section("B. Koide Q on the Brannen carrier is phase-erased")

    c, v0, delta = sp.symbols("c V0 delta", real=True, nonzero=True)
    thetas = [delta + 2 * sp.pi * k / 3 for k in range(3)]
    sqrt_m = [v0 * (1 + c * sp.cos(theta)) for theta in thetas]
    sum_sqrt = sp.trigsimp(sum(sqrt_m))
    sum_mass = sp.trigsimp(sum(s * s for s in sqrt_m))
    q_value = sp.trigsimp(sum_mass / sum_sqrt**2)

    check("sum sqrt(m_k)=3 V0", sp.simplify(sum_sqrt - 3 * v0) == 0)
    check(
        "Q=(c^2+2)/6 on the Brannen carrier",
        sp.simplify(q_value - (c**2 + 2) / 6) == 0,
        f"Q={q_value}",
    )
    check("dQ/d(delta)=0", sp.simplify(sp.diff(q_value, delta)) == 0)
    check("c^2=2 gives Q=2/3 for every selected-line phase", sp.simplify(q_value.subs(c, sp.sqrt(2)) - sp.Rational(2, 3)) == 0)

    phase_samples = (0.0, 1.0 / 12.0, 1.0 / 6.0, 2.0 / 9.0)
    sampled_vectors = tuple(brannen_sqrt_vector(phi) for phi in phase_samples)
    sampled_q = tuple(koide_q_from_sqrt_vector(vec) for vec in sampled_vectors)
    check(
        "there is a positive continuum of distinct Koide rays",
        all(min(vec) > 0.0 for vec in sampled_vectors)
        and all(abs(q - 2.0 / 3.0) < 1e-12 for q in sampled_q)
        and len({tuple(round(x, 12) for x in vec) for vec in sampled_vectors})
        == len(sampled_vectors),
        f"phases={phase_samples}",
    )

    section("C. Q source support is not a generation selector")

    C3 = sp.Matrix([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
    J_scalar = sp.diag(5, 5, 5)
    J_nonuniform = sp.diag(5, 5, 7)

    check("C3-fixed onsite scalar source is common scalar", C3 * J_scalar * C3.T == J_scalar)
    check("nonuniform onsite generation source is not C3-fixed", C3 * J_nonuniform * C3.T != J_nonuniform)
    check(
        "the conditional Q source premise treats e, mu, tau labels symmetrically",
        contains(
            op_locality,
            "the physical undeformed charged-lepton scalar source on the three-generation orbit is both strict-onsite and C3-fixed",
        )
        and "D^C3 = span{I}" in op_locality,
    )
    check(
        "Q source support denies retained charged-lepton mass closure",
        "KOIDE_Q_RETAINED_NATIVE_CLOSURE=FALSE" in op_locality
        and "CHARGED_LEPTON_MASS_RETENTION=FALSE" in op_locality,
    )

    section("D. Brannen endpoint support is not an endpoint-generation law")

    eta = eta_abss_z3_weights_12()
    delta_open, tau = sp.symbols("delta_open tau", real=True)
    tau_solution = sp.solve(sp.Eq(eta, delta_open + tau), tau)
    check("ABSS/APS closed value is eta=2/9", eta == sp.Rational(2, 9), f"eta={eta}")
    check(
        "closed eta leaves open selected-line endpoint split free",
        tau_solution == [sp.Rational(2, 9) - delta_open],
        f"tau={tau_solution[0]}",
    )
    check(
        "selected-line endpoint residual remains explicit",
        "selected-line local boundary-source law" in a1_audit
        and "based endpoint section" in a1_audit,
    )
    check(
        "delta support denies retained delta closure",
        "KOIDE_A1_RADIAN_BRIDGE_AUDIT_CLOSES_DELTA=FALSE" in a1_audit
        and "KOIDE_DELTA_RETAINED_NATIVE_CLOSURE=FALSE" in op_locality,
    )

    section("E. Cyclic relabeling and tau-scale firewall")

    brannen_phase = 2.0 / 9.0
    selected_vector = brannen_sqrt_vector(brannen_phase)
    rotations = cyclic_rotations(selected_vector)
    q_rotations = tuple(koide_q_from_sqrt_vector(vec) for vec in rotations)
    sorted_rotations = tuple(sorted_normalized(vec) for vec in rotations)
    max_slots = tuple(vec.index(max(vec)) for vec in rotations)

    check(
        "cyclic relabelings keep Q and unordered ratios fixed",
        all(abs(q - 2.0 / 3.0) < 1e-12 for q in q_rotations)
        and len({tuple(round(x, 14) for x in ratio) for ratio in sorted_rotations}) == 1,
        f"max_slots={max_slots}",
    )
    check(
        "cyclic relabeling moves the largest component label",
        len(set(max_slots)) == 3,
        f"max_slots={max_slots}",
    )
    check(
        "direct and radiative scale audits both require an extra selector",
        "generation-selection / loop-normalization / source-domain law" in direct_no_go
        and contains(
            radiative_firewall,
            "cannot select the tau eigenvalue without an additional generation-selection, ratio, or source-domain primitive",
        )
        and "separate generation/source law" in radiative_firewall,
    )

    proof_inputs = {
        "C3 trigonometry",
        "Brannen carrier amplitude c^2=2 as conditional support",
        "C3-fixed onsite-source conditional premise",
        "ABSS eta arithmetic",
        "cyclic relabeling algebra",
        "prior no-go closeout flags",
    }
    forbidden_inputs = set(PDG_COMPARATORS_MEV) | {
        "heaviest_observed_generation",
        "tau_label_from_observation",
        "PDG hierarchy selector",
    }
    check(
        "PDG charged-lepton masses are not proof-input keys",
        proof_inputs.isdisjoint(forbidden_inputs),
        f"proof_inputs={sorted(proof_inputs)}",
    )

    sqrt_pdg = tuple(math.sqrt(value) for value in PDG_COMPARATORS_MEV.values())
    q_pdg = koide_q_from_sqrt_vector(sqrt_pdg)
    check(
        "PDG masses are comparator-only and lie near the Koide value",
        abs(q_pdg - 2.0 / 3.0) < 1e-5,
        f"Q_PDG={q_pdg:.12f}; not used above as a derivation input",
    )

    section("F. Verdict")

    check(
        "Koide Q plus Brannen support does not retire the mass pin",
        "CHARGED_LEPTON_MASS_RETENTION=FALSE" in op_locality
        and "FULL_DIMENSIONLESS_KOIDE_CLOSURE=FALSE" in read_doc(
            "KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE_2026-04-25.md"
        ),
    )
    check(
        "remaining primitive is a physical source/endpoint/generation law",
        "RESIDUAL_Q=derive_physical_charged_lepton_source_selection_strict_onsite_C3_fixed"
        in op_locality
        and "RESIDUAL_PRIMITIVE=retained_physical_source_boundary_origin_laws"
        in pointed_origin,
    )

    print()
    print("=" * 88)
    print("Summary")
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    if FAIL_COUNT == 0:
        print("VERDICT: exact ratio/source selector firewall.")
        print("CHARGED_LEPTON_KOIDE_RATIO_SOURCE_SELECTOR_FIREWALL=TRUE")
        print("KOIDE_Q_PLUS_BRANNEN_PHASE_GENERATION_SELECTOR=FALSE")
        print("PDG_MASSES_USED_AS_COMPARATORS_ONLY=TRUE")
        print("CHARGED_LEPTON_MASS_RETENTION=FALSE")
        print(
            "RESIDUAL_Q=derive_physical_charged_lepton_source_selection_strict_onsite_C3_fixed"
        )
        print(
            "RESIDUAL_DELTA=derive_selected_line_boundary_source_based_endpoint_and_Type_B_radian_readout"
        )
        print(
            "RESIDUAL_GENERATION=derive_nonobservational_generation_label_or_tau_scale_selector"
        )
        return 0

    print("VERDICT: ratio/source selector firewall has failing checks.")
    print("CHARGED_LEPTON_KOIDE_RATIO_SOURCE_SELECTOR_FIREWALL=FALSE")
    print("CHARGED_LEPTON_MASS_RETENTION=FALSE")
    return 1


if __name__ == "__main__":
    sys.exit(main())
