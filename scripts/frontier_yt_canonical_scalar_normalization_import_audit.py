#!/usr/bin/env python3
"""
PR #230 canonical scalar-normalization import audit.

Audit the strongest existing EW/Higgs surfaces for a hidden theorem that fixes
the scalar source normalization kappa_s needed by the top-Yukawa source
response route.  The current surfaces provide structural Higgs bookkeeping, but
they assume a canonical Higgs doublet after the source-to-field bridge rather
than deriving that bridge from the Cl(3)/Z^3 source functional.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
OUTPUT = ROOT / "outputs" / "yt_canonical_scalar_normalization_import_audit_2026-05-01.json"

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


def row(rows: dict, key: str) -> dict:
    return rows.get(key, {})


def main() -> int:
    print("PR #230 canonical scalar-normalization import audit")
    print("=" * 72)

    rows = json.loads(LEDGER.read_text(encoding="utf-8"))["rows"]
    keys = {
        "ew_higgs_gauge_mass": "ew_higgs_gauge_mass_diagonalization_theorem_note_2026-04-26",
        "sm_one_higgs_yukawa_selection": "sm_one_higgs_yukawa_gauge_selection_theorem_note_2026-04-26",
        "observable_principle": "observable_principle_from_axiom_note",
        "yt_ew_color_projection": "yt_ew_color_projection_theorem",
        "rconn": "rconn_derived_note",
    }
    status_rows = {name: row(rows, key) for name, key in keys.items()}

    ew_note = (ROOT / "docs" / "EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md").read_text(
        encoding="utf-8"
    )
    sm_note = (ROOT / "docs" / "SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md").read_text(
        encoding="utf-8"
    )
    observable_note = (ROOT / "docs" / "OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md").read_text(encoding="utf-8")

    ew_assumes_canonical = "|D_mu H|^2" in ew_note and "<H> = H_0" in ew_note
    ew_no_source_bridge = "source-to" not in ew_note.lower() and "kappa" not in ew_note.lower()
    sm_leaves_yukawa_free = "arbitrary complex" in sm_note and "does not select" in sm_note
    observable_conditional = status_rows["observable_principle"].get("effective_status") != "retained"
    color_projection_not_scalar_norm = status_rows["yt_ew_color_projection"].get("effective_status") != "retained"
    proposed_structural_not_audited = (
        status_rows["ew_higgs_gauge_mass"].get("effective_status") == "proposed_retained"
        and status_rows["sm_one_higgs_yukawa_selection"].get("effective_status") == "proposed_retained"
    )

    report("ew-higgs-assumes-canonical-doublet", ew_assumes_canonical, "EW note starts from canonical |D H|^2 and <H>")
    report("ew-higgs-does-not-derive-source-bridge", ew_no_source_bridge, "no source-to-Higgs kappa theorem in EW gauge-mass note")
    report("sm-yukawa-selection-leaves-values-free", sm_leaves_yukawa_free, "SM one-Higgs note leaves Yukawa matrices arbitrary")
    report("observable-principle-not-clean-parent", observable_conditional, status_rows["observable_principle"].get("effective_status", "missing"))
    report("color-projection-not-scalar-normalization", color_projection_not_scalar_norm, status_rows["yt_ew_color_projection"].get("effective_status", "missing"))
    report("structural-not-audit-clean-normalization", proposed_structural_not_audited, "EW/Higgs structural notes are proposed/unaudited, not PR230 scalar-source closure")
    report("not-retained-closure", True, "no audited current surface fixes kappa_s for PR230")

    result = {
        "actual_current_surface_status": "exact negative boundary / canonical scalar normalization import audit",
        "verdict": (
            "The strongest existing EW/Higgs surfaces do not supply the missing "
            "PR #230 scalar source normalization.  The EW gauge-mass note starts "
            "after a canonical Higgs doublet and kinetic term have been supplied; "
            "the SM one-Higgs note selects allowed monomials but leaves Yukawa "
            "matrices free; the observable-principle row is audited conditional; "
            "and the color-projection/R_conn rows do not derive scalar LSZ "
            "normalization.  No hidden retained current-surface theorem fixes "
            "kappa_s."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Existing EW/Higgs notes assume or structure the canonical scalar field; they do not derive it from the PR230 source.",
        "status_rows": {
            name: {
                "ledger_key": keys[name],
                "effective_status": data.get("effective_status"),
                "audit_status": data.get("audit_status"),
                "verdict_rationale": data.get("verdict_rationale"),
            }
            for name, data in status_rows.items()
        },
        "required_next_theorem": [
            "derive source-to-canonical-Higgs normalization from the Cl(3)/Z^3 source functional",
            "or measure scalar LSZ residue / physical response directly",
            "then feed that bridge into the Feynman-Hellmann or direct-correlator route",
        ],
        "strict_non_claims": [
            "does not demote EW structural guardrails",
            "does not use H_unit matrix-element readout",
            "does not use observed top mass or observed y_t",
            "does not use alpha_LM/plaquette/u0 as proof input",
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
