#!/usr/bin/env python3
"""
PR #230 FH/LSZ polefit8x8 Stieltjes proxy diagnostic.

This runner tests whether the current finite-shell polefit8x8 scalar-source
proxy can be promoted into the strict Stieltjes moment certificate.  It cannot:
a positive Stieltjes two-point function is non-increasing in Euclidean q^2,
while the current combined C_ss proxy increases across the available shells.

This is a diagnostic boundary only.  It does not claim scalar LSZ closure and
does not create the future strict moment-certificate artifact.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
COMBINED = ROOT / "outputs" / "yt_pr230_fh_lsz_polefit8x8_L12_T24_chunked_combined_2026-05-04.json"
POSTPROCESSOR = ROOT / "outputs" / "yt_fh_lsz_polefit8x8_postprocessor_2026-05-04.json"
STIELTJES_GATE = ROOT / "outputs" / "yt_fh_lsz_stieltjes_moment_certificate_gate_2026-05-05.json"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_polefit8x8_stieltjes_proxy_diagnostic_2026-05-05.json"

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
        if finite(x) and finite(c):
            rows.append(
                {
                    "p_hat_sq": float(x),
                    "C_ss_real": float(c),
                    "C_ss_real_stderr": float(err) if finite(err) else float("nan"),
                    "Gamma_ss_real_proxy": float(gamma) if finite(gamma) else float("nan"),
                }
            )
    return sorted(rows, key=lambda item: item["p_hat_sq"])


def adjacent_monotonicity(rows: list[dict[str, float]]) -> list[dict[str, Any]]:
    violations: list[dict[str, Any]] = []
    for left, right in zip(rows, rows[1:]):
        dx = right["p_hat_sq"] - left["p_hat_sq"]
        dc = right["C_ss_real"] - left["C_ss_real"]
        left_err = left["C_ss_real_stderr"]
        right_err = right["C_ss_real_stderr"]
        if math.isfinite(left_err) and math.isfinite(right_err):
            sigma = math.hypot(left_err, right_err)
        else:
            sigma = float("nan")
        z_score = dc / sigma if math.isfinite(sigma) and sigma > 0.0 else float("nan")
        if dx > 0.0 and dc > 0.0:
            violations.append(
                {
                    "from_p_hat_sq": left["p_hat_sq"],
                    "to_p_hat_sq": right["p_hat_sq"],
                    "delta_C_ss_real": dc,
                    "combined_stderr": sigma,
                    "z_score_if_stderr_trusted": z_score,
                }
            )
    return violations


def theorem_statement() -> str:
    return (
        "For C(x)=int dmu(s)/(x+s) with dmu(s)>=0 and x=q_hat^2>=0, "
        "C(x2)-C(x1)=-(x2-x1) int dmu(s)/((x2+s)(x1+s)) <= 0 whenever "
        "x2>x1.  Any unsubtracted positive Stieltjes scalar two-point "
        "certificate must therefore pass monotonic non-increase before its "
        "Hankel moment tests can be load-bearing."
    )


def main() -> int:
    print("PR #230 FH/LSZ polefit8x8 Stieltjes proxy diagnostic")
    print("=" * 72)

    combined = load_json(COMBINED)
    postprocessor = load_json(POSTPROCESSOR)
    stieltjes_gate = load_json(STIELTJES_GATE)
    rows = extract_rows(combined)
    violations = adjacent_monotonicity(rows)
    positive_rows = all(row["C_ss_real"] > 0.0 for row in rows)
    shells = {round(row["p_hat_sq"], 12) for row in rows}
    zero_shell = any(abs(row["p_hat_sq"]) < 1.0e-12 for row in rows)
    max_z = max(
        (item["z_score_if_stderr_trusted"] for item in violations if math.isfinite(item["z_score_if_stderr_trusted"])),
        default=float("nan"),
    )
    min_z = min(
        (item["z_score_if_stderr_trusted"] for item in violations if math.isfinite(item["z_score_if_stderr_trusted"])),
        default=float("nan"),
    )
    statistically_strong = math.isfinite(min_z) and min_z > 5.0

    report("combined-polefit8x8-input-loaded", bool(combined), rel(COMBINED))
    report("postprocessor-parent-loaded", bool(postprocessor), rel(POSTPROCESSOR))
    report("stieltjes-gate-parent-loaded", bool(stieltjes_gate), rel(STIELTJES_GATE))
    report("finite-positive-c-ss-rows-present", len(rows) >= 4 and positive_rows, f"rows={len(rows)} shells={len(shells)}")
    report("zero-shell-present", zero_shell, f"zero_shell={zero_shell}")
    report("stieltjes-monotonicity-violations-detected", bool(violations), f"violations={len(violations)}")
    report("violations-are-large-relative-to-row-stderr", statistically_strong, f"min_z={min_z:.3f} max_z={max_z:.3f}")
    report("current-proxy-not-strict-moment-certificate", True, "future strict certificate remains absent")
    report("does-not-authorize-proposed-retained", True, "diagnostic boundary only")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / current polefit8x8 C_ss proxy fails "
            "Stieltjes monotonicity"
        ),
        "verdict": (
            "The current eight-mode/x8 finite-shell C_ss proxy cannot be used as "
            "the strict positive Stieltjes scalar two-point certificate.  The "
            "measured proxy is positive but increases with q_hat^2 across every "
            "adjacent shell, while an unsubtracted positive Stieltjes transform "
            "must be non-increasing.  This blocks the tempting shortcut from "
            "finite-shell polefit8x8 rows to scalar-LSZ model-class authority."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The current C_ss proxy fails a necessary Stieltjes monotonicity check "
            "and still lacks contact/subtraction authority, threshold control, "
            "FV/IR control, and scalar-denominator authority."
        ),
        "stieltjes_proxy_certificate_passed": False,
        "theorem": theorem_statement(),
        "input_rows": rows,
        "monotonicity_violations": violations,
        "violation_summary": {
            "violation_count": len(violations),
            "min_z_score_if_stderr_trusted": min_z,
            "max_z_score_if_stderr_trusted": max_z,
            "all_adjacent_intervals_violate_nonincrease": len(violations) == max(len(rows) - 1, 0),
        },
        "parent_certificates": {
            "polefit8x8_combined": rel(COMBINED),
            "polefit8x8_postprocessor": rel(POSTPROCESSOR),
            "stieltjes_moment_certificate_gate": rel(STIELTJES_GATE),
        },
        "future_positive_route": [
            "derive a contact/subtraction or microscopic scalar-denominator authority and rerun this check on that certified scalar two-point object",
            "or produce the strict Stieltjes moment certificate with threshold-gap and FV/IR control required by the existing gate",
            "or bypass scalar-source LSZ through a certified physical-response/source-overlap route",
        ],
        "strict_non_claims": [
            "does not claim scalar LSZ closure",
            "does not create outputs/yt_fh_lsz_stieltjes_moment_certificate_2026-05-05.json",
            "does not define y_t_bare",
            "does not set kappa_s, c2, or Z_match to one",
            "does not use H_unit, Ward authority, alpha_LM, plaquette, u0, or observed targets",
        ],
        "exact_next_action": (
            "Do not use the current polefit8x8 C_ss proxy as the Stieltjes "
            "certificate.  Supply a certified contact-subtracted scalar "
            "two-point object or a microscopic denominator theorem, then rerun "
            "the strict moment-certificate gate."
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
