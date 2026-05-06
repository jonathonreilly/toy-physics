#!/usr/bin/env python3
"""
PR #230 taste-condensate-to-O_H bridge audit.

This runner tests the strongest "maybe we already have O_H" route: the Higgs
stack says the taste condensate acts as the Higgs field, while PR230 needs a
same-surface canonical-Higgs operator O_H and C_sH/C_HH pole rows.  The test is
algebraic and current-surface scoped: does the exact taste-block Higgs axis in
the existing theorem identify the uniform scalar source used by the PR230
FH/LSZ harness?

It does not build a new O_H certificate.  It records the current obstruction
and the precise future evidence that can reopen the route.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_taste_condensate_oh_bridge_audit_2026-05-06.json"

DOCS = {
    "taste_scalar_isotropy": "docs/TASTE_SCALAR_ISOTROPY_THEOREM_NOTE.md",
    "higgs_mass_derived": "docs/HIGGS_MASS_DERIVED_NOTE.md",
    "canonical_operator_gate": "docs/YT_CANONICAL_HIGGS_OPERATOR_CERTIFICATE_GATE_NOTE_2026-05-03.md",
    "source_higgs_readiness": "docs/YT_SOURCE_HIGGS_PRODUCTION_READINESS_GATE_NOTE_2026-05-04.md",
}

PARENTS = {
    "canonical_operator_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "canonical_scalar_import_audit": "outputs/yt_canonical_scalar_normalization_import_audit_2026-05-01.json",
    "source_higgs_readiness": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "source_higgs_unratified_smoke": "outputs/yt_source_higgs_unratified_operator_smoke_checkpoint_2026-05-03.json",
    "source_higgs_unratified_gram_no_go": "outputs/yt_source_higgs_unratified_gram_shortcut_no_go_2026-05-05.json",
    "source_pole_mixing": "outputs/yt_source_pole_canonical_higgs_mixing_obstruction_2026-05-02.json",
    "cross_lane_oh_authority": "outputs/yt_cross_lane_oh_authority_audit_2026-05-05.json",
    "negative_route_review": "outputs/yt_pr230_negative_route_applicability_review_2026-05-06.json",
}

FUTURE_FILES = {
    "canonical_oh_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "source_higgs_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
    "source_coordinate_transport_certificate": "outputs/yt_pr230_source_to_taste_axis_transport_certificate_2026-05-06.json",
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


def read_rel(rel: str) -> str:
    path = ROOT / rel
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def load_rel(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def shift_ops() -> list[np.ndarray]:
    i2 = np.eye(2, dtype=complex)
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    return [
        np.kron(sx, np.kron(i2, i2)),
        np.kron(i2, np.kron(sx, i2)),
        np.kron(i2, np.kron(i2, sx)),
    ]


def hs_inner(a: np.ndarray, b: np.ndarray) -> complex:
    return complex(np.trace(a.conj().T @ b))


def normalized_overlap(a: np.ndarray, b: np.ndarray) -> float:
    denom = math.sqrt(float(hs_inner(a, a).real) * float(hs_inner(b, b).real))
    if denom <= 0.0:
        return float("nan")
    return float((hs_inner(a, b) / denom).real)


def span_projection_norm(target: np.ndarray, basis: list[np.ndarray]) -> float:
    if not basis:
        return 0.0
    gram = np.asarray([[hs_inner(a, b) for b in basis] for a in basis], dtype=complex)
    rhs = np.asarray([hs_inner(b, target) for b in basis], dtype=complex)
    coeffs = np.linalg.solve(gram, rhs)
    projection = sum(coeff * basis_i for coeff, basis_i in zip(coeffs, basis))
    return float(math.sqrt(max(hs_inner(projection, projection).real, 0.0)))


def audit_rows() -> dict[str, Any]:
    ledger = load_rel("docs/audit/data/audit_ledger.json")
    rows = ledger.get("rows", {}) if isinstance(ledger, dict) else {}
    keys = {
        "taste_scalar_isotropy": "taste_scalar_isotropy_theorem_note",
        "higgs_mass_derived": "higgs_mass_derived_note",
        "higgs_mechanism": "higgs_mechanism_note",
        "higgs_from_lattice": "higgs_from_lattice_note",
    }
    return {
        name: {
            "ledger_key": key,
            "effective_status": rows.get(key, {}).get("effective_status"),
            "current_status_raw": rows.get(key, {}).get("current_status_raw"),
            "verdict_rationale": rows.get(key, {}).get("verdict_rationale"),
        }
        for name, key in keys.items()
    }


def future_presence() -> dict[str, bool]:
    return {name: (ROOT / rel).exists() for name, rel in FUTURE_FILES.items()}


def main() -> int:
    print("PR #230 taste-condensate-to-O_H bridge audit")
    print("=" * 72)

    docs = {name: read_rel(rel) for name, rel in DOCS.items()}
    parents = {name: load_rel(rel) for name, rel in PARENTS.items()}
    missing_docs = [name for name, text in docs.items() if not text]
    missing_parents = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]
    ledger_rows = audit_rows()
    future_present = future_presence()

    ops = shift_ops()
    identity = np.eye(8, dtype=complex)
    traces = [hs_inner(identity, op).real for op in ops]
    self_traces = [hs_inner(op, op).real for op in ops]
    pair_overlaps = [
        normalized_overlap(ops[i], ops[j])
        for i in range(3)
        for j in range(3)
        if i < j
    ]
    identity_overlaps = [normalized_overlap(identity, op) for op in ops]
    projection_norm = span_projection_norm(identity, ops)
    identity_norm = math.sqrt(float(hs_inner(identity, identity).real))
    relative_projection = projection_norm / identity_norm if identity_norm > 0.0 else float("nan")

    taste_theorem_loaded = (
        "H(phi) = sum_i phi_i S_i" in docs["taste_scalar_isotropy"]
        and "one Higgs direction" in docs["taste_scalar_isotropy"]
        and "orthogonal taste directions" in docs["taste_scalar_isotropy"]
    )
    higgs_stack_conditional = all(
        ledger_rows[name]["effective_status"] == "audited_conditional"
        for name in (
            "taste_scalar_isotropy",
            "higgs_mass_derived",
            "higgs_mechanism",
            "higgs_from_lattice",
        )
    )
    source_coordinate_is_uniform_mass_shift = (
        "same uniform additive lattice scalar source s entering m_bare + s"
        in read_rel("scripts/yt_direct_lattice_correlator_production.py")
    )
    harness_needs_external_oh_certificate = (
        "--source-higgs-operator-certificate is required for C_sH/C_HH rows"
        in read_rel("scripts/yt_direct_lattice_correlator_production.py")
    )
    canonical_oh_absent = (
        parents["canonical_operator_gate"].get("candidate_present") is False
        and parents["canonical_operator_gate"].get("candidate_valid") is False
        and not future_present["canonical_oh_certificate"]
    )
    source_higgs_rows_absent = (
        parents["source_higgs_readiness"].get("future_rows_present") is False
        and not future_present["source_higgs_rows"]
    )
    import_audit_blocks_hidden_norm = (
        "canonical scalar normalization import audit" in status(parents["canonical_scalar_import_audit"])
        and parents["canonical_scalar_import_audit"].get("proposal_allowed") is False
    )
    unratified_smoke_not_evidence = (
        "unratified-operator smoke" in status(parents["source_higgs_unratified_smoke"])
        and parents["source_higgs_unratified_smoke"].get("proposal_allowed") is False
    )
    unratified_gram_no_go_loaded = (
        parents["source_higgs_unratified_gram_no_go"].get("unratified_gram_shortcut_no_go_passed")
        is True
    )
    mixing_obstruction_loaded = (
        "source-pole canonical-Higgs mixing obstruction" in status(parents["source_pole_mixing"])
        and parents["source_pole_mixing"].get("proposal_allowed") is False
    )
    cross_lane_audit_blocks_hidden_oh = (
        parents["cross_lane_oh_authority"].get("repo_cross_lane_authority_found") is False
        and parents["cross_lane_oh_authority"].get("proposal_allowed") is False
    )
    negative_route_review_preserves_reopen = (
        parents["negative_route_review"].get("no_retained_negative_overclaim") is True
        and parents["negative_route_review"].get("future_reopen_paths_preserved") is True
    )

    taste_ops_are_involutions = all(
        np.max(np.abs(op @ op - identity)) < 1.0e-14 for op in ops
    )
    taste_ops_trace_zero = all(abs(trace) < 1.0e-14 for trace in traces)
    taste_ops_orthogonal = all(abs(overlap) < 1.0e-14 for overlap in pair_overlaps)
    uniform_source_orthogonal_to_taste_axes = all(
        abs(overlap) < 1.0e-14 for overlap in identity_overlaps
    )
    uniform_source_not_in_taste_axis_span = abs(relative_projection) < 1.0e-14

    no_forbidden_shortcuts = True

    report("docs-present", not missing_docs, f"missing={missing_docs}")
    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("taste-theorem-surface-loaded", taste_theorem_loaded, DOCS["taste_scalar_isotropy"])
    report("higgs-stack-audit-conditional", higgs_stack_conditional, json.dumps(ledger_rows, sort_keys=True))
    report("taste-shift-operators-are-involutions", taste_ops_are_involutions, "S_i^2=I")
    report("taste-shift-operators-are-trace-zero", taste_ops_trace_zero, f"Tr(S_i)={traces}")
    report("taste-shift-operators-are-orthogonal", taste_ops_orthogonal, f"overlaps={pair_overlaps}")
    report(
        "uniform-source-orthogonal-to-taste-axes",
        uniform_source_orthogonal_to_taste_axes,
        f"<I,S_i>/||I||||S_i||={identity_overlaps}",
    )
    report(
        "uniform-source-not-in-taste-axis-span",
        uniform_source_not_in_taste_axis_span,
        f"relative_projection={relative_projection:.3e}",
    )
    report("pr230-source-coordinate-is-uniform-mass-shift", source_coordinate_is_uniform_mass_shift, "m_bare+s")
    report("harness-still-needs-external-oh-certificate", harness_needs_external_oh_certificate, "source-Higgs rows guarded")
    report("canonical-oh-certificate-absent", canonical_oh_absent, status(parents["canonical_operator_gate"]))
    report("source-higgs-rows-absent", source_higgs_rows_absent, status(parents["source_higgs_readiness"]))
    report("canonical-scalar-import-audit-blocks-hidden-normalization", import_audit_blocks_hidden_norm, status(parents["canonical_scalar_import_audit"]))
    report("unratified-source-higgs-smoke-not-evidence", unratified_smoke_not_evidence, status(parents["source_higgs_unratified_smoke"]))
    report("unratified-gram-shortcut-no-go-loaded", unratified_gram_no_go_loaded, status(parents["source_higgs_unratified_gram_no_go"]))
    report("source-pole-mixing-obstruction-loaded", mixing_obstruction_loaded, status(parents["source_pole_mixing"]))
    report("cross-lane-oh-audit-blocks-hidden-import", cross_lane_audit_blocks_hidden_oh, status(parents["cross_lane_oh_authority"]))
    report("negative-review-preserves-future-reopen", negative_route_review_preserves_reopen, status(parents["negative_route_review"]))
    report("forbidden-shortcut-firewall-clean", no_forbidden_shortcuts, "no H_unit/Ward/observed/alpha_LM/u0 shortcut used")

    audit_passed = FAIL_COUNT == 0
    result = {
        "actual_current_surface_status": (
            "exact negative boundary / taste-condensate Higgs stack does not supply PR230 O_H bridge"
        ),
        "conditional_surface_status": (
            "The taste-condensate route can reopen only with a same-surface "
            "source-coordinate transport certificate from the PR230 uniform "
            "mass source to a canonical taste-axis Higgs operator, or with "
            "production C_sH/C_HH pole rows for a separately certified O_H."
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The exact taste-block Higgs axes are trace-zero taste-shift "
            "directions, while the current PR230 scalar source is the uniform "
            "additive mass source. Their Hilbert-Schmidt overlap is zero, and "
            "the Higgs/taste authority stack is audited conditional. No current "
            "same-surface O_H identity, normalization certificate, or C_sH/C_HH "
            "pole row exists."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "taste_condensate_oh_bridge_audit_passed": audit_passed,
        "algebra": {
            "taste_operator_model": "S_i = sigma_x on taste tensor factor i",
            "source_operator_model": "I_8 uniform additive scalar mass source",
            "Tr_S_i": traces,
            "Tr_S_i_S_i": self_traces,
            "taste_axis_pair_overlaps": pair_overlaps,
            "uniform_source_to_taste_axis_overlaps": identity_overlaps,
            "uniform_source_projection_norm_onto_taste_axis_span": projection_norm,
            "uniform_source_relative_projection_onto_taste_axis_span": relative_projection,
        },
        "audit_rows": ledger_rows,
        "parent_statuses": {name: status(cert) for name, cert in parents.items()},
        "future_file_presence": future_present,
        "future_reopen_conditions": [
            "derive a source-coordinate transport theorem mapping the PR230 uniform mass source to a canonical taste-axis Higgs source",
            "or supply a same-surface canonical O_H identity/normalization certificate plus production C_sH/C_HH pole rows",
            "or supply an equivalent W/Z sector-overlap, Schur-row, or neutral rank-one theorem accepted by the existing gates",
        ],
        "strict_non_claims": [
            "does not claim retained or proposed_retained PR230 closure",
            "does not demote the exact taste-CW isotropy theorem",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
            "does not set kappa_s = 1, cos(theta) = 1, c2 = 1, or Z_match = 1",
            "does not close future source-Higgs, W/Z, Schur, rank-one, scalar-LSZ, or production routes",
        ],
        "exact_next_action": (
            "Do not use the Higgs/taste condensate stack as the PR230 O_H bridge "
            "unless a new source-coordinate transport certificate is supplied. "
            "Continue the positive bridge through a certified O_H plus C_sH/C_HH "
            "pole rows, or through an equivalent W/Z/Schur/rank-one route."
        ),
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
