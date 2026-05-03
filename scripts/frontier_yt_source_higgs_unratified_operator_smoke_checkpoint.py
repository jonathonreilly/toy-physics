#!/usr/bin/env python3
"""
PR #230 source-Higgs unratified-operator smoke checkpoint.

The source-Higgs Gram-purity route needs same-ensemble C_ss/C_sH/C_HH rows,
but those rows only become physics evidence after a certified canonical-Higgs
operator, pole-residue extraction, FV/IR/model-class control, and retained-route
authorization.  This checkpoint verifies the estimator path runs under an
explicitly unratified operator certificate and that every emitted row remains
barred from y_t evidence.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SMOKE = ROOT / "outputs" / "yt_source_higgs_unratified_operator_smoke_run_2026-05-03.json"
OPERATOR_CERT = ROOT / "outputs" / "yt_source_higgs_unratified_operator_certificate_2026-05-03.json"
OUTPUT = ROOT / "outputs" / "yt_source_higgs_unratified_operator_smoke_checkpoint_2026-05-03.json"

PARENTS = {
    "harness_extension": "outputs/yt_source_higgs_cross_correlator_harness_extension_2026-05-03.json",
    "builder": "outputs/yt_source_higgs_cross_correlator_certificate_builder_2026-05-03.json",
    "postprocessor": "outputs/yt_source_higgs_gram_purity_postprocess_2026-05-03.json",
    "canonical_operator_gate": "outputs/yt_canonical_higgs_operator_realization_gate_2026-05-02.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
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
    return json.loads(path.read_text(encoding="utf-8"))


def load_rel(rel: str) -> dict[str, Any]:
    return load_json(ROOT / rel)


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def mode_rows_complete(analysis: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
    rows = analysis.get("mode_rows", {})
    summary: dict[str, Any] = {
        "mode_count": 0,
        "finite_mode_count": 0,
        "timeseries_labels_complete": False,
        "finite_row_gram_available_count": 0,
        "strict_limit_blocks_finite_gram_as_evidence": False,
        "modes": [],
    }
    if not isinstance(rows, dict) or not rows:
        return False, summary

    required = ("C_ss", "C_sH", "C_HH")
    complete = True
    strict_limits = []
    for key, row in rows.items():
        if not isinstance(row, dict):
            complete = False
            continue
        mode_complete = True
        configuration_count = row.get("configuration_count")
        for label in required:
            mode_complete = mode_complete and finite(row.get(f"{label}_real"))
            mode_complete = mode_complete and finite(row.get(f"{label}_imag"))
            series = row.get(f"{label}_timeseries")
            mode_complete = mode_complete and isinstance(series, list)
            mode_complete = mode_complete and len(series) == configuration_count
            for item in series if isinstance(series, list) else []:
                mode_complete = mode_complete and finite(item.get(f"{label}_real"))
                mode_complete = mode_complete and finite(item.get(f"{label}_imag"))
        finite_row_gram = row.get("finite_row_gram", {})
        if isinstance(finite_row_gram, dict) and finite_row_gram.get("available") is True:
            summary["finite_row_gram_available_count"] += 1
            strict_limits.append(str(finite_row_gram.get("strict_limit", "")))
        complete = complete and mode_complete
        summary["mode_count"] += 1
        summary["finite_mode_count"] += 1 if mode_complete else 0
        summary["modes"].append(
            {
                "mode": key,
                "configuration_count": configuration_count,
                "mode_complete": mode_complete,
                "finite_row_gram_available": finite_row_gram.get("available") is True
                if isinstance(finite_row_gram, dict)
                else False,
            }
        )

    summary["timeseries_labels_complete"] = complete
    summary["strict_limit_blocks_finite_gram_as_evidence"] = all(
        "Finite-mode rows are not pole residues" in text for text in strict_limits
    )
    return complete, summary


def main() -> int:
    print("PR #230 source-Higgs unratified-operator smoke checkpoint")
    print("=" * 72)

    smoke = load_json(SMOKE)
    operator = load_json(OPERATOR_CERT)
    parents = {name: load_rel(rel) for name, rel in PARENTS.items()}
    missing_parents = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]

    metadata = smoke.get("metadata", {})
    source_higgs_meta = metadata.get("source_higgs_cross_correlator", {})
    ensembles = smoke.get("ensembles", [])
    ensemble = ensembles[0] if ensembles else {}
    analysis = ensemble.get("source_higgs_cross_correlator_analysis", {})
    mode_rows_ok, mode_summary = mode_rows_complete(analysis)

    reduced_scope = metadata.get("phase") == "reduced_scope" and "infrastructure evidence only" in str(
        metadata.get("evidence_scope", "")
    )
    seed_control = ensemble.get("rng_seed_control", {})
    rng_seed_control_ok = seed_control.get("seed_control_version") == "numba_gauge_seed_v1"
    source_higgs_enabled = source_higgs_meta.get("enabled") is True
    unratified_operator = (
        source_higgs_meta.get("canonical_higgs_operator_realization") == "certificate_supplied_unratified"
        and source_higgs_meta.get("operator", {}).get("canonical_higgs_operator_identity_passed") is False
        and operator.get("canonical_higgs_operator_identity_passed") is False
    )
    selected_mass_only = (
        source_higgs_meta.get("selected_mass_only") is True
        and ensemble.get("fh_lsz_measurement_policy", {}).get(
            "source_higgs_cross_correlator_selected_mass_only"
        )
        is True
    )
    firewall = source_higgs_meta.get("firewall", {})
    forbidden_imports_false = all(
        firewall.get(key) is False
        for key in (
            "used_observed_targets_as_selectors",
            "used_yt_ward_identity",
            "used_alpha_lm_or_plaquette",
            "used_hunit_matrix_element_readout",
        )
    )
    not_readout = (
        source_higgs_meta.get("used_as_physical_yukawa_readout") is False
        and analysis.get("used_as_physical_yukawa_readout") is False
        and ensemble.get("fh_lsz_measurement_policy", {}).get("used_as_physical_yukawa_readout")
        is False
    )
    finite_rows_not_pole_residues = (
        analysis.get("pole_residue_rows") == []
        and "does not supply pole residues" in str(analysis.get("strict_limit", ""))
        and mode_summary["strict_limit_blocks_finite_gram_as_evidence"]
    )
    builder_still_open = "rows absent" in status(parents["builder"])
    postprocessor_still_open = "awaiting production certificate" in status(parents["postprocessor"])
    canonical_gate_open = "canonical-Higgs operator realization gate not passed" in status(
        parents["canonical_operator_gate"]
    )
    retained_open = "retained closure not yet reached" in status(parents["retained_route"])
    campaign_no_proposal = not parents["campaign_status"].get("proposal_allowed_certificates", [])

    report("smoke-artifact-present", bool(smoke), str(SMOKE.relative_to(ROOT)))
    report("operator-certificate-present", bool(operator), str(OPERATOR_CERT.relative_to(ROOT)))
    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("reduced-scope-only", reduced_scope, metadata.get("evidence_scope", ""))
    report("rng-seed-control-recorded", rng_seed_control_ok, seed_control.get("seed_control_version"))
    report("source-higgs-estimator-enabled", source_higgs_enabled, source_higgs_meta.get("implementation_status", ""))
    report("operator-explicitly-unratified", unratified_operator, source_higgs_meta.get("canonical_higgs_operator_realization", ""))
    report("selected-mass-only-recorded", selected_mass_only, source_higgs_meta.get("selected_mass_parameter"))
    report("forbidden-import-firewall-false", forbidden_imports_false, json.dumps(firewall, sort_keys=True))
    report("not-physical-yukawa-readout", not_readout, "metadata and analysis readout flags false")
    report("finite-csh-chh-rows-emitted", mode_rows_ok, f"modes={mode_summary['mode_count']}")
    report("finite-rows-not-pole-residues", finite_rows_not_pole_residues, "pole_residue_rows empty")
    report("builder-still-rejects-current-surface", builder_still_open, status(parents["builder"]))
    report("postprocessor-still-open", postprocessor_still_open, status(parents["postprocessor"]))
    report("canonical-operator-gate-still-open", canonical_gate_open, status(parents["canonical_operator_gate"]))
    report("retained-route-still-open", retained_open, status(parents["retained_route"]))
    report("campaign-has-no-proposal-authority", campaign_no_proposal, status(parents["campaign_status"]))

    result = {
        "actual_current_surface_status": "bounded-support / source-Higgs unratified-operator smoke checkpoint",
        "verdict": (
            "A tiny reduced-scope run exercised the default-off source-Higgs "
            "cross-correlator estimator and emitted same-ensemble finite-mode "
            "C_ss/C_sH/C_HH rows.  The supplied operator certificate is "
            "explicitly unratified, the canonical-Higgs identity is false, "
            "pole_residue_rows are empty, and all downstream evidence gates "
            "remain open.  This proves instrumentation reach only; it supplies "
            "no source-Higgs Gram purity, canonical-Higgs normalization, or "
            "retained y_t closure."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Smoke rows use an unratified operator and are finite-mode instrumentation rows, not pole-residue evidence.",
        "smoke_artifact": str(SMOKE.relative_to(ROOT)),
        "operator_certificate": str(OPERATOR_CERT.relative_to(ROOT)),
        "mode_summary": mode_summary,
        "source_higgs_metadata": source_higgs_meta,
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not define O_H",
            "does not treat finite-mode C_sH/C_HH rows as pole residues",
            "does not set kappa_s = 1 or cos(theta) = 1",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
            "does not use reduced smoke data as production evidence",
        ],
        "exact_next_action": (
            "Replace the unratified smoke operator with an audit-acceptable "
            "same-surface canonical-Higgs operator certificate, run production "
            "source-Higgs cross-correlator rows, extract isolated-pole residues, "
            "then rerun the certificate builder, Gram-purity postprocessor, and "
            "retained-route gate."
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
