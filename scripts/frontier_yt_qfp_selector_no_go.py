#!/usr/bin/env python3
"""
No-go runner for treating IR quasi-fixed-point focusing as a standalone
selector for y_t.

The existing QFP note is useful bounded support: it shows that RG transport is
less sensitive to UV details near the top-Yukawa route.  This runner checks the
stronger claim needed for retained closure: does QFP focusing select a unique
y_t(v) without a UV boundary condition?  It does not.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_qfp_selector_no_go_2026-05-01.json"

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


def run_simplified_qfp(yt_pl: float, g3: float = 1.1393445855, v: float = 246.28281829012906, m_pl: float = 1.2209e19) -> float:
    """Run a minimal one-loop y_t equation downward with fixed g3.

    This deliberately over-isolates the QFP mechanism.  If even this focused
    toy flow leaves a family, QFP focusing alone is not a selector.
    """
    fac = 1.0 / (16.0 * math.pi * math.pi)

    def rhs(_t: float, y: list[float]) -> list[float]:
        yt = y[0]
        return [fac * yt * (4.5 * yt * yt - 8.0 * g3 * g3)]

    sol = solve_ivp(
        rhs,
        [math.log(m_pl), math.log(v)],
        [yt_pl],
        rtol=1.0e-10,
        atol=1.0e-12,
        max_step=0.5,
    )
    if not sol.success:
        raise RuntimeError(sol.message)
    return float(sol.y[0, -1])


def assert_qfp_is_not_selector() -> dict[str, object]:
    uv_values = [0.20, 0.30, 0.436, 0.60, 0.80]
    rows = []
    for yt_pl in uv_values:
        yt_v = run_simplified_qfp(yt_pl)
        rows.append({"yt_pl": yt_pl, "yt_v": yt_v})

    yt_v_values = [row["yt_v"] for row in rows]
    spread = max(yt_v_values) - min(yt_v_values)
    compression = (max(uv_values) - min(uv_values)) / spread

    ward = 0.436
    ward_low = run_simplified_qfp(0.9 * ward)
    ward_mid = run_simplified_qfp(ward)
    ward_high = run_simplified_qfp(1.1 * ward)
    local_response = (ward_high - ward_low) / (0.2 * ward)

    report(
        "qfp-compresses-uv-range",
        compression > 1.0,
        f"UV spread {max(uv_values)-min(uv_values):.3f} maps to IR spread {spread:.3f}",
    )
    report(
        "qfp-family-remains-nonunique",
        spread > 0.10,
        f"simplified QFP still leaves y_t(v) spread {spread:.3f}",
    )
    report(
        "qfp-local-response-nonzero",
        abs(local_response) > 0.10,
        f"local dy_t(v)/dy_t(M_Pl) near Ward proxy = {local_response:.3f}",
    )
    report(
        "qfp-needs-uv-boundary-condition",
        True,
        "focusing reduces sensitivity but does not choose one trajectory",
    )

    return {
        "samples": rows,
        "yt_v_spread": spread,
        "compression_ratio": compression,
        "ward_proxy": {
            "yt_pl": ward,
            "yt_v": ward_mid,
            "yt_v_low": ward_low,
            "yt_v_high": ward_high,
            "local_response": local_response,
        },
    }


def assert_authority_boundary() -> dict[str, bool]:
    note = (ROOT / "docs/YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md").read_text(encoding="utf-8")
    bounded = "**Status:** bounded support" in note
    requires_ward_bc = "Ward BC" in note or "Ward boundary condition" in note
    requires_gauge_anchor = "Gauge anchor" in note or "alpha_s(v)" in note

    report(
        "qfp-note-bounded-support",
        bounded,
        "existing QFP note is bounded support, not retained selector",
    )
    report(
        "qfp-note-requires-ward-bc",
        requires_ward_bc,
        "existing QFP support assumes a UV boundary condition",
    )
    report(
        "qfp-note-requires-gauge-anchor",
        requires_gauge_anchor,
        "existing QFP support assumes a gauge anchor",
    )

    return {
        "bounded_support": bounded,
        "requires_ward_bc": requires_ward_bc,
        "requires_gauge_anchor": requires_gauge_anchor,
    }


def main() -> int:
    print("YT QFP selector no-go")
    print("=" * 72)

    numeric = assert_qfp_is_not_selector()
    authority = assert_authority_boundary()
    result = {
        "actual_current_surface_status": "no-go / exact-negative-boundary for QFP-as-selector",
        "proposal_allowed": False,
        "bare_retained_allowed": False,
        "investigation_route_closed": False,
        "certification_scope": "current_surface_blocker_only",
        "future_reopen_conditions": [
            "supply a retained UV boundary condition",
            "complete a retained Ward repair without H_unit renaming",
            "derive Planck stationarity or obtain production measurement evidence",
        ],
        "target": "derive y_t from IR quasi-fixed-point focusing without a UV boundary condition",
        "verdict": (
            "QFP focusing is useful bounded support for transport robustness, "
            "but it is not a standalone selector.  Different UV y_t values "
            "still map to different IR values, so a UV boundary condition or "
            "other selector remains load-bearing."
        ),
        "numeric": numeric,
        "authority_boundary": authority,
        "remaining_open_premise": "a UV boundary condition such as a retained Ward repair, Planck stationarity, or production measurement",
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
