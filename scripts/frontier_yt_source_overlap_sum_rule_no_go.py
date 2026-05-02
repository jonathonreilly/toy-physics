#!/usr/bin/env python3
"""
PR #230 source-overlap spectral sum-rule no-go.

This runner tests the adjacent shortcut after the D17 identity attempt: whether
finite positive spectral/moment sum rules for the same-source scalar two-point
function can fix the source-pole residue <0|O_s|h>^2.  They cannot.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import linprog


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_source_overlap_sum_rule_no_go_2026-05-02.json"

CERTS = {
    "d17_source_pole_identity": "outputs/yt_d17_source_pole_identity_closure_attempt_2026-05-02.json",
    "same_source_two_point": "outputs/yt_same_source_scalar_two_point_lsz_measurement_2026-05-01.json",
    "finite_shell_identifiability": "outputs/yt_fh_lsz_finite_shell_identifiability_no_go_2026-05-02.json",
    "stieltjes_model_class": "outputs/yt_fh_lsz_stieltjes_model_class_obstruction_2026-05-02.json",
    "pole_saturation_threshold_gate": "outputs/yt_fh_lsz_pole_saturation_threshold_gate_2026-05-02.json",
    "scalar_contact_scheme": "outputs/yt_scalar_source_contact_term_scheme_boundary_2026-05-01.json",
    "scalar_renorm_overlap": "outputs/yt_scalar_renormalization_condition_overlap_no_go_2026-05-01.json",
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


def load_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def solve_positive_moment_family() -> dict[str, Any]:
    pole_x = 0.25
    continuum_x = np.asarray([0.27, 0.32, 0.45, 0.7, 1.0, 1.5, 2.5, 4.0], dtype=float)
    base_residue = 1.0
    base_weights = np.asarray([4.0, 3.0, 3.0, 2.0, 2.0, 1.0, 1.0, 1.0], dtype=float)
    moment_count = 4
    powers = np.arange(moment_count, dtype=float)
    continuum_matrix = np.vstack([continuum_x**k for k in powers])
    pole_moments = np.asarray([pole_x**k for k in powers], dtype=float)
    target_moments = base_residue * pole_moments + continuum_matrix @ base_weights

    residues = [0.2, 0.5, 1.0, 1.5, 2.0]
    models: list[dict[str, Any]] = []
    for residue in residues:
        rhs = target_moments - residue * pole_moments
        result = linprog(
            c=np.zeros(len(continuum_x)),
            A_eq=continuum_matrix,
            b_eq=rhs,
            bounds=[(0.0, None)] * len(continuum_x),
            method="highs",
        )
        if not result.success:
            models.append({"pole_residue": residue, "success": False, "message": result.message})
            continue
        fitted = residue * pole_moments + continuum_matrix @ result.x
        models.append(
            {
                "pole_residue": residue,
                "success": True,
                "continuum_weights": [float(x) for x in result.x],
                "min_continuum_weight": float(np.min(result.x)),
                "max_abs_moment_residual": float(np.max(np.abs(fitted - target_moments))),
                "source_overlap_z_s": float(math.sqrt(residue)),
                "relative_y_proxy_for_fixed_dE_ds": float(1.0 / math.sqrt(residue)),
            }
        )

    successful = [model for model in models if model.get("success")]
    residues_success = [float(model["pole_residue"]) for model in successful]
    y_proxies = [float(model["relative_y_proxy_for_fixed_dE_ds"]) for model in successful]
    residuals = [float(model["max_abs_moment_residual"]) for model in successful]
    return {
        "pole_location_x": pole_x,
        "continuum_support_x": [float(x) for x in continuum_x],
        "moment_count": moment_count,
        "target_moments": [float(x) for x in target_moments],
        "models": models,
        "checks": {
            "all_models_positive": len(successful) == len(models)
            and all(float(model.get("min_continuum_weight", -1.0)) >= -1.0e-12 for model in successful),
            "max_abs_moment_residual": max(residuals) if residuals else float("inf"),
            "pole_residue_span_factor": max(residues_success) / min(residues_success)
            if residues_success
            else float("nan"),
            "y_proxy_span_factor": max(y_proxies) / min(y_proxies) if y_proxies else float("nan"),
        },
    }


def main() -> int:
    print("PR #230 source-overlap spectral sum-rule no-go")
    print("=" * 72)

    certs = {name: load_json(path) for name, path in CERTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    family = solve_positive_moment_family()
    checks = family["checks"]

    d17_identity_blocked = (
        "D17 source-pole identity closure attempt blocked"
        in status(certs["d17_source_pole_identity"])
        and certs["d17_source_pole_identity"].get("theorem_closed") is False
    )
    same_source_support_only = (
        "same-source scalar two-point" in status(certs["same_source_two_point"])
        and certs["same_source_two_point"].get("proposal_allowed") is False
    )
    finite_shell_blocked = (
        "finite-shell pole-fit identifiability no-go" in status(certs["finite_shell_identifiability"])
        and certs["finite_shell_identifiability"].get("proposal_allowed") is False
    )
    stieltjes_blocked = (
        "Stieltjes model-class obstruction" in status(certs["stieltjes_model_class"])
        and certs["stieltjes_model_class"].get("proposal_allowed") is False
    )
    threshold_gate_blocks = (
        "pole-saturation threshold gate" in status(certs["pole_saturation_threshold_gate"])
        and certs["pole_saturation_threshold_gate"].get("pole_saturation_threshold_gate_passed") is False
    )
    scheme_shortcuts_blocked = (
        "source contact-term scheme boundary" in status(certs["scalar_contact_scheme"])
        and "renormalization-condition source-overlap no-go" in status(certs["scalar_renorm_overlap"])
        and certs["scalar_contact_scheme"].get("proposal_allowed") is False
        and certs["scalar_renorm_overlap"].get("proposal_allowed") is False
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("d17-identity-still-blocked", d17_identity_blocked, status(certs["d17_source_pole_identity"]))
    report("same-source-two-point-support-only", same_source_support_only, status(certs["same_source_two_point"]))
    report("finite-shell-and-stieltjes-blocked", finite_shell_blocked and stieltjes_blocked, "finite shell positivity is not enough")
    report("threshold-gate-still-blocks", threshold_gate_blocks, status(certs["pole_saturation_threshold_gate"]))
    report("renorm-contact-shortcuts-blocked", scheme_shortcuts_blocked, "scheme choices do not fix pole residue")
    report("positive-moment-family-constructed", checks["all_models_positive"], f"residue_span={checks['pole_residue_span_factor']}")
    report("finite-moments-held-fixed", checks["max_abs_moment_residual"] < 1e-10, f"max_residual={checks['max_abs_moment_residual']:.3e}")
    report("pole-residue-not-fixed-by-sum-rules", checks["pole_residue_span_factor"] >= 10.0, f"span={checks['pole_residue_span_factor']:.6g}")
    report("physical-y-proxy-varies", checks["y_proxy_span_factor"] >= 3.0, f"span={checks['y_proxy_span_factor']:.6g}")
    report("does-not-authorize-retained-proposal", True, "finite moment/sum-rule data are not LSZ source normalization")

    result = {
        "actual_current_surface_status": "exact negative boundary / source-overlap spectral sum-rule no-go",
        "verdict": (
            "Finite positive spectral/moment sum rules for the same-source "
            "scalar two-point function do not fix the source-pole residue.  A "
            "positive pole-plus-continuum family can keep the first four "
            "moments exactly fixed while changing the pole residue by a factor "
            "of ten.  Therefore moment or curvature sum rules cannot replace "
            "a microscopic scalar denominator theorem, pole-saturation/"
            "threshold certificate, or production pole-residue measurement."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Finite spectral sum rules leave the source-pole residue underdetermined.",
        "parent_certificates": CERTS,
        "moment_family": family,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not set kappa_s = 1",
            "does not use H_unit matrix-element readout or yt_ward_identity",
            "does not use observed top mass, observed y_t, alpha_LM, plaquette, u0, c2 = 1, or Z_match = 1",
            "does not infer pole saturation from finite spectral moments",
        ],
        "exact_next_action": (
            "Move to a microscopic scalar denominator / threshold theorem, or "
            "wait for seed-controlled production data and apply the pole-fit "
            "model-class/FV/IR/Higgs-identity gates."
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
