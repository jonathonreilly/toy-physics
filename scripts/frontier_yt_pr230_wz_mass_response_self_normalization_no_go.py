#!/usr/bin/env python3
"""
PR #230 W/Z mass-plus-response self-normalization no-go.

The existing W/Z response-only g2 no-go shows that same-source response
slopes determine ratios such as y_t/g2, not the absolute electroweak coupling.
This runner checks the stronger adjacent shortcut: can adding same-surface
top/W/Z mass rows to the same-source response rows self-normalize the absolute
couplings?

No.  The full mass+response dictionary

  m_t = y_t v / sqrt(2),   M_W = g2 v / 2,
  M_Z = sqrt(g2^2 + gY^2) v / 2,
  dm_t/ds = y_t k / sqrt(2), dM_W/ds = g2 k / 2,
  dM_Z/ds = sqrt(g2^2 + gY^2) k / 2

is invariant under (v,k) -> lambda (v,k) and
(y_t,g2,gY) -> (y_t,g2,gY)/lambda.  Thus even ideal top/W/Z
mass+response rows do not fix absolute y_t without a strict v or g2
normalization theorem/certificate.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_wz_mass_response_self_normalization_no_go_2026-05-12.json"
)

PARENTS = {
    "wz_response_ratio_contract": "outputs/yt_pr230_wz_response_ratio_identifiability_contract_2026-05-07.json",
    "wz_g2_authority_firewall": "outputs/yt_wz_g2_authority_firewall_2026-05-05.json",
    "wz_g2_response_self_normalization_no_go": "outputs/yt_wz_g2_response_self_normalization_no_go_2026-05-05.json",
    "wz_g2_bare_running_bridge_attempt": "outputs/yt_pr230_wz_g2_bare_running_bridge_attempt_2026-05-05.json",
    "wz_physical_response_intake": "outputs/yt_pr230_wz_physical_response_packet_intake_checkpoint_2026-05-07.json",
    "wz_accepted_action_root": "outputs/yt_pr230_wz_accepted_action_response_root_checkpoint_2026-05-07.json",
    "wz_mass_fit_path": "outputs/yt_wz_correlator_mass_fit_path_gate_2026-05-04.json",
    "electroweak_g2_builder": "outputs/yt_electroweak_g2_certificate_builder_2026-05-05.json",
}

STRICT_G2_CERT = ROOT / "outputs" / "yt_electroweak_g2_certificate_2026-05-04.json"

FORBIDDEN_FIREWALL = {
    "used_hunit_matrix_element_readout": False,
    "used_yt_ward_identity": False,
    "used_y_t_bare": False,
    "used_observed_top_w_z_or_yt_selector": False,
    "used_observed_g2_selector": False,
    "used_alpha_lm_plaquette_or_u0": False,
    "set_v_or_g2_by_unit_convention": False,
    "treated_static_ew_algebra_as_response_rows": False,
    "treated_scout_or_smoke_rows_as_production": False,
    "claimed_retained_or_proposed_retained": False,
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


def load(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def mass_response_family() -> list[dict[str, Any]]:
    base = {
        "v": 246.0,
        "dv_ds": 3.2,
        "y_t": 0.92,
        "g2": 0.64,
        "gY": 0.36,
    }
    rows: list[dict[str, Any]] = []
    for lam in (0.5, 1.0, 2.0):
        v = lam * base["v"]
        dv_ds = lam * base["dv_ds"]
        y_t = base["y_t"] / lam
        g2 = base["g2"] / lam
        gY = base["gY"] / lam
        gZ = math.sqrt(g2 * g2 + gY * gY)
        rows.append(
            {
                "lambda": lam,
                "parameters": {
                    "v": v,
                    "dv_ds": dv_ds,
                    "y_t": y_t,
                    "g2": g2,
                    "gY": gY,
                    "gZ": gZ,
                },
                "observables": {
                    "m_top": y_t * v / math.sqrt(2.0),
                    "M_W": g2 * v / 2.0,
                    "M_Z": gZ * v / 2.0,
                    "dm_top_ds": y_t * dv_ds / math.sqrt(2.0),
                    "dM_W_ds": g2 * dv_ds / 2.0,
                    "dM_Z_ds": gZ * dv_ds / 2.0,
                    "m_top_over_M_W": (y_t * v / math.sqrt(2.0)) / (g2 * v / 2.0),
                    "dm_top_ds_over_dM_W_ds": (y_t * dv_ds / math.sqrt(2.0))
                    / (g2 * dv_ds / 2.0),
                    "M_W_over_M_Z": (g2 * v / 2.0) / (gZ * v / 2.0),
                    "dM_W_ds_over_dM_Z_ds": (g2 * dv_ds / 2.0)
                    / (gZ * dv_ds / 2.0),
                },
            }
        )
    return rows


def rounded_set(rows: list[dict[str, Any]], group: str, key: str) -> set[float]:
    return {round(float(row[group][key]), 12) for row in rows}


def main() -> int:
    print("PR #230 W/Z mass-plus-response self-normalization no-go")
    print("=" * 76)

    certs = {name: load(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_parents = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]
    rows = mass_response_family()
    observable_keys = list(rows[0]["observables"].keys())
    parameter_keys = ["v", "dv_ds", "y_t", "g2", "gY", "gZ"]
    observable_sets = {key: rounded_set(rows, "observables", key) for key in observable_keys}
    parameter_sets = {key: rounded_set(rows, "parameters", key) for key in parameter_keys}

    all_mass_response_observables_fixed = all(
        len(values) == 1 for values in observable_sets.values()
    )
    absolute_parameters_vary = all(len(values) == len(rows) for values in parameter_sets.values())
    ratios_fixed = all(
        len(observable_sets[key]) == 1
        for key in (
            "m_top_over_M_W",
            "dm_top_ds_over_dM_W_ds",
            "M_W_over_M_Z",
            "dM_W_ds_over_dM_Z_ds",
        )
    )
    g2_firewall_blocks = (
        "WZ response g2 authority absent" in statuses["wz_g2_authority_firewall"]
        and certs["wz_g2_authority_firewall"].get("proposal_allowed") is False
        and certs["wz_g2_authority_firewall"].get("g2_authority_gate_passed") is False
    )
    response_only_no_go_loaded = (
        certs["wz_g2_response_self_normalization_no_go"].get(
            "g2_response_self_normalization_no_go_passed"
        )
        is True
    )
    bare_running_no_go_loaded = (
        certs["wz_g2_bare_running_bridge_attempt"].get(
            "wz_g2_bare_running_bridge_passed"
        )
        is False
        and certs["wz_g2_bare_running_bridge_attempt"].get(
            "exact_negative_boundary_passed"
        )
        is True
    )
    physical_packet_absent = (
        "WZ physical-response packet not present"
        in statuses["wz_physical_response_intake"]
        and certs["wz_physical_response_intake"].get("proposal_allowed") is False
    )
    action_root_absent = (
        "WZ accepted-action response root not closed"
        in statuses["wz_accepted_action_root"]
        and certs["wz_accepted_action_root"].get("proposal_allowed") is False
    )
    mass_fit_path_absent = (
        "WZ correlator mass-fit path absent" in statuses["wz_mass_fit_path"]
        and certs["wz_mass_fit_path"].get("proposal_allowed") is False
    )
    strict_g2_cert_absent = not STRICT_G2_CERT.exists()
    g2_builder_open = (
        "electroweak g2 certificate builder inputs absent"
        in statuses["electroweak_g2_builder"]
        and certs["electroweak_g2_builder"].get("proposal_allowed") is False
    )
    firewall_clean = all(value is False for value in FORBIDDEN_FIREWALL.values())

    no_go_passed = (
        not missing
        and not proposal_parents
        and all_mass_response_observables_fixed
        and absolute_parameters_vary
        and ratios_fixed
        and g2_firewall_blocks
        and response_only_no_go_loaded
        and bare_running_no_go_loaded
        and physical_packet_absent
        and action_root_absent
        and mass_fit_path_absent
        and strict_g2_cert_absent
        and g2_builder_open
        and firewall_clean
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_parents, f"proposal_allowed={proposal_parents}")
    report("mass-response-observables-fixed", all_mass_response_observables_fixed, str(observable_sets))
    report("absolute-parameters-vary", absolute_parameters_vary, str(parameter_sets))
    report("mass-and-response-ratios-fixed", ratios_fixed, str({k: observable_sets[k] for k in observable_sets if 'over' in k}))
    report("g2-authority-firewall-blocks", g2_firewall_blocks, statuses["wz_g2_authority_firewall"])
    report("response-only-g2-no-go-loaded", response_only_no_go_loaded, statuses["wz_g2_response_self_normalization_no_go"])
    report("bare-running-g2-no-go-loaded", bare_running_no_go_loaded, statuses["wz_g2_bare_running_bridge_attempt"])
    report("physical-response-packet-absent", physical_packet_absent, statuses["wz_physical_response_intake"])
    report("accepted-action-root-absent", action_root_absent, statuses["wz_accepted_action_root"])
    report("mass-fit-path-absent", mass_fit_path_absent, statuses["wz_mass_fit_path"])
    report("strict-g2-certificate-absent", strict_g2_cert_absent, str(STRICT_G2_CERT))
    report("electroweak-g2-builder-open", g2_builder_open, statuses["electroweak_g2_builder"])
    report("forbidden-firewall-clean", firewall_clean, str(FORBIDDEN_FIREWALL))
    report("mass-response-self-normalization-no-go", no_go_passed, "mass+response rows still leave scale orbit")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / WZ top-W-Z mass-plus-response "
            "self-normalization does not fix absolute y_t on the current PR230 surface"
        ),
        "conditional_surface_status": (
            "conditional-support if a future strict non-observed g2 certificate, "
            "absolute v authority accepted as a substrate input, or another absolute "
            "EW normalization theorem is supplied"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The same idealized top/W/Z mass and same-source response rows are "
            "invariant under v,dv/ds scaling with inverse coupling scaling. "
            "They determine ratios, not absolute y_t, unless a strict g2/v "
            "normalization authority is supplied."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "wz_mass_response_self_normalization_no_go_passed": no_go_passed,
        "strict_g2_certificate_present": not strict_g2_cert_absent,
        "mass_response_scale_orbit": {
            "transformation": "(v,dv_ds)->lambda*(v,dv_ds); (y_t,g2,gY)->(y_t,g2,gY)/lambda",
            "invariant_observables": {key: sorted(values) for key, values in observable_sets.items()},
            "varying_parameters": {key: sorted(values) for key, values in parameter_sets.items()},
            "rows": rows,
        },
        "parent_statuses": statuses,
        "forbidden_firewall": FORBIDDEN_FIREWALL,
        "allowed_escape_routes": [
            "supply a strict non-observed g2 certificate from an allowed authority",
            "admit v as an explicit substrate input for the specific readout and keep that dependency visible",
            "derive an absolute EW normalization theorem outside top/W/Z mass-response rows",
            "return to direct m_t measurement with explicit v input and matching bridge",
        ],
        "strict_non_claims": [
            "does not claim retained or proposed_retained top-Yukawa closure",
            "does not use observed top/W/Z/y_t/g2 values as proof selectors",
            "does not use H_unit, yt_ward_identity, y_t_bare, alpha_LM, plaquette, or u0",
            "does not set v, g2, c2, Z_match, or kappa_s by unit convention",
            "does not treat W/Z scout or smoke rows as production evidence",
        ],
        "exact_next_action": (
            "Do not pursue W/Z mass+response self-normalization as a g2/v "
            "replacement.  Continue only with a strict g2/v authority, a real "
            "W/Z production packet plus that authority, or a different native "
            "scalar/action/LSZ or neutral-transfer primitive."
        ),
        "summary": {"pass": PASS_COUNT, "fail": FAIL_COUNT},
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
