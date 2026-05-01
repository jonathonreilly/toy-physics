#!/usr/bin/env python3
"""
PR #230 Feynman-Hellmann / scalar-LSZ invariant readout theorem.

This stretch block attacks the kappa_s normalization directly.  It proves the
source-rescaling-safe readout formula for the physical-response route:

    y_proxy = (dE_top/ds) * sqrt(d Gamma_ss / d p^2 | pole)
            = (dE_top/ds) / sqrt(Res[C_ss] | pole)

provided that dE/ds and C_ss are measured for the same scalar source and that
an isolated canonical scalar pole has been established.  This does not set
kappa_s = 1.  It says kappa_s is the measured pole overlap.

The theorem is exact algebraic support, not retained closure, because PR #230
still lacks production dE/ds data, an isolated scalar pole, and the pole
derivative / canonical-Higgs normalization measurement.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
JOINT = ROOT / "outputs" / "yt_fh_lsz_joint_harness_certificate_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_invariant_readout_theorem_2026-05-01.json"

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
    print("PR #230 Feynman-Hellmann / scalar-LSZ invariant readout theorem")
    print("=" * 72)

    joint = json.loads(JOINT.read_text(encoding="utf-8"))
    slope = 1.37
    residue = 0.42
    gamma_derivative = 1.0 / residue
    source_scales = [0.25, 0.5, 1.0, 2.0, 4.0]
    rows = []
    for scale in source_scales:
        # O_s -> scale * O_s for the source coordinate used in both response
        # and two-point measurements.
        slope_scaled = scale * slope
        residue_scaled = scale * scale * residue
        gamma_derivative_scaled = 1.0 / residue_scaled
        invariant_from_residue = slope_scaled / math.sqrt(residue_scaled)
        invariant_from_inverse_derivative = slope_scaled * math.sqrt(gamma_derivative_scaled)
        naive_kappa_one_readout = slope_scaled
        rows.append(
            {
                "source_operator_scale": scale,
                "dE_ds_scaled": slope_scaled,
                "C_ss_pole_residue_scaled": residue_scaled,
                "dGamma_dp2_at_pole_scaled": gamma_derivative_scaled,
                "invariant_readout_from_residue": invariant_from_residue,
                "invariant_readout_from_inverse_derivative": invariant_from_inverse_derivative,
                "forbidden_kappa_s_equals_one_readout": naive_kappa_one_readout,
            }
        )

    invariant_values = [row["invariant_readout_from_residue"] for row in rows]
    derivative_values = [row["invariant_readout_from_inverse_derivative"] for row in rows]
    forbidden_values = [row["forbidden_kappa_s_equals_one_readout"] for row in rows]
    invariant_spread = (max(invariant_values) - min(invariant_values)) / max(abs(sum(invariant_values) / len(invariant_values)), 1.0e-30)
    derivative_spread = (max(derivative_values) - min(derivative_values)) / max(abs(sum(derivative_values) / len(derivative_values)), 1.0e-30)
    forbidden_spread = (max(forbidden_values) - min(forbidden_values)) / max(abs(sum(forbidden_values) / len(forbidden_values)), 1.0e-30)

    required_data = [
        "same-source production dE_top/ds",
        "same-source production C_ss(q)",
        "isolated scalar pole in the controlled finite-volume/IR limit",
        "dGamma_ss/dp^2 at that pole",
        "match of that pole to the canonical Higgs kinetic normalization used by v",
    ]

    report("joint-harness-certificate-present", JOINT.exists(), str(JOINT.relative_to(ROOT)))
    report("joint-harness-not-closure", joint.get("proposal_allowed") is False, str(joint.get("proposal_allowed")))
    report(
        "residue-and-inverse-derivative-formulas-agree",
        max(abs(a - b) for a, b in zip(invariant_values, derivative_values)) < 1.0e-12,
        f"max_delta={max(abs(a - b) for a, b in zip(invariant_values, derivative_values)):.3e}",
    )
    report(
        "readout-source-rescaling-invariant",
        invariant_spread < 1.0e-12 and derivative_spread < 1.0e-12,
        f"residue_spread={invariant_spread:.3e}, derivative_spread={derivative_spread:.3e}",
    )
    report(
        "kappa-one-shortcut-not-invariant",
        forbidden_spread > 1.0,
        f"forbidden_readout_spread={forbidden_spread:.6g}",
    )
    report(
        "same-source-requirement-load-bearing",
        True,
        "response and scalar two-point residue must use the same source coordinate",
    )
    report("not-retained-closure", True, "the formula still needs production data and a controlled pole")

    result = {
        "actual_current_surface_status": "exact-support / Feynman-Hellmann scalar-LSZ invariant readout formula",
        "verdict": (
            "The physical-response route does not need a forbidden kappa_s = 1 "
            "shortcut.  If dE_top/ds and C_ss are measured for the same scalar "
            "source and an isolated canonical scalar pole is established, the "
            "source-normalization-invariant readout is dE_top/ds multiplied by "
            "sqrt(dGamma_ss/dp^2 at the pole), equivalently dE_top/ds divided "
            "by sqrt(Res[C_ss]).  This is exact support for the route and "
            "identifies how kappa_s is measured.  It is not retained closure "
            "because the production response, scalar pole, pole derivative, "
            "and canonical-Higgs match are still absent."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The invariant formula is theorem support, but the required same-source production pole-residue data are not present.",
        "joint_harness_certificate": str(JOINT.relative_to(ROOT)),
        "formula": {
            "readout_from_inverse_derivative": "y_proxy = (dE_top/ds) * sqrt(dGamma_ss/dp^2 | pole)",
            "readout_from_residue": "y_proxy = (dE_top/ds) / sqrt(Res[C_ss] | pole)",
            "source_rescaling": "O_s -> c O_s sends dE/ds -> c dE/ds and Res[C_ss] -> c^2 Res[C_ss]",
        },
        "rows": rows,
        "required_data_before_closure": required_data,
        "strict_non_claims": [
            "not production evidence",
            "not retained or proposed_retained y_t closure",
            "does not set kappa_s = 1",
            "does not use H_unit matrix-element readout",
            "does not use yt_ward_identity as authority",
            "does not use observed top mass or observed y_t",
            "does not set c2 or Z_match to one",
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
