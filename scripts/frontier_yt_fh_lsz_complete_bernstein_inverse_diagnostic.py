#!/usr/bin/env python3
"""
PR #230 FH/LSZ complete-Bernstein inverse diagnostic.

For an unsubtracted positive Stieltjes scalar propagator C(x), with x = q_hat^2,
the inverse denominator Gamma(x) = 1 / C(x) is a complete Bernstein function
when the inverse is well defined.  A necessary first check is monotone
non-decrease of Gamma(x).  The completed polefit8x8 proxy has Gamma decreasing
across every adjacent shell, so the current proxy cannot be promoted into a
strict scalar-LSZ denominator certificate.

This is an exact diagnostic boundary only.  It does not define y_t, does not
claim scalar-LSZ closure, and does not create the future moment/denominator
certificate.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
COMBINED = ROOT / "outputs" / "yt_pr230_fh_lsz_polefit8x8_L12_T24_chunked_combined_2026-05-04.json"
POSTPROCESSOR = ROOT / "outputs" / "yt_fh_lsz_polefit8x8_postprocessor_2026-05-04.json"
STIELTJES_PROXY = ROOT / "outputs" / "yt_fh_lsz_polefit8x8_stieltjes_proxy_diagnostic_2026-05-05.json"
STIELTJES_GATE = ROOT / "outputs" / "yt_fh_lsz_stieltjes_moment_certificate_gate_2026-05-05.json"
PADE_GATE = ROOT / "outputs" / "yt_fh_lsz_pade_stieltjes_bounds_gate_2026-05-05.json"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_complete_bernstein_inverse_diagnostic_2026-05-05.json"

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
        gamma = row.get("Gamma_ss_real_proxy")
        if finite(x) and finite(c) and float(c) > 0.0:
            gamma_value = float(gamma) if finite(gamma) else 1.0 / float(c)
            rows.append(
                {
                    "p_hat_sq": float(x),
                    "C_ss_real": float(c),
                    "C_ss_real_stderr": float(err) if finite(err) else float("nan"),
                    "Gamma_ss_real_proxy": gamma_value,
                }
            )
    return sorted(rows, key=lambda item: item["p_hat_sq"])


def adjacent_inverse_monotonicity(rows: list[dict[str, float]]) -> list[dict[str, Any]]:
    violations: list[dict[str, Any]] = []
    checks: list[dict[str, Any]] = []
    for left, right in zip(rows, rows[1:]):
        dx = right["p_hat_sq"] - left["p_hat_sq"]
        dgamma = right["Gamma_ss_real_proxy"] - left["Gamma_ss_real_proxy"]
        slope = dgamma / dx if dx > 0.0 else float("nan")
        check = {
            "from_p_hat_sq": left["p_hat_sq"],
            "to_p_hat_sq": right["p_hat_sq"],
            "delta_Gamma_ss_real_proxy": dgamma,
            "slope_delta_Gamma_over_delta_x": slope,
        }
        checks.append(check)
        if dx > 0.0 and dgamma < 0.0:
            violations.append(check)
    return violations


def divided_differences(values: list[tuple[float, float]]) -> list[list[float]]:
    table: list[list[float]] = [[y for _, y in values]]
    xs = [x for x, _ in values]
    for order in range(1, len(values)):
        prev = table[-1]
        row = []
        for index in range(len(prev) - 1):
            denom = xs[index + order] - xs[index]
            row.append((prev[index + 1] - prev[index]) / denom)
        table.append(row)
    return table


def complete_bernstein_witness() -> dict[str, Any]:
    """A small positive witness showing the intended future-shape check."""

    mass_sq = 0.42
    residue = 1.15
    continuum_mass_sq = 2.8
    continuum_weight = 0.25
    xs = [0.0, 0.25, 0.55, 0.90, 1.40, 2.00]
    rows = []
    for x in xs:
        c = residue / (x + mass_sq) + continuum_weight / (x + continuum_mass_sq)
        rows.append({"x": x, "C": c, "Gamma": 1.0 / c})
    slopes = [
        (right["Gamma"] - left["Gamma"]) / (right["x"] - left["x"])
        for left, right in zip(rows, rows[1:])
    ]
    dd = divided_differences([(row["x"], row["Gamma"]) for row in rows])
    return {
        "model": "C(x)=R/(x+m2)+W/(x+M2), Gamma=1/C",
        "rows": rows,
        "all_adjacent_gamma_slopes_positive": all(slope > 0.0 for slope in slopes),
        "adjacent_gamma_slopes": slopes,
        "first_divided_differences": dd[1],
        "second_divided_differences": dd[2],
        "interpretation": (
            "This witness is not PR230 evidence.  It records the mathematical "
            "shape expected from a future certified positive Stieltjes scalar "
            "object before inverse-denominator LSZ use."
        ),
    }


def theorem_statement() -> str:
    return (
        "A nonzero positive Stieltjes function C(x) has reciprocal Gamma(x)=1/C(x) "
        "in the complete-Bernstein class.  In particular Gamma is nonnegative and "
        "monotone non-decreasing on x>0.  Therefore a scalar two-point proxy whose "
        "inverse denominator decreases with q_hat^2 cannot be a strict "
        "unsubtracted positive Stieltjes/LSZ denominator certificate."
    )


def main() -> int:
    print("PR #230 FH/LSZ complete-Bernstein inverse diagnostic")
    print("=" * 72)

    combined = load_json(COMBINED)
    postprocessor = load_json(POSTPROCESSOR)
    stieltjes_proxy = load_json(STIELTJES_PROXY)
    stieltjes_gate = load_json(STIELTJES_GATE)
    pade_gate = load_json(PADE_GATE)
    rows = extract_rows(combined)
    violations = adjacent_inverse_monotonicity(rows)
    all_gamma_positive = all(row["Gamma_ss_real_proxy"] > 0.0 for row in rows)
    all_adjacent_violate = bool(rows) and len(violations) == max(len(rows) - 1, 0)
    gamma_span = (
        max(row["Gamma_ss_real_proxy"] for row in rows)
        - min(row["Gamma_ss_real_proxy"] for row in rows)
        if rows
        else float("nan")
    )
    witness = complete_bernstein_witness()
    stieltjes_proxy_already_blocks = (
        "fails Stieltjes monotonicity"
        in str(stieltjes_proxy.get("actual_current_surface_status", ""))
        and stieltjes_proxy.get("stieltjes_proxy_certificate_passed") is False
        and stieltjes_proxy.get("proposal_allowed") is False
    )
    strict_moment_absent = (
        stieltjes_gate.get("moment_certificate_gate_passed") is False
        and stieltjes_gate.get("proposal_allowed") is False
    )
    pade_bounds_absent = (
        pade_gate.get("pade_stieltjes_bounds_gate_passed") is False
        and pade_gate.get("proposal_allowed") is False
    )
    inverse_certificate_passed = False

    report("combined-polefit8x8-input-loaded", bool(combined), rel(COMBINED))
    report("postprocessor-parent-loaded", bool(postprocessor), rel(POSTPROCESSOR))
    report("stieltjes-proxy-parent-loaded", bool(stieltjes_proxy), rel(STIELTJES_PROXY))
    report("strict-stieltjes-moment-gate-loaded", bool(stieltjes_gate), rel(STIELTJES_GATE))
    report("pade-stieltjes-bounds-gate-loaded", bool(pade_gate), rel(PADE_GATE))
    report("finite-positive-inverse-rows-present", len(rows) >= 4 and all_gamma_positive, f"rows={len(rows)} gamma_span={gamma_span:.6g}")
    report("inverse-monotonicity-violations-detected", bool(violations), f"violations={len(violations)}")
    report("all-adjacent-inverse-intervals-violate", all_adjacent_violate, f"rows={len(rows)}")
    report("complete-bernstein-positive-witness-passes", witness["all_adjacent_gamma_slopes_positive"], "synthetic Stieltjes witness")
    report("stieltjes-proxy-already-blocks-current-c-ss", stieltjes_proxy_already_blocks, stieltjes_proxy.get("actual_current_surface_status", ""))
    report("strict-moment-certificate-still-absent", strict_moment_absent, stieltjes_gate.get("actual_current_surface_status", ""))
    report("pade-bounds-certificate-still-absent", pade_bounds_absent, pade_gate.get("actual_current_surface_status", ""))
    report("current-proxy-not-complete-bernstein-certificate", not inverse_certificate_passed, "diagnostic boundary only")
    report("does-not-authorize-proposed-retained", True, "proposal_allowed=false")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / current polefit8x8 inverse proxy fails "
            "complete-Bernstein monotonicity"
        ),
        "verdict": (
            "The completed L12 eight-mode/x8 C_ss proxy also fails the inverse "
            "denominator test: Gamma_ss=1/C_ss is positive but decreases with "
            "q_hat^2 across every adjacent shell.  A reciprocal of a positive "
            "Stieltjes scalar propagator must be a complete Bernstein function, "
            "hence monotone non-decreasing.  The current finite-shell proxy is "
            "therefore not a strict scalar-LSZ denominator certificate."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The current inverse proxy violates a necessary complete-Bernstein "
            "condition and still lacks contact/subtraction authority, threshold "
            "control, FV/IR control, and a strict moment or denominator certificate."
        ),
        "bare_retained_allowed": False,
        "complete_bernstein_inverse_certificate_passed": inverse_certificate_passed,
        "theorem": theorem_statement(),
        "input_rows": rows,
        "inverse_monotonicity_violations": violations,
        "violation_summary": {
            "violation_count": len(violations),
            "all_adjacent_intervals_violate_non_decrease": all_adjacent_violate,
            "gamma_span": gamma_span,
        },
        "positive_witness": witness,
        "parent_certificates": {
            "polefit8x8_combined": rel(COMBINED),
            "polefit8x8_postprocessor": rel(POSTPROCESSOR),
            "polefit8x8_stieltjes_proxy_diagnostic": rel(STIELTJES_PROXY),
            "stieltjes_moment_certificate_gate": rel(STIELTJES_GATE),
            "pade_stieltjes_bounds_gate": rel(PADE_GATE),
        },
        "future_positive_route": [
            "derive a certified contact-subtracted scalar two-point object and rerun Stieltjes plus complete-Bernstein checks",
            "derive a microscopic scalar denominator theorem whose inverse passes complete-Bernstein/Pick/Hankel tests with threshold and FV/IR authority",
            "or bypass scalar-source LSZ through certified O_H/C_sH/C_HH rows or same-source W/Z response rows",
        ],
        "strict_non_claims": [
            "does not claim scalar LSZ closure",
            "does not create outputs/yt_fh_lsz_stieltjes_moment_certificate_2026-05-05.json",
            "does not create outputs/yt_fh_lsz_pade_stieltjes_bounds_certificate_2026-05-05.json",
            "does not define y_t_bare",
            "does not set kappa_s, c2, or Z_match to one",
            "does not use H_unit, Ward authority, alpha_LM, plaquette, u0, or observed targets",
        ],
        "exact_next_action": (
            "Do not use the current polefit8x8 Gamma_ss proxy as an LSZ "
            "denominator.  Supply a certified contact-subtracted scalar object "
            "or a microscopic denominator theorem, then rerun Stieltjes, Pade, "
            "and complete-Bernstein inverse checks."
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
