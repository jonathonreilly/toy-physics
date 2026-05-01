#!/usr/bin/env python3
"""
PR #230 same-source scalar two-point production-harness certificate.

Validate the production-facing stochastic estimator for the same-source scalar
two-point object needed by the Feynman-Hellmann route:

    C_ss(q) = Tr[S V_q S V_-q]
    Gamma_ss(q) = 1 / C_ss(q)

This is a measurement primitive for kappa_s, not a physical Higgs
normalization.  Reduced smoke output remains bounded support only.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "outputs" / "yt_direct_lattice_correlator_scalar_two_point_lsz_smoke_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_scalar_two_point_harness_certificate_2026-05-01.json"

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
    print("PR #230 same-source scalar two-point production-harness certificate")
    print("=" * 72)

    data = json.loads(INPUT.read_text(encoding="utf-8"))
    metadata = data.get("metadata", {})
    ensembles = data.get("ensembles", [])
    lsz_meta = metadata.get("scalar_two_point_lsz", {})
    analyses = [
        ensemble.get("scalar_two_point_lsz_analysis", {})
        for ensemble in ensembles
        if isinstance(ensemble, dict)
    ]
    enabled_analyses = [
        analysis for analysis in analyses if analysis.get("source_coordinate") != "disabled"
    ]
    mode_counts = [len(analysis.get("mode_rows", {})) for analysis in enabled_analyses]
    finite_rows = []
    for analysis in enabled_analyses:
        for row in analysis.get("mode_rows", {}).values():
            c_real = float(row.get("C_ss_real", float("nan")))
            gamma_real = float(row.get("Gamma_ss_real", float("nan")))
            if math.isfinite(c_real) and math.isfinite(gamma_real):
                finite_rows.append(row)
    residue_proxies = [
        float(analysis.get("finite_difference_residue_proxy", {}).get("finite_residue_proxy", float("nan")))
        for analysis in enabled_analyses
    ]
    finite_residue_proxies = [value for value in residue_proxies if math.isfinite(value)]

    report("smoke-certificate-present", INPUT.exists(), str(INPUT.relative_to(ROOT)))
    report("reduced-scope-not-production", metadata.get("phase") == "reduced_scope", f"phase={metadata.get('phase')}")
    report("scalar-two-point-enabled", lsz_meta.get("enabled") is True, str(lsz_meta))
    report(
        "same-source-object-declared",
        "Tr[S V_q S V_-q]" in str(lsz_meta.get("measurement_object", "")),
        str(lsz_meta.get("measurement_object")),
    )
    report(
        "physical-higgs-normalization-not-derived",
        lsz_meta.get("physical_higgs_normalization") == "not_derived",
        str(lsz_meta.get("physical_higgs_normalization")),
    )
    report("two-or-more-modes-measured", bool(mode_counts) and min(mode_counts) >= 2, f"mode_counts={mode_counts}")
    report("finite-stochastic-c-ss-and-gamma", len(finite_rows) >= 2, f"finite_rows={len(finite_rows)}")
    report(
        "finite-difference-residue-proxy-emitted",
        bool(finite_residue_proxies),
        f"finite_residue_proxies={finite_residue_proxies}",
    )
    report(
        "not-used-as-physical-yukawa-readout",
        lsz_meta.get("used_as_physical_yukawa_readout") is False,
        str(lsz_meta.get("used_as_physical_yukawa_readout")),
    )

    result = {
        "actual_current_surface_status": "bounded-support / scalar two-point production-harness extension",
        "verdict": (
            "The direct-correlator production harness now has a stochastic "
            "same-source scalar two-point estimator for C_ss(q)=Tr[S V_q S "
            "V_-q].  This turns the kappa_s LSZ measurement object into a "
            "production-facing observable that can be run on saved gauge "
            "ensembles.  It is not retained closure because the smoke run is "
            "reduced-scope, the estimator has no controlled pole/continuum "
            "limit here, and the canonical Higgs normalization remains "
            "not derived."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The harness emits finite C_ss/Gamma_ss estimates only; kappa_s still requires a controlled pole and canonical LSZ normalization.",
        "input_certificate": str(INPUT.relative_to(ROOT)),
        "phase": metadata.get("phase"),
        "scalar_two_point_metadata": lsz_meta,
        "analysis_summaries": [
            {
                "volume": f"{ensemble.get('spatial_L')}^3x{ensemble.get('time_L')}",
                "selected_mass_parameter": ensemble.get("selected_mass_parameter"),
                "analysis": ensemble.get("scalar_two_point_lsz_analysis", {}),
            }
            for ensemble in ensembles
            if isinstance(ensemble, dict)
        ],
        "required_next_steps": [
            "run the stochastic C_ss(q) estimator on production gauge ensembles for the same source used in dE_top/ds",
            "measure enough nonzero momentum points to fit the inverse denominator and isolate a pole",
            "derive finite-volume, IR, and gauge-zero-mode limits before using dGamma/dp^2",
            "match the pole residue to the canonical Higgs kinetic normalization rather than setting kappa_s = 1",
        ],
        "strict_non_claims": [
            "not production evidence",
            "not a physical y_t derivation",
            "does not use H_unit matrix-element readout",
            "does not use yt_ward_identity as authority",
            "does not use observed top mass or observed y_t",
            "does not set kappa_s, c2, or Z_match to one",
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
