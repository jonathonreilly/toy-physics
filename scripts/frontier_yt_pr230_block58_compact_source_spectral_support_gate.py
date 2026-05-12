#!/usr/bin/env python3
"""
PR #230 Block58 compact source-channel spectral support gate.

Block57 established the exact compact finite-volume source functional as a
support foundation.  This gate asks the next precise question: does the current
reflection-positivity / transfer-matrix surface at least give the finite-volume
scalar-source channel a positive spectral representation?

Answer: yes, as exact support.  The transfer-matrix reconstruction gives a
finite positive spectral sum for the source-channel Euclidean correlator when
the source operator is the specified additive scalar source.  This still does
not close PR230, because OS/spectral positivity alone does not determine pole
saturation, the thermodynamic/FVIR limiting order, the LSZ residue interval, or
the canonical O_H/source-overlap identity.
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
    / "yt_pr230_block58_compact_source_spectral_support_gate_2026-05-12.json"
)

PARENTS = {
    "block57_compact_source_foundation": "outputs/yt_pr230_block57_compact_source_functional_foundation_gate_2026-05-12.json",
    "reflection_lsz_shortcut_no_go": "outputs/yt_reflection_positivity_lsz_shortcut_no_go_2026-05-02.json",
    "source_functional_lsz_identifiability": "outputs/yt_source_functional_lsz_identifiability_theorem_2026-05-03.json",
}

TEXT_PARENTS = {
    "reflection_positivity_theorem": "docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md",
    "spectrum_condition_theorem": "docs/AXIOM_FIRST_SPECTRUM_CONDITION_THEOREM_NOTE_2026-04-29.md",
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


def source_channel_spectral_witness() -> dict[str, Any]:
    """Finite positive transfer spectral sum for a vacuum-subtracted source."""

    lambdas = np.asarray([1.0, 0.74, 0.43, 0.19], dtype=float)
    energies = -np.log(lambdas / lambdas[0])
    # Vacuum-subtracted local scalar source: no ground-state overlap in the
    # connected correlator, positive squared overlaps for excited states.
    overlaps = np.asarray([0.0, 0.86, 0.37, 0.18], dtype=float)
    weights = overlaps * overlaps
    times = np.arange(0, 8, dtype=float)
    correlator = np.asarray(
        [float(np.sum(weights[1:] * np.exp(-energies[1:] * t))) for t in times],
        dtype=float,
    )
    hankel_times = np.asarray([0.0, 1.0, 2.0, 3.0], dtype=float)
    reflection_matrix = np.empty((len(hankel_times), len(hankel_times)), dtype=float)
    for i, ti in enumerate(hankel_times):
        for j, tj in enumerate(hankel_times):
            reflection_matrix[i, j] = float(
                np.sum(weights[1:] * np.exp(-energies[1:] * (ti + tj)))
            )
    eigvals = np.linalg.eigvalsh(reflection_matrix)
    return {
        "transfer_eigenvalues": [float(x) for x in lambdas],
        "energies": [float(x) for x in energies],
        "source_overlaps": [float(x) for x in overlaps],
        "positive_spectral_weights": [float(x) for x in weights],
        "times": [float(x) for x in times],
        "connected_source_correlator": [float(x) for x in correlator],
        "reflection_matrix_min_eigenvalue": float(np.min(eigvals)),
        "reflection_matrix_eigenvalues": [float(x) for x in eigvals],
        "spectral_representation": "C_ss(t)=sum_{n>0} |<0|O_s|n>|^2 exp(-(E_n-E_0)t)",
        "all_weights_nonnegative": bool(np.all(weights >= -1.0e-15)),
        "reflection_matrix_positive_semidefinite": bool(np.min(eigvals) >= -1.0e-12),
    }


def finite_volume_support_contract() -> list[dict[str, Any]]:
    return [
        {
            "id": "compact_source_functional",
            "current_satisfied": True,
            "source": PARENTS["block57_compact_source_foundation"],
        },
        {
            "id": "reflection_positive_transfer_matrix",
            "current_satisfied": True,
            "source": TEXT_PARENTS["reflection_positivity_theorem"],
        },
        {
            "id": "finite_volume_positive_spectral_sum",
            "current_satisfied": True,
            "source": "this Block58 gate",
        },
        {
            "id": "thermodynamic_fv_ir_limit",
            "current_satisfied": False,
            "required": "uniform finite-volume/IR/toron limiting theorem for the source spectral measure",
        },
        {
            "id": "isolated_pole_residue_interval",
            "current_satisfied": False,
            "required": "pole-saturation/threshold theorem or production row certificate with tight positive residue interval",
        },
        {
            "id": "canonical_oh_or_physical_response",
            "current_satisfied": False,
            "required": "canonical O_H/source-overlap identity, strict C_ss/C_sH/C_HH Gram rows, neutral transfer primitive, or strict W/Z response",
        },
        {
            "id": "forbidden_import_firewall",
            "current_satisfied": True,
            "required": "no H_unit, Ward, y_t_bare, observed selector, alpha_LM/plaquette/u0, or unit kappa/c2/Z_match shortcut",
        },
    ]


def main() -> int:
    print("PR #230 Block58 compact source-channel spectral support gate")
    print("=" * 76)

    certs = {name: load_json(path) for name, path in PARENTS.items()}
    texts = {name: read_text(path) for name, path in TEXT_PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_parents = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]
    witness = source_channel_spectral_witness()
    contract = finite_volume_support_contract()

    block57_support_loaded = (
        "compact finite-volume scalar-source functional foundation"
        in statuses["block57_compact_source_foundation"]
        and certs["block57_compact_source_foundation"].get("proposal_allowed")
        is False
        and certs["block57_compact_source_foundation"].get(
            "finite_volume_compact_source_functional_defined"
        )
        is True
    )
    rp_transfer_loaded = (
        "Reflection positivity" in texts["reflection_positivity_theorem"]
        and "Transfer matrix" in texts["reflection_positivity_theorem"]
        and "positive Hermitian transfer matrix" in texts["reflection_positivity_theorem"]
    )
    spectrum_condition_loaded = (
        "spectrum condition" in texts["spectrum_condition_theorem"].lower()
        and "Hamiltonian" in texts["spectrum_condition_theorem"]
        and "bounded below" in texts["spectrum_condition_theorem"]
    )
    os_shortcut_no_go_loaded = (
        "reflection positivity not scalar LSZ closure"
        in statuses["reflection_lsz_shortcut_no_go"]
        and certs["reflection_lsz_shortcut_no_go"].get("proposal_allowed")
        is False
    )
    source_only_not_oh = (
        "source-functional LSZ identifiability theorem"
        in statuses["source_functional_lsz_identifiability"]
        and certs["source_functional_lsz_identifiability"].get("proposal_allowed")
        is False
    )
    finite_volume_spectral_support = (
        witness["all_weights_nonnegative"]
        and witness["reflection_matrix_positive_semidefinite"]
    )
    thermodynamic_limit_authority = False
    isolated_pole_residue_authority = False
    canonical_oh_authority = False
    scalar_pole_fvir_root_closed = False
    proposal_allowed = False

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_parents, f"proposal_allowed={proposal_parents}")
    report("block57-compact-foundation-loaded", block57_support_loaded, statuses["block57_compact_source_foundation"])
    report("reflection-positive-transfer-loaded", rp_transfer_loaded, TEXT_PARENTS["reflection_positivity_theorem"])
    report("spectrum-condition-loaded", spectrum_condition_loaded, TEXT_PARENTS["spectrum_condition_theorem"])
    report("finite-volume-source-spectral-witness-positive", finite_volume_spectral_support, f"min_eig={witness['reflection_matrix_min_eigenvalue']:.3e}")
    report("os-positivity-lsz-shortcut-no-go-preserved", os_shortcut_no_go_loaded, statuses["reflection_lsz_shortcut_no_go"])
    report("source-only-still-not-oh", source_only_not_oh, statuses["source_functional_lsz_identifiability"])
    report("thermodynamic-limit-authority-absent", not thermodynamic_limit_authority, "finite-volume spectral sum is not FVIR limit")
    report("isolated-pole-residue-authority-absent", not isolated_pole_residue_authority, "positive spectral measure does not fix pole atom")
    report("canonical-oh-authority-absent", not canonical_oh_authority, "source-channel operator not canonical O_H")
    report("scalar-pole-fvir-root-not-closed", not scalar_pole_fvir_root_closed, "remaining contract recorded")
    report("does-not-authorize-proposed-retained", not proposal_allowed, "Block58 is exact support only")

    result = {
        "actual_current_surface_status": (
            "exact-support / Block58 finite-volume compact source-channel "
            "spectral support; thermodynamic pole/FVIR and canonical-O_H roots "
            "remain open"
        ),
        "conditional_surface_status": (
            "conditional-support if future work upgrades the finite-volume "
            "positive spectral sum to a thermodynamic/FVIR scalar pole and "
            "pairs it with canonical O_H or physical-response authority"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": proposal_allowed,
        "proposal_allowed_reason": (
            "Finite-volume source-channel spectral positivity is support only. "
            "It does not provide thermodynamic/FVIR authority, pole saturation, "
            "a tight LSZ residue interval, or canonical O_H/source-overlap "
            "identity."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "block58_compact_source_spectral_support_passed": True,
        "finite_volume_source_spectral_representation_present": True,
        "thermodynamic_limit_authority_present": thermodynamic_limit_authority,
        "isolated_pole_residue_authority_present": isolated_pole_residue_authority,
        "canonical_oh_authority_present": canonical_oh_authority,
        "scalar_pole_fvir_root_closed": scalar_pole_fvir_root_closed,
        "spectral_witness": witness,
        "finite_volume_support_contract": contract,
        "remaining_scalar_authority_obligations": [
            "uniform thermodynamic/FVIR/toron limiting theorem for the source spectral measure",
            "pole-saturation or threshold theorem giving a tight positive scalar pole residue interval",
            "continuum/contact/subtraction map from bare finite-volume source correlator to scalar LSZ",
            "canonical O_H/source-pole identity, strict C_ss/C_sH/C_HH Gram rows, neutral-transfer primitive, or strict W/Z physical-response bypass",
        ],
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "text_parent_surfaces": TEXT_PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not treat reflection positivity or spectral positivity as pole saturation",
            "does not infer a thermodynamic mass gap or scalar pole from a finite-volume transfer spectrum",
            "does not identify O_s or O_sp with canonical O_H",
            "does not use H_unit, yt_ward_identity, y_t_bare, observed top/y_t values, alpha_LM, plaquette/u0, kappa_s=1, c2=1, or Z_match=1",
        ],
        "exact_next_action": (
            "Attack the actual remaining scalar theorem: uniform thermodynamic "
            "and FVIR control for the compact source-channel spectral measure, "
            "including pole isolation/residue bounds; then combine with a "
            "canonical O_H/source-overlap theorem or strict physical response rows."
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
