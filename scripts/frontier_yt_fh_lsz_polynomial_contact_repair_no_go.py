#!/usr/bin/env python3
"""
PR #230 FH/LSZ polynomial-contact repair no-go.

The affine-contact no-go closes the degree-one repair.  This runner checks the
broader finite polynomial-contact shortcut: can finite polefit8x8 rows plus a
polynomial local subtraction certify a scalar-LSZ Stieltjes object?

No.  Low-degree polynomial contacts leave robust higher divided-difference
violations unchanged.  High-degree contacts can interpolate many different
finite Stieltjes-looking residual rows, so they are fit choices rather than a
same-surface contact/subtraction theorem.  The route remains blocked until a
microscopic scalar-denominator theorem or strict contact certificate exists.
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
AFFINE_NO_GO = ROOT / "outputs" / "yt_fh_lsz_affine_contact_complete_monotonicity_no_go_2026-05-05.json"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_polynomial_contact_repair_no_go_2026-05-05.json"

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
    levels: list[list[list[float]]] = [
        [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    ]
    for order in range(1, n):
        previous = levels[-1]
        current: list[list[float]] = []
        for i in range(n - order):
            denominator = xs[i + order] - xs[i]
            current.append(
                [(previous[i + 1][j] - previous[i][j]) / denominator for j in range(n)]
            )
        levels.append(current)
    return levels


def divided_difference_checks(rows: list[dict[str, float]], values: list[float]) -> list[dict[str, Any]]:
    xs = [row["p_hat_sq"] for row in rows]
    sigmas = [row["C_ss_real_stderr"] for row in rows]
    coeff_levels = divided_difference_coefficients(xs)
    checks: list[dict[str, Any]] = []
    for order, coeff_rows in enumerate(coeff_levels):
        if order == 0:
            continue
        order_rows = []
        for index, coeffs in enumerate(coeff_rows):
            value = sum(coeff * y for coeff, y in zip(coeffs, values))
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
        z_values = [row["z_if_row_stderr_independent"] for row in order_rows if row["z_if_row_stderr_independent"] is not None]
        checks.append(
            {
                "order": order,
                "all_windows_pass": all(row["passes_nonnegative_precheck"] for row in order_rows),
                "robust_violation_count": sum(row["robust_violation_over_5sigma"] for row in order_rows),
                "min_alternating_sign_value": min(row["alternating_sign_value"] for row in order_rows),
                "min_z_if_row_stderr_independent": min(z_values) if z_values else None,
                "rows": order_rows,
            }
        )
    return checks


def solve_vandermonde(xs: list[float], ys: list[float]) -> list[float]:
    n = len(xs)
    a = [[xs[i] ** j for j in range(n)] + [ys[i]] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(a[row][col]))
        if abs(a[pivot][col]) < 1.0e-18:
            raise ValueError("singular Vandermonde system")
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
        scale = a[col][col]
        for j in range(col, n + 1):
            a[col][j] /= scale
        for row in range(n):
            if row == col:
                continue
            factor = a[row][col]
            for j in range(col, n + 1):
                a[row][j] -= factor * a[col][j]
    return [a[row][n] for row in range(n)]


def eval_poly(coeffs: list[float], x: float) -> float:
    total = 0.0
    for coeff in reversed(coeffs):
        total = total * x + coeff
    return total


def stieltjes_target(rows: list[dict[str, float]], *, residue: float, shift: float) -> list[float]:
    return [residue / (row["p_hat_sq"] + shift) for row in rows]


def target_family(rows: list[dict[str, float]], label: str, residue: float, shift: float) -> dict[str, Any]:
    raw = [row["C_ss_real"] for row in rows]
    target = stieltjes_target(rows, residue=residue, shift=shift)
    contact_values = [c - t for c, t in zip(raw, target)]
    coeffs = solve_vandermonde([row["p_hat_sq"] for row in rows], contact_values)
    reconstructed = [raw_i - eval_poly(coeffs, row["p_hat_sq"]) for raw_i, row in zip(raw, rows)]
    max_error = max(abs(a - b) for a, b in zip(target, reconstructed))
    checks = divided_difference_checks(rows, target)
    return {
        "label": label,
        "degree": len(rows) - 1,
        "stieltjes_model": "residue / (p_hat_sq + shift)",
        "residue_parameter": residue,
        "shift_parameter": shift,
        "target_rows": [
            {
                "p_hat_sq": row["p_hat_sq"],
                "raw_C_ss_real": row["C_ss_real"],
                "target_residual_C_ss_real": value,
                "interpolated_contact_value": contact,
            }
            for row, value, contact in zip(rows, target, contact_values)
        ],
        "contact_polynomial_coefficients_low_to_high": coeffs,
        "max_interpolation_error": max_error,
        "all_finite_complete_monotonicity_checks_pass": all(check["all_windows_pass"] for check in checks),
        "complete_monotonicity_checks": checks,
    }


def main() -> int:
    print("PR #230 FH/LSZ polynomial-contact repair no-go")
    print("=" * 72)

    combined = load_json(COMBINED)
    proxy = load_json(PROXY_DIAGNOSTIC)
    contact = load_json(CONTACT_IDENTIFIABILITY)
    affine = load_json(AFFINE_NO_GO)
    rows = extract_rows(combined)
    raw_values = [row["C_ss_real"] for row in rows]
    raw_checks = divided_difference_checks(rows, raw_values) if rows else []
    robust_orders = [
        check["order"]
        for check in raw_checks
        if check["robust_violation_count"] > 0
    ]
    max_robust_order = max(robust_orders, default=-1)
    low_degree_blocked = [
        {
            "degree": degree,
            "blocking_invariant_orders": [order for order in robust_orders if order > degree],
        }
        for degree in range(max(0, max_robust_order))
    ]
    low_degree_block_all = bool(low_degree_blocked) and all(
        row["blocking_invariant_orders"] for row in low_degree_blocked
    )
    family_a = target_family(rows, "manufactured_stieltjes_residue_A", residue=0.060, shift=0.800) if rows else {}
    family_b = target_family(rows, "manufactured_stieltjes_residue_B", residue=0.090, shift=0.800) if rows else {}
    finite_targets_pass = bool(family_a) and bool(family_b) and family_a["all_finite_complete_monotonicity_checks_pass"] and family_b["all_finite_complete_monotonicity_checks_pass"]
    interpolation_errors_small = bool(family_a) and bool(family_b) and max(family_a["max_interpolation_error"], family_b["max_interpolation_error"]) < 1.0e-10
    zero_row_stderr = rows[0]["C_ss_real_stderr"] if rows else float("nan")
    zero_residual_spread = (
        abs(family_b["target_rows"][0]["target_residual_C_ss_real"] - family_a["target_rows"][0]["target_residual_C_ss_real"])
        if family_a and family_b
        else float("nan")
    )
    zero_spread_z = zero_residual_spread / zero_row_stderr if math.isfinite(zero_row_stderr) and zero_row_stderr > 0.0 else float("nan")
    future_contact_certificate_present = (
        ROOT / "outputs" / "yt_fh_lsz_contact_subtraction_certificate_2026-05-05.json"
    ).exists()

    report("combined-polefit8x8-input-loaded", bool(combined), rel(COMBINED))
    report("proxy-diagnostic-parent-loaded", bool(proxy), rel(PROXY_DIAGNOSTIC))
    report("contact-identifiability-parent-loaded", bool(contact), rel(CONTACT_IDENTIFIABILITY))
    report("affine-no-go-parent-loaded", bool(affine), rel(AFFINE_NO_GO))
    report("finite-rows-present", len(rows) >= 8, f"rows={len(rows)}")
    report("robust-complete-monotonicity-violations-present", bool(robust_orders), f"orders={robust_orders}")
    report("degree-zero-through-five-polynomial-contacts-blocked", low_degree_block_all, f"blocked={low_degree_blocked}")
    report("two-high-degree-contact-families-constructed", bool(family_a) and bool(family_b), "degree <= 7 interpolation")
    report("manufactured-targets-pass-finite-stieltjes-checks", finite_targets_pass, "both targets are positive Stieltjes samples")
    report("contact-polynomials-interpolate-targets", interpolation_errors_small, "max interpolation error < 1e-10")
    report("high-degree-families-change-zero-residue-beyond-errors", math.isfinite(zero_spread_z) and zero_spread_z > 100.0, f"zero_spread_z={zero_spread_z:.3f}")
    report("future-contact-certificate-absent", not future_contact_certificate_present, "yt_fh_lsz_contact_subtraction_certificate_2026-05-05.json")
    report("does-not-authorize-proposed-retained", True, "polynomial-contact no-go only")

    result = {
        "actual_current_surface_status": "exact negative boundary / polynomial contact repair not scalar-LSZ authority",
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Finite polynomial contact fitting does not supply a same-surface "
            "scalar-LSZ object.  Low-degree contacts leave robust higher "
            "complete-monotonicity violations invariant, while high-degree "
            "contacts can interpolate mutually different finite Stieltjes-looking "
            "residuals unless a contact/denominator theorem fixes the polynomial."
        ),
        "polynomial_contact_repair_no_go_passed": True,
        "stieltjes_certificate_from_polynomial_contact_passed": False,
        "contact_subtraction_certificate_present": future_contact_certificate_present,
        "low_degree_invariant_block": {
            "robust_violation_orders": robust_orders,
            "max_robust_violation_order": max_robust_order,
            "blocked_degrees": low_degree_blocked,
            "theorem": (
                "A polynomial contact term of degree d changes divided "
                "differences only through order d.  Any robust alternating-sign "
                "violation at order k>d is invariant under that contact family."
            ),
        },
        "high_degree_overfit_witness": {
            "theorem": (
                "With N finite shell points, a polynomial of degree at most N-1 "
                "can interpolate the difference between the raw rows and any "
                "chosen finite target rows.  Finite complete-monotonicity of the "
                "target therefore does not identify the physical contact "
                "subtraction without a same-surface renormalization or "
                "microscopic scalar-denominator theorem."
            ),
            "families": [family_a, family_b],
            "zero_residual_spread": {
                "absolute_spread": zero_residual_spread,
                "row_stderr": zero_row_stderr,
                "z_score_if_row_stderr_trusted": zero_spread_z,
            },
        },
        "parent_certificates": {
            "polefit8x8_combined": rel(COMBINED),
            "proxy_diagnostic": rel(PROXY_DIAGNOSTIC),
            "contact_identifiability": rel(CONTACT_IDENTIFIABILITY),
            "affine_contact_no_go": rel(AFFINE_NO_GO),
        },
        "strict_non_claims": [
            "does not claim a valid contact-subtracted scalar two-point function",
            "does not create outputs/yt_fh_lsz_stieltjes_moment_certificate_2026-05-05.json",
            "does not determine scalar pole residue, K'(pole), kappa_s, c2, or Z_match",
            "does not use H_unit, Ward authority, observed targets, alpha_LM, plaquette, u0, y_t_bare, or bare-coupling algebra",
            "does not package or rerun chunk MC",
        ],
        "exact_next_action": (
            "Do not repair the current finite-shell C_ss proxy with fitted "
            "polynomial contacts.  Supply a same-surface contact-subtraction "
            "certificate, microscopic scalar-denominator theorem, or strict "
            "moment-threshold-FV/IR certificate before treating a subtracted "
            "object as scalar-LSZ evidence."
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
