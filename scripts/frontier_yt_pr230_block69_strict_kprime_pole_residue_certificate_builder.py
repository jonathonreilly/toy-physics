#!/usr/bin/env python3
"""
PR #230 Block69 strict K-prime pole-residue certificate builder.

This runner is deliberately narrow.  It tries to validate an explicit
Schur/Feshbach K'(pole) row artifact and build the same-source pole-residue
certificate.  If the required rows are absent, it writes the exact row
emissions contract needed from chunk/combiner/theorem code.  It does not scan
for alternative routes and it does not infer K'(pole) from source-only
finite-shell C_ss rows.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "outputs" / "yt_pr230_strict_kprime_pole_residue_certificate_2026-05-12.json"

DEFAULT_ROW_INPUTS = [
    ROOT / "outputs" / "yt_pr230_block69_strict_kprime_pole_residue_rows_2026-05-12.json",
    ROOT / "outputs" / "yt_pr230_strict_kprime_pole_residue_rows_2026-05-12.json",
    ROOT / "outputs" / "yt_schur_kprime_pole_residue_rows_2026-05-12.json",
    ROOT / "outputs" / "yt_pr230_schur_scalar_kernel_rows_2026-05-12.json",
    ROOT / "outputs" / "yt_schur_scalar_kernel_rows_2026-05-03.json",
]

PARENTS = {
    "schur_kprime_sufficiency": "outputs/yt_schur_complement_kprime_sufficiency_2026-05-03.json",
    "schur_kernel_row_contract_gate": "outputs/yt_schur_kernel_row_contract_gate_2026-05-03.json",
    "schur_kprime_row_absence_guard": "outputs/yt_schur_kprime_row_absence_guard_2026-05-03.json",
    "schur_row_candidate_extraction": "outputs/yt_schur_row_candidate_extraction_attempt_2026-05-03.json",
    "fh_lsz_polefit8x8_postprocessor": "outputs/yt_fh_lsz_polefit8x8_postprocessor_2026-05-04.json",
    "full_positive_assembly_gate": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
}

FORBIDDEN_FIREWALL_FIELDS = {
    "used_H_unit": ("used_H_unit", "used_hunit", "used_hunit_matrix_element_readout"),
    "used_yt_ward_identity": ("used_yt_ward_identity", "used_prior_ward_authority"),
    "used_y_t_bare": ("used_y_t_bare", "used_yt_bare", "used_yukawa_bare"),
    "used_alpha_LM": ("used_alpha_LM", "used_alpha_lm", "used_alpha_lm_or_plaquette_u0"),
    "used_plaquette_u0": (
        "used_plaquette_u0",
        "used_plaquette",
        "used_u0",
        "used_alpha_lm_or_plaquette_u0",
    ),
    "used_observed_target_selectors": (
        "used_observed_target_selectors",
        "used_observed_targets_as_selectors",
        "used_observed_top_or_yukawa_as_selector",
    ),
    "used_alias_imports": ("used_alias_imports", "used_alias_import", "used_alias_surface_imports"),
}

PASS_COUNT = 0
FAIL_COUNT = 0


Interval = tuple[float, float]


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
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def interval_from_any(value: Any) -> Interval | None:
    if finite(value):
        point = float(value)
        return (point, point)
    if isinstance(value, list) and len(value) == 2 and finite(value[0]) and finite(value[1]):
        lo = float(value[0])
        hi = float(value[1])
        return (min(lo, hi), max(lo, hi))
    if isinstance(value, dict):
        for lo_key, hi_key in (
            ("lower", "upper"),
            ("lo", "hi"),
            ("min", "max"),
            ("left", "right"),
            ("low", "high"),
        ):
            if finite(value.get(lo_key)) and finite(value.get(hi_key)):
                lo = float(value[lo_key])
                hi = float(value[hi_key])
                return (min(lo, hi), max(lo, hi))
        if finite(value.get("value")):
            center = float(value["value"])
            if finite(value.get("err")):
                err = abs(float(value["err"]))
                return (center - err, center + err)
            if finite(value.get("stderr")):
                err = abs(float(value["stderr"]))
                return (center - err, center + err)
            return (center, center)
    return None


def get_interval(row: dict[str, Any], *names: str) -> Interval | None:
    for name in names:
        for key in (f"{name}_interval", f"{name}_bounds", name):
            if key in row:
                interval = interval_from_any(row[key])
                if interval is not None:
                    return interval
        if name in row and finite(row.get(f"{name}_err")):
            center = float(row[name])
            err = abs(float(row[f"{name}_err"]))
            return (center - err, center + err)
    return None


def interval_add(a: Interval, b: Interval) -> Interval:
    return (a[0] + b[0], a[1] + b[1])


def interval_neg(a: Interval) -> Interval:
    return (-a[1], -a[0])


def interval_sub(a: Interval, b: Interval) -> Interval:
    return interval_add(a, interval_neg(b))


def interval_mul(a: Interval, b: Interval) -> Interval:
    products = (a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1])
    return (min(products), max(products))


def interval_inv(a: Interval) -> Interval | None:
    if a[0] <= 0.0 <= a[1]:
        return None
    values = (1.0 / a[0], 1.0 / a[1])
    return (min(values), max(values))


def interval_div(a: Interval, b: Interval) -> Interval | None:
    inv = interval_inv(b)
    if inv is None:
        return None
    return interval_mul(a, inv)


def interval_square(a: Interval) -> Interval:
    if a[0] <= 0.0 <= a[1]:
        return (0.0, max(a[0] * a[0], a[1] * a[1]))
    return interval_mul(a, a)


def as_interval_dict(interval: Interval | None) -> dict[str, float] | None:
    if interval is None:
        return None
    return {"lower": interval[0], "upper": interval[1]}


def central(interval: Interval | None) -> float | None:
    if interval is None:
        return None
    return 0.5 * (interval[0] + interval[1])


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def pick_first_present(paths: list[Path]) -> tuple[Path | None, dict[str, Any]]:
    for path in paths:
        data = load_json(path)
        if data:
            return path, data
    return None, {}


def selected_schur_row(data: dict[str, Any]) -> dict[str, Any]:
    for key in ("schur_rows", "neutral_scalar_kernel_partition", "transfer_kernel_rows"):
        row = data.get(key)
        if isinstance(row, dict):
            return row
    rows = data.get("schur_kprime_kernel_rows")
    if isinstance(rows, list):
        selected = [row for row in rows if isinstance(row, dict) and row.get("selected_row") is True]
        if selected:
            return selected[0]
        for row in rows:
            if isinstance(row, dict):
                return row
    return {}


def selected_derivative_row(data: dict[str, Any], schur_rows: dict[str, Any]) -> dict[str, Any]:
    for key in ("derivative_row", "kprime_derivative_row", "transfer_kernel_derivative_row"):
        row = data.get(key)
        if isinstance(row, dict):
            return row
    row = schur_rows.get("derivative_row")
    return row if isinstance(row, dict) else {}


def selected_source_projection(data: dict[str, Any]) -> dict[str, Any]:
    for key in ("source_projection", "source_row", "projection_numerator", "source_projection_numerator"):
        row = data.get(key)
        if isinstance(row, dict):
            return row
    return {}


def pole_coordinate(data: dict[str, Any]) -> dict[str, Any]:
    pole = data.get("pole_coordinate")
    if isinstance(pole, dict):
        interval = get_interval(pole, "value", "pole_location_x", "x", "p_hat_sq")
        out = dict(pole)
        out["interval"] = as_interval_dict(interval)
        return out
    pole_control = data.get("pole_control", {})
    if isinstance(pole_control, dict):
        interval = get_interval(pole_control, "pole_location_x", "pole_p_hat_sq", "x_pole")
        return {
            "variable": pole_control.get("variable", "x"),
            "value": central(interval),
            "interval": as_interval_dict(interval),
            "source": "pole_control",
        }
    interval = get_interval(data, "pole_location_x", "pole_p_hat_sq", "x_pole")
    return {
        "variable": data.get("pole_variable", "x"),
        "value": central(interval),
        "interval": as_interval_dict(interval),
        "source": "top_level",
    }


def pole_fit_window(data: dict[str, Any]) -> dict[str, Any]:
    for container in (data, data.get("pole_control", {})):
        if isinstance(container, dict) and isinstance(container.get("pole_fit_window"), dict):
            return dict(container["pole_fit_window"])
    return {}


def diagnostic_pole_from_postprocessor(postprocessor: dict[str, Any]) -> dict[str, Any]:
    fit = postprocessor.get("diagnostic_fit_if_ready")
    if not isinstance(fit, dict) or not finite(fit.get("pole_p_hat_sq")):
        return {"available": False, "used_as_strict_input": False}
    rows = fit.get("input_rows", [])
    xs = [row.get("p_hat_sq") for row in rows if isinstance(row, dict) and finite(row.get("p_hat_sq"))]
    return {
        "available": True,
        "used_as_strict_input": False,
        "reason_not_strict": "finite-shell diagnostic rows are not Schur/Feshbach K-prime residue rows",
        "pole_p_hat_sq": float(fit["pole_p_hat_sq"]),
        "fit_kind": fit.get("fit_kind"),
        "window_p_hat_sq": [min(xs), max(xs)] if xs else None,
        "input_row_count": len(xs),
    }


def compute_schur_derivative(rows: dict[str, Any]) -> dict[str, Any]:
    scalar_keys = {
        "A_at_pole": get_interval(rows, "A_at_pole"),
        "B_at_pole": get_interval(rows, "B_at_pole"),
        "C_at_pole": get_interval(rows, "C_at_pole"),
        "A_prime_at_pole": get_interval(rows, "A_prime_at_pole", "A_prime"),
        "B_prime_at_pole": get_interval(rows, "B_prime_at_pole", "B_prime"),
        "C_prime_at_pole": get_interval(rows, "C_prime_at_pole", "C_prime"),
    }
    if all(value is not None for value in scalar_keys.values()):
        a0 = scalar_keys["A_at_pole"]
        b0 = scalar_keys["B_at_pole"]
        c0 = scalar_keys["C_at_pole"]
        a1 = scalar_keys["A_prime_at_pole"]
        b1 = scalar_keys["B_prime_at_pole"]
        c1 = scalar_keys["C_prime_at_pole"]
        assert a0 is not None and b0 is not None and c0 is not None
        assert a1 is not None and b1 is not None and c1 is not None
        inv_c = interval_inv(c0)
        if inv_c is None:
            return {
                "valid": False,
                "form": "one_orthogonal_mode_v1",
                "reason": "C_at_pole interval contains zero",
            }
        inv_c2 = interval_square(inv_c)
        d_eff = interval_sub(a0, interval_mul(interval_square(b0), inv_c))
        term_b = interval_mul((2.0, 2.0), interval_mul(interval_mul(b0, b1), inv_c))
        term_c = interval_mul(interval_mul(interval_square(b0), c1), inv_c2)
        derivative = interval_add(interval_sub(a1, term_b), term_c)
        return {
            "valid": True,
            "form": "one_orthogonal_mode_v1",
            "D_eff_at_pole_interval": as_interval_dict(d_eff),
            "D_eff_prime_at_pole_interval": as_interval_dict(derivative),
            "expression": "A' - 2 B B' / C + B^2 C' / C^2",
            "input_intervals": {key: as_interval_dict(value) for key, value in scalar_keys.items()},
        }

    contraction_keys = {
        "A_at_pole": get_interval(rows, "A_at_pole"),
        "B_Cinv_B_at_pole": get_interval(rows, "B_Cinv_B_at_pole"),
        "A_prime_at_pole": get_interval(rows, "A_prime_at_pole", "A_prime"),
        "two_Bprime_Cinv_B_at_pole": get_interval(rows, "two_Bprime_Cinv_B_at_pole"),
        "B_Cinv_Cprime_Cinv_B_at_pole": get_interval(rows, "B_Cinv_Cprime_Cinv_B_at_pole"),
    }
    if all(value is not None for value in contraction_keys.values()):
        a0 = contraction_keys["A_at_pole"]
        bcb = contraction_keys["B_Cinv_B_at_pole"]
        a1 = contraction_keys["A_prime_at_pole"]
        tb = contraction_keys["two_Bprime_Cinv_B_at_pole"]
        bcpcb = contraction_keys["B_Cinv_Cprime_Cinv_B_at_pole"]
        assert a0 is not None and bcb is not None and a1 is not None and tb is not None and bcpcb is not None
        d_eff = interval_sub(a0, bcb)
        derivative = interval_add(interval_sub(a1, tb), bcpcb)
        return {
            "valid": True,
            "form": "precontracted_matrix_v1",
            "D_eff_at_pole_interval": as_interval_dict(d_eff),
            "D_eff_prime_at_pole_interval": as_interval_dict(derivative),
            "expression": "A' - 2 B' C^-1 B + B C^-1 C' C^-1 B",
            "input_intervals": {key: as_interval_dict(value) for key, value in contraction_keys.items()},
        }

    missing = [key for key, value in scalar_keys.items() if value is None]
    missing_precontracted = [key for key, value in contraction_keys.items() if value is None]
    return {
        "valid": False,
        "form": None,
        "reason": "missing Schur scalar or precontracted row intervals",
        "missing_one_orthogonal_mode_v1": missing,
        "missing_precontracted_matrix_v1": missing_precontracted,
    }


def derivative_from_rows(data: dict[str, Any], schur_rows: dict[str, Any]) -> dict[str, Any]:
    schur = compute_schur_derivative(schur_rows)
    if schur.get("valid") is True:
        return {"valid": True, "source": "schur_exact_equivalent", **schur}

    derivative_row = selected_derivative_row(data, schur_rows)
    derivative = get_interval(
        derivative_row,
        "denominator_derivative_at_pole",
        "D_eff_prime_at_pole",
        "d_denominator_dx_at_pole",
    )
    if derivative is not None:
        return {
            "valid": True,
            "source": "explicit_denominator_derivative_row",
            "form": derivative_row.get("form", "explicit_denominator_derivative"),
            "D_eff_prime_at_pole_interval": as_interval_dict(derivative),
            "expression": derivative_row.get("expression", "provided denominator derivative"),
            "provided_row": derivative_row,
        }

    kprime = get_interval(
        derivative_row,
        "left_Kprime_right_at_pole",
        "l_Kprime_r_at_pole",
        "kprime_bilinear_at_pole",
    )
    orientation = derivative_row.get("denominator_derivative_sign_convention")
    if kprime is not None and orientation == "D_prime_equals_minus_l_Kprime_r":
        derivative_interval = interval_neg(kprime)
        return {
            "valid": True,
            "source": "bilinear_kprime_row_with_sign_convention",
            "form": derivative_row.get("form", "transfer_kernel_bilinear_v1"),
            "left_Kprime_right_interval": as_interval_dict(kprime),
            "D_eff_prime_at_pole_interval": as_interval_dict(derivative_interval),
            "expression": "D_eff' = - <l, K'(pole) r>",
            "provided_row": derivative_row,
        }
    if kprime is not None and orientation == "D_prime_equals_l_Kprime_r":
        return {
            "valid": True,
            "source": "bilinear_kprime_row_with_sign_convention",
            "form": derivative_row.get("form", "transfer_kernel_bilinear_v1"),
            "left_Kprime_right_interval": as_interval_dict(kprime),
            "D_eff_prime_at_pole_interval": as_interval_dict(kprime),
            "expression": "D_eff' = <l, K'(pole) r>",
            "provided_row": derivative_row,
        }

    return {"valid": False, "schur_attempt": schur, "provided_derivative_row": derivative_row}


def numerator_interval(source_projection: dict[str, Any]) -> Interval | None:
    return get_interval(
        source_projection,
        "source_projection_numerator_at_pole",
        "source_projection_numerator",
        "projection_numerator_at_pole",
        "projection_numerator",
        "numerator_at_pole",
        "N_at_pole",
    )


def fv_ir_contact_checks(data: dict[str, Any]) -> dict[str, Any]:
    checks = data.get("fv_ir_contact_checks")
    if not isinstance(checks, dict):
        checks = data.get("pole_control", {}).get("fv_ir_contact_checks", {})
    if not isinstance(checks, dict):
        checks = {}
    normalized = {
        "finite_volume_passed": checks.get("finite_volume_passed")
        is True
        or checks.get("fv_control_passed") is True
        or data.get("finite_volume_passed") is True,
        "ir_zero_mode_order_passed": checks.get("ir_zero_mode_order_passed")
        is True
        or checks.get("fv_ir_zero_mode_order_certified") is True
        or data.get("fv_ir_zero_mode_control_passed") is True,
        "contact_terms_subtracted_or_bounded": checks.get("contact_terms_subtracted_or_bounded")
        is True
        or checks.get("contact_term_bound_passed") is True
        or data.get("contact_terms_subtracted_or_bounded") is True,
        "model_class_or_analytic_continuation_passed": checks.get(
            "model_class_or_analytic_continuation_passed"
        )
        is True
        or data.get("model_class_or_analytic_continuation_passed") is True,
        "raw": checks,
    }
    normalized["passed"] = all(
        normalized[key]
        for key in (
            "finite_volume_passed",
            "ir_zero_mode_order_passed",
            "contact_terms_subtracted_or_bounded",
            "model_class_or_analytic_continuation_passed",
        )
    )
    return normalized


def forbidden_import_firewall(data: dict[str, Any]) -> dict[str, Any]:
    firewall = data.get("forbidden_import_firewall")
    if not isinstance(firewall, dict):
        firewall = data.get("firewall", {})
    if not isinstance(firewall, dict):
        firewall = {}
    normalized: dict[str, Any] = {}
    missing: list[str] = []
    violations: list[str] = []
    for canonical, aliases in FORBIDDEN_FIREWALL_FIELDS.items():
        present_values = [firewall[alias] for alias in aliases if alias in firewall]
        if not present_values:
            missing.append(canonical)
            normalized[canonical] = None
        elif any(value is not False for value in present_values):
            violations.append(canonical)
            normalized[canonical] = present_values
        else:
            normalized[canonical] = False
    return {
        "passed": not missing and not violations,
        "normalized": normalized,
        "missing_explicit_false_fields": missing,
        "violations": violations,
        "raw": firewall,
    }


def partition_checks(data: dict[str, Any]) -> dict[str, Any]:
    partition = data.get("partition_certificate", {})
    if not isinstance(partition, dict):
        partition = {}
    pole_control = data.get("pole_control", {})
    if not isinstance(pole_control, dict):
        pole_control = {}
    checks = {
        "phase_supported": data.get("phase") in {"production", "theorem"},
        "same_surface_cl3_z3": data.get("same_surface_cl3_z3") is True,
        "source_coordinate_named": isinstance(data.get("source_coordinate"), str)
        and bool(data.get("source_coordinate")),
        "same_surface_neutral_scalar_kernel_partition_passed": partition.get(
            "same_surface_neutral_scalar_kernel_partition_passed"
        )
        is True,
        "source_pole_coordinate_certified": partition.get("source_pole_coordinate_certified") is True,
        "orthogonal_neutral_block_certified": partition.get("orthogonal_neutral_block_certified") is True,
        "source_orthogonal_covariance_included": partition.get(
            "source_orthogonal_covariance_included"
        )
        is True,
        "isolated_scalar_pole_passed": pole_control.get("isolated_scalar_pole_passed") is True
        or data.get("isolated_scalar_pole_passed") is True,
    }
    return {"passed": all(checks.values()), "checks": checks, "missing_or_failed": [k for k, v in checks.items() if not v]}


def residue_interval(numerator: Interval | None, derivative: dict[str, Any]) -> dict[str, Any]:
    derivative_interval = interval_from_any(derivative.get("D_eff_prime_at_pole_interval"))
    if numerator is None or derivative_interval is None:
        return {
            "computed": False,
            "residue_interval": None,
            "reason": "missing numerator interval or denominator derivative interval",
        }
    residue = interval_div(numerator, derivative_interval)
    if residue is None:
        return {
            "computed": False,
            "residue_interval": None,
            "reason": "D_eff_prime interval contains zero",
            "source_projection_numerator_interval": as_interval_dict(numerator),
            "D_eff_prime_at_pole_interval": as_interval_dict(derivative_interval),
        }
    return {
        "computed": True,
        "source_projection_numerator_interval": as_interval_dict(numerator),
        "D_eff_prime_at_pole_interval": as_interval_dict(derivative_interval),
        "residue_interval": as_interval_dict(residue),
        "strict_positive": residue[0] > 0.0,
        "formula": "Res C_ss(pole) = N_source(pole) / D_eff'(pole)",
    }


def required_emissions_contract() -> dict[str, Any]:
    return {
        "artifact_paths_accepted_by_builder": [rel(path) for path in DEFAULT_ROW_INPUTS],
        "top_level_required": {
            "phase": "production or theorem",
            "same_surface_cl3_z3": True,
            "source_coordinate": "same scalar source coordinate used by PR230 FH/LSZ response",
        },
        "pole_coordinate_and_fit_window": {
            "pole_coordinate": {
                "variable": "x or p_hat_sq",
                "value or interval": "finite pole coordinate with source path/provenance",
            },
            "pole_fit_window": {
                "window_points or x_min/x_max": "the certified pole-fit/analytic-continuation window",
                "fit_kind": "pole model or theorem row type",
                "fit_provenance": "chunk/combiner/theorem emission id",
            },
        },
        "source_projection_numerator": {
            "source_projection": {
                "source_projection_numerator_interval": "[lo, hi] with lo > 0 for strict positivity",
                "left_right_projection_rows": "or equivalent source-to-pole numerator rows",
                "normalization_certificate": "same-source normalization, not kappa_s=1 by fiat",
            }
        },
        "schur_or_feshbach_rows": {
            "one_orthogonal_mode_v1": [
                "A_at_pole interval",
                "B_at_pole interval",
                "C_at_pole interval excluding zero",
                "A_prime_at_pole interval",
                "B_prime_at_pole interval",
                "C_prime_at_pole interval",
            ],
            "precontracted_matrix_v1": [
                "A_at_pole interval",
                "B_Cinv_B_at_pole interval",
                "A_prime_at_pole interval",
                "two_Bprime_Cinv_B_at_pole interval",
                "B_Cinv_Cprime_Cinv_B_at_pole interval",
            ],
            "transfer_kernel_bilinear_v1": [
                "<l,K'(pole)r> interval",
                "explicit denominator_derivative_sign_convention",
                "left/right eigenvector normalization certificate",
            ],
        },
        "fv_ir_contact_term_checks": [
            "finite_volume_passed=true",
            "ir_zero_mode_order_passed=true",
            "contact_terms_subtracted_or_bounded=true",
            "model_class_or_analytic_continuation_passed=true",
        ],
        "forbidden_import_firewall": [
            f"{field}=false" for field in FORBIDDEN_FIREWALL_FIELDS
        ],
    }


def missing_required_rows(
    candidate_present: bool,
    pole: dict[str, Any],
    window: dict[str, Any],
    source_projection: dict[str, Any],
    numerator: Interval | None,
    derivative: dict[str, Any],
    partition: dict[str, Any],
    fv_ir_contact: dict[str, Any],
    firewall: dict[str, Any],
) -> list[str]:
    missing: list[str] = []
    if not candidate_present:
        missing.append("strict row artifact absent")
    if pole.get("interval") is None:
        missing.append("pole_coordinate interval/value")
    if not window:
        missing.append("pole_fit_window provenance")
    if not source_projection:
        missing.append("source row/projection numerator container")
    if numerator is None:
        missing.append("source_projection_numerator_at_pole interval")
    if derivative.get("valid") is not True:
        missing.append("Schur/Feshbach A/B/C rows or exact derivative row")
        schur_attempt = derivative.get("schur_attempt", {})
        if isinstance(schur_attempt, dict):
            for key in schur_attempt.get("missing_one_orthogonal_mode_v1", []):
                missing.append(f"one_orthogonal_mode_v1.{key}")
            for key in schur_attempt.get("missing_precontracted_matrix_v1", []):
                missing.append(f"precontracted_matrix_v1.{key}")
    if not partition.get("passed"):
        missing.extend([f"partition.{key}" for key in partition.get("missing_or_failed", [])])
    if not fv_ir_contact.get("passed"):
        for key in (
            "finite_volume_passed",
            "ir_zero_mode_order_passed",
            "contact_terms_subtracted_or_bounded",
            "model_class_or_analytic_continuation_passed",
        ):
            if fv_ir_contact.get(key) is not True:
                missing.append(f"fv_ir_contact_checks.{key}")
    if not firewall.get("passed"):
        missing.extend([f"forbidden_import_firewall.{key}" for key in firewall.get("missing_explicit_false_fields", [])])
        missing.extend([f"forbidden_import_firewall.violation.{key}" for key in firewall.get("violations", [])])
    return sorted(set(missing))


def strict_status(
    missing: list[str],
    residue: dict[str, Any],
    derivative: dict[str, Any],
    pole: dict[str, Any],
) -> str:
    if missing:
        return "missing_rows"
    if derivative.get("valid") is not True or residue.get("computed") is not True:
        return "honest_fail"
    if residue.get("strict_positive") is not True:
        return "honest_fail"
    d_eff_interval = interval_from_any(derivative.get("D_eff_at_pole_interval"))
    if d_eff_interval is not None and not (d_eff_interval[0] <= 0.0 <= d_eff_interval[1]):
        return "honest_fail"
    if pole.get("interval") is None:
        return "honest_fail"
    return "strict_pass"


def build_certificate(row_paths: list[Path], output: Path) -> dict[str, Any]:
    parent_certs = {name: load_json(ROOT / path) for name, path in PARENTS.items()}
    row_path, candidate = pick_first_present(row_paths)
    candidate_present = bool(candidate)
    schur_rows = selected_schur_row(candidate)
    source_projection = selected_source_projection(candidate)
    pole = pole_coordinate(candidate)
    window = pole_fit_window(candidate)
    derivative = derivative_from_rows(candidate, schur_rows)
    numerator = numerator_interval(source_projection)
    residue = residue_interval(numerator, derivative)
    partition = partition_checks(candidate)
    fv_ir_contact = fv_ir_contact_checks(candidate)
    firewall = forbidden_import_firewall(candidate)
    diagnostic_pole = diagnostic_pole_from_postprocessor(parent_certs["fh_lsz_polefit8x8_postprocessor"])
    missing = missing_required_rows(
        candidate_present,
        pole,
        window,
        source_projection,
        numerator,
        derivative,
        partition,
        fv_ir_contact,
        firewall,
    )
    status_value = strict_status(missing, residue, derivative, pole)
    strict_pass = status_value == "strict_pass"

    if status_value == "strict_pass":
        surface_status = "exact-support / strict K-prime pole-residue certificate populated"
        verdict = (
            "The explicit same-surface Schur/Feshbach K'(pole) row artifact "
            "satisfies the partition, pole-window, source-numerator, "
            "derivative, FV/IR/contact-term, and forbidden-import firewalls. "
            "The positive same-source residue interval is computed below. "
            "Any broader PR230 retained-route proposal still belongs to the "
            "parent integration gate."
        )
    elif status_value == "missing_rows":
        surface_status = "open / strict K-prime pole-residue certificate rows missing"
        verdict = (
            "No complete strict K-prime pole-residue row artifact is present. "
            "The builder did not infer missing rows from finite-shell C_ss data "
            "or from the support-only Schur sufficiency theorem; it wrote the "
            "exact emissions contract needed for chunk/combiner/theorem code."
        )
    else:
        surface_status = "honest-fail / strict K-prime pole-residue certificate rows do not pass"
        verdict = (
            "A candidate strict K-prime row artifact was present, but the "
            "rows do not certify a positive pole residue under the required "
            "partition, pole-control, FV/IR/contact, and firewall checks."
        )

    certificate = {
        "artifact": "yt_pr230_block69_strict_kprime_pole_residue_certificate_builder",
        "actual_current_surface_status": surface_status,
        "status": status_value,
        "verdict": verdict,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "This Block69 artifact certifies only the strict K-prime pole-residue "
            "leg.  The parent PR230 retained-route/assembly gate remains "
            "authoritative for any proposed_retained wording."
        ),
        "bare_retained_allowed": False,
        "row_inputs_checked": [rel(path) for path in row_paths],
        "selected_row_input": rel(row_path) if row_path is not None else None,
        "candidate_present": candidate_present,
        "pole_coordinate": pole,
        "pole_fit_window": window,
        "source_row_projection_numerator": {
            "row": source_projection,
            "numerator_interval": as_interval_dict(numerator),
        },
        "schur_feshbach_or_transfer_kernel_rows": {
            "selected_rows": schur_rows,
            "derivative_certificate": derivative,
        },
        "derivative_row_l_Kprime_r_or_exact_equivalent": derivative,
        "residue_interval": residue,
        "FV_IR_contact_term_checks": fv_ir_contact,
        "forbidden_import_firewall": firewall,
        "missing_required_rows": missing,
        "required_emissions_contract": required_emissions_contract() if status_value == "missing_rows" else {},
        "diagnostic_finite_shell_pole_not_used_as_strict_input": diagnostic_pole,
        "parent_statuses": {name: status(cert) for name, cert in parent_certs.items()},
        "parent_certificates": PARENTS,
        "strict_pass": strict_pass,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not infer K'(pole) from finite-shell C_ss rows or source-only slopes",
            "does not use H_unit, yt_ward_identity, y_t_bare, alpha_LM, plaquette/u0, observed target selectors, or alias imports",
            "does not set kappa_s=1, D_eff'(pole)=1, c2=1, Z_match=1, or cos(theta)=1",
            "does not modify Planck, alpha_s, CLAIMS_TABLE, or manuscript surfaces",
        ],
        "exact_next_action": (
            "Emit one accepted strict row artifact containing the pole coordinate, "
            "pole-fit window, source projection numerator, Schur/Feshbach rows "
            "or signed transfer-kernel derivative row, FV/IR/contact checks, and "
            "explicit forbidden-import firewall false fields; then rerun this builder."
            if status_value == "missing_rows"
            else "Feed this certificate to the parent assembly gate; do not promote PR230 wording without that gate."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return certificate


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--rows",
        type=Path,
        nargs="*",
        default=DEFAULT_ROW_INPUTS,
        help="Explicit strict K-prime row artifact paths to try, in order.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    row_paths = [path if path.is_absolute() else ROOT / path for path in args.rows]
    output = args.output if args.output.is_absolute() else ROOT / args.output
    print("PR #230 Block69 strict K-prime pole-residue certificate builder")
    print("=" * 72)
    cert = build_certificate(row_paths, output)

    report("row-input-state-recorded", True, f"selected={cert['selected_row_input']}")
    report("strict-status-recorded", cert["status"] in {"strict_pass", "missing_rows", "honest_fail"}, cert["status"])
    if cert["status"] == "strict_pass":
        report("strict-positive-residue-certificate-populated", True, str(cert["residue_interval"].get("residue_interval")))
    elif cert["status"] == "missing_rows":
        report("missing-required-rows-contract-written", True, f"missing={cert['missing_required_rows']}")
    else:
        report("honest-fail-recorded", True, str(cert["residue_interval"]))

    cert["pass_count"] = PASS_COUNT
    cert["fail_count"] = FAIL_COUNT
    output.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {rel(output)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
