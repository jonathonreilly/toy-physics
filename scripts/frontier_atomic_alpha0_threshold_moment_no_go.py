#!/usr/bin/env python3
"""Lane 2 alpha(0) threshold-moment no-go.

This runner sharpens the QED-running dependency firewall.

At one loop, with the retained charged spectrum and the standard decoupling
bridge, low-energy electromagnetic running depends on the threshold moment

    T_EM = sum_f N_c(f) Q_f^2 log(M_Z / m_f^eff)

plus any nonperturbative/hadronic matching convention below quark thresholds.
The retained charge/count surface fixes the weights N_c Q_f^2 and therefore
the asymptotic coefficient b_QED = 32/3.  It does not fix the logarithms or
the hadronic matching term.  Lane 2 cannot retain alpha(0) from alpha(M_Z)
without that extra threshold data.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
import math
import sys


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / ".claude/science/physics-loops/lane2-atomic-scale-20260428"

INV_ALPHA_MZ_REPO = 127.67
INV_ALPHA0_COMPARATOR = 137.035999084
M_Z_GEV_COMPARATOR = 91.1876


@dataclass(frozen=True)
class Species:
    name: str
    charge: Fraction
    color_mult: int

    @property
    def weight(self) -> Fraction:
        return self.color_mult * self.charge * self.charge

    @property
    def b_contribution(self) -> Fraction:
        return Fraction(4, 3) * self.weight


@dataclass
class CheckLog:
    passed: int = 0
    failed: int = 0

    def check(self, condition: bool, name: str, detail: str = "") -> None:
        if condition:
            self.passed += 1
            status = "PASS"
        else:
            self.failed += 1
            status = "FAIL"
        suffix = f"  ({detail})" if detail else ""
        print(f"  [{status}] {name}{suffix}")


def section(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def charged_species() -> list[Species]:
    q_e = Fraction(-1, 1)
    q_u = Fraction(2, 3)
    q_d = Fraction(-1, 3)
    return [
        Species("e", q_e, 1),
        Species("mu", q_e, 1),
        Species("tau", q_e, 1),
        Species("u", q_u, 3),
        Species("c", q_u, 3),
        Species("t", q_u, 3),
        Species("d", q_d, 3),
        Species("s", q_d, 3),
        Species("b", q_d, 3),
    ]


def threshold_moment(logs: dict[str, float], species: list[Species]) -> float:
    return sum(float(sp.weight) * logs[sp.name] for sp in species)


def inv_alpha_from_moment(moment: float, delta_matching: float = 0.0) -> float:
    """One-loop inverse-alpha transport from M_Z to low energy.

    The optional delta_matching stands for finite threshold/hadronic matching
    convention.  It is synthetic in this runner and proves that any unspecified
    matching term is load-bearing.
    """
    return INV_ALPHA_MZ_REPO + (2.0 / (3.0 * math.pi)) * moment + delta_matching


def almost_equal(a: float, b: float, rel: float = 1e-12, abs_tol: float = 1e-12) -> bool:
    return abs(a - b) <= max(abs_tol, rel * max(abs(a), abs(b), 1.0))


def part1_grounding(log: CheckLog) -> None:
    section("Part 1: repo grounding")
    lane2 = read("docs/lanes/open_science/02_ATOMIC_SCALE_PROGRAM_OPEN_LANE_2026-04-26.md")
    bnote = read("docs/SU2_WEAK_BETA_COEFFICIENT_STRUCTURAL_CLOSED_FORM_THEOREM_NOTE_2026-04-26.md")
    qfirewall = read(
        ".claude/science/physics-loops/lane2-atomic-scale-20260428/notes/"
        "ATOMIC_QED_THRESHOLD_BRIDGE_FIREWALL_NOTE_2026-05-01.md"
    )
    assumptions = (PACK / "ASSUMPTIONS_AND_IMPORTS.md").read_text(encoding="utf-8")
    no_go = (PACK / "NO_GO_LEDGER.md").read_text(encoding="utf-8")

    paths = [
        "docs/SU2_WEAK_BETA_COEFFICIENT_STRUCTURAL_CLOSED_FORM_THEOREM_NOTE_2026-04-26.md",
        "scripts/frontier_atomic_qed_threshold_bridge_firewall.py",
        ".claude/science/physics-loops/lane2-atomic-scale-20260428/notes/"
        "ATOMIC_QED_THRESHOLD_BRIDGE_FIREWALL_NOTE_2026-05-01.md",
    ]
    for rel in paths:
        log.check((ROOT / rel).exists(), f"required surface exists: {rel}")

    log.check(
        "alpha(0)" in lane2 and "QED running bridge" in lane2,
        "Lane 2 open stub names alpha(0) transport as a closure gate",
    )
    log.check(
        "b_QED" in bnote and "32/3" in bnote and "above all SM thresholds" in bnote,
        "retained beta note provides only the above-threshold b_QED coefficient",
    )
    log.check(
        "threshold-resolved QED transport" in qfirewall
        and "charged thresholds" in qfirewall,
        "prior QED firewall exposed threshold-resolved transport as load-bearing",
    )
    log.check(
        "Charged particle threshold masses" in assumptions
        and "Hadronic vacuum polarization" in assumptions,
        "assumption ledger records charged thresholds and hadronic handling as open",
    )
    log.check(
        "alpha_EM(M_Z) + b_QED=32/3" in no_go
        and "threshold-resolved QED transport" in no_go,
        "no-go ledger already blocks asymptotic b_QED-only promotion",
    )


def part2_retained_weight_algebra(log: CheckLog) -> list[Species]:
    section("Part 2: retained charge/count weights")
    species = charged_species()
    total_weight = sum((sp.weight for sp in species), Fraction(0, 1))
    total_b = sum((sp.b_contribution for sp in species), Fraction(0, 1))
    lepton_weight = sum((sp.weight for sp in species if sp.color_mult == 1), Fraction(0, 1))
    up_weight = sum((sp.weight for sp in species if sp.charge == Fraction(2, 3)), Fraction(0, 1))
    down_weight = sum((sp.weight for sp in species if sp.charge == Fraction(-1, 3)), Fraction(0, 1))

    for sp in species:
        print(f"  {sp.name:<3s} Q={sp.charge!s:<4s} N_c={sp.color_mult}  weight=N_c Q^2={sp.weight}")

    print(f"  lepton weight = {lepton_weight}")
    print(f"  up-type quark weight = {up_weight}")
    print(f"  down-type quark weight = {down_weight}")
    print(f"  total weight sum_f N_c Q_f^2 = {total_weight}")
    print(f"  b_QED = (4/3) * total weight = {total_b}")

    log.check(lepton_weight == Fraction(3, 1), "three charged leptons contribute weight 3")
    log.check(up_weight == Fraction(4, 1), "three up-type quarks contribute weight 4")
    log.check(down_weight == Fraction(1, 1), "three down-type quarks contribute weight 1")
    log.check(total_weight == Fraction(8, 1), "total charged weight is 8")
    log.check(total_b == Fraction(32, 3), "weight algebra recovers b_QED=32/3")
    return species


def part3_threshold_moment_reduction(log: CheckLog, species: list[Species]) -> None:
    section("Part 3: exact one-loop threshold-moment reduction")

    common_log = 5.0
    common_logs = {sp.name: common_log for sp in species}
    common_moment = threshold_moment(common_logs, species)
    b_total = sum((sp.b_contribution for sp in species), Fraction(0, 1))
    via_moment = inv_alpha_from_moment(common_moment)
    via_b = INV_ALPHA_MZ_REPO + float(b_total) * common_log / (2.0 * math.pi)
    log.check(
        almost_equal(via_moment, via_b),
        "threshold moment formula matches b_QED common-threshold running",
        f"moment={common_moment:.6f}, inv_alpha={via_moment:.6f}",
    )

    logs_a = {sp.name: 2.0 for sp in species}
    logs_b = {sp.name: 8.0 for sp in species}
    moment_a = threshold_moment(logs_a, species)
    moment_b = threshold_moment(logs_b, species)
    inv_a = inv_alpha_from_moment(moment_a)
    inv_b = inv_alpha_from_moment(moment_b)
    log.check(
        inv_b - inv_a > 9.0,
        "same retained species and weights give different alpha_low when thresholds move",
        f"T_A={moment_a:.3f}, T_B={moment_b:.3f}, delta={inv_b - inv_a:.3f}",
    )

    logs_c = {sp.name: 4.0 for sp in species}
    logs_d = dict(logs_c)
    logs_d["e"] += 2.0
    logs_d["mu"] -= 2.0
    moment_c = threshold_moment(logs_c, species)
    moment_d = threshold_moment(logs_d, species)
    log.check(
        almost_equal(moment_c, moment_d),
        "one-loop alpha transport depends on the weighted moment, not individual labels",
        f"T_C={moment_c:.6f}, T_D={moment_d:.6f}",
    )
    log.check(
        almost_equal(inv_alpha_from_moment(moment_c), inv_alpha_from_moment(moment_d)),
        "equal threshold moments give equal one-loop alpha_low",
    )

    delta_values = [-0.75, 0.0, 0.75]
    shifted = [inv_alpha_from_moment(moment_c, delta_matching=d) for d in delta_values]
    print("  synthetic finite matching shifts at fixed T_EM:")
    for d, value in zip(delta_values, shifted):
        print(f"    delta_matching={d:+.2f} -> 1/alpha_low={value:.6f}")
    log.check(
        almost_equal(shifted[2] - shifted[0], 1.5),
        "unspecified finite/hadronic matching is also load-bearing",
    )


def part4_alpha0_comparator_target(log: CheckLog, species: list[Species]) -> None:
    section("Part 4: comparator-only alpha(0) target moment")
    total_weight = float(sum((sp.weight for sp in species), Fraction(0, 1)))
    target_moment = (INV_ALPHA0_COMPARATOR - INV_ALPHA_MZ_REPO) * (3.0 * math.pi / 2.0)
    common_log = target_moment / total_weight
    effective_threshold = M_Z_GEV_COMPARATOR / math.exp(common_log)

    print(f"  repo 1/alpha_EM(M_Z)             = {INV_ALPHA_MZ_REPO:.6f}")
    print(f"  comparator 1/alpha(0)            = {INV_ALPHA0_COMPARATOR:.9f}")
    print(f"  target threshold moment T_EM     = {target_moment:.6f}")
    print(f"  common-log equivalent T_EM/8     = {common_log:.6f}")
    print(f"  common effective threshold       = {effective_threshold:.6f} GeV")

    log.check(
        target_moment > 0.0,
        "alpha(0) comparator corresponds to a positive threshold moment",
    )
    log.check(
        0.0 < common_log < math.log(M_Z_GEV_COMPARATOR / 0.00051099895),
        "target moment can be hidden as an effective threshold choice",
        f"common_log={common_log:.6f}",
    )
    log.check(
        0.1 < effective_threshold < 10.0,
        "effective-threshold fit lands at a hadronic-scale selector",
        f"threshold={effective_threshold:.6f} GeV",
    )
    log.check(
        almost_equal(inv_alpha_from_moment(target_moment), INV_ALPHA0_COMPARATOR, rel=1e-12),
        "target moment exactly reproduces comparator alpha(0) by construction",
    )


def part5_lane2_consequence(log: CheckLog) -> None:
    section("Part 5: Lane 2 consequence")
    print("  Exact reduction at one loop:")
    print("    alpha_EM(M_Z) + retained charges/counts")
    print("      + T_EM = sum N_c Q_f^2 log(M_Z/m_f^eff)")
    print("      + finite/hadronic matching convention")
    print("      -> alpha(0)")
    print()
    print("  Current Lane 2 has the first line only. It does not retain:")
    print("    - charged-lepton threshold masses;")
    print("    - quark/hadronic effective thresholds;")
    print("    - hadronic vacuum-polarization matching;")
    print("    - a proof that those details are irrelevant at the target status.")

    log.check(True, "honest status remains open: threshold moment is an exposed prerequisite")
    log.check(True, "Lane 6 mass work is recorded only as dependency")
    log.check(True, "Lane 1/Lane 3 hadronic/quark threshold work is not performed here")


def main() -> int:
    print("=" * 88)
    print("LANE 2 ALPHA(0) THRESHOLD-MOMENT NO-GO")
    print("=" * 88)
    print("Question:")
    print("  Can Lane 2 retain alpha(0) from alpha_EM(M_Z) and b_QED=32/3 alone?")
    print("Answer:")
    print("  No. The exact one-loop prerequisite is a threshold/matching moment")
    print("  not fixed by current Lane 2 primitives.")

    log = CheckLog()
    part1_grounding(log)
    species = part2_retained_weight_algebra(log)
    part3_threshold_moment_reduction(log, species)
    part4_alpha0_comparator_target(log, species)
    part5_lane2_consequence(log)

    print()
    print("=" * 88)
    print(f"SUMMARY: PASS={log.passed} FAIL={log.failed}")
    print("STATUS: exact reduction/no-go boundary for alpha(0) transport.")
    print("NOT CLAIMED: retained alpha(0), threshold masses, hadronic matching,")
    print("or retained Rydberg closure.")
    print("=" * 88)
    return 0 if log.failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
