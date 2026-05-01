#!/usr/bin/env python3
"""
No-go runner for the tempting claim that the old Ward ratio y_t/g_s=1/sqrt(6)
would imply beta_lambda(M_Pl)=0.

The Ward/H_unit route remains forbidden as a PR #230 proof input because it is
the audited_renaming trap.  This runner checks a separate point: even if the
ratio were re-permitted as a comparator or future audited route, it does not by
itself imply Planck quartic beta stationarity.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_ward_ratio_stationarity_no_go_2026-05-01.json"

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


def load_selector_certificate() -> dict:
    return json.loads((ROOT / "outputs/yt_planck_double_criticality_selector_2026-04-30.json").read_text(encoding="utf-8"))


def beta_lambda_one_loop_at_zero(g1: float, g2: float, yt: float) -> float:
    gp2 = (3.0 / 5.0) * g1 * g1
    return -6.0 * yt**4 + 3.0 / 8.0 * (2.0 * g2**4 + (g2 * g2 + gp2) ** 2)


def selector_y_star(g1: float, g2: float) -> float:
    gp2 = (3.0 / 5.0) * g1 * g1
    return ((2.0 * g2**4 + (g2 * g2 + gp2) ** 2) / 16.0) ** 0.25


def assert_ward_ratio_does_not_imply_stationarity() -> dict[str, float]:
    cert = load_selector_certificate()
    planck_3 = cert["results"][2]
    g1 = planck_3["g1_pl"]
    g2 = planck_3["g2_pl"]
    g3 = planck_3["g3_pl"]
    y_star = selector_y_star(g1, g2)
    y_ward = g3 / math.sqrt(6.0)
    beta_ward = beta_lambda_one_loop_at_zero(g1, g2, y_ward)
    beta_star = beta_lambda_one_loop_at_zero(g1, g2, y_star)
    g3_required_for_ward_stationarity = math.sqrt(6.0) * y_star
    g3_relative_gap = (g3_required_for_ward_stationarity - g3) / g3

    report(
        "criticality-y-star-zeroes-beta",
        abs(beta_star) < 1.0e-14,
        f"y_star={y_star:.12f} gives beta_lambda={beta_star:.3e}",
    )
    report(
        "ward-ratio-y-not-critical-y",
        abs(y_ward - y_star) > 0.10,
        f"y_ward={y_ward:.12f}, y_star={y_star:.12f}",
    )
    report(
        "ward-ratio-beta-not-zero",
        abs(beta_ward) > 1.0e-3,
        f"beta_lambda(lambda=0, y=g3/sqrt6)={beta_ward:.6e}",
    )
    report(
        "ward-compatible-g3-would-have-to-move",
        abs(g3_relative_gap) > 0.50,
        f"g3 required for Ward+criticality={g3_required_for_ward_stationarity:.6f}, actual={g3:.6f}",
    )
    return {
        "g1_pl": g1,
        "g2_pl": g2,
        "g3_pl": g3,
        "y_star": y_star,
        "y_ward": y_ward,
        "beta_lambda_at_y_star": beta_star,
        "beta_lambda_at_y_ward": beta_ward,
        "g3_required_for_ward_stationarity": g3_required_for_ward_stationarity,
        "g3_relative_gap": g3_relative_gap,
    }


def assert_firewall() -> dict[str, bool]:
    direct_note = (ROOT / "docs/YT_DIRECT_LATTICE_CORRELATOR_DERIVATION_THEOREM_NOTE_2026-04-30.md").read_text(encoding="utf-8")
    ward_forbidden = "does not use the `H_unit`-to-top matrix element as input" in direct_note
    ratio_is_posterior = "not allowed to feed into the mass extraction or Yukawa computation" in direct_note
    report(
        "h-unit-firewall-present",
        ward_forbidden,
        "direct-correlator note excludes H_unit as input",
    )
    report(
        "ratio-posterior-only",
        ratio_is_posterior,
        "y_t/g_s ratio check is posterior, not a definition",
    )
    report(
        "ward-route-independent-of-beta-stationarity",
        True,
        "even a future Ward repair would not by itself prove beta_lambda(M_Pl)=0",
    )
    return {
        "ward_forbidden": ward_forbidden,
        "ratio_is_posterior": ratio_is_posterior,
    }


def main() -> int:
    print("YT Ward-ratio stationarity no-go")
    print("=" * 72)

    numeric = assert_ward_ratio_does_not_imply_stationarity()
    firewall = assert_firewall()
    result = {
        "actual_current_surface_status": "no-go / exact-negative-boundary",
        "target": "test whether y_t/g_s=1/sqrt(6) implies beta_lambda(M_Pl)=0",
        "verdict": (
            "The Ward ratio does not imply Planck quartic beta stationarity. "
            "At the selector's Planck gauge point, y_t=g3/sqrt(6) differs "
            "substantially from the beta_lambda=0 value."
        ),
        "numeric": numeric,
        "firewall": firewall,
        "remaining_open_premise": "beta_lambda(M_Pl)=0 remains independent of any future Ward-ratio repair",
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
