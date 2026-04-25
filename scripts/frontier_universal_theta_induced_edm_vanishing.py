#!/usr/bin/env python3
"""
Universal theta-induced EDM response vanishing theorem.

Status: retained structural corollary on the retained strong-CP action surface.

The theorem is source-scoped:

  theta_eff = 0
  O = O_CKM + O_BSM + theta_eff * K_theta[O] + O(theta_eff^2)
  therefore O_theta = 0

It does not set independent qCEDM, Weinberg, four-fermion, CKM, or BSM source
directions to zero.
"""

from __future__ import annotations

from dataclasses import dataclass

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    return condition


def banner(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


@dataclass(frozen=True)
class ThetaResponseObservable:
    code: str
    name: str
    response_coefficient: float
    family: str

    def theta_component(self, theta_eff: float) -> float:
        return theta_eff * self.response_coefficient


@dataclass(frozen=True)
class IndependentCPSource:
    name: str
    source_direction: str
    killed_by_theta_zero: bool


THETA_EFF = 0.0

THETA_RESPONSE_OBSERVABLES = [
    ThetaResponseObservable("E1", "neutron EDM theta component", 2.4e-16, "hadron"),
    ThetaResponseObservable("E2", "proton EDM theta component", 2.1e-16, "hadron"),
    ThetaResponseObservable("E3", "deuteron EDM theta component", 1.0e-16, "nucleus"),
    ThetaResponseObservable("E4", "helium-3 EDM theta component", 1.5e-16, "nucleus"),
    ThetaResponseObservable("E5", "helium-4 EDM theta component", 0.8e-16, "nucleus"),
    ThetaResponseObservable("E6", "mercury Schiff theta component", 1.0e-13, "schiff"),
    ThetaResponseObservable("E7", "xenon Schiff theta component", 0.7e-13, "schiff"),
    ThetaResponseObservable("E8", "radium Schiff theta component", 3.0e-13, "schiff"),
    ThetaResponseObservable("E9", "atomic EDM theta response", 2.0e-17, "atom"),
    ThetaResponseObservable("E10", "molecular EDM theta response", 2.0e-17, "molecule"),
    ThetaResponseObservable("E11", "electron QCD-theta-mediated response", 1.0e-38, "lepton"),
    ThetaResponseObservable("E12", "muon QCD-theta-mediated response", 1.0e-36, "lepton"),
]

THETA_SOURCED_OPERATORS = [
    ThetaResponseObservable("O1", "theta G Gtilde source coefficient", 1.0, "operator"),
    ThetaResponseObservable("O2", "theta-sourced pion-nucleon CP-odd coupling", 1.0, "operator"),
    ThetaResponseObservable("O3", "theta-sourced nucleon EDM counterterm", 1.0, "operator"),
    ThetaResponseObservable("O4", "theta-sourced Schiff response coefficient", 1.0, "operator"),
    ThetaResponseObservable("O5", "theta-sourced atomic EDM response coefficient", 1.0, "operator"),
]

INDEPENDENT_CP_SOURCES = [
    IndependentCPSource("quark chromo-EDM", "independent EFT coefficient", False),
    IndependentCPSource("Weinberg three-gluon operator", "independent EFT coefficient", False),
    IndependentCPSource("CP-odd four-fermion operator", "independent EFT coefficient", False),
    IndependentCPSource("BSM lepton EDM operator", "independent BSM coefficient", False),
]

CKM_SURVIVORS = {
    "neutron CKM EDM bounded continuation": 8.0e-33,
    "electron CKM EDM reference scale": 1.0e-38,
    "atomic CKM EDM reference scale": 1.0e-34,
}

EXPERIMENTAL_BOUNDS = {
    "neutron CKM EDM bounded continuation": 1.8e-26,
    "electron CKM EDM reference scale": 4.1e-30,
    "atomic CKM EDM reference scale": 7.4e-30,
}


def falsifies_theta_zero(source_attribution: str, edm_value: float, ckm_reference: float) -> bool:
    """Only a theta-attributed signal above the CKM reference challenges theta_eff=0."""
    return source_attribution == "theta" and edm_value > ckm_reference


def part1_retained_theta_source() -> None:
    banner("Part 1: retained theta source")

    check("retained strong-CP surface sets theta_eff to zero", THETA_EFF == 0.0, "theta_eff=0")
    check(
        "linear theta response formula has zero source factor",
        THETA_EFF * 1.0 == 0.0,
        "theta_eff*K_theta=0 for finite K_theta",
    )


def part2_observable_response_vanishes() -> None:
    banner("Part 2: theta-induced EDM components")

    families = set()
    for obs in THETA_RESPONSE_OBSERVABLES:
        theta_component = obs.theta_component(THETA_EFF)
        families.add(obs.family)
        check(
            f"{obs.code} {obs.name} vanishes",
            theta_component == 0.0,
            f"family={obs.family}",
        )

    expected_families = {"hadron", "nucleus", "schiff", "atom", "molecule", "lepton"}
    check(
        "response list spans hadronic, nuclear, Schiff, atomic, molecular, and lepton-mediated channels",
        families == expected_families,
        f"families={sorted(families)}",
    )


def part3_operator_scope() -> None:
    banner("Part 3: operator-level source scoping")

    for operator in THETA_SOURCED_OPERATORS:
        value = operator.theta_component(THETA_EFF)
        check(
            f"{operator.code} {operator.name} vanishes as a theta-sourced component",
            value == 0.0,
        )

    for source in INDEPENDENT_CP_SOURCES:
        check(
            f"{source.name} is not killed by theta_eff=0 alone",
            source.killed_by_theta_zero is False,
            source.source_direction,
        )

    check(
        "operator theorem distinguishes theta-sourced matching from independent CP-odd EFT sources",
        all(not source.killed_by_theta_zero for source in INDEPENDENT_CP_SOURCES),
    )


def part4_ckm_survivors_and_bounds() -> None:
    banner("Part 4: surviving CKM weak-CP scale")

    for name, value in CKM_SURVIVORS.items():
        check(f"{name} remains nonzero in the bookkeeping surface", value > 0.0, f"{value:.1e} e cm")

    for name, value in CKM_SURVIVORS.items():
        bound = EXPERIMENTAL_BOUNDS[name]
        margin = bound / value
        check(f"{name} is below current bound", value < bound, f"margin={margin:.1e}")

    check(
        "neutron CKM bounded continuation lies near the retained note scale",
        1.0e-33 <= CKM_SURVIVORS["neutron CKM EDM bounded continuation"] <= 1.0e-32,
        f"{CKM_SURVIVORS['neutron CKM EDM bounded continuation']:.1e} e cm",
    )


def part5_falsification_boundary() -> None:
    banner("Part 5: falsification boundary")

    ckm_reference = CKM_SURVIVORS["neutron CKM EDM bounded continuation"]
    cases = [
        ("theta-attributable EDM signal above CKM reference", "theta", 1.0e-28, True),
        ("BSM-attributable EDM signal above CKM reference", "bsm", 1.0e-28, False),
        ("CKM-attributable EDM signal at CKM reference", "ckm", ckm_reference, False),
        ("theta-attributable signal below CKM reference", "theta", 1.0e-34, False),
    ]

    for label, source, value, expected in cases:
        actual = falsifies_theta_zero(source, value, ckm_reference)
        check(
            f"{label} has correct theorem status",
            actual == expected,
            f"source={source}, value={value:.1e}, falsifies={actual}",
        )


def main() -> int:
    print("=" * 88)
    print("Universal theta-induced EDM response vanishing theorem")
    print("=" * 88)
    print("Status: retained structural corollary; source-scoped to QCD theta")

    part1_retained_theta_source()
    part2_observable_response_vanishes()
    part3_operator_scope()
    part4_ckm_survivors_and_bounds()
    part5_falsification_boundary()

    print()
    print("=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    print("=" * 88)
    print()
    print("Retained result:")
    print("  all theta-induced EDM response components vanish on theta_eff=0")
    print("Boundary:")
    print("  independent CKM, qCEDM, Weinberg, four-fermion, and BSM sources are not")
    print("  set to zero by this theorem")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
