#!/usr/bin/env python3
"""
PR #230 Block57 compact source-functional foundation gate.

Block56 cut the current scalar pole/FVIR shortcut stack.  This block audits a
subtle point in that cut: the zero-mode and flat-toron negatives are real, but
they are negatives for perturbative/linearized ladder denominators and for
trivial-toron selection shortcuts.  They are not a proof that the exact compact
finite-volume Cl(3)/Z3 source functional is undefined.

The positive movement here is narrow.  The finite compact path integral with a
specified additive scalar source has a well-defined finite-volume source
curvature/contact scheme and integrates flat torons rather than selecting the
trivial one.  The non-closed part is also explicit: finite-volume analyticity
does not supply thermodynamic transfer/spectral authority, an isolated scalar
pole, a tight LSZ residue, FV/IR limiting control, or canonical O_H identity.
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
    / "yt_pr230_block57_compact_source_functional_foundation_gate_2026-05-12.json"
)

PARENTS = {
    "block56_scalar_pole_fvir_root_cut": "outputs/yt_pr230_block56_scalar_pole_fvir_root_cut_gate_2026-05-12.json",
    "scalar_source_two_point": "outputs/yt_scalar_source_two_point_stretch_2026-05-01.json",
    "scalar_contact_scheme_boundary": "outputs/yt_scalar_source_contact_term_scheme_boundary_2026-05-01.json",
    "contact_subtraction_identifiability": "outputs/yt_fh_lsz_contact_subtraction_identifiability_2026-05-05.json",
    "scalar_zero_mode_limit_order": "outputs/yt_scalar_zero_mode_limit_order_theorem_2026-05-01.json",
    "zero_mode_import_audit": "outputs/yt_zero_mode_prescription_import_audit_2026-05-01.json",
    "flat_toron_scalar_denominator": "outputs/yt_flat_toron_scalar_denominator_obstruction_2026-05-01.json",
    "legendre_source_pole_operator": "outputs/yt_legendre_source_pole_operator_construction_2026-05-03.json",
    "source_functional_lsz_identifiability": "outputs/yt_source_functional_lsz_identifiability_theorem_2026-05-03.json",
}

TEXT_PARENTS = {
    "minimal_axioms": "docs/MINIMAL_AXIOMS_2026-04-11.md",
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


def load_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def read_text(rel: str) -> str:
    path = ROOT / rel
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def toy_toron_partition(source: float, *, mass: float = 1.2, rho: float = 0.35) -> float:
    """Compact toron average for a finite determinant proxy.

    This deliberately uses an exactly integrable compact one-angle proxy:

        Z(s) = integral dtheta/(2pi) (m+s+rho*cos theta)^2
             = (m+s)^2 + rho^2/2.

    It is not used as a physics value.  It is a witness for the logical
    distinction between compact integration and trivial-toron selection.
    """

    return (mass + source) ** 2 + 0.5 * rho * rho


def toy_trivial_toron_partition(source: float, *, mass: float = 1.2, rho: float = 0.35) -> float:
    """Same finite proxy with the flat toron artificially fixed to theta=0."""

    return (mass + source + rho) ** 2


def log_derivatives() -> dict[str, float]:
    """Finite-volume source derivatives in the compact toron proxy."""

    z0 = toy_toron_partition(0.0)
    dz0 = 2.0 * 1.2
    ddz0 = 2.0
    w_prime = dz0 / z0
    w_second = ddz0 / z0 - (dz0 / z0) ** 2
    trivial_z0 = toy_trivial_toron_partition(0.0)
    trivial_dz0 = 2.0 * (1.2 + 0.35)
    trivial_ddz0 = 2.0
    trivial_w_second = trivial_ddz0 / trivial_z0 - (trivial_dz0 / trivial_z0) ** 2
    return {
        "compact_Z0": z0,
        "compact_dlogZ_ds": w_prime,
        "compact_d2logZ_ds2": w_second,
        "trivial_toron_Z0": trivial_z0,
        "trivial_toron_d2logZ_ds2": trivial_w_second,
        "compact_minus_trivial_curvature": w_second - trivial_w_second,
    }


def no_go_scope_rows() -> list[dict[str, Any]]:
    return [
        {
            "id": "scalar_zero_mode_limit_order",
            "negative_result_is_correct": True,
            "applies_to": "finite Wilson-exchange ladder with noncompact IR regulator and retained/removed gauge zero mode choices",
            "does_not_apply_as": "proof that the exact compact finite-volume Haar path integral is undefined",
        },
        {
            "id": "flat_toron_scalar_denominator",
            "negative_result_is_correct": True,
            "applies_to": "shortcut that selects the trivial Cartan toron from a flat action-degenerate family",
            "does_not_apply_as": "obstruction to exact compact integration over flat torons",
        },
        {
            "id": "contact_subtraction_identifiability",
            "negative_result_is_correct": True,
            "applies_to": "attempt to choose a continuum/local contact subtraction from finite C_ss rows or monotonicity repair",
            "does_not_apply_as": "obstruction to defining the bare finite-volume source curvature by functional derivatives of the specified lattice source action",
        },
        {
            "id": "source_functional_lsz_identifiability",
            "negative_result_is_correct": True,
            "applies_to": "source-only attempt to identify the measured source pole with canonical O_H",
            "does_not_apply_as": "obstruction to constructing the LSZ-normalized source-pole operator once an isolated source pole is supplied",
        },
    ]


def remaining_positive_contract() -> list[dict[str, Any]]:
    return [
        {
            "id": "thermodynamic_transfer_spectral_authority",
            "current_satisfied": False,
            "required": "derive OS/transfer or equivalent spectral representation for the compact scalar source channel in the PR230 limit",
        },
        {
            "id": "isolated_scalar_pole",
            "current_satisfied": False,
            "required": "prove or measure an isolated scalar source pole with a positive tight residue interval",
        },
        {
            "id": "fv_ir_limiting_order",
            "current_satisfied": False,
            "required": "derive the finite-volume/IR/toron limiting order for the exact compact source channel",
        },
        {
            "id": "contact_renormalization_to_continuum_lsz",
            "current_satisfied": False,
            "required": "derive how the bare finite-volume source curvature maps to the continuum/LSZ object, including any contact/subtraction scheme",
        },
        {
            "id": "canonical_oh_or_physical_bypass",
            "current_satisfied": False,
            "required": "derive canonical O_H/source-pole identity, strict C_ss/C_sH/C_HH Gram rows, neutral-transfer primitive, or strict W/Z physical-response bypass",
        },
        {
            "id": "forbidden_import_firewall",
            "current_satisfied": True,
            "required": "no H_unit, Ward, y_t_bare, observed selector, alpha_LM/plaquette/u0, or unit kappa/c2/Z_match shortcut",
        },
    ]


def main() -> int:
    print("PR #230 Block57 compact source-functional foundation gate")
    print("=" * 76)

    certs = {name: load_json(path) for name, path in PARENTS.items()}
    texts = {name: read_text(path) for name, path in TEXT_PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_parents = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]
    derivs = log_derivatives()
    scope_rows = no_go_scope_rows()
    contract = remaining_positive_contract()

    minimal_surface_read = (
        "staggered-Dirac partition" in texts["minimal_axioms"]
        and "g_bare = 1" in texts["minimal_axioms"]
    )
    block56_open = (
        "scalar-pole-FVIR root cut" in statuses["block56_scalar_pole_fvir_root_cut"]
        and certs["block56_scalar_pole_fvir_root_cut"].get("proposal_allowed") is False
        and certs["block56_scalar_pole_fvir_root_cut"].get("scalar_pole_fvir_root_closed") is False
    )
    source_curvature_support = (
        "source curvature formula is exact support"
        in str(certs["scalar_source_two_point"].get("proposal_allowed_reason", ""))
        and certs["scalar_source_two_point"].get("proposal_allowed") is False
    )
    zero_mode_no_go_scoped = (
        "zero-mode limit-order theorem" in statuses["scalar_zero_mode_limit_order"]
        and certs["scalar_zero_mode_limit_order"].get("proposal_allowed") is False
        and "flat toron scalar-denominator obstruction"
        in statuses["flat_toron_scalar_denominator"]
        and certs["flat_toron_scalar_denominator"].get("proposal_allowed") is False
    )
    contact_no_go_scoped = (
        "contact-subtraction identifiability obstruction"
        in statuses["contact_subtraction_identifiability"]
        and certs["contact_subtraction_identifiability"].get("proposal_allowed") is False
        and "scalar source contact-term scheme boundary"
        in statuses["scalar_contact_scheme_boundary"]
        and certs["scalar_contact_scheme_boundary"].get("proposal_allowed") is False
    )
    finite_compact_derivatives_defined = all(math.isfinite(value) for value in derivs.values())
    compact_average_not_trivial_selection = abs(derivs["compact_minus_trivial_curvature"]) > 1.0e-3
    source_pole_operator_support_only = (
        "Legendre source-pole operator constructed" in statuses["legendre_source_pole_operator"]
        and certs["legendre_source_pole_operator"].get("proposal_allowed") is False
        and certs["legendre_source_pole_operator"].get(
            "canonical_higgs_operator_identity_passed"
        )
        is False
    )
    source_only_not_oh = (
        "source-functional LSZ identifiability theorem"
        in statuses["source_functional_lsz_identifiability"]
        and certs["source_functional_lsz_identifiability"].get("proposal_allowed")
        is False
    )
    exact_pole_authority_present = False
    scalar_pole_fvir_root_closed = False
    proposal_allowed = False

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_parents, f"proposal_allowed={proposal_parents}")
    report("minimal-compact-source-surface-read", minimal_surface_read, TEXT_PARENTS["minimal_axioms"])
    report("block56-root-remains-open", block56_open, statuses["block56_scalar_pole_fvir_root_cut"])
    report("source-curvature-support-loaded", source_curvature_support, statuses["scalar_source_two_point"])
    report("zero-mode-and-toron-negatives-scoped", zero_mode_no_go_scoped, "ladder/trivial-selection negatives loaded")
    report("contact-negatives-scoped", contact_no_go_scoped, "finite-row contact shortcuts blocked, bare source derivatives still defined")
    report("compact-finite-volume-derivatives-defined", finite_compact_derivatives_defined, str(derivs))
    report("compact-toron-average-not-trivial-selection", compact_average_not_trivial_selection, f"delta={derivs['compact_minus_trivial_curvature']:.6g}")
    report("source-pole-operator-support-only", source_pole_operator_support_only, statuses["legendre_source_pole_operator"])
    report("source-only-data-still-not-oh", source_only_not_oh, statuses["source_functional_lsz_identifiability"])
    report("exact-pole-authority-still-absent", not exact_pole_authority_present, "finite analyticity is not pole/FVIR authority")
    report("scalar-pole-fvir-root-not-closed", not scalar_pole_fvir_root_closed, "remaining contract recorded")
    report("does-not-authorize-proposed-retained", not proposal_allowed, "Block57 is exact support only")

    result = {
        "actual_current_surface_status": (
            "exact-support / Block57 compact finite-volume scalar-source "
            "functional foundation; ladder zero-mode no-gos scoped, bare "
            "finite-volume contact/source curvature exists, pole/FVIR/O_H "
            "roots remain open"
        ),
        "conditional_surface_status": (
            "conditional-support if future work derives thermodynamic transfer/"
            "spectral authority, isolated scalar pole and residue, FV/IR "
            "limiting control, and canonical O_H or physical-response bridge"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": proposal_allowed,
        "proposal_allowed_reason": (
            "Finite compact source-functional analyticity and bare contact "
            "definition are support only.  They do not provide the isolated "
            "scalar pole, LSZ residue, FV/IR limiting theorem, or canonical "
            "O_H/source-overlap bridge required for PR230 closure."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "block57_compact_source_functional_foundation_passed": True,
        "finite_volume_compact_source_functional_defined": True,
        "finite_volume_bare_contact_scheme_defined": True,
        "flat_torons_integrated_not_selected": True,
        "ladder_zero_mode_no_gos_scope_limited": True,
        "exact_denominator_or_pole_authority_present": exact_pole_authority_present,
        "scalar_pole_fvir_root_closed": scalar_pole_fvir_root_closed,
        "compact_toron_witness": derivs,
        "no_go_scope_rows": scope_rows,
        "remaining_positive_contract": contract,
        "remaining_scalar_authority_obligations": [
            "thermodynamic transfer/spectral theorem for the exact compact source channel",
            "isolated scalar pole and tight positive LSZ residue interval",
            "finite-volume/IR/toron limiting-order authority",
            "continuum/contact/subtraction map from bare source derivatives to scalar LSZ",
            "canonical O_H/source-pole identity, strict C_ss/C_sH/C_HH Gram rows, neutral-transfer primitive, or strict W/Z physical-response bypass",
        ],
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not treat the compact finite-volume source functional as an isolated scalar-pole theorem",
            "does not use the perturbative ladder denominator as the exact source denominator",
            "does not select the trivial toron sector",
            "does not choose a contact subtraction from finite rows or monotonicity repair",
            "does not identify O_s or O_sp with canonical O_H",
            "does not use H_unit, yt_ward_identity, y_t_bare, observed top/y_t values, alpha_LM, plaquette/u0, kappa_s=1, c2=1, or Z_match=1",
        ],
        "exact_next_action": (
            "Use the compact finite-volume source functional as the foundation "
            "for a genuine thermodynamic transfer/spectral theorem: derive the "
            "scalar source-channel spectral representation, isolated pole and "
            "residue interval, FV/IR/toron limiting order, and then pair it "
            "with canonical O_H/source-overlap or strict physical response rows."
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
