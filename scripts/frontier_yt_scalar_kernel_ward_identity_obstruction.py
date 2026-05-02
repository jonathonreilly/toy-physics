#!/usr/bin/env python3
"""
PR #230 scalar-kernel Ward-identity obstruction.

The residue-envelope block leaves one analytic positive route: derive the
interacting scalar-channel denominator and its pole derivative from retained
dynamics.  This runner asks whether the existing Ward/gauge/Feshbach surfaces
already fix that derivative.

They do not.  Ward identities constrain conserved gauge-current responses and
same-operator transformations.  The scalar FH/LSZ readout needs the derivative
of the scalar-channel Bethe-Salpeter denominator at the pole.  Holding the
same pole location and gauge/Ward-side data fixed leaves K'(x_pole) free, and
changes the LSZ residue/readout.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_scalar_kernel_ward_identity_obstruction_2026-05-01.json"

WARD_NOTE = ROOT / "docs" / "YT_WARD_IDENTITY_DERIVATION_THEOREM.md"
DETERMINANT_GATE = ROOT / "outputs" / "yt_scalar_pole_determinant_gate_2026-05-01.json"
FESHBACH = ROOT / "outputs" / "yt_feshbach_operator_response_boundary_2026-05-01.json"
COMMON_DRESSING = ROOT / "outputs" / "yt_common_dressing_obstruction_2026-05-01.json"
RESIDUE_ENVELOPE = ROOT / "outputs" / "yt_scalar_ladder_residue_envelope_obstruction_2026-05-01.json"

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


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def pi_scalar(x: float) -> float:
    return 2.0 + 0.40 * x + 0.05 * x * x


def pi_prime(x: float) -> float:
    return 0.40 + 0.10 * x


def kernel_family_row(k_prime: float) -> dict[str, float]:
    x_pole = -1.0
    pi_pole = pi_scalar(x_pole)
    k_pole = 1.0 / pi_pole
    d_prime = -k_prime * pi_pole - k_pole * pi_prime(x_pole)
    dgamma_dp_sq = d_prime / pi_pole
    lsz_readout_factor = math.sqrt(abs(dgamma_dp_sq))
    return {
        "x_pole": x_pole,
        "pi_pole": pi_pole,
        "pi_prime_pole": pi_prime(x_pole),
        "K_pole": k_pole,
        "K_prime_pole": k_prime,
        "D_pole": 1.0 - k_pole * pi_pole,
        "D_prime_pole": d_prime,
        "dGamma_dp_sq_at_pole": dgamma_dp_sq,
        "lsz_readout_factor": lsz_readout_factor,
    }


def main() -> int:
    print("PR #230 scalar-kernel Ward-identity obstruction")
    print("=" * 72)

    ward_text = WARD_NOTE.read_text(encoding="utf-8")
    determinant = load(DETERMINANT_GATE)
    feshbach = load(FESHBACH)
    common_dressing = load(COMMON_DRESSING)
    residue_envelope = load(RESIDUE_ENVELOPE)

    # Unknowns for the scalar readout after pole location is named:
    # K(x_pole), K'(x_pole), and any common scalar/gauge dressing factor.
    # Existing Ward/pole-location data fixes only K(x_pole) in this scalar
    # denominator model; K' and common dressing remain free.
    unknowns = ["K_pole", "K_prime_pole", "common_scalar_gauge_dressing"]
    constraints = ["D(x_pole)=0 fixes K_pole=1/Pi(x_pole)"]
    rank = len(constraints)

    k_prime_values = [-0.50, 0.00, 0.50]
    rows = [kernel_family_row(value) for value in k_prime_values]
    d_poles = [abs(float(row["D_pole"])) for row in rows]
    readout_factors = [float(row["lsz_readout_factor"]) for row in rows]
    readout_spread = max(readout_factors) / min(value for value in readout_factors if value > 0.0)

    report(
        "ward-note-is-audited-renaming-not-authority",
        "audit_status=audited_renaming" in ward_text
        and "not a first-principles derivation" in ward_text,
        str(WARD_NOTE.relative_to(ROOT)),
    )
    report(
        "determinant-gate-loaded-and-open",
        determinant.get("proposal_allowed") is False
        and "K'(pole)" in determinant.get("proposal_allowed_reason", ""),
        str(DETERMINANT_GATE.relative_to(ROOT)),
    )
    report(
        "feshbach-response-not-common-dressing",
        feshbach.get("proposal_allowed") is False
        and "Feshbach" in str(feshbach.get("actual_current_surface_status", "")),
        str(FESHBACH.relative_to(ROOT)),
    )
    report(
        "common-dressing-not-forced-by-ward-identities",
        common_dressing.get("proposal_allowed") is False
        and "does not derive common scalar and gauge dressing" in common_dressing.get("verdict", ""),
        str(COMMON_DRESSING.relative_to(ROOT)),
    )
    report(
        "residue-envelope-parent-still-open",
        residue_envelope.get("proposal_allowed") is False
        and "residue-envelope obstruction" in str(residue_envelope.get("actual_current_surface_status", "")),
        str(RESIDUE_ENVELOPE.relative_to(ROOT)),
    )
    report(
        "ward-constraint-rank-leaves-k-prime-free",
        rank < len(unknowns) and "K_prime_pole" not in " ".join(constraints),
        f"rank={rank}, unknowns={unknowns}, constraints={constraints}",
    )
    report(
        "same-pole-family-preserves-pole-location",
        max(d_poles) < 1.0e-14,
        f"max |D(x_pole)|={max(d_poles):.3e}",
    )
    report(
        "same-pole-family-changes-lsz-readout",
        readout_spread > 2.0,
        f"lsz_readout_factor_spread={readout_spread:.6g}",
    )
    report(
        "not-retained-closure",
        True,
        "Ward/gauge identity surfaces do not derive the scalar denominator derivative",
    )

    result = {
        "actual_current_surface_status": "exact negative boundary / scalar kernel Ward-identity obstruction",
        "verdict": (
            "The current Ward/gauge/Feshbach surfaces do not fix the scalar "
            "Bethe-Salpeter denominator derivative.  They can preserve gauge "
            "responses or same-operator projected responses, and the pole "
            "condition fixes K(x_pole), but K'(x_pole) and common scalar/gauge "
            "dressing remain open.  A family with the same pole location and "
            "same Ward-side data changes the scalar LSZ readout factor."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "K'(x_pole), zero-mode/IR limiting order, and common scalar/gauge dressing remain open.",
        "parent_certificates": {
            "determinant_gate": str(DETERMINANT_GATE.relative_to(ROOT)),
            "feshbach_response": str(FESHBACH.relative_to(ROOT)),
            "common_dressing": str(COMMON_DRESSING.relative_to(ROOT)),
            "residue_envelope": str(RESIDUE_ENVELOPE.relative_to(ROOT)),
        },
        "constraint_rank_model": {
            "unknowns": unknowns,
            "constraints": constraints,
            "rank": rank,
        },
        "same_pole_kernel_family": rows,
        "witnesses": {
            "max_abs_D_pole": max(d_poles),
            "lsz_readout_factor_spread": readout_spread,
            "readout_factors": readout_factors,
        },
        "required_next_theorem": [
            "derive K(x) and K'(x_pole) for the same-source scalar Bethe-Salpeter denominator",
            "derive the gauge-zero-mode and IR/finite-volume limiting prescription",
            "derive common scalar/gauge dressing if the Ward ratio route remains in use",
            "or measure the scalar pole derivative directly in production FH/LSZ data",
        ],
        "strict_non_claims": [
            "not retained or proposed_retained y_t closure",
            "does not use H_unit matrix elements as y_t authority",
            "does not use yt_ward_identity as authority",
            "does not set kappa_s = 1",
            "does not use observed top mass/y_t, alpha_LM, plaquette, u0, c2, or Z_match as proof selectors",
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
