#!/usr/bin/env python3
"""
PR #230 kinetic taste-mixing bridge attempt.

Question:
    Can the current Wilson-staggered kinetic dynamics itself turn the PR230
    uniform additive mass source into a canonical taste/Higgs source row?

This is a hard-route check beyond the static source-coordinate no-go.  The
static no-go proves I_8 cannot be relabelled as a trace-zero taste axis by
unit-preserving, trace-preserving, or taste-equivariant maps.  This runner asks
whether the kinetic/transfer algebra can nevertheless produce a nonzero
same-surface C_sH row through dynamics.

Current-surface result:
    No.  On the source surface used by PR230, with no certified Higgs/taste
    background source switched on, the action and measure are invariant under
    independent taste flips.  The source operator is taste-even (I_8); the
    candidate taste-Higgs axes S_i are taste-odd.  Every taste-even transfer
    polynomial has zero Hilbert-Schmidt cross trace with one S_i insertion.
    A nonzero row requires a real symmetry-breaking background/source,
    canonical O_H certificate, or production C_sH/C_HH rows.
"""

from __future__ import annotations

import itertools
import json
import math
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_kinetic_taste_mixing_bridge_attempt_2026-05-06.json"

PARENTS = {
    "source_coordinate_transport_completion": (
        "outputs/yt_pr230_source_coordinate_transport_completion_attempt_2026-05-06.json"
    ),
    "taste_condensate_oh_bridge": (
        "outputs/yt_pr230_taste_condensate_oh_bridge_audit_2026-05-06.json"
    ),
    "canonical_higgs_operator_gate": (
        "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json"
    ),
    "source_higgs_production_readiness": (
        "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json"
    ),
    "holonomic_source_response_gate": (
        "outputs/yt_pr230_holonomic_source_response_feasibility_gate_2026-05-05.json"
    ),
    "full_positive_closure_assembly": (
        "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json"
    ),
    "retained_closure_route": (
        "outputs/yt_retained_closure_route_certificate_2026-05-01.json"
    ),
}

TEXTS = {
    "taste_scalar_isotropy": "docs/TASTE_SCALAR_ISOTROPY_THEOREM_NOTE.md",
    "minimal_axioms": "docs/MINIMAL_AXIOMS_2026-04-11.md",
    "production_harness": "scripts/yt_direct_lattice_correlator_production.py",
}

FUTURE_REOPEN_FILES = {
    "canonical_oh_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "source_higgs_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
    "source_to_taste_axis_transport_certificate": (
        "outputs/yt_pr230_source_to_taste_axis_transport_certificate_2026-05-06.json"
    ),
    "same_source_ew_action_certificate": (
        "outputs/yt_wz_same_source_ew_action_certificate_2026-05-04.json"
    ),
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


def taste_data() -> dict[str, Any]:
    i2 = np.eye(2, dtype=complex)
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)
    identity = np.eye(8, dtype=complex)
    axes = [kron3(sx, i2, i2), kron3(i2, sx, i2), kron3(i2, i2, sx)]
    flips = [kron3(sz, i2, i2), kron3(i2, sz, i2), kron3(i2, i2, sz)]
    return {"identity": identity, "axes": axes, "flips": flips}


def hs_inner(a: np.ndarray, b: np.ndarray) -> complex:
    return complex(np.trace(a.conj().T @ b))


def normalized_overlap(a: np.ndarray, b: np.ndarray) -> float:
    denom = math.sqrt(max(float(hs_inner(a, a).real * hs_inner(b, b).real), 0.0))
    if denom <= 1.0e-30:
        return float("nan")
    return float((hs_inner(a, b) / denom).real)


def is_flip_even(op: np.ndarray, flips: list[np.ndarray], tolerance: float = 1.0e-12) -> bool:
    return all(float(np.max(np.abs(flip @ op @ flip.conj().T - op))) < tolerance for flip in flips)


def pauli_word_basis() -> list[dict[str, Any]]:
    i2 = np.eye(2, dtype=complex)
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)
    local = {"I": i2, "X": sx, "Y": sy, "Z": sz}
    rows = []
    for labels in itertools.product(local, repeat=3):
        mat = kron3(local[labels[0]], local[labels[1]], local[labels[2]])
        rows.append({"label": "".join(labels), "matrix": mat})
    return rows


def deterministic_even_transfer(flips: list[np.ndarray]) -> np.ndarray:
    """A representative taste-even transfer polynomial.

    The concrete coefficients are arbitrary; the point is structural.  The
    operator is built by averaging a generic Hermitian matrix over the taste
    flip group, exactly the projection enforced by a taste-symmetric action.
    """

    rng = np.random.default_rng(230)
    raw = rng.normal(size=(8, 8)) + 1j * rng.normal(size=(8, 8))
    hermitian = 0.5 * (raw + raw.conj().T)
    group = []
    for bits in itertools.product([0, 1], repeat=len(flips)):
        op = np.eye(8, dtype=complex)
        for bit, flip in zip(bits, flips):
            if bit:
                op = op @ flip
        group.append(op)
    projected = sum(g @ hermitian @ g.conj().T for g in group) / len(group)
    return projected


def transfer_cross_rows(transfer: np.ndarray, axes: list[np.ndarray]) -> list[dict[str, float]]:
    identity = np.eye(8, dtype=complex)
    rows = []
    for i, axis in enumerate(axes):
        c_ss = hs_inner(identity, transfer @ identity @ transfer).real / 8.0
        c_sh = hs_inner(identity, transfer @ axis @ transfer).real / 8.0
        c_hh = hs_inner(axis, transfer @ axis @ transfer).real / 8.0
        rows.append(
            {
                "axis": i,
                "C_ss_proxy": float(c_ss),
                "C_sH_proxy": float(c_sh),
                "C_HH_proxy": float(c_hh),
                "normalized_C_sH": float(c_sh / math.sqrt(abs(c_ss * c_hh))) if c_ss * c_hh > 1.0e-30 else float("nan"),
            }
        )
    return rows


def forbidden_firewall() -> dict[str, bool]:
    return {
        "uses_hunit_matrix_element_readout": False,
        "uses_yt_ward_identity": False,
        "uses_observed_top_or_yukawa_targets": False,
        "uses_alpha_lm_plaquette_or_u0": False,
        "sets_source_higgs_overlap_to_one": False,
        "sets_kappa_c2_zmatch_or_cos_to_one": False,
        "claims_retained_or_proposed_retained": False,
    }


def main() -> int:
    print("PR #230 kinetic taste-mixing bridge attempt")
    print("=" * 72)

    parents = {name: load_rel(rel) for name, rel in PARENTS.items()}
    texts = {name: read_rel(rel) for name, rel in TEXTS.items()}
    missing_parents = [name for name, cert in parents.items() if not cert]
    missing_texts = [name for name, text in texts.items() if not text]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    parent_statuses = {name: status(cert) for name, cert in parents.items()}
    future_presence = {name: (ROOT / rel).exists() for name, rel in FUTURE_REOPEN_FILES.items()}

    taste = taste_data()
    identity = taste["identity"]
    axes = taste["axes"]
    flips = taste["flips"]
    basis = pauli_word_basis()
    even_words = [row for row in basis if is_flip_even(row["matrix"], flips)]
    odd_single_axis_words = [
        row
        for row in basis
        if any(
            float(np.max(np.abs(flip @ row["matrix"] @ flip.conj().T + row["matrix"]))) < 1.0e-12
            for flip in flips
        )
    ]
    transfer = deterministic_even_transfer(flips)
    cross_rows = transfer_cross_rows(transfer, axes)

    taste_theorem_loaded = (
        "H(phi) = sum_i phi_i S_i" in texts["taste_scalar_isotropy"]
        and "S_i^2 = I" in texts["taste_scalar_isotropy"]
        and "orthogonal taste directions" in texts["taste_scalar_isotropy"]
    )
    staggered_surface_loaded = (
        "staggered-Dirac partition" in texts["minimal_axioms"]
        and "Staggered Dirac operator" in texts["production_harness"]
        and "same uniform additive lattice scalar source s entering m_bare + s"
        in texts["production_harness"]
    )
    source_even = all(float(np.max(np.abs(flip @ identity @ flip.conj().T - identity))) < 1.0e-14 for flip in flips)
    axes_odd = all(
        float(np.max(np.abs(flips[i] @ axes[i] @ flips[i].conj().T + axes[i]))) < 1.0e-14
        for i in range(3)
    )
    source_axis_overlap_zero = all(abs(normalized_overlap(identity, axis)) < 1.0e-14 for axis in axes)
    even_transfer_commutes = is_flip_even(transfer, flips)
    cross_rows_zero = all(abs(row["C_sH_proxy"]) < 1.0e-12 for row in cross_rows)
    even_subalgebra_small = len(even_words) == 8
    odd_words_present_but_unsourced = len(odd_single_axis_words) > 0
    current_oh_absent = (
        parents["canonical_higgs_operator_gate"].get("candidate_valid") is False
        and not future_presence["canonical_oh_certificate"]
    )
    source_higgs_rows_absent = (
        parents["source_higgs_production_readiness"].get("future_rows_present") is False
        and not future_presence["source_higgs_rows"]
    )
    source_coordinate_shortcut_blocked = (
        "source-coordinate transport not derivable" in parent_statuses["source_coordinate_transport_completion"]
        and parents["source_coordinate_transport_completion"].get("proposal_allowed") is False
    )
    taste_condensate_shortcut_blocked = (
        "taste-condensate Higgs stack does not supply PR230 O_H bridge"
        in parent_statuses["taste_condensate_oh_bridge"]
        and parents["taste_condensate_oh_bridge"].get("proposal_allowed") is False
    )
    holonomic_boundary_loaded = (
        "missing current-surface O_H and h-source"
        in parent_statuses["holonomic_source_response_gate"]
        and parents["holonomic_source_response_gate"].get("proposal_allowed") is False
    )
    closure_still_open = (
        parents["full_positive_closure_assembly"].get("proposal_allowed") is False
        and parents["retained_closure_route"].get("proposal_allowed") is False
    )
    clean_firewall = all(value is False for value in forbidden_firewall().values())

    kinetic_bridge_closes = (
        source_even
        and axes_odd
        and even_transfer_commutes
        and not cross_rows_zero
        and current_oh_absent is False
        and source_higgs_rows_absent is False
        and clean_firewall
    )
    exact_negative_boundary_passed = (
        not missing_parents
        and not missing_texts
        and not proposal_allowed
        and taste_theorem_loaded
        and staggered_surface_loaded
        and source_even
        and axes_odd
        and source_axis_overlap_zero
        and even_transfer_commutes
        and cross_rows_zero
        and even_subalgebra_small
        and odd_words_present_but_unsourced
        and current_oh_absent
        and source_higgs_rows_absent
        and source_coordinate_shortcut_blocked
        and taste_condensate_shortcut_blocked
        and holonomic_boundary_loaded
        and closure_still_open
        and kinetic_bridge_closes is False
        and clean_firewall
    )

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("text-surfaces-present", not missing_texts, f"missing={missing_texts}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("taste-theorem-loaded", taste_theorem_loaded, TEXTS["taste_scalar_isotropy"])
    report("staggered-source-surface-loaded", staggered_surface_loaded, "uniform m_bare+s source")
    report("source-is-taste-even", source_even, "F_i I_8 F_i = I_8")
    report("taste-higgs-axes-are-taste-odd", axes_odd, "F_i S_i F_i = -S_i")
    report("source-axis-overlap-zero", source_axis_overlap_zero, "HS <I_8,S_i>=0")
    report("taste-even-transfer-proxy-built", even_transfer_commutes, "flip-averaged transfer")
    report("taste-even-cross-rows-vanish", cross_rows_zero, str(cross_rows))
    report("even-subalgebra-dimension-checked", even_subalgebra_small, f"even_words={len(even_words)}")
    report("odd-generators-exist-but-require-source", odd_words_present_but_unsourced, f"odd_words={len(odd_single_axis_words)}")
    report("canonical-oh-currently-absent", current_oh_absent, parent_statuses["canonical_higgs_operator_gate"])
    report("source-higgs-rows-currently-absent", source_higgs_rows_absent, parent_statuses["source_higgs_production_readiness"])
    report("source-coordinate-shortcut-blocked", source_coordinate_shortcut_blocked, parent_statuses["source_coordinate_transport_completion"])
    report("taste-condensate-shortcut-blocked", taste_condensate_shortcut_blocked, parent_statuses["taste_condensate_oh_bridge"])
    report("holonomic-boundary-loaded", holonomic_boundary_loaded, parent_statuses["holonomic_source_response_gate"])
    report("kinetic-taste-mixing-bridge-does-not-close", kinetic_bridge_closes is False, "taste-even dynamics gives C_sH=0")
    report("closure-still-open", closure_still_open, "assembly and retained route remain open")
    report("forbidden-firewall-clean", clean_firewall, str(forbidden_firewall()))
    report("exact-negative-boundary-passed", exact_negative_boundary_passed, "dynamic kinetic shortcut closed, future source-breaking routes preserved")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / current staggered kinetic taste symmetry "
            "does not supply the PR230 source-Higgs bridge"
        ),
        "conditional_surface_status": (
            "This does not rule out a future same-surface EW/Higgs action with "
            "a symmetry-breaking Higgs/taste background, a canonical O_H "
            "certificate, or production C_sH/C_HH rows.  It only blocks the "
            "shortcut that taste-even PR230 kinetic dynamics secretly mixes "
            "the uniform mass source into a trace-zero taste axis."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The uniform source is taste-even and the trace-zero taste-Higgs "
            "axes are taste-odd.  With no certified taste-breaking source or "
            "background, taste-flip symmetry forces the dynamic C_sH row to "
            "vanish for every taste-even transfer polynomial."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "kinetic_taste_mixing_bridge_closes_pr230": kinetic_bridge_closes,
        "exact_negative_boundary_passed": exact_negative_boundary_passed,
        "taste_symmetry_model": {
            "source_operator": "I_8",
            "higgs_axes": ["S_0=sigma_xII", "S_1=Isigma_xI", "S_2=IIsigma_x"],
            "taste_flips": ["F_0=sigma_zII", "F_1=Isigma_zI", "F_2=IIsigma_z"],
            "even_pauli_word_count": len(even_words),
            "odd_pauli_word_count": len(odd_single_axis_words),
            "source_axis_overlaps": [normalized_overlap(identity, axis) for axis in axes],
            "cross_rows_for_representative_even_transfer": cross_rows,
        },
        "parent_statuses": parent_statuses,
        "future_reopen_files": future_presence,
        "future_reopen_conditions": [
            "same-source EW/Higgs action with an explicit taste-breaking Higgs background/source",
            "canonical O_H identity and normalization certificate on the PR230 surface",
            "production C_ss/C_sH/C_HH rows with pole isolation and Gram purity",
            "or an equivalent neutral primitive/rank-one theorem that bypasses this trace-zero row",
        ],
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not define y_t_bare",
            "does not use H_unit or yt_ward_identity as proof authority",
            "does not use observed targets, alpha_LM, plaquette, or u0",
            "does not set source-Higgs overlap, kappa_s, c2, Z_match, or cos(theta) to one",
            "does not globally rule out first-principles O_H, W/Z response, Schur, or primitive-rank-one routes",
        ],
        "exact_next_action": (
            "Stop treating kinetic taste mixing as a hidden source-Higgs row. "
            "Move to a real symmetry-breaking artifact: same-source EW/Higgs "
            "action/O_H certificate, W/Z response packet, Schur A/B/C rows, or "
            "neutral primitive transfer."
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
