#!/usr/bin/env python3
"""
PR #230 joint Feynman-Hellmann / scalar-LSZ resource projection.

After the harness can emit both dE/ds and same-source C_ss(q), the remaining
physical-response route is production data plus scalar pole/LSZ normalization.
This certificate turns that route into an explicit compute budget and keeps
the reduced smoke artifacts out of the proof surface.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "yt_production_resource_projection_2026-05-01.json"
JOINT = ROOT / "outputs" / "yt_fh_lsz_joint_harness_certificate_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_joint_resource_projection_2026-05-01.json"

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


def main() -> int:
    print("PR #230 joint Feynman-Hellmann / scalar-LSZ resource projection")
    print("=" * 72)

    base = json.loads(BASE.read_text(encoding="utf-8"))
    joint = json.loads(JOINT.read_text(encoding="utf-8"))

    direct_hours = float(base["total_mass_scaled_hours"])
    direct_conservative_hours = float(base["total_conservative_hours"])
    base_mass_points = int(base["production_protocol"]["fermion_mass_values"])
    source_shifts = 3
    extra_source_shift_masses = source_shifts - 1
    lsz_modes = 4
    lsz_noise_vectors = 16
    point_sources_per_mass = 3
    lsz_solve_equivalent_masses = (2 * lsz_modes * lsz_noise_vectors) / point_sources_per_mass
    total_equivalent_masses = base_mass_points + extra_source_shift_masses + lsz_solve_equivalent_masses
    solve_budget_factor = total_equivalent_masses / base_mass_points

    projected_mass_scaled_hours = direct_hours * solve_budget_factor
    projected_conservative_hours = direct_conservative_hours * solve_budget_factor
    projected_mass_scaled_days = projected_mass_scaled_hours / 24.0
    projected_conservative_days = projected_conservative_hours / 24.0

    rows = []
    for row in base["rows"]:
        projected = dict(row)
        projected["joint_equivalent_mass_points"] = total_equivalent_masses
        projected["joint_solve_budget_factor"] = solve_budget_factor
        projected["joint_mass_scaled_hours"] = float(row["mass_scaled_hours"]) * solve_budget_factor
        projected["joint_conservative_hours"] = float(row["conservative_hours"]) * solve_budget_factor
        rows.append(projected)

    report("base-resource-projection-loaded", BASE.exists(), str(BASE.relative_to(ROOT)))
    report("joint-harness-certificate-loaded", JOINT.exists(), str(JOINT.relative_to(ROOT)))
    report("joint-harness-not-closure", joint.get("proposal_allowed") is False, str(joint.get("proposal_allowed")))
    report("direct-route-already-multiday", direct_hours > 200.0, f"direct_mass_scaled_hours={direct_hours:.3f}")
    report(
        "joint-route-more-expensive-than-direct",
        projected_mass_scaled_hours > direct_hours,
        f"factor={solve_budget_factor:.6g}, hours={projected_mass_scaled_hours:.3f}",
    )
    report(
        "scalar-lsz-noise-load-bearing",
        lsz_solve_equivalent_masses > base_mass_points,
        f"lsz_equivalent_masses={lsz_solve_equivalent_masses:.6g}",
    )
    report("not-retained-closure", True, "resource projection is not production evidence or a scalar LSZ theorem")

    result = {
        "actual_current_surface_status": "bounded-support / joint FH-LSZ production resource projection",
        "verdict": (
            "The joint physical-response route is now executable but not a "
            "foreground closure route.  Using a modest scalar-LSZ plan of four "
            "momenta and sixteen noise vectors per configuration, the fermion "
            "solve budget is about 15.8889 times the existing three-mass direct "
            "projection.  The mass-scaled three-volume projection is therefore "
            f"about {projected_mass_scaled_hours:.2f} single-worker hours "
            f"({projected_mass_scaled_days:.2f} days), before any extra "
            "autocorrelation or pole-fit tuning.  This is exact next-action "
            "planning, not measurement evidence."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Projected compute cost and harness readiness do not derive kappa_s or provide production measurements.",
        "base_resource_projection": str(BASE.relative_to(ROOT)),
        "joint_harness_certificate": str(JOINT.relative_to(ROOT)),
        "assumed_joint_protocol": {
            "base_mass_points": base_mass_points,
            "source_shifts": source_shifts,
            "extra_source_shift_masses": extra_source_shift_masses,
            "scalar_lsz_momentum_modes": lsz_modes,
            "scalar_lsz_noise_vectors_per_configuration": lsz_noise_vectors,
            "point_sources_per_mass_correlator": point_sources_per_mass,
            "scalar_lsz_solve_equivalent_masses": lsz_solve_equivalent_masses,
            "total_equivalent_mass_points": total_equivalent_masses,
            "solve_budget_factor_vs_three_mass_direct": solve_budget_factor,
        },
        "projection": {
            "direct_mass_scaled_hours": direct_hours,
            "direct_conservative_hours": direct_conservative_hours,
            "joint_mass_scaled_hours": projected_mass_scaled_hours,
            "joint_mass_scaled_days": projected_mass_scaled_days,
            "joint_conservative_hours": projected_conservative_hours,
            "joint_conservative_days": projected_conservative_days,
            "volume_rows": rows,
        },
        "exact_next_action": [
            "choose scalar-LSZ momentum/noise budget from a pilot variance study",
            "launch the joint production harness on saved gauge ensembles",
            "fit correlated dE_top/ds and Gamma_ss(q) on the same ensemble stream",
            "derive the scalar pole and dGamma_ss/dp^2 in the controlled finite-volume/IR limit",
            "only then convert dE_top/ds to physical dE_top/dh",
        ],
        "strict_non_claims": [
            "not production evidence",
            "not a physical y_t derivation",
            "does not set kappa_s = 1",
            "does not set c2 or Z_match to one",
            "does not use H_unit or yt_ward_identity",
            "does not use observed top mass or observed y_t",
        ],
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
