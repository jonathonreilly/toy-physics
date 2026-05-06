#!/usr/bin/env python3
"""
PR #230 one-Higgs taste-axis completeness attempt.

Hard route:
    If the Cl(3)/Z3 taste/EW stack proves that exactly one neutral
    top-coupled Higgs axis exists on the same surface, then the orthogonal
    scalar ambiguity in the source-pole readout collapses.

This runner tests whether the current taste scalar theorem plus SM one-Higgs
and EW gauge-mass support already supply that axis/completeness theorem.  They
do not.  The taste theorem is symmetric among three trace-zero taste axes, and
the SM/EW one-Higgs theorems assume a canonical H after it is supplied; neither
derives which taste axis is H, nor excludes orthogonal neutral top-coupled
scalars on the PR230 source surface.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_one_higgs_taste_axis_completeness_attempt_2026-05-06.json"
)

PARENTS = {
    "taste_condensate_oh_bridge": (
        "outputs/yt_pr230_taste_condensate_oh_bridge_audit_2026-05-06.json"
    ),
    "kinetic_taste_mixing_bridge": (
        "outputs/yt_pr230_kinetic_taste_mixing_bridge_attempt_2026-05-06.json"
    ),
    "sm_one_higgs_oh_import_boundary": (
        "outputs/yt_sm_one_higgs_oh_import_boundary_2026-05-03.json"
    ),
    "one_higgs_completeness_gate": (
        "outputs/yt_one_higgs_completeness_orthogonal_null_gate_2026-05-04.json"
    ),
    "no_orthogonal_selection_rule": (
        "outputs/yt_no_orthogonal_top_coupling_selection_rule_no_go_2026-05-02.json"
    ),
    "source_pole_mixing": (
        "outputs/yt_source_pole_canonical_higgs_mixing_obstruction_2026-05-02.json"
    ),
    "canonical_higgs_operator_gate": (
        "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json"
    ),
    "full_positive_assembly": (
        "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json"
    ),
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
}

TEXTS = {
    "taste_scalar_isotropy": "docs/TASTE_SCALAR_ISOTROPY_THEOREM_NOTE.md",
    "sm_one_higgs": "docs/SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md",
    "ew_gauge_mass": "docs/EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md",
}

FUTURE_REOPEN_FILES = {
    "one_higgs_completeness_certificate": (
        "outputs/yt_one_higgs_completeness_certificate_2026-05-04.json"
    ),
    "same_source_ew_action_certificate": (
        "outputs/yt_wz_same_source_ew_action_certificate_2026-05-04.json"
    ),
    "canonical_oh_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "source_higgs_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
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


def load_rel(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def read_rel(rel: str) -> str:
    path = ROOT / rel
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def kron3(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.ndarray:
    return np.kron(a, np.kron(b, c))


def taste_axes() -> list[np.ndarray]:
    i2 = np.eye(2, dtype=complex)
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    return [kron3(sx, i2, i2), kron3(i2, sx, i2), kron3(i2, i2, sx)]


def swap_tensor_factors(which: tuple[int, int]) -> np.ndarray:
    """Permutation matrix on (C^2)^3 swapping two tensor factors."""

    dim = 8
    out = np.zeros((dim, dim), dtype=complex)
    for index in range(dim):
        bits = [(index >> 2) & 1, (index >> 1) & 1, index & 1]
        bits[which[0]], bits[which[1]] = bits[which[1]], bits[which[0]]
        target = (bits[0] << 2) | (bits[1] << 1) | bits[2]
        out[target, index] = 1.0
    return out


def axis_permutation_checks(axes: list[np.ndarray]) -> dict[str, Any]:
    swaps = {
        "swap_01": swap_tensor_factors((0, 1)),
        "swap_12": swap_tensor_factors((1, 2)),
    }
    rows = []
    for name, perm in swaps.items():
        images = []
        for axis in axes:
            conj = perm @ axis @ perm.conj().T
            match = [
                i
                for i, candidate in enumerate(axes)
                if float(np.max(np.abs(conj - candidate))) < 1.0e-14
            ]
            images.append(match[0] if match else None)
        rows.append({"permutation": name, "axis_images": images})
    orbit = set()
    frontier = {0}
    while frontier:
        node = frontier.pop()
        if node in orbit:
            continue
        orbit.add(node)
        for row in rows:
            image = row["axis_images"][node]
            if image is not None and image not in orbit:
                frontier.add(image)
    return {
        "permutation_rows": rows,
        "axis_0_orbit_under_taste_permutations": sorted(orbit),
        "all_axes_same_orbit": orbit == {0, 1, 2},
    }


def counterfamily() -> list[dict[str, Any]]:
    rows = []
    for selected_axis in [0, 1, 2]:
        for y_chi in [-0.25, 0.0, 0.25]:
            rows.append(
                {
                    "selected_higgs_axis": selected_axis,
                    "orthogonal_axis": (selected_axis + 1) % 3,
                    "same_sm_one_higgs_pattern": True,
                    "same_listed_neutral_scalar_charges": True,
                    "orthogonal_top_coupling_y_chi": y_chi,
                    "delta_perp_zero": abs(y_chi) < 1.0e-15,
                }
            )
    return rows


def forbidden_firewall() -> dict[str, bool]:
    return {
        "uses_hunit_matrix_element_readout": False,
        "uses_yt_ward_identity": False,
        "uses_observed_targets": False,
        "uses_alpha_lm_plaquette_or_u0": False,
        "selects_taste_axis_by_fiat": False,
        "sets_orthogonal_top_coupling_to_zero": False,
        "claims_retained_or_proposed_retained": False,
    }


def main() -> int:
    print("PR #230 one-Higgs taste-axis completeness attempt")
    print("=" * 72)

    parents = {name: load_rel(rel) for name, rel in PARENTS.items()}
    texts = {name: read_rel(rel) for name, rel in TEXTS.items()}
    statuses = {name: status(cert) for name, cert in parents.items()}
    missing_parents = [name for name, cert in parents.items() if not cert]
    missing_texts = [name for name, text in texts.items() if not text]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    future_presence = {name: (ROOT / rel).exists() for name, rel in FUTURE_REOPEN_FILES.items()}

    axes = taste_axes()
    axis_checks = axis_permutation_checks(axes)
    family = counterfamily()
    family_varies = len({row["orthogonal_top_coupling_y_chi"] for row in family}) > 1
    axis_choice_varies = len({row["selected_higgs_axis"] for row in family}) == 3

    taste_stack_loaded = (
        "H(phi) = sum_i phi_i S_i" in texts["taste_scalar_isotropy"]
        and "orthogonal taste directions" in texts["taste_scalar_isotropy"]
        and parents["taste_condensate_oh_bridge"].get("proposal_allowed") is False
    )
    taste_stack_not_bridge = (
        "taste-condensate Higgs stack does not supply PR230 O_H bridge"
        in statuses["taste_condensate_oh_bridge"]
        and parents["taste_condensate_oh_bridge"].get("taste_condensate_oh_bridge_audit_passed")
        is True
    )
    kinetic_shortcut_closed = (
        parents["kinetic_taste_mixing_bridge"].get("kinetic_taste_mixing_bridge_closes_pr230")
        is False
        and parents["kinetic_taste_mixing_bridge"].get("exact_negative_boundary_passed")
        is True
    )
    sm_one_higgs_support_not_identity = (
        "SM one-Higgs gauge selection is not PR230 O_H identity"
        in statuses["sm_one_higgs_oh_import_boundary"]
        and parents["sm_one_higgs_oh_import_boundary"].get("proposal_allowed") is False
        and "does not select the numerical entries" in texts["sm_one_higgs"]
    )
    ew_gauge_mass_assumes_h = (
        "Assume a neutral Higgs vacuum" in texts["ew_gauge_mass"]
        and "It does not modify, promote, or close any"
        in texts["ew_gauge_mass"]
    )
    one_higgs_gate_premise_absent = (
        "one-Higgs completeness orthogonal-null theorem; premise absent"
        in statuses["one_higgs_completeness_gate"]
        and parents["one_higgs_completeness_gate"].get("one_higgs_completeness_gate_passed")
        is False
    )
    no_orthogonal_selection_loaded = (
        parents["no_orthogonal_selection_rule"].get(
            "no_orthogonal_top_coupling_selection_rule_gate_passed"
        )
        is False
    )
    source_pole_mixing_loaded = (
        "source-pole canonical-Higgs mixing obstruction" in statuses["source_pole_mixing"]
        and parents["source_pole_mixing"].get("proposal_allowed") is False
    )
    canonical_oh_absent = (
        parents["canonical_higgs_operator_gate"].get("candidate_valid") is False
        and not future_presence["canonical_oh_certificate"]
    )
    retained_still_open = (
        parents["full_positive_assembly"].get("proposal_allowed") is False
        and parents["retained_route"].get("proposal_allowed") is False
    )
    clean_firewall = all(value is False for value in forbidden_firewall().values())

    one_higgs_taste_axis_completeness_derived = (
        axis_checks["all_axes_same_orbit"] is False
        and family_varies is False
        and one_higgs_gate_premise_absent is False
        and canonical_oh_absent is False
        and clean_firewall
    )
    exact_negative_boundary_passed = (
        not missing_parents
        and not missing_texts
        and not proposal_allowed
        and taste_stack_loaded
        and taste_stack_not_bridge
        and kinetic_shortcut_closed
        and sm_one_higgs_support_not_identity
        and ew_gauge_mass_assumes_h
        and axis_checks["all_axes_same_orbit"]
        and axis_choice_varies
        and family_varies
        and one_higgs_gate_premise_absent
        and no_orthogonal_selection_loaded
        and source_pole_mixing_loaded
        and canonical_oh_absent
        and retained_still_open
        and one_higgs_taste_axis_completeness_derived is False
        and clean_firewall
    )

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("text-surfaces-present", not missing_texts, f"missing={missing_texts}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("taste-stack-loaded", taste_stack_loaded, TEXTS["taste_scalar_isotropy"])
    report("taste-stack-not-pr230-bridge", taste_stack_not_bridge, statuses["taste_condensate_oh_bridge"])
    report("kinetic-shortcut-closed", kinetic_shortcut_closed, statuses["kinetic_taste_mixing_bridge"])
    report("sm-one-higgs-support-not-oh-identity", sm_one_higgs_support_not_identity, statuses["sm_one_higgs_oh_import_boundary"])
    report("ew-gauge-mass-assumes-canonical-h", ew_gauge_mass_assumes_h, TEXTS["ew_gauge_mass"])
    report("taste-axes-same-orbit", axis_checks["all_axes_same_orbit"], str(axis_checks))
    report("axis-choice-counterfamily-varies", axis_choice_varies, "selected axis can be 0,1,2")
    report("orthogonal-coupling-counterfamily-varies", family_varies, "y_chi varies with same listed labels")
    report("one-higgs-completeness-premise-absent", one_higgs_gate_premise_absent, statuses["one_higgs_completeness_gate"])
    report("no-orthogonal-selection-loaded", no_orthogonal_selection_loaded, statuses["no_orthogonal_selection_rule"])
    report("source-pole-mixing-loaded", source_pole_mixing_loaded, statuses["source_pole_mixing"])
    report("canonical-oh-currently-absent", canonical_oh_absent, statuses["canonical_higgs_operator_gate"])
    report("one-higgs-taste-axis-completeness-not-derived", one_higgs_taste_axis_completeness_derived is False, "axis selector/completeness absent")
    report("retained-route-still-open", retained_still_open, statuses["retained_route"])
    report("forbidden-firewall-clean", clean_firewall, str(forbidden_firewall()))
    report("exact-negative-boundary-passed", exact_negative_boundary_passed, "one-Higgs/taste-axis shortcut closed")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / one-Higgs taste-axis completeness not "
            "derived from current PR230 taste/EW stack"
        ),
        "conditional_surface_status": (
            "A future same-source EW/Higgs action or one-Higgs completeness "
            "certificate could still collapse the orthogonal scalar ambiguity. "
            "The current taste/EW support does not do so."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The taste scalar theorem leaves the three trace-zero axes in the "
            "same permutation orbit, while the SM/EW one-Higgs theorems assume "
            "canonical H after it is supplied.  No same-surface certificate "
            "selects a taste axis as H or forbids orthogonal neutral top "
            "couplings."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "one_higgs_taste_axis_completeness_derived": one_higgs_taste_axis_completeness_derived,
        "exact_negative_boundary_passed": exact_negative_boundary_passed,
        "axis_permutation_checks": axis_checks,
        "counterfamily": family,
        "future_reopen_files": future_presence,
        "parent_statuses": statuses,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not define O_H by one-Higgs notation or by taste-axis naming",
            "does not set y_chi=0, cos(theta)=1, or source-Higgs overlap to one",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
            "does not globally rule out a future same-source EW action, O_H certificate, W/Z route, Schur rows, or primitive rank-one theorem",
        ],
        "exact_next_action": (
            "Do not use one-Higgs notation or taste-axis language as the "
            "orthogonal-null proof.  Reopen only with a real one-Higgs "
            "completeness certificate, same-source EW/Higgs action, C_sH/C_HH "
            "rows, W/Z response packet, Schur rows, or primitive rank-one "
            "theorem."
        ),
        "forbidden_firewall": forbidden_firewall(),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
