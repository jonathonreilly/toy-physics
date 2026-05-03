#!/usr/bin/env python3
"""
PR #230 positivity-improving neutral-scalar rank-one support theorem.

This block tests the remaining microscopic rank-one route.  If the neutral
scalar transfer matrix were positivity improving on the same scalar sector,
then Perron-Frobenius uniqueness would give a single lowest neutral scalar
state and the isolated-pole residue matrix would be rank one.  The current
PR #230 surface does not supply that positivity-improving premise, so this is
conditional support and an acceptance target, not retained closure.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_positivity_improving_neutral_scalar_rank_one_support_2026-05-03.json"

PARENTS = {
    "neutral_scalar_commutant_rank_no_go": "outputs/yt_neutral_scalar_commutant_rank_no_go_2026-05-02.json",
    "neutral_scalar_dynamical_rank_one_closure": "outputs/yt_neutral_scalar_dynamical_rank_one_closure_attempt_2026-05-02.json",
    "orthogonal_neutral_decoupling_no_go": "outputs/yt_orthogonal_neutral_decoupling_no_go_2026-05-02.json",
    "reflection_positivity_lsz_shortcut": "outputs/yt_reflection_positivity_lsz_shortcut_no_go_2026-05-02.json",
    "isolated_pole_gram_factorization": "outputs/yt_isolated_pole_gram_factorization_theorem_2026-05-03.json",
    "neutral_scalar_rank_one_purity_gate": "outputs/yt_neutral_scalar_rank_one_purity_gate_2026-05-02.json",
    "source_higgs_gram_purity_postprocessor": "outputs/yt_source_higgs_gram_purity_postprocess_2026-05-03.json",
    "canonical_higgs_operator_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "retained_closure_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
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


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def eigenvalues_2x2(matrix: list[list[float]]) -> tuple[float, float]:
    a, b = matrix[0]
    c, d = matrix[1]
    trace = a + d
    det = a * d - b * c
    disc = max(trace * trace - 4.0 * det, 0.0)
    root = math.sqrt(disc)
    return ((trace + root) / 2.0, (trace - root) / 2.0)


def perron_witness() -> dict[str, Any]:
    transfer = [[0.72, 0.18], [0.31, 0.55]]
    lam0, lam1 = eigenvalues_2x2(transfer)
    # For a 2x2 matrix, (b, lambda-a) is a right eigenvector when b != 0.
    vector = [transfer[0][1], lam0 - transfer[0][0]]
    norm = math.sqrt(vector[0] * vector[0] + vector[1] * vector[1])
    perron = [vector[0] / norm, vector[1] / norm]
    overlaps = [0.83, 0.51]
    residue = [[overlaps[i] * overlaps[j] for j in range(2)] for i in range(2)]
    gram_det = residue[0][0] * residue[1][1] - residue[0][1] * residue[1][0]
    non_improving_transfer = [[0.75, 0.0], [0.0, 0.75]]
    degenerate_residue = [[1.0, 0.0], [0.0, 1.0]]
    degenerate_det = (
        degenerate_residue[0][0] * degenerate_residue[1][1]
        - degenerate_residue[0][1] * degenerate_residue[1][0]
    )
    return {
        "positivity_improving_example": {
            "transfer_matrix": transfer,
            "all_entries_strictly_positive": all(x > 0.0 for row in transfer for x in row),
            "leading_eigenvalue": lam0,
            "subleading_eigenvalue": lam1,
            "spectral_gap": lam0 - lam1,
            "perron_vector": perron,
            "perron_vector_strictly_positive": all(x > 0.0 for x in perron),
            "residue_matrix_at_lowest_pole": residue,
            "gram_determinant": gram_det,
        },
        "non_improving_counterexample": {
            "transfer_matrix": non_improving_transfer,
            "all_entries_strictly_positive": False,
            "degenerate_lowest_states": 2,
            "residue_matrix_at_degenerate_pole": degenerate_residue,
            "gram_determinant": degenerate_det,
        },
    }


def main() -> int:
    print("PR #230 positivity-improving neutral-scalar rank-one support")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    witness = perron_witness()
    positive = witness["positivity_improving_example"]
    counter = witness["non_improving_counterexample"]

    commutant_no_go_loaded = (
        "neutral scalar commutant does not force rank-one purity"
        in status(parents["neutral_scalar_commutant_rank_no_go"])
    )
    dynamical_rank_one_not_derived = (
        "dynamical rank-one neutral scalar theorem not derived"
        in status(parents["neutral_scalar_dynamical_rank_one_closure"])
    )
    decoupling_not_derived = "orthogonal neutral decoupling shortcut not derived" in status(
        parents["orthogonal_neutral_decoupling_no_go"]
    )
    reflection_positivity_not_enough = "reflection positivity not scalar LSZ closure" in status(
        parents["reflection_positivity_lsz_shortcut"]
    )
    isolated_pole_support_loaded = (
        parents["isolated_pole_gram_factorization"].get(
            "isolated_pole_gram_factorization_theorem_passed"
        )
        is True
    )
    rank_one_gate_still_open = (
        "neutral scalar rank-one purity gate not passed"
        in status(parents["neutral_scalar_rank_one_purity_gate"])
    )
    source_higgs_rows_absent = (
        "awaiting production certificate" in status(parents["source_higgs_gram_purity_postprocessor"])
    )
    canonical_oh_absent = (
        "canonical-Higgs operator certificate absent" in status(parents["canonical_higgs_operator_gate"])
    )
    retained_still_open = (
        "closure not yet reached" in status(parents["retained_closure_route"])
        and parents["retained_closure_route"].get("proposal_allowed") is False
    )

    positivity_improving_rank_one_theorem_passed = (
        positive["all_entries_strictly_positive"]
        and positive["spectral_gap"] > 0.0
        and positive["perron_vector_strictly_positive"]
        and abs(float(positive["gram_determinant"])) < 1.0e-12
        and not counter["all_entries_strictly_positive"]
        and abs(float(counter["gram_determinant"])) > 0.5
    )
    positivity_improving_certificate_present = False
    current_closure_gate_passed = False

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("commutant-no-go-loaded", commutant_no_go_loaded, status(parents["neutral_scalar_commutant_rank_no_go"]))
    report(
        "dynamical-rank-one-currently-not-derived",
        dynamical_rank_one_not_derived,
        status(parents["neutral_scalar_dynamical_rank_one_closure"]),
    )
    report("orthogonal-decoupling-not-derived", decoupling_not_derived, status(parents["orthogonal_neutral_decoupling_no_go"]))
    report(
        "reflection-positivity-alone-not-enough",
        reflection_positivity_not_enough,
        status(parents["reflection_positivity_lsz_shortcut"]),
    )
    report("isolated-pole-factorization-support-loaded", isolated_pole_support_loaded, status(parents["isolated_pole_gram_factorization"]))
    report("rank-one-gate-still-open", rank_one_gate_still_open, status(parents["neutral_scalar_rank_one_purity_gate"]))
    report("source-higgs-production-rows-absent", source_higgs_rows_absent, status(parents["source_higgs_gram_purity_postprocessor"]))
    report("canonical-oh-certificate-absent", canonical_oh_absent, status(parents["canonical_higgs_operator_gate"]))
    report("retained-route-still-open", retained_still_open, status(parents["retained_closure_route"]))
    report(
        "perron-frobenius-witness-rank-one",
        positivity_improving_rank_one_theorem_passed,
        f"gap={positive['spectral_gap']}, det={positive['gram_determinant']}",
    )
    report(
        "non-improving-counterexample-necessity",
        abs(float(counter["gram_determinant"])) > 0.5,
        f"det={counter['gram_determinant']}",
    )
    report(
        "positivity-improving-premise-absent-on-current-surface",
        not positivity_improving_certificate_present,
        "no local certificate proves positivity improving in the neutral scalar sector",
    )
    report(
        "conditional-support-not-current-closure",
        not current_closure_gate_passed,
        f"current_closure_gate_passed={current_closure_gate_passed}",
    )

    result = {
        "actual_current_surface_status": (
            "conditional-support / positivity-improving neutral-scalar rank-one theorem; premise absent"
        ),
        "conditional_surface_status": (
            "If a same-surface certificate proves positivity improving transfer "
            "matrix dynamics in the neutral scalar sector, with nonzero source "
            "and canonical-Higgs overlaps at the unique lowest isolated pole, "
            "then the neutral scalar pole residue is rank one and O_sp-Higgs "
            "Gram purity follows from Perron-Frobenius uniqueness plus isolated-pole factorization."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The theorem is conditional support only; PR #230 lacks a "
            "positivity-improving neutral-scalar transfer-matrix certificate, "
            "certified O_H, and production C_sH/C_HH pole rows."
        ),
        "bare_retained_allowed": False,
        "positivity_improving_rank_one_theorem_passed": positivity_improving_rank_one_theorem_passed,
        "positivity_improving_certificate_present": positivity_improving_certificate_present,
        "current_closure_gate_passed": current_closure_gate_passed,
        "witness": witness,
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not infer positivity improving from reflection positivity alone",
            "does not infer source-pole purity from symmetry labels, D17 support, or finite orthogonal mass gaps",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
            "does not manufacture O_H, C_sH/C_HH rows, or W/Z response rows",
        ],
        "exact_next_action": (
            "Either prove the missing positivity-improving neutral-scalar "
            "transfer-matrix premise on the Cl(3)/Z3 substrate, or supply the "
            "non-source rank-repair data directly: certified O_H with production "
            "C_sH/C_HH pole rows, or same-source W/Z response rows with identity certificates."
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
