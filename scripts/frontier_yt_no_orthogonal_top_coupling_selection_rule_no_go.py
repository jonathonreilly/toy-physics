#!/usr/bin/env python3
"""
PR #230 no-orthogonal-top-coupling selection-rule no-go.

The target-time-series Higgs-identity no-go leaves a possible escape: prove
that any scalar orthogonal to the canonical Higgs radial mode cannot couple to
the top.  This runner checks whether the current PR #230 authority surface
contains such a selection rule.  It constructs a charge-table witness where an
orthogonal neutral scalar has the same listed substrate/gauge quantum numbers
as the Higgs radial mode, so every current selection rule that allows h tbar t
also allows chi tbar t.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_no_orthogonal_top_coupling_selection_rule_no_go_2026-05-02.json"

PARENTS = {
    "no_orthogonal_top_coupling_import": "outputs/yt_no_orthogonal_top_coupling_import_audit_2026-05-02.json",
    "target_timeseries_higgs_identity": "outputs/yt_fh_lsz_target_timeseries_higgs_identity_no_go_2026-05-02.json",
    "source_pole_mixing": "outputs/yt_source_pole_canonical_higgs_mixing_obstruction_2026-05-02.json",
    "same_source_sector_overlap": "outputs/yt_same_source_sector_overlap_identity_obstruction_2026-05-02.json",
}

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


def load(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def charge_table_witness() -> dict[str, Any]:
    # The listed charges are intentionally limited to the current-surface
    # labels used by PR #230 shortcut attempts.  A new retained charge could
    # distinguish h from chi, but that would be a new premise.
    h = {
        "field": "h",
        "spin": 0,
        "color": "singlet",
        "electric_charge": 0,
        "z3_translation_character": "trivial",
        "cl3_scalar_carrier": "neutral_scalar_singlet",
        "cp": "even",
        "coupling_to_top_bilinear": "allowed",
    }
    chi = {
        "field": "chi",
        "spin": 0,
        "color": "singlet",
        "electric_charge": 0,
        "z3_translation_character": "trivial",
        "cl3_scalar_carrier": "neutral_scalar_singlet",
        "cp": "even",
        "coupling_to_top_bilinear": "allowed",
    }
    top_bilinear = {
        "operator": "tbar_L t_R + h.c.",
        "spin": 0,
        "color": "singlet",
        "electric_charge": 0,
        "z3_translation_character": "trivial",
        "cl3_scalar_carrier": "neutral_scalar_singlet",
        "cp": "even",
    }
    charge_keys = [
        "spin",
        "color",
        "electric_charge",
        "z3_translation_character",
        "cl3_scalar_carrier",
        "cp",
    ]
    same_charges = all(h[key] == chi[key] == top_bilinear[key] for key in charge_keys)
    allowed_terms = {
        "h_tbar_t": same_charges,
        "chi_tbar_t": same_charges,
        "mixed_source": same_charges,
    }
    return {
        "charge_keys": charge_keys,
        "h": h,
        "chi": chi,
        "top_bilinear": top_bilinear,
        "allowed_terms": allowed_terms,
        "checks": {
            "h_and_chi_indistinguishable_by_listed_charges": same_charges,
            "h_top_coupling_allowed": allowed_terms["h_tbar_t"],
            "chi_top_coupling_allowed": allowed_terms["chi_tbar_t"],
            "no_current_selection_rule_forces_y_chi_zero": allowed_terms["chi_tbar_t"],
        },
    }


def main() -> int:
    print("PR #230 no-orthogonal-top-coupling selection-rule no-go")
    print("=" * 72)

    parents = {name: load(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    witness = charge_table_witness()
    checks = witness["checks"]

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report(
        "hidden-no-orthogonal-top-coupling-import-absent",
        "no-orthogonal-top-coupling import audit" in status(parents["no_orthogonal_top_coupling_import"])
        and parents["no_orthogonal_top_coupling_import"].get("proposal_allowed") is False,
        status(parents["no_orthogonal_top_coupling_import"]),
    )
    report(
        "target-timeseries-identity-no-go-loaded",
        "target time series not canonical-Higgs identity" in status(parents["target_timeseries_higgs_identity"])
        and parents["target_timeseries_higgs_identity"].get("proposal_allowed") is False,
        status(parents["target_timeseries_higgs_identity"]),
    )
    report(
        "source-pole-mixing-obstruction-loaded",
        "source-pole canonical-Higgs mixing" in status(parents["source_pole_mixing"])
        and parents["source_pole_mixing"].get("proposal_allowed") is False,
        status(parents["source_pole_mixing"]),
    )
    report(
        "sector-overlap-identity-still-blocked",
        "same-source sector-overlap identity obstruction" in status(parents["same_source_sector_overlap"])
        and parents["same_source_sector_overlap"].get("proposal_allowed") is False,
        status(parents["same_source_sector_overlap"]),
    )
    report("h-and-chi-same-current-charges", checks["h_and_chi_indistinguishable_by_listed_charges"], str(checks))
    report("h-top-coupling-allowed", checks["h_top_coupling_allowed"], str(checks))
    report("chi-top-coupling-also-allowed", checks["chi_top_coupling_allowed"], str(checks))
    report(
        "no-selection-rule-for-y-chi-zero",
        checks["no_current_selection_rule_forces_y_chi_zero"],
        "current listed charges cannot allow h tbar t while forbidding chi tbar t",
    )

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / no-orthogonal-top-coupling selection rule not derived"
        ),
        "verdict": (
            "The current PR #230 substrate/gauge labels do not distinguish the "
            "canonical Higgs radial scalar from an orthogonal neutral scalar "
            "with the same listed charges.  Any selection rule based only on "
            "those labels that allows h tbar t also allows chi tbar t.  "
            "Therefore no-orthogonal-top-coupling cannot be imported from the "
            "current surface; it needs a new retained charge/representation "
            "theorem, a source-pole purity theorem, or a direct measurement."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "A retained selection rule forbidding orthogonal top-coupled scalars is absent.",
        "no_orthogonal_top_coupling_selection_rule_gate_passed": False,
        "parents": PARENTS,
        "witness": witness,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not assume y_chi = 0",
            "does not use H_unit, yt_ward_identity, observed top mass, observed y_t, alpha_LM, plaquette, or u0",
            "does not set kappa_s = 1",
        ],
        "exact_next_action": (
            "Try to derive a new retained charge/representation theorem that "
            "distinguishes all orthogonal neutral scalar modes from the Higgs "
            "radial mode, or measure the orthogonal coupling/source-pole purity "
            "directly."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
