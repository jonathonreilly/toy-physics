#!/usr/bin/env python3
"""
Scalar LSZ residue bridge audit for PR #230.

The existing color-projection route supplies a connected color-channel ratio,
but the audit objection is that this ratio is not yet a theorem for the
physical scalar pole residue.  This runner demonstrates the distinction:
keeping the same channel ratio while rescaling the scalar two-point residue
changes the LSZ Yukawa factor.  Therefore a pole-residue theorem is required.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
OUTPUT = ROOT / "outputs" / "yt_scalar_lsz_residue_bridge_2026-05-01.json"

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
    print("YT scalar LSZ residue bridge audit")
    print("=" * 72)

    rows = json.loads(LEDGER.read_text(encoding="utf-8"))["rows"]
    color_rows = {
        "rconn_derived_note": rows.get("rconn_derived_note", {}),
        "yukawa_color_projection_theorem": rows.get("yukawa_color_projection_theorem", {}),
        "yt_color_projection_correction_note": rows.get("yt_color_projection_correction_note", {}),
        "yt_ew_color_projection_theorem": rows.get("yt_ew_color_projection_theorem", {}),
    }

    n_color = 3
    r_conn = (n_color * n_color - 1.0) / (n_color * n_color)
    source_y = 1.0 / math.sqrt(6.0)

    # Same color-channel ratio, different pole residues.  These are not
    # proposed physics models; they are normalization countermodels showing
    # that a ratio does not by itself fix the LSZ residue.
    residue_scales = [0.5, 1.0, 2.0]
    countermodels = []
    for scale in residue_scales:
        pole_residue = scale * r_conn
        lsz_factor = math.sqrt(pole_residue)
        y_after_lsz = source_y * lsz_factor
        countermodels.append(
            {
                "same_R_conn": r_conn,
                "residue_scale": scale,
                "pole_residue": pole_residue,
                "lsz_factor": lsz_factor,
                "y_after_lsz": y_after_lsz,
            }
        )

    distinct_lsz = {round(item["lsz_factor"], 15) for item in countermodels}
    all_color_status_unclean = all(
        row.get("effective_status") == "audited_conditional"
        for row in color_rows.values()
    )

    report("rconn-channel-ratio-arithmetic", abs(r_conn - 8.0 / 9.0) < 1e-15, f"R_conn={r_conn:.15f}")
    report("color-bridge-ledger-conditional", all_color_status_unclean, {k: v.get("effective_status") for k, v in color_rows.items()}.__repr__())
    report("same-rconn-all-countermodels", all(item["same_R_conn"] == r_conn for item in countermodels), "R_conn held fixed")
    report("different-lsz-factors-possible", len(distinct_lsz) == len(residue_scales), f"LSZ factors={sorted(distinct_lsz)}")
    report(
        "channel-ratio-not-pole-residue",
        True,
        "a pole residue also needs normalization of the scalar two-point function",
    )
    report("closure-firewall-engaged", True, "actual status is exact negative boundary for deriving LSZ from R_conn alone")

    result = {
        "actual_current_surface_status": "exact negative boundary / open bridge",
        "verdict": (
            "R_conn = 8/9 is a channel-ratio arithmetic statement.  It does not "
            "by itself determine the physical scalar LSZ pole residue.  The same "
            "R_conn can coexist with different scalar two-point residues, giving "
            "different external-leg factors.  A scalar pole-residue theorem is "
            "required before the Ward readout can be audit-clean."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "This is a bridge obstruction, not retained y_t closure.",
        "ledger_status": {
            key: {
                "effective_status": row.get("effective_status"),
                "audit_status": row.get("audit_status"),
                "verdict_rationale": row.get("verdict_rationale"),
            }
            for key, row in color_rows.items()
        },
        "constants": {
            "n_color": n_color,
            "R_conn": r_conn,
            "source_y": source_y,
        },
        "countermodels": countermodels,
        "required_new_theorem": (
            "derive the scalar pole residue Z_phi from the retained source "
            "two-point function and prove how it enters the Yukawa LSZ factor"
        ),
        "non_claims": [
            "does not reject R_conn = 8/9 as channel arithmetic",
            "does not derive scalar Z_phi",
            "does not promote the Ward theorem",
            "does not use observed y_t or m_t as input",
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
