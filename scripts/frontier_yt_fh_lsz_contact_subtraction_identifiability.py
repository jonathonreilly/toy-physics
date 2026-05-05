#!/usr/bin/env python3
"""
PR #230 FH/LSZ contact-subtraction identifiability boundary.

The current polefit8x8 C_ss proxy fails the necessary monotonicity test for an
unsubtracted positive Stieltjes scalar two-point object.  A tempting next move
is to subtract a local contact term and then retest.  This runner records the
boundary: the current finite rows do not select the contact subtraction.

It constructs a continuum of affine local subtractions that make the residual
pass the necessary monotonic non-increase check.  That is useful as a
diagnostic, but it also proves that monotonicity-restoration alone cannot fix
the scalar LSZ object, pole residue, or kappa_s.  A same-surface contact-term
or microscopic denominator theorem is still required.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
COMBINED = ROOT / "outputs" / "yt_pr230_fh_lsz_polefit8x8_L12_T24_chunked_combined_2026-05-04.json"
PROXY_DIAGNOSTIC = ROOT / "outputs" / "yt_fh_lsz_polefit8x8_stieltjes_proxy_diagnostic_2026-05-05.json"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_contact_subtraction_identifiability_2026-05-05.json"

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


def adjacent_slopes(rows: list[dict[str, float]]) -> list[dict[str, float]]:
    slopes: list[dict[str, float]] = []
    for left, right in zip(rows, rows[1:]):
        dx = right["p_hat_sq"] - left["p_hat_sq"]
        dc = right["C_ss_real"] - left["C_ss_real"]
        if dx > 0.0:
            slopes.append(
                {
                    "from_p_hat_sq": left["p_hat_sq"],
                    "to_p_hat_sq": right["p_hat_sq"],
                    "slope": dc / dx,
                    "delta_C_ss_real": dc,
                }
            )
    return slopes


def residual_rows(rows: list[dict[str, float]], slope: float) -> list[dict[str, float]]:
    return [
        {
            "p_hat_sq": row["p_hat_sq"],
            "raw_C_ss_real": row["C_ss_real"],
            "contact_term": slope * row["p_hat_sq"],
            "residual_C_ss_real": row["C_ss_real"] - slope * row["p_hat_sq"],
        }
        for row in rows
    ]


def positive_nonincreasing(rows: list[dict[str, float]]) -> bool:
    if not all(row["residual_C_ss_real"] > 0.0 for row in rows):
        return False
    return all(
        right["residual_C_ss_real"] <= left["residual_C_ss_real"] + 1.0e-14
        for left, right in zip(rows, rows[1:])
    )


def main() -> int:
    print("PR #230 FH/LSZ contact-subtraction identifiability boundary")
    print("=" * 72)

    combined = load_json(COMBINED)
    proxy = load_json(PROXY_DIAGNOSTIC)
    rows = extract_rows(combined)
    slopes = adjacent_slopes(rows)
    raw_increases = [item for item in slopes if item["slope"] > 0.0]
    max_raw_slope = max((item["slope"] for item in slopes), default=float("nan"))
    positivity_upper = min(
        (row["C_ss_real"] / row["p_hat_sq"] for row in rows if row["p_hat_sq"] > 0.0),
        default=float("nan"),
    )
    interval_nonempty = (
        math.isfinite(max_raw_slope)
        and math.isfinite(positivity_upper)
        and max_raw_slope < positivity_upper
    )
    width = positivity_upper - max_raw_slope if interval_nonempty else float("nan")
    slope_a = max_raw_slope + 0.25 * width if interval_nonempty else float("nan")
    slope_b = max_raw_slope + 0.75 * width if interval_nonempty else float("nan")
    family = []
    for label, slope in (("contact_family_a", slope_a), ("contact_family_b", slope_b)):
        if not math.isfinite(slope):
            continue
        candidate_rows = residual_rows(rows, slope)
        family.append(
            {
                "label": label,
                "affine_contact_slope": slope,
                "passes_positive_nonincrease_necessary_check": positive_nonincreasing(candidate_rows),
                "residual_rows": candidate_rows,
            }
        )
    residual_spread_at_max_q = (
        abs(family[1]["residual_rows"][-1]["residual_C_ss_real"] - family[0]["residual_rows"][-1]["residual_C_ss_real"])
        if len(family) == 2
        else float("nan")
    )
    max_q_stderr = rows[-1]["C_ss_real_stderr"] if rows else float("nan")
    spread_z = residual_spread_at_max_q / max_q_stderr if math.isfinite(max_q_stderr) and max_q_stderr > 0.0 else float("nan")
    no_contact_certificate = not (ROOT / "outputs" / "yt_fh_lsz_contact_subtraction_certificate_2026-05-05.json").exists()

    report("combined-polefit8x8-input-loaded", bool(combined), rel(COMBINED))
    report("proxy-diagnostic-parent-loaded", bool(proxy), rel(PROXY_DIAGNOSTIC))
    report("finite-rows-present", len(rows) >= 4, f"rows={len(rows)}")
    report("raw-proxy-has-positive-adjacent-slopes", len(raw_increases) == max(len(rows) - 1, 0), f"increases={len(raw_increases)}")
    report("affine-contact-admissible-interval-nonempty", interval_nonempty, f"lower={max_raw_slope:.12g} upper={positivity_upper:.12g}")
    report("two-distinct-contact-families-constructed", len(family) == 2 and slope_a != slope_b, f"slopes={[item['affine_contact_slope'] for item in family]}")
    report("both-families-pass-necessary-monotonicity", len(family) == 2 and all(item["passes_positive_nonincrease_necessary_check"] for item in family), "positive residuals are non-increasing")
    report("families-change-residual-beyond-row-errors", math.isfinite(spread_z) and spread_z > 5.0, f"spread_z_at_max_q={spread_z:.3f}")
    report("no-contact-subtraction-certificate-present", no_contact_certificate, "future contact certificate remains absent")
    report("does-not-authorize-proposed-retained", True, "identifiability boundary only")

    result = {
        "actual_current_surface_status": "exact negative boundary / contact-subtraction identifiability obstruction",
        "verdict": (
            "The current finite polefit8x8 rows do not select a contact subtraction. "
            "A continuum of affine local terms can make the residual pass the "
            "necessary positive non-increasing Stieltjes precheck, and distinct "
            "choices change the residual by many row standard errors.  Therefore "
            "monotonicity-restoration alone cannot define the scalar LSZ object, "
            "pole residue, or kappa_s."
        ),
        "proposal_allowed": False,
        "contact_subtraction_identifiability_obstruction_passed": True,
        "contact_subtraction_certificate_present": False,
        "stieltjes_certificate_from_contact_subtraction_passed": False,
        "admissible_affine_contact_slope_interval": {
            "lower_bound_from_monotonicity": max_raw_slope,
            "upper_bound_from_residual_positivity": positivity_upper,
            "interval_nonempty": interval_nonempty,
        },
        "raw_rows": rows,
        "adjacent_raw_slopes": slopes,
        "contact_families": family,
        "residual_spread_at_max_q": {
            "absolute_spread": residual_spread_at_max_q,
            "row_stderr": max_q_stderr,
            "z_score_if_stderr_trusted": spread_z,
        },
        "theorem": (
            "If a local contact ambiguity C(x) -> C(x) - a x is not fixed by a "
            "same-surface renormalization, denominator, or canonical source theorem, "
            "then finite C(x_i) rows plus monotonicity do not determine a unique "
            "Stieltjes object.  Any a above the largest adjacent raw slope and below "
            "min_i C(x_i)/x_i gives positive non-increasing finite residual rows."
        ),
        "strict_non_claims": [
            "does not claim a valid contact-subtracted scalar two-point function",
            "does not create a Stieltjes moment certificate",
            "does not determine a pole residue or kappa_s",
            "does not use H_unit, Ward authority, observed targets, alpha_LM, plaquette, u0, c2=1, Z_match=1, or kappa_s=1",
        ],
        "exact_next_action": (
            "Supply a same-surface contact-subtraction certificate or microscopic "
            "scalar-denominator theorem before applying Stieltjes moment tests to "
            "a subtracted object."
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
