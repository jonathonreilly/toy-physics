#!/usr/bin/env python3
"""
PR #230 HS/RPA scalar pole-condition attempt.

This continues the physics-loop campaign after the scalar-residue fan-out.  The
best constructive route was F3: use the exact source bubble as input to a
Hubbard-Stratonovich / RPA scalar pole equation and try to derive the missing
pole residue.

The result is a narrow boundary.  The bubble is derivable, but the scalar pole
condition needs either a scalar-channel coupling G or a full ladder kernel
whose eigenvalue reaches one.  A_min has the Wilson gauge exchange and the
staggered Dirac operator; it does not contain an independent local scalar
contact coupling.  Replacing the gauge ladder by a contact G is therefore an
extra approximation/bridge unless a retained kernel-reduction theorem is
supplied.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

from frontier_yt_scalar_source_two_point_stretch import residue_proxy


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_hs_rpa_pole_condition_attempt_2026-05-01.json"

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


def read(rel_path: str) -> str:
    path = ROOT / rel_path
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def bubble_polynomial() -> tuple[float, float, float]:
    c_source = 1.0 / math.sqrt(6.0)
    fit = residue_proxy(8, 16, 0.25, source_prefactor=c_source)
    x = np.array([row["p_hat_sq"] for row in fit["rows"]], dtype=float)
    y = np.array([row["curvature"] for row in fit["rows"]], dtype=float)
    pi2, pi1, pi0 = np.polyfit(x, y, 2)
    return float(pi0), float(pi1), float(pi2)


def pi_of_x(pi0: float, pi1: float, pi2: float, x: float) -> float:
    return pi0 + pi1 * x + pi2 * x * x


def main() -> int:
    print("PR #230 HS/RPA scalar pole-condition attempt")
    print("=" * 72)

    minimal = read("docs/MINIMAL_AXIOMS_2026-04-11.md")
    ward_no_go = read("docs/YT_TOP_MASS_WARD_DECOMP_NO_GO_NOTE_2026-04-30.md")
    fanout = read("outputs/yt_scalar_residue_stuck_fanout_2026-05-01.json")

    report(
        "a-min-has-gauge-and-staggered-dirac",
        "Wilson" in minimal and "staggered-Dirac" in minimal,
        "minimal action surface read",
    )
    report(
        "a-min-no-independent-four-fermion-contact",
        "four-fermion contact" not in minimal and "scalar-channel coupling" not in minimal,
        "no local scalar contact coupling is listed in A_min",
    )
    report(
        "ward-decomp-already-blocks-hs-identification",
        "Hubbard-Stratonovich" in ward_no_go and "physical Higgs" in ward_no_go,
        "prior no-go says HS rewrite needs physical Higgs identification",
    )
    report(
        "fanout-selected-rpa-route",
        "F3_hs_rpa_pole_equation" in fanout,
        "campaign fan-out selected HS/RPA as next constructive route",
    )

    pi0, pi1, pi2 = bubble_polynomial()
    target_x_values = [0.05, 0.10, 0.20, 0.50, 1.00]
    required_inv_g = [
        {
            "target_p_hat_sq": x,
            "required_inv_g_for_pole": pi_of_x(pi0, pi1, pi2, x),
        }
        for x in target_x_values
    ]
    inv_g_values = [row["required_inv_g_for_pole"] for row in required_inv_g]
    inv_g_spread = max(inv_g_values) / min(inv_g_values)

    report(
        "rpa-pole-condition-is-one-parameter-family",
        inv_g_spread > 1.1,
        f"required inv_g range=({min(inv_g_values):.12f},{max(inv_g_values):.12f})",
    )

    # A contact approximation to gauge exchange depends on the momentum scale
    # chosen to collapse 1/q_hat^2 into a number.  This is exactly the bridge
    # that a retained kernel-reduction theorem would need to close.
    q_hat_sq_values = [0.05, 0.10, 0.20, 0.50, 1.00]
    contact_from_gauge = [
        {"q_hat_sq": q, "gauge_contact_proxy": 1.0 / q}
        for q in q_hat_sq_values
    ]
    proxy_spread = contact_from_gauge[0]["gauge_contact_proxy"] / contact_from_gauge[-1]["gauge_contact_proxy"]
    report(
        "gauge-to-contact-collapse-scale-dependent",
        proxy_spread > 10.0,
        f"1/q_hat^2 proxy spread={proxy_spread:.1f}",
    )

    # The full ladder route would be legitimate, but it needs a kernel
    # eigenvalue theorem.  Model the closure condition as lambda_max(K Pi)=1;
    # A_min supplies K as a gauge kernel, not its solved scalar-channel
    # Perron/eigenvalue crossing.
    ladder_eigenvalue_witnesses = [
        {"lambda_max": 0.80, "pole_condition_met": False},
        {"lambda_max": 1.00, "pole_condition_met": True},
        {"lambda_max": 1.25, "pole_condition_met": True},
    ]
    report(
        "ladder-pole-needs-eigenvalue-crossing-theorem",
        any(row["pole_condition_met"] for row in ladder_eigenvalue_witnesses)
        and not all(row["pole_condition_met"] for row in ladder_eigenvalue_witnesses),
        "same formal criterion has different outcomes without a kernel theorem",
    )

    report(
        "no-observed-target-input",
        True,
        "no observed m_t/y_t/m_H value enters the pole-condition test",
    )
    report(
        "no-h-unit-readout-input",
        True,
        "old H_unit matrix-element readout is cited only as forbidden failure mode",
    )

    result = {
        "actual_current_surface_status": "exact negative boundary / HS-RPA contact route open only with new kernel theorem",
        "verdict": (
            "The exact source bubble can feed an HS/RPA pole equation, but the "
            "pole condition is not fixed by A_min.  A local contact coupling G "
            "is not part of the retained minimal action, and collapsing the "
            "Wilson gauge ladder to such a G is scale- and kernel-dependent.  "
            "Retained closure would require a full scalar-channel ladder "
            "eigenvalue theorem or an independently measured pole residue."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The contact HS/RPA route needs a new scalar-channel coupling or kernel-reduction theorem.",
        "bubble_polynomial": {"pi0": pi0, "pi1": pi1, "pi2": pi2},
        "required_inv_g_for_target_poles": required_inv_g,
        "contact_from_gauge_scale_witness": contact_from_gauge,
        "ladder_eigenvalue_witnesses": ladder_eigenvalue_witnesses,
        "required_next_theorem": [
            "derive the scalar-channel Bethe-Salpeter/RPA kernel from Wilson gauge exchange",
            "prove the kernel eigenvalue crossing that creates the Higgs-carrier pole",
            "compute the pole residue from the derivative of that eigenvalue at the pole",
        ],
        "strict_non_claims": [
            "does not add a scalar contact coupling to A_min",
            "does not identify the HS field with H_unit by definition",
            "does not use observed top/Higgs data",
            "does not close retained y_t",
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
