#!/usr/bin/env python3
"""
PR #230 joint Feynman-Hellmann / scalar-LSZ harness certificate.

This validates that the production harness can emit both observables required
by the physical-response route in the same run:

  * dE_top/ds from symmetric uniform scalar-source shifts;
  * same-source C_ss(q) and Gamma_ss(q) for the scalar LSZ normalization.

The joint smoke certificate is intentionally reduced-scope.  It proves
measurement plumbing, not retained top-Yukawa closure.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "outputs" / "yt_direct_lattice_correlator_fh_lsz_joint_smoke_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_joint_harness_certificate_2026-05-01.json"

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
    print("PR #230 joint Feynman-Hellmann / scalar-LSZ harness certificate")
    print("=" * 72)

    data = json.loads(INPUT.read_text(encoding="utf-8"))
    metadata = data.get("metadata", {})
    ensembles = data.get("ensembles", [])
    source_meta = metadata.get("scalar_source_response", {})
    lsz_meta = metadata.get("scalar_two_point_lsz", {})
    source_analyses = [
        ensemble.get("scalar_source_response_analysis", {})
        for ensemble in ensembles
        if isinstance(ensemble, dict)
    ]
    lsz_analyses = [
        ensemble.get("scalar_two_point_lsz_analysis", {})
        for ensemble in ensembles
        if isinstance(ensemble, dict)
    ]
    slopes = [
        float(analysis.get("slope_dE_ds_lat", float("nan")))
        for analysis in source_analyses
        if analysis.get("source_coordinate") != "disabled"
    ]
    finite_slopes = [slope for slope in slopes if math.isfinite(slope)]
    mode_counts = [
        len(analysis.get("mode_rows", {}))
        for analysis in lsz_analyses
        if analysis.get("source_coordinate") != "disabled"
    ]
    residue_proxies = [
        float(analysis.get("finite_difference_residue_proxy", {}).get("finite_residue_proxy", float("nan")))
        for analysis in lsz_analyses
        if analysis.get("source_coordinate") != "disabled"
    ]
    finite_residue_proxies = [value for value in residue_proxies if math.isfinite(value)]

    report("joint-smoke-certificate-present", INPUT.exists(), str(INPUT.relative_to(ROOT)))
    report("reduced-scope-not-production", metadata.get("phase") == "reduced_scope", f"phase={metadata.get('phase')}")
    report("scalar-source-response-enabled", source_meta.get("enabled") is True, str(source_meta))
    report("scalar-two-point-lsz-enabled", lsz_meta.get("enabled") is True, str(lsz_meta))
    report(
        "same-source-coordinate-declared",
        "m_bare + s" in str(source_meta.get("source_coordinate", ""))
        and "same additive scalar source" in str(lsz_meta.get("measurement_object", "")),
        f"source={source_meta.get('source_coordinate')}, lsz={lsz_meta.get('measurement_object')}",
    )
    report("finite-dE-ds-slope-emitted", bool(finite_slopes), f"slopes={finite_slopes}")
    report("two-or-more-lsz-modes-emitted", bool(mode_counts) and min(mode_counts) >= 2, f"mode_counts={mode_counts}")
    report(
        "finite-lsz-residue-proxy-emitted",
        bool(finite_residue_proxies),
        f"finite_residue_proxies={finite_residue_proxies}",
    )
    report(
        "physical-higgs-normalization-not-derived",
        source_meta.get("physical_higgs_normalization") == "not_derived"
        and lsz_meta.get("physical_higgs_normalization") == "not_derived",
        f"source={source_meta.get('physical_higgs_normalization')}, lsz={lsz_meta.get('physical_higgs_normalization')}",
    )
    report(
        "not-used-as-physical-yukawa-readout",
        source_meta.get("used_as_physical_yukawa_readout") is False
        and lsz_meta.get("used_as_physical_yukawa_readout") is False,
        f"source={source_meta.get('used_as_physical_yukawa_readout')}, lsz={lsz_meta.get('used_as_physical_yukawa_readout')}",
    )

    result = {
        "actual_current_surface_status": "bounded-support / joint Feynman-Hellmann scalar-LSZ harness",
        "verdict": (
            "The production harness can now emit the paired physical-response "
            "observables needed for the kappa_s route: dE_top/ds from symmetric "
            "source shifts and same-source C_ss(q)/Gamma_ss(q) for scalar LSZ "
            "normalization.  This defines the exact production measurement "
            "bundle.  It is not retained closure because the run is reduced "
            "scope and the physical conversion still requires production data, "
            "controlled scalar-pole isolation, dGamma/dp^2 at the pole, and "
            "canonical Higgs normalization."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Joint observable plumbing is present, but kappa_s and production pole/response evidence remain open.",
        "input_certificate": str(INPUT.relative_to(ROOT)),
        "phase": metadata.get("phase"),
        "scalar_source_response_metadata": source_meta,
        "scalar_two_point_lsz_metadata": lsz_meta,
        "joint_analysis_summaries": [
            {
                "volume": f"{ensemble.get('spatial_L')}^3x{ensemble.get('time_L')}",
                "selected_mass_parameter": ensemble.get("selected_mass_parameter"),
                "scalar_source_response_analysis": ensemble.get("scalar_source_response_analysis", {}),
                "scalar_two_point_lsz_analysis": ensemble.get("scalar_two_point_lsz_analysis", {}),
            }
            for ensemble in ensembles
            if isinstance(ensemble, dict)
        ],
        "exact_next_action": [
            "run the joint harness on production saved gauge ensembles with common random/source control",
            "fit correlated dE_top/ds from symmetric source shifts",
            "fit Gamma_ss(q) across enough momentum points to isolate the scalar pole",
            "compute dGamma_ss/dp^2 at that pole and derive kappa_s by canonical-Higgs LSZ normalization",
            "only then convert dE_top/ds to physical dE_top/dh",
        ],
        "strict_non_claims": [
            "not production evidence",
            "not retained or proposed_retained y_t closure",
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
