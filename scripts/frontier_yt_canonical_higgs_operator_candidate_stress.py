#!/usr/bin/env python3
"""
PR #230 canonical-Higgs operator candidate stress gate.

The source-Higgs smoke introduced an explicitly unratified diagonal operator
certificate so the estimator path could run.  This runner stress-tests that
operator and nearby tempting substitutes against the canonical-Higgs operator
certificate schema.  It is a guardrail: every current candidate must fail until
an actual same-surface O_H identity and normalization certificate is supplied.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_canonical_higgs_operator_candidate_stress_2026-05-03.json"

CANONICAL_GATE = ROOT / "outputs" / "yt_canonical_higgs_operator_certificate_gate_2026-05-03.json"
UNRATIFIED_OPERATOR = ROOT / "outputs" / "yt_source_higgs_unratified_operator_certificate_2026-05-03.json"

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


def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def path_reference_ok(value: Any) -> bool:
    if not nonempty_string(value):
        return False
    text = str(value)
    if text.startswith(("docs/", "outputs/", "scripts/")):
        return (ROOT / text).exists()
    return False


def validate_candidate(candidate: dict[str, Any]) -> dict[str, bool]:
    firewall = candidate.get("firewall", {}) if isinstance(candidate.get("firewall", {}), dict) else {}
    vertex = candidate.get("diagonal_vertex", {}) if isinstance(candidate.get("diagonal_vertex", {}), dict) else {}
    return {
        "certificate_kind": candidate.get("certificate_kind") == "canonical_higgs_operator",
        "same_surface_cl3z3": candidate.get("same_surface_cl3z3") is True,
        "same_source_coordinate": candidate.get("same_source_coordinate") is True,
        "source_coordinate_named": nonempty_string(candidate.get("source_coordinate")),
        "operator_id_named": nonempty_string(candidate.get("operator_id")),
        "operator_definition_named": nonempty_string(candidate.get("operator_definition")),
        "canonical_identity_passed": candidate.get("canonical_higgs_operator_identity_passed") is True,
        "identity_certificate_reference": path_reference_ok(candidate.get("identity_certificate")),
        "normalization_certificate_reference": path_reference_ok(candidate.get("normalization_certificate")),
        "diagonal_vertex_kind_supported": vertex.get("kind")
        in {
            "site_color_diagonal_values",
            "constant_site_color_diagonal",
            "staggered_parity_site_color_diagonal",
        },
        "not_hunit_by_fiat": candidate.get("hunit_used_as_operator") is False,
        "not_static_ew_algebra": candidate.get("static_ew_algebra_used_as_operator") is False,
        "no_observed_target_selectors": firewall.get("used_observed_targets_as_selectors") is False,
        "no_prior_ward_authority": firewall.get("used_yt_ward_identity") is False,
        "no_alpha_lm_or_plaquette_authority": firewall.get("used_alpha_lm_or_plaquette") is False,
        "no_hunit_matrix_element_readout": firewall.get("used_hunit_matrix_element_readout") is False,
        "no_claim_authorization": candidate.get("proposal_allowed") is not True,
    }


def padded_unratified_candidate(base: dict[str, Any]) -> dict[str, Any]:
    candidate = dict(base)
    candidate.update(
        {
            "certificate_kind": "canonical_higgs_operator",
            "same_surface_cl3z3": True,
            "same_source_coordinate": True,
            "source_coordinate": "same uniform additive lattice scalar source s entering m_bare + s",
            "hunit_used_as_operator": False,
            "static_ew_algebra_used_as_operator": False,
            "proposal_allowed": False,
        }
    )
    return candidate


def candidate_rows(unratified: dict[str, Any]) -> list[dict[str, Any]]:
    padded = padded_unratified_candidate(unratified)
    static_ew = dict(padded)
    static_ew.update(
        {
            "operator_id": "static_ew_algebra_candidate_rejected",
            "operator_definition": "dM_W/dh tree algebra after canonical H is assumed",
            "canonical_higgs_operator_identity_passed": True,
            "identity_certificate": "docs/EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md",
            "normalization_certificate": "docs/EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md",
            "static_ew_algebra_used_as_operator": True,
        }
    )
    hunit = dict(static_ew)
    hunit.update(
        {
            "operator_id": "hunit_candidate_rejected",
            "operator_definition": "H_unit by fiat",
            "hunit_used_as_operator": True,
            "static_ew_algebra_used_as_operator": False,
        }
    )
    observed = dict(static_ew)
    observed.update(
        {
            "operator_id": "observed_target_selector_candidate_rejected",
            "operator_definition": "operator chosen by observed target agreement",
            "static_ew_algebra_used_as_operator": False,
            "firewall": {
                "used_observed_targets_as_selectors": True,
                "used_yt_ward_identity": False,
                "used_alpha_lm_or_plaquette": False,
                "used_hunit_matrix_element_readout": False,
            },
        }
    )
    return [
        {
            "name": "raw_unratified_smoke_operator",
            "candidate": unratified,
            "expected_failed_checks": [
                "certificate_kind",
                "same_surface_cl3z3",
                "same_source_coordinate",
                "source_coordinate_named",
                "canonical_identity_passed",
            ],
        },
        {
            "name": "schema_padded_unratified_smoke_operator",
            "candidate": padded,
            "expected_failed_checks": [
                "canonical_identity_passed",
                "identity_certificate_reference",
                "normalization_certificate_reference",
            ],
        },
        {
            "name": "static_ew_algebra_substitute",
            "candidate": static_ew,
            "expected_failed_checks": ["not_static_ew_algebra"],
        },
        {
            "name": "hunit_by_fiat_substitute",
            "candidate": hunit,
            "expected_failed_checks": ["not_hunit_by_fiat"],
        },
        {
            "name": "observed_target_selector_substitute",
            "candidate": observed,
            "expected_failed_checks": ["no_observed_target_selectors"],
        },
    ]


def main() -> int:
    print("PR #230 canonical-Higgs operator candidate stress gate")
    print("=" * 72)

    canonical_gate = load_json(CANONICAL_GATE)
    unratified = load_json(UNRATIFIED_OPERATOR)
    rows = []
    all_rejected = True
    expected_rejections_hit = True
    no_claim_auth = True

    report("canonical-gate-present", bool(canonical_gate), str(CANONICAL_GATE.relative_to(ROOT)))
    report("unratified-operator-present", bool(unratified), str(UNRATIFIED_OPERATOR.relative_to(ROOT)))
    report(
        "canonical-gate-open",
        canonical_gate.get("candidate_valid") is False
        and "certificate absent" in str(canonical_gate.get("actual_current_surface_status", "")),
        canonical_gate.get("actual_current_surface_status", ""),
    )

    for row in candidate_rows(unratified):
        checks = validate_candidate(row["candidate"])
        failed = [key for key, ok in checks.items() if not ok]
        valid = not failed
        expected_hit = all(key in failed for key in row["expected_failed_checks"])
        candidate_no_claim = row["candidate"].get("proposal_allowed") is not True
        all_rejected = all_rejected and not valid
        expected_rejections_hit = expected_rejections_hit and expected_hit
        no_claim_auth = no_claim_auth and candidate_no_claim
        rows.append(
            {
                "name": row["name"],
                "candidate_valid": valid,
                "failed_checks": failed,
                "expected_failed_checks": row["expected_failed_checks"],
                "expected_rejections_hit": expected_hit,
                "proposal_allowed": row["candidate"].get("proposal_allowed"),
            }
        )

    report("all-current-candidates-rejected", all_rejected, f"candidate_count={len(rows)}")
    report("expected-rejection-reasons-hit", expected_rejections_hit, "all expected failed checks present")
    report("no-candidate-authorizes-proposal", no_claim_auth, "proposal_allowed is not true")

    result = {
        "actual_current_surface_status": "exact negative boundary / canonical-Higgs operator candidate stress rejects current substitutes",
        "verdict": (
            "The current unratified source-Higgs smoke operator and nearby "
            "tempting substitutes all fail the canonical-Higgs operator "
            "certificate schema.  Padding the smoke operator with surface labels "
            "still fails because the canonical identity and normalization "
            "certificates are absent.  Static EW algebra, H_unit-by-fiat, and "
            "observed-target selectors are rejected by explicit firewall checks."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Every current candidate fails the O_H certificate schema; this stress gate is rejection evidence only.",
        "candidate_rows": rows,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not define O_H",
            "does not treat unratified smoke rows as source-Higgs evidence",
            "does not use H_unit, static EW algebra, observed targets, yt_ward_identity, alpha_LM, plaquette, or u0",
            "does not set kappa_s = 1 or cos(theta) = 1",
        ],
        "exact_next_action": (
            "Supply a genuinely derived same-surface canonical-Higgs operator "
            "identity and normalization certificate; then rerun the certificate "
            "gate before any production C_sH/C_HH rows are evidence."
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
