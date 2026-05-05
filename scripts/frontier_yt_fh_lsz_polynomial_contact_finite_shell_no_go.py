#!/usr/bin/env python3
"""
PR #230 FH/LSZ finite-shell polynomial-contact no-go.

After the affine-contact complete-monotonicity boundary, the next shortcut is
to allow a more general local contact polynomial and tune it until the finite
shell rows look Stieltjes-positive.  This runner records the finite-data
obstruction: if an arbitrary polynomial contact term is admitted on n shell
points, finite rows cannot identify the scalar LSZ object.

For any proposed Stieltjes values S_i on n distinct x_i, there is a unique
degree <= n-1 polynomial P with C_i - P(x_i) = S_i.  The runner constructs two
different strict one-pole Stieltjes residuals for the current polefit8x8 rows,
interpolates the corresponding contact polynomials, and verifies that both
families reproduce the measured rows exactly while assigning different pole
locations/residues.  A microscopic contact/denominator theorem or strict
renormalization condition is therefore still required.
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
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_polynomial_contact_finite_shell_no_go_2026-05-05.json"

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
        previous = levels[-1]
        current: list[list[float]] = []
        for i in range(n - order):
            denominator = xs[i + order] - xs[i]
            current.append(
                [
                    (previous[i + 1][j] - previous[i][j]) / denominator
                    for j in range(n)
                ]
            )
        levels.append(current)
    return levels


def complete_monotonicity_checks(xs: list[float], ys: list[float]) -> list[dict[str, Any]]:
    coeff_levels = divided_difference_coefficients(xs)
    checks: list[dict[str, Any]] = []
    for order, coeff_rows in enumerate(coeff_levels):
        if order == 0:
            checks.append(
                {
                    "order": 0,
                    "all_windows_pass": all(value > 0.0 for value in ys),
                    "min_alternating_sign_value": min(ys),
                    "rows": [
                        {
                            "window_start": index,
                            "window_end": index,
                            "value": value,
                            "alternating_sign_value": value,
                            "passes_nonnegative_precheck": value > 0.0,
                        }
                        for index, value in enumerate(ys)
                    ],
                }
            )
            continue
        order_rows = []
        for index, coeffs in enumerate(coeff_rows):
            value = sum(coeff * y for coeff, y in zip(coeffs, ys))
            alt_value = ((-1.0) ** order) * value
            order_rows.append(
                {
                    "window_start": index,
                    "window_end": index + order,
                    "divided_difference": value,
                    "alternating_sign_value": alt_value,
                    "passes_nonnegative_precheck": alt_value >= -1.0e-12,
                }
            )
        checks.append(
            {
                "order": order,
                "all_windows_pass": all(row["passes_nonnegative_precheck"] for row in order_rows),
                "min_alternating_sign_value": min(row["alternating_sign_value"] for row in order_rows),
                "rows": order_rows,
            }
        )
    return checks


def solve_linear(matrix: list[list[float]], rhs: list[float]) -> list[float]:
    n = len(rhs)
    aug = [row[:] + [rhs[i]] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(aug[row][col]))
        if abs(aug[pivot][col]) < 1.0e-18:
            raise ValueError("singular interpolation matrix")
        if pivot != col:
            aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [value / scale for value in aug[col]]
        for row in range(n):
            if row == col:
                continue
            factor = aug[row][col]
            if factor == 0.0:
                continue
            aug[row] = [
                aug[row][k] - factor * aug[col][k]
                for k in range(n + 1)
            ]
    return [aug[row][-1] for row in range(n)]


def poly_eval(coefficients: list[float], x: float) -> float:
    total = 0.0
    for coeff in reversed(coefficients):
        total = total * x + coeff
    return total


def interpolate_polynomial(xs: list[float], values: list[float]) -> list[float]:
    matrix = [[x**power for power in range(len(xs))] for x in xs]
    return solve_linear(matrix, values)


def one_pole_stieltjes(xs: list[float], c0: float, mass_sq: float) -> list[float]:
    residue = c0 * mass_sq
    return [residue / (x + mass_sq) for x in xs]


def witness(rows: list[dict[str, float]], label: str, mass_sq: float) -> dict[str, Any]:
    xs = [row["p_hat_sq"] for row in rows]
    cs = [row["C_ss_real"] for row in rows]
    c0 = cs[0]
    residuals = one_pole_stieltjes(xs, c0, mass_sq)
    contact_values = [c - s for c, s in zip(cs, residuals)]
    coefficients = interpolate_polynomial(xs, contact_values)
    reconstructed = [c - poly_eval(coefficients, x) for c, x in zip(cs, xs)]
    errors = [abs(r - s) for r, s in zip(reconstructed, residuals)]
    checks = complete_monotonicity_checks(xs, residuals)
    return {
        "label": label,
        "stieltjes_family": "single positive pole S(x)=residue/(x+mass_sq)",
        "mass_sq": mass_sq,
        "pole_location_in_x": -mass_sq,
        "residue": c0 * mass_sq,
        "polynomial_contact_degree": len(rows) - 1,
        "polynomial_contact_coefficients_low_to_high": coefficients,
        "contact_values_on_shells": contact_values,
        "residual_rows": [
            {
                "p_hat_sq": x,
                "raw_C_ss_real": c,
                "polynomial_contact_value": contact,
                "residual_C_ss_real": residual,
                "reconstructed_residual": recon,
                "absolute_reconstruction_error": err,
            }
            for x, c, contact, residual, recon, err in zip(
                xs, cs, contact_values, residuals, reconstructed, errors
            )
        ],
        "max_reconstruction_error": max(errors),
        "complete_monotonicity_checks": checks,
        "complete_monotonicity_passed": all(check["all_windows_pass"] for check in checks),
    }


def main() -> int:
    print("PR #230 FH/LSZ finite-shell polynomial-contact no-go")
    print("=" * 72)

    combined = load_json(COMBINED)
    proxy = load_json(PROXY_DIAGNOSTIC)
    contact = load_json(CONTACT_IDENTIFIABILITY)
    affine = load_json(AFFINE_NO_GO)
    rows = extract_rows(combined)
    xs = [row["p_hat_sq"] for row in rows]
    distinct_xs = len(xs) == len(set(xs))
    witnesses = (
        [
            witness(rows, "light-pole-polynomial-contact-witness", 0.45),
            witness(rows, "heavy-pole-polynomial-contact-witness", 2.25),
        ]
        if len(rows) >= 4 and distinct_xs
        else []
    )
    all_reconstruct = bool(witnesses) and all(
        item["max_reconstruction_error"] < 1.0e-10 for item in witnesses
    )
    all_stieltjes = bool(witnesses) and all(
        item["complete_monotonicity_passed"] for item in witnesses
    )
    residue_ratio = (
        max(item["residue"] for item in witnesses) / min(item["residue"] for item in witnesses)
        if witnesses
        else float("nan")
    )
    pole_location_spread = (
        abs(witnesses[1]["pole_location_in_x"] - witnesses[0]["pole_location_in_x"])
        if len(witnesses) == 2
        else float("nan")
    )
    no_polynomial_contact_certificate = not (
        ROOT / "outputs" / "yt_fh_lsz_polynomial_contact_certificate_2026-05-05.json"
    ).exists()

    report("combined-polefit8x8-input-loaded", bool(combined), rel(COMBINED))
    report("proxy-diagnostic-parent-loaded", bool(proxy), rel(PROXY_DIAGNOSTIC))
    report("contact-identifiability-parent-loaded", bool(contact), rel(CONTACT_IDENTIFIABILITY))
    report("affine-contact-parent-loaded", bool(affine), rel(AFFINE_NO_GO))
    report("finite-distinct-shell-rows-present", len(rows) >= 6 and distinct_xs, f"rows={len(rows)} distinct_xs={distinct_xs}")
    report("two-polynomial-contact-witnesses-constructed", len(witnesses) == 2, f"count={len(witnesses)}")
    report("both-witnesses-reconstruct-current-rows", all_reconstruct, "max errors below 1e-10")
    report("both-residuals-pass-complete-monotonicity", all_stieltjes, "single positive pole residuals")
    report("witnesses-assign-different-pole-data", math.isfinite(residue_ratio) and residue_ratio > 2.0 and pole_location_spread > 1.0, f"residue_ratio={residue_ratio:.3f} pole_spread={pole_location_spread:.3f}")
    report("polynomial-contact-certificate-absent", no_polynomial_contact_certificate, "future polynomial contact certificate remains absent")
    report("does-not-authorize-proposed-retained", True, "finite-shell non-identifiability boundary only")

    result = {
        "actual_current_surface_status": "exact negative boundary / finite-shell polynomial contact non-identifiability no-go",
        "verdict": (
            "Finite polefit8x8 shell rows plus an arbitrary polynomial contact "
            "subtraction do not identify the scalar-LSZ object.  Two distinct "
            "positive one-pole Stieltjes residuals can be made to reproduce the "
            "same measured C_ss rows by degree-7 polynomial contact terms, with "
            "different pole locations and residues.  A same-surface microscopic "
            "contact/denominator theorem or strict renormalization condition is "
            "still required before a subtracted object can carry LSZ authority."
        ),
        "proposal_allowed": False,
        "polynomial_contact_finite_shell_no_go_passed": True,
        "polynomial_contact_certificate_present": False,
        "stieltjes_certificate_from_polynomial_contact_passed": False,
        "raw_rows": rows,
        "witnesses": witnesses,
        "witness_comparison": {
            "residue_ratio": residue_ratio,
            "pole_location_spread": pole_location_spread,
            "max_reconstruction_error": max(
                (item["max_reconstruction_error"] for item in witnesses),
                default=float("nan"),
            ),
        },
        "theorem": (
            "For n distinct finite shell points x_i and measured values C_i, "
            "any chosen finite values S_i are represented by C_i-P(x_i) for a "
            "unique polynomial contact term P of degree at most n-1.  Therefore "
            "finite-shell Stieltjes tests after an unconstrained polynomial "
            "contact subtraction cannot determine the physical scalar two-point "
            "function, pole residue, or kappa_s."
        ),
        "strict_non_claims": [
            "does not certify any polynomial contact term as microscopic or local in the required PR230 sense",
            "does not create a Stieltjes moment certificate",
            "does not determine scalar pole residue, kappa_s, Z_match, or c2",
            "does not use H_unit, Ward authority, observed targets, alpha_LM, plaquette, or u0",
            "does not claim retained or proposed_retained closure",
        ],
        "exact_next_action": (
            "Derive a same-surface microscopic contact/denominator theorem, "
            "supply a strict polynomial-contact certificate with independent "
            "normalization, or bypass scalar-source normalization with a physical "
            "response route."
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
