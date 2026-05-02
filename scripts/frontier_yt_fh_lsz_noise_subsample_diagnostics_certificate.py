#!/usr/bin/env python3
"""
PR #230 FH/LSZ scalar-LSZ noise-subsample diagnostics certificate.

This validates a harness extension needed by the eight-mode x8/x16 calibration
route: scalar two-point outputs now carry per-mode noise-subsample stability
diagnostics.  The smoke outputs are reduced-scope instrumentation evidence
only.  They do not justify lowering the production noise budget and do not
provide scalar LSZ normalization.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "scripts" / "yt_direct_lattice_correlator_production.py"
SCALAR_SMOKE = ROOT / "outputs" / "yt_direct_lattice_correlator_scalar_two_point_lsz_smoke_2026-05-01.json"
JOINT_SMOKE = ROOT / "outputs" / "yt_direct_lattice_correlator_fh_lsz_joint_smoke_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_noise_subsample_diagnostics_certificate_2026-05-01.json"

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


def first_analysis(data: dict[str, Any]) -> dict[str, Any]:
    ensembles = data.get("ensembles", [])
    if not isinstance(ensembles, list) or not ensembles:
        return {}
    analysis = ensembles[0].get("scalar_two_point_lsz_analysis", {})
    return analysis if isinstance(analysis, dict) else {}


def analyze_surface(name: str, path: Path) -> dict[str, Any]:
    data = load_json(path)
    metadata = data.get("metadata", {})
    lsz_meta = metadata.get("scalar_two_point_lsz", {})
    analysis = first_analysis(data)
    rows = analysis.get("mode_rows", {})
    mode_stability = {
        key: row.get("noise_subsample_stability", {})
        for key, row in rows.items()
        if isinstance(row, dict)
    }
    top_stability = analysis.get("noise_subsample_stability", {})
    available_modes = [
        key for key, value in mode_stability.items() if value.get("available") is True
    ]
    finite_ratios = [
        float(value.get("C_ss_real_half_delta_over_stderr_max", float("nan")))
        for value in mode_stability.values()
        if math.isfinite(float(value.get("C_ss_real_half_delta_over_stderr_max", float("nan"))))
    ]
    return {
        "name": name,
        "path": str(path.relative_to(ROOT)),
        "exists": bool(data),
        "phase": metadata.get("phase"),
        "noise_vectors_per_configuration": lsz_meta.get("noise_vectors_per_configuration"),
        "mode_count": len(rows) if isinstance(rows, dict) else 0,
        "top_level_available": top_stability.get("available") is True,
        "mode_level_available_count": len(available_modes),
        "max_half_delta_over_stderr": max(finite_ratios) if finite_ratios else None,
        "strict_limit": analysis.get("strict_limit"),
    }


def main() -> int:
    print("PR #230 FH/LSZ scalar-LSZ noise-subsample diagnostics certificate")
    print("=" * 72)

    harness_text = HARNESS.read_text(encoding="utf-8")
    scalar = analyze_surface("scalar_two_point_smoke", SCALAR_SMOKE)
    joint = analyze_surface("joint_fh_lsz_smoke", JOINT_SMOKE)
    surfaces = [scalar, joint]

    report("harness-emits-noise-stability-field", "noise_subsample_stability" in harness_text, str(HARNESS.relative_to(ROOT)))
    report("scalar-smoke-present", scalar["exists"], scalar["path"])
    report("joint-smoke-present", joint["exists"], joint["path"])
    report(
        "smokes-remain-reduced-scope",
        all(surface["phase"] == "reduced_scope" for surface in surfaces),
        f"phases={[surface['phase'] for surface in surfaces]}",
    )
    report(
        "scalar-smoke-top-level-diagnostics",
        scalar["top_level_available"] is True,
        f"available={scalar['top_level_available']}",
    )
    report(
        "joint-smoke-top-level-diagnostics",
        joint["top_level_available"] is True,
        f"available={joint['top_level_available']}",
    )
    report(
        "mode-level-diagnostics-present",
        min(surface["mode_level_available_count"] for surface in surfaces) >= 2,
        f"mode_counts={[surface['mode_level_available_count'] for surface in surfaces]}",
    )
    report(
        "noise-count-recorded",
        all(surface["noise_vectors_per_configuration"] == 2 for surface in surfaces),
        f"noises={[surface['noise_vectors_per_configuration'] for surface in surfaces]}",
    )
    report(
        "diagnostics-not-production-evidence",
        all("not kappa_s" in str(surface["strict_limit"]) for surface in surfaces),
        "strict limits retain non-claim boundary",
    )

    result = {
        "actual_current_surface_status": "bounded-support / FH-LSZ noise-subsample diagnostics harness",
        "verdict": (
            "The production harness now emits noise_subsample_stability fields "
            "for same-source scalar two-point rows and top-level scalar-LSZ "
            "analysis.  This supplies the diagnostic surface needed by a future "
            "paired x8/x16 variance calibration.  The current smoke outputs are "
            "still reduced-scope two-noise, two-mode, one-configuration runs, so "
            "they are instrumentation support only and do not justify lowering "
            "the production noise budget."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Noise diagnostics are harness plumbing, not production pole data or scalar LSZ normalization.",
        "diagnostic_surfaces": surfaces,
        "acceptance_requirements": [
            "run diagnostics on production same-source scalar-LSZ chunks",
            "compare paired eight-mode x8 and x16 outputs on the same saved configuration stream",
            "require stable C_ss(q), Gamma_ss(q), and pole-derivative fits before accepting x8",
            "keep reduced smoke outputs as instrumentation evidence only",
        ],
        "strict_non_claims": [
            "not production evidence",
            "not a kappa_s derivation",
            "does not set kappa_s, c2, or Z_match to one",
            "does not use H_unit or yt_ward_identity",
            "does not use observed top mass or observed y_t",
            "does not use alpha_LM, plaquette, or u0 as proof input",
        ],
        "exact_next_action": (
            "Use the new noise_subsample_stability fields in a paired "
            "eight-mode x8/x16 calibration chunk, or keep the x16 noise plan "
            "and schedule outside the 12-hour foreground window."
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
