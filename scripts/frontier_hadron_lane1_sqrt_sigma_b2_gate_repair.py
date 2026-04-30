#!/usr/bin/env python3
"""Lane 1 sqrt(sigma) B2 gate repair audit.

This runner checks the current Lane 1 string-tension boundary.  The target is
not to promote sqrt(sigma).  It verifies that the existing rough quenched to
dynamical screening factor cannot be treated as a retained closure, and that
the B2 gate must first define the dynamical observable being imported or
measured.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


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


def section(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


# Existing Method 2 constants from CONFINEMENT_STRING_TENSION_NOTE.md and the
# 2026-04-27 Lane 1 gate audit.  These are imported bridge constants, not
# framework-derived outputs.
R0_FM = 0.472
R0_OVER_A = 5.37
SIGMA_A2_QUENCHED = 0.0465
HBARC_MEV_FM = 197.327
ROUGH_SCREENING_FACTOR = 0.96
SQRT_SIGMA_COMPARATOR_MEV = 440.0
SQRT_SIGMA_COMPARATOR_SIGMA_MEV = 20.0


def sqrt_sigma_quenched_mev() -> float:
    a_fm = R0_FM / R0_OVER_A
    return math.sqrt(SIGMA_A2_QUENCHED) / a_fm * HBARC_MEV_FM


def part1_repo_claim_state() -> None:
    section("Part 1: repo claim-state boundary")
    lane = read("docs/lanes/open_science/01_HADRON_MASS_PROGRAM_OPEN_LANE_2026-04-26.md")
    support = read("docs/HADRON_LANE1_SQRT_SIGMA_RETENTION_GATE_AUDIT_SUPPORT_NOTE_2026-04-27.md")
    audit = read("docs/audit/AUDIT_LEDGER.md")

    check(
        "Lane 1 names B2 as a current highest-leverage target",
        "Current highest-leverage targets" in lane
        and ("repaired `(B2)` gate" in lane or "close the `(B2)`" in lane)
        and "`beta=6.0`, `N_f=2+1`" in lane,
    )
    check(
        "B2 is recorded as the dominant residual, not a closed result",
        "dominant residual" in support
        and "rough x0.96" in support.replace("\u00d7", "x"),
    )
    check(
        "support note refuses sqrt(sigma) promotion until B2 is replaced",
        "cannot promote past" in support
        and "proper `N_f = 2+1`" in support,
    )
    check(
        "audit ledger says confinement/string-tension chain does not close",
        "confinement_string_tension_note" in audit
        and "chain closes:** False" in audit
        and "screening factor" in audit,
    )


def part2_current_budget_arithmetic() -> None:
    section("Part 2: current Method 2 screening arithmetic")
    quenched = sqrt_sigma_quenched_mev()
    rough = quenched * ROUGH_SCREENING_FACTOR
    central_factor = SQRT_SIGMA_COMPARATOR_MEV / quenched
    low_factor = (SQRT_SIGMA_COMPARATOR_MEV - SQRT_SIGMA_COMPARATOR_SIGMA_MEV) / quenched
    high_factor = (SQRT_SIGMA_COMPARATOR_MEV + SQRT_SIGMA_COMPARATOR_SIGMA_MEV) / quenched

    print(f"  sqrt(sigma)_quenched = {quenched:.2f} MeV")
    print(f"  rough x0.96 value    = {rough:.2f} MeV")
    print(f"  comparator central factor = {central_factor:.4f}")
    print(f"  comparator 1-sigma factor band = [{low_factor:.4f}, {high_factor:.4f}]")

    check(
        "replays the existing quenched Method 2 value",
        abs(quenched - 484.0) < 1.0,
        f"{quenched:.2f} MeV",
    )
    check(
        "rough x0.96 reproduces the bounded 465 MeV scale",
        abs(rough - 465.0) < 1.0,
        f"{rough:.2f} MeV",
    )
    check(
        "central comparator would require about x0.909, not x0.96",
        abs(central_factor - 0.909) < 0.002,
        f"factor={central_factor:.4f}",
    )
    check(
        "rough x0.96 sits above the comparator one-sigma factor band",
        ROUGH_SCREENING_FACTOR > high_factor,
        f"x0.96 > {high_factor:.4f}",
    )


@dataclass(frozen=True)
class Candidate:
    name: str
    non_circular_source: bool
    has_nf21_dynamics: bool
    defines_dynamical_observable: bool
    has_uncertainty_budget: bool
    has_framework_b5_link: bool

    def closes_b2(self) -> bool:
        return (
            self.non_circular_source
            and self.has_nf21_dynamics
            and self.defines_dynamical_observable
            and self.has_uncertainty_budget
            and self.has_framework_b5_link
        )

    def count(self) -> int:
        return sum(
            [
                self.non_circular_source,
                self.has_nf21_dynamics,
                self.defines_dynamical_observable,
                self.has_uncertainty_budget,
                self.has_framework_b5_link,
            ]
        )


def part3_candidate_gate_model() -> None:
    section("Part 3: B2 closure-gate model")
    candidates = [
        Candidate(
            name="rough_x0p96_existing_factor",
            non_circular_source=True,
            has_nf21_dynamics=False,
            defines_dynamical_observable=False,
            has_uncertainty_budget=False,
            has_framework_b5_link=False,
        ),
        Candidate(
            name="pdg_backsolved_factor",
            non_circular_source=False,
            has_nf21_dynamics=False,
            defines_dynamical_observable=False,
            has_uncertainty_budget=False,
            has_framework_b5_link=False,
        ),
        Candidate(
            name="external_static_energy_or_force_bridge",
            non_circular_source=True,
            has_nf21_dynamics=True,
            defines_dynamical_observable=True,
            has_uncertainty_budget=True,
            has_framework_b5_link=False,
        ),
    ]

    for candidate in candidates:
        print(
            f"  {candidate.name}: {candidate.count()}/5 gate bits; "
            f"closes={candidate.closes_b2()}"
        )

    check(
        "existing rough factor fails the B2 closure gate",
        not candidates[0].closes_b2() and candidates[0].count() == 1,
        "no N_f=2+1 ensemble, observable definition, uncertainty, or B5 link",
    )
    check(
        "PDG backsolve fails as circular comparator use",
        not candidates[1].non_circular_source and not candidates[1].closes_b2(),
        "target value cannot define the screening factor",
    )
    check(
        "external static-energy bridge is the nearest viable route but still needs B5",
        candidates[2].count() == 4 and not candidates[2].has_framework_b5_link,
        "all but framework-to-standard-QCD linkage",
    )
    check(
        "no current-surface candidate currently closes B2",
        not any(candidate.closes_b2() for candidate in candidates),
    )


def part4_repaired_gate_artifact() -> None:
    section("Part 4: repaired gate artifact checks")
    note = read("docs/HADRON_LANE1_SQRT_SIGMA_B2_GATE_REPAIR_AUDIT_NOTE_2026-04-30.md")

    check(
        "new note splits B2 into observable-definition and bridge-value gates",
        "B2a" in note and "B2b" in note and "observable-definition" in note,
    )
    check(
        "new note records string breaking as the reason asymptotic sigma is not the target",
        "string breaking" in note and "asymptotic" in note,
    )
    check(
        "new note forbids rough-factor and comparator-backsolve promotion",
        "rough x0.96" in note
        and "PDG backsolve" in note
        and "cannot promote" in note,
    )


def main() -> int:
    print("=" * 88)
    print("LANE 1 SQRT(SIGMA) B2 GATE REPAIR AUDIT")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can the existing rough quenched-to-dynamical screening factor")
    print("  close the Lane 1 sqrt(sigma) retention gate?")
    print()
    print("Answer:")
    print("  No. B2 must first define the N_f=2+1 dynamical observable and")
    print("  then import or compute it with a residual budget and B5 linkage.")

    part1_repo_claim_state()
    part2_current_budget_arithmetic()
    part3_candidate_gate_model()
    part4_repaired_gate_artifact()

    print()
    print("=" * 88)
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
