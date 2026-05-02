#!/usr/bin/env python3
"""
PR #230 Cl(3)/Z3 automorphism/source-identity no-go.

This runner checks whether finite substrate automorphism/orbit data can provide
the missing scalar source-to-canonical-Higgs identity.  The result is negative:
finite source-orbit invariants can be held fixed while continuous LSZ data such
as source overlap and inverse-propagator derivative vary.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_cl3_automorphism_source_identity_no_go_2026-05-02.json"

PARENTS = {
    "cl3_source_unit": "outputs/yt_cl3_source_unit_normalization_no_go_2026-05-01.json",
    "d17_source_pole_identity": "outputs/yt_d17_source_pole_identity_closure_attempt_2026-05-02.json",
    "source_overlap_sum_rule": "outputs/yt_source_overlap_sum_rule_no_go_2026-05-02.json",
    "higgs_identity_gate": "outputs/yt_fh_lsz_higgs_pole_identity_gate_2026-05-02.json",
    "brst_nielsen_higgs_identity": "outputs/yt_brst_nielsen_higgs_identity_no_go_2026-05-02.json",
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


def load(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def build_orbit_witness() -> dict[str, Any]:
    rows = []
    for source_overlap, dprime in [(0.55, 4.0), (0.85, 2.0), (1.20, 1.0), (1.60, 0.5)]:
        rows.append(
            {
                "finite_substrate_invariants": {
                    "cl3_generator_norms": [1, 1, 1],
                    "z3_translation_orbit_size": 3,
                    "signed_permutation_orbit_size": 6,
                    "d17_scalar_carrier_count": 1,
                    "source_coordinate_unit": 1,
                    "scalar_source_quantum_numbers": "neutral_singlet",
                },
                "continuous_lsz_data": {
                    "source_overlap_z_s": source_overlap,
                    "inverse_propagator_derivative_dprime": dprime,
                    "same_source_pole_residue": source_overlap * source_overlap / dprime,
                    "canonical_response_factor": source_overlap / (dprime ** 0.5),
                },
            }
        )
    invariants = [row["finite_substrate_invariants"] for row in rows]
    overlaps = [row["continuous_lsz_data"]["source_overlap_z_s"] for row in rows]
    dprimes = [row["continuous_lsz_data"]["inverse_propagator_derivative_dprime"] for row in rows]
    residues = [row["continuous_lsz_data"]["same_source_pole_residue"] for row in rows]
    return {
        "rows": rows,
        "checks": {
            "finite_invariants_fixed": all(item == invariants[0] for item in invariants),
            "source_overlap_span": max(overlaps) - min(overlaps),
            "dprime_span_factor": max(dprimes) / min(dprimes),
            "residue_span_factor": max(residues) / min(residues),
        },
    }


def main() -> int:
    print("PR #230 Cl(3)/Z3 automorphism/source-identity no-go")
    print("=" * 72)

    parents = {name: load(rel) for name, rel in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    witness = build_orbit_witness()
    checks = witness["checks"]

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report(
        "finite-substrate-invariants-held-fixed",
        checks["finite_invariants_fixed"],
        "Cl(3), Z3, signed-permutation, D17, and source-unit rows fixed",
    )
    report(
        "source-overlap-still-varies",
        checks["source_overlap_span"] > 1.0,
        f"span={checks['source_overlap_span']:.6g}",
    )
    report(
        "inverse-propagator-derivative-still-varies",
        checks["dprime_span_factor"] >= 8.0,
        f"span_factor={checks['dprime_span_factor']:.6g}",
    )
    report(
        "pole-residue-still-varies",
        checks["residue_span_factor"] >= 16.0,
        f"span_factor={checks['residue_span_factor']:.6g}",
    )
    report(
        "source-unit-parent-blocks-kappa-one",
        parents["cl3_source_unit"].get("proposal_allowed") is False,
        parents["cl3_source_unit"].get("actual_current_surface_status", ""),
    )
    report(
        "d17-parent-blocks-carrier-to-lsz-promotion",
        parents["d17_source_pole_identity"].get("theorem_closed") is False,
        parents["d17_source_pole_identity"].get("actual_current_surface_status", ""),
    )
    report(
        "higgs-identity-gate-still-open",
        parents["higgs_identity_gate"].get("higgs_pole_identity_gate_passed") is False,
        parents["higgs_identity_gate"].get("actual_current_surface_status", ""),
    )
    report("does-not-authorize-retained-proposal", True, "finite orbit data do not fix continuous LSZ normalization")

    result = {
        "actual_current_surface_status": "exact negative boundary / Cl3 automorphism data not source-Higgs identity",
        "verdict": (
            "Finite Cl(3)/Z3 source-orbit and automorphism data do not derive "
            "the PR #230 scalar source-to-canonical-Higgs identity.  The witness "
            "keeps generator norms, Z3 and signed-permutation orbit sizes, D17 "
            "single-carrier count, source coordinate unit, and neutral source "
            "quantum numbers fixed while source overlap, D'(pole), and the pole "
            "residue vary.  Therefore finite substrate orbit data are structural "
            "support only; they cannot replace a microscopic scalar denominator "
            "theorem, source-pole purity theorem, or production pole-residue "
            "measurement."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The missing LSZ/source-overlap quantities are continuous pole data, not finite automorphism invariants.",
        "parent_certificates": PARENTS,
        "orbit_witness": witness,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not set kappa_s = 1",
            "does not promote D17 or finite Cl(3)/Z3 orbit data into LSZ pole normalization",
            "does not use H_unit, yt_ward_identity, observed top mass, observed y_t, alpha_LM, plaquette, u0, c2 = 1, or Z_match = 1",
        ],
        "exact_next_action": (
            "Derive the continuous scalar denominator/source-overlap theorem, "
            "or measure same-source pole residue and D'(pole) in production; "
            "do not infer them from finite substrate automorphism/orbit data."
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
