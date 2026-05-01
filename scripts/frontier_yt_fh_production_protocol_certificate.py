#!/usr/bin/env python3
"""
PR #230 Feynman-Hellmann production protocol certificate.

Design the production-grade top-energy response observable enabled by the
scalar-source harness extension.  The protocol measures dE_top/ds on common
gauge ensembles and states the separate scalar LSZ/canonical-normalization
measurement required before dE_top/ds can become physical dE_top/dh.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_fh_production_protocol_certificate_2026-05-01.json"

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


def load(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def main() -> int:
    print("PR #230 Feynman-Hellmann production protocol certificate")
    print("=" * 72)

    harness = load("outputs/yt_scalar_source_response_harness_certificate_2026-05-01.json")
    fh_scout = load("outputs/yt_feynman_hellmann_source_response_route_2026-05-01.json")
    mass_response = load("outputs/yt_mass_response_bracket_certificate_2026-05-01.json")
    production_resource = load("outputs/yt_production_resource_projection_2026-05-01.json")

    protocol = {
        "observable": "common-ensemble finite-difference slope dE_top/ds",
        "source_coordinate": "uniform additive lattice scalar source s in m_bare + s",
        "source_shifts_lat": [-0.01, 0.0, 0.01],
        "volumes": ["12^3x24", "16^3x32", "24^3x48"],
        "saved_configurations_per_volume": 1000,
        "measurement_rule": "measure all source shifts on the same saved gauge configurations for correlated slope fits",
        "fit_rule": "fit E_top(s) per volume, then jointly fit dE/ds with finite-volume and source-window systematics",
        "strict_rejection_rule": "reduced or cold-gauge runs remain scouts only",
    }
    kappa_measurement = {
        "needed_to_convert": "dE_top/dh = (dE_top/ds) / kappa_s",
        "allowed_measurement": (
            "measure the scalar source two-point function for the same source, "
            "derive an isolated Higgs-channel pole, and compute the "
            "inverse-propagator derivative / canonical residue"
        ),
        "forbidden_shortcuts": [
            "H_unit matrix-element readout",
            "yt_ward_identity as authority",
            "observed top mass or observed y_t as selector",
            "alpha_LM / plaquette / u0 normalization as load-bearing proof",
            "kappa_s = 1 without scalar LSZ/canonical normalization",
            "Z_match = 1 without a matching theorem",
        ],
    }
    source_shifts = protocol["source_shifts_lat"]
    symmetric_window = (
        len(source_shifts) == 3
        and math.isclose(source_shifts[1], 0.0)
        and math.isclose(abs(source_shifts[0]), abs(source_shifts[2]))
    )
    projected_extra_correlator_factor = len(source_shifts)

    report("harness-support-present", harness.get("fail_count") == 0, harness.get("actual_current_surface_status", ""))
    report("fh-scout-support-present", fh_scout.get("fail_count") == 0, fh_scout.get("actual_current_surface_status", ""))
    report("mass-response-data-backed-scout-present", mass_response.get("fail_count") == 0, mass_response.get("actual_current_surface_status", ""))
    report("production-resource-input-present", production_resource.get("fail_count") == 0, production_resource.get("actual_current_surface_status", ""))
    report("symmetric-source-window", symmetric_window, f"source_shifts={source_shifts}")
    report("common-ensemble-rule-declared", "same saved gauge configurations" in protocol["measurement_rule"], protocol["measurement_rule"])
    report("kappa-measurement-required", "inverse-propagator derivative" in kappa_measurement["allowed_measurement"], kappa_measurement["allowed_measurement"])
    report("forbidden-shortcuts-explicit", len(kappa_measurement["forbidden_shortcuts"]) >= 6, str(kappa_measurement["forbidden_shortcuts"]))
    report("not-retained-closure", True, "protocol has no production data and no kappa_s theorem")

    result = {
        "actual_current_surface_status": "bounded-support / Feynman-Hellmann production protocol",
        "verdict": (
            "The Feynman-Hellmann response route is now production-specifiable: "
            "measure E_top(s) at symmetric uniform scalar-source shifts on the "
            "same gauge ensembles and fit dE_top/ds with correlated errors.  "
            "This bypasses additive rest-mass ambiguity, but it still does not "
            "supply physical dE_top/dh.  A scalar two-point LSZ/canonical "
            "normalization measurement or theorem must derive kappa_s, and any "
            "lattice-to-SM response matching must be derived rather than set to "
            "one."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Protocol lacks production response data and scalar LSZ/canonical normalization kappa_s.",
        "protocol": protocol,
        "projected_extra_correlator_factor": projected_extra_correlator_factor,
        "kappa_s_measurement": kappa_measurement,
        "inputs": {
            "harness": harness.get("actual_current_surface_status"),
            "fh_scout": fh_scout.get("actual_current_surface_status"),
            "mass_response": mass_response.get("actual_current_surface_status"),
            "production_resource": production_resource.get("actual_current_surface_status"),
        },
        "strict_non_claims": [
            "not production data",
            "not a physical y_t derivation",
            "does not use H_unit matrix-element readout",
            "does not use yt_ward_identity as authority",
            "does not set kappa_s or Z_match to one",
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
