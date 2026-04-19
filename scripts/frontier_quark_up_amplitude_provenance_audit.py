#!/usr/bin/env python3
"""
Bounded provenance audit for the current top reduced up-sector quark-amplitude
candidates.

Status:
  bounded provenance classifier on the reduced quark closure surface

Safe claim:
  The current branch still does not derive the remaining up-sector amplitude
  `a_u`.

  But the current shortlist is no longer provenance-blind. On the existing
  atlas/support/tensor note stack, the leading candidates split cleanly into:
    - projector-native,
    - support-native,
    - scalar-comparison-native,
    - and external empirical baselines.

  That is a bounded provenance statement, not a retained derivation.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

from frontier_quark_up_amplitude_candidate_scan import (
    CandidateEvaluation,
    evaluate_candidate,
    exact_support_anchor,
)


PASS_COUNT = 0
FAIL_COUNT = 0

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_ROOT = REPO_ROOT / "docs"

ATLAS_NOTE = DOC_ROOT / "CKM_ATLAS_AXIOM_CLOSURE_NOTE.md"
SUPPORT_NOTE = DOC_ROOT / "TENSOR_SUPPORT_CENTER_EXCESS_LAW_NOTE.md"
TENSOR_NOTE = DOC_ROOT / "S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE.md"
CANDIDATE_NOTE = DOC_ROOT / "QUARK_UP_AMPLITUDE_CANDIDATE_SCAN_NOTE_2026-04-19.md"
NATIVE_NOTE = DOC_ROOT / "QUARK_UP_AMPLITUDE_NATIVE_EXPRESSION_SCAN_NOTE_2026-04-19.md"

DELTA_STD = math.atan(math.sqrt(5.0))
PROJECTOR_MAGNITUDE = math.sqrt(5.0 / 6.0)
ETA_THEOREM = math.sqrt(5.0) / 6.0
DELTA_A1_DEM = 1.0 / 42.0
SUPPORT_FRACTION = 6.0 / 7.0
RHO_SCALAR = 1.0 / math.sqrt(42.0)


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)


def require_text(path: Path, snippets: tuple[str, ...]) -> bool:
    text = path.read_text()
    return all(snippet in text for snippet in snippets)


@dataclass(frozen=True)
class CandidateSpec:
    label: str
    classification: str
    value: float
    rationale: str
    references: tuple[str, ...]


@dataclass(frozen=True)
class CandidateReport:
    spec: CandidateSpec
    evaluation: CandidateEvaluation


def build_candidate_specs() -> list[CandidateSpec]:
    return [
        CandidateSpec(
            label="7/9",
            classification="external empirical",
            value=7.0 / 9.0,
            rationale="best small-rational bounded refit baseline, but not promoted by the exact atlas/support notes",
            references=(
                "docs/QUARK_UP_AMPLITUDE_CANDIDATE_SCAN_NOTE_2026-04-19.md:53",
                "docs/QUARK_UP_AMPLITUDE_CANDIDATE_SCAN_NOTE_2026-04-19.md:149",
                "docs/QUARK_UP_AMPLITUDE_NATIVE_EXPRESSION_SCAN_NOTE_2026-04-19.md:138",
            ),
        ),
        CandidateSpec(
            label="sqrt(3/5)",
            classification="external empirical",
            value=math.sqrt(3.0 / 5.0),
            rationale="best small-radical bounded anchored baseline, but not promoted by the exact atlas/support notes",
            references=(
                "docs/QUARK_UP_AMPLITUDE_CANDIDATE_SCAN_NOTE_2026-04-19.md:75",
                "docs/QUARK_UP_AMPLITUDE_CANDIDATE_SCAN_NOTE_2026-04-19.md:149",
                "docs/QUARK_UP_AMPLITUDE_NATIVE_EXPRESSION_SCAN_NOTE_2026-04-19.md:139",
            ),
        ),
        CandidateSpec(
            label="sqrt(5/6) * (6/7)",
            classification="support-native",
            value=PROJECTOR_MAGNITUDE * SUPPORT_FRACTION,
            rationale="projector magnitude dressed by the exact democratic support fraction",
            references=(
                "docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md:72",
                "docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md:84",
                "docs/TENSOR_SUPPORT_CENTER_EXCESS_LAW_NOTE.md:45",
                "docs/QUARK_UP_AMPLITUDE_NATIVE_EXPRESSION_SCAN_NOTE_2026-04-19.md:109",
            ),
        ),
        CandidateSpec(
            label="sqrt(5/6) * (1 - 1/sqrt(42))",
            classification="scalar-comparison-native",
            value=PROJECTOR_MAGNITUDE * (1.0 - RHO_SCALAR),
            rationale="projector magnitude dressed by the retained scalar-comparison package rho_scalar = 1/sqrt(42)",
            references=(
                "docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md:72",
                "docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md:128",
                "docs/QUARK_UP_AMPLITUDE_CANDIDATE_SCAN_NOTE_2026-04-19.md:103",
                "docs/QUARK_UP_AMPLITUDE_NATIVE_EXPRESSION_SCAN_NOTE_2026-04-19.md:82",
            ),
        ),
        CandidateSpec(
            label="atan(sqrt(5)) - sqrt(5)/6",
            classification="projector-native",
            value=DELTA_STD - ETA_THEOREM,
            rationale="built entirely from exact projector-side theorem quantities delta_std and eta",
            references=(
                "docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md:74",
                "docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md:123",
                "docs/QUARK_UP_AMPLITUDE_NATIVE_EXPRESSION_SCAN_NOTE_2026-04-19.md:61",
            ),
        ),
    ]


def evaluate_shortlist() -> list[CandidateReport]:
    anchor_r_uc, anchor_r_ct, _solved_a_u = exact_support_anchor()
    return [
        CandidateReport(
            spec=spec,
            evaluation=evaluate_candidate(
                spec.label,
                spec.classification,
                spec.value,
                anchor_r_uc,
                anchor_r_ct,
            ),
        )
        for spec in build_candidate_specs()
    ]


def part1_exact_atoms() -> None:
    print("\n" + "=" * 72)
    print("PART 1: Exact Provenance Atoms")
    print("=" * 72)

    print(f"\n  delta_std                = atan(sqrt(5)) = {DELTA_STD:.12f}")
    print(f"  projector magnitude      = sqrt(5/6)     = {PROJECTOR_MAGNITUDE:.12f}")
    print(f"  eta theorem              = sqrt(5)/6     = {ETA_THEOREM:.12f}")
    print(f"  democratic delta_A1      = 1/42          = {DELTA_A1_DEM:.12f}")
    print(f"  noncentral support frac  = 6/7           = {SUPPORT_FRACTION:.12f}")
    print(f"  rho_scalar               = 1/sqrt(42)    = {RHO_SCALAR:.12f}")

    check(
        "Projector magnitude matches the exact projector angle",
        abs(math.sin(DELTA_STD) - PROJECTOR_MAGNITUDE) < 1.0e-12,
        f"sin(delta_std) = {math.sin(DELTA_STD):.12f}",
    )
    check(
        "Democratic support fraction is the exact affine dressing 1 - 6 delta_A1",
        abs(SUPPORT_FRACTION - (1.0 - 6.0 * DELTA_A1_DEM)) < 1.0e-12,
        f"1 - 6 delta_A1 = {1.0 - 6.0 * DELTA_A1_DEM:.12f}",
    )
    check(
        "Atlas/support/tensor notes still carry the exact provenance atoms",
        require_text(
            ATLAS_NOTE,
            (
                "delta_std = arctan(sqrt(5))",
                "delta_A1(q_dem) = 1/42",
                "noncentral support fraction `= 6/7`",
                "rho_scalar = 1/sqrt(42)",
            ),
        )
        and require_text(
            SUPPORT_NOTE,
            ("delta_A1(q) =", "survives the shell-blindness theorem"),
        )
        and require_text(
            TENSOR_NOTE,
            ("K_R(q) =", "delta_A1(r) = 1 / (6 (1 + sqrt(6) r))"),
        ),
        "checked atlas/support/tensor note stack",
    )


def part2_shortlist_table(reports: list[CandidateReport]) -> None:
    print("\n" + "=" * 72)
    print("PART 2: Shortlist Classification")
    print("=" * 72)

    print("\n  candidate                        class                         anchor      refit_max")
    for report in reports:
        print(
            f"  {report.spec.label:30s}  "
            f"{report.spec.classification:28s}  "
            f"{report.evaluation.anchor_aggregate:7.3f}%  "
            f"{report.evaluation.refit_max:8.3f}%"
        )
        print(f"    rationale: {report.spec.rationale}")
        print(f"    refs: {', '.join(report.spec.references)}")


def part3_provenance_checks(reports: list[CandidateReport]) -> None:
    print("\n" + "=" * 72)
    print("PART 3: Provenance Checks")
    print("=" * 72)

    by_label = {report.spec.label: report for report in reports}

    support_report = by_label["sqrt(5/6) * (6/7)"]
    scalar_report = by_label["sqrt(5/6) * (1 - 1/sqrt(42))"]
    projector_report = by_label["atan(sqrt(5)) - sqrt(5)/6"]
    rational_report = by_label["7/9"]
    radical_report = by_label["sqrt(3/5)"]

    check(
        "Support-native candidate is exactly the affine support dressing of the projector magnitude",
        abs(support_report.spec.value - math.sin(DELTA_STD) * (1.0 - 6.0 * DELTA_A1_DEM)) < 1.0e-12,
        f"value = {support_report.spec.value:.12f}",
    )
    check(
        "Scalar-comparison-native candidate is exactly the rho_scalar dressing",
        abs(scalar_report.spec.value - PROJECTOR_MAGNITUDE * (1.0 - RHO_SCALAR)) < 1.0e-12,
        f"value = {scalar_report.spec.value:.12f}",
    )
    check(
        "Projector-native candidate uses only projector theorem atoms",
        abs(projector_report.spec.value - (DELTA_STD - ETA_THEOREM)) < 1.0e-12,
        f"value = {projector_report.spec.value:.12f}",
    )
    check(
        "Support-native candidate keeps the anchored CKM+J package near closure",
        support_report.evaluation.anchor_aggregate < 1.2,
        f"anchor aggregate = {support_report.evaluation.anchor_aggregate:.3f}%",
    )
    check(
        "Scalar-comparison-native candidate is the strongest anchored native law on the shortlist",
        scalar_report.evaluation.anchor_aggregate
        < min(support_report.evaluation.anchor_aggregate, projector_report.evaluation.anchor_aggregate),
        f"anchor aggregate = {scalar_report.evaluation.anchor_aggregate:.3f}%",
    )
    check(
        "Projector-native candidate is the strongest refit native law on the shortlist",
        projector_report.evaluation.refit_objective
        < min(support_report.evaluation.refit_objective, scalar_report.evaluation.refit_objective),
        f"refit objective = {projector_report.evaluation.refit_objective:.6f}",
    )
    check(
        "7/9 remains the strongest refit baseline among the current top five",
        rational_report.evaluation.refit_objective
        < min(
            radical_report.evaluation.refit_objective,
            support_report.evaluation.refit_objective,
            scalar_report.evaluation.refit_objective,
            projector_report.evaluation.refit_objective,
        ),
        f"refit objective = {rational_report.evaluation.refit_objective:.6f}",
    )
    check(
        "sqrt(3/5) remains the strongest anchored baseline among the current top five",
        radical_report.evaluation.anchor_aggregate
        < min(
            rational_report.evaluation.anchor_aggregate,
            support_report.evaluation.anchor_aggregate,
            scalar_report.evaluation.anchor_aggregate,
            projector_report.evaluation.anchor_aggregate,
        ),
        f"anchor aggregate = {radical_report.evaluation.anchor_aggregate:.3f}%",
    )
    check(
        "External baselines are still documented as bounded, not framework-forced",
        require_text(
            CANDIDATE_NOTE,
            (
                "a_u = 7/9",
                "a_u = sqrt(3/5)",
                "no claim that `7/9`, `sqrt(3/5)`, or any dressing law is framework-forced.",
            ),
        )
        and require_text(
            NATIVE_NOTE,
            (
                "`7/9` is still the strongest current refit baseline",
                "`sqrt(3/5)` is still the strongest current anchored baseline",
            ),
        )
        and not require_text(
            ATLAS_NOTE,
            (
                "7/9",
                "sqrt(3/5)",
            ),
        ),
        "candidate/native notes yes; atlas note no",
    )


def part4_summary(reports: list[CandidateReport]) -> None:
    print("\n" + "=" * 72)
    print("PART 4: Bounded Provenance Summary")
    print("=" * 72)

    print("\n  strongest provenance conclusions:")
    for report in reports:
        print(
            f"    - {report.spec.label:<30s} -> {report.spec.classification:<26s} "
            f"(anchor = {report.evaluation.anchor_aggregate:.3f}%, "
            f"refit_max = {report.evaluation.refit_max:.3f}%)"
        )

    print(
        "\n  honest endpoint:\n"
        "    - 7/9 and sqrt(3/5) stay as external empirical baselines;\n"
        "    - sqrt(5/6) * (6/7) is the cleanest support-native dressing;\n"
        "    - sqrt(5/6) * (1 - 1/sqrt(42)) is the strongest scalar-comparison-native anchored law;\n"
        "    - atan(sqrt(5)) - sqrt(5)/6 is the strongest projector-native refit law."
    )


def main() -> int:
    reports = evaluate_shortlist()
    part1_exact_atoms()
    part2_shortlist_table(reports)
    part3_provenance_checks(reports)
    part4_summary(reports)

    print("\n" + "=" * 72)
    print(f"FINAL STATUS: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 72)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
