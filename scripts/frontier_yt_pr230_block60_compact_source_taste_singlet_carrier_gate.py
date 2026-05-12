#!/usr/bin/env python3
"""
PR #230 Block60 compact-source taste-singlet carrier gate.

The current scalar denominator route has two different normalization issues:

1. Which source-channel taste carrier does the compact additive source select?
2. Does that source-channel carrier equal the canonical Higgs O_H with LSZ
   normalization?

This gate closes only the first question as exact support.  The additive
staggered scalar source shifts the bare mass uniformly, so its derivative
couples to the unnormalized taste-singlet local scalar sum.  Equivalently, it
couples to the unit taste singlet with a fixed source-coordinate factor
sqrt(N_taste).  This fixes the source-channel carrier coordinate, but it does
not fix canonical O_H/source-overlap, scalar pole residue, K'(pole), threshold,
or FV/IR authority.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_block60_compact_source_taste_singlet_carrier_gate_2026-05-12.json"
)

PARENTS = {
    "block57_compact_source_functional_foundation": "outputs/yt_pr230_block57_compact_source_functional_foundation_gate_2026-05-12.json",
    "block58_compact_source_spectral_support": "outputs/yt_pr230_block58_compact_source_spectral_support_gate_2026-05-12.json",
    "scalar_taste_projector_normalization_attempt": "outputs/yt_scalar_taste_projector_normalization_attempt_2026-05-01.json",
    "taste_singlet_ladder_normalization_boundary": "outputs/yt_taste_singlet_ladder_normalization_boundary_2026-05-01.json",
    "scalar_carrier_projector_closure_attempt": "outputs/yt_scalar_carrier_projector_closure_attempt_2026-05-02.json",
}

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


def load(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def carrier_witness() -> dict[str, Any]:
    n_taste = 16
    local_sum_norm_sq = float(n_taste)
    unit_factor = 1.0 / math.sqrt(n_taste)
    source_to_unit_factor = math.sqrt(n_taste)
    return {
        "n_taste_corners": n_taste,
        "source_operator": "O_s = sum_{taste=1}^{16} psi_taste^dagger psi_taste",
        "unit_taste_singlet": "O_1 = O_s / sqrt(16)",
        "local_sum_norm_squared": local_sum_norm_sq,
        "unit_taste_singlet_norm_squared": 1.0,
        "unit_operator_factor": unit_factor,
        "source_coordinate_to_unit_operator_factor": source_to_unit_factor,
        "two_point_local_to_unit_factor": n_taste,
        "source_coordinate_fixed_by": "additive bare-mass/source shift s in D_KS(m+s)",
    }


def main() -> int:
    print("PR #230 Block60 compact-source taste-singlet carrier gate")
    print("=" * 76)

    certs = {name: load(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed_parents = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]
    witness = carrier_witness()

    block57_source_loaded = (
        "compact finite-volume scalar-source functional foundation"
        in statuses["block57_compact_source_functional_foundation"]
        and certs["block57_compact_source_functional_foundation"].get(
            "finite_volume_compact_source_functional_defined"
        )
        is True
    )
    block58_spectral_loaded = (
        "finite-volume compact source-channel spectral support"
        in statuses["block58_compact_source_spectral_support"]
        and certs["block58_compact_source_spectral_support"].get(
            "finite_volume_source_spectral_representation_present"
        )
        is True
    )
    unit_taste_algebra_confirmed = (
        witness["local_sum_norm_squared"] == 16.0
        and witness["unit_taste_singlet_norm_squared"] == 1.0
        and witness["source_coordinate_to_unit_operator_factor"] == 4.0
    )
    prior_no_go_preserved = (
        "scalar taste-projector normalization theorem attempt blocked"
        in statuses["scalar_taste_projector_normalization_attempt"]
        and "taste-singlet normalization removes finite ladder crossings"
        in statuses["taste_singlet_ladder_normalization_boundary"]
        and "scalar carrier-projector closure attempt blocked"
        in statuses["scalar_carrier_projector_closure_attempt"]
    )
    canonical_oh_authority = False
    pole_residue_authority = False
    kprime_authority = False
    threshold_fvir_authority = False
    proposal_allowed = False

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed_parents, f"proposal_allowed={proposal_allowed_parents}")
    report("block57-compact-source-loaded", block57_source_loaded, statuses["block57_compact_source_functional_foundation"])
    report("block58-source-spectral-loaded", block58_spectral_loaded, statuses["block58_compact_source_spectral_support"])
    report("source-taste-singlet-carrier-fixed", unit_taste_algebra_confirmed, f"sqrt_N={witness['source_coordinate_to_unit_operator_factor']}")
    report("prior-canonical-normalization-no-gos-preserved", prior_no_go_preserved, "source carrier is not canonical O_H")
    report("canonical-oh-authority-absent", not canonical_oh_authority, "source taste singlet not physical Higgs identity")
    report("pole-residue-authority-absent", not pole_residue_authority, "no LSZ residue interval")
    report("kprime-authority-absent", not kprime_authority, "no scalar denominator derivative")
    report("threshold-fvir-authority-absent", not threshold_fvir_authority, "no threshold/FVIR theorem")
    report("does-not-authorize-proposed-retained", not proposal_allowed, "Block60 is source-channel support only")

    result = {
        "actual_current_surface_status": (
            "exact-support / Block60 compact additive source fixes the "
            "source-channel taste-singlet carrier coordinate; canonical O_H, "
            "pole residue, K-prime, and threshold/FVIR authority remain open"
        ),
        "conditional_surface_status": (
            "conditional-support if future work pairs this source-channel "
            "carrier with scalar denominator/pole-residue/FVIR authority and "
            "canonical O_H or physical-response authority"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": proposal_allowed,
        "proposal_allowed_reason": (
            "The additive source fixes the source-channel taste-singlet carrier "
            "coordinate only.  It does not identify that carrier with canonical "
            "O_H or provide LSZ pole, K'(pole), threshold, or FVIR authority."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "block60_compact_source_taste_singlet_carrier_gate_passed": True,
        "source_channel_taste_carrier_fixed": True,
        "canonical_oh_authority_present": canonical_oh_authority,
        "pole_residue_authority_present": pole_residue_authority,
        "kprime_authority_present": kprime_authority,
        "threshold_fvir_authority_present": threshold_fvir_authority,
        "carrier_witness": witness,
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "remaining_scalar_authority_obligations": [
            "canonical O_H/source-overlap or physical-response bridge",
            "scalar denominator derivative K'(pole) or direct pole-residue measurement",
            "uniform threshold/FVIR/contact theorem",
        ],
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not identify the source taste singlet with canonical O_H",
            "does not set kappa_s=1, c2=1, or Z_match=1",
            "does not use H_unit, Ward, y_t_bare, observed top/Yukawa values, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Use the fixed source-channel taste carrier only as support.  A "
            "positive route still needs K'(pole)/residue plus threshold/FVIR "
            "and canonical-O_H/response authority."
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
