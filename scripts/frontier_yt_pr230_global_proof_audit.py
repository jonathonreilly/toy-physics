#!/usr/bin/env python3
"""
Global PR #230 y_t proof inventory.

This runner scans all docs/YT*.md notes and the audit ledger for y_t/top-Yukawa
claims, then checks whether any existing artifact already supplies retained
closure that the audit simply missed.  It does not decide physics by text
search alone; it uses the audit ledger for effective status and records the
proof-looking clusters that still fail their audit boundary.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
OUTPUT = ROOT / "outputs" / "yt_pr230_global_proof_audit_2026-05-01.json"

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


def status_line(text: str) -> str:
    m = re.search(r"\*\*Status:\*\*\s*([^\n]+)", text)
    if m:
        return m.group(1).strip()
    m = re.search(r"actual_current_surface_status:\s*\"?([^\"\n]+)", text)
    if m:
        return m.group(1).strip()
    return ""


def main() -> int:
    print("PR #230 global y_t proof audit")
    print("=" * 72)

    docs = sorted((ROOT / "docs").glob("YT*.md"))
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))["rows"]
    yt_rows = {
        key: row
        for key, row in ledger.items()
        if key.startswith("yt_")
        or "top_mass" in key
        or "yukawa_color_projection" in key
        or "uv_gauge_to_yukawa" in key
    }

    effective_counts: dict[str, int] = {}
    for row in yt_rows.values():
        effective = row.get("effective_status", "unknown")
        effective_counts[effective] = effective_counts.get(effective, 0) + 1

    retained_y_t_rows = {
        key: row
        for key, row in yt_rows.items()
        if row.get("effective_status") == "retained" and key.startswith("yt_")
    }

    named = {key: ledger.get(key, {}) for key in [
        "yt_ward_identity_derivation_theorem",
        "yt_zero_import_authority_note",
        "yt_zero_import_chain_note",
        "yt_color_projection_correction_note",
        "yukawa_color_projection_theorem",
        "yt_direct_lattice_correlator_derivation_theorem_note_2026-04-30",
        "yt_planck_double_criticality_selector_note_2026-04-30",
        "yt_top_mass_cutoff_obstruction_note_2026-05-01",
        "yt_boundary_theorem",
        "yt_eft_bridge_theorem",
    ]}

    route_buckets = {
        "ward_zero_import": [
            "yt_ward_identity_derivation_theorem",
            "yt_zero_import_authority_note",
            "yt_zero_import_chain_note",
            "yt_boundary_theorem",
            "yt_eft_bridge_theorem",
        ],
        "color_projection": [
            "yt_color_projection_correction_note",
            "yukawa_color_projection_theorem",
            "yt_ew_color_projection_theorem",
        ],
        "direct_correlator": [
            "yt_direct_lattice_correlator_derivation_theorem_note_2026-04-30",
            "yt_top_mass_cutoff_obstruction_note_2026-05-01",
        ],
        "planck_selector": [
            "yt_planck_double_criticality_selector_note_2026-04-30",
            "yt_beta_lambda_planck_stationarity_no_go_note_2026-05-01",
            "yt_scale_stationarity_substrate_no_go_note_2026-05-01",
            "yt_trace_anomaly_stationarity_no_go_note_2026-05-01",
            "yt_vacuum_stability_stationarity_no_go_note_2026-05-01",
        ],
        "schur_bridge": [
            "yt_bridge_hessian_selector_note",
            "yt_bridge_endpoint_shift_bound_note",
            "yt_bridge_uv_class_uniqueness_note",
            "yt_exact_schur_normal_form_uniqueness_note",
        ],
        "p1_p2_p3_matching": [
            "yt_p1_bz_quadrature_full_staggered_pt_note_2026-04-18",
            "yt_p2_v_matching_theorem_note_2026-04-17",
            "yt_p3_msbar_to_pole_k1_framework_native_derivation_note_2026-04-17",
            "yt_p3_msbar_to_pole_k2_color_factor_retention_note_2026-04-17",
            "yt_p3_msbar_to_pole_k3_color_factor_retention_note_2026-04-17",
        ],
    }

    bucket_status = {}
    for bucket, keys in route_buckets.items():
        rows = {key: ledger.get(key, {}) for key in keys}
        bucket_status[bucket] = {
            key: {
                "effective_status": row.get("effective_status"),
                "audit_status": row.get("audit_status"),
                "current_status": row.get("current_status"),
                "verdict_rationale": (row.get("verdict_rationale") or "")[:400],
            }
            for key, row in rows.items()
        }

    proof_like_docs = []
    for path in docs:
        text = path.read_text(encoding="utf-8", errors="ignore")
        status = status_line(text)
        if any(word in status.lower() for word in ["derived", "retained", "proposed_retained"]):
            proof_like_docs.append(
                {
                    "path": str(path.relative_to(ROOT)),
                    "title": text.splitlines()[0] if text.splitlines() else "",
                    "status": status,
                    "contains_h_unit": "H_unit" in text,
                    "contains_y_t_bare": "y_t_bare" in text,
                    "contains_beta_lambda": "beta_lambda(M_Pl)" in text,
                }
            )

    ward_status = named["yt_ward_identity_derivation_theorem"].get("effective_status")
    zero_import_authority_status = named["yt_zero_import_authority_note"].get("effective_status")
    color_projection_status = named["yt_color_projection_correction_note"].get("effective_status")
    direct_status = named["yt_direct_lattice_correlator_derivation_theorem_note_2026-04-30"].get("effective_status")
    planck_status = named["yt_planck_double_criticality_selector_note_2026-04-30"].get("effective_status")
    cutoff_status = named["yt_top_mass_cutoff_obstruction_note_2026-05-01"].get("effective_status")

    report("yt-doc-inventory-complete", len(docs) >= 90, f"YT docs={len(docs)}")
    report("yt-ledger-inventory-complete", len(yt_rows) >= 90, f"yt-ish ledger rows={len(yt_rows)}")
    report("no-effective-retained-yt-row", not retained_y_t_rows, f"retained yt rows={list(retained_y_t_rows)}")
    report("ward-is-audited-renaming", ward_status == "audited_renaming", f"ward effective={ward_status}")
    report(
        "zero-import-authority-not-retained",
        zero_import_authority_status == "audited_renaming",
        f"zero-import authority effective={zero_import_authority_status}",
    )
    report(
        "color-projection-conditional",
        color_projection_status == "audited_conditional",
        f"color projection effective={color_projection_status}",
    )
    report(
        "direct-correlator-not-closed",
        direct_status == "audited_conditional",
        f"direct correlator effective={direct_status}",
    )
    report(
        "planck-selector-conditional",
        planck_status == "audited_conditional",
        f"planck selector effective={planck_status}",
    )
    report("cutoff-obstruction-bounded", cutoff_status == "bounded", f"cutoff effective={cutoff_status}")

    result = {
        "actual_current_surface_status": "open / no existing audited-retained y_t closure found",
        "verdict": (
            "Review of all docs/YT*.md notes plus the audit ledger found no "
            "existing retained top-Yukawa proof that the auditor missed.  The "
            "proof-looking zero-import/Ward/color-projection stack still routes "
            "through audited_renaming or audited_conditional nodes; the direct "
            "correlator route is cutoff-obstructed at the current scale; and "
            "the Planck selector remains conditional on beta_lambda(M_Pl)=0."
        ),
        "yt_doc_count": len(docs),
        "yt_ledger_row_count": len(yt_rows),
        "effective_counts": effective_counts,
        "named_status": {
            key: {
                "effective_status": row.get("effective_status"),
                "audit_status": row.get("audit_status"),
                "current_status": row.get("current_status"),
                "load_bearing_step": row.get("load_bearing_step"),
                "verdict_rationale": row.get("verdict_rationale"),
            }
            for key, row in named.items()
        },
        "route_buckets": bucket_status,
        "proof_like_docs": proof_like_docs,
        "retained_y_t_rows": retained_y_t_rows,
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
