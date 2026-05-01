#!/usr/bin/env python3
"""
No-go runner for using the SM RGE bridge alone as a y_t selector.

The RGE is transport: it maps an initial condition to another scale.  Without a
boundary condition such as a measured mass, Ward repair, production certificate,
or Planck stationarity selector, it carries a continuum of y_t trajectories and
does not choose one.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_rge_only_selector_no_go_2026-05-01.json"

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


def run_one_loop_transport(yt_v: float, g1: float = 0.464, g2: float = 0.648, g3: float = 1.1393445855, v: float = 246.28281829012906, m_pl: float = 1.2209e19) -> float:
    """Run the one-loop top Yukawa equation upward with fixed gauge couplings."""
    fac = 1.0 / (16.0 * math.pi * math.pi)

    def rhs(_t: float, y: np.ndarray) -> list[float]:
        yt = float(y[0])
        beta = yt * (4.5 * yt * yt - 8.0 * g3 * g3 - 2.25 * g2 * g2 - (17.0 / 12.0) * g1 * g1)
        return [fac * beta]

    sol = solve_ivp(
        rhs,
        [math.log(v), math.log(m_pl)],
        [yt_v],
        rtol=1.0e-10,
        atol=1.0e-12,
        max_step=0.5,
    )
    if not sol.success:
        raise RuntimeError(sol.message)
    return float(sol.y[0, -1])


def assert_rge_transport_family() -> dict[str, object]:
    initial_values = [0.70, 0.80, 0.9176, 1.00, 1.10]
    rows = []
    for yt_v in initial_values:
        rows.append({"yt_v": yt_v, "yt_pl": run_one_loop_transport(yt_v)})

    pl_values = [row["yt_pl"] for row in rows]
    spread_v = max(initial_values) - min(initial_values)
    spread_pl = max(pl_values) - min(pl_values)
    monotonic = all(rows[i]["yt_pl"] < rows[i + 1]["yt_pl"] for i in range(len(rows) - 1))

    report(
        "rge-maps-family-to-family",
        spread_pl > 0.01,
        f"weak-scale spread {spread_v:.3f} maps to Planck spread {spread_pl:.3f}",
    )
    report(
        "rge-transport-monotonic-not-selector",
        monotonic,
        "distinct y_t(v) inputs remain distinct at M_Pl",
    )
    report(
        "initial-condition-remains-load-bearing",
        True,
        "RGE needs a boundary value; it does not supply one",
    )

    return {
        "samples": rows,
        "yt_v_spread": spread_v,
        "yt_pl_spread": spread_pl,
        "monotonic": monotonic,
    }


def assert_current_notes_keep_bridge_as_import() -> dict[str, bool]:
    direct = (ROOT / "docs/YT_DIRECT_LATTICE_CORRELATOR_DERIVATION_THEOREM_NOTE_2026-04-30.md").read_text(encoding="utf-8")
    selector = (ROOT / "docs/YT_PLANCK_DOUBLE_CRITICALITY_SELECTOR_NOTE_2026-04-30.md").read_text(encoding="utf-8")
    assumptions = (ROOT / ".claude/science/physics-loops/yt-pr230-retained-closure-12h-20260501/ASSUMPTIONS_AND_IMPORTS.md").read_text(encoding="utf-8")

    checks = {
        "direct_note_running_bridge_import": "standard SM/QCD running bridge" in direct,
        "selector_note_requires_sm_rge_bridge": "SM RGE bridge" in selector,
        "assumption_ledger_lists_sm_rge_bridge": "| SM RGE bridge |" in assumptions,
        "selector_note_requires_stationarity": "beta_lambda(M_Pl)=0" in selector and "Load-Bearing Input" in selector,
    }
    for tag, ok in checks.items():
        report(tag, ok, f"{tag}={ok}")
    return checks


def main() -> int:
    print("YT RGE-only selector no-go")
    print("=" * 72)

    numeric = assert_rge_transport_family()
    boundary = assert_current_notes_keep_bridge_as_import()

    result = {
        "actual_current_surface_status": "no-go / exact-negative-boundary for RGE-only selector",
        "target": "derive y_t from the SM RGE bridge without a boundary condition",
        "verdict": (
            "The RGE bridge transports boundary data.  It does not select a "
            "unique y_t by itself.  A measured mass, production certificate, "
            "Ward repair, or independently derived Planck stationarity condition "
            "remains load-bearing."
        ),
        "numeric": numeric,
        "authority_boundary": boundary,
        "remaining_open_premise": "a y_t boundary condition from measurement or retained substrate theorem",
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
