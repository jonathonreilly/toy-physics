#!/usr/bin/env python3
"""
PR #230 W/Z response-only g2 self-normalization no-go.

Same-source top/W/Z response ratios can cancel the scalar source coordinate,
but they cannot determine the absolute electroweak coupling normalization.
This runner constructs an exact family with identical top, W, and Z scalar
source slopes while g2, gY, and y_t all rescale.  The family leaves response
ratios invariant, so a response-only W/Z self-normalization shortcut cannot
replace a strict non-observed g2 certificate.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_wz_g2_response_self_normalization_no_go_2026-05-05.json"

PARENTS = {
    "wz_g2_authority_firewall": "outputs/yt_wz_g2_authority_firewall_2026-05-05.json",
    "wz_mass_fit_response_row_builder": "outputs/yt_wz_mass_fit_response_row_builder_2026-05-04.json",
    "wz_response_measurement_row_contract": "outputs/yt_wz_response_measurement_row_contract_gate_2026-05-03.json",
    "fh_gauge_normalized_response": "outputs/yt_fh_gauge_normalized_response_route_2026-05-02.json",
    "fh_gauge_response_mixed_scalar": "outputs/yt_fh_gauge_response_mixed_scalar_obstruction_2026-05-02.json",
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


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def response_family() -> list[dict[str, float]]:
    base = {
        "kappa_source": 1.35,
        "y_t": 0.92,
        "g2": 0.66,
        "gY": 0.36,
    }
    rows = []
    for lam in (0.75, 1.0, 1.25):
        kappa = lam * base["kappa_source"]
        y_t = base["y_t"] / lam
        g2 = base["g2"] / lam
        gY = base["gY"] / lam
        d_e_top = kappa * y_t / math.sqrt(2.0)
        d_m_w = kappa * g2 / 2.0
        d_m_z = kappa * math.sqrt(g2 * g2 + gY * gY) / 2.0
        rows.append(
            {
                "lambda": lam,
                "kappa_source": kappa,
                "y_t": y_t,
                "g2": g2,
                "gY": gY,
                "dE_top_ds": d_e_top,
                "dM_W_ds": d_m_w,
                "dM_Z_ds": d_m_z,
                "top_over_w_response_ratio": d_e_top / d_m_w,
                "z_over_w_response_ratio": d_m_z / d_m_w,
                "y_t_over_g2": y_t / g2,
                "gY_over_g2": gY / g2,
            }
        )
    return rows


def rounded_values(rows: list[dict[str, float]], key: str) -> set[float]:
    return {round(float(row[key]), 12) for row in rows}


def main() -> int:
    print("PR #230 W/Z response-only g2 self-normalization no-go")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    rows = response_family()

    response_invariants = {
        "dE_top_ds": rounded_values(rows, "dE_top_ds"),
        "dM_W_ds": rounded_values(rows, "dM_W_ds"),
        "dM_Z_ds": rounded_values(rows, "dM_Z_ds"),
        "top_over_w_response_ratio": rounded_values(rows, "top_over_w_response_ratio"),
        "z_over_w_response_ratio": rounded_values(rows, "z_over_w_response_ratio"),
        "y_t_over_g2": rounded_values(rows, "y_t_over_g2"),
        "gY_over_g2": rounded_values(rows, "gY_over_g2"),
    }
    varying_values = {
        "y_t": rounded_values(rows, "y_t"),
        "g2": rounded_values(rows, "g2"),
        "gY": rounded_values(rows, "gY"),
        "kappa_source": rounded_values(rows, "kappa_source"),
    }

    g2_firewall_blocks = (
        "WZ response g2 authority absent"
        in parents["wz_g2_authority_firewall"].get("actual_current_surface_status", "")
        and parents["wz_g2_authority_firewall"].get("proposal_allowed") is False
        and parents["wz_g2_authority_firewall"].get("g2_authority_gate_passed") is False
    )
    row_builder_records_absent_g2 = (
        parents["wz_mass_fit_response_row_builder"]
        .get("g2_validation", {})
        .get("present")
        is False
    )
    mixed_scalar_boundary_loaded = (
        "mixed-scalar obstruction"
        in parents["fh_gauge_response_mixed_scalar"].get("actual_current_surface_status", "")
        and parents["fh_gauge_response_mixed_scalar"].get("proposal_allowed") is False
    )

    all_response_quantities_fixed = all(len(values) == 1 for values in response_invariants.values())
    absolute_couplings_vary = all(len(values) == len(rows) for values in varying_values.values())

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("g2-authority-firewall-loaded", g2_firewall_blocks, PARENTS["wz_g2_authority_firewall"])
    report("wz-row-builder-records-g2-absent", row_builder_records_absent_g2, PARENTS["wz_mass_fit_response_row_builder"])
    report("response-family-keeps-all-response-data-fixed", all_response_quantities_fixed, str(response_invariants))
    report("absolute-yukawa-and-gauge-couplings-vary", absolute_couplings_vary, str(varying_values))
    report("response-only-self-normalization-rejected", all_response_quantities_fixed and absolute_couplings_vary, "same response data do not fix g2 or y_t")
    report("mixed-scalar-boundary-still-loaded", mixed_scalar_boundary_loaded, PARENTS["fh_gauge_response_mixed_scalar"])
    report("does-not-authorize-retained-proposal", True, "exact negative boundary only")

    result = {
        "actual_current_surface_status": "exact negative boundary / WZ response-only g2 self-normalization no-go",
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Same-source top/W/Z response data determine response ratios such as "
            "y_t/g2 and gY/g2, but not the absolute g2 normalization or absolute y_t."
        ),
        "bare_retained_allowed": False,
        "g2_response_self_normalization_no_go_passed": (
            all_response_quantities_fixed and absolute_couplings_vary
        ),
        "parent_certificates": PARENTS,
        "countermodel_family": {
            "transformation": "kappa_source -> lambda*kappa_source; y_t,g2,gY -> (y_t,g2,gY)/lambda",
            "invariant_response_data": {key: sorted(values) for key, values in response_invariants.items()},
            "varying_absolute_parameters": {key: sorted(values) for key, values in varying_values.items()},
            "rows": rows,
        },
        "theorem_statement": (
            "For response observables dE_top/ds=k*y_t/sqrt(2), "
            "dM_W/ds=k*g2/2, and dM_Z/ds=k*sqrt(g2^2+gY^2)/2, the scaling "
            "(k,y_t,g2,gY)->(lambda k,y_t/lambda,g2/lambda,gY/lambda) leaves all "
            "same-source top/W/Z response slopes and ratios invariant while changing "
            "the absolute y_t and g2.  Therefore a response-only W/Z self-normalization "
            "cannot replace an allowed g2 certificate."
        ),
        "allowed_escape_routes": [
            "supply a strict non-observed g2 certificate from an allowed authority",
            "derive an absolute electroweak normalization theorem that is not response-only",
            "derive a separate theorem in which g2 cancels against another already-certified physical observable",
        ],
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not import observed g2, observed W/Z, observed top mass, or observed y_t",
            "does not use H_unit matrix-element readout or yt_ward_identity",
            "does not use alpha_LM, plaquette, or u0 as proof authority",
            "does not set kappa_s=1, c2=1, Z_match=1, or g2 to a package value",
        ],
        "exact_next_action": (
            "Do not spend another block on response-only g2 cancellation.  Either "
            "build an allowed electroweak g2 certificate, add absolute EW normalization "
            "data/theorem outside response-only rows, or continue source-Higgs/Schur/"
            "rank-one identity routes while chunks019-024 run."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {rel(OUTPUT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
