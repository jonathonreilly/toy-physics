#!/usr/bin/env python3
"""
PR #230 top/W matched-covariance marginal-derivation no-go.

This runner tests the derivation-first shortcut for the matched top/W
covariance input.  It proves that a covariance certificate cannot be derived
from separate top-response and W-response marginal support alone: two matched
ensembles can have identical top and W marginals, identical means, identical
variances, and identical response ranges, while their matched covariance has
opposite sign.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from statistics import fmean
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_top_wz_covariance_marginal_derivation_no_go_2026-05-05.json"
FUTURE_MATCHED_ROWS = ROOT / "outputs" / "yt_top_wz_matched_response_rows_2026-05-04.json"

PARENTS = {
    "top_wz_matched_covariance_builder": "outputs/yt_top_wz_matched_covariance_certificate_builder_2026-05-04.json",
    "same_source_top_response_builder": "outputs/yt_same_source_top_response_certificate_builder_2026-05-04.json",
    "same_source_w_response_decomposition": "outputs/yt_same_source_w_response_decomposition_theorem_2026-05-04.json",
    "fh_gauge_normalized_response": "outputs/yt_fh_gauge_normalized_response_route_2026-05-02.json",
    "wz_response_measurement_row_contract": "outputs/yt_wz_response_measurement_row_contract_gate_2026-05-03.json",
    "wz_row_production_attempt": "outputs/yt_wz_response_row_production_attempt_2026-05-03.json",
    "wz_same_source_ew_action_gate": "outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json",
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
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def display(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def covariance(xs: list[float], ys: list[float]) -> float:
    mx = fmean(xs)
    my = fmean(ys)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (len(xs) - 1)


def variance(xs: list[float]) -> float:
    mx = fmean(xs)
    return sum((x - mx) ** 2 for x in xs) / (len(xs) - 1)


def same_multiset(xs: list[float], ys: list[float]) -> bool:
    return sorted(round(x, 15) for x in xs) == sorted(round(y, 15) for y in ys)


def close(a: float, b: float, tol: float = 1.0e-14) -> bool:
    return math.isclose(a, b, rel_tol=tol, abs_tol=tol)


def covariance_counterexample() -> dict[str, Any]:
    top = [1.419, 1.423, 1.427, 1.431]
    w_base = [0.512, 0.515, 0.518, 0.521]
    positive_pairing = list(zip(top, w_base))
    negative_pairing = list(zip(top, list(reversed(w_base))))

    positive_w = [w for _, w in positive_pairing]
    negative_w = [w for _, w in negative_pairing]
    positive_cov = covariance(top, positive_w)
    negative_cov = covariance(top, negative_w)
    return {
        "top_marginal": top,
        "w_marginal": w_base,
        "positive_pairing": [
            {"configuration_id": f"same-marginal-pos-{idx}", "dE_top_ds": x, "dM_W_ds": y}
            for idx, (x, y) in enumerate(positive_pairing)
        ],
        "negative_pairing": [
            {"configuration_id": f"same-marginal-neg-{idx}", "dE_top_ds": x, "dM_W_ds": y}
            for idx, (x, y) in enumerate(negative_pairing)
        ],
        "positive_cov_dE_top_dM_W": positive_cov,
        "negative_cov_dE_top_dM_W": negative_cov,
        "same_top_marginal": same_multiset(top, top),
        "same_w_marginal": same_multiset(positive_w, negative_w),
        "same_top_mean": close(fmean(top), fmean(top)),
        "same_w_mean": close(fmean(positive_w), fmean(negative_w)),
        "same_top_variance": close(variance(top), variance(top)),
        "same_w_variance": close(variance(positive_w), variance(negative_w)),
        "covariance_sign_changes": positive_cov > 0.0 and negative_cov < 0.0,
        "covariance_gap": abs(positive_cov - negative_cov),
    }


def main() -> int:
    print("PR #230 top/W covariance marginal-derivation no-go")
    print("=" * 72)

    certs = {name: load_json(rel) for name, rel in PARENTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    parent_statuses = {name: status(cert) for name, cert in certs.items()}
    witness = covariance_counterexample()

    matched_rows_absent = not FUTURE_MATCHED_ROWS.exists()
    covariance_builder_open = (
        "matched top-W response rows absent" in parent_statuses["top_wz_matched_covariance_builder"]
        and certs["top_wz_matched_covariance_builder"].get(
            "strict_top_wz_matched_covariance_builder_passed"
        )
        is False
    )
    top_response_open = (
        "same-source top-response identity or covariance inputs absent"
        in parent_statuses["same_source_top_response_builder"]
        and certs["same_source_top_response_builder"].get(
            "strict_same_source_top_response_certificate_builder_passed"
        )
        is False
    )
    w_decomposition_support_only = (
        "same-source W-response decomposition theorem"
        in parent_statuses["same_source_w_response_decomposition"]
        and certs["same_source_w_response_decomposition"].get("current_closure_gate_passed")
        is False
    )
    row_contract_support_only = (
        "WZ response measurement-row contract gate"
        in parent_statuses["wz_response_measurement_row_contract"]
        and certs["wz_response_measurement_row_contract"].get("wz_measurement_row_contract_gate_passed")
        is False
    )
    row_production_no_go = (
        "WZ response row production attempt" in parent_statuses["wz_row_production_attempt"]
        and certs["wz_row_production_attempt"].get("measurement_rows_written") is False
    )
    ew_action_absent = (
        "same-source EW action not defined" in parent_statuses["wz_same_source_ew_action_gate"]
        and certs["wz_same_source_ew_action_gate"].get("same_source_ew_action_ready") is False
    )
    no_marginal_derivation = (
        witness["same_top_marginal"]
        and witness["same_w_marginal"]
        and witness["same_top_mean"]
        and witness["same_w_mean"]
        and witness["same_top_variance"]
        and witness["same_w_variance"]
        and witness["covariance_sign_changes"]
        and witness["covariance_gap"] > 0.0
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("future-matched-response-rows-absent", matched_rows_absent, display(FUTURE_MATCHED_ROWS))
    report("covariance-builder-currently-open", covariance_builder_open, parent_statuses["top_wz_matched_covariance_builder"])
    report("top-response-builder-currently-open", top_response_open, parent_statuses["same_source_top_response_builder"])
    report("w-response-decomposition-support-only", w_decomposition_support_only, parent_statuses["same_source_w_response_decomposition"])
    report("wz-row-contract-support-only", row_contract_support_only, parent_statuses["wz_response_measurement_row_contract"])
    report("wz-row-production-no-go-loaded", row_production_no_go, parent_statuses["wz_row_production_attempt"])
    report("same-source-ew-action-absent", ew_action_absent, parent_statuses["wz_same_source_ew_action_gate"])
    report("same-marginal-opposite-covariance-witness", no_marginal_derivation, f"gap={witness['covariance_gap']:.12g}")
    report("marginal-derivation-shortcut-rejected", no_marginal_derivation, "covariance is joint data, not marginal data")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / matched top-W covariance not derivable from marginal response support"
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Separate top-response and W-response support do not determine the "
            "matched covariance.  A strict certificate needs paired rows or an "
            "independent factorization/independence theorem."
        ),
        "bare_retained_allowed": False,
        "marginal_derivation_no_go_passed": no_marginal_derivation,
        "future_matched_rows_present": not matched_rows_absent,
        "counterexample": witness,
        "parent_certificates": PARENTS,
        "parent_statuses": parent_statuses,
        "blocked_shortcut": {
            "candidate": "derive cov_dE_top_dM_W from top marginal support plus W marginal or static EW response",
            "reason": (
                "The same top marginal and same W marginal admit multiple "
                "joint couplings with different covariance, so the covariance "
                "is not a function of the marginal response certificates."
            ),
        },
        "allowed_future_routes": [
            "measure matched top/W response rows on the same configuration set",
            "derive a same-surface factorization or independence theorem that fixes cov_dE_top_dM_W",
            "derive a deterministic W-response theorem with a validated rule for finite-sample covariance against top response",
        ],
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not synthesize production matched rows",
            "does not treat static EW algebra as W/Z measurement rows",
            "does not use observed W/Z, top, y_t, or g2 selectors",
            "does not use H_unit, yt_ward_identity, alpha_LM, plaquette/u0, c2=1, Z_match=1, or kappa_s=1",
        ],
        "exact_next_action": (
            "Either produce matched top/W response rows or derive a real "
            "factorization/independence theorem for the joint top/W source "
            "response.  Do not derive covariance from marginal top and W "
            "response support alone."
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
