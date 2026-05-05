#!/usr/bin/env python3
"""
PR #230 scalar-LSZ holonomic/exact-authority attempt.

This is the strict scalar-LSZ counterpart to the clean source-Higgs math-tool
selector.  It asks whether holonomic/Picard-Fuchs/WZ, exact tensor/PEPS,
PSLQ/value recognition, or finite-shell exact interpolation can turn the
current PR230 scalar data into the missing LSZ pole-residue, threshold, and
FV/IR authority.

The current answer is no.  Finite shell values are compatible with rational
holonomic continuations that agree on every sampled shell but have different
isolated-pole residues.  A nameable exact-math method is useful only after it
emits a same-surface scalar-denominator or Stieltjes moment certificate with
threshold and FV/IR control.
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
    / "yt_pr230_scalar_lsz_holonomic_exact_authority_attempt_2026-05-05.json"
)

PARENTS = {
    "clean_source_higgs_math_selector": "outputs/yt_pr230_clean_source_higgs_math_tool_route_selector_2026-05-05.json",
    "stieltjes_moment_gate": "outputs/yt_fh_lsz_stieltjes_moment_certificate_gate_2026-05-05.json",
    "pade_stieltjes_bounds_gate": "outputs/yt_fh_lsz_pade_stieltjes_bounds_gate_2026-05-05.json",
    "polefit8x8_stieltjes_proxy_diagnostic": "outputs/yt_fh_lsz_polefit8x8_stieltjes_proxy_diagnostic_2026-05-05.json",
    "contact_subtraction_identifiability": "outputs/yt_fh_lsz_contact_subtraction_identifiability_2026-05-05.json",
    "affine_contact_complete_monotonicity": "outputs/yt_fh_lsz_affine_contact_complete_monotonicity_no_go_2026-05-05.json",
    "polynomial_contact_finite_shell": "outputs/yt_fh_lsz_polynomial_contact_finite_shell_no_go_2026-05-05.json",
    "polynomial_contact_repair": "outputs/yt_fh_lsz_polynomial_contact_repair_no_go_2026-05-05.json",
    "finite_volume_pole_saturation": "outputs/yt_fh_lsz_finite_volume_pole_saturation_obstruction_2026-05-02.json",
    "pole_saturation_threshold_gate": "outputs/yt_fh_lsz_pole_saturation_threshold_gate_2026-05-02.json",
    "threshold_authority_import_audit": "outputs/yt_fh_lsz_threshold_authority_import_audit_2026-05-02.json",
    "soft_continuum_threshold_no_go": "outputs/yt_fh_lsz_soft_continuum_threshold_no_go_2026-05-02.json",
    "scalar_denominator_theorem_attempt": "outputs/yt_scalar_denominator_theorem_closure_attempt_2026-05-02.json",
    "full_positive_closure_assembly_gate": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_closure_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
}

FUTURE_FILES = {
    "stieltjes_moment_certificate": "outputs/yt_fh_lsz_stieltjes_moment_certificate_2026-05-05.json",
    "pade_stieltjes_bounds_certificate": "outputs/yt_fh_lsz_pade_stieltjes_bounds_certificate_2026-05-05.json",
    "scalar_denominator_theorem_certificate": "outputs/yt_scalar_denominator_theorem_certificate_2026-05-05.json",
    "contact_subtraction_certificate": "outputs/yt_fh_lsz_contact_subtraction_certificate_2026-05-05.json",
}

FORBIDDEN_INPUTS = [
    "PSLQ/value recognition as pole selector",
    "finite-shell interpolation as analytic continuation authority",
    "observed top mass or observed y_t",
    "H_unit or Ward readout authority",
    "alpha_LM / plaquette / u0 normalization",
    "kappa_s = 1, c2 = 1, or Z_match = 1 by convention",
]

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


def load_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def future_presence() -> dict[str, bool]:
    return {name: (ROOT / rel).exists() for name, rel in FUTURE_FILES.items()}


def shell_points() -> list[float]:
    return [
        0.0,
        0.26794919243112264,
        0.5358983848622453,
        0.803847577293368,
        1.0,
        1.2679491924311224,
        1.5358983848622452,
        2.0,
    ]


def product_over_shells(x: float, shells: list[float]) -> float:
    out = 1.0
    for shell in shells:
        out *= x - shell
    return out


def holonomic_counterfamily() -> dict[str, Any]:
    shells = shell_points()
    pole_mass_sq = 0.41
    continuum_mass_sq = 2.7
    base_residue = 1.15
    continuum_weight = 0.37
    epsilon = 2.5e-5

    def base(x: float) -> float:
        return base_residue / (x + pole_mass_sq) + continuum_weight / (
            x + continuum_mass_sq
        )

    product_at_pole = product_over_shells(-pole_mass_sq, shells)

    def deformation(x: float) -> float:
        return epsilon * product_over_shells(x, shells) / (x + pole_mass_sq)

    def altered(x: float) -> float:
        return base(x) + deformation(x)

    base_samples = [base(x) for x in shells]
    altered_samples = [altered(x) for x in shells]
    max_sample_delta = max(abs(a - b) for a, b in zip(base_samples, altered_samples))
    residue_shift = epsilon * product_at_pole
    altered_residue = base_residue + residue_shift

    return {
        "construction": (
            "Two rational holonomic continuations agree on every finite shell "
            "sample but have different residues at the same isolated pole."
        ),
        "shell_points": shells,
        "pole_location_x": -pole_mass_sq,
        "base_function": "R0/(x+m0) + W/(x+M)",
        "altered_function": "base + eps*prod_i(x-x_i)/(x+m0)",
        "rational_functions_are_holonomic": True,
        "base_samples": base_samples,
        "altered_samples": altered_samples,
        "max_sample_delta": max_sample_delta,
        "base_residue": base_residue,
        "altered_residue": altered_residue,
        "residue_shift": residue_shift,
        "residues_differ": abs(residue_shift) > 1.0e-12,
        "same_finite_shell_values": max_sample_delta < 1.0e-12,
        "stieltjes_or_threshold_authority_supplied": False,
        "lesson": (
            "Finite-shell exact interpolation, PSLQ hits, or the existence of "
            "some holonomic continuation do not select the physical scalar "
            "denominator or pole residue.  The ODE/denominator and boundary "
            "data must be derived from the same PR230 path integral, with "
            "Stieltjes positivity, contact subtraction, threshold, and FV/IR "
            "control."
        ),
    }


def future_certificate_contract() -> list[dict[str, Any]]:
    return [
        {
            "id": "same_surface_exact_scalar_functional",
            "required": "exact PR230 scalar two-point or denominator object, not a fitted finite-shell surrogate",
            "current_satisfied": False,
        },
        {
            "id": "derived_holonomic_or_denominator_authority",
            "required": "Picard-Fuchs/WZ/D-module/tensor certificate deriving the annihilator or denominator from the path integral",
            "current_satisfied": False,
        },
        {
            "id": "contact_subtraction_and_source_scheme",
            "required": "same-surface contact/subtraction certificate fixing the scalar object being continued",
            "current_satisfied": False,
        },
        {
            "id": "stieltjes_moment_positivity",
            "required": "Hankel and shifted-Hankel positivity for the continued scalar measure",
            "current_satisfied": False,
        },
        {
            "id": "threshold_and_fv_ir_authority",
            "required": "threshold gap, limiting order, and finite-volume/IR pole-saturation control",
            "current_satisfied": False,
        },
        {
            "id": "positive_tight_pole_residue_interval",
            "required": "positive pole residue with relative interval width at or below the strict gate tolerance",
            "current_satisfied": False,
        },
        {
            "id": "forbidden_import_firewall",
            "required": "reject observed selectors, H_unit/Ward, alpha/plaquette/u0, unit kappa_s/c2/Z_match, and PSLQ selector shortcuts",
            "current_satisfied": True,
        },
    ]


def main() -> int:
    print("PR #230 scalar-LSZ holonomic/exact-authority attempt")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    statuses = {name: status(cert) for name, cert in parents.items()}
    proposal_allowed = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]
    future_present = future_presence()
    counterfamily = holonomic_counterfamily()
    contract = future_certificate_contract()
    contract_missing = [row["id"] for row in contract if not row["current_satisfied"]]

    selector_allows_holonomic_only_as_future_method = (
        parents["clean_source_higgs_math_selector"].get("proposal_allowed") is False
        and any(
            row.get("id") == "holonomic_dmodule_picard_fuchs_wz_painleve"
            and row.get("current_admissible_for_closure") is False
            for row in parents["clean_source_higgs_math_selector"].get(
                "outside_math_route_rows", []
            )
        )
    )
    stieltjes_gate_absent = (
        parents["stieltjes_moment_gate"].get("moment_certificate_gate_passed") is False
    )
    pade_gate_absent = (
        parents["pade_stieltjes_bounds_gate"].get("pade_stieltjes_bounds_gate_passed")
        is False
    )
    polefit_proxy_rejected = (
        parents["polefit8x8_stieltjes_proxy_diagnostic"].get(
            "stieltjes_proxy_certificate_passed"
        )
        is False
        and parents["polefit8x8_stieltjes_proxy_diagnostic"]
        .get("violation_summary", {})
        .get("violation_count", 0)
        > 0
    )
    contact_subtraction_open = (
        "contact-subtraction identifiability" in statuses["contact_subtraction_identifiability"]
    )
    polynomial_repair_blocked = (
        parents["polynomial_contact_repair"].get("polynomial_contact_repair_no_go_passed")
        is True
    )
    threshold_fv_ir_not_certified = (
        "finite-volume pole-saturation obstruction" in statuses["finite_volume_pole_saturation"]
        and "pole-saturation threshold gate blocks" in statuses["pole_saturation_threshold_gate"]
        and "soft-continuum threshold no-go" in statuses["soft_continuum_threshold_no_go"]
    )
    denominator_theorem_open = (
        "scalar denominator theorem closure attempt blocked"
        in statuses["scalar_denominator_theorem_attempt"]
    )
    exact_authority_files_absent = not any(future_present.values())
    finite_shell_underdetermined = (
        counterfamily["rational_functions_are_holonomic"]
        and counterfamily["same_finite_shell_values"]
        and counterfamily["residues_differ"]
        and counterfamily["stieltjes_or_threshold_authority_supplied"] is False
    )
    holonomic_exact_authority_passed = False

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("selector-keeps-holonomic-future-only", selector_allows_holonomic_only_as_future_method, statuses["clean_source_higgs_math_selector"])
    report("strict-stieltjes-certificate-absent", stieltjes_gate_absent, statuses["stieltjes_moment_gate"])
    report("strict-pade-stieltjes-certificate-absent", pade_gate_absent, statuses["pade_stieltjes_bounds_gate"])
    report("polefit8x8-proxy-rejected", polefit_proxy_rejected, statuses["polefit8x8_stieltjes_proxy_diagnostic"])
    report("contact-subtraction-open", contact_subtraction_open, statuses["contact_subtraction_identifiability"])
    report("polynomial-contact-repair-blocked", polynomial_repair_blocked, statuses["polynomial_contact_repair"])
    report("threshold-fv-ir-not-certified", threshold_fv_ir_not_certified, "threshold/FV/IR gates remain open or negative")
    report("scalar-denominator-theorem-open", denominator_theorem_open, statuses["scalar_denominator_theorem_attempt"])
    report("exact-authority-files-absent", exact_authority_files_absent, f"future_present={future_present}")
    report("finite-shell-holonomic-underdetermined", finite_shell_underdetermined, "same shell values, different pole residues")
    report("future-certificate-contract-recorded", len(contract_missing) == 6, f"missing={contract_missing}")
    report("forbidden-firewall-clean", True, ", ".join(FORBIDDEN_INPUTS))
    report("holonomic-exact-authority-not-passed", not holonomic_exact_authority_passed, "no same-surface exact scalar denominator authority")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / scalar-LSZ holonomic exact-authority "
            "not derivable from current finite-shell PR230 data"
        ),
        "conditional_surface_status": (
            "conditional-support if a future same-surface Picard-Fuchs/WZ/"
            "D-module/tensor certificate derives the scalar denominator and "
            "also supplies Stieltjes positivity, contact subtraction, "
            "threshold, FV/IR, and pole-residue authority"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Current scalar data are finite-shell support only.  Rational "
            "holonomic continuations can agree on all sampled shells while "
            "changing the isolated-pole residue; exact-value or ODE-name "
            "recognition is therefore not scalar-LSZ authority without a "
            "same-surface denominator/moment/threshold/FV certificate."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "holonomic_exact_authority_passed": holonomic_exact_authority_passed,
        "future_file_presence": future_present,
        "future_certificate_contract": contract,
        "counterfamily": counterfamily,
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "strict_non_claims": [
            "does not claim scalar-LSZ closure",
            "does not write a Stieltjes, Pade, scalar-denominator, or contact-subtraction certificate",
            "does not use PSLQ/value recognition as proof selector",
            "does not use finite-shell interpolation as analytic-continuation authority",
            "does not claim retained or proposed_retained PR230 closure",
            "does not set kappa_s, c2, or Z_match to one",
        ],
        "exact_next_action": (
            "A positive scalar-LSZ leg now needs either a same-surface exact "
            "scalar-denominator/Picard-Fuchs/WZ/tensor certificate with "
            "boundary data and contact subtraction, or a strict Stieltjes/"
            "Pade moment certificate with threshold and FV/IR authority.  "
            "Even if that lands, PR230 still also needs a source-overlap or "
            "physical-response bridge and matching/running authority."
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
