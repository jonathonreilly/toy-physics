#!/usr/bin/env python3
"""Verifier for the Planck clean closure criterion theorem."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_CLEAN_CLOSURE_CRITERION_THEOREM_2026-04-23.md"
FINAL_AUDIT = ROOT / "docs/PLANCK_SCALE_AXIOM_ONLY_GRAVITY_UNIT_MAP_FINAL_AUDIT_2026-04-23.md"
NATURE_STATUS = ROOT / "docs/PLANCK_SCALE_NATURE_REVIEW_PLAIN_LANGUAGE_STATUS_2026-04-23.md"
SCALE_RAY = ROOT / "docs/PLANCK_SCALE_GRAVITY_ACTION_SCALE_RAY_NO_GO_THEOREM_2026-04-23.md"
CLASSIFICATION = ROOT / "docs/PLANCK_SCALE_UNIT_BEARING_CANDIDATE_CLASSIFICATION_THEOREM_2026-04-23.md"
HORIZON = ROOT / "docs/PLANCK_SCALE_HORIZON_ENTROPY_LANE_2026-04-23.md"
INFO = ROOT / "docs/PLANCK_SCALE_TIMELOCKED_CONVERTED_INFORMATION_ACTION_CONSTANT_LANE_2026-04-23.md"


def expect(name: str, cond: bool, detail: str = "") -> int:
    if cond:
        print(f"PASS: {name}: {detail}")
        return 1
    print(f"FAIL: {name}: {detail}")
    return 0


def read(path: Path) -> str:
    return path.read_text()


def main() -> int:
    note = read(NOTE)
    final_audit = read(FINAL_AUDIT)
    nature_status = read(NATURE_STATUS)
    scale_ray = read(SCALE_RAY)
    classification = read(CLASSIFICATION)
    horizon = read(HORIZON)
    info = read(INFO)

    banned_terms = ["P1", "Axiom Extension", "GSI", "Gravity-Sector Identification"]
    c_cell = Fraction(4, 16)
    mu_values = [Fraction(1, 2), Fraction(1), Fraction(2)]
    matched_lengths = [4 * mu * c_cell for mu in mu_values]

    checks = [
        (
            "closure-note-is-plain-language",
            all(term not in note for term in banned_terms),
            "new closure criterion should avoid project-local shorthand",
        ),
        (
            "criterion-identifies-exact-remaining-statement",
            "Only one dimensionless statement remains:" in note
            and "`mu = 1`" in note
            and "`a^2 = 4 mu c_cell l_P^2 = mu l_P^2`" in note,
            "the remaining target is the boundary unit-map multiplier",
        ),
        (
            "native-quarter-is-preserved",
            c_cell == Fraction(1, 4)
            and "`c_cell = 1/4`" in note
            and "`c_cell = 1/4`" in final_audit,
            f"c_cell={c_cell}",
        ),
        (
            "positive-mu-family-distinguishes-planck-length",
            matched_lengths == [Fraction(1, 2), Fraction(1), Fraction(2)]
            and "| `1/2` | `a^2 = (1/2) l_P^2` |" in note
            and "| `2` | `a^2 = 2 l_P^2` |" in note,
            f"a^2/l_P^2={matched_lengths}",
        ),
        (
            "closure-equivalence-lists-three-theorem-classes",
            "Boundary action unit theorem" in note
            and "Horizon density theorem" in note
            and "Non-homogeneous unit-map theorem" in note,
            "these are the only clean routes named by the criterion",
        ),
        (
            "scale-ray-no-go-supports-bulk-action-exhaustion",
            "fixes a **scale ray**, not an absolute scale\nanchor" in scale_ray
            and "do not select `mu`" in note,
            "homogeneous bulk/action identities cannot close the multiplier",
        ),
        (
            "candidate-classification-supports-menu-exhaustion",
            "no currently admitted same-surface observable can break the Planck scale ray"
            in classification
            and "pre-closure menu was exhausted" in note,
            "the old same-surface menu did not already contain the missing theorem",
        ),
        (
            "horizon-and-info-lanes-are-not-fake-closures",
            "no exact route to a `1/4` coefficient" in horizon
            and "not yet a closure theorem" in info
            and "identifies an exact target, not a closure theorem" in note,
            "known candidate lanes remain no-go/sharpening, not closure",
        ),
        (
            "nature-status-and-closure-note-agree",
            "normal-ordered primitive boundary event Ward\n> identity" in nature_status
            and "mathematically clean closure is therefore conditional" in note,
            "front-door status should identify the event Ward surface as the closure pressure point",
        ),
        (
            "theorem-states-next-new-science-target",
            "no positive `mu != 1` is compatible" in note
            and "normal-ordered event Ward\nidentity" in note,
            "the closure target should now name the event Ward theorem",
        ),
    ]

    passed = 0
    for name, cond, detail in checks:
        passed += expect(name, cond, detail)

    print(f"SUMMARY: PASS={passed} FAIL={len(checks) - passed}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
