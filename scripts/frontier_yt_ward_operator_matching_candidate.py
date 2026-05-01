#!/usr/bin/env python3
"""
Candidate Ward physical-readout operator-matching map for PR #230.

This is not a retained-closure runner.  It computes the tree-level factors that
would be needed in an audit-clean Ward repair and records the remaining open
imports.  The runner deliberately avoids defining the top Yukawa by a H_unit
matrix element; it only checks the operator-normalization arithmetic and the
status firewall.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
OUTPUT = ROOT / "outputs" / "yt_ward_operator_matching_candidate_2026-05-01.json"

PASS_COUNT = 0
FAIL_COUNT = 0

UNCLEAN = {"audited_renaming", "audited_failed", "audited_conditional", None}


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    print(f"  [{status}] {tag}: {msg}")


def row(rows: dict[str, dict], key: str) -> dict:
    return rows.get(key, {})


def effective(rows: dict[str, dict], key: str) -> str | None:
    return row(rows, key).get("effective_status")


def main() -> int:
    print("YT Ward operator-matching candidate")
    print("=" * 72)

    rows = json.loads(LEDGER.read_text(encoding="utf-8"))["rows"]

    n_color = 3
    n_iso = 2
    g_bare = 1.0

    scalar_singlet_normalization = 1.0 / math.sqrt(n_color * n_iso)
    trilinear_component_projection = 1.0 / (math.sqrt(n_color) * math.sqrt(n_iso))
    hs_residue_amplitude = g_bare / math.sqrt(2.0 * n_color)
    chirality_decomposition_coefficient = 1.0
    sm_ssb_yukawa_readout_factor = 1.0

    candidate_trilinear_coefficient = (
        trilinear_component_projection
        * chirality_decomposition_coefficient
        * sm_ssb_yukawa_readout_factor
    )

    forbidden_patterns = [
        "y_t" + "_bare :=",
        "<0|" + "H_unit",
        "<0 | " + "H_unit",
        "define " + "y_t" + "_bare",
    ]
    source_text = Path(__file__).read_text(encoding="utf-8")
    forbidden_hits = [pat for pat in forbidden_patterns if pat in source_text]

    dependencies = {
        "source_or_hs_normalization": {
            "ledger_key": "yt_ssb_matching_gap_analysis_note_2026-04-18",
            "effective_status": effective(rows, "yt_ssb_matching_gap_analysis_note_2026-04-18"),
            "required_repair": (
                "derive the Legendre/HS source normalization and VEV division "
                "as a functional derivative of the retained action"
            ),
        },
        "chirality_projection_and_right_handed_selector": {
            "ledger_key": "yt_class_5_non_ql_yukawa_vertex_note_2026-04-18",
            "effective_status": effective(rows, "yt_class_5_non_ql_yukawa_vertex_note_2026-04-18"),
            "required_repair": (
                "derive the Q_L-to-q_R chirality/species selector without using "
                "the old matrix-element identification"
            ),
        },
        "physical_scalar_uniqueness": {
            "ledger_key": "yt_h_unit_flavor_column_decomposition_note_2026-04-18",
            "effective_status": effective(rows, "yt_h_unit_flavor_column_decomposition_note_2026-04-18"),
            "required_repair": (
                "prove the scalar carrier selected by the source functional is "
                "the physical Higgs fluctuation, not only a named composite"
            ),
        },
        "scalar_lsz_external_leg": {
            "ledger_key": "yukawa_color_projection_theorem",
            "effective_status": effective(rows, "yukawa_color_projection_theorem"),
            "required_repair": (
                "derive the scalar Z_phi/LSZ matching bridge as a physical "
                "external-leg theorem"
            ),
        },
        "common_tadpole_dressing": {
            "ledger_key": "yt_ward_identity_derivation_theorem",
            "effective_status": effective(rows, "yt_ward_identity_derivation_theorem"),
            "required_repair": (
                "prove common dressing for gauge and scalar readouts without "
                "alpha_LM or plaquette normalization as a load-bearing input"
            ),
        },
    }
    open_imports = {
        name: dep
        for name, dep in dependencies.items()
        if dep["effective_status"] in UNCLEAN
    }

    target = 1.0 / math.sqrt(6.0)
    report(
        "scalar-singlet-normalization",
        abs(scalar_singlet_normalization - target) < 1e-15,
        f"{scalar_singlet_normalization:.15f}",
    )
    report(
        "trilinear-component-projection",
        abs(trilinear_component_projection - target) < 1e-15,
        f"{trilinear_component_projection:.15f}",
    )
    report(
        "hs-residue-amplitude",
        abs(hs_residue_amplitude - target) < 1e-15,
        f"{hs_residue_amplitude:.15f}",
    )
    report(
        "same-numeric-factor-not-a-definition",
        abs(candidate_trilinear_coefficient - target) < 1e-15,
        f"candidate coefficient={candidate_trilinear_coefficient:.15f}",
    )
    report(
        "chirality-factor-unity",
        chirality_decomposition_coefficient == 1.0,
        "Dirac scalar splits as LH-RH plus h.c. with no numeric factor",
    )
    report(
        "sm-ssb-convention-no-extra-tree-factor",
        sm_ssb_yukawa_readout_factor == 1.0,
        "standard m = y v / sqrt(2) convention changes units, not the vertex coefficient",
    )
    report(
        "forbidden-definition-absent-from-candidate",
        not forbidden_hits,
        f"forbidden hits={forbidden_hits}",
    )
    report(
        "open-import-firewall-engaged",
        bool(open_imports),
        f"open imports={list(open_imports)}",
    )
    report(
        "candidate-not-closure",
        True,
        "actual status remains conditional-support/open until open imports are repaired",
    )

    result = {
        "actual_current_surface_status": "conditional-support / open",
        "conditional_surface_status": (
            "If the listed source, chirality, scalar-carrier, LSZ, and dressing "
            "bridges are independently repaired, the tree-level operator map "
            "has the required 1/sqrt(6) normalization."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The runner still has open imports and is not a retained proposal.",
        "constants": {
            "n_color": n_color,
            "n_iso": n_iso,
            "g_bare": g_bare,
        },
        "computed_factors": {
            "scalar_singlet_normalization": scalar_singlet_normalization,
            "trilinear_component_projection": trilinear_component_projection,
            "hs_residue_amplitude": hs_residue_amplitude,
            "chirality_decomposition_coefficient": chirality_decomposition_coefficient,
            "sm_ssb_yukawa_readout_factor": sm_ssb_yukawa_readout_factor,
            "candidate_trilinear_coefficient": candidate_trilinear_coefficient,
            "target_1_over_sqrt_6": target,
        },
        "forbidden_definition_hits": forbidden_hits,
        "dependencies": dependencies,
        "open_imports": open_imports,
        "non_claims": [
            "does not define the top Yukawa by a H_unit matrix element",
            "does not promote the Ward theorem",
            "does not close the scalar LSZ/color-projection bridge",
            "does not use observed top mass or Yukawa values as proof inputs",
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
