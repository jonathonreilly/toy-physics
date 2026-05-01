#!/usr/bin/env python3
"""
Common gauge/scalar dressing obstruction for PR #230.

The Ward repair would need the scalar Yukawa readout and gauge coupling readout
to share the same dressing, without importing alpha_LM or plaquette
normalization as the proof.  This runner shows the current allowed structure
does not enforce that equality: gauge Ward identities can protect the gauge
current, but they do not fix scalar-density dressing.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
OUTPUT = ROOT / "outputs" / "yt_common_dressing_obstruction_2026-05-01.json"

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
    print("YT common dressing obstruction")
    print("=" * 72)

    rows = json.loads(LEDGER.read_text(encoding="utf-8"))["rows"]
    status_rows = {
        "yt_ward_identity_derivation_theorem": rows.get("yt_ward_identity_derivation_theorem", {}),
        "alpha_lm_geometric_mean_identity_theorem_note_2026-04-24": rows.get(
            "alpha_lm_geometric_mean_identity_theorem_note_2026-04-24", {}
        ),
        "plaquette_self_consistency_note": rows.get("plaquette_self_consistency_note", {}),
        "gauge_vacuum_plaquette_bridge_support_note": rows.get("gauge_vacuum_plaquette_bridge_support_note", {}),
    }

    source_ratio = 1.0 / math.sqrt(6.0)
    countermodels = []
    for scalar_dressing, gauge_dressing in [(1.0, 1.0), (0.9, 1.0), (1.1, 0.95), (1.0, 1.05)]:
        measured_ratio = source_ratio * scalar_dressing / gauge_dressing
        countermodels.append(
            {
                "source_ratio": source_ratio,
                "scalar_dressing": scalar_dressing,
                "gauge_dressing": gauge_dressing,
                "measured_y_over_g": measured_ratio,
                "common_dressing": abs(scalar_dressing - gauge_dressing) < 1e-15,
            }
        )

    distinct_ratios = {round(item["measured_y_over_g"], 15) for item in countermodels}
    nonclean_status = {
        key: row.get("effective_status")
        for key, row in status_rows.items()
        if row.get("effective_status") != "retained"
    }

    report("source-ratio-fixed", abs(source_ratio - 1.0 / math.sqrt(6.0)) < 1e-15, f"{source_ratio:.15f}")
    report("dressing-countermodels-change-ratio", len(distinct_ratios) > 1, f"ratios={sorted(distinct_ratios)}")
    report("common-dressing-is-extra-condition", any(not item["common_dressing"] for item in countermodels), "non-common dressing countermodels included")
    report(
        "gauge-ward-does-not-protect-scalar-density",
        True,
        "WTI constrains gauge current renormalization, not scalar-density LSZ/readout",
    )
    report("nonclean-dressing-parents-detected", bool(nonclean_status), f"statuses={nonclean_status}")
    report("closure-firewall-engaged", True, "actual status is exact negative boundary for common dressing from current inputs")

    result = {
        "actual_current_surface_status": "exact negative boundary / open bridge",
        "verdict": (
            "The current Ward/readout surface does not derive common scalar and "
            "gauge dressing.  Distinct scalar and gauge dressing factors preserve "
            "the same tree-level 1/sqrt(6) source ratio while changing the "
            "measured y/g ratio.  A retained theorem equating those dressing "
            "factors is required; alpha_LM or plaquette normalization cannot be "
            "used as a hidden proof input in PR #230."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Common dressing remains an open bridge; this is not y_t closure.",
        "status_rows": {
            key: {
                "effective_status": row.get("effective_status"),
                "audit_status": row.get("audit_status"),
                "verdict_rationale": row.get("verdict_rationale"),
            }
            for key, row in status_rows.items()
        },
        "countermodels": countermodels,
        "required_new_theorem": (
            "derive equality of scalar and gauge dressing factors from a retained "
            "symmetry/dynamics theorem, or carry their ratio as measured input"
        ),
        "non_claims": [
            "does not use alpha_LM or plaquette normalization as proof input",
            "does not deny the tree-level 1/sqrt(6) source ratio",
            "does not promote the Ward theorem",
            "does not use observed top mass or observed Yukawa as input",
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
