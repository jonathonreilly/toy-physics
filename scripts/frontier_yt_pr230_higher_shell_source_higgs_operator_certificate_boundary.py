#!/usr/bin/env python3
"""
PR #230 higher-shell source-Higgs operator-certificate boundary.

The active higher-shell workers include source/operator cross-correlator
instrumentation.  This block checks the exact operator certificate supplied to
that instrumentation.  The current certificate is the two-source taste-radial
source vertex, not a canonical Higgs operator certificate.  Therefore pending
or future completed rows emitted under this certificate are C_sx/C_xx
taste-radial support rows, not strict C_sH/C_HH source-Higgs pole evidence.
"""

from __future__ import annotations

import json
import shlex
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_higher_shell_source_higgs_operator_certificate_boundary_2026-05-12.json"
)

PARENTS = {
    "higher_shell_wave_launcher": "outputs/yt_pr230_schur_higher_shell_wave_launcher_2026-05-12.json",
    "higher_shell_chunk001_pending": "outputs/yt_pr230_schur_higher_shell_chunk001_pending_checkpoint_2026-05-12.json",
    "higher_shell_chunk002_pending": "outputs/yt_pr230_schur_higher_shell_chunk002_pending_checkpoint_2026-05-12.json",
    "two_source_taste_radial_action_certificate": "outputs/yt_pr230_two_source_taste_radial_action_certificate_2026-05-06.json",
    "source_higgs_production_readiness": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "source_higgs_cross_correlator_manifest": "outputs/yt_source_higgs_cross_correlator_manifest_2026-05-02.json",
    "source_higgs_pole_residue_extractor": "outputs/yt_source_higgs_pole_residue_extractor_2026-05-03.json",
    "source_higgs_gram_purity_postprocessor": "outputs/yt_source_higgs_gram_purity_postprocess_2026-05-03.json",
    "physical_euclidean_source_higgs_absence": "outputs/yt_pr230_physical_euclidean_source_higgs_row_absence_after_block44_2026-05-12.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

EXPECTED_OPERATOR_CERT = (
    "outputs/yt_pr230_two_source_taste_radial_action_certificate_2026-05-06.json"
)
CHUNK_OUTPUT_ROOT = ROOT / "outputs" / "yt_pr230_schur_higher_shell_rows"

FORBIDDEN_FIREWALL = {
    "used_hunit_matrix_element_readout": False,
    "used_yt_ward_identity": False,
    "used_y_t_bare": False,
    "used_observed_top_or_yukawa_as_selector": False,
    "used_alpha_lm_plaquette_or_u0": False,
    "treated_taste_radial_x_as_canonical_oh": False,
    "treated_c_sx_c_xx_aliases_as_strict_c_sh_c_hh": False,
    "treated_pending_workers_as_row_evidence": False,
    "treated_completed_higher_shell_rows_as_pole_residues": False,
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


def load(rel: str | Path) -> dict[str, Any]:
    path = Path(rel)
    if not path.is_absolute():
        path = ROOT / path
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def command_tokens(command: str) -> list[str]:
    try:
        return shlex.split(command)
    except ValueError:
        return command.split()


def option_value(tokens: list[str], option: str) -> str | None:
    if option in tokens:
        index = tokens.index(option)
        if index + 1 < len(tokens):
            return tokens[index + 1]
    prefix = option + "="
    for token in tokens:
        if token.startswith(prefix):
            return token[len(prefix) :]
    return None


def source_higgs_commands(wave: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in wave.get("active_process_rows", []) + wave.get("considered_rows", []):
        if not isinstance(row, dict):
            continue
        command = str(row.get("command", ""))
        if "--source-higgs-cross-modes" not in command:
            continue
        tokens = command_tokens(command)
        rows.append(
            {
                "chunk_index": row.get("chunk_index"),
                "operator_certificate": option_value(
                    tokens, "--source-higgs-operator-certificate"
                ),
                "source_higgs_cross_modes": option_value(
                    tokens, "--source-higgs-cross-modes"
                ),
                "source_higgs_cross_noises": option_value(
                    tokens, "--source-higgs-cross-noises"
                ),
                "output": row.get("output"),
                "output_present": bool(row.get("output_present")),
                "active": bool(row.get("active")),
            }
        )
    unique: dict[tuple[Any, Any], dict[str, Any]] = {}
    for row in rows:
        unique[(row.get("chunk_index"), row.get("output"))] = row
    return list(unique.values())


def completed_chunk_outputs() -> list[str]:
    if not CHUNK_OUTPUT_ROOT.exists():
        return []
    return sorted(
        str(path.relative_to(ROOT))
        for path in CHUNK_OUTPUT_ROOT.glob(
            "yt_pr230_schur_higher_shell_rows_L12_T24_chunk*_2026-05-07.json"
        )
    )


def completed_rows_have_taste_radial_aliases(paths: list[str]) -> bool:
    for rel in paths:
        data = load(rel)
        ensembles = data.get("ensembles", [])
        if not isinstance(ensembles, list):
            return False
        for ensemble in ensembles:
            if not isinstance(ensemble, dict):
                return False
            analysis = ensemble.get("source_higgs_cross_correlator_analysis", {})
            if not isinstance(analysis, dict):
                return False
            aliases = analysis.get("two_source_taste_radial_row_aliases", {})
            if aliases.get("available") is not True:
                return False
            if analysis.get("canonical_higgs_operator_identity_passed") is not False:
                return False
            if analysis.get("used_as_physical_yukawa_readout") is not False:
                return False
    return True


def harness_semantic_firewall_present() -> bool:
    source = (ROOT / "scripts" / "yt_direct_lattice_correlator_production.py").read_text(
        encoding="utf-8"
    )
    required = [
        "The certificate, not this estimator",
        "downstream analysis emits C_sx/C_xx aliases",
        "source_higgs_operator_is_taste_radial_second_source",
        "C_sx_aliases_C_sH_schema_field",
        "canonical_higgs_operator_identity_passed",
        "C_sx/C_xx aliases are second-source taste-radial rows",
        "are not canonical-Higgs C_sH/C_HH rows unless a separate",
    ]
    return all(fragment in source for fragment in required)


def main() -> int:
    print("PR #230 higher-shell source-Higgs operator-certificate boundary")
    print("=" * 82)

    certs = {name: load(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing = [name for name, cert in certs.items() if not cert]
    failing = [
        name
        for name, cert in certs.items()
        if int(cert.get("fail_count", cert.get("fails", 0)) or 0) != 0
    ]
    proposal_parents = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    wave = certs["higher_shell_wave_launcher"]
    action = certs["two_source_taste_radial_action_certificate"]
    commands = source_higgs_commands(wave)
    completed = completed_chunk_outputs()

    wave_present_and_support_only = (
        wave.get("wave_launcher_passed") is True
        and wave.get("proposal_allowed") is False
        and "run-control" in statuses["higher_shell_wave_launcher"]
    )
    commands_use_expected_taste_radial_cert = (
        bool(commands)
        and all(row.get("operator_certificate") == EXPECTED_OPERATOR_CERT for row in commands)
        and all(row.get("source_higgs_cross_modes") for row in commands)
        and all(int(row.get("source_higgs_cross_noises") or 0) > 0 for row in commands)
    )
    action_cert_is_taste_radial_not_canonical = (
        "two-source taste-radial action source vertex"
        in statuses["two_source_taste_radial_action_certificate"]
        and action.get("two_source_taste_radial_action_passed") is True
        and action.get("operator_id") == "pr230_taste_radial_hypercube_flip_source_v1"
        and action.get("canonical_higgs_operator_identity_passed") is False
        and action.get("hunit_used_as_operator") is False
        and action.get("proposal_allowed") is False
    )
    action_firewall_clean = (
        action.get("firewall", {}).get("used_taste_radial_axis_as_canonical_oh") is False
        and action.get("firewall", {}).get("used_hunit_matrix_element_readout") is False
        and action.get("firewall", {}).get("used_yt_ward_identity") is False
        and action.get("firewall", {}).get("claimed_retained_or_proposed_retained") is False
    )
    pending_chunks_are_run_control = all(
        certs[name].get("proposal_allowed") is False
        and certs[name].get("completed") is False
        and certs[name].get("pending_active") is True
        and "run-control" in statuses[name]
        for name in ("higher_shell_chunk001_pending", "higher_shell_chunk002_pending")
    )
    harness_firewall = harness_semantic_firewall_present()
    completed_outputs_safe_if_any = (
        completed_rows_have_taste_radial_aliases(completed) if completed else True
    )
    source_higgs_readiness_blocks = (
        "source-Higgs production launch blocked by missing O_H certificate"
        in statuses["source_higgs_production_readiness"]
        and certs["source_higgs_production_readiness"].get("proposal_allowed") is False
    )
    pole_and_gram_wait = (
        "awaiting valid production rows" in statuses["source_higgs_pole_residue_extractor"]
        and "awaiting" in statuses["source_higgs_gram_purity_postprocessor"]
        and "production" in statuses["source_higgs_gram_purity_postprocessor"]
    )
    block44_boundary_still_applies = (
        "source-Higgs row absence" in statuses["physical_euclidean_source_higgs_absence"]
        or "source-Higgs" in statuses["physical_euclidean_source_higgs_absence"]
    ) and certs["physical_euclidean_source_higgs_absence"].get("proposal_allowed") is False
    aggregate_still_open = (
        certs["full_positive_assembly"].get("proposal_allowed") is False
        and certs["campaign_status"].get("proposal_allowed") is False
    )
    firewall_clean = all(value is False for value in FORBIDDEN_FIREWALL.values())

    boundary_passed = all(
        [
            not missing,
            not failing,
            not proposal_parents,
            wave_present_and_support_only,
            commands_use_expected_taste_radial_cert,
            action_cert_is_taste_radial_not_canonical,
            action_firewall_clean,
            pending_chunks_are_run_control,
            harness_firewall,
            completed_outputs_safe_if_any,
            source_higgs_readiness_blocks,
            pole_and_gram_wait,
            block44_boundary_still_applies,
            aggregate_still_open,
            firewall_clean,
        ]
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("parent-certificates-have-no-fails", not failing, f"failing={failing}")
    report("no-parent-authorizes-proposal", not proposal_parents, f"proposal_allowed={proposal_parents}")
    report("higher-shell-wave-support-only", wave_present_and_support_only, statuses["higher_shell_wave_launcher"])
    report("source-higgs-commands-use-taste-radial-cert", commands_use_expected_taste_radial_cert, str(commands[:2]))
    report("operator-cert-is-taste-radial-not-canonical", action_cert_is_taste_radial_not_canonical, statuses["two_source_taste_radial_action_certificate"])
    report("operator-cert-firewall-clean", action_firewall_clean, str(action.get("firewall", {})))
    report("pending-chunks-are-run-control", pending_chunks_are_run_control, "chunk001/chunk002 pending active")
    report("production-harness-semantic-firewall-present", harness_firewall, "C_sx/C_xx alias firewall in harness")
    report("completed-outputs-safe-if-any", completed_outputs_safe_if_any, str(completed))
    report("source-higgs-readiness-still-blocks", source_higgs_readiness_blocks, statuses["source_higgs_production_readiness"])
    report("pole-and-gram-gates-wait", pole_and_gram_wait, f"{statuses['source_higgs_pole_residue_extractor']} / {statuses['source_higgs_gram_purity_postprocessor']}")
    report("block44-boundary-still-applies", block44_boundary_still_applies, statuses["physical_euclidean_source_higgs_absence"])
    report("aggregate-gates-still-open", aggregate_still_open, statuses["full_positive_assembly"])
    report("forbidden-firewall-clean", firewall_clean, str(FORBIDDEN_FIREWALL))
    report("higher-shell-source-higgs-operator-certificate-boundary", boundary_passed, "higher-shell cross rows under current cert remain taste-radial support")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / higher-shell source-Higgs cross rows use "
            "the taste-radial second-source certificate, not canonical O_H"
        ),
        "conditional_surface_status": (
            "conditional-support if future rows are rerun with a certified canonical "
            "O_H operator or a separate same-surface O_H/source-overlap bridge passes"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The active higher-shell source/operator cross-correlator commands use "
            "the PR230 taste-radial second-source certificate.  That certificate "
            "explicitly has canonical_higgs_operator_identity_passed=false, so rows "
            "under it are C_sx/C_xx support rather than strict C_sH/C_HH evidence."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "higher_shell_source_higgs_operator_certificate_boundary_passed": boundary_passed,
        "source_higgs_command_summary": commands,
        "completed_higher_shell_outputs": completed,
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "operator_certificate_summary": {
            "operator_id": action.get("operator_id"),
            "canonical_higgs_operator_identity_passed": action.get(
                "canonical_higgs_operator_identity_passed"
            ),
            "hunit_used_as_operator": action.get("hunit_used_as_operator"),
            "proposal_allowed": action.get("proposal_allowed"),
            "firewall": action.get("firewall", {}),
        },
        "forbidden_firewall": FORBIDDEN_FIREWALL,
        "open_imports": [
            "certified canonical O_H operator identity",
            "same-surface source-overlap or physical neutral-transfer bridge",
            "strict production C_ss/C_sH/C_HH(tau) rows under canonical O_H authority",
            "pole/FV/IR/model-class and Gram-purity authority",
        ],
        "exact_next_action": (
            "If the higher-shell chunks finish, checkpoint them as taste-radial "
            "C_sx/C_xx support unless a separate canonical O_H/source-overlap "
            "certificate lands.  Do not treat C_sH/C_HH schema fields emitted "
            "under the current certificate as strict source-Higgs rows."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 and boundary_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
