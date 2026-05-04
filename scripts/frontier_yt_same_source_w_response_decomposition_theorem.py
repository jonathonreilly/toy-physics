#!/usr/bin/env python3
"""
PR #230 same-source W-response decomposition theorem.

This is a physics theorem for the non-chunk route.  It shows exactly what a
same-source W-mass response would do when paired with the FH/LSZ top response:
the unknown scalar-source normalization cancels, but any orthogonal neutral
top-coupled scalar contribution remains as a measurable correction.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_same_source_w_response_decomposition_theorem_2026-05-04.json"

PARENTS = {
    "ew_higgs_gauge_mass": "docs/EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md",
    "sm_one_higgs_selection": "docs/SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md",
    "wz_same_source_action_gate": "outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json",
    "same_source_sector_overlap_obstruction": "outputs/yt_same_source_sector_overlap_identity_obstruction_2026-05-02.json",
    "non_source_rank_repair": "outputs/yt_non_source_response_rank_repair_sufficiency_2026-05-03.json",
}

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


def load_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def symbolic_derivation() -> dict[str, Any]:
    y_h, y_x, k_h, k_x, g_2, lam = sp.symbols("y_h y_x k_h k_x g_2 lam", nonzero=True)
    sqrt2 = sp.sqrt(2)
    # Source s moves the canonical Higgs radial coordinate by k_h ds and an
    # orthogonal neutral scalar by k_x ds.  W sees only the Higgs radial
    # component; the top energy sees both if the orthogonal scalar has top
    # coupling y_x.
    r_t = (y_h * k_h + y_x * k_x) / sqrt2
    r_w = g_2 * k_h / 2
    y_readout = sp.simplify(g_2 * r_t / (sqrt2 * r_w))
    residual = sp.simplify(y_readout - (y_h + y_x * k_x / k_h))
    no_orthogonal_residual = sp.simplify(y_readout.subs({y_x: 0}) - y_h)
    source_scale_residual = sp.simplify(
        y_readout.subs({k_h: lam * k_h, k_x: lam * k_x}) - y_readout
    )
    return {
        "R_t": str(r_t),
        "R_W": str(r_w),
        "y_readout": str(y_readout),
        "decomposition_residual_zero": residual == 0,
        "no_orthogonal_residual_zero": no_orthogonal_residual == 0,
        "source_rescaling_residual_zero": source_scale_residual == 0,
    }


def counterexample_rows() -> list[dict[str, float]]:
    g2 = 0.648
    y_h = 0.917
    k_h = 1.0
    rows = []
    for y_x, k_x in [(0.0, 0.4), (0.2, 0.4), (-0.2, 0.4)]:
        r_t = (y_h * k_h + y_x * k_x) / math.sqrt(2.0)
        r_w = g2 * k_h / 2.0
        y_readout = g2 * r_t / (math.sqrt(2.0) * r_w)
        rows.append(
            {
                "g2": g2,
                "physical_y_h": y_h,
                "orthogonal_y_x": y_x,
                "kappa_h": k_h,
                "kappa_x": k_x,
                "R_t": r_t,
                "R_W": r_w,
                "same_source_w_readout": y_readout,
                "orthogonal_correction": y_readout - y_h,
            }
        )
    return rows


def main() -> int:
    print("PR #230 same-source W-response decomposition theorem")
    print("=" * 72)

    parent_statuses = {
        name: status(load_json(rel)) if rel.startswith("outputs/") else ("present" if (ROOT / rel).exists() else "")
        for name, rel in PARENTS.items()
    }
    missing = [name for name, rel in PARENTS.items() if not (ROOT / rel).exists()]
    sym = symbolic_derivation()
    rows = counterexample_rows()
    fixed_w_response = len({round(row["R_W"], 12) for row in rows}) == 1
    varied_readout = max(row["same_source_w_readout"] for row in rows) - min(
        row["same_source_w_readout"] for row in rows
    )
    exact_support = (
        not missing
        and sym["decomposition_residual_zero"]
        and sym["no_orthogonal_residual_zero"]
        and sym["source_rescaling_residual_zero"]
        and fixed_w_response
        and varied_readout > 0.0
    )

    report("parent-surfaces-present", not missing, f"missing={missing}")
    report("exact-decomposition-derived", sym["decomposition_residual_zero"], sym["y_readout"])
    report("source-normalization-cancels", sym["source_rescaling_residual_zero"], "k_h,k_x -> lambda k_h,lambda k_x")
    report("orthogonal-null-gives-physical-yt", sym["no_orthogonal_residual_zero"], "y_x=0 implies readout=y_h")
    report("w-response-alone-counterfamily", fixed_w_response and varied_readout > 0.0, f"readout_span={varied_readout:.6f}")
    report("does-not-authorize-current-closure", True, "orthogonal null/correction and W rows absent")

    result = {
        "actual_current_surface_status": "exact-support / same-source W-response decomposition theorem; current rows absent",
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The theorem cancels source normalization but leaves an "
            "orthogonal-neutral top-coupling correction unless a null theorem, "
            "tomography row, or source-Higgs Gram-purity row is supplied."
        ),
        "bare_retained_allowed": False,
        "same_source_w_response_decomposition_theorem_passed": exact_support,
        "current_closure_gate_passed": False,
        "symbolic_derivation": sym,
        "readout_formula": {
            "R_t": "d m_t / d s = (y_h kappa_h + y_x kappa_x) / sqrt(2)",
            "R_W": "d M_W / d s = g_2 kappa_h / 2",
            "same_source_w_readout": "g_2 R_t / (sqrt(2) R_W) = y_h + y_x kappa_x/kappa_h",
            "closure_condition": "orthogonal correction y_x kappa_x/kappa_h = 0 or measured/subtracted",
        },
        "counterexample_rows": rows,
        "parent_certificates": PARENTS,
        "parent_statuses": parent_statuses,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not use observed target values as proof input",
            "does not use H_unit or yt_ward_identity",
            "does not use alpha_LM, plaquette, or u0 authority",
            "does not set kappa_s, c2, Z_match, or cos(theta) to one",
            "does not treat missing W-response rows as evidence",
        ],
        "exact_next_action": (
            "Produce same-source W response rows and either an orthogonal-top "
            "null theorem, a tomography correction row, or O_sp/O_H Gram-purity "
            "rows; then combine with FH/LSZ top response and matching/running."
        ),
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
