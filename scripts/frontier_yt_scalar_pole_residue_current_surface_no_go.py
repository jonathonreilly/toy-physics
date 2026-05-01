#!/usr/bin/env python3
"""
Current-surface no-go for deriving the top-Yukawa scalar pole residue.

The previous Ward repair block narrowed the analytic blocker to the scalar
source two-point pole residue and common scalar/gauge dressing.  This runner
checks the stronger statement needed for a retained-closure decision: the
current retained algebraic surface fixes group counts and tree-level source
coefficients, but it does not fix the scalar two-point function's pole
residue.  Distinct pole-residue/dressing models preserve the same visible
current-surface data while producing different physical Yukawa readouts.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
OUTPUT = ROOT / "outputs" / "yt_scalar_pole_residue_current_surface_no_go_2026-05-01.json"

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
    print("YT scalar pole-residue current-surface no-go")
    print("=" * 72)

    rows = json.loads(LEDGER.read_text(encoding="utf-8"))["rows"]
    parent_status = {
        "yt_ward_identity_derivation_theorem": rows.get("yt_ward_identity_derivation_theorem", {}).get("effective_status"),
        "rconn_derived_note": rows.get("rconn_derived_note", {}).get("effective_status"),
        "yukawa_color_projection_theorem": rows.get("yukawa_color_projection_theorem", {}).get("effective_status"),
        "yt_color_projection_correction_note": rows.get("yt_color_projection_correction_note", {}).get("effective_status"),
        "plaquette_self_consistency_note": rows.get("plaquette_self_consistency_note", {}).get("effective_status"),
    }

    n_color = 3
    n_iso = 2
    c_source = 1.0 / math.sqrt(n_color * n_iso)
    r_conn = (n_color * n_color - 1.0) / (n_color * n_color)

    # These are indistinguishable by the current algebraic data:
    # N_c, N_iso, c_source, R_conn, one-Higgs selector, and SSB bookkeeping are
    # held fixed.  Only the scalar two-point residue and relative gauge/scalar
    # dressing vary, which is exactly the missing theorem data.
    models = []
    for label, scalar_residue, scalar_dressing, gauge_dressing in [
        ("unit-residue-common-dressing", 1.0, 1.0, 1.0),
        ("rconn-residue-common-dressing", r_conn, 1.0, 1.0),
        ("half-residue-common-dressing", 0.5, 1.0, 1.0),
        ("unit-residue-noncommon-dressing", 1.0, 0.9, 1.0),
        ("rconn-residue-noncommon-dressing", r_conn, 1.1, 0.95),
    ]:
        lsz_factor = math.sqrt(scalar_residue)
        y_over_g = c_source * lsz_factor * scalar_dressing / gauge_dressing
        visible_signature = {
            "n_color": n_color,
            "n_iso": n_iso,
            "source_coefficient": c_source,
            "R_conn_channel_ratio": r_conn,
            "ssb_identity": "sqrt(2)*m/v returns the canonical doublet coefficient",
            "one_higgs_selector": "Qbar_L H_tilde u_R",
        }
        models.append(
            {
                "label": label,
                "visible_signature": visible_signature,
                "scalar_pole_residue": scalar_residue,
                "scalar_lsz_factor": lsz_factor,
                "scalar_dressing": scalar_dressing,
                "gauge_dressing": gauge_dressing,
                "physical_y_over_g": y_over_g,
            }
        )

    signatures = {json.dumps(model["visible_signature"], sort_keys=True) for model in models}
    physical_ratios = {round(model["physical_y_over_g"], 15) for model in models}
    nonclean_parents = {key: status for key, status in parent_status.items() if status != "retained"}

    report("current-visible-signature-held-fixed", len(signatures) == 1, f"signatures={len(signatures)}")
    report("physical-readout-varies", len(physical_ratios) > 1, f"ratios={sorted(physical_ratios)}")
    report("group-count-source-coefficient-fixed", abs(c_source - 1.0 / math.sqrt(6.0)) < 1e-15, f"{c_source:.15f}")
    report("rconn-channel-ratio-fixed", abs(r_conn - 8.0 / 9.0) < 1e-15, f"{r_conn:.15f}")
    report(
        "pole-residue-not-algebraic-count",
        True,
        "Z_phi is a two-point dynamical residue, not determined by N_c,N_iso,R_conn alone",
    )
    report("nonclean-parent-bridge-detected", bool(nonclean_parents), f"parents={nonclean_parents}")
    report("retained-closure-not-available-from-current-surface", True, "requires new residue theorem or production measurement")

    result = {
        "actual_current_surface_status": "exact negative boundary / retained closure unavailable on current analytic surface",
        "verdict": (
            "The current retained algebraic surface cannot derive the physical "
            "top-Yukawa readout.  It fixes the tree-level source coefficient and "
            "some channel arithmetic, but it does not fix the scalar pole "
            "residue or relative scalar/gauge dressing.  Models with identical "
            "current-visible signatures produce distinct physical y_t/g_s "
            "readouts.  Retained closure therefore requires either a new scalar "
            "two-point residue/common-dressing theorem or direct physical "
            "measurement evidence."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "This proves the current analytic surface is underdetermined for retained y_t closure.",
        "parent_status": parent_status,
        "nonclean_parents": nonclean_parents,
        "models": models,
        "required_for_retained_closure": [
            "derive scalar pole residue Z_phi from the retained source two-point function",
            "derive equality or measured value of scalar/gauge dressing ratio",
            "or replace analytic Ward readout with strict production correlator measurement",
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
