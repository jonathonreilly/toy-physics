#!/usr/bin/env python3
"""
PR #230 W/Z response g2 authority firewall.

The same-source W/Z bypass needs a non-observed electroweak coupling
certificate before it can turn a top/W response ratio into a physical y_t
readout.  This runner checks that the current PR #230 surface does not silently
import the repo-level EW package value as that certificate, and that g2 remains
a distinct open input unless a strict certificate is supplied.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_wz_g2_authority_firewall_2026-05-05.json"
NOTE_PATH = ROOT / "docs" / "YT_WZ_G2_AUTHORITY_FIREWALL_NOTE_2026-05-05.md"

G2_CERTIFICATE = ROOT / "outputs" / "yt_electroweak_g2_certificate_2026-05-04.json"
WZ_ROW_BUILDER = ROOT / "outputs" / "yt_wz_mass_fit_response_row_builder_2026-05-04.json"
USABLE_INDEX = ROOT / "docs" / "publication" / "ci3_z3" / "USABLE_DERIVED_VALUES_INDEX.md"
EW_NOTE = ROOT / "docs" / "YT_EW_COLOR_PROJECTION_THEOREM.md"
AUDIT_LEDGER = ROOT / "docs" / "audit" / "AUDIT_LEDGER.md"

PASS_COUNT = 0
FAIL_COUNT = 0


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        state = "PASS"
    else:
        FAIL_COUNT += 1
        state = "FAIL"
    print(f"  [{state}] {tag}: {msg}")


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def ratio_witness() -> dict[str, Any]:
    response_ratio = 2.0
    g2_values = [0.60, 0.70]
    yt_values = [g2 / math.sqrt(2.0) * response_ratio for g2 in g2_values]
    return {
        "formula": "y_t = (g2 / sqrt(2)) * (dE_top/ds) / (dM_W/ds)",
        "held_fixed": {
            "response_ratio": response_ratio,
            "same_source_coordinate": True,
            "sector_overlap_identity": "hypothetically fixed",
            "canonical_higgs_identity": "hypothetically fixed",
        },
        "g2_values": g2_values,
        "yt_values": yt_values,
        "yt_spread": max(yt_values) - min(yt_values),
        "conclusion": "The response ratio does not determine y_t unless g2 is certified or otherwise canceled by a new theorem.",
    }


def main() -> int:
    print("PR #230 W/Z response g2 authority firewall")
    print("=" * 72)

    row_builder = load_json(WZ_ROW_BUILDER)
    row_builder_g2 = row_builder.get("g2_validation", {})
    usable_text = read_text(USABLE_INDEX)
    ew_note_text = read_text(EW_NOTE)
    audit_text = read_text(AUDIT_LEDGER)
    explicit_g2_cert = load_json(G2_CERTIFICATE)

    package_g2_present = "g_2(v)" in usable_text and "0.6480" in usable_text
    package_g2_dependency_tainted = any(
        token in usable_text for token in ("plaquette", "R_conn", "alpha")
    ) or any(token in ew_note_text for token in ("plaquette", "R_conn", "observed"))
    audit_warns_against_clean_import = (
        "not safe to claim the retained physical EW couplings are independently derived"
        in audit_text
        or "not safe to claim a retained EW-coupling derivation" in audit_text
    )
    row_builder_records_absent_g2 = (
        row_builder_g2.get("present") is False
        and "electroweak g2 certificate absent" in row_builder_g2.get("failed_checks", [])
    )
    witness = ratio_witness()

    strict_candidate_valid = (
        bool(explicit_g2_cert)
        and explicit_g2_cert.get("phase") in {"production", "exact-support"}
        and finite(explicit_g2_cert.get("g2"))
        and float(explicit_g2_cert.get("g2")) > 0.0
        and explicit_g2_cert.get("used_observed_g2_as_selector") is False
        and explicit_g2_cert.get("proposal_allowed") is False
    )

    report("explicit-g2-certificate-absent", not explicit_g2_cert, rel(G2_CERTIFICATE))
    report(
        "wz-row-builder-records-g2-absent",
        row_builder_records_absent_g2,
        str(row_builder_g2.get("failed_checks", [])),
    )
    report(
        "package-g2-present-but-not-pr230-authority",
        package_g2_present and package_g2_dependency_tainted,
        "usable index/EW note expose package g2, but dependencies include forbidden PR230 proof inputs or conditional EW authority",
    )
    report(
        "audit-warning-blocks-silent-package-import",
        audit_warns_against_clean_import,
        "audit ledger records EW coupling authority caveats",
    )
    report(
        "response-ratio-still-depends-on-g2",
        witness["yt_spread"] > 0.0,
        f"fixed ratio gives yt spread {witness['yt_spread']:.12g}",
    )
    report("strict-g2-candidate-not-accepted", not strict_candidate_valid, f"strict_candidate_valid={strict_candidate_valid}")
    report("does-not-authorize-retained-proposal", True, "firewall only")

    result = {
        "actual_current_surface_status": "exact negative boundary / WZ response g2 authority absent for PR230",
        "proposal_allowed": False,
        "proposal_allowed_reason": "No strict non-observed g2 certificate is present, and the package EW g2 value is not an allowed PR230 proof input under the current firewall.",
        "bare_retained_allowed": False,
        "g2_authority_gate_passed": False,
        "explicit_g2_certificate": {
            "path": rel(G2_CERTIFICATE),
            "present": bool(explicit_g2_cert),
            "strict_candidate_valid": strict_candidate_valid,
        },
        "wz_mass_fit_response_row_builder": {
            "path": rel(WZ_ROW_BUILDER),
            "g2_validation": row_builder_g2,
        },
        "package_g2_surface": {
            "usable_index": rel(USABLE_INDEX),
            "ew_note": rel(EW_NOTE),
            "package_g2_present": package_g2_present,
            "rejected_as_pr230_load_bearing_input": package_g2_dependency_tainted
            or audit_warns_against_clean_import,
            "rejection_reasons": [
                "PR230 firewall forbids alpha_LM/plaquette/u0 as load-bearing proof inputs",
                "repo EW package g2 is not a same-source W/Z response measurement row",
                "audit surface records caveats for treating EW package g2 as an independently derived physical coupling",
            ],
        },
        "ratio_witness": witness,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not import observed g2 or observed W/Z/top/y_t selectors",
            "does not use H_unit or yt_ward_identity",
            "does not use alpha_LM, plaquette, or u0 as proof authority",
            "does not set c2=1, Z_match=1, kappa_s=1, or k_top/k_gauge=1",
        ],
        "exact_next_action": (
            f"Supply {rel(G2_CERTIFICATE)} from an allowed non-observed authority, "
            "or derive a new same-source W/Z response theorem that cancels g2. "
            "Then rerun the W/Z mass-fit response-row builder and top/W response gates."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {rel(OUTPUT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
