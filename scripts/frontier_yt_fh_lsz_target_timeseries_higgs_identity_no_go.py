#!/usr/bin/env python3
"""
PR #230 FH/LSZ target-time-series versus canonical-Higgs identity no-go.

Per-configuration target time series can certify statistics for the source
coordinate.  They still do not identify that source pole with the canonical
Higgs radial mode used by v.  This runner constructs two neutral-scalar
response models with identical same-source time-series limits and different
canonical-Higgs Yukawa couplings.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_target_timeseries_higgs_identity_no_go_2026-05-02.json"

PARENTS = {
    "target_timeseries_harness": "outputs/yt_fh_lsz_target_timeseries_harness_certificate_2026-05-02.json",
    "autocorrelation_ess_gate": "outputs/yt_fh_lsz_autocorrelation_ess_gate_2026-05-02.json",
    "invariant_readout": "outputs/yt_fh_lsz_invariant_readout_theorem_2026-05-01.json",
    "source_pole_mixing": "outputs/yt_source_pole_canonical_higgs_mixing_obstruction_2026-05-02.json",
    "no_orthogonal_top_coupling_import": "outputs/yt_no_orthogonal_top_coupling_import_audit_2026-05-02.json",
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


def source_response(theta: float, y_h: float, y_chi: float) -> float:
    return math.cos(theta) * y_h + math.sin(theta) * y_chi


def witness_family(source_yukawa: float = 1.0, dgamma_dp2: float = 2.5) -> dict[str, Any]:
    theta_a = 0.0
    y_h_a = source_yukawa
    y_chi_a = 0.0

    theta_b = math.pi / 4.0
    y_h_b = 0.80 * source_yukawa
    y_chi_b = (source_yukawa - math.cos(theta_b) * y_h_b) / math.sin(theta_b)

    model_a_source = source_response(theta_a, y_h_a, y_chi_a)
    model_b_source = source_response(theta_b, y_h_b, y_chi_b)
    residue_proxy = 1.0 / abs(dgamma_dp2)
    invariant = source_yukawa * math.sqrt(dgamma_dp2)

    return {
        "shared_same_source_observables": {
            "source_response_limit": source_yukawa,
            "dGamma_ss_dp2_at_pole": dgamma_dp2,
            "same_source_residue_proxy": residue_proxy,
            "same_source_invariant": invariant,
            "target_timeseries_limit": (
                "All per-configuration dE/ds and C_ss/Gamma_ss samples may "
                "converge to these same source-coordinate limits."
            ),
        },
        "model_A_pure_canonical_higgs": {
            "theta": theta_a,
            "source_operator": "O_s = h",
            "canonical_higgs_yukawa": y_h_a,
            "orthogonal_scalar_yukawa": y_chi_a,
            "same_source_response": model_a_source,
        },
        "model_B_mixed_source_pole": {
            "theta": theta_b,
            "source_operator": "O_s = cos(theta) h + sin(theta) chi",
            "canonical_higgs_yukawa": y_h_b,
            "orthogonal_scalar_yukawa": y_chi_b,
            "same_source_response": model_b_source,
        },
        "checks": {
            "same_source_response_equal": abs(model_a_source - model_b_source) < 1.0e-12,
            "dGamma_dp2_equal_by_construction": True,
            "same_source_invariant_equal_by_construction": True,
            "canonical_higgs_yukawa_differs": abs(y_h_a - y_h_b) > 1.0e-12,
            "orthogonal_top_coupling_required_in_mixed_witness": abs(y_chi_b) > 1.0e-12,
        },
    }


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def main() -> int:
    print("PR #230 FH/LSZ target time-series Higgs-identity no-go")
    print("=" * 72)

    parents = {name: load(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    witness = witness_family()
    checks = witness["checks"]

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report(
        "target-timeseries-harness-is-support-only",
        "target time-series harness extension" in status(parents["target_timeseries_harness"])
        and parents["target_timeseries_harness"].get("proposal_allowed") is False,
        status(parents["target_timeseries_harness"]),
    )
    report(
        "autocorrelation-ess-still-not-physical-readout",
        (
            "autocorrelation ESS gate not passed"
            in status(parents["autocorrelation_ess_gate"])
            or "autocorrelation ESS gate passed for target observables"
            in status(parents["autocorrelation_ess_gate"])
        )
        and parents["autocorrelation_ess_gate"].get("proposal_allowed") is False,
        status(parents["autocorrelation_ess_gate"]),
    )
    report(
        "same-source-invariant-readout-not-higgs-identity",
        "invariant readout" in status(parents["invariant_readout"])
        and parents["invariant_readout"].get("proposal_allowed") is False,
        status(parents["invariant_readout"]),
    )
    report(
        "source-pole-mixing-obstruction-loaded",
        "source-pole canonical-Higgs mixing" in status(parents["source_pole_mixing"])
        and parents["source_pole_mixing"].get("proposal_allowed") is False,
        status(parents["source_pole_mixing"]),
    )
    report(
        "no-orthogonal-top-coupling-is-not-available",
        "no-orthogonal-top-coupling import audit" in status(parents["no_orthogonal_top_coupling_import"])
        and parents["no_orthogonal_top_coupling_import"].get("proposal_allowed") is False,
        status(parents["no_orthogonal_top_coupling_import"]),
    )
    report("witness-preserves-source-response", checks["same_source_response_equal"], str(checks))
    report("witness-preserves-source-lsz-data", checks["dGamma_dp2_equal_by_construction"], str(checks))
    report("witness-changes-canonical-yukawa", checks["canonical_higgs_yukawa_differs"], str(checks))
    report(
        "target-timeseries-not-higgs-identity",
        all(
            bool(checks[key])
            for key in (
                "same_source_response_equal",
                "dGamma_dp2_equal_by_construction",
                "same_source_invariant_equal_by_construction",
                "canonical_higgs_yukawa_differs",
            )
        ),
        "same source-coordinate limits can coexist with different canonical-Higgs y_t",
    )

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / FH-LSZ target time series not canonical-Higgs identity"
        ),
        "verdict": (
            "Per-configuration same-source target time series can support "
            "autocorrelation/ESS for dE/ds and C_ss/Gamma_ss, but their "
            "infinite-statistics limit is still a source-coordinate limit.  "
            "The witness keeps the same source response, same source inverse "
            "propagator derivative, and same source-rescaling-invariant "
            "FH/LSZ readout while changing the canonical-Higgs Yukawa by "
            "rotating the source pole into an orthogonal top-coupled scalar.  "
            "Therefore target time series do not by themselves derive kappa_s "
            "or identify the source pole with the canonical Higgs radial mode."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "A source-pole purity theorem, no-orthogonal-top-coupling theorem, "
            "same-source sector-overlap identity, or independent canonical-Higgs "
            "response observable remains required."
        ),
        "target_timeseries_higgs_identity_gate_passed": False,
        "parents": PARENTS,
        "witness": witness,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not treat target time series as physical dE/dh",
            "does not set kappa_s = 1",
            "does not use H_unit, yt_ward_identity, observed top mass, observed y_t, alpha_LM, plaquette, or u0",
            "does not assume no orthogonal top-coupled scalar",
        ],
        "exact_next_action": (
            "Close one of the missing identity premises: source-pole purity, "
            "no orthogonal top coupling, same-source sector-overlap equality, "
            "or an independent canonical-Higgs response observable such as "
            "same-source W/Z mass slopes."
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
