#!/usr/bin/env python3
"""
PR #230 complete same-source spectrum identity no-go.

This runner tests the strongest source-only loophole left after the pole-data
and mixing gates: even if the complete same-source scalar spectrum C_ss(p) and
the same-source top response dE_top/ds were known, the physical canonical-Higgs
Yukawa is not fixed unless an orthogonal top coupling is forbidden or measured.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_complete_source_spectrum_identity_no_go_2026-05-02.json"

PARENTS = {
    "same_source_pole_data_sufficiency": "outputs/yt_same_source_pole_data_sufficiency_gate_2026-05-02.json",
    "fh_lsz_higgs_pole_identity": "outputs/yt_fh_lsz_higgs_pole_identity_gate_2026-05-02.json",
    "source_pole_canonical_higgs_mixing": "outputs/yt_source_pole_canonical_higgs_mixing_obstruction_2026-05-02.json",
    "source_pole_purity_cross_correlator": "outputs/yt_source_pole_purity_cross_correlator_gate_2026-05-02.json",
    "source_higgs_gram_purity": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
    "source_higgs_harness_absence": "outputs/yt_source_higgs_harness_absence_guard_2026-05-02.json",
    "source_higgs_harness_extension": "outputs/yt_source_higgs_cross_correlator_harness_extension_2026-05-03.json",
    "wz_response_harness_absence": "outputs/yt_wz_response_harness_absence_guard_2026-05-02.json",
    "wz_response_repo_harness_import": "outputs/yt_wz_response_repo_harness_import_audit_2026-05-03.json",
    "no_orthogonal_top_coupling_selection": "outputs/yt_no_orthogonal_top_coupling_selection_rule_no_go_2026-05-02.json",
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


def source_spectrum(q2: float, cos_theta: float, sin_theta: float) -> float:
    m_h_sq = 1.0
    m_chi_sq = 2.89
    return (cos_theta * cos_theta) / (q2 + m_h_sq) + (sin_theta * sin_theta) / (q2 + m_chi_sq)


def witness_family() -> dict[str, Any]:
    cos_theta = 0.8
    sin_theta = math.sqrt(1.0 - cos_theta * cos_theta)
    fixed_source_response = 0.8
    q2_grid = [0.0, 0.1, 0.25, 0.5, 1.0, 2.0, 4.0]
    spectrum = [source_spectrum(q2, cos_theta, sin_theta) for q2 in q2_grid]

    rows: list[dict[str, Any]] = []
    for y_h in [0.2, 0.5, 0.8, 0.95]:
        y_chi = (fixed_source_response - cos_theta * y_h) / sin_theta
        response = cos_theta * y_h + sin_theta * y_chi
        rows.append(
            {
                "canonical_higgs_y_t": y_h,
                "orthogonal_scalar_top_coupling": y_chi,
                "same_source_top_response": response,
                "source_spectrum_samples": spectrum,
                "max_abs_spectrum_delta_from_first": 0.0,
            }
        )

    responses = [float(row["same_source_top_response"]) for row in rows]
    y_values = [float(row["canonical_higgs_y_t"]) for row in rows]
    chi_values = [float(row["orthogonal_scalar_top_coupling"]) for row in rows]
    return {
        "basis": ["h_canonical", "chi_orthogonal"],
        "source_operator": {
            "O_s": "cos(theta) h + sin(theta) chi",
            "cos_theta": cos_theta,
            "sin_theta": sin_theta,
        },
        "source_spectrum": {
            "q2_grid": q2_grid,
            "pole_masses_sq": {"h_canonical": 1.0, "chi_orthogonal": 2.89},
            "pole_residues": {
                "h_canonical": cos_theta * cos_theta,
                "chi_orthogonal": sin_theta * sin_theta,
            },
            "samples": spectrum,
        },
        "rows": rows,
        "checks": {
            "source_spectrum_identical_across_rows": all(
                max(abs(a - b) for a, b in zip(rows[0]["source_spectrum_samples"], row["source_spectrum_samples"]))
                < 1.0e-15
                for row in rows
            ),
            "same_source_top_response_identical": max(responses) - min(responses) < 1.0e-15,
            "canonical_higgs_y_span_factor": max(y_values) / min(y_values),
            "orthogonal_top_couplings_finite": all(math.isfinite(value) for value in chi_values),
            "orthogonal_top_couplings_positive": all(value > 0.0 for value in chi_values),
        },
    }


def main() -> int:
    print("PR #230 complete same-source spectrum identity no-go")
    print("=" * 72)

    parents = {name: load(rel) for name, rel in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    witness = witness_family()
    checks = witness["checks"]

    pole_data_support_only = (
        "same-source pole-data sufficiency gate not passed" in status(parents["same_source_pole_data_sufficiency"])
        and parents["same_source_pole_data_sufficiency"].get("proposal_allowed") is False
        and parents["same_source_pole_data_sufficiency"].get("gate_passed") is False
    )
    higgs_identity_blocked = (
        "canonical-Higgs pole identity gate blocking" in status(parents["fh_lsz_higgs_pole_identity"])
        and parents["fh_lsz_higgs_pole_identity"].get("proposal_allowed") is False
        and parents["fh_lsz_higgs_pole_identity"].get("higgs_pole_identity_gate_passed") is False
    )
    mixing_blocked = (
        "source-pole canonical-Higgs mixing obstruction" in status(parents["source_pole_canonical_higgs_mixing"])
        and parents["source_pole_canonical_higgs_mixing"].get("proposal_allowed") is False
    )
    purity_data_absent = (
        "source-pole purity cross-correlator gate not passed" in status(parents["source_pole_purity_cross_correlator"])
        and "source-Higgs Gram purity gate not passed" in status(parents["source_higgs_gram_purity"])
        and parents["source_higgs_gram_purity"].get("source_higgs_gram_purity_gate_passed") is False
    )
    source_higgs_support_only = (
        "source-Higgs harness default-off guard" in status(parents["source_higgs_harness_absence"])
        and parents["source_higgs_harness_absence"].get("proposal_allowed") is False
        and "source-Higgs cross-correlator harness extension"
        in status(parents["source_higgs_harness_extension"])
        and parents["source_higgs_harness_extension"].get("proposal_allowed") is False
    )
    wz_support_only = (
        "WZ response harness absence guard" in status(parents["wz_response_harness_absence"])
        and parents["wz_response_harness_absence"].get("proposal_allowed") is False
        and "repo-wide WZ response harness import audit"
        in status(parents["wz_response_repo_harness_import"])
        and parents["wz_response_repo_harness_import"].get("repo_wz_response_harness_found") is False
    )
    no_selection_rule = (
        "no-orthogonal-top-coupling selection rule not derived"
        in status(parents["no_orthogonal_top_coupling_selection"])
        and parents["no_orthogonal_top_coupling_selection"].get(
            "no_orthogonal_top_coupling_selection_rule_gate_passed"
        )
        is False
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("pole-data-support-only", pole_data_support_only, status(parents["same_source_pole_data_sufficiency"]))
    report("higgs-identity-gate-blocked", higgs_identity_blocked, status(parents["fh_lsz_higgs_pole_identity"]))
    report("mixing-obstruction-present", mixing_blocked, status(parents["source_pole_canonical_higgs_mixing"]))
    report("purity-data-still-absent", purity_data_absent, "C_sH/C_HH purity rows absent")
    report(
        "source-higgs-instrumentation-support-only",
        source_higgs_support_only,
        "default-off source-Higgs instrumentation is not O_H/C_sH/C_HH evidence",
    )
    report(
        "wz-harness-support-only",
        wz_support_only,
        "no same-source W/Z response harness or rows",
    )
    report("no-orthogonal-top-coupling-not-derived", no_selection_rule, status(parents["no_orthogonal_top_coupling_selection"]))
    report("complete-source-spectrum-held-fixed", checks["source_spectrum_identical_across_rows"], "all C_ss(q2) samples identical")
    report("same-source-top-response-held-fixed", checks["same_source_top_response_identical"], "dE_top/ds identical")
    report(
        "canonical-higgs-yukawa-varies",
        checks["canonical_higgs_y_span_factor"] > 4.0,
        f"span={checks['canonical_higgs_y_span_factor']:.6g}",
    )
    report("orthogonal-top-couplings-finite", checks["orthogonal_top_couplings_finite"], "all witness couplings finite")
    report("orthogonal-top-couplings-positive", checks["orthogonal_top_couplings_positive"], "all witness couplings positive")
    report("does-not-authorize-retained-proposal", True, "source-only spectrum is not a canonical-Higgs identity")

    result = {
        "actual_current_surface_status": "exact negative boundary / complete source spectrum not canonical-Higgs closure",
        "verdict": (
            "Complete same-source scalar spectrum data C_ss(p), including pole "
            "masses and residues, plus the same-source top response dE_top/ds "
            "still do not determine the canonical-Higgs Yukawa if an orthogonal "
            "neutral scalar top coupling is not forbidden or measured.  The "
            "witness keeps C_ss(p) and dE_top/ds fixed while varying the "
            "canonical Higgs y_t by a factor greater than four through a finite "
            "orthogonal scalar coupling."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "C_ss(p) and dE_top/ds are source-only data; C_sH/C_HH, W/Z response, or a no-orthogonal-coupling theorem remains required.",
        "witness_family": witness,
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not set kappa_s = 1",
            "does not set cos(theta) = 1",
            "does not set the orthogonal scalar top coupling to zero",
            "does not use H_unit matrix-element readout or yt_ward_identity",
            "does not use observed top mass, observed y_t, alpha_LM, plaquette, u0, c2 = 1, or Z_match = 1",
            "does not treat complete source-only C_ss data as O_H/C_sH/C_HH data",
        ],
        "exact_next_action": (
            "Close one non-source-only identity premise: implement C_sH/C_HH "
            "Gram-purity measurements, implement a real same-source W/Z response "
            "with sector-overlap identity certificates, or derive a theorem "
            "forbidding orthogonal neutral top couplings."
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
