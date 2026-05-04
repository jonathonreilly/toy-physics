#!/usr/bin/env python3
"""
PR #230 source-Higgs production readiness gate.

The highest-ranked non-MC closure route needs real same-surface source-Higgs
rows: C_ss, C_sH, and C_HH with a certified canonical-Higgs operator O_H.  The
production harness already has a guarded, default-off row path, but the current
chunk wave was launched without an O_H certificate.  This runner records that
run-control boundary and the exact conditions for a future source-Higgs launch.

It does not launch jobs, edit the production harness, write measurement rows,
or treat existing FH/LSZ chunks as source-Higgs evidence.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_source_higgs_production_readiness_gate_2026-05-04.json"
PRODUCTION_HARNESS = ROOT / "scripts" / "yt_direct_lattice_correlator_production.py"
OPERATOR_CERT = ROOT / "outputs" / "yt_canonical_higgs_operator_certificate_2026-05-03.json"
FUTURE_ROWS = ROOT / "outputs" / "yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json"
FUTURE_PRODUCTION_CERT = (
    ROOT / "outputs" / "yt_source_higgs_cross_correlator_production_certificate_2026-05-03.json"
)
CHUNK_PATTERN = "yt_pr230_fh_lsz_production_L12_T24_chunk*_2026-05-01.json"

PARENTS = {
    "canonical_operator_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "harness_extension": "outputs/yt_source_higgs_cross_correlator_harness_extension_2026-05-03.json",
    "harness_absence_guard": "outputs/yt_source_higgs_harness_absence_guard_2026-05-02.json",
    "pole_residue_extractor": "outputs/yt_source_higgs_pole_residue_extractor_2026-05-03.json",
    "builder": "outputs/yt_source_higgs_cross_correlator_certificate_builder_2026-05-03.json",
    "gram_postprocessor": "outputs/yt_source_higgs_gram_purity_postprocess_2026-05-03.json",
    "contract_witness": "outputs/yt_source_higgs_gram_purity_contract_witness_2026-05-03.json",
    "unratified_smoke": "outputs/yt_source_higgs_unratified_operator_smoke_checkpoint_2026-05-03.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
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


def display(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def chunk_index(path: Path) -> int:
    stem = path.stem
    marker = "chunk"
    idx = stem.find(marker)
    if idx < 0:
        return -1
    digits = ""
    for ch in stem[idx + len(marker) :]:
        if ch.isdigit():
            digits += ch
        else:
            break
    return int(digits) if digits else -1


def source_higgs_rows_present(ensemble: dict[str, Any]) -> bool:
    analysis = ensemble.get("source_higgs_cross_correlator_analysis", {})
    if not isinstance(analysis, dict):
        return False
    rows = analysis.get("mode_rows", {})
    return isinstance(rows, dict) and bool(rows)


def scan_completed_chunks() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted((ROOT / "outputs").glob(CHUNK_PATTERN), key=chunk_index):
        data = load_json(path)
        metadata = data.get("metadata", {}) if isinstance(data.get("metadata", {}), dict) else {}
        source_meta = metadata.get("source_higgs_cross_correlator", {})
        if not isinstance(source_meta, dict):
            source_meta = {}
        source_higgs_metadata_present = bool(source_meta)
        ensembles = data.get("ensembles", [])
        ensemble = ensembles[0] if isinstance(ensembles, list) and ensembles and isinstance(ensembles[0], dict) else {}
        rows.append(
            {
                "chunk_index": chunk_index(path),
                "path": display(path),
                "phase": metadata.get("phase"),
                "source_higgs_metadata_present": source_higgs_metadata_present,
                "source_higgs_enabled": source_meta.get("enabled") is True,
                "source_higgs_status": source_meta.get("implementation_status"),
                "canonical_higgs_operator_realization": source_meta.get("canonical_higgs_operator_realization"),
                "source_higgs_modes": source_meta.get("modes", []),
                "source_higgs_noises": source_meta.get("noise_vectors_per_configuration", 0),
                "source_higgs_rows_present": source_higgs_rows_present(ensemble),
                "used_as_physical_yukawa_readout": source_meta.get("used_as_physical_yukawa_readout"),
            }
        )
    return rows


def future_launch_template() -> list[str]:
    return [
        "python3 scripts/yt_direct_lattice_correlator_production.py",
        "--volumes 12x24",
        "--masses 0.45,0.75,1.05",
        "--therm 1000",
        "--measurements 16",
        "--separation 20",
        "--engine numba",
        "--production-targets",
        "--scalar-source-shifts=-0.01,0.0,0.01",
        "--scalar-two-point-modes '0,0,0;1,0,0;0,1,0;0,0,1'",
        "--scalar-two-point-noises 16",
        "--source-higgs-cross-modes '0,0,0;1,0,0;0,1,0;0,0,1'",
        "--source-higgs-cross-noises 16",
        f"--source-higgs-operator-certificate {display(OPERATOR_CERT)}",
        "--production-output-dir outputs/yt_direct_lattice_correlator_production_source_higgs/L12_T24_chunkXXX",
        "--seed 20260520XX",
        "--output outputs/yt_pr230_source_higgs_L12_T24_chunkXXX_2026-05-04.json",
    ]


def main() -> int:
    print("PR #230 source-Higgs production readiness gate")
    print("=" * 72)

    certs = {name: load_rel(rel) for name, rel in PARENTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    harness_text = PRODUCTION_HARNESS.read_text(encoding="utf-8") if PRODUCTION_HARNESS.exists() else ""
    chunks = scan_completed_chunks()

    canonical_operator_absent = (
        "canonical-Higgs operator certificate absent" in status(certs["canonical_operator_gate"])
        and certs["canonical_operator_gate"].get("candidate_valid") is False
    )
    harness_extension_available = (
        "source-Higgs cross-correlator harness extension" in status(certs["harness_extension"])
        and certs["harness_extension"].get("proposal_allowed") is False
    )
    default_off_guard_present = (
        "source-Higgs harness default-off guard" in status(certs["harness_absence_guard"])
        and certs["harness_absence_guard"].get("proposal_allowed") is False
    )
    extractor_awaits_valid_rows = (
        "awaiting valid production rows" in status(certs["pole_residue_extractor"])
        and certs["pole_residue_extractor"].get("rows_written") is False
    )
    builder_awaits_rows = (
        "source-Higgs cross-correlator rows absent" in status(certs["builder"])
        and certs["builder"].get("input_present") is False
    )
    postprocessor_awaits_certificate = (
        "awaiting production certificate" in status(certs["gram_postprocessor"])
        and certs["gram_postprocessor"].get("source_higgs_gram_purity_gate_passed") is False
    )
    contract_witness_support_only = (
        "source-Higgs Gram-purity contract witness" in status(certs["contract_witness"])
        and certs["contract_witness"].get("proposal_allowed") is False
    )
    smoke_explicitly_unratified = (
        "source-Higgs unratified-operator smoke checkpoint" in status(certs["unratified_smoke"])
        and certs["unratified_smoke"].get("proposal_allowed") is False
    )
    retained_route_open = (
        "closure not yet reached" in status(certs["retained_route"])
        and certs["retained_route"].get("proposal_allowed") is False
    )

    harness_has_cli = all(
        token in harness_text
        for token in (
            "--source-higgs-cross-modes",
            "--source-higgs-cross-noises",
            "--source-higgs-operator-certificate",
            "stochastic_source_higgs_cross_correlator",
            "fit_source_higgs_cross_correlator",
        )
    )
    harness_requires_certificate = (
        "--source-higgs-operator-certificate is required for C_sH/C_HH rows" in harness_text
    )
    completed_chunks_scanned = bool(chunks)
    completed_chunks_guarded = completed_chunks_scanned and all(
        (
            row["source_higgs_metadata_present"] is False
            or (
                row["source_higgs_enabled"] is False
                and row["source_higgs_status"] == "absent_guarded"
                and row["canonical_higgs_operator_realization"] == "absent"
            )
        )
        for row in chunks
    )
    no_completed_chunk_rows = completed_chunks_scanned and not any(row["source_higgs_rows_present"] for row in chunks)
    no_completed_chunk_yukawa_readout = completed_chunks_scanned and all(
        row["source_higgs_metadata_present"] is False
        or row["used_as_physical_yukawa_readout"] is False
        for row in chunks
    )
    operator_cert_present = OPERATOR_CERT.exists()
    future_rows_present = FUTURE_ROWS.exists()
    future_production_cert_present = FUTURE_PRODUCTION_CERT.exists()
    launch_ready = (
        canonical_operator_absent is False
        and operator_cert_present
        and harness_has_cli
        and harness_requires_certificate
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("canonical-operator-certificate-still-absent", canonical_operator_absent, status(certs["canonical_operator_gate"]))
    report("harness-extension-available", harness_extension_available, status(certs["harness_extension"]))
    report("default-off-guard-present", default_off_guard_present, status(certs["harness_absence_guard"]))
    report("pole-extractor-awaits-valid-rows", extractor_awaits_valid_rows, status(certs["pole_residue_extractor"]))
    report("builder-awaits-source-higgs-rows", builder_awaits_rows, status(certs["builder"]))
    report("gram-postprocessor-awaits-certificate", postprocessor_awaits_certificate, status(certs["gram_postprocessor"]))
    report("contract-witness-support-only", contract_witness_support_only, status(certs["contract_witness"]))
    report("unratified-smoke-not-evidence", smoke_explicitly_unratified, status(certs["unratified_smoke"]))
    report("retained-route-still-open", retained_route_open, status(certs["retained_route"]))
    report("production-harness-has-source-higgs-cli", harness_has_cli, display(PRODUCTION_HARNESS))
    report("production-harness-requires-oh-certificate", harness_requires_certificate, display(PRODUCTION_HARNESS))
    report("completed-chunks-scanned", completed_chunks_scanned, f"count={len(chunks)}")
    report("completed-chunks-source-higgs-absent-guarded", completed_chunks_guarded, "no completed chunk was launched with O_H certificate")
    report("completed-chunks-have-no-source-higgs-rows", no_completed_chunk_rows, "C_sH/C_HH rows absent from completed chunks")
    report("completed-chunks-not-yukawa-readout", no_completed_chunk_yukawa_readout, "source-Higgs metadata is non-readout")
    report("operator-certificate-file-absent", not operator_cert_present, display(OPERATOR_CERT))
    report("future-source-higgs-row-file-absent", not future_rows_present, display(FUTURE_ROWS))
    report("future-production-certificate-absent", not future_production_cert_present, display(FUTURE_PRODUCTION_CERT))
    report("launch-ready-is-false-until-oh-certificate", not launch_ready, f"launch_ready={launch_ready}")

    result = {
        "actual_current_surface_status": "open / source-Higgs production launch blocked by missing O_H certificate",
        "verdict": (
            "The source-Higgs production row path is instrumented but not launch-ready. "
            "The current completed FH/LSZ chunks were produced with source-Higgs rows "
            "absent-guarded, no canonical-Higgs operator certificate, and no C_sH/C_HH "
            "rows.  A future source-Higgs production launch can reuse the existing "
            "default-off harness only after a same-surface O_H certificate exists; "
            "until then no source-Higgs row, pole-residue, Gram-purity, retained, or "
            "proposed_retained claim is authorized."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The O_H certificate and production C_sH/C_HH rows are absent; this is launch readiness bookkeeping only.",
        "bare_retained_allowed": False,
        "source_higgs_launch_ready": launch_ready,
        "operator_certificate": display(OPERATOR_CERT),
        "operator_certificate_present": operator_cert_present,
        "future_rows_path": display(FUTURE_ROWS),
        "future_rows_present": future_rows_present,
        "future_production_certificate": display(FUTURE_PRODUCTION_CERT),
        "future_production_certificate_present": future_production_cert_present,
        "completed_chunk_scan": chunks,
        "current_chunk_wave_can_supply_source_higgs_rows": any(row["source_higgs_rows_present"] for row in chunks),
        "future_launch_template_blocked_until_operator_certificate": future_launch_template(),
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not launch source-Higgs production jobs",
            "does not edit the production harness while FH/LSZ chunks are running",
            "does not treat current FH/LSZ chunks as source-Higgs C_sH/C_HH evidence",
            "does not define O_H by fiat or use H_unit/static EW algebra as O_H",
            "does not use observed targets, yt_ward_identity, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Derive or supply a same-surface canonical-Higgs operator certificate; "
            "then run a separate source-Higgs production chunk with the recorded "
            "CLI surface, followed by the pole-residue extractor, source-Higgs "
            "builder, Gram-purity postprocessor, retained-route certificate, and "
            "campaign status certificate."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {display(OUTPUT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
