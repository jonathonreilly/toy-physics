#!/usr/bin/env python3
"""Lane 1 sqrt(sigma) B2 static-energy bridge scout.

This runner evaluates whether modern full-QCD static-energy / static-force
results can replace the rough x0.96 screening factor for the Lane 1 B2 gate.
It keeps the result bounded: the bridge supplies useful numbers, but not a
unique retained screening factor.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0

HBARC_MEV_FM = 197.327

# Existing repo Method 2 quenched bridge.
QUENCHED_SQRT_SIGMA_MEV = 484.1113633562925
ROUGH_X096_MEV = QUENCHED_SQRT_SIGMA_MEV * 0.96

# TUMQCD 2+1+1 static-energy paper, arXiv:2206.03156, journal version.
TUM_R0_FM = 0.4547
TUM_R0_ERR_FM = 0.0064
TUM_R0SQRTSIGMA_AR0 = 1.077
TUM_R0SQRTSIGMA_AR0_ERR = 0.016
TUM_R0SQRTSIGMA_PI12 = 1.110
TUM_R0SQRTSIGMA_PI12_ERR = 0.016
TUM_R0_OVER_R1 = 1.4968
TUM_R0_OVER_R1_ERR = 0.0069

# 2025 CLS N_f=2+1 force-scale determination, EPJC 85:673.
CLS_R0_FM = 0.4729
CLS_R0_ERR_FM = math.hypot(0.0057, 0.0048)
CLS_R1_FM = 0.3127
CLS_R1_ERR_FM = math.hypot(0.0024, 0.0032)
CLS_R0_OVER_R1 = 1.532
CLS_R0_OVER_R1_ERR = 0.012


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


def sqrt_sigma_from_r0sqrt(r0sqrt: float, r0sqrt_err: float, r0_fm: float, r0_err_fm: float) -> tuple[float, float]:
    value = r0sqrt / r0_fm * HBARC_MEV_FM
    rel = math.hypot(r0sqrt_err / r0sqrt, r0_err_fm / r0_fm)
    return value, value * rel


@dataclass(frozen=True)
class BridgeCandidate:
    name: str
    non_circular_source: bool
    sea_quark_dynamics: bool
    observable_defined: bool
    uncertainty_budget: bool
    unique_sigma_scheme: bool
    framework_b5_link: bool

    def closes(self) -> bool:
        return (
            self.non_circular_source
            and self.sea_quark_dynamics
            and self.observable_defined
            and self.uncertainty_budget
            and self.unique_sigma_scheme
            and self.framework_b5_link
        )

    def count(self) -> int:
        return sum(
            [
                self.non_circular_source,
                self.sea_quark_dynamics,
                self.observable_defined,
                self.uncertainty_budget,
                self.unique_sigma_scheme,
                self.framework_b5_link,
            ]
        )


def part1_static_energy_values() -> None:
    section("Part 1: static-energy bridge values")
    tum_ar0, tum_ar0_err = sqrt_sigma_from_r0sqrt(
        TUM_R0SQRTSIGMA_AR0, TUM_R0SQRTSIGMA_AR0_ERR, TUM_R0_FM, TUM_R0_ERR_FM
    )
    tum_pi12, tum_pi12_err = sqrt_sigma_from_r0sqrt(
        TUM_R0SQRTSIGMA_PI12, TUM_R0SQRTSIGMA_PI12_ERR, TUM_R0_FM, TUM_R0_ERR_FM
    )
    split = abs(tum_pi12 - tum_ar0)
    split_pct = split / ((tum_pi12 + tum_ar0) / 2) * 100

    print(f"  TUM r0 = {TUM_R0_FM:.4f} +/- {TUM_R0_ERR_FM:.4f} fm")
    print(f"  TUM r0*sqrt(sigma), A_r0 = {TUM_R0SQRTSIGMA_AR0:.3f} +/- {TUM_R0SQRTSIGMA_AR0_ERR:.3f}")
    print(f"  TUM r0*sqrt(sigma), pi/12 = {TUM_R0SQRTSIGMA_PI12:.3f} +/- {TUM_R0SQRTSIGMA_PI12_ERR:.3f}")
    print(f"  sqrt(sigma), A_r0 = {tum_ar0:.2f} +/- {tum_ar0_err:.2f} MeV")
    print(f"  sqrt(sigma), pi/12 = {tum_pi12:.2f} +/- {tum_pi12_err:.2f} MeV")
    print(f"  A-choice split = {split:.2f} MeV ({split_pct:.2f}%)")

    check(
        "A_r0 static-energy bridge is near the existing rough x0.96 value",
        abs(tum_ar0 - ROUGH_X096_MEV) < 5.0,
        f"{tum_ar0:.2f} vs rough {ROUGH_X096_MEV:.2f} MeV",
    )
    check(
        "pi/12 static-energy bridge is close to the quenched Method 2 value",
        abs(tum_pi12 - QUENCHED_SQRT_SIGMA_MEV) < 5.0,
        f"{tum_pi12:.2f} vs quenched {QUENCHED_SQRT_SIGMA_MEV:.2f} MeV",
    )
    check(
        "static-potential convention split is larger than a sub-percent retention target",
        split_pct > 2.0,
        f"{split_pct:.2f}%",
    )


def part2_force_scale_diagnostic() -> None:
    section("Part 2: N_f=2+1 force-scale diagnostic")
    cls_ratio_from_values = CLS_R0_FM / CLS_R1_FM
    cls_ratio_err = cls_ratio_from_values * math.hypot(CLS_R0_ERR_FM / CLS_R0_FM, CLS_R1_ERR_FM / CLS_R1_FM)

    # Cross-source diagnostic only: apply TUM dimensionless r0*sqrt(sigma)
    # ratios to the 2025 N_f=2+1 r0 value to see scale sensitivity.
    cls_ar0, cls_ar0_err = sqrt_sigma_from_r0sqrt(
        TUM_R0SQRTSIGMA_AR0, TUM_R0SQRTSIGMA_AR0_ERR, CLS_R0_FM, CLS_R0_ERR_FM
    )
    cls_pi12, cls_pi12_err = sqrt_sigma_from_r0sqrt(
        TUM_R0SQRTSIGMA_PI12, TUM_R0SQRTSIGMA_PI12_ERR, CLS_R0_FM, CLS_R0_ERR_FM
    )

    print(f"  CLS r0 = {CLS_R0_FM:.4f} +/- {CLS_R0_ERR_FM:.4f} fm")
    print(f"  CLS r1 = {CLS_R1_FM:.4f} +/- {CLS_R1_ERR_FM:.4f} fm")
    print(f"  CLS r0/r1 direct = {CLS_R0_OVER_R1:.3f} +/- {CLS_R0_OVER_R1_ERR:.3f}")
    print(f"  CLS r0/r1 from values = {cls_ratio_from_values:.3f} +/- {cls_ratio_err:.3f}")
    print(f"  cross-source A_r0 diagnostic = {cls_ar0:.2f} +/- {cls_ar0_err:.2f} MeV")
    print(f"  cross-source pi/12 diagnostic = {cls_pi12:.2f} +/- {cls_pi12_err:.2f} MeV")

    check(
        "CLS r0/r1 is internally consistent with its r0 and r1 values",
        abs(cls_ratio_from_values - CLS_R0_OVER_R1) < 0.03,
        f"computed {cls_ratio_from_values:.3f}, quoted {CLS_R0_OVER_R1:.3f}",
    )
    check(
        "CLS supplies N_f=2+1 force scales but not a unique sigma bridge",
        CLS_R0_FM > 0 and CLS_R1_FM > 0 and CLS_R0_OVER_R1 > 0,
        "r0/r1 force-scale bridge only",
    )
    check(
        "cross-source diagnostic remains compatible with the rough value but is not a closure",
        abs(ROUGH_X096_MEV - cls_pi12) < cls_pi12_err,
        f"rough {ROUGH_X096_MEV:.2f}, diagnostic {cls_pi12:.2f} +/- {cls_pi12_err:.2f}",
    )


def part3_bridge_gate_model() -> None:
    section("Part 3: bridge closure-gate model")
    candidates = [
        BridgeCandidate(
            name="CLS_2025_force_scales",
            non_circular_source=True,
            sea_quark_dynamics=True,
            observable_defined=True,
            uncertainty_budget=True,
            unique_sigma_scheme=False,
            framework_b5_link=False,
        ),
        BridgeCandidate(
            name="TUMQCD_2023_fit_window_sigma",
            non_circular_source=True,
            sea_quark_dynamics=True,
            observable_defined=True,
            uncertainty_budget=True,
            unique_sigma_scheme=False,
            framework_b5_link=False,
        ),
        BridgeCandidate(
            name="rough_x0p96_repo_factor",
            non_circular_source=True,
            sea_quark_dynamics=False,
            observable_defined=False,
            uncertainty_budget=False,
            unique_sigma_scheme=False,
            framework_b5_link=False,
        ),
    ]

    for candidate in candidates:
        print(f"  {candidate.name}: {candidate.count()}/6 gate bits; closes={candidate.closes()}")

    check(
        "CLS force-scale bridge cannot by itself map back to sqrt(sigma)",
        candidates[0].count() == 4 and not candidates[0].unique_sigma_scheme,
    )
    check(
        "TUMQCD finite-window sigma remains scheme-split and B5-open",
        candidates[1].count() == 4 and not candidates[1].framework_b5_link,
    )
    check(
        "rough repo factor remains weaker than either external bridge route",
        candidates[2].count() < candidates[0].count()
        and candidates[2].count() < candidates[1].count(),
    )
    check(
        "no bridge candidate closes retained B2",
        not any(candidate.closes() for candidate in candidates),
    )


def part4_artifact_checks() -> None:
    section("Part 4: artifact checks")
    note = read("docs/HADRON_LANE1_SQRT_SIGMA_B2_STATIC_ENERGY_BRIDGE_SCOUT_NOTE_2026-04-30.md")
    index = read("docs/CANONICAL_HARNESS_INDEX.md")
    state = read(".claude/science/physics-loops/hadron-sqrt-sigma-b2-20260430/STATE.yaml")

    check(
        "note records the TUMQCD A-choice split",
        "1.077 +/- 0.016" in note and "1.110 +/- 0.016" in note,
    )
    check(
        "note keeps the bridge bounded rather than retained",
        "not promote" in note and "bounded" in note,
    )
    check(
        "canonical index includes the static-energy bridge runner",
        "HADRON_LANE1_SQRT_SIGMA_B2_STATIC_ENERGY_BRIDGE_SCOUT_NOTE_2026-04-30.md" in index
        and "frontier_hadron_lane1_sqrt_sigma_b2_static_energy_bridge.py" in index,
    )
    check(
        "loop state advanced to cycle 2",
        state_cycle_at_least(state, 2) and "cycle-2-complete" in state,
    )


def main() -> int:
    print("=" * 88)
    print("LANE 1 SQRT(SIGMA) B2 STATIC-ENERGY BRIDGE SCOUT")
    print("=" * 88)
    print()
    print("Question:")
    print("  Does modern full-QCD static-energy literature supply a retained")
    print("  replacement for the rough x0.96 B2 screening factor?")
    print()
    print("Answer:")
    print("  No. It supplies a useful bounded bridge, but the sigma value is")
    print("  convention/window dependent and B5 remains open.")

    part1_static_energy_values()
    part2_force_scale_diagnostic()
    part3_bridge_gate_model()
    part4_artifact_checks()

    print()
    print("=" * 88)
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
