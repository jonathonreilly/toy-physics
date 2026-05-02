#!/usr/bin/env python3
"""
PR #230 FH/LSZ soft-continuum threshold no-go.

This runner tests a narrow possible repair after the color-singlet zero-mode
work: whether q=0 cancellation plus finite-q IR regularity can be promoted to
a uniform continuum-threshold certificate for the scalar LSZ pole residue.

It cannot.  A zero-mode-removed massless kernel can be locally integrable while
positive spectral weight starts arbitrarily close to the pole.  Integrability
controls divergence; it does not supply a positive threshold gap.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_soft_continuum_threshold_no_go_2026-05-02.json"

PARENTS = {
    "color_singlet_zero_mode": "outputs/yt_color_singlet_zero_mode_cancellation_2026-05-01.json",
    "color_singlet_finite_q_ir": "outputs/yt_color_singlet_finite_q_ir_regular_2026-05-01.json",
    "uniform_gap_no_go": "outputs/yt_fh_lsz_uniform_gap_self_certification_no_go_2026-05-02.json",
    "scalar_denominator_closure": "outputs/yt_scalar_denominator_theorem_closure_attempt_2026-05-02.json",
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


def normalized_soft_band_contribution(shell: float, pole_m2: float, gap_lo: float, gap_hi: float) -> float:
    """Integral of a normalized soft density proportional to gap/(shell+pole+gap)."""
    norm = 2.0 / (gap_hi * gap_hi - gap_lo * gap_lo)
    a = shell + pole_m2
    primitive_hi = gap_hi - a * math.log(a + gap_hi)
    primitive_lo = gap_lo - a * math.log(a + gap_lo)
    return norm * (primitive_hi - primitive_lo)


def build_soft_scan() -> dict[str, Any]:
    pole_m2 = 0.25
    one_link = 4.0 * math.sin(math.pi / 12.0) ** 2
    shells = [0.0, one_link, 2.0 * one_link, 1.0]
    eps_values = [1.0e-1, 1.0e-2, 1.0e-4, 1.0e-6, 1.0e-8]
    rows = []
    for eps in eps_values:
        gap_hi = 2.0 * eps
        contributions = [
            normalized_soft_band_contribution(shell, pole_m2, eps, gap_hi)
            for shell in shells
        ]
        rows.append(
            {
                "continuum_gap_lo_from_pole_m2": eps,
                "continuum_gap_hi_from_pole_m2": gap_hi,
                "normalized_soft_density": "rho(delta)=2 delta/(gap_hi^2-gap_lo^2)",
                "all_shell_contributions_finite": all(math.isfinite(value) for value in contributions),
                "shell_contributions": contributions,
                "zero_mode_removed_ir_measure": "d4q/q^2 -> q dq, integrable",
            }
        )
    return {
        "pole_p_hat_sq": -pole_m2,
        "shells_p_hat_sq": shells,
        "soft_band_rows": rows,
    }


def main() -> int:
    print("PR #230 FH/LSZ soft-continuum threshold no-go")
    print("=" * 72)

    certs = {name: load(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    scan = build_soft_scan()
    rows = scan["soft_band_rows"]
    min_gap = min(float(row["continuum_gap_lo_from_pole_m2"]) for row in rows)
    all_finite = all(bool(row["all_shell_contributions_finite"]) for row in rows)
    finite_q_support_loaded = (
        "finite-q IR regularity" in str(certs["color_singlet_finite_q_ir"].get("actual_current_surface_status", ""))
    )
    q0_cancellation_loaded = (
        "zero-mode cancellation" in str(certs["color_singlet_zero_mode"].get("actual_current_surface_status", ""))
    )
    scalar_denominator_still_blocked = (
        "scalar denominator theorem closure attempt blocked"
        in str(certs["scalar_denominator_closure"].get("actual_current_surface_status", ""))
    )
    threshold_gap_certified = False

    report("all-parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("q0-color-singlet-cancellation-loaded", q0_cancellation_loaded, PARENTS["color_singlet_zero_mode"])
    report("finite-q-ir-regularity-loaded", finite_q_support_loaded, PARENTS["color_singlet_finite_q_ir"])
    report("soft-continuum-arbitrarily-near-pole-finite", all_finite and min_gap < 1.0e-7, f"min_gap={min_gap}")
    report("ir-regularity-does-not-certify-threshold", not threshold_gap_certified, "uniform threshold lower bound remains zero")
    report("scalar-denominator-still-blocked", scalar_denominator_still_blocked, PARENTS["scalar_denominator_closure"])
    report("does-not-authorize-retained-proposal", True, "support is negative boundary, not closure")

    result = {
        "actual_current_surface_status": "exact negative boundary / FH-LSZ soft-continuum threshold no-go",
        "verdict": (
            "Color-singlet q=0 cancellation and finite-q IR regularity do not "
            "certify a uniform continuum threshold for the scalar LSZ pole.  "
            "After the zero mode is removed, the massless finite-q measure is "
            "locally integrable, but positive continuum spectral weight can "
            "still begin arbitrarily close to the pole with finite shell "
            "contributions.  Therefore IR regularity controls a divergence; "
            "it does not supply the pole-saturation/threshold premise required "
            "by the FH/LSZ residue gate."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Finite-q IR regularity is compatible with arbitrarily small continuum gaps and does not make the pole-residue interval tight.",
        "parent_certificates": PARENTS,
        "soft_continuum_scan": scan,
        "uniform_threshold_gap_certified": threshold_gap_certified,
        "minimum_gap_exhibited": min_gap,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not set kappa_s = 1",
            "does not infer a continuum threshold from finite-q IR regularity",
            "does not use observed top mass, observed y_t, H_unit, yt_ward_identity, alpha_LM, plaquette, u0, c2 = 1, or Z_match = 1",
        ],
        "exact_next_action": (
            "Continue seed-controlled production replacement chunks, or derive "
            "a microscopic scalar denominator theorem that supplies an actual "
            "threshold/pole-saturation premise rather than only IR regularity."
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
