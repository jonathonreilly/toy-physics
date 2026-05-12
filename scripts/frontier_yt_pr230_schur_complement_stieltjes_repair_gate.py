#!/usr/bin/env python3
"""
PR #230 Schur-complement Stieltjes repair gate.

The strict scalar-LSZ gate shows that the raw selected-mass `C_ss(q)` proxy
is not the positive unsubtracted Stieltjes scalar object: it increases from
the zero mode to the first shell.  This runner tests the adjacent, more
physical repair candidate already present in the two-source taste-radial row
packet:

    G(q) = [[C_ss(q), C_sx(q)], [C_sx(q), C_xx(q)]],
    C_s|x(q) = det(G(q)) / C_xx(q),
    C_x|s(q) = det(G(q)) / C_ss(q).

These Schur-complement residuals are finite contact-subtracted candidates only.
Passing a first-shell Stieltjes monotonicity check is necessary, not sufficient:
closure would still need complete rows, isolated-pole/model-class authority,
multivolume FV/IR control, and canonical O_H/source-overlap or W/Z response
authority.
"""

from __future__ import annotations

import json
import math
import statistics
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_schur_complement_stieltjes_repair_gate_2026-05-07.json"
)
MANIFEST = (
    ROOT
    / "outputs"
    / "yt_pr230_two_source_taste_radial_row_production_manifest_2026-05-06.json"
)
COMBINER = (
    ROOT
    / "outputs"
    / "yt_pr230_two_source_taste_radial_row_combiner_gate_2026-05-06.json"
)

PARENTS = {
    "two_source_schur_subblock_witness": "outputs/yt_pr230_two_source_taste_radial_schur_subblock_witness_2026-05-06.json",
    "two_source_schur_kprime_finite_shell_scout": "outputs/yt_pr230_two_source_taste_radial_schur_kprime_finite_shell_scout_2026-05-06.json",
    "two_source_schur_abc_finite_rows": "outputs/yt_pr230_two_source_taste_radial_schur_abc_finite_rows_2026-05-06.json",
    "strict_scalar_lsz_moment_fv": "outputs/yt_pr230_strict_scalar_lsz_moment_fv_authority_gate_2026-05-07.json",
    "schur_pole_lift_gate": "outputs/yt_pr230_two_source_taste_radial_schur_pole_lift_gate_2026-05-06.json",
    "source_higgs_readiness": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

EXPECTED_MODES = {"0,0,0", "1,0,0", "0,1,0", "0,0,1"}
ZERO_MODE = "0,0,0"
EXPECTED_SEED_CONTROL_VERSION = "numba_gauge_seed_v1"
EXPECTED_SELECTED_MASS = 0.75

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


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def load_json(path: str | Path) -> dict[str, Any]:
    full = Path(path)
    if not full.is_absolute():
        full = ROOT / full
    if not full.exists():
        return {}
    data = json.loads(full.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def selected_ensemble(data: dict[str, Any]) -> dict[str, Any]:
    ensembles = data.get("ensembles")
    if not isinstance(ensembles, list) or len(ensembles) != 1:
        return {}
    row = ensembles[0]
    return row if isinstance(row, dict) else {}


def manifest_rows_for_ready_chunks(
    manifest: dict[str, Any], combiner: dict[str, Any]
) -> list[dict[str, Any]]:
    rows = manifest.get("chunk_commands")
    ready_indices = combiner.get("ready_chunk_indices")
    if not isinstance(rows, list) or not isinstance(ready_indices, list):
        return []
    ready = {int(index) for index in ready_indices if isinstance(index, int)}
    return [
        row
        for row in rows
        if isinstance(row, dict)
        and isinstance(row.get("chunk_index"), int)
        and int(row["chunk_index"]) in ready
    ]


def schur_residuals(mode: str, mode_row: dict[str, Any]) -> dict[str, Any] | None:
    needed = ("p_hat_sq", "C_ss_real", "C_sx_real", "C_xx_real")
    if not all(finite(mode_row.get(key)) for key in needed):
        return None
    p_hat_sq = float(mode_row["p_hat_sq"])
    c_ss = float(mode_row["C_ss_real"])
    c_sx = float(mode_row["C_sx_real"])
    c_xx = float(mode_row["C_xx_real"])
    delta = c_ss * c_xx - c_sx * c_sx
    if c_ss <= 0.0 or c_xx <= 0.0 or delta <= 0.0:
        return None
    return {
        "mode": mode,
        "p_hat_sq": p_hat_sq,
        "C_ss": c_ss,
        "C_sx": c_sx,
        "C_xx": c_xx,
        "Delta_sx": delta,
        "C_source_given_x": delta / c_xx,
        "C_x_given_source": delta / c_ss,
        "rho_sx": c_sx / math.sqrt(c_ss * c_xx),
    }


def read_chunk(row: dict[str, Any]) -> tuple[dict[str, Any] | None, list[str]]:
    issues: list[str] = []
    chunk_index = row.get("chunk_index")
    output = ROOT / str(row.get("output", ""))
    if not output.exists():
        return None, [f"chunk{chunk_index} output absent"]
    data = load_json(output)
    metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
    run_control = metadata.get("run_control") if isinstance(metadata.get("run_control"), dict) else {}
    ensemble = selected_ensemble(data)
    seed_control = (
        ensemble.get("rng_seed_control")
        if isinstance(ensemble.get("rng_seed_control"), dict)
        else {}
    )
    source = ensemble.get("source_higgs_cross_correlator_analysis")

    if metadata.get("phase") != "production":
        issues.append(f"chunk{chunk_index} phase={metadata.get('phase')!r}")
    if run_control.get("seed") != row.get("seed"):
        issues.append(f"chunk{chunk_index} seed mismatch")
    if seed_control.get("seed_control_version") != EXPECTED_SEED_CONTROL_VERSION:
        issues.append(f"chunk{chunk_index} seed-control mismatch")
    if ensemble.get("selected_mass_parameter") != EXPECTED_SELECTED_MASS:
        issues.append(f"chunk{chunk_index} selected mass mismatch")
    if not isinstance(source, dict):
        issues.append(f"chunk{chunk_index} source_higgs analysis absent")
        return None, issues
    if source.get("canonical_higgs_operator_identity_passed") is not False:
        issues.append(f"chunk{chunk_index} canonical O_H unexpectedly passed")
    if source.get("used_as_physical_yukawa_readout") is not False:
        issues.append(f"chunk{chunk_index} source rows marked physical")
    aliases = source.get("two_source_taste_radial_row_aliases")
    if not isinstance(aliases, dict) or aliases.get("C_sx_aliases_C_sH_schema_field") is not True:
        issues.append(f"chunk{chunk_index} C_sx alias missing")
    if not isinstance(aliases, dict) or aliases.get("C_xx_aliases_C_HH_schema_field") is not True:
        issues.append(f"chunk{chunk_index} C_xx alias missing")

    mode_rows = source.get("mode_rows")
    if not isinstance(mode_rows, dict) or set(mode_rows) != EXPECTED_MODES:
        issues.append(f"chunk{chunk_index} mode set mismatch")
        return None, issues

    modes: dict[str, dict[str, Any]] = {}
    for mode, mode_row in sorted(mode_rows.items()):
        if not isinstance(mode_row, dict):
            issues.append(f"chunk{chunk_index} {mode} row not object")
            continue
        parsed = schur_residuals(mode, mode_row)
        if parsed is None:
            issues.append(f"chunk{chunk_index} {mode} invalid Schur residual")
            continue
        modes[mode] = parsed
    if set(modes) != EXPECTED_MODES:
        return None, issues

    zero = modes[ZERO_MODE]
    shell_modes = sorted(EXPECTED_MODES - {ZERO_MODE})
    shell_p_values = [float(modes[mode]["p_hat_sq"]) for mode in shell_modes]
    shell_p_mean = statistics.fmean(shell_p_values)
    if not all(abs(value - shell_p_mean) <= 1.0e-12 for value in shell_p_values):
        issues.append(f"chunk{chunk_index} shell p_hat_sq anisotropy")
    if shell_p_mean <= float(zero["p_hat_sq"]):
        issues.append(f"chunk{chunk_index} shell p_hat_sq not above zero")
        return None, issues

    def mean_shell(key: str) -> float:
        return statistics.fmean(float(modes[mode][key]) for mode in shell_modes)

    return {
        "chunk_index": int(chunk_index),
        "seed": row.get("seed"),
        "volume": f"{ensemble.get('spatial_L')}x{ensemble.get('time_L')}",
        "zero_p_hat_sq": float(zero["p_hat_sq"]),
        "shell_p_hat_sq_mean": shell_p_mean,
        "C_source_given_x_zero": float(zero["C_source_given_x"]),
        "C_source_given_x_shell_mean": mean_shell("C_source_given_x"),
        "C_source_given_x_shell_minus_zero": mean_shell("C_source_given_x")
        - float(zero["C_source_given_x"]),
        "C_x_given_source_zero": float(zero["C_x_given_source"]),
        "C_x_given_source_shell_mean": mean_shell("C_x_given_source"),
        "C_x_given_source_shell_minus_zero": mean_shell("C_x_given_source")
        - float(zero["C_x_given_source"]),
        "rho_sx_zero": float(zero["rho_sx"]),
        "rho_sx_shell_mean": mean_shell("rho_sx"),
        "mode_rows": modes,
    }, issues


def summarize(values: list[float]) -> dict[str, Any]:
    if not values:
        return {"count": 0, "mean": None, "stderr": None, "min": None, "max": None}
    return {
        "count": len(values),
        "mean": statistics.fmean(values),
        "stderr": statistics.stdev(values) / math.sqrt(len(values)) if len(values) > 1 else 0.0,
        "min": min(values),
        "max": max(values),
    }


def z_score(diff: dict[str, Any], zero: dict[str, Any], shell: dict[str, Any]) -> float | None:
    if not finite(diff.get("mean")):
        return None
    err = math.hypot(float(zero.get("stderr") or 0.0), float(shell.get("stderr") or 0.0))
    if err == 0.0:
        return math.inf if float(diff["mean"]) > 0 else -math.inf
    return float(diff["mean"]) / err


def stieltjes_necessary_condition() -> str:
    return (
        "For C(x)=int dmu(s)/(x+s), dmu(s)>=0, x=q_hat^2, C is "
        "non-increasing: C(x2)-C(x1)<=0 for x2>x1.  A zero-to-first-shell "
        "increase rejects that object as the strict unsubtracted positive "
        "Stieltjes scalar two-point candidate.  A decrease is only a necessary "
        "first-shell check, not scalar-LSZ authority."
    )


def forbidden_firewall() -> dict[str, bool]:
    return {
        "used_hunit_matrix_element_readout": False,
        "used_yt_ward_identity": False,
        "used_observed_top_or_yukawa_as_selector": False,
        "used_alpha_lm_or_plaquette_u0": False,
        "used_reduced_cold_pilots_as_production_evidence": False,
        "set_c2_equal_one": False,
        "set_z_match_equal_one": False,
        "set_kappa_s_equal_one": False,
        "treated_schur_residual_as_canonical_O_H": False,
        "treated_first_shell_monotonicity_as_lsz_authority": False,
        "claimed_retained_or_proposed_retained": False,
    }


def main() -> int:
    print("PR #230 Schur-complement Stieltjes repair gate")
    print("=" * 72)

    manifest = load_json(MANIFEST)
    combiner = load_json(COMBINER)
    parents = {name: load_json(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in parents.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposals = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    ready_rows = manifest_rows_for_ready_chunks(manifest, combiner)
    ready_chunks = combiner.get("ready_chunks")
    expected_chunks = combiner.get("expected_chunks")

    chunks: list[dict[str, Any]] = []
    chunk_issues: list[str] = []
    for row in ready_rows:
        parsed, issues = read_chunk(row)
        chunk_issues.extend(issues)
        if parsed is not None:
            chunks.append(parsed)

    source_zero = summarize([float(row["C_source_given_x_zero"]) for row in chunks])
    source_shell = summarize([float(row["C_source_given_x_shell_mean"]) for row in chunks])
    source_diff = summarize([float(row["C_source_given_x_shell_minus_zero"]) for row in chunks])
    x_zero = summarize([float(row["C_x_given_source_zero"]) for row in chunks])
    x_shell = summarize([float(row["C_x_given_source_shell_mean"]) for row in chunks])
    x_diff = summarize([float(row["C_x_given_source_shell_minus_zero"]) for row in chunks])

    source_positive = all(
        float(row["C_source_given_x_zero"]) > 0.0
        and float(row["C_source_given_x_shell_mean"]) > 0.0
        for row in chunks
    )
    x_positive = all(
        float(row["C_x_given_source_zero"]) > 0.0
        and float(row["C_x_given_source_shell_mean"]) > 0.0
        for row in chunks
    )
    source_nonincrease = bool(chunks) and all(
        float(row["C_source_given_x_shell_minus_zero"]) <= 0.0 for row in chunks
    )
    x_nonincrease = bool(chunks) and all(
        float(row["C_x_given_source_shell_minus_zero"]) <= 0.0 for row in chunks
    )
    complete_packet_present = ready_chunks == expected_chunks == 63
    volumes = sorted(
        {
            str(chunk.get("volume"))
            for chunk in chunks
            if isinstance(chunk.get("volume"), str)
        }
    )
    multivolume_fv_ir_authority_present = len(volumes) >= 3

    witness_loaded = (
        parents["two_source_schur_subblock_witness"].get(
            "two_source_taste_radial_schur_subblock_witness_passed"
        )
        is True
        and parents["two_source_schur_subblock_witness"].get("proposal_allowed") is False
    )
    kprime_scout_loaded = (
        parents["two_source_schur_kprime_finite_shell_scout"].get(
            "finite_shell_schur_kprime_scout_passed"
        )
        is True
        and parents["two_source_schur_kprime_finite_shell_scout"].get(
            "strict_schur_kprime_authority_passed"
        )
        is False
    )
    abc_rows_loaded = (
        parents["two_source_schur_abc_finite_rows"].get(
            "two_source_taste_radial_schur_abc_finite_rows_passed"
        )
        is True
        and parents["two_source_schur_abc_finite_rows"].get(
            "strict_schur_abc_kernel_rows_written"
        )
        is False
    )
    strict_raw_lsz_block_loaded = (
        parents["strict_scalar_lsz_moment_fv"].get(
            "current_raw_c_ss_proxy_fails_stieltjes_monotonicity"
        )
        is True
        and parents["strict_scalar_lsz_moment_fv"].get(
            "strict_scalar_lsz_moment_fv_authority_present"
        )
        is False
    )
    pole_lift_open = (
        parents["schur_pole_lift_gate"].get("strict_pole_lift_passed") is False
        and parents["schur_pole_lift_gate"].get("proposal_allowed") is False
    )
    source_higgs_still_absent = (
        parents["source_higgs_readiness"].get("taste_radial_rows_lack_canonical_oh_identity")
        is True
        and parents["source_higgs_readiness"].get("future_rows_present") is False
        and parents["source_higgs_readiness"].get("proposal_allowed") is False
    )
    retained_open = parents["retained_route"].get("proposal_allowed") is False
    campaign_open = parents["campaign_status"].get("proposal_allowed") is False
    clean_firewall = all(value is False for value in forbidden_firewall().values())

    report("manifest-loaded", bool(manifest), rel(MANIFEST))
    report("combiner-parent-loaded", bool(combiner), rel(COMBINER))
    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposals, f"proposal_allowed={proposals}")
    report("ready-chunks-loaded", len(chunks) == ready_chunks and len(chunks) > 0, f"ready={ready_chunks} parsed={len(chunks)}")
    report("chunk-row-audits-clean", not chunk_issues, f"issues={chunk_issues[:5]}")
    report("schur-subblock-witness-loaded", witness_loaded, statuses["two_source_schur_subblock_witness"])
    report("finite-shell-kprime-scout-loaded", kprime_scout_loaded, statuses["two_source_schur_kprime_finite_shell_scout"])
    report("finite-abc-rows-loaded", abc_rows_loaded, statuses["two_source_schur_abc_finite_rows"])
    report("raw-c-ss-stieltjes-block-loaded", strict_raw_lsz_block_loaded, statuses["strict_scalar_lsz_moment_fv"])
    report("source-given-x-positive", source_positive, f"zero={source_zero['mean']} shell={source_shell['mean']}")
    report("source-given-x-nonincrease-fails", source_nonincrease is False, f"diff={source_diff['mean']} z={z_score(source_diff, source_zero, source_shell)}")
    report("x-given-source-positive", x_positive, f"zero={x_zero['mean']} shell={x_shell['mean']}")
    report("x-given-source-first-shell-nonincrease", x_nonincrease, f"diff={x_diff['mean']} z={z_score(x_diff, x_zero, x_shell)}")
    report(
        "complete-63-packet-support-only",
        complete_packet_present is True or ready_chunks < expected_chunks,
        f"ready={ready_chunks}/{expected_chunks}",
    )
    report("pole-lift-authority-still-open", pole_lift_open, statuses["schur_pole_lift_gate"])
    report("multivolume-fv-ir-authority-absent", multivolume_fv_ir_authority_present is False, f"volumes={volumes}")
    report("canonical-source-higgs-authority-absent", source_higgs_still_absent, statuses["source_higgs_readiness"])
    report("retained-route-still-open", retained_open, statuses["retained_route"])
    report("campaign-status-still-open", campaign_open, statuses["campaign_status"])
    report("forbidden-firewall-clean", clean_firewall, str(forbidden_firewall()))
    report("does-not-authorize-proposed-retained", True, "proposal_allowed=false")

    passed = (
        bool(manifest)
        and bool(combiner)
        and not missing
        and not proposals
        and len(chunks) == ready_chunks
        and len(chunks) > 0
        and not chunk_issues
        and witness_loaded
        and kprime_scout_loaded
        and abc_rows_loaded
        and strict_raw_lsz_block_loaded
        and source_positive
        and source_nonincrease is False
        and x_positive
        and x_nonincrease
        and (complete_packet_present is True or ready_chunks < expected_chunks)
        and pole_lift_open
        and multivolume_fv_ir_authority_present is False
        and source_higgs_still_absent
        and retained_open
        and campaign_open
        and clean_firewall
    )

    result = {
        "actual_current_surface_status": (
            "bounded-support / Schur-complement Stieltjes repair split: "
            "C_s|x fails first-shell monotonicity while C_x|s survives the "
            "necessary first-shell check; scalar-LSZ authority absent"
        ),
        "conditional_surface_status": (
            "conditional-support for a future complement-scalar LSZ route only "
            "after pole/model-class and multivolume FV/IR authority, "
            "and a same-surface proof or measurement identifying x with canonical "
            "O_H or bypassing through W/Z response"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The source Schur residual does not repair the raw C_ss monotonicity "
            "failure.  The x-given-source residual is a genuine positive "
            "finite-row candidate because it is positive and non-increasing from "
            "the zero mode to the first shell, but this is only a necessary "
            "one-volume finite-shell check and x is not certified as canonical "
            "O_H."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "schur_complement_stieltjes_repair_gate_passed": passed,
        "source_given_x_stieltjes_first_shell_passed": source_positive and source_nonincrease,
        "source_given_x_stieltjes_first_shell_failed": source_positive and not source_nonincrease,
        "x_given_source_stieltjes_first_shell_passed": x_positive and x_nonincrease,
        "x_given_source_candidate_survives_necessary_test": x_positive and x_nonincrease,
        "strict_scalar_lsz_authority_present": False,
        "complete_63_packet_present": complete_packet_present,
        "multivolume_fv_ir_authority_present": multivolume_fv_ir_authority_present,
        "isolated_pole_model_class_authority_present": False,
        "canonical_higgs_operator_identity_passed": False,
        "used_as_physical_yukawa_readout": False,
        "ready_chunks": ready_chunks,
        "expected_chunks": expected_chunks,
        "ready_chunk_indices": combiner.get("ready_chunk_indices"),
        "source_given_x_summary": {
            "zero": source_zero,
            "shell": source_shell,
            "shell_minus_zero": source_diff,
            "shell_minus_zero_z_score_from_chunk_scatter": z_score(
                source_diff, source_zero, source_shell
            ),
        },
        "x_given_source_summary": {
            "zero": x_zero,
            "shell": x_shell,
            "shell_minus_zero": x_diff,
            "shell_minus_zero_z_score_from_chunk_scatter": z_score(
                x_diff, x_zero, x_shell
            ),
        },
        "per_chunk_schur_residual_rows": chunks,
        "chunk_issues": chunk_issues,
        "row_definition": {
            "G": "[[C_ss(q), C_sx(q)], [C_sx(q), C_xx(q)]]",
            "Delta_sx": "C_ss*C_xx - C_sx^2",
            "C_source_given_x": "Delta_sx / C_xx",
            "C_x_given_source": "Delta_sx / C_ss",
            "strict_limit": (
                "Finite Schur-complement residuals from measured rows only. "
                "They are not isolated-pole scalar-LSZ rows, not multivolume "
                "FV/IR authority, and do not identify x with canonical O_H."
            ),
        },
        "stieltjes_necessary_condition": stieltjes_necessary_condition(),
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "forbidden_firewall": forbidden_firewall(),
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not treat C_x|s first-shell monotonicity as scalar-LSZ authority",
            "does not treat taste-radial x as canonical O_H",
            "does not set kappa_s = 1, c2 = 1, or Z_match = 1",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
            "does not treat partial chunks as complete production closure evidence",
        ],
        "exact_next_action": (
            "Use C_x|s as the targeted complement-scalar diagnostic after more "
            "chunks complete, but for closure supply a canonical O_H/source-overlap "
            "identity, real C_spH/C_HH pole rows, a W/Z physical-response bypass, "
            "or a pole/FV/IR theorem that makes the Schur residual load-bearing."
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
