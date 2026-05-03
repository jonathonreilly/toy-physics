#!/usr/bin/env python3
"""
PR #230 canonical-Higgs operator certificate gate.

This is the explicit acceptance schema for a future same-surface O_H operator
certificate.  It does not create O_H and it does not treat EW algebra, H_unit,
or observed targets as an operator identity.  With no candidate certificate
present, it records the current blocker as open.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "outputs" / "yt_canonical_higgs_operator_certificate_2026-05-03.json"
OUTPUT = ROOT / "outputs" / "yt_canonical_higgs_operator_certificate_gate_2026-05-03.json"

TEXTS = {
    "ew_higgs_gauge_mass": "docs/EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md",
    "sm_one_higgs_yukawa_selection": "docs/SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md",
    "canonical_higgs_realization_gate": "docs/YT_CANONICAL_HIGGS_OPERATOR_REALIZATION_GATE_NOTE_2026-05-02.md",
    "hunit_candidate_gate": "docs/YT_HUNIT_CANONICAL_HIGGS_OPERATOR_CANDIDATE_GATE_NOTE_2026-05-02.md",
    "source_higgs_harness_extension": "docs/YT_SOURCE_HIGGS_CROSS_CORRELATOR_HARNESS_EXTENSION_NOTE_2026-05-03.md",
}

CERTS = {
    "canonical_scalar_import": "outputs/yt_canonical_scalar_normalization_import_audit_2026-05-01.json",
    "hunit_candidate_gate": "outputs/yt_hunit_canonical_higgs_operator_candidate_gate_2026-05-02.json",
    "source_higgs_harness_extension": "outputs/yt_source_higgs_cross_correlator_harness_extension_2026-05-03.json",
    "source_higgs_gram_purity": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
    "source_higgs_builder": "outputs/yt_source_higgs_cross_correlator_certificate_builder_2026-05-03.json",
}

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


def load_rel(rel: str) -> dict[str, Any]:
    return load_json(ROOT / rel)


def read_rel(rel: str) -> str:
    path = ROOT / rel
    return path.read_text(encoding="utf-8") if path.exists() else ""


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def path_reference_ok(value: Any) -> bool:
    if not nonempty_string(value):
        return False
    text = str(value)
    if text.startswith("docs/") or text.startswith("outputs/") or text.startswith("scripts/"):
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


def known_surface_audit(texts: dict[str, str], certs: dict[str, dict[str, Any]]) -> dict[str, Any]:
    return {
        "ew_higgs_gauge_mass": {
            "classification": "assumes canonical H after supplied",
            "usable_as_operator_certificate": False,
            "evidence": "|D_mu H|^2" in texts["ew_higgs_gauge_mass"]
            and "Assume a neutral Higgs vacuum" in texts["ew_higgs_gauge_mass"],
        },
        "sm_one_higgs_yukawa_selection": {
            "classification": "gauge monomial selection; leaves Yukawa matrices free",
            "usable_as_operator_certificate": False,
            "evidence": "does not select the numerical entries" in texts["sm_one_higgs_yukawa_selection"],
        },
        "hunit_candidate_gate": {
            "classification": "explicitly rejected unless purity/normalization certificates are supplied",
            "usable_as_operator_certificate": False,
            "status": status(certs["hunit_candidate_gate"]),
        },
        "canonical_scalar_import": {
            "classification": "no hidden source-to-canonical-Higgs normalization import",
            "usable_as_operator_certificate": False,
            "status": status(certs["canonical_scalar_import"]),
        },
        "source_higgs_harness_extension": {
            "classification": "measurement instrumentation only",
            "usable_as_operator_certificate": False,
            "status": status(certs["source_higgs_harness_extension"]),
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    print("PR #230 canonical-Higgs operator certificate gate")
    print("=" * 72)

    texts = {name: read_rel(rel) for name, rel in TEXTS.items()}
    certs = {name: load_rel(rel) for name, rel in CERTS.items()}
    missing_texts = [name for name, text in texts.items() if not text]
    missing_certs = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    candidate = load_json(args.input)
    candidate_present = bool(candidate)
    checks = validate_candidate(candidate) if candidate_present else {}
    missing_checks = [key for key, ok in checks.items() if not ok]
    candidate_valid = candidate_present and not missing_checks
    surface_audit = known_surface_audit(texts, certs)
    hidden_surface_found = any(row["usable_as_operator_certificate"] for row in surface_audit.values())

    report("text-surfaces-present", not missing_texts, f"missing={missing_texts}")
    report("parent-certificates-present", not missing_certs, f"missing={missing_certs}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("candidate-certificate-state-recorded", True, f"present={candidate_present}")
    if candidate_present:
        report("candidate-schema-complete", candidate_valid, f"missing_or_failed={missing_checks}")
    else:
        report("candidate-certificate-absent", True, str(args.input.relative_to(ROOT)))
    report("no-hidden-existing-operator-certificate", not hidden_surface_found, "known EW/Higgs/YT surfaces are not O_H certificates")
    report("hunit-still-not-certificate", "H_unit not canonical-Higgs" in status(certs["hunit_candidate_gate"]), status(certs["hunit_candidate_gate"]))
    report("harness-extension-is-instrumentation-only", "harness extension" in status(certs["source_higgs_harness_extension"]), status(certs["source_higgs_harness_extension"]))
    report("gram-purity-still-open", "not passed" in status(certs["source_higgs_gram_purity"]), status(certs["source_higgs_gram_purity"]))

    result = {
        "actual_current_surface_status": (
            "bounded-support / canonical-Higgs operator certificate candidate valid"
            if candidate_valid
            else "open / canonical-Higgs operator certificate absent"
        ),
        "verdict": (
            "No canonical-Higgs O_H operator certificate is present. Existing "
            "EW/Higgs/YT surfaces either assume canonical H after it is supplied, "
            "select allowed monomials, reject H_unit as a substitute, or provide "
            "measurement instrumentation. They do not supply the same-surface "
            "operator identity and normalization certificate required by PR #230."
            if not candidate_valid
            else (
                "A canonical-Higgs operator certificate candidate satisfies the "
                "schema. It remains support only until production C_sH/C_HH "
                "rows, pole residues, Gram purity, and retained-route gates pass."
            )
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Operator certificate validation is support only; it does not authorize retained/proposed-retained y_t wording.",
        "candidate_input": str(args.input.relative_to(ROOT)) if args.input.is_relative_to(ROOT) else str(args.input),
        "candidate_present": candidate_present,
        "candidate_valid": candidate_valid,
        "candidate_checks": checks,
        "candidate_missing_or_failed_checks": missing_checks,
        "known_surface_audit": surface_audit,
        "acceptance_schema": [
            "certificate_kind == canonical_higgs_operator",
            "same_surface_cl3z3 and same_source_coordinate are true",
            "operator_id and operator_definition are nonempty",
            "canonical_higgs_operator_identity_passed is true",
            "identity_certificate and normalization_certificate are nonempty references",
            "diagonal_vertex.kind is supported by the production harness",
            "hunit_used_as_operator and static_ew_algebra_used_as_operator are false",
            "firewall flags reject observed targets, yt_ward, alpha_LM/plaquette, and H_unit matrix-element readout",
        ],
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not define O_H by fiat",
            "does not treat H_unit or static EW algebra as O_H",
            "does not use observed targets, yt_ward_identity, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Derive or supply a real same-surface canonical-Higgs operator "
            "certificate satisfying this schema, then run source-Higgs "
            "C_sH/C_HH measurements and pole-residue/Gram-purity gates."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {args.output.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
