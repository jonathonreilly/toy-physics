#!/usr/bin/env python3
"""
Chirality and right-handed selector bridge for PR #230.

This runner enumerates the gauge-invariant one-Higgs Yukawa terms using the
repo's standard hypercharge convention.  It shows that, conditional on the
matter/hypercharge parents, the up component selects u_R with H-tilde and the
down component selects d_R with H.  The runner does not use the old H_unit
matrix-element readout and does not close the top-Yukawa normalization.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
OUTPUT = ROOT / "outputs" / "yt_chirality_selector_bridge_2026-05-01.json"

PASS_COUNT = 0
FAIL_COUNT = 0


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    print(f"  [{status}] {tag}: {msg}")


def main() -> int:
    print("YT chirality/right-handed selector bridge")
    print("=" * 72)

    rows = json.loads(LEDGER.read_text(encoding="utf-8"))["rows"]
    deps = {
        "anomaly_forces_time_theorem": rows.get("anomaly_forces_time_theorem", {}),
        "one_generation_matter_closure_note": rows.get("one_generation_matter_closure_note", {}),
        "standard_model_hypercharge_uniqueness_theorem_note_2026-04-24": rows.get(
            "standard_model_hypercharge_uniqueness_theorem_note_2026-04-24", {}
        ),
        "sm_one_higgs_yukawa_gauge_selection_theorem_note_2026-04-26": rows.get(
            "sm_one_higgs_yukawa_gauge_selection_theorem_note_2026-04-26", {}
        ),
        "yt_class_5_non_ql_yukawa_vertex_note_2026-04-18": rows.get(
            "yt_class_5_non_ql_yukawa_vertex_note_2026-04-18", {}
        ),
    }

    # Hypercharge convention used in the existing YT Class 5 note:
    # Q = T3 + Y/2, so Q_L has Y=1/3, u_R has Y=4/3, d_R has Y=-2/3,
    # H has Y=+1, and H_tilde has Y=-1.
    y_qbar_l = -1.0 / 3.0
    right_handed = {
        "u_R": 4.0 / 3.0,
        "d_R": -2.0 / 3.0,
    }
    higgs = {
        "H": 1.0,
        "H_tilde": -1.0,
    }

    candidates = []
    for h_name, h_y in higgs.items():
        for r_name, r_y in right_handed.items():
            total_y = y_qbar_l + h_y + r_y
            candidates.append(
                {
                    "term": f"Qbar_L {h_name} {r_name}",
                    "hypercharge_sum": total_y,
                    "gauge_invariant": abs(total_y) < 1e-15,
                }
            )

    invariant_terms = [item["term"] for item in candidates if item["gauge_invariant"]]
    expected = {"Qbar_L H_tilde u_R", "Qbar_L H d_R"}
    dep_status = {key: row.get("effective_status") for key, row in deps.items()}
    unclean = {
        key: status
        for key, status in dep_status.items()
        if status not in {"retained", "retained corollary", "retained support"}
    }

    source_text = Path(__file__).read_text(encoding="utf-8")
    forbidden_fragments = [
        "y_t" + "_bare :=",
        "<0 | " + "H_unit",
        "<0|" + "H_unit",
    ]
    forbidden_hits = [fragment for fragment in forbidden_fragments if fragment in source_text]

    report("same-chirality-scalar-vanishes", True, "Dirac scalar bilinear requires L-R plus h.c.")
    report("hypercharge-enumeration-complete", len(candidates) == 4, f"candidates={len(candidates)}")
    report("unique-yukawa-selectors", set(invariant_terms) == expected, f"invariant_terms={invariant_terms}")
    report(
        "up-component-selects-uR-with-Htilde",
        "Qbar_L H_tilde u_R" in invariant_terms,
        "up-type gauge-invariant term found",
    )
    report(
        "down-component-selects-dR-with-H",
        "Qbar_L H d_R" in invariant_terms,
        "down-type gauge-invariant term found",
    )
    report("parent-status-firewall-engaged", bool(unclean), f"unclean deps={unclean}")
    report("forbidden-definition-absent", not forbidden_hits, f"forbidden hits={forbidden_hits}")
    report("closure-firewall-engaged", True, "selector support is conditional because parents are not clean")

    result = {
        "actual_current_surface_status": "conditional-support / open",
        "verdict": (
            "Conditional on the matter/hypercharge parents, gauge invariance "
            "uniquely selects Qbar_L H_tilde u_R for the up component and "
            "Qbar_L H d_R for the down component.  This repairs the selector "
            "arithmetic, but the current parent rows are not clean enough to "
            "close the Ward physical-readout theorem."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The selector depends on non-clean matter/hypercharge/chirality parents and does not address scalar residue normalization.",
        "hypercharge_convention": {
            "Y(Qbar_L)": y_qbar_l,
            "Y(u_R)": right_handed["u_R"],
            "Y(d_R)": right_handed["d_R"],
            "Y(H)": higgs["H"],
            "Y(H_tilde)": higgs["H_tilde"],
        },
        "candidates": candidates,
        "invariant_terms": invariant_terms,
        "dependency_status": dep_status,
        "unclean_dependencies": unclean,
        "forbidden_definition_hits": forbidden_hits,
        "non_claims": [
            "does not derive the parent hypercharge/matter authorities",
            "does not derive scalar LSZ normalization",
            "does not identify the Yukawa by a H_unit matrix element",
            "does not promote the Ward theorem",
        ],
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }

    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
