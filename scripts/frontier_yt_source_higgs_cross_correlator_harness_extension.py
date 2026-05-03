#!/usr/bin/env python3
"""
PR #230 source-Higgs cross-correlator harness extension certificate.

This verifies that the production harness now has an optional, default-off
measurement path for same-ensemble C_ss/C_sH/C_HH rows.  It is not a physics
closure certificate: the canonical-Higgs operator identity, pole-residue
extraction, Gram purity, FV/IR control, and retained-route gate remain
load-bearing downstream requirements.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "scripts" / "yt_direct_lattice_correlator_production.py"
OUTPUT = ROOT / "outputs" / "yt_source_higgs_cross_correlator_harness_extension_2026-05-03.json"

PARENTS = {
    "route_selection": "outputs/yt_pr230_source_overlap_route_selection_2026-05-03.json",
    "builder": "outputs/yt_source_higgs_cross_correlator_certificate_builder_2026-05-03.json",
    "postprocessor": "outputs/yt_source_higgs_gram_purity_postprocess_2026-05-03.json",
    "canonical_operator_gate": "outputs/yt_canonical_higgs_operator_realization_gate_2026-05-02.json",
    "gram_purity_gate": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
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


def load_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def main() -> int:
    print("PR #230 source-Higgs cross-correlator harness extension")
    print("=" * 72)

    source = HARNESS.read_text(encoding="utf-8")
    parents = {name: load_json(rel) for name, rel in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]

    has_cli = all(
        token in source
        for token in (
            "--source-higgs-cross-modes",
            "--source-higgs-cross-noises",
            "--source-higgs-operator-certificate",
        )
    )
    has_loader = "def load_source_higgs_operator_certificate" in source
    has_weighted_vertex = "def source_higgs_operator_weights" in source
    has_estimator = "def stochastic_source_higgs_cross_correlator" in source
    has_analysis = "def fit_source_higgs_cross_correlator" in source
    emits_ensemble_analysis = '"source_higgs_cross_correlator_analysis"' in source
    emits_certificate_metadata = '"source_higgs_cross_correlator"' in source and "finite_mode_measurement_enabled_pending_pole_residue_gate" in source
    default_off = "source_higgs_cross_correlator=disabled" in source and "--source-higgs-operator-certificate is required" in source
    not_yukawa_readout = '"used_as_physical_yukawa_readout": False' in source
    strict_limit = "source-Higgs certificate builder, Gram-purity postprocessor" in source

    route_selected = (
        parents["route_selection"].get("actual_current_surface_status")
        == "bounded-support / PR230 source-overlap route selected"
        and parents["route_selection"].get("proposal_allowed") is False
    )
    builder_waiting = "rows absent" in status(parents["builder"])
    postprocessor_waiting = "awaiting production certificate" in status(parents["postprocessor"])
    canonical_gate_open = "canonical-Higgs operator realization gate not passed" in status(
        parents["canonical_operator_gate"]
    )
    gram_gate_open = "source-Higgs Gram purity gate not passed" in status(parents["gram_purity_gate"])

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("route-selection-is-gram-purity", route_selected, status(parents["route_selection"]))
    report("builder-still-waits-for-rows", builder_waiting, status(parents["builder"]))
    report("postprocessor-still-waits", postprocessor_waiting, status(parents["postprocessor"]))
    report("canonical-operator-gate-still-open", canonical_gate_open, status(parents["canonical_operator_gate"]))
    report("gram-purity-gate-still-open", gram_gate_open, status(parents["gram_purity_gate"]))
    report("harness-cli-flags-present", has_cli, "source-Higgs cross-correlator flags")
    report("operator-certificate-loader-present", has_loader, "certificate loader")
    report("diagonal-vertex-realization-present", has_weighted_vertex, "diagonal O_H vertex support")
    report("stochastic-cross-estimator-present", has_estimator, "C_ss/C_sH/C_HH estimator")
    report("finite-row-analysis-present", has_analysis, "finite-mode row aggregation")
    report("ensemble-analysis-emitted", emits_ensemble_analysis, "ensemble analysis key")
    report("certificate-metadata-emitted", emits_certificate_metadata, "certificate metadata block")
    report("default-off-without-certificate", default_off, "no C_sH/C_HH rows without certificate")
    report("not-yukawa-readout", not_yukawa_readout, "used_as_physical_yukawa_readout False")
    report("strict-limit-present", strict_limit, "downstream gates named")

    result = {
        "actual_current_surface_status": "bounded-support / source-Higgs cross-correlator harness extension",
        "verdict": (
            "The production harness now has a default-off same-ensemble "
            "source-Higgs measurement path.  With a supplied operator "
            "certificate it can emit finite-mode C_ss/C_sH/C_HH rows for the "
            "selected FH/LSZ mass.  This is not retained closure: the current "
            "surface still lacks an accepted canonical-Higgs operator "
            "identity, pole residues, Gram purity, FV/IR control, and retained "
            "route authorization."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Harness instrumentation is support only; it does not supply a production O_H/C_sH/C_HH pole-residue certificate.",
        "harness_file": str(HARNESS.relative_to(ROOT)),
        "measurement_objects_enabled_by_certificate": ["C_ss(q)", "C_sH(q)", "C_HH(q)"],
        "current_missing_for_retention": [
            "canonical-Higgs operator identity certificate accepted by audit",
            "production source-Higgs cross-correlator rows",
            "isolated pole residues Res_C_ss/Res_C_sH/Res_C_HH",
            "Gram purity pass at the isolated pole",
            "FV/IR/zero-mode/model-class control",
            "retained-route certificate authorization",
        ],
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not define O_H by fiat",
            "does not treat H_unit or static EW algebra as O_H",
            "does not set kappa_s = 1 or cos(theta) = 1",
            "does not use yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Supply or derive an audit-acceptable canonical-Higgs operator "
            "certificate, run the harness with --source-higgs-cross-modes and "
            "--source-higgs-cross-noises, then build pole-residue rows for the "
            "source-Higgs certificate builder."
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
