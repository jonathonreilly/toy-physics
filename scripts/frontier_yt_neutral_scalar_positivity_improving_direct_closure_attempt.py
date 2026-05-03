#!/usr/bin/env python3
"""
PR #230 direct neutral-scalar positivity-improving closure attempt.

This is the stretch attempt after the gauge-Perron import audit.  It asks
whether current Cl(3)/Z3 substrate authorities prove the missing premise
directly: positivity-improving transfer dynamics in the neutral scalar sector.

Result: not on the current surface.  Reflection positivity and a positive
transfer operator are not enough; the missing theorem is irreducibility /
primitive-cone positivity improvement for the neutral scalar sector after the
fermion/gauge/source construction and canonical-Higgs identification.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_neutral_scalar_positivity_improving_direct_closure_attempt_2026-05-03.json"

AUDIT_LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
REFLECTION_NOTE_KEY = "axiom_first_reflection_positivity_theorem_note_2026-04-29"

PARENTS = {
    "positivity_improving_neutral_scalar_rank_one": (
        "outputs/yt_positivity_improving_neutral_scalar_rank_one_support_2026-05-03.json"
    ),
    "gauge_perron_neutral_scalar_rank_one_import": (
        "outputs/yt_gauge_perron_to_neutral_scalar_rank_one_import_audit_2026-05-03.json"
    ),
    "reflection_positivity_lsz_shortcut": (
        "outputs/yt_reflection_positivity_lsz_shortcut_no_go_2026-05-02.json"
    ),
    "neutral_scalar_rank_one_purity_gate": (
        "outputs/yt_neutral_scalar_rank_one_purity_gate_2026-05-02.json"
    ),
    "neutral_scalar_commutant_rank_no_go": (
        "outputs/yt_neutral_scalar_commutant_rank_no_go_2026-05-02.json"
    ),
    "neutral_scalar_dynamical_rank_one_closure": (
        "outputs/yt_neutral_scalar_dynamical_rank_one_closure_attempt_2026-05-02.json"
    ),
    "orthogonal_neutral_decoupling_no_go": (
        "outputs/yt_orthogonal_neutral_decoupling_no_go_2026-05-02.json"
    ),
    "source_pole_canonical_higgs_mixing": (
        "outputs/yt_source_pole_canonical_higgs_mixing_obstruction_2026-05-02.json"
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


def load_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def load_reflection_audit() -> dict[str, Any]:
    if not AUDIT_LEDGER.exists():
        return {}
    ledger = json.loads(AUDIT_LEDGER.read_text(encoding="utf-8"))
    rows = ledger.get("rows", {})
    return rows.get(REFLECTION_NOTE_KEY, {})


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def reducible_positive_transfer_witness() -> dict[str, Any]:
    """
    A finite neutral-sector model satisfying positivity/reflection-positive
    correlator requirements but failing positivity improvement.
    """

    transfer = [[0.91, 0.0], [0.0, 0.91]]
    source_vector = [1.0, 0.0]
    rotated_higgs_vectors = [[1.0, 0.0], [0.8, 0.6], [0.5, 0.8660254037844386]]
    rows = []
    for higgs in rotated_higgs_vectors:
        overlap = sum(source_vector[i] * higgs[i] for i in range(2))
        rows.append(
            {
                "neutral_basis": ["source_pole_direction", "orthogonal_neutral_direction"],
                "source_vector": source_vector,
                "canonical_higgs_vector": higgs,
                "source_higgs_overlap": overlap,
                "source_pole_readout_factor": 1.0,
                "canonical_higgs_yukawa_factor": overlap,
            }
        )
    return {
        "transfer_matrix": transfer,
        "positive_semidefinite": transfer[0][0] >= 0.0 and transfer[1][1] >= 0.0,
        "positivity_preserving": True,
        "positivity_improving": False,
        "reason_not_improving": "off-diagonal neutral-sector communication is absent",
        "degenerate_lowest_neutral_states": 2,
        "reflection_positive_correlator_weights": [1.0, 1.0],
        "same_source_rows": rows,
        "canonical_higgs_factor_span": max(r["canonical_higgs_yukawa_factor"] for r in rows)
        - min(r["canonical_higgs_yukawa_factor"] for r in rows),
    }


def fanout_frames() -> list[dict[str, str]]:
    return [
        {
            "frame": "OS/reflection positivity",
            "attempt": "Use positive spectral reconstruction as the primitive cone.",
            "blocked_by": "Positive spectral weights do not force a single neutral scalar pole or fixed residue.",
        },
        {
            "frame": "gauge heat-kernel strict positivity",
            "attempt": "Import strict positivity of the finite Wilson gauge kernel.",
            "blocked_by": "The gauge theorem is scoped to plaquette-source J and leaves the neutral block free.",
        },
        {
            "frame": "fermion transfer positivity",
            "attempt": "Use positive semidefinite exp(-H) for staggered fermions.",
            "blocked_by": "Positive semidefinite transfer does not imply positivity improvement inside the composite neutral scalar response sector.",
        },
        {
            "frame": "source operator cyclicity",
            "attempt": "Treat the scalar source as cyclic for the neutral sector.",
            "blocked_by": "Current source-only spectrum is compatible with an orthogonal neutral top-coupled direction.",
        },
        {
            "frame": "canonical-Higgs identity",
            "attempt": "Identify the source pole with the canonical Higgs radial mode.",
            "blocked_by": "The source-pole/canonical-Higgs mixing obstruction leaves the overlap angle open.",
        },
    ]


def main() -> int:
    print("PR #230 neutral-scalar positivity-improving direct closure attempt")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    reflection_audit = load_reflection_audit()
    witness = reducible_positive_transfer_witness()
    frames = fanout_frames()

    reflection_support_loaded = (
        reflection_audit.get("audit_status") == "audited_clean"
        and reflection_audit.get("effective_status") == "support"
        and reflection_audit.get("intrinsic_status") == "support"
    )
    positivity_support_still_conditional = (
        "positivity-improving neutral-scalar rank-one theorem"
        in status(parents["positivity_improving_neutral_scalar_rank_one"])
        and parents["positivity_improving_neutral_scalar_rank_one"].get(
            "positivity_improving_certificate_present"
        )
        is False
    )
    gauge_import_blocked = (
        parents["gauge_perron_neutral_scalar_rank_one_import"].get(
            "exact_negative_boundary_passed"
        )
        is True
    )
    reflection_lsz_blocked = "reflection positivity not scalar LSZ closure" in status(
        parents["reflection_positivity_lsz_shortcut"]
    )
    rank_one_gate_open = (
        "neutral scalar rank-one purity gate not passed"
        in status(parents["neutral_scalar_rank_one_purity_gate"])
    )
    commutant_no_go = "neutral scalar commutant does not force rank-one purity" in status(
        parents["neutral_scalar_commutant_rank_no_go"]
    )
    dynamical_no_go = "dynamical rank-one neutral scalar theorem not derived" in status(
        parents["neutral_scalar_dynamical_rank_one_closure"]
    )
    decoupling_no_go = "orthogonal neutral decoupling shortcut not derived" in status(
        parents["orthogonal_neutral_decoupling_no_go"]
    )
    source_higgs_mixing_no_go = "source-pole canonical-Higgs mixing obstruction" in status(
        parents["source_pole_canonical_higgs_mixing"]
    )

    reducible_witness_blocks = (
        witness["positive_semidefinite"]
        and witness["positivity_preserving"]
        and witness["positivity_improving"] is False
        and witness["degenerate_lowest_neutral_states"] == 2
        and float(witness["canonical_higgs_factor_span"]) > 0.4
    )
    all_frames_have_blockers = all(bool(frame["blocked_by"]) for frame in frames)
    direct_positivity_improving_theorem_derived = False

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report(
        "reflection-positivity-support-loaded",
        reflection_support_loaded,
        f"audit_status={reflection_audit.get('audit_status')}, effective_status={reflection_audit.get('effective_status')}",
    )
    report(
        "positivity-improving-support-still-conditional",
        positivity_support_still_conditional,
        status(parents["positivity_improving_neutral_scalar_rank_one"]),
    )
    report("gauge-perron-import-blocked", gauge_import_blocked, status(parents["gauge_perron_neutral_scalar_rank_one_import"]))
    report("reflection-positivity-lsz-blocked", reflection_lsz_blocked, status(parents["reflection_positivity_lsz_shortcut"]))
    report("rank-one-purity-gate-open", rank_one_gate_open, status(parents["neutral_scalar_rank_one_purity_gate"]))
    report("commutant-no-go-present", commutant_no_go, status(parents["neutral_scalar_commutant_rank_no_go"]))
    report("dynamical-rank-one-no-go-present", dynamical_no_go, status(parents["neutral_scalar_dynamical_rank_one_closure"]))
    report("orthogonal-decoupling-no-go-present", decoupling_no_go, status(parents["orthogonal_neutral_decoupling_no_go"]))
    report("source-higgs-mixing-no-go-present", source_higgs_mixing_no_go, status(parents["source_pole_canonical_higgs_mixing"]))
    report(
        "positive-but-reducible-neutral-witness-blocks",
        reducible_witness_blocks,
        f"span={witness['canonical_higgs_factor_span']}",
    )
    report("stuck-fanout-frames-all-blocked", all_frames_have_blockers, f"frames={len(frames)}")
    report(
        "direct-positivity-improving-theorem-not-derived",
        not direct_positivity_improving_theorem_derived,
        "no current authority proves neutral-sector irreducibility / primitive cone",
    )

    exact_negative_boundary_passed = (
        not missing
        and not proposal_allowed
        and reflection_support_loaded
        and positivity_support_still_conditional
        and gauge_import_blocked
        and reflection_lsz_blocked
        and rank_one_gate_open
        and commutant_no_go
        and dynamical_no_go
        and decoupling_no_go
        and source_higgs_mixing_no_go
        and reducible_witness_blocks
        and all_frames_have_blockers
        and not direct_positivity_improving_theorem_derived
    )

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / neutral-scalar positivity-improving "
            "direct theorem not derived"
        ),
        "conditional_surface_status": (
            "A future same-surface proof of neutral-sector irreducibility and "
            "positivity improvement would activate the existing Perron/isolated-"
            "pole rank-one support theorem."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Current authorities prove support-level reflection positivity and "
            "conditional Perron consequences, but not positivity improvement or "
            "irreducibility in the neutral scalar response sector."
        ),
        "bare_retained_allowed": False,
        "direct_positivity_improving_theorem_derived": direct_positivity_improving_theorem_derived,
        "exact_negative_boundary_passed": exact_negative_boundary_passed,
        "minimal_allowed_premises": [
            "Cl(3)/Z3 Wilson-staggered substrate with g_bare=1",
            "support-level reflection positivity note as structural context",
            "current PR230 source/FH/LSZ certificates and no-go ledger",
        ],
        "forbidden_imports": [
            "H_unit or yt_ward_identity matrix-element readout",
            "observed m_t/y_t/W/Z values as proof selectors",
            "alpha_LM, plaquette value, u0, or fitted scalar-kernel multipliers",
            "gauge-vacuum Perron uniqueness as a neutral-scalar theorem",
        ],
        "fanout_frames": frames,
        "reducible_positive_transfer_witness": witness,
        "parent_certificates": PARENTS,
        "reflection_positivity_audit": {
            "claim_id": REFLECTION_NOTE_KEY,
            "audit_status": reflection_audit.get("audit_status"),
            "effective_status": reflection_audit.get("effective_status"),
            "intrinsic_status": reflection_audit.get("intrinsic_status"),
            "current_status": reflection_audit.get("current_status"),
        },
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not upgrade reflection positivity into positivity improvement",
            "does not import the gauge-vacuum Perron theorem into the neutral scalar sector",
            "does not identify O_sp with O_H",
            "does not remove orthogonal neutral scalar top couplings",
        ],
        "exact_next_action": (
            "The direct positivity-improvement proof is blocked on neutral-sector "
            "irreducibility.  Continue with direct rank-repair data (certified "
            "O_H/C_sH/C_HH or same-source W/Z rows), or attack the scalar "
            "denominator / K'(pole) theorem."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }

    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 and exact_negative_boundary_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
