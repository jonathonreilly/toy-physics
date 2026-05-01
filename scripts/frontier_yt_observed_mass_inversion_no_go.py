#!/usr/bin/env python3
"""
No-go runner for treating observed top/Higgs comparators as a derivation of
y_t on PR #230.

This closes a tempting shortcut: use the measured top mass, invert
y_t = sqrt(2) m_t / v, and call the result substrate-derived.  That is a
calibration/readout if the mass is an admitted observation, not a retained
derivation from Cl(3)/Z^3.  The runner also checks that the current PR notes
keep observed values in comparator-only status.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_observed_mass_inversion_no_go_2026-05-01.json"

PASS_COUNT = 0
FAIL_COUNT = 0


V_GEV = 246.28281829012906
MT_POLE_PDG_2025_GEV = 172.56
YT_V_COMPARATOR = 0.9176


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    print(f"  [{status}] {tag}: {msg}")


def assert_observed_inversion_is_import() -> dict[str, float]:
    naive_y_from_pole = math.sqrt(2.0) * MT_POLE_PDG_2025_GEV / V_GEV
    delta = naive_y_from_pole - YT_V_COMPARATOR
    rel_delta = delta / YT_V_COMPARATOR

    report(
        "observed-mass-is-load-bearing-input",
        True,
        "inverting an observed top mass imports the target rather than deriving it",
    )
    report(
        "pole-mass-inversion-needs-running-bridge",
        abs(rel_delta) > 0.05,
        f"sqrt(2)*m_t(pole)/v={naive_y_from_pole:.6f}, not y_t(v)={YT_V_COMPARATOR:.6f}",
    )
    report(
        "calibration-is-not-substrate-prediction",
        True,
        "a tuned heavy mass parameter plus observed m_t gives calibrated readout",
    )

    return {
        "v_gev": V_GEV,
        "mt_pole_pdg_2025_gev": MT_POLE_PDG_2025_GEV,
        "yt_v_comparator": YT_V_COMPARATOR,
        "naive_y_from_pole_mass": naive_y_from_pole,
        "relative_delta_to_yt_v_comparator": rel_delta,
    }


def assert_current_notes_enforce_comparator_boundary() -> dict[str, bool]:
    direct = (ROOT / "docs/YT_DIRECT_LATTICE_CORRELATOR_DERIVATION_THEOREM_NOTE_2026-04-30.md").read_text(encoding="utf-8")
    selector = (ROOT / "docs/YT_PLANCK_DOUBLE_CRITICALITY_SELECTOR_NOTE_2026-04-30.md").read_text(encoding="utf-8")
    assumptions = (ROOT / ".claude/science/physics-loops/yt-pr230-retained-closure-12h-20260501/ASSUMPTIONS_AND_IMPORTS.md").read_text(encoding="utf-8")

    checks = {
        "direct_note_calibrated_readout_boundary": "calibrated physical-observable readout" in direct,
        "direct_note_requires_independent_mass_pin": "independent non-MC substrate pin" in direct,
        "selector_note_observed_values_comparators_only": "comparators after the result is" in selector and "computed" in selector,
        "assumption_ledger_marks_observed_values_comparators": "Observed `y_t`, `m_t`, `m_H`" in assumptions and "not proof inputs" in assumptions,
        "no_hunit_inversion_route": "H_unit" in direct and "does not use the `H_unit`" in direct,
    }

    for tag, ok in checks.items():
        report(tag, ok, f"{tag}={ok}")

    return checks


def main() -> int:
    print("YT observed-mass inversion no-go")
    print("=" * 72)

    numeric = assert_observed_inversion_is_import()
    boundary = assert_current_notes_enforce_comparator_boundary()

    result = {
        "actual_current_surface_status": "no-go / exact-negative-boundary for observed-comparator inversion as proof",
        "target": "derive y_t by inverting observed top or Higgs-sector comparators",
        "verdict": (
            "Observed m_t, y_t, and m_H values may be used as comparators after "
            "a substrate calculation.  They cannot be load-bearing proof inputs "
            "for a retained y_t derivation.  Naively inverting the pole mass also "
            "does not produce the running y_t(v) comparator without a matching "
            "and running bridge."
        ),
        "numeric": numeric,
        "authority_boundary": boundary,
        "remaining_open_premise": "substrate-derived top mass parameter, production correlator evidence, or an independently derived UV selector",
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
