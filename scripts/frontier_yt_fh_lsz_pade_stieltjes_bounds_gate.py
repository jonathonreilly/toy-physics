#!/usr/bin/env python3
"""
PR #230 FH/LSZ Pade-Stieltjes bounds gate.

This runner attacks the scalar-LSZ non-chunk route directly: can finite
Stieltjes/Pade moment theory replace the month-scale pole-fit compute?

The answer is a bounded yes/no:

* yes, a same-surface Stieltjes moment sequence plus an isolated scalar pole,
  a certified threshold gap, and FV/IR authority would give a strict
  positive-residue interval without using observed y_t;
* no, the current PR #230 surface does not contain those inputs, and finite
  source/shell rows cannot be silently reinterpreted as Pade moment bounds.

The gate therefore adds a positive future contract and keeps the actual
current surface open.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import linprog


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_pade_stieltjes_bounds_gate_2026-05-05.json"
FUTURE_CERTIFICATE = (
    ROOT / "outputs" / "yt_fh_lsz_pade_stieltjes_bounds_certificate_2026-05-05.json"
)

PARENTS = {
    "stieltjes_moment_gate": "outputs/yt_fh_lsz_stieltjes_moment_certificate_gate_2026-05-05.json",
    "pole_saturation_threshold": "outputs/yt_fh_lsz_pole_saturation_threshold_gate_2026-05-02.json",
    "threshold_authority": "outputs/yt_fh_lsz_threshold_authority_import_audit_2026-05-02.json",
    "finite_volume_obstruction": (
        "outputs/yt_fh_lsz_finite_volume_pole_saturation_obstruction_2026-05-02.json"
    ),
    "soft_continuum_no_go": "outputs/yt_fh_lsz_soft_continuum_threshold_no_go_2026-05-02.json",
    "scalar_denominator_attempt": "outputs/yt_scalar_denominator_theorem_closure_attempt_2026-05-02.json",
}

FORBIDDEN_TEXT_FRAGMENTS = (
    "H_unit",
    "yt_ward_identity",
    "YT_WARD_IDENTITY_DERIVATION_THEOREM",
    "alpha_LM",
    "plaquette",
    "u0",
    "observed top mass",
    "observed y_t",
    "PDG selector",
    "kappa_s = 1",
    "c2 = 1",
    "Z_match = 1",
)

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


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def string_values(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        out: list[str] = []
        for child in value.values():
            out.extend(string_values(child))
        return out
    if isinstance(value, list):
        out = []
        for child in value:
            out.extend(string_values(child))
        return out
    return []


def forbidden_fragment_present(candidate: dict[str, Any]) -> list[str]:
    encoded_values = "\n".join(string_values(candidate))
    return [fragment for fragment in FORBIDDEN_TEXT_FRAGMENTS if fragment in encoded_values]


def stieltjes_moments(
    pole_residue: float,
    pole_mass_squared: float,
    continuum_mass_squared: np.ndarray,
    continuum_weights: np.ndarray,
    nmax: int,
) -> np.ndarray:
    moments = []
    for n in range(nmax + 1):
        pole_term = pole_residue / pole_mass_squared ** (n + 1)
        continuum_term = float(
            np.sum(continuum_weights / continuum_mass_squared ** (n + 1))
        )
        moments.append(pole_term + continuum_term)
    return np.asarray(moments, dtype=float)


def residue_interval_from_moments(
    moments: np.ndarray,
    pole_mass_squared: float,
    continuum_grid: np.ndarray,
) -> dict[str, Any]:
    orders = np.arange(len(moments), dtype=float)
    pole_column = 1.0 / pole_mass_squared ** (orders + 1.0)
    continuum_matrix = np.asarray(
        [
            [1.0 / mass_squared ** (n + 1.0) for mass_squared in continuum_grid]
            for n in orders
        ],
        dtype=float,
    )
    matrix = np.column_stack([pole_column, continuum_matrix])
    bounds = [(0.0, None)] * matrix.shape[1]
    min_result = linprog(
        c=np.r_[1.0, np.zeros(len(continuum_grid))],
        A_eq=matrix,
        b_eq=moments,
        bounds=bounds,
        method="highs",
    )
    max_result = linprog(
        c=np.r_[-1.0, np.zeros(len(continuum_grid))],
        A_eq=matrix,
        b_eq=moments,
        bounds=bounds,
        method="highs",
    )
    if not min_result.success or not max_result.success:
        return {
            "feasible": False,
            "min_message": min_result.message,
            "max_message": max_result.message,
        }
    lower = float(min_result.fun)
    upper = float(-max_result.fun)
    if lower > 0.0:
        relative_width = float((upper - lower) / lower)
        y_proxy_span = float(np.sqrt(upper / lower))
    else:
        relative_width = None
        y_proxy_span = None
    return {
        "feasible": True,
        "residue_lower": lower,
        "residue_upper": upper,
        "lower_bound_positive": lower > 1.0e-12,
        "relative_width_over_lower": relative_width,
        "y_proxy_span_factor": y_proxy_span,
    }


def build_pade_stieltjes_scan() -> dict[str, Any]:
    pole_mass_squared = 0.25
    true_pole_residue = 1.0
    moment_orders = [3, 5, 7, 9]
    gap_rows: list[dict[str, Any]] = []

    for threshold_gap in [0.001, 0.01, 0.10, 0.50]:
        continuum_mass_squared = np.asarray(
            [
                pole_mass_squared + threshold_gap,
                pole_mass_squared + 3.0 * threshold_gap,
                1.0,
                2.0,
                4.0,
                8.0,
            ],
            dtype=float,
        )
        continuum_weights = np.full(len(continuum_mass_squared), 0.30, dtype=float)
        continuum_grid = np.unique(
            np.r_[continuum_mass_squared, np.linspace(pole_mass_squared + threshold_gap, 16.0, 80)]
        )
        rows = []
        for nmax in moment_orders:
            moments = stieltjes_moments(
                true_pole_residue,
                pole_mass_squared,
                continuum_mass_squared,
                continuum_weights,
                nmax,
            )
            interval = residue_interval_from_moments(
                moments,
                pole_mass_squared,
                continuum_grid,
            )
            rows.append(
                {
                    "moment_order_nmax": nmax,
                    "moment_count": nmax + 1,
                    **interval,
                }
            )
        gap_rows.append(
            {
                "threshold_gap_m2": threshold_gap,
                "continuum_grid_size": int(len(continuum_grid)),
                "rows": rows,
            }
        )

    separated_tight_rows = [
        row
        for group in gap_rows
        if group["threshold_gap_m2"] >= 0.10
        for row in group["rows"]
        if row.get("feasible")
        and row.get("lower_bound_positive")
        and float(row.get("relative_width_over_lower", 1.0)) <= 0.02
    ]
    near_threshold_broad_rows = [
        row
        for group in gap_rows
        if group["threshold_gap_m2"] <= 0.001
        for row in group["rows"]
        if row.get("feasible")
        and (
            row.get("relative_width_over_lower") is None
            or float(row.get("relative_width_over_lower", 0.0)) > 1.0
        )
    ]

    return {
        "theorem_boundary": (
            "For a positive Stieltjes scalar correlator with certified pole "
            "mass, positive moments, threshold gap, and FV/IR authority, the "
            "truncated moment problem gives Markov/Pade-style upper and lower "
            "bounds on the pole residue.  A tight interval can serve as a "
            "non-MC scalar-LSZ certificate.  Without a certified gap or moment "
            "sequence, the same formalism leaves broad positive-residue "
            "families and cannot identify y_t."
        ),
        "pole_mass_squared": pole_mass_squared,
        "true_pole_residue_for_witness": true_pole_residue,
        "gap_rows": gap_rows,
        "separated_gap_has_tight_rows": bool(separated_tight_rows),
        "near_threshold_has_broad_rows": bool(near_threshold_broad_rows),
        "tight_row_examples": separated_tight_rows[:3],
        "broad_row_examples": near_threshold_broad_rows[:3],
    }


def validate_future_certificate(candidate: dict[str, Any]) -> dict[str, bool]:
    firewall = candidate.get("firewall", {}) if isinstance(candidate.get("firewall"), dict) else {}
    residue_interval = (
        candidate.get("residue_interval", {})
        if isinstance(candidate.get("residue_interval"), dict)
        else {}
    )
    return {
        "certificate_kind": candidate.get("certificate_kind")
        == "fh_lsz_pade_stieltjes_bounds_certificate",
        "same_surface_cl3_z3": candidate.get("same_surface_cl3_z3") is True,
        "moment_certificate_gate_passed": candidate.get("moment_certificate_gate_passed") is True,
        "moment_count_sufficient": int(candidate.get("moment_count", 0) or 0) >= 6,
        "pole_location_certified": candidate.get("pole_location_certified") is True,
        "threshold_gap_certified": candidate.get("threshold_gap_certified") is True,
        "fv_ir_control_certified": candidate.get("fv_ir_control_certified") is True,
        "residue_interval_tight": (
            residue_interval.get("lower_bound_positive") is True
            and float(residue_interval.get("relative_width_over_lower", 1.0) or 1.0) <= 0.02
        ),
        "analytic_continuation_or_denominator_authority": candidate.get(
            "analytic_continuation_or_denominator_authority"
        )
        is True,
        "no_observed_selector": firewall.get("used_observed_targets_as_selectors") is False,
        "no_hunit_or_ward_authority": firewall.get("used_hunit_or_ward_authority") is False,
        "no_alpha_lm_or_plaquette": firewall.get("used_alpha_lm_or_plaquette") is False,
        "no_unit_shortcut": firewall.get("set_kappa_c2_zmatch_equal_one") is False,
        "no_forbidden_text_fragments": not forbidden_fragment_present(candidate),
    }


def main() -> int:
    print("PR #230 FH/LSZ Pade-Stieltjes bounds gate")
    print("=" * 72)

    parents = {name: load_json(ROOT / rel) for name, rel in PARENTS.items()}
    missing_parents = [name for name, cert in parents.items() if not cert]
    statuses = {name: status(cert) for name, cert in parents.items()}
    scan = build_pade_stieltjes_scan()
    future = load_json(FUTURE_CERTIFICATE)
    future_checks = validate_future_certificate(future) if future else {}
    failed_future_checks = [name for name, ok in future_checks.items() if not ok]
    future_gate_passed = bool(future) and not failed_future_checks

    report("parents-loaded", not missing_parents, f"missing={missing_parents}")
    report(
        "moment-certificate-gate-currently-absent",
        parents["stieltjes_moment_gate"].get("moment_certificate_gate_passed") is False,
        statuses["stieltjes_moment_gate"],
    )
    report(
        "threshold-authority-currently-absent",
        parents["threshold_authority"].get("proposal_allowed") is False,
        statuses["threshold_authority"],
    )
    report(
        "scalar-denominator-theorem-currently-open",
        parents["scalar_denominator_attempt"].get("theorem_closed") is False,
        statuses["scalar_denominator_attempt"],
    )
    report(
        "pade-stieltjes-positive-contract-demonstrated",
        scan["separated_gap_has_tight_rows"],
        "separated threshold + enough moments produces tight positive residue bounds",
    )
    report(
        "near-threshold-finite-moments-broad",
        scan["near_threshold_has_broad_rows"],
        "finite moments are broad when continuum can approach the pole",
    )
    report(
        "future-pade-stieltjes-certificate-absent",
        not future,
        str(FUTURE_CERTIFICATE.relative_to(ROOT)),
    )
    if future:
        report(
            "future-pade-stieltjes-certificate-valid",
            future_gate_passed,
            f"failed={failed_future_checks}",
        )
    report(
        "current-surface-does-not-close-scalar-lsz",
        not future_gate_passed,
        f"future_gate_passed={future_gate_passed}",
    )
    report("does-not-authorize-proposed-retained", True, "Pade/Stieltjes bounds are a future contract only")

    result = {
        "actual_current_surface_status": (
            "exact-support / FH-LSZ Pade-Stieltjes bounds gate; strict "
            "moment-threshold certificate absent"
        ),
        "verdict": (
            "The non-chunk scalar-LSZ bypass is now sharply characterized.  "
            "Pade/Stieltjes moment bounds can in principle certify a pole "
            "residue from same-surface data, but only with positive moment "
            "authority, an isolated pole, a certified threshold gap, FV/IR "
            "control, and a tight positive residue interval.  The current "
            "PR230 surface has none of those strict future inputs, so the route "
            "is exact support rather than closure."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "No same-surface Pade/Stieltjes bounds certificate is present; "
            "finite source/shell rows cannot be promoted to scalar-LSZ residue evidence."
        ),
        "bare_retained_allowed": False,
        "pade_stieltjes_bounds_gate_passed": future_gate_passed,
        "future_certificate": str(FUTURE_CERTIFICATE.relative_to(ROOT)),
        "future_certificate_checks": future_checks,
        "future_certificate_missing_or_failed_checks": failed_future_checks,
        "parent_certificates": PARENTS,
        "pade_stieltjes_scan": scan,
        "acceptance_contract": {
            "certificate_kind": "fh_lsz_pade_stieltjes_bounds_certificate",
            "required_fields": [
                "same_surface_cl3_z3",
                "moment_certificate_gate_passed",
                "moment_count >= 6",
                "pole_location_certified",
                "threshold_gap_certified",
                "fv_ir_control_certified",
                "residue_interval.lower_bound_positive",
                "residue_interval.relative_width_over_lower <= 0.02",
                "analytic_continuation_or_denominator_authority",
                "firewall.used_observed_targets_as_selectors == false",
                "firewall.used_hunit_or_ward_authority == false",
                "firewall.used_alpha_lm_or_plaquette == false",
                "firewall.set_kappa_c2_zmatch_equal_one == false",
            ],
            "allowed_positive_route": (
                "strict same-surface Stieltjes moments plus threshold/FV/IR "
                "authority; not a fit to observed y_t or a unit-normalization shortcut"
            ),
        },
        "strict_non_claims": [
            "does not claim scalar-LSZ closure",
            "does not infer Pade bounds from finite source/shell rows without moments",
            "does not define y_t_bare",
            "does not use H_unit, Ward authority, alpha_LM, plaquette, u0, observed targets, or unit shortcuts",
        ],
        "exact_next_action": (
            "Either produce the strict Pade/Stieltjes bounds certificate from "
            "same-surface scalar data, derive the microscopic scalar denominator "
            "theorem that implies it, or continue production chunks until the "
            "postprocessor can emit a certified moment/threshold/FV package."
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
