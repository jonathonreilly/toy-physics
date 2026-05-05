#!/usr/bin/env python3
"""
PR #230 FH/LSZ affine-contact complete-monotonicity no-go.

The prior contact-subtraction boundary showed that first-order monotonicity
restoration does not identify an affine contact term.  This runner tests the
next sharper question: can any affine local contact subtraction make the
current polefit8x8 finite rows look like a positive Stieltjes object under
finite complete-monotonicity checks?

No.  A positive Stieltjes transform is completely monotone, so its divided
differences on ordered points obey (-1)^k f[x_i,...,x_{i+k}] >= 0.  Subtracting
an affine term C(x) -> C(x) - a x changes only first divided differences; all
second and higher divided differences are invariant.  The current polefit8x8
rows have robust higher-order sign violations, so affine contact subtraction
cannot be the missing scalar LSZ/contact certificate.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
COMBINED = ROOT / "outputs" / "yt_pr230_fh_lsz_polefit8x8_L12_T24_chunked_combined_2026-05-04.json"
PROXY_DIAGNOSTIC = ROOT / "outputs" / "yt_fh_lsz_polefit8x8_stieltjes_proxy_diagnostic_2026-05-05.json"
CONTACT_IDENTIFIABILITY = ROOT / "outputs" / "yt_fh_lsz_contact_subtraction_identifiability_2026-05-05.json"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_affine_contact_complete_monotonicity_no_go_2026-05-05.json"

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


def extract_rows(combined: dict[str, Any]) -> list[dict[str, float]]:
    raw = combined.get("combined_lsz_summary", {}).get("mode_rows")
    iterable = raw.values() if isinstance(raw, dict) else raw if isinstance(raw, list) else []
    rows: list[dict[str, float]] = []
    for row in iterable:
        if not isinstance(row, dict):
            continue
        x = row.get("p_hat_sq")
        c = row.get("C_ss_real_weighted")
        err = row.get("C_ss_real_weighted_stderr")
        if finite(x) and finite(c):
            rows.append(
                {
                    "p_hat_sq": float(x),
                    "C_ss_real": float(c),
                    "C_ss_real_stderr": float(err) if finite(err) else float("nan"),
                }
            )
    return sorted(rows, key=lambda item: item["p_hat_sq"])


def divided_difference_coefficients(xs: list[float]) -> list[list[list[float]]]:
    n = len(xs)
    levels: list[list[list[float]]] = []
    levels.append([[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)])
    for order in range(1, n):
        current: list[list[float]] = []
        previous = levels[-1]
        for i in range(n - order):
            denominator = xs[i + order] - xs[i]
            coeffs = [
                (previous[i + 1][j] - previous[i][j]) / denominator
                for j in range(n)
            ]
            current.append(coeffs)
        levels.append(current)
    return levels


def divided_difference_checks(rows: list[dict[str, float]], *, slope: float = 0.0) -> list[dict[str, Any]]:
    xs = [row["p_hat_sq"] for row in rows]
    ys = [row["C_ss_real"] - slope * row["p_hat_sq"] for row in rows]
    sigmas = [row["C_ss_real_stderr"] for row in rows]
    coeff_levels = divided_difference_coefficients(xs)
    checks: list[dict[str, Any]] = []
    for order, coeff_rows in enumerate(coeff_levels):
        if order == 0:
            continue
        order_rows = []
        for index, coeffs in enumerate(coeff_rows):
            value = sum(coeff * y for coeff, y in zip(coeffs, ys))
            alt_value = ((-1.0) ** order) * value
            variance = 0.0
            for coeff, sigma in zip(coeffs, sigmas):
                if math.isfinite(sigma):
                    variance += coeff * coeff * sigma * sigma
            sigma = math.sqrt(max(variance, 0.0))
            z = alt_value / sigma if sigma > 0.0 else None
            order_rows.append(
                {
                    "window_start": index,
                    "window_end": index + order,
                    "divided_difference": value,
                    "alternating_sign_value": alt_value,
                    "sigma_from_row_stderr": sigma,
                    "z_if_row_stderr_independent": z,
                    "passes_nonnegative_precheck": alt_value >= -1.0e-14,
                    "robust_violation_over_5sigma": bool(sigma > 0.0 and alt_value < -5.0 * sigma),
                }
            )
        robust = [row for row in order_rows if row["robust_violation_over_5sigma"]]
        checks.append(
            {
                "order": order,
                "all_windows_pass": all(row["passes_nonnegative_precheck"] for row in order_rows),
                "robust_violation_count": len(robust),
                "min_alternating_sign_value": min(row["alternating_sign_value"] for row in order_rows),
                "min_z_if_row_stderr_independent": min(
                    row["z_if_row_stderr_independent"]
                    for row in order_rows
                    if row["z_if_row_stderr_independent"] is not None
                ),
                "rows": order_rows,
            }
        )
    return checks


def first_order_contact_interval(rows: list[dict[str, float]]) -> dict[str, Any]:
    slopes = []
    for left, right in zip(rows, rows[1:]):
        dx = right["p_hat_sq"] - left["p_hat_sq"]
        if dx <= 0.0:
            continue
        slopes.append((right["C_ss_real"] - left["C_ss_real"]) / dx)
    lower = max(slopes) if slopes else float("nan")
    upper = min(
        (row["C_ss_real"] / row["p_hat_sq"] for row in rows if row["p_hat_sq"] > 0.0),
        default=float("nan"),
    )
    return {
        "lower_bound_from_first_order_monotonicity": lower,
        "upper_bound_from_residual_positivity": upper,
        "interval_nonempty": math.isfinite(lower) and math.isfinite(upper) and lower < upper,
    }


def family_rows(rows: list[dict[str, float]], slope: float) -> list[dict[str, float]]:
    return [
        {
            "p_hat_sq": row["p_hat_sq"],
            "raw_C_ss_real": row["C_ss_real"],
            "affine_contact_term": slope * row["p_hat_sq"],
            "residual_C_ss_real": row["C_ss_real"] - slope * row["p_hat_sq"],
        }
        for row in rows
    ]


def max_higher_difference(left: list[dict[str, Any]], right: list[dict[str, Any]]) -> float:
    out = 0.0
    for left_order, right_order in zip(left, right):
        if left_order["order"] < 2 or right_order["order"] < 2:
            continue
        for left_row, right_row in zip(left_order["rows"], right_order["rows"]):
            out = max(
                out,
                abs(
                    left_row["alternating_sign_value"]
                    - right_row["alternating_sign_value"]
                ),
            )
    return out


def main() -> int:
    print("PR #230 FH/LSZ affine-contact complete-monotonicity no-go")
    print("=" * 72)

    combined = load_json(COMBINED)
    proxy = load_json(PROXY_DIAGNOSTIC)
    contact = load_json(CONTACT_IDENTIFIABILITY)
    rows = extract_rows(combined)
    interval = first_order_contact_interval(rows)
    width = (
        interval["upper_bound_from_residual_positivity"]
        - interval["lower_bound_from_first_order_monotonicity"]
        if interval["interval_nonempty"]
        else float("nan")
    )
    slope_a = interval["lower_bound_from_first_order_monotonicity"] + 0.25 * width
    slope_b = interval["lower_bound_from_first_order_monotonicity"] + 0.75 * width
    raw_checks = divided_difference_checks(rows)
    affine_a_checks = divided_difference_checks(rows, slope=slope_a) if math.isfinite(slope_a) else []
    affine_b_checks = divided_difference_checks(rows, slope=slope_b) if math.isfinite(slope_b) else []
    higher_raw = [row for row in raw_checks if row["order"] >= 2]
    higher_a = [row for row in affine_a_checks if row["order"] >= 2]
    higher_b = [row for row in affine_b_checks if row["order"] >= 2]
    robust_higher_violations = [
        row for row in higher_raw if row["robust_violation_count"] > 0
    ]
    max_invariance_error = max(
        max_higher_difference(raw_checks, affine_a_checks),
        max_higher_difference(raw_checks, affine_b_checks),
    )
    invariant_higher_checks = max_invariance_error < 1.0e-12
    first_order_fixed_by_affine = (
        bool(affine_a_checks)
        and bool(affine_b_checks)
        and affine_a_checks[0]["all_windows_pass"]
        and affine_b_checks[0]["all_windows_pass"]
    )
    affine_complete_monotonicity_fails = (
        first_order_fixed_by_affine
        and bool(robust_higher_violations)
        and not all(row["all_windows_pass"] for row in higher_a)
        and not all(row["all_windows_pass"] for row in higher_b)
    )
    future_contact_certificate_present = (
        ROOT / "outputs" / "yt_fh_lsz_contact_subtraction_certificate_2026-05-05.json"
    ).exists()

    report("combined-polefit8x8-input-loaded", bool(combined), rel(COMBINED))
    report("proxy-diagnostic-parent-loaded", bool(proxy), rel(PROXY_DIAGNOSTIC))
    report("contact-identifiability-parent-loaded", bool(contact), rel(CONTACT_IDENTIFIABILITY))
    report("finite-rows-present", len(rows) >= 6, f"rows={len(rows)}")
    report(
        "first-order-affine-contact-interval-nonempty",
        interval["interval_nonempty"],
        (
            f"lower={interval['lower_bound_from_first_order_monotonicity']:.12g} "
            f"upper={interval['upper_bound_from_residual_positivity']:.12g}"
        ),
    )
    report("affine-family-first-order-monotonicity-fixed", first_order_fixed_by_affine, f"slopes={[slope_a, slope_b]}")
    report(
        "higher-divided-differences-affine-invariant",
        invariant_higher_checks,
        f"orders >=2 are unchanged by C(x)-a x to {max_invariance_error:.3e}",
    )
    report(
        "robust-higher-complete-monotonicity-violations-present",
        bool(robust_higher_violations),
        f"orders={[row['order'] for row in robust_higher_violations]}",
    )
    report(
        "affine-contact-complete-monotonicity-no-go",
        affine_complete_monotonicity_fails,
        "no affine slope can repair higher Stieltjes sign violations",
    )
    report("future-contact-certificate-absent", not future_contact_certificate_present, "yt_fh_lsz_contact_subtraction_certificate_2026-05-05.json")
    report("does-not-authorize-proposed-retained", True, "affine-contact no-go only")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / affine contact complete-monotonicity no-go"
        ),
        "verdict": (
            "The current polefit8x8 rows cannot be promoted to a positive "
            "Stieltjes scalar-LSZ object by an affine contact subtraction.  "
            "Affine subtraction can restore first-order monotonicity, but it "
            "does not change second or higher divided differences.  Those "
            "higher finite complete-monotonicity signs have robust violations "
            "on the current rows, so an affine contact term is not the missing "
            "contact/denominator certificate."
        ),
        "proposal_allowed": False,
        "affine_contact_complete_monotonicity_no_go_passed": affine_complete_monotonicity_fails,
        "affine_contact_stieltjes_certificate_passed": False,
        "contact_subtraction_certificate_present": future_contact_certificate_present,
        "row_source": rel(COMBINED),
        "rows": rows,
        "affine_contact_interval": interval,
        "raw_divided_difference_checks": raw_checks,
        "max_higher_order_affine_invariance_error": max_invariance_error,
        "affine_contact_families": [
            {
                "label": "contact_family_a",
                "affine_contact_slope": slope_a,
                "residual_rows": family_rows(rows, slope_a) if math.isfinite(slope_a) else [],
                "divided_difference_checks": affine_a_checks,
            },
            {
                "label": "contact_family_b",
                "affine_contact_slope": slope_b,
                "residual_rows": family_rows(rows, slope_b) if math.isfinite(slope_b) else [],
                "divided_difference_checks": affine_b_checks,
            },
        ],
        "theorem": (
            "If f is completely monotone on the ordered shell interval, then "
            "(-1)^k f[x_i,...,x_{i+k}] >= 0 for all finite divided "
            "differences.  For f_a(x)=C_raw(x)-a x, all divided differences "
            "of order k>=2 are independent of a.  Therefore any robust "
            "higher-order sign violation in the raw finite rows rules out the "
            "entire affine-contact family as a Stieltjes certificate."
        ),
        "strict_non_claims": [
            "does not rule out a higher-polynomial or microscopic contact-subtraction certificate",
            "does not create a Stieltjes moment certificate",
            "does not determine a pole residue or kappa_s",
            "does not claim retained or proposed_retained y_t closure",
            "does not use H_unit, Ward authority, observed targets, alpha_LM, plaquette/u0, c2=1, Z_match=1, or kappa_s=1",
        ],
        "exact_next_action": (
            "A positive scalar-LSZ route now needs a same-surface microscopic "
            "contact/denominator theorem, a higher-order contact certificate "
            "with independent normalization, or a strict Stieltjes "
            "moment-threshold-FV certificate.  Affine monotonicity repair is closed."
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
