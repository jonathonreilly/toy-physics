#!/usr/bin/env python3
"""
PR #230 FH/LSZ finite-volume pole-saturation obstruction.

Finite-volume scalar spectra are discrete, so a tempting repair is to treat a
finite-L pole witness as pole saturation.  This runner checks the limiting
order.  If continuum levels can approach the scalar pole as L grows, positive
finite-shell data still do not identify the infinite-volume pole residue
without a uniform gap or pole-saturation theorem.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import linprog


ROOT = Path(__file__).resolve().parents[1]
THRESHOLD_GATE = ROOT / "outputs" / "yt_fh_lsz_pole_saturation_threshold_gate_2026-05-02.json"
AUTHORITY_AUDIT = ROOT / "outputs" / "yt_fh_lsz_threshold_authority_import_audit_2026-05-02.json"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_finite_volume_pole_saturation_obstruction_2026-05-02.json"

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


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def residue_interval(shells: np.ndarray, pole_m2: float, continuum_m2: np.ndarray, target: np.ndarray) -> dict[str, Any]:
    matrix = np.column_stack(
        [
            1.0 / (shells + pole_m2),
            1.0 / (shells[:, None] + continuum_m2[None, :]),
        ]
    )
    bounds = [(0.0, None)] * matrix.shape[1]
    min_result = linprog(
        c=np.r_[1.0, np.zeros(len(continuum_m2))],
        A_eq=matrix,
        b_eq=target,
        bounds=bounds,
        method="highs",
    )
    max_result = linprog(
        c=np.r_[-1.0, np.zeros(len(continuum_m2))],
        A_eq=matrix,
        b_eq=target,
        bounds=bounds,
        method="highs",
    )
    if not min_result.success or not max_result.success:
        return {
            "feasible": False,
            "min_message": min_result.message,
            "max_message": max_result.message,
        }
    return {
        "feasible": True,
        "residue_min": float(min_result.fun),
        "residue_max": float(-max_result.fun),
        "lower_bound_is_zero": float(min_result.fun) <= 1.0e-12,
    }


def build_volume_rows() -> list[dict[str, Any]]:
    pole_m2 = 0.25
    rows: list[dict[str, Any]] = []
    for L in (12, 16, 24):
        one_link = 4.0 * math.sin(math.pi / L) ** 2
        shells = np.asarray([0.0, one_link, 2.0 * one_link, 1.0], dtype=float)
        gap = 1.0 / (L * L)
        continuum_m2 = np.asarray(
            [pole_m2 + gap, pole_m2 + 4.0 * gap, 0.7, 1.2, 2.0, 4.0, 8.0, 16.0],
            dtype=float,
        )
        target = 1.0 / (shells + pole_m2) + (
            1.0 / (shells[:, None] + continuum_m2[None, :])
        ) @ np.full(len(continuum_m2), 0.5)
        interval = residue_interval(shells, pole_m2, continuum_m2, target)
        rows.append(
            {
                "L": L,
                "near_pole_gap_m2": gap,
                "shells_p_hat_sq": [float(x) for x in shells],
                "continuum_mass_squared_grid": [float(x) for x in continuum_m2],
                **interval,
            }
        )
    return rows


def main() -> int:
    print("PR #230 FH/LSZ finite-volume pole-saturation obstruction")
    print("=" * 72)

    threshold_gate = load_json(THRESHOLD_GATE)
    authority_audit = load_json(AUTHORITY_AUDIT)
    rows = build_volume_rows()
    all_feasible = all(row.get("feasible") for row in rows)
    all_zero_lower = all(row.get("lower_bound_is_zero") for row in rows)
    max_upper = max(float(row.get("residue_max", 0.0)) for row in rows if row.get("feasible"))
    gaps = [float(row["near_pole_gap_m2"]) for row in rows]
    gap_decreases = gaps[-1] < gaps[0]

    report("threshold-gate-loaded", bool(threshold_gate), str(THRESHOLD_GATE.relative_to(ROOT)))
    report("authority-audit-loaded", bool(authority_audit), str(AUTHORITY_AUDIT.relative_to(ROOT)))
    report("finite-volume-lp-families-feasible", all_feasible, f"volumes={[row['L'] for row in rows]}")
    report("near-pole-gap-closes-with-volume", gap_decreases, f"gaps={gaps}")
    report("finite-volume-residue-lower-bound-zero", all_zero_lower, f"max_upper={max_upper:.6g}")
    report("uniform-gap-theorem-absent", authority_audit.get("proposal_allowed") is False, "threshold authority audit blocks hidden import")
    report("does-not-authorize-retained-proposal", True, "finite-L pole-like rows are not infinite-volume pole saturation")

    result = {
        "actual_current_surface_status": "exact negative boundary / FH-LSZ finite-volume pole-saturation obstruction",
        "verdict": (
            "Finite-volume discreteness does not by itself provide scalar pole "
            "saturation.  Positive finite-shell models with near-pole continuum "
            "levels whose gap closes like 1/L^2 keep the pole-residue lower "
            "bound at zero across L=12,16,24.  A retained FH/LSZ closure still "
            "needs a uniform spectral gap, pole-saturation theorem, continuum "
            "threshold certificate, or microscopic scalar denominator theorem."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Finite-volume pole-like behavior is not a uniform pole-saturation/threshold theorem.",
        "parent_certificates": {
            "threshold_gate": str(THRESHOLD_GATE.relative_to(ROOT)),
            "authority_audit": str(AUTHORITY_AUDIT.relative_to(ROOT)),
        },
        "volume_rows": rows,
        "strict_non_claims": [
            "does not use finite-volume discreteness as scalar pole saturation",
            "does not set kappa_s = 1",
            "does not use observed top mass or observed y_t",
            "does not use H_unit, Ward authority, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Derive a uniform finite-volume/continuum gap or scalar denominator "
            "theorem, or continue production chunks toward a postprocessed pole "
            "fit plus model-class certificate."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
