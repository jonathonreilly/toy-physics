#!/usr/bin/env python3
"""Lane 1 sqrt(sigma) B5 framework-to-standard-QCD link audit.

Cycle 3 of the hadron sqrt(sigma) loop.  The runner checks whether the
current repo surface already closes the B5 bridge that lets standard
lattice-QCD static-energy / string-tension inputs be applied to the
framework gauge substrate.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def state_cycle_at_least(state: str, cycle: int) -> bool:
    match = re.search(r"cycles_completed:\s*(\d+)", state)
    return bool(match) and int(match.group(1)) >= cycle


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


def part1_b5_claim_state() -> None:
    section("Part 1: B5 claim-state surface")
    gate = read("docs/HADRON_LANE1_SQRT_SIGMA_RETENTION_GATE_AUDIT_SUPPORT_NOTE_2026-04-27.md")
    conf = read("docs/CONFINEMENT_STRING_TENSION_NOTE.md")
    audit = read("docs/audit/AUDIT_LEDGER.md")

    check(
        "Lane 1 gate audit marks B5 as open structural bridge",
        "Framework `SU(3)`" in gate
        and "standard `SU(3) YM` identification" in gate
        and "unquantified" in gate,
    )
    check(
        "B5 paths require volume scaling or asymptotic Wilson-loop checks",
        "Path A (volume scaling)" in gate
        and "Path B (Wilson loop area-law verification)" in gate
        and "Path C (independent Creutz-ratio measurement)" in gate,
    )
    check(
        "confinement note says quantitative sigma uses standard lattice simulations",
        "standard lattice QCD simulations" in conf
        and "not from the" in conf
        and "framework's Planck-scale lattice" in conf,
    )
    check(
        "audit ledger keeps confinement/string-tension row conditional",
        "confinement_string_tension_note" in audit
        and "chain closes:** False" in audit
        and "standard_lattice_qcd_sommer_and_string_tension_inputs" in audit,
    )


def part2_dependency_status() -> None:
    section("Part 2: B5 dependency status")
    graph = read("docs/GRAPH_FIRST_SU3_INTEGRATION_NOTE.md")
    gb = read("docs/G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md")
    plaq = read("scripts/canonical_plaquette_surface.py")
    conf_script = read("scripts/frontier_confinement_string_tension.py")

    check(
        "graph-first SU3 support is structural, not a lattice-QCD dynamics equivalence",
        "structural `SU(3)` hole" in graph
        and "What remains bounded" in graph,
    )
    check(
        "g_bare normalization leaves Wilson action form imported",
        "What does NOT close" in gb
        and "action-choice objection" in gb
        and "lattice gauge action" in gb
        and "functional form" in gb,
    )
    check(
        "canonical plaquette surface stores evaluated constants, not a volume-scaling proof",
        "CANONICAL_PLAQUETTE = 0.5934" in plaq
        and "CANONICAL_ALPHA_BARE" in plaq,
    )
    check(
        "confinement runner still hard-codes standard lattice bridge constants",
        "p_lattice_qcd = 0.5934" in conf_script
        and "r0_over_a = 5.37" in conf_script
        and "sigma_a2_quenched = 0.0465" in conf_script,
    )


@dataclass(frozen=True)
class B5Candidate:
    name: str
    framework_side_measurement: bool
    large_volume_or_asymptotic: bool
    standard_qcd_comparator: bool
    action_form_residual_declared: bool
    uncertainty_budget: bool

    def closes_b5(self) -> bool:
        return (
            self.framework_side_measurement
            and self.large_volume_or_asymptotic
            and self.standard_qcd_comparator
            and self.action_form_residual_declared
            and self.uncertainty_budget
        )

    def count(self) -> int:
        return sum(
            [
                self.framework_side_measurement,
                self.large_volume_or_asymptotic,
                self.standard_qcd_comparator,
                self.action_form_residual_declared,
                self.uncertainty_budget,
            ]
        )


def part3_gate_model() -> None:
    section("Part 3: B5 closure-gate model")
    candidates = [
        B5Candidate(
            name="current_4^4_plaquette_wilson_loop_check",
            framework_side_measurement=True,
            large_volume_or_asymptotic=False,
            standard_qcd_comparator=True,
            action_form_residual_declared=True,
            uncertainty_budget=False,
        ),
        B5Candidate(
            name="graph_first_su3_plus_gbare_normalization",
            framework_side_measurement=False,
            large_volume_or_asymptotic=False,
            standard_qcd_comparator=False,
            action_form_residual_declared=True,
            uncertainty_budget=False,
        ),
        B5Candidate(
            name="future_large_volume_creutz_or_force_scale_ladder",
            framework_side_measurement=True,
            large_volume_or_asymptotic=True,
            standard_qcd_comparator=True,
            action_form_residual_declared=True,
            uncertainty_budget=True,
        ),
    ]

    for candidate in candidates:
        print(f"  {candidate.name}: {candidate.count()}/5 gate bits; closes={candidate.closes_b5()}")

    check(
        "current 4^4 check is useful but fails large-volume and uncertainty gates",
        candidates[0].count() == 3 and not candidates[0].closes_b5(),
    )
    check(
        "structural SU3/g_bare support does not by itself instantiate lattice dynamics",
        candidates[1].count() == 1 and not candidates[1].framework_side_measurement,
    )
    check(
        "future large-volume Creutz/force ladder would close the B5 gate by construction",
        candidates[2].closes_b5(),
    )
    check(
        "no current-surface B5 candidate closes",
        not any(candidate.closes_b5() for candidate in candidates[:2]),
    )


def part4_artifact_checks() -> None:
    section("Part 4: artifact checks")
    note = read("docs/HADRON_LANE1_SQRT_SIGMA_B5_FRAMEWORK_LINK_AUDIT_NOTE_2026-04-30.md")
    handoff = read(".claude/science/physics-loops/hadron-sqrt-sigma-b2-20260430/HANDOFF.md")
    state = read(".claude/science/physics-loops/hadron-sqrt-sigma-b2-20260430/STATE.yaml")

    check(
        "note records B5 as current-surface no-go, not closure",
        "current-surface no-go" in note and "not close B5" in note,
    )
    check(
        "note defines the future large-volume ladder",
        "L = 4, 6, 8" in note and "force-scale ladder" in note,
    )
    check(
        "branch-local handoff includes the B5 framework-link runner",
        "HADRON_LANE1_SQRT_SIGMA_B5_FRAMEWORK_LINK_AUDIT_NOTE_2026-04-30.md" in handoff
        and "frontier_hadron_lane1_sqrt_sigma_b5_framework_link_audit.py" in handoff,
    )
    check(
        "loop state advanced to cycle 3",
        state_cycle_at_least(state, 3) and "cycle-3-complete" in state,
    )


def main() -> int:
    print("=" * 88)
    print("LANE 1 SQRT(SIGMA) B5 FRAMEWORK LINK AUDIT")
    print("=" * 88)
    print()
    print("Question:")
    print("  Does the current repo surface close the framework-to-standard-QCD")
    print("  link needed to import static-energy/string-tension bridge values?")
    print()
    print("Answer:")
    print("  No. The current surface has structural SU(3) and beta=6 support,")
    print("  but not a large-volume framework-side Wilson/Creutz/force-scale")
    print("  validation with uncertainty.")

    part1_b5_claim_state()
    part2_dependency_status()
    part3_gate_model()
    part4_artifact_checks()

    print()
    print("=" * 88)
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
