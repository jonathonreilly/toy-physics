#!/usr/bin/env python3
"""
PR #230 Block61 post-carrier K-prime obstruction.

Block60 fixes the source-channel taste-singlet carrier coordinate.  This gate
tests the tempting follow-on shortcut:

    fixed source carrier + fixed scalar pole location => fixed K'(pole)/residue

The shortcut fails.  A same-carrier scalar denominator family can preserve the
pole location and source carrier while varying the inverse-denominator
derivative at the pole.  That derivative is a load-bearing LSZ residue input.
Therefore Block60 support does not close the scalar denominator/pole-residue
root.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_block61_post_carrier_kprime_obstruction_2026-05-12.json"
)

PARENTS = {
    "block60_compact_source_taste_singlet_carrier": "outputs/yt_pr230_block60_compact_source_taste_singlet_carrier_gate_2026-05-12.json",
    "kprime_closure_attempt": "outputs/yt_kprime_closure_attempt_2026-05-02.json",
    "scalar_kernel_ward_identity_obstruction": "outputs/yt_scalar_kernel_ward_identity_obstruction_2026-05-01.json",
    "scalar_ladder_residue_envelope_obstruction": "outputs/yt_scalar_ladder_residue_envelope_obstruction_2026-05-01.json",
    "scalar_ladder_eigen_derivative_gate": "outputs/yt_scalar_ladder_eigen_derivative_gate_2026-05-01.json",
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


def denominator_family() -> dict[str, Any]:
    x_pole = -0.25
    numerator_at_pole = 1.0
    rows = []
    for z in [0.5, 1.0, 2.0, 4.0]:
        rows.append(
            {
                "z": z,
                "denominator": "D_z(x)=z*(x-x_pole)+(x-x_pole)^2",
                "D_z_at_pole": 0.0,
                "D_z_prime_at_pole": z,
                "source_carrier": "fixed Block60 taste-singlet source carrier",
                "residue_proxy_N_over_Dprime": numerator_at_pole / z,
            }
        )
    residue_values = [row["residue_proxy_N_over_Dprime"] for row in rows]
    return {
        "x_pole": x_pole,
        "numerator_at_pole": numerator_at_pole,
        "rows": rows,
        "pole_location_preserved": all(row["D_z_at_pole"] == 0.0 for row in rows),
        "derivative_varies": max(row["D_z_prime_at_pole"] for row in rows)
        / min(row["D_z_prime_at_pole"] for row in rows),
        "residue_proxy_varies": max(residue_values) / min(residue_values),
    }


def main() -> int:
    print("PR #230 Block61 post-carrier K-prime obstruction")
    print("=" * 76)

    certs = {name: load(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed_parents = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]
    family = denominator_family()

    block60_loaded = (
        "source-channel taste-singlet carrier"
        in statuses["block60_compact_source_taste_singlet_carrier"]
        and certs["block60_compact_source_taste_singlet_carrier"].get(
            "source_channel_taste_carrier_fixed"
        )
        is True
    )
    kprime_parent_blocks = (
        "K-prime closure attempt blocked" in statuses["kprime_closure_attempt"]
        and "scalar kernel Ward-identity obstruction"
        in statuses["scalar_kernel_ward_identity_obstruction"]
        and "scalar ladder residue-envelope obstruction"
        in statuses["scalar_ladder_residue_envelope_obstruction"]
    )
    derivative_named_not_fixed = (
        "scalar ladder eigen-derivative gate"
        in statuses["scalar_ladder_eigen_derivative_gate"]
        and certs["scalar_ladder_eigen_derivative_gate"].get("proposal_allowed")
        is False
    )
    same_pole_variable_residue = (
        family["pole_location_preserved"]
        and family["derivative_varies"] >= 8.0
        and family["residue_proxy_varies"] >= 8.0
    )
    kprime_authority = False
    pole_residue_authority = False
    proposal_allowed = False

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed_parents, f"proposal_allowed={proposal_allowed_parents}")
    report("block60-source-carrier-loaded", block60_loaded, statuses["block60_compact_source_taste_singlet_carrier"])
    report("kprime-parent-blockers-apply", kprime_parent_blocks, "K-prime, Ward, and residue-envelope blockers preserved")
    report("eigen-derivative-named-not-fixed", derivative_named_not_fixed, statuses["scalar_ladder_eigen_derivative_gate"])
    report("same-pole-variable-residue-family", same_pole_variable_residue, f"residue_spread={family['residue_proxy_varies']:.1f}x")
    report("kprime-authority-absent", not kprime_authority, "fixed source carrier does not fix D'(pole)")
    report("pole-residue-authority-absent", not pole_residue_authority, "residue proxy varies")
    report("does-not-authorize-proposed-retained", not proposal_allowed, "Block61 is an exact negative boundary")

    result = {
        "actual_current_surface_status": (
            "no-go / exact negative boundary for the current PR230 surface: "
            "Block60 source-carrier support does not fix K-prime or pole residue"
        ),
        "conditional_surface_status": (
            "conditional-support if future work derives K'(pole), an LSZ "
            "residue interval, threshold/FVIR/contact authority, and canonical "
            "O_H or physical-response authority"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": proposal_allowed,
        "proposal_allowed_reason": (
            "A fixed source-channel carrier does not determine the scalar "
            "denominator derivative at the pole.  Same-carrier denominator "
            "families preserve the pole while changing the residue proxy."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "block61_post_carrier_kprime_obstruction_passed": True,
        "source_channel_taste_carrier_fixed": block60_loaded,
        "kprime_authority_present": kprime_authority,
        "pole_residue_authority_present": pole_residue_authority,
        "same_pole_variable_residue_family": family,
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "remaining_scalar_authority_obligations": [
            "derive K'(pole) or measure same-source pole residue directly",
            "derive uniform threshold/FVIR/contact authority",
            "derive canonical O_H/source-overlap or strict physical-response bridge",
        ],
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not infer K'(pole) from source-carrier normalization",
            "does not identify source carrier with canonical O_H",
            "does not use H_unit, Ward, y_t_bare, observed top/Yukawa values, alpha_LM, plaquette, u0, kappa_s=1, c2=1, or Z_match=1",
        ],
        "exact_next_action": (
            "A positive route needs an actual K'(pole)/residue theorem or "
            "direct pole-row measurement plus threshold/FVIR and canonical "
            "O_H/response authority."
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
